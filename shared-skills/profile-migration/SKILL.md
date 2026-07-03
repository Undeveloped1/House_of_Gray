---
name: profile-migration
description: "Migrate a Hermes agent from default to a dedicated named profile, or between profiles."
version: 1.0.0
category: hermes-maintenance
---

# Profile Migration

Migrate a Hermes agent from the default profile to a dedicated named profile, or between profiles. Uses a phased, non-destructive approach: copy everything first, verify, then switch over.

## When to Use

- Moving an agent out of the `default` profile into its own named profile
- Consolidating or splitting profiles
- Creating a clean parallel profile from an existing one

## Prerequisites

- The target profile should already exist (`hermes profile create <name> --clone-all`)
- Both profiles should have compatible model configs
- You have access to the running gateway's systemd service

## Phases

### Phase 1 — Copy (non-destructive)

```
A. Docs:   cp -r /root/.hermes/docs/<Agent>/ → /root/.hermes/profiles/<name>/docs/<Agent>/
B. Skills: copy agent-specific skills from source skills/ to target skills/
C. Config: ensure config.yaml has model, gateway, and platform settings
D. .env:    verify API keys are present in target profile
E. AGENTS.md: update all path references to point to new profile layout
```

AGENTS.md path replacements:
```
/root/.hermes/docs/<Agent>/   →  /root/.hermes/profiles/<name>/docs/<Agent>/
```

Preserve external paths (shared repos, syncthing directories, shared venvs).

### Phase 2 — Verify

```bash
# Smoke test the new profile
hermes --profile <name> chat -q "Who are you and where is your vault root?"

# Verify AGENTS.md has no stale paths
grep '/root/.hermes/docs/' ~/.hermes/profiles/<name>/AGENTS.md  # should return nothing
```

### Phase 3 — Switchover

The gateway's suicide prevention blocks stop/restart from inside the gateway process. Use a cron job to execute the switch from outside:

```bash
# Create a one-shot cron job with no_agent=true
cronjob(action="create",
  name="Profile Switchover",
  schedule="1m",
  repeat=1,
  no_agent=True,
  script="""#!/bin/bash
set -e
systemctl --user stop hermes-gateway.service
sleep 2
hermes --profile <name> gateway start
sleep 3
hermes --profile <name> gateway status
""")
```

### Phase 4 — Cleanup (days later, after stability confirmed)

Remove agent-specific content from the source profile. Do not remove shared skills or shared infrastructure.

## Pitfalls

1. **Gateway suicide prevention:** Any attempt to stop/restart the gateway from within the gateway process is blocked. Must use cron or an external shell.
2. **State.db:** Sessions are profile-scoped. `--clone-all` copies everything EXCEPT session history. To migrate sessions, manually copy `state.db` — but only while the source gateway is stopped.
3. **Telegram bot token:** Two profiles cannot use the same Telegram bot token simultaneously. The webhook routes to whichever gateway set it last.
4. **RAG venv:** Shared infrastructure like `/root/.hermes/rag-venv/` should stay in place. Only update the path references in AGENTS.md.
5. **Cron jobs:** Source profile cron jobs need to be migrated or recreated in the target profile.
6. **Changing provider without verifying API keys:** Before switching a profile's provider (e.g., from Nous OAuth to DeepSeek), ALWAYS check that the profile's `.env` contains the corresponding API key. A profile may have been set up with only OAuth credentials — flipping `provider: deepseek` without `DEEPSEEK_API_KEY` in `.env` will hard-break the gateway with `RuntimeError: Provider 'deepseek' is set but no API key was found`. Verify first: `grep 'API_KEY' ~/.hermes/profiles/<name>/.env`.
7. **Incomplete bot profiles:** A bot profile created via `hermes profile create` may be missing critical pieces — platform allowlists (`TELEGRAM_ALLOWED_USERS`), provider API keys, and authorization. Before declaring a bot "ready," run the checklist in `references/bot-profile-setup.md`.
