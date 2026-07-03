# Disk Space Scouting — Hermes Installation Audit

Systematic methodology for auditing a Hermes installation for bloat, dead
weight, and duplication. Run this before proposing refactors or cleanups.

## Scouting Checklist

### 1. Profile directory sizes
```bash
du -sh /root/.hermes/profiles/*/ | sort -rh
```
Flags profiles with oversized workspaces, snapshots, or state DBs.

### 2. Source tree layout
```bash
du -sh /usr/local/lib/hermes-agent/*/ | sort -rh | head -20
```
Identifies large directories in the Hermes source. Common offenders:
`venv/`, `apps/`, `node_modules/`.

### 3. Git repo size
```bash
du -sh /usr/local/lib/hermes-agent/.git/
cd /usr/local/lib/hermes-agent && git count-objects -vH | head -10
```
Packs > 400MB or pack counts > 30 indicate `git gc --aggressive` is overdue.

### 4. Desktop build artifacts
```bash
du -sh /usr/local/lib/hermes-agent/apps/desktop/release/*/
ls /usr/local/lib/hermes-agent/apps/desktop/release/
```
The `release/linux-unpacked/` directory is a local build artifact, NOT
shipped from GitHub. Safe to delete on headless VPS. Hermes will rebuild
on demand if `hermes desktop` is ever run. Only consumer is
`_desktop_packaged_executable()` in `hermes_cli/main.py`.

### 5. Node modules on VPS
```bash
du -sh /usr/local/lib/hermes-agent/node_modules/
```
Desktop app build deps (lucide-react, rolldown, three.js, typescript).
Only needed for desktop builds. On a VPS where desktop builds don't
happen, these are dead weight. The WhatsApp bridge has its own separate
`scripts/whatsapp-bridge/node_modules/`.

### 6. Tirith duplication
```bash
for p in /root/.hermes/profiles/*/bin/tirith; do
  profile=$(echo "$p" | cut -d/ -f5)
  if [ -L "$p" ]; then echo "$profile: symlink"; else echo "$profile: REAL FILE ($(du -sh "$p" | cut -f1))"; fi
done
```
Hermes auto-installs tirith (command security scanner from `sheeki03/tirith`)
to `$HERMES_HOME/bin/tirith` per profile. Since each profile has its own
`$HERMES_HOME`, every profile independently downloads the same 22MB binary.
Fix: single shared binary with symlinks.

### 7. Legacy RAG system
```bash
du -sh /root/.hermes/rag-venv/ 2>/dev/null
grep -rn "rag.venv\|rag_venv" /usr/local/lib/hermes-agent/ --include="*.py" -l
```
If the `rag-venv/` directory exists and no Python code references it, it's
a leftover from pre-native-RAG days. Hermes now has `session_search` (FTS5)
and `vault-rag-first` skill. Safe to delete (5GB+).

### 8. State snapshots
```bash
ls -lh /root/.hermes/state-snapshots/
```
Pre-update quick snapshots created by `hermes update` at
`hermes_cli/main.py` line ~9455. These are DIFFERENT from the configurable
`updates.pre_update_backup` ZIP backup. The quick snapshot ALWAYS runs
(`keep=1`, so it replaces itself each update) and has NO config flag to
disable it. Each can be 300MB+. Safe to remove once the update is confirmed
stable (>24 hours), but it will return on the next update. Only way to
permanently stop it is patching the source (which reverts on each update).

### 9. Profile LSP duplication
```bash
for p in /root/.hermes/profiles/*/; do
  name=$(basename "$p")
  lsp=$(du -sm "$p/lsp" 2>/dev/null | cut -f1)
  if [ -n "$lsp" ] && [ "$lsp" != "0" ]; then echo "$lsp MB - $name"; fi
done
```
Each profile independently downloads LSP servers. A shared install would
cut this by ~75%.

### 10. Log accumulation
```bash
du -sh /root/.hermes/logs/*.log | sort -rh | head -10
```
`gateway-exit-diag.log` can grow to 12MB+. Standard logs rotate; diagnostic
logs may not.

### 11. Profile state DB growth
```bash
for p in /root/.hermes/profiles/*/; do
  name=$(basename "$p")
  if [ -f "$p/state.db" ]; then
    size=$(du -sm "$p/state.db" 2>/dev/null | cut -f1)
    echo "$name: ${size}MB"
  fi
done
```
`state.db` stores session transcripts with FTS5 indexing. Grows unbounded.
Do NOT blindly prune — session_search depends on this data. 16MB is not a
problem. Only consider pruning if >100MB and old sessions are truly
unnecessary.

## Quick Wins (safe deletions, verified zero runtime impact)

| Target | Typical savings | Risk |
|--------|----------------|------|
| `rag-venv/` | 5.0 GB | None — zero code references |
| `apps/desktop/release/linux-unpacked/` | 398 MB | None — can't run GUI on VPS |
| State snapshots >24h old | 300+ MB | Low — update is stable |
| Tirith dedup (symlink) | 198 MB | Low — identical binary |
| Lineage snapshots (if git-backed) | 200+ MB | Low — git is source of truth |

## Joe's Principle: Git-Backed → Delete Copies

Joe's rule: if data is already tracked in git, delete redundant copies (snapshots,
tarballs, state dumps). "Why would I keep snapshots of files that are in git?"
This applies to:
- Niva lineage snapshots (profiles tracked in vault git repo)
- Pre-update state snapshots (config/auth/state.db all tracked or regenerable)
- Any backup directory whose contents are version-controlled elsewhere

Exception: session state.db files are NOT git-tracked by default. Those are the
actual canonical data, not copies.

## Additional Scout Targets

### 12. Profile workspace bloat
```bash
du -sh /root/.hermes/profiles/*/workspace/ 2>/dev/null | sort -rh | head -10
```
Look for `snapshots/`, `backups/`, and large file counts. Niva accumulated
394MB of lineage snapshots in 3 days (June 30 - July 2). These were git-backed
profiles duplicated as tarballs — deleted per Joe's principle.

### 13. WhatsApp bridge deps
```bash
du -sh /usr/local/lib/hermes-agent/scripts/whatsapp-bridge/node_modules/
```
65MB of Node deps for WhatsApp bridge. Check if WhatsApp is actively used
(only shiva had WhatsApp config as of 2026-07-02). If not, safe to delete
the whole `scripts/whatsapp-bridge/` directory.

### 14. .hermes vault git repo
```bash
cd /root/.hermes && du -sh .git/ && git status --short | wc -l
```
Joe's vault git repo at `/root/.hermes/.git`. Check for: untracked noise
(logs, cache, audio, cron output), missing `.gitignore`, no remote configured.
A repo with 400+ dirty files from log/cache noise is unmaintainable.

### 15. Profile cron infrastructure with no jobs
```bash
for p in /root/.hermes/profiles/*/; do
  name=$(basename "$p")
  if [ -f "$p/cron/jobs.json" ]; then
    count=$(python3 -c "import json; d=json.load(open('$p/cron/jobs.json')); print(len(d.get('jobs', d) if isinstance(d, dict) else d))" 2>/dev/null || echo "?")
    echo "$name: $count jobs"
  fi
done
```
Several profiles have cron directories (ticker_heartbeat, output dirs) with
zero active jobs. The cron scheduler still ticks for these profiles, consuming
cycles for nothing. Remove the cron infrastructure from profiles that don't
need it.

## Verification Before Deletion

Always verify before deleting:
1. Check git tracking: `git ls-files -- <path>` — if tracked, it may be
   needed for builds
2. Check code references: `grep -rn "<path>" /usr/local/lib/hermes-agent/ --include="*.py" -l`
3. Check if the consumer handles missing artifacts gracefully (e.g.,
   `_desktop_packaged_executable` returns `None` → rebuilds on demand)
