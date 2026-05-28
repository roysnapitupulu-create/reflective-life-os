import json
import os
from typing import Any

try:
    import streamlit as st
except Exception:
    st = None

try:
    from supabase import create_client
except Exception:
    create_client = None


TABLE_NAME = "journal_entries"


class CloudStorageError(Exception):
    pass


def _get_secret(name: str, default: str = "") -> str:
    env_value = os.getenv(name, "").strip()
    if env_value:
        return env_value

    if st is None:
        return default

    try:
        return str(st.secrets.get(name, default)).strip()
    except Exception:
        return default


def is_supabase_enabled() -> bool:
    backend = _get_secret("DATABASE_BACKEND").lower()
    return (
        backend == "supabase"
        and bool(_get_secret("SUPABASE_URL"))
        and bool(_get_secret("SUPABASE_KEY"))
        and create_client is not None
    )


def _client():
    if not is_supabase_enabled():
        raise CloudStorageError("Supabase is not configured.")

    try:
        return create_client(_get_secret("SUPABASE_URL"), _get_secret("SUPABASE_KEY"))
    except Exception as exc:
        raise CloudStorageError("Storage cloud belum bisa diakses.") from exc


def _themes_to_jsonb(value: Any) -> list[str]:
    if isinstance(value, list):
        return value
    if not value:
        return []
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return parsed if isinstance(parsed, list) else []
        except json.JSONDecodeError:
            return [value]
    return []


def _to_supabase_row(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        "user_id": entry.get("user_id"),
        "created_at": entry.get("created_at"),
        "updated_at": entry.get("updated_at"),
        "journal_date": entry.get("entry_date"),
        "life_area": entry.get("life_area"),
        "activity": entry.get("activity"),
        "duration_minutes": entry.get("duration_minutes"),
        "cost": entry.get("cost"),
        "food": entry.get("food"),
        "calories": entry.get("calories"),
        "mood": entry.get("mood_score"),
        "energy": entry.get("energy_score"),
        "personal_reflection": entry.get("personal_reflection"),
        "gratitude_note": entry.get("gratitude_note"),
        "improvement_action": entry.get("improvement_action"),
        "themes": _themes_to_jsonb(entry.get("themes")),
        "lens_name": entry.get("lens_name"),
        "lens_source": entry.get("lens_source"),
        "meaning_response": entry.get("meaning_response"),
        "meaning_question": entry.get("meaning_question"),
        "micro_action": entry.get("micro_action"),
        "created_source": entry.get("created_source", "streamlit"),
    }


def _from_supabase_row(row: dict[str, Any]) -> dict[str, Any]:
    themes = row.get("themes") or []
    return {
        "id": row.get("id"),
        "user_id": row.get("user_id"),
        "entry_date": row.get("journal_date"),
        "activity": row.get("activity") or "",
        "life_area": row.get("life_area") or "",
        "duration_minutes": row.get("duration_minutes") or 0,
        "cost": row.get("cost") or 0,
        "food": row.get("food") or "",
        "calories": row.get("calories") or 0,
        "mood_score": row.get("mood") or 0,
        "energy_score": row.get("energy") or 0,
        "personal_reflection": row.get("personal_reflection") or "",
        "gratitude_note": row.get("gratitude_note") or "",
        "improvement_action": row.get("improvement_action") or "",
        "created_at": row.get("created_at") or "",
        "updated_at": row.get("updated_at") or "",
        "themes": json.dumps(themes, ensure_ascii=False),
        "lens_name": row.get("lens_name") or "",
        "lens_source": row.get("lens_source") or "",
        "meaning_response": row.get("meaning_response") or "",
        "meaning_question": row.get("meaning_question") or "",
        "micro_action": row.get("micro_action") or "",
    }


def save_journal_entry(entry: dict[str, Any]) -> dict[str, Any]:
    try:
        response = _client().table(TABLE_NAME).insert(_to_supabase_row(entry)).execute()
    except Exception as exc:
        raise CloudStorageError("Storage cloud belum bisa diakses.") from exc

    data = response.data or []
    return _from_supabase_row(data[0]) if data else entry


def load_journal_entries(user_id: str, limit: int = 100) -> list[dict[str, Any]]:
    try:
        response = (
            _client()
            .table(TABLE_NAME)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .limit(limit)
            .execute()
        )
    except Exception as exc:
        raise CloudStorageError("Storage cloud belum bisa diakses.") from exc

    return [_from_supabase_row(row) for row in response.data or []]


def get_recent_entries(user_id: str, limit: int = 10) -> list[dict[str, Any]]:
    return load_journal_entries(user_id, limit=limit)


def get_entries_by_date(user_id: str, journal_date: str) -> list[dict[str, Any]]:
    try:
        response = (
            _client()
            .table(TABLE_NAME)
            .select("*")
            .eq("user_id", user_id)
            .eq("journal_date", str(journal_date))
            .order("created_at", desc=True)
            .execute()
        )
    except Exception as exc:
        raise CloudStorageError("Storage cloud belum bisa diakses.") from exc

    return [_from_supabase_row(row) for row in response.data or []]
