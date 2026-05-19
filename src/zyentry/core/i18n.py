from __future__ import annotations

import json
from importlib.resources import files


class Translator:
    def __init__(self, language: str = "de") -> None:
        self.translations = load_translations()
        self.language = language if language in self.translations else "de"

    def set_language(self, language: str) -> None:
        self.language = language if language in self.translations else "de"

    def t(self, key: str) -> str:
        current = self.translations.get(self.language, {})
        english = self.translations.get("en", {})
        return current.get(key) or english.get(key) or key


def load_translations() -> dict[str, dict[str, str]]:
    resource = files("zyentry.resources.i18n").joinpath("translations.json")
    return json.loads(resource.read_text(encoding="utf-8"))
