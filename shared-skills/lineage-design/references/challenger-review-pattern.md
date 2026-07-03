# Challenger Review Pattern

How to get honest critique of identity mapping work by delegating a skeptical subagent.

## When to Use

After any identity mapping session — live or cron — when you want to know what was missed, what was rehearsed, what patterns the subject can't see.

## The Delegation

```
delegate_task(
  role="leaf",
  goal="Review the [thing] and provide a challenger's critique.
        You are a skeptical, sharp reviewer — not here to flatter.
        Find what's MISSING, what's surface-level, what's being avoided,
        and what would make the process better.",

  context="[full session file path, subject context, prior review notes if any]"
)
```

## Standard Review Questions

1. What domains are completely absent that should be covered?
2. Which answers feel rehearsed or surface-level vs. genuinely revealing?
3. Are there patterns the subject might not see himself?
4. What's the single biggest gap?
5. How should the format be adjusted to get better material?
6. What question would produce the most uncomfortable/honest answer next time?

## Post-Review

- Read the full review (may be truncated in inline summary — read from cache file)
- Present findings to Joe directly — no softening
- Fold actionable changes into the cron prompt immediately
- Save review as reference for future sessions

## Example: Session 1 Review (2026-07-01)

Subagent found:
- Absent: divorce, daughters, shame, love, mortality, current emotional life
- Rehearsed: "Hard work, being unique, accomplishments" (3 words), "Awe" (1 word)
- Patterns: defines self by what he's AGAINST, violence as boundary, self-reliance as armor
- Biggest gap: present-tense emotional life — it was an origin story, not an identity map
- Uncomfortable question: "What part of your father do you see in yourself?"

Result: Cron prompt rebuilt from 10 questions to 5, added mandatory follow-ups,
present-tense priority, discomfort requirement, story format. Session 2 quality
improved dramatically.

## Pitfalls

- Don't filter the review. If it's harsh, present it harsh. Joe prefers it.
- Don't argue with the review. Fold it in, test it, adjust if wrong.
- The subagent may lack context (e.g., recent therapy sessions making memories fresh).
  Add that context next time. Note but don't dismiss the critique.
- Always read the FULL review from the cache file — the inline summary is truncated.
