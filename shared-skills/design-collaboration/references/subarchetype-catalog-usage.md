# Sub-Archetype Catalog Usage

## What it is

An exhaustive reference of every proven MTG and Hearthstone interaction pattern — organized by category with Bruiser fit (Yes/Maybe/No) for each. ~190 patterns across 6 categories in the Cursor repo version, ~60 in the Paul vault version. Both should be read.

**Repo location:** `docs/bridge/paul_design/TCG_SUBARCHETYPE_CATALOG.md`
**Vault location:** `Paul/design/TCG_Subarchetype_Catalog.md`

## When to use

1. **Before locking a function registry** — cross-reference every F01-F22 function against the catalog. Ask: which proven pattern does this function express? Are we missing patterns the faction should use?

2. **When designing a new faction** — use the catalog as the full menu. Filter Yes/Maybe/No for the faction, then build the function registry from the filtered list.

3. **When a faction's design feels thin or samey** — consult the catalog for patterns adjacent to the faction's identity that could add depth without violating blind spots.

## How to use

### Validation pass (per function)

For each function in the registry:
1. Identify which catalog pattern(s) it expresses
2. Confirm the catalog says Yes or Maybe for that pattern on this faction
3. If the catalog says No — flag it. Either the function is wrong, or the catalog judgment needs updating.

### Gap analysis (per faction)

1. Scan the catalog for all Yes and Maybe patterns for the faction
2. Check if each has a corresponding function in the registry
3. Flag patterns with No coverage — these are potential new functions
4. Flag patterns intentionally excluded — document why (blind spot, faction identity, etc.)

### Disagreement resolution

When Paul and Cursor disagree on a Bruiser fit (e.g., Cursor says Voltron is No, Paul says Maybe):
1. Present both rationales to Joe
2. Joe resolves
3. Update the catalog to reflect the locked judgment
4. Update the function registry if the resolution creates or removes a function

## Key patterns per Bruiser archetype

### Wall/Fortress (primary)
- Vendetta/Taunt walls (Yes)
- Go-Tall / +1/+1 Counters (Yes — Grit)
- Defensive Wall / Fortress (Yes)
- Enrage / When-Damaged (Yes — Grit triggers)
- Tax / Resource Choke (Yes — extortion F09)
- Payback / Thorns (Yes)
- Control Warrior / Armor (Yes — Silver wall + armor analog)

### Midrange Combat (secondary — Tommy)
- Overkill / Trample (Yes)
- Rampage Chain (Yes — 5C native)
- Midrange Curve (Yes)
- Handbuff (Maybe — Coach training)
- Dormant / Awaken (Cursor says Yes, Paul says Maybe — Joe to resolve)

### Value / Engine (secondary — Silver)
- Draw Engines (Yes — Vic mirror draw)
- Scry / Selection (Yes — F11 intel)
- Tutor Toolbox (Maybe — Towel Boy)
- Go-Tall / +1/+1 Counters (Yes — Grit scaling)
- Proliferate (Maybe — one effect max)

### Attrition / Dock Tax (tertiary — Irving)
- Resource Tax / Stax (Yes — F09 extortion)
- Attrition / Resource Choke (Yes)
- Discard-as-Resource (No — but board-linked toll Maybe)
- Pillow Fort (Maybe — Vendetta bodies as mobile walls)

## Patterns to explicitly avoid (Bruiser)

- Stealth / Evasion (No — can't miss these guys)
- Burn / Direct Damage (No — combat only)
- Go-Wide Tokens (No — tall not wide)
- Reanimator / Cheat-from-Graveyard (No)
- Storm / Solitaire Combo (No — board required)
- Voltron / One Champion (Maybe — Joe 2026-05-24: Grit + weapon stacking on one fighter is valid. Giant Rampage guy with a weapon fits cavalry. No hexproof.)
- Dormant / Awaken (No — Joe 2026-05-24: stealth-adjacent. Untargetable while dormant. Rampage timing delivers the cavalry wave feel.)
- Aristocrats / Death Triggers (Maybe — Joe 2026-05-24: brotherhood angle. When a brother dies in combat, the rest fight harder. Not self-sacrifice engine.)
- Blink / Flicker (No — Joe 2026-05-24: Bruisers stay on the board. Skivers could blink, not Bruiser.)
- Rush / Charge (UNRESOLVED — Joe needs clarification on HS Rush vs MTG Haste. Cursor to clarify.)
- Villium Burst / Coin Tempo (UNRESOLVED — Joe uncertain. Cursor to provide more context on Tommy lethal turn spike viability.)
