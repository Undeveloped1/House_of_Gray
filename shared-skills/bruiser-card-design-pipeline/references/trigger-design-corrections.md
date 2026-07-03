# Trigger Design Corrections (2026-06-06 Session)

Load before any Trigger function, mechanics, or card design work. These are
concrete corrections from Joe that override Paul's initial assumptions.

---

## Mark is a Bonus, Not a Requirement

**Wrong (Paul v1-v3):** "F04 Marked Removal — conditional removal requiring Mark setup."
**Correct (Joe):** A Professional can kill anything. Mark means you get Paid for it.

The Mark → kill → Paid sequence is an incentive structure, not a permission gate.
Removal works without Mark — just less efficient or with fewer payoffs. The function
registry describes removal with Marked upside, not removal gated by Mark.

Contract wording: "Deal 4 damage to target minion. If it was Marked, draw a card."
Not: "Destroy target Marked minion."

---

## Court = Control Tier (Not Taxing, Not Counterspells)

Trigger's control comes from the Court — hand disruption, social nullification, bounce.
Not from Management bureaucracy. Not from counterspells.

**Court mechanical expressions:**
- Hand disruption: "Look at opponent's hand. Put one card on bottom. They draw."
- Social nullification: "Target minion can't attack or block this turn."
- Reality distortion: "Opponent bottoms their hand and draws that many." (Rare+)
- Name erasure: "Name a card. Opponent reveals and discards all copies." (Rare+)

**What Court does NOT do:**
- Taxing (enemy spells cost more) — that's Management bureaucracy
- Counterspells — Trigger has no counters. Bullet Time protects; doesn't counter.
- Hard removal — that's Professionals. The Court leaves you alive on purpose.

All Court expressions live under F09 Intel — same function, different crew tier.

---

## Dead Man's Eyes vs Dead Man's Hand

Same Villium capability (perception/intel). Different who's using it:

- **Dead Man's Eyes** — Professional/Management. Passive intel. Hand peek, scry.
  "I see what you're holding."
- **Dead Man's Hand** — Court. Active interference. Hand replacement, forced redraw.
  "Here's your new hand. You're gonna wish you were dead."

Both live under F09 Intel as separate mechanical expressions. Dead Man's Hand is
the Court face; Dead Man's Eyes is the Professional/Management face.

---

## Locked On = Lock + Bullet Time (One Function)

Joe: "Lock and Bullet Time, as far as I understood, are the same mechanics."

Locked On has two faces, one function (F08):
1. **Scaling payoff** — Locked On 2/4/6: effects scale on position in turn's chain
2. **Chain protection** — Bullet Time: "Your spells can't be countered this turn." (Rare+)

The protective side is the Rare+ expression of the same mechanic. Don't split
into two F-IDs. "When the chain is locked, nothing interrupts it."

---

## Terminology: "Locked On" Not "Lock"

Joe: "You're also not using locked on, you're using lock. So that doesn't even
match what the design documents call for."

The mechanic name is **Locked On** (Locked On 2, Locked On 4, Locked On 6).
"Locked on target" — firearms/military acquisition terminology. The warmup doc
used "Lock" as shorthand and Paul's mechanics doc drifted to match. Always
cross-reference the latest Daily Handover or Lock_Governance.md for canonical
mechanic names before writing new documents.

---

## Honed Cut

Joe: "We're probably gonna end up getting rid of Honed. It doesn't really provide
any additional value and just convolutes the ammo and weapon system."

**Before:** Armed → Honed → Ammo Management → Special Ammo (4 weapon functions)
**After:** Armed → Ammo Management → Special Ammo (3 weapon functions)

Inner_Circle.md listed Honed as a Help card lane ("Armed · Honed · utility").
Joe overrides: cut anyway. Three functions do the work of four, cleaner.

---

## Blind Spots That Were Paul Extrapolation

**Wrong (Paul, in warmup doc):**
- "No direct hero damage spells (the Contract is for minions)"
- "No AOE board clear (individual answers only)"

**Corrected (Joe):**
- Direct hero damage IS allowed — 1-2 spells targeting "minion or hero"
- AOE is not a meaningful Trigger-specific blind spot (nobody has it except Duster)
- Il Trio (Rare) is the exception for multi-target removal

**Rule:** Blind spots only go in documents if Joe explicitly locked them.
"Extrapolated from philosophy" is not a source. Mark proposed constraints
as PROPOSED or ask Joe.

---

## Crew Distribution Target

| Tier | Target % | ~Cards (of 55) |
|------|----------|----------------|
| Professionals | 50% | 27-28 |
| Street | 20% | 11 |
| Help | 20% | 11 |
| Management | 10% | 5-6 |

**Professionals+Street: 70%** (the minion bulk, Mark/Paid/Armed bodies)
**Management+Help: 30%** (spells, intel, ammo support, Court disruption)

The Design_Bible.md still says ~40% Management. That's the OLD distribution
from before the crew rebalance Joe locked in Session 2. Always use the latest
locked numbers from the Daily Handover or Build Facts doc.

---

## Mandatory Doc Read List for Trigger

Before any Trigger function/mechanics/card work, read ALL of these from the
tcg-engine repo (`/root/tcg-engine/docs/Five_Crests/factions/Trigger/`):

1. 00_INDEX.md
2. Identity.md
3. Playstyle.md
4. Design_Bible.md
5. Inner_Circle.md
6. Lock_Governance.md
7. Functions.md (legacy — mine for concepts, don't treat as current framework)
8. Daily_Life.md
9. Territory.md
10. Support_Network.md
11. Precon.md
12. Hero_Cards.md

Skip: Mechanical_Brainstorm_REFERENCE.md (BANK/NOT SHIP), Archetypes_Factory
(BANK), Timeline_Factory (reference), Art_Direction_Factory (reference).

Paul's vault docs to also load:
- `workspace/Villium_Faction_Relationships_Paul.md`
- `workspace/Trigger_Function_Registry_v3_2026-06-06_Paul.md`
- `workspace/Trigger_Build_Facts_v1_2026-06-06_Paul.md`
- `workspace/Trigger_Synergy_Web_Warmup_2026-06-06_Paul.md` (if continuing from warmup)
