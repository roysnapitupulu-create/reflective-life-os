# meaning_synthesizer.py

from typing import Any

from life_observation_library import pick_life_observation
from meaning_modifiers import apply_meaning_modifiers
from scene_composer import compose_scene_observation
from voice_selector import select_voice


THEME_TITLES = {
    "tree": "Keteduhan dan Ketahanan",
    "thinkpad": "Kesetiaan Benda Kecil",
    "urban_survival": "Catatan dari Jalanan",
    "spiritual": "Ruang Batin",
}


def _raw(context: dict[str, Any]) -> str:
    return str(context.get("raw_text") or "").lower()


def _first_theme(context: dict[str, Any]) -> str:
    themes = context.get("themes") or []
    if not themes:
        return ""
    return str(themes[0])


def synthesize_meaning_v2(context: dict[str, Any]) -> dict[str, str]:
    symbol = _first_theme(context)

    scene_observation = compose_scene_observation(context)
    if scene_observation:
        voice = select_voice(symbol, context) if symbol else "reflective"

        return {
            "theme": THEME_TITLES.get(symbol, "Life Observation"),
            "observation": scene_observation,
            "side_note": scene_observation,
            "reflection_question": "",
            "voice": voice,
        }

    if symbol:
        voice = select_voice(symbol, context)
        observation = pick_life_observation(symbol, voice)
        observation = apply_meaning_modifiers(symbol, observation, context)

        if observation:
            return {
                "theme": THEME_TITLES.get(symbol, "Life Observation"),
                "observation": observation,
                "side_note": observation,
                "reflection_question": "",
                "voice": voice,
            }

    text = _raw(context)

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
            "theme": "Kesederhanaan yang Menenangkan",
            "observation": "Ada ritme sederhana yang terasa pelan dalam catatan ini.",
            "side_note": "Hal-hal kecil kadang tidak meminta perhatian besar. Tapi justru di sana hidup terasa lebih bisa dihuni.",
            "reflection_question": "Hal sederhana apa yang ingin kamu beri ruang lagi besok?",
        }

    return {
        "theme": "Hari yang Perlu Didengar",
        "observation": "Belum ada pola besar yang perlu disimpulkan. Tetapi ada sesuatu yang layak didengarkan lebih pelan.",
        "side_note": "Ada hal kecil yang tidak perlu langsung dijelaskan. Cukup disimpan sebagai tanda bahwa hari ini pernah hadir.",
        "reflection_question": "Apa bagian hari ini yang belum sempat kamu dengarkan?",
    }