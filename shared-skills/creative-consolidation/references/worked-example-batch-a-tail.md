# Worked example: batch_a_tail (mostly-FOUND pass)

**Date:** 2026-06-01
**Batch:** 3 (per PAUL_ARCHIVE_DCW_RETRO_PLAN.md)
**Source folder:** `docs/archive/workspace_merged_2026-05-30/batch_a_tail/` (23 files)
**Result:** 20 FOUND, 3 NEW, 0 CONFLICT

## What made this batch different

Unlike Inner Circle (lore draft versions) or Minion Rosters (design docs with card lists), batch_a_tail was mostly **sources already processed into live canon**. The Identity.md explicitly cites `Bruiser_Faction_Structure_v1.md` as its source. The Design Bible already has the "mob game" directive. The old card sets are superseded.

A mostly-FOUND pass is still a successful pass — it proves preservation. The process catches what DCW would call "HERITAGE" and gives it a clean disposition rather than leaving it in an ambiguous queue.

## Key technique: finding fond in compressed sources

`Bruiser_Faction_Structure_v1.md` (161 lines) was the source for `Identity.md` § Internal tiers. The live canon compressed the detailed day-to-day prose into a summary table. Three texture beats were recovered that had been lost in compression:

1. **Morning/after-work culture** — dock workers on water by 5am, the split between family men and bar/gym guys
2. **Monthly fight nights** — bare-knuckle matches between crews, behind factories, competitive but good-natured
3. **Industrial subculture distinctions** — Dock Workers (crudest tattoos), Rail Yard (mobile, better intel), Steel Workers (fatalistic), Welders (technical, forge access), Factory Workers (regimented)

**Pattern:** When a source file is cited by live canon, don't assume everything was captured. Check whether the canon compressed the facts into a summary and lost the texture.

## Key technique: batch scope resolution

Joe said "ready for batch 3 review." The Daily Handover said "Batch 3 (D9-D18 or whatever Joe assigns)." Initial attempt checked the DCW queue (`paul_archive_dcw_queue.md`) which showed D9-D18 as already CLOSED — ambiguous. Joe corrected: "I have no idea, homie. You got to look at the document that I had."

The document Joe meant was `PAUL_ARCHIVE_DCW_RETRO_PLAN.md` — the master plan that maps batch numbers to folders:

| Batch | Scope |
|-------|-------|
| 1 | batch3/ + bruiser_red_team_v4/ |
| 2 | batch2/ craft passes |
| 3 | batch_a_tail/ |

The DCW queue tracks individual file status. The plan document defines batch membership. When hunting for batch scope, check the plan, not the queue.

## Key technique: spell flavor hooks as reserve

`DESIGN_SKELETON_DRAFT.md` had 16 spell slots with lore hooks ("Wrong wrench, right head", "Ink sleeps until the body fails", "Salt only marks the ready"). The card mechanics are superseded, but the flavor hooks are reusable. Rather than trying to match them to specific live cards, bank them in `Card_Bank.md` as flavor text reserve.

## Disposition breakdown

| Type | Count | Examples |
|------|-------|----------|
| FOUND | 14 beats | Dual leadership, internal tiers, mob game directive, crew list |
| NEW | 3 beats | Day-to-day texture, monthly fight nights, industrial subculture distinctions |
| PARTIAL | 2 beats | Spell lore hooks (bank as reserve, not patched to specific cards) |
| REDUNDANT | ~20+ | Old card sets (v2, v3, v4), changelogs (empty), status reports, decision logs |
| CONFLICT | 0 | — |

## Files produced

- Working doc: `merge_plans/batch_a_tail_fond_pass_2026-06-01.md`
- Archive: `docs/archive/paul_workspace/2026-06-01/batch_a_tail/`
- Live patches: `Identity.md` (3 texture beats), `Card_Bank.md` (8 spell flavor hooks)
