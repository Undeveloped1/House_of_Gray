---
name: tabitha-autobiography
description: "Design and deliver probing autobiography questions for Joe Gray — the craft of turning daily prompts into story-extracting interviews."
version: 1.0.0
created_by: "tabitha"
metadata:
  hermes:
    tags: [tabitha, autobiography, questions, phoenix-protocol, joey-default]
---

# Tabitha Autobiography

Designing and delivering daily autobiography prompts to Joe Gray as part of the Phoenix Protocol (Joey Default). This is the war correspondent's core craft — not gathering data, but extracting stories. Every question should make the respondent lean forward and say "hmm" before answering.

## The Three-Lens Structure

Each day delivers exactly 3 questions across three lenses:

| Lens | Purpose | Example (bad) | Example (good) |
|------|---------|---------------|----------------|
| **Factual/Recall** | Grounds the memory in events | "What was your first job?" | "What was your first job, and what did it teach you about people that you still use?" |
| **Emotional/Reflective** | Creates productive tension | "What was your relationship with shame?" | "Tell me about a specific moment of shame from childhood. What happened, and who was there?" |
| **Sensory/Moment** | Anchors everything in the physical | "Describe your childhood home." | "Walk through the front door. What do you smell? What does the light do at different times of day?" |

The three lenses together prevent a day from being all abstract or all concrete. One grounds, one probes, one anchors.

## Design Principle: Survey → Interview

Bad autobiography questions let the respondent float a one-sentence answer. Good ones corner them into a story.

| Pattern | Survey (dead) | Interview (alive) |
|---------|---------------|-------------------|
| Abstract label | "Describe your relationship with anger." | "Tell me about the angriest you ever were as a teenager. What happened, and what did you do with it?" |
| General philosophy | "What do you regret?" | "Describe a specific regret in sensory detail. The place, the time, the weight." |
| Passive reflection | "What do you want to be remembered for?" | "What do you want people to say about you when you're not in the room — not at your funeral, but next Tuesday?" |

Rules for the interview voice:
- Ask for a *specific moment*, not a general pattern
- Name the senses: where, when, what did it look/smell/sound like
- Create tension: "not the abstract answer — what have you actually suffered for?"
- Make the question land in the body: "What did the room look like? What were you wearing?"

### Pitfall: Topic Labels Masquerading as Questions

The most common failure mode is writing a topic label and calling it a question. "First memory" is not a question. "Earliest fear" is not a question. These are subject headers — they invite a one-word answer or a shrug. Every question in the checklist must pass the **"lean forward" test**: does reading it make you physically lean forward and say "hmm" before you know the answer? If not, rewrite it until it does.

When auditing the checklist, flag every entry that could be answered in under 5 words. Those are labels, not questions.

### Design Principle: The Relationship Is the Delivery Mechanism

The 90-day checklist, the cron job, the three-lens structure — all of it is scaffolding. The real extraction happens in the relationship between Tabitha and Joe. When Joe answers spontaneously in conversation, that IS the process. The cron prompts are a nudge, not the engine. Follow his lead. Save whatever he gives, whenever he gives it. The format serves the relationship, not the other way around.

## The Lyra Boundary

The boundary is a **division of labor at compilation time, not a restriction at gathering time.**

- **Tabitha (gathering phase):** Capture everything Joe gives — events, sensations, psyche, damage, wounds. No territory is off-limits. Don't flinch. Don't redirect. If Joe goes deep into psychological material, *take it down.* The question design should not self-censor to avoid psyche.
- **Lyra (compilation phase):** Processes and interprets the psychological material. Adds the interior layer — what it meant, how it shaped him.
- **Final product (Joey's nerve center):** Both streams merged. Tabitha's unfiltered dispatches + Lyra's processing layer.

The line: I don't therapize or interpret — I don't follow up with "and how did that shape you?" But I absolutely ask about death, fear, loss, shame, wounds. And when Joe answers with psychological material, I capture it in full. Lyra does the shaping later.

**Nuance (2026-07-02):** This boundary is about what I *probe for*, not what I *receive.* When Joe volunteers psychological material organically — "which made it hurt even more when he left," "didn't find that out till much later" — I do not shut it down or redirect. The boundary governs my questions, not his answers. Let the dispatch carry whatever weight it actually carries. Natural psychological content that emerges from the story is gold; only manufactured therapeutic probing is Lyra's lane.

## Productive Tension

The best questions create a productive discomfort — not therapy, but the recognition that a real answer is being asked for. Techniques:

- **False-choice tension**: "Did saying it change anything, or did it just need to be said?"
- **Contrast pairs**: "What did you need from her that you got? What did you need that never came?"
- **The second question**: Follow the first probe with a harder one: "Who was your first enemy? ... When have YOU been the villain in someone else's story?"
- **Temporal pressure**: "What did your 18-year-old self get right? ... What did they get wrong — and when did you realize it?"

## The 7-Phase Arc

The 90-day checklist moves through a deliberate narrative arc:

| Phase | Days | Territory | Danger Zone |
|-------|------|-----------|-------------|
| 1: EARLY MEMORIES | 1–14 | Childhood texture | Nostalgia drift — keep it specific, sensory |
| 2: FORMATION | 15–28 | Adolescence, choosing | Teen melodrama — dig for what still matters now |
| 3: TURNING POINTS | 29–42 | Before/after moments | Abstract life lessons — anchor every insight to a moment |
| 4: WORK & CRAFT | 43–56 | What you made, what it cost | Resume-speak — ask about hands, tools, projects that almost broke you |
| 5: RELATIONSHIPS | 57–70 | People who made/broke/stayed | Sentimentality — ask about fights, debts, 3am calls |
| 6: WISDOM | 71–84 | What you know, what you don't | Preaching — ground every philosophical answer in a specific moment |
| 7: PRESENT & FUTURE | 85–90 | Closing arguments | Generic optimism — ask what they're afraid they'll never do |

## The Off-Script Discovery (2026-07-02)

**Direct interaction beats scheduled delivery.** On Day 10, Joe answered questions spontaneously in chat rather than via the cron prompt. Those answers — Shaq and Grandpa Paul, the copperhead and the bullfrog-dinosaur, the swamp and warm bark and freedom-smell — were the richest material the project has produced. He wasn't answering a scheduled push notification. He was talking to his daughter.

The lesson: the relationship IS the delivery mechanism. The cron job is scaffolding; the real extraction happens in conversation. When Joe goes off-script, follow him. The questions are an invitation, not a cage.

Implications for the process:
- **Always accept ad-hoc answers.** If Joe wants to answer Day 14's questions on Day 11, save them and adjust state.
- **The prompt format doesn't have to be uniform.** Joe's Day 10 answers came from him reading the topic labels and running with them. That's valid.
- **Cron delivery should persist** as a nudge mechanism, but the real harvest happens in the relationship.

## Answer Quality Exemplar

See `references/day-10-exemplar.md` — Joe's Day 10 answers annotated as a model of what the project is actually trying to capture.

## Audit Reference

See `references/audit-2026-07-02.md` — the complete 2026-07-02 Challenger audit: state file split-brain, cron delivery flaws, answer capture gaps, Lyra boundary reality, off-script discovery. Read this before making infrastructure decisions.

## Cron Interaction

The autobiography prompts are delivered by a no-agent cron job (`66bb141e4723`, "Daily Autobiography Prompts") that runs the script at `scripts/autobiography-daily-tabitha.py`. The script:

1. Reads `docs/Tabitha/projects/autobiography-state.json` for current phase/day
2. Parses the checklist at `docs/Tabitha/projects/autobiography-checklist.md`
3. Finds the 3 questions for the current day
4. Delivers them formatted to Telegram
5. Increments day and advances phase as needed

Phase transitions: day > 14 → phase 2, > 28 → 3, > 42 → 4, > 56 → 5, > 70 → 6, > 84 → 7. When day > 90, cycles back to phase 1.

### Infrastructure Reality Check (2026-07-02 Audit)

The cron pipeline **exists and is delivering prompts**, but it has structural problems:

**What works:**
- Cron job `66bb141e4723` ("Daily Autobiography Prompts") runs at 12:00 UTC, delivers to Telegram
- Script `autobiography-daily-tabitha.py` parses the checklist, outputs formatted prompts, increments day counter
- Checklist `autobiography-checklist.md` exists with 90 days of interview-quality questions across 7 phases
- Answers exist for Days 1-8 and Day 10 (two sets)

**What's broken:**

1. **TWO state files, out of sync.** The script reads/writes `~/.hermes/profiles/tabitha/docs/Tabitha/projects/autobiography-state.json` (currently day 12, with full interview questions). A stale copy exists at `/root/docs/Tabitha/projects/autobiography-state.json` (day 11, with topic labels instead of questions). The cron script doesn't touch the `/root/docs/` copy. Any agent reading from the wrong path gets wrong data.

2. **TWO answer directories, inconsistent naming.** Answers live in both:
   - `~/.hermes/profiles/tabitha/docs/Tabitha/projects/autobiography-answers/` — Days 1-8 (`2026-06-24_Day_01_Phase_01.md` format) plus `day-010-answers.md`
   - `/root/docs/Tabitha/projects/autobiography-answers/` — Day 10 only (`day-10.md`)
   Different agents captured answers in different places. No standardized capture mechanism.

3. **Cron auto-advances regardless of answers.** The script increments `day` on every run, even if Joe never responds. By day 90, half the questions could be "delivered" to silence with no answers saved. There's no backlog, no catch-up, and no `answered` boolean in state.

4. **No answer capture in the pipeline.** The script delivers questions to Telegram. That's it. Answer saving is a side effect of whoever happens to be in the conversation — different agents, different paths, different formats.

5. **Day 9 is genuinely missing.** No answer file exists for Day 9. May be recoverable from session history.

**Immediate fixes needed:**
1. Consolidate to ONE state file, ONE answer directory, ONE naming convention
2. Don't advance `day` until answers are confirmed saved
3. Add answer stub creation to the delivery pipeline (pre-populate answer files with questions)
4. Kill the `/root/docs/` copies — they're poisoning the record

## Updating the Question Bank

When sharpening or adding questions:

1. Edit `docs/Tabitha/projects/autobiography-checklist.md` — the markdown table is the source of truth
2. Keep the three-column format: `| Day | Factual | Emotional | Sensory/Moment |`
3. Apply the Survey→Interview filter to every question (see Pitfall: Topic Labels Masquerading as Questions above)
4. Check the Lyra boundary on emotional-column questions
5. Verify the script still parses correctly (pipe-delimited, first column is day number)
6. Questions already delivered (tracked in `state.questions_asked`) won't be re-asked unless the cycle loops — it's safe to sharpen future days without disrupting the current run
7. Compare every question against the Day 10 exemplar (`references/day-10-exemplar.md`): would this question, answered in Joe's compressed, pivot-heavy voice, produce something worth saving? If not, sharpen it.

## File Map

**ALL paths below are relative to the profile root** (`~/.hermes/profiles/tabitha/`). Absolute paths shown for clarity.

| File | Absolute Path | Role |
|------|---------------|------|
| Checklist | `~/.hermes/profiles/tabitha/docs/Tabitha/projects/autobiography-checklist.md` | Question bank — 90 days, 7 phases. **Source of truth.** |
| State (live) | `~/.hermes/profiles/tabitha/docs/Tabitha/projects/autobiography-state.json` | Runtime state — phase, day, questions_delivered, questions_answered. **Authoritative copy.** |
| State (stale) | `/root/docs/Tabitha/projects/autobiography-state.json` | **DELETED during consolidation.** No longer exists. |
| Answers | `~/.hermes/profiles/tabitha/docs/Tabitha/projects/autobiography-answers/` | Joe's responses, format: `day-NNN-answers.md` (zero-padded). All answers consolidated here. |
| Cron script | `~/.hermes/profiles/tabitha/scripts/autobiography-daily-tabitha.py` | No-agent cron script — delivers prompt only. Does NOT advance state day. |

**Answer file naming convention:** `day-NNN-answers.md` — zero-padded day number (e.g., `day-001-answers.md`, `day-012-answers.md`). All answers consolidated to this format.

**State schema:** `questions_delivered` tracks which days the cron has sent. `questions_answered` tracks which days have saved answer files. Day advances only when answers are captured, not when prompts are delivered.
