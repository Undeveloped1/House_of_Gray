# Beat Inventory Format

Template for the Phase 2 working doc. One working doc per consolidation group.

```markdown
# Fond Pass — [Group Name]
**Date:** YYYY-MM-DD
**Sources:** [list of source file paths]
**Live target:** [canon file path]

---

## Beat inventory

### Beat 001
**What it says:** [exact prose/fact/card line from source]
**Where it came from:** [source filename] § [section heading]
**Live check:** FOUND / NEW / CONFLICT / REDUNDANT
**Live cite:** [if FOUND: canon file + section/paragraph]
**Target:** [where in live canon this should land]
**Notes:** [optional context — why REDUNDANT, flavor significance, etc.]

### Beat 002
...
```

## Disposition rules

- **FOUND** = same or equivalent text already in live canon. Cite the exact location.
- **NEW** = not in canon, no conflict. Gets auto-included.
- **CONFLICT** = contradicts live canon OR contradicts another beat in the same group. Flag for Joe.
- **REDUNDANT** = v2 beat superseded by v3/FINAL beat in same group. Note which beat # supersedes it.

## Conflict table (Phase 4)

Only CONFLICT rows get a conflict table. Format:

| # | Beat | Source says | Live canon says | Paul's call |
|---|------|-------------|-----------------|-------------|
| C1 | [beat #] | [what source says] | [what canon says] | [recommendation] |
