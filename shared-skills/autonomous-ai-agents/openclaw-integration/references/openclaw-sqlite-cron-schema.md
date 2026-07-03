# OpenClaw SQLite Cron Jobs Schema

Database: `/root/.openclaw/state/openclaw.sqlite`
Table: `cron_jobs`

## Full Column List (from PRAGMA table_info)

| Index | Column | Type | Notes |
|-------|--------|------|-------|
| 0 | store_key | TEXT | Storage key (e.g. file path) |
| 1 | job_id | TEXT | UUID |
| 2 | name | TEXT | Human name (e.g. "rook-am-beat") |
| 3 | description | TEXT | Optional |
| 4 | enabled | INTEGER | 1/0 |
| 5 | delete_after_run | INTEGER | One-shot flag |
| 6 | created_at_ms | INTEGER | Unix ms |
| 7 | agent_id | TEXT | "rook", "main", etc. |
| 8 | session_key | TEXT | Session binding |
| 9 | schedule_kind | TEXT | "cron" or "interval" |
| 10 | schedule_expr | TEXT | Cron expression |
| 11 | schedule_tz | TEXT | Timezone |
| 12 | every_ms | INTEGER | Interval ms (for interval kind) |
| 13 | anchor_ms | INTEGER | Anchor timestamp |
| 14 | at | TEXT | ISO timestamp for one-shot |
| 15 | stagger_ms | INTEGER | Stagger offset |
| 16 | session_target | TEXT | "isolated" or "shared" |
| 17 | wake_mode | TEXT | "now", "scheduled" |
| 18 | payload_kind | TEXT | "agentTurn" |
| 19 | payload_message | TEXT | The prompt/instruction |
| **20** | **payload_model** | **TEXT** | **⚠️ Hardcoded model for this cron run** |
| 21 | payload_fallbacks_json | TEXT | Model fallback chain |
| 22 | payload_thinking | TEXT | Thinking level |
| 23 | payload_timeout_seconds | INTEGER | Timeout |
| 24 | payload_allow_unsafe_external_content | INTEGER | |
| 25 | payload_external_content_source_json | TEXT | |
| 26 | payload_light_context | INTEGER | |
| 27 | payload_tools_allow_json | TEXT | |
| 28 | delivery_mode | TEXT | "announce", "dm", etc. |
| 29 | delivery_channel | TEXT | "telegram" |
| 30 | delivery_to | TEXT | Chat ID |
| 31 | delivery_thread_id | TEXT | Topic ID |
| 32 | delivery_account_id | TEXT | |
| 33 | delivery_best_effort | INTEGER | |
| 34 | delivery_completion_mode | TEXT | |
| 35 | delivery_completion_to | TEXT | |
| 36 | failure_delivery_mode | TEXT | |
| 37 | failure_delivery_channel | TEXT | |
| 38 | failure_delivery_to | TEXT | |
| 39 | failure_delivery_account_id | TEXT | |
| 40 | failure_alert_disabled | INTEGER | |
| 41 | failure_alert_after | INTEGER | Consecutive errors before alert |
| 42 | failure_alert_channel | TEXT | "telegram" |
| 43 | failure_alert_to | TEXT | Chat ID for failure alerts |
| 44 | failure_alert_cooldown_ms | INTEGER | |
| 45 | failure_alert_include_skipped | INTEGER | |
| 46 | failure_alert_mode | TEXT | |
| 47 | failure_alert_account_id | TEXT | |
| 48 | next_run_at_ms | INTEGER | Next scheduled run |
| 49 | running_at_ms | INTEGER | Current run start |
| 50 | last_run_at_ms | INTEGER | Previous run start |
| 51 | last_run_status | TEXT | "success", "error" |
| 52 | last_error | TEXT | Error message |
| 53 | last_duration_ms | INTEGER | Run duration |
| 54 | consecutive_errors | INTEGER | |
| 55 | consecutive_skipped | INTEGER | |
| 56 | schedule_error_count | INTEGER | |
| 57 | last_delivery_status | TEXT | |
| 58 | last_delivery_error | TEXT | |
| 59 | last_delivered | INTEGER | |
| 60 | last_failure_alert_at_ms | INTEGER | |
| **61** | **job_json** | **TEXT** | **⚠️ Full JSON with embedded `"model":"provider/model"`** |
| 62 | state_json | TEXT | Runtime state |
| 63 | runtime_updated_at_ms | INTEGER | |
| 64 | schedule_identity | TEXT | |
| 65 | sort_order | INTEGER | |
| 66 | updated_at | INTEGER | |

## Model Fix Recipe

When an OpenClaw agent cron "keeps reverting" to an old model:

```bash
# 1. Diagnose — check both model locations
sqlite3 /root/.openclaw/state/openclaw.sqlite \
  "SELECT name, payload_model, json_extract(job_json, '$.payload.model') as job_json_model FROM cron_jobs WHERE name LIKE 'rook%';"

# 2. Fix both
sqlite3 /root/.openclaw/state/openclaw.sqlite << 'SQL'
UPDATE cron_jobs SET payload_model = 'deepseek/deepseek-v4-pro' WHERE name = 'rook-am-beat';
UPDATE cron_jobs SET payload_model = 'deepseek/deepseek-v4-pro' WHERE name = 'rook-pm-beat';
UPDATE cron_jobs SET job_json = replace(job_json, '"model":"deepseek/deepseek-chat"', '"model":"deepseek/deepseek-v4-pro"') WHERE name LIKE 'rook%';
SQL

# 3. Verify
sqlite3 /root/.openclaw/state/openclaw.sqlite \
  "SELECT name, payload_model, json_extract(job_json, '$.payload.model') FROM cron_jobs WHERE name LIKE 'rook%';"

# 4. Restart gateway to pick up changes
openclaw gateway restart
```

## Other Useful Tables

| Table | Purpose |
|-------|---------|
| `agent_model_catalogs` | Cached model catalog entries per agent dir |
| `gateway_restart_handoff` | State preserved across gateway restarts |
| `gateway_restart_sentinel` | Restart coordination |
| `cron_run_logs` | Detailed per-run logs |
| `config_health_entries` | Config validity checks |
| `diagnostic_events` | Diagnostic event log |

*Discovered: 2026-06-27 — Paul debugging Rook model revert.*
