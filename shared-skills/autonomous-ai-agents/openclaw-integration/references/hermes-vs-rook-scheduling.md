# Hermes cron vs Rook HEARTBEAT — what to offload

Use when Joe wants schedules, reminders, and beats split between Paul and Rook.

## Keep on Paul (Hermes)

- `no_agent: true` scripts (session backup, `hermes update`)
- Creative LLM jobs (devotional pairing, Five Crests, vault writes)
- **Telegram group delivery** (polished beats, group-facing format)
- Exact-time one-shots if Hermes cron is already working

## Give Rook (OpenClaw HEARTBEAT.md)

- Personal **reminders** and **watch alerts** → deliver via `notify-joe.sh`
- Scrape/collect → `shared/` (e.g. `/root/shared/rook-paul/`)
- Weekly recap file + short DM to Joe
- Joe relay to Paul → still `ping-paul.sh` (HARD RULE)

## Timing

| Mechanism | Granularity |
|-----------|-------------|
| Hermes `cronjob` | Cron / `every Nm` — exact schedule |
| Rook heartbeat | Wake-bound (e.g. every 12h) — "due on next wake" |

Fuzzy reminders ("Friday") → Rook HEARTBEAT. "In 17 minutes" or **early-morning flight** → Hermes one-shot script calling `notify-joe.sh` — see `references/hermes-cron-rook-dm.md`.

## Adding reminders from a Paul session

Paul edits Rook's `~/.openclaw/agents/<agent>/workspace/HEARTBEAT.md` directly. For items due **today**, also invoke `notify-joe.sh` once and mark the table row `sent`. Template: `references/heartbeat-personal-reminders.md`.

## Duplicate beats (avoid)

If both Paul cron and Rook HEARTBEAT scrape the same accounts, pause or retarget one. Typical split: Rook collects + optional Joe DM digest; Paul curates + posts to group.