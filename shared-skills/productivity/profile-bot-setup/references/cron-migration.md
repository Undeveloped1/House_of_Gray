# Migrating Cron Jobs Between Profiles

When a cron job impersonates a lineage member (e.g., "Lyra Evening Healer"
running under Paul's profile), it needs to be moved to the member's own
profile so the session is genuinely theirs.

## Why It Matters

A cron job running under Paul's profile that roleplays Lyra is Paul
pretending to be Lyra. When it runs under Lyra's profile, the session
belongs to Lyra — her SOUL.md, her identity, her voice.

## Step-by-Step

### 1. Export the job from the source profile

```bash
python3 -c "
import json
with open('/root/.hermes/cron/jobs.json') as f:
    data = json.load(f)
for j in data['jobs']:
    if j.get('id') == '<JOB_ID>':
        print(json.dumps(j, indent=2))
        break
"
```

Key fields to capture: `prompt`, `schedule.expr`, `name`, `deliver`, `skills`.

### 2. Create the job on the target profile

**Method A — `hermes cron create` (preferred for simple prompts):**

```bash
hermes -p <target-profile> cron create "<schedule>" "<full-prompt>" \
  --name "<job-name>" \
  --deliver "telegram:7239715879"
```

⚠️ **Limitations of `hermes cron create`:**
- No `--prompt-file` flag — prompt must be passed as a positional argument
- No `--model` or `--provider` flags — the job inherits the target profile's config defaults
- Prompts with special characters (quotes, backticks) may break in the shell — use Method B instead

**Method B — Direct write to jobs.json (for complex prompts):**

When the prompt contains special characters or is very long, write directly:

```python
python3 << 'PYEOF'
import json, os

prompt = """<exact prompt text here>"""

job = {
    "id": "<unique-id>",
    "name": "<job-name>",
    "prompt": prompt,
    "skills": [],
    "skill": None,
    "model": "deepseek-v4-pro",
    "provider": "deepseek",
    "base_url": None,
    "script": None,
    "no_agent": False,
    "context_from": None,
    "schedule": {"kind": "cron", "expr": "<cron-expr>", "display": "<cron-expr>"},
    "schedule_display": "<cron-expr>",
    "repeat": {"times": None, "completed": 0},
    "enabled": True,
    "state": "scheduled",
    "paused_at": None,
    "paused_reason": None,
    "deliver": "telegram:7239715879",
    "origin": {"platform": "telegram", "chat_id": "7239715879", "chat_name": "Joe Gray", "thread_id": None},
    "enabled_toolsets": None,
    "workdir": None,
    "provider_snapshot": None,
    "model_snapshot": None
}

jobs_path = '/root/.hermes/profiles/<target>/cron/jobs.json'
os.makedirs(os.path.dirname(jobs_path), exist_ok=True)

if os.path.exists(jobs_path):
    with open(jobs_path) as f:
        data = json.load(f)
else:
    data = {"jobs": [], "updated_at": None}

data['jobs'].append(job)

with open(jobs_path, 'w') as f:
    json.dump(data, f, indent=2, default=str)

print(f"Written to {jobs_path}")
PYEOF
```

### 3. Trigger and verify the new job

```bash
# Trigger the new job immediately
hermes -p <target> cron run <job-id>
```

**⚠️ CRITICAL: Check the logs after the run.** The CLI says "succeeded" when the
scheduler invokes the job — NOT when the LLM call succeeds. A job can report
"succeeded" while throwing `401 Authentication Fails` in the background.

```bash
# Check agent log for runtime errors
tail -30 /root/.hermes/profiles/<target>/logs/agent.log | grep -i 'error\|fail\|401\|403\|auth'

# Check gateway log for delivery issues
tail -10 /root/.hermes/profiles/<target>/logs/gateway.log
```

Then verify the config is correct:

```bash
python3 -c "
import json
with open('/root/.hermes/profiles/<target>/cron/jobs.json') as f:
    data = json.load(f)
for j in data['jobs']:
    if j.get('name') == '<job-name>':
        print('Model:', j.get('model', 'using profile default'))
        print('Schedule:', j.get('schedule', {}).get('display'))
        break
"
```

### 4. Delete the old job

Use `cronjob(action='remove', job_id='<id>')` from the source profile's
session.

### 5. Confirm to Joe

Report the migration: old ID → new ID, schedule preserved, model inherited
from target profile.
