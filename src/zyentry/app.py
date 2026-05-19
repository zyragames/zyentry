from __future__ import annotations

import sys


def main() -> int:
    from PySide6.QtWidgets import QApplication

    from zyentry.ui.main_window import MainWindow

    app = QApplication(sys.argv)
    app.setApplicationName("ZyEntry")
    app.setOrganizationName("ZyraGames")
    window = MainWindow()
    window.show()
    return app.exec()
