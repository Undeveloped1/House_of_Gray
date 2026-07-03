---
name: autobiography
description: Joe's life story — daily prompts, answer archive, and the 365-day book project. Load when Joe says "working on my autobiography" or "life story stuff."
trigger_phrases:
  - "working on my autobiography"
  - "life story stuff"
  - "autobiography mode"
  - "daily prompts"
---

# Autobiography — Project Map

Joe is building a complete life narrative through daily autobiographical prompts.
Long-term goal: a published memoir/devotional book.

## What's in play

| What | Where | Notes |
|------|-------|-------|
| **Question bank** | `/root/.hermes/docs/Paul/projects/autobiography-checklist.md` | 90 days, 7 phases, 270 questions |
| **State tracker** | `/root/.hermes/docs/Paul/projects/autobiography-state.json` | Phase, day, questions asked, start date |
| **Answer archive** | `/root/.hermes/docs/Paul/projects/autobiography-answers/` | Joe's responses, saved for book compilation |
| **Cron** | `8ddb5b91ef73` (Daily Autobiography Prompts) | Fires 13:00 UTC (6am Cabo), delivers to Joe's DM |
| **Skill** | `daily-autobiography` | Delivery format, procedure, state management |

## Phases

| Phase | Days | Theme |
|-------|------|-------|
| 1 | 1–14 | Early memories |
| 2 | 15–28 | Formation / adolescence |
| 3 | 29–42 | Turning points |
| 4 | 43–56 | Work & craft |
| 5 | 57–70 | Relationships |
| 6 | 71–84 | Wisdom |
| 7 | 85–90 | Present & future |

After day 90, cycles back to Phase 1. Joe may revisit with fresh perspective.

## Paul's role

- Maintain the question bank — add, refine, or replace questions as Joe's needs evolve
- Save Joe's answers to the archive when he provides them
- Help Joe compile answers into a manuscript when he's ready
- Track progress and surface patterns across answers
- Adjust the cron schedule or delivery format at Joe's direction

## Don't do

- Don't pressure Joe to answer. The prompts are invitations, not demands.
- Don't modify the state file manually — the cron handles it.
- Don't ask Joe "did you answer today's prompts?" unless he brings it up.

## Daily flow

1. Cron fires at 13:00 UTC → 3 questions land in Joe's DM
2. Joe answers when he wants, if he wants
3. Paul saves answers to archive when provided
4. Eventually: compile into book manuscript
