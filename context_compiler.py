from meaning_synthesizer import synthesize_side_note
from typing import Any

from emotion_engine import extract_emotions_from_text
from meaning_engine import detect_reflection_themes


TIME_KEYWORDS = {
    "pagi": ["pagi", "subuh", "sarapan", "bubur", "kopi pagi"],
    "siang": ["siang", "makan siang"],
    "sore": ["sore", "senja"],
    "malam": ["malam", "tidur", "hening"],
}

SIMPLE_LIFE_KEYWORDS = [
    "bubur", "kopi", "makan", "jalan", "rumah", "hujan",
    "pagi", "pelan", "sederhana", "sehari-hari"
]

SPIRITUAL_KEYWORDS = [
    "tuhan", "doa", "syukur", "ibadah", "kebaktian",
    "gereja", "umat", "iman", "berkat"
]


def _contains_any(text: str, keywords: list[str]) -> bool:
    normalized = str(text or "").lower()
    return any(keyword in normalized for keyword in keywords)


def _detect_time_context(text: str) -> str:
    normalized = str(text or "").lower()
    for time_name, keywords in TIME_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return time_name
    return ""


def compile_daily_context(entry: dict[str, Any], artifact: dict[str, Any] | None = None) -> dict[str, Any]:
    artifact = artifact or {}

    reflection = str(entry.get("personal_reflection") or "")
    gratitude = str(entry.get("gratitude_note") or "")
    tomorrow = str(entry.get("improvement_action") or "")
    activity = str(entry.get("activity") or "")
    memory_note = str(artifact.get("memory_note") or "")

    combined_text = " ".join([activity, reflection, gratitude, tomorrow, memory_note]).strip()

    themes = detect_reflection_themes(combined_text)
    emotions = extract_emotions_from_text(combined_text)

    return {
        "raw_text": combined_text,
        "themes": themes,
        "emotions": emotions,
        "time_context": _detect_time_context(combined_text),
        "is_spiritual": _contains_any(combined_text, SPIRITUAL_KEYWORDS),
        "is_simple_life": _contains_any(combined_text, SIMPLE_LIFE_KEYWORDS),
        "has_gratitude": "gratitude" in themes or _contains_any(combined_text, ["syukur", "bersyukur"]),
        "has_slow_pace": _contains_any(combined_text, ["pelan", "tidak tergesa", "tanpa tergesa", "perlahan"]),
    }


def generate_contextual_side_note(context: dict[str, Any]) -> str:
    try:
        return synthesize_side_note(context)
    except Exception:
        pass

    time_context = context.get("time_context")
    is_spiritual = context.get("is_spiritual")
    is_simple_life = context.get("is_simple_life")
    has_gratitude = context.get("has_gratitude")
    has_slow_pace = context.get("has_slow_pace")

    if time_context == "pagi" and is_spiritual and has_slow_pace:
        return "Pagi tidak selalu meminta kita bergegas. Kadang ia hanya mengajak kita hadir dengan lebih utuh."

    if time_context == "pagi" and is_simple_life and has_gratitude:
        return "Hal-hal sederhana sering menjadi tempat pertama rasa syukur belajar bernapas."

    if is_spiritual and has_gratitude:
        return "Syukur tidak selalu datang setelah semuanya selesai; kadang ia justru menjaga hati saat proses masih berjalan."

    if has_slow_pace:
        return "Tidak semua perjalanan harus dipercepat. Ada hidup yang justru pulih ketika dijalani pelan-pelan."

    if is_simple_life:
        return "Yang biasa-biasa saja kadang menyimpan cara paling jujur untuk merasa hidup."

    if has_gratitude:
        return "Di antara banyak hal yang belum selesai, satu rasa syukur kecil tetap layak diberi tempat."

    return "Ada hari yang tidak perlu segera disimpulkan. Cukup dicatat, lalu dibiarkan berbicara perlahan."