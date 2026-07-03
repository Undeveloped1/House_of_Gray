# Worked Example — Minion Rosters Fond Pass (2026-06-01)

**Group:** Minion Rosters — MERGED, PlanB, Rev007, Rev007b
**Targets:** `Bruiser_Cards.md`, flavor bank
**Outcome:** 2 files extracted, 0 beats patched to live canon

---

## What we found

### PlanB (595 lines) — Full alternate design fork

PlanB rebuilt Bruiser around a 4-crew structure (Dock/Yard, Hall, Street, The Spread) with experimental keywords. The card mechanics were dead (superseded by live canon), but the **crew texture** sections were exceptional:

- **Dock/Yard scams:** Ghost freight, spillage, the holding fee, Villium priority, the short route (Russo skims 20%, daughter's in college)
- **Hall day-to-day:** Marge's desk, Vic's dinner circuit, ghost workers, dues skimming, the no-strike guarantee
- **Street:** Gym at 5:30am, Tuesday/Friday collections, fight night at the Armory, Leg Breaker's hammer
- **The Spread:** Three-tier vice (social club / restaurant / Club Midtown), the whisper network, "Vic drinks at all three. He's the only one who moves between them without changing who he is."

Extracted to: `docs/Paul/workspace/bruiser_lore/Bruiser_Crew_Texture_PlanB_extract.md` (34KB)

### Rev007b (118 lines) — Full naming pass

One-syllable names + art direction stubs + flavor one-liners. 13 killer lines:

> "Door don't check IDs. Door checks if you can fly."
> "When you're a hammer, everything's a nail."
> "Silk's touch is soft. Silk's needle is not."
> "Grudge remembers that thing you did in '57."
> "Crow opens things. Cars, safes, people."

Extracted to: `docs/Paul/workspace/bruiser_lore/Minion_Rosters_Fond_Pass_2026-06-01.md`

### MERGED and Rev007 — Heritage

MERGED (193 lines) was the Round 006 parent merge. Rev007 was a revision pass. Both used the old 10-crew structure. Card stats superseded by live canon. No beats to extract.

---

## Key lessons

1. **Design docs need different handling.** PlanB had dead mechanics but living flavor — extract the flavor as a standalone file rather than trying to map beats to live cards.
2. **Flavor banks work.** When card structures changed between versions, a "flavor bank" file lets Joe draw from the best lines later without forcing a mapping to current cards.
3. **Check git for full bodies.** The workspace files were stubs. Full content was in `docs/archive/workspace_merged_2026-05-30/batch2/`.
4. **Subgroup by document type.** Group Minion Rosters together, Craft Passes together, etc. — not all 28 batch2 files in one pass.
