from typing import Any


THREAD_KEYWORDS = {
    "tekanan pekerjaan": ["kerja", "pekerjaan", "deadline", "atasan", "meeting", "tugas"],
    "relasi yang terasa berat": ["konflik", "relasi", "pasangan", "teman", "keluarga", "sendiri"],
    "kebingungan": ["bingung", "bimbang", "ragu", "tidak tahu", "ga tahu", "gak tahu"],
    "rasa takut atau khawatir": ["takut", "khawatir", "cemas", "gelisah", "was-was"],
    "kehilangan arah": ["kehilangan arah", "hampa", "kosong", "stuck", "mandek"],
    "kelelahan": ["lelah", "capek", "letih", "penat", "berat"],
}


def detect_unfinished_thread(entries: list[dict[str, Any]]) -> str | None:
    if len(entries) < 2:
        return None

    latest = entries[0]
    candidate = entries[1]
    seed_text = str(latest.get("created_at") or latest.get("entry_date") or "")
    seed = sum(ord(char) for char in seed_text)

    # Jangan selalu mengingatkan masa lalu; beri ruang bernapas.
    if seed % 3 == 0:
        return None

    combined_text = " ".join(
        [
            str(candidate.get("activity") or ""),
            str(candidate.get("personal_reflection") or ""),
            str(candidate.get("improvement_action") or ""),
        ]
    ).lower()

    for topic, keywords in THREAD_KEYWORDS.items():
        if any(keyword in combined_text for keyword in keywords):
            return f"Kemarin kamu sempat menyinggung soal {topic}. Apa itu masih terasa hari ini?"

    return None
