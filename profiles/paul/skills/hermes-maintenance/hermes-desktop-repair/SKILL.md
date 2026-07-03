---
name: hermes-desktop-repair
description: Diagnose and repair a broken Hermes Desktop app on macOS — setup helper stuck, missing Electron runtime, npm ignore-scripts, auto-update failure, version mismatch between CLI and desktop.
tags: [hermes, desktop, repair, macos, electron]
---

# Hermes Desktop Repair (macOS)

## When to Use

- Hermes Desktop shows "Install" / setup helper instead of the real app
- Hermes Desktop won't launch or silently fails after auto-update
- `/Applications/Hermes.app` is the setup helper, not the real app
- Electron runtime missing (`npm config get ignore-scripts` = true)

## Root Causes

The desktop app can get stuck or show the wrong version for three main reasons:

1. **Auto-update downloaded but failed to replace** `/Applications/Hermes.app` — the setup helper remains in place.
2. **Desktop build failed** due to missing Electron runtime — commonly caused by `npm ignore-scripts=true`, which prevents Electron's postinstall script from downloading the Electron binary.
3. **Desktop package.json version string was never bumped.** The CLI and actual code are current (`hermes update` succeeds, same git commit), but `apps/desktop/package.json` hardcodes an old version like `0.15.1`. The desktop runs correct code but *displays* the stale version. This is NOT cosmetic — version mismatches confuse users and should be fixed.

## Diagnostic Steps

### Step 0: Check for version mismatch between CLI and desktop sources

```bash
hermes --version | head -1
grep '"version"' ~/.hermes/hermes-agent/apps/desktop/package.json
```

If CLI reports a newer version but desktop package.json is behind, this is root cause #3 — bump and rebuild (see "Step 5b: Version string mismatch" below).

### Step 1: Is /Applications/Hermes.app real or the setup helper?

```bash
defaults read /Applications/Hermes.app/Contents/Info CFBundleIdentifier
defaults read /Applications/Hermes.app/Contents/Info CFBundleExecutable
```

| State | CFBundleIdentifier | CFBundleExecutable |
|-------|-------------------|-------------------|
| **Real app** (good) | `com.nousresearch.hermes` | `Hermes` |
| **Setup helper** (broken) | `com.nousresearch.hermes.setup` | `Hermes-Setup` |

### Step 2: Check logs for build/update failures

```bash
tail -260 ~/.hermes/logs/desktop.log
tail -260 ~/.hermes/logs/bootstrap-installer.log
```

Look for errors like:
- `electronDist does not exist` — Electron runtime missing
- `~/.hermes/hermes-agent/node_modules/electron/dist` path not found
- Pack/rebuild failure messages

### Step 3: Check Electron runtime

```bash
ls -lah ~/.hermes/hermes-agent/node_modules/electron
ls -lah ~/.hermes/hermes-agent/node_modules/electron/dist
npm config get ignore-scripts --location=project
npm config get ignore-scripts --location=user
```

If `electron/dist` is missing and `ignore-scripts` = true, that's the cause. Electron's postinstall script downloads the Electron binary — ignored when scripts are disabled.

## Repair Steps

### Step 4: Rebuild Electron (with scripts enabled)

```bash
npm -C ~/.hermes/hermes-agent rebuild electron --ignore-scripts=false
```

Verify:

```bash
ls -lah ~/.hermes/hermes-agent/node_modules/electron/dist
node -e "console.log(require('$HOME/.hermes/hermes-agent/node_modules/electron'))"
```

### Step 5: Rebuild Hermes Desktop

```bash
npm -C ~/.hermes/hermes-agent/apps/desktop run pack
```

### Step 6: Replace /Applications/Hermes.app

```bash
stamp=$(date +%Y%m%d-%H%M%S)
mv /Applications/Hermes.app "/Applications/Hermes-setup-backup-$stamp.app"
ditto ~/.hermes/hermes-agent/apps/desktop/release/mac-arm64/Hermes.app /Applications/Hermes.app
xattr -dr com.apple.quarantine /Applications/Hermes.app 2>/dev/null || true
```

Note: `release/mac-arm64` — adjust to `mac-arm64` or `mac-x64` depending on architecture.

### Step 7: Launch and verify

```bash
open /Applications/Hermes.app
sleep 5
defaults read /Applications/Hermes.app/Contents/Info CFBundleIdentifier
defaults read /Applications/Hermes.app/Contents/Info CFBundleVersion
pgrep -laf "/Applications/Hermes.app|Contents/MacOS/Hermes|Hermes Helper|hermes_cli.main dashboard"
```

Also check if launchd services are running:

```bash
launchctl list | grep -i hermes
```

## Version Mismatch Repair (CLI current, desktop package.json stale)

This is a lighter fix than the Electron rebuild — no missing binary, just a stale version string.

**Symptom:** `hermes --version` says e.g. `v0.16.0`, but the desktop app displays `0.15.1`. The actual desktop code is on the same git commit as the CLI. The version string in `apps/desktop/package.json` was never bumped.

### Fix: Bump and rebuild

```bash
# Bump the version in desktop package.json
sed -i '' 's/"version": "0.15.1"/"version": "0.16.0"/' ~/.hermes/hermes-agent/apps/desktop/package.json

# Rebuild and launch
hermes desktop --force-build
```

On a remote/VPS where you can't run the GUI, the build will succeed but launch will fail (headless) — the artifact at `release/linux-unpacked/Hermes` is still built correctly. Copy it to the target machine or rebuild locally.

Verify after rebuild:

```bash
grep '"version"' ~/.hermes/hermes-agent/apps/desktop/package.json
hermes --version | head -1
```

Both should now match.

**Pitfall:** Don't dismiss this as "cosmetic." A version mismatch is a real bug — the user sees the wrong version and distrusts the update. The fix is one line and a rebuild. the user's model/provider config unless explicitly asked. This repair is about the desktop app/update loop, not switching models.

## Pitfalls

- **User forgot to rebuild Electron first.** Even if the CLI is up to date (`hermes update` succeeds), the desktop pack WILL fail if Electron's runtime isn't present. Rebuild Electron with `--ignore-scripts=false` before packing.
- **`hermes desktop --force-build` is simpler but may fail silently** for the same Electron-missing reason. When both fail, the root cause is always: Electron dist missing + ignore-scripts.
- **`npm config get ignore-scripts --location=user` may differ from `--location=project`.** Check both. The user-level setting is what matters for the repair, but the project-level `.npmrc` may override it.
- **Don't dismiss version mismatches as "cosmetic."** If the CLI reports v0.16.0 but the desktop says 0.15.1, that's a real bug — the user sees the wrong version and distrusts the update. The package.json version string needs to be bumped and the desktop rebuilt.
- **Don't `rm` the old app — `mv` it with a timestamp backup.** If the rebuild fails, you can restore.
