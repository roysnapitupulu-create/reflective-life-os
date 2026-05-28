from typing import Any

import streamlit as st

from emotion_engine import extract_entry_emotions


def render_entry_card(entry: dict[str, Any]) -> None:
    with st.container(border=True):
        st.markdown(
            f"""
            <div style="color:#e7bf88;font-size:0.82rem;margin-bottom:0.35rem;">
                {entry.get("entry_date", "-")}
            </div>
            <div style="font-size:1.08rem;font-weight:700;color:#f7eadb;margin-bottom:0.25rem;">
                {entry.get("activity") or "Catatan hari ini"}
            </div>
            """,
            unsafe_allow_html=True,
        )
        if entry.get("life_area"):
            st.caption(f"Area: {entry.get('life_area')}")
        st.markdown(
            f"""
            <div style="
                display:flex;
                gap:0.45rem;
                flex-wrap:wrap;
                margin:0.65rem 0 0.75rem;
                color:#d8c8b6;
                font-size:0.9rem;
            ">
                <span>Mood {entry.get("mood_score")}/10</span>
                <span>Energi {entry.get("energy_score")}/10</span>
                <span>{entry.get("duration_minutes")} menit</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        emotions = extract_entry_emotions(entry)
        if emotions:
            st.caption(f"Nuansa hari ini: {', '.join(emotions)}")

        if entry.get("personal_reflection"):
            st.markdown("**Yang tertulis:**")
            st.write(entry["personal_reflection"])

        if entry.get("gratitude_note"):
            st.markdown("**Yang masih bisa disyukuri:**")
            st.write(entry["gratitude_note"])

        if entry.get("improvement_action"):
            st.markdown("**Untuk besok:**")
            st.write(entry["improvement_action"])
