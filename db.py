from pathlib import Path
import sqlite3
from typing import Any
import uuid


DB_PATH = Path(__file__).parent / "data" / "journal.db"


def get_connection() -> sqlite3.Connection:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS journal_entries (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                entry_date TEXT,
                activity TEXT,
                life_area TEXT,
                duration_minutes INTEGER,
                cost REAL,
                food TEXT,
                calories INTEGER,
                mood_score INTEGER,
                energy_score INTEGER,
                personal_reflection TEXT,
                gratitude_note TEXT,
                improvement_action TEXT,
                created_at TEXT,
                updated_at TEXT,
                themes TEXT,
                lens_name TEXT,
                lens_source TEXT,
                meaning_response TEXT,
                meaning_question TEXT,
                micro_action TEXT
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_profiles (
                user_id TEXT PRIMARY KEY,
                first_seen_at TEXT,
                last_active_at TEXT,
                preferred_reflection_style TEXT,
                total_entries INTEGER DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS memory_artifacts (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                journal_entry_id INTEGER,
                image_path TEXT,
                memory_note TEXT,
                side_note TEXT,
                created_at TEXT
            )
            """
        )
        columns = {
            row["name"]
            for row in conn.execute("PRAGMA table_info(journal_entries)").fetchall()
        }
        if "life_area" not in columns:
            conn.execute("ALTER TABLE journal_entries ADD COLUMN life_area TEXT")
        if "user_id" not in columns:
            conn.execute("ALTER TABLE journal_entries ADD COLUMN user_id TEXT")
        if "updated_at" not in columns:
            conn.execute("ALTER TABLE journal_entries ADD COLUMN updated_at TEXT")
        meaning_columns = {
            "themes": "TEXT",
            "lens_name": "TEXT",
            "lens_source": "TEXT",
            "meaning_response": "TEXT",
            "meaning_question": "TEXT",
            "micro_action": "TEXT",
        }
        for column_name, column_type in meaning_columns.items():
            if column_name not in columns:
                conn.execute(f"ALTER TABLE journal_entries ADD COLUMN {column_name} {column_type}")
        conn.commit()


def ensure_user_profile(user_id: str, now: str, preferred_reflection_style: str = "Lembut") -> None:
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO user_profiles (
                user_id,
                first_seen_at,
                last_active_at,
                preferred_reflection_style,
                total_entries
            )
            VALUES (?, ?, ?, ?, 0)
            ON CONFLICT(user_id) DO UPDATE SET
                last_active_at = excluded.last_active_at,
                preferred_reflection_style = excluded.preferred_reflection_style
            """,
            (user_id, now, now, preferred_reflection_style),
        )
        conn.commit()


def update_user_activity(user_id: str, now: str, preferred_reflection_style: str) -> None:
    with get_connection() as conn:
        conn.execute(
            """
            UPDATE user_profiles
            SET last_active_at = ?,
                preferred_reflection_style = ?,
                total_entries = (
                    SELECT COUNT(*)
                    FROM journal_entries
                    WHERE user_id = ?
                )
            WHERE user_id = ?
            """,
            (now, preferred_reflection_style, user_id, user_id),
        )
        conn.commit()


def insert_entry(
    user_id: str,
    entry_date: str,
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
    created_at: str,
    updated_at: str,
    themes: str = "",
    lens_name: str = "",
    lens_source: str = "",
    meaning_response: str = "",
    meaning_question: str = "",
    micro_action: str = "",
) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO journal_entries (
                user_id,
                entry_date,
                activity,
                life_area,
                duration_minutes,
                cost,
                food,
                calories,
                mood_score,
                energy_score,
                personal_reflection,
                gratitude_note,
                improvement_action,
                created_at,
                updated_at,
                themes,
                lens_name,
                lens_source,
                meaning_response,
                meaning_question,
                micro_action
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                user_id,
                entry_date,
                activity,
                life_area,
                duration_minutes,
                cost,
                food,
                calories,
                mood_score,
                energy_score,
                personal_reflection,
                gratitude_note,
                improvement_action,
                created_at,
                updated_at,
                themes,
                lens_name,
                lens_source,
                meaning_response,
                meaning_question,
                micro_action,
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def insert_memory_artifact(
    user_id: str,
    journal_entry_id: int,
    image_path: str,
    memory_note: str,
    side_note: str,
    created_at: str,
    artifact_id: str | None = None,
) -> dict[str, Any]:
    artifact_id = artifact_id or str(uuid.uuid4())
    with get_connection() as conn:
        conn.execute(
            """
            INSERT INTO memory_artifacts (
                id,
                user_id,
                journal_entry_id,
                image_path,
                memory_note,
                side_note,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                artifact_id,
                user_id,
                int(journal_entry_id),
                image_path,
                memory_note,
                side_note,
                created_at,
            ),
        )
        conn.commit()
    return {
        "id": artifact_id,
        "user_id": user_id,
        "journal_entry_id": int(journal_entry_id),
        "image_path": image_path,
        "image_url": image_path,
        "memory_note": memory_note,
        "side_note": side_note,
        "created_at": created_at,
    }


def get_entries(user_id: str) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM journal_entries
            WHERE user_id = ?
            ORDER BY created_at DESC, entry_date DESC, id DESC
            """,
            (user_id,),
        ).fetchall()
    return [dict(row) for row in rows]


def get_memory_artifacts(user_id: str) -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM memory_artifacts
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        ).fetchall()
    artifacts = [dict(row) for row in rows]
    for artifact in artifacts:
        artifact["image_url"] = artifact.get("image_path")
    return artifacts


def get_entry_by_id(entry_id: int, user_id: str) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM journal_entries WHERE id = ? AND user_id = ?",
            (entry_id, user_id),
        ).fetchone()
    return dict(row) if row else None
