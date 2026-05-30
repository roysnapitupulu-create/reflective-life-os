# life_observation_library.py
from __future__ import annotations

import random


LIFE_OBSERVATION_LIBRARY = {
    "tree": {
        "reflective": [
            "Pohon tidak pernah terburu-buru menjadi besar. Ia hanya setia tumbuh, sedikit demi sedikit, bahkan ketika tidak ada yang memperhatikan.",
            "Keteduhan sering datang dari sesuatu yang diam, berakar, dan tidak banyak menjelaskan dirinya.",
            "Pohon mengajarkan bahwa kekuatan tidak selalu perlu bergerak cepat. Kadang ia cukup berdiri, memberi ruang bagi yang lelah.",
        ],
        "micro_wonder": [
            "Kadang satu pohon cukup untuk membuat siang terasa tidak sepenuhnya keras.",
            "Daun-daun kecil bisa menjadi cara bumi berbisik bahwa dunia belum seluruhnya kasar.",
        ],
        "gentle_humor": [
            "Pohon itu mungkin tidak pernah ikut seminar produktivitas, tapi ia tahu cara bertumbuh tanpa panik.",
            "Kalau pohon bisa bicara, mungkin ia cuma bilang: pelan-pelan saja, yang penting tetap berakar.",
        ],
        "philosophical_humor": [
            "Pohon tidak punya kalender target tahunan, tapi anehnya ia tetap berhasil menjadi dirinya sendiri.",
            "Manusia sering sibuk mencari makna hidup, sementara pohon sudah lama mempraktikkannya: diam, tumbuh, memberi teduh.",
        ],
    },
    "thinkpad": {
        "reflective": [
            "ThinkPad tua kadang seperti saksi sunyi dari pikiran yang belum selesai, pekerjaan yang bertumpuk, dan kesetiaan kecil pada alat yang masih bisa diandalkan.",
            "Ada benda-benda yang tidak sekadar dipakai. Ia ikut menyimpan ritme hidup, jejak kerja, dan percakapan panjang dengan diri sendiri.",
        ],
        "micro_wonder": [
            "Di balik tombol keyboard yang mulai aus, ada banyak hari yang pernah diselesaikan pelan-pelan.",
            "Kadang benda sederhana terasa hidup karena terlalu sering menemani manusia berpikir.",
        ],
        "gentle_humor": [
            "ThinkPad itu seperti kawan lama: tampilannya tidak sok cantik, tapi kalau diajak kerja masih tahu diri.",
            "Ada laptop yang ingin terlihat mewah. Ada ThinkPad yang hanya ingin menyelesaikan pekerjaan.",
        ],
        "philosophical_humor": [
            "ThinkPad mungkin tidak menjanjikan keindahan, tapi ia menawarkan sesuatu yang lebih langka: ketahanan tanpa banyak drama.",
            "Di zaman perangkat ingin tampak seperti perhiasan, ThinkPad tetap seperti palu: tidak genit, tapi berguna.",
        ],
    },
    "urban_survival": {
        "reflective": [
            "Di jalanan, waktu bukan sekadar jam. Ia bisa berubah menjadi kesempatan yang harus segera ditangkap sebelum lewat.",
            "Ada orang-orang yang tidak sedang mengejar kemenangan besar. Mereka hanya sedang memastikan hari ini cukup untuk dilanjutkan sampai besok.",
            "Angkot yang mengejar penumpang kadang terlihat seperti kendaraan biasa, padahal ia sedang membawa kecemasan kecil tentang dapur, waktu, dan bertahan hidup.",
        ],
        "micro_wonder": [
            "Kadang kota menyimpan puisinya bukan di taman, tapi di kaca depan angkot yang berdebu.",
            "Di balik klakson dan panas jalanan, ada manusia yang sedang berdamai dengan kerasnya hari.",
        ],
        "gentle_humor": [
            "Angkot itu seperti filsuf jalanan: tidak banyak teori, tapi tahu bahwa hidup harus tetap jalan walau panas.",
            "Survival of the fittest versi kota kadang sederhana: siapa cepat dapat penumpang, siapa sabar dapat cerita.",
        ],
        "philosophical_humor": [
            "Darwin mungkin tidak membayangkan teorinya akan ikut naik angkot di siang bolong.",
            "Di jalanan kota, evolusi kadang berbentuk sopir yang hafal kapan harus ngebut, kapan harus sabar, dan kapan harus pura-pura tidak mendengar klakson.",
        ],
    },
    "spiritual": {
        "reflective": [
            "Kadang iman tidak datang sebagai jawaban besar, melainkan sebagai ruang kecil untuk tetap bernapas di tengah hal yang belum selesai.",
            "Kehadiran Tuhan tidak selalu menghapus pergumulan. Kadang Ia membuat hati cukup kuat untuk tinggal sebentar di dalamnya.",
        ],
        "micro_wonder": [
            "Ada doa yang tidak mengubah keadaan seketika, tapi mengubah cara hati menatap keadaan itu.",
            "Kadang yang paling menenangkan bukan masalah yang selesai, melainkan rasa bahwa kita tidak sendirian menjalaninya.",
        ],
        "gentle_humor": [
            "Tuhan kadang tidak menjawab secepat notifikasi, tapi anehnya hati tetap bisa dibuat tenang.",
            "Doa itu bukan tombol darurat semata. Kadang ia seperti kursi kecil untuk duduk sebentar di tengah ributnya hidup.",
        ],
        "philosophical_humor": [
            "Manusia ingin jawaban final. Tuhan sering memberi cukup terang untuk satu langkah dulu.",
            "Mungkin iman adalah seni berjalan tanpa seluruh peta, tapi dengan keyakinan bahwa jalan tidak sedang kosong.",
        ],
    },
}


TEXT_SYMBOL_KEYWORDS = {
    "tree": ["pohon", "mangga", "keteduhan", "teduh", "daun", "akar"],
    "thinkpad": ["thinkpad", "laptop", "keyboard", "layar", "komputer"],
    "urban_survival": [
        "angkot", "mobil angkot", "penumpang", "terminal", "halte",
        "ojek", "ojol", "pedagang", "warung", "gerobak",
        "berburu waktu", "mengejar", "survival", "fittest",
        "nafkah", "rezeki", "jalanan",
    ],
    "spiritual": ["tuhan", "doa", "iman", "rahmat", "syukur", "gereja", "masjid", "berkat", "kasih"],
}


def get_observations(symbol: str, voice: str = "reflective") -> list[str]:
    symbol_pack = LIFE_OBSERVATION_LIBRARY.get(symbol)

    if not symbol_pack:
        return []

    return symbol_pack.get(voice) or symbol_pack.get("reflective", [])


def detect_symbol_from_text(text: str) -> str | None:
    normalized = str(text or "").lower()

    for symbol, keywords in TEXT_SYMBOL_KEYWORDS.items():
        if any(keyword in normalized for keyword in keywords):
            return symbol

    return None


def pick_life_observation(text: str, voice: str = "reflective") -> str:
    """Backward-compatible function expected by meaning_synthesizer.py."""
    symbol = detect_symbol_from_text(text)
    if not symbol:
        return ""

    observations = get_observations(symbol, voice=voice)
    if not observations:
        return ""

    seed = sum(ord(char) for char in str(text or ""))
    return observations[seed % len(observations)]

def pick_life_observation(symbol: str, voice: str = "reflective") -> str:
    observations = get_observations(symbol, voice)

    if not observations:
        return ""

    seed = sum(ord(char) for char in f"{symbol}:{voice}") % len(observations)
    return observations[seed]