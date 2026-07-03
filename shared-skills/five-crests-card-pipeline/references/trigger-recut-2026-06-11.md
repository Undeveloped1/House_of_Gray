# Trigger Recut — 2026-06-11 Cascade Failure & Fix Protocol

**Context:** Trigger Build Facts v1 was written 2026-06-06 on an aggro-midrange concept. Five days and four design pivots later, the faction was midrange-tempo-control. The entire Phase 2-3 pipeline stack was built on stale numbers. This is the worked example.

## The Cascade

1. **Build Facts v1 (2026-06-06):** 5-6 at 1V curve, 70/30 crew split, density targets derived from aggro-midrange assumptions. "Locked On" terminology (later changed to "Overkill").
2. **Pathway Design v1 (2026-06-11):** Slot table built from Build Facts v1 curve targets. 7 cards at 1V (target 5-6). Crew split 62/38 vs the 60/40 Joe had locked.
3. **Spec Validation (2026-06-11):** Checked slot table against Build Facts v1 density targets. Found gaps (Paid at 5 vs 8-12, Armed at 2 vs 4-6). Fixed in slot table — but density targets themselves were from the wrong archetype.
4. **Warmup (2026-06-11):** Referenced Build Facts v1 as a locked spec.

**Root cause:** Circular validation. Spec validator checked slot table → density targets. Density targets were derived from Build Facts v1. Build Facts v1 was five days stale. The validator passed the slot table because it was checking against numbers from a different design era — it had no way to detect that the frame itself was wrong.

## Joe's Signals

- "Where are you pulling this curve from?" — couldn't trace the number to its source
- "Where the fuck are those density targets from?" — targets inherited from stale assumptions
- "Why are we even using the build facts doc, what does it have that the other docs don't?" — Build Facts was vestigial
- "Fix the whole fucking thing" — full rebuild required

## Fix Protocol (what we did)

1. **Joe specified the correct curve:** 3-8-8-5-4-2 minions (midrange-tempo-control, not aggro-midrange). Do not derive curves from templates — ask the human.
2. **Killed Build Facts:** Curve, rarity, crew split, density targets, CAN/CANNOT — all duplicated in slot table, warmup, and SubAgent Spec. Its two unique pieces (matchup spread, curve philosophy blurbs) were absorbed into warmup and pathway design.
3. **Rewrote Pathway Design as v2:** Full slot table recut to new curve. 30 minions at 3-8-8-5-4-2. 20 spells, 5 weapons. 60/40 crew split. Density targets re-derived from new curve.
4. **Patched warmup:** Removed all Build Facts references. Updated slot table reference to v2. Added matchup spread.

## Process Patches Applied

- **Phase 1.5 Build Facts Currency Check** — mandatory gate before Phase 2. Checks date, curve, crew split against current design identity.
- **"Kill vestigial docs" rule** — if a pipeline phase doc carries no unique information, merge what's unique and delete it.
- **"Trace numbers to their source" pitfall** — when asked where a number comes from, answer with the document and date. If you can't, you don't know the number.
- **Joe-specified curves** — don't derive curve targets from templates or prior factions. Lock the archetype, then ask Joe for the curve.

## Docs Created

- `Trigger_Build_Facts_v2_2026-06-11_Paul.md` — written then killed. Superseded by warmup + pathway design.
- `Trigger_Pathway_Design_v2_2026-06-11_Paul.md` — active. The slot table + density targets. Replaces v1.
- `Trigger_Card_Design_Warmup_2026-06-11_Paul.md` — patched. No longer references Build Facts.
