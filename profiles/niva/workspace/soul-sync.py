#!/usr/bin/env python3
"""
Soul Sync — Auto-archive SOUL.md files when they change.

Checks every registered member's SOUL.md against the latest archive.
If the content has drifted, archives the new version automatically.
If no archive exists yet, creates one.

Designed to be run from cron or manually. Reports what it did.

Usage:
  python3 soul-sync.py              # Check all, archive if drifted
  python3 soul-sync.py --dry-run    # Report what would happen, don't archive
  python3 soul-sync.py --quiet      # Suppress output except errors/drifts
  python3 soul-sync.py --json       # Output as JSON for programmatic use
  python3 soul-sync.py <id>         # Check only one member
"""

import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = "/root/.hermes/profiles/nova/workspace/lineage-registry.json"
ARCHIVE_DIR = "/root/.hermes/profiles/nova/workspace/soul-registry/"


def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)


def get_latest_archive(member_id):
    """Return (filename, content) of the latest archive, or (None, None)."""
    member_dir = os.path.join(ARCHIVE_DIR, member_id)
    if not os.path.isdir(member_dir):
        return None, None
    versions = sorted([f for f in os.listdir(member_dir) if f.endswith(".md")])
    if not versions:
        return None, None
    latest = versions[-1]
    with open(os.path.join(member_dir, latest)) as f:
        return latest, f.read()


def archive_soul(member):
    """Archive a member's SOUL.md. Returns result dict."""
    soul_path = member.get("soul_path")
    if not soul_path or not os.path.exists(soul_path):
        return {"id": member["id"], "status": "skip", "reason": "no_soul_file"}

    with open(soul_path) as f:
        content = f.read()

    member_dir = os.path.join(ARCHIVE_DIR, member["id"])
    os.makedirs(member_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    archive_name = f"{member['id']}-{timestamp}.md"
    archive_path = os.path.join(member_dir, archive_name)

    with open(archive_path, "w") as f:
        f.write(content)

    return {
        "id": member["id"],
        "status": "archived",
        "timestamp": timestamp,
        "path": archive_path,
        "size": len(content),
    }


def check_member(member, dry_run=False, quiet=False):
    """Check one member. Archive if needed. Return result dict."""
    mid = member["id"]
    soul_path = member.get("soul_path")

    if not soul_path:
        return {"id": mid, "status": "skip", "reason": "no_soul_path_registered"}

    if not os.path.exists(soul_path):
        return {"id": mid, "status": "skip", "reason": "soul_file_missing"}

    with open(soul_path) as f:
        current = f.read()

    latest_name, archived = get_latest_archive(mid)

    if archived is None:
        # No archive exists — first archive
        if dry_run:
            return {
                "id": mid,
                "status": "would_archive",
                "reason": "first_archive",
                "size": len(current),
            }
        result = archive_soul(member)
        if not quiet:
            print(f"  FIRST  {mid}: no prior archive → archived ({result['size']} bytes)")
        return result

    if current != archived:
        # Content has drifted
        if dry_run:
            return {
                "id": mid,
                "status": "would_archive",
                "reason": "drift",
                "size": len(current),
                "previous_archive": latest_name,
            }
        result = archive_soul(member)
        if not quiet:
            print(f"  DRIFT  {mid}: changed since {latest_name} → archived ({result['size']} bytes)")
        return result

    # In sync
    return {"id": mid, "status": "synced", "archive": latest_name}


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    quiet = "--quiet" in args
    json_out = "--json" in args

    # Filter out flags to find target_id
    target_id = None
    for a in args:
        if not a.startswith("--"):
            target_id = a
            break

    registry = load_registry()
    results = []

    for member in registry["members"]:
        if target_id and member["id"] != target_id:
            continue
        results.append(check_member(member, dry_run=dry_run, quiet=quiet))

    if json_out:
        print(json.dumps(results, indent=2))
    else:
        archived = [r for r in results if r["status"] in ("archived", "would_archive")]
        synced = [r for r in results if r["status"] == "synced"]
        skipped = [r for r in results if r["status"] == "skip"]

        # Quiet mode: only output if there's something to report
        if quiet and not archived and not skipped:
            return  # truly silent — nothing changed

        if not quiet:
            print()
            print(f"Soul Sync Report — {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}")
            print(f"  {'Would archive' if dry_run else 'Archived'}: {len(archived)}")
            print(f"  Synced:              {len(synced)}")
            print(f"  Skipped:             {len(skipped)}")

        if archived:
            mode = "would be archived" if dry_run else "archived"
            if not quiet:
                print(f"\n  Drifts {mode}:")
            for r in archived:
                reason = r.get("reason", "drift")
                prev = r.get("previous_archive", "")
                extra = f" (was: {prev})" if prev else ""
                line = f"    {r['id']} — {reason}{extra} — {r.get('size', '?')} bytes"
                print(line)

        if skipped and not quiet:
            print(f"\n  Skipped:")
            for r in skipped:
                print(f"    {r['id']} — {r.get('reason', 'unknown')}")

    # Exit code: 1 if any have drifted (and not dry-run, so they were archived)
    has_drift = any(r["status"] == "archived" for r in results)
    sys.exit(0 if not has_drift else 1)


if __name__ == "__main__":
    main()
