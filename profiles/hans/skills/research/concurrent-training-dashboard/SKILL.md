---
name: concurrent-training-dashboard
description: "Combined weekly dashboard for athletes running multiple concurrent training modalities (e.g., lifting + BJJ) — unified tracking, RPE-based auto-regulation, and recovery management."
platforms: [linux]
---

# Concurrent Training Dashboard

## When to use

Joe is running **two or more training modalities simultaneously** (e.g., strength training 3×/week + BJJ 2×/week) and needs a unified tracking system that:

- Shows all sessions on one page
- Communicates fatigue between modalities (Thursday BJJ intensity → Friday lift adjustment)
- Tracks RPE, sleep, and weight daily
- Has auto-regulation rules to prevent overtraining
- Includes a weekly review ritual

Do NOT use when Joe is only doing one modality. The standard workout log files (`workouts/fullbody-ramp.md`, `workouts/bjj-journal.md`) are sufficient for single-modality tracking.

## Dashboard structure

Create at `workouts/weekly-dashboard.md`. The file is a living document — update it after every session, not just at the end of the week.

### Daily Log table

| Column | Purpose |
|--------|---------|
| Day | Mon–Sun |
| Date | MM/DD |
| Activity | "Lift," "BJJ," "Rest" |
| RPE (1–10) | Session intensity — see the RPE scale below |
| Sleep (hrs) | Previous night's sleep |
| Weight (kg) | Morning weigh-in, same conditions |
| Key Note | One-line: what happened, how it felt, anything relevant |

### Lift Sessions section

Each lift session gets a table with: exercise, sets × reps target, weight, per-set RPE, and a **session-level RPE** after the table. Include a **pre-session note** that references the previous day's activity and any auto-regulation adjustments.

### BJJ Sessions section

Each BJJ session gets a metrics table (duration, rounds, focus, post-session RPE) and a **Friday lift modifier** row: ⬜ Normal / ⬜ Reduced / ⬜ Skip. This is the bridge between systems.

### Recovery Rules section

Codify the auto-regulation logic:

| Rule | Detail |
|------|--------|
| **Friday lift modifier** | After Thursday BJJ, mark whether Friday is normal / reduced volume (2 sets, lighter weight) / skipped |
| **Monday adjustment** | If Friday was RPE 8+, Monday squat stays flat — no weight increase |
| **Deload trigger** | Any session at RPE 9+ two weeks in a row → next week deload at 50% volume |
| **Return from layoff** | After 2+ weeks off, first 2 sessions back are auto-reduced regardless of RPE |

### Weekly Review section (Sunday)

Template with 4 prompts:
- Best session this week
- Hardest session
- Fatigue trend (↑ ↓ →)
- One thing to adjust next week

This takes 2 minutes and prevents the systemic drift that kills long-term programs.

## RPE Scale (1–10)

| RPE | Meaning | Training Implication |
|-----|---------|---------------------|
| 1–4 | Easy. Could've done twice as much. | Too light — increase next session |
| 5–6 | Working. Challenging but manageable. | Sweet spot for most sessions |
| 7–8 | Heavy. Last reps were a fight. | Good effort day. Watch recovery. |
| 9 | Near max. Barely finished. | Flag it. Two in a row = deload. |
| 10 | Absolute limit. Couldn't do one more. | Should be rare. Adjust program. |

**The goal is not to train at RPE 9+ every day.** The goal is to see the *pattern* — if Friday is always 8–9 while Monday is 5–6, BJJ is eating recovery and volume needs to shift.

## Friday Lift Modifier (critical for lifting + BJJ concurrent training)

This is the most important auto-regulation rule. After every Thursday BJJ session, Joe marks one of:

- **Normal** — felt great, full send
- **Reduced** — drop to 2 sets per exercise instead of 3, keep weight light, prioritize form. Use extra time to test/calibrate weights on untested exercises.
- **Skip** — body's cooked, rest wins. Don't feel guilty about it.

The decision is based on: Thursday BJJ RPE, how many weeks since last layoff, and subjective fatigue.

## "Build While Flying" Philosophy

When Joe is just starting a new system (first week of a ramp protocol, first BJJ journal entries), it's expected that gaps will emerge. The dashboard evolves with the training — add columns, rules, and sections as needs surface. The dashboard on week 1 will be simpler than the dashboard on week 12. That's how it should be.

## Daily Log (`workouts/daily-log.md`)

The daily log is the **highest-frequency tracking file** — updated every day, often multiple times. It captures everything the weekly dashboard doesn't: sleep, food, caffeine, nicotine, and subjective feel. The dashboard tracks *training*. The daily log tracks *life*.

### Structure

| Section | Columns | Update cadence |
|---------|---------|----------------|
| Sleep & Recovery | Hours, quality, morning fatigue /10, soreness | Morning (once) |
| Training | Session, duration, RPE, notes | Post-session |
| Body | Morning weight | Morning |
| Nutrition | Time, what, est. kcal | Throughout day (cron + manual) |
| Hydration | Current oz, daily target oz | Throughout day |
| Intake | Caffeine, nicotine | Throughout day |
| How I Feel | Free text | End of day |

### Filling workflow

The user prefers a **batch fill** pattern:

1. Hans presents the missing fields — "Here's what's blank: sleep, fatigue, soreness, food, water, caffeine, nicotine."
2. Joe fires off all the answers in one message.
3. Hans patches the file and returns a clean summary table.

Do NOT ask one question at a time. Present all blanks together. Joe answers in bulk. This is faster and respects his preference for efficiency.

### Relationship to crons

Three food check-in crons (10am, 3pm, 8pm) ping Joe for what he's eaten. These feed the Nutrition section. But Joe often fills the log manually before a cron fires — check the file first during cron runs so you don't ask "what have you eaten?" when it's already logged.

### Calibration: coffee orders

When Joe gives a coffee order, **do not assume defaults.** Ask or infer from his description:

- **Single-shot drinks**: If he says "one shot of espresso," that's ~65mg caffeine, NOT ~150mg (standard double). His caramelo latte from Arido is a 12oz single-shot whole milk drink.
- **House-made syrups/caramels**: These add 30–50 kcal beyond what a chain equivalent would. Don't treat them like Starbucks pumps.
- **Milk matters**: 12oz of whole milk (after accounting for espresso + caramel) is ~10oz of milk, ~180 kcal. Oat/almond would change the math.

Default assumption for Joe's coffee: **single shot, whole milk, ~12oz, local shop** — unless he specifies otherwise.

### Nicotine tracking

Joe uses Zyn pouches. Track by mg, not count — a "1.5mg black cherry" is the standard unit. Log each one in the Intake section as it's reported.

### Hydration tracking

Water is a **permanent field** in the daily log. The Hydration section lives between Nutrition and Intake:

| Metric | Value |
|--------|-------|
| Current | `<oz so far>` |
| Target | `<daily target oz>` |

**Target calculation** — Joe lives in Cabo San Lucas (hot, dry, low humidity, coastal). Calculate per-day, not a static number:

| Factor | Contribution |
|--------|-------------|
| **Baseline** (body weight) | ~0.5 oz per lb of body weight. At ~280 lbs: ~100oz |
| **Climate bump** | Hot + dry + low humidity: +16–24oz |
| **Training day** | 70min BJJ sweat loss: +24–32oz |
| **Rest day** | No training bump |

**Target ranges:**
- Training days: ~130–150oz
- Rest days: ~100–120oz

Joe sometimes adds Himalayan sea salt to his water — note this in the Current field as a signal of electrolyte awareness. It's a positive indicator, not just flavor.

## Pitfalls

- **Template creation dates ≠ execution dates.** Plan files carry old creation timestamps in headers. The dashboard should reflect actual session dates, not when the template was written.
- **RPE inflation after layoffs.** The first 1–2 sessions back after 2+ weeks off will feel harder than the objective workload. A "mid 7" after a 3-week layoff may reflect detraining, not a normally hard session. Use the layoff return rule: first two sessions back are auto-reduced.
- **Empty RPE columns.** The dashboard's value comes from seeing patterns. Two weeks of consistent RPE data reveals recovery problems. One week of empty columns reveals nothing. Make RPE logging non-negotiable.
- **Don't over-structure the BJJ log for a flow-rolling focus.** If Joe's BJJ is non-competitive flow rolling for endurance (not competition prep), tracking "taps given/received" and "submission success rate" is overkill. Duration, rounds, focus area, and RPE are sufficient.
- **Caffeine estimation — don't guess double shots.** Joe's default coffee is a single-shot latte (~65mg caffeine), not a double. Confirm if he hasn't specified. Erring high here inflates caffeine tracking and makes later pattern analysis less useful.
- **Water target is climate-dependent, not static.** Joe lives in Cabo San Lucas — hot, dry, low humidity. A generic "8 glasses a day" recommendation ignores climate + training load. Always calculate based on body weight, climate, and whether it's a training day. See the Hydration tracking section above for the formula.

## References

- `templates/weekly-dashboard-template.md` — blank weekly dashboard template. Copy to `workouts/weekly-dashboard.md` when starting a new training block.
- `references/daily-log-template.md` — blank daily log template. Copy to `workouts/daily-log.md` when starting a new week.
