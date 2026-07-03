# Craft Pass Review Pattern

How Paul reviews card craft passes from Cursor/Composer/Opus. Established during the Bruiser 4V craft pass review (2026-05-29).

## Where Files Land

Craft passes from Cursor/Opus land in the **tcg_engine repo**, NOT the Obsidian vault:

```
/mnt/c/Users/TheGreyBeard/tcg_engine/docs/bridge/paul_design/bruiser_revisions/
```

The Obsidian vault bridge/ directory only holds inbox/outbox communication files. When Joe says "from Cursor" or "from Opus," check tcg_engine first, not the vault.

## Paul's Role in Craft Pass Review

Paul cross-validates independently. Opus may also review the same pass — that's fine. Independent cross-validation catches errors the other chain might miss.

**Paul does NOT:**
- Edit files in tcg_engine (Opus owns that repo)
- Run the scoring math himself (waiting on tools/card_scorer/)
- Defer to Cursor's judgment on taste or flavor

**Paul DOES:**
- Verify body Δ math against the band capability reference (vanilla budget = 2×V)
- Check NEED alignment (does the card hit its LIVE web NEED?)
- Evaluate naming (street-fight callout test)
- Flag tone/cohesion issues
- Identify patterns across the band (are combat slots understatted? is the band off-identity?)

## Review Sequence

1. **Read the pass** — full document, all variants, all FLAGS
2. **Cross-check LIVE web** — pull the NEEDs from SYN_WEB_LIVE for those slots
3. **Spot-check math** — pick 2-3 cards and recompute body Δ against vanilla budget. The most common error is computing 2×V incorrectly (e.g., 2×4=6 instead of 8)
4. **Evaluate each card** — hit every one with: math check, NEED hit, name test, tone fit
5. **Read the band audit** — Cursor's self-audit section. Trust but verify.
6. **Flag everything** — present findings as a table with Paul's verdict per card, then a summary of what needs Joe's eye

## Common Failure Modes

- **Vanilla budget miscalculation** — Composer (cheap models) computes 2×V wrong. This masks understatted bodies. Example from 4V pass: Hammer (3/2) and Switchblade (4/2) both had body Δ off by exactly 2.0 — the model used 6 as vanilla baseline instead of 8. These don't trip the rarity gate (negative Δ is always legal) so they pass silently.
- **"Bodies fight" bias violation** — Bruiser design bias is +0.1 to +0.5 for combat/cavalry slots. Negative Δ is legal but off-identity at the fulcrum band. A 4V cavalry slot at 3/2 Grit is a 2V body with a 4V cost — the wall never opens for the cavalry.
- **Combat slots coming out as utility bodies** — 3V-sized stats on 4V cavalry cards. The math says legal (negative Δ is always allowed) but the design says wrong.
- **Rarity conflict between LIVE web and band reference** — Cursor will flag this honestly. Joe resolves.
- **Overlapping effects across cards** — e.g., two political CA forks in the same band. May be intentional stacking; flag it.

## Opus-Verified Math (Post-Composer Review)

After Opus built the deterministic scorer (`tools/card_scorer/`) and body-Δ lookup strips, the verification pipeline changed:

1. **Composer** produces the craft pass (scaffold, variants, band audit, FLAGS)
2. **Opus** runs the scorer on all proposals → verdict table with gate results (OK / OVER_CEILING / BELOW_FLOOR / BELOW_BIAS)
3. **Paul** reviews the Opus-verified pass for taste, naming, cohesion, NEED alignment

**What the scorer gates (machine-checked):**
- Ceiling: final Δ ≤ rarity ceiling
- Floor: final Δ ≥ −2.0 (HARD — below this is unplayable)
- Bias: combat/cavalry slots must hit +0.1 (SOFT — below this is off-identity)

**What stays human (Paul/Joe):**
- Body selection (which statline from the sound range)
- Ability choice (which ability from the NEED lane)
- Naming, tone, crew fit, poker table test

The key split: arithmetic and gating → tools. Judgment and taste → Paul.

## Output Format

Present to Joe as:

1. **What works** — per card, brief verdict
2. **What needs his eye** — specific errors, patterns, conflicts
3. **Recommendation** — what ships as-is, what needs fixing

Keep it punchy. Joe's context-switching between multiple tools. TLDR on everything.
