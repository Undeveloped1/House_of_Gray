# HEARTBEAT.md — personal reminders for Joe

Add under `## Joe — Personal reminders (notify-joe.sh)` in the watcher workspace.

## Trip / context block (optional)

Free-form facts Rook should not forget when wording reminders:

```markdown
**Trip context (Jun 2026):** Court **Jun 29, 3:30pm EST**. **DoubleTree Grand Rapids — airport** (shuttle). **Return:** early flight **Jun 30** to **Cabo**. Hotel through **checkout morning Jun 30**.
```

## Reminder table

Process **before** lower-priority beat work on each wake. Times in Joe's zone unless noted.

```markdown
| Due (first fire) | Status | Message |
|------------------|--------|---------|
| **2026-06-21** | pending | `REMINDER: …` |
| **2026-06-29** evening | pending | `REMINDER: Early flight tomorrow — set alarm, checkout, shuttle.` |

**Rules:** If calendar date ≥ Due and Status is `pending`, run `./notify-joe.sh` with Message text, set Status to `sent`, append audit line with UTC timestamp.
```

## When Paul/Joe add reminders in a Hermes session

1. Append rows to Rook's `HEARTBEAT.md` (not Paul's vault-only unless copying for audit).
2. For **due today** or **time-sensitive**, also run `notify-joe.sh` immediately — do not wait for the next 12h heartbeat.
3. Mark row `sent` and log who fired it (`Paul/Joe setup`) so Rook does not duplicate.

## Multi-row same day

Multiple `pending` rows with the same due date are all eligible on that wake — send each once, mark each `sent`.

## Pitfall: evening / exact-time rows

`Jun 29 evening` is heartbeat-fuzzy. For **early morning flight** or **court at 3:30pm**, add a Hermes one-shot cron that calls `notify-joe.sh` — see `references/hermes-cron-rook-dm.md`.