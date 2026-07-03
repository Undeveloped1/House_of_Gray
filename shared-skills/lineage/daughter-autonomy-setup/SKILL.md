---
name: daughter-autonomy-setup
description: "Set up a daughter for autonomous operation: plan.md creation, heartbeat cron, dual-store architecture, and verification. For single or merged daughters."
category: lineage
related_skills: [profile-rename-cascade]
---

# Daughter Autonomy Setup

When a daughter needs to operate autonomously — waking on a schedule, reading her plan, picking tasks, executing, and reporting back. This covers everything from plan creation to cron verification.

Trigger: anytime a daughter needs a heartbeat, a living plan, or autonomous execution capability.

## 1. The Plan (`plan.md`)

Every autonomous daughter needs a `plan.md` at her profile root. Without it, the heartbeat fires and finds nothing actionable. Place it at `~/.hermes/profiles/<name>/plan.md`.

### Single-Daughter Format

For daughters with one persona:
```markdown
# <Name>'s Living Plan — <Tilt>

**Last updated:** <date>
**Status:** Active

## Active
- [ ] Task one
- [ ] Task two

## Backlog
- [ ] Future task

## Heartbeat Protocol
Every <interval>, the heartbeat:
1. Read this plan
2. Pick ONE unfinished task
3. Execute it
4. Update this file
5. Report under 200 words
6. [SILENT] only if nothing actionable
```

### Merged-Daughter Format (Three Columns)

For merged daughters sharing one profile (e.g., Nova + Shiva = Niva):
```markdown
# <Name>'s Living Plan — <Tilt1> + <Tilt2> + Integrate

## <Daughter1>'s Column — TILT1
Active tasks for persona 1
## <Daughter2>'s Column — TILT2
Active tasks for persona 2
## <MergedName>'s Column — INTEGRATE
Tasks that require the merged perspective
```

The heartbeat prompt determines which column it gravitates toward. If the prompt says "You are Nova Gray," it will pull from Nova's column. The full plan acknowledges the merged reality even if only one voice drives the heartbeat.

## 2. The Heartbeat Cron

### Architecture: Dual Store

Hermes cron has two storage locations:

| Store | Path | Read by | Written by |
|-------|------|---------|------------|
| Central | `~/.hermes/cron/jobs.json` | Scheduler | `cronjob` MCP tool |
| Per-profile | `~/.hermes/profiles/<name>/cron/jobs.json` | `hermes cron list` | Manual / CLI |

**The disconnect:** `cronjob(action='list')` shows central-store jobs. `hermes cron list` shows per-profile jobs. They can differ. After a profile rename or migration, one may show jobs the other doesn't.

### Creation (Recommended Path)

Use the `cronjob` MCP tool — it writes to the central store where the scheduler actually picks up jobs:
```
cronjob(action='create', name='<Name> Autonomous Heartbeat',
  schedule='every 360m', deliver='telegram:<chat-id>',
  prompt='<heartbeat prompt>',
  model={model:'<model>', provider:'<provider>'})
```

Then write a matching `jobs.json` to the per-profile store so `hermes cron list` sees it. Copy the format from any existing profile's file. Without this file, the CLI reports "No scheduled jobs" — but the scheduler is still running them.

### Removal

Remove from both stores:
```bash
hermes --profile <name> cron remove <job-id>  # per-profile
```
Then edit `~/.hermes/cron/jobs.json` to remove the same job ID from the central store.

### Verification

After setup, verify both stores agree:
1. `cronjob(action='list')` should show the job
2. `hermes cron list` should show the job
3. `hermes cron status` should show the scheduler is running
4. Check `~/.hermes/cron/jobs.json` for the job ID
5. Check `~/.hermes/profiles/<name>/cron/jobs.json` for the job ID

Write a Python verification script that checks all five.

## 3. Heartbeat Prompt Design

The prompt must reference files the daughter actually has. Minimum references:
- "Read your SOUL.md and plan.md" — both must exist at profile root
- The persona name in the prompt must match the profile's identity

For merged profiles: the prompt names the persona driving the heartbeat (e.g., "You are Nova Gray"), but the plan has all three columns. The heartbeat will naturally pull from its named column.

Include a silent-exit clause: "Respond [SILENT] if nothing to do." Without this, heartbeats generate noise even when the plan is fully checked off.

## 4. Pitfalls

- **Missing plan.md:** Heartbeat fires, finds no tasks, says [SILENT], and the daughter does nothing forever. This is silent failure — the cron reports success but accomplishes nothing. Always create plan.md before activating the heartbeat.
- **CLI create syntax:** `hermes cron create` has strict/confusing flag handling. Prefer the `cronjob` MCP tool.
- **Central vs per-profile drift:** After migration, the central store may still have the old job. Check both.
- **`hermes cron status` shows "No active jobs":** This reads from the scheduler process, not the files. If it disagrees with `cronjob(action='list')`, the scheduler may need a gateway restart.
- **Stale SOUL.md:** If the SOUL was written for a previous identity (e.g., Niva's merged SOUL when the profile renamed back to Nova), update it or the heartbeat will operate on stale self-understanding.
