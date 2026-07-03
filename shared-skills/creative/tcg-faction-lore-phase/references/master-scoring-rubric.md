# Master Scoring Rubric — 5Crests Pipeline
## v1.0 | 2026-06-07 | Paul Autonomous Build

**Purpose:** One document. Every critic agent loads this. Every lane (lore, cards, art, naming) has mechanical, numbered criteria. Critics cite criteria by number. Score < 2 = auto-patch candidate. No subjective language.

**Score definitions:** 0=absent, 1=wrong (canon violation), 2=correct/thin, 3=ship-ready.

**Source:** Built from Lore Panel Fast Path A-H checklist + Compendium Build Checklist + Faceless v2 Cohesion Check patterns. Proof-run against Faceless v3 bible: 140/141 (99.3%).

## Lane 1: Lore (A-H Identity Bible)
### A. Thesis and Identity
- A1: One-line thesis — quotable in one breath, traces to every section
- A2: Core motivation — why they fight, specific mechanism
- A3: Who they are — 4+ blocks (class, bond type, economy, daily life)
- A4: Who they are NOT — 5+ explicit negatives with reasoning, tied to mechanical blind spots
- A5: Voice/tone — 2+ pass examples, 2+ fail examples, tone rules
- A6: Visual identity — silhouette, dress, era, palette, movement language per tier
- A7: Caste/table position — who looks down, who they look down on, strategic implications
- A8: Contrast anchor — nearest faction, bond-type contrast (circumstance vs choice)

### B. Body and Presence
- B1: Thumbnail read — single figure at 69×96, visually distinct from all factions
- B2: Movement language — 3 registers min, written for art panel
- B3: Villium relationship — acquisition, use, sensory detail, what it does NOT do
- B4: Rank-and-file vs named — tier descriptions, named characters with humanizing details

### C. Geography and Landmarks
- C1: Core territory — 3-5 named zones with thematic meaning
- C2: Territory→mechanic bridge — table, 4+ entries with reasoning
- C3: Friction map — who they border, specific friction points
- C4: Landmark table — card/art use, art direction notes
- C5: Do NOT use — other factions' landmarks excluded, canon citations
- C6: Overlap doc — shared territory mechanism acknowledged

### D. History and Cast
- D1: Founding beat — year + event, timeline matches Inner_Circle.md
- D2: Founding cast table — name, role, card slot, canon knowledge states verified
- D3: Internal rifts — 2+ camps mapped to play styles
- D4: Long arc — 3-act trajectory, faction-specific stakes
- D5: Headline test — 3+ named characters pass "would I open this in a pack?"

### E. Mechanical Implications
- E1: Signature keywords 3-5 — each has street-read one-liner tied to identity
- E2: Spine vs splash — separated with reasoning
- E3: Blind spots — mechanical can'ts match narrative can'ts (A4)
- E4: Card type lean — minion/spell/weapon/ambush bias with reason
- E5: Curve lean — primary/secondary aggro/mid/control
- E6: Diplomacy — partner faction + all tensions with specific hooks

### F. Play Styles
- F1: Three archetypes — named lanes from internal identity + hero assignment
- F2: Win line each — faction-specific, player-legible
- F3: Hero fantasy each — character + emotional job + opponent experience
- F4: Overlap rule — shared identity, different payoffs, cross-splash costs

### G. Art Direction
- G1: Artist profile target — verified against tools/art_pipeline/profiles/
- G2: Palette/line/era — matches A6, period-accurate
- G3: Scene grammar — 3+ scene types with lighting/focal point/emotional register, anti-patterns listed
- G4: Compliance hooks — faction-specific gates (no occult, era accuracy, etc.)

### H. Lock and Governance
- H1: Status — clearly marked (DRAFT/LOCKED)
- H2: Open items — ≤5 Joe decisions, flavor depth auto-generated not deferred
- H3: Joe batch format — provided
- H4: Don't-reopen list — 8+ locked decisions cited against canon
- H5: Vault pointers — all source + destination paths

## Lane 2: Canon Alignment (K)
Cross-reference gate before card design:
- K1: Inner_Circle.md match — all C-01 through C-0N verified
- K2: Territory.md match — territory model and ownership claims
- K3: Playstyle.md match — keywords, exclusivity rules, blind spots
- K4: Hero roster match — names, HP, knowledge states
- K5: DCW Beat 1 decisions — all Joe-gated decisions respected

## Lane 3: Cards (M)
- M1: Mechanical identity match — keywords per exclusivity rules
- M2: Blind spot respect — no violations
- M3: Rarity floor — score meets floor
- M4: Naming — passes A5 voice test
- M5: Flavor text — faction-coherent, card-specific
- M6: Ludonarrative — mechanic matches name/flavor
- M7: Three-reaction test — Legendaries only

## Lane 4: Art (V)
- V1: Profile match — Clovis/Alan etc. verified
- V2: Palette match — matches A6
- V3: Era lock — 1961 Detroit, no anachronisms
- V4: Occult lock — no horror aesthetics
- V5: Movement match — correct register per tier
- V6: Villium accuracy — violet only

## Lane 5: Naming (N)
- N1: Era match — 1961 appropriate
- N2: Faction voice — matches A5
- N3: Headline test — works as card title
- N4: Canon consistency — matches locked character names
- N5: Syllable weight — one-syllable preferred for Bruiser non-legendaries

## Lane 6: Process (P)
Self-improvement gate:
- P1: Patch generation — every score < 2 produces patch candidate
- P2: Patch application — prior patches present in current playbook
- P3: Compound tracking — first-attempt scores tracked across factions
- P4: Human handoff — ≤5 Joe decisions per artifact

## Usage Protocol

Critic agents: load rubric → score every criterion in applicable lanes → for score < 2, generate PATCH CANDIDATE with specific playbook path, section, and new line → output scores table, failures table, canon alignment summary, Joe decisions (≤5), first-attempt score, and compound delta.
