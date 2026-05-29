import json
import os
from typing import Any
import uuid

from memory_artifacts import get_image_extension

try:
    import streamlit as st
except Exception:
    st = None

try:
    from supabase import create_client
except Exception:
    create_client = None


TABLE_NAME = "journal_entries"
MEMORY_ARTIFACTS_TABLE = "memory_artifacts"
MEMORY_ARTIFACTS_BUCKET = "memory-artifacts"


class CloudStorageError(Exception):
    pass


def _describe_exception(exc: Exception) -> str:
    parts = [type(exc).__name__]
    message = str(exc).strip()
    if message:
        parts.append(message)
    if getattr(exc, "args", None):
        parts.append(f"args={exc.args!r}")
    response = getattr(exc, "response", None)
    if response is not None:
        status_code = getattr(response, "status_code", "")
        text = getattr(response, "text", "")
        if status_code:
            parts.append(f"status={status_code}")
        if text:
            parts.append(f"response={text}")
    return " | ".join(parts)


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


def _signed_url_for_path(path: str) -> str:
    if not path:
        return ""
    try:
        response = _client().storage.from_(MEMORY_ARTIFACTS_BUCKET).create_signed_url(path, 60 * 60)
    except Exception:
        return ""

    if isinstance(response, dict):
        return str(response.get("signedURL") or response.get("signedUrl") or response.get("signed_url") or "")

    data = getattr(response, "data", None)
    if isinstance(data, dict):
        return str(data.get("signedURL") or data.get("signedUrl") or data.get("signed_url") or "")
    return str(getattr(response, "signed_url", "") or "")


def _from_artifact_row(row: dict[str, Any]) -> dict[str, Any]:
    image_path = row.get("image_path") or ""
    return {
        "id": row.get("id"),
        "user_id": row.get("user_id"),
        "journal_entry_id": row.get("journal_entry_id"),
        "image_path": image_path,
        "image_url": _signed_url_for_path(image_path),
        "memory_note": row.get("memory_note") or "",
        "side_note": row.get("side_note") or "",
        "created_at": row.get("created_at") or "",
    }


def save_memory_artifact(
    user_id: str,
    journal_entry_id: Any,
    image_bytes: bytes,
    filename: str,
    content_type: str,
    memory_note: str,
    side_note: str,
    created_at: str,
) -> dict[str, Any]:
    artifact_id = str(uuid.uuid4())
    extension = get_image_extension(filename, content_type)
    image_path = f"{user_id}/{journal_entry_id}/{artifact_id}{extension}"

    try:
        bucket = _client().storage.from_(MEMORY_ARTIFACTS_BUCKET)
        file_options = {
            "content-type": content_type or "image/jpeg",
            "cache-control": "3600",
            "upsert": "false",
        }
        try:
            bucket.upload(path=image_path, file=image_bytes, file_options=file_options)
        except TypeError:
            bucket.upload(image_path, image_bytes, file_options)
    except Exception as exc:
        raise CloudStorageError(f"Foto belum bisa diunggah ke storage: {_describe_exception(exc)}") from exc

    try:
        response = (
            _client()
            .table(MEMORY_ARTIFACTS_TABLE)
            .insert(
                {
                    "id": artifact_id,
                    "user_id": user_id,
                    "journal_entry_id": str(journal_entry_id),
                    "image_path": image_path,
                    "memory_note": memory_note,
                    "side_note": side_note,
                    "created_at": created_at,
                }
            )
            .execute()
        )
    except Exception as exc:
        try:
            _client().storage.from_(MEMORY_ARTIFACTS_BUCKET).remove([image_path])
        except Exception:
            pass
        raise CloudStorageError(f"Metadata foto belum bisa disimpan: {_describe_exception(exc)}") from exc

    data = response.data or []
    return _from_artifact_row(data[0]) if data else {
        "id": artifact_id,
        "user_id": user_id,
        "journal_entry_id": journal_entry_id,
        "image_path": image_path,
        "image_url": _signed_url_for_path(image_path),
        "memory_note": memory_note,
        "side_note": side_note,
        "created_at": created_at,
    }


def load_memory_artifacts(user_id: str) -> list[dict[str, Any]]:
    try:
        response = (
            _client()
            .table(MEMORY_ARTIFACTS_TABLE)
            .select("*")
            .eq("user_id", user_id)
            .order("created_at", desc=True)
            .execute()
        )
    except Exception as exc:
        raise CloudStorageError("Memory artifact belum bisa dibaca.") from exc

    return [_from_artifact_row(row) for row in response.data or []]


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
