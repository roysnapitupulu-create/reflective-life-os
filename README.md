# Reflective Life OS

Reflective Life OS adalah early reflective journaling companion yang berjalan ringan dengan Streamlit dan SQLite. Ia dibuat untuk membantu seseorang menulis, mengingat, dan melihat pola kecil dalam hidupnya tanpa terasa seperti dashboard produktivitas.

Ini bukan aplikasi diagnosis, bukan chatbot motivasi, dan bukan sistem penilaian diri. Ia lebih dekat ke ruang menulis pribadi yang pelan: tempat untuk mencatat hari, memberi nama pada rasa, dan melihat beberapa benang yang mungkin terus muncul.

## Filosofi Produk

- Tenang lebih penting daripada ramai.
- Insight sederhana yang tepat lebih baik daripada analisis panjang.
- Tidak semua catatan perlu disimpulkan.
- Memory harus terasa lembut, bukan invasif.
- Data pribadi tetap lokal selama dijalankan secara lokal.

## Fitur Early Beta

- Daily journal dan Quick Reflection
- Timeline history yang terasa seperti catatan pribadi
- Reflection style: Lembut, Praktis, Filosofis, Stoic, Religius
- Pattern noticing ringan dari beberapa entry terakhir
- Continuity memory prompt yang tidak selalu muncul
- Emotion tag sederhana berbasis keyword
- Weekly Reflection
- Access code untuk early adopter
- UI warm dark yang nyaman untuk journaling malam

## Install Lokal di Windows

Pastikan Python 3.10+ sudah terpasang.

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Run Lokal

```powershell
streamlit run app.py
```

Streamlit akan menampilkan local URL yang bisa dibuka di browser. Jika ingin mencoba dari HP di jaringan Wi-Fi yang sama, gunakan Network URL yang muncul di terminal.

## Access Code

Untuk beta publik, set `ACCESS_CODE` melalui environment variable atau Streamlit secrets.

Environment variable lokal:

```powershell
$env:ACCESS_CODE="kode-beta"
streamlit run app.py
```

Streamlit Community Cloud secrets:

```toml
ACCESS_CODE = "kode-beta"
```

Jika `ACCESS_CODE` kosong, gate akan dilewati agar local development tetap mudah.

## Data

Database SQLite dibuat otomatis di:

```text
data/journal.db
```

Folder `data/` tidak ikut commit. Untuk deployment di Streamlit Community Cloud, penyimpanan file lokal cocok untuk early testing ringan, tetapi belum ideal sebagai penyimpanan permanen jangka panjang.

## Deployment Notes

Project ini sengaja tetap kecil:

- Tidak ada login kompleks
- Tidak ada cloud database
- Tidak ada OpenAI/API/LLM
- Tidak ada Docker

Tujuan early beta ini adalah menguji rasa: apakah app terasa tenang, aman, manusiawi, dan cukup berguna untuk menemani refleksi harian.
