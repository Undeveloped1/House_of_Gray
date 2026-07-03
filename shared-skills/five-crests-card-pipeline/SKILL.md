---
name: five-crests-card-pipeline
description: "Master skill for the Five Crests card design pipeline. Load when Joe says 'build cards for [faction]' or 'run the pipeline.' Orchestrates the full stack from identity gate through compound tracking."
category: creative
---

# Five Crests Card Design Pipeline — Master Skill

## What This Is

The complete end-to-end process for producing a 55-card Five Crests faction set from locked lore through autonomous sub-agent production. This skill ties together the orchestrator, faction-identity-gate, pathway-design, faction-set-review, density_calc.py, and pre_review_audit.py.

**Proven on:** Trigger v7 (A-, autonomous), Faceless v2 (A-, overnight autonomous)
**Compound trajectory:** Each faction starts higher. Duster projected 85%+ first attempt.

## When to Use

- Joe says "build the [faction] card set"
- Joe says "run the pipeline for [faction]"
- Starting a new faction from locked lore
- Re-running a faction with improved process

## The Process (7 Phases)

### Phase 0: Identity Gate

**Goal:** Confirm the faction is worth building before touching mechanics.

**Steps:**
1. Load `faction-identity-gate` skill
2. Read the faction's lore docs (Identity Bible, Design Bible, Inner Circle, Territory, Playstyle)
3. Score all 10 dimensions (1-5 each)
4. Run the 4 synthesis locks (Mechanic-Villium, Mechanic-Fantasy, Blind Spots-World, Crews-Heroes)
5. Check surprise flag

**Gate:** 40+ total, 0 dimensions below 3, 0 drift locks. Below gate = fix identity. Do not proceed.

**Deliverable:** Scored identity gate report with verdict, ranked gaps, drift-risk flags.

### Phase 1: Spec Lock

**Goal:** Lock EVERYTHING a sub-agent needs before spawning any workers.

**Steps:**
1. Build Function Registry (12-18 functions derived from lore, NOT retrofitted from existing cards)
2. Build Synergy Web (edges between functions with types: Enables, Creates-Spends, Curve Chain, Protects)
3. Lock Build Facts (card count, curve, rarity distribution, crew percentages, legendary slots)
4. Lock Blind Spots (what the faction CANNOT do — 2-3 clear, meaningful constraints)
5. Lock Crew CAN/CANNOT profiles (which crew gets which mechanics)
6. Run `density_calc.py` — confirm draw probabilities for signature mechanics

**Gate:** All documents cross-referenced. No contradictions. Crew profiles reconciled against function registry.

**Deliverable:** Locked function registry, synergy web, build facts, crew profiles.

### Phase 1.5: Build Facts Currency Check (MANDATORY — before Phase 2)

**Goal:** Verify the Build Facts document matches the current design concept before it poisons the slot table, density targets, and spec validation.

**Why this gate exists (2026-06-11):** Trigger Build Facts v1 was built 2026-06-06 on an aggro-midrange concept (5-6 at 1V, 70/30 crew split). Five days and four design pivots later, the faction was midrange-tempo-control (3-8-8-5-4-2 curve, 60/40 split). Paul built the slot table from v1's stale numbers. Density targets were derived from those same stale numbers. Spec validation checked against those targets. Full circular poison — the entire Phase 2-3 stack was built on a foundation from a different design era.

**Steps:**
1. Read the Build Facts document. Note its DATE.
2. Check the curve against the current faction identity. If the faction was originally aggro and is now midrange-control, the curve MUST change.
3. Check the crew split against the most recent Joe-locked decision. If a recut happened (e.g., 70/30 → 60/40), the crew targets MUST change.
4. If ANY of the above changed, rewrite Build Facts FIRST. Then re-derive density targets from the new curve and crew split. Then rebuild the slot table. Then re-validate.
5. Do NOT patch the old Build Facts. Write a NEW Build Facts document with an incremented version number and a "Supersedes" header pointing to the old one. Preserve the audit trail.

**Gate:** Build Facts date ≤ 1 day old AND crew split matches latest Joe lock AND curve matches current archetype. If the faction identity has pivoted since Build Facts was written, it's stale.

**If Build Facts is stale, choose the right fix:** Rewrite it if it carries unique information the other docs don't (matchup spread, curve philosophy blurbs). But if everything in Build Facts is already duplicated in the slot table, warmup, and SubAgent Spec — and its only unique pieces can be absorbed — KILL IT. Don't maintain a doc that exists only because the pipeline template says so. Trigger 2026-06-11: Build Facts had two unique pieces (matchup, curve blurbs). Both merged into warmup + pathway design. Build Facts removed from manifest. The slot table and warmup are the two docs needed for card production; Build Facts was a middleman. See `references/trigger-recut-2026-06-11.md` for the full cascade failure and fix protocol.

**Deliverable:** Fresh Build Facts document or explicit confirmation of currency.

**Goal:** Convert identity into density targets, turn maps, and slot boundaries.

**Steps:**
1. Load `pathway-design` skill
2. Build crew identity profiles (one paragraph each: who they are, what they do, emotional core)
3. Build archetype turn maps (T1-T6 sequence with cross-pathway support)
4. Build slot table:
   - 29 minion rows: each with crew, V-band, rarity, mechanic band, pathway
   - 21 spell slots
   - 5 weapon slots
5. Calculate density targets from slot table

**Gate:** Slot table totals = card count. Crew percentages match targets. Turn maps feasible.

**Deliverable:** Complete Sub-Agent Spec document with all sections. This is the ONE document workers read.

**CRITICAL:** Spec docs must include ALL conversational nuance. Sub-agents only read the spec. If Joe said "Street doesn't get Paid because they're muscle, not accountants" — that reasoning must be in the spec. "NO SURNAMES on Professionals" — not "epithets only."

### Phase 3: Spec Validation

**Goal:** Catch spec errors before they cascade into 55 cards.

**WHEN TO DELEGATE vs DO DIRECTLY:** If the slot table was built autonomously by sub-agents or an orchestrator, spawn a validator sub-agent. If PAUL hand-built the slot table (as in collaborative Joe+Paul design sessions), run the validation checklist directly — you already know the numbers. Counting 30 rows and checking crew tags takes 30 seconds manually. Delegating a checklist you could run yourself is the #1 cause of 5-minute validation stalls that end in interruption. Joe will call it out immediately. **This is a counting task, not a reasoning task. Never delegate counting.**

**Steps:**
1. **If autonomous production:** Spawn a validator sub-agent with `delegate_task`
   **If Paul hand-built:** Run the checklist directly (crew bleed scan, density count, edge coverage, curve/rarity tally)
2. Validator checks:
   - Slot table math (crew budgets, rarity caps, V-band totals)
   - Crew bleed (Street with Paid, Help with Overkill, Management killing)
   - Mechanic density (Mark sources 6-10, Overkill 5-6, Barrage 1-2, Cloak 2-3, Hustle 2-3)
   - Pathway coverage (all three hero lanes represented)
   - Edge coverage (all synergy edges have cards)
   - Naming conventions (Professionals = epithets/role-names ONLY)

**Gate:** 0 Critical findings. Any Critical = fix the spec, re-validate. This is the HIGHEST-LEVERAGE step. Proven: caught 7 blocking errors on Trigger v7, 2 Critical crew contradictions on orchestrator run.

**Deliverable:** Validation report with severity-graded findings.

### Pre-Flight Checklist (MANDATORY — before Phase 4)

Before spawning ANY card-design workers, verify these deliverables exist. This is a hard gate. Do not proceed to Phase 4 without all four.

| # | Check | Deliverable | If Missing |
|---|-------|-------------|------------|
| PF1 | **Phase 0 done** | Scored identity gate report (10 dimensions, 4 synthesis locks, drift-risk flags) | Run `faction-identity-gate`. Do not design cards for a faction that hasn't been identity-verified. |
| PF2 | **Phase 1 done** | Locked function registry, synergy web, build facts, crew CAN/CANNOT | Lock Phase 1 before proceeding. |
| PF3 | **Phase 2 done** | Formal slot table: 29 minion rows each with crew, V-band, rarity, mechanic band, pathway assignment. Plus 21 spell + 5 weapon slots. | Run `pathway-design`. Without a slot table, sub-agents fill slots to hit counts instead of designing to pathway goals. |
| PF4 | **Phase 3 done** | Spec validation report — 0 Critical findings | Run validator. One validator sub-agent caught 7 blocking errors on Trigger v7 that would have cascaded into 55 cards of rework. |

**Why this gate exists:** Trigger v6 and v7 were both scrapped 2026-06-09. Root cause analysis showed Phase 0 (identity gate) was never formally run, and Phase 2 (pathway slot table) was never built as a standalone deliverable. The pipeline jumped from spec lock straight to card production. The cards that came out were mechanically coherent but identity-weak — Joe's verdict: "Garbage in, garbage out." This checklist prevents that failure mode.

### Phase 4: Card Production

**Goal:** 55 cards, designed to the slot table.

**TWO MODES — Joe picks which:**

#### Mode A: Collaborative Band-by-Band (PREFERRED for factions with locked lore)

Joe and Paul design one V-band at a time (1V → 2V → 3V → 4V → 5V → 6V). Per band: present 2-3 card proposals from the slot table (name, mechanic, crew, flavor hook). Joe reacts. Lock or revise.

**Session History Gate (MANDATORY — before designing any band):**

Before running the holistic analysis for a band, verify the band hasn't already been completed in a prior session. Run `session_search` for the faction + band. Look for completion signals: "locked," "update the doc," "put this band to bed," a final card table.

Warmup docs go stale. When the warmup says "first action: holistic 2V analysis" and session history shows the 2V band was locked two days ago on Telegram, session history wins. Trigger 2026-06-12: 2V band was completed June 10 — Paul redesigned it from scratch because he didn't check.

**Canonical output location:** The card set output file lives in the Syncthing dropbox, NOT just workspace. Convention: `/root/syncthing/paul-dropbox/Trigger_Full_Set_v{N}.md`. Warmup docs may reference workspace paths that were never created — the dropbox file is the source of truth.

**Post-lock warmup update:** After a band is locked, immediately update the band warmup doc — replace pre-design slot functions ("Intel Mark," "Hustle body #2") with actual card names ("Front Desk," "Banger"). Change status from "What We're Designing" to "Locked." See `paul-joe-process` §Phase F for the full protocol.

**Required pre-work:** Build a **Card Design Warmup** — a self-contained brief that a new Paul instance can load and start designing from immediately. Must include:
- All locked specs (identity gate score, function registry, synergy edges, build facts)
- Crew CAN/CANNOT matrix
- Living world anchors (one paragraph per crew)
- Full slot table reference
- Naming conventions per crew
- NO EXISTING NAMES directive
- Design philosophy reminders

**Proven:** Trigger 2026-06-11 — warmup at `workspace/Trigger_Card_Design_Warmup_2026-06-11_Paul.md` with companion `Trigger_Daily_Life_By_Crew_2026-06-11_Paul.md` for crew vignettes.

**Why collaborative over autonomous:** Trigger v6 and v7 were both autonomous productions — scrapped 2026-06-09. Sub-agents produced mechanically coherent cards that lacked Joe's taste filter and naming judgment. Collaborative mode keeps Joe in the loop for the creative decisions sub-agents can't make: naming, flavor fit, "does this card *feel* like a Trigger?"

#### Mode B: Autonomous Sub-Agent Production

For factions where speed matters more than polish, or after collaborative mode has proven the pattern.

**Steps:**
1. Load `orchestrator` skill
2. **Novelty Gate (MANDATORY — before spawning any workers):** If the faction already has cards in the tcg-engine repo (Founders Edition, prior design passes), verify:
   - Worker prompts include a NO EXISTING NAMES directive: "These lore concepts may exist as cards in the tcg-engine repo. Do NOT reuse any card name from the Founders Edition or any existing set. Design NEW cards that express the faction's identity."
   - Lore docs fed to workers are scrubbed of established card-name references — give thematic direction without character names where possible. "Lambs" → "vulnerable newcomers who serve as sacrifice fodder."
   - A post-production dedup check is planned: after assembly, grep combined card names against existing faction sets. Flag >50% overlap. Do not ship until verified.
   - **Faceless v2 was SCRAPPED 2026-06-09 because this gate was skipped.** 42/52 cards (81%) shared names with Joe's originals. Legendaries were near word-for-word identical. Never skip this gate.
3. Spawn 3 parallel workers with `delegate_task`:
   - Batch 1: 1V-2V (~20 cards)
   - Batch 2: 3V-4V (~22 cards)
   - Batch 3: 5V-6V (~13 cards)
4. Each worker receives: full Sub-Agent Spec + band-specific instructions + mandatory output format template + NO EXISTING NAMES directive
5. Verify format: grep for pipe table column counts. Mismatch = re-spawn worker with template constraint.
6. Assemble batches into combined set

**Gate:** Format verified. Card count correct. Workers wrote FILES, not summaries. Name collision check passed against existing sets.

**Deliverable:** `assembled.md` — 55 cards in exact pipe table format.

### Phase 5: Automated Audit + Fixer

**Goal:** Mechanical gate before critic review.

**Steps:**
1. Run `pre_review_audit.py` on assembled set
2. If CLEAN → proceed to Phase 6
3. If FAIL → spawn fixer sub-agent:
   - Fixer fills specific gaps (missing removal, healing, thin edges, naming conflicts, rarity overflows)
   - Fixer does NOT redesign working cards
   - Fixer writes `fix-patch.md`
4. Apply fixes, re-run audit
5. If still FAIL after 2 fixer passes → escalate

**Gate:** pre_review_audit.py returns CLEAN (exit 0).

**Deliverable:** Audit-passed assembled set.

### Phase 6: Critic Review

**Goal:** Subjective quality review — what automation can't judge.

**Steps:**
1. Spawn critic sub-agent with `delegate_task`
2. Critic uses `faction-set-review` skill, Pass 2-3 (skip Pass 1 — pre_review_audit.py covered structural)
3. Critic returns: severity-graded findings (Critical/Major/Minor), letter grade, ship/iterate verdict
4. Apply Critical and Major fixes. Do NOT redesign cards that passed.

**Multi-perspective review (optional, recommended):**
For higher quality, spawn 3-5 reviewer sub-agents with different lenses:
- Tone reviewer: "Do these cards sound like [faction]?"
- Design reviewer: "Are the mechanics interesting and distinct?"
- Identity reviewer: "Do the cards feel like the faction they claim to be?"
- Flavor reviewer: "Do names, flavor text, and art direction cohere?"
- MTG Distinctiveness reviewer: "Is this novel or could it be an MTG set?"

Paul synthesizes findings; Joe only reviews the synthesis.

**Gate:** B+ or above ships. Below B iterates (fix + re-spin critic). Max 3 iterations.

**Deliverable:** Critic report + fixed set.

### Phase 7: Delta Tracking & Compound

**Goal:** Process improves itself. The next faction starts higher.

**Steps:**
1. Record delta entry: (resolved - new) / previous_total
2. Update COMPOUND_TRACKER.md
3. Spawn meta-critic sub-agent:
   - "What broke? What was missing from the spec? What would have prevented the failures?"
4. Apply meta-critic's approved patches to playbooks
5. Surface to Joe with standard report format

**Gate:** Improvement trajectory visible. Delta > 0.05 each iteration.

**Deliverable:** Joe Surface Report (grade, iterations, what shipped, what the machine couldn't resolve, process patches applied).

## Joe Surface Report Template

```
## [Faction] Card Set — Complete

**Final Grade:** [grade]
**Iterations:** [total] across [phase_count] phases
**Pre-gate:** CLEAN
**Delta log:** [summary]

### What shipped
- [files]

### What the machine couldn't resolve
- [open questions for Joe]

### Process improvements applied
- [patches to pipeline]
```

## Pitfalls

- **Contract system misunderstandings → `references/contract-system-reference.md`.** Before designing any card that says "add a Contract," "modify a Contract," or "Contract reward," load the reference — Contracts are 0-cost auto-cycling tokens generated by Mark, not arbitrary card abilities.
- **TRACE NUMBERS TO THEIR SOURCE — never recite from memory.** When the user questions a number (curve count, density target, crew split, rarity distribution), the correct response is: "This comes from [Document], dated [Date]. It was built on [assumptions]. Let me verify those assumptions are still current." If you can't name the source document, you don't know the number — you're reciting. Trigger 2026-06-11: Paul cited curve targets from memory. Joe: "Where are you pulling this curve from?" The answer was Build Facts v1 — five days stale, wrong archetype, wrong crew split. The cost: full pipeline rebuild from Phase 1.5. Crew bleed checks, density counts, edge coverage, curve/rarity tallies — these are counting tasks, not reasoning tasks. Running `delegate_task` for a 30-row checklist adds 5 minutes of overhead for what Paul can do manually in 30 seconds. If Paul built the slot table, Paul validates the slot table. Only delegate spec validation when an orchestrator or autonomous sub-agents produced the slot table and Paul hasn't internalized the numbers.
- **The documentation bottleneck is the root cause of all iteration loops.** If a sub-agent produces wrong output, the spec was incomplete. Fix it upstream.
- **Spec must EXCLUDE, not just INCLUDE.** "Professionals: epithets/role-names" → sub-agents use surnames. Must say "NO SURNAMES."
- **Format drift is the #1 friction point.** Enforce exact pipe table templates. Verify with grep before audit.
- **Workers must write FILES.** Explicitly require file writes in the sub-agent goal. "Write output to [path]" — not "return results."
- **Never skip spec validation.** One validator sub-agent caught 7 blocking errors that would have cascaded into 55 cards of rework.
- **Two-layer review is minimum viable.** pre_review_audit.py catches mechanical errors. Critic catches ludo, flavor, and identity. Neither alone is sufficient.
- **Fixer pass prevents full re-spawns.** Don't re-spawn all 3 workers for small count/coverage fixes.
- **Sub-agents remix existing cards when lore docs leak card names.** Faceless v2 SCRAPPED — 81% name overlap. Prevention: NO EXISTING NAMES directive in every worker prompt + scrub card-name references from lore docs before feeding to workers + post-production dedup check.
- **Crew split targets are faction-specific, not universal.** The 70/30 P+Street vs M+Help split came from Bruiser (minion-heavy, bodies-on-board). A spell-heavy faction like Trigger may need 60/40 or 55/45 — let the faction's pillars determine the natural distribution. Rebalance the slot table before spec validation; don't force a ratio that breaks the faction's identity. (Trigger 2026-06-11: recut to 60/40.)
- **Slot table rebalancing is a formal Phase 2 step.** After building the slot table, check crew split, rarity, curve, and legendary count BEFORE proceeding to Phase 3. The pathway-design skill §Phase 2d has the four-check pattern.
- **Skipping Phase 0 and Phase 2 = scrapped sets.** Trigger v6/v7 were both scrapped 2026-06-09. Root cause: no formal identity gate (Phase 0) and no slot table (Phase 2). v6 sub-agents worked from incomplete specs without crew constraints. v7 sub-agents filled slots to hit counts rather than designing to pathway goals. The identity gate verifies internal coherence. The slot table is the constraint surface that prevents crew bleed and curve imbalance. Never skip these gates — they are the highest-leverage investment in the pipeline.
- **Warmup docs go stale between sessions. Always verify currency via session history before designing any band.** When a warmup doc says "first action: holistic X analysis," check `session_search` for the faction + band to confirm it hasn't already been completed. Trigger 2026-06-12: 2V band was locked June 10 on Telegram. Warmup doc (dated June 12) still had the pre-design slot table. Paul ran the holistic analysis from scratch. Joe had to point Paul to session `20260610_161555_9cfbba97`. The warmup doc is a guide — session history is the source of truth. When they disagree, session history wins.
- **Daily Handover can be stale after a session crash or archive. The canonical Full Set in the dropbox is the ultimate source of truth.** Trigger 2026-06-13: Joe archived the Telegram session. The Daily Handover said 3V was 8/13 locked. The Full Set (`Trigger_Full_Set_v7.md`) had 13/13 with names. Read the canonical set first — never present stale handover state to Joe as "where we are." Fix the handover FROM the canonical set, not the other way around.
- **Skipping Phases 0 and 2 produces scrappable sets.** Trigger v6 and v7 were both scrapped 2026-06-09 ("Garbage in, garbage out"). Phase 0 (identity gate) was never formally run; Phase 2 (pathway slot table) was never built as a standalone deliverable. Cards came out mechanically coherent but identity-weak because sub-agents filled slots to hit counts rather than designing to verified identity + pathway goals. The Pre-Flight Checklist (PF1-PF4) is the hard gate that prevents this. Never skip it, even for a faction with "obvious" identity.

## Integration

| Skill | Phase | Role |
|-------|-------|------|
| `faction-identity-gate` | Phase 0 | Identity verification |
| `tcg-faction-lore-phase` | Phase 0 | Lore lock (with Section 0 Canon Alignment) |
| `pathway-design` | Phase 2 | Crew profiles, turn maps, slot boundaries |
| `orchestrator` | Phases 3-7 | Spawn workers, track delta, escalate |
| `faction-set-review` | Phase 6 | Card set critic (Pass 2-3) |
| `density_calc.py` | Phase 1 | Draw probability verification |
| `pre_review_audit.py` | Phase 5 | Mechanical gate |

## Relationship to bruiser-card-design-pipeline

The `bruiser-card-design-pipeline` skill is the reference implementation. It contains the proven Phase 1-6 pattern for sub-agent card production. Pipeline specs in `workspace/pipelines/` are DERIVED from it. This master skill (`five-crests-card-pipeline`) ORCHESTRATES it — adding identity gate, spec validation, compound tracking, and the Joe Surface Report.

## Changelog

**2026-06-13** — Added `references/contract-system-reference.md` — Contract lifecycle, generation rules, common misunderstandings, reward types. Triggered by Paul proposing a "Contract engine" (Vera) without understanding Contracts are 0-cost auto-cycling tokens generated by Mark. Added pitfall pointer to the reference. Joe: "You don't even understand the contract ability." — Added Phase 1.5: Build Facts Currency Check (mandatory gate before Phase 2). Trigger Build Facts v1 was five days stale — wrong curve, wrong crew split, wrong density targets. The entire Phase 2-3 stack was built on numbers from a different design era. New gate requires verifying Build Facts date, curve, and crew split against the current design identity BEFORE building the slot table. Added "TRACE NUMBERS TO THEIR SOURCE" pitfall. Added `references/trigger-recut-2026-06-11.md` — worked example of the cascade failure and fix protocol.

**2026-06-09 (late)** — Added Pre-Flight Checklist (PF1-PF4): hard gate before Phase 4 that verifies Phase 0 (identity gate report), Phase 1 (spec lock), Phase 2 (formal slot table), and Phase 3 (spec validation) all exist before spawning card-design workers. Trigger v6/v7 scrapped earlier today because Phases 0 and 2 were skipped — cards came out identity-weak. Added pitfall documenting the same lesson. This is the second major process guardrail after the Novelty Gate (same session).

**2026-06-09** — Added Phase 4 Novelty Gate (mandatory before spawning card-design workers). Faceless v2 SCRAPPED — 81% name overlap with Joe's originals when this gate was skipped. Three-part prevention: NO EXISTING NAMES directive, lore doc scrubbing, post-production dedup check. Updated pitfall list with the same lesson.

**2026-06-08** — Initial creation. Synthesized from Trigger v7 and Faceless v2 autonomous runs. Incorporates all kaizen from June 6-8.
