# Cohesion Check — Post-Design Gate

**When to use:** After a card design pass exists, before shipping. Compares card text against all lore documents for factual and tonal consistency. Complementary to the pre-design Faction Identity Gate — this is the post-design verification.

**Exit condition:** Zero critical findings (❌). All ⚠️ items flagged for Joe. All ✅ items verified.

---

## Check Dimensions

### 1. Voice — Does the faction sound like itself?

Read every card's flavor text, voice line, and character identity. Ask:
- Does the tone match the lore bible?
- Do the emotional chords come through in card text?
- Are there tonal mismatches — a card that sounds like a different faction?
- Is the one-line dialogue test passed per card? (Could only a member of THIS faction say it?)

**Output:** "What rings true" list + "What sounds off" list with specific cards.

### 2. History — Factual Accuracy

Check every card against all canon documents. Specific checks:
- Character knowledge states: does the card reveal something the character shouldn't know yet?
- Timeline: does the card reference an event at the wrong time?
- Pronoun/identity locks: any Joe-locked gender/identity spec violated?
- Death states: do dead characters appear alive? Do alive characters appear dead?
- Hidden knowledge: does a card reveal something the faction doesn't canonically know? (e.g., Henry faked his death — Dusters don't know → no card should reference this)
- Location locks: does the card put the faction in the wrong place?

**Output:** "Passes scrutiny" list + "Factual issues found" list (with canonical citation).

### 3. Cast — Character Accuracy

For every named character card:
- Does the flavor text match their Inner_Circle.md or lore bible description?
- Are relationships correct? (parent/child, leader/subordinate, ally/rival)
- Any character referred to with a relationship they don't canonically have?
- Name spelling, title, and nickname all consistent?

**Output:** "Name quality" assessment + "Relationship clarity" check + any errors.

### 4. Mechanics — Keyword & Constraint Audit

Check every card against the faction's mechanical identity:
- Signature keywords used correctly? (e.g., Overdose is mandatory engine-locked — no card treats it as optional)
- Blind spots respected? (No Taunt, no healing — verify every card)
- Faction-exclusive keywords maintained? (Blur only on Duster cards — no bleed to other factions)
- The Bends triggers correctly? (after 2nd lifetime OD, permanent mutation — consistent across all Touched cards)
- No keyword is unreachable? (e.g., a card has Bends but no Overdose → Bends can never trigger)

**Output:** Constraint-by-constraint table with ✅/⚠️/❌ and evidence.

### 5. Territory — Location Audit

- Does any card reference a location that conflicts with Territory.md?
- Are Detroit-specific references (neighborhoods, streets, landmarks) accurate to 1961?
- Does the faction's geography match how they're described on cards?

**Output:** Any conflicts found, or "Zero conflicts."

### 6. Cross-Faction — Relationship Audit

- Do card references to other factions match the established relationships?
- Any incorrect alliances or rivalries stated?
- Any faction referenced that the card's faction shouldn't canonically know about? (e.g., Dusters don't know Faceless exist → no Duster card should reference Faceless)

**Output:** Any conflicts found, or "Neutral — no incorrect claims."

### 7. Don't Reopen — Joe Lock Audit

Check every Joe-locked decision from the most recent DCW merge or lore consolidation:
- For each locked decision (C-01 through C-NN), verify the card design doesn't contradict or reopen it
- If the card design accepts the lock as-is → ✅
- If the card design implies a different resolution → ❌

**Output:** Table of every Joe lock with status.

### 8. Open Questions — For Joe Batch

Any factual ambiguities the card design introduces that need a designer decision. Not errors — questions. Format: question + recommendation if you have one.

---

## Severity Markers

| Marker | Meaning |
|--------|---------|
| ✅ | Verified — matches canon |
| ⚠️ | Flagged — minor issue, doesn't block ship |
| ❌ | Critical — blocks ship, must fix |

---

## Output Format

1. Voice assessment (rings true + sounds off)
2. History assessment (passes + issues)
3. Cast assessment (names + relationships)
4. Mechanics audit (constraint table)
5. Territory audit
6. Cross-faction audit
7. Don't Reopen audit (Joe lock table)
8. Open Questions (for Joe batch)
9. Summary — one-line verdict + ranked issues
