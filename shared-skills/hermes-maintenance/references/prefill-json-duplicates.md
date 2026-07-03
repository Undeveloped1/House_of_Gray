# prefill.json — Duplicate Identity Files in System Prompt

## Symptom

The system prompt contains TWO different versions of SOUL.md or AGENTS.md —
contradictory text, different section headers, different sizes. Every turn
the model gets conflicting identity/protocol instructions.

## Root Cause

`~/.hermes/prefill.json` is a file that injects raw system messages BEFORE
the normal identity loading (SOUL.md, AGENTS.md) happens. It is typically
created during migration or manual setup as a bridge, then forgotten.

When it exists, the turn structure becomes:

```
prefill.json[0]  →  OLD SOUL (stale, pre-migration)
prefill.json[1]  →  OLD AGENTS (stale, pre-migration)
[normal loading] →  CURRENT SOUL.md
[normal loading] →  CURRENT AGENTS.md  (via /root/AGENTS.md symlink)
```

The model sees both versions and has no way to know which is authoritative.

## Diagnostic Path

1. **Confirm duplicates on disk are NOT the cause.** Check for symlinks:
   ```bash
   file /root/AGENTS.md /root/.hermes/AGENTS.md /root/.hermes/SOUL.md
   ls -la /root/SOUL.md /root/AGENTS.md 2>&1
   ```
   If `/root/AGENTS.md` is a symlink to `/root/.hermes/AGENTS.md`, there is
   only ONE file on disk — the duplicate is coming from elsewhere.

2. **Grep for unique phrases** from each version to find injection sources:
   ```bash
   grep -rl "unique phrase from version A" /root/.hermes/ 2>/dev/null
   grep -rl "unique phrase from version B" /root/.hermes/ 2>/dev/null
   ```
   If one version traces to `prefill.json` and the other to `SOUL.md`/`AGENTS.md`,
   prefill.json is the culprit.

3. **Inspect prefill.json structure:**
   ```python
   import json
   with open("/root/.hermes/prefill.json") as f:
       data = json.load(f)
   # List of {role, content} dicts — each is a pre-injected system message
   for i, item in enumerate(data):
       print(f"[{i}] role={item['role']} len={len(item['content'])} first100={item['content'][:100]}")
   ```

## Fix

1. **Diff the versions** to find unique content in the stale prefill version
   that the current file lost. Extract section headers from both:
   ```python
   import re, json
   with open("/root/.hermes/prefill.json") as f:
       old = json.load(f)[0]['content']  # or [1] for AGENTS
   with open("/root/.hermes/SOUL.md") as f:
       new = f.read()
   old_sections = set(re.findall(r'^##? .+', old, re.MULTILINE))
   new_sections = set(re.findall(r'^##? .+', new, re.MULTILINE))
   print("In old but not new:", old_sections - new_sections)
   ```

2. **Merge unique content** into the canonical file via `patch` tool. Add a
   changelog entry documenting what was merged and why.

3. **Back up and remove prefill.json:**
   ```bash
   cp /root/.hermes/prefill.json /root/.hermes/prefill.json.bak.$(date +%Y%m%d)
   rm /root/.hermes/prefill.json
   ```

4. **No gateway restart needed.** prefill.json is read per-session at init,
   not cached at the gateway level. The fix takes effect on the next new
   session. The current session still has the old duplicate in context —
   that cannot be fixed mid-session.

## Verification

Start a new session and confirm:
- Only one SOUL.md version appears in the system prompt
- Only one AGENTS.md version appears
- No contradictory instructions (e.g., memory review at start vs. close)

## When NOT to Remove prefill.json

If prefill.json contains content that is NOT duplicated by the normal
identity files (genuinely unique bridge content still in use), do NOT
remove it blindly. Merge that content into the canonical files first,
then remove. The backup ensures nothing is lost if you make a mistake.
