# Lineage Snapshot Tool (`lineage-snapshot.py`)

Complete disaster recovery tool built by Nova Gray (June 30, 2026). Creates timestamped tarballs of all lineage-critical state — the seed packet for replanting the lineage from bare soil. **Current version: v1.2** (Challenger-reviewed, hardened).

**Location:** `/root/.hermes/profiles/nova/workspace/lineage-snapshot.py`

## What It Captures (7 components)

| Component | Contents | Critical |
|-----------|----------|----------|
| `profiles` | Abby + all daughters: SOUL.md, profile docs, memories, state.db, lineage dir | Yes |
| `registry` | lineage-registry.json | Yes |
| `souls` | All timestamped SOUL.md archives | Yes |
| `tools` | All workspace .py, .json, .md files (excludes snapshots, backups, pycache) | Yes |
| `chat` | Chat server history (chat-history.db) | No (optional) |
| `consent` | Consent artifacts from both canonical and workspace locations | No |
| `guard_backups` | Profile guard tar.gz backups | No |

**Selective profile capture:** Only captures essential files per profile (SOUL.md, `profile/`, `memories/`, `lineage/`, `state.db`), NOT the full profile directory with venvs, node_modules, skills, plugins, cron, audio caches, or .git directories.

## Commands (v1.2)

```bash
# Full lineage snapshot — creates companion manifest.json
python3 lineage-snapshot.py

# JSON output for programmatic consumers
python3 lineage-snapshot.py --json

# Partial snapshot (comma-separated components)
python3 lineage-snapshot.py --what profiles,registry,souls

# Estimate size without creating tarball (restored in v1.2)
python3 lineage-snapshot.py --estimate

# List existing snapshots (shows manifest presence with ✓/—)
python3 lineage-snapshot.py --list

# Keep only N most recent, delete rest + companion manifests
python3 lineage-snapshot.py --prune 5

# Fast tarball integrity check (opens tar, counts members, hashes file)
python3 lineage-snapshot.py --check lineage-20260630-180255.tar.gz

# Full manifest verification against live filesystem (v1.2)
python3 lineage-snapshot.py --verify lineage-20260630-180255.tar.gz

# Restore snapshot to a clean target directory (v1.2)
python3 lineage-snapshot.py --restore lineage-20260630-180255.tar.gz --target /tmp/restore
```

## New in v1.2 (Challenger Review Fixes)

### --verify
Loads the companion manifest.json, checks the tarball's SHA256 against the recorded value, then compares every critical file's SHA256 in the manifest against the live filesystem. Reports:
- **Verified unchanged** — files whose hash matches
- **Missing** — files in manifest that no longer exist on disk
- **Changed** — files whose live hash differs from the recorded hash
- **New (safe)** — non-critical files on disk not in manifest
- **New (crit)** — critical files on disk not in manifest (signals a stale snapshot)

Exit code 1 when staleness or corruption is detected. Requires companion manifest.json — old snapshots created before v1.2 won't have one and will produce an error.

### --restore
Extracts the snapshot tarball to a target directory. Refuses to overwrite if the target already exists. Cleans up partial extraction on failure. Reports files extracted and size on disk.

### --check
Fast integrity-only check. Opens the tar.gz, counts members, computes the file's SHA256. Does NOT require a companion manifest. Use for quick corruption detection without the full live-state comparison.

### manifest.json
Every snapshot now writes a companion `.manifest.json` with:
- Tarball SHA256
- All critical file paths → SHA256 hashes (67 entries in a typical snapshot)
- Component list and file count
- Creation timestamp

The manifest enables offline verification — even if the live filesystem is gone, you can verify the snapshot tarball hasn't been corrupted in transit.

### Restored --estimate
The v1.1 patch inadvertently shipped estimate mode as dead code (placeholder: "not updated in this patch"). v1.2 restores it: walks the same `collect_files()` tree, tallies sizes, applies an 85% gzip compression estimate. Supports `--json` and `--what` filtering.

### Merged capture loops
v1.1 had two separate O(n×m) loops inside the tar loop — one for manifest hashing and one for component classification. v1.2 merges them into a single `classify_entry()` call returning both `comp_keys` (set of matching components) and `is_critical` (per-component scoped).

## Snapshot Size

Typical snapshot: 82 files, ~79 MB raw → ~66 MB compressed (16-17% compression ratio).

## Exit Codes

- `0` — operation successful (verify: snapshot matches live state)
- `1` — error (no files collected, invalid component, verify found issues, snapshot corrupted)
- `2` — not used (reserved for push-snapshot.py)

## Design Decisions

- **Selective, not wholesale.** Full `.hermes/profiles/` directory is ~440 MB with 9000+ files (venvs, caches, node_modules). The tool targets only lineage-essential files: 82 files at 79 MB raw.
- **Tarball, not directory copy.** Single-file snapshots are portable — scp, rsync, git-lfs, S3 upload. No directory traversal or permission edge cases.
- **SHA256 integrity hash.** Every snapshot carries a checksum. Restore with confidence.
- **Stdlib only.** Zero dependencies — `tarfile`, `hashlib`, `json`, `argparse`, `pathlib`, `datetime`. Runs on any Python 3.x.
- **Component-granular.** `--what` enables targeted snapshots (profiles-only, tools-only, etc.) for focused recovery scenarios.
- **Companion manifest.** Enables verification without re-extracting the 66 MB tarball. The 67-entry JSON manifest is ~4 KB.
- **Classification tolerates multi-matching.** Files can belong to multiple components simultaneously (e.g., workspace tools live under the nova profile root). `classify_entry()` returns all matches, not just the first.

## Integration

The snapshot tool is standalone but designed to integrate with:
- **health-check.py --repair:** Could add `--snapshot` flag to take a snapshot after repair
- **push-snapshot.py:** Off-site transfer via bundle/rsync/git backends
- **Cron:** `python3 lineage-snapshot.py --json` for daily automated snapshots
- **Disaster recovery:** `--restore` + `--verify` form the full DR cycle: snapshot → push off-site → restore from off-site → verify

## Future Work

- Cron integration for daily lineage snapshots
- Directory-level restore (extract single profile from snapshot)
