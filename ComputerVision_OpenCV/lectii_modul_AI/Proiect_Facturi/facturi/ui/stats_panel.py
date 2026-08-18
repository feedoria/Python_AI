# -*- coding: utf-8 -*-
from PyQt6.QtCharts import QBarCategoryAxis, QBarSeries, QBarSet, QChart, QChartView, QValueAxis
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from db import repository
from ui.style import ACCENT, MUTED, PRIMARY


class StatsPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("statsPanel")
        self.setMinimumWidth(320)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        title = QLabel("Statistici")
        title.setObjectName("sectionTitle")
        layout.addWidget(title)

        self.total_caption = QLabel("Total cheltuieli (filtrat)")
        self.total_caption.setStyleSheet(f"color: {MUTED}; font-weight: 600;")
        layout.addWidget(self.total_caption)

        self.total_value = QLabel("0,00")
        self.total_value.setObjectName("totalValue")
        layout.addWidget(self.total_value)

        cat_title = QLabel("Cheltuieli pe categorie")
        cat_title.setStyleSheet("font-weight: 700; margin-top: 6px;")
        layout.addWidget(cat_title)

        self.category_chart_view = QChartView()
        self.category_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.category_chart_view.setMinimumHeight(220)
        layout.addWidget(self.category_chart_view)

        month_title = QLabel("Cheltuieli pe lună (ultimele 12)")
        month_title.setStyleSheet("font-weight: 700; margin-top: 6px;")
        layout.addWidget(month_title)

        self.month_chart_view = QChartView()
        self.month_chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.month_chart_view.setMinimumHeight(220)
        layout.addWidget(self.month_chart_view)

        layout.addStretch(1)

    def refresh(self, filters: dict = None):
        total = repository.total_sum(filters)
        self.total_value.setText(f"{total:,.2f}".replace(",", " "))

        self._render_category_chart(repository.stats_by_category(filters, limit=8))
        self._render_month_chart(repository.stats_by_month(filters, months=12))

    def _render_category_chart(self, data):
        chart = QChart()
        chart.legend().setVisible(False)
        chart.setBackgroundVisible(False)

        bar_set = QBarSet("Sumă")
        bar_set.setColor(QColor(PRIMARY))
        categories = []
        for name, value in data:
            bar_set.append(value or 0)
            categories.append(str(name))

        series = QBarSeries()
        series.append(bar_set)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(categories)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        max_val = max([v or 0 for _, v in data], default=0)
        axis_y.setRange(0, max_val * 1.15 if max_val else 1)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        self.category_chart_view.setChart(chart)

    def _render_month_chart(self, data):
        chart = QChart()
        chart.legend().setVisible(False)
        chart.setBackgroundVisible(False)

        bar_set = QBarSet("Sumă")
        bar_set.setColor(QColor(ACCENT))
        months = []
        for luna, value in data:
            bar_set.append(value or 0)
            months.append(luna)

        series = QBarSeries()
        series.append(bar_set)
        chart.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append(months)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)

        axis_y = QValueAxis()
        max_val = max([v or 0 for _, v in data], default=0)
        axis_y.setRange(0, max_val * 1.15 if max_val else 1)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)

        self.month_chart_view.setChart(chart)
