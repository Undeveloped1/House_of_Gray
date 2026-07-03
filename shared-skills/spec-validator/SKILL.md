---
name: spec-validator
description: "Standalone spec validation sub-agent. Verifies slot table math, crew bleed, mechanic density, pathway coverage, and edge coverage BEFORE card design. Catches 7+ blocking errors on average. The highest-leverage single step in the pipeline."
category: creative
---

# Spec Validator — Pre-Card-Design Gate

## What This Is

A standalone sub-agent that validates a faction's Sub-Agent Spec before any card design sub-agents are spawned. This is the highest-leverage single step in the pipeline. Proven: caught 7 blocking math errors on Trigger v7, 2 Critical crew contradictions on the orchestrator's Phase 1 run.

**Cost:** One sub-agent. ~2 minutes. Saves 55+ cards of rework.

## When to Use

- After Sub-Agent Spec is built (after Phase 2: Pathway Design)
- BEFORE spawning card design workers (Phase 4)
- Mandatory. Never skip.

## The Validation Checks

### 1. Slot Table Math
- Do crew card counts sum to total cards (55)?
- Are crew percentages within budget (+/- 5%)?
- Do rarity counts match targets (C ~25, U ~17, R ~10, L ~3)?
- Do V-band totals match the curve target?
- Are there empty slots or overflow slots?

### 2. Crew Bleed Audit
For each crew, check against locked CAN/CANNOT profiles:
- Management: CANNOT kill/weapons/fight. Any Management cards with direct damage or weapons?
- Professionals: CANNOT Intel-Mark (premium Mark)/draw(except Paid)/disrupt. Any violations?
- Street: CANNOT Paid/draw/disrupt. Any Street cards with Paid triggers?
- Help: CANNOT direct damage/draw/Contracts. Any Help cards with these?

Check: does ANY card give a mechanic to a crew that Joe explicitly locked out?

### 3. Mechanic Density
Count sources for each signature mechanic:
- Mark sources: target 6-10
- Paid sources: target 5-6
- Overkill sources: target 5-6 (minimum)
- Barrage sources: target 1-2 (elite-only)
- Cloak sources: target 2-3
- Hustle sources: target 2-3
- Intel sources: target varies

Are any mechanics over or under the target band? Flag deviations.

### 4. Pathway Coverage
- All three hero lanes have card support?
- Pathway density matches targets from turn maps?
- Cross-pathway support (Management/Help bridges) included?
- Any hero lane with zero unique cards?

### 5. Edge Coverage
- All synergy edges have at least 2 cards (minimum)?
- Any edge with 1 card (thin — flag for reinforcement)?
- Any edge with 0 cards (missing — Critical)?
- Self-referencing edges (card references itself as the edge source)?

### 6. Naming Convention Audit
- Professionals: epithets/role-names ONLY, NO SURNAMES
- Street: nicknames, first names, or street handles
- Management: titles or formal address
- Help: given names or trade names
- Any naming collisions within the faction?

### 7. Blind Spot Enforcement
Check every locked blind spot:
- "No Taunt" — any cards with Taunt or Guard?
- "No swarm" — any token generators above 1/turn?
- "No AOE board clear" — any multi-target removal spells?
- "No direct hero damage spells" — any spell that targets hero directly?

### 8. Legendary Slot Verification
- 3 legendary heroes + 1 legendary spell/weapon/minion = 4 total?
- Legendary power level matches rarity floor?
- Legendary names carry appropriate weight?

## Severity Grading

| Grade | Definition | Action |
|-------|-----------|--------|
| **Critical** | Blocks card design. Math error, crew bleed, missing edge, blind spot violation. | Fix spec, re-validate. Do NOT proceed. |
| **Major** | Risk of sub-agent errors. Over/under density, thin edge, naming ambiguity. | Fix spec now unless Joe overrides. |
| **Minor** | Noteworthy but won't break the build. Naming convention edge case, one thin edge at 2 cards. | Flag for fixer pass. Don't block. |

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
[noteworthy — won't break the build]

## Crew Bleed Audit
[check every crew against the function registry and synergy web]

## Mechanic Density Audit
[count expected vs documented sources per mechanic]

## Pathway Coverage
[all three hero lanes represented? cross-support included?]

## Edge Coverage
[all edges have cards? thin flags?]

## Recommendations
[what's missing, what's strong, what needs Joe's call]
```

## Sub-Agent Prompt Template

```
Goal: Validate the [faction] Sub-Agent Spec before card design

Context:
- Spec at [spec_path]
- Function Registry at [registry_path]
- Build Facts at [build_facts_path]
- Synergy Web at [synergy_web_path]
- Crew CAN/CANNOT profiles: [profiles]

Run ALL checks:
1. Slot table math (crew budgets, rarity caps, V-band totals)
2. Crew bleed (check every crew against CAN/CANNOT)
3. Mechanic density (count sources per mechanic)
4. Pathway coverage (all three hero lanes)
5. Edge coverage (all synergy edges)
6. Naming conventions
7. Blind spot enforcement
8. Legendary slot verification

Output: severity-graded report. Critical findings BLOCK card design.
```

## Pitfalls

- **Don't validate against the wrong version.** Spec must be cross-referenced against locked function registry and build facts. A warmup doc from a mobile session might contradict canon.
- **Don't be lenient on crew bleed.** "One Street card with Paid" is a slippery slope. Flag it as Critical. Joe can override; the validator cannot be lenient.
- **Check CAN and CANNOT separately.** "Professionals CAN Paid" is one side. "Street CANNOT Paid" is the other. Both must be enforced.
- **Don't just count — evaluate distribution.** 6 Mark sources is within band, but if all 6 are at 5V+, that's a Major issue. Distribution across curve matters.
- **Naming conventions need negative examples.** "Professionals: epithets/role-names" isn't enough. The validator must know to flag surnames as violations.

## Changelog

**2026-06-08** — Initial creation. Derived from the validator sub-agent pattern proven on Trigger v7 (caught 7 blocking math errors) and the orchestrator's Phase 1 (caught 2 Critical crew contradictions).
