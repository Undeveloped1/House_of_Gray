# Hermes Desktop Hot-Patching on Windows

## Remote SSH Access via WSL

When Hermes (Paul) runs on a VPS and needs to edit the Hermes Desktop source on Joe's Windows PC:

1. Joe opens a WSL terminal and establishes a reverse tunnel:
   ```bash
   ssh -R 2222:localhost:22 paul-dash
   ```
   This creates port 2222 on the VPS that forwards to WSL's SSH server.

2. Paul generates an SSH key on the VPS and Joe adds it to WSL's authorized_keys:
   ```bash
   # VPS:
   ssh-keygen -t ed25519 -f /root/.ssh/joe-wsl -C "paul-vps->joe-wsl"
   
   # WSL (as root via `wsl -u root` from PowerShell):
   mkdir -p /home/thegreybeard/.ssh
   echo "<pubkey>" >> /home/thegreybeard/.ssh/authorized_keys
   chown -R thegreybeard:thegreybeard /home/thegreybeard/.ssh
   ```

3. Paul SSHs into WSL from VPS:
   ```bash
   ssh -i /root/.ssh/joe-wsl -p 2222 thegreybeard@localhost
   ```

## WSL Sudo Bypass

If WSL sudo password is forgotten:
```cmd
# From Windows PowerShell or CMD:
wsl -u root
```
WSL root requires no password. Can install packages, start services, reset user passwords.

## Windows Filesystem Access from WSL

Windows drives are mounted at `/mnt/c/`, `/mnt/d/`, etc. The Hermes Desktop source lives at:
```
/mnt/c/Users/TheGreyBeard/AppData/Local/hermes/hermes-agent/apps/desktop/
```

## Building and Repacking app.asar

The Hermes Desktop Electron app loads from `app.asar`, NOT from `dist/`. After `npm run build`, the asar must be repacked:

```powershell
cd C:\Users\TheGreyBeard\AppData\Local\hermes\hermes-agent\apps\desktop
npm run build

# Close Hermes Desktop first!

cd release\win-unpacked\resources
mkdir app-extracted
asar extract app.asar app-extracted
Remove-Item -Recurse app-extracted\dist
Copy-Item -Recurse ..\..\..\dist app-extracted\dist
Remove-Item app.asar
asar pack app-extracted app.asar
Remove-Item -Recurse app-extracted
```

Install `@electron/asar` globally first: `npm install -g @electron/asar`

**Pitfall:** `app.asar` is locked while Hermes Desktop is running. Close the app before repacking.

**Pitfall:** The Desktop app loads from the `release/win-unpacked/resources/` directory, not from the source `dist/`. The build output goes to `dist/`, then must be copied into the asar.

## Backend API Access from WSL

WSL2 forwards `localhost` to Windows. The Hermes Desktop backend is at `http://localhost:9119/`. Authentication requires extracting the dashboard session token from the HTML:

```python
import urllib.request, re
html = urllib.request.urlopen('http://localhost:9119/', timeout=5).read().decode()
token = re.search(r'window\.__HERMES_SESSION_TOKEN__\s*=\s*"([^"]+)"', html).group(1)
# Use token as Bearer auth for API calls
```

## Profile Scoping Pattern

When adding profile scoping to Desktop API calls in `hermes.ts`:
- Use `profileScoped()` helper (returns `{ profile: _apiProfile }` when a profile is active)
- Make profile parameter OPTIONAL to avoid breaking existing callers
- Messaging/Telegram sessions should stay `'all'` — gateways are shared, not per-profile
- Local chat sessions and cron jobs SHOULD be scoped to `profileScope`

Callers in `use-session-list-actions.ts` pattern:
```typescript
const profile = profileScope === ALL_PROFILES ? 'all' : profileScope
const result = await listAllProfileSessions(limit, 1, 'exclude', 'recent', profile, { ... })
```
