# Pipeline Orchestrator — Autonomous Factory
## v1.0 | 2026-06-07 | Paul Build

**Purpose:** Master workflow that spawns sub-agents in sequence, wires critic→patch→compound, and removes human middleware from the TCG design pipeline.

**How to run:** Drop this document into a fresh session. Say "Run Phase 1 for <Faction>." The orchestrator bootstraps, spawns agents, scores, iterates, patches, and hands off.

## Phases

### Phase 0: Bootstrap
Read: Master Rubric, Lore Panel Fast Path, Compendium Build Checklist, faction canon docs (00_INDEX, Inner_Circle, Identity, Territory, Playstyle), set design doc, art pipeline profiles.

### Phase 1: Lore Lane
1. LORE AGENT → produce Identity Bible v1 (A-H checklist, 15-30 pages)
2. LORE CRITIC → score against rubric Lane 1 (Lore) + Lane 2 (Canon). Every score < 2 = patch candidate.
3. Iterate until score ≥ 75%. If canon gate fails, return to step 1 with specific contradictions.
4. Canon gate: Lane 2 must score 100% before proceeding to cards.

### Phase 2: Card Lane
1. CARD AGENT → read locked bible, produce card designs
2. CARD CRITIC → score against rubric Lane 3 (Cards) + Lane 5 (Naming)
3. Iterate until pass rate ≥ 75%

### Phase 3: Art Lane
1. ART AGENT → produce art direction brief from bible Section G
2. ART CRITIC → score against rubric Lane 4 (Art)

### Phase 4: Process Lane
1. PROCESS AGENT → read all critic reports, collect patch candidates, apply patches to playbooks
2. Compound tracking: add row to COMPOUND_TRACKER.md
3. PROCESS CRITIC → score against rubric Lane 6 (Process)

### Phase 5: Human Handoff
1. Collect all DESIGNER DECISION NEEDED flags. Target ≤ 5.
2. Drop everything to workspace + Syncthing: identity bible, card designs, art brief, critic reports, patch log, Joe decision batch.

## Anti-Patterns
- Don't run Phase 2 before Phase 1.4 passes (canon gate)
- Don't auto-resolve canon contradictions — flag them
- Don't let critic be nice — a critic that gives all 3s is broken
- Don't skip Phase 4 — without it, compound doesn't compound
- Don't merge Joe decisions with auto-decisions
- Don't run more than 3 iterations per phase — if not converged by v3, rubric or agent is broken
- The boring work IS the work — every criterion scored, every patch applied, every compound logged
