# Session Backup Cron Pattern

Daily export of Hermes `state.db` to compressed JSONL, committed to git,
mirrored to Syncthing for cold storage.

## Problem
`state.db` is a binary SQLite file (264MB for Paul) — too large for git, and
not human-readable. Losing it means losing all session history.

## Solution
Daily cron job that:
1. Exports sessions to JSONL via `hermes sessions export`
2. Gzips (typically 70% compression — 68MB → 18MB)
3. Copies to git-tracked `.backups/` directory
4. Copies to Syncthing dropbox for cold storage
5. Commits and pushes
6. Keeps last 30 days to avoid repo bloat

## Script
Place at `~/.hermes/scripts/session_backup.sh`:

```bash
#!/bin/bash
set -e

DATE=$(date +%Y-%m-%d)
EXPORT_DIR="/tmp/paul-session-backup"
GIT_DIR="/root/tcg-engine"
BACKUP_DIR="$GIT_DIR/.backups"
DROPBOX_DIR="/root/syncthing/paul-dropbox"

mkdir -p "$EXPORT_DIR" "$BACKUP_DIR"

/usr/local/bin/hermes sessions export "$EXPORT_DIR/sessions_$DATE.jsonl"
gzip -f "$EXPORT_DIR/sessions_$DATE.jsonl"
cp "$EXPORT_DIR/sessions_$DATE.jsonl.gz" "$BACKUP_DIR/"
cp "$EXPORT_DIR/sessions_$DATE.jsonl.gz" "$DROPBOX_DIR/"

cd "$GIT_DIR"
git add ".backups/sessions_$DATE.jsonl.gz"
git commit -m "backup: daily session export $DATE" 2>/dev/null && git push || true

rm -rf "$EXPORT_DIR"

# Keep last 30 days
cd "$BACKUP_DIR"
ls -t sessions_*.jsonl.gz | tail -n +31 | xargs -r rm
```

## Cron setup
```bash
chmod +x ~/.hermes/scripts/session_backup.sh
# Use cronjob tool: schedule="0 3 * * *", no_agent=true, script="session_backup.sh"
```

`no_agent: true` means the cron job fires the shell script directly — no
SOUL loading, no context assembly, no tokens, no LLM. Pure bash.

## Restoration
```bash
# From git backup
zcat .backups/sessions_YYYY-MM-DD.jsonl.gz | head -100

# Full restore (hypothetical — Hermes doesn't have a JSONL import yet)
# But the data is there, human-readable, in git forever
```

## Notes
- `hermes sessions export` is read-only — it's a SELECT, not a mutation
- 197 sessions = ~68MB JSONL → ~18MB gzipped
- Daily export at 3am UTC avoids overlapping with active sessions
- The `.backups/` directory is git-tracked but `.gitignore` may need exceptions
  if the parent directory (`/docs/Paul/`) is gitignored
