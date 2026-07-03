---
name: bruiser-card-design-pipeline
description: "Five Crests card design pipeline: Lore → Crews → Archetypes → Functions → Mechanics → Synergy Webs → Build Facts → Expressions → Quality Gates."
version: 2.0.0
author: Paul
---

# Five Crests Card Design Pipeline

Full original archived at `docs/Paul/workspace/bruiser-card-design-pipeline-archive.md`.

## ABSOLUTE FIRST — Navigation Layer

Before any card design, read these from `/root/tcg-engine/docs/Five_Crests/`:
1. `00_START_HERE.md` — corpus organization, layers, faction maturity
2. `STATE_OF_THE_CORPUS.md` — what's deep/shell/missing, card-authority rule
3. `TOOLS_INDEX.md` — factory spine, playbooks, processes

**PITFALL: Skipping nav layer** produces MadLibs rosters. **PITFALL: Stale repo** — `cd /root/tcg-engine && git pull` at every session start.

## Mandatory Pipeline (12 Steps)

Sequential and non-negotiable. Never open the card table before step 8.

```
Step 0   Villium Relationship    What does Villium mean? Delivery, capabilities, cost. LOCK before functions.
Step 1   Lore                    Read all faction lore docs. Audit inconsistencies. Lock story, characters, world.
Step 2   Crews                   Who works with who. Role pools. Character profiles. Flesh before mechanics.
Step 3   Archetypes              One-sentence identity. Tempo? Control? Midrange?
Step 4   Playstyle Matrix        Win lines, hero HP, matchup spread, precon cores.
Step 5   Function Registry       12-18 functions derived from archetypes + crews. Consolidate from 22-26 → ~16.
Step 6   Mechanics               Levers per function. Keyword candidates noted, NOT locked. (Keywords lock AFTER cards surface patterns: 3 cards = card text, 10+ = keyword.)
Step 7   Synergy Web             8-15 named edges with mechanical hooks. Two layers: function edges (skeleton) + LIVE web (flesh with synergy triangles, slot table, gap list).
Step 8   Build Facts / Curve     Card counts, rarities, V-curve, tier allocation. From the human, not templates.
Step 9   Expressions             Role + stats + text. Names come LAST. Stats from Model B. Flavor from Living World.
Step 10  Competitive Slotting    Cross-compare same-cost cards. Cut or redesign weakest.
Step 11  Stress Testing          Simulate T1-T5 vs counter-faction. All three archetypes.
Step 12  Quality Gates           FERM + guardrails + iterative sub-agent review. Keywords surface organically from built set.
```

**The rule:** Every card maps to ≥1 function. No function edge = cut candidate.

## Pre-Expression Gate (MANDATORY — before any card row)

Verify ALL are drafted and coherent:
- [ ] Villium relationship LOCKED
- [ ] Playstyle Matrix LOCKED
- [ ] Function registry (~16, consolidated)
- [ ] Crew mechanical identities
- [ ] Mechanics: levers defined, keywords NOT locked
- [ ] Synergy web: 8-15 typed edges
- [ ] Build facts: card type distribution, rarity, V-curve
- [ ] Living World Method understood
- [ ] Keyword scope: elite-only locked to Rare+/Legendary
- [ ] Legendary picks identified
- [ ] Function ID reference table written

## Function Registry Rules

**Consolidation rules (Joe lock 2026-06-06):**
1. **Subsidiary rule:** Fold byproducts into parent functions. "Weapon Recovery" → Ammo Management. "Mass Mark" → Mark.
2. **Build facts are NOT functions.** Curve bodies, cheap spells, baseline efficiency — distribution notes.
3. **Design principles are NOT functions.** "Baseline efficiency baked into stats."
4. **One-card Rare+ expressions** stay under parent function.
5. **Complexity tax:** If a function doesn't add unique value, cut it.
6. **Same-mechanic rule:** Two modes of same mechanic = one function.
7. **Organize by pillar, not game term.**

**Joe review format:** Present functions ONE AT A TIME. Per function: what it does, what card types carry it, why it matters, what role it plays in the machine.

## Sub-Agent Card Production

**Spec Lock Sprint:** Lock everything before spawning workers. Sub-agents working from locked specs produce correct cards on pass one. Sub-agents from draft specs need 5-6 iterations.

**Format enforcement:** Templates must match `pre_review_audit.py` exactly:
- Minion: `| # | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |`
- Spell: `| S# | V | R | Name | Text | Pathway | Edges |`
- Ambush: `| A# | V | R | Name | Trigger | Text | Edges |`
- Weapon: `| W# | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |`

**Split by V-band:** Batch 1: 1V-2V (~20), Batch 2: 3V-4V (~22), Batch 3: 5V-6V (~13).

**Before spawning:** Spec MUST pass validator. Validator catches crew bleed, rarity overflow, mechanic density errors.

## Critical Pitfalls (Compact)

- **Inventing blind spots Joe never locked.** Extrapolated from philosophy ≠ locked. Mark as PROPOSED or ask.
- **Mark as gating requirement instead of bonus.** Contract is incentive, not permission gate. Professional kills anything — Mark just means you get Paid.
- **Using wrong terminology.** Cross-reference Daily Handover or function registry for canonical mechanic names.
- **Over-tightening to synergy web.** ~70% edge-mapped, ~30% draft fodder. 4-5 vanillas minimum.
- **Locked On on reactive cards (Ambushes).** Ambushes trigger on opponent's turn — can't control sequencing.
- **Contract dead draws without cycling.** Contract tokens auto-cycle. Built into keyword sidebar.
- **Locked On density < 4 cards.** Minimum viable: 5-6 cards at varying rarities/costs.
- **Multi-archetype stress test required.** Test all three archetypes vs counters.
- **Keyword bleed across archetypes.** Exile vs Purge — distinction matters for passive triggers.
- **Skipping faction docs.** Read EVERY canon .md in faction directory before function/mechanics work.
- **Pipe tables for card display.** Joe HATES them. Use monospaced code blocks. R before V. See `design-collaboration` skill.
- **Production format to Joe.** Two files: one display (monospaced), one production (pipes). Never deliver pipes to Joe.
- **Spawning sub-agents before specs locked.** Terminology drift → 55 cards of rework. Lock spec, THEN spawn.
- **Slot table math not reconciled.** Run validator BEFORE card design. Cheaper than 55 cards of rework.
- **Warmup crew profiles contradict function registry.** Registry wins. Reconcile after every spec-lock session.
- **Sub-agents reach for surnames.** Spec must say "NO SURNAMES" explicitly. Ambiguity favors the easier path.
- **Format drift across sub-agent batches.** Mandatory templates + grep verification. Never patch parse_card_table() — enforce at spec time.
- **Sub-agents without creative context produce MadLibs.** Must include: Inner_Circle.md, Daily_Life.md, character profiles, location anchors, crew identity paragraphs.
- **Mechanical correctness ≠ good cards.** A- on soulless cards is a LIED grade.
- **Sub-agents remix existing cards when lore docs leak names.** NO EXISTING NAMES directive. Scrub card-name references from lore. Post-production dedup check (>50% overlap = scrap).
- **Skipping competitive slotting and stress testing.** Functions Pass → Competitive Slotting → Stress Test → Draw-at-Any-Turn → One-Card Wonder Test.
- **Wrong pipeline.** Repo pipeline may be corrupted. Correct order is this document.
- **Over-granular function registries.** First pass 22-26 → consolidate to ~16.
- **Designing mechanics without checking canon docs.** Label unverified mechanics as PROPOSAL. Don't build 55-card set around them.

## Verification (Post-Build)

```bash
# Card count (handles single and double-digit numbers)
grep -cP '^\w\s+\d\s+' roster.md

# Function annotation audit
grep "F12" roster.md | grep -v "Cloak"  # catches F12↔F14 swaps

# Per-band rarity
for v in 1 2 3 4 5 6; do for r in C U R L; do count=$(grep -cP "^$r\s+$v\s+" roster.md); [ "$count" -gt 0 ] && echo "  $r: $count"; done; done
```

Target: C ~25 (45%), U ~17 (31%), R ~10 (18%), L 3 (5%). ±2 drift acceptable.

## Iterative Sub-Agent Review

1. Write set to file. 2. Spin up multi-perspective reviewers (Tone, Design, Identity, Flavor, Digital-Native) or single critic (10 categories). 3. Grade: A+ ship, B+ minor fixes, B one more pass, C+ two passes, C− structural. 4. Fix criticals first. 5. Re-spin. Iterate to B+.

**Two-layer review minimum:** `pre_review_audit.py` catches mechanical. Critic catches ludo, flavor, identity. Never ship with only one.

## Design Authority & Workspace

Joe operates above design rules. Flag once, accept override. Paul's workspace: `docs/Paul/workspace/`. Dropbox: `/root/syncthing/paul-dropbox/`. tcg-engine: READ-ONLY.

## Orchestrator — Overnight Builds

Use tmux (not cron, not `hermes chat -q`):
```bash
tmux new-session -d -s factory -x 160 -y 50 'hermes --model deepseek-v4-pro --provider deepseek'
sleep 10
tmux send-keys -t factory "<prompt>" Enter
```
Monitor: `tmux capture-pane -t factory -p | tail -25`. Do NOT include rejected v1 set in warmup — fresh instance will tweak instead of build from registry.

## References
- Design pillars: `references/design-pillars-2026-06-05.md`
- Trigger corrections: `references/trigger-design-corrections.md`
- Warmup doc pattern: `references/warmup-document-pattern.md`
- Sub-agent card production: `references/sub-agent-card-production.md`
- Multi-perspective review: `references/multi-perspective-review.md`
- Full methodology: `references/full-methodology.md`
