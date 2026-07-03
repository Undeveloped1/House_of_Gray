# Autonomous Creative Production with Self-Review

When Joe drops a warmup doc and says "run this autonomously" for creative work (identity bibles, lore documents, design artifacts), the correct pattern is **produce → review → revise** in a single autonomous pass. Do not hand Joe a v1 that hasn't been gutted by a hostile reader first.

## The Three-Phase Pattern

### Phase 1: Build v1

Execute the warmup doc at full depth. Read all source materials completely before writing. Produce the complete deliverable. Follow every quality gate and anti-pattern from the warmup.

### Phase 2: Spawn Hostile Reviewer

Use `delegate_task` to spawn a critical reviewer subagent. The reviewer must be HARSH — not a friendly peer review, but a hostile read designed to find everything wrong.

**Reviewer prompt template:**

```
You are a CRITICAL REVIEWER. Your job is to gut [DELIVERABLE NAME] ruthlessly and honestly. This is not a friendly review — find everything wrong, weak, thin, contradictory, or below the bar.

Read these two files:
1. [PATH TO DELIVERABLE] — the document to review
2. [PATH TO WARMUP/SPEC] — the spec with quality gates and anti-patterns

Then produce a CRITICAL REVIEW with these sections:

## Section-by-Section Weaknesses
Go through every section. For each, flag:
- What's MISSING (the spec asked for something the deliverable didn't deliver)
- What's THIN (present but insufficient depth — would a downstream user be blocked?)
- What's WRONG (contradicts source material or itself)
- What's BOILERPLATE (reads like retrieval, not like someone who knows the project)

## Quality Gate Failures
Check against the spec's quality checklist. Which items actually FAIL, not just technically-pass?

## Anti-Pattern Violations
Check against the spec's anti-patterns. Which were violated?

## Depth Comparison
Compare against the gold standard example (if one exists). Where does the deliverable fall short?

## Top 5 Fixes Required
Rank the 5 most important things that MUST be fixed before review. Be specific — cite section IDs and exact gaps.

Be harsh. If you're not sure whether something is bad, call it bad. The writer can defend it in the second pass. Err on the side of criticism.
```

### Phase 3: Build v2

Incorporate the reviewer's feedback — but this is not a checkbox exercise. The reviewer identifies symptoms; the writer diagnoses root causes. Common root causes for creative documents:

- **Boilerplate:** The document was built by filling a template rather than inhabiting the material. Fix: rewrite the opening to evoke rather than explain. Kill all self-referential meta-commentary. Add sensory texture.
- **Missing soul:** The document explains the subject but doesn't make the reader feel it. Fix: add phenomenological descriptions (what does X feel like?), character texture (one humanizing detail per named figure), sensory language (smells, sounds, light quality).
- **Contradictions:** Two sections say incompatible things. Fix: resolve definitively — don't hedge with "cross-reference when available."
- **Process leakage:** Build-process scaffolding (checkmarks, self-assessment, "this section maps to...") leaked into the deliverable. Fix: strip all of it. The document should stand on its content.

After building v2, add a changelog at the bottom documenting what changed and why.

## Deliverables

Both v1 and v2 go to:
- The vault workspace (`/root/.hermes/docs/Paul/workspace/...`)
- The syncthing dropbox (`/root/syncthing/paul-dropbox/`)
- Reader notes (if applicable) alongside the deliverable

## When to Use

- Joe drops a warmup doc with explicit autonomous instructions
- The task is a complete creative artifact (identity bible, lore document, design spec)
- Joe says "run this" or "produce the full draft" or "Joe reviews after"

## When NOT to Use

- Joe is actively collaborating in real time — use the collaborative chunk-by-chunk pattern instead
- The task is mechanical/audit (card scoring, format checking, red team pass) — those are verification tasks, not creative production
- The warmup says "draft one section at a time" — follow those instructions, not this pattern

## Proven In

- Faceless Identity Bible production (2026-06-03/06): v1 produced from warmup, hostile reviewer identified "soulless prose" as core problem, v2 rewrote opening, added sensory texture, resolved territory contradiction, stripped boilerplate, added character depth. Total: ~5 hours autonomous production.
