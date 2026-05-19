from __future__ import annotations

import os
from pathlib import Path


def config_dir() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")
    return (Path(base) if base else Path.home() / ".config") / "zyentry"


def settings_path() -> Path:
    return config_dir() / "settings.json"


def applications_dir() -> Path:
    base = os.environ.get("XDG_DATA_HOME")
    return (Path(base) if base else Path.home() / ".local" / "share") / "applications"
