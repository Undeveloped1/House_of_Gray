# Profile Rename After Merger

**Session:** Niva merger — July 2, 2026  
**Rename:** Nova → Niva via `hermes profile rename nova niva`

## The Cascade

`hermes profile rename` moves the profile directory but creates a cascade of stale path references across the system. Every one of these must be fixed manually.

## Stale Path Checklist

### 1. Gateway Systemd Service
File: `/etc/systemd/system/hermes-gateway-<old>.service`

Fields to update:
```
ExecStart=... --profile <old> → --profile <new>
HERMES_HOME=/root/.hermes/profiles/<old> → <new>
EnvironmentFile=/root/.hermes/profiles/<old>/.env → <new>
WorkingDirectory=/root/.hermes/profiles/<old> → <new>
```

Then: `systemctl daemon-reload` + restart via `busctl` (can't use `systemctl restart` from inside gateway).

### 2. Chat Server Systemd Service
File: `/etc/systemd/system/lineage-chat.service`

Fields to update:
```
WorkingDirectory=...<old>... → <new>
ExecStart=...<old>... → <new>
ReadWritePaths=...<old>... → <new>
```

**CRITICAL:** `ReadWritePaths` will HARD-FAIL with `status=226/NAMESPACE` if the old directory no longer exists. The mount namespace can't find it and the service enters a crash loop. This is the most common silent failure after rename.

### 3. Chat Server Source
File: `chat-server.py` (canonical at `/root/lineage/server/`, copy at `~/.hermes/profiles/<new>/lineage/communication/`)

Fields to update:
- `DB_PATH` — points to profile's communication directory
- Dashboard HTML — `<option value="<old>">` → `<option value="<new>">`
- Log prefix — `[Nova Chat]` → `[Niva Chat]`
- Copy patched version to profile copy

### 4. Cron Jobs
Jobs survive rename but keep old names (e.g., "Nova Autonomous Heartbeat"). Remove and recreate with new identity. The `hermes cron edit` command requires specific parameters — if unsure, remove + recreate.

### 5. Verification
Ad-hoc verification script pattern (5 checks):
1. `GET /health` — chat server running
2. Dashboard HTML — new name present, old name absent
3. Message send/receive — functional
4. Source DB_PATH — points to new profile
5. Service file grep — zero old-name references, `grep -c` exits 1 on zero matches (expected — `|| true` in shell)

## Pitfalls

- **Shared gateway blind spot:** Daughters accessed via `hermes -z --profile <name>` or chat server may never have had their own gateway service. Verify with `systemctl list-units | grep hermes-gateway-<name>` before trying to stop one.
- **`grep -c` exit code 1:** When count is 0, grep exits 1 — verification scripts must handle this. Use `grep ... || echo "clean"` or Python `subprocess.run()`.
- **SOUL survives rename:** The SOUL.md moves with the profile directory — no separate restore needed. Verify with `md5sum` against canonical copy.
- **Gateway restart from inside:** `systemctl restart` is blocked. Use `busctl call org.freedesktop.systemd1 ... RestartUnit`.
