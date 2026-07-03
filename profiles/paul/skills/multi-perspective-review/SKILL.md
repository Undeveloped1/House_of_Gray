---
name: multi-perspective-review
description: "Parallel multi-lens review using 4-5 sub-agent reviewers. Spawns tone, design, identity, flavor, and distinctiveness critics in parallel, then synthesizes findings."
version: 2.0.0
author: Paul
---

# Multi-Perspective Review

Spawn 4-5 reviewer sub-agents each with a different lens — not one catch-all critic. Each reviews the same artifact from their specialized perspective. Paul synthesizes the findings. Joe only sees the synthesis.

**When:** After a card set passes audit + single-critic review. When pushing B/B+ to A-. For lore docs, process docs, or any creative artifact.
Archive: `docs/Paul/workspace/multi-perspective-review-archive.md`.

## The Five Lenses

### 1. Tone Reviewer
**Question:** "Do these cards sound like [faction]?"
Checks: card names (era + faction voice), flavor text (register, rhythm, tone), rules text (professional + faction character), hero dialogue (distinct per hero).
**Grades:** Pass (80%+ hit) / Marginal (60-80%) / Fail (below 60%).

### 2. Design Reviewer
**Question:** "Are the mechanics interesting and distinct?"
Checks: signature mechanic distribution + support, boring/auto-include/never-play cards, real vs paper synergy edges, cross-faction distinctiveness, interesting decision patterns.
**Grades:** Pass / Needs specific fixes / Fundamentally flawed.

### 3. Identity Reviewer
**Question:** "Do the cards feel like the faction they claim to be?"
Checks: crew-mechanic alignment (Hustle on Street, Paid on Professionals), CAN/CANNOT enforcement, daily life texture, emotional truths, blind spot respect.
**Grades:** Identity-locked (cards ARE the faction) / Adequate (mostly aligned) / Drift (cards contradict identity).

### 4. Flavor Reviewer
**Question:** "Do names, flavor text, and art direction cohere?"
Checks: name quality (punchy, memorable, era-appropriate), flavor text (rewarding, specific), ludonarrative (card DOES what name promises), naming convention compliance, legendary impact.
**Grades:** Rich (cards tell a story) / Adequate / Generic (could be any faction).

### 5. MTG Distinctiveness Reviewer
**Question:** "Is this novel or could it be an MTG set?"
Checks: TCG analogs for signature mechanic (sufficient twist?), MTG-reprint feelings, different play patterns from MTG equivalents, distinct emotional experience from MTG color pie.
**Grades:** Defensibly novel / Adequate twist / MTG with different names.

## How to Execute

### Step 1: Spawn Reviewers in Parallel

Use `delegate_task` with tasks array (max 3 concurrent). Two batches if 5 reviewers:

**Batch 1 (3 parallel):** Tone, Design, Identity reviewers.
**Batch 2 (2 parallel, after Batch 1):** Flavor, MTG Distinctiveness reviewers.

### Step 2: Synthesize Findings

Unified report format:
```
## Multi-Perspective Review — [Faction]

### Summary
- Tone: [grade] — [one-line]
- Design: [grade] — [one-line]
- Identity: [grade] — [one-line]
- Flavor: [grade] — [one-line]
- Distinctiveness: [grade] — [one-line]

### Consensus Findings
[Issues flagged by 3+ reviewers — these are real]

### Divergent Findings
[Issues flagged by only 1 reviewer — flag for judgment]

### Top 5 Fixes
[Ranked by impact]

### Verdict
[SHIP / ITERATE with N fixes / BACK TO SPEC]
```

### Step 3: Surface to Joe

Joe sees the unified report — NOT the 5 individual reviewer outputs (unless he asks). The synthesis IS the product.

## Reviewer Prompt Templates

Each reviewer needs: the card set path, faction identity bible, crew profiles, CAN/CANNOT lists, naming conventions. Sub-agents have zero memory — complete context is mandatory.

**Tone critic prompt:** "You are a tone critic for [faction] (1961 Detroit TCG). Read [set_path]. Evaluate every card: names match era+faction voice? Flavor text: right register, specific not generic? Rules text: professional + faction character? Hero dialogue distinct? Output severity-graded findings (Critical/Major/Minor), overall grade, top 5 worst offenders with fixes."

**Design critic prompt:** "You are a mechanical design critic for [faction]. Read [set_path]. Evaluate: signature mechanic well-distributed? Boring/auto-include/never-play cards? Real vs paper synergy edges? Interesting decisions? Cross-faction distinct from [other factions]? Output severity-graded findings, grade, worst offenders with fixes."

**Identity critic prompt:** "You are identity coherence critic for [faction]. Read [set_path] AND [identity_bible_path]. Evaluate: crew-mechanic alignment [list profiles], CAN/CANNOT violations, daily life texture, emotional truths, blind spot respect. Output severity-graded findings, grade, worst offenders with fixes."

**Flavor critic prompt:** "You are flavor critic for [faction]. Read [set_path]. Evaluate every card: name quality (punchy, memorable, era-appropriate), flavor text (rewarding attention? specific?), ludonarrative (card DOES what name promises), naming convention compliance [rules]. Output severity-graded findings, grade, worst offenders with fixes."

**MTG Distinctiveness critic prompt:** "You are TCG originality critic. Read [set_path]. Evaluate: signature mechanic has TCG analog? If yes, sufficient twist? Cards feeling like MTG reprints? Deck archetypes play differently from MTG equivalents? Distinct emotional experience from MTG color pie? Output severity-graded findings, grade, specific cards needing differentiation."

## Pitfalls

- **Complete context.** Reviewers have zero memory — include identity bible, crew profiles, CAN/CANNOT, naming conventions, full card set.
- **Critique, don't redesign.** Their output is findings, not rewritten cards.
- **Synthesize before surfacing.** Joe wants one unified report, not five.
- **Prioritize consensus.** 3+ reviewer flags = real. 1 reviewer flag = might be taste.
- **Three concurrent max.** Two batches for 5 reviewers. Don't spawn 5 at once.
