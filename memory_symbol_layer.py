# memory_symbol_layer.py

from collections import Counter
from typing import Any


def build_symbol_memory(entries: list[dict[str, Any]], min_count: int = 2) -> dict[str, dict[str, Any]]:
    symbol_counter: Counter[str] = Counter()

    for entry in entries:
        symbols = entry.get("symbols") or []
        if not isinstance(symbols, list):
            continue

        unique_symbols = list(dict.fromkeys(str(symbol) for symbol in symbols if symbol))
        symbol_counter.update(unique_symbols)

    memory: dict[str, dict[str, Any]] = {}

    for symbol, count in symbol_counter.items():
        if count >= min_count:
            memory[symbol] = {
                "count": count,
                "status": "recurring",
            }

    return memory


def build_scene_memory(entries: list[dict[str, Any]], min_count: int = 2) -> dict[str, dict[str, Any]]:
    scene_counter: Counter[str] = Counter()

    for entry in entries:
        scene = entry.get("scene") or {}
        if not isinstance(scene, dict):
            continue

        actors = scene.get("actors") or []
        actions = scene.get("actions") or []
        settings = scene.get("settings") or []

        for actor in actors:
            for action in actions:
                key = f"{actor}:{action}"
                scene_counter.update([key])

        for action in actions:
            for setting in settings:
                key = f"{action}@{setting}"
                scene_counter.update([key])

    memory: dict[str, dict[str, Any]] = {}

    for scene_key, count in scene_counter.items():
        if count >= min_count:
            memory[scene_key] = {
                "count": count,
                "status": "recurring",
            }

    return memory


def summarize_symbol_memory(symbol_memory: dict[str, dict[str, Any]]) -> list[str]:
    summaries: list[str] = []

    for symbol, data in symbol_memory.items():
        count = data.get("count", 0)

        summaries.append(
            f"Simbol '{symbol}' muncul berulang sebanyak {count} kali. "
            "Ini mungkin mulai menjadi tanda kecil yang layak diperhatikan."
        )

    return summaries


def generate_memory_side_note(current_symbols: list[str], symbol_memory: dict[str, dict[str, Any]]) -> str:
    for symbol in current_symbols:
        if symbol in symbol_memory:
            count = symbol_memory[symbol].get("count", 0)

            if symbol == "warung":
                return (
                    f"Warung muncul lagi dalam catatanmu. Setelah {count} kemunculan, "
                    "mungkin ia bukan sekadar tempat membeli sesuatu, tetapi tanda kecil "
                    "bahwa hidupmu sering mencari jeda di tempat-tempat sederhana."
                )

            if symbol == "tree":
                return (
                    f"Pohon muncul lagi dalam catatanmu. Setelah {count} kemunculan, "
                    "mungkin ada bagian dari dirimu yang terus mengenali arti teduh, "
                    "akar, dan ketahanan yang tidak banyak bicara."
                )

            if symbol == "ojol":
                return (
                    f"Ojol muncul lagi dalam catatanmu. Setelah {count} kemunculan, "
                    "mungkin kamu sedang sering memperhatikan manusia-manusia yang bekerja "
                    "di sela tunggu, jalan, dan ketidakpastian rezeki."
                )

            return (
                f"Simbol '{symbol}' muncul lagi dalam catatanmu. Setelah {count} kemunculan, "
                "mungkin ini mulai menjadi benang kecil yang menghubungkan beberapa hari."
            )

    return ""