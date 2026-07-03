# Subagent Card Design Pipeline

**When to use:** After lore lock on a faction. The emotional chords, crew structure, and character identities are approved. Card design begins.

## Subagent Prompt Template

For each crew lane, use this template. The key fields are `goal` (one-sentence), `context` (lore path + chords + crew identity + mechanical constraints), and `emotional target` (which chord to hit).

```
## Crew: [Crew Name] — [Archetype]

### Hero Card
Design the [Hero Name] hero card for the [Crew Name] archetype. HP must be stated. Voice line must hit chord #[N].

| Slot | Name | Cost | Text |
|------|------|------|------|

Include design rationale: why these mechanics deliver the chord.

### Crew Cards ([N] cards)
For each card: name, cost, rarity, stats, effect, flavor text. Flavor text must hit one of the five chords on first read.

### Format
Heroes: **Name — Archetype** | HP / *"flavor blurb"* / table
Minions: **Name** | Cost | Rarity | ATK/HP / *"flavor"* / Effect
Spells: **Name** | Cost | Rarity / *"flavor"* / Effect

### Constraints
[Faction-specific mechanical NOT list]
```

## Synthesis Rules

After subagents complete:

1. **Read all subagent outputs.** Identify conflicting mechanical assumptions (e.g., different Overdose models, different HP standards).
2. **Resolve conflicts.** Pick the correct model (usually: engine-aligned) and adapt all cards to it. Mark resolutions with **[PAUL RESOLVE]**.
3. **Chord distribution table.** Every card should map to at least one chord. If a card doesn't land, flag it.
4. **Archetype synthesis.** Per-hero win lines, pilot feel, player fantasy (one paragraph), closest TCG analog, skill floor/ceiling, keyword suite, counterplay.
5. **Faction overview.** Overall archetype, unique selling points, player-type map.
6. **Open items for Joe.** Flag anything the subagents disagreed on that you couldn't resolve, plus design questions needing Joe's call.

## Duster Worked Example (2026-06-06)

**Subagent split:**
- Subagent 1: Esme (The Séance) + Séance crew + Wrenches crew + archetype synthesis
- Subagent 2: Terressa (The Storm) + Touched crew
- Subagent 3: Hitch (The Ride) + Jackals crew + Vox

**Conflict resolved:** Overdose mechanic — subagent 2 treated OD as an activated ability (pay V + HP); engine uses mandatory-on-play with V-lock. Synthesis kept engine model.

**Output:** `Duster_Card_Design_Bible_Synthesis.md` — 3 heroes, 23 cards, 4 crew lanes, chord distribution map, 8 open items for Joe.
