---
name: spec-validator
description: "Standalone spec validation sub-agent. Verifies slot table math, crew bleed, mechanic density, pathway coverage, and edge coverage BEFORE card design. Highest-leverage single step in the pipeline."
version: 2.0.0
author: Paul
---

# Spec Validator — Pre-Card-Design Gate

A standalone sub-agent that validates a faction's Sub-Agent Spec before card design sub-agents are spawned. Highest-leverage single step in the pipeline — catches 7+ blocking errors on average, saving 55+ cards of rework.

**When:** After Sub-Agent Spec is built (after Phase 2: Pathway Design), BEFORE spawning card design workers (Phase 4). Mandatory. Never skip.
Archive: `docs/Paul/workspace/spec-validator-archive.md`.

## The Validation Checks

### 1. Slot Table Math
- Crew card counts sum to 55?
- Crew percentages within budget (±5%)?
- Rarity counts match targets (C ~25, U ~17, R ~10, L ~3)?
- V-band totals match curve target?
- Empty or overflow slots?

### 2. Crew Bleed Audit
Check every crew against locked CAN/CANNOT profiles:
- Management: CANNOT kill/weapons/fight
- Professionals: CANNOT Intel-Mark (premium Mark) / draw (except Paid) / disrupt
- Street: CANNOT Paid / draw / disrupt
- Help: CANNOT direct damage / draw / Contracts

### 3. Mechanic Density
Count sources for each signature mechanic. Flag deviations:
- Mark sources: 6-10. Paid sources: 5-6. Overkill sources: 5-6 minimum.
- Elite-only mechanics (Barrage): 1-2. Splash mechanics (Cloak, Hustle): 2-3.

### 4. Pathway Coverage
All three hero lanes have card support? Pathway density matches turn map targets? Cross-pathway support included? Any lane with zero unique cards?

### 5. Edge Coverage
All synergy edges have ≥2 cards? Any edges with 1 card (thin — flag)? Any with 0 cards (missing — Critical)? Self-referencing edges?

### 6. Naming Convention Audit
Professionals: epithets/role-names ONLY, NO SURNAMES. Street: nicknames or first names. Management: titles or formal address. Help: given names or trade names. Any naming collisions within faction?

### 7. Blind Spot Enforcement
"No Taunt" — any Taunt/Guard cards? "No swarm" — token generators above 1/turn? "No AOE board clear" — multi-target removal spells? "No direct hero damage spells"?

### 8. Legendary Slot Verification
Exactly 4 (3 legendary heroes + 1 legendary spell/weapon/minion)? Power level matches rarity floor? Names carry appropriate weight?

## Severity Grading

| Grade | Definition | Action |
|-------|-----------|--------|
| **Critical** | Blocks card design. Math error, crew bleed, missing edge, blind spot violation. | Fix spec, re-validate. Do NOT proceed. |
| **Major** | Risk of sub-agent errors. Over/under density, thin edge, naming ambiguity. | Fix spec now unless Joe overrides. |
| **Minor** | Noteworthy but won't break build. Edge case, one thin edge at 2 cards. | Flag for fixer pass. Don't block. |

## Sub-Agent Prompt Template

```
Goal: Validate the [faction] Sub-Agent Spec before card design

Context: Spec, Function Registry, Build Facts, Synergy Web, Crew CAN/CANNOT profiles.

Run ALL 8 checks:
1. Slot table math (crew budgets, rarity, V-band)
2. Crew bleed (every crew against CAN/CANNOT)
3. Mechanic density (sources per mechanic)
4. Pathway coverage (all three hero lanes)
5. Edge coverage (all synergy edges)
6. Naming conventions
7. Blind spot enforcement
8. Legendary slot verification

Output: severity-graded report. Critical findings BLOCK card design.
```

## Output Format

```
# Spec Validation Report — [Faction]

## Summary
PASS/FAIL — {count} Critical, {count} Major, {count} Minor

## Critical Issues
[blocking — must fix before card design]

## Major Issues
[should fix — risk of sub-agent errors]

## Minor Issues
[noteworthy — won't break build]

## Crew Bleed Audit
[check every crew against function registry]

## Mechanic Density Audit
[expected vs documented sources per mechanic]

## Pathway Coverage
[all hero lanes represented? cross-support?]

## Edge Coverage
[all edges have cards? thin flags?]

## Recommendations
[what's missing, what's strong, what needs Joe's call]
```

## Pitfalls

- **Don't validate against wrong version.** Cross-reference against locked function registry and build facts.
- **Don't be lenient on crew bleed.** "One Street with Paid" is a slippery slope. Flag Critical. Joe can override.
- **Check CAN and CANNOT separately.** Both sides of each crew boundary.
- **Evaluate distribution, not just count.** 6 Mark sources within band but all at 5V+ = Major.
- **Naming conventions need negative examples.** "Professionals: epithets/role-names" isn't enough — validator must flag surnames as violations.
