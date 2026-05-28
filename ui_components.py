from typing import Any

import streamlit as st

from emotion_engine import extract_entry_emotions


def render_entry_card(entry: dict[str, Any]) -> None:
    with st.container(border=True):
        st.caption(entry.get("entry_date", "-"))
        st.markdown(f"**{entry.get('activity') or 'Catatan hari ini'}**")
        if entry.get("life_area"):
            st.caption(f"Area: {entry.get('life_area')}")
        st.write(
            f"Mood: {entry.get('mood_score')}/10 | "
            f"Energi: {entry.get('energy_score')}/10 | "
            f"Durasi: {entry.get('duration_minutes')} menit"
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
