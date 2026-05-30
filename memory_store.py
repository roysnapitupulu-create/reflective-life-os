# memory_store.py

import json
from pathlib import Path


MEMORY_FILE = Path("memory_store.json")


def load_entries():
    if not MEMORY_FILE.exists():
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def save_entries(entries):
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(
            entries,
            f,
            ensure_ascii=False,
            indent=2
        )


def append_entry(entry):
    entries = load_entries()
    entries.append(entry)
    save_entries(entries)