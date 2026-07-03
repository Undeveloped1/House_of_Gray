# Context Budget Audit

How to measure what's actually burning tokens at session start, using request_dump JSON files.

## When to Use

- User says "I'm burning too many tokens" or "context feels heavy"
- After identity file changes (SOUL, AGENTS, prefill.json) to verify the fix worked
- Periodic hygiene check on context overhead
- Diagnosing duplicate or stale injections

## The Methodology

### Step 1: Find request dump files

```bash
ls -t ~/.hermes/sessions/request_dump_*.json | head -5
```

These are written when API errors occur. They capture the full request body sent to the model — the ground truth of what's consuming context.

### Step 2: Parse the structure

```python
import json

with open(dump_path) as f:
    data = json.load(f)

body = data['request']['body']
messages = body['messages']      # list of {role, content}
tools = body.get('tools', [])    # list of tool definitions
```

### Step 3: Identify system messages

System messages are at the start of `messages[]`. There may be 1-3 of them. Each is a separate injection layer:

```python
for i, msg in enumerate(messages):
    if msg['role'] == 'system':
        print(f"[{i}] {len(msg['content']):,} chars — {msg['content'][:120]}")
```

**Red flag:** Multiple system messages with similar headers (e.g., two "# SOUL" blocks) = duplicate injection. Common cause: stale `prefill.json` (see `references/prefill-json-duplicates.md`).

### Step 4: Break down system message [0] by component

The primary system message is a composite built by Hermes from multiple sources. Find the boundaries:

```python
content = messages[0]['content']

markers = [
    ("SOUL.md", 0, content.find("# Finishing the job")),
    ("Hermes framework", content.find("# Finishing the job"), content.find("## Skills (mandatory)")),
    ("Skills instruction", content.find("## Skills (mandatory)"), content.find("<available_skills>")),
    ("Available skills list", content.find("<available_skills>"), content.find("Host:")),
    ("Environment + platform", content.find("Host:"), content.find("# Project Context")),
    ("AGENTS.md", content.find("# Project Context"), content.find("MEMORY")),
    ("MEMORY block", content.find("MEMORY"), len(content)),
]
```

### Step 5: Measure tool definitions

```python
tool_sizes = [(t['function']['name'], len(json.dumps(t))) for t in tools]
tool_sizes.sort(key=lambda x: -x[1])
for name, chars in tool_sizes:
    print(f"{name:<35} {chars:>8,} chars  {chars//4:>6} tokens")
```

### Step 6: Calculate total overhead

```python
total_system = sum(len(m['content']) for m in messages if m['role'] == 'system')
total_tools = sum(len(json.dumps(t)) for t in tools)
total_overhead = total_system + total_tools
print(f"Total overhead: {total_overhead:,} chars ≈ {total_overhead // 4:,} tokens")
```

## Reference Budget (Paul VPS, post-fix 2026-06-21)

| Component | ~Tokens | Notes |
|-----------|---------|-------|
| SOUL.md | 4,000 | Essential — identity |
| Hermes framework | 1,300 | Hermes-injected, can't control |
| Skills instruction + list | 3,200 | 114 skills listed |
| Environment + platform | 350 | Session metadata |
| AGENTS.md | 2,100 | Protocols |
| MEMORY block | 2,500 | Core memory injection |
| Tool definitions (33) | 14,700 | Biggest chunk — all actively used |
| **Total** | **~28k** | |

## What's actionable vs. immovable

**Actionable:**
- Duplicate system messages (prefill.json, stale identity files) — biggest win
- Pruning unused skills (each skill in the list costs ~25-50 tokens)
- Tightening SOUL/AGENTS prose (marginal — content is essential)

**Immovable:**
- Tool definitions — cost of having capabilities. Can't trim without disabling tools.
- Hermes framework instructions — injected by the runtime
- Skills list — needed so the agent knows what's available

## Key Insight

The tools are the biggest chunk (~50% of overhead) but they're all actively used. The real waste is almost always in duplicate or stale injections — things that shouldn't be there at all. A 5k-token duplicate SOUL is pure waste; a 2k-token tool definition is load-bearing infrastructure. Don't confuse the two.
