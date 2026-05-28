from datetime import date, datetime
import os

import pandas as pd
import streamlit as st

from db import get_entries, init_db, insert_entry
from emotion_engine import extract_entry_emotions
from memory_engine import detect_unfinished_thread
from pattern_engine import analyze_recent_patterns
from reflection_engine import generate_reflection
from response_engine import generate_submit_response
from ui_components import render_entry_card
from welcome_engine import generate_welcome


LIFE_AREAS = [
    "Kerja",
    "Relasi",
    "Spiritual",
    "Kesehatan",
    "Finansial",
    "Pembelajaran",
    "Emosi",
    "Lainnya",
]

REFLECTION_STYLES = ["Lembut", "Praktis", "Filosofis", "Stoic", "Religius"]


st.set_page_config(
    page_title="Reflective Life OS",
    page_icon="R",
    layout="wide",
)

st.markdown(
    """
    <style>
    @keyframes softFadeIn {
        from {
            opacity: 0;
            transform: translateY(4px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .stApp {
        background: #2c2722;
        color: #f0e7dc;
    }
    section[data-testid="stSidebar"] {
        background: #342e28;
        border-right: 1px solid #4b4036;
    }
    .block-container {
        max-width: 820px;
        padding-top: 2rem;
        padding-bottom: 4rem;
        animation: softFadeIn 360ms ease-out;
    }
    h1, h2, h3 {
        letter-spacing: 0;
        font-weight: 600;
        color: #f7efe5;
    }
    p, li, label, div {
        line-height: 1.72;
    }
    div[data-testid="stForm"] {
        border: 1px solid #5b4f44;
        border-radius: 8px;
        padding: 1.35rem;
        background: #332d27;
        transition: border-color 180ms ease, background 180ms ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: #584c41;
        background: #332d27;
        transition: border-color 180ms ease, transform 180ms ease, background 180ms ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: #746558;
        background: #38312a;
        transform: translateY(-1px);
    }
    .stButton > button, .stFormSubmitButton > button {
        min-height: 3rem;
        border-radius: 8px;
        border-color: #7b6c5d;
        background: #e1cdb6;
        color: #2b241f;
        font-weight: 600;
        transition: background 160ms ease, transform 160ms ease;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: #ead9c4;
        color: #2b241f;
        transform: translateY(-1px);
    }
    textarea, input, select {
        border-radius: 8px !important;
    }
    textarea {
        min-height: 150px !important;
        line-height: 1.65 !important;
    }
    input, textarea, select {
        background-color: #3a332c !important;
        color: #f2e8dc !important;
        border-color: #625448 !important;
    }
    .quiet-note {
        color: #c7b9aa;
        font-size: 0.95rem;
        margin-top: -0.25rem;
    }
    .beta-label {
        color: #c7b9aa;
        font-size: 0.78rem;
        letter-spacing: 0.02em;
        margin-top: -0.35rem;
        margin-bottom: 0.6rem;
    }
    .welcome-space {
        padding-top: 0.25rem;
        margin-bottom: 0.75rem;
    }
    .welcome-space h3 {
        line-height: 1.45;
        margin-bottom: 0.45rem;
    }
    .companion-response {
        border-left: 2px solid #9d856e;
        padding: 0.75rem 0 0.75rem 1rem;
        margin-top: 1rem;
        color: #f2e8dc;
        animation: softFadeIn 420ms ease-out;
    }
    div[data-testid="stAlert"] {
        background: #3b332c;
        border-color: #6a5a4c;
        color: #f2e8dc;
    }
    @media (max-width: 640px) {
        .block-container {
            padding-left: 1.05rem;
            padding-right: 1.05rem;
            padding-top: max(2.75rem, calc(1.5rem + env(safe-area-inset-top)));
            padding-bottom: max(4.5rem, calc(3rem + env(safe-area-inset-bottom)));
        }
        .welcome-space {
            padding-top: 0.7rem;
            margin-bottom: 1rem;
        }
        .welcome-space h3 {
            font-size: 1.18rem;
            line-height: 1.55;
            margin-bottom: 0.65rem;
        }
        h1 {
            font-size: 1.85rem;
            line-height: 1.2;
            margin-top: 0.35rem;
            margin-bottom: 0.7rem;
        }
        h2, h3 {
            font-size: 1.25rem;
            line-height: 1.35;
        }
        div[data-testid="column"] {
            width: 100% !important;
            flex: 1 1 100% !important;
        }
        textarea {
            min-height: 170px !important;
            font-size: 1rem !important;
        }
        div[data-testid="stForm"] {
            padding: 1.15rem;
            margin-top: 0.35rem;
        }
        .stButton > button, .stFormSubmitButton > button {
            min-height: 3.25rem;
            width: 100%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_db()


def get_access_code() -> str:
    env_code = os.getenv("ACCESS_CODE", "").strip()
    if env_code:
        return env_code

    try:
        return str(st.secrets.get("ACCESS_CODE", "")).strip()
    except Exception:
        return ""


def require_access_code() -> None:
    expected_code = get_access_code()
    if not expected_code:
        st.sidebar.caption("Access code belum dikonfigurasi.")
        return

    if st.session_state.get("access_granted"):
        return

    st.markdown("### Masukkan kode akses early adopter.")
    st.caption("Ruang ini masih beta kecil. Masukkan kode untuk lanjut.")

    with st.form("access_code_form"):
        entered_code = st.text_input("Kode akses", type="password")
        submitted = st.form_submit_button("Masuk")

    if submitted:
        if entered_code.strip() == expected_code:
            st.session_state["access_granted"] = True
            st.rerun()
        else:
            st.error("Kode belum cocok.")

    st.stop()


def format_rupiah(value: float) -> str:
    return f"Rp {value:,.0f}".replace(",", ".")


def make_entry(
    entry_date: date,
    activity: str,
    life_area: str,
    duration_minutes: int,
    cost: float,
    food: str,
    calories: int,
    mood_score: int,
    energy_score: int,
    personal_reflection: str,
    gratitude_note: str,
    improvement_action: str,
) -> dict:
    return {
        "entry_date": entry_date.isoformat(),
        "activity": activity.strip(),
        "life_area": life_area,
        "duration_minutes": int(duration_minutes),
        "cost": float(cost),
        "food": food.strip(),
        "calories": int(calories),
        "mood_score": int(mood_score),
        "energy_score": int(energy_score),
        "personal_reflection": personal_reflection.strip(),
        "gratitude_note": gratitude_note.strip(),
        "improvement_action": improvement_action.strip(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def save_entry(entry: dict) -> None:
    insert_entry(**entry)


def show_welcome(entries: list[dict]) -> None:
    st.markdown('<div class="welcome-space">', unsafe_allow_html=True)
    st.markdown(f"### {generate_welcome(entries)}")
    continuity_prompt = detect_unfinished_thread(entries)
    if continuity_prompt:
        st.markdown(f'<p class="quiet-note">{continuity_prompt}</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    st.divider()


def show_pattern_noticing(entries: list[dict], title: str = "Pattern Noticing") -> None:
    st.subheader(title)
    for pattern in analyze_recent_patterns(entries):
        st.write(pattern)


def show_emotion_note(entry: dict) -> None:
    emotions = extract_entry_emotions(entry)
    if emotions:
        st.markdown(
            f'<p class="quiet-note">Nuansa hari ini: {", ".join(emotions)}</p>',
            unsafe_allow_html=True,
        )


def show_feedback_section() -> None:
    with st.sidebar.expander("Feedback untuk early version"):
        st.caption("Kalau ada bagian yang terasa janggal, terlalu ramai, atau kurang manusiawi, catat di sini dulu.")
        st.text_area(
            "Catatan feedback",
            placeholder="Apa yang terasa enak, aneh, atau perlu dilunakkan?",
            height=120,
            key="early_feedback_note",
        )
        st.caption("Untuk versi awal ini, feedback belum disimpan otomatis.")


def show_input_page(reflection_style: str, entries: list[dict]) -> None:
    st.title("Ruang Menulis")
    st.caption("Tidak perlu rapi. Cukup tulis yang masih tertinggal di dalam diri.")

    mode = st.radio(
        "Pilih cara menulis",
        ["Journal Lengkap", "Quick Reflection"],
        horizontal=True,
    )

    if mode == "Quick Reflection":
        show_quick_reflection_form(entries)
    else:
        show_full_journal_form(reflection_style, entries)


def show_full_journal_form(reflection_style: str, entries: list[dict]) -> None:
    with st.form("daily_journal_form", clear_on_submit=True):
        entry_date = st.date_input("Tanggal", value=date.today())

        col_left, col_right = st.columns(2)
        with col_left:
            activity = st.text_input("Aktivitas utama")
            life_area = st.selectbox("Area hidup", LIFE_AREAS)
            duration_minutes = st.number_input(
                "Durasi aktivitas (menit)",
                min_value=0,
                step=5,
                value=0,
            )
            cost = st.number_input(
                "Pengeluaran",
                min_value=0.0,
                step=10_000.0,
                value=0.0,
                format="%.0f",
            )

        with col_right:
            mood_score = st.slider("Mood", min_value=1, max_value=10, value=5)
            energy_score = st.slider("Energi", min_value=1, max_value=10, value=5)
            food = st.text_input("Makanan/minuman utama")
            calories = st.number_input(
                "Estimasi kalori",
                min_value=0,
                step=50,
                value=0,
            )

        personal_reflection = st.text_area(
            "Refleksi pribadi",
            placeholder="Apa yang paling tinggal di pikiranmu hari ini?",
            height=190,
        )
        gratitude_note = st.text_area(
            "Catatan syukur",
            placeholder="Satu hal kecil yang masih layak disyukuri.",
            height=130,
        )
        improvement_action = st.text_area(
            "Aksi perbaikan",
            placeholder="Jika besok sedikit lebih ringan, apa satu hal kecil yang ingin kamu coba?",
            height=130,
        )

        submitted = st.form_submit_button("Simpan catatan")

    if submitted:
        if not activity.strip():
            st.error("Aktivitas utama perlu diisi.")
            return

        entry = make_entry(
            entry_date,
            activity,
            life_area,
            int(duration_minutes),
            float(cost),
            food,
            int(calories),
            int(mood_score),
            int(energy_score),
            personal_reflection,
            gratitude_note,
            improvement_action,
        )
        save_entry(entry)
        updated_entries = [entry] + entries
        st.success("Catatan tersimpan.")
        st.markdown(
            f'<div class="companion-response">{generate_submit_response(entry, updated_entries)}</div>',
            unsafe_allow_html=True,
        )
        show_emotion_note(entry)

        with st.expander("Baca refleksi singkat"):
            st.write(generate_reflection(entry, reflection_style))


def show_quick_reflection_form(entries: list[dict]) -> None:
    with st.form("quick_reflection_form", clear_on_submit=True):
        entry_date = st.date_input("Tanggal", value=date.today(), key="quick_date")
        life_area = st.selectbox("Area hidup", LIFE_AREAS, key="quick_life_area")
        mood_score = st.slider("Mood", min_value=1, max_value=10, value=5, key="quick_mood")
        energy_score = st.slider("Energi", min_value=1, max_value=10, value=5, key="quick_energy")
        one_sentence = st.text_area(
            "Satu kalimat",
            placeholder="Hari ini yang paling terasa adalah...",
            height=150,
        )
        gratitude_note = st.text_input(
            "Syukur singkat (opsional)",
            placeholder="Satu hal kecil yang masih ada.",
        )

        submitted = st.form_submit_button("Simpan catatan singkat")

    if submitted:
        if not one_sentence.strip():
            st.error("Tulis satu kalimat dulu.")
            return

        entry = make_entry(
            entry_date,
            "Quick reflection",
            life_area,
            0,
            0.0,
            "",
            0,
            int(mood_score),
            int(energy_score),
            one_sentence,
            gratitude_note,
            "",
        )
        save_entry(entry)
        updated_entries = [entry] + entries
        st.success("Catatan singkat tersimpan.")
        st.markdown(
            f'<div class="companion-response">{generate_submit_response(entry, updated_entries)}</div>',
            unsafe_allow_html=True,
        )
        show_emotion_note(entry)


def show_history_page() -> None:
    st.title("Jejak Catatan")
    st.caption("Beberapa hal memang baru terlihat setelah diberi jarak.")

    entries = get_entries()
    if not entries:
        st.info("Belum ada yang ditulis. Tidak perlu buru-buru.")
        return

    for entry in entries:
        render_entry_card(entry)

    with st.expander("Lihat data mentah"):
        df = pd.DataFrame(entries)
        display_columns = [
            "id",
            "entry_date",
            "life_area",
            "activity",
            "duration_minutes",
            "cost",
            "food",
            "calories",
            "mood_score",
            "energy_score",
            "personal_reflection",
            "gratitude_note",
            "improvement_action",
            "created_at",
        ]
        st.dataframe(df[display_columns], use_container_width=True, hide_index=True)


def show_today_insight_page(reflection_style: str) -> None:
    st.title("Hari Ini")

    entries = get_entries()
    if not entries:
        st.info("Belum ada catatan untuk dibaca hari ini. Ruangnya tetap ada.")
        return

    latest_entry = entries[0]

    st.subheader(latest_entry["entry_date"])
    st.write(f"Area hidup: {latest_entry.get('life_area') or 'Belum dicatat'}")
    st.write(f"Aktivitas utama: {latest_entry['activity']}")
    st.write(
        f"Mood {latest_entry['mood_score']}/10, energi {latest_entry['energy_score']}/10, "
        f"durasi {latest_entry['duration_minutes']} menit."
    )
    st.write(f"Biaya: {format_rupiah(float(latest_entry['cost'] or 0))}")
    show_emotion_note(latest_entry)

    if latest_entry.get("improvement_action"):
        st.write(f"Aksi berikutnya: {latest_entry['improvement_action']}")

    st.divider()
    st.subheader("Bacaan singkat")
    st.write(generate_reflection(latest_entry, reflection_style))

    st.divider()
    show_pattern_noticing(entries)


def show_weekly_reflection_page(reflection_style: str) -> None:
    st.title("Refleksi Mingguan")
    st.caption("Bukan penilaian. Hanya melihat beberapa hari terakhir dengan sedikit jarak.")

    entries = get_entries()
    if not entries:
        st.info("Belum ada cukup cerita untuk dirangkum. Mulai dari satu catatan kecil saja.")
        return

    weekly_entries = entries[:7]
    df = pd.DataFrame(weekly_entries)

    average_mood = df["mood_score"].mean()
    average_energy = df["energy_score"].mean()
    total_cost = df["cost"].sum()
    total_activities = len(df)
    area_counts = df["life_area"].fillna("Belum dicatat").replace("", "Belum dicatat").value_counts()
    most_common_area = area_counts.index[0] if not area_counts.empty else "Belum dicatat"

    summary_rows = pd.DataFrame(
        [
            {"Ringkasan": "Rata-rata mood", "Nilai": f"{average_mood:.1f}/10"},
            {"Ringkasan": "Rata-rata energi", "Nilai": f"{average_energy:.1f}/10"},
            {"Ringkasan": "Total biaya", "Nilai": format_rupiah(float(total_cost))},
            {"Ringkasan": "Total aktivitas", "Nilai": str(total_activities)},
            {"Ringkasan": "Area hidup paling sering", "Nilai": most_common_area},
        ]
    )
    st.dataframe(summary_rows, use_container_width=True, hide_index=True)

    st.divider()
    show_pattern_noticing(weekly_entries, "Pattern Noticing Mingguan")

    st.divider()
    st.subheader("Bacaan mingguan")
    weekly_entry = {
        "mood_score": round(float(average_mood)),
        "energy_score": round(float(average_energy)),
        "cost": float(total_cost),
        "calories": int(df["calories"].sum() / max(total_activities, 1)),
        "personal_reflection": " ".join(df["personal_reflection"].fillna("").astype(str).tolist()),
        "gratitude_note": " ".join(df["gratitude_note"].fillna("").astype(str).tolist()),
    }
    st.write(generate_reflection(weekly_entry, reflection_style))


require_access_code()

entries_at_start = get_entries()

st.sidebar.title("Reflective Life OS")
st.sidebar.markdown('<div class="beta-label">Early Reflective Beta</div>', unsafe_allow_html=True)
reflection_style = st.sidebar.selectbox("Reflection Style", REFLECTION_STYLES)
page = st.sidebar.radio(
    "Navigasi",
    ["Input Harian", "History", "Insight Hari Ini", "Weekly Reflection"],
)
show_feedback_section()

show_welcome(entries_at_start)

if page == "Input Harian":
    show_input_page(reflection_style, entries_at_start)
elif page == "History":
    show_history_page()
elif page == "Insight Hari Ini":
    show_today_insight_page(reflection_style)
else:
    show_weekly_reflection_page(reflection_style)
