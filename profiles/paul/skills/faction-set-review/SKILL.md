---
name: faction-set-review
description: "Ruthless game critic checklist for reviewing a Five Crests faction card set. Three passes — structural, mechanical, polish."
version: 2.0.0
author: Paul
---

# Faction Set Review

Three-pass critic review of a card set. Archive: `docs/Paul/workspace/faction-set-review-archive.md`.

## Pipeline

```
Build set → pre_review_audit.py (automated mechanical gate)
  → PASS → Three-pass critic review
  → B+ or better → SHIP
```

**Before slot-filling:** run density calculator (`python3 tools/density_calc.py`). Answers "how many Mark sources for 90% draw consistency by Turn 2?" before any card is designed.

**Run pre-review script first.** `python3 scripts/pre_review_audit.py <set_md>`. Only sets that pass go to critic. Format compatibility: if zero cards found, column order doesn't match script expectations — patch `parse_card_table()` column indices.

## Pass 1: Structural (Can You Read It?)

**Gate:** Any fail = cannot review further. Fix first.

| # | Check |
|---|-------|
| 1.1 | **Keyword sidebar exists.** Every mechanical keyword defined in one place. |
| 1.2 | **Every keyword on a card IS in the sidebar.** No undefined mechanics. |
| 1.3 | **No naming conflicts.** Keyword and card don't share name. |
| 1.4 | **No phantom references.** Every referenced object exists. |
| 1.5 | **Card counts match build facts.** 30 minions + 15 spells + 5 ambushes + 5 weapons = 55. Rarity totals match targets (±1). |
| 1.6 | **No blank rows.** Every card has cost, rarity, crew, stats (if minion/weapon), rules text, edge assignment. |

**Grade:** All 6 = A. 1 fail = C. 2+ fails = stop and fix.

## Pass 2: Mechanical (Does It Work?)

| # | Check | Threshold |
|---|-------|-----------|
| 2.1 | **Core loop density** | ≥10 cards participating in primary loop. Below = CRITICAL. |
| 2.2 | **Synergy edges are real** | Every edge has ≥2 cards. 1-card "edges" = MAJOR. |
| 2.3 | **Enabler-to-payoff ratio** | ≤3:1 ratio. Above = MAJOR. |
| 2.4 | **Curve supports gameplan** | Aggro: peak 1-2V. Midrange: peak 2-3V. Control: peak 3-4V. |
| 2.5 | **1V slot is functional** | ≥3 minions at 1V. ≥1 applies pressure (2+ ATK). Below = MAJOR. |
| 2.6 | **Conditional vs unconditional removal** | ≥2 unconditional kill spells at common. Below = MAJOR for draft. |
| 2.7 | **Blind spot compliance** | Zero violations of faction CANNOT list. Any violation = CRITICAL. |
| 2.8 | **Mechanical anti-synergy** | No cards fighting their own faction (Cue on reactive ambushes, Contract hand clog). Systemic = MAJOR. |
| 2.9 | **Turn feasibility** | Can key mechanic fire on curve? V+N-1 minimum. Case A (threshold IS the card — below-rate body without it) → MAJOR. Case B (threshold is bonus on good body) → MINOR. |

**Grade:** 0 criticals + 0-1 majors = A. 0 criticals + 2-3 majors = B. 1+ criticals = C or below.

## Pass 3: Polish (Is It Good?)

| # | Check | Threshold |
|---|-------|-----------|
| 3.1 | **Legendary impact** | "Hell Yeah / Hoot / Oh Shit" test. Unplayable legendaries = CRITICAL. Overtuned = MAJOR. |
| 3.2 | **Hero power tradeoffs** | HP totals map to fragility. Hero powers useful in 80%+ of decks (not parasitic). Parasitic = MAJOR. |
| 3.3 | **Draft fundamentals** | 3-5 vanilla/french vanilla commons. 2+ common removal spells. 2+ common ambushes if defining. Below = MAJOR. |
| 3.4 | **Splashy uncommons** | 1-2 build-around uncommons. Zero = MINOR. |
| 3.5 | **Healing exists** | ≥2 cards restoring HP. Zero = MODERATE. |
| 3.6 | **Templating is tight** | No ambiguous targeting or scoping. Every ambiguous = MINOR. |
| 3.7 | **Fun factor** | Core loop creates satisfying moments? If best draw = "play vanilla and hope" = MAJOR. |
| 3.8 | **Ludo verification** | Every card name matches what card DOES. Spotter dealing damage = wrong. Flag mismatch as MAJOR. |
| 3.9 | **SOUL CHECK (BLOCKING GATE)** | **Mechanical correctness ≠ good cards.** Would someone who'd never heard of this faction know who these people are? Feel 1961 Detroit? Street-fight callout test? Every card a PERSON, not spreadsheet cell? Any "no" = FAIL regardless of Pass 1-3 grades. Critic sub-agent must load Inner_Circle.md, Daily_Life.md, and character profiles to perform this check — otherwise grade is invalid. |

**Grade:** 0 criticals + 0-1 majors = A. 0 criticals + 2-3 majors = B. 1+ criticals = C or below.

## Final Grade

Average Pass 2 + Pass 3 (Pass 1 is a gate, not graded).

| Average | Verdict |
|---------|---------|
| A | Ship it. |
| A− | Ship with minor fixes noted. |
| B+ | Ship-ready. One quick cleanup pass. |
| B | Needs iteration. One focused pass on 2-3 biggest problems. |
| B− | Multiple systems need rework. |
| C+ or below | Core loop or structure broken — rebuild. |

## Common Failure Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Keyword soup** | 7+ sub-mechanics in 55 cards. None have density. | Pick 3-4, commit. Cut rest to set #2. |
| **Paper web** | Edges defined but not populated. | Count every edge. Cut <2 or add cards. |
| **Parasitic draft** | Cards are blanks without specific partners. | Add enablers at common. Add vanilla-rate keyword bodies. |
| **Trap legendary** | Reads exciting but unplayable. | Playtest floor case. "6 mana do nothing" = redesign. |
| **Blank hero** | Hero power interacts with <5 cards. | Broaden trigger. |
| **Aspirational edge** | Edge claims 6, actually has 3. | Audit against actual card list. Point to card name or it doesn't count. |
| **Phonetic keyword collision** | "Paid" and "Payoff" — shared syllable confuses drafters. | Check new keyword against all existing faction keywords. |
| **Over-salvaging** | Every old card "kept" or "reworked." Set is a remix. | Old cards are inspiration, not obligation. Vanilla commons are intentional. |
| **Crew bleed** | Street with Paid. Help with direct damage. | Check every card against crew CANNOT DO. |
| **Decorative mechanic** | Overkill 2 on 2V — fires T3+. | Calculate activation turn. If 2+ turns late = decorative. |

## Post-Review Output

1. Letter grade with pass/fail counts
2. Ranked problem list (Critical → Major → Minor)
3. Specific fix for each Critical and Major
4. "Ship" or "Iterate" verdict
