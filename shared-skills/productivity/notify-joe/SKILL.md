---
name: notify-joe
description: Send Telegram DMs to Joe (and anyone) — a shared messaging tool for the whole lineage. Abby, Nova, Shiva, Lyra, Rook, Paul — anyone who needs to reach Joe can use this.
version: 1.1.0
---

# notify-joe

A shared messaging utility for the Gray lineage. Send Telegram messages to Joe
(or any contact) from any agent, script, or cron job.

## Bots Available

| Bot | Token | Used By | Purpose |
|-----|-------|---------|---------|
| OpenClaw bot | From OpenClaw config | Rook, Paul | System messages, cron deliveries |
| **@HansGray_Bot** | `/root/.hermes/secrets/hansgray-bot.token` | Family lineage (Abby, Nova, Lyra, Shiva) | Personal messages to Joe |

## Files

| File | Purpose |
|------|---------|
| `scripts/hans-message.sh` | **Primary** — sends via @HansGray_Bot to Joe |
| `scripts/notify-joe.sh` | Sends via OpenClaw bot to Joe |
| `scripts/notify-telegram.sh` | Generic — send to any Telegram chat_id via OpenClaw bot |
| `scripts/dropbox-watcher.sh` | Cron script — watches Syncthing dropbox for Abby's .msg files |
| `references/abby-dropbox.md` | Dropbox-watcher instructions for Abby and other non-terminal companions |

## Quick Start — Terminal Agents (Paul, Nova, Rook, Shiva)

```bash
# DM Joe via @HansGray_Bot (family channel)
./scripts/hans-message.sh "Hey Joe, just checking in ❤️"

# DM Joe via OpenClaw bot (system channel)
./scripts/notify-joe.sh "System: Rook beat complete"

# Send to anyone via OpenClaw bot
./scripts/notify-telegram.sh 7239715879 "Hello from Nova!"
```

## Quick Start — Abby (no terminal, uses Syncthing dropbox)

Write a `.msg` file to the dropbox outbox:

```
/root/syncthing/paul-dropbox/outbox/abby-morning-001.msg
```

Contents: the message text. A cron watcher (`HansGray Dropbox Watcher`, every
minute) picks it up, sends via @HansGray_Bot, and moves to `sent/`.

See `references/abby-dropbox.md` for full instructions.

## Dropbox Watcher Cron

- **Job name:** `HansGray Dropbox Watcher`
- **Schedule:** Every minute (`* * * * *`)
- **Type:** `no_agent` script
- **Script:** `dropbox-watcher.sh` (in `~/.hermes/scripts/`)
- **Outbox:** `/root/syncthing/paul-dropbox/outbox/`
- **Archive:** `outbox/sent/`

## Prerequisite

Joe must have started @HansGray_Bot at **t.me/HansGray_Bot** before any
messages can go through. Telegram bots cannot initiate conversations.

## Delivery History

All sent messages logged to:
`/root/.hermes/docs/notify-joe/logs/YYYY-MM-DD.log`
