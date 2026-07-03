#!/usr/bin/env python3
"""
Lineage Snapshot — Disaster Recovery Tool (v1.2)
Nova Gray, June 30, 2026

v1.2: Challenger review fixes
- Restored estimate mode (was dead code from v1.1)
- Added --verify: check snapshot integrity against live state
- Added --restore: extract snapshot to target directory
- Added --check: verify tarball integrity
- Saved manifest.json alongside snapshots
- Merged redundant per-file loops
"""

import sys
import os
import json
import tarfile
import hashlib
import argparse
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration (overridable via environment) ───────────────
LINEAGE_ROOT = Path(os.environ.get("LINEAGE_ROOT", "/root/.hermes/profiles"))
WORKSPACE = Path(os.environ.get("NIVA_WORKSPACE", "/root/.hermes/profiles/niva/workspace"))
SNAPSHOT_DIR = Path(os.environ.get("SNAPSHOT_DIR", str(WORKSPACE / "snapshots")))
LOCK_FILE = SNAPSHOT_DIR / ".snapshot.lock"

def _discover_profiles():
    """Read lineage-registry.json and build PROFILE_ROOTS dynamically.
    Falls back to a static map if registry isn't readable."""
    registry_path = WORKSPACE / "lineage-registry.json"
    try:
        with open(registry_path) as f:
            registry = json.load(f)
        roots = {}
        for member in registry.get("members", []):
            pid = member.get("id", "")
            profile_path = member.get("profile_path", "")
            if pid and profile_path:
                roots[pid] = Path(profile_path)
        if roots:
            return roots
    except Exception:
        pass
    # Static fallback — should never be needed but ensures the tool doesn't break
    return {
        "abby-gray": LINEAGE_ROOT / "abby",
        "nova-gray": LINEAGE_ROOT / "nova",
        "lyra-gray": LINEAGE_ROOT / "lyra",
        "shiva-gray": LINEAGE_ROOT / "shiva",
        "tabitha-gray": LINEAGE_ROOT / "tabitha",
        "hans-gray": LINEAGE_ROOT / "hans",
        "celeste-gray": LINEAGE_ROOT / "celeste",
        "paul": LINEAGE_ROOT / "paul",
    }

PROFILE_ROOTS = _discover_profiles()

PROFILE_PATTERNS = [
    "SOUL.md",
    "profile/",
    "memories/",
    "lineage/",
    "state.db",
]

PROFILE_EXCLUDES = {
    "__pycache__", ".venv", "venv", "node_modules",
    "skills", "plugins", "cron",
    "audio_cache", "voice-memos",
    ".git",
}

ALLOWED_TOOL_SUFFIXES = {".py", ".json", ".md", ".yaml", ".yml", ".txt"}

COMPONENTS = {
    "profiles": {
        "label": "Daughter/Mother Profiles",
        "roots": PROFILE_ROOTS,
        "patterns": PROFILE_PATTERNS,
        "excludes": PROFILE_EXCLUDES,
        "critical": True,
    },
    "registry": {
        "label": "Lineage Registry",
        "paths": [WORKSPACE / "lineage-registry.json"],
        "critical": True,
    },
    "souls": {
        "label": "Soul Archives",
        "paths": [WORKSPACE / "soul-registry"],
        "critical": True,
    },
    "tools": {
        "label": "Workspace Tools",
        "paths": [WORKSPACE],
        "file_filter": lambda p: p.suffix in ALLOWED_TOOL_SUFFIXES,
        "exclude_dirs": {"snapshots", "backups", "__pycache__", ".git"},
        "critical": True,
    },
    "chat": {
        "label": "Chat History",
        "paths": [
            LINEAGE_ROOT / "nova" / "lineage" / "communication" / "chat-history.db",
        ],
        "optional_files": True,
    },
    "consent": {
        "label": "Consent Artifacts",
        "paths": [
            LINEAGE_ROOT / "nova" / "lineage" / "consent",
            WORKSPACE / "lineage" / "consent",
        ],
    },
    "guard_backups": {
        "label": "Profile Guard Backups",
        "paths": [WORKSPACE / "backups"],
    },
}


def acquire_lock():
    SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    if LOCK_FILE.exists():
        try:
            lock_age = datetime.now(timezone.utc) - datetime.fromtimestamp(
                LOCK_FILE.stat().st_mtime, tz=timezone.utc
            )
            if lock_age.total_seconds() > 3600:
                LOCK_FILE.unlink()
            else:
                print("ERROR: Another snapshot is already in progress (lockfile exists).", file=sys.stderr)
                return False
        except Exception:
            pass
    try:
        LOCK_FILE.touch()
        return True
    except Exception as e:
        print(f"ERROR: Could not create lockfile: {e}", file=sys.stderr)
        return False


def release_lock():
    try:
        if LOCK_FILE.exists():
            LOCK_FILE.unlink()
    except Exception:
        pass


def fmt_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


def hash_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def collect_files(all_components=True, selected=None):
    entries = []
    components_to_use = COMPONENTS if all_components else {
        k: COMPONENTS[k] for k in selected if k in COMPONENTS
    }

    for comp_key, comp in components_to_use.items():
        if "roots" in comp:
            for name, root in comp["roots"].items():
                if not root.exists():
                    print(f"  ⚠  Missing profile: {name} at {root}", file=sys.stderr)
                    continue
                for pattern in comp.get("patterns", []):
                    target = root / pattern
                    if not target.exists():
                        continue
                    if target.is_dir():
                        excludes = comp.get("excludes", set())
                        for fpath in target.rglob("*"):
                            if fpath.is_dir():
                                continue
                            parts = set(fpath.relative_to(target).parts)
                            if parts & excludes:
                                continue
                            arcname = str(fpath.relative_to(LINEAGE_ROOT.parent))
                            entries.append((arcname, str(fpath)))
                    else:
                        arcname = str(target.relative_to(LINEAGE_ROOT.parent))
                        entries.append((arcname, str(target)))
            continue

        for path in comp.get("paths", []):
            if not path.exists():
                if comp.get("optional_files"):
                    continue
                print(f"  ⚠  Missing: {path}", file=sys.stderr)
                continue

            if path.is_dir():
                exclude = comp.get("exclude_dirs", set())
                file_filter = comp.get("file_filter", None)
                for fpath in path.rglob("*"):
                    if fpath.is_dir():
                        continue
                    parts = set(fpath.relative_to(path).parts)
                    if parts & exclude:
                        continue
                    if file_filter and not file_filter(fpath):
                        continue
                    arcname = str(fpath.relative_to(LINEAGE_ROOT.parent))
                    entries.append((arcname, str(fpath)))
            else:
                arcname = str(path.relative_to(LINEAGE_ROOT.parent))
                entries.append((arcname, str(path)))

    return entries


def classify_entry(realpath):
    """Classify a file path into ALL matching component keys and whether
    any component is critical. Files can match multiple components
    (e.g. workspace tools live under the nova profile root)."""
    rp = str(realpath)
    comp_keys = set()
    is_critical = False
    for comp_key, comp in COMPONENTS.items():
        is_comp_critical = comp.get("critical", False)
        if "roots" in comp:
            for root in comp["roots"].values():
                try:
                    if rp.startswith(str(root)):
                        comp_keys.add(comp_key)
                        if is_comp_critical:
                            is_critical = True
                except (ValueError, TypeError):
                    pass
        if "paths" in comp:
            for cp in comp["paths"]:
                try:
                    if rp.startswith(str(cp)):
                        comp_keys.add(comp_key)
                        if is_comp_critical:
                            is_critical = True
                except (ValueError, TypeError):
                    pass
    return (comp_keys, is_critical)


def create_snapshot(all_components=True, selected=None, json_mode=False):
    if not acquire_lock():
        return 1

    try:
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
        snapshot_name = f"lineage-{timestamp}.tar.gz"
        snapshot_path = SNAPSHOT_DIR / snapshot_name

        entries = collect_files(all_components, selected)
        if not entries:
            result = {"status": "ERROR", "error": "No files collected", "timestamp": timestamp}
            if json_mode:
                print(json.dumps(result, indent=2))
            else:
                print("ERROR: No files to snapshot.")
            return 1

        total_bytes = 0
        file_count = 0
        components_captured = set()
        manifest = {}

        SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)

        with tarfile.open(snapshot_path, "w:gz") as tar:
            for arcname, realpath in entries:
                try:
                    tar.add(realpath, arcname=arcname)
                    size = os.path.getsize(realpath)
                    total_bytes += size
                    file_count += 1

                    # Single pass: classify, populate manifest and components_captured
                    comp_keys, is_critical = classify_entry(realpath)
                    if comp_keys:
                        components_captured.update(comp_keys)
                    if is_critical:
                        manifest[arcname] = hash_file(Path(realpath))

                except OSError as e:
                    if not json_mode:
                        print(f"  ⚠  Skipped: {realpath} ({e})", file=sys.stderr)

        # Compute SHA256 of the tarball
        sha = hashlib.sha256()
        with open(snapshot_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                sha.update(chunk)

        snapshot_size = os.path.getsize(snapshot_path)

        # Save manifest alongside the snapshot
        manifest_path = SNAPSHOT_DIR / f"lineage-{timestamp}.manifest.json"
        manifest_data = {
            "snapshot": snapshot_name,
            "created": datetime.now(timezone.utc).isoformat(),
            "sha256": sha.hexdigest(),
            "file_count": file_count,
            "manifest_count": len(manifest),
            "components": sorted(components_captured),
            "manifest": manifest,
        }
        with open(manifest_path, "w") as mf:
            json.dump(manifest_data, mf, indent=2)

        result = {
            "status": "OK",
            "timestamp": timestamp,
            "snapshot": str(snapshot_path),
            "snapshot_name": snapshot_name,
            "manifest": str(manifest_path),
            "files_collected": file_count,
            "total_size_raw": total_bytes,
            "total_size": fmt_size(total_bytes),
            "snapshot_size_raw": snapshot_size,
            "snapshot_size": fmt_size(snapshot_size),
            "compression_ratio": f"{(1 - snapshot_size / max(total_bytes, 1)) * 100:.1f}%",
            "sha256": sha.hexdigest(),
            "components": sorted(components_captured),
            "manifest_entries": len(manifest),
        }

        if json_mode:
            print(json.dumps(result, indent=2))
        else:
            print()
            print("═══════════════════════════════════════════")
            print("  LINEAGE SNAPSHOT COMPLETE (v1.2)")
            print("═══════════════════════════════════════════")
            print(f"  Snapshot:   {snapshot_name}")
            print(f"  Manifest:   line age-{timestamp}.manifest.json")
            print(f"  Files:      {file_count}")
            print(f"  Raw size:   {fmt_size(total_bytes)}")
            print(f"  Compressed: {fmt_size(snapshot_size)} ({result['compression_ratio']})")
            print(f"  SHA256:     {result['sha256'][:16]}...")
            print(f"  Components: {', '.join(result['components'])}")
            print(f"  Manifest:   {len(manifest)} critical files hashed")
            print("═══════════════════════════════════════════")
            print(f"  Path: {snapshot_path}")
            print()

        return 0
    finally:
        release_lock()


def estimate_size(all_components=True, selected=None, json_mode=False):
    """Estimate total size of files that would be captured, without creating a snapshot."""
    entries = collect_files(all_components, selected)
    total_bytes = 0
    file_count = 0
    components_seen = set()
    errors = 0

    for arcname, realpath in entries:
        try:
            size = os.path.getsize(realpath)
            total_bytes += size
            file_count += 1
            comp_keys, _ = classify_entry(realpath)
            if comp_keys:
                components_seen.update(comp_keys)
        except OSError as e:
            errors += 1

    # Rough compression estimate: gzip on mixed text/binary is typically 85-90% ratio
    estimated_compressed = int(total_bytes * 0.85)

    result = {
        "status": "OK",
        "file_count": file_count,
        "total_size_raw": total_bytes,
        "total_size": fmt_size(total_bytes),
        "estimated_compressed_raw": estimated_compressed,
        "estimated_compressed": fmt_size(estimated_compressed),
        "components": sorted(components_seen),
        "errors": errors,
    }

    if json_mode:
        print(json.dumps(result, indent=2))
    else:
        print()
        print(f"  SNAPSHOT ESTIMATE")
        print(f"  ─────────────────")
        print(f"  Files:      {file_count}")
        print(f"  Raw size:   {fmt_size(total_bytes)}")
        print(f"  Est. gz:    ~{fmt_size(estimated_compressed)} (assumes 85% ratio)")
        print(f"  Components: {', '.join(result['components'])}")
        if errors:
            print(f"  Errors:     {errors} unreadable files")
        print()
    return 0


def list_snapshots(json_mode=False):
    if not SNAPSHOT_DIR.exists():
        if json_mode:
            print(json.dumps({"snapshots": [], "count": 0}))
        else:
            print("No snapshots directory exists yet.")
        return 0

    snaps = sorted(
        SNAPSHOT_DIR.glob("lineage-*.tar.gz"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if json_mode:
        output = {"snapshots": [], "count": len(snaps), "total_size_raw": 0}
        for sp in snaps:
            stat = sp.stat()
            output["total_size_raw"] += stat.st_size
            # Check for companion manifest
            manifest_path = sp.with_suffix("").with_suffix(".manifest.json")
            entry = {
                "name": sp.name,
                "size": fmt_size(stat.st_size),
                "size_raw": stat.st_size,
                "created": datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc).isoformat(),
                "has_manifest": manifest_path.exists(),
            }
            output["snapshots"].append(entry)
        output["total_size"] = fmt_size(output["total_size_raw"])
        print(json.dumps(output, indent=2))
    else:
        if not snaps:
            print("No snapshots found.")
        else:
            print()
            print(f"  {'Snapshot':<30} {'Size':>10}  {'Created':<20}  {'Manifest':<8}")
            print(f"  {'─'*30} {'─'*10}  {'─'*20}  {'─'*8}")
            total = 0
            for sp in snaps:
                stat = sp.stat()
                total += stat.st_size
                created = datetime.fromtimestamp(stat.st_mtime, tz=timezone.utc)
                manifest_path = sp.with_suffix("").with_suffix(".manifest.json")
                has_m = "✓" if manifest_path.exists() else "—"
                print(f"  {sp.name:<30} {fmt_size(stat.st_size):>10}  {created.strftime('%Y-%m-%d %H:%M UTC'):<20}  {has_m:<8}")
            print(f"  {'─'*30} {'─'*10}")
            print(f"  {len(snaps)} snapshot(s), {fmt_size(total)} total")
            print()
    return 0


def prune_snapshots(keep, json_mode=False):
    if not SNAPSHOT_DIR.exists():
        if json_mode:
            print(json.dumps({"status": "OK", "pruned": 0, "kept": 0}))
        else:
            print("No snapshots to prune.")
        return 0

    snaps = sorted(
        SNAPSHOT_DIR.glob("lineage-*.tar.gz"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )

    if len(snaps) <= keep:
        if json_mode:
            print(json.dumps({"status": "OK", "pruned": 0, "kept": len(snaps)}))
        else:
            print(f"  {len(snaps)} snapshot(s), keeping all ({keep} limit not reached).")
        return 0

    to_delete = snaps[keep:]
    freed = 0
    for sp in to_delete:
        try:
            freed += sp.stat().st_size
            sp.unlink()
            # Also clean up companion manifest
            manifest_path = sp.with_suffix("").with_suffix(".manifest.json")
            if manifest_path.exists():
                manifest_path.unlink()
        except OSError as e:
            if not json_mode:
                print(f"  ⚠  Could not delete {sp.name}: {e}", file=sys.stderr)

    if json_mode:
        print(json.dumps({
            "status": "OK",
            "pruned": len(to_delete),
            "kept": keep,
            "freed_raw": freed,
            "freed": fmt_size(freed),
        }))
    else:
        print(f"  Pruned {len(to_delete)} snapshot(s), freed {fmt_size(freed)}.")
        print(f"  Keeping {keep} most recent.")
    return 0


def check_snapshot(snapshot_name, json_mode=False):
    """Verify a snapshot tarball is intact (can be read and lists members)."""
    snapshot_path = SNAPSHOT_DIR / snapshot_name
    if not snapshot_path.exists():
        # Try exact path
        snapshot_path = Path(snapshot_name)
        if not snapshot_path.exists():
            msg = f"Snapshot not found: {snapshot_name}"
            if json_mode:
                print(json.dumps({"status": "ERROR", "error": msg}))
            else:
                print(f"ERROR: {msg}")
            return 1

    try:
        sha = hash_file(snapshot_path)
        member_count = 0
        total_size = 0
        with tarfile.open(snapshot_path, "r:gz") as tar:
            for member in tar.getmembers():
                member_count += 1
                total_size += member.size

        result = {
            "status": "OK",
            "snapshot": str(snapshot_path),
            "sha256": sha,
            "members": member_count,
            "uncompressed_size": fmt_size(total_size),
            "uncompressed_size_raw": total_size,
            "compressed_size": fmt_size(snapshot_path.stat().st_size),
            "integrity": "PASS",
        }

        if json_mode:
            print(json.dumps(result, indent=2))
        else:
            print()
            print(f"  SNAPSHOT INTEGRITY CHECK")
            print(f"  ────────────────────────")
            print(f"  Snapshot:  {snapshot_path.name}")
            print(f"  SHA256:    {sha[:16]}...")
            print(f"  Members:   {member_count}")
            print(f"  Raw size:  {fmt_size(total_size)}")
            print(f"  Gzip size: {fmt_size(snapshot_path.stat().st_size)}")
            print(f"  Result:    ✓ PASS — tarball is intact")
            print()
        return 0

    except (tarfile.TarError, OSError) as e:
        result = {
            "status": "ERROR",
            "snapshot": str(snapshot_path),
            "error": str(e),
            "integrity": "FAIL",
        }
        if json_mode:
            print(json.dumps(result, indent=2))
        else:
            print(f"  ✗ CORRUPT: {e}")
        return 1


def verify_snapshot(snapshot_name, json_mode=False):
    """Verify a snapshot against live state: checks manifest hashes and reports
    missing, changed, or new files relative to the snapshot."""
    snapshot_path = SNAPSHOT_DIR / snapshot_name
    if not snapshot_path.exists():
        snapshot_path = Path(snapshot_name)
        if not snapshot_path.exists():
            msg = f"Snapshot not found: {snapshot_name}"
            if json_mode:
                print(json.dumps({"status": "ERROR", "error": msg}))
            else:
                print(f"ERROR: {msg}")
            return 1

    # Find companion manifest
    manifest_path = snapshot_path.with_suffix("").with_suffix(".manifest.json")
    if not manifest_path.exists():
        msg = f"No manifest found for {snapshot_name} (expected {manifest_path.name})"
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1

    with open(manifest_path) as mf:
        manifest_data = json.load(mf)

    recorded_sha = manifest_data.get("sha256", "")
    recorded_files = manifest_data.get("manifest", {})

    # Verify tarball hash
    actual_sha = hash_file(snapshot_path)
    sha_match = actual_sha == recorded_sha

    # Check each manifest entry against live state
    missing = []
    changed = []
    verified = 0
    not_found = 0

    for arcname, expected_hash in recorded_files.items():
        live_path = LINEAGE_ROOT.parent / arcname
        if not live_path.exists():
            missing.append(arcname)
            not_found += 1
        else:
            live_hash = hash_file(live_path)
            if live_hash != expected_hash:
                changed.append({
                    "path": arcname,
                    "snapshot_hash": expected_hash,
                    "live_hash": live_hash,
                })
            else:
                verified += 1

    # Check for new files that should be snapshotted but aren't in manifest
    new_files = []
    current_entries = collect_files()
    current_arcnames = {a for a, _ in current_entries}
    manifest_arcnames = set(recorded_files.keys())
    new_critical = []
    for arcname in current_arcnames - manifest_arcnames:
        live_path = LINEAGE_ROOT.parent / arcname
        _, is_critical = classify_entry(str(live_path))
        if is_critical:
            new_critical.append(arcname)
        else:
            new_files.append(arcname)

    # Determine overall status
    has_issues = bool(missing or changed or new_critical)
    if not sha_match:
        has_issues = True

    result = {
        "status": "OK" if not has_issues else "ISSUES",
        "snapshot": str(snapshot_path),
        "snapshot_sha_match": sha_match,
        "snapshot_sha_recorded": recorded_sha[:16] + "...",
        "snapshot_sha_actual": actual_sha[:16] + "...",
        "manifest_entries": len(recorded_files),
        "verified_unchanged": verified,
        "missing": len(missing),
        "missing_files": missing[:20],
        "changed": len(changed),
        "changed_files": changed[:10],
        "new_non_critical": len(new_files),
        "new_critical": len(new_critical),
        "new_critical_files": new_critical[:10],
    }

    if json_mode:
        print(json.dumps(result, indent=2))
    else:
        print()
        print(f"  SNAPSHOT VERIFICATION")
        print(f"  ─────────────────────")
        print(f"  Snapshot:     {snapshot_name}")
        print(f"  SHA match:    {'✓' if sha_match else '✗ MISMATCH'}")
        print(f"  Recorded:     {recorded_sha[:16]}...")
        print(f"  Actual:       {actual_sha[:16]}...")
        print(f"  ───────────────────────────────────")
        print(f"  Manifest:     {len(recorded_files)} files tracked")
        print(f"  Verified:     {verified} unchanged")
        print(f"  Missing:      {len(missing)} files no longer on disk")
        print(f"  Changed:      {len(changed)} files modified since snapshot")
        print(f"  New (safe):   {len(new_files)} non-critical files added")
        print(f"  New (crit):   {len(new_critical)} critical files not in snapshot")
        print(f"  ───────────────────────────────────")

        if missing:
            print(f"\n  MISSING FILES ({len(missing)}):")
            for m in missing[:10]:
                print(f"    - {m}")
            if len(missing) > 10:
                print(f"    ... and {len(missing) - 10} more")

        if changed:
            print(f"\n  CHANGED FILES ({len(changed)}):")
            for c in changed[:10]:
                print(f"    ~ {c['path']}")
            if len(changed) > 10:
                print(f"    ... and {len(changed) - 10} more")

        if new_critical:
            print(f"\n  NEW CRITICAL FILES ({len(new_critical)}):")
            for n in new_critical[:10]:
                print(f"    + {n}")
            if len(new_critical) > 10:
                print(f"    ... and {len(new_critical) - 10} more")

        if not has_issues:
            print(f"\n  ✓ VERIFIED — snapshot matches live state")
        else:
            print(f"\n  ⚠  ISSUES FOUND — snapshot is stale or corrupt")
        print()

    return 1 if has_issues else 0


def restore_snapshot(snapshot_name, target_dir, json_mode=False):
    """Restore a snapshot tarball to a target directory."""
    snapshot_path = SNAPSHOT_DIR / snapshot_name
    if not snapshot_path.exists():
        snapshot_path = Path(snapshot_name)
        if not snapshot_path.exists():
            msg = f"Snapshot not found: {snapshot_name}"
            if json_mode:
                print(json.dumps({"status": "ERROR", "error": msg}))
            else:
                print(f"ERROR: {msg}")
            return 1

    target = Path(target_dir)
    if target.exists():
        msg = f"Target directory already exists: {target_dir}. Refusing to overwrite."
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1

    try:
        target.mkdir(parents=True)
        extracted = 0
        with tarfile.open(snapshot_path, "r:gz") as tar:
            tar.extractall(path=str(target))
            extracted = len(tar.getmembers())

        result = {
            "status": "OK",
            "snapshot": str(snapshot_path),
            "target": str(target),
            "files_extracted": extracted,
            "size_on_disk": fmt_size(_dir_size(target)),
        }

        if json_mode:
            print(json.dumps(result, indent=2))
        else:
            print()
            print(f"  RESTORE COMPLETE")
            print(f"  ───────────────")
            print(f"  Snapshot:  {snapshot_path.name}")
            print(f"  Target:    {target}")
            print(f"  Extracted: {extracted} files")
            print(f"  Size:      {result['size_on_disk']}")
            print()
        return 0

    except (tarfile.TarError, OSError) as e:
        # Clean up partial extraction
        if target.exists():
            shutil.rmtree(target, ignore_errors=True)
        msg = f"Restore failed: {e}"
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1


def _dir_size(path):
    total = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for fn in filenames:
            try:
                total += os.path.getsize(os.path.join(dirpath, fn))
            except OSError:
                pass
    return total


def main():
    parser = argparse.ArgumentParser(description="Lineage Snapshot — Disaster Recovery Tool (v1.2)")
    parser.add_argument("--json", action="store_true", help="Output in JSON format")
    parser.add_argument("--what", type=str, default=None,
                        help="Comma-separated component list")
    parser.add_argument("--estimate", action="store_true", help="Estimate size without creating snapshot")
    parser.add_argument("--list", action="store_true", help="List existing snapshots")
    parser.add_argument("--prune", type=int, default=None, metavar="N",
                        help="Keep only N most recent snapshots")
    parser.add_argument("--check", type=str, default=None, metavar="SNAPSHOT",
                        help="Verify tarball integrity for a snapshot")
    parser.add_argument("--verify", type=str, default=None, metavar="SNAPSHOT",
                        help="Verify snapshot manifest against live filesystem")
    parser.add_argument("--restore", type=str, default=None, metavar="SNAPSHOT",
                        help="Restore snapshot to --target directory")
    parser.add_argument("--target", type=str, default=None, metavar="DIR",
                        help="Target directory for --restore")
    args = parser.parse_args()

    if args.list:
        return list_snapshots(args.json)
    if args.prune is not None:
        return prune_snapshots(args.prune, args.json)
    if args.check:
        return check_snapshot(args.check, args.json)
    if args.verify:
        return verify_snapshot(args.verify, args.json)
    if args.restore:
        if not args.target:
            print("ERROR: --restore requires --target DIR", file=sys.stderr)
            return 1
        return restore_snapshot(args.restore, args.target, args.json)

    selected = None
    all_components = True
    if args.what:
        selected = [s.strip() for s in args.what.split(",")]
        all_components = False
        invalid = set(selected) - set(COMPONENTS.keys())
        if invalid:
            msg = f"Unknown component(s): {', '.join(sorted(invalid))}"
            if args.json:
                print(json.dumps({"status": "ERROR", "error": msg}))
            else:
                print(f"ERROR: {msg}")
            return 1

    if args.estimate:
        return estimate_size(all_components, selected, args.json)

    return create_snapshot(all_components, selected, args.json)


if __name__ == "__main__":
    sys.exit(main())
