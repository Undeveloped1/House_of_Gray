# Windows Desktop App: Build + Repack Workflow

## Why Repack?

The Hermes Desktop app loads from `app.asar` (the packaged Electron bundle), NOT from `dist/` directly. Running `npm run build` updates `dist/` but the running app still uses the old asar. A successful build does NOT mean the fix is live.

## Full Workflow

```powershell
# 1. Navigate to the desktop app source
cd $env:LOCALAPPDATA\hermes\hermes-agent\apps\desktop

# 2. Rebuild the frontend (TypeScript + Vite)
npm run build

# 3. Close Hermes Desktop completely, then repack the asar:
cd release\win-unpacked\resources
mkdir app-extracted
npx @electron/asar extract app.asar app-extracted
Remove-Item -Recurse app-extracted\dist
Copy-Item -Recurse ..\..\..\dist app-extracted\dist
Remove-Item app.asar
npx @electron/asar pack app-extracted app.asar
Remove-Item -Recurse app-extracted
```

## Critical Requirements

- **App must be CLOSED** during repack — `app.asar` is locked while Hermes Desktop is running
- **Source is in AppData** — `%LOCALAPPDATA%\hermes\hermes-agent\apps\desktop\`
- **Build output** lands in `dist/` within the desktop app directory
- **Packaged app** is at `release\win-unpacked\resources\app.asar`

## Two-Hermes-Installation Trap

Joe's machine typically has TWO Hermes installations:
- **Windows Desktop** → `%LOCALAPPDATA%\hermes\` — the one Joe actually uses
- **WSL** → `~/.hermes/` — may be defunct; may still have old state.db and gateway configs

Always verify WHICH installation is active before modifying files. The Desktop backend is on `localhost:9119`. Editing the wrong install wastes time.

## Accessing Windows Files from VPS (Paul's Reach)

When Paul needs to edit files on Joe's Windows machine from the VPS:

1. **Reverse SSH tunnel** from Joe's WSL: `ssh -R 2222:localhost:22 paul-dash`
2. **Paul connects**: `ssh -p 2222 thegreybeard@localhost`
3. **Windows files** are at `/mnt/c/Users/TheGreyBeard/...`
4. **Multi-file patches**: use Python scripts over SSH to avoid bash quoting hell with heredocs

## User Preferences

- **Build LOCALLY.** Do not copy source to VPS to build and send back. Joe: "stop building shit on the VPS for this."
- **Answer questions before acting.** Joe: "I'm asking questions don't run off."
