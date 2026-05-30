from typing import Any


MEANING_MODIFIERS: dict[str, dict[str, Any]] = {
    "adversity": {
        "signals": ["buas", "terik", "panas", "sengatan", "keras", "berat", "menekan"],
        "tone": "tekanan",
    },
    "quiet": {
        "signals": ["hening", "sunyi", "diam", "sepi", "pelan"],
        "tone": "keheningan",
    },
    "nostalgia": {
        "signals": ["sendu", "rindu", "kenangan", "dulu", "lama"],
        "tone": "kenangan",
    },
    "warmth": {
        "signals": ["hangat", "nyaman", "teduh", "lembut", "dekat"],
        "tone": "kehangatan",
    },
    "complexity": {
        "signals": ["kusut", "rumit", "acak", "berantakan", "ribet"],
        "tone": "kerumitan",
    },
}


def detect_meaning_modifiers(text: str) -> list[dict[str, str]]:
    normalized = str(text or "").lower()
    matches: list[dict[str, str]] = []

    for key, item in MEANING_MODIFIERS.items():
        if any(signal in normalized for signal in item["signals"]):
            matches.append({"key": key, "tone": item["tone"]})

    return matches


def first_modifier_key(text: str) -> str:
    modifiers = detect_meaning_modifiers(text)
    return modifiers[0]["key"] if modifiers else ""