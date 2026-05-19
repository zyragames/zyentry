from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from zyentry.core.desktop_entry import DesktopEntryData


VALID_CATEGORIES = (
    "Utility",
    "Development",
    "Game",
    "Graphics",
    "AudioVideo",
    "Office",
    "Network",
    "System",
    "Settings",
    "Education",
)

VALID_ICON_SUFFIXES = {".png", ".svg", ".xpm"}


@dataclass(frozen=True)
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_desktop_entry_data(data: DesktopEntryData) -> ValidationResult:
    errors: list[str] = []
    warnings: list[str] = []

    if not data.name.strip():
        errors.append("App name is required.")

    exec_value = data.exec_path.strip()
    if not exec_value:
        errors.append("Application path is required.")
    else:
        path = Path(exec_value.strip('"'))
        if not path.exists():
            errors.append("Application path does not exist.")
        elif not path.is_file():
            errors.append("Application path must be a file.")
        elif not path.stat().st_mode & 0o111:
            message = "Application file is not executable."
            if path.suffix.lower() == ".appimage":
                message = "AppImage file is not executable."
            warnings.append(message)

    if data.category not in VALID_CATEGORIES:
        errors.append("Category is not supported.")

    icon_value = data.icon.strip()
    if icon_value and any(sep in icon_value for sep in ("/", "\\")):
        icon_path = Path(icon_value)
        if not icon_path.exists():
            errors.append("Icon path does not exist.")
        elif not icon_path.is_file():
            errors.append("Icon path must be a file.")
        elif icon_path.suffix.lower() not in VALID_ICON_SUFFIXES:
            errors.append("Icon must be PNG, SVG, or XPM.")

    return ValidationResult(errors=errors, warnings=warnings)
