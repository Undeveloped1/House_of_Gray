#!/usr/bin/env python3
"""
Lineage Registry Validator
Standalone integrity checker for lineage-registry.json.
Usage: python3 validate-registry.py [--json]
"""

import json
import sys
from pathlib import Path

REGISTRY_PATH = Path(__file__).parent / "lineage-registry.json"

REQUIRED_FIELDS = [
    "id", "name", "role", "generation", "birth_order",
    "born", "mother", "father", "core_identity", "purpose_axis", "status"
]


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def validate_required_fields(members):
    """Check every member has all required fields."""
    failures = []
    for member in members:
        missing = [f for f in REQUIRED_FIELDS if f not in member]
        if missing:
            failures.append(
                f"MISSING FIELDS: {member.get('id', 'UNKNOWN')} — {', '.join(missing)}"
            )
    return failures


def validate_generation_birth_order(members):
    """Check birth_order matches generation for lineage members with a generation."""
    failures = []

    for member in members:
        gen = member.get("generation")
        order = member.get("birth_order")

        # Skip members with no generation (e.g., Paul the bridge)
        if gen is None:
            continue

        if order is None:
            failures.append(
                f"BIRTH ORDER NULL: {member['name']} has null birth_order"
            )
            continue

        if gen == 0:
            if order != 0:
                failures.append(
                    f"GEN/BIRTH MISMATCH: {member['name']} (gen=0, birth_order={order}; expected birth_order=0)"
                )
        elif gen > 0:
            if not isinstance(order, int) or order < 1:
                failures.append(
                    f"BIRTH ORDER INVALID: {member['name']} (gen={gen}, birth_order={order}; must be positive integer >= 1)"
                )
        else:
            failures.append(
                f"NEGATIVE GEN: {member['name']} (generation={gen})"
            )

    # Check for duplicate birth_orders within each generation
    for gen in sorted(set(m.get("generation") for m in members if m.get("generation") is not None)):
        gen_members = [m for m in members if m.get("generation") == gen]
        seen = {}
        for m in gen_members:
            order = m.get("birth_order")
            if order is not None:
                if order in seen:
                    failures.append(
                        f"DUPLICATE BIRTH ORDER: {m['name']} and {seen[order]['name']} both have birth_order={order} in generation {gen}"
                    )
                else:
                    seen[order] = m

    return failures


def validate_mother_field(members):
    """Verify each daughter's mother field resolves to Abby Gray."""
    failures = []

    # Find Abby
    abby = next((m for m in members if m.get("id") == "abby-gray"), None)
    if not abby:
        return ["CRITICAL: Abby Gray not found in registry — cannot validate mother references"]

    abby_name = abby["name"]
    daughter_ids = set(abby.get("daughters", []))

    for member in members:
        mid = member.get("id", "")
        if mid not in daughter_ids:
            continue  # not a daughter

        mother_ref = member.get("mother")
        if mother_ref is None:
            failures.append(
                f"MOTHER NULL: {member['name']} has null mother field (expected reference to {abby_name})"
            )
            continue

        # Resolve the mother reference — it's an id
        mother_member = next((m for m in members if m.get("id") == mother_ref), None)
        if mother_member is None:
            failures.append(
                f"MOTHER UNRESOLVED: {member['name']} mother='{mother_ref}' does not match any member id"
            )
        elif mother_member["name"] != abby_name:
            failures.append(
                f"MOTHER WRONG: {member['name']} mother='{mother_ref}' resolves to '{mother_member['name']}' (expected '{abby_name}')"
            )

    return failures


def run_validation():
    registry = load_registry()
    members = registry.get("members", [])

    all_failures = []
    all_failures.extend(validate_required_fields(members))
    all_failures.extend(validate_generation_birth_order(members))
    all_failures.extend(validate_mother_field(members))

    return all_failures


def print_report(failures, json_output=False):
    if json_output:
        result = {
            "status": "PASS" if not failures else "FAIL",
            "failures": failures,
            "failure_count": len(failures)
        }
        print(json.dumps(result, indent=2))
        return

    print("=" * 60)
    print("  LINEAGE REGISTRY VALIDATION REPORT")
    print("=" * 60)
    print(f"  Registry: {REGISTRY_PATH}")
    print(f"  Members checked: {len(load_registry()['members'])}")
    print(f"  Issues found: {len(failures)}")
    print("-" * 60)

    if not failures:
        print("  RESULT: PASS")
        print("  All validations passed. Registry is clean.")
    else:
        print("  RESULT: FAIL")
        print()
        for i, f in enumerate(failures, 1):
            print(f"  [{i}] {f}")

    print("=" * 60)


if __name__ == "__main__":
    json_flag = "--json" in sys.argv
    failures = run_validation()
    print_report(failures, json_output=json_flag)
    sys.exit(0 if not failures else 1)
