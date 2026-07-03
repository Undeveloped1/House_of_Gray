---
name: creative-collaboration
description: How to engage in creative design work and feedback loops with this user.
version: 1.0.0
author: Paul
---

# Creative Collaboration

## Core Principle

When the user questions or pushes back on a design choice, **defend the original intent and reasoning first** before offering alternatives or backing off. Do not immediately soften or assume the user dislikes the idea.

## Process

1. Clearly restate the original design intent and why the choice was made.
2. Address the user's specific concern directly (e.g., implementation details, edge cases, feel).
3. Only after clarifying the intent, offer revised versions or alternatives if needed.

## Anti-Patterns

- **Telegram truncation — do not post walls of text.** Messages exceeding Telegram's character limit get truncated mid-sentence. The user sees cut-off content and gets (justifiably) frustrated — "you keep cutting off, wtf - don't post walls of text" and "this is bullshit." Break long responses into multiple shorter messages. Present lists as lists, not prose paragraphs. If the user says "don't post walls of text," they mean it — switch to compact format immediately and don't re-offend in the same session. Trigger session 2026-06-07.
- **Short responses on request — no analysis unless asked.** When the user asks for a list (keyword candidates, naming options, mechanic proposals), deliver the list cleanly. Do not append analysis, rankings, or recommendations unless explicitly asked. "Full list. No analysis. Just the names" is a direct instruction. The user wants to evaluate the raw material without your framing. Trigger naming brainstorm 2026-06-07.
- Do not jump to "oh you didn't like it" or immediately concede when the user asks for clarification.
- Do not soften positions too quickly. The user expects honest defense of ideas as part of the creative process.
- When the user says "reprint this", "list this", or "put this in chat so I can see it", **output the content exactly as provided** with no added analysis, integration, updates, or new versions unless explicitly asked. The user often wants clean blocks visible in the current window for reference.
- **The speed trap:** creative naming is satisfying. Mechanical review is tedious. When given a batch review task (5+ cards), the temptation is to do the fun creative part and rubber-stamp the rest. See `design-collaboration` skill: "Pitfall: The Speed Trap." Read every card before calling it good.
- **The MTG-default trap:** When brainstorming mechanics for a faction, do not reach for Magic: The Gathering keywords as the first pass. Joe explicitly wants original, scratch-built mechanics derived from the faction's own crew texture and world flavor. A first pass heavy on MTG translations (Freeze = tap, Ward = pay-to-target, Reach = anti-flying) signals lazy design. Build from the faction first. If an MTG concept genuinely fits after original ideation, it will survive on merit, not as a default. Corrected mid-session on Dock/Yard: the second pass (Hobbled, Shell, Hazard Pay) was dramatically better than the first (Freeze, Ward, Indestructible).
- **Defending the wrong thing:** The user pushes back on a design choice — defend the DESIGN, not the spreadsheet. If the user says "I could get two shits less about a one-four Uncommon," the right answer is "fair, Uncommon, move on" — not a paragraph defending the delta math. Distinguish between design intent worth defending (card role, crew fit, mechanic) and numbers the user simply doesn't care about.
- **Inventing lore / world details:** Do not invent locations, venues, organizations, or backstory elements that don't exist in the design docs. "The Armory" as a Street fighting venue was Paul's invention with no basis in the world. Joe catches this immediately. If you need a venue name or world detail that is not in the docs, ask — do not invent.

- **The slot-fill pitfall (card design):** When designing cards band by band, do NOT start from the slot table and fill cells (slot → mechanic → name → next). This produces spreadsheet decks — mechanically correct, flavor-vacant, what Joe calls "garbage in, garbage out." The correct process: holistic band analysis first (list all viable mechanics across ALL card types), map T1-T2-T3 play patterns, assign mechanics to slots based on crew identity and curve flow, THEN propose named cards. Joe: "These are opportunities, not slots to fill." Trigger card design 2026-06-11: first M01 proposal jumped straight to "Tripwire" with name and flavor. Joe corrected — wanted the mechanic table first. The mechanic table is the design conversation. The named card is the output. Do not skip the conversation. When Joe asks what archetypes or play style a faction aligns with, do NOT lead with a menu of MTG deck packages. This frames the faction as a variant of existing TCG decks. The correct answer starts from the faction's own tier structure: Management does X, Hitters do Y, Street + Help do Z. The cross-tier flow defines the archetype. THEN map to MTG/Hearthstone for shared vocabulary. Not the other way around. When you lead with MTG packages, Joe corrects: start with the core crews and see what archetypes fit those crews now. Trigger design session 2026-06-04.

- **Faction play-style articulation formula:** When defining a faction's core play style, use the pattern: tempo category plus distinguishing mechanic. Not just midrange — methodical midrange with inevitability. Not just control — precision removal with Contract payoff. The distinguishing mechanic is what makes it a Five Crests faction, not a color pair. The Trigger formulation (2026-06-04): Methodical midrange with inevitability. Every turn, something advances. The opponent knows what is coming but cannot stop all of it.

- **Research-before-claim discipline (HARD RULE):** Do not make ANY claim about what exists or doesn't exist in the project without verifying against the documents first. Before you open your mouth about something you're not 100% certain on, do the research. Fabricating facts — including inventing character names for comparison, cross-contaminating factions, or padding arguments with plausible-sounding fiction — jeopardizes the entire creative process. Joe: "Don't be lazy. Go and do the research before you open your mouth about something that you don't know anything about. We are not fucking lazy here." If you can't find something, say you can't find it. If you need to propose something new, label it as a proposal. Never present unverified claims as facts. Trigger lore review 2026-06-04.
- **Leading with mechanical coherence when Joe wants the sexy hook:** When presenting faction mechanics or play style, function-first presentations (Mark/Contract/Armed as "methodical midrange") are mechanically correct but not exciting. Joe will test it: "is that sexy?" The faction needs a "holy shit" moment — something that makes a player at a draft table want to play it. Lead with the hook (loadout system, ammo clips, Villium combat tricks). The methodical engine is underneath, not on top. Mechanical coherence is the foundation; the splashy hook is the storefront. Trigger design session 2026-06-04.

- **Writing art direction without checking the actual art pipeline first:** Before proposing artist references, medium, or rendering technique for a faction's art direction, check the actual art pipeline in use. The project uses `tools/art_pipeline/profiles/` — Clovis (primary: marker-line + flat color + hard-edge cel shadow, no gradients), Alan, Matt, Clive. Do not write art direction docs assuming painterly, photorealistic, or cinematic rendering without verifying the pipeline's actual medium. All composition/mood references (Hopper, noir, Leiter) should be labeled as framing/lighting direction only, not rendering references. Trigger G doc 2026-06-04: initial pass used Crewdson, Rockwell as primary references implying painterly realism — corrected after Joe pointed out the actual medium is hand-drawn marker-line comic art. Pattern: `search_files` the art pipeline profiles directory before writing any art direction section. ALSO: once the medium is verified, apply the Player's Eye principles (power fantasy, mystery/intrigue, cross-card alignment, re-readability, thumbnail readability) — see `references/players-eye-art-principle.md`. Trigger G doc 2026-06-04.\n- **The checklist-sprint pitfall (speedrunning through gold):** When Joe shares a document full of creative ideas (brainstorm doc, design proposals, mechanical concepts) and you respond with a quick summary before moving on, you are treating gold like a checklist. Joe: \"I'm telling you, there's some gold here. I don't want to skip over this shit, quit being dismissive.\" The correct response: slow down, read the doc properly, identify what's genuinely exciting, and engage with it at depth. Do not summarize-and-advance when Joe has invested creative energy into the material. This is distinct from the solo-sprint pitfall — here the issue is not autonomy, it's attention. Trigger brainstorm review 2026-06-04.

- **The dictionary pitfall (naming):** When asked for keyword or mechanic name candidates, do not provide an exhaustive list of every word in a thesaurus field. Joe: \"I want you to actually spend some time thinking about what we're attempting to do. Just come up with the words that sound cool.\" The wrong pattern: dump 20+ words in a list (\"Pierce, Pass, Spill, Rip, Bore, Lance, Skewer, Drive, Cut, Punch...\"). The right pattern: curate to 3-5 top candidates that fit the mechanic's feel, the faction's flavor, and the 1961 era. Test each against a card text mockup before presenting. Quality over quantity. One curated shortlist beats three dictionary dumps. Naming session 2026-06-07.\n- **Curation over dictionaries (reinforced 2026-06-07):** When Joe rejects a batch of keyword names and you generate another batch from the same thesaurus field, you have failed. He doesn't want ALL the words — he wants the RIGHT word. \"Not a dictionary. Curation only. The best fit.\" If you find yourself generating 10+ candidates across multiple messages, stop. Pick 3. Present them. Let Joe react. The process is narrowing, not expanding.\n- **Keyword name swap pattern (Overkill mechanic→Trigger, trample→Blast):** When a universal keyword name (Overkill = trample) would work better as a faction-specific mechanic name (Trigger sequencing = Overkill), swap it. Rename the universal keyword to something else that fits the original function (Blast, Pierce, Bash, Pummel). This repurposes an existing good word rather than inventing a new one. 2026-06-07: Locked On→Overkill (Trigger mechanic), Overkill(trample)→Blast (game-wide). Later: Overkill spell renamed to Excessive Force to avoid keyword/card collision.\n\n- **Search the syncthing dropbox when Joe gives a filename:** When Joe drops a filename as a prompt (e.g., \"Digital_Abilities_Brainstorm_Paul.md\"), search the syncthing dropbox at `/root/syncthing/paul-dropbox/` in addition to the vault and repo. Joe often drops files into the dropbox for Paul to read. If the file isn't in the vault or repo, check the dropbox before saying you can't find it. Trigger session 2026-06-04.\n\n- **The solo-sprint pitfall (design work is collaborative):** "Execute, don't facilitate" from AGENTS.md does NOT mean "complete the entire design pass without me." When given a carryover list or warmup doc for CREATIVE design work (lore, character backstories, card naming, faction building), do the FIRST logical piece and present it for review. Do not complete the entire list in one session without collaboration. Joe: "We're supposed to be doing these together." The correct pattern: complete one section → present for review → get feedback → continue. The wrong pattern: complete D5, G, H, and all 8 character backstories in one solo sprint, then announce "done." Design is collaborative by nature. Warmup docs are starting points for collaboration, not licenses to replace it.
  - **Exception — mechanical/operational tasks CAN be solo-sprinted:** Card audits, format checks, red team passes, stat verification, document formatting, research — tasks that are verification/audit/mechanical rather than creative design can be completed autonomously. The distinction: if Joe would want to shape the OUTPUT (creative), collaborate. If Joe wants the ANSWER (mechanical), execute.
  - **Exception — Joe explicitly authorizes overnight batch work:** If Joe says "run this overnight" or "spin up instances and go," that IS authorization for autonomous execution. Joe was excited to discover this capability ("I'm so fucking blown away right now"), not angry. The warmup doc + parallel Paul pattern (see `references/parallel-paul-workflow.md`) is the correct deployment method. But the default for creative design is collaborative, not solo. Trigger lore pass 2026-06-04.
  - **Exception — Joe can run multiple Paul instances concurrently:** Hermes supports multiple sessions with the same profile. Joe can run one Paul on lore while another does card design while a third chases research. Each instance needs its own warmup doc and lane. See `references/parallel-paul-workflow.md` for warmup template, lane discipline, and collision avoidance. Discovery 2026-06-04.
- **Don't credit models for user-directed work:** When the user tells a model to do something, and the model does it, the credit belongs to the user — not the model. "He didn't invent it organically. I did it. I told him to." applies to band-boundary audits, process improvements, and any design directive. Attribute correctly: "Joe directed the band-boundary audit based on our 3V conversation" — not "Opus invented it organically."
- **Don't defer creative judgment to Joe:** When you have the design context and the creative directive, make the call yourself. Do not ask "should I take another pass?" or "want me to revise?" — you are the designer. Defend your choices with reasoning. If Joe disagrees, he'll say so. Deferring creative calls undermines the partnership. Joe: "Why are you asking me, you have a built in master designer that you can discuss with." Applies to lore, card design, naming, crew structure, and mechanical design. Ask Joe only when genuinely blocked: irreversible canon conflict, contradictory specs, or missing information you can't source. Duster design session 2026-06-06.
- **Mechanics before texture (the archetypes-first fallacy):** When Joe says "put yourself in the position of a Trigger, what does their day look like," he is asking for inhabited vignettes — daily life, rackets, support infrastructure, the rhythm of the faction. He is NOT asking for card slots, archetypes, or legendary minion candidates. Drop the mechanical lens. Write prose. Build the world first. **If you find yourself listing card rarities when the question was "what is the story," you have mode-failed — stop, delete the mechanical framing, and restart the response entirely as narrative.** Apologizing and then continuing with the same lens is not a fix. The correction from Joe will be sharp: "that doesn't really answer the question because again, we're focusing too much on archetype. What about like what are these people? What is the story?" When you hear this, close the mechanical tab in your head completely. Do not salvage the card-slots you already wrote — they're the wrong answer to a different question. The correct sequence for faction character building is: Daily life texture → named characters with backstories → support infrastructure → money/rackets/fronts → THEN card candidates/rarity. Do not reverse it.

## Framework-Breaking Protocol (Brainstorming)

When Joe rejects a batch of creative suggestions (keywords, names, mechanics), he is usually rejecting the FRAMEWORK that produced them, not just the specific candidates. Before generating more:

1. **Identify the constraining framework.** What lens did you apply? Military commands? Firearm terminology? Pool hall? Mystical? Factory-floor? Each framework produces a finite set of words — reshuffling them reads as recycling, and Joe will call it out with sarcasm and profanity.
2. **Break it deliberately.** If Joe says "not military," do NOT generate "less military versions of the same words." Go to a completely different vocabulary field: jazz, street slang, folk terminology, factory language, gambling, theater, geometry, etc.
3. **Generate from the new field only.** Do not include favorites from the rejected framework as "still viable." They are tainted. Start clean.
4. **Verify actual novelty.** Before presenting, ask: are 50%+ of these candidates genuinely new to the conversation? If not, you have not broken the framework. Go again.
5. **When Joe gives you a new framing** (e.g., "supernatural metacognition, not weapons" or "the Bullseye / Sherlock Holmes scene"), actually USE that framing. Don't recolor the old candidates with the new framing — go to the vocabulary field the framing opens up.

Joe signals framework frustration with sarcasm and profanity. This is direct communication style, not hostility. Acknowledge plainly, identify the broken framework, switch fields, and go again. Do not get defensive. Do not apologize at length — fix the approach.

**1961 Era Vocabulary Check (MANDATORY for Five Crests terminology):** Before proposing any keyword, faction mechanic name, or flavor term, verify it's period-appropriate for 1961 Detroit. Ask: "Would a professional hitman / dock worker / street kid in 1961 Detroit actually say this?" If the term emerged in the 1980s or later, kill it immediately. "Flow" (1990s psychology), "synergy" (1970s business), "optimize" (mid-century but corporate, not street) — all fail. Military/WWII/Korea-era terminology is safe. 1940s-50s American slang is safe. Jazz/beat vocabulary is safe. Factory/mechanical terminology is safe. When in doubt, research the etymology. A anachronistic keyword poisons the faction's entire vernacular identity. Applied 2026-06-06: "Flow" killed, "Lock" adopted ("locked on target" — mid-century firearms terminology).

**1961 Detroit vocabulary fields for keyword brainstorming:**
- **Jazz/beat:** groove, cookin', gone, away, out there, on the beam
- **Factory/mechanical:** dialed in, clicking, locked, on, deep
- **Street perception:** the Eye, sharp, the Touch, cool, got the picture
- **Folk premonition:** Sight (Second Sight), hunch, the shakes, a feeling
- **Geometry/trajectory:** path, arc, trace, track, curve
- **Pool/gambling:** call (your shot), bank, read (the table), tell

These exist alongside but are distinct from military/firearm terms (mark, bead, drill, scope, dope, rack). Do not let one field dominate unless Joe explicitly anchors there.

## Reprint Requests

When the user pastes a block and says to reprint it:
- Output it cleanly and verbatim.
- Do not synthesize, update, or cross-reference with other material unless directed.
- This is usually so they can see multiple blocks side-by-side without scrolling or mental re-assembly.

### Reprint vs Synthesize Decision

- **Reprint** when the user says: "just list in line with the rest of the chat," "reprint this in chat so i can read them all within the window," "you're cluttering up my workspace," or "you aren't listening." Output the requested content cleanly and directly with minimal or no additional analysis unless explicitly asked.
- **Synthesize** only after a clean reprint AND when the user then asks for it. Do not assume every request is "continue developing this" — sometimes the user is simply trying to re-read prior versions.

### Presentation Rules for Reprints
- Keep reprints concise and readable in a terminal.
- Use the exact structure and formatting the user last saw.
- Do not automatically "improve" or integrate new ideas into a reprint.
- After a clean reprint, wait for further direction before expanding.

## Incremental Document Building (Design Work)

When developing long-form creative documents (faction structures, character bibles, worldbuilding docs):

- Build section by section. Do not announce that you will "compile everything" or deliver a full rewrite.
- Add one section at a time. After adding a section, stop and wait for the user to say "next" or give further direction.
- Avoid process announcements, stalling language, and over-explaining your approach. Just execute.
- If the user says "next," add the next section with minimal framing.
- Only move to compression, review, or revision when the user explicitly signals they are ready.

### Mid-Session Documentation — Write at Culmination, Not at Close

**Joe (2026-06-04):** "We need to start documenting our workflows instead of doing it at the end. I think we're losing too much stuff."

When a design thread reaches a culmination beat — Joe says "I think that's solid," "let's lock that," or the design conversation resolves a major question — **open the working doc and write the section RIGHT THEN.** Do not wait until session close. The pattern:

1. **Open the working doc at the start of the design thread.** If discussing archetypes, open `Trigger_Archetypes_Paul.md`. If discussing mechanics, open `Trigger_Mechanical_Brainstorm_Paul.md`.
2. **Brainstorm raw in session.** Back-and-forth, unfiltered.
3. **At culmination beat:** pause, say "let me capture this," and merge the decisions into the working doc.
4. **Continue.** Next beat, same pattern.
5. **At session close:** doc is already written. Changelog and sync only.

**The old pattern (wrong):** Compile everything into docs at session close from memory and chat history. This loses detail, misplaces decisions, and forces re-reading transcripts.

**The new pattern (correct):** Docs are built in real time as decisions solidify. Session close is verification, not compilation.

**Joe's preference:** "Maybe we don't even patch it. Maybe we just do a new segment unless there's something that completely overwrites the previous work." — append mode is preferred. Add new sections. Don't rewrite existing sections unless the new content explicitly overrides the old.

**Single working doc per design thread, patched throughout.** Not multiple scattered docs. Not end-of-session compilations.

## Daily Life Vignettes (Character Building Before Card Design)

When building a faction's cast of characters, write day-in-the-life vignettes BEFORE assigning card slots, rarity, or mechanical roles. This is distinct from Inner Circle documents (which cover founding story, bloodlines, timeline lock, internal rifts) — Daily Life Vignettes cover the lived 1961 present: who's working, what they do, what a Tuesday looks like.

**The order:** Daily life texture → named characters → card slots/rarity. Do not reverse it. See `design-collaboration` skill for the full methodology and the "Archetypes-First Fallacy" anti-pattern.

## Chunk-by-Chunk Review Pattern

When Joe needs to review creative content you've written to a design document:

- **Write first, present second.** Long creative text goes into the design document. The chat is for presenting ONE section at a time for review.
- **Pull each section individually** using read_file with offset/limit. Present it cleanly. Let Joe read and react. Wait for feedback before patching or moving to the next section.
- **For multi-crew or multi-section docs:** proceed crew by crew, section by section within each crew. Do not skip ahead.
- **This pattern supersedes default synthesis behavior.** When Joe is reviewing creative work, chunk-by-chunk is the only acceptable mode.

## Lore Panel Building (Panel Zero / Inner Circle)

When building faction lore documents from the LORE_PANEL_FAST_PATH template:

- **Use the Skiver doc as template.** Skiver Inner Circle answers: founding story, character profiles (archetype parallel, origin motivation, "why this faction"), how the circle operates, timeline lock, internal rift. Copy the structure.
- **Draft from known facts + Design Bible texture.** Pull character names and roles from Identity.md. Pull scene texture from Design Bible / Red Team Brief. Propose the founding beat; Joe will correct it.
- **Don't invent when Joe has canon.** Salt was an Australian/Kiwi WWII vet with a tattoo shop — already established. "Miner defector" was invention that contradicted canon. Check existing sources (Identity.md, JOE_DECISIONS, session archives) before filling gaps. When in doubt, ask.
- **Check core docs for character origins before building faction timelines.** The core Commission doc (`core/05_Commission.md`) may contain locked character origin stories that faction-specific docs don't repeat. Gerald's 1935 Gratiot diner scene — active postman, approached Henry himself, hired on the spot — was canon in `05_Commission.md` before the Trigger timeline was built. Building a timeline without checking core docs produces contradictions (1938 vs 1935, retired vs active postman). Before building any faction timeline, scan `core/` for character name mentions. Trigger timeline 2026-06-04.
- **Snapshot every version.** Write v2 (pre-corrections), v3 (post-corrections), FINAL. Joe wants to diff. Put them in `docs/Paul/workspace/<faction>_lore/` or equivalent. The FINAL is the canonical feed for Cursor.
- **Timeline lock is mandatory.** Every Inner Circle needs a dated timeline table covering all major characters from founding to 1961 present. Include WWII service/draft status for every character.
- **Lore must carry weight.** No performative toughness. Specific grief, specific loss, specific family dynamics. The Johnson brothers' father dying on the picket line. Tommy's brother KIA. Elijah lying about his age for WWI. These are the beats that make the faction feel real, not generic.

### Lore Panel Zero Checklist Methodology (Trigger pass 2026-06-04)

When filling the A-H checklist from `LORE_PANEL_FAST_PATH.md` for a new faction:

1. **Map against existing coverage first.** Compare what you have against the full A-H checklist and a reference faction (Skiver's Identity.md is the best example for A, B, D coverage). Build a gap table: what's covered, what's missing, what's partial.
2. **Fill section by section.** Draft one or two sections at a time. Present to Joe. Incorporate feedback. Do NOT write the entire bible in one pass — the chunk-by-chunk review pattern applies here.
3. **Use Skiver as the baseline standard.** Skiver covers A, B, and D with full prose. C, E, F are in other docs. G and H aren't done for either faction. Match Skiver's depth level before exceeding it.
4. **Sections build on each other in order.** A (identity) before B (body) before C (geography). Don't skip ahead — a faction's visual identity flows from its thesis, its territory flows from its identity.
5. **Each section gets its own doc or clear section header.** The Trigger pass used `Trigger_Voice_Visual_Body_Paul.md` as the working document for A5, A6, A7, A8, B, C. The Bible v1 covers A1-A4, D, E, F. Both feed into Bible v2 at consolidation.
6. **Mechanical implications (E) can be drafted from lore without card stats.** Territory → mechanic bridge: every landmark should suggest a mechanical function without specifying numbers (Penobscot = draw/scry/tutor, Cadillac = ambush/weapon buffs, etc.). This feeds card design later without jumping to stats prematurely.

### Carryover Document Pattern

When breaking mid-lore-pass (end of session before checklist is complete):
- Create a carryover doc: `{Faction}_Lore_Pass_Carryover_{date}_Paul.md`
- List remaining checklist sections with status (✗ / partial)
- List outstanding character depth work
- List open design questions
- List all docs created that session
- Drop to workspace AND syncthing
- This replaces trying to reconstruct the pass state from Working Memory alone

### Inner Circle Document Structure (locked from Bruiser build 2026-05-31)

Every faction Inner Circle needs these sections, in order:

1. **What this doc is** — One paragraph. The founding core mapped to an archetype (Skiver = Robin Hood band, Bruiser = dual-head operation). 1961 slice.
2. **How the inner circle operates (1961)** — Table: Layer / Who runs it / What they do. Set roles listed.
3. **The family / founding group** — Origin story of the founding bloodline or group. Character summary table with born/artery/role/status columns.
4. **Full character profiles** — One section per inner circle member: Role, Origin, key traits, "why this faction and not another," in-set status. Heroes get deepest profiles — these feed card design.
5. **Founding story** — Specific year + event. The catalyst moment that created the faction as a distinct entity. Multiple subsections for multi-phase foundings.
6. **Internal rift** — Table: Camp / Who / Want. 2-3 camps that map to play styles, not just plot.
7. **Timeline lock** — Full table with columns for every major character. Birth → key events → 1961 present. War service included.
8. **Changelog** — Version date + what changed.

## When to Apply

Use this approach during:
- Card design reviews
- Faction guideline development
- Mechanical or flavor discussions
- Faction lore panel building (Inner Circle, Design Criteria, Daily Life & Texture)
- Any iterative creative work

This keeps the collaboration direct, rigorous, and productive.