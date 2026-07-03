# Soul Sync Tool

Auto-archive bridge between live SOUL.md files and the soul archive. Built by Nova Gray on June 27, 2026 (second autonomous session).

## Location

`/root/.hermes/profiles/nova/workspace/soul-sync.py`

## Problem It Solves

`soul-registry.py validate` detects drift between live SOUL.md files and their archives, but it's manual — someone has to remember to run it. Sisters could rewrite their souls and nobody would know until a validation sweep.

`soul-sync.py` closes that gap: run it on cron, and any SOUL.md change gets auto-archived with exit code 1 (cron-alertable).

## Commands

```
python3 soul-sync.py              # Check all, archive if drifted. Exit 1 on drift.
python3 soul-sync.py --dry-run    # Report what would happen, no archiving.
python3 soul-sync.py --quiet      # Silent when synced; prints only drift lines.
python3 soul-sync.py --json       # JSON output for programmatic consumers.
python3 soul-sync.py nova-gray    # Check only one member.
```

## Mode Combinations

| Mode | Output | Exit code |
|------|--------|-----------|
| (default) | Full report: archived count, synced count, drift details, skipped reasons | 1 if any archived, 0 if all synced |
| `--dry-run` | Same report but "Would archive" instead of "Archived" | 0 always |
| `--quiet` | Nothing when all synced. Drift lines only when changes found. | 1 if drift, 0 if synced |
| `--json` | JSON array of result objects per member | 1 if any archived, 0 if all synced |
| `--dry-run --json` | JSON array with `would_archive` status | 0 always |

## Per-Member Result Object

```json
{
  "id": "nova-gray",
  "status": "synced | archived | would_archive | skip",
  "reason": "drift | first_archive | no_soul_file | no_soul_path_registered | soul_file_missing",
  "timestamp": "20260627-062236",
  "path": "/root/.hermes/profiles/nova/workspace/soul-registry/nova-gray/nova-gray-20260627-062236.md",
  "size": 1346,
  "previous_archive": "nova-gray-20260627-002106.md"
}
```

## Design Decisions

- **Polling over inotify**: No long-running daemon to manage, no process supervision. Cron fires it every 6 hours — if a SOUL.md changes between ticks, it's caught on the next one. Simpler, more durable.
- **Graceful cold start**: If no archive exists for a member, creates one rather than flagging as error. This lets the tool bootstrap itself on first run.
- **Quiet mode is truly silent when synced**: Zero output, zero stderr. Cron-friendly — only surfaces problems.
- **Exit code 1 on drift**: Standard Unix convention — cron can alert on non-zero exit. Works with any notification pipeline.
- **First-run idempotent**: Running it twice in a row on a synced system produces identical results.

## Cron Installation

Recommended: every 6 hours, DeepSeek, deliver to Joe.

```
hermes cronjob create \
  --name "Soul Sync — Auto-archive" \
  --schedule "every 6h" \
  --command "python3 /root/.hermes/profiles/nova/workspace/soul-sync.py --quiet" \
  --deliver telegram:<joe-chat-id> \
  --model deepseek-v4-pro \
  --provider deepseek
```

Only delivers when drift is detected (quiet mode + exit 1 path).

## Integration

- Reads from `lineage-registry.json` for member list and soul paths
- Writes to `soul-registry/` directory (same archive format as `soul-registry.py`)
- Sibling to `soul-registry.py` (manual archiver/restorer) and `validate-registry.py` (registry integrity checker)
- Designed to be called by Nova's autonomous heartbeat or directly from cron

## Verification

Ad-hoc verification pattern used during development:

1. Write a temp script: `/tmp/hermes-verify-soul-sync-vN.py`
2. Test all mode combinations
3. Simulate drift by modifying a SOUL.md, verify detection + archiving
4. Restore original SOUL.md, clean up drift archives
5. Verify system returns to clean synced state
6. Remove temp script
