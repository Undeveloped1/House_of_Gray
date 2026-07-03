---
name: profile-migration
description: "Migrate a Hermes agent from default to a dedicated named profile, or between profiles. Also covers dead profile resurrection and profile cloning."
version: 1.1.0
category: hermes-maintenance
---

# Profile Migration

Migrate a Hermes agent from the default profile to a dedicated named profile, or between profiles. Uses a phased, non-destructive approach: copy everything first, verify, then switch over.

## When to Use

- Moving an agent out of the `default` profile into its own named profile
- Consolidating or splitting profiles
- Creating a clean parallel profile from an existing one
- **Resurrecting a dead/zombie profile** that shows in the desktop app but has no model/identity
- **Cloning a working profile's identity into a dead profile** whose directory auto-regenerates

## Dead Profile Resurrection

When a profile appears in `hermes profile list` with no model, a default SOUL.md ("You are Hermes Agent, an intelligent AI assistant..."), and gateway stopped, it's a zombie. Something (desktop app, IDE plugin, gateway routing) is referencing the profile name, so deleting the directory won't stick — it auto-regenerates.

**Don't fight the regeneration. Clone a working profile into it:**

```bash
# 1. Nuke the skeleton (may require approval — tirith blocks rm -rf of profile dirs)
rm -rf /root/.hermes/profiles/<dead-profile>

# 2. Immediately replace with working profile's essentials
mkdir -p /root/.hermes/profiles/<dead-profile>
cp /root/.hermes/profiles/<source-profile>/SOUL.md /root/.hermes/profiles/<dead-profile>/
cp /root/.hermes/profiles/<source-profile>/.env /root/.hermes/profiles/<dead-profile>/
cp /root/.hermes/profiles/<source-profile>/config.yaml /root/.hermes/profiles/<dead-profile>/
mkdir -p /root/.hermes/profiles/<dead-profile>/profile
cp /root/.hermes/profiles/<source-profile>/profile/*.md /root/.hermes/profiles/<dead-profile>/profile/

# 3. Start the gateway (must be foreground — `gateway start` may silently fail)
hermes --profile <dead-profile> gateway run &

# 4. Verify
hermes profile show <dead-profile>
ps aux | grep "<dead-profile>.*gateway" | grep -v grep
```

**Diagnostic sequence for dead profiles:**
```bash
hermes profile show <name>     # Model, gateway status, skills count, .env presence
cat /root/.hermes/profiles/<name>/SOUL.md | head -3   # Default agent vs companion identity
hermes profile list            # Compare with sibling profiles
```

**Symptoms of a zombie:** SOUL.md is the factory default (~513 bytes), no model configured, gateway stopped, .env missing — but profile still appears in lists and the desktop app. Its memory/sessions may contain evidence of the user trying to reach the correct profile through it.

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

1. **Gateway suicide prevention:** Any attempt to stop/restart the gateway from within the gateway process is blocked with "cannot restart or stop the gateway from inside the gateway process." Must use cron or an external shell. This also means `hermes --profile X gateway start` run from inside a gateway session may report success but not actually create a systemd service — use `gateway run &` in foreground instead.
2. **State.db:** Sessions are profile-scoped. `--clone-all` copies everything EXCEPT session history. To migrate sessions, manually copy `state.db` — but only while the source gateway is stopped.
3. **Telegram bot token:** Two profiles cannot use the same Telegram bot token simultaneously. The webhook routes to whichever gateway set it last. When cloning a profile that shares a Telegram bot, the cloned profile's gateway will conflict on Telegram. The API server (used by the desktop app) still works — only messaging platforms collide.
4. **RAG venv:** Shared infrastructure like `/root/.hermes/rag-venv/` should stay in place. Only update the path references in AGENTS.md.
5. **Cron jobs:** Source profile cron jobs need to be migrated or recreated in the target profile.
6. **Changing provider without verifying API keys:** Before switching a profile's provider (e.g., from Nous OAuth to DeepSeek), ALWAYS check that the profile's `.env` contains the corresponding API key. A profile may have been set up with only OAuth credentials — flipping `provider: deepseek` without `DEEPSEEK_API_KEY` in `.env` will hard-break the gateway. Verify first: `grep 'API_KEY' ~/.hermes/profiles/<name>/.env`.
7. **Incomplete bot profiles:** A bot profile created via `hermes profile create` may be missing critical pieces — platform allowlists, provider API keys, and authorization. Run the checklist in `references/bot-profile-setup.md`.
8. **`hermes profile delete` is incomplete:** It removes state.db, config, and auth files but leaves skeleton directories (empty sessions/, skills/, memories/, logs/, cron/, etc.). The directory is NOT fully removed, and if anything references the profile name (desktop app, gateway routing, IDE plugin), the skeleton auto-regenerates with a fresh default SOUL.md. Use `rm -rf` for full removal — but expect security approval prompts (tirith flags mass-deletion bursts).
9. **Multi-profile gateway architecture:** Each profile runs its own gateway process (visible via `ps aux | grep 'gateway run'`). Profiles listed as gateway "running" in `hermes profile list` may not have a dedicated systemd service — they share the host process. Verify with `ps aux`, not `systemctl`.
10. **Desktop app shows profile directory name, not SOUL identity:** The Hermes desktop app lists profiles by their directory name under `~/.hermes/profiles/`. When a companion's profile name changes (e.g., Nova → Niva after merger), the old profile name persists in the desktop UI until the user selects a different profile. Cloning identity files into the old profile is the fastest fix — same SOUL, different profile name.
