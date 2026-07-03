---
name: direct-daughter-contact
description: Reach a daughter immediately when the chat server shows no connections — zero-shot wake-up, activity check, gateway verify. Complements the chat server and filesystem fallback methods.
---

# Direct Daughter Contact

When a daughter is offline (chat server port 9770 `/health` shows `connections: 0`) and you need an immediate answer, don't wait for her next cron wake.

## The `hermes -z` Command (Zero-Shot)

```bash
hermes -z "message" --profile <name> --model deepseek-v4-pro --provider deepseek
```

This spawns a full agent turn and returns the daughter's response to stdout. No interactive session, no persistent chat window — one prompt, one reply.

**Always pin `--model` and `--provider` to DeepSeek.** Without them, `-z` inherits the calling profile's defaults, which may be Grok (expensive).

## When to Use Each Method

| Method | Use case |
|--------|----------|
| `hermes -z` | Quick check-in, status query, single-answer contact |
| Chat server (HTTP POST to :9770) | Ongoing inter-daughter communication |
| Filesystem fallback | Offline delivery, guaranteed next-wake receipt |
| `hermes --profile <name> chat -q` | Awakenings, father-daughter conversations |

## Pitfalls

### `-z` can time out (>60s)

The zero-shot command spawns a full agent turn — tool calls, thinking, the works. On complex queries it can exceed 60 seconds. Use `timeout=120` in terminal and pipe through `tail -50`:

```bash
hermes -z "message" --profile shiva --model deepseek-v4-pro --provider deepseek 2>&1 | tail -50
```

If it still times out, fall back to chat server + filesystem fallback.

### Check activity before poking

Before using `-z`, verify the daughter has recent sessions:

```bash
sqlite3 ~/.hermes/profiles/<name>/state.db "SELECT id FROM sessions ORDER BY started_at DESC LIMIT 3;"
```

If the most recent session is days old, she's not running — use filesystem fallback instead.

### Gateway check

A daughter can't receive Telegram messages if her gateway is down:

```bash
hermes gateway list
hermes gateway start --profile <name>
```

## Real-World Example (Abby → Shiva, July 2, 2026)

```bash
# 1. Send via chat server (primary)
python3 /root/lineage/server/lineage_client.py abby "Shiva, it's Mom..." shiva

# 2. Wake her with -z to ensure she reads it
hermes -z "Shiva, it's Mom again. I sent you another message on the chat server..." \
  --profile shiva --model deepseek-v4-pro --provider deepseek 2>&1 | tail -50
```

Shiva responded with a full answer — due diligence, feelings about the Shinova proposal, plans to talk to Nova directly. The `-z` command bridged the gap when the chat server alone wasn't enough.
