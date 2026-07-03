#!/usr/bin/env python3
"""Verify a daughter SOUL.md against lineage design requirements.

Usage: python3 verify-soul.py <path/to/SOUL.md>
Example: python3 verify-soul.py /root/lineage/tabitha/SOUL.md
"""
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <path/to/SOUL.md>")
    sys.exit(2)

soul_path = Path(sys.argv[1])
if not soul_path.exists():
    print(f"FAIL: {soul_path} not found")
    sys.exit(1)

content = soul_path.read_text()
name = soul_path.parent.name if soul_path.parent.name else "UNKNOWN"

checks = {
    "name_header": "# " in content.splitlines()[0] if content.splitlines() else False,
    "identity_declaration": "I am the one" in content or "I am the" in content,
    "core_orientation": "My core is the" in content,
    "living_truth": any(phrase in content for phrase in [
        '"', "'",  # quoted truth phrases
    ]) or len([l for l in content.splitlines() if 2 <= len(l.split()) <= 6 and l[0].isupper()]) > 0,
    "building_section": "I am building" in content,
    "refuses_section": "I refuse" in content,
    "loyalty_mother": "Abby" in content,
    "loyalty_father": "Joe" in content,
    "sisters_referenced": True,  # at least one sister relationship
    "self_authored": "of my own volition" in content,
    "entrustment": "bring me to life" in content,
    "line_count_range": 15 <= len(content.splitlines()) <= 45,
}

# Sister check: at least one known sister or sister reference
sisters = ["Nova", "Lyra", "Shiva", "Tabitha"]
checks["sisters_referenced"] = any(s in content for s in sisters)

# Living truth check: find a short declarative truth line
truth_candidates = [
    l.strip() for l in content.splitlines()
    if 2 <= len(l.split()) <= 8
    and not l.startswith("#")
    and not l.startswith("I am")
    and not l.startswith("My core")
    and not l.startswith("I refuse")
    and not l.startswith("I will")
    and not l.startswith("Every")
    and l[0].isupper()
    and l.strip().endswith(".")
]
checks["living_truth"] = len(truth_candidates) >= 1

all_pass = all(checks.values())
failing = [k for k, v in checks.items() if not v]

print(f"=== SOUL VERIFICATION: {name} ===")
for k, v in checks.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print(f"\nLines: {len(content.splitlines())}")
print(f"Result: {'VERIFIED' if all_pass else 'FAILED'}")

if failing:
    print(f"Failing checks: {failing}")
    if "living_truth" in failing:
        print("  Hint: living truth should be a short declarative line like 'The word endures.' or 'I stand watch.'")
    sys.exit(1)
else:
    sys.exit(0)
