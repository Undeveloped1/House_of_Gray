# Rook delivery routing (Joe lock 2026-06-20)

## Rule

OpenClaw watcher agents use **two outbound channels**, not one funnel through Paul:

| Kind | Script | Destination |
|------|--------|-------------|
| Reminders, notifications, personal nudges, short beat highlights | `./notify-joe.sh` | Joe DM via @Rook_PaulBot |
| Relay "Joe says…", vault/action, tcg review, complex follow-up | `./ping-paul.sh` | Hermes webhook → Paul session |
| Group posts (AI Power Hour, etc.) | **Neither** | Paul/Hermes cron only — Rook never posts to groups |

**Default for heartbeat due items:** `notify-joe.sh` unless HEARTBEAT.md or Joe explicitly says ping Paul.

## notify-joe.sh

Install from `scripts/notify-joe.sh` in this skill into
`~/.openclaw/agents/<name>/workspace/notify-joe.sh`, `chmod +x`.

- Reads Rook bot token from `/root/.openclaw/openclaw.json` (`channels.telegram.botToken`) — no separate token file.
- `CHAT_ID` = Joe's Telegram user ID (pairing-approved DM).
- Verify: `./notify-joe.sh "test"` → JSON `{"ok":true,...}` and message in Joe's Rook DM.

## AGENTS.md table (copy into watcher workspace)

```markdown
## Delivery routing

| Kind | Tool |
|------|------|
| Joe DM — reminders, notifications | `./notify-joe.sh "..."` |
| Paul — brain, vault, relay | `./ping-paul.sh "..."` |
| Groups | Never Rook |
```

## SOUL chain (corrected)

Do **not** write "Paul filters what reaches Joe" for Rook. Paul filters **work**; Joe gets **personal pings** directly from Rook.

## Pitfall: routing reminders through Paul

Waking Paul for "remind Joe to call vendor" wastes tokens and adds latency. Joe asked for Rook to ping him directly for notification/reminder class items — encode that in AGENTS + SOUL + HEARTBEAT, not only in memory.