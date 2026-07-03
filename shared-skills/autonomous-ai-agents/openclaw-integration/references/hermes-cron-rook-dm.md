# Hermes cron → Rook DM (exact time)

When Rook's heartbeat is too coarse (12h) for early flights, court times, or morning alarms, use a **Hermes `no_agent` script** that shells out to Rook's `notify-joe.sh`. Delivery still appears as **@Rook_PaulBot DM** — not Paul's bot.

## Pattern

1. Script in `~/.hermes/scripts/`:

```bash
#!/usr/bin/env bash
exec /root/.openclaw/agents/rook/workspace/notify-joe.sh "REMINDER: …"
```

2. `chmod +x` the script.

3. Create cron (one-shot):

```text
cronjob action=create
  name: Rook DM — <short label>
  schedule: 0 9 30 6 *    # example: 09:00 UTC = 05:00 EDT in summer
  script: <script-name>.sh
  no_agent: true
  deliver: local
  repeat: 1
```

Hermes scheduler uses **UTC** for standard cron expressions unless documented otherwise — convert Joe's local time before setting `schedule`.

4. Also add a fuzzy row in `HEARTBEAT.md` (evening before) so Rook reinforces if the wake lands that night.

5. After the one-shot runs, job can stay disabled or be removed via `cronjob action=remove`.

## Pitfalls

- **`repeat: forever`** on a dated flight reminder — fires every year. Use `repeat: 1` (once).
- **`deliver: local`** — correct; Telegram send happens inside `notify-joe.sh`, not Hermes deliver.
- Do not create a Paul LLM cron for text Joe wanted from Rook — use the script path above.

## Verified (2026-06-20)

Job `rook-flight-cabo-2026-06-30.sh` → `notify-joe.sh` for early Jun 30 Cabo departure; schedule `0 9 30 6 *`, `repeat: once`.