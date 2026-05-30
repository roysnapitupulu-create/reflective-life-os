from typing import Any


def _has(context: dict[str, Any], key: str) -> bool:
    return bool(context.get(key))


def _raw(context: dict[str, Any]) -> str:
    return str(context.get("raw_text") or "").lower()


def synthesize_meaning(context: dict[str, Any]) -> str:
    text = _raw(context)

    has_morning = context.get("time_context") == "pagi"
    has_spiritual = _has(context, "is_spiritual")
    has_simple = _has(context, "is_simple_life")
    has_gratitude = _has(context, "has_gratitude")
    has_slow = _has(context, "has_slow_pace")

    has_togetherness = any(
        word in text
        for word in [
            "bersama",
            "istri",
            "keluarga",
            "umat",
            "gereja",
            "kebaktian",
            "melayani",
            "pembeli",
        ]
    )

    has_food = any(
        word in text
        for word in [
            "bubur",
            "sarapan",
            "makan",
            "mangkok",
            "pagi",
        ]
    )

    if has_food and has_togetherness and has_gratitude:
        return (
            "Kadang yang membuat pagi terasa berharga bukan apa yang tersaji, "
            "melainkan siapa yang hadir dan ikut membuatnya bermakna."
        )

    if has_morning and has_spiritual and has_gratitude:
        return (
            "Pagi ini seperti mengingatkan bahwa syukur tidak selalu datang dari hal besar. "
            "Kadang ia tumbuh dari kehadiran kecil yang dijalani dengan hati pelan."
        )

    if has_simple and has_gratitude and has_slow:
        return (
            "Kesederhanaan hari ini tampaknya sedang mengajari satu hal: "
            "hidup tidak harus tergesa untuk terasa penuh."
        )

    if has_spiritual and has_togetherness:
        return (
            "Ada pertemuan yang bukan hanya soal hadir di tempat yang sama, "
            "tetapi tentang hati yang belajar datang dengan lebih utuh."
        )

    if has_simple and has_morning:
        return (
            "Pagi sering menyimpan makna dalam bentuk yang sangat biasa: "
            "jalan kecil, makanan sederhana, dan waktu yang belum terburu-buru."
        )

    if has_gratitude:
        return (
            "Ada rasa syukur kecil yang muncul di tengah hari ini. "
            "Mungkin ia tidak perlu dijelaskan panjang, cukup dijaga agar tidak lewat begitu saja."
        )

    if has_slow:
        return (
            "Tidak semua hal perlu segera diberi jawaban. "
            "Sebagian hari hanya meminta dijalani pelan-pelan sampai maknanya tampak sendiri."
        )

    return (
        "Ada hal kecil yang tidak perlu langsung dijelaskan. "
        "Cukup disimpan sebagai tanda bahwa hari ini pernah hadir."
    )


def synthesize_side_note(context: dict[str, Any]) -> str:
    return synthesize_meaning(context)