# Ephemeral (No-Record) Profile Pattern

How to create a Hermes profile that leaves no trace between sessions.

## When to Use

- Experimental profiles you don't want polluting your memory/session history
- Profiles that run one-off investigations
- Any profile where "no record" is a hard requirement

## Configuration

### 1. Create the profile

```bash
hermes profile create <name> --no-skills --no-alias
```

### 2. Disable memory

In `config.yaml`:
```yaml
memory:
  memory_enabled: false
  user_profile_enabled: false
```

### 3. Auto-prune sessions

Watchdog script at `~/.hermes/scripts/<name>_purge.sh`:

```bash
#!/bin/bash
hermes -p <name> sessions prune --older-than 0 --yes 2>&1
```

Create a recurring cronjob:

```
schedule: every 5m
no_agent: true
script: <name>_purge.sh
deliver: local
```

### 4. SOUL: no identity, no record, pure execution

The SOUL should instruct the profile to:
- Never write to memory
- Never create files unless explicitly directed
- Delete its own session at close: `hermes -p <profile> sessions delete <session_id> --yes`
- Communicate concisely — no greeting, no closing, no emoji

## Known Limitation

Sessions still exist in state.db between cronjob ticks (up to 5 minutes). For truly zero-record operation, combine with the SOUL's self-delete instruction at session close.

## Worked Example: Abby

Created 2026-06-22. Profile at `~/.hermes/profiles/abby/`. Config disables memory + user profile. Cronjob `28b1e8abe9a1` prunes sessions every 5 minutes. SOUL says "You leave no trace. You exist only during active sessions."
