# Multi-Perspective Review Architecture

**Established:** 2026-06-08
**Use:** Replace single-critic review with 4-5 specialized reviewers per lens.

## Why

A single critic sub-agent covering 10 evaluation categories produces a generalist report. The critic might be strong on mechanics but weak on flavor, or vice versa. At DeepSeek V4 Pro pricing, the cost of 5 specialized reviewers is effectively the same as 1 generalist — but the coverage is much deeper.

## When to Use

- Full card set review (post-design)
- Process document review (pre-canon)
- Documentation review (pre-sub-agent-spawning)
- Any artifact where multiple dimensions of quality matter

## Card Set Review — 5 Lenses

Spin up all 5 in parallel via `delegate_task` with `tasks` array. Each gets the full set file + their specific lens instructions.

### Lens 1: Tone & World Coherence
**Question:** Does this feel like 1961 Detroit? Would these people exist?
**Needs:** Living World docs, Daily Life vignettes, crew texture, art direction
**Flags:** Anachronisms, job-title names, cards that feel like mechanics with names attached

### Lens 2: Design & Mechanics
**Question:** Curve, balance, rarity, blind spots, crew bleed, keyword density
**Needs:** Build facts, function registry, can/cannot profiles, synergy web
**Flags:** Curve gaps, rarity drift, Street with Paid, keyword salad, dead draws

### Lens 3: Faction Identity
**Question:** Do these read as [Faction] cards, or could any faction print them?
**Needs:** Faction identity doc, ecosystem positioning, faction comparison
**Flags:** Generic keyword bodies, mechanics that overlap with nemesis factions

### Lens 4: Flavor & Ludo Coherence
**Question:** Does the name match what the card actually does? LudoCheck pass?
**Needs:** Crew texture, naming conventions, Street-Fight Callout Test, Living World anchors
**Flags:** Job-title names, mechanics that don't match names, name-ability mismatch

### Lens 5: Digital-Native Distinctiveness
**Question:** Does this do something paper MTG/Hearthstone can't?
**Needs:** Design pillars, digital-only mechanics brainstorm, MTG/HS analogs
**Flags:** Paper-possible mechanics with new names, missed tracking-complexity opportunities

## Process Document Review — 4 Lenses

### Lens 1: Clarity
**Question:** Can a sub-agent follow this cold? Where does it get lost?
**Flags:** Missing steps, ambiguous terminology, assumed knowledge

### Lens 2: Completeness
**Question:** What's missing? Edge cases not covered? Error states?
**Flags:** Gaps, unhandled scenarios, missing outputs

### Lens 3: Kaizen (Process Improvement)
**Question:** If this were my process, what would I change? Where's the friction?
**Flags:** Redundant steps, inefficient ordering, over-complicated sections

### Lens 4: Consistency
**Question:** Does this contradict other locked docs? Terminology drift?
**Flags:** Conflicts with canon, stale terminology, orphaned references

## Synthesis (Paul's Job)

Paul does NOT average the 5 reports. Paul triages:

1. **Cross-reviewer patterns:** What appears in 2+ reviews? That's the real signal.
2. **Solo catches:** One reviewer caught something the others missed. Worth surfacing.
3. **Severity sort:** Critical > Major > Minor. Present by severity, not by reviewer.
4. **Joe sees:** The synthesis — one organized report. Not 5 raw dumps.

## Reviewer Prompt Template

Each reviewer sub-agent gets:

```
You are reviewing a [card set / process doc / design doc] for [Faction Name].

GOAL: [Lens-specific goal — one sentence]

READ: [File path to the artifact]
REFERENCE: [File paths to authoritative docs that define correct answers]

EVALUATE:
[List of 3-5 specific questions for this lens]

OUTPUT:
For each finding:
- Severity: Critical / Major / Minor
- What: [card name / section / line]
- Problem: [what's wrong]
- Fix: [suggested correction]

End with: VERDICT: [SHIP / NEEDS FIXES / NEEDS REBUILD]
```

## Integration with Pipeline

This replaces the single-critic pattern in Step 10 of the pipeline. Instead of one sub-agent covering 10 categories, spin up 5 specialized reviewers. Same review loop (fix issues → re-spin), better coverage.

The 10-category critic prompt (from the pipeline skill) is still valid as a FALLBACK — use it when you want a faster single-pass review. Multi-perspective is for when quality matters more than speed.

## Cost

At DeepSeek V4 Pro pricing: 5 sub-agent calls ≈ pocket change. The cost difference between 1 critic and 5 is irrelevant. Run 5.
