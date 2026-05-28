from pathlib import Path
import sqlite3
from typing import Any


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
        conn.commit()


def insert_entry(
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
) -> int:
    with get_connection() as conn:
        cursor = conn.execute(
            """
            INSERT INTO journal_entries (
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
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
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
            ),
        )
        conn.commit()
        return int(cursor.lastrowid)


def get_entries() -> list[dict[str, Any]]:
    with get_connection() as conn:
        rows = conn.execute(
            """
            SELECT *
            FROM journal_entries
            ORDER BY entry_date DESC, created_at DESC, id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def get_entry_by_id(entry_id: int) -> dict[str, Any] | None:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT * FROM journal_entries WHERE id = ?",
            (entry_id,),
        ).fetchone()
    return dict(row) if row else None
