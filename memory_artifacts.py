from pathlib import Path
import random
from typing import Any


MAX_IMAGE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp", "image/heic", "image/heif"}
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}

SIDE_NOTE_CATEGORIES = {
    "teknologi": [
        "Visual Studio Code pertama kali dirilis pada tahun 2015.",
        "Git dibuat pada tahun 2005 untuk membantu pengembangan kernel Linux.",
        "Istilah bug dalam komputer sudah dipakai sebelum komputer modern ada.",
        "Wi-Fi tidak berarti wireless fidelity; nama itu dipilih karena mudah diingat.",
        "QR code pertama kali dibuat di Jepang untuk melacak komponen otomotif.",
        "Bluetooth dinamai dari Harald Bluetooth, seorang raja Denmark abad ke-10.",
        "USB pertama kali diperkenalkan pada pertengahan 1990-an untuk menyederhanakan koneksi perangkat.",
        "Emoji pertama di ponsel dibuat di Jepang pada akhir 1990-an.",
        "Kabel serat optik membawa data sebagai pulsa cahaya.",
        "Baterai lithium-ion menjadi umum karena ringan dan bisa diisi ulang berkali-kali.",
    ],
    "komputer": [
        "Visual Studio Code pertama kali dirilis pada tahun 2015.",
        "Banyak perangkat lunak yang digunakan jutaan orang setiap hari pernah ditulis di editor kode biasa.",
        "Simbol $ dan > di terminal adalah bagian dari tradisi komputasi yang sudah puluhan tahun.",
        "Desain ThinkPad terinspirasi dari kotak makan siang bento Jepang.",
        "TrackPoint merah kecil di tengah keyboard ThinkPad punya penggemar yang sangat setia.",
        "Tata letak QWERTY populer sejak era mesin tik mekanik.",
        "Tombol Escape berasal dari kebutuhan untuk keluar dari mode atau perintah tertentu.",
        "Keyboard mekanik memakai switch terpisah di bawah tiap tombol.",
        "Banyak keyboard laptop memakai mekanisme gunting kecil di bawah tombolnya.",
        "Touchpad laptop modern bisa membaca beberapa titik sentuhan sekaligus.",
        "Monitor LCD bekerja dengan mengatur cahaya melalui kristal cair.",
        "Pixel adalah singkatan dari picture element.",
        "Kipas laptop kecil bisa berputar ribuan kali per menit saat suhu naik.",
        "SSD tidak memiliki piringan berputar seperti hard disk lama.",
        "RAM menyimpan data sementara agar komputer bisa bekerja cepat.",
        "Port HDMI membawa audio dan video lewat satu kabel.",
        "Webcam laptop biasanya memakai sensor gambar yang sangat kecil.",
    ],
    "perangkat kerja": [
        "Meja kerja sering menyimpan jejak proyek yang tidak pernah terlihat oleh orang lain.",
        "Kursi kantor modern banyak dipengaruhi riset ergonomi abad ke-20.",
        "Lampu meja awalnya populer karena orang mulai bekerja dan membaca lebih lama di dalam ruangan.",
        "Monitor eksternal membuat orang bisa melihat lebih banyak konteks tanpa berpindah jendela.",
        "Mouse komputer pertama dibuat dari kayu.",
        "Mouse wheel baru menjadi umum pada akhir 1990-an.",
        "Kabel kusut sering terjadi karena benda fleksibel mudah membentuk simpul saat bergerak bebas.",
        "Router rumah kecil melakukan banyak pekerjaan diam-diam: menerima, mengirim, dan mengatur paket data.",
        "Headphone noise-cancelling awalnya dikembangkan untuk mengurangi bising di lingkungan penerbangan.",
        "Sticky note ditemukan setelah lem yang awalnya dianggap terlalu lemah ternyata berguna.",
        "Binder clip ditemukan pada awal abad ke-20 dan bentuknya hampir tidak banyak berubah.",
        "Whiteboard mulai populer di kantor setelah spidol non-permanen menjadi mudah digunakan.",
    ],
    "alat tulis": [
        "Pensil tidak mengandung timah. Isinya terutama grafit dan tanah liat.",
        "Penghapus karet menjadi umum setelah karet alam mulai dipakai untuk menghapus grafit.",
        "Pulpen ballpoint memakai bola kecil untuk menggulung tinta ke kertas.",
        "Kertas dibuat dari serat yang saling mengikat saat airnya mengering.",
        "Klip kertas punya banyak variasi bentuk, tetapi desain Gem clip menjadi salah satu yang paling dikenal.",
        "Stabilo pertama kali populer karena tinta neon membuat teks mudah ditemukan kembali.",
        "Penggaris kayu dan logam sudah lama dipakai sebelum plastik menjadi umum.",
        "Buku catatan spiral memudahkan halaman dibuka rata di atas meja.",
        "Tinta permanen biasanya dirancang agar lebih tahan air dan cahaya.",
        "Karbon pada kertas karbon memungkinkan satu tulisan menyalin diri ke lembar lain.",
    ],
    "rumah": [
        "Kunci rumah modern bekerja dengan pin kecil yang harus sejajar di dalam silinder.",
        "Engsel pintu adalah salah satu mekanisme sederhana yang sudah dipakai selama ribuan tahun.",
        "Kaca jendela menjadi jauh lebih umum setelah teknik produksi kaca semakin murah.",
        "Keramik mug mengeras karena tanah liat berubah saat dibakar pada suhu tinggi.",
        "Kulkas rumah tangga mengubah cara orang menyimpan makanan sehari-hari.",
        "Jam dinding kuarsa menjaga waktu dengan getaran kristal kecil.",
        "Kipas angin memindahkan udara; ia tidak menurunkan suhu ruangan secara langsung.",
        "Sakelar lampu membuat rangkaian listrik terbuka atau tertutup.",
        "Spons dapur penuh rongga kecil yang membuatnya mudah menyerap air.",
        "Sabun bekerja karena molekulnya punya sisi yang menyukai air dan sisi yang menyukai minyak.",
    ],
    "benda sehari-hari": [
        "Coffee trees can live for decades.",
        "The smell after rain has a name: petrichor.",
        "Many old books release compounds similar to vanilla.",
        "Clouds can weigh hundreds of thousands of kilograms.",
        "A single sheet of paper can be folded only a limited number of times by hand.",
        "The first umbrellas were often used for shade before rain.",
        "Some seashells keep growing in a spiral because one side grows faster than the other.",
        "Bread gets its airy texture from tiny pockets of carbon dioxide.",
        "Tea leaves and white tea can come from the same plant.",
        "The word window comes from an old phrase meaning wind eye.",
        "Rainbows are full circles, but the ground usually hides the lower half.",
        "Old film photographs are made from tiny light-sensitive crystals.",
        "Many city streets are warmer at night because stone and asphalt hold heat.",
        "Paper was invented long before bound books became common.",
        "Some stars visible tonight may no longer exist in the same form.",
        "The color of sunset changes as light travels through more atmosphere.",
        "Denim was originally valued because it was sturdy work fabric.",
        "A candle flame has different colors because its parts burn at different temperatures.",
        "Glass is made mostly from sand heated until it changes form.",
        "The scent of fresh-cut grass comes from compounds plants release when damaged.",
        "Some flowers close at night in a movement called nyctinasty.",
        "Salt was once valuable enough to shape trade routes.",
        "A handwritten line carries small pressure changes from the writer's hand.",
        "Zippers became common on clothing after they were first used more often on boots and bags.",
        "Velcro was inspired by tiny burrs that stick to fabric and fur.",
    ],
}

KEYWORD_CATEGORIES = {
    "teknologi": [
        "bluetooth",
        "wifi",
        "wi-fi",
        "usb",
        "qr",
        "baterai",
        "battery",
        "kabel",
        "charger",
        "internet",
        "teknologi",
    ],
    "komputer": [
        "laptop",
        "thinkpad",
        "vscode",
        "vs code",
        "visual studio code",
        "ngoding",
        "coding",
        "code",
        "terminal",
        "keyboard",
        "monitor",
        "komputer",
        "pc",
        "ssd",
        "ram",
        "webcam",
    ],
    "perangkat kerja": [
        "meja",
        "desk",
        "kerja",
        "work",
        "router",
        "mouse",
        "headphone",
        "kursi",
        "lampu",
        "sticky",
        "whiteboard",
        "clip",
    ],
    "alat tulis": [
        "pensil",
        "pulpen",
        "pena",
        "buku",
        "notebook",
        "catatan",
        "kertas",
        "penghapus",
        "stabilo",
        "penggaris",
        "tinta",
    ],
    "rumah": [
        "rumah",
        "pintu",
        "jendela",
        "kunci",
        "mug",
        "gelas",
        "kulkas",
        "jam",
        "kipas",
        "lampu",
        "sakelar",
        "sabun",
        "dapur",
    ],
    "benda sehari-hari": [
        "kopi",
        "coffee",
        "hujan",
        "rain",
        "langit",
        "sky",
        "makanan",
        "food",
        "roti",
        "bread",
        "teh",
        "tea",
        "payung",
        "umbrella",
        "jalan",
        "street",
        "baju",
        "denim",
        "foto",
    ],
}

SIDE_NOTES = [
    side_note
    for category_notes in SIDE_NOTE_CATEGORIES.values()
    for side_note in category_notes
]


def _matching_categories(context: str) -> list[str]:
    normalized_context = context.lower()
    matches: list[str] = []
    for category, keywords in KEYWORD_CATEGORIES.items():
        if any(keyword in normalized_context for keyword in keywords):
            matches.append(category)
    return matches


def choose_side_note(memory_note: str = "", filename: str = "") -> str:
    context = f"{memory_note} {filename}".strip()
    matches = _matching_categories(context)
    if matches:
        category = random.choice(matches)
        return random.choice(SIDE_NOTE_CATEGORIES[category])
    return random.choice(SIDE_NOTES)


def get_image_extension(filename: str, mime_type: str = "") -> str:
    extension = Path(str(filename or "")).suffix.lower()
    if extension in ALLOWED_IMAGE_EXTENSIONS:
        return extension
    if mime_type in {"image/heic", "image/heif"}:
        return ".heic"
    if mime_type == "image/png":
        return ".png"
    if mime_type == "image/webp":
        return ".webp"
    return ".jpg"


def validate_image_upload(uploaded_file: Any) -> str | None:
    if uploaded_file is None:
        return None

    mime_type = str(getattr(uploaded_file, "type", "") or "")
    extension = Path(str(getattr(uploaded_file, "name", "") or "")).suffix.lower()
    if mime_type not in ALLOWED_IMAGE_TYPES and extension not in ALLOWED_IMAGE_EXTENSIONS:
        if mime_type.startswith("image/"):
            return None
        return "Foto perlu berupa file gambar dari kamera atau galeri."

    try:
        size = int(getattr(uploaded_file, "size", 0) or 0)
    except (TypeError, ValueError):
        size = 0
    if size > MAX_IMAGE_BYTES:
        return "Ukuran foto maksimal 10 MB untuk versi awal ini."

    return None
