# -*- coding: utf-8 -*-
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QProgressDialog,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)

from ERP.Proiect_Facturi.facturi.db import repository
from ERP.Proiect_Facturi.facturi.db.repository import EDITABLE_FIELDS
from ERP.Proiect_Facturi.facturi.services import importer

FIELD_LABELS = {
    "numar_factura": "Nr. factură *",
    "furnizor": "Furnizor *",
    "data_factura": "Data",
    "categorie": "Categorie",
    "suma_fara_tva": "Sumă fără TVA",
    "tva": "TVA",
    "suma_totala": "Sumă totală",
    "moneda": "Monedă",
    "stare": "Stare",
    "observatii": "Observații",
}

NONE_OPTION = "(niciuna)"


class ImportCancelled(Exception):
    pass


class ImportWorker(QThread):
    progress = pyqtSignal(int, int)
    finished_ok = pyqtSignal(int, list)
    failed = pyqtSignal(str)
    cancelled = pyqtSignal()

    def __init__(self, path, mapping):
        super().__init__()
        self.path = path
        self.mapping = mapping
        self._cancel_requested = False

    def cancel(self):
        self._cancel_requested = True

    def _on_progress(self, done, total):
        self.progress.emit(done, total)
        if self._cancel_requested:
            raise ImportCancelled()

    def run(self):
        try:
            df = importer.read_file(self.path)
            rows, errors = importer.build_rows(df, self.mapping)
            inserted = repository.bulk_insert(rows, progress_callback=self._on_progress)
            self.finished_ok.emit(inserted, errors)
        except ImportCancelled:
            self.cancelled.emit()
        except Exception as exc:
            self.failed.emit(str(exc))


class ImportDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Import facturi din Excel/CSV")
        self.setMinimumWidth(560)
        self.path = None
        self.mapping_combos = {}
        self.worker = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        title = QLabel("Import facturi din Excel/CSV")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        file_row = QHBoxLayout()
        self.file_label = QLabel("Niciun fișier selectat")
        pick_btn = QPushButton("Alege fișier...")
        pick_btn.clicked.connect(self._pick_file)
        file_row.addWidget(self.file_label, 1)
        file_row.addWidget(pick_btn)
        layout.addLayout(file_row)

        mapping_box = QGroupBox("Corespondență coloane")
        self.mapping_form = QFormLayout(mapping_box)
        for field in EDITABLE_FIELDS:
            combo = QComboBox()
            combo.addItem(NONE_OPTION)
            self.mapping_combos[field] = combo
            self.mapping_form.addRow(QLabel(FIELD_LABELS.get(field, field)), combo)
        layout.addWidget(mapping_box)

        preview_label = QLabel("Previzualizare (primele rânduri):")
        layout.addWidget(preview_label)
        self.preview_table = QTableWidget(0, 0)
        self.preview_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.preview_table.setMaximumHeight(160)
        layout.addWidget(self.preview_table)

        buttons = QDialogButtonBox()
        cancel_btn = buttons.addButton("Anulează", QDialogButtonBox.ButtonRole.RejectRole)
        self.import_btn = buttons.addButton("Importă", QDialogButtonBox.ButtonRole.AcceptRole)
        self.import_btn.setObjectName("primaryButton")
        self.import_btn.setEnabled(False)
        cancel_btn.clicked.connect(self.reject)
        self.import_btn.clicked.connect(self._start_import)
        layout.addWidget(buttons)

    def _pick_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Alege fișier facturi", "", "Fișiere Excel/CSV (*.xlsx *.xls *.csv)"
        )
        if not path:
            return
        try:
            preview_df = importer.read_file(path, nrows=15)
        except Exception as exc:
            QMessageBox.critical(self, "Eroare la citire", f"Nu s-a putut citi fișierul:\n{exc}")
            return

        self.path = path
        self.file_label.setText(path)
        self.import_btn.setEnabled(True)
        self._populate_mapping(preview_df.columns.tolist())
        self._populate_preview(preview_df)

    def _populate_mapping(self, columns):
        auto_map = importer.auto_map_columns(columns)
        for field, combo in self.mapping_combos.items():
            combo.blockSignals(True)
            combo.clear()
            combo.addItem(NONE_OPTION)
            combo.addItems(columns)
            detected = auto_map.get(field)
            if detected:
                combo.setCurrentText(detected)
            combo.blockSignals(False)

    def _populate_preview(self, df):
        self.preview_table.setColumnCount(len(df.columns))
        self.preview_table.setHorizontalHeaderLabels([str(c) for c in df.columns])
        self.preview_table.setRowCount(len(df.index))
        for r in range(len(df.index)):
            for c, col in enumerate(df.columns):
                value = str(df.iloc[r, c])
                self.preview_table.setItem(r, c, QTableWidgetItem(value))

    def _current_mapping(self):
        mapping = {}
        for field, combo in self.mapping_combos.items():
            text = combo.currentText()
            mapping[field] = None if text == NONE_OPTION else text
        return mapping

    def _start_import(self):
        mapping = self._current_mapping()
        if not mapping.get("numar_factura") or not mapping.get("furnizor"):
            QMessageBox.warning(
                self, "Corespondență incompletă",
                "Selectează coloanele pentru Nr. factură și Furnizor înainte de import."
            )
            return

        self.progress_dialog = QProgressDialog("Se importă facturile...", "Anulează", 0, 100, self)
        self.progress_dialog.setWindowTitle("Import în curs")
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setValue(0)

        self.worker = ImportWorker(self.path, mapping)
        self.worker.progress.connect(self._on_progress)
        self.worker.finished_ok.connect(self._on_finished)
        self.worker.failed.connect(self._on_failed)
        self.worker.cancelled.connect(self._on_cancelled)
        self.progress_dialog.canceled.connect(self.worker.cancel)
        self.import_btn.setEnabled(False)
        self.worker.start()

    def _on_progress(self, done, total):
        if total > 0:
            self.progress_dialog.setMaximum(total)
            self.progress_dialog.setValue(done)

    def _on_finished(self, inserted, errors):
        self.progress_dialog.close()
        msg = f"Import finalizat: {inserted} facturi adăugate."
        if errors:
            shown = "\n".join(errors[:20])
            more = f"\n... și încă {len(errors) - 20} rânduri ignorate." if len(errors) > 20 else ""
            msg += f"\n\n{len(errors)} rânduri ignorate:\n{shown}{more}"
        QMessageBox.information(self, "Import finalizat", msg)
        self.accept()

    def _on_failed(self, message):
        self.progress_dialog.close()
        self.import_btn.setEnabled(True)
        QMessageBox.critical(self, "Eroare la import", message)

    def _on_cancelled(self):
        self.progress_dialog.close()
        self.import_btn.setEnabled(True)
        QMessageBox.information(self, "Import anulat", "Importul a fost anulat. Nicio factură nu a fost adăugată.")
