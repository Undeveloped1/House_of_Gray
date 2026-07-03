# Worked Example: A1-A4 Workspace Stubs (Git Recovery + Spell Moments)

**Date:** 2026-06-01
**Batch:** A1-A4 (workspace factory stubs)
**Fond Process pass**

## What they looked like

Four files in `docs/Paul/workspace/` — all stubbed to redirects:

- A1: `Bruiser_Hero_Cards_2026-05-31_Paul.md` — MERGED stub, 17 lines
- A2: `Bruiser_NonMinion_Locked_2026-05-30_Paul.md` — MERGED stub, 13 lines
- A3: `Bruiser_Spell_Roster_2026-05-30_Paul.md` — SUPERSEDED stub, 17 lines
- A4: `Bruiser_Spells_v6_Draft_2026-05-30_Paul.md` — SUPERSEDED stub, 15 lines

Every file said "DO NOT EDIT" and pointed to live canon paths.

## What we found

A1-A3 were genuinely empty stubs — zero creative fond to recover. The live canon had everything.

A4's stub said "Name/moment prose harvested to Card_Bank 2026-06-01" — but only the NAMES were banked. The creative MOMENTS (scene prose) behind each spell were never captured.

## Recovery technique

Recovered the original body from git:

```bash
git log --oneline -- "docs/Paul/workspace/Bruiser_Spells_v6_Draft_2026-05-30_Paul.md"
git show <commit>:"docs/Paul/workspace/Bruiser_Spells_v6_Draft_2026-05-30_Paul.md"
```

This revealed a full 200+ line spell design draft with:
- 8-step spell design methodology
- 3 LOCKED spells with moments
- 7 PROPOSED spells with moments and verdicts
- 3 NEEDS REWORK spells with design problems
- 17-spell summary table

## What we banked

10 spell moments — the creative scene prose behind each spell concept:

| Spell | Moment |
|-------|--------|
| Adrenaline Rush | "Coach slaps a guy's face between rounds, he comes out swinging — 'Walk it off. Now GO.'" |
| Ground Strike | "Dock boss slams a cargo hook into the floor. Everything stops." |
| Heavy Hands | "Coach wraps the fighter's hands. Extra tape on the knuckles. 'You feel that? That's the difference.'" |
| The Shakedown | "Two guys in a car. One talks. One stands behind him. 'Nice shop. Be a shame if something happened to it.'" |

These went to `Card_Bank.md` under the existing "Spell name reserve" section as a "Spell moments (voice reserve)" subsection.

## Key lesson

**Stubs aren't empty.** The redirect stub may say "harvested to Card_Bank" but the original body might have content that wasn't captured. Git history is the source of truth. Always check git for the full body before calling a stub clean — especially when the stub says something was "harvested" that may have only been partially captured.

## Pattern

When a stubbed file claims content was "harvested":
1. Recover full body from git
2. Check what was actually banked in the claimed destination
3. Look for content NOT captured: moments, scene prose, design rationale, methodology
4. Bank the gap

This turns a 0-fond stub into a recovered resource.
