from __future__ import annotations

import json
import shutil
from dataclasses import asdict, dataclass
from pathlib import Path

from zyentry.core.paths import settings_path


@dataclass
class Settings:
    language: str = "de"
    theme: str = "dark"
    window_width: int = 1280
    window_height: int = 840
    last_app_path: str = ""
    last_icon_path: str = ""
    default_category: str = "Utility"
    terminal: bool = False
    startup_notify: bool = True

    @classmethod
    def load(cls, path: Path | None = None) -> "Settings":
        target = path or settings_path()
        if not target.exists():
            return cls()
        try:
            raw = json.loads(target.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            broken = target.with_suffix(target.suffix + ".broken")
            try:
                shutil.copy2(target, broken)
            except OSError:
                pass
            return cls()
        except OSError:
            return cls()

        defaults = asdict(cls())
        data = {key: raw.get(key, value) for key, value in defaults.items()}
        if data["language"] not in {"de", "en", "fr"}:
            data["language"] = "de"
        if data["theme"] not in {"dark", "light"}:
            data["theme"] = "dark"
        return cls(**data)

    def save(self, path: Path | None = None) -> None:
        target = path or settings_path()
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(asdict(self), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
