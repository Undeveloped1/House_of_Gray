---
name: faction-set-review
description: Ruthless game critic checklist for reviewing a Five Crests faction card set. Three passes — structural, mechanical, polish. Used to score sets from C through A. Model-agnostic, faction-agnostic.
category: creative
---

# Faction Set Review — Pipeline + Checklist

**Full pipeline for a faction card set review:**

```
Build set from synergy web + slot table
        │
        ▼
┌─────────────────────────────────┐
│  pre_review_audit.py            │  ← 30 seconds, automated mechanical gate
│  (scripts/pre_review_audit.py)  │     card counts, rarity, keywords, edges,
│                                 │     curve, 1V pressure, blind spots,
│                                 │     removal, vanillas, healing, naming
└──────────┬──────────────────────┘
           │
     PASS? ─── NO → Fix, re-run. Do not send to critic.
           │
          YES
           │
           ▼
┌─────────────────────────────────┐
│  Three-pass critic review       │  ← subagent, subjective checks only
│  (Pass 1 gate already met)      │     core loop density, enabler ratio,
│                                 │     anti-synergy, legendaries, heroes,
│                                 │     draft feel, fun factor, templating
└──────────┬──────────────────────┘
           │
     B+? ─── NO → Iterate (fewer issues now)
           │
          YES
           │
           ▼
         SHIP
```

**Before slot-filling: run the density calculator.** `python3 tools/density_calc.py` (hypergeometric distribution). Answers "how many Mark sources do we need for 90% draw consistency by Turn 2?" before any card is designed. The slot table is derived from density targets, not guessed. See `references/pathway-design.md` for the full pathway-design methodology (turn maps, crew identity profiles, as-fan calculations).

**Run the pre-review script first.** `python3 scripts/pre_review_audit.py <set_md>`. Only sets that pass go to the critic. The script catches everything mechanical — the critic should never flag a missing keyword sidebar, a count error, or a thin edge because the script already caught it.

**Format compatibility:** If the script returns zero cards found, the card table column order doesn't match the script's expected format. Patch `parse_card_table()` column indices in the script to match the actual format, and update `EXPECTED` for correct card counts (e.g., 29 minions vs script-default 30). See `bruiser-card-design-pipeline` skill, `references/sub-agent-card-production.md` for the Trigger v7 format mapping.

**After the script passes**, run the three-pass checklist below.

---

## Pass 1: Structural (Can You Read It?)

**Gate:** If any question in Pass 1 fails, the set cannot be reviewed further. Fix first.

| # | Check | Pass/Fail |
|---|-------|-----------|
| 1.1 | **Keyword sidebar exists.** Every mechanical keyword on any card is defined in one place. Mark, Contract, Paid, Cue, Bullet Time, Cloak, Hustle, Silence, Barrage, Armed, Reload — every word a player might not know. | |
| 1.2 | **Every keyword on a card IS in the sidebar.** No card references a mechanic not defined in the document. | |
| 1.3 | **No naming conflicts.** A keyword and a card do not share the same name (e.g., "Reload" keyword vs "Reload" spell). | |
| 1.4 | **Every card references only existing objects.** "Gain a Commission weapon" — does Commission exist? "Equip Saturday Night" — does Saturday Night exist? No phantom references. | |
| 1.5 | **Card counts match build facts.** 30 minions, 15 spells, 5 ambushes, 5 weapons = 55. Rarity totals match targets (±1 acceptable). | |
| 1.6 | **Every card has a cost, rarity, crew, stats (if minion/weapon), rules text, and edge assignment.** No blank rows. | |

**Pass 1 grade:** All 6 pass = A. 1 fail = C. 2+ fails = stop and fix.

---

## Pass 2: Mechanical (Does It Work?)

| # | Check | What to look for |
|---|-------|-----------------|
| 2.1 | **Core loop density** | The faction's signature mechanic needs enough cards to fire reliably. Minimum: 10 cards that participate in the primary loop. If Mark→Paid is the core, count every Mark source + every Paid payoff. Below 10 = CRITICAL. |
| 2.2 | **Synergy web edges are real** | Each edge in the web must have ≥2 cards. An edge with 1 card is not an edge — it's a single card's internal text. Count every edge. Flag all 1-card edges as MAJOR. |
| 2.3 | **Enabler-to-payoff ratio** | Does the faction have enough enablers for its payoffs? Weapons: 5 weapons, 13 cards that care about weapons → 2.6:1 ratio is acceptable but high. Count enablers vs payoff targets. Ratio above 3:1 is MAJOR. |
| 2.4 | **Curve supports gameplan** | Does the mana curve match the faction's tempo? Aggro: peak at 1-2V. Midrange: peak at 2-3V. Control: peak at 3-4V. Count minions per V-band. |
| 2.5 | **1V slot is functional** | At least 3 minions at 1V. At least 1 applies pressure (2+ ATK). Midrange decks need early board presence. Below 3 or zero pressure = MAJOR. |
| 2.6 | **Conditional vs unconditional removal** | Does the set have removal that works without setup? Count unconditional kill spells. Below 2 at common = MAJOR for draft. |
| 2.7 | **Blind spot compliance** | Check every card against the faction's "cannot do" list. Trigger cannot: Taunt, swarm, counterspell. Flag every violation as CRITICAL. |
| 2.8 | **Mechanical anti-synergy** | Do any cards fight their own faction? Cue on reactive ambushes (triggers on opponent's turn, can't sequence). Contract clutter (hand clogged with 0V tokens). Flag systemic anti-synergy as MAJOR. |
| 2.9 | **Turn feasibility** | Can each card's key mechanic actually fire on curve? Formula: a card at cost V with Overkill N needs V+N-1 mana minimum. **Distinguish two cases:** (A) The threshold IS the card — without it, the body is below rate (e.g. Spotter 2/3 vanilla for 3V). If this can't fire on curve, MAJOR. (B) The threshold is a BONUS on an already-good body (e.g. Bearcat 3/2 for 2V, Overkill 2 gives +1 ATK on turn 3+). If the floor is playable, late activation is fine. Flag case A as MAJOR, case B as MINOR (noteworthy but not blocking). | |

**Pass 2 grade:** 0 criticals + 0-1 majors = A. 0 criticals + 2-3 majors = B. 1+ criticals = C or below.

---

## Pass 3: Polish (Is It Good?)

| # | Check | What to look for |
|---|-------|-----------------|
| 3.1 | **Legendary impact** | Every legendary must pass: "Would a player feel something when they draw this?" Hell Yeah / Hoot / Oh Shit test. Flag unplayable legendaries as CRITICAL. Flag overtuned legendaries as MAJOR. |
| 3.2 | **Hero power tradeoffs** | HP totals should map to fragility: combo/aggro heroes get lower HP, control/grind heroes get higher HP. Hero powers should be useful in 80%+ of decks (not parasitic on 2 cards). Flag parasitic hero as MAJOR. |
| 3.3 | **Draft fundamentals** | Vanilla/french vanilla commons: 3-5 minimum. Common removal: 2+ spells. Common ambushes: 2+ if ambushes are faction-defining. Below any threshold = MAJOR. |
| 3.4 | **Splashy uncommons** | At least 1-2 uncommons that make a drafter say "I want to build around this." Not just role players — signpost cards that signal an archetype. Zero splashy uncommons = MINOR. |
| 3.5 | **Healing exists** | In a game with 26-30 HP heroes, a set with zero life gain is a design gap. Minimum 2 cards that restore HP. Zero = MODERATE. |
| 3.6 | **Templating is tight** | No ambiguous targeting ("target enemy" — minion or hero?). No unclear scoping ("Paid triggers fire twice" — yours or everyone's?). Every ambiguous card = MINOR. |
| 3.7 | **Fun factor** | When the machine fires, is it satisfying? Does the core loop create moments? If the faction's best draw feels like "play vanilla creatures and hope," that's MAJOR. If it feels like "I am executing my plan and it is working," that's good. |
| 3.8 | **Ludo verification** | Does every card name match what the card DOES? Spotter dealing damage = wrong (spotters watch and report, they don't shoot). Dues Taker drawing cards = wrong (they collect money, not intel). The Shooter dealing damage AFTER Paid fires = backwards (shooters shoot, THEN get paid). Check: "What is this person's job? Does the card text match?" Flag every ludo mismatch as MAJOR. Run this as a separate pass — it's the difference between a set that reads like game mechanics and one that reads like a world. |
| 3.9 | **SOUL CHECK (BLOCKING GATE — 2026-06-08)** | **Mechanical correctness ≠ good cards.** Ask: "If I showed this set to someone who'd never heard of the faction, would they know who these people are? Would they feel 1961 Detroit? Do the names pass the street-fight callout test? Is every card a PERSON, not a spreadsheet cell?" If the answer to ANY of these is no, the set FAILS — regardless of Pass 1-3 grades. **A- on soulless cards is a LIED grade.** The SOUL CHECK cannot be automated. It requires the reviewer to have read the faction lore docs. If the critic sub-agent hasn't loaded Inner_Circle.md, Daily_Life.md, and character profiles, it cannot perform this check — and its grade is invalid. This check is why Trigger v7 (audit-clean, A- by critic) was called "dog shit" by Joe — it passed every mechanical gate but had no creative soul. |

**Pass 3 grade:** 0 criticals + 0-1 majors = A. 0 criticals + 2-3 majors = B. 1+ criticals = C or below.

---

## Final Grade

Average of Pass 2 + Pass 3 grades (Pass 1 is a gate, not graded).

| Average | Verdict |
|---------|---------|
| A | Ship it. |
| A− | Ship with minor fixes noted. |
| B+ | Ship-ready. One quick cleanup pass. |
| B | Needs iteration. One focused pass on the 2-3 biggest problems. |
| B− | Needs iteration. Multiple systems need rework. |
| C+ or below | Needs rebuild. Core loop or structure is broken. |

---

## Common Failure Patterns

| Pattern | Symptom | Fix |
|---------|---------|-----|
| **Keyword soup** | 7+ sub-mechanics in 55 cards. None have density. | Pick 3-4 mechanics and commit. Cut the rest to set #2. |
| **Paper web** | Synergy edges defined but not populated. Edges are design-document fiction. | Count every edge. Cut edges with <2 cards or add cards. |
| **Parasitic draft** | Cards are blanks without specific partners. 2-card combos in a 55-card set. | Add more enablers at common. Add vanilla-rate bodies that happen to have the keyword. |
| **Trap legendary** | Legendary that reads exciting but is unplayable. | Playtest the floor case. If the floor is "6 mana do nothing," redesign. |
| **Blank hero** | Hero power interacts with <5 cards in the faction. | Broaden the trigger. "Your next Trigger card" not "Your next Locked On card." |
| **Aspirational edge** | Edge claims 6 cards, actually has 3. Designer's brain filling in cards that don't exist. | Audit every edge count against the actual card list. If you can't point to the card name, it doesn't count. |
| **Phonetic keyword collision** | Two keywords share a prefix or sound pattern (e.g., "Paid" and "Payoff"). Players confuse them at every draft table. | Check new keyword names against all existing keywords in the faction. If they share a syllable, pick a different word. See design-collaboration skill § Mechanic Naming Criteria. |
| **Over-salvaging** | Every card from the old set is "kept" or "reworked." The new set is a remix, not a rebuild. | Old cards are inspiration, not obligation. Steal what's worth a damn — name or ability. The rest is draft fodder. Not everything needs an edge. Vanilla commons and french vanillas are intentional, not failures. |
| **Crew bleed** | A Street minion has Paid. A Help minion deals direct damage. A Management minion carries a weapon. | Every crew has a CANNOT DO list. Check every card against its crew's identity profile. If the crew distinction collapses, the faction reads as "55 cards with different art" instead of "four crews with different jobs." |
| **Decorative mechanic** | Overkill 2 on a 2V minion — fires T3 at earliest. Mechanic exists on paper but can't fire on curve. | Calculate activation turn: cost V + threshold N − 1. If 2+ turns late, the mechanic is decorative. Either cut it or accept it as bonus text on an already-good body. |

---

## Post-Review Output

After the three passes, produce:
1. Letter grade with pass/fail counts
2. Ranked problem list (Critical → Major → Minor)
3. Specific fix for each Critical and Major
4. "Ship" or "Iterate" verdict
