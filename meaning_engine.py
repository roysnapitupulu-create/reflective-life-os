import json
import re
from collections import Counter
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
    "Existential": {
        "source": "existential reflection",
        "reason": "User sedang menyinggung kehilangan arah, pilihan hidup, atau rasa hampa.",
    },
    "Compassionate": {
        "source": "self-compassion practice",
        "reason": "User sedang terdengar keras pada diri sendiri atau merasa tidak cukup.",
    },
    "Gentle Grounding": {
        "source": "gentle grounding practice",
        "reason": "User sedang menyentuh lelah mental dan butuh kembali ke hal yang paling dekat.",
    },
    "Humanistic": {
        "source": "humanistic reflection",
        "reason": "User sedang menulis tentang relasi, kebutuhan didengar, atau konflik antarmanusia.",
    },
    "Philosophical": {
        "source": "philosophical reflection",
        "reason": "User sedang mencari makna, arah, atau cara memahami hidupnya.",
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

STOPWORDS = {
    "aku",
    "yang",
    "dan",
    "di",
    "ke",
    "ini",
    "itu",
    "hari",
    "dengan",
    "untuk",
    "tidak",
    "gak",
    "ga",
    "ada",
    "jadi",
    "karena",
    "rasanya",
    "dalam",
    "dari",
    "masih",
    "sudah",
    "bisa",
    "mau",
    "ingin",
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


def _entry_text(entry: dict[str, Any]) -> str:
    return " ".join(
        [
            str(entry.get("personal_reflection") or ""),
            str(entry.get("gratitude_note") or ""),
            str(entry.get("improvement_action") or ""),
            str(entry.get("activity") or ""),
        ]
    )


def _keywords_from_text(text: str) -> list[str]:
    words = re.findall(r"[a-zA-ZÀ-ÿ]+", text.lower())
    return [word for word in words if len(word) >= 5 and word not in STOPWORDS]


def analyze_reflection_memory(recent_entries: list[dict[str, Any]]) -> dict[str, Any]:
    recent = recent_entries[:7]
    theme_counter: Counter[str] = Counter()
    area_counter: Counter[str] = Counter()
    word_counter: Counter[str] = Counter()
    total_mood = 0
    total_energy = 0
    scored_entries = 0

    for entry in recent:
        text = _entry_text(entry)
        theme_counter.update(detect_reflection_themes(text))
        word_counter.update(_keywords_from_text(text))
        if entry.get("life_area"):
            area_counter.update([str(entry.get("life_area"))])
        if entry.get("mood_score") is not None and entry.get("energy_score") is not None:
            total_mood += int(entry.get("mood_score") or 0)
            total_energy += int(entry.get("energy_score") or 0)
            scored_entries += 1

    average_mood = total_mood / scored_entries if scored_entries else 0
    average_energy = total_energy / scored_entries if scored_entries else 0

    if average_energy and average_energy <= 4:
        tone = "lelah"
    elif average_mood and average_mood <= 4:
        tone = "berat"
    elif "gratitude" in theme_counter:
        tone = "reflektif dan masih mencari pegangan"
    else:
        tone = "tenang bercampur mencari arah"

    return {
        "repeated_themes": [theme for theme, count in theme_counter.most_common(4) if count >= 2],
        "dominant_area": area_counter.most_common(1)[0][0] if area_counter else "",
        "frequent_words": [word for word, count in word_counter.most_common(4) if count >= 2],
        "tone": tone,
    }


def _memory_sentence(memory: dict[str, Any]) -> str:
    repeated_themes = memory.get("repeated_themes") or []
    dominant_area = memory.get("dominant_area") or ""

    if "exhaustion" in repeated_themes:
        return "Belakangan ini aku melihat tema kelelahan beberapa kali muncul."
    if "control" in repeated_themes or "work pressure" in repeated_themes:
        return "Kamu beberapa kali menulis soal tekanan untuk tetap mengendalikan banyak hal."
    if "self-worth" in repeated_themes or "guilt" in repeated_themes:
        return "Ada pola halus tentang cara kamu menilai dirimu sendiri."
    if "relationship" in repeated_themes:
        return "Relasi tampaknya beberapa kali menjadi ruang yang cukup terasa."
    if dominant_area:
        return f"Area {dominant_area.lower()} cukup sering muncul dalam catatan terakhirmu."
    return ""


def select_reflective_lens(themes: list[str], life_area: str, reflection_style: str) -> dict[str, str]:
    theme_set = set(themes)
    normalized_area = str(life_area or "").lower()
    normalized_style = str(reflection_style or "").lower()

    if "faith" in theme_set or "gratitude" in theme_set or normalized_style == "religius":
        lens_name = "Spiritual"
    elif {"control", "work pressure", "anger"} & theme_set:
        lens_name = "Stoic"
    elif {"self-worth", "guilt"} & theme_set:
        lens_name = "Compassionate"
    elif {"relationship", "loneliness"} & theme_set:
        lens_name = "Humanistic"
    elif {"exhaustion", "anxiety"} & theme_set:
        lens_name = "Gentle Grounding"
    elif {"meaning"} & theme_set:
        lens_name = "Philosophical"
    elif {"uncertainty"} & theme_set:
        lens_name = "Existential"
    elif {"anxiety", "fear"} & theme_set:
        lens_name = "Gentle Grounding"
    elif {"discipline"} & theme_set or normalized_area == "pembelajaran":
        lens_name = "Practical Growth"
    else:
        lens_name = "Humanistic"

    return {"name": lens_name, **LENSES[lens_name]}


def _build_response(themes: list[str], lens_name: str, memory: dict[str, Any]) -> tuple[str, str, str]:
    theme_set = set(themes)
    memory_intro = _memory_sentence(memory)
    prefix = f"{memory_intro} " if memory_intro else ""

    if lens_name == "Stoic":
        return (
            prefix
            + "Aku menangkap ada tekanan untuk mengurus banyak hal sekaligus. Lensa Stoic mengajakmu memisahkan mana yang sungguh ada dalam kendalimu hari ini.",
            "Apa satu hal yang sebenarnya tidak harus kamu kendalikan malam ini?",
            "Pilih satu tindakan kecil yang masih bisa kamu lakukan tanpa memaksa seluruh dirimu.",
        )
    if lens_name == "Gentle Grounding":
        return (
            prefix
            + "Aku menangkap lelah yang bukan sekadar fisik. Mungkin malam ini bukan waktunya menekan diri, tapi kembali ke satu hal yang paling dekat dan nyata.",
            "Apa yang tubuhmu butuhkan lebih dulu: diam, tidur, makan, atau ditemani?",
            "Rapikan satu hal kecil di sekitarmu, lalu berhenti sebentar.",
        )
    if lens_name == "Existential":
        return (
            prefix
            + "Ada rasa mencari arah di catatan ini. Lensa existential tidak memaksamu punya jawaban besar; ia hanya mengajakmu melihat pilihan kecil yang masih terasa benar.",
            "Pilihan kecil apa yang paling selaras dengan dirimu sekarang?",
            "Tulis satu hal yang ingin kamu dekati, bukan satu hal yang ingin kamu selesaikan.",
        )
    if lens_name == "Philosophical":
        return (
            prefix
            + "Tulisanmu menyentuh kebutuhan untuk memahami makna, bukan hanya menjalani rutinitas. Mungkin jawabannya belum perlu besar; cukup satu makna kecil yang bisa kamu hormati hari ini.",
            "Apa yang hari ini terasa kecil, tapi tetap bermakna?",
            "Simpan satu kalimat tentang hal yang ingin kamu jaga dalam hidupmu.",
        )
    if lens_name == "Compassionate":
        return (
            prefix
            + "Aku menangkap bagian dirimu yang sedang cukup keras menilai diri sendiri. Lensa compassionate mengajakmu tidak langsung memperbaiki diri, tapi mendengar dulu bagian yang terluka.",
            "Bagian mana dari dirimu yang paling butuh didengar tanpa dihakimi?",
            "Tulis satu kalimat yang akan kamu ucapkan pada teman jika ia merasakan hal yang sama.",
        )
    if lens_name == "Humanistic":
        return (
            prefix
            + "Ada sisi manusiawi yang kuat di sini: kebutuhan untuk dipahami, didengar, atau tidak sendirian membawa semuanya. Itu bukan kelemahan.",
            "Apa yang sebenarnya ingin kamu sampaikan, tapi belum menemukan tempat yang aman?",
            "Kirim satu pesan sederhana atau tulis satu kalimat jujur yang belum sempat keluar.",
        )
    if lens_name == "Spiritual":
        return (
            prefix
            + "Ada nada syukur, doa, atau penyerahan di catatan ini. Mungkin hari ini cukup dibawa dengan jujur: apa yang bisa diusahakan, dan apa yang perlu dilepaskan pelan-pelan.",
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
    memory = analyze_reflection_memory(recent_entries)
    for repeated_theme in memory.get("repeated_themes", []):
        if repeated_theme not in themes:
            themes.append(repeated_theme)

    if not themes and int(entry.get("energy_score") or 0) <= 4:
        themes.append("exhaustion")
    if not themes and str(entry.get("life_area") or "").lower() == "kerja":
        themes.append("work pressure")

    lens = select_reflective_lens(
        themes,
        str(entry.get("life_area") or ""),
        str(entry.get("reflection_style") or ""),
    )
    response, question, micro_action = _build_response(themes, lens["name"], memory)

    return {
        "themes": themes,
        "lens": lens,
        "response": response,
        "question": question,
        "micro_action": micro_action,
        "memory": memory,
    }


def serialize_themes(themes: list[str]) -> str:
    return json.dumps(themes, ensure_ascii=False)
