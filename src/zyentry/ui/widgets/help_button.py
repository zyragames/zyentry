from __future__ import annotations

from PySide6.QtWidgets import QMessageBox, QPushButton, QWidget


class HelpButton(QPushButton):
    def __init__(self, title: str, text: str, parent: QWidget | None = None) -> None:
        super().__init__("?", parent)
        self.setObjectName("HelpButton")
        self._title = title
        self._text = text
        self.setToolTip(text)
        self.clicked.connect(self.show_help)

    def set_help(self, title: str, text: str) -> None:
        self._title = title
        self._text = text
        self.setToolTip(text)

    def show_help(self) -> None:
        QMessageBox.information(self, self._title, self._text)
