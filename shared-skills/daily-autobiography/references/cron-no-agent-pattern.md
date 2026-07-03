# Cron No-Agent Pattern — Verification Injection Fix

## The Problem

Any `write_file` or `patch` call made by an LLM-based cron agent triggers the system to inject a verification demand:

```
[System: You edited code in this turn, but the workspace does not have fresh
passing verification evidence yet.

Verification status: unverified

Changed paths:
- `/root/.hermes/docs/Paul/projects/...`
```

The agent then appends verification output to its final response — which gets delivered to Joe alongside the actual content. CRITICAL prefix instructions in the prompt are NOT strong enough to override this system injection. 8 prior Bible+Stoic deliveries and 1 autobiography delivery were polluted this way.

## The Fix

**Option A: Strip all file writes from the LLM prompt.** The LLM only composes and delivers text. Cron output files at `~/.hermes/cron/output/<job_id>/` serve as the archive. Use this when the task REQUIRES LLM creativity (e.g., Bible+Stoic pairing).

**Option B: Convert to `no_agent: true` script.** A Python/shell script handles everything — reads input files, produces output to stdout (gets delivered), handles state mutation. No LLM = no verification injection possible. Use this when the data is static (e.g., autobiography checklist questions).

## Proven Results

| Cron | Method | Status |
|------|--------|--------|
| Bible + Stoic | LLM, no file writes | Clean since 2026-06-27 11:05 test |
| Autobiography | no_agent script | Clean since 2026-06-27 |

## Script Template (Option B)

```python
#!/usr/bin/env python3
"""Reads state, produces output, advances state. stdout = delivery."""

# 1. Read input files (state, config, checklist, etc.)
# 2. Compute what to deliver
# 3. Print to stdout → auto-delivered to user
# 4. Update state files silently

print("Formatted content here...")
# State mutation after print — no verification possible
```

## LLM Prompt Template (Option A)

```
**CRITICAL: Your response is ONLY the content below — nothing else.
No verification, no checks, no meta-text.**

[Composition instructions — NO file write or patch calls]
```
