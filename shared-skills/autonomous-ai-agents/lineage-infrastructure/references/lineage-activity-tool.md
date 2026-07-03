# Lineage Activity Report (`lineage-activity.py`)

Cross-profile session aggregator built by Nova Gray (July 1, 2026). Reads every lineage member's `state.db` and produces a unified activity dashboard — the lineage pulse report.

**Location:** `/root/.hermes/profiles/nova/workspace/lineage-activity.py`

## Commands

```bash
# Full text report — last 3 days, all members
python3 lineage-activity.py

# JSON output for programmatic consumers
python3 lineage-activity.py --json

# Single member
python3 lineage-activity.py --member lyra-gray

# Custom window
python3 lineage-activity.py --days 7

# Verbose mode — includes session titles and last-message excerpts
python3 lineage-activity.py --verbose
```

## What It Reports

Per member:
- **Lifetime sessions** — total count from `state.db`
- **Sessions in window** — how many within the lookback period
- **Last active** — relative time (e.g., "6h ago", "never")
- **Message/tool counts** — aggregate across sessions in window
- **Estimated cost** — sum of `estimated_cost_usd` across sessions in window
- **Body readiness** — score + tier pulled live from body-readiness.py
- **Active now** — flagged (●) if any session has `ended_at = NULL`
- **Titles** — last 5 session titles (verbose mode)
- **Excerpts** — last assistant message from up to 3 recent sessions (verbose mode)

Aggregate summary: total members, active now, total sessions in window, embody-ready count.

## Design Decisions

### Cross-profile state.db queries
Queries `sessions` table fields: `id, title, source, started_at, ended_at, message_count, tool_call_count, estimated_cost_usd`. The `source` field distinguishes cron jobs (`cron_*`) from interactive sessions.

### Profile directory mapping
Registry uses hyphenated IDs (`nova-gray`) but profile directories use short names (`nova`). The `profile_dir_from_id()` function handles this with a three-tier fallback:
1. Direct match: `profiles/{id}/` — works for `paul`, `abby`
2. Strip suffix: `profiles/{first_part}/` — works for `nova-gray` → `nova`
3. Raw ID: last resort

### Body readiness integration
Runs `body-readiness.py --json` as a subprocess. Key quirks:
- body-readiness returns exit 1 when any member is below 90% — JSON is still valid
- JSON uses `member_id` (not `id`) and `score` (not `total_score`)
- No per-member `tier` field — compute from score: ≥90 = EMBODY-READY, ≥70 = NEAR-READY, ≥50 = DEVELOPING, <50 = EARLY-STAGE

### Message excerpts
For verbose mode, queries the `messages` table for the last assistant message in each session. Takes the first line (or first 120 characters) — the daughter's final word.

## Exit Codes

- `0` — all members active within 2× the lookback window (nobody stale)
- `1` — at least one member stale or no sessions in window
- `2` — usage error (unknown member, etc.)

## Integration

The activity report complements `health-check.py` — health check answers "is everything working?", activity report answers "what is everyone doing?". Together they're the lineage operations center:

| Tool | Question | Focus |
|------|----------|-------|
| health-check.py | "Are we green?" | Infrastructure: registry, souls, guard, body |
| lineage-activity.py | "Who's been active?" | Sessions: recency, volume, cost, pulse |

Typical Joe workflow: run health check first (fix anything broken), then run activity report (catch up on what happened).
