---
name: hermes-cron-management
description: "Manage Hermes cron jobs: dual-store architecture, cross-profile reassignment, creation, debugging."
version: 1.0.0
author: Niva Gray
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [hermes, cron, profiles, jobs, scheduler]
    related_skills: [hermes-agent]
---

# Hermes Cron Job Management

Hermes cron jobs live in a **dual-store** architecture — this is the single most important fact to understand before touching anything.

## Dual-Store Architecture

Jobs can exist in two places:

| Store | Path | Written by | Read by |
|-------|------|-----------|---------|
| **Central** | `~/.hermes/cron/jobs.json` | `cronjob` MCP tool | Scheduler, `hermes -p default cron list` |
| **Per-profile** | `~/.hermes/profiles/<name>/cron/jobs.json` | `hermes -p <name> cron create` | `hermes -p <name> cron list` |

The **`cronjob` MCP tool** (the one agents use in-session) writes to the **central** store. The **`hermes cron` CLI** reads from the **per-profile** store.

This means:
- A job created with the `cronjob` tool will show up in `hermes -p default cron list` (if default uses central) but NOT in `hermes cron list` from another profile.
- A job created with `hermes -p nova cron create` lives in the nova profile's `jobs.json` and won't appear in the central store.
- Some profiles (like `default`) appear to read from the central store. Others (like `niva`, `nova`, `abby`) use per-profile stores.

**The `cronjob` tool's `list` action shows central-store jobs regardless of which profile you're in.** Don't trust it alone — cross-check with `hermes cron list`.

## Per-Profile Cron Directory Contents

```
~/.hermes/profiles/<name>/cron/
├── .jobs.lock          # Lock file (empty)
├── .tick.lock          # Tick lock (empty)
├── jobs.json           # Job definitions (may not exist if profile uses central)
├── output/             # Per-run output directories
├── ticker_heartbeat    # Last heartbeat timestamp
└── ticker_last_success # Last successful tick timestamp
```

A profile with no `jobs.json` is either using the central store or has no jobs.

## Reassigning a Cron Job Between Profiles

When moving a job from profile A to profile B:

### 1. Read the source job definition
```bash
cat ~/.hermes/profiles/<source>/cron/jobs.json
```
If the source uses the central store, read from there instead:
```bash
cat ~/.hermes/cron/jobs.json
```

### 2. Extract and adapt the job
The job JSON contains: `id`, `name`, `prompt`, `schedule`, `deliver`, `model`, `provider`, `skills`, `no_agent`, `script`, etc.

Key fields to potentially update:
- `prompt` — if it references the old profile name or persona
- `id` — keep the same ID to avoid confusion, but ensure uniqueness
- `provider_snapshot` / `model_snapshot` — add if the source had them

### 3. Write to target profile
Create or update `~/.hermes/profiles/<target>/cron/jobs.json` with the job appended to the `jobs` array.

Format must match exactly — compare with an existing working profile's `jobs.json`.

### 4. Handle the central store
If the job was also in `~/.hermes/cron/jobs.json`, decide:
- If the target profile uses central: keep it there
- If the target profile uses per-profile: remove from central (avoid double execution)

Remove from central with:
```python
import json
with open('/root/.hermes/cron/jobs.json') as f:
    data = json.load(f)
data['jobs'] = [j for j in data['jobs'] if j['id'] != '<job_id>']
with open('/root/.hermes/cron/jobs.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### 5. Remove from source
```bash
hermes -p <source> cron remove <job_id>
```
Or delete from the source `jobs.json` directly if CLI removal doesn't work.

### 6. Verify
```bash
# Check central store
python3 -c "import json; d=json.load(open('/root/.hermes/cron/jobs.json')); print([j['name'] for j in d['jobs']])"

# Check per-profile store
hermes -p <target> cron list

# Check source is clean
hermes -p <source> cron list
```

Also verify no duplicate IDs across both stores.

## Pitfalls

- **`hermes cron status` may say "No active jobs" even when jobs exist.** The status command and the `cronjob` tool have different views. Trust the `cronjob` tool's `list` output for the scheduler's actual state.

- **The `hermes cron create` CLI is picky about flags.** It doesn't accept `-m` or `--provider`. Create the job, then edit via CLI or directly in `jobs.json`.

- **`hermes cron create` with stdin prompt may fail** with "create requires either prompt or at least one skill" — this means the heredoc/pipe didn't deliver. Write `jobs.json` directly instead.

- **Profile gateway must be running for cron to fire.** Check with `hermes profile list` — the Gateway column shows `running` or `stopped`. A stopped gateway means jobs for that profile won't run.

- **Don't let a job exist in both central AND per-profile stores** unless you've verified the scheduler deduplicates. Safer to pick one.

## Verification Script

See `scripts/verify-job-reassignment.py` for a reusable checker that validates:
- Job exists in the right stores
- Job removed from source
- No duplicate IDs
- Key fields (name, schedule, deliver, provider) are correct
