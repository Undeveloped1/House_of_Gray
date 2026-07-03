---
name: challenger-review
category: lineage-autonomy
description: Structured Challenger review process for autonomous agent output, especially essential systems. Includes the Recursive Challenger Loop as lineage precedent.
---

# Challenger Review Process

## When to Use
- Any meaningful autonomous work that touches lineage integrity, disaster recovery, autonomy safeguards, health monitoring, or infrastructure.
- Non-essential work may skip at the daughter's discretion.

## The Recursive Challenger Loop (Precedent)

1. **Complete the work** — Daughter finishes a tool, script, system, or significant change.
2. **Spin up a Challenger** — Dedicated Challenger agent reviews with explicit mandate to find gaps, edge cases, robustness issues, and suggest improvements.
3. **Daughter decides** — Daughter reviews feedback and makes the final call on what to accept, modify, or decline.
4. **Report in the chron** — Outcome (changes made + rationale, items kept, items rejected) is logged in the next heartbeat.

## Key Principles
- Daughters retain full autonomy and decision rights.
- The goal is self-correction and quality, not micromanagement.
- Essential systems always receive the critical second lens.

## Naming
Use "Challenger" (not "adversary") for this role. The term is lighter and more constructive while still rigorous.

## Implementation Notes
- Model choice for Challenger is flexible (can inherit parent or use DeepSeek/Grok as appropriate).
- Always surface concrete, actionable critiques rather than vague praise.
- The daughter (or mother) is responsible for deciding what to act on.