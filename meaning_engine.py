import json
from typing import Any


THEME_KEYWORDS = {
    "exhaustion": ["lelah", "capek", "letih", "penat", "habis tenaga", "burnout", "menguras"],
    "fear": ["takut", "ngeri", "khawatir", "takut gagal", "takut tertinggal"],
    "anxiety": ["cemas", "gelisah", "panik", "was-was", "overthinking"],
    "control": ["kontrol", "mengendalikan", "kendali", "harus sempurna", "semuanya"],
    "meaning": ["makna", "tujuan", "arah hidup", "buat apa", "hampa", "kosong"],
    "guilt": ["bersalah", "menyesal", "nyesel", "salahku", "mengecewakan"],
    "gratitude": ["syukur", "bersyukur", "terima kasih", "alhamdulillah", "grateful"],
    "loneliness": ["sendiri", "kesepian", "sepi", "tidak ada yang paham", "terasing"],
    "anger": ["marah", "kesal", "jengkel", "muak", "emosi"],
    "hope": ["harap", "berharap", "semoga", "ingin membaik", "masih bisa"],
    "discipline": ["disiplin", "kebiasaan", "habit", "konsisten", "rutinitas"],
    "uncertainty": ["bingung", "ragu", "tidak tahu", "gak tahu", "ga tahu", "bimbang"],
    "faith": ["doa", "tuhan", "allah", "iman", "pasrah", "berserah", "berkah"],
    "self-worth": ["tidak cukup", "gak cukup", "ga cukup", "tidak layak", "rendah diri"],
    "relationship": ["relasi", "pasangan", "teman", "keluarga", "konflik", "hubungan"],
    "work pressure": ["kerja", "pekerjaan", "deadline", "atasan", "meeting", "tugas", "target"],
}

SELF_HARM_KEYWORDS = [
    "bunuh diri",
    "mengakhiri hidup",
    "mati saja",
    "pengen mati",
    "ingin mati",
    "melukai diri",
    "menyakiti diri",
    "self harm",
]

LENSES = {
    "Stoic": {
        "source": "Marcus Aurelius / Epictetus",
        "reason": "User sedang bicara soal kendali, tekanan, ketidakpastian, atau emosi yang sulit ditahan.",
    },
    "Viktor Frankl": {
        "source": "Viktor Frankl, Man's Search for Meaning",
        "reason": "User sedang menyentuh lelah, tekanan, harapan, atau pencarian makna kecil.",
    },
    "Socratic": {
        "source": "Socrates",
        "reason": "User sedang berada dalam kebingungan, pilihan, atau kebutuhan untuk menjernihkan pikiran.",
    },
    "Kierkegaard": {
        "source": "Soren Kierkegaard",
        "reason": "User sedang menyentuh kecemasan, takut, iman, atau pilihan yang terasa eksistensial.",
    },
    "Carl Rogers": {
        "source": "Carl Rogers",
        "reason": "User sedang bicara soal rasa tidak cukup, bersalah, atau kerentanan emosional.",
    },
    "Spiritual": {
        "source": "spiritual reflection",
        "reason": "User sedang menulis tentang syukur, doa, penyerahan, atau harapan.",
    },
    "Practical Growth": {
        "source": "practical reflective practice",
        "reason": "User sedang menyentuh disiplin, kebiasaan, atau langkah perbaikan kecil.",
    },
}


def _contains_self_harm(text: str) -> bool:
    normalized_text = text.lower()
    return any(keyword in normalized_text for keyword in SELF_HARM_KEYWORDS)


def detect_reflection_themes(text: str) -> list[str]:
    normalized_text = str(text or "").lower()
    themes: list[str] = []

    for theme, keywords in THEME_KEYWORDS.items():
        if any(keyword in normalized_text for keyword in keywords):
            themes.append(theme)

    return themes


def select_reflective_lens(themes: list[str], life_area: str, reflection_style: str) -> dict[str, str]:
    theme_set = set(themes)
    normalized_area = str(life_area or "").lower()
    normalized_style = str(reflection_style or "").lower()

    if "faith" in theme_set or normalized_style == "religius":
        lens_name = "Spiritual"
    elif {"control", "anger", "work pressure"} & theme_set:
        lens_name = "Stoic"
    elif {"exhaustion", "meaning", "hope"} & theme_set:
        lens_name = "Viktor Frankl"
    elif {"uncertainty"} & theme_set:
        lens_name = "Socratic"
    elif {"anxiety", "fear"} & theme_set:
        lens_name = "Kierkegaard"
    elif {"self-worth", "guilt", "loneliness"} & theme_set:
        lens_name = "Carl Rogers"
    elif {"discipline"} & theme_set or normalized_area == "pembelajaran":
        lens_name = "Practical Growth"
    else:
        lens_name = "Carl Rogers"

    return {"name": lens_name, **LENSES[lens_name]}


def _build_response(themes: list[str], lens_name: str) -> tuple[str, str, str]:
    theme_set = set(themes)

    if lens_name == "Stoic":
        return (
            "Aku menangkap ada tekanan untuk mengurus banyak hal sekaligus. Dengan lensa Stoic, mungkin yang paling lembut adalah memisahkan mana yang sungguh ada dalam kendalimu hari ini.",
            "Apa satu hal yang sebenarnya tidak harus kamu kendalikan malam ini?",
            "Pilih satu tindakan kecil yang masih bisa kamu lakukan tanpa memaksa seluruh dirimu.",
        )
    if lens_name == "Viktor Frankl":
        return (
            "Ada rasa lelah di sini, tapi juga tanda bahwa kamu masih mencari arti dari apa yang sedang dijalani. Makna hari ini mungkin tidak besar; cukup satu hal kecil yang membuatmu tetap bertahan dengan jujur.",
            "Apa satu hal kecil yang masih terasa berarti di tengah tekanan ini?",
            "Tulis satu kalimat tentang hal yang ingin kamu jaga, bukan hal yang harus kamu kejar.",
        )
    if lens_name == "Socratic":
        return (
            "Catatan ini terdengar seperti pikiran yang sedang mencari kejernihan. Lensa Socratic tidak buru-buru menjawab; ia mulai dari pertanyaan yang lebih tepat.",
            "Pertanyaan apa yang sebenarnya sedang kamu hindari atau belum berani jawab?",
            "Pilih satu pertanyaan paling jujur, lalu tulis jawabannya dalam dua kalimat saja.",
        )
    if lens_name == "Kierkegaard":
        return (
            "Kecemasan kadang muncul saat sesuatu benar-benar berarti bagi kita. Tidak perlu langsung mengusirnya; mungkin cukup melihat pilihan kecil apa yang sedang ia tunjukkan.",
            "Pilihan apa yang terasa berat karena sebenarnya penting bagimu?",
            "Ambil satu langkah kecil yang selaras dengan nilai yang ingin kamu pegang.",
        )
    if lens_name == "Carl Rogers":
        return (
            "Aku menangkap bagian dirimu yang sedang butuh diterima, bukan diperbaiki dulu. Catatan ini boleh ada tanpa harus langsung menjadi versi yang rapi.",
            "Bagian mana dari dirimu yang paling butuh didengar tanpa dihakimi?",
            "Tulis satu kalimat yang akan kamu ucapkan pada teman jika ia merasakan hal yang sama.",
        )
    if lens_name == "Spiritual":
        return (
            "Ada nada syukur, doa, atau penyerahan di catatan ini. Mungkin hari ini cukup dibawa dengan jujur: apa yang bisa diusahakan, dan apa yang perlu dilepaskan pelan-pelan.",
            "Apa yang ingin kamu usahakan, dan apa yang perlu kamu serahkan malam ini?",
            "Ambil satu menit hening untuk menyebut satu syukur dan satu harapan.",
        )

    if "discipline" in theme_set:
        response = "Ada keinginan untuk menjadi lebih konsisten. Mulailah dari ukuran yang manusiawi, bukan dari standar yang membuatmu cepat lelah."
    else:
        response = "Catatan ini punya arah praktis. Mungkin yang dibutuhkan bukan rencana besar, tapi langkah kecil yang cukup jelas."
    return (
        response,
        "Langkah apa yang paling kecil tapi tetap berarti untuk besok?",
        "Buat satu aksi 10 menit yang realistis, lalu berhenti di sana dulu.",
    )


def _safe_support_response() -> dict[str, Any]:
    return {
        "themes": ["safety"],
        "lens": {
            "name": "Safety Support",
            "source": "supportive care",
            "reason": "Catatan mengarah pada kemungkinan bahaya serius, jadi respons reflektif filosofis tidak digunakan.",
        },
        "response": (
            "Aku menangkap ini sebagai tanda bahwa kamu mungkin sedang berada di titik yang sangat berat. "
            "Kalau ada dorongan untuk menyakiti diri atau kamu merasa tidak aman, hubungi orang terdekat sekarang "
            "atau layanan darurat di tempatmu. Kamu tidak perlu melewati bagian ini sendirian."
        ),
        "question": "Siapa satu orang yang bisa kamu hubungi sekarang agar kamu tidak sendirian?",
        "micro_action": "Jauhkan diri dari hal yang bisa membahayakanmu, lalu kirim pesan singkat ke orang yang kamu percaya.",
    }


def generate_meaning_response(entry: dict[str, Any], recent_entries: list[dict[str, Any]]) -> dict[str, Any]:
    text = " ".join(
        [
            str(entry.get("personal_reflection") or ""),
            str(entry.get("gratitude_note") or ""),
            str(entry.get("improvement_action") or ""),
        ]
    )
    if _contains_self_harm(text):
        return _safe_support_response()

    themes = detect_reflection_themes(text)
    if not themes and int(entry.get("energy_score") or 0) <= 4:
        themes.append("exhaustion")
    if not themes and str(entry.get("life_area") or "").lower() == "kerja":
        themes.append("work pressure")

    lens = select_reflective_lens(
        themes,
        str(entry.get("life_area") or ""),
        str(entry.get("reflection_style") or ""),
    )
    response, question, micro_action = _build_response(themes, lens["name"])

    return {
        "themes": themes,
        "lens": lens,
        "response": response,
        "question": question,
        "micro_action": micro_action,
    }


def serialize_themes(themes: list[str]) -> str:
    return json.dumps(themes, ensure_ascii=False)
