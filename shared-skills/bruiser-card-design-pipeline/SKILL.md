---
name: bruiser-card-design-pipeline
description: "Design workflow for Five Crests TCG cards. Pipeline: Lore → Crews → Archetypes → Playstyle Matrix → Functions → Mechanics → Synergy Webs → Build Facts/Curve → Expressions → Quality Gates. Never open the card table until step 8."
---

# Five Crests Card Design Pipeline

## ABSOLUTE FIRST STEP — Navigation Layer

**Before any card design, read these three docs in order:**

1. `docs/Five_Crests/00_START_HERE.md` — corpus organization, layers, faction maturity, reading order
2. `docs/Five_Crests/STATE_OF_THE_CORPUS.md` — what's deep/shell/missing, finite gap list, card-authority rule
3. `docs/Five_Crests/TOOLS_INDEX.md` — factory spine, playbooks, processes, runnable tools

**CRITICAL: These live in the tcg-engine repo** at `/root/tcg-engine/docs/Five_Crests/`, NOT in Paul's vault at `/root/.hermes/docs/Paul/`. Warmup docs may reference them by short name without specifying the full path — always resolve them against the tcg-engine repo first.

From TOOLS_INDEX, trace links to the playbooks that govern your task:
- New faction: `FACTION_FROM_SCRATCH_GUIDE.md` then `LORE_PANEL_FAST_PATH.md`
- Rework: `FACTION_SET_REWORK_PLAYBOOK.md`
- Card design: `game/DESIGN_GUIDELINES.md` (THE design doc)
- Red team: `REDTEAM_FAST_PATH.md`
- Build facts: `FACTORY_BUILD_FACTS_AND_SYNERGY_WEB.md`

**PITFALL: Skipping the nav layer.** If you jump straight to card tables from lore, you will produce a spreadsheet roster ("MadLibs") that passes composition gates but reads as assembly. This is exactly what happened on the Trigger overnight run (2026-06-05). Joe: "You didn't follow the existing processes."

**PITFALL: Working from a stale repo.** The tcg-engine repo at `/root/tcg-engine/` is Joe's design corpus. Joe merges documents throughout the day via Cursor. If you don't pull before a design session, you're working from outdated docs — missing character profiles, crew structures, locked decisions, and lore that Joe already finalized. This happened 2026-06-05: Paul read Trigger docs from a stale repo, then built v1 and v2 sets without seeing the full crew structure and Inner Circle material Joe had already merged. The mandatory step: `cd /root/tcg-engine && git pull` at the start of every new Daily Handover, and at session starts within the same day if significant time has passed. Encoded in AGENTS.md (Session Start Protocol).

**PITFALL: Inventing blind spots and design constraints Joe never locked.** Paul has a recurring failure mode: extrapolating "what this faction doesn't do" from design philosophy and writing it as a locked blind spot. This happened 2026-06-06: "no direct hero damage spells" and "no AOE board clear" appeared in the Trigger warmup doc as blind spots — neither was locked by Joe. "No direct hero damage" was Paul's extrapolation from "the Contract is for minions" (which means Contracts target minions, not that spells can't go face). When Joe saw these, he explicitly overrode them. **Rule: blind spots only go in warmup docs or registries if Joe explicitly stated them as constraints. "Extrapolated from philosophy" is not a source. If you're not sure whether Joe locked it, ask or mark it PROPOSED.**

**PITFALL: Treating Mark as a gating requirement instead of a bonus multiplier.** The Contract engine is an incentive structure, not a permission gate. A Professional can kill anything — Mark just means you get Paid for it. Building the function registry with "removal requiring Mark setup" as the core assumption produces a hamstrung faction that folds when Marks are removed. The correct framing: removal works without Mark (just less efficient or with fewer payoffs). Mark → kill → Paid is the BONUS path. 2026-06-06: the v1-v3 function registries all described F04 as "conditional removal requiring Mark setup." Joe corrected: you don't need a Contract to shoot someone who's shooting at you.

**PITFALL: Using shorthand terminology that diverges from locked mechanic names.** Warmup docs written quickly may use shorthand ("Lock" instead of "Locked On") that drifts from Joe's locked terminology. Always cross-reference the latest Daily Handover or function registry for the canonical mechanic name before writing new documents. 2026-06-06: the warmup used "Lock" throughout; the actual locked mechanic is "Locked On" (Locked On 2/4/6). Warmup docs are written from last session's understanding and can reference retired frameworks, banked docs, or stale document lists as if they're current. The 2026-06-06 Trigger warmup pointed to Archetypes_Factory and Mechanical_Brainstorm (both marked BANK/NOT SHIP in the repo) as reference docs, and framed Hunt/Barrage/Arsenal as "validate or revise" when Playstyle.md and Design_Bible.md had already retired them. Always cross-reference warmup claims against the live faction docs before acting. If a warmup says "read X for reference" and X's header says BANK/NOT SHIP, treat X as salvage material — mine for concepts, don't treat as current framework.

**PITFALL: Over-tightening every card to the synergy web.** Joe wants draft fodder and vanilla bodies in the set — not every card needs to be a web node. Target ~70% edge-mapped cards, ~30% draft fodder and spice. Two vanillas in 30 minions is minimum; 4-5 is better. Joe: "Need some vanilla and draft fodder — not everything is going to make it from the old design. Use it as inspiration primarily, and steal what's worth a damn in name or ability." The rule "a card with no edge is a cut candidate" applies to the synergy web build phase, not to the final set — draft vanillas are explicitly allowed and encouraged. Trigger v4: FNG (2/1 vanilla) and Bearcat (3/2 vanilla) kept by Joe's direction. 2026-06-07.

**PITFALL: Sequencing mechanics (Locked On) on reactive cards (Ambushes).** Ambushes trigger on the opponent's turn when you can't control sequencing. Placing Locked On on an Ambush creates anti-synergy — the Ambush is always the "first" card of the turn and never benefits from the mechanic. The correct fix: use the faction's core mechanic instead (e.g., "If Marked, deal 5 instead" rather than "Locked On 3: deal 5"). Discovered during Trigger v3 critic review. 2026-06-07.

**PITFALL: Mechanic generates dead draws without cycling.** The Mark→Contract→Paid loop generates 0V Contract tokens that sit dead in hand until the Marked minion dies. Multiple Marks = multiple dead draws. The fix: Contract tokens auto-cycle. "At the start of your turn: if the minion that spawned this Contract is dead, discard this and draw 1." Or: "You may play this as a 0V spell: draw 1 if the Marked minion died this turn." Built into the keyword sidebar definition. Discovered during Trigger v3 critic review — Contract hand clutter was the #2 remaining structural problem. 2026-06-07.

**PITFALL: Locked On density — less than 4 cards is a trap.** A sequencing mechanic that gets its own hero (Bunny) and only 2 cards is a hero whose power is literally blank in 90% of decks. The fix: either add 4-6 Locked On cards across minions, spells, and weapons, or redesign the hero power to work independently. Minimum viable density: 5-6 cards at varying rarities and mana costs so the mechanic shows up in draft and constructed. Trigger v3→v4: Locked On went from 2 cards to 5 cards (Primer 1V, Snap Decision 2V, Spotter 3V, Quick Draw LO3, Locked On 6 5V). 2026-06-07.

**PITFALL: Multi-archetype stress test required.** Running a stress test for only one archetype (e.g., Service vs Skiver) leaves Sermon and Sin untested against their counters. Sermon vs Bruiser midrange and Sin vs Duster control expose different failure modes. Test all three. Discovered during Faceless card design 2026-06-08. The build facts specify 4 legendaries (2 minion, 1 spell, 1 weapon). Boom! Headshot (4V L ambush) in Trigger v1 consumed a legendary slot that didn't match the build facts. Ambushes are spells — they use the spell legendary slot. If the spell legendary is already taken (Locked On 6), the legendary ambush either drops to Rare or gets cut. Trigger v4: Boom! Headshot → Rare. 2026-06-07.

**PITFALL: Keyword bleed across archetypes — Exile vs Purge.** Cards in non-Sermon archetypes that remove opponent's cards should use "Exile," not "Purge." Purge triggers Burke's passive (Wearing Them Down) and advances the Sermon clock. A Way of Sin card that Purging would give Sin access to a Sermon payoff — that's keyword bleed. Use Exile for Sin removal, Purge for Sermon removal. The distinction matters mechanically (Burke passive trigger) and for archetype identity. Discovered during Faceless card design 2026-06-08: Hear Thy Words (Sin, steal-and-play) originally read "Purge it afterward" — corrected to "Exile it." ("Pay cost: restore durability and load payload") and the spell Reload ("1V: restore 1 durability") had the same name but different mechanics. Rename the spell to Field Strip — military term, same flavor family, no keyword confusion. Always audit keyword names against spell/weapon names before shipping. 2026-06-07.

**PITFALL: Skipping faction docs during function/mechanics design (2026-06-06).** Reading Identity, Playstyle, and Design_Bible is not enough. Joe: "Did you actually load up all of your fucking files that you're supposed to? I don't feel like you're actually up to date on anything." Before any function derivation or mechanics work, read EVERY canon .md file in the faction directory that isn't explicitly marked BANK/NOT SHIP or archived. Use `search_files(target='files', pattern='*.md', path='...faction/')` to list the directory, then read them. The mandatory minimum: 00_INDEX.md, Identity.md, Playstyle.md, Design_Bible.md, Inner_Circle.md, Lock_Governance.md, Functions.md, Daily_Life.md, Territory.md, Support_Network.md, Precon.md, Hero_Cards.md. Skipping Lock_Governance and Inner_Circle is what caused the terminology drift ("Lock" vs "Locked On") and crew lane misalignment in Trigger v3 — those docs had the locked terminology and crew card lanes that the warmup doc didn't carry forward.

**PITFALL: Using markdown pipe tables for card output.** Joe explicitly hates pipe-delimited tables for card display ("I really don't like the tabling format" — 2026-06-05). Use the fixed-width monospaced column format from `design-collaboration` skill, `references/card-display-format.md`. Cards organized by Villium band, then rarity within band. Columns: R · V · Name · Stats · Text · [Tier]. Numbers optional. This applies to rosters, comparison reports, hero cards — ALL card output. Never use `| col | col |` format.

**PITFALL: Delivering player-facing cards in production format (2026-06-08).** The production format (pipes, pathway columns, edge references, partners) is for sub-agents and audit scripts. The player-facing format is monospaced code blocks: R before V, crew at end in brackets, no pipes, no edges, no pathway tags. When Joe asks for "the set" or "the cards," give him the display format. The production format file is for future sub-agent work. Trigger v7 was delivered to Joe in production format — he called it out. Two files: one display, one production. Never deliver pipes to Joe.

**Spec Lock Sprint (2026-06-08):** When using sub-agent parallelism for card production, the Pre-Expression Gate items become the SPEC that sub-agents consume. This spec lock sprint — where every gate item is reviewed, corrected, and locked — pays for itself many times over. Sub-agents working from locked specs produce correct cards on pass one. Sub-agents working from draft specs produce cards that need Joe-level correction (5-6 review iterations). The spec lock sprint is the investment. Card-level sub-agent parallelism is the dividend.
design cards, they produce 3 different pipe table formats unless the spec enforces
exact column order. Fix: add mandatory output format templates to every SubAgent
Spec. Templates must match `pre_review_audit.py` column order exactly:
- Minion: `| # | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |`
- Spell: `| S# | V | R | Crew | Name | Text | Pathway | Edges |`
- Ambush: `| A# | V | R | Name | Trigger | Text | Edges |`
- Weapon: `| W# | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |`
Section headers must be exactly `## Minions`, `## Spells`, `## Ambushes`, `## Weapons`.
Include grep verification commands (`grep -c '^| [0-9]'` etc.) in the spec.
This cost 2 wasted iterations on the Trigger orchestrator run before permanent fix.

## Mandatory Pipeline (Joe Lock 2026-06-05, corrected 2026-06-06)

The pipeline is sequential and non-negotiable. Every step must be completed before the next begins. Jumping to card rows before completing earlier steps produces spreadsheet rosters, not designed sets. Each step daisy-chains into the next — you can't determine functions without archetypes, you can't determine mechanics without functions, you can't determine synergy webs without mechanics.

**Pipeline revision 2026-06-06:** Villium relationship added as Step 0 — must be locked before function derivation. Keywords moved from Step 6 to after Step 10 — keyword patterns are identified organically from the built card set, not declared upfront. A mechanic appearing on 3 cards is card text. A mechanic appearing on 10+ cards earns a keyword.

```
Step 0   Villium Relationship       What does Villium mean to this faction? How do they use
   |                                  it? What does it let them DO? What does it cost them?
   |                                  LOCK before functions. The mechanical identity foundation.
Step 1   Lore                        Read all faction lore docs. Audit for inconsistencies.
   |                                  Lock the story, characters, world. Flag gaps.
Step 2   Crews                       Who works with who. Role pools. Character profiles.
   |                                  Inner_Circle.md or equivalent. Flesh before mechanics.
Step 3   Archetypes                  What kind of deck does this faction build?
   |                                  Tempo? Control? Midrange? Aggro? One-sentence identity.
Step 4   Playstyle Matrix + Core     Win lines, hero HP, precons, core pool (~15-20 cards).
   |                                  Based on archetypes. "How does this faction win?"
Step 5   Function registry           What does the faction DO mechanically? 12-18 functions.
   |                                  Derived from archetypes + crews — NOT retrofitted from cards.
Step 6   Mechanics                   Mechanical levers. What levers express each function?
   |                                  Keyword candidates noted, NOT locked. Boundaries. NOT lists.
   |                                  Pricing (Model B). Keywords locked AFTER cards surface patterns.
Step 7   Synergy web                 Connect functions: A enables B, C protects D.
   |                                  8-15 named edges with mechanical hooks.
Step 8   Build Facts / Curve         How many cards, rarities, V-curve, power curve, tone.
   |                                  Cascade validation lives here. Allocation before filling slots.
Step 9   Expressions                 Role + stats + text. Names come LAST.
   |                                  Stats from Model B. Flavor from Living World Method.
Step 10  Competitive Slotting         Every card fights for its slot. No linear upgrades.
   |                                  Cross-compare same-cost cards within AND across archetypes.
   |                                  Flag redundancies. Cut or redesign the weakest.
Step 11  Stress Testing               Simulate 5-turn matchup vs appropriate counter-faction.
   |                                  All three archetypes tested. Draw-at-any-turn eval.
   |                                  Verify blind spots are real, not aspirational.
Step 12  Quality gates               FERM + guardrails + iterative sub-agent review + Joe batch.
   |                                  Spin up sub-agent to grade against documentation baseline.
   |                                  Rework until 90-95%. Iterate up to 3 passes.
         → Keyword patterns: audit built set for effects repeating 10+ times → keyword them.
           • 3 cards = card text. 15 cards = a keyword.
           • Keywords are compression, not design. Let patterns surface organically.
         Final doc lock then Pass 6 JSON
```

**The rule:** Do not open the card table until steps 0-8 are drafted. Rows are expressions of functions, not a quota to fill. Every card maps to ≥1 function. A card with no function edge is a cut candidate.

**The keyword rule (2026-06-06):** Do NOT lock keywords at Step 6. Define mechanical levers. Note keyword candidates. Lock keywords only AFTER the card set is built and patterns have surfaced organically. If you define keywords first, you design to your own categories instead of discovering what the faction naturally wants to do.

**PITFALL: Jumping to card rows before pipeline steps complete (2026-06-06).** Joe caught Paul compressing the entire pipeline into one file write and heading straight for 55 card rows. Joe: "Are you actually following the processes? Seems to me that you're skipping straight to the end and doing a fifty five card count. Is that how you're supposed to do this?" This is the same failure mode as the Trigger overnight runs (v1 and v2), but during an active session. The pipeline exists for a reason — each step constrains the next. If you find yourself writing card names before the function registry is complete, stop. If you catch yourself thinking "I know the answer, let me just write it," stop. The impulse to produce visible output (card rows) before invisible scaffolding (function registry, synergy web) is a known cognitive trap. The output IS the scaffolding — card rows come from it, not before it.

**Pre-Expression Gate (MANDATORY — complete before any card row is written):**

Before writing the first card row, verify ALL of the following are drafted and coherent:
- [ ] Villium relationship: what does the substance mean to this faction? Delivery method, capabilities, cost. LOCKED.
- [ ] Playstyle Matrix: hero win lines, HP, matchup spread, precon cores, midrange→control spectrum. LOCKED.
- [ ] Function registry: ~16 functions (12-18 band), consolidated per subsidiary rule, each derived from lore + crews (NOT retrofitted from existing cards). First pass will run 22-26 — consolidation pass is mandatory before proceeding to mechanics.
- [ ] Crew mechanical identities: each crew has a documented signature and gameplay feel
- [ ] Mechanics: mechanical levers defined for each function. Keyword candidates noted, NOT locked (keywords lock AFTER card patterns surface)
- [ ] Synergy web: 8-15 named edges, each typed (Enables/Protects/Creates→Spends/Punishes/Curve Chain), mechanically specific
- [ ] Build facts: card type distribution, rarity burn-down, V-curve, tier allocation targets
- [ ] Living World Method: understood for the faction — what's the 7am? what's the rhythm?
- [ ] Keyword scope: elite-only levers (Barrage) locked to Rare+/Legendary only
- [ ] Legendary picks: 3 candidates identified, former Legendaries demoted if Joe confirmed
- [ ] Function ID reference table: write down which ID = which mechanic BEFORE annotating cards (prevents F12↔F14 swaps)

**PITFALL: Using markdown pipe tables for card output.** Joe explicitly hates pipe-delimited tables for card display ("I really don't like the tabling format" — 2026-06-05). Use the fixed-width monospaced column format from `design-collaboration` skill, `references/card-display-format.md`. Cards organized by Villium band, then rarity within band. Columns: R · V · Name · Stats · Text · [Tier]. Numbers optional. This applies to rosters, comparison reports, hero cards — ALL card output. Never use `| col | col |` format.

**PITFALL: Delivering player-facing cards in production format (2026-06-08).** The production format (pipes, pathway columns, edge references, partners) is for sub-agents and audit scripts. The player-facing format is monospaced code blocks: R before V, crew at end in brackets, no pipes, no edges, no pathway tags. When Joe asks for "the set" or "the cards," give him the display format. The production format file is for future sub-agent work. Trigger v7 was delivered to Joe in production format — he called it out. Two files: one display, one production. Never deliver pipes to Joe.

**Spec Lock Sprint (2026-06-08):** When using sub-agent parallelism for card production, the Pre-Expression Gate items become the SPEC that sub-agents consume. This spec lock sprint — where every gate item is reviewed, corrected, and locked — pays for itself many times over. Sub-agents working from locked specs produce correct cards on pass one. Sub-agents working from draft specs produce cards that need Joe-level correction (5-6 review iterations). The spec lock sprint is the investment. Card-level sub-agent parallelism is the dividend.

**PITFALL: Spawning card-design sub-agents before specs are locked.** If the function registry still has terminology drift, if crew can/cannot profiles aren't encoded, if the slot table has gaps — sub-agents will produce cards with crew bleed, wrong keywords, and identity drift. Fixing 55 cards individually costs more than locking the spec once. Lock the spec, THEN spawn the sub-agents.

**PITFALL: Slot table math not reconciled against Build Facts.** The slot table (minion rows + spells + weapons) is built from pathway turn maps. The Build Facts (55 cards, crew budgets, rarity caps, V-band totals) are a separate document. If they're not arithmetically reconciled BEFORE spawning card sub-agents, the sub-agents will produce cards at the wrong crew counts, rarity tiers, and V-bands. The fix: run a validator sub-agent on the spec slot table against build facts. Trigger v1 spec had 7 blocking math errors — crew budgets 50-150% over, rarity overflow, Overkill at 2x target density. All caught by the validator BEFORE any cards were designed. Validator is cheaper than 55 cards of rework.

**PITFALL: Warmup crew profiles must be cross-referenced against the locked function registry before becoming spec inputs.** Warmup docs written during spec-lock sessions (especially mobile sessions) may contain draft crew CAN/CANNOT profiles that contradict locked documents. Trigger 2026-06-08: the warmup said Management owns Mark and Professionals CANNOT initiate Contracts — but the locked function registry F01 assigns Mark to Professionals, and v6 cards had 4 Professional Mark minions. The orchestrator spec-validate worker caught this before any cards were designed. Rule: after every spec-lock session, reconcile crew profiles against the function registry. If they conflict, the registry wins. Applies to Silence, Intel, and any mechanic with ownership locked in the function registry Crew column.

**PITFALL: Professional naming convention — sub-agents reach for surnames.** Sub-agents default to Italian surnames (Ricci, Caruso, Lupo) because they're easier to generate than epithets. The spec must explicitly say: "Professionals: epithets or role-names ONLY. NO SURNAMES. If it sounds like a birth certificate, it's wrong." Examples — Hammer, Ghost, Wolf, Collector, Sculptor, Finger Man, Button Man, Bagman. Trigger v7 batch 2 had four surname violations caught post-assembly. Lesson: the naming convention must EXCLUDE surnames explicitly, not just suggest epithets. Sub-agents interpret "last names or epithets" as "last names are fine" — ambiguity favors the easier path.

**PITFALL: Using markdown pipe tables for card output.** Joe explicitly hates pipe-delimited tables for card display ("I really don't like the tabling format" — 2026-06-05). Use the fixed-width monospaced column format from `design-collaboration` skill, `references/card-display-format.md`. Cards organized by Villium band, then rarity within band. Columns: R · V · Name · Stats · Text · [Tier]. Numbers optional. This applies to rosters, comparison reports, hero cards — ALL card output. Never use `| col | col |` format.

**PITFALL: Delivering player-facing cards in production format (2026-06-08).** The production format (pipes, pathway columns, edge references, partners) is for sub-agents and audit scripts. The player-facing format is monospaced code blocks: R before V, crew at end in brackets, no pipes, no edges, no pathway tags. When Joe asks for "the set" or "the cards," give him the display format. The production format file is for future sub-agent work. Trigger v7 was delivered to Joe in production format — he called it out. Two files: one display, one production. Never deliver pipes to Joe.

**Spec Lock Sprint (2026-06-08):** When using sub-agent parallelism for card production, the Pre-Expression Gate items become the SPEC that sub-agents consume. This spec lock sprint — where every gate item is reviewed, corrected, and locked — pays for itself many times over. Sub-agents working from locked specs produce correct cards on pass one. Sub-agents working from draft specs produce cards that need Joe-level correction (5-6 review iterations). The spec lock sprint is the investment. Card-level sub-agent parallelism is the dividend.

**PITFALL: Spawning card-design sub-agents before specs are locked.** If the function registry still has terminology drift, if crew can/cannot profiles aren't encoded, if the slot table has gaps — sub-agents will produce cards with crew bleed, wrong keywords, and identity drift. Fixing 55 cards individually costs more than locking the spec once. Lock the spec, THEN spawn the sub-agents.

**PITFALL: Slot table math not reconciled against Build Facts.** The slot table (minion rows + spells + weapons) is built from pathway turn maps. The Build Facts (55 cards, crew budgets, rarity caps, V-band totals) are a separate document. If they're not arithmetically reconciled BEFORE spawning card sub-agents, the sub-agents will produce cards at the wrong crew counts, rarity tiers, and V-bands. The fix: run a validator sub-agent on the spec slot table against build facts. Trigger v1 spec had 7 blocking math errors — crew budgets 50-150% over, rarity overflow, Overkill at 2x target density. All caught by the validator BEFORE any cards were designed. Validator is cheaper than 55 cards of rework.

**PITFALL: Warmup crew profiles must be cross-referenced against the locked function registry before becoming spec inputs.** Warmup docs written during spec-lock sessions (especially mobile sessions) may contain draft crew CAN/CANNOT profiles that contradict locked documents. Trigger 2026-06-08: the warmup said Management owns Mark and Professionals CANNOT initiate Contracts — but the locked function registry F01 assigns Mark to Professionals, and v6 cards had 4 Professional Mark minions. The orchestrator spec-validate worker caught this before any cards were designed. Rule: after every spec-lock session, reconcile crew profiles against the function registry. If they conflict, the registry wins. Applies to Silence, Intel, and any mechanic with ownership locked in the function registry Crew column.

**PITFALL: Professional naming convention — sub-agents reach for surnames.** Sub-agents default to Italian surnames (Ricci, Caruso, Lupo) because they're easier to generate than epithets. The spec must explicitly say: "Professionals: epithets or role-names ONLY. NO SURNAMES. If it sounds like a birth certificate, it's wrong." Examples — Hammer, Ghost, Wolf, Collector, Sculptor, Finger Man, Button Man, Bagman. Trigger v7 batch 2 had four surname violations caught post-assembly. Lesson: the naming convention must EXCLUDE surnames explicitly, not just suggest epithets. Sub-agents interpret "last names or epithets" as "last names are fine" — ambiguity favors the easier path.

**PITFALL: Format drift across sub-agent batches (2026-06-08).** When 3 parallel
workers design cards by V-band, each produces a different pipe table format:
batch 1 uses `·` separators, batch 2 swaps Rarity/Crew columns, batch 3 uses
`Cw` instead of `Crew`. The `pre_review_audit.py` script parses by column index
and returns zero cards if the format doesn't match. **Fix:** Include mandatory
output format templates in every spec. Section headers must be exactly
`## Minions`, `## Spells`, `## Ambushes`, `## Weapons`. See
`references/sub-agent-output-format.md` for exact copy-pasteable templates and
verification commands. Workers verify format BEFORE declaring done. Format drift
cost 3 iterations on the Trigger orchestrator run before this was locked.

**PITFALL: Skipping competitive slotting and stress testing (2026-06-08).**
The Faceless Upgraded Pipeline v2 (`Faceless_Card_Design_Upgraded_v2_Paul.md`)
proved that competitive slotting and stress testing catch design problems the
rubric alone misses: same-function-different-cost redundancies, linear stat
upgrades of the same card, and curve fragility. Add these phases between the
slot table and expressions:
  1. **Functions Pass** — one sentence per card. No numbers. Verify no two cards share the same function sentence.
  2. **Competitive Slotting** — for each slot, ask "why wouldn't I always pick this over another same-cost card?" Cut or redesign the weakest.
  3. **Stress Test** — simulate T1-T5 vs aggro and control matchups. Does the curve hold?
  4. **Draw-at-Any-Turn** — score each card at T1, T5, T8. Dead both early AND late = cut.
  5. **One-Card Wonder Test** — every L and R must make a drafter say "I want to build around this."

**PITFALL: Using the wrong pipeline.** The pipeline in the tcg-engine repo (CARD_PRODUCTION_PIPELINE.md, DESIGN_GUIDELINES.md §2) was assembled from ~8500 merged documents and contains errors. The correct order is the one above: Lore → Crews → Archetypes → Playstyle Matrix → Functions → Mechanics → Synergy Webs → Build Facts/Curve → Expressions → Quality Gates. The old pipeline had functions before crews, placed build facts too early, and omitted the playstyle matrix step. Joe corrected this 2026-06-05: "That pipeline is wrong. Like fundamentally flawed."

**PITFALL: Skipping steps.** Jumping from Lore directly to Card Rows (skipping Crews, Archetype, Functions, Mechanics, Synergy Web, Build Facts) produces cards built from memory and habit rather than design. This happened on Trigger v1 AND v2 (2026-06-05) — both sets were rejected because the pipeline wasn't followed. Joe: "We're gonna start over from scratch."

**PITFALL: Over-granular function registries (2026-06-06).** First-pass function registries run 22-26 functions because every subsidiary gets its own slot. Joe: "A lot of this shit is the same thing, just named something different. Can probably shoot for around 16." Consolidation pass applies the subsidiary rule: if an effect is a byproduct of another function, fold it. If it's a build fact (curve body, chain enabler), cut it. If it's a design principle (baseline efficiency), cut it. If it's a one-card Rare+ expression (multi-weapon, Lock finisher), keep it under the parent function. Target ~16 after consolidation. Trigger v1→v2: 26→16 by folding Mass Mark into Mark, Weapon Recovery into Ammo Management, Ballistic Clarity into Special Ammo, Hard Removal into Marked Removal, and cutting 4 build-fact/design-principle entries. The function registry must be derived from archetypes + crews first. Naming functions after cards you've already designed ("F01: Gerald Creates Ghost Permanents") is backwards. Functions describe what the faction DOES; cards are expressions of those functions. If you find yourself writing function descriptions that match specific cards you're already picturing, you're doing it wrong.

**PITFALL: Designing mechanics from first principles without checking canon docs.** The Trigger v2 overnight run (2026-06-05) invented Ghost Permanents, Hidden Contract, and Simultaneous Hidden Choice as flagship mechanics — none of which exist in the Trigger faction's canon docs (Identity.md, Playstyle.md, Functions.md). The canon Trigger is Mark → Contract → Kill → Paid → Loot + Weapon sub-game. Before proposing a mechanic that isn't explicitly in the faction's playstyle or function registry, verify against the canon docs. If it's not there, label it as a PROPOSAL and ask Joe to decide whether to add it to canon. Do not build a 55-card set around unverified mechanics.

### Step 0 — Living World Method

Every card starts from a concept in the world, not a mechanical need:
1. See it as real — a person/place/moment in Detroit 1961
2. Explore its life — what shaped them? What's their 7am?
3. Find the hidden impact — the second-order effect where the mechanic lives
4. The mechanic writes itself — translate, don't invent
5. Then refine with math — math validates, doesn't create

### Step 4 — Playstyle Matrix + Core

Lock before proceeding to functions. Answer these for the faction:

**Hero Win Lines:**
| Element | Definition |
|---------|-----------|
| Hero name + lane | 3 heroes, one per pillar |
| HP | Grind hero gets 30, pressure/aggro gets 28, spectacle/combo gets 26 |
| Win line | One sentence: "Wins by X on turns Y-Z" |
| Core pool | 15-20 cards the precon builds around. Curve distribution by card type. |

**Matchup Spread:**
Rate each hero against every other faction: Favored / Even / Unfavored. One sentence
explaining why. A faction that's favored against everything is poorly designed. A
faction that's unfavored against everything has no reason to exist.

**Midrange → Control Spectrum:**
If the faction can flex into control, define what the player cuts and what they add.
A skilled player should be able to construct an alternative build from the same
card pool by selecting different expressions of the same functions. The set leans
toward the default archetype; the control build assembles from existing pieces.

**Deliverable:** A playstyle matrix document or section that Joe can lock in one
pass. Hero abilities come AFTER card design (Step 9), not here — but the lanes
must be clear enough that cards can be designed to them.

### Step 5 — Function Registry

List what the set must DO (game actions, decisions, moments). Target **~16 functions**
(12-18 band). Derived from archetypes + crews — NOT retrofitted from cards.

Template: `game/DESIGN_FUNCTION_REGISTRY_TEMPLATE.md`

Function vocabulary: enable keyword, payoff keyword, mark/tax, splash payoff, protect
key piece, disrupt plan, finisher, grind engine, tempo pressure, safety valve,
curve/rodman.

**Joe review format (2026-06-06):** After writing the function registry to a file and
syncing to dropbox, present functions to Joe ONE AT A TIME in chat — not as a table
dump. For each function, cover four things in plain English:

1. **What it does** — the mechanical description. Not a keyword, not a card, the verb.
2. **What card types carry it** — minion battlecries, spells, weapons, with rough counts
   (e.g., "4-5 minion battlecries, 1-2 cantripped spells").
3. **Why it matters to the faction** — what happens if this function doesn't exist? What
   breaks? How does it connect to the faction identity?
4. **What role it plays in the machine** — the enabler, the payoff, the safety valve,
   the finisher. How it relates to other functions.

Start at F01 and work through sequentially. Let Joe interrupt, redirect, or lock before
moving to the next function. Don't rush — the depth IS the deliverable. This format
replaces the table-dump approach that buries the detail.

**PITFALL: Veering off during one-at-a-time function review.** When Joe asks for
individual function breakdowns, stay on the track. 2026-06-06: started F01 Mark,
then the conversation veered into blind spot corrections, Hearthstone Rogue
research, Dead Man's Hand naming, and Playstyle Matrix. F02-F13 were never
individually reviewed. The deep-dive format only works if you complete the
sequence. If Joe redirects, follow — but do not be the one to redirect. After
an interruption, return to the next function and ask: Continue with F02?
Do not assume the review is done or that the table dump was sufficient.

**Consolidation rules (Joe lock 2026-06-06):**

First draft will be too granular — that's normal. Consolidation pass is mandatory.

1. **Subsidiary rule:** If an effect is a subsidiary or byproduct of another function,
   fold it into the parent. "Weapon Recovery from graveyard" is a byproduct of Ammo
   Management, not its own function. "Mass Mark" is still Mark — wider scope, same
   function. "Multi-Weapon" is Armed at Rare+. If the parent function describes the
   class of action and the child is a specific expression, fold.

2. **Build facts are NOT functions.** Curve bodies, cheap spells to feed sequencing,
   baseline stat efficiency — these are distribution notes for the build facts step,
   not functions. If it's true of every faction or it's a curve/math concern, cut it.

3. **Design principles are NOT functions.** "Baseline efficiency baked into stats"
   is a design principle. It governs HOW you build cards, not WHAT a card does.

4. **One-card expressions stay with the parent.** Lock Finisher (Legendary, Lock 6)
   is an expression of Lock — one card at the top of the curve. Don't give it an
   F-slot. Multi-weapon (Rare+) is an expression of Armed. Don't give it an F-slot.
   If it's 1-2 cards at Rare+, it's the parent function at high rarity.

5. **Iterative collapse:** First pass runs 22-26. Joe review collapses to ~16.
   Don't fight it — the subsidiaries are visible in the v1 and Joe will tell you
   which ones are the same thing under different names.

6. **Complexity tax rule (2026-06-06):** Every function adds cognitive load to the
   faction. A function that "doesn't really provide any additional value and just
   convolutes the system" (Joe, on Honed) should be cut, not because it's a
   subsidiary, but because the system is cleaner without it. Ask: does this function
   do something that no other function already covers? If Armed + Ammo Management +
   Special Ammo covers weapon depth, Honed is a fourth layer that doesn't earn its
   slot. Trigger v3: Honed cut, Armed/Ammo Management/Special Ammo kept. Three
   functions do the work of four, cleaner.

7. **Same-mechanic rule (2026-06-06):** If two functions are "the same mechanics"
   (Joe, on Lock and Bullet Time), they're one function with two expressions.
   Locked On has two faces: scaling payoff (Locked On 2/4/6) and chain protection
   (Bullet Time). The protective side is the Rare+ expression of the same mechanic.
   Don't split a mechanic into two F-IDs because it has a defensive and offensive
   mode — the F-ID describes the class of action, not each mode.

8. **Organize by pillar, not by game term.** Group functions under the faction's
   mechanical pillars (Contracts, Ammo, Lock) — not under categories like "Combat"
   or "Utility." The pillar IS the organizational principle. Cross-pillar functions
   (Cloak, Hustle) can live under a shared category, but the pillar functions stay
   in their pillar.

9. **Legacy Functions.md trap:** The repo's Functions.md may use a retired taxonomy
   (e.g., Hunt/Arsenal/Barrage for Trigger). Cross-reference the faction's
   Design_Bible.md before trusting legacy function lists. If Design_Bible says the
   taxonomy is retired, the Functions.md is salvage material — mine for concepts,
   don't treat as current framework.

### Step 7 — Synergy Web (LIVE)

**Canonical process:** [`FACTORY_BUILD_FACTS_AND_SYNERGY_WEB.md`](https://github.com/nous-repos/tcg-engine/blob/main/docs/playbooks/FACTORY_BUILD_FACTS_AND_SYNERGY_WEB.md) in the tcg-engine repo. This is a gate — no band craft passes until the synergy web is started.

**Two layers, built in sequence:**

**Layer 1 — Function edges (skeleton):** 8-15 named edges between functions, each typed:
- **Enables**: A makes B's condition true
- **Protects**: C keeps D alive to do its job
- **Creates→Spends**: E creates resource F uses
- **Rewards**: Scaling payoff — bigger X makes Y bigger
- **Curve chain**: Play order T1 to T4

Number edges E01–E15. Use function IDs (F01→F02). Each edge gets a one-sentence mechanical hook. This layer defines the grammar. A card that touches zero edges is a cut candidate.

**PITFALL: Function self-edges.** Don't create edges where a function references itself (e.g., Bullet Time→Locked On when both are F08). If one mechanic has two expressions, that's one function, not a synergy edge. Baked into the function definition.

**PITFALL: Wrong edge type on scaling loops.** Contract Scaling→Paid looks like a Curve Chain but isn't — there's no T1→T2 play pattern. Scaling loops are Creates→Spends (each Paid feeds the scale) + Rewards (bigger scale means bigger payouts). Use Rewards as the edge type for scaling payoffs.

**Layer 2 — LIVE web (deliverable):** After function edges lock, build the LIVE web per the process doc. Four deliverables:

1. **Synergy Triangles** — keyword/mechanic chains (A+B+C=Payoff), mapped to hero precons. Modeled after Bruiser's T1–T8.
2. **Win-line packages** — A/B/C readable combo scripts per hero win line.
3. **Slot table** — 33 rows (minions), banded by V. Each row: #, Crew, Rarity, Status (LOCKED/OPEN), Name+stats or `[NEED: triangle, layer, job]`, Partner A, Partner B, Package. The gate: if a row has no Partner A and Partner B, do not lock — redesign or cut.
4. **Gap list** — Named holes: what's missing, why it matters, what can fill it. Format: Need / Why / Can Be.

**Worked example:** Bruiser's [`Synergy_Web.md`](https://github.com/nous-repos/tcg-engine/blob/main/docs/Five_Crests/factions/Bruiser/Synergy_Web.md) — 8 triangles, 3-layer formation, per-triangle NEEDs table, 33-row slot table with OPEN/LOCKED status, spell/weapon/ambush matrix, gap list.

Function edges are the skeleton. The LIVE web is the flesh. Both are required.

## CRITICAL: File Discipline

**NEVER overwrite existing files in place.** All new content goes into NEW files. Joe will NOT tolerate lost work.

## Iterative Sub-Agent Review (Step 10 — Quality Gates)

After the card roster is written, run an iterative review cycle using sub-agents via `delegate_task`:

### Review Loop

1. **Write the set to a file.** Full roster with edge annotations, keyword sidebar, build facts. Self-contained — the critic gets one file.
2. **Spin up reviewer sub-agents.** Two patterns:

   **Advanced (preferred): Multi-Perspective Review.** Spin up 5 specialized reviewers in parallel via `delegate_task` with `tasks` array. Each gets one lens: Tone, Design, Identity, Flavor, Digital-Native. Paul synthesizes the 5 reports into one organized brief for Joe. See `references/multi-perspective-review.md` for full lens prompts, synthesis methodology, and reviewer templates.

   **Fallback: Single Critic.** One sub-agent covering all 10 categories. Faster setup, shallower coverage. Use when time matters more than depth.

   The critic gets NO context about prior iterations.
3. **Grade the result.** A+: ship. B+: ship with minor fixes. B: needs one more pass. C+: needs two passes. C− or below: structural problems.
4. **Apply fixes.** Fix criticals first, then majors. Cut underperformers. Redistribute density. Iterate.
5. **Re-spin.** New sub-agent(s), same prompt(s). Iterate until B+ or A−.

### Single Critic Prompt Pattern (Fallback)

The sub-agent needs a **self-contained prompt** with these 10 evaluation categories:

1. Faction coherence — does the set play like one faction?
2. Synergy web integrity — are edges realized, or aspirational fiction?
3. Curve and tempo — does the curve support the archetype?
4. Legendary impact — do the 4 legendaries feel legendary?
5. Draft environment — commons, vanillas, removal density, parasitic risk
6. Blind spot compliance — does the faction do things it shouldn't?
7. Hero design — distinct, thematic, balanced?
8. Killer cards — what dominates? What's unplayable?
9. Fun factor — moment-to-moment experience
10. MTG distinctiveness — does this feel like something MTG can't do?

The critic should be **ruthless, not polite.** "A 75 is better than a padded 90." For each problem: severity (Critical/Major/Minor), which cards, why it's a problem, suggested fix. End with letter grade and status (ship-ready / needs iteration / needs rebuild).

### Proven Results (Trigger 2026-06-07)

- v2: C− — Contract undefined, Locked On 2 cards, Francis Cage unplayable, zero healing, keyword salad
- v3: B — keyword sidebar added, Locked On 2→6, Francis Cage redesigned, heroes reworked
- v4: B+ — Contract auto-cycling, Locked On 6 three-tier, healing added, edge counts audited

The loop caught annotation errors, missing density (Locked On at 2 cards with its own hero), unplayable legendaries (Francis Cage 6/3 win-more), naming conflicts (Reload keyword vs Reload spell), and the Ambush anti-synergy (Locked On on reactive cards).

**Key insight:** Two critic passes with fixes between them got the set from C− to B+ in one session. The critic is a force multiplier — it catches what the designer is too close to see.

## Verification (Post-Build)

After writing the card roster, run these checks before declaring done. Skipping verification = shipping unverified counts.

### Card Count Verification (grep pitfall)

Card tables in markdown code blocks use column alignment. Single-digit card numbers get a leading space; two-digit numbers don't. The correct grep pattern:

```bash
# Count ALL card entries (handles both " 7" and "10" formats)
grep -cP '^\w\s+\d\s+' roster.md
```

**PITFALL:** Using `^\s+` (one-or-more spaces) misses two-digit card numbers (10-30) because they start flush. Use `^\w\s+` (rarity letter + space + digit). This cost 15 minutes of debugging on Trigger v2.

### Function Annotation Audit (2026-06-06)

After writing all card rows, audit every card's function annotations against its actual mechanics:

```bash
# Cards claiming F12 (Cloak) — verify they actually have Cloak
grep "F12" roster.md | grep -v "Cloak"

# Cards claiming F14 (Hustle) — verify they actually have Hustle
grep "F14" roster.md | grep -v "Hustle"
```

**PITFALL: Swapping F12 and F14.** On Trigger v3 (2026-06-06), Cloak (F12) and Hustle (F14) function IDs were systematically swapped across 5+ cards. Wallflower (Cloak) claimed F14. Banger (Hustle) claimed F12. This cascaded into wrong synergy edge assignments. The root cause: writing function annotations from memory instead of referencing a function ID table. Always write down F01-F18 definitions before annotating cards.

### Per-Band Rarity Audit

```bash
for v in 1 2 3 4 5 6; do
  echo "--- ${v}V ---"
  for r in C U R L; do
    count=$(grep -cP "^$r\s+$v\s+" roster.md)
    if [ "$count" -gt 0 ]; then echo "  $r: $count"; fi
  done
done
```

This catches hidden drift — a C→U promotion in one band that wasn't balanced elsewhere. Trigger v4 drifted to 26C/16R before this check caught it.

### Curve Distribution Check

```bash
for v in 1 2 3 4 5 6; do
  count=$(grep -cP "^\s*\d+\s+[CURL]\s+${v}\s+" roster.md)
  echo "${v}V: $count"
done
```

**Drift tolerance:** ±1 per band is acceptable if the curve shape holds (heaviest at 2-3V for midrange, tapering at 4V, power spikes at 5-6V). Document any drift in design notes. The total count (55) is non-negotiable.

### Rarity Check

```bash
for r in C U R L; do
  count=$(grep -cP "^\s*\d+\s+${r}\s+\d\s+" roster.md)
  echo "$r: $count"
done
```

Target: C ~25 (45%), U ~17 (31%), R ~10 (18%), L 3 (5%). ±2 drift acceptable for first-set commons.

### Synergy Web Audit

After writing the roster, cross-reference every synergy web edge (W01-W14) against actual card text. An edge is "realized" if both cards exist and their abilities create the described interaction. Document the audit in design notes.

### Design Parameter Checklist

Verify every locked parameter from the latest function registry + playstyle matrix:
- **Legendary picks:** 4 total (2 minion, 1 spell, 1 weapon for weapon factions; adjust for non-weapon factions)
- **Heroes:** 3, not counted in the 55-card roster
- **Barrage sources:** 1-2 (elite-only — Legendary + maybe one Rare)
- **Cloak sources:** 2-3 (small placement, high-end Professionals)
- **Hustle sources:** 2-3 (Street tier)
- **Mark density:** 6-10 cards with Mark (battlecry, spell, triggered, deathrattle)
- **Direct hero damage spells:** 1-2 (exists — not a blind spot)
- **Curve cap:** 6V (no 7V+)
- **Taunt:** 0 (Bruiser territory — hard blind spot)
- **International characters:** 0 (expansion only)
- **Ghosts:** Lore-only in Founder's Edition. No Ghost cards.

**Do NOT verify stale parameters from overnight runs.** Ghost Permanents, Hidden
Contract, Simultaneous Hidden Choice, Cover scaling, The Forger — all BANK/NOT
SHIP and should not appear in any checklist. If a parameter appears in a warmup
doc but the referenced source file is marked BANK/NOT SHIP, the parameter is dead.

### Warmup Document Pattern

For autonomous overnight builds, a self-contained warmup document (see `references/warmup-document-pattern.md`) is the most reliable launch method. It should contain: Phase 0 (all documents to read, in order), Phase 1 (function registry, pre-built), Phase 2 (synergy web, pre-built), Phase 3 (band allocation targets), Phase 4 (Living World Method steps), Phase 5 (faction locked parameters), Phase 6 (output file specs), Phase 7 (rules/anti-patterns). A fresh instance dropped into this document can produce a complete 55-card set without additional steering.

## Design Authority

Joe operates above design rules. Paul's job: flag violations clearly, accept Joe's override. Flag it once, state your case, move on.

## Paul's Workspace

`/root/.hermes/docs/Paul/workspace/` — all drafts go here.
Dropbox: `/root/syncthing/paul-dropbox/` — completed work for Cursor/Joe pickup.
tcg-engine repo at `/root/tcg-engine/` is READ-ONLY (except `docs/Paul_Handoff/incoming/`).

## Faction-Specific Design References

- **Trigger:** `references/trigger-design-corrections.md` — Mark-as-bonus philosophy, Court control pattern, Locked On terminology, Honed cut, crew distribution targets. Load this before any Trigger design work.
- **Salvage methodology:** When mining an existing faction's card list for reusable material, apply the four-question test: (1) Does it map to ≥1 function in the new registry? (2) Does it touch ≥1 synergy web edge? (3) Does it respect crew distribution? (4) If yes to all three → salvage. If no → bank or rework. Joe: "Use it as inspiration primarily, and steal what's worth a damn in name or ability." Names can be salvaged even when mechanics change — Bearcat went from 2V vanilla to a different role, but the name survived. Bathroom Break stayed because Joe liked it. Don't force-salvage cards that don't fit the new web just because they exist.

## Design Pillars (Game-Level Rules)

See `references/design-pillars-2026-06-05.md` — faction mixing penalty (+1V/+2V), cross-faction synergy scarcity ("target friendly Bruiser minion"), Hearthstone as structural analog, success criteria for Five Crests decks, design philosophy. Locked by Joe 2026-06-05. These apply to ALL faction design work, not just Trigger.

## Orchestrator Pattern — Overnight Autonomous Builds

When spawning a fresh Paul instance for overnight card design, the orchestrator (you) must:

### 1. Build the Warmup Document

A self-contained brief (see `references/warmup-document-pattern.md`). Contains: function registry, synergy web, band allocation, lore references, process steps, output specs. The fresh instance reads this ONE file and follows the references.

### 2. Spawn the Instance

**Use tmux. Not cron. Not `hermes chat -q`.**

Three methods tested 2026-06-05:
- **cronjob**: scheduler ticker unreliable on VPS — jobs stuck in "scheduled" state
- **`hermes chat -q`**: exited after single turn, does not perform multi-step autonomous work
- **tmux**: works. The only reliable method.

```bash
# Start
tmux new-session -d -s trigger_factory -x 160 -y 50 'hermes --model deepseek-v4-pro --provider deepseek'

# Wait for init (10s)
sleep 10

# Send prompt
tmux send-keys -t trigger_factory "<prompt>" Enter
```

### 3. Monitor Progress

Check every 2-3 minutes:

```bash
tmux capture-pane -t trigger_factory -p | tail -25
```

Watch for: document reads completing, plan task progress, context not blowing out. If the instance is stuck thinking for 5+ minutes with no tool calls, it's either doing heavy synthesis (normal) or stalled (check if context hit limit).

### 4. Validate Outputs

When files appear in the workspace:
- Verify file sizes are non-trivial (>10KB for roster, >8KB for design notes)
- Run card count verification (see Verification section below)
- Check all three files exist (roster, design notes, heroes)
- Confirm copies in `/root/syncthing/paul-dropbox/`

### 5. Do NOT Hand v1 Set to Fresh Instance

If you built a first-pass set and it was rejected for skipping the pipeline, do NOT include it in the warmup doc. The fresh instance will treat it as the answer and tweak rather than build from the function registry. The warmup doc should contain: function registry, synergy web, band allocation, lore docs, process steps. NOT a reference set.

### 6. Pre-Lock Legendary Picks

Specify Legendary picks with exact rarity, card type, and cost (e.g., "Mr. Fox — L/6V Hitter minion"). Mark them LOCKED. Add a rule in the warmup: "If you find a better Legendary during design, you may substitute, but MUST flag the deviation prominently in Design Notes and update the roster header." The Trigger v2 instance changed the third Legendary (Smoke and Mirrors → Everybody Pays) mid-design without updating the header — the roster said one thing, the cards said another. Locking prevents this.

## Sub-Agent Card Production Pipeline (Proven 2026-06-08)

End-to-end pipeline from spec lock to passing 55-card set. Produced Trigger v7 at A- in one session.

**Orchestrator integration:** The `orchestrator` skill (`creative/orchestrator`) now manages this pipeline autonomously — spawning workers, running critics, tracking delta, and escalating when flat. Pipeline specs live at `workspace/pipelines/`. See `workspace/pipelines/trigger-card-design.yaml` for the reference implementation. The orchestrator was proven end-to-end on 2026-06-08: Phase 1 (spec-validate) caught 2 Critical contradictions, Phase 2 (card-design) spawned 3 parallel workers, pre-gate caught mechanical issues. The loop works.

### Phase 1: Spec Lock Sprint (Collaborative — Joe + Paul)

Lock everything a sub-agent needs BEFORE spawning anyone:

1. Crew CAN/CANNOT profiles (one table, hard boundaries)
2. Living World anchors (identity paragraphs per crew — the WHO, not the mechanics)
3. Archetype turn maps (T1-T6 ideal sequences per pathway, V-banded, with hero power integration, interaction turns, recovery lines, Management/Help cross-pathway support)
4. Density targets (mechanic × crew matrix, V-band distribution)
5. Slot table (every row has crew, rarity, V-band, mechanical spec, edge targets, pathway tag, partner references)
6. Sub-agent instructions (design rules, naming conventions, geographic anchors, pre-design audit step, output format)

**PITFALL: Insufficient detail at spec time.** Sub-agents only read what's in the spec file. Every conversational nuance — crew flavor details, mechanic philosophy, cross-pathway interactions — must be WRITTEN INTO THE SPEC. If it's only in chat, it doesn't reach the sub-agent. Joe (voice memo, 2026-06-08): "If you don't flesh out all the little intricate details, then none of that stuff is going to make it into the spec."

### Phase 2: Validator Sub-Agent (Autonomous)

BEFORE spawning card-design sub-agents, run a validator sub-agent against the spec. Checks: slot table math vs. build facts (crew budgets, rarity caps, V-band totals, mechanic density), crew bleed (Street with Paid, Help with card draw), pathway coverage gaps, edge coverage. Trigger spec v1 had 7 blocking math errors — crew budgets 50-150% over, rarity overflow, Overkill at 2x target. The validator caught them all. Fixing the spec prevents 55+ cards of rework.

### Phase 3: Parallel Card Design (Autonomous)

Spawn 3 sub-agents in parallel, split by V-band:
- Batch 1: 1V-2V cards
- Batch 2: 3V-4V cards
- Batch 3: 5V-6V cards + legendaries + weapons

Each sub-agent gets: full spec file + function registry + build facts + keyword sidebar. Each sub-agent must be told explicitly: "WRITE OUTPUT TO FILE." Sub-agents return summaries by default — instructions must include file write requirement.

### Phase 4: Assembly + Audit (Autonomous)

Paul assembles the 3 batch outputs into a combined set file. Run `pre_review_audit.py` immediately. Fix failures, re-run. Iterate until CLEAN. The script catches: card counts, rarity, keyword sidebar, edge density, curve, 1V slot, blind spots, vanillas, healing, naming conflicts.

**PITFALL: pre_review_audit.py format mismatch.** The script expects specific column order in card tables. If card format differs, the script returns zero cards found. **Permanent fix (2026-06-08): Do NOT patch the script. Enforce exact output format in the SubAgent Spec.** Add mandatory copy-pasteable templates for every card type under exact `## Minions`, `## Spells`, `## Ambushes`, `## Weapons` section headers. Three Trigger iterations failed on format drift before this fix. See `references/sub-agent-card-production.md` § Format Compatibility for the exact templates and verification commands. The old advice to patch `parse_card_table()` is wrong — it masks the problem. Enforce format at spec time, never convert after the fact.

**PITFALL: Sub-agents produce mixed card formats.** When spawning parallel card-design sub-agents, different workers WILL use different output formats — some use `·` separators, some use pipe tables with `| # | V | Name | R | Crew | ATK/HP | Text | Edge |`, some use `| # | V | Name | R | Cw | ATK/HP | Text | Edge |`. None match the script's expected `| # | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |`. The assembly step MUST normalize all batch outputs to a single format before running pre_review_audit.py. Proven on the first orchestrator run (2026-06-08): 3 batches × 3 formats = normalization script required before audit could parse any cards. See `scripts/normalize_card_batches.py` for the conversion utility.

### Phase 5: Critic Review (Autonomous)

Run the faction-set-review Pass 2-3 critic via sub-agent. Only review subjective stuff (fun factor, legendary impact, ludo, draft feel) — the audit script already caught mechanical issues. Apply critic fixes. Target B+ or higher.

**Two-layer review is minimum viable (2026-06-08):** `pre_review_audit.py` catches mechanical issues (card counts, rarity, keywords, edge density, curve, blind spots, vanillas, healing). Critic sub-agent catches subjective issues (fun factor, legendary impact, ludo coherence, draft feel, name collisions, paper edges). Both are required. Never ship a set that passes only one. Trigger v7 passed audit but critic found E12 paper edge, S20 floor, and name collision — problems the script couldn't see.

### Phase 6: Ship

Final audit pass. Dropbox copy. Daily Handover update. Git push.

---

## Sub-Agent Usage

Reserved for: parallel faction design, Red Team review passes, flavor passes, critic reviews, spec validation.
Paul designs the function registry and synergy web directly — sub-agents can't see the cross-slot picture.
Card-level design is sub-agent territory — use 3 parallel sub-agents split by V-band. Never design 55 cards sequentially.

**PITFALL: Sub-agents without creative context produce MadLibs (2026-06-08 — CRITICAL).** A slot table + crew CAN/CANNOT matrix + density targets is NOT sufficient for card-design sub-agents. Without the creative layer — faction lore docs, character profiles, Daily Life vignettes, location anchors, crew identity paragraphs — sub-agents produce mechanically correct cards with no soul. Trigger v7 passed every audit, graded A- by the critic, and Joe called it "dog shit" that "lacks a fundamental understanding of what the faction is." The set was spreadsheet cells with names. This is the same MadLibs failure mode as the cascade tests, just with cleaner math.

The sub-agent context MUST include, at minimum:
- `Inner_Circle.md` — who these people are, their relationships, the power structure
- `Daily_Life.md` — the Tuesday at 7am texture, the smells, the rhythms
- Character profiles — named characters with backstories and motivations
- Location anchors — where do these people live, work, fight, drink?
- The creative identity paragraphs from the Living World Anchors section

**Division of labor (Joe, 2026-06-08):** The creative layer and the mechanical layer are different work. Sub-agents need BOTH. Without the creative layer, you get Sculptor — a word that fits a slot but isn't a card. Without the mechanical layer, you get flavor text with no gameplay. The sub-agent spec must carry the full faction corpus, not just the spreadsheet.

**The sub-agent IS you.** Sub-agents have access to the same memory, AGENTS.md, SOUL.md, skills, and tools. They CAN design with taste if they're given the creative context. The failure is not the sub-agent's capability — it's the orchestrator handing them a spreadsheet and saying "fill these slots" instead of saying "here's who works in this crew, here's what their day looks like, here's what they want. What card would this person be?"

**PITFALL: Mechanical correctness ≠ good cards (2026-06-08).** A set can pass every audit — card counts, rarity, keywords, edge density, curve, blind spots, vanillas, healing, name uniqueness — and still be creatively dead. The critic grade is meaningless if the critic only reviews mechanical cohesion. A- on soulless cards is a LIED grade. Never confuse "passing the audit" with "good enough to show Joe."

**PITFALL: Sub-agents remix existing cards when lore docs leak established names (2026-06-09 — CRITICAL).** If the faction already has cards in the tcg-engine repo (Founders Edition, prior passes), sub-agents will reuse those card names. Faceless v2 was SCRAPPED — 42/52 cards (81%) shared names with Joe's originals. The legendaries were near word-for-word identical. Root cause: the Identity Bible fed to sub-agents contained established character names (Lamb, Street Preacher, The Anointed, Temple Guardian, etc.). Sub-agents saw those names in the lore and reproduced Joe's existing designs instead of creating new cards.

**Prevention (mandatory before any card-design sub-agent spawn):**
1. **NO EXISTING NAMES directive** — every worker prompt must say: "These lore concepts exist as cards in the tcg-engine repo. Do NOT reuse any card name from the Founders Edition or any existing set. Design NEW cards that express the faction's identity."
2. **Scrub card-name references from lore docs** — feed sub-agents thematic direction and identity concepts without established character names where possible. "The faction recruits Lambs" → "The faction recruits vulnerable newcomers who serve as sacrifice fodder." Give the concept, not the name.
3. **Post-production dedup check** — after assembly, grep the combined set for card names against existing faction sets in the tcg-engine repo. Flag anything >50% overlap. Do not ship until verified.

This is NOT a format or mechanical failure — it's an identity failure. The set LOOKS original (different stats, remixed mechanics) but ISN'T (same names, same concepts, same creative DNA). Joe: "It literally looks like it verbatim copied and pasted my existing cards into it." The autonomy claim was false. Never ship a set without verifying name novelty.

### Batch Card Production by V-Band (Proven Pattern)

After the spec is locked and validated, split the complete card set across 3 sub-agents by V-band tier. Each gets the identical full spec + all reference docs. This produced a 55-card Trigger set in ~5 minutes per batch (2026-06-08).

| Batch | V-Band | Cards | Notes |
|-------|--------|-------|-------|
| 1 | 1V–2V | ~20 | Minions, spells, weapons at low curve. Vanillas and draft fodder live here. |
| 2 | 3V–4V | ~22 | Midrange payoff. Core mechanics at full power. Ambushes, Special Ammo, Contract Scaling. |
| 3 | 5V–6V | ~13 | Finishers and legendaries. Curve-toppers. The cards players remember. |

**Context per sub-agent:** The full spec file + function registry + build facts + keyword sidebar. Do NOT trim context — the sub-agent needs the CAN/CANNOT matrix, living world anchors, naming conventions, and geographic anchors to produce correct-flavor cards. Crew bleed is the #1 failure mode when sub-agents lack the full constraint surface.

**Before spawning:** The spec MUST pass the validator step (see Spec Validation Step above). Sub-agents spawned against unreconciled specs will produce cards with crew bleed, wrong rarity counts, and broken mechanic density — exactly the 5-6 iteration loop the spec lock sprint is meant to prevent.

**After all three batches return:** Assemble into a single set file and run `pre_review_audit.py`. The automated gate catches count errors, rarity drift, keyword mismatches, and blind spot violations the sub-agents may have introduced.

## Reference

Full methodology details preserved in `references/full-methodology.md`.
The authoritative design doc is `docs/Five_Crests/game/DESIGN_GUIDELINES.md` in the tcg-engine repo — BUT the pipeline within it may be corrupted from ~8500 merged documents. The correct pipeline is in this skill and in `references/card-production-pipeline-v2.md`.
Autonomous build pattern: `references/warmup-document-pattern.md` — proven trigger for fresh-instance faction builds.
Verification patterns: see Verification section above (grep counting, curve/rarity checks, parameter audit).
Sub-agent card production workflow (proven 2026-06-08): `references/sub-agent-card-production.md` — prompt templates, format compatibility, kaizen notes.
Verification patterns: see Verification section above (grep counting, curve/rarity checks, parameter audit).

## Changelog

**2026-06-09** — Added PITFALL: Sub-agents remix existing cards when lore docs leak established names. Faceless v2 SCRAPPED — 81% name overlap with Joe's originals. Prevention: NO EXISTING NAMES directive in every worker prompt, scrub card-name references from lore docs before feeding to sub-agents, post-production dedup check against existing faction sets. This is a CRITICAL failure mode — the set passes all mechanical gates but is creatively fraudulent.

**2026-06-08 (orchestrator first run)** — Added PITFALL: Warmup crew profiles must be cross-referenced against locked function registry. Trigger spec-validate run caught Management/Mark and Silence ownership contradictions between warmup profiles and locked registry/v6 cards. Spec-lock sessions must reconcile crew profiles against the registry before declaring the spec locked.: Modeling mechanics from memory instead of keyword sidebar. Overkill cumulative-vs-per-turn mistake required full pathway rewrite. Rule: re-read keyword sidebar before building any turn map. Added "Batch Card Production by V-Band" pattern to Sub-Agent Usage section — 3 sub-agents split by curve tier, proven on 55-card Trigger set. Updated Spec Validation Step with slot-table reconciliation details (crew budgets, rarity caps, V-band sums, mechanic density).

**2026-06-08 (Faceless clean-slate build)** — Added Steps 10 (Competitive Slotting) and 11 (Stress Testing) to the mandatory pipeline, between Expressions (9) and Quality Gates (12). Added `references/competitive-slotting-stress-testing.md` with full methodology, output formats, and Faceless proven results. Added pitfalls: Keyword bleed (Exile vs Purge), Multi-archetype stress testing required.: 5-lens card set review (Tone, Design, Identity, Flavor, Digital-Native) and 4-lens process doc review (Clarity, Completeness, Kaizen, Consistency). Reviewer prompt templates. Synthesis methodology. Added "Spec Lock Sprint" concept to Pre-Expression Gate — lock specs before spawning card-design sub-agents. Updated Step 10 review loop to show multi-perspective as primary pattern, single critic as fallback.

**2026-06-06 (function registry session)** — Added three new pitfalls: inventing blind spots Joe never locked, treating Mark as gating requirement instead of bonus multiplier, using shorthand terminology that diverges from locked mechanic names. Added function registry consolidation rules (subsidiary, build facts, design principles, one-card expressions, iterative collapse, complexity tax, same-mechanic, pillar organization, legacy Functions.md trap). Added Joe review format — present functions one at a time, four things each. Added `references/trigger-design-corrections.md` — Mark-as-bonus philosophy, Court control pattern, Locked On terminology, Honed cut, crew distribution targets. Updated Pre-Expression Gate to consolidate function count band (12-18 → ~16). Updated Step 5 to capture review format and consolidation rules.\n\n**2026-06-06 (late)** — Major pipeline revision. Added Step 0: Villium Relationship (mandatory pre-design gate, LOCK before functions). Moved keyword lock from Step 6 to after Step 10 — keywords surface organically from built card sets, not declared upfront. 3 cards = card text, 10+ = keyword. Updated Pre-Expression Gate checklist accordingly ("Mechanics: keyword lock" → "Mechanics: levers defined. Keyword candidates noted, NOT locked").

**2026-06-06 (late)** — Function registry consolidation rules added (Joe lock). Subsidiary rule: fold byproducts into parent functions. Build facts and design principles are NOT functions. One-card Rare+ expressions stay under parent. Target ~16 after consolidation pass. Added PITFALL: over-granular function registries.

**2026-06-06 (late)** — Removed stale HERMES_BOOT.md reference from "Working from a stale repo" pitfall.

**2026-06-06** — Added PITFALL: Reading entire documents for simple factual queries. Use `search_files` + `read_file(offset, limit)` for targeted corpus retrieval instead of burning context on whole-document reads.

**2026-06-06** — Added nav-layer pitfall: STATE_OF_THE_CORPUS.md and TOOLS_INDEX.md live in tcg-engine repo (`/root/tcg-engine/docs/Five_Crests/`), not Paul's vault. Warmup docs may reference by short name without full path. Updated `references/warmup-document-pattern.md`: added second use case (Joe+Paul direct sessions as handoff/continuity docs), fixed duplicate line.

**2026-06-05 (late)** — Added Verification section: grep patterns for card counting (with `^\\s*` vs `^\\s+` pitfall), curve/rarity distribution checks, synergy web audit, design parameter checklist. Added `references/warmup-document-pattern.md` — proven autonomous build template validated on Trigger v2 (55 cards, zero mid-build corrections).

**2026-06-05** — Major restructure. Slimmed from 100K+ to focused pipeline. Added mandatory navigation-layer step. Added Living World Method. Added function registry to synergy web to card row sequence. Encoded "never open card table before function registry" as hard rule. Pitfall: skipping nav layer leads to MadLibs roster. Reference material moved to `references/full-methodology.md`.
