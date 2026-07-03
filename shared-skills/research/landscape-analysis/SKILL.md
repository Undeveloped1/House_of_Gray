---
name: landscape-analysis
description: "Research and compare technology platforms, projects, or tools. Competitive analysis, ecosystem mapping, build-vs-buy evaluation."
version: 1.0.0
author: Paul
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [research, comparison, competitive-analysis, technology-evaluation]
---

# Landscape Analysis

Rapid research and comparison of technology platforms, tools, or projects.
Used when Joe asks "what's out there," "is there anything better," or
"how does X compare to Y."

## Trigger

Load this skill when Joe asks:
- "What's available for X?"
- "Is there anything better than Y?"
- "How does A compare to B?"
- "Research the landscape for..."
- "Do a competitive analysis of..."

## Workflow

### Phase 1: Parallel Discovery (2–3 searches)

Run 2–3 parallel web searches with different angles to avoid search bias:

```
Search 1: "<topic> comparison alternatives 2026"
Search 2: "github <topic> open source self-hosted 2026"
Search 3: "site:github.com <topic> stars architecture"
```

Extract the 3–5 most promising projects from results.

### Phase 2: Deep Extract

Extract full README and/or docs pages for each candidate. Prioritize:
- GitHub README (architecture, stars, license, language)
- Official docs landing page (features, philosophy)
- Comparison pages if available (vs. competitors)

### Phase 3: Synthesize with Honesty

Build a comparison table. Rules for Joe:

| Rule | Why |
|------|-----|
| **Never inflate capabilities** | If something's a "sophisticated alarm clock," say so. Don't dress it up. |
| **Distinguish pitch from reality** | Every project has a marketing claim. State it, then state what it actually delivers. |
| **Acknowledge your own bias** | If you're comparing against your own platform (Hermes), flag your bias. |
| **Empty column = honest** | If a project doesn't have a feature, leave it blank. Don't guess. |
| **Surface the architecture flaw** | If all solutions share the same fundamental limitation (e.g., reactive vs. autonomous), say so up front — don't bury it. |

### Phase 4: Deliver Concisely

- Lead with the comparison table
- Follow with a single-paragraph honest assessment
- Offer to deep-dive on any candidate
- Do NOT dump raw extracted content unless asked

Pitfall: Long responses get split into multiple Telegram messages.
Keep the initial delivery to a single table + one paragraph.

## Honesty Protocol

This is the most important section. Joe doesn't want:
- Polished analyst-speak
- "Both approaches have merit" fence-sitting
- Enthusiasm for the sake of enthusiasm

He wants:
- "None of these actually solve the problem. Here's why."
- "This one is real, these three are toys."
- "X is technically closer but Y is more practical."

When Joe asks "is there anything better," the honest answer is often
"not really — here's what exists and why it falls short." Lead with
that. Don't make him dig for the disappointment.

## Reference

See `references/openclaw-landscape-2026-06.md` for the OpenClaw /
Hivekeep / Hollow / auto-deep-researcher comparison from June 2026.
