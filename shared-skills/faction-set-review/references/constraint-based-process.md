# Constraint-Based Card Design Process v2

**Status:** **CANONICAL PROCESS.** Replaces slot-filling with constraint-based design.
**Date:** 2026-06-07
**Reference:** `playbooks/CARD_DESIGN_PROCESS_v2.md` for the full document.

This reference is a condensed summary for the `faction-set-review` skill context.

## Core Shift

Old: Functions → Synergy Web → Slot Table → Fill Slots → Review → Iterate
New: Identity → Pathways → Density → Constraints → Subagent Batches → Review → Ship

The machine handles the no. The humans handle the yes.

## Key Tools

| Tool | Phase | What It Does |
|------|-------|-------------|
| `faction-identity-gate` | Phase 1 | 10-dimension scored gate. Is the concept worth building? |
| `density_calc.py` | Phase 2 | Hypergeometric distribution. How many copies for 90% draw? |
| `pre_review_audit.py` | Phase 3 | Automated mechanical gate. 11 checks. Exit 0 = clean. |
| `faction-set-review` | Phase 3 | Three-pass critic checklist. B+ ships. |

## Design Principles

1. **Constraint-based, not slot-filling.** The subagent receives a box. Creativity is inside it. Math is never in context.
2. **Pathway-first, not card-first.** Design the archetype turn map. Derive density targets. THEN design cards.
3. **Crew-grounded, not mechanic-grounded.** Every card answers: who is this person? What's their job? What do they NEVER do?
4. **Math is pre-calculated.** Density, curve, stat budgets — computed before the first card name.
5. **Subagents design, Paul curates.** Parallel batches. Multiple candidates per slot. Paul picks the best.
6. **The critic is a gate, not a fix-it loop.** Sets passing `pre_review_audit.py` should score B+ on first critic pass.
