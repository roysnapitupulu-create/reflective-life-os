# context_compiler.py

from typing import Any

from scene_extractor import extract_scene
from symbol_taxonomy import contains_any, detect_symbols


HEAT_KEYWORDS = [
    "terik",
    "panas",
    "sengatan",
    "siang yang buas",
    "matahari",
    "gerah",
]

URGENCY_KEYWORDS = [
    "berburu waktu",
    "mengejar",
    "tergesa",
    "diburu",
    "cepat",
    "kejar",
    "deadline",
]

GRATITUDE_KEYWORDS = [
    "syukur",
    "bersyukur",
    "terima kasih",
    "berterima kasih",
    "lega",
    "cukup",
]

SLOW_PACE_KEYWORDS = [
    "pelan",
    "perlahan",
    "diam",
    "hening",
    "teduh",
    "menunggu",
    "rehat",
]

SIMPLE_LIFE_KEYWORDS = [
    "warung",
    "kopi",
    "teras",
    "jalanan",
    "angkot",
    "ojol",
    "gerobak",
    "halte",
    "lampu merah",
    "pohon",
    "hujan",
    "rumah",
    "dapur",
]

MORNING_KEYWORDS = ["pagi", "subuh"]
NOON_KEYWORDS = ["siang", "tengah hari"]
EVENING_KEYWORDS = ["sore", "senja", "petang"]
NIGHT_KEYWORDS = ["malam", "larut"]


def _entry_text(entry: dict[str, Any]) -> str:
    return " ".join(
        [
            str(entry.get("activity") or ""),
            str(entry.get("personal_reflection") or ""),
            str(entry.get("gratitude_note") or ""),
            str(entry.get("improvement_action") or ""),
        ]
    ).strip()


def _artifact_text(artifact: dict[str, Any] | None) -> str:
    if not artifact:
        return ""

    return " ".join(
        [
            str(artifact.get("memory_note") or ""),
            str(artifact.get("side_note") or ""),
        ]
    ).strip()


def compile_context(text: str) -> dict[str, Any]:
    text = str(text or "")
    text_lower = text.lower()

    themes, symbols = detect_symbols(text_lower)
    emotions: list[str] = []

    time_context = None

    if contains_any(text_lower, HEAT_KEYWORDS):
        emotions.append("adversity")

    if contains_any(text_lower, URGENCY_KEYWORDS):
        emotions.append("urgency")

    has_gratitude = contains_any(text_lower, GRATITUDE_KEYWORDS)
    if has_gratitude:
        emotions.append("gratitude")

    has_slow_pace = contains_any(text_lower, SLOW_PACE_KEYWORDS)
    is_simple_life = contains_any(text_lower, SIMPLE_LIFE_KEYWORDS)
    is_spiritual = "spiritual" in themes

    if contains_any(text_lower, MORNING_KEYWORDS):
        time_context = "pagi"
    elif contains_any(text_lower, NOON_KEYWORDS):
        time_context = "siang"
    elif contains_any(text_lower, EVENING_KEYWORDS):
        time_context = "senja"
    elif contains_any(text_lower, NIGHT_KEYWORDS):
        time_context = "malam"

    unique_themes = list(dict.fromkeys(themes))
    unique_symbols = list(dict.fromkeys(symbols))
    unique_emotions = list(dict.fromkeys(emotions))

    scene = extract_scene(
        text_lower,
        {
            "themes": unique_themes,
            "symbols": unique_symbols,
            "emotions": unique_emotions,
            "time_context": time_context,
        },
    )

    return {
        "raw_text": text,
        "themes": unique_themes,
        "symbols": unique_symbols,
        "emotions": unique_emotions,
        "time_context": time_context,
        "is_spiritual": is_spiritual,
        "is_simple_life": is_simple_life,
        "has_gratitude": has_gratitude,
        "has_slow_pace": has_slow_pace,
        "scene": scene,
    }


def compile_daily_context(
    entry: dict[str, Any],
    artifact: dict[str, Any] | None = None,
) -> dict[str, Any]:
    text = " ".join(
        [
            _entry_text(entry),
            _artifact_text(artifact),
        ]
    ).strip()

    return compile_context(text)


def generate_contextual_side_note(context: dict[str, Any]) -> str:
    try:
        from meaning_synthesizer import synthesize_meaning_v2

        meaning = synthesize_meaning_v2(context)
        side_note = str(meaning.get("side_note") or "").strip()

        if side_note:
            return side_note

    except Exception:
        pass

    return "Ada hal kecil yang tidak perlu langsung dijelaskan. Cukup disimpan sebagai tanda bahwa hari ini pernah hadir."