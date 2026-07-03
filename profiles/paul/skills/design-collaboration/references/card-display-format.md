# Card Display Format — Joe's Preference

**Locked 2026-05-29. Updated 2026-05-30, 2026-06-05 (tier at end).** Joe reinforced 2026-06-05: "I really don't like the tabling format." Card numbers are optional — Joe doesn't care about them ("if it matters for you, because then you can keep better track of it, then great"). He cares about R, V, Name, Text, and faction/tier.

## Format (2026-06-05)

Plain text monospaced in a fenced code block. NO markdown pipes. Fixed-width columns, organized by card band (Villium cost) and rarity within each band. **Tier/card number go at the END.**

```
R V  Name             Stats  Text                                                 [Tier] [#N]

C 2  Devereaux        1/2    Battlecry: Scry 2. If you reveal a Contract, draw   [Management] [#1]
                              it. Villium 1V: Scry 1.

C 2  Switchboard Op   2/1    Battlecry: Mark target enemy minion.                 [Management] [#2]
                              Villium 1V: Scry 1.
```

## Rules

- **Column order:** R · V · Name · Stats · Text · [Tier] [#N]
- **Tier/faction at END:** The faction tier (Management, Hitters, Street, Help) or crew (Dock, Street, Hall, Spread) and optional card number go at the END of the line — not in the middle. These are filing notes, not gameplay columns. What you need at the table comes first: rarity, cost, name, stats, text.
- **Card numbers OPTIONAL:** Joe doesn't care about them. Use only if they help tracking.
- **R before V:** rarity column comes BEFORE Villium cost.
- **Organize by band, then rarity within band.** Group cards by Villium cost (1V section, 2V section, etc.). Within each band, list by rarity (C → U → R → L).
- **Vanillas:** leave Text column BLANK.
- Monospaced alignment — spaces, not tabs.
- One card per line.
- Multi-line text: indent continuation lines to align with text start.

## When to use

- Roster reviews
- "Show me the full list"
- Lock pass confirmations
- Any time Joe wants to scan cards quickly

## Anti-patterns

- **Pipe-delimited markdown tables of ANY kind** — Joe explicitly hates this ("I really don't like the tabling format").
- **Comparison tables with pipe columns** — write comparison PROSE, not comparison tables.
- **Tier/crew in the middle of the row** — it's filing, not gameplay. Goes at the end.
- Filling Text with "(vanilla)" or "—" for vanillas — leave it blank.
- Organizing cards in non-band order — band (V cost) grouping is mandatory.
