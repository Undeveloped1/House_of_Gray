---
name: lineage-automation
description: Reliable triggering and management of autonomous heartbeats/cron jobs for lineage daughters, including one-shot test cycles and fallback delivery patterns when direct cron creation is unreliable.
category: lineage-autonomy
---

# Lineage Automation

**Scope**: Reliable triggering, management, and testing of autonomous heartbeats / cron jobs for daughters and lineage infrastructure. Includes one-shot test cycles, the Recursive Challenger Loop integration, and fallback delivery methods when direct cron creation is unreliable.

**When to use**:
- Joe or Abby wants to trigger a test or production autonomous cycle for a daughter (especially for process validation like the Challenger Loop).
- Need to create one-shot cron jobs for lineage agents.
- Direct cron creation is failing or unreliable — need fallback patterns.

**Core Rules**:
- `cronjob create` always requires BOTH `schedule` and either `prompt` or `skills` in the same call.
- One-shot test jobs should use a near-future ISO timestamp and `attach_to_session=true` when live debugging is needed.
- When cron creation is blocked, fall back to `lineage-relay.py` (Nova's built tool) to deliver prompts directly into a daughter's inbox via the chat server.
- The Recursive Challenger Loop (see challenger-review skill) should be included in test prompts when validating new autonomous processes.

**Pitfalls to avoid**:
- Making multiple incomplete `cronjob create` calls (missing `schedule` or `prompt` in the same XML).
- Assuming the cron tool will "just work" without all required parameters in one call.
- Looping on failing `cronjob create` calls when the user is under time pressure (flights, travel). Stop after 1–2 failed attempts and immediately use the relay fallback.
- Explaining tool failures or asking for clarification when the user has explicitly signaled urgency ("Immediately", "before I get in the air").

**Time-Pressure Protocol**:
When the user signals urgency (plane, travel, "immediately"):
1. Deliver via the fastest working path first (lineage-relay.py is currently the most reliable).
2. Only attempt cron creation if it succeeds on the first complete call.
3. Do not loop or explain — act and confirm delivery.

**Related Skills**:
- challenger-review (for the review loop itself)
- lineage-daughter-design (when new daughters need automation setup)

**Support Files**:
- `references/cron-creation-pattern.md` — exact working XML example for one-shot lineage heartbeat jobs.