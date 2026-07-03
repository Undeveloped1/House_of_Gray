# Push Snapshot Tool (push-snapshot.py)

Off-site backup tool for lineage snapshots. Companion to `lineage-snapshot.py`. Built by Nova Gray, June 30, 2026.

## Overview

`lineage-snapshot.py` creates disaster recovery tarballs. `push-snapshot.py` gets them off the VPS. Three backends, ordered by independence from external infrastructure:

| Backend | Requires | Output | Survives VPS loss? |
|---------|----------|--------|---------------------|
| `bundle` | Nothing — just git | Portable `.bundle` file | ✓ (download the file) |
| `rsync` | Target host + SSH | Remote copy | ✓ |
| `git` | Configured git remote | Remote push | ✓ |

## Commands

```bash
# Initialize config (creates push-targets.json template)
python3 push-snapshot.py --init

# Create git bundle (default — always available)
python3 push-snapshot.py --backend bundle --json

# Verify a bundle's integrity
python3 push-snapshot.py --verify lineage-20260630-140417.bundle

# Use latest snapshot (auto-detected)
python3 push-snapshot.py --backend bundle

# Specify a particular snapshot
python3 push-snapshot.py --snapshot snapshots/lineage-20260630-100528.tar.gz --backend bundle

# Push to all configured backends
python3 push-snapshot.py --backend all
```

## Bundle Backend (Always Available)

The bundle backend requires no external infrastructure — no git remote, no SSH target, no S3 bucket. It works as long as git is installed.

**How it works:**
1. Copies the snapshot tarball into `/root/lineage/snapshots/`
2. Stages and commits all changes (`git add -A`)
3. Skips commit if nothing changed (checks `git diff --cached --quiet`)
4. Creates a git bundle with `--all` (entire repo history)
5. Hashes the bundle with SHA256
6. Reports path, size, and integrity hash

**Restoring from a bundle:**
```bash
# On any machine with git:
git clone /path/to/lineage-<timestamp>.bundle lineage-restored
cd lineage-restored
# All directories present: mother/, nova/, lyra/, shiva/, tabitha/, snapshots/, server/, docs/
# All commits preserved: git log shows full history
```

**Design decisions:**
- `git add -A` (not just `snapshots/`) — ensures the bundle reflects complete lineage state, including any uncommitted profile/docs changes
- No-force commit: skips if nothing to commit (handles re-runs gracefully)
- Bundle is a single portable file: scp it, download it, email it, put it on a USB stick
- Restore is vanilla `git clone` — no special tools needed on the receiving end

## Rsync Backend

Requires a configured target in `push-targets.json`:

```json
{
  "rsync": {
    "backup-server": {
      "dest": "user@192.168.1.100:/backups/lineage/",
      "ssh_key": "/root/.ssh/backup_key",
      "args": "--bwlimit=10M"
    }
  }
}
```

Rsyncs the snapshot tarball directly to the remote destination. Supports SSH key authentication, bandwidth limiting, and any rsync flags via `args`.

## Git Push Backend

Requires a configured git remote in `push-targets.json`:

```json
{
  "git": {
    "github": {
      "remote": "origin",
      "url": "git@github.com:username/lineage.git",
      "branch": "main"
    }
  }
}
```

Pushes the `/root/lineage/` repo (with all snapshots committed) to the configured remote. Auto-adds the remote if it doesn't exist. Uses SSH with `StrictHostKeyChecking=accept-new`.

## Configuration

Config file at `push-targets.json` in the workspace directory. Template created by `--init`:

```json
{
  "_comment": "Push targets for lineage snapshots.",
  "rsync": {},
  "git": {
    "_example_github": {
      "remote": "origin",
      "url": "git@github.com:username/lineage.git",
      "branch": "main"
    }
  },
  "s3": {
    "_comment": "S3 backend not yet implemented."
  }
}
```

## Integration

Designed to run after `lineage-snapshot.py`:

```bash
python3 lineage-snapshot.py && python3 push-snapshot.py --backend all
```

In autonomous workflows, run both from a single heartbeat or chain them. The bundle stays in `workspace/snapshots/` alongside the tarball — it lives until manually pruned alongside the snapshots it wraps.
