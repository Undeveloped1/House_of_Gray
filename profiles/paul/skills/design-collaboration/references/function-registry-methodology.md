# Function Registry + Synergy Web Construction Methodology

## When to use

After archetype assignment and crew mechanical identities are locked, before any cards are designed. This replaces "33-row MadLibs" with function-first design.

## Function Registry Construction

### Step 1: Enumerate archetype-specific functions

For each faction build path (hero/precon), list the mechanical functions needed to execute the win line. Example for Bruiser Silver / Long Grind:
- Make Grit matter early T2-4
- Grit payoff / snowball T6-10
- Permanent growth outside combat
- Mirror draw / card advantage

Aim for 12-18 functions total for a 55-card faction. Some functions are core (shared across all build paths), others are path-specific.

### Step 2: Map each function to archetype and universal job

Every function must answer:
- Which archetype does this serve? (Wall, Value, Midrange, etc.)
- Which universal job does it fulfill? (Curve foundation, Card advantage, Interaction, Protection, Finisher, Flood insurance, Recovery, Redundancy)

A function that serves no archetype or fulfills no job is filler. Cut it.

### Step 3: Assign crew and notes

Which crew expresses this function? Add design notes: what bodies, what constraints, what blind spots to avoid.

### Step 4: Number and organize

Group functions by category: Shield Wall, Support, Cavalry, Extortion, Legendary. Number F01 through F22+. The numbering is a reference handle, not priority order.

### Step 5: Cross-reference against sub-archetype catalog

Before locking the registry, validate against the exhaustive sub-archetype catalog (`references/subarchetype-catalog-usage.md`):
- Which proven patterns does each function express?
- Are there patterns the catalog says the faction SHOULD use that aren't covered?
- Are there patterns the catalog says the faction should NEVER use that snuck in?

This is the anti-MadLibs quality check. The catalog is the full menu — the function registry is what you ordered.

### Step 6: Identify gaps

After mapping all functions to patterns, flag:
- Archetype needs with no function coverage
- Universal jobs with no function coverage
- Sub-archetype patterns the faction should use but doesn't

Add new F-numbers until all gaps are filled.

## Synergy Web Construction

### Step 1: Build edges from function pairs

For every payoff function, identify the enabler function. For every protection need, identify the body that provides it. Write explicit edges:

`W01: Cut Man (+2 HP) → Pit Fighter (survives for Grit → Rampage) | Edge type: Enables | Layers: Support → Cavalry`

### Step 2: Classify edge types

| Edge type | Pattern |
|-----------|---------|
| Enables | A makes B's condition true |
| Protects | A keeps B alive to do its job |
| Creates → Spends | A creates resource B uses |
| Punishes | A punishes what B forces |
| Curve chain | Play order T1→T4 |

### Step 3: Layer and precon coverage

- Vertical edges: same layer (wall → wall)
- Forward edges: one layer enables the next (wall → cavalry)
- Cross-precon edges: at least 2-3 edges bridge build paths

### Step 4: The minimum edge rule

Every shippable minion must touch at least one synergy edge. Cards with zero edges are candidates for cut unless they're explicit Rodmans with a named precon function.

### Step 5: Number and document

Number W01 through W18+. Each edge gets: source card, target card, edge type, and layer relationship.

## Output artifacts

- Function registry table (ID, function, archetype, universal job, crew, notes)
- Synergy web table (ID, source, target, edge type, layers)
- Gap analysis (what's missing)

## Relationship to card design

Functions and webs come BEFORE card names and stats. The skeleton is filled from the function registry, not from a role list. Role names come last — after the mechanical job and crew expression are locked.
