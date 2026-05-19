from __future__ import annotations

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QPainter, QPaintEvent
from PySide6.QtWidgets import QCheckBox, QWidget


class ThemeSwitch(QCheckBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedSize(58, 30)

    def sizeHint(self) -> QSize:
        return QSize(58, 30)

    def paintEvent(self, event: QPaintEvent) -> None:
        del event
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        track_color = QColor("#dbeafe") if self.isChecked() else QColor("#08203d")
        border_color = QColor("#facc15") if self.isChecked() else QColor("#2f6fa8")
        thumb_color = QColor("#facc15") if self.isChecked() else QColor("#0ea5e9")

        rect = self.rect().adjusted(1, 1, -1, -1)
        painter.setPen(border_color)
        painter.setBrush(track_color)
        painter.drawRoundedRect(rect, 14, 14)

        diameter = 22
        x = self.width() - diameter - 4 if self.isChecked() else 4
        y = (self.height() - diameter) // 2
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(thumb_color)
        painter.drawEllipse(x, y, diameter, diameter)
