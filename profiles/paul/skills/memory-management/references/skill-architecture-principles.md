# Skill Architecture Principles

Joe's preference for how Paul's skill library should be shaped, established 2026-05-29.

## Class-Level Umbrellas, Not Narrow One-Shots

Target shape: CLASS-LEVEL skills, each with a rich SKILL.md and a `references/` directory for session-specific detail. Not a long flat list of narrow one-session-one-skill entries.

- **Bad:** `fix-bruiser-card-17`, `debug-cascade-test-a`, `audit-roster-2026-05-29`
- **Good:** `bruiser-card-design` (umbrella, with `references/` for specific passes, rosters, scoring tables)

## references/ Directory

Session-specific detail goes in `references/` under the umbrella skill — error transcripts, reproduction recipes, specific roster snapshots, scoring tables. The SKILL.md stays lean and class-level; the `references/` holds the concrete artifacts.

## templates/ and scripts/

- `templates/` — starter files meant to be copied and modified (boilerplate configs, card templates, scoring sheets)
- `scripts/` — re-runnable actions (verification scripts, fixture generators, deterministic probes)

## When to Create New vs Extend Existing

1. **Patch a currently-loaded skill first** — if a skill was loaded this session and covers the territory, extend it.
2. **Patch an existing umbrella** — if no loaded skill fits but an existing class-level skill does.
3. **Add a support file** — if the learning is session-specific detail, not structural change.
4. **Create new umbrella** — only if no existing skill covers the class of work.

## Don't Capture

- Environment-dependent failures (missing binaries, path mismatches)
- Negative claims about tools ("X tool is broken")
- Session-specific transient errors that resolved
- One-off task narratives
