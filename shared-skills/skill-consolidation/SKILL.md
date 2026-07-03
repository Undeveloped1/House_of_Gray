---
name: skill-consolidation
description: "Use when consolidating bloated skills. Audit → classify → archive → condense → verify. Proven across 12 skills (60% total reduction) without knowledge loss."
version: 1.0.0
author: Paul
---

# Skill Consolidation

Systematic workflow for condensing skills that have grown bloated through organic accumulation — dated narratives, session logs disguised as protocol, duplicate pitfalls, excessive whitespace.

**When:** Skills have 30%+ blank lines, dated violation narratives ("Trigger 2026-06-13 worked example..."), duplicate content, or 70+ sections. Any skill growing past 500+ lines is a candidate.

## The Pattern

For each skill: audit → classify → archive → condense → verify. Never lose knowledge.

### Step 1: Audit
Read the full skill with `skill_view(name)`. Count lines, identify blank line %, note section headers. Classify bloat signals:
- Dated narratives ("2026-06-13 worked example: Joe said...")
- Duplicate sections (same heading appearing twice)
- Session logs passing as protocol
- 30%+ blank lines

### Step 2: Classify
Tag every piece of content:

| Tag | Meaning | Action |
|-----|---------|--------|
| **KEEP** | Core protocol, process, or principle | Condense to compact prose |
| **ARCHIVE** | Dated narratives, violation histories, extended quotes | Save to archive, cut from skill |
| **POINTER** | Reference to another doc or file | One-liner |
| **CUT** | Duplicate or no-op prose | Delete |

### Step 3: Archive
**BEFORE touching the skill**, copy the full original to archive:
`docs/Paul/workspace/{skill-name}-archive.md`

Everything cut goes to the archive. Joe's rule: "you know how much I hate losing knowledge." The archive is permanent recovery. Verify the copy exists before writing.

### Step 4: Condense
Write consolidated version. Target format:

```yaml
---
name: skill-name
description: "One-sentence trigger + behavior."
version: 2.0.0
author: Paul
---

# Title

One-line archive pointer: `docs/Paul/workspace/{name}-archive.md`.

## Core sections (compact prose, tables where efficient)
## Pitfalls (compact bullets, no dated narratives)
## References (one-liners to external docs)
```

Rules:
- **No dated violation narratives.** Principles only. "Proposing a card without understanding the mechanic" — not "Trigger 2026-06-13: Paul proposed Vera..."
- **Blank lines under 30%.** Every header earns its place.
- **Tables where efficient.** Slot formats, checklists, crew profiles.
- **Bullet lists for pitfalls.** One line per pitfall: symptom → fix.
- **Version bump to 2.0.0.** Consolidated skills start at 2.0.0.

### Step 5: Verify
Cross-check every protocol/principle from original is preserved. Count lines before/after. Report % cut.

## Target Sizes

| Skill Tier | Target Lines |
|------------|-------------|
| Core operational (paul-joe-process, design-collaboration) | 200-260 |
| Phase-specific (faction-identity-gate, pathway-design) | 100-170 |
| Support tools (spec-validator, multi-perspective-review) | 80-120 |

## Write Destination

Consolidated skills go to the **profile** skill directory:
`/root/.hermes/profiles/paul/skills/{name}/SKILL.md`

NOT the global `/root/.hermes/skills/`. The global directory holds originals; profile directory takes precedence at runtime. `skill_view` loads from global but profile skills are what the agent actually runs.

## Cross-Session Handoff — Warmup Doc Format

When splitting consolidation across sessions, write a warmup doc at `docs/Paul/workspace/consolidation-warmup-{tier}.md`:

```
# Consolidation Warmup — Tier N

## What We're Doing
[one-paragraph context]

## What's Already Done
[before/after table with line counts, archive paths]

## Your Job
[numbered list of skills with current line counts and paths]

## The Pattern (per skill)
[numbered steps — the same pattern every time]

## Rules
- NEVER lose knowledge. Everything cut goes to archive.
- Not all skills have bloat. Audit honestly.
- Read finished Tier N-1 skills to match format.
- Priority order specified.

## Reference
[all paths: consolidated skills, archives, workspace]
```

The warmup is the bridge between sessions. A new instance should know exactly what to do from the warmup alone.

## Pitfalls

- **Archiving after writing.** Always archive the full original FIRST. If you write the condensed version and realize you missed something, the original is gone.
- **Forcing consolidation on tight skills.** `faction-set-review` at 143 lines was already tight — don't force cuts. Audit honestly.
- **Losing behavioral anchors.** `faction-identity-gate` scoring tables with behavioral anchors ARE the protocol. Those tables stay even if they're long.
- **Writing to wrong directory.** Profile skills go to `/root/.hermes/profiles/paul/skills/`, not `/root/.hermes/skills/`.
- **Skipping the warmup doc.** Autonomous sessions need the warmup. Without it, the new instance has no inventory of what's done vs what's next.
- **Dry consolidation (zero bloat identified).** If a skill is already tight, report "audited — no bloat found" and move on. Don't cut for cutting's sake.
