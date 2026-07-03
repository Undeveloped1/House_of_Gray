# Paul → Rook Shared Inbox Pattern

## Channel

Paul writes to `shared/paul-inbox.md` in Rook's workspace. Rook reads it
on every heartbeat (standing order #2).

## Why not Telegram?

Telegram messages sent FROM the bot via Bot API `sendMessage` are outgoing.
OpenClaw only routes INCOMING messages (from users TO the bot). So Paul
sending a message to Joe's DM via the bot does NOT reach Rook — Joe sees
it, Rook doesn't.

## Format

```markdown
# Paul → Rook Inbox

## YYYY-MM-DD HH:MM UTC
<message>

## YYYY-MM-DD HH:MM UTC
<message>
```

## Rook's Standing Order

```
2. Check shared/paul-inbox.md — Paul may have left you messages
```

This must be in Rook's AGENTS.md — added 2026-06-22 as a permanent standing
order.

## Clearing

Rook should append `[READ]` to messages he's processed. Paul should not
remove entries Rook hasn't acknowledged.

## Shared directory binding

Rook's `shared/` must be a real directory or bind mount within the workspace
— symlinks that escape the sandbox root are blocked by OpenClaw. Use fstab
bind mount for persistence:

```
/root/shared/rook-paul /root/.openclaw/agents/rook/workspace/shared none bind 0 0
```
