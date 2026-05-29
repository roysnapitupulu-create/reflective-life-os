from collections import Counter
from datetime import date, timedelta
import os
from pathlib import Path
import uuid

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from db import (
    ensure_user_profile,
    get_entries,
    get_memory_artifacts,
    init_db,
    insert_entry,
    insert_memory_artifact,
    update_user_activity,
)
from emotion_engine import extract_entry_emotions
from identity_engine import (
    get_current_user_context,
    get_or_create_user_id,
    mark_access_trusted,
    utc_now_iso,
)
from meaning_engine import generate_meaning_response, serialize_themes
from memory_artifacts import choose_side_note, get_image_extension, validate_image_upload
from memory_engine import detect_unfinished_thread
from pattern_engine import analyze_recent_patterns
from reflection_engine import generate_reflection
from response_engine import generate_submit_response
from storage_supabase import (
    CloudStorageError,
    is_supabase_enabled,
    load_journal_entries,
    load_memory_artifacts,
    save_journal_entry,
    save_memory_artifact,
)
from time_utils import format_human_time
from ui_components import render_entry_card, render_memory_artifacts
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

WEEKLY_MIRROR_STOPWORDS = {
    "aku",
    "yang",
    "dan",
    "atau",
    "di",
    "ke",
    "ini",
    "itu",
    "hari",
    "minggu",
    "dengan",
    "untuk",
    "tidak",
    "gak",
    "ga",
    "ada",
    "jadi",
    "karena",
    "dari",
    "masih",
    "sudah",
    "bisa",
    "mau",
    "ingin",
    "lebih",
    "satu",
    "hal",
    "kecil",
    "terasa",
    "rasanya",
    "cukup",
    "hari",
    "besok",
    "malam",
}


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
        background:
            radial-gradient(circle at 18% 0%, rgba(180, 122, 61, 0.2), transparent 34%),
            radial-gradient(circle at 88% 12%, rgba(233, 190, 128, 0.12), transparent 28%),
            linear-gradient(180deg, #2b241f 0%, #201b18 58%, #181513 100%);
        color: #f0e7dc;
    }
    section[data-testid="stSidebar"] {
        background: rgba(50, 42, 35, 0.94);
        border-right: 1px solid rgba(201, 158, 103, 0.16);
    }
    section[data-testid="stSidebar"] > div,
    section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        background: rgba(50, 42, 35, 0.98);
        color: #f7eadb;
    }
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] span,
    section[data-testid="stSidebar"] div {
        color: #f7eadb;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] label {
        border-radius: 12px;
        padding: 0.25rem 0.35rem;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] label:hover {
        background: rgba(240, 201, 142, 0.12);
    }
    section[data-testid="stSidebar"] [role="radio"][aria-checked="true"],
    section[data-testid="stSidebar"] [data-baseweb="radio"] [aria-checked="true"] {
        color: #f0c98e;
    }
    section[data-testid="stSidebar"] [data-baseweb="select"] > div {
        background: rgba(24, 18, 14, 0.92);
        border-color: rgba(240, 201, 142, 0.38);
        color: #f7eadb;
    }
    .block-container {
        max-width: 820px;
        padding-top: 1.35rem;
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
        border: 1px solid rgba(222, 181, 128, 0.18);
        border-radius: 18px;
        padding: 1.35rem;
        background: rgba(48, 40, 33, 0.78);
        box-shadow: 0 18px 45px rgba(0, 0, 0, 0.2);
        backdrop-filter: blur(10px);
        transition: border-color 180ms ease, background 180ms ease, box-shadow 180ms ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-color: rgba(222, 181, 128, 0.18);
        border-radius: 18px;
        background: rgba(49, 41, 34, 0.72);
        box-shadow: 0 14px 32px rgba(0, 0, 0, 0.16);
        transition: border-color 180ms ease, transform 180ms ease, background 180ms ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover {
        border-color: rgba(230, 187, 128, 0.34);
        background: rgba(58, 48, 39, 0.78);
        transform: translateY(-1px);
    }
    .stButton > button, .stFormSubmitButton > button {
        min-height: 3.25rem;
        border-radius: 999px;
        border: 1px solid rgba(255, 221, 174, 0.42);
        background: linear-gradient(135deg, #f0c98e 0%, #c98645 100%);
        color: #201814;
        font-weight: 700;
        letter-spacing: 0;
        box-shadow: 0 12px 26px rgba(192, 121, 53, 0.22);
        transition: background 160ms ease, transform 160ms ease, box-shadow 160ms ease;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background: linear-gradient(135deg, #f6d7a8 0%, #d49552 100%);
        color: #201814;
        transform: translateY(-1px);
        box-shadow: 0 16px 32px rgba(192, 121, 53, 0.28);
    }
    textarea, input, select {
        border-radius: 8px !important;
    }
    textarea {
        min-height: 150px !important;
        line-height: 1.65 !important;
    }
    input, textarea, select {
        background-color: rgba(37, 31, 27, 0.72) !important;
        color: #f7eadb !important;
        border-color: rgba(216, 173, 118, 0.2) !important;
    }
    textarea:focus, input:focus {
        border-color: rgba(240, 201, 142, 0.58) !important;
        box-shadow: 0 0 0 1px rgba(240, 201, 142, 0.16) !important;
    }
    div[data-testid="stForm"] label,
    div[data-testid="stForm"] label p,
    div[data-testid="stForm"] [data-testid="stWidgetLabel"],
    div[data-testid="stForm"] [data-testid="stWidgetLabel"] p,
    div[data-testid="stTextInput"] label,
    div[data-testid="stTextArea"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stDateInput"] label {
        color: #f3d7b8 !important;
        opacity: 1 !important;
        font-weight: 650 !important;
    }
    div[data-testid="stTextInput"],
    div[data-testid="stTextArea"],
    div[data-testid="stNumberInput"],
    div[data-testid="stSelectbox"],
    div[data-testid="stDateInput"] {
        color: #fff3e6 !important;
    }
    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stDateInput"] input,
    div[data-baseweb="input"] input,
    div[data-baseweb="textarea"] textarea {
        background: rgba(55, 46, 39, 0.95) !important;
        color: #fff3e6 !important;
        caret-color: #e0a45f !important;
        border-color: rgba(214, 160, 92, 0.35) !important;
        -webkit-text-fill-color: #fff3e6 !important;
    }
    div[data-testid="stTextInput"] input::placeholder,
    div[data-testid="stTextArea"] textarea::placeholder,
    div[data-testid="stNumberInput"] input::placeholder,
    div[data-testid="stDateInput"] input::placeholder,
    div[data-baseweb="input"] input::placeholder,
    div[data-baseweb="textarea"] textarea::placeholder {
        color: #bda58f !important;
        opacity: 1 !important;
        -webkit-text-fill-color: #bda58f !important;
    }
    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] div[data-baseweb="input"],
    div[data-testid="stTextArea"] div[data-baseweb="textarea"],
    div[data-testid="stNumberInput"] div[data-baseweb="input"],
    div[data-testid="stDateInput"] div[data-baseweb="input"],
    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        background: rgba(55, 46, 39, 0.95) !important;
        border-color: rgba(214, 160, 92, 0.35) !important;
        color: #fff3e6 !important;
        box-shadow: none !important;
    }
    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="select"]:focus-within > div,
    div[data-testid="stTextInput"]:focus-within div[data-baseweb="input"],
    div[data-testid="stTextArea"]:focus-within div[data-baseweb="textarea"],
    div[data-testid="stNumberInput"]:focus-within div[data-baseweb="input"],
    div[data-testid="stDateInput"]:focus-within div[data-baseweb="input"],
    div[data-testid="stSelectbox"]:focus-within div[data-baseweb="select"] > div {
        border-color: #e0a45f !important;
        box-shadow: 0 0 0 1px rgba(224, 164, 95, 0.4) !important;
    }
    div[data-baseweb="select"] span,
    div[data-testid="stSelectbox"] span,
    div[data-baseweb="select"] svg,
    div[data-testid="stSelectbox"] svg {
        color: #fff3e6 !important;
        fill: #fff3e6 !important;
    }
    div[data-testid="stNumberInput"] button,
    div[data-testid="stNumberInput"] button svg {
        background: rgba(75, 58, 44, 0.98) !important;
        color: #f3d7b8 !important;
        fill: #f3d7b8 !important;
        border-color: rgba(214, 160, 92, 0.35) !important;
    }
    div[data-testid="stNumberInput"] button:hover,
    div[data-testid="stNumberInput"] button:hover svg {
        background: rgba(105, 75, 50, 0.98) !important;
        color: #fff3e6 !important;
        fill: #fff3e6 !important;
    }
    div[data-baseweb="popover"],
    div[data-baseweb="menu"],
    ul[role="listbox"] {
        background: rgba(30, 24, 19, 0.98) !important;
        border-color: rgba(214, 160, 92, 0.35) !important;
        color: #fff3e6 !important;
    }
    li[role="option"],
    div[role="option"] {
        background: rgba(30, 24, 19, 0.98) !important;
        color: #fff3e6 !important;
    }
    li[role="option"]:hover,
    div[role="option"]:hover {
        background: rgba(105, 75, 50, 0.98) !important;
        color: #fff3e6 !important;
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
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(230, 187, 128, 0.18);
        border-radius: 22px;
        padding: 1.15rem 1.2rem 1.05rem;
        margin-bottom: 1rem;
        background:
            linear-gradient(135deg, rgba(92, 63, 42, 0.75), rgba(40, 33, 29, 0.82)),
            radial-gradient(circle at 90% 20%, rgba(240, 201, 142, 0.18), transparent 36%);
        box-shadow: 0 18px 42px rgba(0, 0, 0, 0.22);
        backdrop-filter: blur(12px);
    }
    .welcome-space h3 {
        line-height: 1.42;
        margin-bottom: 0.4rem;
        max-width: 88%;
    }
    .welcome-kicker {
        color: #e7bf88;
        font-size: 0.78rem;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.45rem;
    }
    .welcome-copy {
        color: #d8c8b6;
        font-size: 0.96rem;
        margin-top: 0.25rem;
        max-width: 34rem;
    }
    .cozy-orbit {
        position: absolute;
        right: 1rem;
        top: 1rem;
        width: 54px;
        height: 54px;
        border-radius: 18px;
        background:
            radial-gradient(circle at 50% 46%, #f1ca8e 0 10%, transparent 11%),
            linear-gradient(135deg, rgba(240, 201, 142, 0.24), rgba(255, 255, 255, 0.04));
        border: 1px solid rgba(240, 201, 142, 0.24);
        box-shadow: inset 0 0 24px rgba(255, 221, 174, 0.1), 0 10px 24px rgba(0, 0, 0, 0.18);
    }
    .soft-divider {
        height: 1px;
        margin: 1.15rem 0;
        background: linear-gradient(90deg, transparent, rgba(226, 179, 120, 0.26), transparent);
    }
    .journey-section {
        border: 1px solid rgba(226, 179, 120, 0.16);
        border-radius: 16px;
        padding: 1rem;
        margin: 0.95rem 0;
        background: rgba(31, 26, 23, 0.34);
    }
    .journey-section-title {
        color: #f3d5a8;
        font-weight: 700;
        margin-bottom: 0.1rem;
    }
    .journey-section-copy {
        color: #c8b7a5;
        font-size: 0.9rem;
        margin-bottom: 0.85rem;
    }
    .mode-helper {
        color: #c8b7a5;
        font-size: 0.92rem;
        margin-top: -0.25rem;
        margin-bottom: 0.8rem;
    }
    .companion-response {
        border-left: 2px solid #9d856e;
        padding: 0.75rem 0 0.75rem 1rem;
        margin-top: 1rem;
        color: #f2e8dc;
        animation: softFadeIn 420ms ease-out;
    }
    .meaning-card {
        border: 1px solid rgba(240, 201, 142, 0.2);
        border-radius: 20px;
        padding: 1rem 1.05rem;
        margin: 1.1rem 0;
        background:
            linear-gradient(135deg, rgba(69, 49, 34, 0.86), rgba(31, 25, 21, 0.9)),
            radial-gradient(circle at 92% 0%, rgba(240, 201, 142, 0.16), transparent 34%);
        box-shadow: 0 18px 42px rgba(0, 0, 0, 0.22);
    }
    .meaning-kicker {
        color: #e7bf88;
        font-size: 0.78rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.35rem;
    }
    .meaning-lens {
        color: #f7eadb;
        font-size: 1.02rem;
        font-weight: 700;
        margin-bottom: 0.65rem;
    }
    .meaning-copy {
        color: #ead9c4;
        line-height: 1.72;
        margin-bottom: 0.85rem;
    }
    .meaning-small {
        color: #d8c8b6;
        font-size: 0.94rem;
        margin-top: 0.55rem;
    }
    .mirror-card {
        border: 1px solid rgba(240, 201, 142, 0.18);
        border-radius: 20px;
        padding: 1rem 1.05rem;
        margin: 1rem 0;
        background: rgba(42, 33, 27, 0.82);
        box-shadow: 0 16px 36px rgba(0, 0, 0, 0.18);
    }
    .mirror-row {
        color: #d8c8b6;
        margin: 0.4rem 0;
    }
    .mirror-row strong {
        color: #f3d5a8;
    }
    div[data-testid="stAlert"] {
        background: #3b332c;
        border-color: #6a5a4c;
        color: #f2e8dc;
    }
    @media (max-width: 640px) {
        section[data-testid="stSidebar"] {
            background: rgba(24, 18, 14, 0.98) !important;
            border-right: 1px solid rgba(240, 201, 142, 0.22);
            box-shadow: 18px 0 48px rgba(0, 0, 0, 0.38);
        }
        section[data-testid="stSidebar"] > div,
        section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            background: rgba(24, 18, 14, 0.98) !important;
            backdrop-filter: none;
        }
        section[data-testid="stSidebar"] h1,
        section[data-testid="stSidebar"] h2,
        section[data-testid="stSidebar"] h3,
        section[data-testid="stSidebar"] label,
        section[data-testid="stSidebar"] p,
        section[data-testid="stSidebar"] span,
        section[data-testid="stSidebar"] div {
            color: #f7eadb !important;
            opacity: 1 !important;
        }
        section[data-testid="stSidebar"] [role="radiogroup"] label {
            min-height: 2.4rem;
            display: flex;
            align-items: center;
            border-radius: 14px;
            margin: 0.15rem 0;
            background: rgba(255, 255, 255, 0.02);
        }
        section[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
            background: rgba(201, 116, 48, 0.22);
            outline: 1px solid rgba(240, 201, 142, 0.36);
        }
        section[data-testid="stSidebar"] input[type="radio"] {
            accent-color: #f0c98e;
        }
        section[data-testid="stSidebar"] [data-baseweb="select"] > div,
        section[data-testid="stSidebar"] input,
        section[data-testid="stSidebar"] textarea {
            background: rgba(38, 28, 22, 0.98) !important;
            border-color: rgba(240, 201, 142, 0.42) !important;
            color: #f7eadb !important;
        }
        section[data-testid="stSidebar"] .beta-label {
            color: #f0c98e !important;
        }
        .block-container {
            padding-left: 1.05rem;
            padding-right: 1.05rem;
            padding-top: max(2.35rem, calc(1.35rem + env(safe-area-inset-top)));
            padding-bottom: max(4.5rem, calc(3rem + env(safe-area-inset-bottom)));
        }
        .welcome-space {
            padding: 1rem 1rem 0.95rem;
            margin-bottom: 1.15rem;
            border-radius: 20px;
        }
        .welcome-space h3 {
            font-size: 1.08rem;
            line-height: 1.48;
            margin-bottom: 0.5rem;
            max-width: 82%;
        }
        .welcome-copy {
            font-size: 0.9rem;
            max-width: 100%;
        }
        .cozy-orbit {
            right: 0.75rem;
            top: 0.85rem;
            width: 42px;
            height: 42px;
            border-radius: 15px;
        }
        h1 {
            font-size: 1.72rem;
            line-height: 1.2;
            margin-top: 0.25rem;
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
            padding: 1rem;
            margin-top: 0.35rem;
            border-radius: 18px;
        }
        .journey-section {
            padding: 0.9rem;
            margin: 0.85rem 0;
        }
        .stButton > button, .stFormSubmitButton > button {
            min-height: 3.35rem;
            width: 100%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

init_db()


def render_browser_identity_bridge() -> None:
    components.html(
        """
        <script>
        (function () {
            const mappings = [
                ["rid", "rlos_user_id"],
                ["trusted_until", "rlos_trusted_until"],
                ["trust_sig", "rlos_trust_sig"]
            ];
            try {
                const parentWindow = window.parent;
                const url = new URL(parentWindow.location.href);
                let shouldReload = false;

                mappings.forEach(([paramKey, storageKey]) => {
                    const paramValue = url.searchParams.get(paramKey);
                    const storedValue = parentWindow.localStorage.getItem(storageKey);

                    if (paramValue) {
                        parentWindow.localStorage.setItem(storageKey, paramValue);
                        return;
                    }

                    if (storedValue) {
                        url.searchParams.set(paramKey, storedValue);
                        shouldReload = true;
                    }
                });

                if (shouldReload) {
                    parentWindow.location.replace(url.toString());
                }
            } catch (error) {
                // If browser storage is unavailable, Streamlit falls back to the access code flow.
            }
        })();
        </script>
        """,
        height=0,
        width=0,
    )


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
    user_context = get_current_user_context(st, expected_code)

    if not user_context["storage_ready"]:
        st.info("Menyiapkan ruang refleksimu...")
        st.stop()

    if not expected_code:
        st.sidebar.caption("Access code belum dikonfigurasi.")
        if user_context["user_id"]:
            st.session_state["user_id"] = user_context["user_id"]
        return

    if user_context["access_trusted"]:
        st.session_state["user_id"] = user_context["user_id"]
        return

    if st.session_state.get("access_granted") and st.session_state.get("user_id"):
        mark_access_trusted(st, st.session_state["user_id"], expected_code)
        return

    st.markdown("### Masukkan kode akses early adopter.")
    st.caption("Ruang ini masih beta kecil. Masukkan kode untuk lanjut.")

    with st.form("access_code_form"):
        entered_code = st.text_input("Kode akses", type="password")
        submitted = st.form_submit_button("Masuk")

    if submitted:
        if entered_code.strip() == expected_code:
            user_id = user_context["user_id"]
            if not user_id:
                user_id, _ = get_or_create_user_id(st)
            mark_access_trusted(st, user_id, expected_code)
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
    user_id: str,
) -> dict:
    now = utc_now_iso()
    return {
        "user_id": user_id,
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
        "created_at": now,
        "updated_at": now,
        "themes": "",
        "lens_name": "",
        "lens_source": "",
        "meaning_response": "",
        "meaning_question": "",
        "micro_action": "",
    }


def save_entry(entry: dict) -> dict:
    if is_supabase_enabled():
        try:
            return save_journal_entry(entry)
        except CloudStorageError:
            st.error("Storage cloud belum bisa diakses.")
            st.stop()

    entry_id = insert_entry(**entry)
    return {**entry, "id": entry_id}


def attach_memory_artifacts(entries: list[dict], artifacts: list[dict]) -> list[dict]:
    artifacts_by_entry_id: dict[str, list[dict]] = {}
    for artifact in artifacts:
        entry_id = str(artifact.get("journal_entry_id") or "")
        if not entry_id:
            continue
        artifacts_by_entry_id.setdefault(entry_id, []).append(artifact)

    enriched_entries: list[dict] = []
    for entry in entries:
        entry_id = str(entry.get("id") or "")
        enriched_entries.append(
            {
                **entry,
                "memory_artifacts": artifacts_by_entry_id.get(entry_id, []),
            }
        )
    return enriched_entries


def load_entries(user_id: str, limit: int = 100) -> list[dict]:
    if is_supabase_enabled():
        try:
            entries = load_journal_entries(user_id, limit=limit)
        except CloudStorageError:
            st.error("Storage cloud belum bisa diakses.")
            return []
        try:
            artifacts = load_memory_artifacts(user_id)
            return attach_memory_artifacts(entries, artifacts)
        except CloudStorageError:
            return entries

    return attach_memory_artifacts(get_entries(user_id), get_memory_artifacts(user_id))


def save_local_memory_artifact(
    user_id: str,
    journal_entry_id: int,
    uploaded_file,
    memory_note: str,
    side_note: str,
) -> dict:
    artifact_id = str(uuid.uuid4())
    extension = get_image_extension(
        getattr(uploaded_file, "name", ""),
        getattr(uploaded_file, "type", ""),
    )
    artifact_dir = Path(__file__).parent / "data" / "memory_artifacts" / user_id / str(journal_entry_id)
    artifact_dir.mkdir(parents=True, exist_ok=True)
    image_path = artifact_dir / f"{artifact_id}{extension}"
    image_path.write_bytes(uploaded_file.getvalue())
    return insert_memory_artifact(
        user_id=user_id,
        journal_entry_id=int(journal_entry_id),
        image_path=str(image_path),
        memory_note=memory_note.strip(),
        side_note=side_note,
        created_at=utc_now_iso(),
        artifact_id=artifact_id,
    )


def save_entry_memory_artifact(
    saved_entry: dict,
    uploaded_file,
    memory_note: str,
    user_id: str,
    journal_text: str = "",
) -> dict | None:
    if uploaded_file is None:
        return None

    entry_id = saved_entry.get("id")
    if not entry_id:
        raise CloudStorageError("Catatan tersimpan, tapi id catatan belum tersedia untuk foto.")

    side_note = choose_side_note(memory_note, getattr(uploaded_file, "name", ""), journal_text)
    if is_supabase_enabled():
        return save_memory_artifact(
            user_id=user_id,
            journal_entry_id=entry_id,
            image_bytes=uploaded_file.getvalue(),
            filename=getattr(uploaded_file, "name", ""),
            content_type=getattr(uploaded_file, "type", "") or "image/jpeg",
            memory_note=memory_note.strip(),
            side_note=side_note,
            created_at=utc_now_iso(),
        )

    return save_local_memory_artifact(
        user_id=user_id,
        journal_entry_id=int(entry_id),
        uploaded_file=uploaded_file,
        memory_note=memory_note,
        side_note=side_note,
    )


def enrich_entry_with_meaning(entry: dict, recent_entries: list[dict], reflection_style: str) -> dict:
    meaning_entry = {**entry, "reflection_style": reflection_style}
    meaning = generate_meaning_response(meaning_entry, recent_entries)
    entry["themes"] = serialize_themes(meaning["themes"])
    entry["lens_name"] = meaning["lens"]["name"]
    entry["lens_source"] = meaning["lens"]["source"]
    entry["meaning_response"] = meaning["response"]
    entry["meaning_question"] = meaning["question"]
    entry["micro_action"] = meaning["micro_action"]
    return entry


def show_meaning_response(entry: dict) -> None:
    if not entry.get("meaning_response"):
        return

    lens_name = entry.get("lens_name") or "Reflektif"
    question = entry.get("meaning_question") or ""
    micro_action = entry.get("micro_action") or ""
    st.markdown(
        f"""
        <div class="meaning-card">
            <div class="meaning-kicker">Sudut Pandang Hari Ini</div>
            <div class="meaning-lens">Lensa: {lens_name}</div>
            <div class="meaning-copy">{entry["meaning_response"]}</div>
            {f'<div class="meaning-small"><strong>Pertanyaan kecil:</strong> {question}</div>' if question else ''}
            {f'<div class="meaning-small"><strong>Langkah kecil:</strong> {micro_action}</div>' if micro_action else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_welcome(entries: list[dict]) -> None:
    st.markdown('<div class="welcome-space">', unsafe_allow_html=True)
    st.markdown('<div class="cozy-orbit"></div>', unsafe_allow_html=True)
    st.markdown('<div class="welcome-kicker">Early Reflective Beta</div>', unsafe_allow_html=True)
    st.markdown(f"### {generate_welcome(entries)}")
    st.markdown(
        '<div class="welcome-copy">Satu ruang kecil untuk menaruh hari ini, tanpa harus langsung kuat atau selesai.</div>',
        unsafe_allow_html=True,
    )
    continuity_prompt = detect_unfinished_thread(entries)
    if continuity_prompt:
        st.markdown(f'<p class="quiet-note">{continuity_prompt}</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


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


def parse_entry_date(entry: dict) -> date | None:
    raw_date = str(entry.get("entry_date") or entry.get("created_at") or "").strip()
    if not raw_date:
        return None
    try:
        return date.fromisoformat(raw_date[:10])
    except ValueError:
        return None


def get_weekly_mirror_entries(entries: list[dict]) -> list[dict]:
    today = date.today()
    week_start = today - timedelta(days=6)
    dated_entries = [
        entry
        for entry in entries
        if (entry_date := parse_entry_date(entry)) and week_start <= entry_date <= today
    ]
    return dated_entries or entries[:7]


def entry_text_for_mirror(entry: dict) -> str:
    return " ".join(
        [
            str(entry.get("activity") or ""),
            str(entry.get("personal_reflection") or ""),
            str(entry.get("gratitude_note") or ""),
            str(entry.get("improvement_action") or ""),
            str(entry.get("food") or ""),
        ]
    )


def collect_weekly_words(entries: list[dict], limit: int = 3) -> list[str]:
    words: list[str] = []
    for entry in entries:
        normalized = entry_text_for_mirror(entry).lower()
        cleaned = "".join(char if char.isalpha() or char.isspace() else " " for char in normalized)
        for word in cleaned.split():
            if len(word) >= 5 and word not in WEEKLY_MIRROR_STOPWORDS:
                words.append(word)

    word_counts = Counter(words)
    return [word for word, count in word_counts.most_common(limit) if count >= 2]


def collect_weekly_artifacts(entries: list[dict]) -> list[dict]:
    artifacts: list[dict] = []
    for entry in entries:
        for artifact in entry.get("memory_artifacts") or []:
            artifacts.append(artifact)
    return artifacts


def collect_memory_notes(artifacts: list[dict], limit: int = 3) -> list[str]:
    notes: list[str] = []
    for artifact in artifacts:
        note = str(artifact.get("memory_note") or "").strip()
        if note and note not in notes:
            notes.append(note)
        if len(notes) >= limit:
            break
    return notes


def collect_activity_fragments(entries: list[dict], limit: int = 3) -> list[str]:
    fragments: list[str] = []
    for entry in entries:
        activity = str(entry.get("activity") or "").strip()
        if activity and activity.lower() != "quick reflection" and activity not in fragments:
            fragments.append(activity)
        if len(fragments) >= limit:
            break
    return fragments


def build_weekly_mirror_lines(entries: list[dict]) -> list[str]:
    artifacts = collect_weekly_artifacts(entries)
    memory_notes = collect_memory_notes(artifacts)
    activities = collect_activity_fragments(entries)
    repeated_words = collect_weekly_words(entries)

    lines = ["Minggu ini sempat meninggalkan beberapa jejak kecil."]

    if activities:
        activities_text = ", ".join(activities[:2])
        lines.append(f"Ada catatan tentang {activities_text}.")

    if artifacts:
        if len(artifacts) == 1:
            lines.append("Ada satu foto yang ikut tersimpan.")
        else:
            lines.append("Ada beberapa foto yang ikut tersimpan.")

    if memory_notes:
        quoted_notes = " / ".join(f'"{note}"' for note in memory_notes[:2])
        lines.append(f"Ada catatan kecil: {quoted_notes}.")

    if repeated_words:
        quoted_words = ", ".join(f'"{word}"' for word in repeated_words)
        lines.append(f"Kata {quoted_words} sempat muncul lebih dari sekali.")

    if len(lines) == 1:
        lines.append("Tidak banyak yang perlu dipaksa menjadi cerita besar.")

    lines.append("Tidak banyak yang perlu disimpulkan dari itu.")
    lines.append("Tapi minggu ini sungguh terjadi.")
    return lines


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


def show_onboarding_note(entries: list[dict]) -> None:
    if entries:
        st.caption("Catatanmu bersifat personal. Ruang ini hanya menampilkan perjalananmu.")
    else:
        st.caption("Ruang ini akan perlahan mengenali ritme dan refleksimu.")


def show_input_page(reflection_style: str, entries: list[dict], user_id: str) -> None:
    st.title("Ruang Menulis")
    st.caption("Tidak perlu rapi. Cukup mulai dari bagian yang paling jujur.")

    st.markdown('<div class="mode-helper">Pilih ritme menulismu malam ini.</div>', unsafe_allow_html=True)
    if hasattr(st, "segmented_control"):
        mode = st.segmented_control(
            "Pilih cara menulis",
            ["Journal Lengkap", "Quick Reflection"],
            default="Journal Lengkap",
            label_visibility="collapsed",
        )
    else:
        mode = st.radio(
            "Pilih cara menulis",
            ["Journal Lengkap", "Quick Reflection"],
            horizontal=True,
        )

    if mode == "Quick Reflection":
        show_quick_reflection_form(entries, user_id)
    else:
        show_full_journal_form(reflection_style, entries, user_id)


def show_full_journal_form(reflection_style: str, entries: list[dict], user_id: str) -> None:
    with st.form("daily_journal_form", clear_on_submit=True):
        st.markdown(
            '<div class="journey-section-title">Awal catatan</div>'
            '<div class="journey-section-copy">Beri konteks kecil, agar dirimu nanti tahu hari ini sedang tentang apa.</div>',
            unsafe_allow_html=True,
        )
        entry_date = st.date_input("Tanggal", value=date.today())

        col_left, col_right = st.columns(2)
        with col_left:
            activity = st.text_input(
                "Aktivitas utama",
                placeholder="Misalnya: kerja panjang, ngobrol dengan teman, istirahat total",
            )
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
            food = st.text_input(
                "Makanan/minuman utama",
                placeholder="Apa yang cukup mewakili tubuhmu hari ini?",
            )
            calories = st.number_input(
                "Estimasi kalori",
                min_value=0,
                step=50,
                value=0,
            )

        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="journey-section">'
            '<div class="journey-section-title">Refleksi pribadi</div>'
            '<div class="journey-section-copy">Tulis bagian yang masih tertinggal. Tidak harus bijak, tidak harus selesai.</div>',
            unsafe_allow_html=True,
        )
        personal_reflection = st.text_area(
            "Yang paling terasa",
            placeholder="Apa yang paling tinggal di pikiranmu hari ini?",
            height=190,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="journey-section">'
            '<div class="journey-section-title">Catatan syukur</div>'
            '<div class="journey-section-copy">Cari satu titik kecil yang masih bisa menjadi pegangan.</div>',
            unsafe_allow_html=True,
        )
        gratitude_note = st.text_area(
            "Yang masih bisa disyukuri",
            placeholder="Satu hal kecil yang masih layak disyukuri.",
            height=130,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="journey-section">'
            '<div class="journey-section-title">Arah besok</div>'
            '<div class="journey-section-copy">Bukan target besar. Hanya satu gerakan kecil yang manusiawi.</div>',
            unsafe_allow_html=True,
        )
        improvement_action = st.text_area(
            "Satu hal kecil",
            placeholder="Jika besok sedikit lebih ringan, apa satu hal kecil yang ingin kamu coba?",
            height=130,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            '<div class="journey-section">'
            '<div class="journey-section-title">Memory Artifact</div>'
            '<div class="journey-section-copy">Jika suatu hari kamu melihat foto ini lagi, apa yang ingin kamu ingat?</div>',
            unsafe_allow_html=True,
        )
        memory_photo = st.file_uploader(
            "Upload 1 foto",
            type=["jpg", "jpeg", "png", "webp", "heic", "heif"],
            accept_multiple_files=False,
        )
        memory_note = st.text_area(
            "Catatan kecil opsional",
            placeholder="Satu kalimat kecil untuk dirimu nanti.",
            height=100,
        )
        st.markdown("</div>", unsafe_allow_html=True)

        submitted = st.form_submit_button("Simpan & Renungkan")

    if submitted:
        if not activity.strip():
            st.error("Aktivitas utama perlu diisi.")
            return
        image_error = validate_image_upload(memory_photo)
        if image_error:
            st.error(image_error)
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
            user_id,
        )
        entry = enrich_entry_with_meaning(entry, entries, reflection_style)
        saved_entry = save_entry(entry)
        artifact = None
        if memory_photo is not None:
            try:
                journal_context = " ".join(
                    [
                        activity,
                        personal_reflection,
                        gratitude_note,
                        improvement_action,
                        food,
                    ]
                )
                artifact = save_entry_memory_artifact(
                    saved_entry,
                    memory_photo,
                    memory_note,
                    user_id,
                    journal_context,
                )
            except CloudStorageError as exc:
                st.warning("Catatan tersimpan. Foto belum berhasil disimpan, jadi kamu bisa mencoba lagi nanti.")
                with st.expander("Detail teknis upload foto"):
                    st.code(str(exc))

        if artifact:
            saved_entry = {**saved_entry, "memory_artifacts": [artifact]}
        updated_entries = [saved_entry] + entries
        st.success("Catatan tersimpan.")
        if artifact:
            st.caption("Foto tersimpan bersama catatan ini.")
            if artifact.get("side_note"):
                st.caption(f"Catatan Pinggir: {artifact['side_note']}")
        st.markdown(
            f'<div class="companion-response">{generate_submit_response(saved_entry, updated_entries)}</div>',
            unsafe_allow_html=True,
        )
        show_emotion_note(saved_entry)
        show_meaning_response(saved_entry)

        with st.expander("Baca refleksi singkat"):
            st.write(generate_reflection(saved_entry, reflection_style))


def show_quick_reflection_form(entries: list[dict], user_id: str) -> None:
    with st.form("quick_reflection_form", clear_on_submit=True):
        st.markdown(
            '<div class="journey-section-title">Catatan cepat</div>'
            '<div class="journey-section-copy">Untuk hari ketika menulis panjang terasa terlalu berat.</div>',
            unsafe_allow_html=True,
        )
        entry_date = st.date_input("Tanggal", value=date.today(), key="quick_date")
        life_area = st.selectbox("Area hidup", LIFE_AREAS, key="quick_life_area")
        mood_score = st.slider("Mood", min_value=1, max_value=10, value=5, key="quick_mood")
        energy_score = st.slider("Energi", min_value=1, max_value=10, value=5, key="quick_energy")
        st.markdown('<div class="soft-divider"></div>', unsafe_allow_html=True)
        one_sentence = st.text_area(
            "Satu kalimat",
            placeholder="Hari ini yang paling terasa adalah...",
            height=150,
        )
        gratitude_note = st.text_input(
            "Syukur singkat (opsional)",
            placeholder="Satu hal kecil yang masih ada.",
        )

        submitted = st.form_submit_button("Tutup Hari Ini Dengan Tenang")

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
            user_id,
        )
        entry = enrich_entry_with_meaning(entry, entries, "Lembut")
        save_entry(entry)
        updated_entries = [entry] + entries
        st.success("Catatan singkat tersimpan.")
        st.markdown(
            f'<div class="companion-response">{generate_submit_response(entry, updated_entries)}</div>',
            unsafe_allow_html=True,
        )
        show_emotion_note(entry)
        show_meaning_response(entry)


def show_history_page() -> None:
    st.title("Jejak Catatan")
    st.caption("Beberapa hal memang baru terlihat setelah diberi jarak.")

    entries = load_entries(st.session_state["user_id"])
    if not entries:
        st.info("Belum ada jejak tulisan di sini. Kadang satu kalimat jujur sudah cukup untuk memulai.")
        return

    for entry in entries:
        render_entry_card(entry)

    with st.expander("Lihat detail tabel"):
        df = pd.DataFrame(entries)
        df["ditulis"] = df.apply(
            lambda row: format_human_time(row.get("created_at"), journal_date=row.get("entry_date")),
            axis=1,
        )
        display_columns = [
            "id",
            "ditulis",
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
            "lens_name",
            "meaning_question",
        ]
        st.dataframe(df[display_columns], use_container_width=True, hide_index=True)


def show_today_insight_page(reflection_style: str) -> None:
    st.title("Hari Ini")

    entries = load_entries(st.session_state["user_id"])
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
    render_memory_artifacts(latest_entry)

    if latest_entry.get("improvement_action"):
        st.write(f"Aksi berikutnya: {latest_entry['improvement_action']}")

    st.divider()
    show_meaning_response(latest_entry)

    st.divider()
    st.subheader("Bacaan singkat")
    st.write(generate_reflection(latest_entry, reflection_style))

    st.divider()
    show_pattern_noticing(entries)


def show_weekly_reflection_page() -> None:
    st.title("Cermin Mingguan")
    st.caption("Bukan laporan. Hanya beberapa jejak dari minggu yang baru lewat.")

    entries = load_entries(st.session_state["user_id"])
    if not entries:
        st.info("Belum ada cukup catatan untuk dipantulkan. Satu kalimat jujur pun sudah bisa menjadi awal.")
        return

    weekly_entries = get_weekly_mirror_entries(entries)
    mirror_lines = build_weekly_mirror_lines(weekly_entries)
    mirror_html = "".join(f'<p class="mirror-row">{line}</p>' for line in mirror_lines)
    st.markdown(
        f"""
        <div class="mirror-card">
            <div class="meaning-kicker">Cermin Mingguan</div>
            <div class="meaning-copy">{mirror_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    artifacts = collect_weekly_artifacts(weekly_entries)
    if artifacts:
        artifact = artifacts[0]
        image_source = artifact.get("image_url") or artifact.get("image_path")
        st.markdown("#### Yang ikut tersimpan")
        if image_source:
            st.image(image_source, width=180)
        if artifact.get("memory_note"):
            st.caption("Catatan kecil:")
            st.write(artifact["memory_note"])
        if artifact.get("side_note"):
            st.caption(f"Catatan Pinggir: {artifact['side_note']}")

    st.markdown(
        '<p class="quiet-note">Kalau ada satu bagian dari minggu ini yang masih ingin disimpan pelan-pelan, biarkan ia tetap di sini dulu.</p>',
        unsafe_allow_html=True,
    )


render_browser_identity_bridge()
require_access_code()

current_user_id = st.session_state["user_id"]
ensure_user_profile(current_user_id, utc_now_iso())
entries_at_start = load_entries(current_user_id)

st.sidebar.title("Reflective Life OS")
st.sidebar.markdown('<div class="beta-label">Early Reflective Beta</div>', unsafe_allow_html=True)
reflection_style = st.sidebar.selectbox("Reflection Style", REFLECTION_STYLES)
update_user_activity(current_user_id, utc_now_iso(), reflection_style)
page = st.sidebar.radio(
    "Navigasi",
    ["Input Harian", "History", "Insight Hari Ini", "Cermin Mingguan"],
)
show_feedback_section()

show_welcome(entries_at_start)
show_onboarding_note(entries_at_start)

if page == "Input Harian":
    show_input_page(reflection_style, entries_at_start, current_user_id)
elif page == "History":
    show_history_page()
elif page == "Insight Hari Ini":
    show_today_insight_page(reflection_style)
else:
    show_weekly_reflection_page()
