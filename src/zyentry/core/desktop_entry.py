from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from zyentry.core.paths import applications_dir


@dataclass(frozen=True)
class DesktopEntryData:
    name: str
    exec_path: str
    comment: str = ""
    icon: str = ""
    category: str = "Utility"
    terminal: bool = False
    startup_notify: bool = True


def _quote_exec(value: str) -> str:
    value = value.strip()
    if not value:
        return value
    if any(ch.isspace() for ch in value) and not (value.startswith('"') and value.endswith('"')):
        return '"' + value.replace('"', '\\"') + '"'
    return value


def sanitize_desktop_file_id(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", name.strip().lower()).strip("-._")
    return cleaned or "zyentry-app"


def build_desktop_entry(data: DesktopEntryData) -> str:
    category = data.category.strip() or "Utility"
    if not category.endswith(";"):
        category = f"{category};"

    lines = [
        "[Desktop Entry]",
        "Type=Application",
        f"Name={data.name.strip()}",
    ]
    if data.comment.strip():
        lines.append(f"Comment={data.comment.strip()}")
    lines.extend(
        [
            f"Exec={_quote_exec(data.exec_path)}",
            f"Icon={data.icon.strip()}",
            f"Terminal={str(data.terminal).lower()}",
            f"Categories={category}",
            f"StartupNotify={str(data.startup_notify).lower()}",
        ]
    )
    return "\n".join(lines) + "\n"


def install_desktop_entry(data: DesktopEntryData, target_dir: Path | None = None, refresh: bool = True) -> Path:
    directory = target_dir or applications_dir()
    directory.mkdir(parents=True, exist_ok=True)
    target = directory / f"{sanitize_desktop_file_id(data.name)}.desktop"
    target.write_text(build_desktop_entry(data), encoding="utf-8")
    target.chmod(target.stat().st_mode | 0o100)
    if refresh:
        refresh_desktop_databases(directory)
    return target


def refresh_desktop_databases(directory: Path) -> None:
    commands = [
        ["update-desktop-database", str(directory)],
        ["kbuildsycoca6"],
        ["kbuildsycoca5"],
    ]
    env = os.environ.copy()
    for command in commands:
        if shutil.which(command[0]) is None:
            continue
        try:
            subprocess.run(command, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=env)
        except OSError:
            continue
