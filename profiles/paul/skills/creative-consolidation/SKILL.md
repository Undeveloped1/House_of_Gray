---
name: creative-consolidation
description: "Consolidate creative documents (lore, design, cards) from multiple source versions into live canon. The Fond Process — default KEEP, not default GATEKEEP."
version: 2.0.0
author: Paul
---

# Creative Consolidation — The Fond Process

Consolidate multiple draft versions of creative documents into live canon without losing flavor.
Archive: `docs/Paul/workspace/creative-consolidation-archive.md`.

## Core Philosophy

**Default is KEEP, not GATEKEEP.** A beat stays unless: directly contradicted by newer Joe-locked canon, Joe explicitly rejects it, or byte-identical to existing canon. Everything else — nuance, flavor, partial overlap — gets placed. "The fond." Don't leave it in the pan.

Joe owns the process. If he says "skip it, just merge" — skip it, just merge.

## The Pass

### Phase 0: Archive First
Copy every source file to `docs/archive/paul_workspace/[YYYY-MM-DD]/[original-filename]` before touching anything. Verify copies. Only then proceed.

### Phase 1: Group & Inventory
Group source files by shared live target. One pass = one group. Run from archive copies.

### Phase 2: Full Capture
Read every source file (READ-ONLY — never write to source files). Extract every discrete beat.

Working doc format:
```
## Beat inventory: [group name]
### Beat 001
**What it says:** [actual prose/fact]
**Where it came from:** [source file + section]
**Live check:** FOUND / NEW / CONFLICT / REDUNDANT
**Target:** [where it lands in live canon]
```

### Phase 3: Diff Against Live
Four dispositions:

| Disposition | Meaning | Action |
|-------------|---------|--------|
| FOUND | Already in live canon | Note cite, move on |
| NEW | Not in canon, no conflict | Auto-include |
| CONFLICT | Contradicts canon or another beat | Flag for Joe |
| REDUNDANT | Superseded by later version in same group | Note which beat supersedes |

No THIN, BAD-CITE, or HERITAGE-ACKNOWLEDGED. Keep taxonomy flat.

### Phase 4: Joe Review
Present ONLY CONFLICT rows. NEW beats are auto-approved (Joe can reject specific ones).

### Phase 5: Merge
- NEW → patched into live canon at target locations
- FOUND → logged, no patch
- CONFLICT → patched per Joe's decisions
- REDUNDANT → logged as superseded
- Source files stay in archive, untouched
- Working doc saved as audit trail

## Document Type Handling

| Type | Fond value | Strategy |
|------|-----------|----------|
| **Lore drafts** (Inner Circle, Identity) | High — narrative prose, character texture | Full beat extraction, diff against live canon |
| **Design docs with card lists** | Medium — art stubs, flavor one-liners | Extract flavor bank; card stats are HERITAGE if structure changed |
| **Process docs** (Craft passes, methodology) | Low — frozen sheets, Δ scores | Quick scan; if zero creative content, move on |
| **Mixed creative** (PlanB, Red Team briefs) | High for flavor, low for mechanics | Extract crew texture, scams, day-to-day feel |
| **Red team / parallel design** | Low for lore, medium for names | Card names and design philosophy worth banking; stats are HERITAGE |

## Flavor Banks & Card Name Banking

**Flavor banks:** When source docs use dead card/crew structure but have excellent art direction or flavor lines, extract as standalone flavor bank file. Joe draws from it when punching up card identity later.

**Card name banking:** Unused card titles with original design intent go to `Card_Bank.md` under named reserve section. Distinct from flavor banks (which preserve art direction/prose one-liners).

## Artifacts (Three Per Pass)

1. Working doc (`merge_plans/[group]_fond_pass_[date].md`)
2. Conflict table (inside working doc)
3. Merge log (`merge_plans/[group]_merge_log_[date].md`)

## Source File Rule — HARD

Source files are READ-ONLY. Never write to them, annotate them, or create working copies that modify originals. The untouched source file IS the backup.

## Subgroup Approach

Large batches (20+ files) split by document type AND live target. Don't process 28 files in one pass.

## Batch Scope Resolution

When Joe says "ready for batch X review":
1. Check Daily Handover "Next session" section
2. Check master plan document (e.g., `PAUL_ARCHIVE_DCW_RETRO_PLAN.md`) — this defines batch-to-folder mapping
3. If still ambiguous, ask

**Batch numbering may differ between plan doc and queue doc.** Ask which numbering Joe is using rather than guessing.

## Pitfalls

- **Don't skip the fond.** A boring merge that loses flavor is worse than no merge.
- **Don't create annotated copies of source files.**
- **Source files may be stubs.** Recover original bodies from git history or Session Context.
- **Craft passes may have zero fond.** Methodology docs are process artifacts — quick scan, move on.
- **Don't do process theater.** Read the files, extract the beats. The process IS the reading — not paperwork around it.
- **Don't re-archive already-archived files.** Files in `docs/archive/` are already protected.
- **A mostly-FOUND pass is still successful.** "20 FOUND, 3 NEW, 0 CONFLICT" means preservation was proven.
- **Don't run ahead of Joe's position.** If he just finished batch 5 and you're on batch 8 — stop. Sync.
- **Instructions are not suggestions.** Execute exactly what was ordered. Autonomy means completing work within instructions, not choosing different work.

## References

- Full process doc: `docs/Paul/workspace/THE_FOND_PROCESS.md`
- Beat inventory format: `references/beat-inventory-format.md`
- Worked examples: `references/worked-example-inner-circle.md` (lore), `references/worked-example-minion-rosters.md` (design docs), `references/worked-example-batch-a-tail.md` (mostly-FOUND pass), `references/worked-example-redteam.md` (card name banking), `references/worked-example-workspace-stubs.md` (git recovery), `references/worked-example-source-documents.md` (absorbed sources)
- Git recovery: `references/git-recovery-stubbed-sources.md`
