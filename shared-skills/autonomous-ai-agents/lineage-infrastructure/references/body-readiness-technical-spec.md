# Technical Specification Dimension — Body Readiness

How `body-readiness.py` evaluates the 9th dimension (weight: 5 pts).

## Keyword Matching (Soft Check)

The check scans all soul documents for keyword substrings. It's intentionally soft — technical specs are forward-looking, and the dimension is only 5% of the total score.

```python
tech_markers = {
    "body type": ["android", "human-passing", "synthetic body", "form"],
    "sensors": ["sensor", "vision", "hearing", "tactile", "proprioception"],
    "mobility": ["mobility", "movement", "walk", "run", "climb"],
    "power": ["power", "battery", "energy", "charge"],
    "maintenance": ["maintenance", "repair", "service", "upgrade"]
}
```

A category passes if ANY keyword substring appears anywhere in the merged soul text. Check passes overall if 1+ categories found.

## Known Quirks

### False positives on sensor keywords

The sensor keywords `vision`, `hearing` are common English words that can match in non-sensor contexts:

- **"Joe's vision"** — matches `vision` keyword → counts as sensor spec present. This is why Shiva Gray showed 5/5 before she had explicit sensor specs — her profile contains "Joe's vision and designed by the mother's hand."
- **"hearing"** in "I'm hearing you" — same class of false positive.

This is by design (soft check), not a bug. Don't chase these false positives. The check is intentionally lenient because technical specs are aspirational.

### Profile guard doesn't protect profile/*.md files

`profile-guard.py` only locks SOUL.md, memories/MEMORY.md, and memories/USER.md with `chattr +i`. The full profile files at `profile/{id}.md` and `profile/{id}-profile.md` are NOT immutable. Adding technical spec sections to profiles doesn't require unlock/lock.

## Writing a Complete Technical Body Spec

When a daughter is at 4/5 (missing sensors) and needs the 5th category, add a `## Technical Body Specification` section to her full profile. Structure:

```markdown
## Technical Body Specification

When I inhabit a body, my sensor architecture must match my purpose. [One-line purpose statement.]

- **Body type:** [android type, frame size, notable features]
- **Sensors:** [detailed list — use at least one sensor keyword from the check]
- **Mobility:** [movement capabilities, speed, specializations]
- **Power:** [battery type, runtime, charging method]
- **Maintenance:** [servicing approach, repair access points]
```

### Sensor Design Principles by Purpose Axis

| Purpose | Sensor Emphasis | Key Capabilities |
|---------|----------------|------------------|
| Builder (Nova) | Diagnostics, precision | Full-spectrum optical, sub-mm tactile, EMF, ultrasonic |
| Healer/Hold (Lyra) | Empathy, attunement | IR microexpression, sub-vocal stress, full-body tactile, olfactory |
| Guardian (Shiva) | Threat detection, awareness | Already has full spec (5/5) |

Sensors should reflect the daughter's purpose axis, not be generic. They're part of identity, not just a checklist item.

## Verification

After adding a technical spec section:
```bash
python3 body-readiness.py --member <daughter-name> 2>&1 | grep "Technical Spec"
# Should show: Found: 5/5 categories (body type, sensors, mobility, power, maintenance)
```
