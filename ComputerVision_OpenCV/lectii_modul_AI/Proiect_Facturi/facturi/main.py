# -*- coding: utf-8 -*-
import sys

from PyQt6.QtWidgets import QApplication

from db.database import get_connection
from ui.main_window import MainWindow
from ui.style import QSS


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
