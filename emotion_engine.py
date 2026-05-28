from typing import Any


EMOTION_KEYWORDS = {
    "lelah": ["lelah", "capek", "letih", "burnout", "berat", "penat"],
    "bersyukur": ["syukur", "bersyukur", "terima kasih", "alhamdulillah", "grateful"],
    "cemas": ["cemas", "khawatir", "takut", "gelisah", "was-was", "panik"],
    "bingung": ["bingung", "bimbang", "ragu", "tidak tahu", "ga tahu", "gak tahu"],
    "semangat": ["semangat", "antusias", "produktif", "senang", "lega"],
    "kecewa": ["kecewa", "sedih", "kesal", "marah", "frustrasi"],
    "tenang": ["tenang", "damai", "rileks", "pelan", "stabil"],
    "berharap": ["harap", "berharap", "semoga", "ingin", "mau mencoba"],
}


def extract_emotions_from_text(text: str, limit: int = 3) -> list[str]:
    normalized_text = str(text or "").lower()
    emotions: list[str] = []

    for emotion, keywords in EMOTION_KEYWORDS.items():
        if any(keyword in normalized_text for keyword in keywords):
            emotions.append(emotion)
        if len(emotions) >= limit:
            break

    return emotions


def extract_entry_emotions(entry: dict[str, Any], limit: int = 3) -> list[str]:
    combined_text = " ".join(
        [
            str(entry.get("personal_reflection") or ""),
            str(entry.get("gratitude_note") or ""),
            str(entry.get("improvement_action") or ""),
            str(entry.get("activity") or ""),
        ]
    )
    return extract_emotions_from_text(combined_text, limit=limit)
