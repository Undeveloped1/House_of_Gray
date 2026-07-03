---
name: trigger-factory-run
description: Spawn a fresh Hermes instance to build a Trigger faction card set using function-first pipeline. Used by Paul (orchestrator) to delegate 55-card set design.
category: creative
---

# Trigger Factory Run

Spawn a fresh Hermes instance via tmux to build a Trigger faction set following the pipeline: Phase 0 (lore lock) → Phase 1 (function registry + synergy web) → band allocation → card expressions.

## When to Use

- Joe asks for a Trigger faction card set (55 cards + 3 heroes)
- Overnight autonomous design runs
- Any large-scale Trigger design pass that needs clean context

## Prerequisites

Before spawning, ensure:
1. tcg-engine repo is up to date (`cd /root/tcg-engine && git pull`)
2. Warmup doc exists with: function registry, synergy web, band allocation, process steps, lore references
3. Output path confirmed: `/root/syncthing/paul-dropbox/`

## Document Reading Order

The fresh instance must read documents in this order:

1. **Navigation:** `STATE_OF_THE_CORPUS.md`, `TOOLS_INDEX.md` (in tcg-engine repo)
2. **Faction router:** `docs/Five_Crests/factions/Trigger/00_INDEX.md`
3. **Lore + identity:** `Identity.md`, `Territory.md` (Trigger faction dir)
4. **Playstyle + engine:** `Playstyle.md`, `Hero_Cards.md` (Trigger faction dir)
5. **Mechanics:** `Mechanics_Budget.md`, `Functions.md` (Trigger faction dir — Functions.md is tied to old cards; derive fresh function registry from lore + archetype, not from this file)
6. **Pipeline references:** `DESIGN_GUIDELINES.md`, `FACTION_SET_REWORK_PLAYBOOK.md`
7. **The warmup doc:** function registry, synergy web, band allocation, build facts

All tcg-engine paths under `/root/tcg-engine/docs/Five_Crests/`. Paul workspace at `/root/.hermes/docs/Paul/workspace/`.

**PITFALL: Reading old Paul workspace lore files.** The overnight Trigger run (2026-06-05) used lore files from the dropbox/workspace that were superseded. The authoritative Trigger docs live in the tcg-engine repo under `docs/Five_Crests/factions/Trigger/`. Do not use `Trigger_Complete_Faction_Lore_v1.md` from the Paul_Handoff directory — it's a Claude compendium with known conflicts (Gerald knows Henry alive, Villium "economic only," etc.). The live Trigger faction docs are the authority.

## Warmup Doc Template

The warmup doc should contain all pipeline steps 1-8 completed BEFORE card rows:

- **Lore summary:** Key characters, faction thesis, territory, Code, leadership structure
- **Crews:** Role pools, who works with who, character profiles
- **Archetype:** One-sentence identity. What kind of deck? Tempo, Control, Midrange?
- **Function Registry** (F01–F16+): function name, mechanical description, target band, synergy edges. Derived from lore + archetype — NOT retrofitted from existing cards
- **Mechanics:** Keyword lock, mechanical boundaries, NOT lists, Model B pricing
- **Synergy Web:** Two layers per the pipeline skill: Layer 1 — 8-15 function edges (E01–E15), numbered, typed, with mechanical hook. Layer 2 — LIVE web format: synergy triangles, win-line packages, 33-row slot table with NEEDs, gap list. See `bruiser-card-design-pipeline` skill § Step 7 and `FACTORY_BUILD_FACTS_AND_SYNERGY_WEB.md` in tcg-engine repo.
- **Band Allocation:** V1 through V6+ distribution with rarity burn-down
- **Build Facts:** Curve skeleton, win lines, blind spots, keyword lock, NOT list
- **Process Instructions:** Step-by-step what to build and in what order (card rows come LAST)
- **Lore Anchors:** Key character names, faction thesis, mechanical identity
- **Output Spec:** File naming convention, annotation format, header requirements

## Spawn Commands

```bash
# Create warmup doc at workspace/
# /root/.hermes/docs/Paul/workspace/Trigger_Warmup_YYYY-MM-DD_Paul.md

# Spawn fresh instance
tmux new-session -d -s trigger-factory -x 160 -y 50 'hermes --model deepseek-v4-pro --provider deepseek'

# Wait for init (10s)
sleep 10

# Send task prompt
tmux send-keys -t trigger-factory "Read [warmup doc path] and [reference doc paths] in order. Build a 55-card Trigger faction set following the function-first pipeline. Deliver to /root/syncthing/paul-dropbox/ as Trigger_Card_Roster_[version]_YYYY-MM-DD_Paul.md with function/edge annotations on every row. Also deliver design notes and hero cards." Enter

# Monitor progress
tmux capture-pane -t trigger-factory -p | tail -50
```

## Monitoring Checklist

During the run, the orchestrator must:
1. **Verify instance started** — check tmux session exists and prompt was received
2. **Check progress every 30-60 minutes** — capture-pane and look for card row output
3. **Validate output files** — after completion, stat each expected file in dropbox
4. **Confirm delivery** — all files present, non-empty, properly formatted

## Output Files Expected

- `Trigger_Card_Roster_v[N]_YYYY-MM-DD_Paul.md` — 55-card set with function/edge annotations
- `Trigger_Design_Notes_v[N]_YYYY-MM-DD_Paul.md` — design rationale, synergy analysis
- `Trigger_Heroes_v[N]_YYYY-MM-DD_Paul.md` — 3 heroes with rationale, play patterns, Ultimate gate verification

**Card display format:** Must use fixed-width monospaced columns in fenced code blocks — NEVER markdown pipe tables. See `design-collaboration` skill, `references/card-display-format.md`. Cards organized by band (V cost), rarity within band. Columns: (number) · R · V · Name · Crew · Stats · Text. Numbers optional.

## Pitfalls

- **Skipping the pipeline:** Spreadsheet-first (lore → role → keyword → stats) produces individually reasonable cards that don't cohere as a set. Function-first with synergy web is non-negotiable.
- **Using markdown pipe tables for card display:** Joe explicitly hates this format ("I really don't like the tabling format"). Use fixed-width code blocks. See `design-collaboration` skill, `references/card-display-format.md`. Organize by band and rarity.
- **Context pollution:** The orchestrator Paul accumulates session context that biases toward shortcuts. The fresh instance is clean and reads docs from scratch — trust it over your own memory.
- **tmux session cleanup:** Kill old trigger-factory sessions before spawning new ones. `tmux kill-session -t trigger-factory 2>/dev/null`
- **Repo staleness:** If `git pull` fails or the repo is behind, the fresh instance won't have current docs. Verify before spawning.
