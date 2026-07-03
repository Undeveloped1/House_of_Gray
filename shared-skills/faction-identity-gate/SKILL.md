---
name: faction-identity-gate
description: Pre-design gate that evaluates whether a faction concept is worth building. Runs BEFORE card design — checks lore depth, mechanical identity, player appeal, Villium relationship, crew structure, cross-faction dynamics, and 1961 Detroit texture. Phase 0. Model-agnostic, faction-agnostic.
category: creative
---

# Faction Identity Gate — Phase 0

**When to use:** After lore is drafted, before function registry or card design. This gate answers: "Is this faction worth building?"

**Exit condition:** All 10 dimensions score 3+ out of 5. No synthesis locks rated "drift." Below 3 on any dimension = fix the identity before touching mechanics.

---

## The 10 Dimensions

For each, score 1 (broken), 2 (weak), 3 (solid), 4 (strong), 5 (definitive).

### 1. Hook — One-Sentence Sell

**The question:** Can I sell this faction to a stranger in one sentence?

| Score | Standard | Behavioral Anchor |
|-------|----------|-------------------|
| 1 | Can't describe it without paragraphs | You need setup to explain what they are |
| 2 | Has a description, not a hook — reads like a wiki entry | Person nods and says "okay" |
| 3 | Clean sentence, communicates what they are | Person can explain it back to you in their own words |
| 4 | Memorable, specific, makes you curious | You can restate it from memory after one read and get the gist right |
| 5 | Instant mental image. "I want to play that." | You say it to a friend who doesn't play TCGs and they ask "is that a book? can I read it?" |

**Format:** "[Faction] are [who] who [do what] in [where] because [why]."

**Sub-check — Name:** Does the faction name carry meaning? Is it earned in the lore, not just applied? Would a new player be curious about what it means?

---

### 2. Mechanical Identity — What They Do

**The question:** What does this faction DO mechanically that no other faction does? What's the signature mechanic?

| Score | Standard | Behavioral Anchor |
|-------|----------|-------------------|
| 1 | Generic. Could be any faction. | You'd need faction labels to tell their cards apart from another faction |
| 2 | Borrowed from MTG/Hearthstone with no twist | Recognizable archetype, no Five Crests spin |
| 3 | Has a clear signature mechanic that defines the faction | You can name it immediately; it appears on most cards |
| 4 | The mechanic IS the identity — you can't separate them | If you removed it, the faction's lore would stop making sense |
| 5 | Novel. No TCG analog. Makes designers jealous. | You describe it to another designer and they pause |

**Test:** If you removed this mechanic and gave them something else, would the faction still make sense? If yes, the mechanic isn't the identity. Score high only if the answer is no.

**Sub-check — Philosophy:** If you explained the faction's signature mechanic to a new player, would they correctly infer the faction's philosophy? If not, the mechanic and the identity are running on separate rails.

---

### 3. Blind Spots — What They Can't Do

**The question:** What can't this faction do? Do the weaknesses create real deckbuilding tension?

| Score | Standard | Behavioral Anchor |
|-------|----------|-------------------|
| 1 | No blind spots defined. Can do everything. | Answer to "what can't they do?" is silence |
| 2 | Has one weak blind spot ("no big heals") — doesn't matter | Blind spot exists but doesn't change deckbuilding |
| 3 | 2-3 clear, meaningful blind spots that shape deckbuilding | You actively consider the blind spot while building |
| 4 | Blind spots are painful enough you actively want to splash | You'd pay a real cost to cover one of them |
| 5 | The blind spot IS the faction's defining constraint. Defines them as much as the strength. | Players mention the weakness before the strength when describing the faction |

**Format:** List the 2-3 things they CANNOT do. Each should force a real choice.

**Drift-risk flag:** What happens if the team gets lazy and patches one of the blind spots with one card? Name the slippery slope. Example: "We'll just add one Taunt card, it'll be fine" → faction identity erodes.

---

### 4. Villium Relationship — What the Substance Means

**The question:** What is Villium TO this faction? Power source? Addiction? Currency? Mystery? Weapon? Why do they care?

| Score | Standard | Behavioral Anchor |
|-------|----------|-------------------|
| 1 | No relationship defined. They use Villium "because." | You can't answer "why Villium specifically?" |
| 2 | Generic: "it gives them powers" | Could swap their Villium relationship with another faction |
| 3 | Specific, unique relationship that shapes how they use it | Another faction's Villium use wouldn't make sense for them |
| 4 | The relationship is emotional, not just mechanical | You can describe how Villium makes them FEEL |
| 5 | You could write a short story about how Villium changed this faction specifically | The faction's origin IS their Villium relationship — remove it and they don't exist |

**Test:** Could you swap this faction's Villium relationship with another faction's and nobody would notice? If yes, score low.

---

### 5. Player Fantasy — Who Picks This

**The question:** Who is the player who mains this faction? What emotional experience are they chasing?

| Score | Standard | Behavioral Anchor |
|-------|----------|-------------------|
| 1 | No clear player identity. "People who like blue cards." | You can't name a person |
| 2 | Generic: "people who like control" | Archetype preference, not identity |
| 3 | A clear player type with a clear emotional payoff | You can describe the feeling they're chasing |
| 4 | The fantasy is specific, emotional, and the mechanics deliver it | You could write their Steam review: "I love this faction because..." |
| 5 | Players describe this faction by how it makes them FEEL, not what it does | The faction has a personality cult |

**Sub-check — Emotional truths:** Name 2-3 specific emotional truths this faction expresses. Would someone who's never played a TCG recognize themselves in one of them? If none would land with a non-player, cap at 3.

**Format:** "The player who picks [Faction] wants to feel [emotion] by [mechanical expression]."

**Sub-check — One-line dialogue:** Write one sentence that could ONLY be spoken by a member of this faction. If another faction's member could credibly say it, the voice isn't specific enough.

---

### 6. Crew Structure — Who's Inside

| 6 | **Crew Structure** | Does the faction have 3-4 distinct crews with clear identities, jobs, tensions, and CANNOT DO lists? If crews share mechanics without distinction (Street and Professionals both have Paid), the crew system is cosmetic. Validate: can you describe what each crew DOES and what it CANNOT DO in one sentence? If not, score low. Load `pathway-design` skill for the full crew identity profile template. |

| Score | Standard | Behavioral Anchor |
|-------|----------|-------------------|
| 1 | No crew structure. Just a list of cards. | Cards don't cluster into groups |
| 2 | Has crews but they blur together — can't tell them apart | You need labels to distinguish them |
| 3 | 3-4 crews, each with a distinct job and flavor identity | You can name each crew's function from memory |
| 4 | Crews have internal tensions, different play patterns, different emotional tones | The crews disagree with each other about something meaningful |
| 5 | Each crew could be a faction. Their conflicts fuel the faction's internal story. | You could write a scene between two crew leads that's dramatically tense without mentioning any other faction |

**Format:** List each crew with: name, job (what they DO), vibe (how they FEEL), tension (who they conflict with inside the faction).

---

### 7. Hero Lanes — Three Paths

**The question:** Three heroes, three distinct win conditions, three different emotional experiences. Do they exist?

| Score | Standard | Behavioral Anchor |
|-------|----------|-------------------|
| 1 | One hero, or three heroes that play identically | Decklists would look the same |
| 2 | Three heroes but two are variations of the same idea | Two heroes differ by 5-8 cards |
| 3 | Three heroes with different gameplans and different emotional payoffs | Each hero's win condition is distinct |
| 4 | The three heroes represent three philosophies within the faction — you pick the one you believe in | Players argue about which hero is "right" |
| 5 | Playing each hero feels like a completely different faction experience | You'd recommend different heroes to different friends based on who they are, not what they play |

**Format:** Hero, HP, lane, win line, emotional thesis.

---

### 8. Cross-Faction — Friends and Enemies

**The question:** Who do they love, hate, fear, or ignore? Why? Does it create natural narrative tension?

| Score | Standard | Behavioral Anchor |
|-------|----------|-------------------|
| 1 | No cross-faction relationships defined | Blank table |
| 2 | Vague: "they don't like Bruisers" — no reason | Relationships exist but you can't explain why |
| 3 | Clear allies and rivals with clear reasons | Each relationship has a "because" |
| 4 | Relationships are grounded in specific historical events or philosophical conflicts | You can point to the event that defined the relationship |
| 5 | You could write a scene between any two faction leaders that would be dramatically interesting | Every pair has dramatic potential |

**Format:** For each other faction: relationship (ally/rival/neutral/ignore), why, tension point.

**Sub-check — Contrast anchor:** What other faction is this one most likely to be confused with? Articulate the single sentence that distinguishes them. If you can't, the identity isn't sharp enough — cap at 3.

---

### 9. World Texture — 1961 Detroit Specificity

**The question:** Does this feel like it could only exist in this place and time? Or could you transplant it anywhere?

| Score | Standard | Behavioral Anchor |
|-------|----------|-------------------|
| 1 | Generic fantasy. Could be any city, any year. | Change the date to 2024 and nothing breaks |
| 2 | Has some Detroit references but they're wallpaper | References exist but don't shape the faction |
| 3 | Detroit 1961-specific details that matter to the identity | The year and place are load-bearing |
| 4 | The city and era shape how the faction operates and sees the world | Changing the era would change how they think |
| 5 | You could navigate Detroit using only this faction's lore | Street names, neighborhoods, specific geography |

**Checklist:** Do the cards reference: specific Detroit geography? period technology? era-appropriate language? real historical texture? If not, score low.

**Sub-check — Daily life scene:** Write one paragraph of daily life for this faction. It should be specific to 1961 Detroit and impossible to transplant to another faction. If you can't, cap at 3.

---

### 10. Fun Check — Would I Play This? (Split Profile)

**The question:** The gut check. Be honest. Scored across three player profiles, each 1-3. Sum for total (max 9).

| Score | Spike — Competitive | Vorthos — Lore/Art | Johnny — Creative/Brewing |
|-------|---------------------|---------------------|---------------------------|
| 1 | Win con feels clunky or unrewarding | Cards don't tell a story. Generic. | Obvious build, no space to experiment |
| 2 | Satisfying but familiar — seen it before | Interesting lore, cards partly deliver it | Some brewing space but lanes are rigid |
| 3 | Mastery feels rewarded. Tight, deep. | Cards ARE the story. Want to read every flavor text. | Multiple builds, cross-archetype space, "what if?" questions |

**Spike test:** Would a competitive player feel clever for winning with this? Is there depth to master?
**Vorthos test:** Do the cards make you want to read the lore? Does flavor text reward attention?
**Johnny test:** Can you see at least two different builds per hero? Is there obvious space to brew?

---

## Synthesis Locks — 4 Mandatory Cross-Checks

Not scored. Rated: **locked** (tight), **staple** (adjacent but not fused — flag for rework), or **drift** (contradict or ignore each other — fail the gate regardless of individual scores).

| Pair | Question |
|------|----------|
| **Mechanic ↔ Villium** | If you explained the mechanic, would a new player infer the philosophy? Does the Villium relationship explain WHY the mechanic exists? |
| **Mechanic ↔ Fantasy** | Does winning with this deck feel like the emotional payoff the lore promises? Does the victory condition match the fantasy? |
| **Blind Spots ↔ World Texture** | Are the weaknesses grounded in who they are, or just balance decisions? Does the lore explain WHY they can't do those things? |
| **Crews ↔ Heroes** | Does each hero clearly draw from a different crew? Is there a crew with no hero (gap) or a hero with no crew (float)? |

Any "drift" rating = fail the gate. Fix the disconnection before proceeding.

---

## Surprise Flag — Binary Bonus

**"Did this faction do something that made you stop and reconsider what a TCG faction can be?"**

If yes: +2 to total score. This is the gap between "complete" and "magnetic."

---

## Scoring

| Total Score | Verdict |
|-------------|---------|
| 52-61 | **Magnetic.** Don't just build this — protect it. This faction is special. |
| 40-51 | **Ready for card design.** The faction is fully realized. |
| 30-39 | **Needs work.** 1-3 dimensions are weak. Fix before functions. |
| 20-29 | **Back to lore.** Multiple dimensions are undefined or generic. |
| Below 20 | **Rebuild.** The concept isn't landing. |

Individual dimension threshold: any dimension scored 2 or below must be fixed before proceeding, regardless of total.

Synthesis threshold: any lock rated "drift" fails the gate, regardless of total.

---

## Drift-Risk Flags — Per Dimension

After scoring, for each dimension name: "If we get lazy, what does the bad version look like?" This is a guardrail for card design, not a score modifier.

Example:
- Fantasy drift: "Wizards on motorcycles — lose the carnival warmth, keep the leather aesthetic."
- Blind spots drift: "We'll just add one Taunt card, it'll be fine" → slippery slope.
- World texture drift: "Generic wasteland bikers — forget it's 1961 Detroit, not post-apocalypse."

---

## Output Format

After running the gate, produce:

1. **Scored table** — 10 dimensions, scores, notes
2. **Fun check split** — Spike/Vorthos/Johnny, each 1-3, sum
3. **Synthesis locks** — 4 pairs, rated locked/staple/drift
4. **Surprise flag** — yes/no, +2 if yes
5. **Total score + verdict**
6. **Ranked gap list** — what needs work, with specific suggestions
7. **What's already strong** — what should be protected during card design
8. **Drift-risk flags** — per-dimension failure modes to guard against
9. **Emotional truths** — 2-3 universal truths the faction expresses
10. **Dialogue line** — one sentence only a member of this faction would say
11. **Daily life scene** — one paragraph of 1961 Detroit texture
12. **Contrast anchor** — nearest faction, one-sentence distinction
13. **Expansion potential** — story suggested but not told in the base set

---

## Post-Gate

**Reference example:** `references/trigger-identity-gate-example.md` — Trigger scored 50/61 (Magnetic) 2026-06-11. Full dimension scores, synthesis locks, and what made the gate work.

If the faction passes (30+, no 2s, no drift locks), proceed to:
1. Function Registry (12-18 functions derived from lore)
2. Synergy Web (edges between functions)
3. Build Facts (curve, crew distribution, rarity targets)
4. Card Design (expressions, review, ship)

If it fails, fix the identity. Do not design cards for a faction that doesn't know what it is.

## Post-Design — Cohesion Check

After card design exists, run the cohesion check to verify cards against all lore documents. See `references/cohesion-check.md` for the full 8-dimension audit format (voice, history, cast, mechanics, territory, cross-faction, don't reopen, open questions). This is the companion to the pre-design identity gate — catches factual errors, tonal mismatches, and keyword constraint violations before ship.
