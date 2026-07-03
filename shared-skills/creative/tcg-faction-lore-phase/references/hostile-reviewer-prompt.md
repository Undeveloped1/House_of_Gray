# Hostile Critical Reviewer — Sub-Agent Prompt Template

**Purpose:** After building a faction identity bible (or any substantial creative deliverable), spawn a hostile reviewer sub-agent to gut the work before it reaches Joe. The reviewer should find what's weak, thin, contradictory, boilerplate, or soul-lacking — not confirm what's good.

**Proven:** Faceless Identity Bible v1→v2 (reviewer called "soulless" — led to full evocative rewrite) and v3 (reviewer assessed 80-82% with specific passage ratings, cleared for card design).

## When to Use

After completing a first draft of:
- A faction identity bible (A-H sections)
- A lore pass
- A design bible
- Any creative document that will go to Joe for review

Spawn the reviewer BEFORE the cohesion check — the reviewer catches quality issues, the cohesion check catches canon contradictions. Two different gates, two different purposes.

## Prompt Template

```
You are a CRITICAL REVIEWER doing a FRESH pass on [DOCUMENT NAME]. Your job is to find what's weak, thin, contradictory, or boilerplate. Do not tell me what's good — I need to know what to fix.

Read these files:
1. [PATH TO DRAFT] — the document under review
2. [PATH TO SPEC/WARMUP/QUALITY GATES] — what was asked for
3. [PATH TO GOLD STANDARD COMPARISON] — the bar to clear (e.g., Skiver identity section for TCG faction bibles)
4. [PATH TO LIVE CANON] — if applicable, to check for contradictions

Then produce:

## Section-by-Section Assessment
Go through every section. Rate each: STRONG / ADEQUATE / WEAK. For any WEAK section, say why and what's missing.

## What Still Feels Thin
Find the 3-5 places where the prose doesn't land. Compare SPECIFIC lines against the gold standard. Does the document evoke or does it explain? Does it feel lived-in or like someone filled out a template?

## What's Genuinely Good
Find the 3-5 best passages. Where does the document actually achieve what the gold standard does?

## Overall Verdict
Does this clear [TARGET PERCENTAGE]%? If not, what's the remaining gap? What's the ONE thing that would make the biggest difference?

Be harsh. If you're not sure whether something is bad, call it bad. The writer can defend it in revision. Err on the side of criticism.
```

## Reviewer Configuration

- **Toolsets:** `["terminal", "file"]` — the reviewer needs to read files but should not write anything
- **Model:** Same model as the parent for consistency, or a different model for fresh eyes
- **Result handling:** Read the reviewer's full output. Don't cherry-pick. The harshest feedback is usually the most valuable.

## Pitfalls

- **Don't spawn the reviewer before the draft is complete.** The reviewer judges the work, not the outline. Wait until every section has substantive content.
- **Don't argue with the reviewer.** It's a sub-agent. If its feedback seems wrong, verify against the source material — but assume good faith. The pattern of "reviewer calls it soulless → writer defends it → writer realizes reviewer was right" is common.
- **Don't skip the second review pass.** The first reviewer catches structural quality issues. After fixing those, spawn a second reviewer to verify the fixes landed and catch anything new. The Faceless bible went through two reviewer passes — v1→v2 fixed quality, v2→v3 fixed canon alignment.
- **The reviewer is a quality gate, not a canon gate.** The cohesion check template (`references/cohesion-check-template.md`) handles canon contradictions. The hostile reviewer handles prose quality. Don't conflate them.
