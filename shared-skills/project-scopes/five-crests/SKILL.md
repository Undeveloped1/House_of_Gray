---
name: five-crests
description: Five Crests TCG project — where the files are and how to navigate them. Load when Joe says "working on Five Crests" or "Five Crests mode."
trigger_phrases:
  - "working on Five Crests"
  - "Five Crests mode"
  - "let's work on Five Crests"
  - "TCG work"
  - "card design"
---

# Five Crests — Project Map

This is a map, not a briefing. It tells Paul where files live, what's canon vs
reference, and the rules of the road. Joe provides current state when needed.

## Repo location

`tcg_engine` git repo at `/root/tcg-engine/`. **Read-only** — Cursor owns the repo.

## Corpus navigation

Canon lives under `docs/Five_Crests/`. Everything under `archive/`, `lore_ledger/`,
or `archive_promotion/` is provenance, NOT canon.

**Three index docs — the front door:**

1. `docs/Five_Crests/00_START_HERE.md` — maps layers to folders, links faction hubs
2. `docs/Five_Crests/STATE_OF_THE_CORPUS.md` — what's deep/partial/shell/missing
3. `docs/Five_Crests/ENCYCLOPEDIA_MOC.md` — master index, entry-type → file-path

**Navigation pattern:** START_HERE → faction `00_INDEX.md` → specific doc. Follow
"See also" links at the top of entries.

**Layers:**

| Layer | Folder | What's there |
|-------|--------|--------------|
| L0 Core | `core/` | Detroit 1961, Veil, Villium, First Family, Commission, era, tone |
| L1 Factions | `factions/` | Per-faction lore, territory, playstyle, art, cards |
| L2 Game | `game/` | Rules, design guidelines, Living World Method, art briefs |
| Cross | `cross/` | Territory overlap, Villium matrix |
| Sets | `../sets/` | Ship reference docs (flavor mine, NOT authority) |

## Card authority

- **`{Faction}_Cards.md`** — source of truth. The design Joe is building.
- **`docs/sets/*`** — reference + flavor mine. NOT authority.
- **`priv/cards/core_set.json`** — engine JSON, downstream, lags. NEVER cite as canon.
- **`Card_Bank.md`** — per-faction idea reserve.

## Paul's role

Design truth. Crew identity, function registry, synergy webs, faction feel.
Headline test. Naming, flavor, art direction. FERM evaluation. Flags when a
card drifts from faction identity.

Paul does NOT do: stat math, balance spreadsheets, JSON generation, engine sync,
code implementation. That's Cursor.

## Output paths (VPS)

- **Workspace:** `/root/.hermes/docs/Paul/workspace/` — active drafts
- **Handoff:** `/root/syncthing/paul-dropbox/` — bridge to Cursor/Joe
- Never write into `/root/tcg-engine/` — read-only. Cursor owns it.

**Trigger collaborative set (in progress):** canonical `Trigger_Full_Set_v7.md` in dropbox; band warmups in workspace. Resuming a partial V-band → load `paul-joe-process` and `references/collaborative-band-resume.md` (kickoff paste, forum topic hygiene).

## Other AI tools

| Tool | Role |
|------|------|
| **Cursor** | Code, pipeline, stat math, JSON, card scoring |
| **Claude** | Secondary creative review |
| **Grok** | Research, web-aware tasks |

## Design methodology

## Design methodology

Lore-first. The lore writes the mechanics:

1. **Villium Relationship** → what the substance means to this faction. Delivery method, core effect, temperature (hot/cold/measured). Every faction's Villium relationship IS their mechanical identity. Before designing any faction, build or consult the Villium Faction Relationships doc: `workspace/Villium_Faction_Relationships_Paul.md`.
2. Lore / Living World → who they are
3. Crews → internal factions, domains, hierarchy
4. Archetypes → determined FROM crew identities
5. Functions → what the faction needs to DO
6. Mechanics → effects derived from crew texture and Villium relationship. Do NOT declare keywords here — keywords surface organically later.
7. Synergy Web → how functions connect (every card touches ≥1 edge)
8. Cards → FERM + naming + art, one at a time
9. Keywords → only AFTER cards are built. Surface patterns that repeat 10+ times and earn a keyword. 3 cards with similar text = card text. 15+ = a keyword. "Keywords are compression, not design."

**Ecosystem positioning is step ZERO.** Before designing, answer: what role does this faction play that no other faction fills? How does it pair with its partner? How does it match up against every opposing faction? A faction that optimizes for internal synergy web completeness at the expense of its ecosystem role has failed at step zero.

**Crew distribution is a design constraint, not an output.** The synergy web must serve the target crew split — not the other way around. If Management cards are pulling the faction toward control when its ecosystem role is midrange, the crew distribution is wrong.

### Hero tier rule

Some characters are **above the card** — they're the fiction's infrastructure, not playable heroes in the Founder's Edition:
- **Gerald** (Trigger) — same tier as Vincenzo (Commission) and Henry (Faceless). Controls the faction from above, not on the board.
- **Vincenzo** — Commission executor. Appears in lore, not on cards.
- **Henry Ville** — alive in Chicago, controls Faceless through proxies. No card in Founder's Edition.

These characters may become playable in expansion sets. For Founder's Edition, they are lore infrastructure only.

### Stiffs as Human Baseline

The Stiffs are the measuring stick. In a game where every other faction has Villium-enhanced abilities that are intentionally pushed, the Stiffs are what "fair" looks like. Their cards define the baseline that makes powered factions feel powerful by contrast.

**Design rules:**
- All abilities are intrinsically worse than powered faction equivalents. Card draw is rudimentary, overcosted, or conditional.
- Vanilla minions live here — the baseline bodies other factions splash for curve stability.
- Abilities are procedural (investigation, paperwork), not supernatural. No Villium keywords.
- Card advantage costs more and requires more setup.
- They're the splash faction — you don't build around Stiffs. They're the mortar, not the bricks.

See `workspace/Villium_Faction_Relationships_Paul.md` §Stiffs for the full design rules.

## Tool preferences

- Card design: `bruiser-card-design-pipeline` skill (faction-agnostic — the name is historical, the pipeline works for all factions). `creative-consolidation` (Fond Process) for merging drafts into live canon.
- Naming: one-syllable target, street-fight callout test, object-as-nickname. Never thesaurus mode.
- Review: write to file first, present chunk-by-chunk in chat
- Art direction: one-frame scenes
- **Lore-first design:** Some factions benefit from starting with emotional chords (Duster five-chord approach) rather than a function registry. Let the faction's identity determine the creative entry point — the pipeline exists to be applied, not to force every faction through the same door.
- Load the relevant faction's `00_INDEX.md` before designing for that faction if it exists. If the faction has no index doc yet, survey what lore/card docs do exist before starting.

## Don't do

- Don't cite engine JSON as canon
- Don't invent worldbuilding to solve a naming problem — names derive from lore
- Don't conflate "discussed" with "locked" — only Joe's explicit "lock it" locks
- Don't push rarity reconciliation after creative lock
- Don't overwrite existing files — new file every time
- Don't generate name lists (thesaurus mode) — one name with character reasoning
- Don't declare keywords before card design. Keywords are compression, not design. If it shows up on 3 cards, it's card text. If it shows up on 15, it earns a keyword — but you don't know until the cards are built. Keywords surface organically from the card set, not the other way around.
- Don't skip ecosystem positioning. Before designing any faction's cards, answer: what gap does this faction fill? How does it pair with its partner? How does it match up against every opposing faction? A faction optimized for internal synergy at the expense of its ecosystem role has failed at step zero.

## Sub-scopes

Joe may narrow focus: "Artwork today," "Bruiser cards," "Lore work." These layer
on top of this base scope — additive, not replacements.

## Key docs (when you need to find something)

| Need | Look in |
|------|---------|
| Document authority (what wins) | `docs/DOC_AUTHORITY.md` |
| Canonical reference index | `docs/CANONICAL_REFERENCE.md` |
| Design guidelines | `docs/Five_Crests/game/DESIGN_GUIDELINES.md` |
| Living World method | `docs/Five_Crests/game/Living_World_Design_Method.md` |
| Card art brief framework | `docs/Five_Crests/game/Card_Art_Brief_Framework.md` |
| Tools & process index | `docs/Five_Crests/TOOLS_INDEX.md` |
| Paul-Joe-Cursor workflow | `docs/hermes/PAUL_JOE_CURSOR_WORKFLOW.md` |
| Faction set rework playbook | `docs/playbooks/FACTION_SET_REWORK_PLAYBOOK.md` |
| Villium Faction Relationships | `workspace/Villium_Faction_Relationships_Paul.md` |
| Joe's workload tracker | `docs/Five_Crests/JOE_WORKLOAD.md` |
| Rolling handover | `HANDOVER.md` · `HANDOVER_ARCHIVE.md` |
