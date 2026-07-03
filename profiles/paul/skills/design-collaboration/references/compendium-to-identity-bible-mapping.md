# Compendium → Identity Bible Mapping

**When to use:** Building a Lore Panel Zero A-H Identity Bible from an existing 20-part Faction Lore Compendium. This reference maps every compendium part onto the A-H checklist so you don't miss coverage.

**Source doc:** `FACTION_LORE_COMPENDIUM_BUILD_CHECKLIST.md` (20-part structure)
**Target doc:** `LORE_PANEL_FAST_PATH.md` (A-H checklist)

---

## Full Mapping Table

| Compendium Part | Feeds Into | Priority | Notes |
|-----------------|------------|----------|-------|
| Part 1 (Who They Are) | A1–A8 (Thesis/Identity) | **CRITICAL** | Primary source for thesis, motivation, who they are, who they are NOT, caste position, contrast anchor |
| Part 2 (Inner Circle) | D1–D5 (History/Cast) | **CRITICAL** | Characters, hero kits, legendary minions — all locked here |
| Part 3 (Named Characters) | D5 (Headline Test) | HIGH | Every legendary + named rare passes the card-title test |
| Part 4 (Founding Story) | D1–D2 (Founding Beat/Cast) | **CRITICAL** | Year + event + timeline table + founder contributions |
| Part 5 (Territory) | C1–C6 (Geography) | HIGH | Zones, neighborhoods, thematic meaning, mechanical hooks |
| Part 6 (Haunts) | C4 (Landmark Table) | MEDIUM | Locale cards + implied locations. Note: locales parked pending engine |
| Part 7 (Livelihood) | C2 (Territory→Mechanic) | HIGH | Money source → what it suggests mechanically |
| Part 8 (Internal Conflict) | D3 (Internal Rifts) | HIGH | Rifts MUST map to play styles, not just plot |
| Part 9 (Narrative Arc) | D4 (Long Arc) | HIGH | Label expansion-era beats "not v1 mechanic" |
| Part 10 (Cross-Faction) | C3 (Friction Map), A7 (Caste) | HIGH | Every other faction relationship + story hooks |
| Part 11 (Cosmology) | B3 (Villium Relationship) | HIGH | How this faction gets/uses magic; on-card limits |
| Part 12 (Mechanical Identity) | E1–E6 (Mechanical Implications) | **CRITICAL** | Keywords, blind spots, type lean, curve lean, diplomacy |
| Part 13 (Pre-Con) | F1–F4 (Play Styles) | HIGH | Archetype names, win lines, hero fantasies, overlap rule |
| Part 14 (Tutorial) | — (design-only, not identity) | LOW | Skip for bible — tutorial placement is downstream design |
| Part 15 (Visual/Audio) | B1–B4 (Body/Presence), G1–G4 (Art Direction) | **CRITICAL** | Silhouette, movement language, palette, scene grammar |
| Part 16 (Design Principles) | E1–E6 (cross-check) | HIGH | Through-line, ludonarrative test, naming pass |
| Part 17 (Deckbuilding) | F4 (Overlap Rule) | MEDIUM | Splash penalties, in-world justification |
| Part 18 (Open Items) | H1–H5 (Lock/Governance) | **CRITICAL** | Every TBD, every source conflict, every character gap flagged |
| Part 19 (Cross-References) | H5 (Vault Pointers) | MEDIUM | All docs mentioning this faction + other factions' references |
| Part 20 (Thesis Statement) | A1 (One-Line Thesis) | **CRITICAL** | Should be the first thing the reader encounters in A1 |

---

## Build Order (A → H, Not 1 → 20)

Work the A-H checklist in order. Each compendium part may feed multiple checklist items. The mapping table tells you where to find the source material — the checklist tells you what to build.

1. **A (Thesis/Identity):** Pull from Parts 1, 10, 20. The thesis from Part 20 anchors everything.
2. **B (Body/Presence):** Pull from Parts 11, 15. Art panel handoff lives here.
3. **C (Geography):** Pull from Parts 5, 6, 7, 10. Territory→mechanic bridge is the key creative work.
4. **D (History/Cast):** Pull from Parts 2, 3, 4, 8, 9. Founding beat + cast table first. Rifts must map to play styles.
5. **E (Mechanical Implications):** Pull from Parts 12, 16. No stats — keyword one-liners, blind spots, card type lean.
6. **F (Play Styles):** Pull from Parts 13, 17. Three named lanes with win lines and hero fantasies.
7. **G (Art Direction):** Pull from Part 15. **Verify against `tools/art_pipeline/profiles/` before writing.** Palette, line, scene grammar.
8. **H (Lock/Governance):** Pull from Parts 18, 19. Every open item flagged. Don't-reopen list populated.

---

## Quality Gates (Before Joe Review)

- Every A–H section has substantive content (no stubs, no "TBD" without reason)
- A4 has minimum 5 explicit negatives with reasoning
- C2 territory→mechanic bridge has minimum 4 entries
- D1 founding beat has a specific year
- D2 founding cast table lists on-card slot for each character
- D3 internal rifts map to play styles, not just plot
- E1 each signature keyword has a street-read one-liner
- E3 blind spots match A4 (mechanical can'ts = narrative can'ts)
- G1 artist profile verified against actual pipeline
- Prose reads like someone who knows the project — not retrieval boilerplate

---

## Anti-Patterns

- **Skipping the compendium read.** Must read full compendium before writing any bible section.
- **Inventing new lore.** Compendium is pre-corpus draft. Extend and synthesize; do not invent. Gaps → H2 flag.
- **Jumping to card design.** "Suggests a 4V 3/3" is the maximum. No full card designs.
- **Writing art direction without checking the actual pipeline.** `search_files` the art pipeline profiles directory before writing G1.
- **Making Henry a card.** Locked: Henry does NOT appear as a card in Founder's Edition.
