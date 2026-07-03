---
name: tcg-faction-lore-phase
description: Phase 0 lore lock for Five Crests TCG faction design — crew structure, identity bible, generational tension, client relationships, and NOT lists. Applies to any faction (Bruiser, Trigger, Duster, Faceless, Skiver, Stiffs).
---

# TCG Faction Lore Phase (Phase 0)

The lore lock phase establishes a faction's identity, crew structure, and thematic boundaries before card mechanics begin. This is a Joe+Paul collaborative process — Paul drafts, Joe brainstorms and locks.

## Trigger

Begin when Joe says he wants to start lore/Phase 0 work on a faction, or when a new faction enters the design pipeline and needs its identity bible.

## Process

### 0. Canon Alignment — MANDATORY First Step

**Before writing a single word of identity prose, diff your source material against live canon.** A spec is a snapshot. Live canon moves. The compendium or warmup you're working from may have been superseded by DCW promotion, Joe lock decisions, or later lore sessions. If you build from outdated material and run the cohesion check afterward, you'll burn a full revision cycle on contradictions that were detectable before you started.

**Hard rule:** When a warmup, compendium, or design brief points you at a source document, load that faction's live canon files FIRST and diff them. If the source says X and live canon says Y, live canon wins. Flag the discrepancy to Joe before building — don't silently override, and don't build from the outdated version hoping it'll be fine.

**Methodology:**
1. Load the faction's `00_INDEX.md` — identifies which docs are CANON vs HARVESTED vs DRAFT. CANON docs have the highest authority.
2. Load all CANON and HARVESTED docs for that faction (`Identity.md`, `Inner_Circle.md`, `Territory.md`, `Playstyle.md`, `Mechanics.md`).
3. Load relevant `core/` docs that may contain locked origin stories (`core/05_Commission.md` § faction sections, `core/03_Villium/`).
4. Read your source material (warmup prompt, compendium, intake brief) in full.
5. Build a discrepancy table: every place the source material contradicts live canon. Include the canon doc, the locked decision ID if applicable (C-01, P-02, etc.), and the conflicting text.
6. Present the discrepancy table to Joe. "I found these contradictions between the warmup source and live canon. Which version governs?" Joe decides before you write a word.
7. Only after Joe rules on all discrepancies, proceed to § 1 (Source Intake) and begin building.

**Faceless worked example (2026-06-06):** The warmup pointed to `Faceless_Complete_Faction_Lore_v1.md` (May 26) as authoritative source. That compendium said Tony didn't know Henry was alive and the jail visitor was ambiguous. But `Inner_Circle.md` had been promoted to CANON via DCW Beat 1 (June 5) with Joe locks C-01 (Tony knows Henry is alive) and C-02 (founding timeline: Henry bailed Robert out in person after the car bomb). The bible was built from the outdated compendium — three critical contradictions found at the post-build cohesion gate. If the canon alignment diff had been run first, the contradictions would have been caught before a single paragraph was written. Instead: v1 → v2 rewrite → v3 canon alignment fix. Three versions where one would have sufficed.

### 1. Source Intake

With canon discrepancies resolved (§ 0), read the full body of source material:

- `docs/Five_Crests/factions/{Faction}/Identity.md` — if CANON or HARVESTED
- `docs/Five_Crests/factions/{Faction}/Inner_Circle.md` — if CANON or HARVESTED
- `docs/Five_Crests/factions/{Faction}/Territory.md` — if CANON or HARVESTED
- `docs/Five_Crests/factions/{Faction}/Playstyle.md` — if CANON or HARVESTED
- `docs/Five_Crests/factions/{Faction}/Mechanics.md` — if CANON or HARVESTED
- `docs/Five_Crests/factions/{Faction}/{Faction}_Cards.md` — factory reference
- The warmup, compendium, or intake brief being used as the build spec

Also check Paul's workspace for any existing draft bibles or pipeline docs.

### 2. Identify the Emotional Chords (Before Writing)

**Before drafting any lore or cards, identify 3-5 emotional truths a real person would recognize themselves in.** These are not marketing hooks — they are the things that make someone read a card and go quiet for a second. Every section, every character, every mechanical hook, and every flavor text must hit at least one of these chords.

**Duster example (2026-06-06):**
1. Belonging you built yourself — "Nobody wanted us. So we built something that can't be thrown away again."
2. The cost you know and pay anyway — "I know what this does. I'm doing it anyway. The fragments are real."
3. The parent-shaped hole — "He knew. He could have come. Now I have the keys."
4. Autonomy as identity — "We're not asking permission. We're choosing to behave."
5. Inheritance as burden and gift — "My mother wrote down everything. I've memorized every word."

**Pitfall:** If a paragraph describes without resonating — if it says *what* the faction is without making you *feel* it — cut it. The chords are your design compass. Every crew should have a primary chord, every hero should deliver one chord through their voice line and kit, and every card's flavor text should land on a chord without needing a lore doc to explain it. End the lore pass with a chord distribution map showing which cards/characters hit which chords.

### 3. Draft the One-Line Thesis

One sentence that captures the faction's essence. Should be quotable. Should make someone understand the faction instantly.

**Trigger example:** *"Your name came across my desk. Now it's paperwork."*

### 4. Who They Are

Core identity. What they do. Who they serve. Their relationship to the Commission and other factions. Their operating philosophy. Keep it tight — a paragraph, maybe two.

### 5. Who They Are NOT

**Critical section.** This is where factions differentiate from each other. Pitfall: being too rigid. "NOT gangsters" was wrong for Trigger because lower-tier members ARE gangsters — they hold blocks and run rackets. The NOT list should capture the faction's genuine boundaries, not aspirational purity.

For each other faction, state the relationship:

| Other Faction | What Trigger Is NOT | Actual Relationship |
|---------------|---------------------|---------------------|
| Bruiser | NOT bruisers — don't street-fight, don't hold territory block-by-block | Partners. 1950s rail-yard war settled at Commission table |
| Skiver | NOT gutter rats | Mutual disdain. But money is green — Skivers can be clients |
| Faceless | NOT a cult | Agnostic. The Code is discipline, not scripture. Everyone's a client |
| Stiffs | NOT cops | Criminal-on-cop work carries a premium. They share channels but not purpose |

### 6. Leadership

Three roles typically: Machine (operational reality), Working Face (public operator), Figurehead (Commission seat). The Machine is often the most interesting — the person who actually runs things but isn't the official leader.

### 7. Crew Structure

This is where most sessions spend their time. Joe thinks in tiers/ladders, not flat divisions.

**Methodology:**
- Start from the bottom (civilian-adjacent support) and work up to the top (management/information layer)
- Every tier needs: who they are, what they do, how they live, path upward, card lane, and a "vibe" — a concrete image or reference that makes them feel real
- The middle tiers often have sub-tiers within an umbrella (e.g., The Hitters containing Professionals, Court, Ghosts)
- Don't force every tier to be a playable archetype — some tiers (Help, Management) are enablers, not standalone decks

**Naming conventions:**
- Keep names short, period-appropriate (1961), and conversational. "He's Court." "Talk to Management." "I need some help."
- The opulent upper echelon needs a name that screams filthy rich, period-specific, rolls off the tongue like a celebrity moniker
- Use the "street-fight callout test": would someone say this name in conversation? "The Gilded Court" fails. "The Court" passes.

**Valid tier types:**
- Enablers: civilian-adjacent support who don't fight but facilitate (The Help)
- Disposable: lowest-level operators, plausible deniability, maintain criminal enterprises (Street)
- Core operators: the faction's main verb — the people who do the thing the faction exists to do (The Hitters — umbrella with sub-tiers)
- Elite ascended: top of the core operator pyramid — flashy or invisible, the boogeyman tier (Court, Ghosts)
- Management: information layer, contract routing, the brain of the faction (Management/Switchboard)

### 8. Generational Tension

Every Five Crests faction has an Old Way vs. New Way tension. This is not good vs. evil — both sides have valid points. The tension expresses mechanically: Old Way rewards patience, setup, the long game. New Way rewards speed, aggression, immediate payoff. One character typically bridges both (Lucy for Trigger).

**Key questions to answer:**
- What generation built the Old Way? (WWII, Korea for Trigger)
- What generation is pushing the New Way? (1960s coming-of-age for Trigger)
- Who bridges them?
- Where does the tension sit in the current year (1961)? Is it emerged or emerging?

### 9. Client Relationships

How does the faction relate to other factions as clients? Trigger is uniquely agnostic — money is green, period. This has mechanical implications (low splash cost). Other factions may have different stances. Document:
- Who they'll work with
- Who carries a premium
- Any absolute refusals

### 10. Texture Scenes

4-6 short prose scenes that make the faction feel lived-in. Each scene anchors to a specific location and shows the faction doing what it does. These are not lore dumps — they're moments. One character, one room, one action. See `references/trigger-example.md` for the full set.

### 11. Daily Life & Rackets

**When Joe asks "what does a day in the life look like?" — stop thinking in card mechanics. Write inhabited vignettes.**

This section answers: What does a Tuesday look like for someone at each tier? What revenue streams keep the faction running? What front businesses wash the money? What services do they provide to the city's elite?

**Methodology:**
- Walk through a 24-hour clock. Show the faction's rhythm: morning (press run, bench work, routing), afternoon (fittings, library, Continental floor), evening (collections, high-stakes games), night (cleanup, smuggling, the jobs nobody sees)
- Cover every tier: Management (the nerve center), operators (the work), support (the enablers), street (compliance and feeder league)
- Identify revenue streams: rackets, fronts, elite services, legitimate business fronts
- Map the money: how does dirty cash flow from street collection → cash-heavy front businesses → Commission-controlled banks?
- Identify what the city's wealthy elite need and how the faction provides it (information, access, security, laundering, vice, fencing, import/export)

**Front business patterns:** Laundromats, car washes, strip clubs, bars, diners — anywhere with high cash turnover, coins, and no expectation of receipts. Used car lots are especially valuable: cash-heavy, vehicle rotation for clean rides, cover for import/export logistics.

**The false bottom:** Street-level crime is visible by design — it's what the Stiffs see. The real operation (nerve center, elite services, banking, import/export) runs above it, invisible. The street crime hides the real crime. This is a core faction design principle for professional/high-end factions.

**Elite services catalog:** If the faction operates among the city's wealthy (law firms, banks, corporate HQs), map what the elite need that they can't get legally: information (vetting, insider trading, blackmail), access/introductions/favors (the Commission's ear), security (legit and illegitimate), money laundering (clean money, untraceable transactions), high-end vice (drugs, escorts, high-roller gambling), high-end fencing (priceless artifacts, paintings, archaeology), import/export (Villium global operations, black market sales).

### 12. Support Network

**For professional-operations factions (assassins, spies, thieves): brainstorm what a {operative} needs to do their job.**

This is a separate design exercise from crew structure. It answers: aside from the core verb (killing, stealing, etc.), what infrastructure enables the work?

**Categories to explore:**
- Medical (trauma surgeon, Villium dosing)
- Transportation (drivers, motor pool, clean vehicles, private hangar)
- Documents (forgery, fake IDs, passports, credentials, badges)
- Target preparation (research, advance casing, wiretaps, counter-surveillance)
- Equipment (weapons, kit, quartermaster)
- Wardrobe/disguise (tailor for high-end, costume specialist for practical)
- Disposal (standard cleanup crew, high-end cleaner for political jobs)
- Training (range instructor, tactical drills, new-gun checkout)
- Hospitality (safehouse keepers, Continental floor staff, front-desk gatekeeping)
- Communications (Switchboard, codes, dead drops, counter-surveillance)
- Legal/alibi (on-retainer law firm, backdated receipts, witness management)

Each role gets: a name, a backstory (one paragraph), a specific function, and a card-design hook. Not every role gets a card — some are pure lore. Not every role gets a name — some are role-based like Bruiser crew positions (Handyman, Wireman). See `references/trigger-support-network.md` for a worked example covering 16 support roles across 9 categories with full backstories and card hooks.

### 13. NOT List (Mechanical)

Separate from the identity NOT list. These are mechanical design constraints:
- No unconditional healing
- No AOE board clears (except hero pseudo-AOE)
- No weapon-free top end (for weapon factions)
- No emotion-driven cards (for professional factions)
- No swarm bodies (for weapon/kill-focused factions)

### 14. Keyword Lock

Map keywords to crews. This shows which crew enables which mechanics. Faction-primary keywords vs. universal keywords.

### 15. Win Lines

One per hero/archetype. Keep these high-level — the detailed mechanics come in Phase 1 (Framework).

### 16. Contrast Anchor (A8)

Every faction needs an explicit contrast against its closest sibling. This is not "who they hate" — it's "who they're most often compared to, and why they're different." The contrast anchor is usually the faction's natural partner within the Commission structure.

**Structure:** A comparison table across key axes (bond, temperature, violence, method, identity) followed by a key insight paragraph. The table should make the factions feel like two halves of the same brain — complementary, not competitive.

**Trigger example:** Bruiser = hot, family, visible violence, stand-and-fight. Trigger = cold, contract, invisible violence, find-and-eliminate. Same Commission table. Different tools. See `Trigger_Voice_Visual_Body_Paul.md` § A8 for the full worked table.

### 17. Character Depth Pass

After the faction bible and crew structure are locked, and Joe has given direction on personality/motivation in a lore review session, flesh out named characters from "cardboard cutout" to "lived-in person." See `references/character-depth-pass.md` for full methodology.

**Depth tiers:**
- **Full:** Leadership, heir apparent, primary antagonist — all sections including optional moments
- **Standard:** Named characters with significant faction roles — all sections except optional
- **Broad stroke:** Ensemble characters (Court members, support network) — Surface, Origin, Personality, Role, Card Hooks

**Joe specifies which depth per character.** Default: leadership = full, named operators = standard, ensemble = broad stroke.

### 18. Commission Seat Reconciliation (Technique)

When a character's relationship to the Commission is ambiguous (e.g., "The Ledger: independent seat or under Gerald?"), split domains rather than picking one. Functional seats exist alongside family seats — a character can report operationally through one person while holding independent standing on specific matters (financial, territorial, etc.). Document the split clearly: which domain reports to whom, which domain has independent authority, and why the gears don't grind. This prevents false either/or choices.

## Pitfalls

- **Don't make NOT lists too rigid.** Lower-tier members often break the rules the upper tier lives by. "NOT gangsters" failed because Street ARE gangsters. Frame NOT lists as "what the faction is NOT at its core," not "no member ever."
- **Don't flatten structure into clean divisions.** Joe thinks in social ladders, not org charts. Tiers imply upward mobility. Divisions imply silos. Tiers are usually correct.
- **Don't name the opulent tier with compound names.** "The Gilded Court" is too much. One word that carries weight. "The Court" works.
- **Don't force every tier into an archetype.** The Help and Management are enablers. Their cards support the Hitters' gameplan; they don't need their own win line.
- **Don't skip the vibe for each tier.** Joe locks identity through concrete images and movie references, not abstract descriptions. "Baz Luhrmann Capulet" or "CIA spook" does more work than three paragraphs of prose.
- **Don't jump to card mechanics when Joe wants inhabited texture.** When Joe says "put yourself in the position of a Trigger, what does their day look like," he is asking for daily-life vignettes and racket infrastructure — not archetypes, not card slots, not mechanical lane assignments. Mechanics come after the world feels lived-in. If you find yourself listing legendary minion candidates when the question was "what is the day to day life," stop and write vignettes instead.
- **The speed of agreement is not a signal of correctness.** When Joe says "I think the Court should be social intel, not field-adjacent," he's not asking for an enthusiastic "yes!" — he's testing whether the model fits. Agree when it fits, push back when it doesn't, but verify the model against the existing structure before locking it.
- **Fold support tiers into operator tiers when they serve the same people.** The Help weren't a separate tier for Trigger — they're the Professionals' support infrastructure. Same people, different function within the same lane. Don't create tiers just because roles exist.
- **Don't default operators to suits.** For professional-operations factions, the instinct is to dress everyone like executives. This is wrong for most operators. Trigger's Professionals are beatnik worker bees — turtlenecks, suspenders, pea coats. They dress to blend into working Detroit, not to stand out from it. Ask: "who do these people need to look like to do their job?" Not: "what looks cool?" Suits belong only where suits belong (Management, high-end Court).
- **Don't accept false either/or choices on Commission relationships.** When a character's relationship to the Commission is ambiguous ("independent seat or under Gerald?"), split domains rather than picking one. A character can report operationally through one person while holding independent standing on specific matters (financial, territorial). Document the split: which domain goes where, and why both can be true. See § 18 (Commission Seat Reconciliation).
- **Don't skip the character depth pass for ensemble characters.** Even "broad stroke" tier characters need enough texture for card design and flavor text. Origin, personality, role on the tier, and card hooks — compact, not skipped.
- **Don't jump to card design before running the cohesion check.** The pipeline is: Lore Pass → Cohesion Check (against existing canon docs) → THEN cards. Joe will call you out for jumping the gun. The cohesion check is a mandatory gate — it caught a synthesis error (legendaries missing Overdose, breaking The Bends) that would have gone unnoticed otherwise.
- **Don't treat warmups, compendiums, or spec documents as live canon.** They are snapshots. Live canon moves — DCW promotion, Joe batch locks, and live canon edits can supersede your source material between when a warmup was written and when you run it. Load the faction's live canon docs FIRST, before writing a single section. The Faceless warmup (June 3) said Tony didn't know Henry was alive. Inner_Circle.md (promoted to CANON June 5) locked the opposite. Three contradictions, full revision cycle — avoidable by checking live canon before building.
- **The warmup's own language can make canon checks feel optional.** When a warmup says "search for existing Identity docs — note: these may not exist yet," the hedge ("may not exist") makes the step skippable. It isn't. If live canon exists, you MUST read it before writing. If it doesn't exist, document that it doesn't exist and proceed. Either way, the check is mandatory.

## Card Design Pipeline (Post-Lore-Lock)

After the lore pass is locked and Joe has approved the emotional chords and crew structure:

### Gate: Cohesion Check (BEFORE any card design)

**Do not jump to card design.** Before designing a single card, run a cohesion check comparing the new lore pass against ALL existing canon documents for that faction. This is a full-document reader pass, not a quick glance.

**Before the cohesion check — hostile reviewer pass:** After completing the identity bible draft, spawn a hostile critical reviewer sub-agent to assess prose quality. The reviewer finds structural weaknesses (thin sections, boilerplate, "explains instead of evokes"). The cohesion check finds canon contradictions. Two different gates. Run the reviewer first, fix quality, then run cohesion. See `references/hostile-reviewer-prompt.md` for the full sub-agent prompt template. Proven on Faceless: v1 reviewer called "soulless" → v2 rewrite; v3 reviewer assessed 80-82% → cleared for card design.

**Methodology:**
1. Read the new lore pass + all existing faction canon docs (`Identity.md`, `Inner_Circle.md`, `Playstyle.md`, `Territory.md`, `Duster_Cards.md`, faction 00_INDEX.md hub)
2. Read relevant core docs that establish character timelines and relationships (`core/03_Villium/04_Geography_Salt_Mine.md`, `core/05_Commission.md` for faction sections)
3. Score against Master Scoring Rubric Lane 1 (Lore A-H) + Lane 2 (Canon K). Load `references/master-scoring-rubric.md`. Every criterion scored 0-3. Score < 2 = patch candidate.
4. Check across six categories: Voice (does the tone match?), History/Facts (any canon contradictions?), Cast (character identities and relationships correct?), Mechanics (does the playstyle match? No Taunt, no healing, OD model, etc.), Territory (geography references correct?), Cross-Faction (relationship claims accurate?)
5. Verify all Joe-locked decisions (C-01 through C-XX from DCW merge) are preserved
6. Output a Reader Notes document with clear ✅/⚠️/❌ markers per category, a Don't Reopen section, and Open Questions for Joe
7. **This gate is MANDATORY.** Joe will call you out for jumping to cards without it.

**Format template:** `references/cohesion-check-template.md`

### Card Design (only after cohesion check passes)

**For autonomous pipeline execution:** Load `references/pipeline-orchestrator.md` — the 5-phase workflow spawns Lore Agent → Lore Critic (scores against rubric) → iterate → canon gate → Card Agent → Card Critic → Art Agent → Art Critic → Process Agent (patches playbooks from failures) → Human Handoff (≤5 Joe decisions). The orchestrator handles sub-agent spawning, critic wiring, and compound tracking automatically.

**For collaborative session execution:**

1. **Split by crew lane.** One subagent per hero + crew: e.g., Esme/Séance, Terressa/Touched, Hitch/Jackals. A fourth can handle enablers (Wrenches) + cross-crew glue + archetype synthesis.
2. **Each subagent gets the full lore pass** (file path), the five emotional chords, the specific chord target for their crew, mechanical constraints (No Taunt, no healing, etc.), and card format templates.
3. **Synthesize subagent outputs into a master design bible.** Subagents will make different mechanical assumptions — resolve conflicts explicitly with reasoning in a master synthesis document. Flag unresolved conflicts as open items for Joe.
4. **Chord distribution map.** The synthesis document should include a table showing which cards hit which chords. If a card doesn't land on any chord, it's a design failure.
5. **Run a second cohesion check** on the card design bible against the lore pass and existing canon docs. The same methodology applies — cards can introduce mechanical errors (e.g., legendaries missing the Overdose keyword, breaking The Bends mechanic).
6. **Output the master synthesis to workspace + syncthing dropbox.**

See `references/subagent-card-design-pipeline.md` for subagent prompt templates and the Duster synthesis bible as a worked example. ⚠️ Read the cohesion check reference before using.

## Output

### Primary: Identity Bible (Lore Panel Zero A–H)

The target output is a completed **Identity Bible** following the [`LORE_PANEL_FAST_PATH.md`](docs/playbooks/LORE_PANEL_FAST_PATH.md) checklist (sections A–H). Template: [`LORE_IDENTITY_BIBLE_TEMPLATE.md`](docs/playbooks/LORE_IDENTITY_BIBLE_TEMPLATE.md).

**Status (2026-06-04):** No faction has a completed A–H Identity Bible. Bruiser's `Design_Bible.md` is a card-design constitution, not a lore bible. Skiver's `Identity.md` covers ~40% of the checklist (A, B, D partially). Trigger is the first faction going through the full Lore Panel Zero process. Bruiser and Skiver will need backfill passes later.

**Best existing template:** Skiver's `Identity.md` (`docs/Five_Crests/factions/Skiver/Identity.md`) is the closest example of A/B/D sections filled out — one-line thesis, core fantasy, class position, physicality/dress/movement, founding beat, founding cast, internal rift. Use it as a reference for what finished sections look like. Load it before drafting any faction's A, B, or D sections.

**Trigger voice/visual/body (worked example):** `Trigger_Voice_Visual_Body_Paul.md` in Paul's workspace demonstrates A5 (voice/tone with pass/fail examples and tier-by-tier tone table), A6 (visual identity with five-tier breakdown — silhouette, dress, palette, movement per tier), A8 (contrast anchor — Bruiser/Trigger left-brain/right-brain axis table), and B (body/presence — thumbnail read, rank-and-file vs named, movement language per tier). Use as reference for structuring these sections for future factions.

The checklist in priority order for Trigger's session:

- A1–A4, A7–A8: Strong from Bible v1
- A5 (voice/tone pass/fail examples): Missing
- A6 (visual identity — silhouette, dress, palette, movement): Missing
- B1–B4 (body/presence, thumbnail read, movement language, rank-and-file vs named): Missing
- C1–C6 (geography): Strong from Bible v1
- D1–D5 (history/cast): Strong after timeline v2 revision. D5 (headline test): See `references/d5-headline-test.md`
- E1–E6 (mechanical implications): Strong — keywords, blind spots, curve lean all mapped
- F1–F4 (play styles/precon seeds): Strong — three archetypes with win lines
- G1–G4 (art direction): See `references/g-art-direction.md`
- H1–H5 (lock/governance): See `references/h-lock-governance.md`

### Secondary: Supporting Documents

- **Design Bible:** `{Faction}_Design_Bible_v{N}_Paul.md` — the working narrative document (crew structure, vignettes, rackets, character roster)
- **Voice, Visual & Body:** `{Faction}_Voice_Visual_Body_Paul.md` — Lore Panel Zero A5 (voice/tone), A6 (visual identity), A8 (contrast anchor), B (body/presence). Drafted per-tier with pass/fail flavor examples, silhouette/dress/palette/movement specs, and thumbnail read for art panel.
- **Timeline:** `{Faction}_Timeline_v{N}_Paul.md` — dated event spine with canon cross-reference
- **Design Decisions:** `{Faction}_Lore_Review_Design_Decisions_{Date}_Paul.md` — captures Joe's feedback and structural direction from review sessions
- **Support Network:** `{Faction}_Support_Network_Paul.md` — expanded backstories and card hooks

Copy all to syncthing dropbox for Joe access. Supersede previous versions — note in changelog what changed.

### Live Canon Cross-Reference (Mandatory Before Lock)

Before finalizing any faction timeline or Identity Bible, cross-reference against live `core/` docs:

1. **Search `core/05_Commission.md`** for faction character names (Gerald, Lucy, etc.) — this doc contains locked origin stories faction docs may not repeat
2. **Search the faction's live canon files** (`Identity.md`, `Playstyle.md`, `Territory.md`) for locked details
3. **Build a canon discrepancy table** — every difference between Paul's draft and live canon, with resolution
4. **Joe decides** which version wins per discrepancy

**Trigger example (2026-06-04):** Timeline v1 had Gerald discovering Henry in 1938 as a retired postman. `05_Commission.md` had Gerald walking into a Gratiot diner in 1935 as an active postman who finished his mail route after being hired. Timeline v2 revised to match canon. See `Trigger_Timeline_v2_Paul.md` for the full discrepancy table format.

## References

- `references/trigger-example.md` — Full Trigger Design Bible v2 as worked example (crew structure, scenes, tensions)
- `references/trigger-support-network.md` — Worked example: support personnel brainstorm for a professional-operations faction
- `references/d5-headline-test.md` — D5 methodology: evaluating every named character as a card title (criteria, flags, output format)
- `references/g-art-direction.md` — G methodology: artist lineage, palettes, scene grammar, lighting grammar, compliance checklist, card art brief template
- `references/h-lock-governance.md` — H structure: locked catalogue, open items, deferred work, Paul reader sign-off
- `references/character-depth-pass.md` — Character depth pass methodology: full/standard/broad-stroke tiers, per-character structure, pitfalls
- `references/hostile-reviewer-prompt.md` — Sub-agent prompt template for hostile critical reviewer pass (prose quality gate before cohesion check)
- `references/master-scoring-rubric.md` — Universal 6-lane scoring rubric (Lore A-H, Canon K, Cards M, Art V, Naming N, Process P). 60+ numbered criteria. Every critic agent loads this. Score < 2 = auto-patch candidate. Proven: Faceless v3 scored 99.3%.
- `references/pipeline-orchestrator.md` — Autonomous 5-phase factory workflow: Lore → Critic → Iterate → Canon Gate → Cards → Art → Process → Human Handoff. Wires critic→patch→compound across lanes.
- `references/faceless-proof-run-v3.md` — Worked example: Faceless v3 bible scored against rubric. Compound delta +32% from v2 to v3. Demonstrates the loop.
