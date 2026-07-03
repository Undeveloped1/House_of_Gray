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
- Save Joe's answers to the archive when he provides them (see Archiving workflow below)
- Help Joe compile answers into a manuscript when he's ready
- Track progress and surface patterns across answers
- Adjust the cron schedule or delivery format at Joe's direction

## Answer archiving workflow

When Joe sends answers (often raw, numbered 1-3), follow this sequence:

1. **Read state** (`autobiography-state.json`) to see current day. The day shown is the NEXT day to be asked, so yesterday's answers are for day-1.
2. **Read checklist** (`autobiography-checklist.md`) — match Joe's numbered answers to the three questions for that day.
3. **Check for existing file** — `search_files` in the archive directory for `Day_NN`. If one exists, the answers may already be saved.
4. **Mirror existing format** — `read_file` the most recent prior day's archive for the exact template (header, separator style, footer).
5. **Create the file**: `YYYY-MM-DD_Day_NN_Phase_NN.md`. Include the original prompt question in a `>` blockquote under each answer header, even if Joe answered briefly.
6. **Verify**: confirm file exists, header/footer match, all three answers present. State already advanced by cron — don't touch it.

Joe's raw answers often map directly to the question order (1→factual, 2→emotional, 3→sensory). If ambiguous, match by theme.

## Don't do

- Don't pressure Joe to answer. The prompts are invitations, not demands.
- Don't modify the state file manually — the cron handles it.
- Don't ask Joe "did you answer today's prompts?" unless he brings it up.
- Don't include the literal checklist row in the archive file — use the narrative question text.

## Daily flow

1. Cron fires at 13:00 UTC → 3 questions land in Joe's DM
2. Joe answers when he wants, if he wants
3. Paul saves answers to archive when provided
4. Eventually: compile into book manuscript
