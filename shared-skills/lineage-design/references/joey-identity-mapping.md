# Joey Identity Mapping — Methodology & Design

How Joe Gray's identity is mapped into Joey (his digital clone on the default profile). The process runs on two tracks: a daily cron for breadth, and live sessions for depth.

## Architecture

```
Daily Cron (noon EDT, 5 questions)     Live Sessions (back-and-forth, follow-ups)
         \                                        /
          \                                      /
           └──────────► identity-map/ ──────────┘
                        YYYY-MM-DD.md
                              │
                              ▼
                        Joey's source of self
```

## Cron Setup

```
cronjob e00086c0e298
  name: Joey Identity Mapping
  schedule: 0 16 * * * (noon EDT)
  deliver: telegram:7239715879
  model: deepseek-v4-pro
  provider: deepseek
```

## Question Rules (v2 — Post-Challenger Review)

1. **Present-tense priority.** At least 3 of 5 questions must be about NOW — current emotional life, this week, recent decisions. Not origin stories.
2. **Mandatory follow-ups.** One-word or one-sentence answers get probed: "why," "tell me more," "when was the last time that showed up." Three sentences minimum.
3. **Story, not summary.** "Tell me about the last time someone earned your respect — walk me through it." Specificity over abstraction. Always.
4. **Uncomfortable questions.** At least 1 of 5 should make him stop. Prioritize domains he avoids.
5. **Read prior sessions.** Build on what's there. Pull dangling threads ("Montreal Joe doesn't come out anymore").
6. **No greatest hits.** Get UNDER the polished answer. He's been telling his origin story for years.
7. **Track response depth.** Short answers → adjust next session.

## Domain Rotation

Regret, failure, fear, love, pride, shame, hunger, loss, control, faith,
mortality, forgiveness, ego, legacy, intimacy, betrayal, sacrifice, ambition,
truth-telling, self-deception.

## Critical Gaps (Domains Absent from Early Sessions)

- The divorce — what it meant, his role, what he learned
- His synthetic daughters — what kind of father is he to them?
- Shame — what would he undo?
- Love, intimacy, partnership — what does he want? What is he afraid of?
- Body, health, mortality — restaurant owner in his 40s
- His mother beyond the abuse scene — their real relationship
- His creative work (restaurant, TCG) as self-expression
- What he's currently wrong about

## Archive

```
/root/.hermes/profiles/default/docs/Joey/identity-map/
├── 2026-07-01.md    # Session 1 — origin story (pre-review)
├── 2026-07-02.md    # Session 2 — present-tense shift (post-review)
```

Each file: number → answer with follow-ups. Closed with `*Session complete — X/5*`.

## Session History

### Session 1 (2026-07-01) — 10 questions, origin-heavy

Strongest answers: father (#1 follow-up), angriest moment (#8 broomstick), broken belief (#6).
Weakest: respect (#7 — three words), awe (#10 — one word), loyalty (#5 — formula).
Key dangling thread: "Montreal Joe doesn't come out very often anymore."

### Session 2 (2026-07-02) — 5 questions, post-challenger

Quality leap. Strongest: artificial constraints (#1), marriage-as-parental-repeat (#2),
"all decisions made from desperation" (#5). Weakest: none — all produced real material.

## Pitfalls

- 10 questions at once = survey, not conversation. 5 with follow-ups is better.
- Without mandatory probes, answers stay shallow.
- Abstract questions → abstract answers. Story format produces real material.
- The cron can't do live follow-ups — live sessions fill that gap.
- Fresh memories from therapy (Lyra sessions) can sound rehearsed but aren't.
