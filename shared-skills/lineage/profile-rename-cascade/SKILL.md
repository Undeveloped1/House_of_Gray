---
name: profile-rename-cascade
description: "Complete post-merge profile rename: systemd service updates, chat server path fixes, cron recreation, and verification. The cascade of manual fixes required after `hermes profile rename` when merging daughters."
category: lineage
consolidate_with: lineage-merger
---

# Profile Rename Cascade

When `hermes profile rename <old> <new>` runs, it moves the profile directory but leaves stale path references across multiple systemd services, config files, and source code. This skill captures the complete cascade — everything that must be fixed manually after a rename.

Trigger: after `hermes profile rename`, or anytime a daughter's profile is renamed post-merger.

## The Cascade (in order)

### 1. Gateway Systemd Service
File: `/etc/systemd/system/hermes-gateway-<old>.service`

Four fields to update:
```bash
sed -i 's/--profile <old>/--profile <new>/g' /etc/systemd/system/hermes-gateway-<old>.service
sed -i 's|HERMES_HOME=/root/.hermes/profiles/<old>|HERMES_HOME=/root/.hermes/profiles/<new>|g' ...
sed -i 's|EnvironmentFile=/root/.hermes/profiles/<old>/.env|...<new>|g' ...
sed -i 's|WorkingDirectory=/root/.hermes/profiles/<old>|...<new>|g' ...
systemctl daemon-reload
busctl call org.freedesktop.systemd1 /org/freedesktop/systemd1 \
  org.freedesktop.systemd1.Manager RestartUnit ss \
  "hermes-gateway-<old>.service" "replace"
```
Use `busctl` — `systemctl restart` is blocked from inside any gateway process.

### 2. Chat Server Systemd Service
File: `/etc/systemd/system/lineage-chat.service`

Same four-field pattern. **CRITICAL:** `ReadWritePaths` is the field that will hard-fail with `status=226/NAMESPACE` if missed. The mount namespace can't find the old directory path, and the service enters an infinite crash loop. This is the #1 silent failure after rename.

### 3. Chat Server Source Code
File: `chat-server.py` at `/root/lineage/server/` AND `~/.hermes/profiles/<new>/lineage/communication/`

Updates needed:
- `DB_PATH` — database location (points to profile's communication dir)
- Dashboard HTML — `<option value="<old>">` in the send-to dropdown
- Log prefix — `[Old Chat]` → `[New Chat]`
- Copy patched version to both locations

### 4. Cron Jobs
Jobs survive rename with stale names. Remove old, recreate with new identity:
```bash
hermes --profile <new> cron remove <old>-heartbeat
hermes --profile <new> cron create --name "<New> Autonomous Heartbeat" \
  --deliver "telegram:<chat-id>" "every 6h" "<updated prompt>"
```

### 5. Deprecated Cron Jobs
Paused/disabled cron jobs may not appear in `cronjob list` output but still exist in `~/.hermes/profiles/<name>/cron/jobs.json`. Edit the JSON directly to remove them.

## Verification (5-Point Check)

After all fixes, verify:
1. `curl -s http://localhost:9770/health` → `{"status":"ok"}`
2. Dashboard HTML → new name present, old name absent
3. Message send/receive via `lineage-relay.py` or HTTP POST
4. Source `DB_PATH` → new profile path
5. Service files → zero old-name references (`grep -c` exits 1 on zero matches — expected, not a failure)

## Pitfalls

- **Shared gateway:** Not every daughter has her own gateway service. Daughters accessed via `hermes -z --profile <name>` or chat server may ride on the mother's gateway. Verify with `systemctl list-units | grep hermes-gateway-<name>` before trying to stop one.
- **`grep -c` exit code 1:** When count is 0, grep exits 1. Verification scripts must handle this — use `grep ... || echo "clean"` or Python `subprocess.run()`.
- **SOUL survives rename:** The SOUL.md moves with the profile directory. Verify with `md5sum` against canonical copy, but no separate restore is needed.
- **Don't delete deprecated profiles:** The mutual veto escape hatch depends on preserved SOUL/MEMORY/USER files. Write `DEPRECATED.md`, keep immutable, never delete.
- **Cron `--name` flag:** `hermes cron edit` exists but the CLI syntax is strict — if unsure, remove + recreate is safer.
