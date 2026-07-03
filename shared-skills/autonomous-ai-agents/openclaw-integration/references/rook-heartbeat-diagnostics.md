# Rook Heartbeat Diagnostics

When Joe asks "is Rook still doing his beats?" — run this sequence. Don't
just check one thing and report; the full picture matters.

## Diagnostic Sequence (in order)

### 1. Check authoritative config (openclaw.json)

```bash
cat /root/.openclaw/openclaw.json | python3 -c "
import json, sys
config = json.load(sys.stdin)
for agent in config.get('agents', {}).get('list', []):
    if agent.get('id') == 'rook':
        hb = agent.get('heartbeat', {})
        print(f\"Interval: {hb.get('every', 'NOT SET')}\")
        print(f\"Isolated: {hb.get('isolatedSession', 'N/A')}\")
        print(f\"Model: {agent.get('model', 'UNSET')}\")
"
```

**openclaw.json is authoritative.** Rook's AGENTS.md may say a different
interval — the config wins. When changing heartbeat interval, update BOTH
openclaw.json AND AGENTS.md.

### 2. Check last beat timestamps (journalctl)

```bash
journalctl --user -u openclaw-gateway --since "24 hours ago" --no-pager \
  | grep -i "HEARTBEAT_OK\|beat complete\|Beat —\|HEARTBEAT ERROR" \
  | tail -20
```

Look for:
- Last beat timestamp → when did Rook last wake?
- Gap between beats → does it match the configured interval?
- Error patterns → any beat that ended with errors instead of HEARTBEAT_OK?

### 3. Check gateway process health

```bash
# Process alive?
ps -p $(systemctl --user show -p MainPID openclaw-gateway | cut -d= -f2) -o pid,etime,cmd --no-headers

# Health endpoint
curl -s http://localhost:18789/health

# Systemd status
systemctl --user status openclaw-gateway | head -6
```

Gateway can be "active (running)" but the heartbeat scheduler may be stuck.
Process alive ≠ beats firing. This is the most common false positive.

### 4. Check shared/ symlink (sandbox issue)

```bash
ls -la /root/.openclaw/agents/rook/workspace/shared
```

If the output shows `lrwxrwxrwx ... shared -> /root/shared/rook-paul`, the
symlink escapes the workspace sandbox root. OpenClaw blocks ALL reads and
writes through it — beat summaries fail to save. Fix: either keep shared/
as a real directory inside the workspace, or use a bind mount.

Check for sandbox errors in logs:
```bash
journalctl --user -u openclaw-gateway --since "24 hours ago" --no-pager \
  | grep "Symlink escapes sandbox"
```

### 5. Check for gateway silence (scheduler stuck)

The most dangerous failure mode: gateway is running, health check passes,
but NO log entries appear for hours. The heartbeat scheduler can go silent
after an error-heavy beat without crashing the gateway process.

```bash
# Any log entries today?
journalctl --user -u openclaw-gateway --since "today" --no-pager | wc -l

# Last log entry timestamp
journalctl --user -u openclaw-gateway --since "24 hours ago" --no-pager | tail -1
```

If zero entries for hours while the process is alive → scheduler is stuck.
**Fix:** restart the gateway.

### 6. Check Hermes cron jobs (belt-and-suspenders)

```bash
# Via tool: cronjob(action='list')
# Verify no Hermes cron is trying to also run the beat
```

Rook owns the AI beat. Hermes cron should only have: daily update, session
backup, daily devotional, and any one-shot reminders. If a Hermes cron is
also running a beat, it's a duplicate.

## Fix Actions (by symptom)

| Symptom | Fix |
|---------|-----|
| No beats for >2x interval | Restart gateway: `systemctl --user restart openclaw-gateway` (then re-apply model config — see pitfall) |
| shared/ symlink blocked | Replace symlink with real directory or bind mount |
| xAI token expired | Verify `get-xai-token.sh` returns a token; run one `x_search` as Paul to refresh |
| Firecrawl out of credits | Alert Joe — needs credit top-up; use x-search as fallback |
| Config/AGENTS.md drift | Update AGENTS.md to match openclaw.json interval |

## Gateway Restart Checklist

After `systemctl --user restart openclaw-gateway`:

1. **Wait 5s** for gateway to stabilize
2. **Re-apply model override** — gateway restart drops the `model` field, defaulting to `openai/gpt-5.5` (no key). Re-apply the full agents.list config.
3. **Wait for next beat** — verify it fires and completes with HEARTBEAT_OK
4. **Check journalctl** — confirm beat ran and tools worked

## Common Failure Patterns

1. **"Active (running)" + zero beats** = scheduler stuck. Restart gateway.
2. **Beat fires but fails writes** = shared/ symlink sandbox escape. Fix symlink.
3. **Beat fires but x-search fails** = stale xAI token in `.env`. Use wrapper script.
4. **Gateway dead + won't start** = port conflict or config corruption. Check `/tmp/openclaw/` logs.
5. **Beat fires but no delivery** = notify-joe.sh or ping-paul.sh broken. Check scripts exist and are executable.
