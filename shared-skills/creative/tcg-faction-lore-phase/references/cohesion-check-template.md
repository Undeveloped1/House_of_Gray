# Cohesion Check — Reader Notes Template

**Purpose:** Gate between Lore Pass and Card Design. Compare new design work against all existing canon documents. This is a full-document reader pass — not a quick glance.

## Methodology

1. Read the design document being checked (lore pass OR card design bible)
2. Read ALL existing faction canon docs: `Identity.md`, `Inner_Circle.md`, `Playstyle.md`, `Territory.md`, `{Faction}_Cards.md`, `00_INDEX.md`
3. Read relevant core docs: `core/03_Villium/04_Geography_Salt_Mine.md` (character timelines), `core/05_Commission.md` (faction relationship sections)
4. Check across the following categories, using ✅/⚠️/❌ markers
5. Verify all Joe-locked decisions (from DCW merge or prior gates) are preserved
6. Output to syncthing dropbox as `{Faction}_{Document}_Cohesion_Check_Paul.md`

## Categories

### Voice
Does the tone match the lore? Are the emotional chords coming through in card text / flavor blurbs / hero voice lines? Flag tonal mismatches.

### History — Factual Accuracy
Canon contradictions. Check: character knowledge states, timeline dates, location references, death/alive status, who knows what. Every factual claim in the design document must match the canon docs.

### Cast
Character name quality, relationship clarity, identity consistency. Does each character's card/flavor match their Inner_Circle.md or lore description? Are relationships correct? Any character referred to with a relationship they don't canonically have?

### Mechanics
Does the playstyle / keyword usage match established constraints? Check: No Taunt, no healing, OD model (mandatory vs optional), Blur faction-exclusivity, Bends trigger threshold, body stat ranges per track (Sight vs Road), weapon limitations.

### Territory
Do location references match Territory.md? Any geography contradictions?

### Cross-Faction
Do faction relationship claims match established dynamics? Any incorrect or outdated cross-faction references?

### Don't Reopen
Verify every Joe-locked decision (C-01 through C-XX from DCW merge, O-XX locks from prior gates) is preserved. This section is a checklist — each lock gets a row with status.

### Open Questions
Factual ambiguities or edge cases the design document introduces. For Joe batch only.

## Example (Duster Card Design Bible, 2026-06-06)

Sections from the worked example:

```
### History — Factual Accuracy

**Passes scrutiny:**
- Esme knows Henry is her father — will packet confirmed (Inner_Circle.md). ✅

**Factual issues found:**
- None. Zero canon contradictions across 23 cards and 3 heroes. ✅

### Mechanics

**❌ CRITICAL FINDING: Mary Lou Denton and James Cash missing Overdose keyword.**
The synthesis table dropped OD from both legendaries, making Bends mechanically unreachable.
Fix: Restore Overdose 1 with base effects, aligned to engine model.

### Don't Reopen

| Lock | Status |
|------|--------|
| C-01: Land claim honored | ✅ |
| C-02: Esme's wound = absent father | ✅ |
| C-07: Terressa = woman | ✅ |
```

## Pitfalls

- **Don't mistake "no errors found" for "the check is done."** The check is a full document. Zero errors is a result, not an excuse to skip the output document.
- **Pay special attention to synthesis documents.** When subagent outputs are merged, mechanical errors can be introduced during reconciliation (e.g., keyword removal, stat drift). The cohesion check is the safety net.
- **Flag open questions explicitly.** Don't bury edge cases in prose. Joe needs to see them as a numbered list.
