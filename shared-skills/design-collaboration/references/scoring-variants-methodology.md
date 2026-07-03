# Scoring Variants Methodology (Paul + Joe, locked 2026-05-27)

When designing a card at 3V+, present scoring variants — not "here's the card," but "here are the body options with delta calculations so you can see the floor and ceiling."

## The Process

For each card design:

1. **Concept first** — who is this person? What do they do? How does that translate mechanically?
2. **Present body options** — 2-3 stat line variants with delta calculations
3. **Show the math** — body delta, each ability cost with modifiers broken out, final delta
4. **Let Joe decide** — the numbers guide the decision, Joe locks the body
5. **Lock and move on**

## Joe's Rule (2026-05-27)

"I think sometimes you're in such a rush to do so much work we should really be taking these cards one at a time because then you have to walk through every single process. The process becomes you're brainstorming: what is this guy going to do? Okay if this guy has a 2-3, what's the score? If he has a 2-2, what's the score? If he has this ability and a 2-2, what's the score? That kind of gives you the range. It kind of gives you the floor and the ceiling of where the card could go and then it fleshes out from there."

## Anti-Rushing Signal

Joe (2026-05-27): "I think you're just going to gloss over this shit because you're trying to rush to get these cards done."

When you present a card and Joe says something like this, you skipped the process. Back up. One card. Scoring variants. Full walkthrough.

## Scoring Tools

Do NOT load the full 22K `Bruiser_Scoring_System.md` every session. Use:

1. **Quick-Ref** — `design/bruiser_revisions/Bruiser_Scoring_QuickRef.md` (~2K tokens). Base costs + faction modifiers + checklist. Load at session start.
2. **Calculator** — `design/bruiser_revisions/bruiser_scorer.py`. `score_card(V, ATK, HP, 'crew', ['ability1', ...])` → full delta breakdown. Use for verification.

## Example: Bouncer (2V Spread)

Concept: bouncer at the social club door. Checks IDs. Turns people away.

Body options at 2V (vanilla 4 pts):
- 2/2: body Δ 0.0. BC: Reveal top, discard if minion + gain +1 ATK (~1.2). Final Δ +1.2 ⚠
- 2/3: body Δ +1.0. Same ability. Final Δ +2.2 ✗ RED

2/2 with kicker was the sweet spot. The +1 ATK is temporary — he deals with the problem, then goes back to being a 2/2.

## Scoring Checklist

1. Body Δ = (ATK+HP) − (2×V)
2. Look up each ability base cost
3. Add Bruiser-wide modifier
4. Add crew-specific modifier
5. Sum all ability costs
6. Final Δ = Body Δ + total ability cost
7. Check range: −2.0 to +2.0. Flag extremes. Red at +2.0+
8. Target +0.1 to +0.5 for non-legendaries

## Rarity Bands (2026-05-27 — delta determines minimum rarity)

**Rarity is determined BY the score, not assigned after.** Score the card → delta determines minimum rarity → design TO that rarity's complexity budget.

| Rarity | Δ Ceiling | Rule |
|--------|-----------|------|
| Common | ≤ +0.5 | Vanilla or one simple keyword. Workhorse. |
| Uncommon | ≤ +1.0 | Two keywords or keyword + trigger. Complexity allowed. |
| Rare | ≤ +2.0 | Two keywords + synergy. Pushed stat line possible. |
| Legendary | Any | Above +2.0 = Legendary ONLY. |

**Rules:**
- Negative Δ is fine at any rarity. Only the ceiling gates.
- If Δ > assigned rarity ceiling → RARITY FAIL. Promote or redesign.
- Calculator: `score_card(V, ATK, HP, 'crew', ['abilities'], 'assigned_rarity')` — `validate_rarity()` flags mismatches.
- Gopher (+1.0 as Common → FAIL, must be Uncommon). Bouncer (+1.5 as Common → FAIL, must be Rare).
