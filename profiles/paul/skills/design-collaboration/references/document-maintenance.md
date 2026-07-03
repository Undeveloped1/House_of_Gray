# Design Document Maintenance

How to maintain and update living working documents during TCG design sessions.

## Core Rule

Whenever the user gives direction, suggestions, or approval on content that belongs in a working document, **explicitly update the document** and confirm by showing the update (or stating the file path and what was added).

## When to Update

- After any non-trivial addition of roles, crews, philosophy, constraints, or naming conventions.
- After the user approves or refines a list of ideas.
- When new categories (e.g. adjacent businesses, female/non-traditional roles, hangarounds) are defined.

**Alternative: DREAM: design markers.** For changes that should be staged rather than written immediately (direction still evolving, user hasn't explicitly approved), use `DREAM: design: <doc> § <section> | <proposed change>` in the Daily Handover instead of writing directly. These are batch-processed at compression points. See `memory-management` skill for the full DREAM: processing workflow.

## How to Confirm

- Use `write_file` or `patch` to update the target document.
- Explicitly state: which document was updated, what section was added/modified, that the info is now saved.

## Protected Documents

- `Bruiser_Criminal_Crews_Working_Doc.md` — primary living design document for Bruiser crews.
- `Bruiser_Design_Brief_v1.md` — polished reference version for handoff.

## Document Discovery at Session Start

When Joe asks to pull/resume documentation:

1. **Filesystem search first** — search the project repo, bridge directories, and Obsidian vault.
2. **Cross-reference the Daily Handover** — many files live in Session Context, bridge subdirectories, or under unexpected names.
3. **Session Search for critical path** — if the Daily Handover mentions an ongoing review or blocker.
4. **Present the complete map** — authority docs, design system docs, faction-specific docs — before Joe has to ask.

### Pitfalls

- Never leave the user wondering whether information was captured.
- Do not wait until end of session to batch updates.
- **Do not write monster patches.** Apply changes chunk by chunk — one section or one crew at a time. Joe prefers incremental updates. If a replacement string exceeds ~30 lines, break it.
- **Do not rely on filesystem search alone.** The Daily Handover often references files in Session Context or bridge subdirectories.

## Cursor Sync Overwrite Prevention

When Joe runs "Pull Paul design" / `hermes-bridge.ps1 pull-design`, Cursor's repo versions sync INTO the vault — overwriting vault content.

**Prevention:**
- Before telling Joe to trigger a sync, save Session Context copies of all docs.
- After a sync, verify vault doc sizes haven't regressed.
- When overwrite is detected, rebuild from Session Context backup + Cursor's additions.

**Workflow when overwrite occurs:**
1. Read the repo version to identify what Cursor added.
2. Fold additions back into the fuller vault version.
3. Update Session Context with the merged result.
4. Tell Joe to re-sync.

## Document Status Lifecycle (Canonical Consolidation)

When one document becomes the single source of truth:

### Status markers

| Marker | Meaning | When to apply |
|--------|---------|---------------|
| **CANONICAL MASTER** | Single source of truth. Edit here only. | The doc with all locked decisions. |
| **SYNCED COPY** | Do not edit. Sync from canonical. | Duplicate for accessibility. |
| **HISTORICAL** | Reference only. Do not edit. | Superseded versions. |
| **ACTIVE** | Still authoritative for a specific domain. | Authority trail docs. |
| **POINTER** | Redirects to canonical. | Files that exist so old links don't break. |

### Consolidation steps

1. Identify the master — most complete, up-to-date version.
2. Update master header with "(CANONICAL MASTER)" + last-updated date + authority docs.
3. Mark synced copy with pointer to canonical.
4. Mark superseded docs as HISTORICAL — add pointer to canonical, add "Do not edit."
5. Leave authority docs (JOE_DECISIONS_*.md) as ACTIVE.
6. Sync the bridge copy: `cp <canonical> <bridge/paul_design/copy>`.
7. Do NOT delete anything. Do NOT update historical docs' content — only their status headers.
8. Verify archive copies exist in `Brain/Session Context/`.

### Document map pattern

Present every doc with status marker and full relative path from repo root. Group by status: CANONICAL → SYNCED → ACTIVE → HISTORICAL.
