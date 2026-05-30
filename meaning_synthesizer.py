from typing import Any

from life_observation_library import pick_life_observation


def _raw(context: dict[str, Any]) -> str:
    return str(context.get("raw_text") or "").lower()


def synthesize_meaning_v2(context: dict[str, Any]) -> dict[str, str]:
    text = _raw(context)

    observation = pick_life_observation(text)
    if observation:
        return {
            "theme": "Life Observation",
            "observation": observation,
            "side_note": observation,
            "reflection_question": "",
        }

    has_morning = context.get("time_context") == "pagi"
    has_spiritual = bool(context.get("is_spiritual"))
    has_simple = bool(context.get("is_simple_life"))
    has_gratitude = bool(context.get("has_gratitude"))
    has_slow = bool(context.get("has_slow_pace"))

    has_togetherness = any(
        word in text
        for word in [
            "bersama",
            "istri",
            "keluarga",
            "gereja",
            "umat",
            "kebaktian",
            "melayani",
            "pembeli",
        ]
    )

    has_food = any(
        word in text
        for word in [
            "bubur",
            "sarapan",
            "makan",
            "mangkok",
            "pagi",
        ]
    )

    if has_food and has_togetherness and has_gratitude:
        return {
            "theme": "Syukur dalam Kebersamaan",
            "observation": "Hari ini syukur tampaknya tidak berdiri sendiri. Ia hadir bersama orang-orang yang ikut memberi makna pada harimu.",
            "side_note": "Kadang yang membuat pagi terasa berharga bukan apa yang tersaji, melainkan siapa yang hadir dan ikut membuatnya bermakna.",
            "reflection_question": "Siapa yang paling kamu syukuri kehadirannya hari ini?",
        }

    if has_morning and has_spiritual and has_gratitude:
        return {
            "theme": "Kehadiran yang Pelan",
            "observation": "Ada nuansa pagi yang tenang dan spiritual dalam catatan hari ini.",
            "side_note": "Pagi tidak selalu meminta kita bergegas. Kadang ia hanya mengajak kita hadir dengan lebih utuh.",
            "reflection_question": "Apa yang paling membuatmu merasa hadir pagi ini?",
        }

    if has_simple and has_slow:
        return {
            "theme": "Kesederhanaan",
            "observation": "Hal-hal yang sederhana tampaknya sedang membawa makna yang lebih besar dari biasanya.",
            "side_note": "Kesederhanaan hari ini tampaknya sedang mengajari satu hal: hidup tidak harus tergesa untuk terasa penuh.",
            "reflection_question": "Hal sederhana apa yang paling membekas hari ini?",
        }

    return {
        "theme": "Hari yang Perlu Didengar",
        "observation": "Belum ada pola besar yang perlu disimpulkan. Tetapi ada sesuatu yang layak didengarkan lebih pelan.",
        "side_note": "Ada hal kecil yang tidak perlu langsung dijelaskan. Cukup disimpan sebagai tanda bahwa hari ini pernah hadir.",
        "reflection_question": "Apa bagian hari ini yang belum sempat kamu dengarkan?",
    }


def synthesize_meaning(context: dict[str, Any]) -> str:
    return synthesize_meaning_v2(context)["side_note"]


def synthesize_side_note(context: dict[str, Any]) -> str:
    return synthesize_meaning_v2(context)["side_note"]