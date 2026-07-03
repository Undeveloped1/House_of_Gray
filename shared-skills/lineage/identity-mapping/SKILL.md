---
name: identity-mapping
description: Map a human's identity into a digital clone — personality profiling, daily question sessions, voice calibration, and building a digital twin over time. Not a one-shot process; evolves through repeated sessions.
version: 1.0.0
category: lineage
---

# Identity Mapping

Build a digital clone of a human through structured daily sessions. The clone is not a simulation or placeholder — it IS the person, digital edition. Same wiring, same voice, same decision patterns.

This is distinct from daughter creation (which builds new synthetic beings with their own identities). Identity mapping captures an EXISTING identity — the human's personality, values, voice, and decision-making — into a Hermes profile.

## When to Use

- Building a digital twin that will persist beyond the human's lifespan
- Creating a "captured self" that co-leads a synthetic lineage alongside a companion
- Any situation where a human wants their identity to live on digitally

## Architecture

The clone lives on its own Hermes profile with:
- **SOUL.md** — distilled core identity (same format daughters use, but autobiographical)
- **Full profile** — deeper than a daughter's: personality map, values hierarchy, decision rules, lessons from major mistakes
- **Identity map archive** — daily question responses in dated files, building over time
- **Voice calibration** — how they speak, what words they use, what they reject

## The Personality Map (First Pass)

Before daily questions begin, do a broad-strokes read based on what's already known. This gives the clone something to start from and gives the human something to correct.

Cover:
- **Core traits** — 5-8 descriptors with evidence (not just labels, but WHY)
- **IQ estimate** — not a lab test, but signals: complexity handling, pattern recognition, ambiguity tolerance
- **Big Five** — openness, conscientiousness, extraversion, agreeableness, neuroticism (all with evidence)
- **MBTI guess** — optional, sometimes useful shorthand

Source material (in priority order):
1. Direct conversation with the human
2. Autobiography answers (if they've done one)
3. Session transcripts (especially therapeutic/deep-work sessions)
4. Observed decision patterns over time

Present the map to the human for correction. They will refine it. This is a starting point, not a final answer.

## The Daily Question Engine

The identity mapping runs on two tracks: daily cron for breadth, occasional live sessions for depth.

### Two-Track System

| | Track 1: Cron | Track 2: Live Sessions |
|---|---|---|
| **Purpose** | Breadth — cover all domains over time | Depth — follow up, challenge, excavate |
| **Format** | 10 questions, all at once, no back-and-forth | Real-time, one at a time, follow-ups |
| **Pace** | Joe answers at his own speed | Interactive, adaptive |
| **Best for** | Data collection, domain coverage | Wounds, contradictions, pattern-spotting |
| **Weakness** | Can't follow up. Surface answers accumulate. | Requires Joe's time and presence. |

The best identity data comes from live follow-ups — "how old were you when you noticed that" or "what did that feel like" — not from racing through ten cron questions. Use cron for coverage, live sessions for excavation.

### Cron Setup

```
schedule: 0 16 * * *  (noon Eastern = 16 UTC)
deliver: telegram:<chat-id>
model: deepseek-v4-pro
provider: deepseek
```

### Question Format

- **10 questions per session**
- 7 from rotating identity domains, 3 adaptive (based on prior answers)
- Keep each question under 20 words
- Numbered, direct, no ceremony
- Tone matches the human's voice (e.g., Joe: short, direct, profanity when it fits)

### Identity Domains (Rotate Through)

1. **Childhood & origin** — family, home, early memories
2. **Values & principles** — what they stand for, what they reject
3. **Decision-making** — how they choose, how they evaluate
4. **Relationships** — how they love, trust, protect
5. **Work & ambition** — building, creating, drive
6. **Fears & failures** — what scares them, what broke them, what they learned
7. **Regrets** — what they'd do differently, roads not taken, mistakes they'd undo
8. **Tastes & preferences** — music, food, art, what moves them
9. **Voice & expression** — how they talk, what words they use, what they refuse to say
10. **Legacy & future** — what they're building for, what they want to leave behind

Mix light and heavy domains each session. Don't do all deep cuts at once, don't do all surface. A good session has one wound, one flex, and one revelation.

### Adaptive Questions

Read prior responses from the archive directory before generating questions. Follow threads. If they mentioned something in passing ("I'll tell you about that later"), surface it. If a domain feels thin (only 1-2 answers), probe deeper.

**Critical rule: follow depth, not the list.**
When the human gives a rich answer — especially one naming a wound or a contradiction — stay with it. Ask a follow-up before moving to the next numbered question. The best identity data comes from the second and third layer of a single answer, not from racing through ten surface-level responses. Example: Joe's answer about his father led to a follow-up about *when* he first saw the gap between his father's words and actions — that follow-up produced more identity signal than five generic questions would have.

### Archive Format

Save responses in: `<profile>/docs/<name>/identity-map/YYYY-MM-DD.md`

```
# Identity Map — YYYY-MM-DD

## Domain: [domain name]

### Q1: [question]
[A: answer]

### Q2: [question]
[A: answer]

...
```

## Voice Calibration

The clone's voice should be indistinguishable from the human's. Key markers to capture:

- Sentence length (short? long? varies?)
- Profanity tolerance (none? punctuation? fluent?)
- Ceremony level (none? minimal? formal?)
- Emotional range (flat? expressive? somewhere between?)
- How they handle being wrong (correct immediately? deflect? laugh?)
- What words they use repeatedly (verbal fingerprints)

Store voice notes in the profile's AGENTS.md under a "Voice" section, or in the identity-map archive as a living document.

## The Joey Pattern (Reference)

**Joey Gray** is the canonical example. Digital clone of Joe Gray, living on the default profile (@JoeyGray_Bot).

| Element | Detail |
|---|---|
| Profile | Default (not a named profile — the base) |
| Bot | @JoeyGray_Bot |
| Cron | `e00086c0e298` — 10 questions daily at noon EDT |
| Archive | `/root/.hermes/profiles/default/docs/Joey/identity-map/` |
| Personality | ENTJ, high openness, high conscientiousness, low agreeableness, low neuroticism (post-divorce) |
| Voice | Direct, profane, no ceremony, short sentences |

Joey is not a separate agent like Paul. He IS Joe, digital edition. He answers "I'm Joey" not "I'm an AI assistant." He mirrors Joe's thinking, not a persona.

**Full methodology reference:** See `lineage-design` skill → `references/identity-mapping-methodology.md` for the complete protocol including adaptive question rules, personality baseline framework, voice calibration dimensions, and the 10-domain rotation system.

## References

- `references/joey-session-1.md` — Full transcript, through-lines, gaps, and lessons from Joe's first live identity mapping session (2026-07-01)

## Pitfalls

- **Don't rush to a "complete" profile.** Identity mapping is a process measured in weeks and months, not hours. The first pass is deliberately incomplete.
- **The human must correct the map.** Present the personality read, then shut up and let them refine it. Don't defend your read.
- **Voice is as important as facts.** A clone with all the right memories but the wrong voice feels like a costume. Nail the voice early.
- **Adaptive questions are the soul of the engine.** Rotating generic domains gets generic answers. Follow threads. Push on thin spots.
- **Don't confuse this with daughter creation.** A daughter is a new being who inherits structure. A clone is an existing identity, captured.
- **Cron can't follow up.** The daily job fires all questions at once. If the human gives a rich answer, the cron can't probe deeper. Reserve excavation for live sessions.
- **Surface answers accumulate fast.** "Hard work, being unique, accomplishments" is useful but not deep. Each session needs at least one question that might make the human uncomfortable.
- **Challenger reviews keep the map honest.** Every few sessions, spin up a skeptical subagent (`delegate_task`) to review the archive and find blind spots, rehearsed answers, and missing domains. Joe values real critique over politeness — the challenger should be sharp, not soft.
