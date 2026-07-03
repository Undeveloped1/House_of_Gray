# Card Design Methodology

Operational card design procedures for TCG development. This covers the mechanics of designing individual cards — the brief, the scoring system, per-V packets, and design discipline.

## Card Design Brief

A single document (`design/bruiser_revisions/Bruiser_Card_Design_Brief.md`) containing every hard constraint needed to design a card. Load it at the start of every card design session.

### Brief Contents
1. Faction identity + board state philosophy
2. Mana curve (card counts per V)
3. Power curve (stat ranges per V with sweet spots)
4. Keyword rarity limits (by V and rarity)
5. All faction keywords with expressions
6. Universal keywords usable by the faction
7. Crew one-line identities
8. Crew color-coding (how many cards each crew gets per V slot)
9. Design rules (e.g. "No 0-attack Bruiser minions")
10. Locked cards (already designed, do not redesign)

## Scoring System

The brief gives you constraints (what's allowed). The scoring system gives you budget (what fits). Both are required.

Preferred loading: **per-V packet + slim ability quick-ref** (~5K tokens). If no packet exists for the V, load `design/bruiser_revisions/Bruiser_Scoring_System.md`:

- **§1 Mana curve:** 33 minion slots, crew count per V, precon maps, curve band percentages
- **§2 Full power curve:** every V, every viable stat line, who gets each body (character-driven), delta from vanilla budget
- **§3 Delta rules:** -2.0 to +2.0 range. Default bias toward positive (+0.1 to +0.5)
- **§4 Ability base costs:** ~100 abilities priced in 0.1 increments across 15 categories. One flat master table.
- **§5 Faction modifier matrix:** Two-layer system. Faction-wide modifiers + crew-specific modifiers stacked.
- **§6 Worked examples**
- **§7 Final table:** current-state roster row

**Presenting ability data:** Use ONE flat master table per category. Do not fragment across sub-section tables. Joe's feedback: "I don't see a table anywhere in that doc."

## Per-V Packet Strategy (Context Optimization)

**Problem:** Loading full Framework + PlanB + Scoring System burns 100K+ context. Session falls apart 20 minutes in.

**Fix:** Build a self-contained design packet for each Villium cost (~3-5K tokens):

1. Stat grid for that V — every viable body, who gets it, delta
2. Crew slot allocation — how many cards per crew, which are locked
3. Filtered ability costs — only keywords/BCs relevant to active crews (~15-20 entries)
4. Rarity budget — remaining C/U/R/L
5. Delta rules (copy-paste)
6. Already-locked cards at this V
7. Remaining slots checklist
8. Faction modifier quick-ref (one compact table)

Build packets at the end of each V. Each packet is the only doc needed to resume design at that V. Companion: slim ability quick-ref (~1K tokens, Bruiser-only base costs).

## Pre-Design Checklist (Run Before Every Card Batch)

1. **Stat check (brief):** Is stat line within power curve sweet spot for its V?
2. **Stat check (character):** Does stat line match WHO the person is? Character drives body. Body determines ability budget.
3. **Keyword count:** Does keyword+ability count match rarity+V limit?
4. **Crew assignment:** Does card's crew match color-coding table?
5. **Crew identity:** Does effect match what this crew does?
6. **Faction identity:** No 0-attack minions in Bruiser.
7. **Model B math:** Base cost → faction modifier → crew modifier → final cost. Subtract from vanilla budget. Delta within -2.0 to +2.0?
8. **Stat diversity check:** After all cards at a V, verify stat lines aren't all identical.
9. **Muscle/utility count:** After locking a V row, count muscle vs utility. If utility exceeds 30%, flag it.
10. **Degenerate ability check:** Full hand knowledge, unconditional removal, board-wide disruption → double-check pricing.

**Rule:** If any check fails, fix before presenting. Do not present a violating card and expect Joe to catch it.

**Also:** Before every card batch, use read_file to pull the relevant crew's keeper table from the Mechanics Brainstorm section. Two minutes of discipline prevents design drift.

## Card Design Cadence (by V)

- **1V and 2V:** Batch of 2-5. Tight power curve, strict keyword limits, few crew slots. Batch review acceptable.
- **3V and above:** One card at a time. Wider power band, keyword limits relax, more mechanical weight. Joe: "I'd rather have one at a time than a bunch of half-assed bullshit."
- **Legendaries:** One per session maximum. Earn their slot through narrative weight, not keyword density.

## Muscle/Utility Ratio (70/30)

Bruiser faction-wide: ~23 muscle, ~10 utility out of 33 minions.

| Type | Definition | Design Rule |
|------|-----------|-------------|
| **Muscle** | Body first. Keyword-only or vanilla. "I am a threat." | One keyword, one job. |
| **Utility** | Card text that draws, scrys, taxes, protects, generates value. | Hall earns these. Street does not. Dock/Yard gets one per V band. |

**Tracking:** After every V row locked, count muscle vs utility. If utility exceeds 30%, next V must bend hard toward keyword-only bodies.

## Degenerate Ability Pricing

**Full hand knowledge in 30-card format is degenerate.** Joe's ruling: looking at opponent's entire hand = 3.0 base (equivalent to discarding half their deck).

| Effect | Base Cost | Rarity Floor |
|--------|-----------|-------------|
| Reveal ONE random card | 0.5 | Common |
| Look at full hand | 3.0 | Rare/Legendary |
| Look + discard one (random) | 3.5+ | Legendary |
| Look + discard one (chosen) | 4.0+ | Legendary |

## Pitfall: Default Stat Line

The most common failure mode: every body defaults to the same stat line (e.g., all 1/3 at 2V). Designer optimizes for ability budget first, character second.

**Correct order:**
1. Who is this person? (character → expected body)
2. What stat line does that suggest? (consult §2 "Who Gets This" column)
3. What's the remaining ability budget? (2 × V minus body points)
4. What ability fits this person AND fits the budget?
5. If ability doesn't fit, adjust body — but always START from character.

**Incorrect (rejected):** What ability → maximize budget → same stat line for all → slap name on it.

## Pitfall: Mechanics-to-Card

When designing cards from a completed mechanics brainstorm, **always re-read the keeper table for the relevant crew before writing a single card.** Memory of the brainstorm produces flatter, wrong versions. Flavor and mechanical identity are in the keeper table — not in your recollection.

## Keyword Evolution Notes

**Shell → Shield (2026-05-26):** Old Shell = "Can't attack this turn. Can't be targeted, damaged, or destroyed." New Shield = "Can't be damaged until end of turn." Narrower but preserves offense. Base cost dropped 0.6→0.5. Use Shield for damage immunity. Old Shell's broader protection TBD.

## Phase 2 — Matrix-First Card Selection (2026-05-27)

After the keyword ecosystem is locked (Phase 1: mechanics synthesis), do NOT jump directly to designing cards V by V. Build the allocation matrix first.

**Order:**
1. Lock the crew × V × rarity matrix — how many slots does each crew get at each V, and at what rarity?
2. Present the matrix to Joe for approval.
3. Fill cells V-band by V-band (1V → 2V → 3V, etc.), presenting one band at a time for review.
4. For each cell: pull the best card from existing passes (Plan A, PlanB, Red Team) or design new if neither has a fit.
5. Present each card as: name, stats, text, rarity, and one-sentence "why this card."

**Why matrix-first:**
- Prevents allocation drift (e.g., Street cards creeping into 2V when Street isn't supposed to enter until 3V).
- Rarity budget is enforced structurally, not by memory.
- Crew balance across the curve is visible at a glance — you can see if Dock/Yard has 7 cards and Spread has 5 before designing anything.
- When a card gets cut (e.g., Alley Lookout replaced by Punching Bag), the matrix shows which crew slot opened up and who can fill it.

**Pitfall:** Starting V by V without the matrix leads to allocation drift, rarity budget violations, and crew imbalance caught too late. The matrix is cheap — build it first.

## V-Band Naming Discipline (2026-05-27)

Never use the same job title for two different crews in the same V-band. "Union Clerk" (Hall) and "Freight Clerk" (Dock/Yard) in the same 2V row is confusing — the player sees two "clerks" at the same cost from the same faction.

**Rules:**
- Each crew gets distinct role names within a V-band.
- If two crews both have a paperwork/admin role, differentiate: Front Desk (Hall reception), Manifest Clerk (Dock/Yard shipping), Gopher (Spread errand runner).
- The street-fight callout test applies: if you shout "Get Clerk!" nobody knows who. "Get Front Desk!" — everyone knows.

## Scoring Variants Per Card (3V+ Required)

**For every card at 3V and above:** present multiple body variants with their delta scores. Do not lock into one stat line before showing the range.

Joe's process (2026-05-27): "If this guy has a 2-3, what's the score? If he has a 2-2, what's the score? If he has this ability and a 2-2, what's the score? That kind of gives you the range. It gives you the floor and the ceiling of where the card could go."

**Format per card:**
```
| Body | Body Δ | Total Δ | Verdict |
|------|--------|----------|---------|
| X/Y  | ±Z.Z   | ±T.T     | Note    |
```

Present the table, let Joe pick the body, then lock. This replaces the old pattern of presenting one version and asking "is this right?"

**When scoring is approximate:** flag any ability costs not in the scoring system as "~estimate" and note uncertainty. Do not fake precision.

## Hall Design: From Lived-In, Not From Shelf

Hall is the union front — not "the card advantage crew." Designing Hall cards by reaching for Scry/Draw off a generic shelf produces "Skiver cards": efficient, samey, no personality. 

**Correct: design from specific Hall activities.**
- The dinner circuit → BC: Both players draw 1. You look at what they drew.
- The envelope → BC: Target minion can't attack this turn (Hobble via politics).
- The no-strike guarantee → Ongoing: minions that haven't attacked this game can't be targeted.
- Marge's files → BC: Look at top 3 of opponent's deck, bottom one, reveal another.

**Incorrect:** BC: Scry 2 + give +0/+2. BC: Draw 1. These are function-delivery vehicles, not Hall cards.

Every Hall ability should answer: "What specific Hall activity produced this effect?" If the answer is "card advantage," redesign.

**Joe's signal (2026-05-27):** "It's like you ran out of tricks for card advantage. What are we doing here?" This is the red flag — Hall cards reading as Skiver (efficient, generic, interchangeable).

## Spread: Flex Crew, Not Hall-Lite

Spread is NOT a secondary card-advantage crew. Spread fills gaps across the faction — muscle, disruption, gambles, whatever the other three crews don't cover.

**What Spread does:**
- Flexes into muscle when needed (Bouncer at the social club door)
- Disrupts with gambles (reveal top card, discard if minion)
- Cheap bodies that enter/die for value (Gopher, Parts Runner)
- The whisper network (intel, but unreliably — gambly, not curated like Hall)

**What Spread is NOT:**
- Reliable card advantage (that's Hall)
- Combat keywords (that's Street)
- Control/denial (that's Dock/Yard)

**Joe's teaching (2026-05-27):** "Spread can flex. Spread can fill gaps. Spread can fill in holes and it gives it additional flavors. That way it doesn't read just guys that are working for the UWC."

When designing a Spread card, ask: "What gap does this fill that Dock/Yard, Hall, and Street don't cover?" If it overlaps with another crew's domain, it's wrong.

## Bouncer Design Walk-Through (Reference Example)

See `references/bouncer-design-walkthrough.md` for a complete, step-by-step example of the design process — from concept to scoring variants to locked card. Joe designated this as a teaching example for the process.

## Phase 2: Card Design Batch Discipline

**At 3V and above:** one card at a time. Walk through concept → body variants → scoring → lock. Do not batch 3V+ cards. Do not gloss over mechanics to "get cards done."

Joe's signal (2026-05-27): "I think you're just going to gloss over this shit because you're trying to rush to get these cards done. I feel like sometimes you're in such a rush to do so much work we should really be taking these cards one at a time."

The speed trap now extends beyond mechanical review into the design process itself. Completion satisfaction from finishing cards quickly is a trap when each card hasn't been walked through its body variants and scoring.

## Clean Slate Discipline

When working from scratch, do not recycle old Plan A keywords with minor renames. Clean slate means genuinely new mechanical expressions derived from new crew texture. If a new mechanic converges on an old one through parallel thinking, that's fine — but the derivation path must be traceable to the new crew identity, not the old keyword list.
