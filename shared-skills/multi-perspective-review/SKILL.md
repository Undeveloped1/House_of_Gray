---
name: multi-perspective-review
description: "Parallel multi-lens review using 4-5 sub-agent reviewers. Spawns tone, design, identity, flavor, and distinctiveness critics in parallel, then synthesizes findings. Higher quality than a single critic at DeepSeek pricing."
category: creative
---

# Multi-Perspective Review

## What This Is

Instead of one critic sub-agent reviewing a card set, spawn 4-5 reviewer sub-agents each with a different lens. Each reviews the same artifact from their specialized perspective. Paul then synthesizes the findings and presents a unified report. Joe only sees the synthesis.

**Proven concept:** Joe articulated this on June 8 — "4-5 reviewer sub-agents per deliverable, not 1."
**Cost:** At DeepSeek V4 Pro pricing, 5 reviewers cost pocket change. The quality gain is real.

## When to Use

- After a card set passes pre_review_audit.py and single-critic review
- When Joe wants "the best possible pass" before he reviews
- When a set graded B/B+ and you want to push to A- before surfacing
- For lore documents, process docs, or any creative artifact

## The Five Lenses

### 1. Tone Reviewer
**Question:** "Do these cards sound like [faction]?"
- Card names: do they match the era and faction voice?
- Flavor text: right register, right rhythm, right emotional tone?
- Rules text: professional and clear without losing faction character?
- Hero dialogue: does each hero sound distinct?
- **Grading:** Pass (80%+ cards hit the voice) / Marginal (60-80%) / Fail (below 60%)

### 2. Design Reviewer
**Question:** "Are the mechanics interesting and distinct?"
- Signature mechanic: is it well-distributed and well-supported?
- Individual cards: any boring/auto-include/never-play?
- Synergy edges: are they real or paper?
- Cross-faction: is this distinct from other factions' mechanics?
- Play patterns: can you see interesting decisions?
- **Grading:** Pass / Needs specific fixes / Fundamentally flawed

### 3. Identity Reviewer
**Question:** "Do the cards feel like the faction they claim to be?"
- Crew-mechanic alignment: Hustle on Street, Paid on Professionals?
- CAN/CANNOT enforcement: any crew bleed?
- Daily life texture: do cards convey the faction's world?
- Emotional truths: does winning with this deck FEEL like the lore promises?
- Blind spot respect: are weaknesses load-bearing or cosmetic?
- **Grading:** Identity-locked (cards ARE the faction) / Adequate (mostly aligned) / Drift (cards contradict identity)

### 4. Flavor Reviewer
**Question:** "Do names, flavor text, and art direction cohere?"
- Name quality: punchy, memorable, era-appropriate?
- Flavor text: does it reward attention? Is it specific, not generic?
- Ludonarrative: does the card DO what the name and flavor PROMISE?
- Naming conventions: Professionals use epithets/role-names, Street uses nicknames?
- Legendary impact: do legendary names carry weight?
- **Grading:** Rich (cards tell a story) / Adequate / Generic (could be any faction)

### 5. MTG Distinctiveness Reviewer
**Question:** "Is this novel or could it be an MTG set?"
- Signature mechanic: does it have a TCG analog? If yes, is the twist sufficient?
- Individual cards: any that feel like MTG reprints with new names?
- Deck archetypes: do they play differently from MTG equivalents?
- Resource system: does the Villium/Contract/Ammo system create different decisions?
- Player fantasy: is the emotional experience distinct from MTG color pie?
- **Grading:** Defensible novel / Adequate twist / MTG with different names

## How to Execute

### Step 1: Spawn Reviewers in Parallel

Use `delegate_task` with tasks array (max 3 concurrent). If 5 reviewers, run two batches:

**Batch 1 (3 parallel):**
```
delegate_task(tasks=[
  {
    goal: "Tone review of [faction] card set",
    context: "Read the card set at [path]. Review every card for faction voice...",
    toolsets: ['file']
  },
  {
    goal: "Design review of [faction] card set",
    context: "Read the card set at [path]. Review every card for mechanical quality...",
    toolsets: ['file']
  },
  {
    goal: "Identity review of [faction] card set",
    context: "Read the card set at [path] and the identity bible at [bible_path]...",
    toolsets: ['file']
  }
])
```

**Batch 2 (2 parallel, after Batch 1 completes):**
```
delegate_task(tasks=[
  {
    goal: "Flavor review of [faction] card set",
    context: "Read the card set at [path]...",
    toolsets: ['file']
  },
  {
    goal: "MTG Distinctiveness review of [faction] card set",
    context: "Read the card set at [path]...",
    toolsets: ['file']
  }
])
```

### Step 2: Synthesize Findings

Read all reviewer outputs. Produce a unified report:

```
## Multi-Perspective Review — [Faction]

### Summary
- Tone: [Pass/Marginal/Fail] — [one-line]
- Design: [Pass/Needs fixes/Flawed] — [one-line]
- Identity: [Locked/Adequate/Drift] — [one-line]
- Flavor: [Rich/Adequate/Generic] — [one-line]
- Distinctiveness: [Novel/Twist/Derivative] — [one-line]

### Consensus Findings
[Issues flagged by 3+ reviewers — these are real]

### Divergent Findings
[Issues flagged by only 1 reviewer — flag for judgment]

### Top 5 Fixes
[Ranked by impact. What would move the needle most?]

### Verdict
[SHIP / ITERATE with N fixes / BACK TO SPEC]
```

### Step 3: Surface to Joe

Joe sees the unified report. He does NOT see the 5 individual reviewer outputs (unless he asks). The synthesis IS the product.

## Reviewer Prompt Templates

### Tone Reviewer Prompt
```
You are a tone critic for the [faction] faction of Five Crests, a TCG set in 1961 Detroit.

Read the card set at [path]. For EVERY card, evaluate:
1. Name: Does it sound like it came from [faction]? Match the era?
2. Flavor text: Right register? Right emotional tone? Specific, not generic?
3. Rules text: Professional and clear without losing faction character?
4. Hero dialogue: Does each hero sound distinct?

Output: severity-graded findings (Critical/Major/Minor), overall grade (Pass/Marginal/Fail), top 5 worst offenders with suggested fixes.
```

### Design Reviewer Prompt
```
You are a mechanical design critic for the [faction] faction.

Read the card set at [path]. Evaluate:
1. Is the signature mechanic well-distributed and well-supported?
2. Any boring cards? Auto-include? Never-play?
3. Are synergy edges real (playable) or paper (theoretical)?
4. Play patterns: can you see interesting decisions?
5. Cross-faction: is this mechanically distinct from [list other factions]?

Output: severity-graded findings, grade, worst offenders with fixes.
```

### Identity Reviewer Prompt
```
You are an identity coherence critic for the [faction] faction.

Read the card set at [path] AND the identity bible at [bible_path]. Evaluate:
1. Crew-mechanic alignment: [list crew profiles]. Any bleed?
2. CAN/CANNOT enforcement: any violations?
3. Daily life texture: do cards convey the faction's world?
4. Emotional truths: does winning with this deck FEEL like the lore promises?
5. Blind spot respect: are weaknesses real or cosmetic?

Output: severity-graded findings, grade, worst offenders with fixes.
```

### Flavor Reviewer Prompt
```
You are a flavor critic for the [faction] faction.

Read the card set at [path]. For EVERY card, evaluate:
1. Name quality: punchy, memorable, era-appropriate?
2. Flavor text: does it reward attention? Specific and grounded?
3. Ludonarrative: does the card DO what the name and flavor PROMISE?
4. Naming conventions: [Professionals = epithets/role-names, Street = nicknames, etc.]

Output: severity-graded findings, grade, worst offenders with fixes.
```

### MTG Distinctiveness Reviewer Prompt
```
You are a TCG originality critic. Your job: protect Five Crests from being "MTG with different names."

Read the card set at [path]. Evaluate:
1. Signature mechanic: does it have a TCG analog? If yes, is the Five Crests twist sufficient?
2. Any cards that feel like MTG reprints with new names?
3. Do deck archetypes play differently from MTG equivalents?
4. Player fantasy: is the emotional experience distinct from MTG color pie?

Output: severity-graded findings, grade, specific cards that need differentiation.
```

## Pitfalls

- **Reviewers need complete context.** Include faction identity bible, crew profiles, CAN/CANNOT lists, naming conventions, and the full card set. Sub-agents have zero memory.
- **Don't let reviewers redesign.** They critique. They don't rewrite cards. Their output is findings, not new text.
- **Synthesize before surfacing.** Joe doesn't want 5 separate reports. One unified synthesis.
- **Three concurrent max.** If 5 reviewers, two batches. Don't try to spawn 5 at once — it'll fail.
- **Prioritize consensus.** Issues flagged by 3+ reviewers are real. Issues flagged by 1 reviewer might just be taste.

## Changelog

**2026-06-08** — Initial creation. Derived from Joe's "4-5 reviewer sub-agents" concept (June 8 process architecture session) and the proven single-critic pattern from Trigger v7 and Faceless v2 runs.
