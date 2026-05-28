from typing import Any


HIGH_COST_THRESHOLD = 100_000
HIGH_CALORIES_THRESHOLD = 2_500


def _apply_style(text: str, style: str) -> str:
    style = style.lower()

    if style == "praktis":
        return f"{text} Langkah kecilnya: pilih satu tindakan yang bisa dilakukan dalam 10 menit."
    if style == "stoic":
        return f"{text} Bedakan mana yang bisa kamu kendalikan hari ini, lalu lepaskan sisanya pelan-pelan."
    if style == "filosofis":
        return f"{text} Mungkin ini juga undangan kecil untuk melihat pola hidupmu dengan lebih jernih."
    if style == "religius":
        return f"{text} Bawa ini juga dalam syukur, doa, dan harapan yang sederhana."
    if style == "lembut":
        return f"{text} Kamu tidak perlu memaksa semuanya selesai hari ini."
    return text


def generate_reflection(entry: dict[str, Any], style: str = "Lembut") -> str:
    mood = int(entry.get("mood_score") or 0)
    energy = int(entry.get("energy_score") or 0)
    cost = float(entry.get("cost") or 0)
    calories = int(entry.get("calories") or 0)
    personal_reflection = str(entry.get("personal_reflection") or "").strip()
    gratitude_note = str(entry.get("gratitude_note") or "").strip()

    notes: list[str] = []

    if mood <= 4 and energy <= 4:
        notes.append(
            _apply_style(
                "Hari ini tampaknya cukup berat. Istirahat yang layak dan satu tindakan kecil "
                "yang jelas sudah cukup untuk menjaga arah.",
                style,
            )
        )
    elif mood >= 7 and energy <= 4:
        notes.append(
            _apply_style(
                "Ada tanda bahwa harimu terasa cukup memuaskan, tetapi tubuh mungkin sedang meminta recovery. "
                "Pertahankan hal yang membuatmu puas, sambil memberi ruang untuk pemulihan fisik.",
                style,
            )
        )

    if cost >= HIGH_COST_THRESHOLD:
        notes.append(
            _apply_style(
                "Pengeluaran hari ini relatif tinggi. Ini bisa jadi momen baik untuk melihat kembali apakah "
                "belanja tersebut memang mendukung kebutuhan atau hanya respons cepat terhadap situasi hari ini.",
                style,
            )
        )

    if calories >= HIGH_CALORIES_THRESHOLD:
        notes.append(
            _apply_style(
                "Asupan kalori hari ini cukup tinggi. Catat ini sebagai data, bukan alasan untuk menyalahkan diri; "
                "besok bisa mulai dari pilihan makan yang sedikit lebih sadar.",
                style,
            )
        )

    if not personal_reflection:
        notes.append(
            _apply_style(
                "Refleksi pribadi masih kosong. Cukup tulis satu kalimat jujur tentang apa yang paling terasa hari ini.",
                style,
            )
        )

    if gratitude_note:
        notes.append(
            _apply_style(
                "Catatan syukurmu menunjukkan masih ada pegangan positif, bahkan jika hari tidak sempurna.",
                style,
            )
        )

    if not notes:
        notes.append(
            _apply_style(
                "Data hari ini terlihat cukup stabil. Pilih satu hal yang ingin dipertahankan besok, lalu satu hal kecil "
                "yang bisa dibuat sedikit lebih rapi.",
                style,
            )
        )

    return "\n\n".join(notes)
