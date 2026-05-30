import sys

from context_compiler import compile_daily_context, generate_contextual_side_note
from memory_store import append_entry, load_entries
from memory_symbol_layer import build_scene_memory, build_symbol_memory, generate_memory_side_note

try:
    from meaning_synthesizer import synthesize_meaning_v2
except Exception:
    synthesize_meaning_v2 = None


def main() -> None:
    text = " ".join(sys.argv[1:]).strip()

    if not text:
        print("Usage:")
        print('  python simulator.py "ThinkPad tua menemani lembur malam ini."')
        return

    entry = {
        "activity": "",
        "personal_reflection": text,
        "gratitude_note": "",
        "improvement_action": "",
    }

    artifact = {
        "memory_note": text,
    }

    context = compile_daily_context(entry, artifact)

    existing_entries = load_entries()

    symbol_memory_before = build_symbol_memory(existing_entries)
    memory_note = generate_memory_side_note(
        context.get("symbols", []),
        symbol_memory_before,
    )

    current_memory_entry = {
        "raw_text": text,
        "themes": context.get("themes", []),
        "symbols": context.get("symbols", []),
        "scene": context.get("scene", {}),
        "emotions": context.get("emotions", []),
        "time_context": context.get("time_context"),
    }

    append_entry(current_memory_entry)

    updated_entries = load_entries()
    symbol_memory_after = build_symbol_memory(updated_entries)
    scene_memory_after = build_scene_memory(updated_entries)

    print("\n=== INPUT ===")
    print(text)

    print("\n=== CONTEXT ===")
    print(f"themes       : {context.get('themes')}")
    print(f"symbols      : {context.get('symbols')}")
    print(f"scene        : {context.get('scene')}")
    print(f"emotions     : {context.get('emotions')}")
    print(f"time_context : {context.get('time_context')}")
    print(f"spiritual    : {context.get('is_spiritual')}")
    print(f"simple_life  : {context.get('is_simple_life')}")
    print(f"gratitude    : {context.get('has_gratitude')}")
    print(f"slow_pace    : {context.get('has_slow_pace')}")

    if synthesize_meaning_v2:
        meaning = synthesize_meaning_v2(context)
        print("\n=== MEANING V2 ===")
        print(f"theme        : {meaning.get('theme')}")
        print(f"observation  : {meaning.get('observation')}")
        print(f"side_note    : {meaning.get('side_note')}")
        if meaning.get("reflection_question"):
            print(f"question     : {meaning.get('reflection_question')}")
        if meaning.get("voice"):
            print(f"voice        : {meaning.get('voice')}")

    print("\n=== MEMORY SYMBOL LAYER ===")
    print(f"entries_before : {len(existing_entries)}")
    print(f"entries_after  : {len(updated_entries)}")
    print(f"symbol_memory  : {symbol_memory_after}")
    print(f"scene_memory   : {scene_memory_after}")
    print(f"memory_note    : {memory_note}")

    print("\n=== FINAL SIDE NOTE ===")
    final_side_note = generate_contextual_side_note(context)

    if memory_note:
        print(memory_note)
    else:
        print(final_side_note)


if __name__ == "__main__":
    main()