# Faceless Upgraded Pipeline v2 — Competitive Slotting + Stress Testing

Source: `workspace/Faceless_Card_Design_Upgraded_v2_Paul.md` (2026-06-07)
Proven on Faceless faction — 98.7% critic score, 4 redundancies caught that rubric missed.

## The Process (11 Phases)

### PHASE 1: Functions Pass
One sentence per card. No numbers. No keywords. Pure function.
- Example: "Sacrifice fodder that enables bigger effects" — not "1/1 Blessed"
- Reveals redundancies: if two cards have the same function sentence, one is wrong
- Anti-pattern: filling a mana slot first, then writing a function to justify it

### PHASE 2: Competitive Slotting
Cards fight for their slot. For every mana cost:
1. **Within archetype:** Same function? Pick one. Cut or re-function the other.
2. **Across archetypes at same cost:** Different archetypes CAN coexist — but must feel like different decks.
3. **Rank within cost tier:** Bottom 20% are redesign-or-cut.
4. **"Why wouldn't I always pick this?"** test: if a card is clear best-in-slot, other cards at that cost need a reason to exist.
5. **Slot Competition Matrix:** Table with Card/Archetype/Function/Competes With/Verdict for the most contested slot (usually 3V).

Catches: same-function-different-cost (Recruiter 3V vs Street Preacher 1V), linear upgrades (Brother 3V vs Hushed Witness 2V).

### PHASE 3: Stress Test
Simulated combat against aggro and control matchups.
- Build opponent's ideal T1-T5 curve
- Run it against the faction's draw
- Does the faction stabilize in time?
- Test all three archetypes against their natural counters

### PHASE 4: Build the Cards
Using functions pass + slotting analysis, design cards into the constrained slots.
Redesign cards that had red flags from slotting.

### PHASE 5: Competitive Ranking
Rank every minion in the archetype from strongest to weakest.
- S-tier, A-tier, B-tier, C-tier, D-tier
- Identifies power gaps: if D-tier (essential but weak) and S-tier are both in the same archetype, the deck has a fragile curve
- Identifies B-tier role players that never excite — cut candidates

### PHASE 6: Draw-at-Any-Turn Evaluation
Score each card at Turn 1, Turn 5, Turn 8.
- Dead early, dead late, viable at all stages
- Identifies cards that are only good in one game state

### PHASE 7: One-Card Wonder Test
"Would a player open this in a pack and want to build around it?"
- Every Legendary must pass. Most Rares should pass.
- Commons and Uncommons are role players — they're allowed to fail.

### PHASE 8: Cross-Splash Verification
Verify the +1V splash tax works for all six cross-archetype combinations.
- Flag low-cost cards that become unplayable with the tax.

### PHASE 9: Scoring Against Rubric
Score refactored cards against Master Rubric Lanes M (Cards) and N (Naming).

### PHASE 10: Patch Candidates
Every failure generates a patch candidate for the playbooks.
Format: `PATCH: <playbook> § <section> | Add: <specific line>`

### PHASE 11: Compound Tracker
Log date, faction, phase, cards scored, pass rate, patches applied.

## What It Catches That The Standard Pipeline Misses

1. Same-function-different-cost redundancies (slotting, not the rubric)
2. Linear upgrades (same function, bigger numbers — passes rubric, fails slotting)
3. Canon contradictions in context (changelog vs set doc)
4. Power curve health (ranking exposes fragile curves)
5. Draw reliability across game states (T1/T5/T8 scoring)

## When To Use

Use this full process for:
- New faction card design from scratch
- Major set reworks
- Any design session where card count > 20

Skip phases 5-8 for:
- Quick iteration passes (≤5 card changes)
- Post-critic fix passes
