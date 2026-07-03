---
name: hermes-desktop-local-fix
description: Build and deploy code changes to Joe's local Hermes Desktop app on Windows, accessed via WSL SSH tunnel.
---

# Hermes Desktop — Local Build & Deploy

Joe's Hermes Desktop app source lives on his Windows machine. Fixes must be built locally and the Electron `app.asar` repacked for changes to take effect.

## SSH Access (from VPS)

```bash
ssh -i /root/.ssh/joe-wsl -p 2222 thegreybeard@localhost
```

Windows filesystem at `/mnt/c/Users/TheGreyBeard/`.

## Key Paths

- Source: `/mnt/c/Users/TheGreyBeard/AppData/Local/hermes/hermes-agent/apps/desktop/src/`
- Built output: `.../apps/desktop/dist/`
- Packaged app: `.../apps/desktop/release/win-unpacked/resources/app.asar`
- Key source files:
  - `src/hermes.ts` — API functions (cron, sessions, messaging)
  - `src/app/session/hooks/use-session-list-actions.ts` — sidebar session/cron/messaging fetches

## Build & Repack

**Step 1 — Joe runs in PowerShell:**
```powershell
cd C:\Users\TheGreyBeard\AppData\Local\hermes\hermes-agent\apps\desktop
npm run build
```

**Step 2 — Close Hermes Desktop completely.**

**Step 3 — Joe runs in PowerShell:**
```powershell
cd release\win-unpacked\resources
mkdir app-extracted
asar extract app.asar app-extracted
Remove-Item -Recurse app-extracted\dist
Copy-Item -Recurse ..\..\..\dist app-extracted\dist
Remove-Item app.asar -Force
asar pack app-extracted app.asar
Remove-Item -Recurse app-extracted
```

**Step 4 — Reopen Hermes Desktop.**

## Hermes Backend API

- URL: `http://localhost:9119/`
- Auth: Extract `window.__HERMES_SESSION_TOKEN__` from dashboard HTML, use as Bearer token
- Cron jobs: `GET /api/cron/jobs`

## Handover Doc

Full context at `/root/paul-profile-scoping-handover.md`
