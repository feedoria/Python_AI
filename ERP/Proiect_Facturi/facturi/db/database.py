# -*- coding: utf-8 -*-
import os
import sqlite3
import threading

from ERP.Proiect_Facturi.facturi.constants import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS invoices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numar_factura TEXT NOT NULL,
    furnizor TEXT NOT NULL,
    data_factura TEXT NOT NULL,
    categorie TEXT,
    suma_fara_tva REAL NOT NULL DEFAULT 0,
    tva REAL NOT NULL DEFAULT 0,
    suma_totala REAL NOT NULL DEFAULT 0,
    moneda TEXT NOT NULL DEFAULT 'RON',
    stare TEXT NOT NULL DEFAULT 'Neplătită',
    observatii TEXT,
    data_creare TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_invoices_data ON invoices(data_factura);
CREATE INDEX IF NOT EXISTS idx_invoices_furnizor ON invoices(furnizor);
CREATE INDEX IF NOT EXISTS idx_invoices_categorie ON invoices(categorie);
CREATE INDEX IF NOT EXISTS idx_invoices_stare ON invoices(stare);
CREATE INDEX IF NOT EXISTS idx_invoices_numar ON invoices(numar_factura);
"""

# sqlite3 nu permite folosirea aceleiași conexiuni din alt thread decât cel
# în care a fost creată — importul și exportul rulează pe QThread-uri separate,
# așa că fiecare thread primește propria conexiune (WAL permite acest lucru).
_local = threading.local()


def get_connection():
    conn = getattr(_local, "connection", None)
    if conn is None:
        db_dir = os.path.dirname(DB_PATH)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir, exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        conn.execute("PRAGMA foreign_keys=ON;")
        conn.execute("PRAGMA busy_timeout=5000;")
        conn.executescript(SCHEMA)
        conn.commit()
        _local.connection = conn
    return conn


def close_connection():
    conn = getattr(_local, "connection", None)
    if conn is not None:
        conn.close()
        _local.connection = None
