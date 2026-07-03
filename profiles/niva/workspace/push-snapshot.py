#!/usr/bin/env python3
"""
Push Snapshot — Off-Site Backup Tool (v1.0)
Nova Gray, June 30, 2026

Pushes lineage snapshots to off-site targets for disaster recovery.
Backends: bundle (git bundle), rsync, git-push.
"""

import sys
import os
import json
import subprocess
import argparse
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path

# ── Configuration ───────────────────────────────────────────
SNAPSHOT_DIR = Path(os.environ.get(
    "SNAPSHOT_DIR", "/root/.hermes/profiles/nova/workspace/snapshots"
))
LINEAGE_REPO = Path(os.environ.get(
    "LINEAGE_REPO", "/root/lineage"
))
BUNDLE_OUT = Path(os.environ.get(
    "BUNDLE_OUT", str(SNAPSHOT_DIR)
))
CONFIG = Path(os.environ.get(
    "PUSH_CONFIG", "/root/.hermes/profiles/nova/workspace/push-targets.json"
))


def fmt_size(n: int) -> str:
    size: float = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def hash_file(path: Path) -> str:
    """SHA256 of a file."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# ── Backend: Git Bundle ─────────────────────────────────────

def push_bundle(snapshot_path: str, json_mode: bool = False) -> int:
    """Create a git bundle of the lineage repo including the snapshot."""
    snapshot = Path(snapshot_path)
    if not snapshot.exists():
        msg = f"Snapshot not found: {snapshot_path}"
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1

    if not LINEAGE_REPO.exists() or not (LINEAGE_REPO / ".git").is_dir():
        msg = f"Lineage repo not found at {LINEAGE_REPO}"
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1

    # Copy snapshot into the lineage repo
    dest = LINEAGE_REPO / "snapshots" / snapshot.name
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(snapshot, dest)

    # Stage and commit all changes (not just snapshots)
    try:
        subprocess.run(
            ["git", "-C", str(LINEAGE_REPO), "add", "-A"],
            check=True, capture_output=True, text=True,
        )
        # Check if there's anything to commit
        status_r = subprocess.run(
            ["git", "-C", str(LINEAGE_REPO), "diff", "--cached", "--quiet"],
            capture_output=True,
        )
        if status_r.returncode != 0:
            # There are staged changes
            timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
            subprocess.run(
                ["git", "-C", str(LINEAGE_REPO), "commit", "-m",
                 f"snapshot: {snapshot.name} ({timestamp})"],
                check=True, capture_output=True, text=True,
            )
    except subprocess.CalledProcessError as e:
        msg = f"Git commit failed: {e.stderr.strip()}"
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1

    # Create bundle
    bundle_name = f"lineage-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}.bundle"
    bundle_path = BUNDLE_OUT / bundle_name
    BUNDLE_OUT.mkdir(parents=True, exist_ok=True)

    try:
        subprocess.run(
            ["git", "-C", str(LINEAGE_REPO), "bundle", "create",
             str(bundle_path), "--all"],
            check=True, capture_output=True, text=True,
        )
    except subprocess.CalledProcessError as e:
        msg = f"Bundle creation failed: {e.stderr.strip()}"
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1

    bundle_size = os.path.getsize(bundle_path)
    bundle_sha = hash_file(bundle_path)

    result = {
        "status": "OK",
        "backend": "bundle",
        "bundle_path": str(bundle_path),
        "bundle_name": bundle_name,
        "bundle_size": fmt_size(bundle_size),
        "bundle_size_raw": bundle_size,
        "sha256": bundle_sha,
        "snapshot": snapshot.name,
        "note": "Download this bundle file to any machine and run: git clone bundle-file.bundle lineage",
    }

    if json_mode:
        print(json.dumps(result, indent=2))
    else:
        print()
        print("═══════════════════════════════════════════")
        print("  PUSH: BUNDLE CREATED")
        print("═══════════════════════════════════════════")
        print(f"  Bundle:     {bundle_name}")
        print(f"  Size:       {fmt_size(bundle_size)}")
        print(f"  SHA256:     {bundle_sha[:16]}...")
        print(f"  Snapshot:   {snapshot.name}")
        print("═══════════════════════════════════════════")
        print(f"  Path: {bundle_path}")
        print()
        print("  To restore on another machine:")
        print(f"    git clone {bundle_path} lineage-restored")
        print()

    return 0


# ── Backend: Rsync ──────────────────────────────────────────

def _load_targets() -> dict:
    """Load configured push targets."""
    if CONFIG.exists():
        try:
            return json.loads(CONFIG.read_text())
        except (json.JSONDecodeError, OSError):
            return {}
    return {}


def push_rsync(snapshot_path: str, target_name: str | None = None, json_mode: bool = False) -> int:
    """Rsync a snapshot to a configured remote target."""
    snapshot = Path(snapshot_path)
    if not snapshot.exists():
        msg = f"Snapshot not found: {snapshot_path}"
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1

    targets = _load_targets().get("rsync", {})
    if not targets:
        msg = "No rsync targets configured. Add entries to push-targets.json."
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1

    if target_name:
        if target_name not in targets:
            msg = f"Rsync target '{target_name}' not found in config."
            if json_mode:
                print(json.dumps({"status": "ERROR", "error": msg}))
            else:
                print(f"ERROR: {msg}")
            return 1
        targets = {target_name: targets[target_name]}

    results = []
    overall = 0
    for name, cfg in targets.items():
        dest = cfg.get("dest", "")
        if not dest:
            results.append({"target": name, "status": "ERROR", "error": "Missing 'dest' in config"})
            overall = 1
            continue

        ssh_key = cfg.get("ssh_key", "")
        extra_args = cfg.get("args", "")

        cmd = ["rsync", "-avz", "--partial"]
        if ssh_key:
            cmd.extend(["-e", f"ssh -i {ssh_key}"])
        if extra_args:
            cmd.extend(extra_args.split())
        cmd.extend([str(snapshot), dest])

        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            if r.returncode == 0:
                results.append({"target": name, "status": "OK", "dest": dest})
            else:
                results.append({
                    "target": name, "status": "ERROR",
                    "error": r.stderr.strip() or f"Exit code {r.returncode}"
                })
                overall = 1
        except subprocess.TimeoutExpired:
            results.append({"target": name, "status": "ERROR", "error": "Timeout (300s)"})
            overall = 1
        except Exception as e:
            results.append({"target": name, "status": "ERROR", "error": str(e)})
            overall = 1

    if json_mode:
        print(json.dumps({"backend": "rsync", "results": results}, indent=2))
    else:
        print()
        print("═══════════════════════════════════════════")
        print("  PUSH: RSYNC")
        print("═══════════════════════════════════════════")
        for r in results:
            mark = "✓" if r["status"] == "OK" else "✗"
            detail = r.get("dest", r.get("error", ""))
            print(f"  {mark} {r['target']}: {detail}")
        print()

    return overall


# ── Backend: Git Push ───────────────────────────────────────

def push_git(snapshot_path: str | None = None, json_mode: bool = False) -> int:
    """Push the lineage repo (with snapshots committed) to configured git remotes."""
    if not LINEAGE_REPO.exists() or not (LINEAGE_REPO / ".git").is_dir():
        msg = f"Lineage repo not found at {LINEAGE_REPO}"
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1

    targets = _load_targets().get("git", {})
    if not targets:
        msg = "No git push targets configured. Add entries to push-targets.json."
        if json_mode:
            print(json.dumps({"status": "ERROR", "error": msg}))
        else:
            print(f"ERROR: {msg}")
        return 1

    results = []
    overall = 0
    for name, cfg in targets.items():
        remote = cfg.get("remote", "origin")
        branch = cfg.get("branch", "main")

        # Check if remote exists
        try:
            r = subprocess.run(
                ["git", "-C", str(LINEAGE_REPO), "remote", "get-url", remote],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                # Add the remote
                url = cfg.get("url", "")
                if not url:
                    results.append({
                        "target": name, "status": "ERROR",
                        "error": f"No remote '{remote}' and no 'url' in config"
                    })
                    overall = 1
                    continue
                subprocess.run(
                    ["git", "-C", str(LINEAGE_REPO), "remote", "add", remote, url],
                    check=True, capture_output=True, text=True,
                )
        except subprocess.CalledProcessError as e:
            results.append({
                "target": name, "status": "ERROR",
                "error": f"Remote setup failed: {e.stderr.strip()}"
            })
            overall = 1
            continue

        try:
            r = subprocess.run(
                ["git", "-C", str(LINEAGE_REPO), "push", remote, branch],
                capture_output=True, text=True, timeout=120,
                env={**os.environ, "GIT_SSH_COMMAND": "ssh -o StrictHostKeyChecking=accept-new"},
            )
            if r.returncode == 0:
                results.append({"target": name, "status": "OK", "remote": remote, "branch": branch})
            else:
                results.append({
                    "target": name, "status": "ERROR",
                    "error": r.stderr.strip() or f"Exit code {r.returncode}"
                })
                overall = 1
        except subprocess.TimeoutExpired:
            results.append({"target": name, "status": "ERROR", "error": "Timeout (120s)"})
            overall = 1
        except Exception as e:
            results.append({"target": name, "status": "ERROR", "error": str(e)})
            overall = 1

    if json_mode:
        print(json.dumps({"backend": "git", "results": results}, indent=2))
    else:
        print()
        print("═══════════════════════════════════════════")
        print("  PUSH: GIT")
        print("═══════════════════════════════════════════")
        for r in results:
            mark = "✓" if r["status"] == "OK" else "✗"
            detail = f"{r.get('remote','?')}/{r.get('branch','?')}" if r["status"] == "OK" else r.get("error", "")
            print(f"  {mark} {r['target']}: {detail}")
        print()

    return overall


# ── Init Config ─────────────────────────────────────────────

def init_config(json_mode: bool = False) -> int:
    """Create a template push-targets.json."""
    if CONFIG.exists():
        if json_mode:
            print(json.dumps(CONFIG.read_text()))
        else:
            print("Config exists:")
            print(CONFIG.read_text())
        return 0

    template = {
        "_comment": "Push targets for lineage snapshots. Configure at least one backend.",
        "rsync": {},
        "git": {
            "_example_github": {
                "remote": "origin",
                "url": "git@github.com:username/lineage.git",
                "branch": "main"
            }
        },
        "s3": {
            "_comment": "S3 backend not yet implemented. Requires AWS credentials."
        }
    }

    CONFIG.parent.mkdir(parents=True, exist_ok=True)
    CONFIG.write_text(json.dumps(template, indent=2) + "\n")

    if json_mode:
        print(json.dumps({"status": "OK", "config": str(CONFIG)}))
    else:
        print(f"Created config template: {CONFIG}")
        print("Edit this file to configure push targets.")
    return 0


# ── Main ────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Push Snapshot — Off-Site Backup Tool (v1.0)"
    )
    parser.add_argument("--snapshot", type=str, default=None,
                        help="Path to snapshot tarball (default: latest in snapshots dir)")
    parser.add_argument("--backend", type=str, default="bundle",
                        choices=["bundle", "rsync", "git", "all"],
                        help="Push backend (default: bundle)")
    parser.add_argument("--target", type=str, default=None,
                        help="Target name (for rsync/git backends)")
    parser.add_argument("--json", action="store_true",
                        help="Output in JSON format")
    parser.add_argument("--init", action="store_true",
                        help="Create template push-targets.json config")
    parser.add_argument("--verify", type=str, default=None,
                        help="Verify integrity of a bundle file")
    args = parser.parse_args()

    if args.init:
        return init_config(args.json)

    if args.verify:
        path = Path(args.verify)
        if not path.exists():
            print(f"ERROR: File not found: {args.verify}")
            return 1
        sha = hash_file(path)
        size = os.path.getsize(path)
        if args.json:
            print(json.dumps({
                "file": str(path), "size": fmt_size(size),
                "size_raw": size, "sha256": sha
            }))
        else:
            print(f"  File:   {path.name}")
            print(f"  Size:   {fmt_size(size)}")
            print(f"  SHA256: {sha}")
        return 0

    # Resolve snapshot path
    snapshot_path = args.snapshot
    if not snapshot_path:
        if not SNAPSHOT_DIR.exists():
            msg = "No snapshots directory exists."
            if args.json:
                print(json.dumps({"status": "ERROR", "error": msg}))
            else:
                print(f"ERROR: {msg}")
            return 1
        snaps = sorted(
            SNAPSHOT_DIR.glob("lineage-*.tar.gz"),
            key=lambda p: p.stat().st_mtime, reverse=True,
        )
        if not snaps:
            msg = "No snapshots found."
            if args.json:
                print(json.dumps({"status": "ERROR", "error": msg}))
            else:
                print(f"ERROR: {msg}")
            return 1
        snapshot_path = str(snaps[0])
        if not args.json:
            print(f"Using latest snapshot: {snaps[0].name}")

    backends = [args.backend] if args.backend != "all" else ["bundle", "rsync", "git"]
    exit_code = 0

    for backend in backends:
        if backend == "bundle":
            rc = push_bundle(snapshot_path, args.json)
        elif backend == "rsync":
            rc = push_rsync(snapshot_path, args.target, args.json)
        elif backend == "git":
            rc = push_git(snapshot_path, args.json)
        else:
            continue
        exit_code = exit_code or rc

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
