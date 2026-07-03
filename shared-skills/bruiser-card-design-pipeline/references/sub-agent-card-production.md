# Sub-Agent Card Production Pipeline

Proven end-to-end workflow for producing a 55-card faction set using parallel sub-agents. Validated on Trigger faction (2026-06-08) — produced A- set in one session.

## Prompt Templates

### Validator Sub-Agent Prompt

```
Validate the [Faction] Sub-Agent Spec. Be ruthless. Find every contradiction, gap, missing constraint, or ambiguity that would let a sub-agent produce wrong cards.

Specifically check:
1. Internal consistency — crew budgets, rarity caps, V-band totals, mechanic density
2. Constraint gaps — what CAN a sub-agent do that they shouldn't?
3. Slot table audit — do rows add up to build facts totals?
4. Pathway coverage — every row serves ≥1 pathway?
5. Mechanic coverage — all functions (F01-F1X) have card expressions?
6. Crew bleed — Street with Paid, Help with card draw, Management with weapons?
7. Missing sections — what does a sub-agent need that isn't in the spec?

Return: prioritized issues with severity (blocking/major/minor) and specific fixes.
```

### Card Design Sub-Agent Prompt (per batch)

```
Design the [V-band range] cards for the [Faction] faction. Read the spec doc at [path] FIRST, then design every card in the batch list. Follow ALL design rules. WRITE OUTPUT TO FILE at [output_path]. Return complete cards with names, stats, rules text, pathway, edges, and flavor notes.
```

### Critic Sub-Agent Prompt

```
Critically review the [Faction] v[N] 55-card set using the faction-set-review Pass 2 (Mechanical) and Pass 3 (Polish) checklists. Load the card set, the review skill, and the spec. Return graded findings with specific fixes. Be ruthless — a 75 is better than a padded 90. Target B+ or higher to ship.
```

## pre_review_audit.py Format Compatibility (PERMANENT FIX)

**Do NOT patch the script.** Patch the SPEC to enforce exact format. Three iterations
of Trigger card design failed on format drift (2026-06-08). The permanent fix:

Add this to every SubAgent Spec's Output Format section:

```
### Output Format (MANDATORY — EXACT FORMAT REQUIRED)

Section headers MUST be exactly: ## Minions, ## Spells, ## Ambushes, ## Weapons

Minion:  | # | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |
Spell:   | S# | V | R | Crew | Name | Text | Pathway | Edges |
Ambush:  | A# | V | R | Name | Trigger | Text | Edges |
Weapon:  | W# | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |

Rules:
1. Exact column order. Same pipe count. No bold/italics in cells.
2. Crew: P/St/M/H or —. Pathway: C/W/O/X or —. Partners: card name or —.
3. Flavor prose AFTER the table, not inside it.
4. Verify with grep before declaring done:
   grep -c '^| [0-9]' <file>   # minions
   grep -c '^| S' <file>         # spells
   grep -c '^| A' <file>         # ambushes
   grep -c '^| W' <file>         # weapons
```

**Failure mode without this:** Workers produce 3 different formats (`·`-separated, swapped
R/Crew columns, missing Pathway/Partners columns). Script returns zero cards found.
Assembly scripts break. Three iterations wasted on format conversion. Enforce format
at spec time — never convert after the fact.

The old advice to "patch parse_card_table()" is wrong. It masks the problem instead
of solving it. Enforce the format, don't adapt to the drift.

## Kaizen Notes

- Sub-agents return summaries by default — explicitly instruct to write files
- execute_code `read_file()` returns content with line number prefixes — strip before writing
- Session-scoped execute_code consent — fire one early to unlock
- Three V-band batches work well — 1V-2V, 3V-4V, 5V-6V+weapons
- The audit→fix→re-audit loop is fast when issues are surgical

## Cross-Cutting Gaps + Fixer Pass (PERMANENT FIX)

When 3 sub-agents design cards by V-band tier, no single worker owns cross-cutting
concerns. A band that assumes another band covers removal produces a set with zero
removal. Proven on Trigger 2026-06-08: iter-3 had zero common removal, zero healing,
and thin edge E13 until the fixer pass.

**Fixer pass pattern (mandatory after assembly, before critic):**

```
Goal: Fix the pre-review audit gaps in the assembled set. Do NOT redesign existing cards. Fill gaps only.

Context:
- Assembled set at {assembled_path}
- Pre-review audit output: {audit_output}
- Spec at {spec_path}

Only fix the specific gaps listed. Add cards, demote rarities, rename conflicts.
Do NOT touch cards that pass. Zero redesigns. Output a fix-patch.md.
```

After the fixer returns, apply the patches and re-run pre_review_audit.py.
If CLEAN, proceed to critic. If still FAIL but with fewer issues, run fixer
one more time. If 2 fixer passes don't clear the gate, escalate.

**What the fixer handles:**
- Missing common removal spells (add 1-2)
- Missing healing cards (add 1-2 through Paid)
- Naming conflicts with keywords (rename the card)
- Thin edges (add 1-2 cards with the edge)
- Rarity overflows (demote R→U)
- Count mismatches (add/remove as needed)

**What the fixer does NOT do:**
- Redesign existing cards
- Change crew assignments
- Alter core mechanics
- Touch cards that pass audit
