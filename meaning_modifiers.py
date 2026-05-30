# meaning_modifiers.py

from typing import Any


def apply_tree_modifiers(symbol: str, observation: str, context: dict[str, Any]) -> str:
    emotions = context.get("emotions", [])

    if symbol == "tree":
        if "adversity" in emotions:
            return (
                "Keteduhan terasa paling berarti bukan ketika cuaca sedang baik-baik saja, "
                "tetapi ketika terik sedang menunjukkan seluruh kekuatannya."
            )

    return observation


def apply_urban_survival_modifiers(symbol: str, observation: str, context: dict[str, Any]) -> str:
    emotions = context.get("emotions", [])
    symbols = context.get("symbols", [])

    if symbol != "urban_survival":
        return observation

    if "ojol" in symbols and "lampu_merah" in symbols and "tree" in symbols:
        return (
            "Lampu merah membuat semua kendaraan berhenti sejenak. "
            "Tetapi bagi sebagian orang, berhenti bukan berarti selesai bekerja. "
            "Ada yang tetap menunggu rezeki datang dari arah yang belum terlihat, "
            "berteduh kecil-kecilan di bawah pohon yang tidak banyak bertanya."
        )

    if "ojol" in symbols and "lampu_merah" in symbols:
        return (
            "Di dekat lampu merah, menunggu bukan selalu tanda tidak bergerak. "
            "Bagi sebagian orang, menunggu adalah bentuk lain dari bekerja."
        )

    if "warung" in symbols:
        return (
            "Warung kecil sering menjadi tempat hidup berhenti sebentar. "
            "Di sana, orang tidak hanya membeli sesuatu, tetapi juga meminjam jeda dari hari yang panjang."
        )

    if "gerobak" in symbols:
        return (
            "Gerobak yang berjalan pelan kadang membawa lebih dari dagangan. "
            "Ia membawa ketekunan seseorang yang tetap bergerak meski hari belum tentu mudah."
        )

    if "halte" in symbols:
        return (
            "Halte adalah tempat orang menunggu arah. "
            "Sebagian menunggu kendaraan, sebagian lagi mungkin sedang menunggu hidup sedikit lebih jelas."
        )

    if "adversity" in emotions and "urgency" in emotions:
        return (
            "Di teriknya siang, angkot itu tidak cuma mengejar penumpang. "
            "Ia seperti potret kecil manusia kota yang sedang bernegosiasi "
            "dengan waktu, rezeki, dan kerasnya hukum bertahan hidup."
        )

    if "adversity" in emotions:
        return (
            "Panas membuat perjuangan terlihat lebih telanjang. "
            "Apa yang biasanya disebut rutinitas, ternyata adalah cara seseorang "
            "bertahan di tengah hari yang tidak selalu ramah."
        )

    if "urgency" in emotions:
        return (
            "Tidak semua orang tergesa karena ambisi. "
            "Sebagian tergesa karena hari ini harus cukup untuk menyambung esok."
        )

    return observation


def apply_spiritual_modifiers(symbol: str, observation: str, context: dict[str, Any]) -> str:
    spiritual = context.get("is_spiritual", False)
    emotions = context.get("emotions", [])

    if symbol == "spiritual" and spiritual:
        if "gratitude" in emotions:
            return (
                "Syukur kadang bukan karena semua hal sudah selesai, "
                "melainkan karena hati masih diberi ruang untuk percaya di tengah prosesnya."
            )

    return observation


def apply_meaning_modifiers(symbol: str, observation: str, context: dict[str, Any]) -> str:
    observation = apply_tree_modifiers(symbol, observation, context)
    observation = apply_urban_survival_modifiers(symbol, observation, context)
    observation = apply_spiritual_modifiers(symbol, observation, context)

    return observation