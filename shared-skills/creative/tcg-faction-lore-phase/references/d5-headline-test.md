# D5 — Headline Test Methodology

**Lore Panel Zero D5:** Verify every named character works as a card title. Pass/fail with notes.

## Criteria

A card title passes if:
- **Memorable** — you'd remember pulling it from a pack
- **Flavor-fit** — sounds like it belongs in this faction, this world
- **Distinct** — doesn't blur with another faction's naming conventions
- **Evocative** — implies something about the character before you read the card text

## Process

1. Extract every named character from the faction bible (all tiers, all support roles)
2. Include intentionally-unnamed role-based characters (Handyman, Wireman) — their role IS the card title
3. Test each against the four criteria above
4. Flag (not fail) names that have minor issues (too generic, single name too light for Rare function, nickname without real name)
5. Document the faction's naming convention pattern — what patterns hold across tiers?

## Flag Categories

| Flag Type | Example | Recommendation |
|-----------|---------|----------------|
| **Single name too light for rare** | "Etta" for a Rare function | Add surname for gravitas |
| **First name too soft** | "Bernie" for a card title | Keep if Uncommon; revisit if bumped to Rare |
| **Too generic** | "James" for concierge | Confirm: intentional invisibility or needs distinction? |
| **Nickname without real name** | "Doc" as only identity | Decide: is the nickname the full card identity or does he get a real name? |

## Output Format

```
| Name | Verdict | Notes |
|------|---------|-------|
| **Character Name** | ✓ PASS | Why it works |
| **Character Name** | ⚠️ PASS (FLAG) | What the minor issue is |
```

Summary table by tier, overall pass/fail count, flag recommendations, design observation on naming convention patterns.

## Naming Convention Patterns

Look for tier-correlated patterns that reinforce faction identity:

- **Management:** Professional surnames or evocative titles (Gerald, The Ledger)
- **Elite/aristocratic tier:** Full names with nicknames, foreign titles (Sidney "Vicious" Lark, Count Aksel Falk)
- **Core operators:** Grounded full names + occupational handles (Carlo Abruzzo, Big Iron)
- **Street/low-tier:** Nickname-anchored working-class names (Tony "Toothless" DeMarco)
- **Support:** Single names or descriptive titles (Mick, The Artist)

If the pattern holds across the faction, note it. If there's bleed (a Street name sounds like Management), flag it.
