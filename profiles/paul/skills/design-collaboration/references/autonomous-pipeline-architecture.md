# Autonomous Pipeline Architecture

## The Pattern

Every lane (lore, cards, art, naming) follows the same shape:

```
AGENT → produces artifact → CRITIC scores against rubric → iterate until ≥75% → lock
                                                                    ↓
                                                              PROCESS AGENT patches playbooks from failures
                                                                    ↓
                                                              Next faction starts higher
```

## Core Documents

| Document | Location | Role |
|----------|----------|------|
| **Master Scoring Rubric** | `docs/Paul/workspace/Master_Scoring_Rubric_v1_Paul.md` | 6 lanes, 60+ mechanical criteria. Every critic loads this. |
| **Pipeline Orchestrator** | `docs/Paul/workspace/Pipeline_Orchestrator_v1_Paul.md` | Phase 0-5 autonomous factory. Drop in fresh session. |
| **Card Design Warmup** | `docs/Paul/workspace/Faceless_Card_Design_Warmup_2026-06-07_Paul.md` | Card lane warmup template. |
| **Compound Tracker** | `docs/Paul/workspace/COMPOUND_TRACKER.md` | Score tracking across faction cycles. |

## Scoring System

- **0** — Absent. Criterion not addressed.
- **1** — Present but wrong. Contradicts locked canon. Auto-fail.
- **2** — Present and correct but thin. Meets minimum.
- **3** — Ship-ready. Passes "another AI reads only this" test.

## 6 Lanes

1. **Lore A-H** (8 sections, 47 criteria) — Identity bible quality
2. **Canon K** (5 criteria) — Cross-reference against Inner_Circle.md, Territory.md, Playstyle.md
3. **Cards M** (7 criteria) — Mechanical identity, blind spots, rarity, ludonarrative
4. **Art V** (6 criteria) — Profile match, palette, era, occult lock, movement, Villium
5. **Naming N** (5 criteria) — Era, voice, headline test, canon consistency, syllable weight
6. **Process P** (4 criteria) — Patch generation, patch application, compound tracking, human handoff

## Joe Decision Budget

**Target: ≤5 Joe decisions per artifact.** Every decision beyond 5 is a process failure — the critic or rubric should have auto-resolved it. Flavor-depth backstories without mechanical impact should be auto-generated, not deferred to Joe.

## Compound Mechanics

After every faction cycle, the PROCESS AGENT:
1. Reads all critic reports
2. Applies patch candidates to playbooks
3. Logs the change in the playbook's changelog
4. Updates the compound tracker: faction, phase, first score, final score, patches applied

## Proof Run

Faceless lore: v2 FAIL (3 canon contradictions) → v3 140/141 (99.3%). +32% delta in one iteration. The mechanism works.
