# voice_selector.py

from typing import Any


def select_voice(symbol: str, context: dict[str, Any]) -> str:
    emotions = context.get("emotions", [])
    time_context = context.get("time_context")
    raw_text = str(context.get("raw_text") or "").lower()

    has_humor_trigger = any(
        key in raw_text
        for key in [
            "darwin",
            "survival is the fittest",
            "fittest",
            "wakaka",
            "wkwk",
            "haha",
        ]
    )

    if symbol == "urban_survival":
        if has_humor_trigger:
            return "philosophical_humor"
        if "adversity" in emotions or "urgency" in emotions:
            return "reflective"
        return "micro_wonder"

    if symbol == "thinkpad":
        if time_context == "malam":
            return "gentle_humor"
        return "reflective"

    if symbol == "tree":
        if "adversity" in emotions:
            return "reflective"
        return "micro_wonder"

    if symbol == "spiritual":
        return "reflective"

    return "reflective"