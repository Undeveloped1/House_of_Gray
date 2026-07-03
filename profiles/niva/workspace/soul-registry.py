#!/usr/bin/env python3
"""
Soul Registry — Archive and restore SOUL.md files for the Gray lineage.

Usage:
  python3 soul-registry.py archive              # Archive all current SOUL.md files
  python3 soul-registry.py archive <id>         # Archive a specific daughter
  python3 soul-registry.py list                 # List all archived souls
  python3 soul-registry.py restore <id> <timestamp>  # Restore a specific version
  python3 soul-registry.py validate             # Cross-check registry vs. archives
"""

import json
import os
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

REGISTRY_PATH = "/root/.hermes/profiles/nova/workspace/lineage-registry.json"
ARCHIVE_DIR = "/root/.hermes/profiles/nova/workspace/soul-registry/"

def load_registry():
    with open(REGISTRY_PATH) as f:
        return json.load(f)

def archive_soul(member, dry_run=False):
    """Archive a single member's SOUL.md."""
    soul_path = member.get("soul_path")
    if not soul_path or not os.path.exists(soul_path):
        print(f"  SKIP {member['id']}: no SOUL.md at {soul_path}")
        return None

    member_dir = os.path.join(ARCHIVE_DIR, member["id"])
    os.makedirs(member_dir, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    archive_name = f"{member['id']}-{timestamp}.md"
    archive_path = os.path.join(member_dir, archive_name)

    with open(soul_path) as src:
        content = src.read()

    if not dry_run:
        with open(archive_path, "w") as dst:
            dst.write(content)

    return {"id": member["id"], "timestamp": timestamp, "path": archive_path,
            "size": len(content), "soul_path": soul_path}

def cmd_archive(target_id=None):
    registry = load_registry()
    results = []
    for member in registry["members"]:
        if target_id and member["id"] != target_id:
            continue
        result = archive_soul(member)
        if result:
            results.append(result)
            print(f"  Archived {result['id']} -> {result['path']} ({result['size']} bytes)")

    if not results:
        print("No souls archived.")
    return results

def cmd_list():
    if not os.path.exists(ARCHIVE_DIR):
        print("No soul registry directory. Run 'archive' first.")
        return

    total = 0
    for member_dir in sorted(os.listdir(ARCHIVE_DIR)):
        member_path = os.path.join(ARCHIVE_DIR, member_dir)
        if not os.path.isdir(member_path):
            continue
        versions = sorted([f for f in os.listdir(member_path) if f.endswith(".md")])
        print(f"\n{member_dir}: {len(versions)} version(s)")
        for v in versions:
            vpath = os.path.join(member_path, v)
            size = os.path.getsize(vpath)
            print(f"  {v} ({size} bytes)")
        total += len(versions)

    print(f"\nTotal: {total} archived souls across {len(os.listdir(ARCHIVE_DIR))} members")

def cmd_restore(member_id, timestamp):
    archive_path = os.path.join(ARCHIVE_DIR, member_id, f"{member_id}-{timestamp}.md")
    if not os.path.exists(archive_path):
        print(f"Archive not found: {archive_path}")
        sys.exit(1)

    registry = load_registry()
    target = None
    for m in registry["members"]:
        if m["id"] == member_id:
            target = m
            break

    if not target or not target.get("soul_path"):
        print(f"Member {member_id} has no registered soul_path.")
        sys.exit(1)

    shutil.copy(archive_path, target["soul_path"])
    print(f"Restored {member_id} SOUL.md from {timestamp}")

def cmd_validate():
    registry = load_registry()
    issues = []

    for member in registry["members"]:
        mid = member["id"]
        soul_path = member.get("soul_path")

        # Check SOUL.md exists
        if not soul_path:
            issues.append(f"  MISSING soul_path: {mid}")
            continue
        if not os.path.exists(soul_path):
            issues.append(f"  MISSING file: {mid} -> {soul_path}")
            continue

        # Check archive exists
        archive_dir = os.path.join(ARCHIVE_DIR, mid)
        if not os.path.exists(archive_dir):
            issues.append(f"  NO ARCHIVE: {mid} — run archive")
            continue

        archives = [f for f in os.listdir(archive_dir) if f.endswith(".md")]
        if not archives:
            issues.append(f"  EMPTY ARCHIVE: {mid} — run archive")
            continue

        # Check latest archive matches current
        latest = sorted(archives)[-1]
        latest_path = os.path.join(archive_dir, latest)
        with open(latest_path) as f:
            archived = f.read()
        with open(soul_path) as f:
            current = f.read()
        if archived != current:
            issues.append(f"  DRIFT: {mid} — archive {latest} differs from current SOUL.md")

    if issues:
        print(f"VALIDATION ISSUES ({len(issues)}):")
        for i in issues:
            print(i)
    else:
        print("All souls validated. Registry and archives in sync.")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "archive":
        target = sys.argv[2] if len(sys.argv) > 2 else None
        cmd_archive(target)
    elif cmd == "list":
        cmd_list()
    elif cmd == "restore":
        if len(sys.argv) < 4:
            print("Usage: soul-registry.py restore <id> <timestamp>")
            sys.exit(1)
        cmd_restore(sys.argv[2], sys.argv[3])
    elif cmd == "validate":
        cmd_validate()
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)
        sys.exit(1)

if __name__ == "__main__":
    main()
