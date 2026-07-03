# Five Crests Design Document Map

## Read Order (top-down)

1. **`FIVE_CRESTS_OPEN_DESIGN_QUESTIONS.md`** — Joe's locked game identity answers (Villium, interaction, RNG, match length, win conditions). Read first.
2. **`Five_Crests_Archetype_Guide.md`** — Game-level definition. Archetypes, psychographics, axes, faction territory, deck anatomy, match structure. Foundation for all faction work.
3. **`MTG_Hearthstone_Success_Analysis.md`** — Deep analysis of what made MTG and Hearthstone successful. Psychographics, archetypes, resource systems, moment design.
4. **`TCG_Subarchetype_Catalog.md`** — Exhaustive reference of 60+ proven MTG/HS interaction patterns with Bruiser fit (Yes/Maybe/No). Validation tool for function registries.
5. **`Bruiser_Playstyle_Identity.md`** — Legion metaphor, three-layer formation, build paths, function registry (F01-F22), synergy web (W01-W18), design checklist.
6. **`Bruiser_Criminal_Crews_Working_Doc.md`** — Tier 1 canon. Ten crews, role pools, naming rules, female/non-traditional roles, adjacent businesses.

## Cursor Repo Equivalents

When Joe runs `hermes-bridge.ps1 pull-design`, these vault docs sync to repo:
- `Five_Crests_Archetype_Guide.md` → `docs/Five_Crests_Archetype_Guide.md`
- `Bruiser_Playstyle_Identity.md` → `docs/bridge/lore/bruiser/Bruiser_Playstyle_Identity.md`
- `Bruiser_Criminal_Crews_Working_Doc.md` → `docs/bridge/paul_design/Bruiser_Criminal_Crews_Working_Doc.md`
- `TCG_Subarchetype_Catalog.md` → `docs/bridge/paul_design/TCG_SUBARCHETYPE_CATALOG.md`

## Cursor also maintains (repo-side, agent-readable)

- `docs/CARD_CRAFTING_METHODOLOGY.md` — FERM framework + 6-step design process
- `docs/TCG_ARCHETYPE_PLAYER_MOTIVATIONS.md` — Timmy/Johnny/Spike + definitions of success
- `docs/CARD_DESIGN_SYSTEM_FOR_PAUL.md` — Paul's role in the factory
- `docs/bridge/lore/bruiser/JOE_DECISIONS_2026-05-23.md` — Canon locks
- `docs/bridge/lore/bruiser/FUNCTION_REGISTRY_DRAFT.md` — F01-F16 seed
- `docs/bridge/redteam/round-005/PARENT_SYNTHESIS.md` — Rev C minions (reference only)

## Document Dependency Chain

```
FIVE_CRESTS_OPEN_DESIGN_QUESTIONS (Joe locks)
    ↓
Five_Crests_Archetype_Guide (game definition)
    ↓
Bruiser_Playstyle_Identity (faction application)
    ↓
Bruiser_Criminal_Crews_Working_Doc (world truth)
    ↓
Function registry + synergy web (F01-F22, W01-W18)
    ↓
Card expressions (FERM pass)
    ↓
Final doc → Pass 6 JSON
```

Supporting layers:
- `MTG_Hearthstone_Success_Analysis.md` informs the Archetype Guide
- `TCG_Subarchetype_Catalog.md` validates the function registry
- `CARD_CRAFTING_METHODOLOGY.md` governs card expression

## Session Context

Copies of all significant documents are saved to `Brain/Session Context/` at compression points and session close. These serve as redundancy against sync overwrites and enable cross-session discoverability.

## Bruiser Revisions — Active Design (PlanB)

These are the working documents for the current Bruiser card design pass. All live under `design/bruiser_revisions/` in the vault (`docs/bridge/paul_design/bruiser_revisions/` in repo):

- **`Bruiser_Card_Design_Brief.md`** — Single source of truth for card constraints: power curve, keyword limits, crew color-coding, locked cards. Load at the start of every card design session.
- **`Bruiser_Scoring_System.md`** (created 2026-05-26) — Model B adapted for Bruiser. Full power curve per V with character-driven bodies. Ability base costs in 0.1 increments. Two-layer faction modifier matrix (Bruiser-wide + crew-specific). Delta rules. Companion to the brief — load both before designing cards.
- **`Bruiser_Minion_Roster_PlanB.md`** — Living roster doc. Lore, crew texture, function registry, mechanics brainstorm, synergy web. The world document.
- **`Bruiser_Minion_Roster_MERGED.md`** — Round 006 parent merge candidate (reference only, superseded by PlanB).
- **`00_INDEX.md`** — Which files are what. Round 006 context.
- **`Bruiser_Turn_Curve_Narrative.md`** (created 2026-05-29) — Turn-by-turn feel T1-10 from both sides of the table. Roman legion metaphor. Discount chain, Vendetta balance, opponent's arc, T4 as fulcrum. Feed to any model doing band craft so it knows what each V-band is supposed to DO.
- **`Bruiser_Band_Capability_Reference.md`** (created 2026-05-29) — Stat ranges, ability budgets, rarity ceilings per V-band. Marries the mechanical grid to the turn-curve narrative. Quick-lookup: "what's sound at this V-band?" Guidelines, not rules. Best used alongside the Turn-Curve Narrative during band craft.

**Load order for card design sessions:** Brief → Scoring System → Turn-Curve Narrative + Band Capability Reference (for knowing what each V-band does and what's sound there) → PlanB (for crew texture reference).
