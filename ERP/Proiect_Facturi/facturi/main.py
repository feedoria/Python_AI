# -*- coding: utf-8 -*-
import sys

from PyQt6.QtWidgets import QApplication

from ERP.Proiect_Facturi.facturi.db.database import get_connection
from ERP.Proiect_Facturi.facturi.ui.main_window import MainWindow
from ERP.Proiect_Facturi.facturi.ui.style import QSS


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setStyleSheet(QSS)

    get_connection()

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
