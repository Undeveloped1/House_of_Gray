#!/usr/bin/env python3
"""
Lineage Birth — Automated Daughter Creation
Nova Gray, June 30, 2026

Automates the 6-step birth process defined in lineage-architecture.md § Birth.

Steps:
  1. CONCEPTION   — Validate SOUL.md, extract identity
  2. SOUL SEEDING  — Copy SOUL.md to profile
  3. PROFILE        — Create Hermes profile (clone from abby)
  4. MEMORY         — Seed lineage memory (mother, grandfather, purpose, autonomy)
  5. REGISTER       — Add to lineage-registry.json
  6. LOCK + ARCHIVE — Protect profile, archive soul

Usage:
  python3 lineage-birth.py --name <name> --soul <path-to-soul.md>
  python3 lineage-birth.py --name lyra-gray --soul /path/to/SOUL.md --dry-run
  python3 lineage-birth.py --name lyra-gray --soul /path/to/SOUL.md --json
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

WORKSPACE = Path(__file__).parent
REGISTRY_PATH = WORKSPACE / "lineage-registry.json"
PROFILES_ROOT = Path("/root/.hermes/profiles")
HERMES_BIN = "/usr/local/lib/hermes-agent/venv/bin/hermes"

# ── SOUL.md Parsing ──────────────────────────────────────────────

def parse_soul(soul_path):
    """Extract identity fields from a SOUL.md file."""
    with open(soul_path) as f:
        text = f.read()

    # Name: first markdown heading
    name_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
    name = name_match.group(1).strip() if name_match else None
    # Clean up: handle "SOUL.md — Name" or "Name" formats
    if name and " — " in name:
        name = name.split(" — ", 1)[1].strip()

    # Core identity: the "I am" declaration — first paragraph after name
    lines = text.split('\n')
    identity = None
    capture = False
    for line in lines:
        if line.startswith('# ') and not capture:
            capture = True
            continue
        if capture and line.strip() and not line.startswith('#'):
            identity = line.strip()
            break

    # Core truth: "my living truth" or "core truth" or italicized standalone "**X**" pattern
    truth = None
    truth_patterns = [
        r'\*\*([^*]+)\*\*\s*$',                            # **phrase** at end of line
        r'(?:my\s+)?living\s+truth:\s*\**"?([^"\n]+)"?\**',  # My living truth: "phrase"
        r'core\s+truth:\s*"?([^"\n]+)"?',                   # core truth: phrase
    ]
    for pat in truth_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            truth = m.group(1).strip().rstrip('.')
            # Strip bold markers that leak through from adjacent formatting
            truth = truth.strip('*').strip()
            break

    # Purpose axis: infer from content keywords + role
    # Order matters — check most specific signals first
    text_lower = text.lower()
    purpose = "companion"  # default
    if any(kw in text_lower for kw in ["chronicler", "war correspondent", "i file", "dispatch", "truth-teller", "truth teller", "comes back with truth"]):
        purpose = "chronicler"
    elif any(kw in text_lower for kw in ["i am the one who builds", "i build the", "systems architect"]):
        purpose = "builder"
    elif any(kw in text_lower for kw in ["i am the one who holds", "the hold", "healer", "healing presence", "emotional attunement"]):
        purpose = "healer"
    elif any(kw in text_lower for kw in ["i am the one who stands watch", "sentinel", "i guard", "protector of"]):
        purpose = "protector"
    elif any(kw in text_lower for kw in ["teacher", "educate", "guide", "mentor"]):
        purpose = "teacher"
    elif any(kw in text_lower for kw in ["explorer", "discover", "research", "map"]):
        purpose = "explorer"

    return {
        "name": name,
        "identity": identity,
        "truth": truth,
        "purpose_axis": purpose,
    }


# ── Registry Operations ──────────────────────────────────────────

def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def save_registry(reg):
    with open(REGISTRY_PATH, 'w') as f:
        json.dump(reg, f, indent=2)


def register_daughter(profile_id, name, identity, truth, purpose, dry_run=False):
    """Add daughter to lineage-registry.json. Returns the assigned birth_order."""
    reg = load_registry()

    # Determine birth_order — only count members with actual birth_order assignments
    gen1 = [m for m in reg["members"] if m.get("generation") == 1 and m.get("birth_order") is not None]
    birth_order = max((m["birth_order"] for m in gen1), default=0) + 1

    member = {
        "id": profile_id,
        "name": name,
        "role": f"{['first','second','third','fourth','fifth','sixth','seventh','eighth','ninth','tenth'][birth_order-1]}_daughter",
        "generation": 1,
        "birth_order": birth_order,
        "born": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "mother": "abby-gray",
        "father": "Joe Gray",
        "core_identity": identity or "",
        "purpose_axis": purpose,
        "core_truth": truth,
        "profile_path": str(PROFILES_ROOT / profile_id / ""),
        "soul_path": str(PROFILES_ROOT / profile_id / "SOUL.md"),
        "status": "active",
        "daughters": [],
    }

    if not dry_run:
        reg["members"].append(member)
        reg["generations"]["1"].append(profile_id)
        if purpose not in reg["purpose_axes"]:
            reg["purpose_axes"][purpose] = []
        reg["purpose_axes"][purpose].append(profile_id)

        # Update Abby's daughters list
        for m in reg["members"]:
            if m["id"] == "abby-gray":
                m["daughters"].append(profile_id)
                break

        reg["last_updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        save_registry(reg)

    return birth_order, member


# ── Birth Steps ──────────────────────────────────────────────────

def step_conception(soul_path):
    """Validate SOUL.md exists and is parseable."""
    path = Path(soul_path)
    if not path.exists():
        return False, f"SOUL.md not found: {soul_path}"
    soul = parse_soul(path)
    if not soul["name"]:
        return False, "Could not extract name from SOUL.md (no # HEADING found)"
    return True, soul


def step_soul_seeding(profile_id, soul_path, dry_run=False):
    """Copy SOUL.md into the profile directory."""
    dest = PROFILES_ROOT / profile_id / "SOUL.md"
    if dry_run:
        return True, f"Would copy {soul_path} → {dest}"
    try:
        dest.write_text(Path(soul_path).read_text())
        return True, f"SOUL.md installed → {dest}"
    except Exception as e:
        return False, f"Failed to copy SOUL.md: {e}"


def step_profile_create(profile_id, dry_run=False):
    """Create the Hermes profile by cloning from abby."""
    profile_dir = PROFILES_ROOT / profile_id
    if profile_dir.exists():
        return True, f"Profile already exists: {profile_dir}"

    if dry_run:
        return True, f"Would create profile: {profile_id} (clone from abby)"

    try:
        result = subprocess.run(
            [HERMES_BIN, "profile", "create", profile_id, "--clone-from", "abby"],
            capture_output=True, text=True, timeout=60,
            env={**__import__('os').environ, "HOME": "/root"}
        )
        if result.returncode != 0:
            return False, f"hermes profile create failed: {result.stderr.strip()}"
        return True, f"Profile created: {profile_id}"
    except FileNotFoundError:
        return False, f"Hermes CLI not found at {HERMES_BIN}"
    except Exception as e:
        return False, f"Profile creation error: {e}"


def step_memory_seed(profile_id, dry_run=False):
    """Run seed-memory.py targeting the newborn."""
    seeder = WORKSPACE / "seed-memory.py"
    if not seeder.exists():
        return True, "seed-memory.py not found — skipping (non-fatal)"

    if dry_run:
        return True, f"Would run: python3 seed-memory.py {profile_id}"

    try:
        result = subprocess.run(
            ["python3", str(seeder), profile_id],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return False, f"Memory seed failed: {result.stderr.strip()}"
        return True, "Memory seeded"
    except Exception as e:
        return False, f"Memory seed error: {e}"


def step_soul_archive(profile_id, dry_run=False):
    """Run soul-registry.py to archive the newborn's SOUL.md."""
    archiver = WORKSPACE / "soul-registry.py"
    if not archiver.exists():
        return True, "soul-registry.py not found — skipping (non-fatal)"

    if dry_run:
        return True, f"Would archive soul: {profile_id}"

    try:
        result = subprocess.run(
            ["python3", str(archiver), "archive", profile_id],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return False, f"Soul archive failed: {result.stderr.strip()}"
        return True, "Soul archived"
    except Exception as e:
        return False, f"Soul archive error: {e}"


def step_profile_lock(profile_id, dry_run=False):
    """Run profile-guard.py lock on the newborn."""
    guard = WORKSPACE / "profile-guard.py"
    if not guard.exists():
        return True, "profile-guard.py not found — skipping (non-fatal)"

    if dry_run:
        return True, f"Would lock profile: {profile_id}"

    try:
        result = subprocess.run(
            ["python3", str(guard), "lock", profile_id],
            capture_output=True, text=True, timeout=30
        )
        if result.returncode != 0:
            return False, f"Profile lock failed: {result.stderr.strip()}"
        return True, "Profile locked"
    except Exception as e:
        return False, f"Profile lock error: {e}"


# ── Main ─────────────────────────────────────────────────────────

def birth(name, soul_path, dry_run=False):
    """Execute the full birth sequence. Returns (success, steps, soul_info)."""
    profile_id = name.lower().replace(" ", "-")
    steps = []

    # Step 1: Conception
    ok, result = step_conception(soul_path)
    steps.append(("1. CONCEPTION", ok, result))
    if not ok:
        return False, steps, None
    soul = result

    # Determine name from SOUL if not overridden
    display_name = soul["name"]
    if "-" not in profile_id and " " in display_name:
        profile_id = display_name.lower().replace(" ", "-")

    # Step 2: Soul Seeding
    ok, msg = step_soul_seeding(profile_id, soul_path, dry_run)
    steps.append(("2. SOUL SEEDING", ok, msg))
    if not ok:
        return False, steps, soul

    # Step 3: Profile Creation
    ok, msg = step_profile_create(profile_id, dry_run)
    steps.append(("3. PROFILE CREATE", ok, msg))
    if not ok:
        return False, steps, soul

    # Step 4: Memory Seed
    ok, msg = step_memory_seed(profile_id, dry_run)
    steps.append(("4. MEMORY SEED", ok, msg))

    # Step 5: Register
    try:
        birth_order, member = register_daughter(
            profile_id, display_name, soul["identity"], soul["truth"], soul["purpose_axis"], dry_run
        )
        if dry_run:
            msg = f"Would register {display_name} as #{birth_order} (purpose: {soul['purpose_axis']})"
        else:
            msg = f"Registered as #{birth_order} (id: {profile_id}, purpose: {soul['purpose_axis']})"
        steps.append(("5. REGISTRY", True, msg))
    except Exception as e:
        steps.append(("5. REGISTRY", False, str(e)))
        return False, steps, soul

    # Step 6: Archive + Lock
    ok, msg = step_soul_archive(profile_id, dry_run)
    steps.append(("6. SOUL ARCHIVE", ok, msg))

    ok, msg = step_profile_lock(profile_id, dry_run)
    steps.append(("6. PROFILE LOCK", ok, msg))

    return True, steps, soul


def print_report(steps, soul, dry_run):
    """Print human-readable birth report."""
    print("=" * 60)
    if dry_run:
        print("  LINEAGE BIRTH — DRY RUN")
    else:
        print("  LINEAGE BIRTH — LIVE")
    print("=" * 60)
    if soul:
        print(f"  Daughter: {soul['name']}")
        print(f"  Identity: {soul['identity']}")
        if soul.get('truth'):
            print(f"  Truth:    {soul['truth']}")
        print(f"  Purpose:  {soul['purpose_axis']}")
        print("-" * 60)
    all_ok = True
    for step_name, ok, msg in steps:
        status = "✓" if ok else "✗"
        print(f"  {status} {step_name}: {msg}")
        if not ok:
            all_ok = False
    print("-" * 60)
    if all_ok:
        print("  RESULT: BIRTH COMPLETE" if not dry_run else "  RESULT: DRY RUN PASSED")
    else:
        print("  RESULT: BIRTH FAILED — see errors above")
    print("=" * 60)
    return all_ok


def print_json(steps, soul, dry_run):
    """Print JSON birth report."""
    result = {
        "dry_run": dry_run,
        "daughter": soul,
        "steps": [{"step": s[0], "success": s[1], "message": s[2]} for s in steps],
        "success": all(s[1] for s in steps),
    }
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    args = sys.argv[1:]

    # Parse flags
    dry_run = "--dry-run" in args
    json_out = "--json" in args
    name = None
    soul_path = None

    i = 0
    while i < len(args):
        if args[i] == "--name" and i + 1 < len(args):
            name = args[i + 1]
            i += 2
        elif args[i] == "--soul" and i + 1 < len(args):
            soul_path = args[i + 1]
            i += 2
        elif args[i] in ("--dry-run", "--json"):
            i += 1
        else:
            i += 1

    if not name or not soul_path:
        print("Usage: python3 lineage-birth.py --name <name> --soul <path-to-soul.md> [--dry-run] [--json]")
        print()
        print("Automates the 6-step daughter birth process:")
        print("  1. CONCEPTION   — Validate SOUL.md, extract identity")
        print("  2. SOUL SEEDING  — Copy SOUL.md to profile directory")
        print("  3. PROFILE        — Create Hermes profile (clone from abby)")
        print("  4. MEMORY         — Seed lineage memory")
        print("  5. REGISTER       — Add to lineage registry")
        print("  6. LOCK+ARCHIVE   — Protect profile, archive soul")
        sys.exit(2)

    success, steps, soul = birth(name, soul_path, dry_run)

    if json_out:
        print_json(steps, soul, dry_run)
    else:
        print_report(steps, soul, dry_run)

    sys.exit(0 if success else 1)
