from __future__ import annotations

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QSizePolicy, QVBoxLayout, QWidget

from zyentry.ui.widgets.help_button import HelpButton


class StepCard(QFrame):
    def __init__(self, number: int, content: QWidget, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.setObjectName("StepCard")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.badge = QLabel(str(number))
        self.badge.setObjectName("Badge")
        self.badge.setFixedSize(48, 48)
        self.badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel()
        self.title.setObjectName("StepTitle")
        self.title.setWordWrap(True)
        self.title.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.MinimumExpanding)
        self.help_button = HelpButton("", "")
        content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)

        text_layout = QVBoxLayout()
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(0)
        text_layout.addWidget(self.title)

        left = QHBoxLayout()
        left.setContentsMargins(0, 0, 0, 0)
        left.setSpacing(18)
        left.addWidget(self.badge)
        left.addLayout(text_layout, 1)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)
        layout.setSpacing(24)
        layout.addLayout(left, 4)
        layout.addWidget(content, 5)
        layout.addWidget(self.help_button)

    def set_texts(self, title: str, description: str, help_text: str) -> None:
        del description
        self.title.setText(title)
        self.help_button.set_help(title, help_text)
