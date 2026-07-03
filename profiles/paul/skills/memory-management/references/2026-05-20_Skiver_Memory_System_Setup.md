# 2026-05-20 — Skiver Memory System Setup

**Session Focus:** Building a complete, self-managed memory and context system for long-term creative work (Skiver faction development + general project memory).

## What Was Built

- `Brain/` folder structure at vault root (protected memory home)
- `Daily/` — Full session handovers with synopsis + timestamped compressions
- `Working Memory/` — Slim, fast-loading context (latest 1–2 compressions only)
- `Session Context/` — Raw source documents organized by date
- `Archive/` — Long-term storage (2-month rule)
- `Protocols/` — Detailed, standalone process documents
- Updated `AGENTS.md` with:
  - Explicit Autonomy clause
  - Trigger Rules section
  - References to all protocols

## Key Design Decisions

- Compression is primarily **user-initiated** ("compress this", "let's do a compression")
- Working Memory stays intentionally slim to reduce context load on new sessions
- Daily Handover is the source of truth and contains full detail + rationale
- All memory work is version-controlled inside the user's Obsidian vault (not a proprietary system)

## Lessons Captured

- User wants minimal, clean instructions in `AGENTS.md` rather than exhaustive rules
- User prefers the agent to take initiative on completing memory tasks once direction is given
- Context recovery should not require re-reading full chat logs

## Open Items

- Continue refining protocols as real usage reveals friction points
- Test the system across multiple sessions to validate compression cadence and handover quality

---

*This reference captures the initial implementation and rationale for the memory-management system.*