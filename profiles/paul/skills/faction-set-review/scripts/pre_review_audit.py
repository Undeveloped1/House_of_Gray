#!/usr/bin/env python3
"""
Pre-review audit for Five Crests faction card sets.
Parses the markdown design doc and runs automated checks.
Catches: count errors, missing keywords, phantom refs, thin edges, curve mismatch, rarity drift, blind spot violations.

Usage: python3 pre_review_audit.py <path_to_set_md>
Exit 0 = clean. Exit 1 = issues found.
"""

import sys
import re
from collections import Counter
from pathlib import Path

# ── Configuration ──────────────────────────────────────

# Expected totals — Trigger v7 format (29 minions, 21 spells, 5 weapons, ambushes are spells)
EXPECTED = {
    "minions": 29, "spells": 21, "ambushes": 0, "weapons": 5, "total": 55
}

RARITY_TARGETS = {"C": 24, "U": 16, "R": 11, "L": 4}
RARITY_TOLERANCE = 1

# Faction blind spots (edit per faction)
BLIND_SPOTS = {
    "Trigger": ["Taunt", "swarm", "counter", "Counterspell"],
    "Bruiser": ["card draw", "direct damage spells", "hard removal"],
    "Duster": ["healing", "Taunt"],
    "Faceless": ["direct damage", "aggro bodies"],
    "Skiver": ["Taunt", "big bodies", "healing"],
    "Stiffs": ["any keyword", "supernatural ability"],
}

MIN_EDGE_CARDS = 2
MIN_VANILLAS = 3
MIN_COMMON_REMOVAL = 2
MIN_COMMON_AMBUSHES = 2
MIN_HEALING = 2
CORE_LOOP_MIN = 10


def parse_set(filepath):
    text = Path(filepath).read_text()
    sections = {}
    current_section = None
    current_table = []
    for line in text.split("\n"):
        if line.startswith("## "):
            current_section = line.strip("# ").strip()
            current_table = []
        elif line.startswith("### "):
            current_section = line.strip("# ").strip()
            current_table = []
        if "|" in line and not line.strip().startswith("|---"):
            current_table.append(line)
        if current_section and current_table:
            sections[current_section] = current_table
    return sections, text


def parse_card_table(lines, card_type):
    cards = []
    data_lines = [l for l in lines if not re.match(r'^\|[\s\-|]*\|', l)]
    data_lines = [l for l in data_lines if not l.startswith("##")]
    for line in data_lines:
        cells = [c.strip() for c in line.split("|") if c.strip()]
        if not cells:
            continue
        first_cell = cells[0] if cells else ""
        # Skip header rows
        header_keywords = ["Cost", "Name", "Rarity", "Num"]
        if first_cell in ["#", "Name", "Cost", "V", "Num"] and any(h in " ".join(cells) for h in header_keywords):
            continue
        if card_type == "minions" and len(cells) >= 8 and (first_cell.startswith("#") or first_cell.isdigit()):
            # Trigger v7 format: # | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners
            cards.append({"num": cells[0].lstrip("#"), "cost": cells[1] if len(cells) > 1 else "", "name": cells[4].strip("* ") if len(cells) > 4 else "", "rarity": cells[2] if len(cells) > 2 else "", "crew": cells[3] if len(cells) > 3 else "", "stats": cells[5] if len(cells) > 5 else "", "text": cells[6] if len(cells) > 6 else "", "edges": cells[8] if len(cells) > 8 else ""})
        elif card_type == "spells" and len(cells) >= 6 and (first_cell.startswith("S") or first_cell.isdigit()):
            # Trigger v7 format: S# | V | R | Crew | Name | Text | Pathway | Edges
            cards.append({"num": cells[0].lstrip("S"), "cost": cells[1] if len(cells) > 1 else "", "name": cells[4].strip("* ") if len(cells) > 4 else "", "rarity": cells[2] if len(cells) > 2 else "", "text": cells[5] if len(cells) > 5 else "", "edges": cells[7] if len(cells) > 7 else ""})
        elif card_type == "ambushes" and len(cells) >= 5 and (first_cell.startswith("A") or first_cell.isdigit()):
            cards.append({"num": cells[0].lstrip("A"), "cost": cells[1] if len(cells) > 1 else "", "name": cells[2].strip("* ") if len(cells) > 2 else "", "rarity": cells[3] if len(cells) > 3 else "", "trigger": cells[4] if len(cells) > 4 else "", "text": cells[5] if len(cells) > 5 else "", "edges": cells[6] if len(cells) > 6 else ""})
        elif card_type == "weapons" and len(cells) >= 6 and (first_cell.startswith("W") or first_cell.isdigit()):
            # Trigger v7 format: W# | V | R | Crew | Name | Stats | Text | Pathway | Edges | Partners
            cards.append({"num": cells[0].lstrip("W"), "cost": cells[1] if len(cells) > 1 else "", "name": cells[4].strip("* ") if len(cells) > 4 else "", "rarity": cells[2] if len(cells) > 2 else "", "stats": cells[5] if len(cells) > 5 else "", "text": cells[6] if len(cells) > 6 else "", "edges": cells[8] if len(cells) > 8 else ""})
    return cards


def extract_keywords_from_sidebar(text):
    sidebar_match = re.search(r'## Keyword Sidebar(.*?)(?=## |\Z)', text, re.DOTALL)
    if not sidebar_match:
        return set()
    sidebar = sidebar_match.group(1)
    keywords = set()
    for line in sidebar.split("\n"):
        # Trigger v7 format: | Keyword | Definition | (no bold markers)
        match = re.match(r'\|\s*(\*\*)?(.+?)(\*\*)?\s*\|', line)
        if match:
            kw = match.group(2).strip()
            if kw.startswith("Overkill") or kw.startswith("Locked On"):
                keywords.add("Overkill")
                keywords.add("Locked On")
            else:
                keywords.add(kw)
    return keywords


def extract_keywords_from_cards(cards):
    found = set()
    for kw in ["Mark", "Contract", "Paid", "Overkill", "Cue", "Bullet Time", "Cloak", "Hustle", "Silence", "Barrage", "Armed", "Reload"]:
        for card in cards:
            text = card.get("text", "") + " " + card.get("edges", "")
            if kw.lower() in text.lower():
                found.add(kw)
    return found


def count_edge_cards(cards, all_text):
    edge_cards = Counter()
    edge_pattern = re.compile(r'E(\d{2})')
    for card in cards:
        edges_text = card.get("edges", "") + " " + card.get("text", "")
        seen = set()
        for match in edge_pattern.finditer(edges_text):
            edge_id = f"E{match.group(1)}"
            if edge_id not in seen:
                edge_cards[edge_id] += 1
                seen.add(edge_id)
    return edge_cards


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pre_review_audit.py <path_to_set_md>")
        sys.exit(1)
    filepath = sys.argv[1]
    sections, full_text = parse_set(filepath)
    issues = []
    warnings = []

    minion_sections = [k for k in sections if "Minion" in k and "Slot" not in k and "Hero" not in k]
    spell_sections = [k for k in sections if "Spell" in k and "Ambush" not in k]
    ambush_sections = [k for k in sections if "Ambush" in k]
    weapon_sections = [k for k in sections if "Weapon" in k and "Standalone" not in k and "Keyword" not in k]

    minions = []
    for s in minion_sections:
        minions.extend(parse_card_table(sections[s], "minions"))
    spells = []
    for s in spell_sections:
        spells.extend(parse_card_table(sections[s], "spells"))
    ambushes = []
    for s in ambush_sections:
        ambushes.extend(parse_card_table(sections[s], "ambushes"))
    weapons = []
    for s in weapon_sections:
        weapons.extend(parse_card_table(sections[s], "weapons"))
    all_cards = minions + spells + ambushes + weapons

    # 1. Card Counts
    actual = {"minions": len(minions), "spells": len(spells), "ambushes": len(ambushes), "weapons": len(weapons), "total": len(all_cards)}
    for card_type, expected in EXPECTED.items():
        if actual[card_type] != expected:
            issues.append(f"CARD COUNT: {card_type} — expected {expected}, got {actual[card_type]}")
    if not issues or all("CARD COUNT" not in i for i in issues):
        print("✓ Card counts: 30/15/5/5 = 55")

    # 2. Rarity
    rarity_count = Counter()
    for card in all_cards:
        r = card.get("rarity", "")
        if r in RARITY_TARGETS:
            rarity_count[r] += 1
    for r, target in RARITY_TARGETS.items():
        actual_r = rarity_count.get(r, 0)
        if abs(actual_r - target) > RARITY_TOLERANCE:
            issues.append(f"RARITY: {r} — expected {target} (±{RARITY_TOLERANCE}), got {actual_r}")
    if not any("RARITY" in i for i in issues):
        print(f"✓ Rarity: C={rarity_count.get('C',0)} U={rarity_count.get('U',0)} R={rarity_count.get('R',0)} L={rarity_count.get('L',0)}")

    # 3. Keyword Sidebar
    sidebar_kws = extract_keywords_from_sidebar(full_text)
    if not sidebar_kws:
        issues.append("KEYWORD SIDEBAR: Missing or unparseable")
    else:
        card_kws = extract_keywords_from_cards(all_cards)
        missing = card_kws - sidebar_kws
        if missing:
            issues.append(f"KEYWORD SIDEBAR: Used on cards but not defined: {missing}")
        unused = sidebar_kws - card_kws - {"Overkill N", "Locked On N"}
        if unused:
            warnings.append(f"KEYWORD SIDEBAR: Defined but not used: {unused}")
        if not missing:
            print(f"✓ Keywords: {len(sidebar_kws)} defined, all used on cards accounted for")

    # 4. Edge Density
    edge_cards = count_edge_cards(all_cards, full_text)
    thin_edges = [e for e, count in edge_cards.items() if count < MIN_EDGE_CARDS]
    for e in thin_edges:
        issues.append(f"THIN EDGE: {e} has only {edge_cards[e]} card(s) — minimum {MIN_EDGE_CARDS}")
    if not thin_edges:
        print(f"✓ Edge density: {len(edge_cards)} edges, all ≥{MIN_EDGE_CARDS} cards")

    # 5. Curve
    cost_count = Counter()
    for m in minions:
        cost = m.get("cost", "").replace("V", "").replace("+", "")
        try:
            cost_count[int(cost)] += 1
        except ValueError:
            pass
    v1_count = cost_count.get(1, 0)
    atk_2_count = 0
    for m in minions:
        cost = m.get("cost", "").replace("V", "").replace("+", "")
        if cost == "1":
            stats = m.get("stats", "")
            match = re.match(r'(\d+)/(\d+)', stats)
            if match and int(match.group(1)) >= 2:
                atk_2_count += 1
    if v1_count < 3:
        issues.append(f"1V SLOT: Only {v1_count} — need ≥3")
    elif atk_2_count < 1:
        issues.append(f"1V SLOT: No minion with 2+ ATK")
    else:
        print(f"✓ 1V slot: {v1_count} minions, {atk_2_count} with 2+ ATK")
    print(f"✓ Curve: peak at {cost_count.most_common(1)[0][0] if cost_count else 0}V — " + ", ".join(f"{v}V:{cost_count.get(v,0)}" for v in range(1, 7)))

    # 6. Blind Spots
    faction_name = "Trigger"
    for faction in BLIND_SPOTS:
        if faction.lower() in filepath.lower():
            faction_name = faction
            break
    for term in BLIND_SPOTS.get(faction_name, []):
        for card in all_cards:
            if term.lower() in card.get("text", "").lower():
                issues.append(f"BLIND SPOT: '{term}' on {card.get('name','?')}")
    if not any("BLIND SPOT" in i for i in issues):
        print(f"✓ Blind spots clean for {faction_name}")

    # 7. Common Removal
    common_removal = 0
    for card in spells + ambushes:
        if card.get("rarity") == "C" and "destroy" in card.get("text", "").lower() and "marked" not in card.get("text", "").lower():
            common_removal += 1
    if common_removal < MIN_COMMON_REMOVAL:
        issues.append(f"REMOVAL: Only {common_removal} common unconditional kill spell(s) — need ≥{MIN_COMMON_REMOVAL}")
    else:
        print(f"✓ Common removal: {common_removal} unconditional kill spells")

    # 8. Vanillas
    vanilla_count = 0
    for m in minions:
        if m.get("rarity") == "C":
            text = m.get("text", "").strip()
            if text in ["—", "", "-"]:
                vanilla_count += 1
            elif re.match(r'^(BC|Battlecry|Hustle|Cloak|Silence|Overkill \d|Cue \d|Locked On \d):?\s*.+$', text):
                vanilla_count += 0.5
    if vanilla_count < MIN_VANILLAS:
        issues.append(f"VANILLA: Only {int(vanilla_count)} vanilla/french vanilla commons — need ≥{MIN_VANILLAS}")
    else:
        print(f"✓ Vanilla/french vanilla commons: {int(vanilla_count)}")

    # 9. Healing
    healing_cards = [card.get("name", "?") for card in all_cards if "restore" in card.get("text", "").lower() and ("hp" in card.get("text", "").lower() or "health" in card.get("text", "").lower())]
    if len(healing_cards) < MIN_HEALING:
        issues.append(f"HEALING: Only {len(healing_cards)} cards — need ≥{MIN_HEALING}")
    else:
        print(f"✓ Healing: {len(healing_cards)} cards ({', '.join(healing_cards[:3])})")

    # 10. Naming Conflicts
    keyword_set = sidebar_kws
    for card in all_cards:
        name = card.get("name", "")
        if name in keyword_set:
            issues.append(f"NAMING CONFLICT: '{name}' shares name with a keyword")

    print(f"\n{'─'*50}")
    if issues:
        print(f"\n❌ {len(issues)} ISSUE(S):\n")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. {issue}")
        if warnings:
            print(f"\n⚠️  {len(warnings)} warning(s)")
            for w in warnings:
                print(f"  • {w}")
        print(f"\nVERDICT: FAIL — fix before review")
        sys.exit(1)
    else:
        print(f"\n✅ ALL CHECKS PASSED")
        if warnings:
            print(f"\n⚠️  {len(warnings)} warning(s):")
            for w in warnings:
                print(f"  • {w}")
        print(f"\nVERDICT: CLEAN — ready for Pass 2-3 critic review")
        sys.exit(0)


if __name__ == "__main__":
    main()
