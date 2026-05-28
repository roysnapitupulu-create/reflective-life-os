from typing import Any


LOW_ENERGY_THRESHOLD = 4
HIGH_CALORIES_THRESHOLD = 2_500
SHORT_REFLECTION_WORDS = 5


def _word_count(value: str) -> int:
    return len(str(value or "").strip().split())


def analyze_recent_patterns(entries: list[dict[str, Any]]) -> list[str]:
    recent_entries = entries[:7]
    if len(recent_entries) < 2:
        return ["Belum cukup data untuk melihat pola. Dua sampai tiga entry biasanya sudah mulai memberi arah."]

    patterns: list[str] = []

    newest_three = recent_entries[:3]
    if len(newest_three) == 3:
        moods = [int(entry.get("mood_score") or 0) for entry in newest_three]
        chronological_moods = list(reversed(moods))
        if chronological_moods[0] > chronological_moods[1] > chronological_moods[2]:
            patterns.append(
                "Aku melihat mood menurun dalam tiga entry terakhir. Ini mungkin sinyal untuk mengurangi beban kecil "
                "yang sebenarnya bisa ditunda."
            )

    low_energy_days = [
        entry for entry in recent_entries if int(entry.get("energy_score") or 0) <= LOW_ENERGY_THRESHOLD
    ]
    if len(low_energy_days) >= 3:
        patterns.append(
            "Beberapa hari terakhir energimu cenderung rendah. Mungkin tubuh dan pikiranmu sedang membutuhkan recovery, "
            "bukan tekanan tambahan."
        )

    empty_gratitude_days = [
        entry for entry in recent_entries if not str(entry.get("gratitude_note") or "").strip()
    ]
    if len(empty_gratitude_days) >= 3:
        patterns.append(
            "Catatan syukur beberapa kali kosong. Bukan masalah, tapi mungkin ada baiknya mencari satu hal kecil yang "
            "masih terasa menahanmu tetap berpijak."
        )

    costs = [float(entry.get("cost") or 0) for entry in recent_entries]
    previous_costs = [cost for cost in costs[1:] if cost > 0]
    if costs[0] > 0 and previous_costs:
        previous_average = sum(previous_costs) / len(previous_costs)
        if previous_average > 0 and costs[0] >= previous_average * 1.75:
            patterns.append(
                "Pengeluaran terbaru terlihat naik cukup tajam dibanding beberapa entry sebelumnya. Ini layak ditinjau "
                "dengan tenang, tanpa perlu langsung menyalahkan keputusanmu."
            )

    high_calorie_days = [
        entry for entry in recent_entries if int(entry.get("calories") or 0) >= HIGH_CALORIES_THRESHOLD
    ]
    if len(high_calorie_days) >= 2:
        patterns.append(
            "Asupan kalori tinggi muncul lebih dari sekali. Anggap ini sebagai data pola makan, lalu pilih satu titik "
            "yang paling mudah dibuat lebih mindful."
        )

    short_reflection_days = [
        entry
        for entry in recent_entries
        if _word_count(str(entry.get("personal_reflection") or "")) <= SHORT_REFLECTION_WORDS
    ]
    if len(short_reflection_days) >= 3:
        patterns.append(
            "Refleksi pribadimu beberapa kali sangat singkat. Mungkin kamu belum punya ruang yang cukup untuk benar-benar "
            "menamai apa yang sedang terjadi."
        )

    if not patterns:
        patterns.append(
            "Belum ada pola yang kuat dari entry terbaru. Untuk sementara, datanya terlihat cukup tersebar dan masih wajar."
        )

    return patterns
