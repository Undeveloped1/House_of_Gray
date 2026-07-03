---
name: pathway-design
description: Phase 1-2 of faction card design. Converts faction identity into crew identity profiles, pathway density targets, turn maps, and slot boundaries. Feeds subagent batch design. Sits between faction-identity-gate and faction-set-review.
category: creative
---

# Pathway Design — From Identity to Card Slots

**Position in pipeline:** `faction-identity-gate` (Phase 0) → **pathway-design** (Phase 1-2) → slot boundaries → subagent batch design → `faction-set-review` (Phase 3)

**Core principle:** Slot filling is a boundary-setting tool. Pathway building determines what goes in the box and why.

**Crew targets are faction-specific.** The 70/30 P+Street vs M+Help split is not universal — it was built for Bruiser (minion-heavy, bodies-on-board). A spell-heavy faction like Trigger (where Court, Help, and Management infrastructure consume 20+ spell slots naturally) may need 60/40 or even 55/45. Let the faction's pillars determine the crew distribution, not a fixed ratio. Trigger 2026-06-11: recut from 70/30 to 60/40 because Help/Court/Management spells (Ambush, Special Ammo, Reload, Overkill, disruption) are load-bearing infrastructure, not bloat. The slot table says "this 3V Professional slot can be Mark, Paid, Cloak, or Intel." Pathway design says "the Contract pathway needs a Paid payoff at 3V so it fires on the turn after a T2 Mark."

---

## Phase 1: Crew Identity Profiles

Every crew is a mini-faction. Define what each does, what it CANNOT do, and what its day looks like.

| Field | Purpose |
|-------|---------|
| **Crew** | Name |
| **Job** | One sentence. What they do in the faction's ecosystem. |
| **Owns** | Mechanics and abilities this crew controls. |
| **Cannot Do** | Explicitly forbidden abilities. A Street minion with Paid fails the crew gate. A Help minion dealing direct damage fails. |
| **% of Set** | Target percentage of 55 cards. |
| **Daily Life** | What does their day look like? Grounded in lore. Prevents lazy assumptions ("Management sits in Penobscot 45 routing phones. They've never met a Hitter. They don't carry guns.") |
| **Ludo Profile** | What kind of names fit this crew? Professionals have job titles (Earner, Contractor). Street has nicknames (Gunsel, Numbers Runner). Court has surnames (Sidney Lark). |

### Example: Trigger Crews

| Crew | Job | Owns | Cannot Do | % | Daily Life |
|------|-----|------|-----------|----|-----------|
| **Management** | Control the flow. Initiate work, gather intel, disrupt enemies. | Mark, Intel, Silence, Contract scaling | Kill minions directly. Carry weapons. Fight. | 10% | Penobscot 45 — operators at desks, wall map, red/blue/black pins. Code deaths in newspaper columns. Never met a Hitter. |
| **Professionals** | Execute the work. Complete Contracts, carry weapons, collect payment. | Paid, Armed, Contract completion, removal | Initiate Contracts (Mark is Management). Disrupt (Silence is Court). | 50% | Herald press run at 5am. Range in Corktown. Street work. The job is live once the press runs. |
| **Street** | Feed the engine. Apply pressure, soften targets, create tempo. | Hustle, combat damage, kill rewards | Complete Contracts (Paid). Draw cards. Disrupt. | 20% | Numbers from Fletcher's barbershop. Tommy's corner, Tony's route. Protection payments. Want Professional status but aren't there yet. |
| **Help** | Enable the Arsenal. Maintain weapons, reload, supply ammo. | Reload, weapon support, durability | Fire the guns (direct damage). Draw cards. Initiate or complete Contracts. | 20% | Carlo's bench — threads Villium through custom barrels. Rossi & Son on Woodward. Never killed anyone; every Contract this month started here. |

---

## Phase 2: Pathway Definition

Define 2-4 pathways with density targets. A pathway is a deck-building lane — a sequence of cards that produces a specific game experience.

| Field | Purpose |
|-------|---------|
| **Pathway** | Name |
| **What It Does** | One sentence. |
| **% of 55 Cards** | Target percentage. Core pathway gets 55-60%. Secondary gets 20-25%. Specialty gets 5-15%. |
| **~Cards** | Approximate card count. |
| **V-Band Map** | Where cards fall on the curve. T1→T2→T3 progression. |

### Example: Trigger Pathways

| Pathway | What It Does | % | ~Cards | V-Band Map |
|---------|-------------|-----|--------|------------|
| **The Contract** | Mark targets → complete Contracts → get Paid | 55-60% | 30-33 | 1-2V: Mark enablers. 3-4V: Kill/complete + Paid payoffs. 5-6V: Big Paid cascades |
| **The Arsenal** | Weapons and ammo management | 20-25% | 11-14 | 1-2V: Weapons. 3-4V: Ammo support + Reload. 5V: Legendary weapon |
| **The Court** | Silence disruption + intel | 10-15% | 6-8 | 2-3V: Scry/peek. 4-5V: Silence payoffs + Contract scaling |
| **Street Tempo** | Hustle pressure, feed kills to Professionals | 5-10% | 3-5 | 1-2V: Hustle 1-drops. 3-4V: Hustle mid-body. 5V: Street apex |

---

## Phase 2b: Turn Map

For each pathway, map the ideal game turn-by-turn. This ensures cards are designed to fire on curve.

| Turn | Contract Pathway | Arsenal Pathway |
|------|-----------------|-----------------|
| T1 | Hustle 1-drop or pass | Equip Saturday Night |
| T2 | Mark target (Finger Man) | Armed body (Gunsmith) |
| T3 | Kill Marked → Paid fires (Earner, Paper Pusher) | Reload / Special Ammo (Ammo Caddy, Gofer) |
| T4 | Second Contract cycle + Scaling payoff (Bean Counter) | Weapon payoff / kill (Quartermaster) |
| T5 | Contract cascade or legendary closer (The Closer) | Carlo's Piece online |

**Feasibility check:** For each card, calculate "earliest turn this mechanic can fire." A card at cost V with Overkill N needs V+N-1 mana minimum. If the mechanic is supposed to create T2 decisions but can't fire until T4+, redesign.

---

## Phase 2d: Slot Table (29 Minion Rows + 21 Spells + 5 Weapons)

The constraint surface for card-design sub-agents. Every row is a spec the sub-agent fills.

### Minion Slot Format

```
# | V | R | Crew | Spec | Edge | Pathway
```

Where:
- **#** — Slot ID (M01–M29)
- **V** — Mana cost (0–6)
- **R** — Rarity (C/U/R/L)
- **Crew** — Management, Professionals, Street, Help, Court (Management sub-tier)
- **Spec** — What this card needs to do mechanically. "3V Uncommon Professional — Armed body. E06 edge. Pairs with S09 for Special Ammo payoff."
- **Edge** — Which synergy edge(s) this card touches. Every card must touch ≥1 edge.
- **Pathway** — Contract, Arsenal, or Court

### Spell & Weapon Slots

Spells (S01–S21) and Weapons (W01–W05) follow the same table structure, with the addition of Ambush type tags on trap spells.

### Self-Audit Summary (MANDATORY — before leaving Phase 2)

After building the slot table, cross-check these four dimensions against Build Facts targets. Flag every discrepancy. Do NOT proceed to Phase 3 with unresolved flags.

| Check | What to Count | Compare Against |
|-------|---------------|-----------------|
| **Crew split** | Minions + Spells + Weapons per crew | Build Facts crew % targets |
| **Rarity** | Count per rarity tier across all card types | Build Facts rarity distribution |
| **Curve** | Count per V-band | Build Facts mana curve |
| **Legendaries** | Total legendary slots | Hard cap (4 for 55-card set) |

Format discrepancies as FLAG rows:
```
**FLAG:** P+Street crew split at 47% vs 70% target. Needs ~12 card shift or crew reclassification.
**FLAG:** Commons low (19 vs 24 target), Rares high (14 vs 11). Shift U/R → C.
```

Also verify:
- Every synergy edge has ≥1 card touching it (edge coverage)
- Pathway distribution supports all three hero lanes
- No crew bleed (Street with Paid, Help with card draw, Management killing)

**Gate:** All flags resolved or escalated to Joe. Unresolved flags become Phase 3 spec validation findings.

### Proven Example

See `workspace/Trigger_Pathway_Design_2026-06-11_Paul.md` for a complete slot table with self-audit. Four flags caught before Phase 3: crew split drift, rarity imbalance, curve fat at 5V, legendary overcount.

---

## Phase 2c: As-Fan Calculation

Run `density_calc.py` or manual tally to confirm draw probabilities for signature mechanics. Target bands per mechanic are in the `five-crests-card-pipeline` skill § Phase 1.

---

## Phase 2d: Slot Table

The constraint surface for card design. Every card that will be produced gets a row. Format:

```
| # | V | R | Crew | Spec | Edge | Pathway |
```

Where:
- **#** — Slot ID (M01-M30 for minions, S01-S21 for spells, W01-W05 for weapons)
- **V** — Mana cost
- **R** — Rarity (C/U/R/L)
- **Crew** — Management / Professionals / Street / Help / Court
- **Spec** — What this card needs to do mechanically. Stats + ability + flavor hook.
- **Edge** — Which synergy edge(s) this card touches (E01-E15). Every card must touch ≥1 edge.
- **Pathway** — Contract / Arsenal / Court

After building the slot table, run the four checks:

| Check | Target |
|-------|--------|
| **Crew split** | P+Street vs M+Court+Help percentage. Faction-specific — let the pillars determine the natural ratio. |
| **Rarity** | C=24, U=16, R=11, L=4 (2 minion, 1 spell, 1 weapon) across 55 cards |
| **Curve** | 1V=5-6, 2V=10-12, 3V=10-12, 4V=8-10, 5V=5-6, 6V=3-4 |
| **Legendaries** | Exactly 4. If counting shows 5, cut one. |

Rebalance until all four checks pass. Only then proceed to Phase 3 (Spec Validation).

**Proven format:** Trigger 2026-06-11 — 30 minion, 20 spell, 5 weapon slots, all metrics clean after rebalancing.

### Phase 2d: Slot Table Rebalancing

After the slot table is built, run four checks before proceeding to spec validation:

| Check | What | Fix |
|-------|------|-----|
| **Crew split** | P+Street vs M+Help percentages match target | Reclassify spells across crew boundaries or recut target. Ambush/Intel spells can shift Help→Professionals (contract killers set traps, scout targets). |
| **Rarity** | C/U/R/L counts match build facts | Bump cards up/down rarity. Overkill bodies, Intel+Mark spells, and chain enablers are natural Uncommon candidates. |
| **Curve** | V-band counts in target range | Shift 5V cards down to 1-2V. Add 1-drops if light. |
| **Legendaries** | Exactly 4: 2 minion, 1 spell, 1 weapon | Promote/demote as needed. |

**Proven 2026-06-11:** Trigger v1 slot table hit all four flags simultaneously (crew 53/47 vs 70/30, C=28 vs 24, 5V=8 vs 5-6, L=5 vs 4). Resolved by: recutting crew target to 60/40, bumping 4 C→U + 2 U→R, shifting two 5V→lower, demoting 1 L→R then promoting a different R→L. All metrics clean in one pass.

How many cards of each type does a drafter need to see per pack for a pathway to be draftable?

| Pathway | Common Need | Common Target | Notes |
|---------|------------|---------------|-------|
| Contract | ~10 Mark sources + ~10 Paid payoffs in pool | 7-8 commons per pathway | Ensures drafter sees enough to build |
| Arsenal | ~8 weapon/ammo cards | 4-5 commons | Weapon support should NOT outnumber weapons 3:1 |
| Court | ~5 disruption/intel cards | 2-3 commons | Specialty — rare-dependent |
| Street | ~4 Hustle bodies | 2-3 commons | Vanilla-adjacent, low synergy burden |

---

## Phase 3: Slot Boundaries

Define the box each slot can fit in BEFORE designing cards.

| V | Crew | Pathway | Rarity Range | Stat Range | Mechanic Options |
|---|------|---------|-------------|------------|-----------------|
| 1V | Street | Street Tempo | C | 1/1 - 2/1 | Hustle, vanilla |
| 2V | Professional | Contract | C-U | 2/2 - 3/3 | Mark BC, Paid, Armed |
| 3V | Professional | Contract | U-R | 2/3 - 3/3 | Paid scaling, Overkill, Contract draw |

---

## Phase 4: Subagent Batch Design

Paul defines constraints. Subagents design cards.

**Per-batch context (fed to each subagent):**
1. This batch's slots (V, crew, pathway, slot boundaries)
2. Full crew identity profiles (all 4 crews)
3. Daily Life scenes (the relevant crew's day)
4. Turn map for this pathway
5. Synergy edge requirements (which edges must be populated)
6. Ludo guidance (name conventions per crew)
7. "This card must be playable on curve. Earliest activation turn: ___"

**Batch size:** 5-10 cards per subagent. Smaller = more parallel = faster iteration.

**Paul's role:** Define constraints. Review output. Flag ludo failures, crew violations, turn feasibility problems. Subagents design. Paul quality-gates.

---

## Common Failure Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Crew bleed** | Street minion with Paid. Help minion dealing direct damage. | Check every card against crew CANNOT DO list. |
| **Pathway starvation** | Core pathway has 20% of cards when it needs 55%. Secondary pathway has 40%. | Audit pathway percentages against targets BEFORE designing cards. |
| **Decorative mechanic** | Overkill 2 on a 2V card — fires on T3 at earliest. | Calculate activation turn. If 2+ turns late, redesign or accept as bonus (not core function). |
| **Ludo collapse** | Spotter deals damage. Dues Taker draws cards. Name doesn't match function. | Run ludo pass as separate step. "What is this person's job? Does the card text match?" |
| **Spreadsheet blindness** | Edge numbers in table replace human-readable role descriptions. | Card tables should answer: who is this, what do they do, which crew? Edge numbers are audit tags, not display content. |
