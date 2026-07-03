# Skill Consolidation Methodology

Skills bloat organically — every mistake corrected becomes a dated paragraph with quoted dialogue and emotional context. Over time, protocol gets buried under session logs. When a skill exceeds ~400 lines or has 30%+ blank lines, consolidate it.

## Process

1. **Inventory.** Extract every section header with line ranges. Record: blank line %, reference pointers, dated narratives. Identify the bloat pattern.

2. **Classify everything.** Three categories:
   - **Protocol (keep):** Design rules, methodology, behaviors — the actual skill content
   - **Session log (archive):** Dated violation narratives ("Violation 2026-06-04:"), extended quotes, flea jar stories, shelving narratives
   - **Reference pointer (one-liner):** "See references/foo.md" — these are already separate files, keep the pointer line only

3. **Archive first — never lose anything.** Save all dated narratives, violation stories, and extended quotes to a `*-archive.md` in the vault. Verify the archive contains every cut narrative before proceeding. Joe explicitly: "you know how much I hate that" (losing information). This step is non-negotiable.

4. **Write consolidated skill.** Compact prose, §-delimited where appropriate. Collapse redundant sections (e.g., the same rule explained three different ways in three different contexts). Target 65-70% reduction. Preserve hierarchy. Bump version to 2.0.0.

5. **Cross-check every principle.** Enumerate all design rules, methodologies, and behaviors from the original. Verify each one maps to the new version. This is the quality gate — if something was cut, it better be in the archive, not lost.

6. **Report reduction stats.** Lines before/after, blank line %, size reduction in chars.

## Worked Example (design-collaboration, 2026-07-02)

- Before: 893 lines, 317 blank (35%), 98,524 chars, 87 sections
- After: 260 lines, 69 blank (27%), 23,091 chars
- Reduction: 71% lines, 75,433 chars
- Archive: 24,406 chars preserved to `docs/Paul/workspace/design-collaboration-archive.md`
- All 40+ design principles cross-checked — zero knowledge lost

## File Auto-Sync (Profile Memories)

Writing to `~/.hermes/profiles/<profile>/memories/USER.md` automatically updates the `memory()` tool's user-profile entries — no separate `memory()` call needed. The tool splits §-delimited sections into individual entries. Same mechanism for `MEMORY.md` → memory target. Use this for bulk updates instead of individual `memory()` API calls.

Discovered 2026-07-02 during USER.md consolidation — writing the merged file to disk immediately reflected in the `memory()` tool's entries.
