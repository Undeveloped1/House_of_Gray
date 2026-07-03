---
name: pathway-design
description: "Phase 1-2 of faction card design. Converts faction identity into crew profiles, pathway density targets, turn maps, and slot boundaries. Feeds subagent batch design."
version: 2.0.0
author: Paul
---

# Pathway Design — From Identity to Card Slots

**Position in pipeline:** `faction-identity-gate` (Phase 0) → **pathway-design** (Phase 1-2) → slot boundaries → subagent batch design → `faction-set-review` (Phase 3). Archive at `docs/Paul/workspace/pathway-design-archive.md`.

**Core principle:** Slot filling is a boundary-setting tool. Pathway building determines what goes in the box and why. Crew targets are faction-specific — no fixed ratio. Let the faction's pillars determine crew distribution.

## Phase 1: Crew Identity Profiles

Every crew is a mini-faction. Define what each does, what it CANNOT do, and what its day looks like.

| Field | Purpose |
|-------|---------|
| **Crew** | Name |
| **Job** | One sentence. What they do in the faction's ecosystem. |
| **Owns** | Mechanics and abilities this crew controls. |
| **Cannot Do** | Explicitly forbidden abilities. A Street minion with Paid fails crew gate. |
| **% of Set** | Target percentage of 55 cards. |
| **Daily Life** | What does their day look like? Grounded in lore. |
| **Ludo Profile** | Naming conventions per crew. |

### Example: Trigger Crews

| Crew | Job | Owns | Cannot Do | % | Daily Life |
|------|-----|------|-----------|----|-----------|
| Management | Control flow. Initiate work, gather intel, disrupt enemies. | Mark, Intel, Silence, Contract scaling | Kill minions directly. Carry weapons. Fight. | 10% | Penobscot 45 — operators at desks, wall map, red/blue/black pins. |
| Professionals | Execute work. Complete Contracts, carry weapons, collect payment. | Paid, Armed, Contract completion, removal | Initiate Contracts (Mark is Management). Disrupt (Silence is Court). | 50% | Herald press run at 5am. Range in Corktown. The job is live once press runs. |
| Street | Feed the engine. Apply pressure, soften targets, create tempo. | Hustle, combat damage, kill rewards | Complete Contracts (Paid). Draw cards. Disrupt. | 20% | Numbers from Fletcher's barbershop. Want Professional status but aren't there yet. |
| Help | Enable the Arsenal. Maintain weapons, reload, supply ammo. | Reload, weapon support, durability | Fire guns (direct damage). Draw cards. Initiate/complete Contracts. | 20% | Carlo's bench — threads Villium through custom barrels. Never killed anyone. |

## Phase 2: Pathway Definition

Define 2-4 pathways with density targets. A pathway is a deck-building lane — a sequence of cards producing a specific game experience.

| Field | Purpose |
|-------|---------|
| **Pathway** | Name |
| **What It Does** | One sentence. |
| **% of 55 Cards** | Core pathway 55-60%, secondary 20-25%, specialty 5-15%. |
| **~Cards** | Approximate card count. |
| **V-Band Map** | Where cards fall on the curve. T1→T2→T3 progression. |

### Example: Trigger Pathways

| Pathway | What It Does | % | ~Cards | V-Band Map |
|---------|-------------|-----|--------|------------|
| The Contract | Mark targets → complete Contracts → get Paid | 55-60% | 30-33 | 1-2V: Mark enablers. 3-4V: Kill/complete + Paid payoffs. 5-6V: Big Paid cascades |
| The Arsenal | Weapons and ammo management | 20-25% | 11-14 | 1-2V: Weapons. 3-4V: Ammo support + Reload. 5V: Legendary weapon |
| The Court | Silence disruption + intel | 10-15% | 6-8 | 2-3V: Scry/peek. 4-5V: Silence payoffs + Contract scaling |
| Street Tempo | Hustle pressure, feed kills to Professionals | 5-10% | 3-5 | 1-2V: Hustle 1-drops. 3-4V: Hustle mid-body. 5V: Street apex |

## Phase 2b: Turn Map

For each pathway, map the ideal game turn-by-turn. Ensures cards fire on curve.

| Turn | Contract Pathway | Arsenal Pathway |
|------|-----------------|-----------------|
| T1 | Hustle 1-drop or pass | Equip Saturday Night |
| T2 | Mark target (Finger Man) | Armed body (Gunsmith) |
| T3 | Kill Marked → Paid fires (Earner) | Reload / Special Ammo (Ammo Caddy) |
| T4 | Second Contract cycle + Scaling payoff | Weapon payoff / kill (Quartermaster) |
| T5 | Contract cascade or legendary closer | Carlo's Piece online |

**Feasibility check:** For each card, calculate "earliest turn this mechanic can fire." A card at cost V with Overkill N needs V+N-1 mana minimum. If mechanic should create T2 decisions but fires T4+, redesign.

## Phase 2c: As-Fan Calculation

Run `density_calc.py` or manual tally to confirm draw probabilities for signature mechanics. Target bands per mechanic are in `five-crests-card-pipeline` skill.

## Phase 2d: Slot Table & Self-Audit

The constraint surface for card-design sub-agents. Every card gets a row.

### Minion Slot Format
```
| # | V | R | Crew | Spec | Edge | Pathway |
```
- **#** — Slot ID (M01–M29)
- **V** — Mana cost (0–6), **R** — Rarity (C/U/R/L)
- **Crew** — crew assignment
- **Spec** — What this card needs to do mechanically. "3V Uncommon Professional — Armed body. E06 edge. Pairs with S09 for Special Ammo payoff."
- **Edge** — Which synergy edge(s) this card touches. Every card must touch ≥1 edge.
- **Pathway** — Contract, Arsenal, or Court

### Spell & Weapon Slots
Spells (S01–S21) and Weapons (W01–W05) follow the same table structure, with Ambush type tags on trap spells.

### Self-Audit Summary (MANDATORY — before leaving Phase 2)

Cross-check these four dimensions against Build Facts targets. Flag every discrepancy.

| Check | What to Count | Compare Against |
|-------|---------------|-----------------|
| **Crew split** | Minions + Spells + Weapons per crew | Build Facts crew % targets |
| **Rarity** | Count per rarity tier across all card types | Build Facts rarity distribution (C=24, U=16, R=11, L=4) |
| **Curve** | Count per V-band | Build Facts mana curve (1V=5-6, 2V=10-12, 3V=10-12, 4V=8-10, 5V=5-6, 6V=3-4) |
| **Legendaries** | Total legendary slots | Hard cap (4: 2 minion, 1 spell, 1 weapon) |

Format discrepancies as FLAG rows. Also verify: every synergy edge has ≥1 card touching it, pathway distribution supports all three hero lanes, no crew bleed (Street with Paid, Help with card draw, Management killing).

**Gate:** All flags resolved or escalated to Joe. Unresolved flags become Phase 3 spec validation findings.

### Rebalancing

After building, run four checks. Fix each before proceeding:

| Check | What | Fix |
|-------|------|-----|
| **Crew split** | P+Street vs M+Help percentages match target | Reclassify spells across crew boundaries or recut target. |
| **Rarity** | C/U/R/L counts match build facts | Bump cards up/down rarity. Overkill bodies, Intel+Mark spells are natural Uncommon candidates. |
| **Curve** | V-band counts in target range | Shift 5V cards down to 1-2V. Add 1-drops if light. |
| **Legendaries** | Exactly 4 | Promote/demote as needed. |

### Draft Feasibility
How many cards of each type does a drafter need to see per pack for a pathway to be draftable?

| Pathway | Common Need | Common Target | Notes |
|---------|------------|---------------|-------|
| Contract | ~10 Mark + ~10 Paid in pool | 7-8 commons per pathway | Ensures drafter sees enough to build |
| Arsenal | ~8 weapon/ammo cards | 4-5 commons | Weapon support shouldn't outnumber weapons 3:1 |
| Court | ~5 disruption/intel cards | 2-3 commons | Specialty — rare-dependent |
| Street | ~4 Hustle bodies | 2-3 commons | Vanilla-adjacent, low synergy burden |

## Phase 3: Slot Boundaries

Define the box each slot can fit in BEFORE designing cards.

| V | Crew | Pathway | Rarity Range | Stat Range | Mechanic Options |
|---|------|---------|-------------|------------|-----------------|
| 1V | Street | Street Tempo | C | 1/1 - 2/1 | Hustle, vanilla |
| 2V | Professional | Contract | C-U | 2/2 - 3/3 | Mark BC, Paid, Armed |
| 3V | Professional | Contract | U-R | 2/3 - 3/3 | Paid scaling, Overkill, Contract draw |

## Phase 4: Subagent Batch Design

Paul defines constraints. Subagents design cards.

**Per-batch context (fed to each subagent):**
1. This batch's slots (V, crew, pathway, slot boundaries)
2. Full crew identity profiles (all crews)
3. Daily Life scenes (the relevant crew's day)
4. Turn map for this pathway
5. Synergy edge requirements (which edges must be populated)
6. Ludo guidance (name conventions per crew)
7. "This card must be playable on curve. Earliest activation turn: ___"

**Batch size:** 5-10 cards per subagent. Smaller = more parallel = faster iteration.
**Paul's role:** Define constraints. Review output. Flag ludo failures, crew violations, turn feasibility problems.

## Common Failure Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Crew bleed** | Street with Paid. Help with direct damage. | Check every card against crew CANNOT DO list. |
| **Pathway starvation** | Core pathway at 20% when it needs 55%. | Audit pathway percentages against targets BEFORE designing cards. |
| **Decorative mechanic** | Overkill 2 on 2V card — fires T3 at earliest. | Calculate activation turn. If 2+ turns late, redesign or accept as bonus. |
| **Ludo collapse** | Spotter deals damage. Dues Taker draws cards. Name doesn't match function. | Run ludo pass as separate step: "What is this person's job? Does card text match?" |
| **Spreadsheet blindness** | Edge numbers replace human-readable role descriptions. | Card tables should answer: who, what do they do, which crew? Edge numbers are audit tags. |
