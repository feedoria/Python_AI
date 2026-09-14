# -*- coding: utf-8 -*-

PRIMARY = "#4F46E5"
PRIMARY_DARK = "#4338CA"
PRIMARY_LIGHT = "#EEF2FF"
ACCENT = "#0EA5A5"
BG = "#F4F5FA"
CARD_BG = "#FFFFFF"
BORDER = "#E3E5EC"
TEXT = "#1F2430"
MUTED = "#6B7280"
SUCCESS = "#1A7F37"
DANGER = "#DC2626"
DANGER_DARK = "#B91C1C"

QSS = f"""
* {{
    font-family: "Segoe UI", "Inter", sans-serif;
    font-size: 13px;
    color: {TEXT};
}}

QMainWindow, QDialog {{
    background: {BG};
}}

QWidget#filterBar, QWidget#statsPanel {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
}}

QToolBar {{
    background: {CARD_BG};
    border: none;
    border-bottom: 1px solid {BORDER};
    padding: 6px 10px;
    spacing: 8px;
}}

QToolButton {{
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 6px 12px;
    font-weight: 600;
}}

QToolButton:hover {{
    background: {PRIMARY_LIGHT};
    border: 1px solid {PRIMARY};
}}

QPushButton {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 7px 16px;
    font-weight: 600;
}}

QPushButton:hover {{
    border: 1px solid {PRIMARY};
    color: {PRIMARY};
}}

QPushButton:pressed {{
    background: {PRIMARY_LIGHT};
}}

QPushButton#primaryButton {{
    background: {PRIMARY};
    color: white;
    border: 1px solid {PRIMARY};
}}

QPushButton#primaryButton:hover {{
    background: {PRIMARY_DARK};
    border: 1px solid {PRIMARY_DARK};
    color: white;
}}

QPushButton#dangerButton {{
    background: white;
    color: {DANGER};
    border: 1px solid {DANGER};
}}

QPushButton#dangerButton:hover {{
    background: {DANGER};
    color: white;
}}

QLineEdit, QComboBox, QDateEdit, QDoubleSpinBox, QSpinBox, QTextEdit {{
    background: white;
    border: 1px solid {BORDER};
    border-radius: 6px;
    padding: 5px 8px;
    selection-background-color: {PRIMARY_LIGHT};
}}

QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QDoubleSpinBox:focus, QTextEdit:focus {{
    border: 1px solid {PRIMARY};
}}

QComboBox::drop-down {{
    border: none;
    width: 20px;
}}

QLabel#fieldLabel {{
    font-weight: 600;
    color: {MUTED};
}}

QLabel#sectionTitle {{
    font-size: 15px;
    font-weight: 700;
    color: {TEXT};
}}

QLabel#totalValue {{
    font-size: 22px;
    font-weight: 800;
    color: {PRIMARY};
}}

QTableView {{
    background: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
    gridline-color: {BORDER};
    alternate-background-color: #FAFBFF;
    selection-background-color: {PRIMARY_LIGHT};
    selection-color: {TEXT};
}}

QTableView::item {{
    padding: 6px;
    border-bottom: 1px solid {BORDER};
}}

QHeaderView::section {{
    background: {CARD_BG};
    color: {MUTED};
    font-weight: 700;
    padding: 8px;
    border: none;
    border-bottom: 2px solid {BORDER};
}}

QStatusBar {{
    background: {CARD_BG};
    border-top: 1px solid {BORDER};
}}

QScrollBar:vertical {{
    background: transparent;
    width: 10px;
}}

QScrollBar::handle:vertical {{
    background: #C7CAD6;
    border-radius: 5px;
    min-height: 24px;
}}

QScrollBar::handle:vertical:hover {{
    background: {MUTED};
}}

QScrollBar:horizontal {{
    background: transparent;
    height: 10px;
}}

QScrollBar::handle:horizontal {{
    background: #C7CAD6;
    border-radius: 5px;
    min-width: 24px;
}}

QProgressDialog {{
    background: {CARD_BG};
}}

QMenu {{
    background: white;
    border: 1px solid {BORDER};
}}
"""
