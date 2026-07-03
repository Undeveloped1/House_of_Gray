---
name: process-documentation
description: Build SOPs, workflow documents, and procedural guides from user dictation or description. Iterative refinement with gap flagging — never guess, always confirm.
category: productivity
---

# Process Documentation

## When to Use

When the user describes a multi-step process they want documented — shipping workflows, operational procedures, onboarding checklists, any repeatable business process. The source material can be voice dictation, chat messages, or screen-share narration.

## Core Workflow

### 1. Restate Before Building
Before writing a single line of the document, restate what you heard. "You want X documented — the steps are A → B → C. Is that right?" This catches misunderstandings before they're baked into the document structure.

### 2. Build v1 With Flagged Gaps
Write the first draft with:
- Clear phase/section breaks
- Numbered steps where the order matters
- **Explicit open items** at the bottom for anything ambiguous
- A changelog section from the start

Never guess what the user meant. If a step is unclear, write a placeholder and flag it. "Create Workflow Template — is this a macro, a menu item, or a button?" is better than guessing wrong and embedding a mistake.

### 3. Iterative Patching
When the user fills a gap or adds detail, use `patch()` — don't rewrite the entire file. Surgical edits keep the changelog meaningful and prevent drift. Each patch should:
- Replace only the section being updated
- Update the changelog with what changed
- Remove resolved open items

### 4. Critical Warnings
Process documents often have "if you do this wrong, it costs money/breaks things" moments. Call these out prominently with ⚠️ and concrete consequences: "Uneven boxes = $300+ placement fee" hits harder than "Ensure even distribution."

### 5. Keep Open Items Visible
Don't bury gaps. A dedicated "Open Items" section at the bottom of the doc makes it obvious what's still needed. Remove items as they're resolved. The document should be usable even with open items — someone should be able to follow 80% of the process while waiting for the last 20%.

## Document Structure

```markdown
# [Process Name] — Standard Operating Procedure

**Date:** YYYY-MM-DD
**Status:** Draft v1 — pending review
**Purpose:** One-sentence description

---

## Phase 1: [Name]
### 1.1 [Step]
### 1.2 [Step]

---

## Phase 2: [Name]
...

---

## Reference: Key Locations
| Resource | Where |
|----------|-------|

---

## Open Items
1. Unresolved questions

---

## Changelog
| Date | Note |
|------|------|
```

## Pitfalls

- **Don't guess.** If the user's voice dictation is garbled or ambiguous on a step, flag it. Wrong documentation is worse than incomplete documentation.
- **Don't assume context.** "The Operations Worksheet" means something specific to the user — ask where it lives, don't assume it's a Seller Central report.
- **Don't over-structure too early.** Wait until the full process is described before finalizing the phase/section breakdown. The user may reveal mid-flow that steps you thought were separate are actually the same phase.
- **Keep the changelog.** Multiple iterations across voice messages can get confusing. The changelog is the audit trail.

## Voice Dictation Specifics

When source material is voice messages:
- Restate what you heard after each chunk — voice-to-text is lossy
- "Commintory" might be "Inventory." Use context to disambiguate, but confirm if unsure.
- Build incrementally. Don't wait for the full process to be described before writing — capture each phase as it comes.

For Paul/Joe-specific Amazon FBA conventions (output paths, voice-note patterns, Amazon-specific warnings), see `references/paul-amazon-sop-conventions.md`.
