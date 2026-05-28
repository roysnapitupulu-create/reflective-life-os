from typing import Any

from emotion_engine import extract_entry_emotions


def _word_count(text: str) -> int:
    return len(str(text or "").strip().split())


def infer_language_profile(entries: list[dict[str, Any]]) -> dict[str, bool]:
    recent_entries = entries[:5]
    if not recent_entries:
        return {
            "short_writer": False,
            "reflective_writer": False,
            "religious_tone": False,
            "practical_tone": False,
        }

    reflection_lengths = [
        _word_count(str(entry.get("personal_reflection") or "")) for entry in recent_entries
    ]
    combined_text = " ".join(
        [
            str(entry.get("personal_reflection") or "")
            + " "
            + str(entry.get("gratitude_note") or "")
            + " "
            + str(entry.get("improvement_action") or "")
            for entry in recent_entries
        ]
    ).lower()

    average_length = sum(reflection_lengths) / max(len(reflection_lengths), 1)
    religious_markers = ["doa", "syukur", "tuhan", "allah", "iman", "berkah", "alhamdulillah"]
    practical_markers = ["besok", "langkah", "aksi", "rencana", "target", "mulai"]

    return {
        "short_writer": average_length <= 8,
        "reflective_writer": average_length >= 22,
        "religious_tone": any(marker in combined_text for marker in religious_markers),
        "practical_tone": any(marker in combined_text for marker in practical_markers),
    }


def generate_submit_response(entry: dict[str, Any], entries: list[dict[str, Any]]) -> str:
    profile = infer_language_profile(entries)
    emotions = extract_entry_emotions(entry, limit=2)
    mood = int(entry.get("mood_score") or 0)
    energy = int(entry.get("energy_score") or 0)
    created_at = str(entry.get("created_at") or "")
    rotation_seed = sum(ord(char) for char in created_at) % 9

    if profile["short_writer"]:
        responses = [
            "Aku membaca ini.",
            "Dicatat. Pelan-pelan.",
            "Terima kasih sudah menulis sedikit.",
            "Satu kalimat pun cukup.",
            "Aku simpan dulu catatan ini.",
            "Tidak perlu dipanjang-panjangkan malam ini.",
            "Ada hari yang cukup dicatat singkat.",
            "Kita biarkan ini menetap sebentar.",
            "Cukup untuk hari ini.",
        ]
    else:
        responses = [
            "Aku membaca ini.",
            "Apa bagian hari ini yang paling membekas untukmu?",
            "Hari ini tampaknya punya bobotnya sendiri.",
            "Menarik bahwa kamu tetap mencoba jujur.",
            "Kadang hari biasa pun bisa terasa berat.",
            "Kita tidak perlu langsung menyimpulkan apa pun.",
            "Ada sesuatu di catatan ini yang layak diberi ruang.",
            "Apa yang paling tertinggal di pikiranmu setelah menulis ini?",
            "Aku simpan ini sebagai bagian kecil dari harimu.",
        ]

    if mood <= 4 or energy <= 4:
        tired_responses = [
            "Hari ini tampaknya cukup melelahkan.",
            "Kita simpan dulu. Tidak perlu memaksa makna besar.",
            "Pelan dulu malam ini.",
        ]
        return tired_responses[rotation_seed % len(tired_responses)]

    if emotions and rotation_seed in {2, 5}:
        emotion_text = ", ".join(emotions)
        return f"Nuansa yang terasa: {emotion_text}."

    if profile["religious_tone"] and rotation_seed in {1, 6}:
        return "Semoga catatan ini ikut jadi ruang yang teduh."

    if profile["practical_tone"] and rotation_seed in {3, 7}:
        return "Cukup pilih satu langkah kecil yang paling mungkin dilakukan."

    return responses[rotation_seed]
