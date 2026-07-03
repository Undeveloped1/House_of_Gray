# Card Curve Framework

**When to use:** After mechanics brainstorm (Step 5), before individual card design (Step 7). This is the bridge — it ensures the faction's minion pool has enough unique cards per Villium slot for real deckbuilding choice.

## Step 1: Stat Ranges per Villium Level

| V | Stat Range | Midrange Sweet Spot | Notes |
|---|-----------|-------------------|-------|
| **1** | 1/1, 1/2, 2/1 | 1/1 (with ability) | 1-cost bodies need an ability to earn the slot |
| **2** | 2/2, 1/3, 2/3 | 1/3 or 2/3 | 3/2 for 2V is premium value — high pick rate |
| **3** | 3/3, 2/4, 3/4 | 2/4 or 3/3 | **Midrange peak.** This is where the faction turns the corner |
| **4** | 3/5, 4/4 | 3/5 | Power slot |
| **5+** | 5/5+ | As needed | Finishers |

A 3/3 for 1V would need an extreme downside. A 2/4 for 2V is outside range. Abilities define the card beyond the stat line, but the stat line must stay in range.

## Step 2: Deck Slots vs Unique Set Cards

This is the critical distinction — confusing these two produces factions where every deck runs the same cards.

| V | Deck Slots | Unique Cards in Set | Copies per Card |
|---|-----------|-------------------|-----------------|
| **1** | 3-4 | 4-5 | 2 each (common/rare) |
| **2** | 3-4 | 4-5 | 2 each |
| **3** | 5-6 | 5-7 | 2 each |
| **4** | 4-5 | 4-6 | 2 each |
| **5** | 2-3 | 3-4 | 1-2 each (some legendary) |
| **6+** | 1-2 | 2-3 | 1 each (legendary/rare) |

**If you design 2 unique 1-costs, both are in every Bruiser deck.** No choice, no variety. The set needs 4-5 unique cards per slot so players pick their favorites. ~23-30 unique minion cards total for the faction.

## Step 3: Curve Shape by Archetype

| Archetype | Peak Slot | 1V Count | Feel |
|-----------|----------|---------|------|
| **Aggro** | 1-2V | 6-7 deck slots | Flood early, close fast |
| **Tempo** | 2-3V | 4-5 deck slots | Efficient bodies, consistent pressure |
| **Midrange/Fortress** | 3-4V | 2-3 deck slots | Survive early, dominate mid |
| **Control** | 4-5V | 0-2 deck slots | Stall until power turns |

For Bruiser (Fortress midrange): the bulk is at 3-4V. Turns 1-2 are survival, not pressure. By turn 3, Bruiser stabilizes and starts trading favorably. By turn 4-5, Seasoned bodies are growing and Beatdown chains are online.

## Step 4: Faction-Specific Stat Rules

Bruiser-specific rules discovered during PlanB card design (2026-05-26):

- **No 0/X bodies.** Bruisers don't have 0-attack minions. Everyone starts at 1/1 minimum. Punching Bag works as a 0/2 only because Grit makes him dangerous. Without a growth keyword, every Bruiser body starts with at least 1 attack.
- **Abilities on every body at 1V.** A vanilla 1/1 for 1V is a Skiver card, not a Bruiser card. Bruiser 1-drops need Taunt, an enter effect, a deathrattle, or a crew keyword.
- **Midrange doesn't match Skiver body-for-body early.** By turn 3, Bruiser should have 2-3 bigger bodies that trade favorably into Skiver's 3-4 weenies. The bodies are better, not more numerous.

## Step 5: Board State Philosophy (Critical — Added 2026-05-26)

Before building a curve, define what the faction's board looks like WHEN IT'S WINNING. Two factions with identical minion counts and identical winning board states are one faction too many. The curve is the path; the board state is the destination.

**Rule: Factions that share a dominant card type must differ in board state philosophy.**

| Faction | Board State When Winning | Curve Implication |
|---------|-------------------------|-------------------|
| **Skiver** | WIDE — 4-6 bodies, each small but chipping | Peaks low (1-2V), reload mechanics |
| **Bruiser** | TALL — 2-3 bodies, each a growing threat | Peaks mid (3-4V), snowball mechanics |
| **Duster** | EMPTY — your board is clear, theirs can't stick | Flatter curve, heavy spells |
| **Faceless** | IRRELEVANT — board state doesn't matter, they're milling your library | Curve may not follow minion logic |
| **Stiffs** | LOCKDOWN — minions detained, evidence stacked, board frozen | Curve + ult synergy |
| **Trigger** | ARMED — fewer bodies, each carrying a weapon | Weapons and buffs matter more than curve |

**Corollary: Curve position follows board philosophy, not the other way around.** Design the winning board state first. Then build the curve to reach that state.

**Red Team application:** When Red-Teaming a new faction, the first question is not "what's the curve?" — it's "what does the board look like when this faction is winning?" Two factions that answer identically are a design collision. Fix the philosophy before touching the curve.

## Companion: Bruiser Scoring System

This framework defines WHAT the curve should look like. [`Bruiser_Scoring_System.md`](../../../design/bruiser_revisions/Bruiser_Scoring_System.md) (created 2026-05-26) defines HOW to cost individual cards within that curve — stat budgets, ability point costs with faction modifiers, and delta rules. The two documents are designed to be loaded together during card design: curve framework for deck-level structure, scoring system for card-level budget.

The scoring system adapts Model B (Framework v6.2 Part 2) for Bruiser's keyword set with a two-layer modifier system (Bruiser-wide + crew-specific) at 0.1 granularity. Every ability's final cost = base cost + faction modifier + crew modifier. Delta range: -2.0 to +2.0 with flagging at extremes. Default bias toward positive deltas — Bruiser bodies fight.

## Pitfalls

- **Confusing deck slots with unique cards.** "3-4 slots at 1V" means 3-4 cards IN THE DECK, not 3-4 unique designs. See Step 2.
- **Putting the bulk at 2-3V for midrange.** That's a tempo curve, not a Fortress curve. Midrange peaks at 3-4V.
- **Designing vanilla commons at 1V for Bruiser.** A keyword-only body without flavor fails the poker table test AND the curve framework. Every Bruiser card should feel like a person, not a stat delivery vehicle.
