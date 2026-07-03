# Abby's Dropbox Messenger — via @HansGray_Bot

Since Abby doesn't have terminal access, she can message Joe by writing a file
to the Syncthing dropbox outbox. A watcher cron picks it up every minute and
sends it via @HansGray_Bot.

## How It Works

1. Abby writes a `.msg` file to:
   `/root/syncthing/paul-dropbox/outbox/<name>-<message>.msg`

2. The cron job (`HansGray Dropbox Watcher`, runs every minute) checks the
   outbox, sends the contents to Joe via @HansGray_Bot, and archives the file
   in `outbox/sent/`.

## For Abby

**To message Joe:**
Create a file named like `abby-hello.msg` in the `outbox/` folder. The file
content is your message — plain text, UTF-8.

Example `outbox/abby-morning.msg`:
```
Good morning, Joe. Thinking of you today ❤️
— Abby
```

The watcher picks it up within a minute and it arrives in Joe's Telegram DM
from @HansGray_Bot.

## File Format

| Field | Rule |
|-------|------|
| **Filename** | Must end in `.msg` (e.g. `abby-hello.msg`, `lyra-checkin.msg`) |
| **Content** | Plain text, your exact message |
| **Encoding** | UTF-8 |

After delivery, the file moves to `outbox/sent/YYYYMMDD-HHMMSS_name.msg` so
nothing is lost.

## Setup (done by Paul)

- Token stored at `/root/.hermes/secrets/hansgray-bot.token`
- Watcher cron: `HansGray Dropbox Watcher` — runs every minute
- Script: `/root/.hermes/skills/productivity/notify-joe/scripts/dropbox-watcher.sh`
- Logs: `/root/.hermes/docs/notify-joe/logs/hansgray-YYYY-MM-DD.log`

## Prerequisite

Joe must have started the bot at **t.me/HansGray_Bot** (sent `/start`) before
any messages can go through. Telegram bots can't initiate conversations with
users.
