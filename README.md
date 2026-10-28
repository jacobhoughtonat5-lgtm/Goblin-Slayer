# Persistent Chat Game

A text-based chat game with **unlimited persistent character memories** and full state stored in this GitHub repository.

## Core Idea

- The entire game world, player state, and every reappearing NPC’s personal memories (events, conversations, knowledge) live in this repository.
- Memories are subjective and per-character. NPCs remember what *they* experienced or were told, and will reference those memories in later conversations.
- There is no limit on how many NPCs can have their own memory banks — only characters that actually interact receive memory files.
- Every important change can be committed. Git history becomes the permanent record of the story.

## Quick Start

1. Clone or download this repository.
2. Copy the contents into a new GitHub repository (public or private).
3. On first play, tell the AI (Grok) the repository URL or paste the contents of `state/current.json` + relevant memory files.
4. Play in chat. After major turns or when you type `save`, the AI will output updated files.
5. Commit and push the changes.
6. To resume later: open a new chat and point the AI at this repository (or the latest files).

## Key Commands (in chat)

- `status` / `where am I?` — Current situation summary
- `save` / `commit` — Output the files that need updating
- `what does [NPC] remember about me?`
- `full status` — Detailed character + world state
- `load latest` — Reload from the repository

## Repository Layout

```
state/current.json          ← Live game state (source of truth)
memories/                   ← Personal memory banks (one file per character)
  player.json
  <npc-id>.json
  index.json
world/                      ← Static & semi-static world data
scripts/validate_state.py   ← Consistency checker
.github/workflows/          ← Runs validation on every push
```

## Validation

A GitHub Action automatically checks structural consistency on every push.
You can also run it locally:

```bash
python scripts/validate_state.py
# or
./scripts/validate.sh
```

## License

This starter is free to use and modify for your own games.
