# -*- coding: utf-8 -*-
import csv

import pandas as pd

from ERP.Proiect_Facturi.facturi.constants import STARE_NEPLATITA
from ERP.Proiect_Facturi.facturi.db.repository import EDITABLE_FIELDS

# alias-uri posibile de coloane (comparate case-insensitive, fără diacritice/spații) -> câmp canonic
COLUMN_ALIASES = {
    "numar_factura": ["numarfactura", "nrfactura", "numar", "nr", "invoicenumber", "numarfactura*"],
    "furnizor": ["furnizor", "supplier", "vendor"],
    "data_factura": ["datafactura", "data", "date", "invoicedate"],
    "categorie": ["categorie", "category", "categoriecheltuiala"],
    "suma_fara_tva": ["sumafaratva", "sumafarat.v.a", "bazaimpozabila", "net", "subtotal"],
    "tva": ["tva", "vat", "tax"],
    "suma_totala": ["sumatotala", "total", "totalgeneral", "sumatotal"],
    "moneda": ["moneda", "currency", "valuta"],
    "stare": ["stare", "status", "stareplata"],
    "observatii": ["observatii", "note", "notes", "comentarii", "obs"],
}


def _normalize_header(name: str) -> str:
    name = str(name).strip().lower()
    replacements = {
        "ă": "a", "â": "a", "î": "i", "ș": "s", "ş": "s", "ț": "t", "ţ": "t",
    }
    for src, dst in replacements.items():
        name = name.replace(src, dst)
    return "".join(ch for ch in name if ch.isalnum())


def _detect_delimiter(path: str, encoding: str) -> str:
    with open(path, "r", encoding=encoding, newline="") as f:
        sample = f.read(4096)
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t").delimiter
    except csv.Error:
        return ","


def read_file(path: str, nrows: int = None) -> pd.DataFrame:
    if path.lower().endswith(".csv"):
        encoding = "utf-8-sig"
        try:
            with open(path, "r", encoding=encoding) as f:
                while f.read(65536):
                    pass
        except UnicodeDecodeError:
            encoding = "latin-1"
        delimiter = _detect_delimiter(path, encoding)
        return pd.read_csv(
            path, encoding=encoding, dtype=str, keep_default_na=False, nrows=nrows, sep=delimiter
        )
    return pd.read_excel(path, dtype=str, nrows=nrows)


def auto_map_columns(columns) -> dict:
    normalized = {_normalize_header(c): c for c in columns}
    mapping = {}
    for field, aliases in COLUMN_ALIASES.items():
        found = None
        for alias in aliases:
            if alias in normalized:
                found = normalized[alias]
                break
        mapping[field] = found
    return mapping


def _parse_date(value) -> str:
    if value is None or str(value).strip() == "":
        return ""
    try:
        return pd.to_datetime(str(value), dayfirst=False).strftime("%Y-%m-%d")
    except (ValueError, TypeError):
        try:
            return pd.to_datetime(str(value), dayfirst=True).strftime("%Y-%m-%d")
        except (ValueError, TypeError):
            return ""


def _parse_number(value) -> float:
    if value is None:
        return 0.0
    s = str(value).strip().replace(" ", "")
    if s == "":
        return 0.0
    if "," in s and "." in s:
        # separatorul care apare ultimul e cel zecimal (ex: "1.234,56" RO vs "1,234.56" US)
        if s.rfind(",") > s.rfind("."):
            s = s.replace(".", "").replace(",", ".")
        else:
            s = s.replace(",", "")
    else:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return 0.0


def build_rows(df: pd.DataFrame, mapping: dict):
    """Transformă DataFrame-ul brut în rânduri gata de inserat, folosind maparea de coloane.

    Returnează (rows, errors) unde errors e o listă de mesaje pentru rânduri invalide (lipsă câmpuri obligatorii).
    """
    rows = []
    errors = []

    for i, record in enumerate(df.to_dict(orient="records")):
        row = {f: "" for f in EDITABLE_FIELDS}
        for field, source_col in mapping.items():
            if source_col and source_col in record:
                row[field] = record[source_col]

        numar = str(row.get("numar_factura") or "").strip()
        furnizor = str(row.get("furnizor") or "").strip()
        if not numar or not furnizor:
            errors.append(f"Rând {i + 2}: lipsește numărul facturii sau furnizorul — a fost ignorat.")
            continue

        data_factura = _parse_date(row.get("data_factura"))
        suma_fara_tva = _parse_number(row.get("suma_fara_tva"))
        tva = _parse_number(row.get("tva"))
        suma_totala = _parse_number(row.get("suma_totala"))
        if suma_totala == 0 and (suma_fara_tva or tva):
            suma_totala = round(suma_fara_tva + tva, 2)

        rows.append({
            "numar_factura": numar,
            "furnizor": furnizor,
            "data_factura": data_factura or pd.Timestamp.today().strftime("%Y-%m-%d"),
            "categorie": str(row.get("categorie") or "").strip(),
            "suma_fara_tva": suma_fara_tva,
            "tva": tva,
            "suma_totala": suma_totala,
            "moneda": str(row.get("moneda") or "RON").strip() or "RON",
            "stare": str(row.get("stare") or STARE_NEPLATITA).strip() or STARE_NEPLATITA,
            "observatii": str(row.get("observatii") or "").strip(),
        })

    return rows, errors
