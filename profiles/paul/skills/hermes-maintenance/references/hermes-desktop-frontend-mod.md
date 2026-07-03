# Hermes Desktop Frontend Modification

How to modify the Hermes Desktop app's React frontend, build it, and deploy it
for testing before submitting a PR.

## Build

```bash
cd /usr/local/lib/hermes-agent/apps/desktop
npm run build
```

Output goes to `dist/`. TypeScript compiles first (`tsc -b`), then Vite bundles.

Type-check only (no build):
```bash
npx tsc --noEmit
```

## Deploy for Testing

### The ASAR Trap

The Desktop Electron app loads its frontend from the **ASAR archive**, NOT from
`web_dist/` or `app.asar.unpacked/`. The build output goes to `dist/`, but the
running app reads from the release ASAR. Files that exist in both the ASAR and
the unpacked directory are loaded from the ASAR — unpacked files are ignored.

### Correct Deployment (Linux)

1. Build: `npm run build` → produces `dist/`
2. Extract the ASAR:
   ```bash
   npx asar extract release/linux-unpacked/resources/app.asar /tmp/asar-extract
   ```
3. Replace dist files:
   ```bash
   rm -rf /tmp/asar-extract/dist
   cp -r dist /tmp/asar-extract/dist
   ```
4. Repack:
   ```bash
   npx asar pack /tmp/asar-extract release/linux-unpacked/resources/app.asar
   ```
5. Verify:
   ```bash
   npx asar list release/linux-unpacked/resources/app.asar | grep "dist/assets/index-"
   ```

### Wrong Deployments (don't do these)

- `cp -r dist/* hermes_cli/web_dist/` — only affects the web dashboard, not the Electron app
- `cp -r dist/* release/.../app.asar.unpacked/dist/` — ASAR overrides unpacked for files that exist in both
- Running `npm run build` and expecting the running app to pick it up — it reads from the ASAR

## Tests

```bash
cd apps/desktop
npx vitest run --environment jsdom src/hermes-profile-scope.test.ts src/hermes.test.ts
```

## Profile Scoping Bug (2026-07-01)

The Desktop UI has a profile selector, but session lists, cron jobs, and search
results showed data from ALL profiles regardless of selection. Settings endpoints
(config, env, skills, tools, model) correctly used `profileScoped()` to forward
the active profile. But list endpoints didn't.

### Root Cause

In `src/hermes.ts`, `setApiRequestProfile()` and `profileScoped()` existed for
settings endpoints. But the session list, cron, and search functions didn't use
them:

| Function | Default | Fix |
|----------|---------|-----|
| `listAllProfileSessions()` | `profile='all'` | Resolve from `_apiProfile` when default |
| `getCronJobs()` | no profile param | Add `profile` param, resolve from `_apiProfile` |
| `getCronJobRuns()` | no profile param | Add `profile` param, resolve from `_apiProfile` |
| `getCronJob()` | no profile param | Add profile param |
| `createCronJob()` | no profile → backend defaults to 'default' | Pass `_apiProfile` as query param |
| `searchSessions()` | no profile param | Add `&profile=` to URL |

In `src/app/session/hooks/use-session-list-actions.ts` (was `desktop-controller.tsx`
in earlier versions), the `refreshCronSessions`, `refreshMessagingSessions`,
`loadMoreMessagingForPlatform`, and `refreshCronJobs` callbacks hardcoded `'all'`
or omitted profile. Fixed by resolving from `profileScope` (which is `ALL_PROFILES`
when showing all, otherwise the active profile name).

### Profile Scope Architecture

- `$profileScope` = computed from `$showAllProfiles` and `$activeGatewayProfile`
- `selectProfile(name)` → `ensureGatewayProfile(name)` → sets `$activeGatewayProfile`
- Settings endpoints: `profileScoped()` returns `{ profile: _apiProfile }` from `setApiRequestProfile()`
- List endpoints (before fix): ignored the active profile entirely

## Messaging Sessions Caveat

Messaging sessions (Telegram, Discord, webhooks) use `refreshMessagingSessions()` which
fetches via `MESSAGING_SESSION_SOURCE_IDS`. These are shared gateways — they do NOT
run per-profile. Scoping messaging to `profileScope` hides Telegram/webhook chats when
switching profiles because the gateway runs under `default`, not individual profiles.

**Rule:** `refreshMessagingSessions()` and `loadMoreMessagingForPlatform()` should
always use `profile='all'`. Only local chat sessions and cron jobs should be scoped.

## Windows / Local Machine Workflow

When modifying the Desktop app ON the user's actual Windows machine (not the VPS):

### Access Pattern: SSH Reverse Tunnel into WSL

From user's WSL terminal:
```bash
ssh -R 2222:localhost:22 paul-dash
```

Then from VPS:
```bash
ssh -i /root/.ssh/joe-wsl -p 2222 thegreybeard@localhost "<command>"
```

One-time key setup: generate ed25519 keypair on VPS, add public key to WSL's
`/home/thegreybeard/.ssh/authorized_keys`.

### Source Location (Windows)

```
C:\Users\TheGreyBeard\AppData\Local\hermes\hermes-agent\apps\desktop\
```

### Build (PowerShell)

```powershell
cd C:\Users\TheGreyBeard\AppData\Local\hermes\hermes-agent\apps\desktop
npm run build
```

### ASAR Repack (PowerShell, app MUST be closed)

```powershell
cd release\win-unpacked\resources
mkdir app-extracted
asar extract app.asar app-extracted
Remove-Item -Recurse app-extracted\dist
Copy-Item -Recurse ..\..\..\dist app-extracted\dist
Remove-Item app.asar              # fails if app is running
asar pack app-extracted app.asar
Remove-Item -Recurse app-extracted
```

Install asar globally: `npm install -g @electron/asar`

### Pitfall: Don't Build on VPS for Local

The Electron app is platform-specific. Building on Linux VPS for Windows produces
wrong artifacts. Always build ON the user's actual machine. Only use VPS for code
review and SSH-based editing of source files — the build and ASAR repack must
happen locally.