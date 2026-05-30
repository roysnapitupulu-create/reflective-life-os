from typing import Any


LIFE_OBSERVATION_LIBRARY: dict[str, dict[str, Any]] = {
    "tree": {
        "signals": ["pohon", "daun", "akar", "rindang", "teduh", "keteduhan"],
        "symbols": ["keteduhan", "ketahanan", "pertumbuhan"],
        "reflective": [
            "Keteduhan tidak selalu lahir dari tempat yang teduh. Kadang ia datang dari sesuatu yang tetap berdiri di bawah terik.",
        ],
        "micro_wonder": [
            "Pohon tidak menghentikan matahari. Ia hanya membuat dunia sedikit lebih ramah di bawahnya.",
        ],
        "gentle_humor": [
            "Pohon ini tampaknya sudah cukup lama hidup untuk tahu bahwa tidak semua musim perlu ditanggapi dengan panik.",
        ],
        "philosophical_humor": [
            "Pohon ini tampaknya tidak terlalu memikirkan determinisme. Ia memilih tumbuh saja, lalu membiarkan para filsuf berdebat di bawah keteduhannya.",
        ],
    },
    "street_food": {
        "signals": ["gerobak", "bubur", "sarapan", "pedagang", "pembeli", "warung"],
        "symbols": ["kesederhanaan", "nafkah", "ritme pagi"],
        "reflective": [
            "Kesederhanaan sering memulai hari lebih awal daripada yang kita sadari.",
        ],
        "micro_wonder": [
            "Sebelum kota benar-benar sibuk, ada orang-orang yang sudah menyiapkan sarapan untuknya.",
        ],
        "gentle_humor": [
            "Gerobak bubur punya kemampuan membuat orang yang tadinya tidak lapar mulai mempertimbangkan ulang hidupnya.",
        ],
        "philosophical_humor": [
            "Kalau Socrates lahir di gang kecil, mungkin ia akan mulai dialognya dari semangkuk bubur.",
        ],
    },
    "coffee": {
        "signals": ["kopi", "cangkir", "ngopi", "espresso", "americano"],
        "symbols": ["jeda", "ritual", "percakapan"],
        "reflective": [
            "Kadang secangkir kopi bukan soal kafein, tetapi cara kecil untuk kembali hadir.",
        ],
        "micro_wonder": [
            "Kopi punya cara sederhana membuat waktu terasa punya pegangan.",
        ],
        "gentle_humor": [
            "Kopi sering terlihat seperti minuman, padahal kadang ia adalah tombol restart yang menyamar.",
        ],
        "philosophical_humor": [
            "Descartes mungkin berkata: aku berpikir, maka aku butuh kopi dulu.",
        ],
    },
    "rain": {
        "signals": ["hujan", "gerimis", "rinai", "basah", "payung"],
        "symbols": ["jeda", "pemulihan", "pembersihan"],
        "reflective": [
            "Hujan kadang tidak menyelesaikan apa-apa. Ia hanya memberi dunia alasan untuk melambat.",
        ],
        "micro_wonder": [
            "Ada suara-suara kecil dari langit yang membuat hari terasa lebih pelan.",
        ],
        "gentle_humor": [
            "Hujan punya bakat membuat rencana manusia terlihat terlalu percaya diri.",
        ],
        "philosophical_humor": [
            "Camus mungkin tetap mendorong batunya. Tapi kalau hujan begini, ia mungkin membawa payung cadangan.",
        ],
    },
    "thinkpad": {
        "signals": ["thinkpad", "laptop", "keyboard", "terminal", "kode", "coding"],
        "symbols": ["kerja sunyi", "ketekunan", "alat berpikir"],
        "reflective": [
            "Ada pekerjaan yang tidak terlihat ramai, tetapi tetap meninggalkan jejak.",
        ],
        "micro_wonder": [
            "Keyboard ini mungkin sudah menyimpan lebih banyak cerita daripada yang terlihat di layar.",
        ],
        "gentle_humor": [
            "ThinkPad selalu terlihat seperti sedang mengerjakan sesuatu yang penting, bahkan ketika sebenarnya cuma membuka playlist lagu galau.",
        ],
        "philosophical_humor": [
            "Descartes mungkin berkata aku berpikir maka aku ada. ThinkPad ini menjawab: aku panas, maka aku bekerja.",
        ],
    },
    "cable": {
        "signals": ["kabel", "charger", "colokan", "adapter"],
        "symbols": ["koneksi", "ketergantungan kecil", "kekusutan"],
        "reflective": [
            "Kadang hal kecil yang menghubungkan justru paling mudah diabaikan.",
        ],
        "micro_wonder": [
            "Kabel tampak diam, padahal tugasnya membawa tenaga dari satu tempat ke tempat lain.",
        ],
        "gentle_humor": [
            "Kabel selalu punya bakat menemukan cara baru untuk saling merindukan.",
        ],
        "philosophical_humor": [
            "Socrates mungkin akan bertanya apa itu keterhubungan. Kabel ini memilih menjawab dengan kusut.",
        ],
    },
}


PHILOSOPHY_SIGNALS = [
    "eksistensi", "eksistensial", "absurd", "makna", "socrates",
    "descartes", "camus", "nietzsche", "kierkegaard", "filsafat",
]


def detect_observation_symbols(text: str) -> list[dict[str, Any]]:
    normalized = str(text or "").lower()
    matches = []

    for key, item in LIFE_OBSERVATION_LIBRARY.items():
        score = sum(1 for signal in item["signals"] if signal in normalized)
        if score:
            matches.append({"key": key, "score": score, **item})

    return sorted(matches, key=lambda item: item["score"], reverse=True)


def detect_voice_register(text: str) -> str:
    normalized = str(text or "").lower()

    if any(signal in normalized for signal in PHILOSOPHY_SIGNALS):
        return "philosophical_humor"

    if any(word in normalized for word in ["wkwk", "haha", "lucu", "receh", "nyengir"]):
        return "gentle_humor"

    if any(word in normalized for word in ["syukur", "tuhan", "doa", "ibadah", "gereja", "iman"]):
        return "reflective"

    return "micro_wonder"


def pick_life_observation(text: str) -> str:
    symbols = detect_observation_symbols(text)
    if not symbols:
        return ""

    voice = detect_voice_register(text)
    symbol = symbols[0]

    candidates = symbol.get(voice) or symbol.get("micro_wonder") or symbol.get("reflective") or []
    return candidates[0] if candidates else ""