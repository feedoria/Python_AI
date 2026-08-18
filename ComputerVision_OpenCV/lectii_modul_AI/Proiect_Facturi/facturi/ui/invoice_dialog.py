# -*- coding: utf-8 -*-
from PyQt6.QtCore import QDate, Qt
from PyQt6.QtWidgets import (
    QComboBox,
    QCompleter,
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from constants import CATEGORII_IMPLICITE, COTE_TVA, MONEDE, STARE_NEPLATITA, STARI


class InvoiceDialog(QDialog):
    def __init__(self, parent=None, invoice: dict = None, furnizori=None, categorii=None):
        super().__init__(parent)
        self.invoice = invoice
        self.setWindowTitle("Editează factură" if invoice else "Adaugă factură")
        self.setMinimumWidth(440)
        self._build_ui(furnizori or [], categorii or [])
        if invoice:
            self._populate(invoice)
        else:
            self._set_defaults()
        self._recalc()

    def _build_ui(self, furnizori, categorii):
        layout = QVBoxLayout(self)
        title = QLabel("Editează factură" if self.invoice else "Adaugă factură nouă")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignmentFlag.AlignRight)

        self.numar_edit = QLineEdit()
        self.numar_edit.setPlaceholderText("ex: FF-2026-00123")
        form.addRow(self._label("Nr. factură *"), self.numar_edit)

        self.furnizor_edit = QLineEdit()
        self.furnizor_edit.setPlaceholderText("Numele furnizorului")
        if furnizori:
            completer = QCompleter(furnizori, self)
            completer.setCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
            self.furnizor_edit.setCompleter(completer)
        form.addRow(self._label("Furnizor *"), self.furnizor_edit)

        self.data_edit = QDateEdit()
        self.data_edit.setCalendarPopup(True)
        self.data_edit.setDisplayFormat("yyyy-MM-dd")
        form.addRow(self._label("Data *"), self.data_edit)

        self.categorie_combo = QComboBox()
        self.categorie_combo.setEditable(True)
        items = list(dict.fromkeys(CATEGORII_IMPLICITE + list(categorii)))
        self.categorie_combo.addItems(items)
        form.addRow(self._label("Categorie"), self.categorie_combo)

        self.suma_fara_tva_spin = QDoubleSpinBox()
        self.suma_fara_tva_spin.setRange(0, 999_999_999)
        self.suma_fara_tva_spin.setDecimals(2)
        self.suma_fara_tva_spin.valueChanged.connect(self._recalc)
        form.addRow(self._label("Sumă fără TVA *"), self.suma_fara_tva_spin)

        self.cota_combo = QComboBox()
        self.cota_combo.addItems([f"{c}%" for c in COTE_TVA])
        self.cota_combo.setCurrentIndex(len(COTE_TVA) - 1)
        self.cota_combo.currentIndexChanged.connect(self._recalc)
        form.addRow(self._label("Cotă TVA"), self.cota_combo)

        self.tva_spin = QDoubleSpinBox()
        self.tva_spin.setRange(0, 999_999_999)
        self.tva_spin.setDecimals(2)
        form.addRow(self._label("TVA"), self.tva_spin)

        self.total_spin = QDoubleSpinBox()
        self.total_spin.setRange(0, 999_999_999)
        self.total_spin.setDecimals(2)
        form.addRow(self._label("Sumă totală"), self.total_spin)

        self.moneda_combo = QComboBox()
        self.moneda_combo.addItems(MONEDE)
        form.addRow(self._label("Monedă"), self.moneda_combo)

        self.stare_combo = QComboBox()
        self.stare_combo.addItems(STARI)
        form.addRow(self._label("Stare"), self.stare_combo)

        self.observatii_edit = QTextEdit()
        self.observatii_edit.setFixedHeight(70)
        form.addRow(self._label("Observații"), self.observatii_edit)

        layout.addLayout(form)

        buttons = QDialogButtonBox()
        cancel_btn = buttons.addButton("Anulează", QDialogButtonBox.ButtonRole.RejectRole)
        save_btn = buttons.addButton("Salvează", QDialogButtonBox.ButtonRole.AcceptRole)
        save_btn.setObjectName("primaryButton")
        cancel_btn.clicked.connect(self.reject)
        save_btn.clicked.connect(self._on_save)
        layout.addWidget(buttons)

    def _label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("fieldLabel")
        return lbl

    def _set_defaults(self):
        self.data_edit.setDate(QDate.currentDate())
        self.stare_combo.setCurrentText(STARE_NEPLATITA)

    def _populate(self, invoice: dict):
        self.numar_edit.setText(invoice.get("numar_factura") or "")
        self.furnizor_edit.setText(invoice.get("furnizor") or "")
        date_str = invoice.get("data_factura")
        if date_str:
            self.data_edit.setDate(QDate.fromString(date_str, "yyyy-MM-dd"))
        else:
            self.data_edit.setDate(QDate.currentDate())
        categorie = invoice.get("categorie") or ""
        idx = self.categorie_combo.findText(categorie)
        if idx >= 0:
            self.categorie_combo.setCurrentIndex(idx)
        else:
            self.categorie_combo.setCurrentText(categorie)
        self.suma_fara_tva_spin.setValue(invoice.get("suma_fara_tva") or 0)
        self.tva_spin.setValue(invoice.get("tva") or 0)
        self.total_spin.setValue(invoice.get("suma_totala") or 0)
        moneda = invoice.get("moneda") or "RON"
        if moneda in MONEDE:
            self.moneda_combo.setCurrentText(moneda)
        stare = invoice.get("stare") or STARE_NEPLATITA
        if stare in STARI:
            self.stare_combo.setCurrentText(stare)
        self.observatii_edit.setPlainText(invoice.get("observatii") or "")

    def _recalc(self):
        cota = COTE_TVA[self.cota_combo.currentIndex()]
        baza = self.suma_fara_tva_spin.value()
        tva = round(baza * cota / 100, 2)
        self.tva_spin.setValue(tva)
        self.total_spin.setValue(round(baza + tva, 2))

    def _on_save(self):
        if not self.numar_edit.text().strip():
            QMessageBox.warning(self, "Câmp obligatoriu", "Introdu numărul facturii.")
            return
        if not self.furnizor_edit.text().strip():
            QMessageBox.warning(self, "Câmp obligatoriu", "Introdu furnizorul.")
            return
        self.accept()

    def get_data(self) -> dict:
        return {
            "numar_factura": self.numar_edit.text().strip(),
            "furnizor": self.furnizor_edit.text().strip(),
            "data_factura": self.data_edit.date().toString("yyyy-MM-dd"),
            "categorie": self.categorie_combo.currentText().strip(),
            "suma_fara_tva": self.suma_fara_tva_spin.value(),
            "tva": self.tva_spin.value(),
            "suma_totala": self.total_spin.value(),
            "moneda": self.moneda_combo.currentText(),
            "stare": self.stare_combo.currentText(),
            "observatii": self.observatii_edit.toPlainText().strip(),
        }
