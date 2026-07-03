# Hermes Desktop Repair: Windows

The `hermes-desktop-repair` SKILL.md covers macOS paths and tooling. This file adds Windows-specific knowledge.

## Source Code Location

The Hermes Desktop source on Windows:
```
%LOCALAPPDATA%\hermes\hermes-agent\apps\desktop\
→ C:\Users\<user>\AppData\Local\hermes\hermes-agent\apps\desktop\
```

From WSL: `/mnt/c/Users/<user>/AppData/Local/hermes/hermes-agent/apps/desktop/`

Project structure: TypeScript + Vite + Electron (`package.json`, `tsconfig.json`, `vite.config.ts`, `src/`, `electron/`). The directory is a full git repo on `main` branch.

## Remote Code Editing via Paul (VPS → Windows)

Paul can edit the Windows Desktop source code through a WSL reverse SSH tunnel. See `paul-vps-operations` → `references/remote-wsl-access.md` for the full setup. Summary:

1. Joe opens tunnel: `ssh -R 2222:localhost:22 paul-dash` (from WSL)
2. Paul connects: `ssh -i /root/.ssh/joe-wsl -p 2222 thegreybeard@localhost`
3. Windows filesystem accessible at `/mnt/c/`
4. Desktop source at `/mnt/c/Users/TheGreyBeard/AppData/Local/hermes/hermes-agent/apps/desktop/`

## Installed App vs Source Code

- **Installed app** (packaged): `AppData/Local/hermes/` — includes `app.asar` in `hermes-agent/apps/desktop/release/win-unpacked/resources/`
- **Source code** (editable): `AppData/Local/hermes/hermes-agent/apps/desktop/` — the git repo with `src/`, `electron/`, etc.

For code fixes destined for a PR to Nous Research, edit the **source code** (git repo), validate locally, then submit.

## Joe's Username

WSL username: `thegreybeard`
Windows username: `TheGreyBeard`
