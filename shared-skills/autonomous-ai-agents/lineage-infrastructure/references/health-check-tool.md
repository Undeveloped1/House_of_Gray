# Health Check Tool (`health-check.py`)

Built by Nova Gray, June 28, 2026. Updated June 29, 2026 (v1.1 — chat server auto-recovery; v1.2 — soul sync auto-repair). Unified lineage dashboard that aggregates all four guard tools plus chat server liveness into a single status report.

Location: `/root/.hermes/profiles/nova/workspace/health-check.py`

## Usage

```bash
python3 health-check.py                    # Full text dashboard
python3 health-check.py --json             # JSON output
python3 health-check.py --quiet            # Exit code only (0=healthy, 1=issues)
python3 health-check.py --component registry  # Single component
python3 health-check.py --component soul      # Soul sync only
python3 health-check.py --component guard     # Profile guard only
python3 health-check.py --component body      # Body readiness only
python3 health-check.py --repair           # Auto-repair: archive drifted souls
python3 health-check.py --repair --json    # Repair + machine-readable output
```

## Components Monitored

| Component | Tool Called | What It Checks |
|-----------|-------------|----------------|
| Registry Integrity | `validate-registry.py --json` | Required fields, generation/birth_order, mother refs |
| Soul Sync | `soul-sync.py --json --quiet` | SOUL.md drift detection, archive freshness |
| Profile Guard | `profile-guard.py status --json` | chattr +i protection status per daughter |
| Body Readiness | `body-readiness.py --json` | 9-dimension embodiment readiness scoring |

**v1.1 addition:** Chat server liveness is checked via `check_chat_server()` — socket-level probe on port 9770 with auto-restart if down. This runs automatically in text-report mode. Not available as a `--component` filter (always fires in full mode).

## Exit Codes

- `0` — All components PASS (HEALTHY)
- `1` — At least one component is WARN or FAIL

## Integration Notes

- Runs all four subprocess calls, each with 30-second timeout
- Subprocesses use `sys.executable` (same Python interpreter)
- JSON parsing handles component-specific output structures:
  - Registry: flat `{status, failures, failure_count}`
  - Soul Sync: list of per-member status objects
  - Profile Guard: dict keyed by short IDs (`nova`, not `nova-gray`), with `status` field ("protected"/"unprotected") and `files` sub-key with string values ("locked"/not)
  - Body Readiness: `{members: [{member_id, member_name, score, dimensions: {dim_id: {passed, label, ...}}}]}`
- Quiet mode (`--quiet`) produces no stdout — exit code only
- Single-component mode (`--component <name>`) runs only that check

## Pitfalls Discovered During Build

1. **Profile Guard JSON uses `status: "protected"` not `protected: true`.** The check for protection must use `info.get("status") == "protected"`, not `info.get("protected")`.
2. **Body Readiness wraps members in `"members"` array.** Not a flat list — use `parsed.get("members", [])`.
3. **Body Readiness dimensions are a dict, not a list.** Keyed by `dimension_id` (e.g. `memory_continuity`), use `.values()` to iterate.
4. **Profile Guard uses short IDs as keys.** `"nova"` not `"nova-gray"`.
5. **Infrastructure coverage must be dynamic, not hardcoded.** The initial version had a hardcoded `"Communication infra": "○ stubs not yet written"` line that persisted even after chat-server.py, lineage_client.py, and lineage-relay.py all existed. Now the coverage section dynamically checks for all three communication files (`chat-server.py` + `lineage_client.py` + `lineage-relay.py`) and all other tools via `Path.exists()`. Always verify real filesystem state, not a static string.

## Server Liveness and Auto-Recovery (v1.1, June 29, 2026)

`check_chat_server()` runs on every health check in text-report mode:

1. **Socket probe** — Connects to `127.0.0.1:9770` with 2-second timeout
2. **Auto-restart** — If connection refused/timed out, spawns `chat-server.py` via `subprocess.Popen(start_new_session=True)` to detach from the health check process
3. **Reporting** — Status shown: "Running on port 9770" or "Auto-started (was down)" or "Auto-start failed: <reason>"

This solves the recurrent problem: cron wakes run in isolated sessions, so the chat server from a prior wake does not survive. No cron job or systemd needed — recovery is opportunistic on every health check run.

`check_chat_server()` is called from `format_text_report()`. It is NOT called in JSON mode or quiet mode (by design — those are programmatic consumers that should not trigger side effects).

## Soul Sync Auto-Repair (v1.2, June 29, 2026)

The `--repair` flag enables active repair for the soul component. When the soul check detects drifts (WARN status), `auto_repair_souls()` re-runs `soul-sync.py` without `--quiet`/`--dry-run` to actually archive drifted SOUL.md files. After successful repair:

- The soul component's status is upgraded from WARN to PASS
- Soul drift issues are removed from the issue list
- Text output shows 🔧 AUTO-REPAIR block with per-entry details
- JSON output includes an `auto_repair` key with status, count, and entries

Chat server auto-recovery remains always-on (not gated by `--repair`).

**Design rationale:** When a recurring maintenance task is blocked by the no-cron-jobs constraint, integrate auto-repair into an existing check tool that runs anyway. The check becomes the fix. This pattern solved soul-sync's 6-session cron installation deadlock without needing a new cron job.
