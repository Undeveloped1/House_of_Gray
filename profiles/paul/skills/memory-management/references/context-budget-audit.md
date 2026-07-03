# Context Budget Audit

Technique for measuring exactly what's loading in the system prompt at session
start, identifying waste, and calculating token savings from fixes.

## When to use

- Joe suspects token waste ("why am I burning 30k context?")
- After config changes (model migration, prefill changes, skill installs/removals)
- After identity file merges or deduplication
- Periodic hygiene — every few weeks if session start feels heavy

## How to execute

### 1. Find the most recent request dump

```bash
ls -t ~/.hermes/sessions/request_dump_*.json | head -1
```

Request dumps are created on API errors and some other events. If none exist
recent enough, you can still reason about the system prompt composition from
the loaded files, but a real dump gives exact numbers.

### 2. Parse the JSON structure

```python
import json

with open('/root/.hermes/sessions/request_dump_<latest>.json') as f:
    data = json.load(f)

body = data['request']['body']
messages = body['messages']
tools = body.get('tools', [])
```

The structure is:
- `messages[0]` — system prompt (composite: SOUL + framework + skills list + AGENTS + memory + session context)
- `messages[1+]` — additional system messages (prefill injections, if any) then conversation
- `tools` — tool definitions (JSON schemas, verbose)

### 3. Break down system prompt [0] by component

The system prompt is a layered build. Find the boundaries by searching for
known markers:

| Component | Start marker | What it is |
|-----------|-------------|------------|
| SOUL.md | `# SOUL` | Identity, voice, boundaries |
| Hermes framework | `# Finishing the job` or `You run on Hermes` | Tool-use enforcement, parallel calls, mid-turn steering |
| Skills instruction | `## Skills (mandatory)` | Skill loading directive |
| Skills list | `<available_skills>` | All skill names + descriptions (scales with skill count) |
| Environment | `Host: Linux` | OS, Python, platform info |
| AGENTS.md | `# Project Context` or `## AGENTS.md` | Protocols, paths, workflows |
| MEMORY | `════...MEMORY` | Core memory injection |
| Session context | `# Current Session Context` | Source chat, thread, session type |

Measure each block: `content[start:end]`, len() it, divide by 4 for ~tokens.

### 4. Identify duplicates and waste

Look for:
- **Duplicate SOUL/AGENTS** — multiple system messages with overlapping content.
  Root cause is usually `prefill.json` (a legacy pre-injection file at
  `~/.hermes/prefill.json`). If it exists, it injects old versions of SOUL and
  AGENTS as separate system messages before the real ones load. Fix: merge any
  unique content from the prefill into the canonical files, back up the prefill,
  remove it.
- **Oversized skills list** — 114 skills × ~100 chars each = ~11k chars / ~2.8k
  tokens. Pruning unused skills saves proportionally.
- **Tool definitions** — 33 tools at ~58k chars / ~14.7k tokens. This is the
  single biggest chunk. Tools are load-bearing (you can't trim without disabling
  capabilities) but worth knowing about.
- **Stale memory at high capacity** — if MEMORY block is >90% of cap, the
  Memory Lifecycle Protocol should be run.

### 5. Calculate savings

```
Pre-fix overhead = sum(all system messages) + tool definitions
Post-fix overhead = pre-fix - removed waste
Tokens saved = removed waste / 4
```

### Worked example (2026-06-21 audit)

| Component | Chars | ~Tokens | Status |
|-----------|-------|---------|--------|
| SOUL.md (real) | 15,906 | 3,976 | Essential |
| OLD SOUL (prefill duplicate) | 11,423 | 2,855 | **KILLED** |
| OLD AGENTS (prefill duplicate) | 11,582 | 2,895 | **KILLED** |
| Hermes framework | 5,306 | 1,326 | Essential |
| Skills instruction + list | 12,647 | 3,161 | Essential (prune unused for savings) |
| AGENTS.md (real) | 8,437 | 2,109 | Essential |
| MEMORY block | 9,823 | 2,455 | Essential (governed by Lifecycle Protocol) |
| Tool definitions (33 tools) | 58,654 | 14,663 | Essential (cost of capabilities) |
| **TOTAL pre-fix** | **135,665** | **~34k** | |
| **TOTAL post-fix** | **112,660** | **~28k** | |
| **SAVED** | **23,005** | **~5,750** | |

### Key insight

The tool definitions (~14.7k tokens) are the single biggest overhead component
and are immovable — they're the cost of having capabilities. The real waste is
in duplicate identity files and oversized skill lists. After killing duplicates,
the remaining ~28k overhead is mostly load-bearing: tools, identity, memory,
skills. There's maybe another 1-2k to squeeze from skill pruning, but not
another 5k without cutting capability.

### Checking for prefill.json

```bash
ls -la ~/.hermes/prefill.json*
```

If `prefill.json` exists, it's injecting system messages before the normal
identity loading. Check if its content duplicates the canonical SOUL.md and
AGENTS.md. If so:
1. Diff prefill SOUL vs canonical SOUL — merge any unique sections
2. Diff prefill AGENTS vs canonical AGENTS — merge any unique sections
3. Back up: `cp ~/.hermes/prefill.json ~/.hermes/prefill.json.bak.YYYYMMDD`
4. Remove: `rm ~/.hermes/prefill.json`
5. Change takes effect next session (prefill is read per-session, no gateway restart needed)
