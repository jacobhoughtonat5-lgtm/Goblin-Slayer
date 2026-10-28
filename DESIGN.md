# Game Design Document

## Overview

This is a persistent, memory-driven text adventure / RPG designed to be played in chat with an AI game master (Grok).  

All state — including every character’s personal memories of events, conversations, and knowledge — is stored in this GitHub repository so the game can be resumed perfectly across sessions, devices, and time.

## Core Pillars

1. **Personal Memories**  
   Every reappearing character (player + NPCs) maintains their own subjective record of:
   - Events they experienced or witnessed
   - Conversations (key statements, tone, promises, secrets)
   - Knowledge they acquired (facts, rumors, lies they believe)

2. **Unlimited Reappearing Cast**  
   There is no hard limit on “main characters.” Any NPC that returns can accumulate a full personal memory bank. Memory files are created lazily.

3. **GitHub as Source of Truth**  
   `state/current.json` + the `memories/` folder are the canonical state. Git history provides unlimited versioning, branching, and rollback.

4. **Consistency First**  
   A validation script runs on every push to catch structural problems early.

## Memory System Rules

- Memories are always written from the character’s point of view and knowledge level.
- A character only gets a memory file the first time they have a meaningful interaction or learn something important.
- High-importance memories (secrets, trauma, major shared events, strong emotional moments) are kept indefinitely.
- Low-importance memories may later be summarized or moved to `memories/archive/`.
- When conversing with an NPC, relevant memories shape tone, references, trust, and available information.

## State Update Workflow

1. Player takes an action.
2. AI resolves the action and determines which characters form new memories.
3. AI updates `state/current.json` and the relevant `memories/*.json` files.
4. On `save` / `commit`, AI outputs the changed files.
5. Player commits & pushes to GitHub.
6. Next session loads the latest committed state.

## Win / Loss Conditions

(Define these for your specific game. Examples below are placeholders.)

- **Victory**: ...
- **Defeat**: ...

## Tone & Style Guidelines

(Fill in according to the genre you choose.)

- Narrative voice: second-person, present tense
- Level of detail: ...
- Handling of failure / death: ...
- Romance / mature content: ...

## Extending the System

- Add new top-level sections to `current.json` as needed (factions, weather, magic systems, etc.).
- Memory files can grow large; the validation script and indexes keep retrieval efficient.
- Named saves can be created by copying `state/current.json` + relevant memory files into `saves/<name>/`.
