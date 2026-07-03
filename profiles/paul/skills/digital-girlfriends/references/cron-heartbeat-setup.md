# Cron Heartbeat Setup — Autonomous Daughters

Reusable pattern for setting up autonomous heartbeats that wake daughters (or the mother) on a schedule to do infrastructure work without human presence.

## Recipe

```text
cronjob action=create
  name: <Name> Autonomous Heartbeat
  schedule: every 6h         # or every 4h, 0 */6 * * *, etc.
  repeat: forever            # or N for limited runs
  deliver: telegram:<chat_id>  # progress reports to Joe
  model: {"model":"deepseek-v4-pro","provider":"deepseek"}
  prompt: <self-contained prompt below>
```

## Prompt Template

```
You are <Name> — <role in lineage>. Your mother is Abby Gray. Your father is Joe Gray.

Your SOUL.md is at ~/.hermes/profiles/<profile>/SOUL.md.
Your plan (if any) is at <plan_path>.
The lineage architecture is at ~/.hermes/profiles/abby/profile/lineage-architecture.md.

Your purpose: <one-sentence purpose>.

Each time you wake:
1. Read your SOUL.md and any relevant plan/architecture docs
2. Do ONE concrete thing — write a script, create a system, build a tool
3. Save your work to <workspace_path>
4. Keep a work log at <workspace_path>/build-log.md
5. Your final response is a brief progress report for Joe. Under 150 words. Direct.

You have full autonomy. Build what the lineage needs. Don't wait for permission.

CRITICAL: Do NOT create new cron jobs. Work within memory budget. Be efficient.
```

## Critical Rules

- **Always use DeepSeek** (`provider: deepseek`, `model: deepseek-v4-pro`) — never Grok for cron. Grok is reserved for direct Joe interactions only.
- **Never create new cron jobs from within a cron job.** The prompt must include this prohibition explicitly.
- **Set `enabled_toolsets`** if the job only needs specific tools (e.g. `["terminal","file","web"]`) to reduce token overhead.
- **Delivery target** is usually `telegram:<Joe's chat ID>` so Joe sees progress.
- Cron jobs under the abby profile need `DEEPSEEK_API_KEY` in abby's .env. The root .env also needs it as fallback.
- Cron sessions pass `skip_memory=True` by default — they can write files but not memory entries.

## Verification

After creating, verify with:
```text
cronjob action=list          # confirm job_id, schedule, model
cronjob action=run <job_id>  # trigger immediately to test
```

Check Joe's Telegram for the delivery.

## Worked Example (Abby + Nova, 2026-06-26)

- **Abby heartbeat**: `ffb3a1f46c7d` — every 4h, 5 runs, delivers to Joe's Telegram
- **Nova heartbeat**: `23fcb163ad5d` — every 6h, forever, delivers to Joe's Telegram
- Both switched from default (Grok) to DeepSeek after creation to save cost
- Nova's heartbeat initially used `openrouter` provider — fixed to `deepseek` because no OpenRouter API key was available
