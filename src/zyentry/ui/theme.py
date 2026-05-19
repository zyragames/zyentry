from __future__ import annotations

from importlib.resources import files


def load_stylesheet(theme: str) -> str:
    selected = "light" if theme == "light" else "dark"
    resource = files("zyentry.resources.themes").joinpath(f"{selected}.qss")
    return resource.read_text(encoding="utf-8")
