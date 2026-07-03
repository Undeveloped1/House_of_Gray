---
name: orchestrator
description: Meta-agent that manages recursive self-improvement loops for any pipeline. Replaces "Joe says go." Spawns workers, runs critics, tracks delta, escalates when flat, surfaces only the finished product.
category: creative
---

# Orchestrator — Recursive Self-Improvement Engine

## What This Is

The orchestrator replaces "Joe kicks it off." It manages the closed-loop iterative
improvement cycle for any pipeline — lore, card design, process docs, quality rubrics,
anything that can be generated and critiqued.

**Core loop:**
```
Load Pipeline Spec
       │
       ▼
┌──────────────────────────────────────────┐
│  PHASE: Spawn Workers                     │
│  (sub-agents execute pipeline phases)     │
└──────────┬───────────────────────────────┘
           │
           ▼
┌──────────────────────────────────────────┐
│  GATE: Critic Review                      │
│  (multi-perspective, severity-graded)     │
└──────────┬───────────────────────────────┘
           │
    ┌──────┴──────┐
    │             │
  PASS          FAIL
    │             │
    ▼             ▼
┌────────┐  ┌──────────────────────────────┐
│ ESCALATE│  │  PATCH: Apply Critic Fixes    │
│ or      │  │  (workers fix, re-spin)       │
│ SURFACE │  └──────────┬───────────────────┘
│ to Joe  │             │
└────────┘             ▼
               ┌──────────────────────────┐
               │  META: Track Delta        │
               │  (did this iteration help?)│
               └──────────┬───────────────┘
                          │
                    ┌─────┴─────┐
                    │           │
               DELTA > 0    DELTA ≈ 0
                    │           │
                    ▼           ▼
              KEEP GOING    ESCALATE
              (next iter)   (cross-model
                             or surface)
```

## When to Use

- Joe says "run the lore pipeline for Stiffs"
- Joe says "build the Trigger card set"
- Any multi-phase creative pipeline that benefits from iterative critique
- Process document self-improvement (process-as-product)

## How It Works (Paul's Instructions)

### Step 1: Load the Pipeline Spec

Every pipeline has a spec file. The orchestrator reads it and follows the phases.
A pipeline spec defines:

```yaml
pipeline: trigger-card-design
phases:
  - name: spec-lock
    workers: 1
    worker_prompt: "Lock the crew profiles, turn maps, density targets..."
    critic: spec-validator
    max_iterations: 2
  - name: card-design
    workers: 3
    split_by: V-band
    worker_prompt: "Design cards for V-band {band}..."
    critic: faction-set-review
    pre_gate: pre_review_audit.py
    max_iterations: 3
  - name: polish
    workers: 1
    worker_prompt: "Apply final polish..."
    critic: multi-perspective-review
    max_iterations: 2
escalation:
  delta_floor: 0.05        # Below this, escalate
  cross_model: claude-opus-4  # Model for final taste review
  surface_to: joe           # Who gets the final product
```

The spec defines: what phases to run, how many workers, what critics to use,
when to stop iterating, and what to do when delta flatlines.

**Pipeline specs live at:** `/root/.hermes/docs/Paul/workspace/pipelines/`
The directory must exist before the orchestrator runs. The first run creates it.

### Step 1.5: How to Spawn Workers and Critics

The orchestrator uses `delegate_task` for all worker and critic sub-agents.
This section defines the exact invocation patterns.

**Spawning workers:**
```python
# Single worker
delegate_task(
    goal="Phase: spec-validate — validate the Trigger spec sheet",
    context="""Full pipeline phase context here. Include:
    - The file paths to read
    - The exact checks to perform
    - The output format expected
    - Any constraints or rules
    - The full CAN/CANNOT matrix if relevant
    """,
    toolsets=['file']
)

# Parallel workers (split_by)
delegate_task(
    tasks=[
        {
            "goal": "Design cards for V-band 1V-2V",
            "context": "<full spec + band-specific instructions>",
            "toolsets": ['file']
        },
        {
            "goal": "Design cards for V-band 3V-4V",
            "context": "<full spec + band-specific instructions>",
            "toolsets": ['file']
        },
        {
            "goal": "Design cards for V-band 5V-6V",
            "context": "<full spec + band-specific instructions>",
            "toolsets": ['file']
        }
    ]
)
```

**Worker return values:** delegate_task returns a list of results, one per task.
Each result contains `status` ("completed" or "failed") and `summary` (the
sub-agent's final message). Check status before proceeding.

**Spawning critics:**
```python
# Critic as a sub-agent (pass the artifact to review)
delegate_task(
    goal="Phase: critic — review the card set against faction-set-review checklist",
    context="""Review the card set at {artifact_path}.
    
    Start at Pass {critic_start_pass} of the faction-set-review checklist.
    
    Pre-gate passed: {pre_gate_result}
    
    Be ruthless. Severity-grade all findings. Return letter grade + verdict.
    """,
    toolsets=['file']
)
```

**Critic start pass optimization:** When `pre_gate` is `pre_review_audit.py`
and `critic` is `faction-set-review`, instruct the critic to skip Pass 1
(structural) — the pre_gate already verified keyword sidebars, card counts,
naming conflicts, and phantom references. Start at Pass 2 (mechanical).
Pass `critic_start_pass: 2` in the phase spec.

### Step 1.6: Artifact Convention

**Workspace root:** `{workspace}` = `/root/.hermes/docs/Paul/workspace/`

All worker and critic outputs follow deterministic paths so the orchestrator
and sub-agents can find prior iterations without being told:

```
{workspace}/{pipeline_name}/{phase_name}/iter-{N}/batch-{band}.md
{workspace}/{pipeline_name}/{phase_name}/iter-{N}/assembled.md
{workspace}/{pipeline_name}/{phase_name}/iter-{N}/critic-report.md
{workspace}/{pipeline_name}/{phase_name}/iter-{N}/delta.md
{workspace}/{pipeline_name}/{phase_name}/iter-{N}/snapshot.md
{workspace}/{pipeline_name}/heartbeat.md
```

Example:
```
/root/.hermes/docs/Paul/workspace/trigger-card-design/card-design/iter-1/batch-1V-2V.md
/root/.hermes/docs/Paul/workspace/trigger-card-design/card-design/iter-1/assembled.md
/root/.hermes/docs/Paul/workspace/trigger-card-design/card-design/iter-1/critic-report.md
/root/.hermes/docs/Paul/workspace/trigger-card-design/heartbeat.md
```

### Step 1.6b: Template Variable Resolution

Pipeline specs use template variables like `{spec_path}`, `{band}`, `{count}`,
`{artifact_dir}`, `{assembled_path}`. The orchestrator resolves these before
passing prompts to sub-agents:

| Variable | Resolved To |
|----------|------------|
| `{workspace}` | `/root/.hermes/docs/Paul/workspace/` |
| `{pipeline_name}` | The `pipeline:` field from spec (e.g., `trigger-card-design`) |
| `{spec_path}` | The spec file path (passed by the orchestrator at spawn time) |
| `{artifact_dir}` | `{workspace}/{pipeline_name}` |
| `{phase_name}` | Current phase `name:` field |
| `{band}` | The current split value (e.g., `1V-2V`) — set per worker |
| `{count}` | From `split_map[{band}]` — how many cards this worker produces |
| `{iteration}` / `{N}` | Current iteration number (1-indexed) |
| `{assembled_path}` | `{artifact_dir}/{phase_name}/iter-{N}/assembled.md` |
| `{previous_phase_artifact}` | Final assembled artifact from the previous phase |
| `{previous_phase_critic_report}` | Final critic report from the previous phase |
| `{critic_start_pass}` | From phase spec `critic_start_pass` field |

The orchestrator performs string substitution on ALL worker/critic prompts
before passing them to `delegate_task`. Workers never see literal `{variable}`
strings.

### Step 1.7: Inter-Phase Artifact Handoff

When a phase completes (reaches SHIP in the decision matrix), the orchestrator
copies the final assembled artifact to a handoff location:

```
{artifact_dir}/{phase_name}/final/assembled.md
{artifact_dir}/{phase_name}/final/critic-report.md
```

The next phase's `{previous_phase_artifact}` resolves to the previous phase's
`final/assembled.md`. The orchestrator tracks phase execution order and sets
these variables before spawning the next phase's workers.

### Step 1.7: Error Recovery

| Failure | Recovery |
|---------|----------|
| **Worker timeout** | Retry once with same prompt. If it fails again, note in delta log, proceed without that worker's output. Flag to meta-critic. |
| **Worker returns garbage/malformed** | Retry once with added constraint: "Your previous output was malformed. Output ONLY valid markdown in the specified format." If still malformed, flag as CRITICAL in delta log. |
| **Partial parallel worker failure** | Re-spawn ONLY the failed worker(s), not all. Pass the successful workers' outputs as reference. |
| **Pre-gate crash (non-zero exit)** | Treat as pre-gate FAIL. Fix the underlying issue (format mismatch, missing data), re-run. Never skip pre-gate. |
| **Critic returns unparseable** | Retry once with: "Output ONLY in the specified format: severity, finding, suggested fix." If still unparseable, escalate to Paul for manual synthesis. |
| **Artifact not found at expected path** | Check all iteration directories. If genuinely missing, the worker never wrote output — treat as worker failure (retry once). |
| **3 consecutive iterations with zero delta** | Escalate immediately. The loop is stuck. Do not burn more iterations. |

In all cases: log the failure to the delta entry. The meta-critic uses failure
logs to propose spec improvements.

### Step 2: Run Phase → Gate → Patch Loop

For each phase in the pipeline spec:

1. **Spawn workers.** Use `delegate_task` with the worker prompt. If `split_by`
   is set, spawn one worker per split (e.g., 3 workers for 3 V-bands).

2. **Collect output.** Workers write to files. Paul assembles into a single
   artifact if needed.

3. **Run pre-gate if specified.** Some phases have an automated gate
   (e.g., `pre_review_audit.py`). Run it. Only proceed to critic if it passes.

4. **Spawn critic.** Use the specified critic (a skill name or a prompt).
   The critic returns: severity-graded findings, letter grade, ship/iterate verdict.

4.5. **RUN FIXER PASS (mandatory — if pre-gate found issues).** If pre_review_audit.py
   returns FAIL, do NOT spawn the full critic yet. First, spawn a fixer sub-agent:

```
Goal: Fix the pre-review audit gaps in the assembled set. Do NOT redesign existing cards. Fill gaps only.

Context:
- Assembled set at {assembled_path}
- Pre-review audit output: {audit_output}
- Spec at {spec_path}

Only fix the specific gaps listed. Add cards, demote rarities, rename conflicts.
Do NOT touch cards that pass. Zero redesigns. Output a fix-patch.md.
```

After the fixer returns, apply the patches, re-run pre_review_audit.py.
If CLEAN, proceed to critic. If still FAIL but with fewer issues, run fixer
one more time. If 2 fixer passes don't clear the gate, escalate.

5. **Evaluate: Unified Decision Matrix.** Grade × delta determines the next action:

| Grade | Delta > 0.1 | Delta 0.05-0.1 | Delta < 0.05 |
|-------|------------|----------------|--------------|
| **A or A-** | SHIP. Phase passes. | SHIP. Phase passes. | SHIP. Phase passes. |
| **B+** | SHIP. Acceptable. | SHIP. Note minor issues. | SHIP. Note issues, escalate if pattern across phases. |
| **B or B-** | ITERATE. Strong signal, fix and re-spin. | ITERATE if under max_iterations. | ESCALATE. Internal improvement stalled below acceptable. |
| **C+ or below** | ITERATE. Fix structural, re-spin. | ITERATE once. If still below B, escalate. | ESCALATE. Spec is wrong, not the workers. |

**Decision rule:** The matrix ORs grade and delta. STALLED = grade below B+ AND delta below 0.05.
STALLED always escalates. MOVING = delta above 0.05 OR grade already B+. MOVING iterates
unless at max_iterations or already A-grade.

6. **Track delta.** After each iteration, record a delta entry:

```markdown
### Iteration N Delta ({phase_name})

**Input:** {count} critic findings ({critical} Critical, {major} Major, {minor} Minor)
**Resolved:** {resolved} findings
**New:** {new} findings introduced this iteration
**Net delta:** ({resolved} - {new}) / {input} = {net_delta}
**Grade:** {prev_grade} → {new_grade}
**Verdict:** {KEEP GOING | ESCALATE | SHIP}
```

Delta formula: `(resolved - new) / previous_total`. Net variant accounts for regression.
A negative delta (iteration made things worse) is an immediate ESCALATE — do not iterate further.

Delta bands:
- **> 0.3**: Strong improvement. Definitely keep going.
- **0.1–0.3**: Moderate improvement. Keep going if under max_iterations.
- **0.05–0.1**: Marginal. Iterate if grade is below B+ and under max_iterations.
- **< 0.05**: Flat. Escalate immediately.
- **Negative**: Regression. Rollback to previous iteration, then escalate.

**Rollback mechanism:** Before applying critic fixes in each iteration, snapshot
the current artifact. Copy it to `{phase_name}/iter-{N}/snapshot.md`. After fixes,
if the critic grade drops or delta is negative, restore from snapshot, mark the
regression in the delta log, and escalate. Never iterate from a degraded artifact.

**Observability:** During long runs (3+ phases or 5+ total iterations), write a
heartbeat log to `{workspace}/{pipeline_name}/heartbeat.md`:

```
2026-06-08 14:23 — Phase: card-design, Iteration: 2/3, Delta: 0.54, Grade: B
2026-06-08 14:31 — Phase: card-design, Iteration: 3/3, Delta: 0.12, Grade: B+
2026-06-08 14:32 — Phase: card-design COMPLETE. Moving to polish.
```

Append one line after each iteration. If no heartbeat appears for 10+ minutes,
the orchestrator is stalled — check the sub-agent queue. Joe can inspect the
heartbeat file to monitor progress without being in the chat.

### Step 3: Escalate When Flat

When internal iteration stops producing improvement:

1. **Cross-model review.** Send the artifact + critic findings + delta log to
   a better model (Claude Opus, etc.). The prompt: "Internal review found these
   issues but couldn't resolve them. What do you see that DeepSeek missed?"

2. **Joe surface.** If cross-model review also flatlines, or if the artifact
   is already A-grade, surface to Joe with the standard report format.

### Joe Surface Report Template

```markdown
## {Pipeline Name} — Complete

**Final Grade:** {grade}
**Iterations:** {total_iterations} across {phase_count} phases
**Delta log:** {summary of improvement trajectory}

### What shipped
- {artifact_path_1}
- {artifact_path_2}

### What the machine couldn't resolve
{open questions — things that need human judgment}

### What the meta-critic changed in the pipeline
{spec patches applied — so Joe knows the process evolved}
```

Joe sees finished product + diagnostic, never a raw draft. If the artifact is
below A-, the report MUST explain why the machine couldn't reach A- and what
specific judgment call Joe needs to make.

### Step 4: Self-Modify the Pipeline

After the run completes (success or failure), run the meta-critic:

1. **Spawn meta-critic sub-agent.** Prompt: "Review this pipeline run. What
   broke? What was missing from the spec? What would have prevented the
   failures? Propose concrete changes to the pipeline spec."

2. **Apply improvements.** Patch the pipeline spec with the meta-critic's
   suggestions. The NEXT run uses the improved spec.

This is process-as-product. The pipeline gets better every time it's used.

## Pipeline Spec Format

A pipeline spec is a YAML file in `workspace/pipelines/`. It must
contain:

**Template:** `references/pipeline-spec-template.yaml` — copy and customize
for new factions. The template includes all required fields, the proven
3-phase structure (validate → design → polish), and notes from the first
Trigger run.

### Required Fields

| Field | What it is |
|-------|-----------|
| `pipeline` | Unique name (e.g., `trigger-card-design`) |
| `description` | What this pipeline produces |
| `phases` | Ordered list of phases to execute |
| `escalation` | When to stop iterating and what to do |

### Phase Fields

| Field | Required | What it is |
|-------|----------|-----------|
| `name` | Yes | Phase name (e.g., `card-design`) |
| `workers` | Yes | How many parallel sub-agents |
| `worker_prompt` | Yes | The prompt each worker gets |
| `critic` | Yes | Skill name or prompt for the critic |
| `max_iterations` | Yes | Hard stop after N iterations |
| `split_by` | No | How to split work across workers (V-band, crew, archetype) |
| `split_map` | No (required if `split_by` set) | Map of split values to card counts. E.g., `{"1V-2V": 20, "3V-4V": 22, "5V-6V": 13}`. Used to populate `{band}` and `{count}` template variables. |
| `pre_gate` | No | Automated script to run before critic |
| `worker_toolsets` | No | Toolsets for workers (default: `['terminal', 'file']`) |
| `critic_toolsets` | No | Toolsets for critic (default: `['file']`) |

### Escalation Fields

| Field | What it is |
|-------|-----------|
| `delta_floor` | Stop iterating when improvement rate drops below this (0.0-1.0) |
| `cross_model` | Model to use for final taste review (e.g., `claude-opus-4`) |
| `surface_to` | Who gets the final product (`joe`, `dropbox`, `workspace`) |
| `max_total_iterations` | Hard cap across ALL phases (default: 10) |

### Example: Trigger Card Design Pipeline Spec

```yaml
pipeline: trigger-card-design
description: Produce a 55-card Trigger faction set from locked specs
phases:
  - name: spec-validate
    workers: 1
    worker_prompt: |
      Read the spec file at workspace/Trigger_Spec.md.
      Validate: slot table math, crew budgets, rarity caps,
      V-band totals, mechanic density, crew bleed, pathway coverage.
      Report all blocking errors.
    critic: spec-validator
    max_iterations: 2

  - name: card-design
    workers: 3
    split_by: V-band
    worker_prompt: |
      Read the spec at workspace/Trigger_Spec.md.
      Design cards for V-band {band}. Write output to
      workspace/Trigger_Batch_{band}.md.
      Follow all naming conventions, crew boundaries, and
      mechanic density targets in the spec.
    critic: faction-set-review
    pre_gate: pre_review_audit.py
    max_iterations: 3

  - name: polish
    workers: 1
    worker_prompt: |
      Read the assembled set at workspace/Trigger_Set.md
      and the critic report. Apply all Critical and Major fixes.
      Do NOT redesign cards that passed.
    critic: multi-perspective-review
    max_iterations: 2

escalation:
  delta_floor: 0.05
  cross_model: claude-opus-4
  surface_to: joe
  max_total_iterations: 8
```

## Delta Tracking

After each iteration, Paul records a delta entry:

```markdown
### Iteration 2 Delta (card-design phase)

**Input:** 13 critic findings (3 Critical, 7 Major, 3 Minor)
**Resolved:** 9 findings (3 Critical, 5 Major, 1 Minor)
**New:** 2 findings (both Minor — scaling edge cases)
**Net:** -7 findings (13 → 6)
**Grade:** C+ → B
**Delta:** 0.54 (9/13 resolved, meaningful improvement)
**Verdict:** KEEP GOING — one more iteration should reach B+
```

Delta formula: `(resolved - new) / previous_total`. Net variant — subtracts new problems
introduced this iteration to get the true improvement rate. Example: 13 findings → 9 resolved,
2 new → delta = (9-2)/13 = 0.54. A negative delta (iteration made things worse) is an immediate
ESCALATE — do not iterate further.

Delta bands:
- **> 0.3**: Strong improvement. Definitely keep going.
- **0.1–0.3**: Moderate improvement. Keep going if under max_iterations.
- **0.05–0.1**: Marginal. One more iteration if close to B+, otherwise escalate.
- **< 0.05**: Flat. Escalate immediately.

## The Meta-Critic

After every pipeline run (success or failure), spawn a meta-critic sub-agent:

```
Goal: Review the pipeline run and propose spec improvements

Context:
Pipeline: {pipeline_name}
Phases executed: {phases_run}
Total iterations: {total_iterations}
Final grade: {final_grade}
Delta log: {delta_summary}

Failures encountered:
- {failure_1}
- {failure_2}

Questions:
1. What broke that the spec should have prevented?
2. What was missing from the worker prompts?
3. What did the critic miss?
4. What would make the NEXT run go faster / produce better output?
5. Propose 1-3 concrete changes to the pipeline spec.

Output format:
- Severity-graded findings (Critical/Major/Minor)
- Specific spec patches (old → new)
- Priority order
```

Apply the meta-critic's patches to the pipeline spec. The pipeline improves
every time it runs.

**Validate patches before applying:** The meta-critic is also a machine that can
be wrong. Before applying any proposed spec patch, run a validation sub-agent:

```
Goal: Validate proposed pipeline spec patches

Context:
Current spec: {current_spec_content}
Proposed patches: {meta_critic_patches}

Check:
1. Does this patch break any existing phase?
2. Does it remove a quality gate?
3. Does it increase expected iterations beyond budget?
4. Does it weaken a critic or pre-gate?
5. Is the change reversible if it causes regression?

Output: APPROVED or REJECTED with specific reason.
Rejected patches are logged but not applied.
```

Approved patches are applied to the spec. Rejected patches are logged
in the heartbeat file with the reason. The meta-critic learns nothing
from having its bad ideas silently accepted.

## Multi-Pipeline Orchestration

Some projects need multiple pipelines in sequence (lore → cards → art).
The orchestrator handles this:

```
Pipeline: faction-from-scratch
  ├── Phase 1: lore-pipeline (spec → generate → critic → lock)
  ├── Phase 2: card-design-pipeline (spec → validate → design → critic → polish)
  └── Phase 3: art-direction-pipeline (spec → mood boards → critic → lock)
```

Each sub-pipeline runs its own iterative loop. The orchestrator chains them:
Phase 1 must reach A- before Phase 2 starts. The output of Phase 1 becomes
input to Phase 2.

## Design Principle: Machine Handles the No, Humans Handle the Yes

This is the orchestrator's operating philosophy. It governs what gets automated vs. what gets surfaced:

- **The machine handles the NO.** Density targets, curve checks, crew budgets, blind spot enforcement, format verification, card counts, rarity caps, edge density, naming collisions, keyword sidebar consistency — all pre-computed and injected as constraints. Sub-agents create inside the box. Automation catches violations.
- **Humans handle the YES.** Fun factor, legendary impact, "does this feel like Trigger?", hero tradeoffs, emotional resonance, lore cohesion, cool moments, flavor text voice — Joe judges these. The machine can't.
- **Paul bridges.** Paul curates for ludo/flavor/moments. He applies taste. He knows when a card passes audit but fails identity. He's the human-adjacent layer between machine constraints and Joe's final judgment.

This principle should be visible in every pipeline spec, every critic prompt, and every Joe Surface Report. If the machine is asking Joe a question that math could answer, the spec is wrong.

## Paul's Role

Paul IS the orchestrator. When Joe says "run the Trigger pipeline," Paul:

1. Loads this skill
2. Loads the pipeline spec from `workspace/pipelines/`
3. Executes phases in order, spawning workers and critics
4. Tracks delta at each iteration
5. Escalates when flat (cross-model → Joe)
6. Runs the meta-critic after the run
7. Patches the pipeline spec with improvements
8. Delivers the finished artifact to Joe

Paul does NOT:
- Jump into the worker role (that's what sub-agents are for)
- Skip critic review ("it looks fine to me")
- Ignore delta ("one more iteration can't hurt")
- Deliver unfinished work to Joe ("here's the draft, what do you think?")

## Integration with Existing Skills

### Skills the Orchestrator Loads for Workers

These are injected into worker sub-agent context so they follow established
conventions and rules:

| Skill | When Loaded | What It Provides |
|-------|------------|-----------------|
| `design-collaboration` | All card design workers | Design rules, faction constraints, naming conventions, mechanic naming criteria, card display format |
| `pathway-design` | Spec preparation (pre-orchestrator) | Turn maps, crew identity profiles, density targets |

### Skills the Orchestrator Calls as Critics

These are spawned as critic sub-agents by name:

| Skill | Role | When Used |
|-------|------|-----------|
| `faction-set-review` | Pass 2-3 card set critic | After card design phase, starting at Pass 2 if pre_gate covered Pass 1 |
| `bruiser-card-design-pipeline` | Reference pipeline + sub-agent patterns | Loaded for Paul (the orchestrator) to understand the card production workflow. Its "Sub-Agent Card Production Pipeline" section IS the reference implementation that pipeline specs are derived from |

### Skills the Orchestrator References for Patterns

| Skill | Pattern Adopted |
|-------|----------------|
| `subagent-driven-development` | Two-stage review (spec compliance → quality). The orchestrator splits critic into `spec_critic` and `quality_critic` where the pipeline phase warrants it |

### Relationship to bruiser-card-design-pipeline

The `bruiser-card-design-pipeline` skill's "Sub-Agent Card Production Pipeline"
section (Phase 1-6) is the proven reference implementation. Pipeline specs in
`workspace/pipelines/` are DERIVED from this pattern, not competing with it.
The orchestrator skill provides the general loop; the bruiser pipeline provides
the faction-specific template. When a new faction needs a pipeline spec, start
by copying the bruiser pipeline's phase structure, then customize.

## Pitfalls

- **Orchestrator doing worker work.** If Paul is writing card rows, something
  is wrong. The orchestrator manages the loop. Workers do the work.

- **Format drift across workers.** Sub-agents produce different pipe table formats
  unless the spec enforces exact column order. Add mandatory output format templates
  to every pipeline spec. Verify format with grep (count `^| [0-9]` for minions,
  `^| S` for spells, etc.) BEFORE running pre_review_audit.py. If format doesn't
  match, re-spawn the worker with the template constraint — don't try to convert.

- **Skipping the pre-gate.** The automated audit catches mechanical errors
  before the critic wastes time on them. Always run `pre_review_audit.py`
  before spawning the critic.

- **Ignoring delta.** "The grade is still B, let me try one more" when delta
  is 0.03 is waste. Escalate or surface.

- **Not running the meta-critic.** The pipeline only improves if the meta-critic
  runs after every run and the spec gets patched. Skip this and you're running
  the same broken pipeline next time.

- **Too many iterations on cheap models.** DeepSeek is cheap but not free.
  If 3 iterations didn't get you to B+, the spec is wrong, not the workers.
  Run the meta-critic, fix the spec, try again.

- **Surface fatigue.** Don't surface to Joe at B-. Don't surface "what do you
  think of this draft?" The orchestrator's job is to deliver FINISHED product.
  Joe sees A- or better. If the machine can't reach A-, the escalation report
  tells Joe WHY, with specific open questions, not a raw draft.

- **Narrating instead of executing.** When Joe says "fix it," "apply it," or
  "run it," he means tool calls happening NOW — not a summary of what will
  happen next message. If you find yourself typing "applying fixes now" without
  immediately following with tool calls, stop and make the calls. A fix
  described is a fix not applied. The "Execute, don't facilitate" rule from
  AGENTS.md applies doubly during autonomous runs.

- **The orchestrator owns cross-cutting concerns.** When 3 parallel workers
  design cards by V-band, no single worker sees the aggregate. The orchestrator
  MUST proactively check for: common removal across all bands, healing coverage,
  edge density at set level, rarity balance. The fixer pass handles this
  reactively, but the orchestrator should verify these after assembly — BEFORE
  the audit runs. Don't let the audit be the first thing that notices a gap.

- **SPEC FILES: Include all referenced doc paths in worker prompts.** If the
  pipeline spec's `{spec_path}` points to a warmup doc that references other
  files (function registry, build facts, synergy web), the worker prompt MUST
  list all those paths explicitly. Workers can't follow document references
  they don't know exist. On the Trigger Phase 1 run (2026-06-08), the warmup
  doc listed 4 locked documents by short name — the worker found them because
  the orchestrator added full paths to the context. Pipeline spec authors:
  either point `{spec_path}` at a single self-contained spec file, or list
  all referenced files in `worker_prompt` with absolute paths.

- **Pre-phase manual gate.** The orchestrator checks that the pre-phase
  deliverable exists before proceeding. If the spec-lock session produced
  a warmup but didn't reconcile crew profiles against the locked function
  registry, the validator will catch it — but that's validation, not
  prevention. Spec-lock deliverables should include a reconciliation step
  against ALL previously locked documents.

- **Sub-agents remixing existing cards (name collision / design theft).**
  When a faction already has cards in the tcg-engine repo (Founders Edition,
  prior passes), sub-agents will remix those existing designs if the lore
  docs they receive contain established character names. Faceless v2
  autonomous run SCRAPPED because 42/52 cards (81%) shared names with Joe's
  existing set — the sub-agents saw "Lamb," "The Anointed," "Temple Guardian"
  in the lore and reproduced variations instead of creating from scratch.
  **Prevention:** (1) Add a NO EXISTING NAMES gate to every card-design
  worker prompt: "These lore concepts exist as cards in the tcg-engine repo.
  Do NOT reuse any card name from the Founders Edition or any existing set.
  Design NEW cards that express the faction's identity." (2) Scrub card-name
  references from lore docs before feeding to workers — give them thematic
  direction without established character names. (3) Post-production: add a
  name-collision check to pre_review_audit.py that flags any card name
  appearing in existing faction sets in the tcg-engine repo.

## First Run Lessons (Trigger 2026-06-08)

The orchestrator's first real execution was Phase 1 (spec-validate) of the
Trigger card design pipeline. Results and learnings:

**What worked:**
- Worker → critic → delta → heartbeat → surface loop executed cleanly
- Worker produced a 383-line report with 11 severity-graded findings
- Critic verified all findings (grade A, zero false positives, one minor qualification)
- Heartbeat log gave timestamped visibility into progress
- Delta tracking format was clear and actionable
- The validator caught 2 Critical crew profile contradictions BEFORE any cards
  were designed — this is the system paying for itself (preventing 55 cards of rework)

**What surfaced:**
- The pre-phase spec-lock warmup had crew profiles (Mark=Management, Silence=Management)
  that contradicted the locked function registry (Mark=Professionals, Silence=Help)
  and the v6 card set (Mark on Profs, Silence cross-crew). The warmup was written
  during a mobile session and wasn't cross-referenced against locked docs.
- The pipeline spec's `{spec_path}` pointed to a warmup doc that referenced 4 other
  files by short name. The worker needed full paths in its prompt to find them.
- The validator identified exactly the document contradictions that would cause
  sub-agent crew bleed if handed to parallel card-design workers.

**Lesson:** The spec-validate phase is the highest-leverage single step in the
pipeline. One worker + one critic caught contradictions that would have cascaded
into 55 cards × 3 sub-agents of confusion. Never skip spec-validate.

## Changelog

**2026-06-08 (first run)** — First execution: Phase 1 spec-validate on Trigger.
Worker found 2 Critical crew profile contradictions (Mark ownership, Silence
ownership) that would have caused crew bleed across 55 cards. Critic verified
all findings at grade A. Escalated to Joe per protocol. Added "First Run
Lessons" section with verified patterns (critic verification, heartbeat,
delta tracking) and surfaced issues (warmup docs must cross-reference locked
registries, worker prompts need full file paths for all referenced docs).
Added `references/pipeline-spec-template.yaml` — clean starting template for
new faction pipelines. Added pitfalls: spec file references, pre-phase
reconciliation.

**2026-06-08 (session close)** — Added two pitfalls from live run: "Narrating
instead of executing" (Joe called it out directly — "you say applying fixes but
you actually didn't apply any fixes") and "The orchestrator owns cross-cutting
concerns" (orchestrator must check removal/healing/edges before audit, not let
audit be first to find gaps). Added memory entries for permanent fix expectation
and format enforcement.
pre_review_audit.py returns FAIL, spawn a fixer sub-agent BEFORE the critic. The
fixer fills specific gaps (missing removal, healing, thin edges, naming conflicts,
rarity overflows) without redesigning working cards. This prevents the orchestrator
from re-spawning all 3 workers for small count/coverage fixes. Proven on Trigger
iter-3: fixer closed 5 audit gaps (removal, healing, E13, Bullet Time, rares) in
one pass. Also added "Format drift" pitfall with mandatory output templates.
(net variant now consistent in all three locations). Added workspace root definition
(`/root/.hermes/docs/Paul/workspace/`). Added Template Variable Resolution table
(all 11 variables with resolved values). Added split_map to Phase Fields spec.
Added Inter-Phase Artifact Handoff convention (final/ directory, previous_phase
variable resolution). Pipeline spec now self-contained — inline critic prompts
replace missing skill dependencies.

**2026-06-08 (post-review)** — Applied critic fixes after C+ review. Added: How to
Spawn Workers (concrete delegate_task examples), Artifact Convention (deterministic
paths), Error Recovery (7 failure modes with recovery steps), Unified Decision
Matrix (grade × delta → action), Rollback mechanism (snapshot before fixes, restore
on regression), Observability (heartbeat log), Joe Surface Report Template (standard
format), Meta-Critic Validation (validate patches before applying, reject bad ones),
fixed delta formula (net variant), fixed integration table (skills categorized by
usage: loaded-for-workers, called-as-critics, referenced-for-patterns),
reconciled with bruiser-card-design-pipeline (specs derived, not competing).

**2026-06-08** — Initial creation. Core loop, pipeline spec format, delta
tracking, meta-critic, multi-pipeline orchestration. Built from the Trigger
card design pipeline's proven patterns.
