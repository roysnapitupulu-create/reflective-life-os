# memory_test.py

from memory_symbol_layer import (
    build_scene_memory,
    build_symbol_memory,
    generate_memory_side_note,
    summarize_symbol_memory,
)


entries = [
    {
        "symbols": ["warung"],
        "scene": {
            "actors": [],
            "actions": [],
            "settings": ["warung", "malam"],
        },
    },
    {
        "symbols": ["tree"],
        "scene": {
            "actors": [],
            "actions": ["berteduh"],
            "settings": ["jalan"],
        },
    },
    {
        "symbols": ["warung"],
        "scene": {
            "actors": [],
            "actions": [],
            "settings": ["warung", "malam"],
        },
    },
    {
        "symbols": ["ojol", "lampu_merah", "tree"],
        "scene": {
            "actors": ["ojol"],
            "actions": ["menunggu", "berteduh"],
            "settings": ["lampu_merah"],
        },
    },
    {
        "symbols": ["warung"],
        "scene": {
            "actors": [],
            "actions": [],
            "settings": ["warung", "malam"],
        },
    },
]

symbol_memory = build_symbol_memory(entries)
scene_memory = build_scene_memory(entries)

print("=== SYMBOL MEMORY ===")
print(symbol_memory)

print("\n=== SCENE MEMORY ===")
print(scene_memory)

print("\n=== SUMMARY ===")
for line in summarize_symbol_memory(symbol_memory):
    print("-", line)

print("\n=== MEMORY SIDE NOTE ===")
print(generate_memory_side_note(["warung"], symbol_memory))