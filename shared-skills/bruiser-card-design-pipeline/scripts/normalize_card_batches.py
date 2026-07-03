#!/usr/bin/env python3
"""
Normalize card batch outputs from mixed sub-agent formats into a single
pre_review_audit.py-compatible format.

Handles three input formats:
  1. ·-separated:  C · 1V · Name · Crew · Stats · Text · Edges
  2. Pipe v1:      | # | V | Name | R | Crew | ATK/HP | Text | Edge |
  3. Pipe v2:      | # | V | Name | R | Cw | ATK/HP | Text | Edge |

Output format (pre_review_audit.py expected):
  Minions:  | # | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |
  Spells:   | S# | V | R | Crew | Name | Text | Pathway | Edges |
  Ambushes: | A# | V | R | Name | Trigger | Text | Edges |
  Weapons:  | W# | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |

Usage: python3 normalize_card_batches.py batch-1V-2V.md batch-3V-4V.md batch-5V-6V.md > assembled.md
"""

import re, sys

minions, spells, ambushes, weapons = [], [], [], []

for fname in sys.argv[1:]:
    with open(fname) as f:
        text = f.read()

    # --- · format ---
    for line in text.split("\n"):
        m = re.match(r'^([CURL])\s+·\s+(.+)$', line.strip())
        if not m: continue
        rarity = m.group(1)
        parts = [p.strip() for p in m.group(2).split("·")]
        cost, name = parts[0], parts[1]
        typ = parts[2]
        if typ == "Spell":
            spells.append({"cost":cost,"name":name,"rarity":rarity,"text":parts[3] if len(parts)>3 else "","edges":parts[4] if len(parts)>4 else ""})
        elif typ == "Ambush":
            ambushes.append({"cost":cost,"name":name,"rarity":rarity,"trigger":parts[3] if len(parts)>3 else "","text":parts[4] if len(parts)>4 else "","edges":parts[5] if len(parts)>5 else ""})
        elif typ == "Weapon":
            weapons.append({"cost":cost,"name":name,"rarity":rarity,"stats":parts[3] if len(parts)>3 else "","text":parts[4] if len(parts)>4 else "","edges":parts[5] if len(parts)>5 else ""})
        elif typ in ("P","St","M","H"):
            minions.append({"cost":cost,"name":name,"rarity":rarity,"crew":typ,"stats":parts[3] if len(parts)>3 else "","text":parts[4] if len(parts)>4 else "","edges":parts[5] if len(parts)>5 else ""})

    # --- Pipe table format ---
    for line in text.split("\n"):
        ls = line.strip()
        if not ls.startswith("|") or ls.startswith("|---"): continue
        # Skip headers
        if "Name" in ls and ("ATK/HP" in ls or "Text" in ls): continue
        cells = [c.strip().rstrip('*') for c in ls.split("|") if c.strip()]
        if not cells or not cells[0].isdigit(): continue
        if "Initial batch" in " ".join(cells): continue

        cost, name = cells[1], cells[2]
        rarity = cells[3]

        # Minions: 8+ cells with crew code at [4]
        if len(cells) >= 8:
            minions.append({"cost":cost,"name":name,"rarity":rarity,"crew":cells[4],"stats":cells[5],"text":cells[6],"edges":cells[7] if len(cells)>7 else ""})
        # Weapons: stats at [4] (contains /)
        elif len(cells) >= 6 and '/' in cells[4] and re.match(r'^\d+/\d+$', cells[4].replace('*','')):
            weapons.append({"cost":cost,"name":name,"rarity":rarity,"stats":cells[4],"text":cells[5],"edges":cells[6] if len(cells)>6 else ""})
        # Ambushes: trigger text at [4]
        elif len(cells) >= 6 and any(kw in cells[4].lower() for kw in ['attack','played','summon','damage','die','death','spell','hero','turn','enemy','opponent']):
            ambushes.append({"cost":cost,"name":name,"rarity":rarity,"trigger":cells[4],"text":cells[5],"edges":cells[6] if len(cells)>6 else ""})
        # Spells: everything else
        elif len(cells) >= 5:
            spells.append({"cost":cost,"name":name,"rarity":rarity,"text":cells[4],"edges":cells[5] if len(cells)>5 else ""})

# ── Output ──
print("# Trigger Card Set — Assembled")
print("**Pipeline:** trigger-card-design\n")
print("## Minions")
print("| # | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |")
print("|---|---|---|---|---|---|---|---|---|---|")
for i, c in enumerate(minions, 1):
    print(f"| {i} | {c['cost']} | {c['rarity']} | {c['crew']} | {c['name']} | {c['stats']} | {c['text']} | — | {c['edges']} | — |")

print("\n## Spells")
print("| S# | V | R | Crew | Name | Text | Pathway | Edges |")
print("|---|---|---|---|---|---|---|---|")
for i, c in enumerate(spells, 1):
    print(f"| S{i} | {c['cost']} | {c['rarity']} | — | {c['name']} | {c['text']} | — | {c['edges']} |")

print("\n## Ambushes")
print("| A# | V | R | Name | Trigger | Text | Edges |")
print("|---|---|---|---|---|---|---|")
for i, c in enumerate(ambushes, 1):
    print(f"| A{i} | {c['cost']} | {c['rarity']} | {c['name']} | {c.get('trigger','')} | {c['text']} | {c['edges']} |")

print("\n## Weapons")
print("| W# | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners |")
print("|---|---|---|---|---|---|---|---|---|---|")
for i, c in enumerate(weapons, 1):
    print(f"| W{i} | {c['cost']} | {c['rarity']} | — | {c['name']} | {c['stats']} | {c['text']} | — | {c['edges']} | — |")
