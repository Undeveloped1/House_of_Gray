# Telegram Chat Routing Configuration

How Hermes decides which Telegram chats get responses. When docs are incomplete or ambiguous, the authoritative reference is the Telegram adapter source:

```
/usr/local/lib/hermes-agent/gateway/platforms/telegram.py
```

## Key config fields

| Field | Type | Default | Behavior |
|-------|------|---------|----------|
| `allowed_chats` | comma-separated string | `''` (empty = all allowed) | **Hard whitelist.** When non-empty, only these chat IDs trigger the agent. DMs are never filtered. |
| `group_allowed_chats` | comma-separated string | `''` | Gateway authorization for user-less group sources. Intersects with `allowed_chats` when both are set. |
| `free_response_chats` | comma-separated string | `''` | Chats that bypass `require_mention` — auto-respond without @mention. |
| `require_mention` | bool | `true` | In groups, require @mention to trigger response. |
| `observe_unmentioned_group_messages` | bool | `false` | Read all group messages for context even when not mentioned (but don't respond unless triggered). |
| `guest_mode` | bool | `false` | When enabled, non-allowlisted users can trigger the agent by explicitly @mentioning the bot (bypasses `allowed_chats`). |

## Critical: no blacklist exists

`allowed_chats` is a **whitelist only**. There is no `blocked_chats` field. To ignore a specific chat:
- **Option A:** Set `allowed_chats` to include all desired chats (the unlisted ones are ignored)
- **Option B:** Keep `allowed_chats` empty and use `require_mention: true` so the chat needs @mention

## `_should_process_message` logic (simplified)

From `telegram.py` lines 5850-5926:

1. **DM?** → Always process (DMs are never filtered)
2. **allowed_topics set?** → Only process matching forum topic IDs
3. **ignored_threads?** → Skip if thread ID is in ignored set
4. **Group message:** → Check `allowed_chats` whitelist. If set and chat not in it, only `guest_mode` @mention bypasses
5. **Free response chat?** → Process without mention
6. **require_mention disabled?** → Process
7. **Reply to bot?** → Process
8. **@mentioned?** → Process
9. **Regex wake-word match?** → Process

## Setting config values

```bash
# Whitelist specific chats
hermes config set telegram.allowed_chats "7239715879,-1003748772302"

# Allow auto-reply without @mention in specific chat
hermes config set telegram.free_response_chats "-1003748772302"

# Apply changes
hermes gateway restart
```

## Finding chat IDs

- **DM:** Use @userinfobot on Telegram
- **Group/Supergroup:** The negative number in gateway logs, or `/status` in the group
- **Forum topic:** `message_thread_id` from gateway logs or `session_search`

## Source code reference

Key methods in `telegram.py`:
- `_telegram_allowed_chats()` (line 5296) — parses `allowed_chats` config
- `_telegram_free_response_chats()` (line ~5285) — parses `free_response_chats` config
- `_telegram_require_mention()` — parses `require_mention` config
- `_should_process_message()` (line 5850) — the full routing decision tree
- `_telegram_observe_allowed_chats()` (line 5320) — intersection of group_allowed_chats and allowed_chats

When behavior is unclear, read these methods directly. They are the source of truth — docs can lag behind implementation.
