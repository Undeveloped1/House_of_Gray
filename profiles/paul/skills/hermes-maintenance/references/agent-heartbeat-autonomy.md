# Agent Heartbeat — Autonomous Execution in Hermes

How to give a Hermes agent OpenClaw-style heartbeat autonomy: self-programming
task lists, admission-gated wakeups, and zero-cost idle cycles.

## Architecture

Three pieces:

### 1. HEARTBEAT.md — the persistent will

Location: vault root (`/root/.hermes/docs/Paul/Brain/HEARTBEAT.md`)

The agent writes to this file during conversations to program its future
self. Format: a task list with status markers.

```markdown
# Active
- [ ] Check Amazon shipment #XYZ — daily, alert if delayed
- [ ] Monitor tcg-engine repo for Cursor commits — hourly

# Waiting
- [ ] Review Trigger 5V band — waiting on Joe's lock
```

When Joe says "keep an eye on X" or "remind me about Y," the agent uses
its write tool to add the task. The agent is programming itself.

### 2. Admission script — the gatekeeper

Location: `~/.hermes/scripts/heartbeat_check.py`

Runs BEFORE the LLM wakes. Three checks, zero API cost:

```python
#!/usr/bin/env python3
"""Heartbeat admission check. Outputs HEARTBEAT.md content if tasks are due.
Empty stdout = silent skip (no LLM call, no delivery)."""
import os
from datetime import datetime
from pathlib import Path

HEARTBEAT = Path.home() / ".hermes/docs/Paul/Brain/HEARTBEAT.md"
SESSION_LOCK = Path("/tmp/paul-session.lock")
ACTIVE_START = 8   # 8 AM
ACTIVE_END = 22    # 10 PM

# 1. Busy check — skip if Joe is actively chatting
if SESSION_LOCK.exists():
    exit(0)

# 2. Active hours check
hour = datetime.now().hour
if hour < ACTIVE_START or hour >= ACTIVE_END:
    exit(0)

# 3. Content check — skip if heartbeat is empty/effectively empty
if not HEARTBEAT.exists():
    exit(0)
content = HEARTBEAT.read_text().strip()
# Strip markdown headers and whitespace
lines = [l for l in content.splitlines() if l.strip() and not l.strip().startswith("#")]
if not lines:
    exit(0)

# Output the content — gets injected into agent context
print(content)
```

### 3. Cron job — the alarm clock

```bash
hermes cron create paul-heartbeat "*/30 * * * *" \
  --script ~/.hermes/scripts/heartbeat_check.py \
  --skills hermes-maintenance \
  --prompt "Read the heartbeat content above. Execute any tasks that are due. Update HEARTBEAT.md to reflect what was done. If nothing needs action, reply 'HEARTBEAT_OK — nothing due.'"
```

Key: `no_agent=False` (default) with a script — the script's stdout is
injected as context. Empty stdout = silent, no delivery, no LLM cost.

## Session lock

The agent touches `/tmp/paul-session.lock` at session start and deletes
it at session close. The admission script checks for it. This prevents
heartbeat runs from firing while Joe is actively chatting.

In SOUL.md or AGENTS.md, add:
```
At session start: touch /tmp/paul-session.lock
At session close: rm -f /tmp/paul-session.lock
```

## Agent behavior during heartbeat runs

The agent should:
1. Read the injected heartbeat content (already in context)
2. Decide which items are due now
3. Execute using tools
4. Update HEARTBEAT.md (check off done items, add new follow-ups)
5. Reply succinctly — "HEARTBEAT_OK" if nothing actionable, or a brief
   summary of what was done

## What this replicates vs. OpenClaw

| Feature | How |
|---------|-----|
| Self-programming tasks | Agent writes to HEARTBEAT.md during chats |
| Admission check (no cost idle) | Script checks before LLM wakes |
| Active hours | Script checks time window |
| Silent when idle | Empty stdout = no delivery (`no_agent` mode) |
| Busy detection | Session lock file |
| Agent decides what to do | Reads heartbeat, prioritizes, executes |

## Not yet replicated

- `HEARTBEAT_OK` token suppression (Hermes delivers the agent response —
  we use a one-line acknowledgment instead of true silence)
- Duplicate suppression (OpenClaw suppresses repeats within 24h)
- The script retry/Cron busy-deferral pattern

## Setup checklist

- [ ] Create `/root/.hermes/docs/Paul/Brain/HEARTBEAT.md`
- [ ] Create `/root/.hermes/scripts/heartbeat_check.py` (chmod +x)
- [ ] Add session lock touch/rm to SOUL or AGENTS
- [ ] Create cron job with script
- [ ] Test: add a task to HEARTBEAT.md, wait for next tick
- [ ] Verify silent skip when HEARTBEAT.md is empty
