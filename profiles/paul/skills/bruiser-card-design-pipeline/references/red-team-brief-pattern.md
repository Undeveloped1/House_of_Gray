# Red Team Brief Construction Pattern

Pattern for building self-contained Red Team packages. Two variants documented below.

## STRIP RULE — Read First

**Before delivering any brief, scan for faction keyword names.** Every word of every process example must be generic. Describe the EFFECT not the KEYWORD NAME.

Proven failure modes:
- "A dock worker might have Hobbled (can't attack)" → teaches Hobbled
- "A fighter might have Seasoned (gets stronger)" → teaches Seasoned
- "Rush (Hustle — attack immediately)" → teaches Hustle
- "A freight clerk → Hobble. A leg breaker → Sucker Punch" → teaches both
- **Listing function categories under a "Keywords:" header for crews that have NO keywords** → Red Team prints function labels as game mechanics

Fix: "A dock worker might delay shipments — their mechanic name should reflect that world." Describe the effect. Never name the keyword.

For crews that express through card text (not keywords): explicitly state "does not have faction-specific keywords."

---

## Variant A: Pure Lore (Blind Test)

Give: lore only. Test: can an AI independently derive crews, keywords, and cards?

### Two-Doc Structure

**Doc 1: Brief (lore + process + instructions)**

1. Orchestrator instructions at top. Spin up sub-agents, one per crew.
2. Pure lore — living texture of people and places, no named crews.
3. Full process explained: crews, archetypes, functions, mechanics, synergy, FERM.
4. Output format and evaluation criteria.

**Doc 2: Methodology (technical appendix)**

1. Mana curve — V-by-V counts, raw numbers only.
2. Power curve — 2×V = vanilla, stat grids, delta system.
3. Rarity distribution — 13C/10U/7R/3L.
4. Design rules — hard rules, faction constraints, ability budgeting guidelines.

### What to STRIP
- Crew names, definitions, keywords, mechanics, functions, cards
- Archetype labels, precon names, cross-matchup targets
- Interpretive curve labels, 70/30 split
- ALL keyword names from process examples

### Reference
Bruiser Red Team v2: `design/bruiser_revisions/Bruiser_Red_Team_Brief_v2.md` + `Bruiser_Red_Team_Methodology_v2.md`

---

## Variant B: Full Framework, No Cards

Give: everything except the 33 cards. Test: does the framework inevitably produce our cards?

### Single-Doc Structure

1. Orchestrator instructions.
2. All four crews with definitions, mechanical identities, and ACTUAL keywords (for crews that have them).
3. Function registry (16 functions).
4. Mana curve with crew allocation per V.
5. Rarity distribution.
6. Power curve with stat grids and delta system.
7. Design rules and faction constraints.
8. Output format.

### Crew Keyword Rules

- **Dock/Yard and Street:** List their actual faction keywords (Hobble, Tax, Shield, Hazard Pay, Taunt | Sucker Punch, Beatdown, Seasoned, Intimidation, Hustle, Overkill, Rampage).
- **Hall and Spread:** Explicitly state "does not have faction-specific keywords. Expresses through card text." Do NOT list function names (Deal, Recon, Pawn, Payout, etc.) under a Keywords header.

### What to STRIP
- All 33 card designs (names, stats, text, flavor)
- Any pseudo-keywords for Hall/Spread

### Reference
Bruiser Red Team v3: `design/bruiser_revisions/Bruiser_Red_Team_Brief_v3.md`
