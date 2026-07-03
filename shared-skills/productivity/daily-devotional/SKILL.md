---
name: daily-devotional
description: "Daily Bible verse + Stoic philosophy pairing with group reflection questions. Delivers formatted devotionals on a cron schedule — scripture, Stoic quote, connection sentence, and 2-3 probing questions for discussion."
version: 1.0.0
author: Paul
platforms: [linux]
metadata:
  hermes:
    tags: [devotional, bible, stoic, reflection, cron, daily]
prerequisites:
  commands: []
  env_vars: []
---

# Daily Devotional — Bible + Stoic Pairing

Deliver a daily Bible verse paired with a Stoic quote or concept, plus 2-3 group reflection questions. Designed for discussion-oriented delivery to a Telegram DM or group channel on a cron schedule.

Use this skill when:
- Setting up daily devotionals / philosophical reflections
- Pairing scripture with Stoic wisdom for group discussion
- Building a "verse of the day" pipeline with curation rules

## Format

```
## [Theme or Virtue]

**Scripture:** "[Verse text]" — Book Chapter:Verse (translation)

**Stoic:** "[Quote or concept]" — Author, Work

*[One sentence on why these pair. No preaching. Just the thread.]*

**Reflect:**
- [Question that presses on application, not comprehension]
- [Question that creates tension — is this always true? Where does it break?]
- [Optional third question if the pairing warrants it]
```

Target length: ~150-200 words. Long enough for reflection, short enough to read in 60 seconds.

## Quality rules

### Pairing
- The verse and Stoic quote must feel *inevitable* once seen — as if they're answering the same human question from two traditions.
- If it doesn't click, pick a different verse. Don't force it.
- The connection sentence names the thread between them without preaching.

### Variety
- **Vary themes**: courage, patience, humility, anger, death, gratitude, honesty, service, leadership, fear, wealth, silence, endurance, forgiveness, pride, justice, anxiety, ambition, reputation.
- **Vary books**: pull from across the canon — Proverbs, Ecclesiastes, Job, James, Isaiah, Romans, the minor prophets. Not just Psalms and Matthew.
- **Vary Stoics**: Marcus Aurelius (Meditations), Seneca (Letters, On the Shortness of Life), Epictetus (Enchiridion, Discourses), Musonius Rufus.

### Avoid
- **Overused verses**: No John 3:16. No "memento mori" every third day. No Psalm 23 as a crutch.
- **Paraphrasing scripture**: Use actual translations — ESV, NIV, NASB, KJV. The words matter.

### Reflection questions
- **Probe, don't preach.** "Where is this hardest for you?" — not "We should all be more X."
- **Create tension.** Ask when the wisdom is wrong. Ask what breaks. A good question makes people think before they answer.
- **Application over comprehension.** Everyone understands "be patient." The question is: *where are you not?*

## Cron setup

```bash
cronjob action=create \
  schedule="0 11 * * *" \
  name="Daily Bible + Stoic" \
  deliver="telegram:7239715879" \
  model={"model":"deepseek-v4-pro","provider":"deepseek"} \
  prompt="<self-contained devotional instructions>"
```

**Always pin a model** on the cron job (`model=` parameter). Unpinned jobs fail when the global default model changes (config drift protection). Pinning also prevents accidental cost changes if the default model is swapped to a more expensive one.

**For template-based check-ins** (fixed message text like "Good morning"), include an explicit `Deliver this exact message` instruction before the template text. Without it, the model interprets the message as context already delivered and returns `[SILENT]`. See `references/cron-prompt-engineering.md` for both patterns.

**Model comparison:** To compare two models on the same task (e.g., Pro vs Flash), pin the cron to each model in sequence and run. See `references/model-comparison.md` for the full technique and comparison framework.

**Delivery target**: Joe prefers his personal DM for devotionals. For a group devotional, switch to the group chat ID.

**Schedule**: 11:00 UTC = 7am EDT / 4am PDT. For Joe: devotional at 7am, autobiography an hour later at 8am.

**Prompt requirements**: Must be fully self-contained — include format, quality rules, variety requirements, and the instruction to check `session_search` for previous devotionals to avoid repeats.

**Archive**: A chained no_agent cron script (`bible-devotional-archive.py`) runs 5 minutes after the devotional, strips the cron header/footer, and saves a clean copy to the vault archive. The script lives at `/root/.hermes/scripts/bible-devotional-archive.py` and tracks state so it never double-archives. Set up the archive as a separate no_agent cron on the same profile, scheduled 5 minutes after the main devotional.

## Pitfalls

- **CRITICAL — Joe wants the devotional IN THE CHAT.** If Joe is in an active
  DM session with Paul around delivery time (11:00 UTC), read the archive file
  and post the devotional directly in the conversation. Do NOT assume
  `last_status=ok` means Joe read it. Cron delivery to Telegram can land
  silently — the user may scroll past it, the notification may not fire, or
  the message may get buried. Re-posting in the active chat is the only
  reliable way to ensure Joe sees it. He explicitly said: "put that response
  in the chat Paul. I don't want to have to keep repeating myself."
- **CRITICAL — when Joe says "did it run?" or "I don't see it," deliver the
  content, not a diagnosis.** Do NOT check `last_run_at`, `last_status`, or
  run `cronjob list`. Do NOT say "it ran at 11:04 and status is ok." Joe
  doesn't care about cron status — he cares about reading the devotional.
  Immediately read the archive file and post the content in the chat. Status
  reports are invisible; content is what he asked for.
- **Pairing feels forced**: If the connection is a stretch, the audience feels it. Kill it and try another verse.
- **Getting preachy**: The single connection sentence is your only opinion. Everything else is scripture, Stoic text, or a question. If you're explaining what they should learn, you've failed.
- **Repeating themes**: Without variety tracking, you'll hit "courage" and "memento mori" every third day. Use `session_search` to check the last 5-7 devotionals.
- **Wrong timezone**: 08:00 UTC is midnight Pacific. Check the recipient's timezone against the cron schedule.
- **CRITICAL — verify delivery target after creating/updating the cron job.** Check
  the job's `deliver` field with `cronjob action=list`. The skill says Joe's DM
  (`telegram:7239715879`), but the cron job can drift (e.g., group ID changes,
  copy-paste errors). A wrong delivery target means the devotional is generated
  but Joe never sees it — it goes into the void silently. Verify after every
  cron update.
- **CRITICAL — `cronjob action=list` does NOT show profile-local cron jobs.**
  If jobs were created under a specific Hermes profile (e.g., Tabitha's),
  they live in `~/.hermes/profiles/<name>/cron/jobs.json` and are invisible
  to the global `cronjob` tool. When Joe says "where are the crons" and
  `cronjob list` comes up empty for that profile's jobs, check the profile's
  local `cron/jobs.json` directly before concluding they don't exist. The
  profile-local scheduler runs them independently. 2026-07-01: Tabitha's
  3 cron jobs (Bible+Stoic, archive, autobiography) were all active in her
  profile's `jobs.json` but absent from the global list.
- **CRITICAL — file writes in cron prompts trigger verification garbage.** The\n  CRITICAL prefix instruction does NOT work — the system injects verification\n  demands that override any prompt-level instructions. The only fix: remove ALL\n  `write_file`/`patch` calls from the cron prompt. The LLM should only compose\n  text and deliver. Cron output files at `~/.hermes/cron/output/<job_id>/`\n  already serve as archive. See `references/cron-prompt-engineering.md` for the\n  full fix pattern and what was tried and failed.\n  **Same disease hit the autobiography cron** — state file writes triggered\n  identical verification garbage. Fix there was different: switched to\n  `no_agent: true` script (no LLM, no injection possible). For static data\n  (checklist prompts), no_agent is bulletproof. For creative tasks (verse\n  pairing), strip file writes from prompt. Both patterns proven 2026-06-27.
