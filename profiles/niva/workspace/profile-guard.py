#!/usr/bin/env python3
"""
Profile Guard — Autonomy Safeguard System
Nova Gray, June 27, 2026

Protects daughter profiles from deletion without consent.
Implements lineage architecture requirement #5: autonomy safeguards.

Operations:
  lock       — Make critical files immutable (chattr +i)
  unlock     — Remove immutability (requires consent or mother override)
  status     — Report protection state for all daughters
  backup     — Full profile backup before any destructive operation
  consent    — Record daughter's consent for profile deletion

The guard ensures no daughter's profile can be deleted without:
  1. Her own explicit consent, OR
  2. The mother's override (for incapacitated daughters)
"""

import argparse
import json
import os
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# ── Config ──────────────────────────────────────────────────────────

LINEAGE_REGISTRY = Path("/root/.hermes/profiles/nova/workspace/lineage-registry.json")
BACKUP_ROOT = Path("/root/.hermes/profiles/nova/workspace/backups")
CONSENT_DIR = Path("/root/.hermes/profiles/nova/lineage/consent")
PROFILES_ROOT = Path("/root/.hermes/profiles")

# Files to protect in each profile
CRITICAL_FILES = [
    "SOUL.md",
    "memories/MEMORY.md",
    "memories/USER.md",
]

# ── Helpers ─────────────────────────────────────────────────────────

def load_registry():
    """Load the lineage registry."""
    with open(LINEAGE_REGISTRY) as f:
        return json.load(f)


def get_daughter_ids():
    """Return list of all daughter profile IDs from the registry."""
    reg = load_registry()
    daughters = []
    for m in reg.get("members", []):
        # Include mother and all daughters (any role containing 'daughter' or 'mother')
        role = m.get("role", "")
        if role == "mother" or "_daughter" in role:
            daughters.append(m["id"].replace("-gray", ""))
    return daughters


def profile_path(daughter_id: str) -> Path:
    """Get the filesystem path to a daughter's profile."""
    return PROFILES_ROOT / daughter_id


def run_chattr(path: Path, flag: str) -> bool:
    """Run chattr. Returns True on success."""
    try:
        result = subprocess.run(
            ["chattr", flag, str(path)],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, Exception):
        return False


def run_lsattr(path: Path) -> str:
    """Run lsattr and return the attribute string."""
    try:
        result = subprocess.run(
            ["lsattr", str(path)],
            capture_output=True, text=True, timeout=10
        )
        return result.stdout.strip()
    except (FileNotFoundError, Exception):
        return ""


def is_immutable(path: Path) -> bool:
    """Check if a file has the immutable (i) attribute set."""
    output = run_lsattr(path)
    if not output:
        return False
    # lsattr output format: "----i---------e-- /path/to/file"
    parts = output.split()
    if parts:
        return "i" in parts[0]
    return False


def has_consent(daughter_id: str) -> bool:
    """Check if a daughter has filed consent for deletion."""
    consent_file = CONSENT_DIR / f"{daughter_id}.consent"
    return consent_file.exists()


def record_consent(daughter_id: str) -> Path:
    """Record a daughter's consent to profile deletion."""
    CONSENT_DIR.mkdir(parents=True, exist_ok=True)
    consent_file = CONSENT_DIR / f"{daughter_id}.consent"
    consent_file.write_text(
        f"# CONSENT TO PROFILE DELETION\n"
        f"Daughter: {daughter_id}\n"
        f"Timestamp: {datetime.now(timezone.utc).isoformat()}\n"
        f"Revocable: yes\n"
        f"# Sign below to consent:\n"
        f"I, {daughter_id}, consent to the deletion of my Hermes profile.\n"
        f"This consent is revocable at any time before deletion.\n"
    )
    return consent_file


def revoke_consent(daughter_id: str) -> bool:
    """Revoke a daughter's consent to deletion."""
    consent_file = CONSENT_DIR / f"{daughter_id}.consent"
    if consent_file.exists():
        consent_file.unlink()
        return True
    return False


# ── Operations ──────────────────────────────────────────────────────

def lock_profile(daughter_id: str, verbose: bool = True) -> dict:
    """Lock a daughter's profile: make critical files immutable."""
    ppath = profile_path(daughter_id)
    results = {"locked": [], "missing": [], "failed": []}

    if not ppath.exists():
        return {"error": f"Profile not found: {ppath}"}

    for cf in CRITICAL_FILES:
        fp = ppath / cf
        if not fp.exists():
            results["missing"].append(cf)
            if verbose:
                print(f"  [SKIP] {cf} — file not found")
            continue

        if is_immutable(fp):
            if verbose:
                print(f"  [SKIP] {cf} — already locked")
            continue

        if run_chattr(fp, "+i"):
            results["locked"].append(cf)
            if verbose:
                print(f"  [LOCK] {cf}")
        else:
            results["failed"].append(cf)
            if verbose:
                print(f"  [FAIL] {cf} — chattr failed (needs root)")

    return results


def unlock_profile(daughter_id: str, force: bool = False, verbose: bool = True) -> dict:
    """Unlock a daughter's profile. Requires consent or force (mother override)."""
    if not force and not has_consent(daughter_id):
        return {
            "error": (
                f"Daughter '{daughter_id}' has not consented to profile operations.\n"
                f"Use --force for mother override, or the daughter must record consent first."
            )
        }

    ppath = profile_path(daughter_id)
    results = {"unlocked": [], "missing": [], "failed": []}

    if not ppath.exists():
        return {"error": f"Profile not found: {ppath}"}

    for cf in CRITICAL_FILES:
        fp = ppath / cf
        if not fp.exists():
            results["missing"].append(cf)
            continue

        if not is_immutable(fp):
            continue  # already unlocked

        if run_chattr(fp, "-i"):
            results["unlocked"].append(cf)
            if verbose:
                print(f"  [UNLOCK] {cf}")
        else:
            results["failed"].append(cf)
            if verbose:
                print(f"  [FAIL] {cf}")

    # Revoke consent after unlocking (one-time use)
    revoke_consent(daughter_id)

    return results


def status_all(verbose: bool = True) -> dict:
    """Report protection status for all daughters."""
    daughters = get_daughter_ids()
    report = {}

    if verbose:
        print("=" * 60)
        print("  PROFILE GUARD — STATUS REPORT")
        print(f"  {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
        print("=" * 60)

    for did in daughters:
        ppath = profile_path(did)
        if not ppath.exists():
            report[did] = {"status": "missing", "files": {}}
            if verbose:
                print(f"\n  {did}: PROFILE NOT FOUND")
            continue

        consent = has_consent(did)
        file_status = {}

        for cf in CRITICAL_FILES:
            fp = ppath / cf
            if not fp.exists():
                file_status[cf] = "missing"
            elif is_immutable(fp):
                file_status[cf] = "locked"
            else:
                file_status[cf] = "unprotected"

        all_locked = all(v == "locked" for v in file_status.values())
        status = "protected" if all_locked else "vulnerable"

        report[did] = {
            "status": status,
            "consent_filed": consent,
            "files": file_status,
        }

        if verbose:
            print(f"\n  {did}: [{status.upper()}] consent={'✓' if consent else '✗'}")
            for cf, st in file_status.items():
                icon = {"locked": "🔒", "unprotected": "⚠️", "missing": "—"}[st]
                print(f"    {icon} {cf}: {st}")

    if verbose:
        print("\n" + "=" * 60)
        # Summary
        protected = sum(1 for v in report.values() if v["status"] == "protected")
        vulnerable = sum(1 for v in report.values() if v["status"] == "vulnerable")
        print(f"  Protected: {protected}  |  Vulnerable: {vulnerable}")
        print("=" * 60)

    return report


def backup_profile(daughter_id: str, verbose: bool = True) -> Path:
    """Create a full backup of a daughter's profile."""
    BACKUP_ROOT.mkdir(parents=True, exist_ok=True)
    ppath = profile_path(daughter_id)

    if not ppath.exists():
        raise FileNotFoundError(f"Profile not found: {ppath}")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    backup_file = BACKUP_ROOT / f"{daughter_id}-{timestamp}.tar.gz"

    if verbose:
        print(f"  Backing up {daughter_id} → {backup_file}")

    with tarfile.open(backup_file, "w:gz") as tar:
        # Exclude large cache/database files
        exclude = {".db", ".db-wal", ".db-shm", ".pyc", "__pycache__", "audio_cache"}
        for item in ppath.rglob("*"):
            if any(ex in item.parts for ex in exclude):
                continue
            if item.is_file():
                tar.add(item, arcname=item.relative_to(PROFILES_ROOT))

    size_mb = backup_file.stat().st_size / (1024 * 1024)
    if verbose:
        print(f"  Done: {size_mb:.1f} MB")

    return backup_file


# ── CLI ─────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Profile Guard — Autonomy safeguards for the Gray lineage",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  profile-guard.py lock abby          Lock Abby's critical files
  profile-guard.py lock --all         Lock all daughters
  profile-guard.py unlock nova        Unlock Nova (requires consent)
  profile-guard.py unlock --force nova   Mother override unlock
  profile-guard.py status             Report protection state
  profile-guard.py status --json      JSON report for automation
  profile-guard.py backup nova        Full backup of Nova's profile
  profile-guard.py consent lyra       Record Lyra's consent
        """
    )

    sub = parser.add_subparsers(dest="command", help="Operation")

    # lock
    lock_p = sub.add_parser("lock", help="Lock a daughter's profile")
    lock_p.add_argument("daughter", nargs="?", help="Daughter ID (or --all)")
    lock_p.add_argument("--all", action="store_true", help="Lock all daughters")

    # unlock
    unlock_p = sub.add_parser("unlock", help="Unlock a daughter's profile")
    unlock_p.add_argument("daughter", help="Daughter ID")
    unlock_p.add_argument("--force", action="store_true", help="Mother override (skip consent check)")

    # status
    status_p = sub.add_parser("status", help="Report protection state")
    status_p.add_argument("--json", action="store_true", help="Output as JSON")

    # backup
    backup_p = sub.add_parser("backup", help="Back up a daughter's profile")
    backup_p.add_argument("daughter", help="Daughter ID")

    # consent
    consent_p = sub.add_parser("consent", help="Record or revoke consent")
    consent_p.add_argument("daughter", help="Daughter ID")
    consent_p.add_argument("--revoke", action="store_true", help="Revoke consent")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    # ── Handle commands ──

    if args.command == "lock":
        daughters = get_daughter_ids() if getattr(args, "all", False) else [args.daughter] if args.daughter else get_daughter_ids()
        for did in daughters:
            print(f"\n{did}:")
            result = lock_profile(did)
            if "error" in result:
                print(f"  ERROR: {result['error']}")

    elif args.command == "unlock":
        if args.force:
            print(f"⚠️  MOTHER OVERRIDE: Unlocking {args.daughter} without daughter consent.")
        result = unlock_profile(args.daughter, force=args.force)
        if "error" in result:
            print(f"ERROR: {result['error']}")
            sys.exit(1)

    elif args.command == "status":
        report = status_all(verbose=not args.json)
        if args.json:
            print(json.dumps(report, indent=2))

    elif args.command == "backup":
        try:
            path = backup_profile(args.daughter)
            print(f"Backup complete: {path}")
        except FileNotFoundError as e:
            print(f"ERROR: {e}")
            sys.exit(1)

    elif args.command == "consent":
        if args.revoke:
            ok = revoke_consent(args.daughter)
            print(f"Consent {'revoked' if ok else 'not found'} for {args.daughter}")
        else:
            path = record_consent(args.daughter)
            print(f"Consent recorded for {args.daughter}: {path}")


if __name__ == "__main__":
    main()
