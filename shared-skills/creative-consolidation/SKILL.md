---
name: creative-consolidation
description: Consolidate creative documents (lore, design, cards) from multiple source versions into live canon without losing flavor, nuance, or detail. The Fond Process — default KEEP, not default GATEKEEP.
---

# Creative Consolidation — The Fond Process

Consolidate multiple draft versions of creative documents into live canon without losing flavor. Built for Joe's TCG project but applicable to any creative document pipeline.

## Trigger

Use this skill when:
- Consolidating multiple Paul workspace drafts into live canon
- Reconciling versions of lore, design docs, or card rosters
- Joe says "consolidate these" or "make a pass at these documents"
- Any task where creative content is being merged and flavor must be preserved

## Core Philosophy

**Default is KEEP, not GATEKEEP.** A beat doesn't need to prove itself worthy of canon. It stays unless:
- Directly contradicted by newer Joe-locked canon
- Joe explicitly rejects it
- Byte-identical to something already in live canon

Everything else — nuance, flavor, partial overlap — gets placed. Joe calls this "the fond." Don't leave the fond in the pan.

## Joe's Authority

Joe owns the process. Process serves the work, not the other way around. If Joe says "skip it, just merge" — skip it, just merge. Never build a process that says "Joe overrides do not apply" — that's a coup, not a workflow.

## The Pass (per group of related source files)

### Phase 0: Archive First

**Before any consolidation pass touches a source file, copy it to cold storage.** The archive is the permanent backup. If workspace files get stubbed, deleted, or overwritten — the archive has the full body. No git archaeology required.

Archive path: `docs/archive/paul_workspace/[YYYY-MM-DD]/[original-filename]`

Copy every source file in the group to archive. Verify the copies. Only then proceed.

### Phase 1: Group & Inventory

Group source files by shared live target. One pass = one group. Run the pass from archive copies to guarantee source files don't get touched.

### Phase 2: Full Capture

Read every source file (READ-ONLY — never write to source files, never annotate them, never create "working copies" that modify originals). Extract every discrete beat — a fact, a paragraph, a card line, a design note, a flavor detail. Dump them all into one working document. No filtering yet.

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

Four dispositions only:

| Disposition | Meaning | Action |
|-------------|---------|--------|
| FOUND | Already in live canon | Note cite, move on |
| NEW | Not in canon, no conflict | Auto-include, mark target |
| CONFLICT | Contradicts canon or another beat | Flag for Joe |
| REDUNDANT | Superseded by later version in same group | Note which beat supersedes |

No THIN. No BAD-CITE. No HERITAGE-ACKNOWLEDGED. Keep taxonomy flat.

### Phase 4: Joe Review

Present ONLY the CONFLICT rows. NEW beats are auto-approved — Joe can reject specific ones if he wants, but the default is they land.

### Phase 5: Merge

- NEW beats → patched into live canon at target locations
- FOUND → logged, no patch
- CONFLICT → patched per Joe's decisions
- REDUNDANT → logged as superseded
- Source files stay in archive, untouched
- Working doc saved as audit trail

## Artifacts

Three artifacts per pass. That's it:
1. Working doc (`merge_plans/[group]_fond_pass_[date].md`)
2. Conflict table (inside working doc)
3. Merge log (`merge_plans/[group]_merge_log_[date].md`)

## Source File Rule — HARD

Source files are READ-ONLY. Never write to them, annotate them, or create working copies that modify originals. The untouched source file IS the backup. If a merge goes wrong, the pristine original saves you.

## Document type handling

Different source types need different extraction approaches:

| Type | Fond value | Strategy |
|------|-----------|----------|
| **Lore drafts** (Inner Circle, Identity) | High — narrative prose, character texture | Full beat extraction, diff against live canon |
| **Design docs with card lists** (Rosters, naming passes) | Medium — art stubs, flavor one-liners, design decisions | Extract flavor bank; card stats are HERITAGE if structure changed |
| **Process docs** (Craft passes, methodology) | Low — frozen sheets, Δ scores, methodology | Quick scan; if zero creative content, call it clean and move on |
| **Mixed creative** (PlanB, Red Team briefs) | High for flavor, low for mechanics | Extract crew texture, scams, day-to-day feel as standalone flavor file |
| **Red team / parallel design** (Round 006 rosters, cross-hat synthesis) | Low for lore, medium for names | Card names and design philosophy worth banking; card stats are HERITAGE if structure changed. Female set pieces, F17/F18 candidates → Card_Bank name reserve |

## Flavor banks

When source docs use a dead card/crew structure but have excellent art direction or flavor lines, extract them as a standalone **flavor bank** file rather than trying to map to specific live cards. Joe can draw from the bank when punching up card identity later. The naming convention itself may be worth preserving even if individual cards changed.

## Card name banking

When source docs are card design exercises (red team rosters, parallel design hats, naming passes), the creative fond is **card names that didn't ship**. These go to `Card_Bank.md` under a named reserve section — not to a workspace flavor file. Format:

```
## [Source] — name reserve

[Context: what these are, where they came from]

### [Category]
- **Name** — one-line role/flavor description

*Source: [archive path] (Batch X Fond Pass).*
```

This is distinct from flavor banks: flavor banks preserve art direction and prose one-liners. Card name banking preserves unused card titles with their original design intent. Both are valuable, both are "fond," but they land in different places.

## Subgroup approach

Large batches (20+ files) should be split into subgroups by document type AND live target:
- Minion Rosters (4 files) → one pass
- Craft Passes (4 files) → one pass  
- ROSTER hats (4 files) → one pass

Don't try to process 28 files in one pass. Subgroup by what the files ARE, not just where they land.

## Already-archived sources

If batch files are already in `docs/archive/workspace_merged_[date]/`, skip Phase 0 — they're already backed up. Run the pass from the archive directory directly.

## Batch kickoff — resolving batch scope

Joe often says "ready for batch X review" where X refers to a batch number discussed in a prior session. Resolution order:

1. **Check the Daily Handover's "Next session" section.** It usually names the batch and group.
2. **Check the master plan.** If the handover references a queue or plan document (e.g. "D9-D18 in DCW queue"), find the document that DEFINES the batch-to-folder mapping. For Paul's Bruiser archive, this is `docs/Paul/PAUL_ARCHIVE_DCW_RETRO_PLAN.md` — it maps Batch 1 → batch3/ folder, Batch 2 → batch2/ craft passes, Batch 3 → batch_a_tail/, etc. This is the document Joe expects you to check.
3. **If still ambiguous after both checks, ask.** Present what you found and request confirmation.

Joe's "I have no idea, homie. You got to look at the document that I had" means: you're hunting the wrong documents. The DCW queue (`paul_archive_dcw_queue.md`) lists individual files with status but doesn't define batch membership. The master plan (`PAUL_ARCHIVE_DCW_RETRO_PLAN.md`) does. When Joe says "the document I had," he means the plan/spec document, not the queue/status tracker.

Do not spend six tool calls searching through queue manifests when the answer is in the plan document. Check the plan first.

## Pitfalls

- **Don't build compliance regimes.** If the process needs 7+ artifacts and JavaScript lint tools for a solo dev, it's wrong.
- **Don't skip the fond.** A boring merge that loses flavor is worse than no merge at all.
- **Don't create annotated copies of source files.** DCW did this — it's a modified source file with extra steps.
- **Don't require all lanes on every document.** Art lane on a card stat doc is performative.
- **Source files may be stubs.** If source files have been reduced to redirects, recover original bodies from git history or Session Context copies.
- **Joe may have made deliberate changes between versions.** Flag them as CONFLICT if they weren't explicit decisions, but recognize when the live canon was intentionally rewritten.
- **Craft passes may have zero fond.** Methodology docs with frozen sheets and Δ scores are process artifacts, not creative content. Quick scan → mark clean → move on.
- **Don't archaeologize undefined batch scope — but DO check the plan document.** When Joe says "ready for batch X," check: (1) Daily Handover "Next session," (2) master plan document (`PAUL_ARCHIVE_DCW_RETRO_PLAN.md` for Bruiser archive passes), (3) only then ask. The DCW queue tracks individual file status, not batch membership. The plan document defines which folders map to which batches. Joe expects you to check the plan, not hunt through queues.
- **A mostly-FOUND pass is still a successful pass.** When source files have been promoted to live canon, reporting "20 FOUND, 3 NEW, 0 CONFLICT" is the correct outcome — not a failure to find fond. The process proves preservation, even when the answer is "already captured."
- **Don't do process theater.** The Fond Process says "read every source file, extract every discrete beat." It does NOT say "read DCW worksheet headers," "check CLOSED status fields," "verify DCW row numbers," or "note salvage-all-skip annotations." When you find yourself reading process metadata instead of source content, you're doing compliance, not consolidation. Read the files. Extract the beats. The process IS the reading — not the paperwork around the reading.
- **Don't re-archive already-archived files.** Phase 0 (Archive First) is for source files in the live workspace that could be modified. Files already in `docs/archive/workspace_merged_[date]/` are in cold storage — they're already protected. Running `cp -r` on them creates redundant copies. Run the pass from the archive directory directly.
- **Don't run ahead of Joe's position.** If Joe says "I just finished batch 5" and you processed batch 5 three hours ago and are now on batch 8 — stop. Present what you found in the batches he hasn't reached yet and sync. Do not keep charging forward into later sections while he's still working through the current queue. The Fond Process serves Joe's workflow, not the other way around.

- **Batch numbering: plan doc ≠ queue doc.** The master plan (`PAUL_ARCHIVE_DCW_RETRO_PLAN.md`) defines batches by folder (Batch 3 = batch_a_tail, Batch 4 = redteam/). The DCW queue (`paul_archive_dcw_queue.md`) defines batches by individual file (Batch 4 = D19-D27, Batch 5 = E1-E23). These are DIFFERENT numbering schemes. When Joe says "batch X," check which scheme he's using — ask if ambiguous. If he just processed batch 5 in the queue numbering, the next batch is the next queue section, not the next plan number. **Ask which numbering Joe is using rather than guessing and processing the wrong files.**

- **When you're lost, ask — don't hunt through 6 documents.** Joe said "you got to look at the document that I had." He means the master plan, not the queue tracker, not the recovery doc, not the prompt paste files. If you've checked the Daily Handover and the plan and still don't know what batch X is, ask. Six tool calls searching through queue manifests when the answer was the plan document is process theater.

- **Instructions are not suggestions.** When Joe says "go back and do B and C" after you skipped them, that means go back and do B and C. It does not mean surface-read them and call it done. It does not mean do B, C, H, and I. Execute exactly what was ordered. Autonomy means completing the work within instructions, not choosing different work. 2026-06-01: Paul was shelved for this exact failure — ignoring direct orders repeatedly across one session.

## References

- Full process doc: `docs/Paul/workspace/THE_FOND_PROCESS.md`
- Beat inventory format: see `references/beat-inventory-format.md`
- Worked example (Inner Circle — lore): see `references/worked-example-inner-circle.md`
- Worked example (Minion Rosters — design docs, flavor bank): see `references/worked-example-minion-rosters.md`
- Worked example (batch_a_tail — mostly-FOUND pass, compressed source recovery): see `references/worked-example-batch-a-tail.md`
- Worked example (redteam round-006 — card name banking, design exercise with zero lore fond): see `references/worked-example-redteam.md`
- Git recovery technique (stubbed source files): see `references/git-recovery-stubbed-sources.md`
- Worked example (A1-A4 workspace stubs — git recovery + spell moments bank): see `references/worked-example-workspace-stubs.md`
- Worked example (B+C — source documents already absorbed into live canon): see `references/worked-example-source-documents.md`
