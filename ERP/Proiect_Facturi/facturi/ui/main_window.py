# -*- coding: utf-8 -*-
from PyQt6.QtCore import QDate, QThread, Qt, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QAbstractItemView,
    QCheckBox,
    QComboBox,
    QDateEdit,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QProgressDialog,
    QPushButton,
    QSplitter,
    QStatusBar,
    QTableView,
    QToolBar,
    QVBoxLayout,
    QWidget,
)

from ERP.Proiect_Facturi.facturi.constants import CATEGORII_IMPLICITE, STARI
from ERP.Proiect_Facturi.facturi.db import repository
from ERP.Proiect_Facturi.facturi.models.invoice_table_model import InvoiceTableModel
from ERP.Proiect_Facturi.facturi.services import exporter
from ERP.Proiect_Facturi.facturi.ui.import_dialog import ImportDialog
from ERP.Proiect_Facturi.facturi.ui.invoice_dialog import InvoiceDialog

TOATE_CATEGORIILE = "Toate categoriile"
TOATE_STARILE = "Toate stările"

SORTABLE_COLUMNS = repository.COLUMNS


class ExportWorker(QThread):
    finished_ok = pyqtSignal(int)
    failed = pyqtSignal(str)

    def __init__(self, path, filters):
        super().__init__()
        self.path = path
        self.filters = filters

    def run(self):
        try:
            count = exporter.export(self.path, self.filters)
            self.finished_ok.emit(count)
        except Exception as exc:
            self.failed.emit(str(exc))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Gestiune Facturi")
        self.resize(1420, 860)

        self.model = InvoiceTableModel()
        self._sort_column = "data_factura"
        self._sort_dir = "DESC"
        self.export_worker = None

        self._build_toolbar()
        self._build_central_widget()
        self._build_statusbar()

        self._reload_categories()
        self._apply_filters()

    # --- construcție UI ---

    def _build_toolbar(self):
        toolbar = QToolBar("Acțiuni")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        self.action_add = QAction("➕ Adaugă factură", self)
        self.action_add.triggered.connect(self._on_add)
        toolbar.addAction(self.action_add)

        self.action_edit = QAction("✏️ Editează", self)
        self.action_edit.triggered.connect(self._on_edit)
        self.action_edit.setEnabled(False)
        toolbar.addAction(self.action_edit)

        self.action_delete = QAction("🗑️ Șterge", self)
        self.action_delete.triggered.connect(self._on_delete)
        self.action_delete.setEnabled(False)
        toolbar.addAction(self.action_delete)

        toolbar.addSeparator()

        self.action_import = QAction("⭳ Import Excel/CSV", self)
        self.action_import.triggered.connect(self._on_import)
        toolbar.addAction(self.action_import)

        self.action_export = QAction("⭱ Export Excel/CSV", self)
        self.action_export.triggered.connect(self._on_export)
        toolbar.addAction(self.action_export)

        toolbar.addSeparator()

        self.action_refresh = QAction("⟳ Reîmprospătează", self)
        self.action_refresh.triggered.connect(self._reload_all)
        toolbar.addAction(self.action_refresh)

    def _build_central_widget(self):
        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        layout.addWidget(self._build_filter_bar())

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._build_table())

        from ERP.Proiect_Facturi.facturi.ui.stats_panel import StatsPanel
        self.stats_panel = StatsPanel()
        splitter.addWidget(self.stats_panel)
        splitter.setStretchFactor(0, 3)
        splitter.setStretchFactor(1, 1)
        layout.addWidget(splitter, 1)

        self.setCentralWidget(central)

    def _build_filter_bar(self):
        bar = QWidget()
        bar.setObjectName("filterBar")
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(10)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Caută după nr. factură, furnizor, observații...")
        self.search_edit.returnPressed.connect(self._apply_filters)
        layout.addWidget(self.search_edit, 2)

        self.date_filter_check = QCheckBox("Interval date")
        self.date_filter_check.stateChanged.connect(self._on_date_filter_toggled)
        layout.addWidget(self.date_filter_check)

        self.date_from = QDateEdit()
        self.date_from.setCalendarPopup(True)
        self.date_from.setDisplayFormat("yyyy-MM-dd")
        self.date_from.setDate(QDate.currentDate().addMonths(-1))
        self.date_from.setEnabled(False)
        layout.addWidget(self.date_from)

        layout.addWidget(QLabel("–"))

        self.date_to = QDateEdit()
        self.date_to.setCalendarPopup(True)
        self.date_to.setDisplayFormat("yyyy-MM-dd")
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setEnabled(False)
        layout.addWidget(self.date_to)

        self.categorie_combo = QComboBox()
        self.categorie_combo.addItem(TOATE_CATEGORIILE)
        layout.addWidget(self.categorie_combo)

        self.stare_combo = QComboBox()
        self.stare_combo.addItem(TOATE_STARILE)
        self.stare_combo.addItems(STARI)
        layout.addWidget(self.stare_combo)

        filter_btn = QPushButton("Filtrează")
        filter_btn.setObjectName("primaryButton")
        filter_btn.clicked.connect(self._apply_filters)
        layout.addWidget(filter_btn)

        reset_btn = QPushButton("Resetează")
        reset_btn.clicked.connect(self._reset_filters)
        layout.addWidget(reset_btn)

        return bar

    def _build_table(self):
        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnHidden(0, True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().sectionClicked.connect(self._on_header_clicked)
        self.table.doubleClicked.connect(self._on_edit)
        self.table.selectionModel().selectionChanged.connect(self._on_selection_changed)
        return self.table

    def _build_statusbar(self):
        self.status = QStatusBar()
        self.setStatusBar(self.status)

    # --- filtre ---

    def _on_date_filter_toggled(self, state):
        enabled = self.date_filter_check.isChecked()
        self.date_from.setEnabled(enabled)
        self.date_to.setEnabled(enabled)

    def _reload_categories(self):
        current = self.categorie_combo.currentText()
        self.categorie_combo.blockSignals(True)
        self.categorie_combo.clear()
        self.categorie_combo.addItem(TOATE_CATEGORIILE)
        categories = sorted(set(CATEGORII_IMPLICITE) | set(repository.distinct_categories()))
        self.categorie_combo.addItems(categories)
        idx = self.categorie_combo.findText(current)
        self.categorie_combo.setCurrentIndex(idx if idx >= 0 else 0)
        self.categorie_combo.blockSignals(False)

    def _current_filters(self) -> dict:
        filters = {}
        text = self.search_edit.text().strip()
        if text:
            filters["text"] = text
        if self.date_filter_check.isChecked():
            filters["date_from"] = self.date_from.date().toString("yyyy-MM-dd")
            filters["date_to"] = self.date_to.date().toString("yyyy-MM-dd")
        if self.categorie_combo.currentText() != TOATE_CATEGORIILE:
            filters["categorie"] = self.categorie_combo.currentText()
        if self.stare_combo.currentText() != TOATE_STARILE:
            filters["stare"] = self.stare_combo.currentText()
        return filters

    def _apply_filters(self):
        filters = self._current_filters()
        self.model.set_filters(filters)
        self.stats_panel.refresh(filters)
        self._update_status()

    def _reset_filters(self):
        self.search_edit.clear()
        self.date_filter_check.setChecked(False)
        self.categorie_combo.setCurrentIndex(0)
        self.stare_combo.setCurrentIndex(0)
        self._apply_filters()

    def _reload_all(self):
        self._reload_categories()
        self._apply_filters()

    def _on_header_clicked(self, logical_index):
        column_name = SORTABLE_COLUMNS[logical_index]
        if column_name == "id":
            return
        if self._sort_column == column_name:
            self._sort_dir = "ASC" if self._sort_dir == "DESC" else "DESC"
        else:
            self._sort_column = column_name
            self._sort_dir = "ASC"
        order = Qt.SortOrder.AscendingOrder if self._sort_dir == "ASC" else Qt.SortOrder.DescendingOrder
        self.table.horizontalHeader().setSortIndicator(logical_index, order)
        self.table.horizontalHeader().setSortIndicatorShown(True)
        self.model.set_sort(self._sort_column, self._sort_dir)
        self._update_status()

    def _on_selection_changed(self):
        rows = self._selected_rows()
        self.action_edit.setEnabled(len(rows) == 1)
        self.action_delete.setEnabled(len(rows) >= 1)

    def _selected_rows(self):
        return sorted({idx.row() for idx in self.table.selectionModel().selectedRows()})

    def _update_status(self):
        loaded = self.model.loaded_count()
        total = self.model.total_count()
        total_sum = repository.total_sum(self.model.filters)
        self.status.showMessage(
            f"{loaded} din {total} facturi afișate    •    Sumă totală (filtrat): {total_sum:,.2f}".replace(",", " ")
        )

    # --- acțiuni CRUD ---

    def _on_add(self):
        dialog = InvoiceDialog(
            self, furnizori=repository.distinct_furnizori(), categorii=repository.distinct_categories()
        )
        if dialog.exec():
            repository.add_invoice(dialog.get_data())
            self._reload_all()

    def _on_edit(self):
        rows = self._selected_rows()
        if len(rows) != 1:
            return
        invoice_id = self.model.invoice_id(rows[0])
        invoice = repository.get_invoice(invoice_id)
        if not invoice:
            return
        dialog = InvoiceDialog(
            self, invoice=invoice, furnizori=repository.distinct_furnizori(),
            categorii=repository.distinct_categories()
        )
        if dialog.exec():
            repository.update_invoice(invoice_id, dialog.get_data())
            self._reload_all()

    def _on_delete(self):
        rows = self._selected_rows()
        if not rows:
            return
        ids = [self.model.invoice_id(r) for r in rows]
        text = "această factură" if len(ids) == 1 else f"aceste {len(ids)} facturi"
        reply = QMessageBox.question(
            self, "Confirmare ștergere", f"Sigur vrei să ștergi {text}? Acțiunea nu poate fi anulată.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            repository.delete_invoices(ids)
            self._reload_all()

    def _on_import(self):
        dialog = ImportDialog(self)
        if dialog.exec():
            self._reload_all()

    def _on_export(self):
        path, selected_filter = QFileDialog.getSaveFileName(
            self, "Export facturi", "facturi.xlsx", "Excel (*.xlsx);;CSV (*.csv)"
        )
        if not path:
            return
        if selected_filter.startswith("Excel") and not path.lower().endswith(".xlsx"):
            path += ".xlsx"
        elif selected_filter.startswith("CSV") and not path.lower().endswith(".csv"):
            path += ".csv"

        self.export_progress = QProgressDialog("Se exportă facturile...", None, 0, 0, self)
        self.export_progress.setWindowTitle("Export în curs")
        self.export_progress.setMinimumDuration(0)
        self.export_progress.setCancelButton(None)
        self.export_progress.show()

        self.export_worker = ExportWorker(path, dict(self.model.filters))
        self.export_worker.finished_ok.connect(self._on_export_finished)
        self.export_worker.failed.connect(self._on_export_failed)
        self.export_worker.start()

    def _on_export_finished(self, count):
        self.export_progress.close()
        QMessageBox.information(self, "Export finalizat", f"{count} facturi exportate cu succes.")

    def _on_export_failed(self, message):
        self.export_progress.close()
        QMessageBox.critical(self, "Eroare la export", message)
