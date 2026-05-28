from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo


JAKARTA_TZ = ZoneInfo("Asia/Jakarta")


def _time_greeting(now: datetime) -> str:
    hour = now.hour
    if 4 <= hour < 11:
        return "Selamat pagi. Mulai pelan saja, tidak perlu langsung penuh energi"
    if 11 <= hour < 15:
        return "Selamat siang. Ambil napas sebentar sebelum lanjut"
    if 15 <= hour < 18:
        return "Selamat sore. Hari ini sudah berjalan cukup jauh, dan itu layak diakui"
    return "Selamat malam. Ini ruang kecil untuk menutup hari dengan lebih tenang"


def generate_welcome(entries: list[dict[str, Any]], now: datetime | None = None) -> str:
    current_time = now.astimezone(JAKARTA_TZ) if now else datetime.now(JAKARTA_TZ)
    greeting = _time_greeting(current_time)

    if not entries:
        return f"{greeting}."

    latest = entries[0]
    mood = int(latest.get("mood_score") or 0)
    energy = int(latest.get("energy_score") or 0)
    activity = str(latest.get("activity") or "hari terakhirmu").strip()
    reflection = str(latest.get("personal_reflection") or "").lower()

    if mood <= 4 or energy <= 4:
        return f"{greeting}. Terakhir, {activity} tampaknya cukup mengurasmu. Kita mulai pelan saja."

    tired_words = ["lelah", "capek", "berat", "penat"]
    if any(word in reflection for word in tired_words):
        return f"{greeting}. Di catatan terakhir ada sedikit rasa lelah. Semoga kali ini lebih ringan."

    if str(latest.get("gratitude_note") or "").strip():
        return f"{greeting}. Aku ingat kamu masih menemukan satu hal kecil untuk disyukuri."

    return f"{greeting}. Selamat datang kembali. Tidak perlu buru-buru menamai semuanya."
