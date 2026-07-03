# Gateway Health Check — Systematic Diagnostic Sequence

When a user reports the gateway is broken (spinning clock, no response, can't communicate),
run this checklist in order. Each step either rules out a failure mode or finds the root
cause. Do NOT skip steps or jump to restart — the goal is diagnosis first.

## 1. Check if gateway process exists

```bash
ps aux | grep -E 'hermes.*gateway' | grep -v grep
```

If nothing returns, the gateway is dead. Start it: `hermes gateway run` (foreground) or
`hermes gateway start` (service). Skip to step 6.

If you see a `hermes dashboard` process on port 9119, that's the Web UI, NOT the gateway.
The gateway process looks like `python -m hermes_cli.main gateway run`.

## 2. Check service status (systemd)

```bash
systemctl --user status hermes-gateway 2>/dev/null
# or
systemctl status hermes-gateway 2>/dev/null
```

**If "not found" or "not installed":** The gateway is running as a raw process, not a
managed service. This is common — the gateway may have been started manually or via
`hermes dashboard` which auto-launches it. The raw process is perfectly functional;
the missing service is cosmetic unless you need auto-restart on crash. To install:

```bash
hermes gateway install
```

## 3. Check port binding

```bash
ss -tlnp | grep hermes
```

The gateway and dashboard bind to different ports:
- Gateway: typically loopback-only (port varies, often random)
- Dashboard/WebUI: port 9119 on 127.0.0.1
- Webhook server: port 8644 (Tailscale IP) if configured

If nothing listens where you expect, the gateway didn't start correctly.

## 4. Health check

```bash
curl -s -o /dev/null -w "HTTP %{http_code} in %{time_total}s\n" http://127.0.0.1:9119/health
```

Port 9119 is the dashboard. A 200 response means Hermes is alive. Note the response time —
if it's >5s, something is contending for resources.

## 5. Check logs for errors

```bash
# Gateway log (canonical source)
tail -50 ~/.hermes/logs/gateway.log

# Error log (warnings + errors across all components)
tail -30 ~/.hermes/logs/errors.log

# Key patterns to grep for
grep -E "(error|ERROR|timeout|429|retry|Broken pipe|stale)" ~/.hermes/logs/gateway.log | tail -20
```

**Critical signal — "Broken pipe":** Stream stale for 180s → killed connection. Usually a
provider-side issue (DeepSeek, OpenRouter, etc.), not the gateway itself. The gateway will
retry automatically.

**Critical signal — "cross-process write":** Cache invalidation messages like:
```
Agent cache invalidated for session ... : message_count changed (X -> Y), possible cross-process write
```
This means TWO processes are fighting over the same session (e.g., TUI gateway and main
Telegram gateway both polling the same Telegram DM). The session keeps resetting its cache
and responses may be slow or duplicate. Fix: identify the competing process and stop one.
See **Cross-Process Session Collision** section below.

## 6. Direct Telegram API test (bypass gateway entirely)

This is the SINGLE MOST VALUABLE TEST. It proves the bot token works and Telegram API is
reachable, independent of the gateway. If this works but the gateway doesn't, the problem
is inside the gateway. If this fails, the problem is the bot token or Telegram API.

```bash
# Get the bot token (may be redacted in tool output — that's fine, the curl still works)
source ~/.hermes/.env 2>/dev/null

# Send a test message to Joe's DM
curl -s -X POST "https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage" \
  -H "Content-Type: application/json" \
  -d '{"chat_id": "7239715879", "text": "🔧 Gateway pipe test — reply if you see this."}'
```

**Interpreting results:**
- `{"ok":true, "result":{"message_id":2651,...}}` — token works, API accessible, message
  delivered. The gateway should be working. Check for gateway-specific issues.
- `{"ok":false, "description":"Unauthorized"}` — token is wrong or revoked
- `{"ok":false, "description":"chat not found"}` — wrong chat ID or user never messaged bot
- Connection error / timeout — network issue or Telegram API down

## 7. Check event loop health (advanced)

If the gateway process exists but seems unresponsive:

```bash
# Check process state — 'S' (sleeping) is normal, 'D' (uninterruptible I/O) is a problem
ps -p <pid> -o pid,stat,etime,cputime,%cpu,%mem,args --no-headers

# Trace what the event loop is doing
timeout 3 strace -p <pid> -e trace=epoll_wait -c 2>&1
```

A healthy gateway will show hundreds of epoll_wait calls per second. If epoll_wait returns
zero calls, the event loop is hung.

## 8. Check for competing processes (session collision)

When the same user has both TUI (Hermes desktop/TUI) and Telegram connected, both gateways
poll the same Telegram chat. This causes constant cache invalidations:

```bash
# Look for the pattern
grep "cross-process write" ~/.hermes/logs/gateway.log | tail -10
# Example output:
# message_count changed (19 -> 47), possible cross-process write
```

**Fix:** Stop the TUI session or the stale gateway worker. Identify the competing process:

```bash
ps aux | grep hermes | grep -v grep
# Look for tui_gateway workers or duplicate gateway processes
```

## Cross-Process Session Collision

**Symptom:** User on Telegram sees spinning clocks, intermittent responses, or messages
that arrive out of order. Gateway log shows frequent "cross-process write" invalidations
on the same session ID.

**Root cause:** Two Hermes processes both polling the same Telegram chat. Common scenario:
- Main gateway (Telegram) running in background
- TUI gateway worker spawned for slash commands or desktop app

Both processes update the session's message count, causing the other's cache to invalidate.
This cycle repeats every time either process reads a new message.

**Fix:** Identify and stop the competing process. If the user is on Telegram, stop the TUI
worker. If the user is on TUI, stop the Telegram gateway for that session.

## Telegram Polling Conflict ("Conflict: terminated by other getUpdates request")

**Symptom:** User sees spinning clock, messages don't deliver. Gateway log shows:
```
WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram polling conflict (1/5)
— previous session still held open on Telegram's servers. Waiting 20s for it to expire.
Error: Conflict: terminated by other getUpdates request; make sure that only one bot instance is running
```

**Root cause:** Two processes are long-polling the SAME Telegram bot token. Telegram only
allows one active `getUpdates` connection per bot. When a second process polls, it kicks
the first one, which then retries and kicks the second — ping-pong conflict.

**Common triggers:**
- A second Hermes profile's gateway using the same bot token (e.g., Abby's gateway cloned
  from Paul's `.env` without changing `TELEGRAM_BOT_TOKEN`)
- TUI slash worker spawning a Telegram connection while the main gateway already holds one
- Old gateway process that didn't fully release its long-poll before a new one started

**Diagnosis:**
```bash
# Check for multiple gateway processes
ps aux | grep "gateway run" | grep -v grep

# Check if they're using the same bot token (compare token prefix lengths)
grep TELEGRAM_BOT_TOKEN ~/.hermes/.env
grep TELEGRAM_BOT_TOKEN ~/.hermes/profiles/*/.env 2>/dev/null

# Check gateway log for the conflict pattern
grep "getUpdates" ~/.hermes/logs/gateway.log | tail -5
```

**Fix:** Identify which process is the interloper and stop it. If a second profile's
gateway is using the wrong token, fix that profile's `.env`. If a TUI worker is
competing, stop the worker. The conflict auto-resolves within ~20 seconds after the
offending process releases the connection, but recurring conflicts indicate a config
problem.

**Prevention:** When creating a new profile that needs Telegram, generate a SEPARATE
bot via @BotFather (e.g., @AbbyHermBot vs @DrPaulStoneBot). Never reuse the same bot
token across profiles — Telegram enforces single-poll per token at the API level.

## Common Pitfalls

- **Don't restart the gateway as the first response.** Restarting drops the current session
  and loses diagnostic state. Diagnose first, restart only if the gateway is actually dead.
- **Port 9119 is the dashboard, not the gateway.** The dashboard is a Web UI. The gateway
  is a separate process. Both can be running or stopped independently.
- **"Gateway service is not installed" is not an error.** Raw process mode is fully
  functional. The `hermes gateway install` command is for systemd auto-restart on crash.
- **Model slowness ≠ gateway failure.** A 50-second model response looks like a dead
  gateway to the user (spinning clock on Telegram). Check the gateway log — if you see
  "response ready: ... time=50.5s", the gateway was fine, the model was slow.
- **DeepSeek "Broken pipe" stalls.** Stream stale for 180s → retry. This is normal
  provider behavior. The gateway handles retries automatically. Not a gateway bug.
- **"Gateway service is not installed" is not a problem.** The gateway runs as a raw
  process by default. `hermes gateway install` adds systemd management but isn't required
  for function. Check `ps aux | grep gateway` before assuming it's dead.
