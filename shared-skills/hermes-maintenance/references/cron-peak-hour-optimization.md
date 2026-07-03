# Cron Peak-Hour Cost Optimization

When an API provider introduces surge/peak-hour pricing, audit ALL cron jobs across
ALL profiles and shift them into off-peak windows. The audit path is:

1. Identify the provider's peak-hour windows (always in UTC)
2. Convert to the user's local timezone
3. List every cron job across every profile
4. Flag any job whose UTC schedule lands in a peak window
5. Shift flagged jobs to the nearest safe UTC hour

## Provider Peak-Hour Patterns

### DeepSeek (as of June 2026)
- **Peak windows (UTC):** 01:00–04:00 and 06:00–10:00
- **Surge:** 2× regular pricing during peak
- **EDT equivalent (UTC-4):** 9 PM–midnight and 2 AM–6 AM
- **Safe UTC hours for EDT daytime:** 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 00

## Cross-Profile Cron Audit

Check the default profile FIRST (via `cronjob(action='list')`), then scan every
profile directory:

```bash
for profile in /root/.hermes/profiles/*/; do
  name=$(basename "$profile")
  jobfile="$profile/cron/jobs.json"
  if [ -f "$jobfile" ]; then
    echo "=== $name ==="
    python3 -c "
import json, sys
from datetime import datetime, timezone
with open('$jobfile') as f:
    data = json.load(f)
for j in data.get('jobs', []):
    schedule = j.get('schedule', {})
    disp = schedule.get('display', j.get('schedule_display', 'unknown'))
    print(f\"  {j['name']}: {disp}\")
"
  fi
done
```

## Timing Conflicts With Interval Schedules

`every Nm` interval schedules can create unavoidable peak conflicts. Example:
Nova's heartbeat at `every 360m` (6 hours) — one of four daily runs ALWAYS lands in a
peak window because peak blocks (1-4, 6-10 UTC) leave a max continuous safe gap of
14 hours, and 6×3=18 wraps from safe into peak.

**Fix:** Replace `every Nm` with explicit hours that all land in safe windows. For
4× daily, use `0 10,14,18,22 * * *` (all EDT daytime).

## Cross-Profile Cron Editing

`cronjob(action='update')` only operates on the current profile's cron database.
To edit another profile's cron jobs, directly patch its `jobs.json`:

```bash
# Read
cat /root/.hermes/profiles/<name>/cron/jobs.json

# Edit with patch tool (set cross_profile=true)
```

Remember to update ALL timestamp fields in the JSON:
- `schedule.run_at`
- `schedule.display`
- `schedule_display`
- `next_run_at`
- Any hardcoded time references in the `prompt` string

## System Crontab — The Third Cron Source

Beyond Hermes cron (`cronjob(action='list')`) and profile `jobs.json` files, cron
jobs can also live in the **system crontab** (`crontab -l`). These are invisible to
Hermes tools and must be checked separately:

```bash
crontab -l
```

Common pattern: shell scripts that predate Hermes cron migration. Check each entry's
timing against peak windows regardless of whether it uses the API — shift for
consistency even if shell-only.

## "No API Call" Exception

Shell-only cron scripts (disk checks, process monitoring, echo-to-log) that don't
make LLM API calls are **not affected** by peak-hour pricing — they don't consume
tokens. They can stay in peak windows. But for consistency and to avoid future
surprises (if the script is later upgraded to use an LLM), shifting them is
low-cost insurance.
