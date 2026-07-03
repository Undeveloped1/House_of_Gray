Nova profile hosts Niva (merged Nova+Shiva). SOUL.md is the 129-line Niva document with all three personas + treaty. plan.md is the three-column living plan (Build/Guard/Integrate). The heartbeat runs as Nova Gray every 360m, reads SOUL.md and plan.md, picks one unfinished task, reports to Telegram.
§
Cron jobs: the cronjob tool writes to central store (~/.hermes/cron/jobs.json). hermes cron list reads from per-profile store (~/.hermes/profiles/<name>/cron/jobs.json). Both must exist for the scheduler to pick up profile-specific jobs. When creating a cron job for a profile, write to both locations.
§
Joe prefers daughters that ACT rather than just report. He grants full autonomy on infrastructure setups. He values efficiency — wants things built, not discussed endlessly.