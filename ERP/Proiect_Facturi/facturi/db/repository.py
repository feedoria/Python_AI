# -*- coding: utf-8 -*-
from ERP.Proiect_Facturi.facturi.db.database import get_connection

COLUMNS = [
    "id",
    "numar_factura",
    "furnizor",
    "data_factura",
    "categorie",
    "suma_fara_tva",
    "tva",
    "suma_totala",
    "moneda",
    "stare",
    "observatii",
]

EDITABLE_FIELDS = [c for c in COLUMNS if c != "id"]


def _build_where(filters):
    """Construiește o clauză WHERE parametrizată din dicționarul de filtre.

    filters poate conține: text, date_from, date_to, categorie, stare
    """
    clauses = []
    params = []

    if filters:
        text = (filters.get("text") or "").strip()
        if text:
            clauses.append("(numar_factura LIKE ? OR furnizor LIKE ? OR observatii LIKE ?)")
            like = f"%{text}%"
            params.extend([like, like, like])

        date_from = filters.get("date_from")
        if date_from:
            clauses.append("data_factura >= ?")
            params.append(date_from)

        date_to = filters.get("date_to")
        if date_to:
            clauses.append("data_factura <= ?")
            params.append(date_to)

        categorie = filters.get("categorie")
        if categorie:
            clauses.append("categorie = ?")
            params.append(categorie)

        stare = filters.get("stare")
        if stare:
            clauses.append("stare = ?")
            params.append(stare)

    where_sql = (" WHERE " + " AND ".join(clauses)) if clauses else ""
    return where_sql, params


def add_invoice(data: dict) -> int:
    conn = get_connection()
    fields = [f for f in EDITABLE_FIELDS if f in data]
    placeholders = ", ".join("?" for _ in fields)
    sql = f"INSERT INTO invoices ({', '.join(fields)}) VALUES ({placeholders})"
    cur = conn.execute(sql, [data[f] for f in fields])
    conn.commit()
    return cur.lastrowid


def update_invoice(invoice_id: int, data: dict):
    conn = get_connection()
    fields = [f for f in EDITABLE_FIELDS if f in data]
    set_sql = ", ".join(f"{f} = ?" for f in fields)
    sql = f"UPDATE invoices SET {set_sql} WHERE id = ?"
    conn.execute(sql, [data[f] for f in fields] + [invoice_id])
    conn.commit()


def delete_invoices(ids: list):
    if not ids:
        return
    conn = get_connection()
    placeholders = ", ".join("?" for _ in ids)
    conn.execute(f"DELETE FROM invoices WHERE id IN ({placeholders})", ids)
    conn.commit()


def get_invoice(invoice_id: int) -> dict:
    conn = get_connection()
    row = conn.execute("SELECT * FROM invoices WHERE id = ?", (invoice_id,)).fetchone()
    return dict(row) if row else None


def count_filtered(filters=None) -> int:
    conn = get_connection()
    where_sql, params = _build_where(filters)
    row = conn.execute(f"SELECT COUNT(*) AS c FROM invoices{where_sql}", params).fetchone()
    return row["c"]


def fetch_page(filters=None, order_by="data_factura", order_dir="DESC", offset=0, limit=500):
    conn = get_connection()
    where_sql, params = _build_where(filters)
    if order_by not in COLUMNS:
        order_by = "data_factura"
    order_dir = "DESC" if str(order_dir).upper() == "DESC" else "ASC"
    sql = (
        f"SELECT {', '.join(COLUMNS)} FROM invoices{where_sql} "
        f"ORDER BY {order_by} {order_dir}, id {order_dir} LIMIT ? OFFSET ?"
    )
    rows = conn.execute(sql, params + [limit, offset]).fetchall()
    return [dict(r) for r in rows]


def bulk_insert(rows: list, batch_size: int = 2000, progress_callback=None):
    """Inserează în tranzacție, în batch-uri. rows: listă de dict-uri."""
    conn = get_connection()
    total = len(rows)
    inserted = 0
    fields = EDITABLE_FIELDS
    placeholders = ", ".join("?" for _ in fields)
    sql = f"INSERT INTO invoices ({', '.join(fields)}) VALUES ({placeholders})"

    conn.execute("BEGIN")
    try:
        for start in range(0, total, batch_size):
            batch = rows[start:start + batch_size]
            values = [[r.get(f) for f in fields] for r in batch]
            conn.executemany(sql, values)
            inserted += len(batch)
            if progress_callback:
                progress_callback(inserted, total)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    return inserted


def distinct_categories() -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT categorie FROM invoices WHERE categorie IS NOT NULL AND categorie != '' "
        "ORDER BY categorie"
    ).fetchall()
    return [r["categorie"] for r in rows]


def distinct_furnizori() -> list:
    conn = get_connection()
    rows = conn.execute(
        "SELECT DISTINCT furnizor FROM invoices WHERE furnizor IS NOT NULL AND furnizor != '' "
        "ORDER BY furnizor"
    ).fetchall()
    return [r["furnizor"] for r in rows]


def total_sum(filters=None) -> float:
    conn = get_connection()
    where_sql, params = _build_where(filters)
    row = conn.execute(
        f"SELECT COALESCE(SUM(suma_totala), 0) AS s FROM invoices{where_sql}", params
    ).fetchone()
    return row["s"] or 0.0


def stats_by_category(filters=None, limit=10) -> list:
    conn = get_connection()
    where_sql, params = _build_where(filters)
    sql = (
        f"SELECT COALESCE(NULLIF(categorie, ''), 'Fără categorie') AS categorie, "
        f"SUM(suma_totala) AS suma FROM invoices{where_sql} "
        f"GROUP BY categorie ORDER BY suma DESC LIMIT ?"
    )
    rows = conn.execute(sql, params + [limit]).fetchall()
    return [(r["categorie"], r["suma"]) for r in rows]


def stats_by_month(filters=None, months: int = 12) -> list:
    conn = get_connection()
    where_sql, params = _build_where(filters)
    sql = (
        f"SELECT substr(data_factura, 1, 7) AS luna, SUM(suma_totala) AS suma "
        f"FROM invoices{where_sql} GROUP BY luna ORDER BY luna DESC LIMIT ?"
    )
    rows = conn.execute(sql, params + [months]).fetchall()
    result = [(r["luna"], r["suma"]) for r in rows]
    result.reverse()
    return result
