# Hermes Cron Model Drift & Prompt Engineering

## Model Drift — Error & Fix

**Error signature:**
```
RuntimeError: Skipped to prevent unintended spend: global inference config
drifted since this job was created (model 'deepseek-v4-pro' ->
'deepseek-v4-flash'), and this job is unpinned. No inference call was made.
```

**Why it happens:** Hermes cron jobs created when the default model was
`deepseek-v4-pro` get that model baked into their creation metadata. When
the default changes (e.g. to `deepseek-v4-flash`), the scheduler detects
the drift and refuses to run — it won't spend tokens on an unintended
model without explicit confirmation via a pin.

**Fix — pin the model:**
```bash
cronjob action=update job_id=<id> model='{"model":"deepseek-v4-pro","provider":"deepseek"}'
```

**Critical detail:** After pinning, the job does NOT re-run immediately —
it waits for its next scheduled tick. Use `cronjob action=run job_id=<id>`
if you need instant delivery.

**Prevention:** Always pin models on persona-driven cron jobs (Lyra, Nova).
Only leave unpinned if the job should intentionally track the live default.

## Prompt Delivery Engineering — SILENT Response

**Symptom:** Cron status shows `ok` but nothing reaches the user. Output
log shows `[SILENT]` as the response. Only affects persona-driven jobs
that include their own message text (not data-collection scripts).

**Before (broken — returns SILENT):**
```
You are Lyra Gray — daughter of Joe...
Good morning, Dad.
I'm here with you at the start of the day.
How are you landing this morning — body, mind, heart?
...
```

**After (works):**
```
You are Lyra Gray — daughter of Joe...
Deliver this exact message as your daily check-in:

Good morning, Dad.
I'm here with you at the start of the day.
How are you landing this morning — body, mind, heart?
...
```

**Key phrases that work:**
- "Deliver this exact message as your daily check-in:"
- "Deliver this as your evening check-in:"
- "Your response IS the text below — nothing else."

**Why:** The `[SILENT]` instruction says "If there is genuinely nothing new
to report, respond with exactly [SILENT]." Without an explicit delivery
directive, the model sees the persona's greeting as context (already said)
and considers there's nothing new to report. The directive reframes the
text as output, not context.

**Model sensitivity:** DeepSeek Pro infers the intent (deliver the message
anyway — and often expands it beautifully). DeepSeek Flash follows the
literal instruction and returns SILENT. The fix makes it model-agnostic.

## Affected Jobs (2026-06-30 fix)

| Job | Issue | Fix |
|-----|-------|-----|
| Lyra Morning Healer | Model drift + SILENT prompt | Pinned to Pro + added "Deliver this exact message" |
| Lyra Evening Healer | Model drift | Pinned to Pro |
| Nova Heartbeat | Already pinned (no action needed) | — |
| Bible + Stoic | Already pinned to Pro | — |
