# Warmup Document Pattern — Faction Design Sessions

**Validated:** Trigger v2, 2026-06-05 (autonomous build) · Trigger Phase 1, 2026-06-06 (Joe+Paul direct session)

## Two Use Cases

**1. Joe + Paul direct sessions** — the warmup is a handoff/continuity doc. Contains: where we are in the pipeline, phase status, design pillars locked, documents to load (in order), what to do next. Paul reads this at session start to pick up where the last session left off without Joe re-explaining. Example: `Trigger_Session_Warmup_2026-06-06_Paul.md` — Phase 1 Framework warmup that bootstrapped archetype → function → mechanics derivation in one session.

**2. Autonomous overnight builds** — the warmup is the ENTIRE brief for a fresh instance. Contains pre-built function registry, synergy web, band allocation, lore references, process steps, output specs. The fresh instance reads this one file and follows the references.

## Structure

A warmup document has seven phases. Each is self-contained so a fresh instance needs only this file plus the referenced docs.

### Phase 0 — What You MUST Read First

List every document the instance needs, in reading order. Group by category:

1. **Process & Pipeline** — CARD_PRODUCTION_PIPELINE.md, DESIGN_GUIDELINES.md, etc.
2. **Corpus Navigation** — 00_START_HERE.md, STATE_OF_THE_CORPUS.md, TOOLS_INDEX.md, faction 00_INDEX.md
3. **Faction Lore** — Faction bible, archetypes doc, lock governance, mechanical brainstorm, character depth pass, voice/visual, art direction, headline test
4. **Format Reference** — Bruiser_Cards.md, Hero_Cards.md

**PITFALL:** Do not include a reference set (v1 cards) in the reading list. The instance will treat it as the answer.

### Phase 1 — Function Registry (Pre-Built)

List 12-18 named functions with descriptions. Format:

```
F01  Function Name     Description of what this function accomplishes.
F02  Function Name     ...
```

Include a tier-to-function mapping table so the instance knows which tier handles which functions.

### Phase 2 — Synergy Web (Pre-Built)

List 8-15 named edges. Format:

```
W01  Card A → Card B     Type (Enables/Protects/Creates→Spends). Description.
```

Include an edge-type breakdown table (Enables, Protects, Creates→Spends, Punishes, Curve chain).

### Phase 3 — Band Allocation

Villium curve targets per cost, with tier distribution and rarity targets. Give exact numbers per band.

### Phase 4 — How to Design Each Card

Copy the Living World Method steps from DESIGN_GUIDELINES.md §3. Include anti-patterns and the six jobs.

### Phase 5 — Faction Locked Parameters

- Four-tier structure with mechanical identity per tier
- Villium activations per tier
- Core abilities (faction-defining, primary, supporting, digital-native)
- Named characters with rarity targets
- Legendary picks (4 total: 2 minion, 1 spell, 1 weapon for weapon factions)
- Curve cap (6V for all factions in Founder's Edition)
- Hard blind spots with Joe quotes — only include constraints Joe explicitly stated
- Crew distribution targets (70/30 Professionals+Street vs Management+Help for Trigger)

**PITFALL: Stale parameters from previous runs.** If a parameter references a mechanic or card from a doc marked BANK/NOT SHIP (Ghost Permanents, Hidden Contract, Cover scaling, Simultaneous Hidden Choice, The Forger), it is DEAD. Do not include it. Cross-reference every listed parameter against the faction's Design_Bible.md before finalizing the warmup.

**PITFALL: Blind spot extrapolation.** Do not include negative constraints (\"no X\") unless Joe explicitly stated them. Paul has a recurring failure mode of deriving blind spots from design philosophy and writing them as locked constraints. \"No direct hero damage spells\" appeared in the Trigger warmup as a blind spot — Joe never said this and explicitly overrode it. If you're not sure whether Joe locked something, mark it PROPOSED or omit it. A stale blind spot in a warmup doc propagates through the entire design session.

### Phase 6 — Output Files

Exact file names, formats, and contents expected. Include the card table format:

```
  #  R  V  Name             Tier         Stats  Text
```

### Phase 7 — Rules

Non-negotiable rules for the instance: function-first always, draw from lore, annotation requirements, etc.

## Example Warmup Doc

A complete, proven warmup document (Trigger, 55 cards) is at:
`/root/.hermes/docs/Paul/workspace/Trigger_Warmup_v2_2026-06-05_Paul.md`

Reference it for structure and tone.

## Key Design Decisions the Orchestrator Makes

The orchestrator pre-builds these so the instance doesn't have to:

1. **Function registry** — what the set must DO
2. **Synergy web** — how cards relate to each other
3. **Band allocation** — curve targets
4. **Legendary picks** — which three (from the candidates). **Mark these as LOCKED.** Specify rarity + card type for each (e.g., "L/6V minion," "L/5V spell").
5. **Hero candidates** — which three characters, with HP values
The instance fills in: card rows (as expressions of functions), design notes, hero card text.

### Pitfall: Legendary Drift

The fresh instance may change Legendary picks or rarity slots mid-design without updating the header. Example from Trigger v2 (2026-06-05): the warmup specified Smoke and Mirrors as the third Legendary (L/5V spell), but the instance created "Everybody Pays" at L/5V instead and demoted Smoke and Mirrors to R/4V without flagging the deviation. The roster header still listed the original picks.

**Prevention:** In Phase 5 of the warmup, add a rule: "The three Legendary picks below are LOCKED. If you find a better Legendary during design, you may substitute it, but you MUST flag the deviation prominently in the Design Notes §10 and update the roster header."

The instance fills in: card rows (as expressions of functions), design notes, hero card text.