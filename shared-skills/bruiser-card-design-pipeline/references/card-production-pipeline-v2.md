# Card Production Pipeline v2

**Status:** CANON — corrected by Joe 2026-06-05
**Replaces:** CARD_PRODUCTION_PIPELINE.md (v1 — corrupted by ~8500 merged documents in the tcg-engine corpus)

## The Pipeline

```
1. Lore                 Who are they? Where? What would they never do?
       ↓
2. Crews                From the lore — who works where, role pools, mechanical signatures
       ↓
3. Archetypes           From the crews — what kind of decks does this faction build?
       ↓
4. Playstyle Matrix     Win lines, hero HP, precons, core pool — based on archetypes
       ↓
5. Functions            From the archetypes — what does the set need to DO? (12-18 functions)
       ↓
6. Mechanics            From the functions — keywords, mechanical boundaries, NOT list
       ↓
7. Synergy Webs         From the mechanics — A enables B, C answers D
       ↓
8. Build Facts / Curve  From the archetypes — how many cards, rarities, V-curve, power curve, tone
       ↓                       (Cascade tools live here — validate allocation before filling slots)
9. Expressions           Role + stats + text. Names come LAST.
       ↓
10. Quality Gates        FERM + guardrails + red team + Joe batch → Final doc lock → Pass 6 JSON
```

## Key Principles

- Each step daisy-chains into the next. You can't determine functions without archetypes. You can't determine mechanics without functions. You can't determine synergy webs without mechanics.
- Living World Method is woven throughout — not a separate step. Every card is a person, place, moment, or action in 1960s Detroit.
- Do not open the card table until step 8. Skeleton rows are expressions of functions, not a quota to fill.
- Archetypes inform everything downstream — curve shape, power band, rarity distribution, tone.
- Build facts live at step 8 — after you know what the set DOES but before you fill slots.

## Changelog

**2026-06-05** — Created from Joe's direction. Replaces the corrupted v1 pipeline assembled from ~8500 merged documents.
