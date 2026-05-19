from __future__ import annotations

import sys
from pathlib import Path

import PySide6
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QColor, QIcon, QPainter, QPen, QPixmap
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from zyentry import __version__
from zyentry.core.desktop_entry import DesktopEntryData, build_desktop_entry, install_desktop_entry
from zyentry.core.i18n import Translator
from zyentry.core.settings import Settings
from zyentry.core.validation import VALID_CATEGORIES, validate_desktop_entry_data
from zyentry.ui.theme import load_stylesheet
from zyentry.ui.widgets.step_card import StepCard
from zyentry.ui.widgets.theme_switch import ThemeSwitch


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.settings = Settings.load()
        self.translator = Translator(self.settings.language)
        self.step_cards: list[StepCard] = []

        self.setWindowTitle("ZyEntry")
        self.setMinimumSize(1180, 760)
        self.resize(1280, 890)
        self._build_ui()
        self._apply_theme()
        self._apply_translations()
        self._load_settings_to_form()
        self._connect_signals()
        self._update_preview_and_validation()

    def _build_ui(self) -> None:
        central = QWidget()
        central.setObjectName("Central")
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(24, 18, 24, 18)
        root.setSpacing(12)

        root.addWidget(self._build_header())

        scroll = QScrollArea()
        scroll.setObjectName("StepsScroll")
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        steps_widget = QWidget()
        steps_widget.setObjectName("StepsContainer")
        steps_layout = QVBoxLayout(steps_widget)
        steps_layout.setContentsMargins(0, 0, 0, 0)
        steps_layout.setSpacing(12)

        self.app_path_input = QLineEdit()
        self.browse_button = QPushButton()
        self.terminal_check = QCheckBox()
        path_row = self._row(self.app_path_input, self.browse_button)
        step1 = self._stack(path_row, self.terminal_check)

        self.name_input = QLineEdit()
        self.comment_input = QLineEdit()
        step2 = self._stack(self.name_input, self.comment_input)

        self.icon_preview = QLabel("▧")
        self.icon_preview.setObjectName("IconPreview")
        self.icon_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_preview.setFixedSize(78, 78)
        self.icon_button = QPushButton()
        self.icon_hint = QLabel()
        self.icon_hint.setProperty("muted", True)
        self.icon_hint.setWordWrap(True)
        icon_controls = self._stack(self.icon_button, self.icon_hint)
        step3 = self._row(self.icon_preview, icon_controls)

        self.category_combo = QComboBox()
        self.category_combo.addItems(VALID_CATEGORIES)
        self.category_combo.setFixedWidth(300)
        step4 = self._left_widget(self.category_combo)

        self.preview_button = QPushButton()
        self.preview_button.setObjectName("SecondaryButton")
        self.install_button = QPushButton()
        self.install_button.setObjectName("PrimaryButton")
        self.install_status = QLabel()
        self.install_status.setObjectName("StatusText")
        self.install_status.setWordWrap(True)
        action_row = self._stack(self.preview_button, self.install_button, self.install_status)
        step5 = self._left_widget(action_row)

        contents = [step1, step2, step3, step4, step5]
        for index, content in enumerate(contents, start=1):
            card = StepCard(index, content)
            self.step_cards.append(card)
            steps_layout.addWidget(card)

        steps_layout.addStretch(1)
        scroll.setWidget(steps_widget)
        root.addWidget(scroll, 1)
        root.addWidget(self._build_footer())

    def _build_header(self) -> QWidget:
        header = QFrame()
        header.setObjectName("Header")
        layout = QHBoxLayout(header)
        layout.setContentsMargins(18, 10, 18, 10)
        layout.setSpacing(14)

        logo = QFrame()
        logo.setObjectName("Logo")
        logo.setFixedSize(46, 46)
        logo_layout = QHBoxLayout(logo)
        logo_layout.setContentsMargins(0, 0, 0, 0)
        logo_text = QLabel(">_")
        logo_text.setObjectName("LogoText")
        logo_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo_layout.addWidget(logo_text)

        title_box = QVBoxLayout()
        title_box.setContentsMargins(0, 0, 0, 0)
        title_box.setSpacing(0)
        self.title_label = QLabel("ZyEntry")
        self.title_label.setObjectName("Title")
        self.subtitle_label = QLabel()
        self.subtitle_label.setObjectName("Subtitle")
        title_box.addWidget(self.title_label)
        title_box.addWidget(self.subtitle_label)

        layout.addWidget(logo)
        layout.addLayout(title_box)
        layout.addStretch(1)

        self.language_combo = QComboBox()
        self.language_combo.setObjectName("LanguageCombo")
        self.language_combo.setIconSize(QSize(22, 14))
        self.language_combo.setSizeAdjustPolicy(QComboBox.SizeAdjustPolicy.AdjustToContents)
        layout.addWidget(self.language_combo)

        theme_box = QWidget()
        theme_layout = QHBoxLayout(theme_box)
        theme_layout.setContentsMargins(0, 0, 0, 0)
        theme_layout.setSpacing(4)
        self.light_icon = QLabel("☀")
        self.light_icon.setObjectName("ThemeIcon")
        self.theme_button = ThemeSwitch()
        self.theme_button.setObjectName("ThemeSwitch")
        self.dark_icon = QLabel("☾")
        self.dark_icon.setObjectName("ThemeIcon")
        theme_layout.addWidget(self.light_icon)
        theme_layout.addWidget(self.theme_button)
        theme_layout.addWidget(self.dark_icon)
        layout.addWidget(theme_box)
        return header

    def _build_footer(self) -> QWidget:
        footer = QFrame()
        footer.setObjectName("Footer")
        layout = QHBoxLayout(footer)
        layout.setContentsMargins(18, 10, 18, 10)
        self.about_button = QPushButton()
        self.about_button.setObjectName("AboutButton")
        layout.addWidget(self.about_button)
        layout.addStretch(1)
        self.claim_label = QLabel()
        self.claim_label.setObjectName("Pill")
        layout.addWidget(self.claim_label)
        return footer

    def _row(self, *widgets: QWidget) -> QWidget:
        box = QWidget()
        layout = QHBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(16)
        for index, widget in enumerate(widgets):
            layout.addWidget(widget, 1 if index == 0 else 0)
        return box

    def _stack(self, *widgets: QWidget) -> QWidget:
        box = QWidget()
        layout = QVBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        for widget in widgets:
            layout.addWidget(widget)
        return box

    def _left_widget(self, widget: QWidget) -> QWidget:
        box = QWidget()
        layout = QHBoxLayout(box)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        layout.addStretch(1)
        return box

    def _connect_signals(self) -> None:
        self.browse_button.clicked.connect(self._browse_app)
        self.icon_button.clicked.connect(self._browse_icon)
        self.preview_button.clicked.connect(self._show_preview_dialog)
        self.about_button.clicked.connect(self._show_about_dialog)
        self.install_button.clicked.connect(self._install)
        self.theme_button.clicked.connect(self._toggle_theme)
        self.language_combo.currentIndexChanged.connect(self._language_selected)
        for widget in (self.app_path_input, self.name_input, self.comment_input):
            widget.textChanged.connect(self._update_preview_and_validation)
            widget.textChanged.connect(self._save_form_settings)
        self.category_combo.currentTextChanged.connect(self._update_preview_and_validation)
        self.category_combo.currentTextChanged.connect(self._save_form_settings)
        self.terminal_check.toggled.connect(self._update_preview_and_validation)
        self.terminal_check.toggled.connect(self._save_form_settings)

    def _load_settings_to_form(self) -> None:
        self.app_path_input.setText(self.settings.last_app_path)
        self.category_combo.setCurrentText(self.settings.default_category)
        self.terminal_check.setChecked(self.settings.terminal)
        if self.settings.last_icon_path:
            self._set_icon_path(self.settings.last_icon_path)

    def _apply_translations(self) -> None:
        t = self.translator.t
        self.subtitle_label.setText(t("app.subtitle"))
        self.browse_button.setText(t("browse"))
        self.icon_button.setText(t("choose_icon_button"))
        self.app_path_input.setPlaceholderText(t("path.placeholder"))
        self.name_input.setPlaceholderText(t("name.placeholder"))
        self.comment_input.setPlaceholderText(t("comment.placeholder"))
        self.icon_hint.setText(t("icon.hint"))
        self.terminal_check.setText(t("terminal"))
        self.preview_button.setText(t("preview.show"))
        self.install_button.setText(t("install"))
        for index, card in enumerate(self.step_cards, start=1):
            card.set_texts(t(f"step{index}.title"), t(f"step{index}.desc"), t(f"step{index}.help"))
        self.language_combo.blockSignals(True)
        self.language_combo.clear()
        for language in ("de", "en", "fr"):
            self.language_combo.addItem(self._language_icon(language), t(f"language.{language}"), language)
        index = self.language_combo.findData(self.settings.language)
        self.language_combo.setCurrentIndex(max(index, 0))
        self.language_combo.setFixedWidth(self.language_combo.sizeHint().width())
        self.language_combo.blockSignals(False)
        self.about_button.setText(t("about.button"))
        self.claim_label.setText(t("footer.claim"))
        self.theme_button.setChecked(self.settings.theme == "light")
        self.theme_button.setToolTip(t("theme.toggle"))
        self.light_icon.setToolTip(t("theme.light"))
        self.dark_icon.setToolTip(t("theme.dark"))

    def _language_icon(self, language: str) -> QIcon:
        pixmap = QPixmap(28, 18)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if language == "de":
            painter.fillRect(0, 0, 28, 6, QColor("#111827"))
            painter.fillRect(0, 6, 28, 6, QColor("#dc2626"))
            painter.fillRect(0, 12, 28, 6, QColor("#facc15"))
        elif language == "fr":
            painter.fillRect(0, 0, 9, 18, QColor("#2563eb"))
            painter.fillRect(9, 0, 10, 18, QColor("#ffffff"))
            painter.fillRect(19, 0, 9, 18, QColor("#dc2626"))
        else:
            painter.fillRect(0, 0, 28, 18, QColor("#1d4ed8"))
            painter.setPen(QPen(QColor("#ffffff"), 4))
            painter.drawLine(0, 0, 28, 18)
            painter.drawLine(28, 0, 0, 18)
            painter.setPen(QPen(QColor("#dc2626"), 2))
            painter.drawLine(0, 0, 28, 18)
            painter.drawLine(28, 0, 0, 18)
            painter.setPen(QPen(QColor("#ffffff"), 6))
            painter.drawLine(14, 0, 14, 18)
            painter.drawLine(0, 9, 28, 9)
            painter.setPen(QPen(QColor("#dc2626"), 3))
            painter.drawLine(14, 0, 14, 18)
            painter.drawLine(0, 9, 28, 9)

        painter.setPen(QPen(QColor("#0f172a"), 1))
        painter.drawRoundedRect(0, 0, 27, 17, 3, 3)
        painter.end()
        return QIcon(pixmap)

    def _apply_theme(self) -> None:
        self.setStyleSheet(load_stylesheet(self.settings.theme))

    def _toggle_theme(self) -> None:
        self.settings.theme = "light" if self.theme_button.isChecked() else "dark"
        self._apply_theme()
        self.settings.save()

    def _language_selected(self, *_args: object) -> None:
        language = self.language_combo.currentData()
        if isinstance(language, str) and language != self.settings.language:
            self._set_language(language)

    def _set_language(self, language: str) -> None:
        self.settings.language = language
        self.translator.set_language(language)
        self._apply_translations()
        self._update_preview_and_validation()
        self.settings.save()

    def _browse_app(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, self.translator.t("step1.title"), "", "Applications/Binaries (*.AppImage *.sh *.run);;All files (*)")
        if path:
            self.app_path_input.setText(path)

    def _browse_icon(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, self.translator.t("step3.title"), "", "Images (*.png *.svg *.xpm);;All files (*)")
        if path:
            self._set_icon_path(path)
            self.settings.last_icon_path = path
            self.settings.save()
            self._update_preview_and_validation()

    def _set_icon_path(self, path: str) -> None:
        self.icon_preview.setToolTip(path)
        pixmap = QIcon(path).pixmap(64, 64)
        if not pixmap.isNull():
            self.icon_preview.setPixmap(pixmap)
        elif Path(path).suffix.lower() == ".png":
            image = QPixmap(path)
            if not image.isNull():
                self.icon_preview.setPixmap(image.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        else:
            self.icon_preview.setText("▧")

    def _data(self) -> DesktopEntryData:
        return DesktopEntryData(
            name=self.name_input.text(),
            exec_path=self.app_path_input.text(),
            comment=self.comment_input.text(),
            icon=self.settings.last_icon_path,
            category=self.category_combo.currentText(),
            terminal=self.terminal_check.isChecked(),
            startup_notify=self.settings.startup_notify,
        )

    def _preview_data(self) -> DesktopEntryData:
        data = self._data()
        return DesktopEntryData(
            name=data.name.strip() or self.translator.t("sample.name"),
            exec_path=data.exec_path.strip() or "/home/user/Apps/Beispiel-App.AppImage",
            comment=data.comment.strip() or self.translator.t("sample.comment"),
            icon=data.icon.strip() or "beispiel-app",
            category=data.category,
            terminal=data.terminal,
            startup_notify=data.startup_notify,
        )

    def _update_preview_and_validation(self) -> None:
        data = self._data()
        result = validate_desktop_entry_data(data)
        self.install_button.setEnabled(result.ok)
        self.install_status.setText("\n".join(self._localized_messages(result.warnings[:2])))

    def _show_preview_dialog(self) -> None:
        dialog = QDialog(self)
        dialog.setObjectName("PreviewDialog")
        dialog.setWindowTitle(self.translator.t("preview.title"))
        dialog.resize(720, 520)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        preview_text = QPlainTextEdit()
        preview_text.setObjectName("PreviewText")
        preview_text.setReadOnly(True)
        preview_text.setPlainText(build_desktop_entry(self._preview_data()))
        layout.addWidget(preview_text, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.button(QDialogButtonBox.StandardButton.Close).setText(self.translator.t("close"))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def _show_about_dialog(self) -> None:
        dialog = QDialog(self)
        dialog.setObjectName("AboutDialog")
        dialog.setWindowTitle(self.translator.t("about.title"))
        dialog.resize(440, 300)

        layout = QVBoxLayout(dialog)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        info = QLabel(
            self.translator.t("about.text").format(
                app_version=__version__,
                python_version=f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                pyside_version=PySide6.__version__,
            )
        )
        info.setWordWrap(True)
        info.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        layout.addWidget(info, 1)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Close)
        buttons.button(QDialogButtonBox.StandardButton.Close).setText(self.translator.t("close"))
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)

        dialog.exec()

    def _localized_messages(self, messages: list[str]) -> list[str]:
        keys = {
            "App name is required.": "validation.name_required",
            "Application path is required.": "validation.path_required",
            "Application path does not exist.": "validation.path_missing",
            "Application path must be a file.": "validation.path_file",
            "Application file is not executable.": "validation.not_executable",
            "AppImage file is not executable.": "validation.appimage_not_executable",
            "Category is not supported.": "validation.category",
            "Icon path does not exist.": "validation.icon_missing",
            "Icon path must be a file.": "validation.icon_file",
            "Icon must be PNG, SVG, or XPM.": "validation.icon_type",
        }
        return [self.translator.t(keys.get(message, message)) for message in messages]

    def _save_form_settings(self) -> None:
        self.settings.last_app_path = self.app_path_input.text()
        self.settings.default_category = self.category_combo.currentText()
        self.settings.terminal = self.terminal_check.isChecked()
        self.settings.save()

    def _install(self) -> None:
        data = self._data()
        result = validate_desktop_entry_data(data)
        if not result.ok:
            QMessageBox.warning(self, "ZyEntry", self.translator.t("validation_failed") + "\n\n" + "\n".join(self._localized_messages(result.errors)))
            return
        target = install_desktop_entry(data)
        QMessageBox.information(self, "ZyEntry", f"{self.translator.t('success')}\n\n{target}")
