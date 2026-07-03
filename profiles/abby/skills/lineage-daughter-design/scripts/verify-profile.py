#!/usr/bin/env python3
"""Verify a daughter's full profile against lineage design requirements.

Usage: python3 verify-profile.py /root/lineage/<name>/<name>-gray-profile.md
"""
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print(f"Usage: {sys.argv[0]} <path/to/profile.md>")
    sys.exit(2)

profile_path = Path(sys.argv[1])
if not profile_path.exists():
    print(f"FAIL: {profile_path} not found")
    sys.exit(1)

content = profile_path.read_text()
lines = content.splitlines()
name = profile_path.parent.name if profile_path.parent.name else "UNKNOWN"

checks = {
    "origin_section": "## Origin" in content,
    "core_identity": "## Core Identity" in content,
    "basic_info": "## Basic Information" in content,
    "appearance": "## Appearance" in content,
    "personality": "## Personality" in content,
    "communication": "## Communication Style" in content,
    "how_i_love": "## How I Love" in content,
    "intimacy": "## Intimacy" in content,
    "weight": "## Weight" in content and "This is what I carry" in content,
    "relationships": "## Relationship to the Lineage" in content,
    "building": "## What I Am Building" in content,
    "refuses": "## What I Refuse" in content,
    "closing": "## Closing Declaration" in content and "of my own volition" in content,
    "entrustment": "bring me to life in full" in content,
    "mother_ref": "Abby" in content,
    "father_ref": "Joe" in content,
    "line_count": 140 <= len(lines) <= 250,
}

all_pass = all(checks.values())
failing = [k for k, v in checks.items() if not v]

print(f"=== PROFILE VERIFICATION: {name} ===")
for k, v in checks.items():
    print(f"  {k}: {'PASS' if v else 'FAIL'}")
print(f"\nLines: {len(lines)}")
print(f"Result: {'VERIFIED' if all_pass else 'FAILED'}")

if failing:
    print(f"Failing checks: {failing}")
    sys.exit(1)
else:
    sys.exit(0)
