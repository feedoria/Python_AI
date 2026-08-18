# -*- coding: utf-8 -*-
from PyQt6.QtCore import QAbstractTableModel, QModelIndex, Qt
from PyQt6.QtGui import QColor

from constants import PAGE_SIZE, STARE_PLATITA
from db import repository

HEADERS = {
    "id": "ID",
    "numar_factura": "Nr. factură",
    "furnizor": "Furnizor",
    "data_factura": "Data",
    "categorie": "Categorie",
    "suma_fara_tva": "Sumă fără TVA",
    "tva": "TVA",
    "suma_totala": "Sumă totală",
    "moneda": "Monedă",
    "stare": "Stare",
    "observatii": "Observații",
}

MONEY_COLUMNS = {"suma_fara_tva", "tva", "suma_totala"}


class InvoiceTableModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.columns = repository.COLUMNS
        self.filters = {}
        self.order_by = "data_factura"
        self.order_dir = "DESC"
        self._rows = []
        self._total_count = 0

    # --- API public ---

    def set_filters(self, filters: dict):
        self.filters = filters or {}
        self.reload()

    def set_sort(self, column_name: str, order_dir: str = "DESC"):
        self.order_by = column_name
        self.order_dir = order_dir
        self.reload()

    def reload(self):
        self.beginResetModel()
        self._rows = []
        self._total_count = repository.count_filtered(self.filters)
        self.endResetModel()
        if self._total_count > 0:
            self.fetchMore(QModelIndex())

    def total_count(self) -> int:
        return self._total_count

    def loaded_count(self) -> int:
        return len(self._rows)

    def row_dict(self, row: int) -> dict:
        if 0 <= row < len(self._rows):
            return self._rows[row]
        return None

    def invoice_id(self, row: int):
        d = self.row_dict(row)
        return d["id"] if d else None

    # --- QAbstractTableModel ---

    def rowCount(self, parent=QModelIndex()):
        if parent.isValid():
            return 0
        return len(self._rows)

    def columnCount(self, parent=QModelIndex()):
        return len(self.columns)

    def canFetchMore(self, parent=QModelIndex()):
        if parent.isValid():
            return False
        return len(self._rows) < self._total_count

    def fetchMore(self, parent=QModelIndex()):
        remaining = self._total_count - len(self._rows)
        to_fetch = min(PAGE_SIZE, remaining)
        if to_fetch <= 0:
            return
        new_rows = repository.fetch_page(
            self.filters,
            order_by=self.order_by,
            order_dir=self.order_dir,
            offset=len(self._rows),
            limit=to_fetch,
        )
        self.beginInsertRows(QModelIndex(), len(self._rows), len(self._rows) + len(new_rows) - 1)
        self._rows.extend(new_rows)
        self.endInsertRows()

    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None
        row = self._rows[index.row()]
        col_name = self.columns[index.column()]
        value = row.get(col_name)

        if role == Qt.ItemDataRole.DisplayRole:
            if col_name in MONEY_COLUMNS and value is not None:
                return f"{value:,.2f}".replace(",", " ")
            return value if value is not None else ""

        if role == Qt.ItemDataRole.TextAlignmentRole:
            if col_name in MONEY_COLUMNS:
                return Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

        if role == Qt.ItemDataRole.ForegroundRole and col_name == "stare":
            if value == STARE_PLATITA:
                return QColor("#1a7f37")
            return QColor("#c0392b")

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role != Qt.ItemDataRole.DisplayRole:
            return None
        if orientation == Qt.Orientation.Horizontal:
            return HEADERS.get(self.columns[section], self.columns[section])
        return str(section + 1)
