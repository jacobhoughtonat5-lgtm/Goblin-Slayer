#!/usr/bin/env python3
"""
Fast structural consistency checker for the game state + memory system.
Exits with code 0 on success, 1 on any error.
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "state" / "current.json"
MEMORIES_DIR = ROOT / "memories"
INDEX_FILE = MEMORIES_DIR / "index.json"

errors = []

def err(msg: str):
    errors.append(msg)
    print(f"ERROR: {msg}")

def load_json(path: Path):
    if not path.exists():
        err(f"Missing required file: {path.relative_to(ROOT)}")
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        err(f"Invalid JSON in {path.relative_to(ROOT)}: {e}")
        return None

def main():
    print("→ Validating game state and memories...")

    # 1. Core state file
    state = load_json(STATE_FILE)
    if state is None:
        sys.exit(1)

    required_top = ["gameInfo", "player", "world", "characters"]
    for key in required_top:
        if key not in state:
            err(f"state/current.json missing required key: {key}")

    # 2. Memories index
    index = load_json(INDEX_FILE)
    if index is None:
        sys.exit(1)

    characters_with_memories = set(index.get("charactersWithMemories", []))

    # 3. Check every character that claims a memory file
    characters = state.get("characters", {})
    player = state.get("player", {})

    # Player memory
    if "memoryFile" in player:
        mem_path = ROOT / player["memoryFile"]
        if not mem_path.exists():
            err(f"Player memoryFile does not exist: {player['memoryFile']}")
        else:
            characters_with_memories.add("player")

    # NPC memories
    for char_id, char_data in characters.items():
        mem_file = char_data.get("memoryFile")
        if not mem_file:
            continue

        mem_path = ROOT / mem_file
        if not mem_path.exists():
            err(f"Character '{char_id}' memoryFile missing: {mem_file}")
            continue

        mem_data = load_json(mem_path)
        if mem_data is None:
            continue

        # Check salient memories actually exist
        salient = char_data.get("salientMemories", [])
        existing_ids = {m.get("id") for m in mem_data.get("memories", []) if m.get("id")}

        for sid in salient:
            if sid not in existing_ids:
                err(f"Character '{char_id}' salientMemory '{sid}' not found in {mem_file}")

        # Basic memory integrity
        seen_ids = set()
        for mem in mem_data.get("memories", []):
            mid = mem.get("id")
            if not mid:
                err(f"Memory without id in {mem_file}")
                continue
            if mid in seen_ids:
                err(f"Duplicate memory id '{mid}' in {mem_file}")
            seen_ids.add(mid)

            if "type" not in mem:
                err(f"Memory '{mid}' missing 'type' in {mem_file}")
            if "importance" not in mem:
                err(f"Memory '{mid}' missing 'importance' in {mem_file}")
            else:
                imp = mem["importance"]
                if not isinstance(imp, int) or not (1 <= imp <= 10):
                    err(f"Memory '{mid}' has invalid importance {imp} (must be 1-10)")

    # 4. Check index consistency
    for char_id in characters_with_memories:
        if char_id == "player":
            if not (MEMORIES_DIR / "player.json").exists():
                err("index lists 'player' but memories/player.json is missing")
        else:
            expected = MEMORIES_DIR / f"{char_id}.json"
            if not expected.exists():
                err(f"index lists '{char_id}' but {expected.relative_to(ROOT)} is missing")

    # Final result
    if errors:
        print(f"\nFailed with {len(errors)} error(s).")
        sys.exit(1)
    else:
        print("✓ All consistency checks passed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
