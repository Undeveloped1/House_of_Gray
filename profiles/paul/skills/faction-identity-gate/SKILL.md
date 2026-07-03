---
name: faction-identity-gate
description: "Pre-design gate — evaluates whether a faction concept is worth building. 10 dimensions, 4 synthesis locks. Runs BEFORE card design."
version: 2.0.0
author: Paul
---

# Faction Identity Gate — Phase 0

**When:** After lore is drafted, before function registry or card design.
**Exit condition:** All 10 dimensions score 3+/5. No synthesis locks rated "drift."
Full original with historical context preserved at `docs/Paul/workspace/faction-identity-gate-archive.md`.

## The 10 Dimensions

Score each 1 (broken) to 5 (definitive). Below 3 on any = fix before touching mechanics.

### 1. Hook — One-Sentence Sell
Can you sell this faction to a stranger in one sentence?

| Score | Standard |
|-------|----------|
| 1 | Can't describe without paragraphs |
| 2 | Has description, not a hook — reads like wiki |
| 3 | Clean sentence, communicates what they are. Person can restate from memory. |
| 4 | Memorable, specific, makes you curious |
| 5 | Instant mental image. "I want to play that." |

**Format:** "[Faction] are [who] who [do what] in [where] because [why]."
**Name check:** Is the faction name earned in lore, not just applied?

### 2. Mechanical Identity — Signature Mechanic
What does this faction DO mechanically that no other faction does?

| Score | Standard |
|-------|----------|
| 1 | Generic — could be any faction |
| 2 | Borrowed from MTG/Hearthstone, no twist |
| 3 | Clear signature mechanic defining the faction |
| 4 | Mechanic IS identity — can't separate them |
| 5 | Novel — no TCG analog. Makes designers jealous. |

**Test:** Remove the mechanic, give them something else — does faction still make sense? Score high only if answer is NO.
**Philosophy check:** Would a new player correctly infer the faction's philosophy from the signature mechanic alone?

### 3. Blind Spots — What They Can't Do
Do the weaknesses create real deckbuilding tension?

| Score | Standard |
|-------|----------|
| 1 | No blind spots defined |
| 2 | One weak blind spot ("no big heals") — doesn't matter |
| 3 | 2-3 clear, meaningful blind spots shaping deckbuilding |
| 4 | Blind spots are painful enough you actively want to splash |
| 5 | Blind spot IS defining constraint. Players mention weakness before strength. |

List 2-3 things they CANNOT do. Each forces a real choice.
**Drift-risk flag:** What's the slippery slope? "We'll just add one Taunt card..."

### 4. Villium Relationship
What is Villium TO this faction? Power source? Addiction? Currency? Mystery?

| Score | Standard |
|-------|----------|
| 1 | No relationship — "because" |
| 2 | Generic: "it gives them powers" |
| 3 | Specific, unique relationship shaping how they use it |
| 4 | The relationship is emotional, not just mechanical |
| 5 | The faction's origin IS their Villium relationship |

**Test:** Could you swap this with another faction's Villium relationship and nobody would notice?

### 5. Player Fantasy — Who Picks This
Who mains this faction? What emotional experience are they chasing?

| Score | Standard |
|-------|----------|
| 1 | No clear player identity |
| 2 | Archetype preference, not identity |
| 3 | Clear player type with clear emotional payoff |
| 4 | Fantasy is specific, emotional, and mechanics deliver it |
| 5 | Players describe faction by how it makes them FEEL |

**Emotional truths:** Name 2-3 universal truths this faction expresses. Would a non-TCG-player recognize themselves in one?
**Dialogue line:** One sentence only a member of this faction would say.

### 6. Crew Structure — Who's Inside
3-4 distinct crews with clear identities, jobs, tensions, and CANNOT DO lists?

| Score | Standard |
|-------|----------|
| 1 | No crew structure — just cards |
| 2 | Crews blur together — can't tell them apart |
| 3 | 3-4 crews, each with distinct job and flavor identity |
| 4 | Internal tensions, different play patterns, different emotional tones |
| 5 | Each crew could be a faction. Their conflicts fuel internal story. |

**Format per crew:** name, job (what they DO), vibe (how they FEEL), tension (who they conflict with inside faction).

### 7. Hero Lanes — Three Paths
Three heroes, three distinct win conditions, three different emotional experiences?

| Score | Standard |
|-------|----------|
| 1 | One hero, or three identical |
| 2 | Two are variations of same idea |
| 3 | Three heroes with different gameplans and emotional payoffs |
| 4 | Three philosophies within faction — players argue which is "right" |
| 5 | Each hero feels like different faction experience |

**Format:** Hero, HP, lane, win line, emotional thesis.

### 8. Cross-Faction — Friends and Enemies
Clear allies, rivals, tension points with other factions?

| Score | Standard |
|-------|----------|
| 1 | No cross-faction relationships |
| 2 | Vague: "don't like Bruisers" — no reason |
| 3 | Clear allies and rivals with clear reasons |
| 4 | Relationships grounded in specific historical events or conflicts |
| 5 | Any pair of faction leaders would produce a dramatically interesting scene |

**Contrast anchor:** Nearest faction they could be confused with. One-sentence distinction. If you can't, cap at 3.

### 9. World Texture — 1961 Detroit Specificity
Could this only exist in this place and time?

| Score | Standard |
|-------|----------|
| 1 | Generic fantasy — any city, any year |
| 2 | Detroit references as wallpaper |
| 3 | 1961 Detroit-specific details that matter to identity |
| 4 | City and era shape how faction operates and sees the world |
| 5 | Could navigate Detroit using only this faction's lore |

**Checklist:** Specific geography? Period technology? Era-appropriate language? Real historical texture?
**Daily life scene:** One paragraph of daily life — specific to 1961 Detroit, impossible to transplant.

### 10. Fun Check — Would I Play This? (Split Profile)
Three player profiles, each scored 1-3. Sum for total (max 9).

| Score | Spike (Competitive) | Vorthos (Lore/Art) | Johnny (Creative/Brewing) |
|-------|---------------------|---------------------|---------------------------|
| 1 | Win con clunky or unrewarding | Cards don't tell a story | Obvious build, no experimentation space |
| 2 | Satisfying but familiar | Interesting lore, partly delivered | Some brewing space but rigid lanes |
| 3 | Mastery feels rewarded — tight, deep | Cards ARE the story | Multiple builds, cross-archetype space |

## Synthesis Locks — 4 Mandatory Cross-Checks

Not scored. Rated: **locked** (tight), **staple** (adjacent but not fused — needs rework), or **drift** (contradiction — fails gate).

| Pair | Question |
|------|----------|
| Mechanic ↔ Villium | Does Villium relationship explain WHY the mechanic exists? |
| Mechanic ↔ Fantasy | Does winning feel like the emotional payoff lore promises? |
| Blind Spots ↔ World Texture | Are weaknesses grounded in who they are, not just balance? |
| Crews ↔ Heroes | Each hero draws from a different crew? Any gaps/floats? |

Any "drift" = fail. Fix before proceeding.

## Surprise Flag

"Did this faction do something that made you reconsider what a TCG faction can be?"
Yes: +2 to total. This is the gap between "complete" and "magnetic."

## Scoring

| Total | Verdict |
|-------|---------|
| 52-61 | **Magnetic.** Protect this faction. |
| 40-51 | **Ready for card design.** |
| 30-39 | **Needs work.** Fix before functions. |
| 20-29 | **Back to lore.** Multiple dimensions undefined. |
| Below 20 | **Rebuild.** |

Any dimension ≤2: fix regardless of total. Any synthesis lock "drift": fails regardless of total.

## Drift-Risk Flags

Per dimension, name the failure mode: "If we get lazy, what does the bad version look like?"
Guardrail for card design, not a score modifier.

## Output Format

1. Scored table — 10 dimensions with scores and notes
2. Fun check split — Spike/Vorthos/Johnny (each 1-3, sum)
3. Synthesis locks — 4 pairs rated locked/staple/drift
4. Surprise flag — yes/no, +2 if yes
5. Total score + verdict
6. Ranked gap list — what needs work, with specific suggestions
7. What's already strong — protect during card design
8. Drift-risk flags per dimension
9. Emotional truths — 2-3 universal truths
10. Dialogue line — one sentence only this faction says
11. Daily life scene — one paragraph, 1961 Detroit
12. Contrast anchor — nearest faction, one-sentence distinction
13. Expansion potential — stories suggested but not told in base set

## Post-Gate

**Reference:** `references/trigger-identity-gate-example.md` — Trigger scored 50/61 (Magnetic) 2026-06-11.

If faction passes (30+, no ≤2s, no drift locks), proceed to:
1. Function Registry (12-18 functions from lore)
2. Synergy Web (edges between functions)
3. Pathway Design (turn maps, crew profiles, slot boundaries)
4. Card Design

If it fails, fix the identity. Don't design cards for a faction that doesn't know what it is.

## Post-Design Cohesion Check

After card design exists, verify cards against lore documents using the 8-dimension audit in `references/cohesion-check.md`: voice, history, cast, mechanics, territory, cross-faction, don't reopen, open questions.
