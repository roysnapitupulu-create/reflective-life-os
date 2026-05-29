from pathlib import Path
import random
from typing import Any


MAX_IMAGE_BYTES = 10 * 1024 * 1024
ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/jpg", "image/png", "image/webp", "image/heic", "image/heif"}
ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".heic", ".heif"}

SIDE_NOTE_LIBRARY = {
    "teknologi": {
        "fakta": [
            "Bluetooth dinamai dari Harald Bluetooth, raja Denmark abad ke-10.",
            "Kode QR pertama kali dibuat di Jepang untuk melacak komponen otomotif.",
            "USB diperkenalkan untuk membuat koneksi perangkat tidak terlalu memusingkan.",
            "Serat optik membawa data sebagai pulsa cahaya.",
            "Baterai lithium-ion menjadi populer karena ringan dan bisa diisi ulang berkali-kali.",
            "Wi-Fi bukan singkatan resmi; namanya dipilih agar mudah diingat.",
            "Layar sentuh kapasitif membaca perubahan listrik kecil dari jari.",
            "Ponsel modern punya lebih banyak sensor daripada yang biasanya terlihat dari luar.",
            "Kamera ponsel memakai sensor kecil yang sangat sibuk menangkap cahaya.",
            "Mode pesawat awalnya dibuat agar perangkat tidak memancarkan sinyal radio tertentu.",
        ],
        "micro_wonder": [
            "Ada cahaya kecil yang bolak-balik di dalam kabel serat optik, membawa pesan yang tidak terlihat.",
            "Satu notifikasi bisa melintasi beberapa server sebelum muncul sebagai bunyi kecil.",
            "Baterai tampak diam, padahal di dalamnya ion sedang berpindah tempat.",
            "Kabel pengisi daya terlihat sederhana, tapi diam-diam ia bernegosiasi soal daya.",
            "Kode QR itu seperti labirin kecil yang justru dibuat agar mesin tidak tersesat.",
            "Sinyal Wi-Fi memenuhi ruangan tanpa pernah meminta kursi.",
            "Layar yang gelap tetap menyimpan kemungkinan ribuan warna.",
            "Tombol daya kecil itu punya tugas yang agak dramatis: membangunkan seluruh mesin.",
            "Nama Bluetooth datang dari sejarah tua, lalu hidup lagi di telinga nirkabel.",
            "Benda paling modern kadang masih bergantung pada colokan yang sangat biasa.",
        ],
        "genit_bermartabat": [
            "Kabel selalu punya bakat menjadi kusut bahkan ketika tidak ada yang mengundangnya.",
            "Charger adalah benda kecil yang sering dicari tepat ketika baterai mulai bersikap tegang.",
            "Wi-Fi punya cara halus untuk membuat satu rumah langsung sadar saat ia menghilang.",
            "Kode QR terlihat seperti teka-teki, tapi sebenarnya cuma ingin dipindai dengan sopan.",
            "Bluetooth kadang seperti pertemanan lama: sudah dipasangkan, tapi tetap bisa pura-pura lupa.",
            "Power bank membawa energi cadangan dengan gaya yang sangat rendah hati.",
            "Kabel yang rapi adalah peristiwa langka yang pantas dicatat sebentar.",
            "Adaptor kecil sering menjadi diplomat antara lubang colokan yang tidak sepaham.",
            "Lampu indikator mungil itu pandai sekali membuat orang bertanya, ini menyala atau tidak.",
            "Teknologi paling canggih pun masih sering kalah oleh pertanyaan: kabelnya mana?",
        ],
    },
    "laptop": {
        "fakta": [
            "Desain ThinkPad terinspirasi dari kotak makan siang bento Jepang.",
            "TrackPoint merah di ThinkPad dikenal sebagai salah satu ciri paling mudah dikenali.",
            "Banyak laptop memakai mekanisme engsel yang diuji ribuan kali buka-tutup.",
            "Laptop modern sering mengatur kecepatan kipas berdasarkan suhu prosesor.",
            "SSD tidak memakai piringan berputar seperti hard disk lama.",
            "RAM menyimpan data sementara agar komputer bisa bekerja cepat.",
            "Touchpad modern bisa membaca beberapa titik sentuhan sekaligus.",
            "Banyak keyboard laptop memakai mekanisme gunting kecil di bawah tombol.",
            "Webcam laptop biasanya memakai sensor yang sangat kecil.",
            "Port HDMI membawa audio dan video lewat satu kabel.",
        ],
        "micro_wonder": [
            "Di balik layar laptop, jutaan piksel kecil menunggu giliran menyala.",
            "Kipas laptop kecil bisa terdengar seperti mesin mungil yang sedang berunding dengan panas.",
            "Satu engsel laptop memikul banyak pagi, malam, dan buka-tutup yang tidak dihitung.",
            "TrackPoint merah itu kecil, tapi reputasinya tidak kecil.",
            "SSD bekerja tanpa suara, seolah semua file disimpan di ruangan yang sangat tenang.",
            "Keyboard laptop menyimpan jejak tekanan jari tanpa pernah bercerita.",
            "Layar laptop adalah jendela yang tidak menghadap keluar, tapi sering membawa dunia masuk.",
            "Lampu kecil di tombol daya kadang terasa seperti napas mesin.",
            "Stiker di laptop sering menjadi arsip kecil dari hal-hal yang pernah disukai.",
            "Baterai laptop menghitung waktu dengan cara yang sedikit menegangkan.",
        ],
        "genit_bermartabat": [
            "Tombol merah kecil itu membuat foto ini sulit menyamar sebagai selain ThinkPad.",
            "ThinkPad punya aura tas kantor yang diam-diam pernah membaca banyak dokumen.",
            "Laptop yang sedikit panas selalu punya cara mengumumkan bahwa ia juga sedang bekerja.",
            "Keyboard laptop tua kadang terdengar seperti sedang mengetik dengan pendirian.",
            "Engsel laptop adalah bagian yang paling sering diajak kompromi tanpa diminta pendapatnya.",
            "TrackPoint merah itu kecil, tapi ia berjalan seperti punya klub penggemar rahasia.",
            "Laptop hitam selalu tampak seperti sudah siap ikut rapat, bahkan saat cuma membuka musik.",
            "Stiker di laptop adalah tato kecil untuk mesin yang terlalu sopan.",
            "Touchpad boleh luas, tapi sebagian orang tetap setia pada titik merah mungil itu.",
            "Kipas laptop tidak dramatis. Ia hanya suka membuat keberadaannya diketahui.",
        ],
    },
    "programmer": {
        "fakta": [
            "Visual Studio Code pertama kali dirilis pada tahun 2015.",
            "Git dibuat pada tahun 2005 untuk membantu pengembangan kernel Linux.",
            "Istilah bug sudah dipakai dalam dunia teknik sebelum komputer modern populer.",
            "Terminal teks sudah menjadi bagian dari komputasi jauh sebelum antarmuka grafis umum.",
            "Simbol $ dan > di terminal berasal dari tradisi panjang baris perintah.",
            "Commit di Git menyimpan potret perubahan pada satu titik waktu.",
            "Nama Python terinspirasi dari grup komedi Monty Python.",
            "JavaScript pertama kali dibuat dalam waktu yang sangat singkat pada 1995.",
            "Banyak server di internet menjalankan sistem berbasis Unix atau Linux.",
            "Ekstensi editor kode bisa mengubah editor sederhana menjadi lingkungan kerja lengkap.",
        ],
        "micro_wonder": [
            "Satu titik koma kecil kadang punya kekuasaan yang tidak masuk akal.",
            "Terminal tampak kosong, padahal ia sedang menunggu perintah dengan sabar sekali.",
            "Commit kecil bisa menjadi penanda bahwa sesuatu pernah berubah di sini.",
            "Bug sering bersembunyi bukan di tempat rumit, tapi di baris yang terlihat terlalu polos.",
            "Warna-warna di editor kode membantu mata menemukan pola sebelum pikiran sempat lelah.",
            "Satu pesan error kadang lebih jujur daripada dokumentasi panjang.",
            "Branch di Git seperti jalan samping yang bisa kembali, bisa juga menjadi cerita sendiri.",
            "Kursor yang berkedip punya cara sederhana untuk bilang: lanjut?",
            "Deploy terdengar besar, padahal kadang dimulai dari tombol yang sangat kecil.",
            "Log aplikasi adalah jejak kaki kecil dari sesuatu yang baru saja terjadi.",
        ],
        "genit_bermartabat": [
            "Tidak semua pahlawan memakai jubah. Sebagian hanya memakai Ctrl+C dan Ctrl+V.",
            "Terminal terlihat galak, tapi sebenarnya cuma menunggu diketik dengan benar.",
            "Bug punya bakat muncul tepat ketika semuanya terasa hampir selesai.",
            "Commit message pendek kadang menyimpan drama yang lebih panjang dari isinya.",
            "VSCode punya kemampuan membuat satu folder terasa seperti semesta kecil.",
            "Deploy adalah momen ketika kode berhenti menjadi teori dan mulai mencari masalah sendiri.",
            "Branch yang namanya rapi belum tentu hidupnya rapi.",
            "Error merah punya cara masuk ruangan tanpa mengetuk.",
            "Kursor berkedip itu seperti teman yang sabar, tapi sedikit menghakimi benda mati.",
            "Komentar TODO adalah janji kecil yang sering punya umur panjang.",
            "Stack trace panjang kadang terlihat seperti puisi yang sedang marah.",
            "Pull request bisa terlihat sederhana sampai percakapan mulai tumbuh di bawahnya.",
        ],
    },
    "spreadsheet": {
        "fakta": [
            "Spreadsheet elektronik populer jauh sebelum banyak aplikasi kerja modern muncul.",
            "VisiCalc adalah salah satu spreadsheet awal yang ikut membuat komputer pribadi berguna untuk bisnis.",
            "Excel pertama kali dirilis pada 1980-an.",
            "Formula spreadsheet bisa merujuk ke sel lain dan berubah saat data berubah.",
            "CSV adalah format teks sederhana untuk menyimpan data bertabel.",
            "Pivot table membantu merangkum data tanpa mengubah data aslinya.",
            "Sel spreadsheet biasanya dinamai dari kombinasi huruf kolom dan angka baris.",
            "Fungsi salin dan tempel menjadi salah satu kebiasaan paling umum di komputer kerja.",
            "Grafik batang sudah digunakan jauh sebelum komputer kantor ada.",
            "Tabel membuat informasi lebih mudah dibandingkan ketika semuanya ditulis sebagai paragraf.",
        ],
        "micro_wonder": [
            "Satu sel kecil bisa mengubah seluruh tabel jika formulanya sedang percaya diri.",
            "Spreadsheet adalah kotak-kotak kecil yang pura-pura tenang sambil menyimpan banyak keputusan.",
            "Angka dalam tabel sering terlihat dingin, padahal mereka membawa cerita dari banyak tempat.",
            "Formula yang benar memberi rasa lega yang sangat spesifik.",
            "Satu koma di CSV bisa menentukan apakah data pulang dengan rapi atau tersesat.",
            "Baris dan kolom membuat dunia kantor tampak bisa ditata sebentar.",
            "Grafik kecil kadang membuat angka akhirnya mau berbicara.",
            "Sel kosong juga informasi, meski sering membuat orang curiga.",
            "Filter tabel punya cara ajaib membuat kekacauan terlihat lebih sopan.",
            "Warna kuning di spreadsheet sering berarti: tolong lihat aku dulu.",
        ],
        "genit_bermartabat": [
            "Spreadsheet adalah salah satu bentuk kehidupan yang paling sulit punah di dunia kantor.",
            "Sebagian proyek besar mungkin dimulai dari tabel yang terlihat sama membosankannya dengan ini.",
            "Excel bisa terlihat kalem, lalu tiba-tiba membuka tiga puluh kolom tambahan.",
            "Sel A1 selalu tampak seperti tempat paling awal untuk berpura-pura semuanya teratur.",
            "Formula yang rusak punya cara membuat satu kantor menjadi lebih religius sebentar.",
            "Tabel rapi adalah ilusi kecil yang sangat berguna.",
            "Kolom yang terlalu lebar sering menyimpan ambisi yang belum sempat dirapikan.",
            "Filter aktif adalah sumber dari banyak misteri kantor.",
            "Lembar bernama Selesai jarang benar-benar selesai. Dunia tahu itu.",
            "Ctrl+C dan Ctrl+V mungkin adalah ritual kantor paling tua yang masih terasa modern.",
        ],
    },
    "dunia_kerja": {
        "fakta": [
            "Catatan tempel populer setelah lem yang awalnya dianggap terlalu lemah ternyata berguna.",
            "Binder clip ditemukan pada awal abad ke-20 dan bentuknya hampir tidak banyak berubah.",
            "Kursi kantor modern banyak dipengaruhi riset ergonomi.",
            "Whiteboard menjadi umum setelah spidol non-permanen mudah digunakan.",
            "Kalkulator elektronik kecil mulai umum pada abad ke-20.",
            "Printer laser memakai listrik statis dan panas untuk menempelkan toner ke kertas.",
            "Tinta printer inkjet ditembakkan sebagai tetesan sangat kecil.",
            "Mouse komputer pertama dibuat dari kayu.",
            "Roda gulir mouse baru menjadi umum pada akhir 1990-an.",
            "Meja kerja berdiri sudah ada jauh sebelum kantor modern populer.",
        ],
        "micro_wonder": [
            "Meja kerja sering menyimpan jejak proyek yang tidak pernah terlihat oleh orang lain.",
            "Catatan tempel kecil bisa memindahkan satu pikiran dari kepala ke permukaan meja.",
            "Kalkulator punya cara membuat angka terasa lebih berani.",
            "Printer adalah benda yang membuat dunia digital tiba-tiba menjadi kertas.",
            "Kursi yang baik sering baru terasa penting setelah terlalu lama duduk.",
            "Rapat meninggalkan jejaknya bukan hanya di kalender, tapi juga di coretan kecil.",
            "Mouse bergerak sedikit, pointer berjalan jauh.",
            "Headset bisa membuat satu meja terasa seperti ruang kecil tersendiri.",
            "Lampu meja membuat satu lingkaran terang yang cukup untuk mulai.",
            "Kabel di meja kerja sering tahu lebih banyak tentang perangkat daripada pemiliknya.",
        ],
        "genit_bermartabat": [
            "Rapat punya kemampuan membuat jam bergerak dengan kepribadian berbeda.",
            "Catatan tempel kecil itu percaya diri sekali untuk benda yang mudah hilang.",
            "Printer sering menunggu momen paling penting untuk menjadi misterius.",
            "Meja kerja yang rapi kadang terasa seperti screenshot, bukan keadaan alami.",
            "Kalkulator tidak banyak bicara, tapi sering diminta menjadi penengah.",
            "Kursi kantor adalah saksi bisu dari banyak keputusan yang tidak masuk notulen.",
            "Mouse tampak kecil, tapi ia menggerakkan banyak niat di layar.",
            "Headset membuat orang terlihat siap rapat bahkan ketika batinnya masih mencari sinyal.",
            "Laci meja punya bakat menyimpan benda yang tidak punya kategori.",
            "Kalender kerja adalah bentuk sastra pendek yang penuh ketegangan.",
        ],
    },
    "alat_tulis": {
        "fakta": [
            "Pensil tidak mengandung timah. Isinya terutama grafit dan tanah liat.",
            "Pulpen ballpoint memakai bola kecil untuk menggulung tinta ke kertas.",
            "Kertas dibuat dari serat yang saling mengikat saat airnya mengering.",
            "Penghapus karet menjadi umum setelah karet alam mulai dipakai untuk menghapus grafit.",
            "Stabilo populer karena tinta neon membuat teks mudah ditemukan kembali.",
            "Klip kertas punya banyak variasi bentuk, tetapi desain Gem clip sangat dikenal.",
            "Buku catatan spiral memudahkan halaman dibuka rata di atas meja.",
            "Tinta permanen biasanya dibuat agar lebih tahan air dan cahaya.",
            "Karbon pada kertas karbon memungkinkan satu tulisan menyalin diri ke lembar lain.",
            "Penggaris plastik menjadi umum setelah produksi plastik makin murah.",
        ],
        "micro_wonder": [
            "Garis pensil adalah jejak grafit kecil yang menempel di serat kertas.",
            "Pulpen menyimpan cairan, lalu mengubahnya menjadi garis yang bisa dibaca.",
            "Kertas kosong punya kesabaran yang agak mengesankan.",
            "Penghapus tidak menghapus masa lalu. Ia hanya mengangkat grafit dari permukaan.",
            "Stabilo membuat satu kalimat berdiri lebih tegak dari yang lain.",
            "Klip kertas kecil memegang halaman-halaman yang belum tentu sepakat.",
            "Buku catatan menyimpan urutan pikiran yang sering datang tidak berurutan.",
            "Tinta yang mengering adalah cara tulisan menetap sebentar.",
            "Coretan pinggir kadang lebih hidup daripada kalimat utama.",
            "Satu halaman terlipat bisa menjadi penanda tanpa perlu berkata apa-apa.",
        ],
        "genit_bermartabat": [
            "Pensil selalu punya rencana cadangan: penghapus.",
            "Pulpen yang hilang sering punya kehidupan sosial yang lebih luas dari dugaan.",
            "Stabilo kuning adalah cara paling sopan untuk berteriak di atas kertas.",
            "Kertas kosong terlihat polos, padahal ia menantang dengan sangat tenang.",
            "Klip kertas kecil itu bekerja tanpa minta jabatan.",
            "Buku catatan baru punya aura terlalu bersih untuk langsung diajak jujur.",
            "Penghapus sering datang belakangan, seperti editor yang sabar.",
            "Tinta biru punya rasa kantor yang sulit dijelaskan.",
            "Penggaris membawa ketegasan lurus di dunia yang sering miring.",
            "Halaman terakhir buku catatan selalu terlihat seperti rahasia kecil.",
        ],
    },
    "rumah": {
        "fakta": [
            "Kunci rumah modern bekerja dengan pin kecil yang harus sejajar di dalam silinder.",
            "Engsel pintu adalah mekanisme sederhana yang sudah dipakai selama ribuan tahun.",
            "Kaca jendela menjadi umum setelah teknik produksi kaca makin murah.",
            "Keramik mug mengeras karena tanah liat berubah saat dibakar pada suhu tinggi.",
            "Kulkas rumah tangga mengubah cara orang menyimpan makanan sehari-hari.",
            "Jam kuarsa menjaga waktu dengan getaran kristal kecil.",
            "Kipas angin memindahkan udara; ia tidak menurunkan suhu ruangan secara langsung.",
            "Sakelar lampu membuat rangkaian listrik terbuka atau tertutup.",
            "Spons penuh rongga kecil yang membuatnya mudah menyerap air.",
            "Sabun bekerja karena molekulnya punya sisi yang menyukai air dan sisi yang menyukai minyak.",
        ],
        "micro_wonder": [
            "Jendela adalah benda sederhana yang membuat ruangan punya hubungan dengan luar.",
            "Kunci kecil bisa memisahkan rumah dari dunia dengan sangat tenang.",
            "Kipas angin tidak membuat dingin, tapi membuat udara lebih rajin bergerak.",
            "Lampu mengubah listrik menjadi suasana dalam satu klik.",
            "Mug keramik pernah menjadi tanah yang dibakar sampai berubah sifat.",
            "Jam dinding mengubah waktu menjadi gerakan kecil yang berulang.",
            "Pintu adalah teknologi lama yang masih sangat dipercaya.",
            "Spons dapur bekerja karena penuh ruang kosong.",
            "Bayangan di dinding adalah catatan singkat dari arah cahaya.",
            "Lantai rumah menyimpan banyak langkah yang tidak pernah dihitung.",
        ],
        "genit_bermartabat": [
            "Kipas angin bekerja keras membuat udara merasa punya tujuan.",
            "Sakelar lampu punya kekuasaan besar untuk benda sekecil itu.",
            "Jendela selalu terlihat seperti sedang menyimpan kabar dari luar.",
            "Pintu rumah tahu banyak kedatangan dan kepergian, tapi tetap tidak banyak bicara.",
            "Mug punya cara sederhana menjadi benda penting begitu ada minuman hangat.",
            "Jam dinding tidak pernah panik, meski pekerjaannya adalah waktu.",
            "Kunci kecil itu dramatis: satu putaran, dunia berubah status.",
            "Kursi kosong sering tampak seperti sedang menunggu cerita.",
            "Lampu meja membuat ruangan terlihat sedikit lebih serius.",
            "Tas di dekat pintu selalu terlihat siap pergi sebelum pemiliknya.",
        ],
    },
    "sehari_hari": {
        "fakta": [
            "Pohon kopi bisa hidup puluhan tahun.",
            "Bau tanah setelah hujan punya nama: petrikor.",
            "Banyak buku lama berbau manis karena kertas melepaskan senyawa tertentu saat menua.",
            "Awan bisa memiliki massa yang sangat besar meski tampak melayang.",
            "Pelangi sebenarnya berbentuk lingkaran, tetapi tanah biasanya menyembunyikan bagian bawahnya.",
            "Roti mengembang karena kantong-kantong kecil karbon dioksida.",
            "Daun teh hijau dan teh putih bisa berasal dari tanaman yang sama.",
            "Kata jendela dalam beberapa bahasa tua berkaitan dengan gagasan mata angin.",
            "Lilin memiliki warna api berbeda karena bagian apinya memiliki suhu berbeda.",
            "Kaca dibuat terutama dari pasir yang dipanaskan sampai berubah bentuk.",
            "Aroma rumput baru dipotong berasal dari senyawa yang dilepas tanaman saat rusak.",
            "Sebagian bunga menutup pada malam hari dalam gerakan yang disebut niktinasti.",
            "Garam pernah cukup berharga untuk membentuk jalur perdagangan.",
            "Ritsleting awalnya lebih sering dipakai pada sepatu dan tas sebelum umum di pakaian.",
            "Velcro terinspirasi dari duri kecil tanaman yang menempel pada kain dan bulu.",
        ],
        "micro_wonder": [
            "Secangkir kopi adalah hasil perjalanan panjang dari biji kecil yang dipanggang.",
            "Hujan membuat udara membawa bau tanah yang tiba-tiba terasa punya nama.",
            "Buku lama kadang menyimpan aroma waktu dengan cara yang sangat literal.",
            "Langit sore berubah warna karena cahaya mengambil jalan lebih panjang.",
            "Payung adalah atap kecil yang bisa berjalan.",
            "Jalan pulang sering terlihat sama, tapi cahaya di atasnya jarang benar-benar sama.",
            "Tas sehari-hari adalah gudang kecil yang bisa ikut berpindah.",
            "Sepatu menyimpan bentuk perjalanan tanpa perlu menyimpan peta.",
            "Kunci di saku sering lebih penting daripada ukurannya.",
            "Gelas bening membuat air terlihat seperti benda yang punya bentuk sementara.",
            "Buku yang terbuka membuat meja terlihat sedang berpikir.",
            "Hujan di kaca selalu menulis dengan huruf yang tidak bisa dibaca.",
            "Langit sore kadang hanya berubah warna, tapi seluruh ruangan ikut berubah rasa.",
            "Kopi dingin dan kopi panas punya aroma yang berbeda karena senyawa menguapnya berubah.",
            "Payung basah membawa sedikit cuaca masuk ke ruangan.",
        ],
        "genit_bermartabat": [
            "Kopi punya reputasi terlalu besar untuk minuman yang sering habis terlalu cepat.",
            "Hujan selalu datang dengan efek suara yang tidak perlu dipasang.",
            "Buku lama kadang berbau seperti perpustakaan yang sedang berbisik.",
            "Langit sore pintar sekali membuat orang berhenti sebentar tanpa memberi alasan.",
            "Payung adalah benda yang paling percaya diri saat awan mulai gelap.",
            "Tas punya kemampuan misterius untuk menjadi lebih berat dari daftar isinya.",
            "Jalan pulang kadang terlihat seperti adegan yang diulang dengan pencahayaan berbeda.",
            "Sepatu paling tahu rute harian, tapi tidak pernah ikut memberi komentar.",
            "Gelas kosong selalu tampak seperti sedang menunggu keputusan.",
            "Buku tertutup punya gaya diam yang agak sombong.",
            "Ritsleting adalah penemuan kecil yang membuat tas tidak mudah menjadi drama.",
            "Velcro punya suara khas yang tidak pernah bisa masuk ruangan diam-diam.",
            "Kopi di meja sering terlihat seperti anggota rapat yang paling tenang.",
            "Hujan di luar jendela punya bakat membuat ruangan terasa sedikit lebih jauh dari dunia.",
            "Payung yang tertinggal biasanya baru diingat ketika langit mulai bercanda.",
        ],
    },
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
        "hp",
        "ponsel",
        "kamera",
    ],
    "laptop": [
        "laptop",
        "thinkpad",
        "probook",
        "hp probook",
        "trackpoint",
        "touchpad",
        "webcam",
        "ssd",
        "ram",
        "hdmi",
    ],
    "programmer": [
        "vscode",
        "vs code",
        "visual studio code",
        "ngoding",
        "coding",
        "kode",
        "code",
        "terminal",
        "git",
        "bug",
        "deploy",
        "commit",
        "branch",
        "pull request",
        "python",
        "javascript",
        "server",
        "log",
        "error",
    ],
    "spreadsheet": [
        "spreadsheet",
        "excel",
        "sheet",
        "tabel",
        "table",
        "formula",
        "csv",
        "pivot",
        "kolom",
        "baris",
    ],
    "dunia_kerja": [
        "meja",
        "desk",
        "kerja",
        "work",
        "kantor",
        "rapat",
        "meeting",
        "router",
        "mouse",
        "headset",
        "headphone",
        "printer",
        "kalkulator",
        "sticky",
        "whiteboard",
        "clip",
        "kursi",
        "lampu",
    ],
    "alat_tulis": [
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
        "sakelar",
        "sabun",
        "dapur",
        "kursi",
        "tas",
    ],
    "sehari_hari": [
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
        "pulang",
        "baju",
        "denim",
        "foto",
        "sepatu",
        "gelas",
    ],
}


def _all_side_notes() -> list[str]:
    return [
        note
        for category_notes in SIDE_NOTE_LIBRARY.values()
        for style_notes in category_notes.values()
        for note in style_notes
    ]


SIDE_NOTES = _all_side_notes()


def _matching_categories(context: str) -> list[str]:
    normalized_context = context.lower()
    matches: list[str] = []
    for category, keywords in KEYWORD_CATEGORIES.items():
        if any(keyword in normalized_context for keyword in keywords):
            matches.append(category)
    return matches


def choose_side_note(memory_note: str = "", filename: str = "", journal_text: str = "") -> str:
    context = f"{memory_note} {filename} {journal_text}".strip()
    matches = _matching_categories(context)
    if matches:
        category = random.choice(matches)
        style = random.choice(["micro_wonder", "genit_bermartabat", "fakta"])
        return random.choice(SIDE_NOTE_LIBRARY[category][style])
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
