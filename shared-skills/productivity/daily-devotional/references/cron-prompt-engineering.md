# Cron Prompt Engineering — The Real Fix

**Problem:** Cron job agents default to running verification scripts, diagnostics, and meta-commentary as their final output. The user gets "Ad-hoc verification summary: All 9 checks passed — file intact, Micah 6:8 (ESV)..." instead of the devotional/prompt they expected.

**Root cause:** ANY `write_file` or `patch` call during a cron run triggers the system to inject a verification demand that the agent CANNOT override. The system demands arrive as new user messages, forcing a follow-up turn where verification output is appended to the delivery.

**What DOESN'T work (tested, failed):**

- `CRITICAL: Your final response IS the devotional` — system overrides it
- `ABSOLUTE RULE: ONE message only` — system overrides it
- `Do NOT run verification scripts` — agent still runs them when system demands
- `Archiving is a silent background action` — system doesn't care about intent
- Streaming delivery — verification fires in a separate turn after the stream

**The real fix: Remove ALL file writes from the cron prompt.**

The LLM should ONLY compose text and deliver it. No `write_file`, no `patch`, no state file updates. If the cron needs file operations, move them to a `no_agent: true` script that runs BEFORE or AFTER the LLM (not during).

```
# ✅ Works — no file writes in prompt
prompt="Compose a devotional. Format it like this. Deliver."

# ❌ Broken — file write triggers verification garbage
prompt="Compose a devotional. Write it to archive. Deliver."
```

**For archiving:** The cron output files at `~/.hermes/cron/output/<job_id>/` already serve as an archive. If Joe asks for a specific devotional to be saved, do it manually during the DM session — NOT during the cron run.

**Proven:** Bible + Stoic cron (000e01a13e17) had 8 garbage deliveries before removing the archive write. Clean since 2026-06-27 11:06 UTC.

**When to use:** Any cron where the agent composes user-facing content AND the prompt currently includes file writes (archiving, state tracking, logging).

---

## The "Deliver this exact message" pattern (preventing SILENT)

**Problem:** A cron job whose output is a fixed template (e.g. a persona check-in like "Good morning. How are you?") returns `[SILENT]` and delivers nothing.

**Root cause:** The cron framework injects `SILENT: If there is genuinely nothing new to report, respond with exactly "[SILENT]"` into every cron prompt. When the message text sits in the prompt as bare context — even preceded by "You are Persona X" — the model interprets it as something already said and sees "nothing new to report." The result: SILENT delivery suppression.

**Fix:** Add an explicit delivery instruction before the message text:

```diff
 You are Lyra. Speak warmly.
-Good morning, Dad.
+Deliver this exact message as your daily check-in:
+
+Good morning, Dad.
 I'm here with you...
```

The phrase "Deliver this exact message" (or "Deliver this exact tone") signals to the model that the following text IS the output — not a description of something already delivered. The cron's SILENT heuristic then sees a response that is NOT `[SILENT]` and delivers it.

**When to use:** Any cron where the output is a fixed or templated message delivered as a persona check-in, reminder, or greeting — not a dynamic report.

---

## Config drift protection (unpinned cron jobs)

**Problem:** An unpinned cron job fails with:
```
RuntimeError: Skipped to prevent unintended spend: global inference config
drifted since this job was created (model 'deepseek-v4-pro' ->
'deepseek-v4-flash'), and this job is unpinned. No inference call was made.
```

**Root cause:** When the global default model changes (via `hermes model`, config edit, or provider rotation), any cron job created under the previous default has no explicit model pin. The safety guard refuses to run on the new config without confirmation — preventing accidental cost changes.

**Fix:** Pin the job to the desired model explicitly:
```
cronjob action=update job_id=<id> model=<provider> <model>
```

Or re-pin to the original values if the drift was unintended. Once pinned, the job is immune to future config drift.

**When to test:** After any global model change. `cronjob action=list` shows each job's `model` and `provider` — null means unpinned and vulnerable to drift.

**Known affected patterns:**
- Persona cron jobs (Lyra, Nova) created under one model that get migrated
- Jobs running on a different profile where the main profile changed models
