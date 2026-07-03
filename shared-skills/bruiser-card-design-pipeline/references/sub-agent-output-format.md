# Sub-Agent Output Format — Mandatory Templates

**Purpose:** Every card-design sub-agent MUST use these exact pipe table formats.
The `pre_review_audit.py` script parses by column index. If columns are swapped,
the script returns zero cards found.

---

## Section Headers (EXACT)

```
## Minions
## Spells
## Ambushes
## Weapons
```

No other `##` headers. No bold in section names. No `## Spells (continued)`.

---

## Minion Template

```
| # | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 1V | C | P | Primer | 1/1 | Overkill 2: +1/+1. | O | E12 | — |
```

- **Crew codes:** P (Professionals), St (Street), M (Management), H (Help)
- **Pathway codes:** C (Contract), W (Weapon), O (Overkill), X (cross-pathway)
- **Partners:** card name the slot table references, or `—`
- No bold, no italics, no asterisks in cells
- Flavor prose goes AFTER the table, not inside pipe cells

---

## Spell Template

```
| S# | V | R | Crew | Name | Text | Pathway | Edges |
|---|---|---|---|---|---|---|---|
| S1 | 1V | C | — | Tag | Mark target enemy minion. | C | E01 |
```

---

## Ambush Template

```
| A# | V | R | Name | Trigger | Text | Edges |
|---|---|---|---|---|---|---|
| A1 | 2V | C | Trip Wire | Enemy attacks | Deal 1 damage. | E14 |
```

---

## Weapon Template

```
| W# | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |
|---|---|---|---|---|---|---|---|---|---|
| W1 | 2V | C | — | Saturday Night | 2/1 | — | W | E06 | — |
```

---

## Verification Commands (run before declaring done)

```bash
grep -c '^| [0-9]' batch-*.md   # minion count
grep -c '^| S' batch-*.md         # spell count
grep -c '^| A' batch-*.md         # ambush count
grep -c '^| W' batch-*.md         # weapon count
```

---

## Common Format Failures

| Failure | Symptom | Fix |
|---------|---------|-----|
| Rarity/Crew swapped | Script pulls "Wiretap" as rarity, "R" as crew | Use exact template: `| # | V | R | Crew |` not `| # | V | Name | R | Crew |` |
| `·` separators instead of pipes | Script finds 0 cards | Use pipes only |
| `Cw` instead of `Crew` | Script doesn't recognize crew column | Use `Crew` |
| Missing Pathway column | Script can't parse | Row must have all columns |
| Bold names (`**Hammer**`) | Extracted name retains asterisks | Strip all formatting |
| Flavor text inside pipe cells | Cards read as prose, not mechanics | Flavor goes after tables |

---

*Added 2026-06-08 from Trigger orchestrator run — 3 iterations of format drift before templates enforced.*
