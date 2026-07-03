# pre_review_audit.py — Exact Format Requirements

The script at `scripts/pre_review_audit.py` parses pipe-delimited markdown tables
with specific column order. Any deviation returns zero cards found.

## Section Headers

Section headers MUST be exactly:
- `## Minions`
- `## Spells`
- `## Ambushes`
- `## Weapons`

The script finds tables by matching these headers. Tables under any other header
(e.g., `## PHASE 1: Functions Pass`, `## Competitive Slotting`) are ignored.

## Column Order (DO NOT REORDER)

**Minions:**
```
| # | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |
```
Script reads: col[0]=#, col[1]=V, col[2]=R, col[3]=Crew, col[4]=Name, col[5]=Stats, col[6]=Text, col[7]=Pathway, col[8]=Edges, col[9]=Partners

**Spells:**
```
| S# | V | R | Crew | Name | Text | Pathway | Edges |
```
Script reads: col[0]=S#, col[1]=V, col[2]=R, col[3]=Crew, col[4]=Name, col[5]=Text, col[6]=Pathway, col[7]=Edges

**Ambushes:**
```
| A# | V | R | Name | Trigger | Text | Edges |
```
Script reads: col[0]=A#, col[1]=V, col[2]=R, col[3]=Name, col[4]=Trigger, col[5]=Text, col[6]=Edges

**Weapons:**
```
| W# | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |
```
Same column indices as minions.

## Cell Values

- Rarity: C, U, R, L (single letter)
- Crew: P, St, M, H (single letter or two-letter code). Use `—` if no crew.
- Pathway: C, W, O, X. Use `—` if none.
- Partners: card name or `—`
- No bold (`**`), no italics (`*`), no markdown in cells

## Common Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Zero cards found | Column order doesn't match script expectations | Use the exact templates above |
| Wrong card type counts | Section headers don't match (`### Minions` vs `## Minions`) | Use `## ` not `### ` |
| Minions classified as spells | Crew column missing or in wrong position | Crew must be col[3] for minions |
| Rarity counts wrong | Rarity column in wrong position (e.g., swapped with Name) | Rarity must be col[2] for minions/spells |

## Keyword Sidebar

Must be under `## Keyword Sidebar` section header, using pipe table format:
```
| Keyword | Definition |
```
The script regex-matches `| **Keyword** | Definition |` or `| Keyword | Definition |`.
