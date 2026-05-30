# scene_composer.py

from typing import Any


def compose_scene_observation(context: dict[str, Any]) -> str:
    scene = context.get("scene") or {}

    actors = scene.get("actors", [])
    actions = scene.get("actions", [])
    settings = scene.get("settings", [])
    objects = scene.get("objects", [])
    supports = scene.get("supporting_symbols", [])

    if (
        "ojol" in actors
        and "menunggu" in actions
        and "order" in objects
        and "lampu_merah" in settings
        and "tree" in supports
    ):
        return (
            "Tidak semua perjalanan dimulai dengan bergerak. "
            "Ada yang dimulai dari seseorang yang sabar menunggu, "
            "di bawah pohon kecil, dekat lampu merah, "
            "sambil berharap layar ponselnya memberi tanda bahwa rezeki sedang mendekat."
        )

    if "ojol" in actors and "menunggu" in actions and "order" in objects:
        return (
            "Ada pekerjaan yang bentuknya bukan selalu bergerak. "
            "Kadang ia berupa menunggu dengan sabar, sambil berharap satu pesanan kecil "
            "cukup untuk membuat hari ini tetap berjalan."
        )

    if "gerobak" in actors and ("berjalan" in actions or "bekerja" in actions):
        return (
            "Gerobak yang berjalan pelan kadang membawa lebih dari dagangan. "
            "Ia membawa ketekunan seseorang yang tetap bergerak meski hari belum tentu mudah."
        )

    if "angkot" in actors and "bekerja" in actions:
        return (
            "Angkot yang berjalan di jalanan kota tidak hanya membawa penumpang. "
            "Ia juga membawa usaha seseorang untuk membuat hari ini cukup sampai malam."
        )

    if "halte" in settings and "menunggu" in actions:
        return (
            "Halte adalah tempat orang menunggu arah. "
            "Sebagian menunggu kendaraan, sebagian lagi mungkin sedang menunggu hidup sedikit lebih jelas."
        )

    if "warung" in settings and "malam" in settings:
        return (
            "Warung kecil yang masih buka di malam hari sering terasa seperti lampu kecil bagi hidup yang belum selesai. "
            "Di sana, seseorang bisa membeli sesuatu, atau sekadar meminjam jeda dari hari yang panjang."
        )

    return ""