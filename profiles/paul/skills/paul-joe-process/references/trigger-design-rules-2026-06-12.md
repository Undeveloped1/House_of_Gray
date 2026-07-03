# Trigger Design Rules — 2026-06-12

Living rules locked during the 2V band collaborative design session. 
Serve as a worked example of the "Living Design Rules — Create Immediately" pattern.

**Updated 2026-06-13** with 3V/4V rules: bullet/loader philosophy, Management stat-gap rule, Legendary brokenness, rare spread.

---

## Core Design Philosophy

**"The bullet, not the loader."** Direct effects over enablers. No "Choose One" ammo spells. No enabler chains that require three cards to fire before anything happens. The card does the thing — not sets up for something else to do the thing. Joe lock 2026-06-10/13.

**Character-first.** The character truth writes the mechanic. Re-read the Daily Life vignette before proposing any card.

**"One card at a time."** Present, discuss, lock, next. Don't throw multiple variants when the frame is undefined.

**"Do X" pattern.** When the trigger is clear (Joe said "if X, then do Y"), present 3-4 payoff options. When the entire card concept is undefined, design ONE proposal grounded in lore.

**Management at 4V+ needs Legendary-tier impact.** Management bodies are 1/1–1/3 territory (Scorekeeper, Dispatcher). To justify a 4V+ slot, the ability must be "crazy" — surgical intel that warps turns. At 5V, even crazier. Joe lock 2026-06-13.

**Legendaries are broken, not balanced.** Push past the line. If it could reasonably be Rare, it's not Legendary enough. Joe lock 2026-06-13.

**Rare spread at 4V/5V/6V:** 4/4/3. Joe lock 2026-06-13.

**Court at 3/4/5V.** Julian at 3V (Legendary). S11 Mass Mark at 4V (Uncommon). M23 Silence body + new Armed Legendary at 5V. Joe lock 2026-06-13.

---

## Armed Philosophy Shift

**Old assumption:** Armed bodies deploy standard weapons (e.g., "Armed: Equip a 2/1 Pistol"). W01 is the baseline Pistol drop.

**Joe's lock:** Armed bodies must NOT deploy vanilla weapons. Each Armed card needs a unique weapon with its own identity. Standalone weapons (W slots) are for deckbuilding — players can choose to include them. Armed weapons are signatures tied to specific bodies — they can't be obtained any other way.

**Example:** Specialist → Armed: Street Sweeper (1 ammo, spend ammo: deal 1 to target + 1 to adjacent). Not "equip a 2/1 Pistol."

**Implication:** W01 (Basic Pistol) is a Stiffs weapon now. Trigger standalone weapons need unique identity — armor piercing, rapid fire, hustle-granting, etc. Joe: "These are Triggers. They need to have a gun that's going to change the gameplay."

---

## 2V Stat Thresholds

Joe's explicit lock on what's acceptable at 2V:

| Stats | Requirement |
|-------|-------------|
| 1/1 | Must have a strong ability that justifies the 2V slot |
| 1/2 | Needs an ability (Bandolier: +2 ammo) |
| 2/1 | Needs an ability (Banger: ping 1) |
| 2/2 | Floor — the baseline 2V body |
| 2/3 | Acceptable |
| 3/2 | Acceptable (Bearcat) |
| 3/3 | Maximum — REQUIRES a drawback or opponent benefit to balance |

**Bearcat math note:** 3/2 Paid: +1/+1. Survives a 1/1 ping → becomes 4/2. Dies to a 2-attack creature. Joe: "You're not taking into account that she's going to take sustained damage from that first interaction."

---

## Overkill Chain Design — Rethink

**Issue:** The original Overkill chain enabler (S03) was spec'd as "Overkill 4: Draw 2 instead." Joe flagged that at 2V you physically can't chain 4 cards.

**Joe's direction:** Overkill needs tiered thresholds across the curve:
- **Early turns (2-3V):** Smaller thresholds (Overkill 2-3) with smaller payoffs
- **Mid turns (4-5V):** Medium thresholds (Overkill 4-5) — set pieces
- **Late turns (7-8V):** Finishers (Overkill 6+) — game-enders

S03 needs re-examination: how many cards can you realistically chain at 2V?

---

## Weapon Identity

**Joe's lock:** Basic pistols are for Stiffs. Trigger weapons must have mechanical identity:
- Snub Nose concept: close-range, double damage to Taunt minions, +1 ATK to wielder
- Armor piercing
- Rapid fire
- Hustle-granting
- Ammo-activated abilities

Weapons don't always represent distance — close-range weapons influence combat outcomes differently.

---

## Management Body Distribution

Joe questioned whether Management needs many bodies at low V-bands. Their strength is in spells (intel, Mark, disruption). Bodies may concentrate at higher curve where they're bigger, "curvier" threats. Front Desk at 1/2 is the right profile — thin body, strong filter ability.

---

## Contract Loop — Rube Goldberg Machine

Joe's analogy: the Contract loop (Mark → kill → Paid → Contract Scaling) is a Rube Goldberg machine. You're cycling through pieces, each triggering the next. Card draw and filtering (Front Desk, Shine Boy) are essential to keep finding pieces to "keep building the robe."

---

## Working Doc Convention

When Joe locks design rules mid-session, create a faction-specific `{Faction}_Design_Rules_Living_{date}_Paul.md` in the workspace. Reference it during design instead of re-stating locked rules. This file is the reference version — the workspace file is the working copy.
