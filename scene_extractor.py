# scene_extractor.py

from typing import Any


ACTION_KEYWORDS = {
    "menunggu": ["menunggu", "nunggu", "menanti"],
    "berteduh": ["berteduh", "teduh", "di bawah pohon"],
    "berjalan": ["berjalan", "lewat", "melintas"],
    "bekerja": ["bekerja", "mencari nafkah", "jualan", "mengantar", "mengejar penumpang"],
    "pulang": ["pulang", "pulang kerja"],
    "berhenti": ["berhenti", "lampu merah"],
}

SETTING_KEYWORDS = {
    "lampu_merah": ["lampu merah", "perempatan", "traffic light"],
    "jalan": ["jalan", "jalanan", "gang", "trotoar"],
    "halte": ["halte", "terminal"],
    "warung": ["warung", "warteg", "kedai"],
    "malam": ["malam", "larut"],
    "siang": ["siang", "terik", "panas"],
}

OBJECT_KEYWORDS = {
    "ponsel": ["ponsel", "hp", "handphone", "layar"],
    "order": ["order", "pesanan"],
    "dagangan": ["dagangan", "jualan"],
    "kendaraan": ["kendaraan", "motor", "mobil", "angkot"],
}


def _contains_any(text: str, keywords: list[str]) -> bool:
    return any(keyword in text for keyword in keywords)


def extract_scene(text: str, context: dict[str, Any] | None = None) -> dict[str, list[str]]:
    text_lower = str(text or "").lower()
    context = context or {}

    symbols = context.get("symbols", []) or []

    actors: list[str] = []
    actions: list[str] = []
    settings: list[str] = []
    objects: list[str] = []
    supporting_symbols: list[str] = []

    for symbol in symbols:
        if symbol in ["ojol", "angkot", "gerobak"]:
            actors.append(symbol)
        elif symbol in ["tree"]:
            supporting_symbols.append(symbol)
        elif symbol in ["lampu_merah", "halte", "warung"]:
            settings.append(symbol)

    for action, keywords in ACTION_KEYWORDS.items():
        if _contains_any(text_lower, keywords):
            actions.append(action)

    for setting, keywords in SETTING_KEYWORDS.items():
        if _contains_any(text_lower, keywords):
            settings.append(setting)

    for obj, keywords in OBJECT_KEYWORDS.items():
        if _contains_any(text_lower, keywords):
            objects.append(obj)

    return {
        "actors": list(dict.fromkeys(actors)),
        "actions": list(dict.fromkeys(actions)),
        "settings": list(dict.fromkeys(settings)),
        "objects": list(dict.fromkeys(objects)),
        "supporting_symbols": list(dict.fromkeys(supporting_symbols)),
    }