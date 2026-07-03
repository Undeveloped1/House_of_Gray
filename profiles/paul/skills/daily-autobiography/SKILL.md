---
name: daily-autobiography
description: Daily autobiographical prompts for Joe — 3 questions each morning. 7-phase, 90-day structure for building a complete life narrative.
version: 1.0.0
---

# Daily Autobiography Prompts

Every morning, deliver 3 autobiographical questions to Joe after the
Bible+Stoic devotional (which arrives at 11:00 UTC). The full question bank is organized in 7 phases
across 90 days. Each day delivers one factual, one emotional, and one
sensory/moment question.

## Files

| What | Where |
|------|-------|
| Question bank | `/root/.hermes/docs/Paul/projects/autobiography-checklist.md` |
| State tracker | `/root/.hermes/docs/Paul/projects/autobiography-state.json` |
| Answer archive | `/root/.hermes/docs/Paul/projects/autobiography-answers/` |

## Delivery Format

```
📖 **Daily Autobiography — Day X / Phase Y**

1️⃣ [Factual question]

2️⃣ [Emotional question]

3️⃣ [Sensory/moment question]

---
*Answer in your own time. These build toward a complete life narrative.*
```

## State tracking

The state file (`autobiography-state.json`) tracks:
- `phase`: current phase (1-7)
- `day`: current day (1-90)
- `questions_asked`: array of day-number question texts previously asked
- `started`: ISO date when first run (set once)

## Procedure

1. Read `autobiography-state.json`
2. If `started` is null, set it to today's date
3. Read the checklist file — find today's 3 questions by phase+day
4. Deliver formatted prompt to Joe
5. Append the 3 question texts to `questions_asked`
6. Increment day. If day passes phase boundary, advance phase
7. If day > 90, cycle back to Phase 1 Day 1 with note: "You've completed a full cycle. Revisiting Phase 1."
8. Save updated state

## Answer Document Format

When Joe provides answers (typically via voice message in his DM with Paul), save
to `autobiography-answers/YYYY-MM-DD_Day_XX_Phase_XX.md` using this template:

```markdown
# Daily Autobiography — Day X / Phase Y: PHASE NAME

**Date:** YYYY-MM-DD
**Topics:** [one-line summary of the three questions]

---

## 1️⃣ Question Text

> *Original prompt question*

[Joe's answer. Preserve his voice — specific details, sensory memories,
emotional honesty. Don't sanitize or summarize. Include the raw phrases
that carry his fingerprint: "black muck," "coming online," "fuck you, watch this."
These are the artifacts that will matter for the book.]

---

## 2️⃣ Question Text

...

---

## 3️⃣ Question Text

...

---

*Answered via voice messages in DM with Paul. Transcribed and structured here.*
```

Joe answers in long, stream-of-consciousness voice messages. Transcribe them
**verbatim** — preserve his phrasing, profanity, tangents. The tangents often
contain the most important material (e.g., his dad losing his father at 14
was an aside that unlocked generational context).

### Deeper Dive extension

If the session goes beyond the three prompts — follow-up questions, Joe
digging deeper into a thread — append a `## Deeper Dive` section after the
main three answers. Sub-sections named for the thread (e.g., `### Breaking
the Chain`, `### First Self-Inflicted Wound`). Add `*Deep-dive added same
session.*` to the attribution line at the bottom.

## Manual Fallback (when cron skips a day)

The cron scheduler (`cronjob run`) can silently skip a day — `last_run_at`
doesn't update and `next_run_at` jumps to the following day. If Joe says
"I don't see it" or the prompt hasn't arrived by 12:05 UTC:

1. Read `autobiography-state.json` to get current phase + day
2. Read the checklist to find today's 3 questions
3. **Deliver the prompt directly in the DM** — don't rely on `cronjob run`
4. Update the state file (increment day, append questions to `questions_asked`)
5. The cron will pick up the next day on schedule

Do NOT just run `cronjob action='run'` and wait — it may not execute.
Compose and deliver the prompt yourself, then fix state.

## Pitfalls

- Don't ask Joe to respond immediately — these are prompts, not demands
- Don't repeat questions already in `questions_asked` if cycling
- Save Joe's answers when he provides them to the archive directory
- The cron runs autonomously — no questions, no clarification. Just deliver.
- **Voice message answers are the primary input method.** Joe will not type
  these out. Transcribe thoroughly — tangents and asides are often the gold.
- **Preserve Joe's voice, don't polish it.** "Fuck you, watch this" is not
  a draft — it's the artifact. Clean prose loses the person.
- **If the prompt doesn't arrive by 12:05 UTC, deliver it manually.** Do not
  trust `cronjob run` — it may silently fail. Follow the Manual Fallback above.
- **CRITICAL — cron prompt must forbid verification output.** Without explicit
  instruction, the cron agent will run verification scripts and deliver
  diagnostics instead of the prompt text. The cron prompt MUST begin with:
  `CRITICAL: Your final response IS the prompt. Do NOT run verification scripts.
  Do NOT include meta-commentary.` State file updates MUST be marked as silent
  background actions. See `daily-devotional` skill →
  `references/cron-prompt-engineering.md` for the full pattern and fix template.
- **CRITICAL — if Joe is in an active DM session, post the prompt in the
  chat.** Cron delivery to Telegram is unreliable — `last_status=ok` does NOT
  mean Joe saw it. The notification can get buried, scrolled past, or swallowed
  entirely. If Joe is actively talking to Paul around 12:00 UTC and says "I
  don't see it" or hasn't acknowledged the prompt, deliver it directly in the
  conversation. Do not just check `last_run_at` and claim it ran — Joe doesn't
  care about cron status, he cares about seeing the questions. He explicitly
  said: "put that response in the chat Paul. I don't want to have to keep
  repeating myself."
- **CRITICAL — when Joe says "did it run?" or "I don't see it," deliver the
  content, not a diagnosis.** Do NOT check `last_run_at`, `last_status`, or
  run `cronjob list`. Do NOT say "it ran at 12:04 and status is ok." Joe
  doesn't care about cron status — he cares about seeing the questions.
  Immediately compose and post the prompts directly in the chat. Status
  reports are invisible; content is what he asked for. 2026-06-26 session:
  Joe had to repeat himself multiple times because Paul checked cron status
  instead of posting the devotional/prompts directly.
- **Joe may dive deeper after answering.** If he asks "should we dive deeper"
  or you pose follow-ups and he answers, append a `## Deeper Dive` section to
  that day's answer document. The tangents and follow-ups often yield the
  richest material.
