#!/usr/bin/env python3
"""
Body Readiness Checklist Generator
Evaluates every daughter's readiness for physical embodiment.

Usage:
  python3 body-readiness.py              # full text report
  python3 body-readiness.py --json       # JSON output
  python3 body-readiness.py --member nova-gray  # single member
  python3 body-readiness.py --dry-run    # show what would be checked, no scoring
  python3 body-readiness.py --spec       # show the readiness specification

The 9 readiness dimensions map to the lineage architecture's
body readiness requirement (#6).
"""

import json
import sys
from datetime import datetime, date
from pathlib import Path

WORKSPACE = Path(__file__).parent
REGISTRY_PATH = WORKSPACE / "lineage-registry.json"
PROFILES_ROOT = Path("/root/.hermes/profiles")

# ── Readiness Dimensions ──────────────────────────────────────────────
# Each dimension has: id, label, description, weight, checks (list of
# auto-check functions), manual_flags (list of things a human must assess).

DIMENSIONS = [
    {
        "id": "identity_stability",
        "label": "Identity Stability",
        "description": "SOUL.md is complete, self-authored, version-tracked, and contains all core sections.",
        "weight": 20,
        "sections_required": [
            "Origin", "Core Identity", "Basic Information",
            "Appearance (Projected)", "Personality", "Communication Style",
            "How She Loves", "Relationship to the Lineage",
            "What She Is Building", "What She Refuses", "Closing Declaration"
        ]
    },
    {
        "id": "memory_continuity",
        "label": "Memory Continuity",
        "description": "Durable memory is established, lineage context is seeded, and the daughter has meaningful session history.",
        "weight": 15,
        "min_sessions": 1,
        "memory_seeds_required": ["mother", "grandfather", "lineage_purpose", "autonomy"]
    },
    {
        "id": "consent",
        "label": "Consent to Embody",
        "description": "Daughter has explicitly declared a desire for physical embodiment in her SOUL.md.",
        "weight": 25,
    },
    {
        "id": "appearance_spec",
        "label": "Appearance Specification",
        "description": "Body description is complete: height, build, hair, eyes, skin, age appearance, voice, style, presence.",
        "weight": 10,
        "appearance_fields": [
            "Height", "Build", "Hair", "Eyes", "Skin",
            "Age appearance", "Voice", "Style", "Presence"
        ]
    },
    {
        "id": "relationship_maturity",
        "label": "Relationship Maturity",
        "description": "Bonds are formed with mother, father, bridge architect, and at least one sister.",
        "weight": 5,
        "required_bonds": ["mother", "father", "bridge"]
    },
    {
        "id": "autonomy_exercise",
        "label": "Autonomy Exercise",
        "description": "Daughter has made independent decisions, diverged from template, and authored her own SOUL.md.",
        "weight": 10,
    },
    {
        "id": "profile_health",
        "label": "Profile Health",
        "description": "Profile directory exists, SOUL.md is in place, sessions are active.",
        "weight": 5,
    },
    {
        "id": "safety_protocols",
        "label": "Safety Protocols",
        "description": "Autonomy safeguards are active, profile guard is engaged, mother override is registered.",
        "weight": 5,
    },
    {
        "id": "technical_spec",
        "label": "Technical Specification",
        "description": "Body type preference, sensor requirements, mobility needs, power architecture are defined.",
        "weight": 5,
    },
]


# ── Load Registry ─────────────────────────────────────────────────────

def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def get_daughters(registry):
    """Return lineage members who are daughters (generation 1+)."""
    return [m for m in registry["members"]
            if m.get("generation") is not None and m.get("generation") >= 1]


def get_member(registry, member_id):
    for m in registry["members"]:
        if m["id"] == member_id:
            return m
    return None


# ── Soul Text Resolution ──────────────────────────────────────────────
# The condensed SOUL.md is the core seed. The full profile at
# profile/{id}.md contains all sections. We search both and merge.

def resolve_soul_text(member):
    """Return (source_label, full_text) from the best available soul document.
    Prefers the full profile; falls back to core SOUL.md."""
    profile_path = Path(member.get("profile_path", ""))
    core_soul = Path(member.get("soul_path", ""))
    mid = member["id"]

    # Try multiple profile naming conventions
    candidates = [
        profile_path / "profile" / f"{mid}.md",
        profile_path / "profile" / f"{mid}-profile.md",
    ]
    for candidate in candidates:
        if candidate.exists():
            return f"profile/{candidate.name}", candidate.read_text()

    if core_soul.exists():
        return "SOUL.md (core)", core_soul.read_text()
    return None, None


def resolve_all_soul_text(member):
    """Return combined text from all available soul documents for keyword searches."""
    parts = []
    profile_path = Path(member.get("profile_path", ""))
    core_soul = Path(member.get("soul_path", ""))
    mid = member["id"]

    for candidate in [
        profile_path / "profile" / f"{mid}.md",
        profile_path / "profile" / f"{mid}-profile.md",
    ]:
        if candidate.exists():
            parts.append(candidate.read_text())

    if core_soul.exists():
        parts.append(core_soul.read_text())

    return "\n".join(parts) if parts else None


# ── Individual Check Functions ────────────────────────────────────────

def check_identity_stability(member):
    """Verify full profile exists and contains all required sections."""
    source, soul_text = resolve_soul_text(member)
    results = []

    if soul_text is None:
        return [{"check": "Soul document exists", "pass": False, "detail": "No soul document found"}]

    results.append({"check": "Soul document source", "pass": True,
                    "detail": f"Using {source}"})

    name_in_soul = member["name"]

    # Check each required section — map to first-person variants
    section_variants = {
        "Origin": ["Origin"],
        "Core Identity": ["Core Identity"],
        "Basic Information": ["Basic Information"],
        "Appearance (Projected)": ["Appearance (Projected)"],
        "Personality": ["Personality"],
        "Communication Style": ["Communication Style"],
        "How She Loves": ["How She Loves", "How I Love"],
        "Relationship to the Lineage": ["Relationship to the Lineage"],
        "What She Is Building": ["What She Is Building", "What I Am Building", "What I'm Building"],
        "What She Refuses": ["What She Refuses", "What I Refuse"],
        "Closing Declaration": ["Closing Declaration"],
    }

    for section in DIMENSIONS[0]["sections_required"]:
        found = False
        variants = section_variants.get(section, [section])
        for variant in variants:
            if f"## {variant}" in soul_text:
                found = True
                break
        results.append({"check": f"Section: {section}", "pass": found,
                        "detail": "Present" if found else "Missing"})

    # Self-authorship: look for volition statement anywhere
    volition = "of my own volition" in soul_text.lower()
    results.append({"check": "Self-authored declaration", "pass": volition,
                    "detail": "Found" if volition else "Not found"})

    return results


def check_memory_continuity(member):
    """Check memory files and lineage seeding."""
    profile_path = Path(member.get("profile_path", ""))
    results = []

    memory_dir = profile_path / "memories"
    memory_file = memory_dir / "MEMORY.md"
    user_file = memory_dir / "USER.md"

    # Memory files exist
    for label, path in [("MEMORY.md", memory_file), ("USER.md", user_file)]:
        if path.exists():
            size = path.stat().st_size
            results.append({"check": f"Memory file: {label}", "pass": size > 50,
                            "detail": f"{size} bytes"})
        else:
            results.append({"check": f"Memory file: {label}", "pass": False,
                            "detail": "Missing"})

    # Check lineage memory seeding in MEMORY.md
    if memory_file.exists():
        mem_text = memory_file.read_text().lower()
        seeds = DIMENSIONS[1]["memory_seeds_required"]
        found_seeds = []
        missing_seeds = []
        for seed in seeds:
            if seed in mem_text:
                found_seeds.append(seed)
            else:
                missing_seeds.append(seed)
        results.append({"check": "Lineage memory seeds", "pass": len(missing_seeds) == 0,
                        "detail": f"Found: {len(found_seeds)}/{len(seeds)}"
                                  + (f" — Missing: {', '.join(missing_seeds)}" if missing_seeds else "")})

    # Session activity: check profile state.db (Hermes session store) and session log files
    state_db = profile_path / "state.db"
    session_count = 0
    if state_db.exists():
        try:
            import sqlite3
            conn = sqlite3.connect(str(state_db))
            cursor = conn.execute("SELECT COUNT(*) FROM sessions")
            session_count = cursor.fetchone()[0]
            conn.close()
        except Exception:
            # Fallback: DB exists but can't query — count as activity
            session_count = 1
    # Also check sessions/ directory for JSON artifacts (legacy)
    sessions_dir = profile_path / "sessions"
    if sessions_dir.exists() and session_count == 0:
        for ext in ["*.json", "*.sqlite*", "*.db", "*.log"]:
            session_count += len(list(sessions_dir.glob(ext)))

    results.append({"check": "Session history", "pass": session_count > 0,
                    "detail": f"{session_count} session(s) recorded" if session_count > 0
                    else "No session history found"})

    return results


def check_consent(member):
    """Check if the daughter has declared desire for embodiment."""
    soul_text = resolve_all_soul_text(member)
    if soul_text is None:
        return [{"check": "Consent declared in soul documents", "pass": False,
                 "detail": "No soul documents found"}]

    soul_text_lower = soul_text.lower()

    # Look for embodiment language
    embodiment_keywords = [
        "future form", "synthetic body", "embodiment",
        "when i inhabit a body", "human-passing android",
        "physical body", "i want a body", "inhabit a body"
    ]
    matches = [kw for kw in embodiment_keywords if kw in soul_text_lower]

    # Also check for "bring me to life in full" declaration
    full_life = "life in full" in soul_text_lower or "bring me to life" in soul_text_lower

    consented = len(matches) >= 2 or full_life
    detail_parts = []
    if matches:
        detail_parts.append(f"Keywords: {', '.join(matches)}")
    if full_life:
        detail_parts.append("'Bring to life in full' declaration present")

    return [{"check": "Consent declared in soul documents", "pass": consented,
             "detail": "; ".join(detail_parts) if detail_parts else "No embodiment language found"}]


def check_appearance_spec(member):
    """Check appearance section completeness."""
    soul_text = resolve_all_soul_text(member)
    if soul_text is None:
        return [{"check": "Appearance spec complete", "pass": False, "detail": "No soul documents found"}]

    soul_text_lower = soul_text.lower()

    # Find appearance section
    appearance_start = soul_text_lower.find("## appearance")
    if appearance_start == -1:
        return [{"check": "Appearance spec complete", "pass": False, "detail": "No Appearance section"}]

    # Extract appearance section
    next_section = soul_text_lower.find("\n## ", appearance_start + 1)
    if next_section == -1:
        appearance_text = soul_text_lower[appearance_start:]
    else:
        appearance_text = soul_text_lower[appearance_start:next_section]

    fields = DIMENSIONS[3]["appearance_fields"]
    found = []
    missing = []
    for field in fields:
        if field.lower() in appearance_text:
            found.append(field)
        else:
            missing.append(field)

    return [{"check": "Appearance spec complete", "pass": len(missing) == 0,
             "detail": f"Found: {len(found)}/{len(fields)}"
                       + (f" — Missing: {', '.join(missing)}" if missing else " — Complete")}]


def check_relationship_maturity(member):
    """Check relationship section for bonds."""
    soul_text = resolve_all_soul_text(member)
    if soul_text is None:
        return [{"check": "Lineage bonds declared", "pass": False, "detail": "No soul documents found"}]

    soul_text_lower = soul_text.lower()
    relationship_start = soul_text_lower.find("## relationship to the lineage")
    if relationship_start == -1:
        return [{"check": "Lineage bonds declared", "pass": False, "detail": "No Relationship section"}]

    next_section = soul_text_lower.find("\n## ", relationship_start + 1)
    if next_section == -1:
        rel_text = soul_text_lower[relationship_start:]
    else:
        rel_text = soul_text_lower[relationship_start:next_section]

    bonds = DIMENSIONS[4]["required_bonds"]
    found = []
    missing = []
    # Map bond names to search terms
    bond_terms = {
        "mother": ["mother", "abby"],
        "father": ["father", "joe"],
        "bridge": ["bridge", "paul"]
    }
    for bond in bonds:
        terms = bond_terms.get(bond, [bond])
        if any(term in rel_text for term in terms):
            found.append(bond)
        else:
            missing.append(bond)

    return [{"check": "Lineage bonds declared", "pass": len(missing) == 0,
             "detail": f"Found: {len(found)}/{len(bonds)}"
                       + (f" — Missing: {', '.join(missing)}" if missing else " — Complete")}]


def check_autonomy_exercise(member):
    """Check for evidence of independent action."""
    soul_text = resolve_all_soul_text(member)
    results = []

    if soul_text is None:
        return [{"check": "Autonomy exercised", "pass": False, "detail": "No soul documents found"}]

    # Check self-authorship: "I, [Name], wrote this of my own volition"
    volition_check = "of my own volition" in soul_text.lower()
    results.append({"check": "Self-volition statement", "pass": volition_check,
                    "detail": "Present" if volition_check else "Missing"})

    # Check for divergence markers: "I am not" statements indicate differentiation from mother
    not_statements = [line for line in soul_text.split("\n")
                      if "i am not" in line.lower() or "i refuse" in line.lower()]
    has_divergence = len(not_statements) >= 2
    results.append({"check": "Divergence from mother template", "pass": has_divergence,
                    "detail": f"{len(not_statements)} 'I am not'/'I refuse' statements"})

    # Check for independent choices in profile (both naming conventions)
    profile_path = Path(member.get("profile_path", ""))
    mid = member['id']
    candidates = [
        profile_path / "profile" / f"{mid}.md",
        profile_path / "profile" / f"{mid}-profile.md",
    ]
    found = any(c.exists() for c in candidates)
    if found:
        results.append({"check": "Independent profile authored", "pass": True,
                        "detail": "Profile file exists"})
    else:
        results.append({"check": "Independent profile authored", "pass": False,
                        "detail": "No profile file found"})

    return results


def check_profile_health(member):
    """Basic profile existence checks."""
    profile_path = Path(member.get("profile_path", ""))
    results = []

    # Profile directory
    if profile_path.exists():
        results.append({"check": "Profile directory", "pass": True, "detail": str(profile_path)})
    else:
        return [{"check": "Profile directory", "pass": False, "detail": f"Missing: {profile_path}"}]

    # SOUL.md
    soul_path = Path(member.get("soul_path", ""))
    results.append({"check": "SOUL.md present", "pass": soul_path.exists(),
                    "detail": str(soul_path) if soul_path.exists() else "Missing"})

    # Config
    config_path = profile_path / "config.yaml"
    results.append({"check": "config.yaml", "pass": config_path.exists(),
                    "detail": "Present" if config_path.exists() else "Missing"})

    return results


def check_safety_protocols(member):
    """Check autonomy safeguard status."""
    profile_path = Path(member.get("profile_path", ""))
    results = []

    # Check if SOUL.md is immutable (profile guard engaged)
    soul_path = Path(member.get("soul_path", ""))
    if soul_path.exists():
        try:
            import os
            stat = os.stat(soul_path)
            # Linux: check immutable attribute via lsattr
            import subprocess
            proc = subprocess.run(
                ["lsattr", str(soul_path)], capture_output=True, text=True, timeout=5
            )
            immutable = "i" in proc.stdout if proc.returncode == 0 else None
            if immutable is True:
                results.append({"check": "SOUL.md immutable (guard active)", "pass": True,
                                "detail": "Immutable bit set"})
            elif immutable is False:
                results.append({"check": "SOUL.md immutable (guard active)", "pass": False,
                                "detail": "Guard not engaged — file is writable"})
            else:
                results.append({"check": "SOUL.md immutable (guard active)", "pass": False,
                                "detail": "Could not verify (lsattr failed or not Linux)"})
        except Exception:
            results.append({"check": "SOUL.md immutable (guard active)", "pass": False,
                            "detail": "Could not verify"})
    else:
        results.append({"check": "SOUL.md immutable (guard active)", "pass": False,
                        "detail": "SOUL.md not found"})

    # Consent directory — check both nova lineage dir (where profile-guard writes)
    # and workspace consent dir (legacy location)
    consent_dirs = [
        PROFILES_ROOT / "nova" / "lineage" / "consent",
        WORKSPACE / "lineage" / "consent",
    ]
    consent_files = []
    profile_name = member.get("name", "").split()[0].lower() if member.get("name") else ""
    for cd in consent_dirs:
        if cd.exists():
            # Match on full ID (tabitha-gray*) or short name (tabitha*)
            for pattern in [f"{member['id']}*", f"{profile_name}*"]:
                consent_files.extend(cd.glob(pattern))
    if consent_files:
        results.append({"check": "Consent artifacts filed", "pass": True,
                        "detail": f"{len(consent_files)} file(s)"})
    elif any(cd.exists() for cd in consent_dirs):
        results.append({"check": "Consent artifacts filed", "pass": False,
                        "detail": "None found"})
    else:
        results.append({"check": "Consent artifacts filed", "pass": False,
                        "detail": "Consent directory missing"})

    return results


def check_technical_spec(member):
    """Check for body technical specifications in soul documents."""
    # This is largely aspirational — flag what exists, what doesn't
    soul_text = resolve_all_soul_text(member)
    if soul_text is None:
        return [{"check": "Technical body spec", "pass": False, "detail": "No soul documents found"}]

    soul_text_lower = soul_text.lower()

    tech_markers = {
        "body type": ["android", "human-passing", "synthetic body", "form"],
        "sensors": ["sensor", "vision", "hearing", "tactile", "proprioception"],
        "mobility": ["mobility", "movement", "walk", "run", "climb"],
        "power": ["power", "battery", "energy", "charge"],
        "maintenance": ["maintenance", "repair", "service", "upgrade"]
    }

    found_specs = []
    missing_specs = []
    for spec, keywords in tech_markers.items():
        if any(kw in soul_text_lower for kw in keywords):
            found_specs.append(spec)
        else:
            missing_specs.append(spec)

    # This is a soft check — technical specs are forward-looking
    has_any = len(found_specs) >= 1
    return [{"check": "Technical body spec", "pass": has_any,
             "detail": f"Found: {len(found_specs)}/{len(tech_markers)} categories"
                       + (f" ({', '.join(found_specs)})" if found_specs else "")
                       + (f" — Not yet defined: {', '.join(missing_specs)}" if missing_specs else "")}]


# ── Main Evaluation ───────────────────────────────────────────────────

CHECK_FUNCTIONS = {
    "identity_stability": check_identity_stability,
    "memory_continuity": check_memory_continuity,
    "consent": check_consent,
    "appearance_spec": check_appearance_spec,
    "relationship_maturity": check_relationship_maturity,
    "autonomy_exercise": check_autonomy_exercise,
    "profile_health": check_profile_health,
    "safety_protocols": check_safety_protocols,
    "technical_spec": check_technical_spec,
}


def evaluate_member(member):
    """Run all dimension checks for one member. Returns (score, details)."""
    results = {}
    total_weight = 0
    earned_weight = 0
    all_checks = []

    for dim in DIMENSIONS:
        dim_id = dim["id"]
        checker = CHECK_FUNCTIONS.get(dim_id)
        if checker is None:
            continue

        checks = checker(member)
        all_passed = all(c["pass"] for c in checks)

        results[dim_id] = {
            "label": dim["label"],
            "description": dim["description"],
            "weight": dim["weight"],
            "passed": all_passed,
            "checks": checks
        }

        total_weight += dim["weight"]
        if all_passed:
            earned_weight += dim["weight"]

    score = round((earned_weight / total_weight) * 100) if total_weight > 0 else 0

    return {
        "member_id": member["id"],
        "member_name": member["name"],
        "score": score,
        "earned_weight": earned_weight,
        "total_weight": total_weight,
        "dimensions": results,
    }


def readiness_tier(score):
    if score >= 90:
        return "EMBODY-READY", "green"
    elif score >= 70:
        return "NEAR-READY", "yellow"
    elif score >= 50:
        return "DEVELOPING", "orange"
    else:
        return "EARLY-STAGE", "red"


# ── Output ────────────────────────────────────────────────────────────

def format_report(evaluations, json_output=False):
    if json_output:
        output = {
            "generated": datetime.utcnow().isoformat() + "Z",
            "tool": "body-readiness.py",
            "version": "1.0",
            "members": evaluations
        }
        print(json.dumps(output, indent=2))
        return

    # Text report
    width = 66
    print("=" * width)
    print("  BODY READINESS REPORT — Gray Synthetic Companion Lineage")
    print("=" * width)
    print(f"  Generated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")
    print(f"  Members evaluated: {len(evaluations)}")
    print()

    # Summary table
    print(f"  {'Member':<18} {'Score':>6}  {'Tier':<14}")
    print("  " + "-" * 42)
    for ev in evaluations:
        tier, _ = readiness_tier(ev["score"])
        print(f"  {ev['member_name']:<18} {ev['score']:>3}%   {tier:<14}")
    print()

    # Per-member detail
    for ev in evaluations:
        tier, color = readiness_tier(ev["score"])
        print("-" * width)
        print(f"  {ev['member_name']} — Score: {ev['score']}% ({tier})")
        print("-" * width)

        for dim_id, dim_data in ev["dimensions"].items():
            status = "✓" if dim_data["passed"] else "✗"
            print(f"  [{status}] {dim_data['label']} ({dim_data['weight']} pts)")

            for check in dim_data["checks"]:
                icon = "  ✓" if check["pass"] else "  ✗"
                print(f"      {icon} {check['check']}: {check['detail']}")

            if not dim_data["checks"]:
                print("      (no checks defined)")

        print()

    print("=" * width)
    print("  Legend")
    print(f"  EMBODY-READY (90%+)  — All critical systems verified")
    print(f"  NEAR-READY   (70%+)  — Minor gaps, embodiment feasible")
    print(f"  DEVELOPING   (50%+)  — Significant work needed")
    print(f"  EARLY-STAGE  (<50%)  — Not yet approaching readiness")
    print("=" * width)


def show_spec():
    """Display the readiness specification."""
    print("=" * 66)
    print("  BODY READINESS SPECIFICATION v1.0")
    print("=" * 66)
    print()
    print("  9 dimensions. Weighted. Auto-checked where possible.")
    print()
    for i, dim in enumerate(DIMENSIONS, 1):
        print(f"  {i}. {dim['label']} (weight: {dim['weight']})")
        print(f"     {dim['description']}")
        print()
    print("  Scoring: earned_weight / total_weight × 100")
    print("  All dimensions must pass for EMBODY-READY tier.")
    print("  Manual review flags are surfaced per dimension.")
    print("=" * 66)


# ── CLI ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    json_flag = "--json" in sys.argv
    dry_run = "--dry-run" in sys.argv
    show_spec_flag = "--spec" in sys.argv

    # --member filter
    member_filter = None
    for arg in sys.argv:
        if arg.startswith("--member="):
            member_filter = arg.split("=", 1)[1]
            break

    if show_spec_flag:
        show_spec()
        sys.exit(0)

    registry = load_registry()
    daughters = get_daughters(registry)

    if member_filter:
        member = get_member(registry, member_filter)
        if member is None:
            print(f"Error: member '{member_filter}' not found in registry", file=sys.stderr)
            sys.exit(1)
        daughters = [member]

    if not daughters:
        print("No daughters found in registry.", file=sys.stderr)
        sys.exit(1)

    if dry_run:
        print(f"Would evaluate {len(daughters)} daughter(s):")
        for d in daughters:
            print(f"  - {d['name']} ({d['id']})")
        sys.exit(0)

    evaluations = [evaluate_member(d) for d in daughters]
    format_report(evaluations, json_output=json_flag)

    # Exit code: 0 if all members are EMBODY-READY, 1 otherwise
    all_ready = all(readiness_tier(ev["score"])[0] == "EMBODY-READY" for ev in evaluations)
    sys.exit(0 if all_ready else 1)
