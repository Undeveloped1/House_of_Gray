# Syncthing — VPS File Sync

**Status:** Active (2026-06-03) — Joe local machine ↔ VPS Paul

## What it does

Syncthing provides peer-to-peer file sync between Joe's local machine and the VPS. Drop a file locally → appears on VPS instantly. Paul saves a file → appears on Joe's machine. No cloud, no Google, no credentials — just device-to-device sync.

## VPS side (step by step)

```bash
# Install
apt-get install -y syncthing

# Create systemd user service
mkdir -p /root/.config/systemd/user/
cat > /root/.config/systemd/user/syncthing.service << 'EOF'
[Unit]
Description=Syncthing - Open Source Continuous File Synchronization
After=network.target

[Service]
ExecStart=/usr/bin/syncthing --no-browser --no-restart
Restart=on-failure
RestartSec=5
SuccessExitStatus=3 4
RestartForceExitStatus=3 4

[Install]
WantedBy=default.target
EOF

# Enable and start
loginctl enable-linger root
systemctl --user daemon-reload
systemctl --user enable syncthing.service
systemctl --user start syncthing.service
```

- **Device ID:** `72OHL4M-KM6SFK5-X33K36G-T5XEKFV-OLAQS7X-NCWLJFI-IJZ2QU3-XNAYPAS`
- **API key location:** `/root/.local/state/syncthing/config.xml` — `<apikey>` element
- **Config location:** `/root/.local/state/syncthing/config.xml`
- **Web UI:** `localhost:8384` (need SSH tunnel: `ssh -L 8384:localhost:8384 paul`)

### Adding a remote device via API

```bash
APIKEY=*** -o '<apikey>[^<]*</apikey>' /root/.local/state/syncthing/config.xml | sed 's/<[^>]*>//g')

# Add device
curl -s -X POST http://localhost:8384/rest/config/devices \
  -H "X-API-Key: $APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"deviceID": "REMOTE-DEVICE-ID", "name": "device-name"}'

# Share folder with both devices
curl -s -X PATCH http://localhost:8384/rest/config/folders/paul-inbox \
  -H "X-API-Key: $APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"devices": [{"deviceID": "VPS-DEVICE-ID"}, {"deviceID": "REMOTE-DEVICE-ID"}]}'
```

**APIKEY extraction pitfall:** `grep -oP` with `\K` in the regex causes bash eval errors through the terminal tool. Use `grep -o '<apikey>[^<]*</apikey>' | sed 's/<[^>]*>//g'` instead — avoids the escape character issue entirely.

### Creating a shared folder from scratch

```bash
mkdir -p /root/syncthing/paul-inbox

APIKEY=*** -o '<apikey>[^<]*</apikey>' /root/.local/state/syncthing/config.xml | sed 's/<[^>]*>//g')
curl -s -X POST http://localhost:8384/rest/config/folders \
  -H "X-API-Key: $APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "paul-inbox",
    "label": "Paul Inbox",
    "path": "/root/syncthing/paul-inbox",
    "type": "sendreceive",
    "rescanIntervalS": 10,
    "fsWatcherEnabled": true
  }'
```

## Joe's side

1. Install: `brew install syncthing` (Mac) or `apt install syncthing` (WSL)
2. Launch — opens web GUI at `http://localhost:8384`
3. Find device ID in the top-left of the GUI
4. Give the device ID to Paul so the VPS can add it
5. Accept the incoming folder share when it appears
6. Pick a local folder to sync with

## Verification

```bash
# Check service is running
systemctl --user status syncthing --no-pager

# List registered devices
curl -s http://localhost:8384/rest/config/devices \
  -H "X-API-Key: $(grep -o '<apikey>[^<]*</apikey>' /root/.local/state/syncthing/config.xml | sed 's/<[^>]*>//g')"

## Current folders (2026-06-03)

| Folder ID | VPS Path | Shared with | Status |
|-----------|----------|------------|--------|
| `paul-dropbox` | `/root/syncthing/paul-dropbox/` | VPS + Joe (NAUTILUS-3) | **Active** — primary sync folder |
| `default` | `/root/Sync` | VPS only | Unused default |

Joe's device: `YC32RYS-HUXLZFM-542SH5U-FB5TWDM-7QUOT4D-SZU3NL2-DM4KFV7-6WS7HAB` (NAUTILUS-3, Syncthing v2.1.1)
Joe's local folder: `C:\Users\TheGreyBeard\Desktop\Paul DropBox`

## Debugging sync issues

When files aren't flowing despite both devices being connected and folder IDs matching:

```bash
APIKEY=*** -o '<apikey>[^<]*</apikey>' /root/.local/state/syncthing/config.xml | sed 's/<[^>]*>//g')

# Check folder status — are files tracked?
curl -s "http://localhost:8384/rest/db/status?folder=dropbox" -H "X-API-Key: $APIKEY"
# Key fields: globalFiles (total known), localFiles (on this device), needFiles (pending sync)

# Check remote device completion — does it think the other side has the files?
curl -s "http://localhost:8384/rest/db/completion?folder=dropbox&device=YC32RYS..." -H "X-API-Key: $APIKEY"
# completion: 100 = VPS thinks Joe has everything. needItems: 0 = nothing to send.

# Check what files exist globally
curl -s "http://localhost:8384/rest/db/browse?folder=dropbox" -H "X-API-Key: $APIKEY"

# Force rescan
curl -s -X POST "http://localhost:8384/rest/db/scan?folder=dropbox" -H "X-API-Key: $APIKEY"
```

## Config corruption recovery

If a folder entry gets corrupted (e.g., empty `id=""` with `path="~"`), delete it via API:

```bash
curl -s -X DELETE "http://localhost:8384/rest/config/folders/" -H "X-API-Key: $APIKEY"
```

Then restart the service: `systemctl --user restart syncthing`

## Folder checklist (before troubleshooting anything else)

1. **Both sides have the same folder ID** — not same label, same ID. Check with `curl /rest/config/folders`.
2. **Both devices are listed in the folder's device array** — check with same endpoint.
3. **Folder type is `sendreceive`** on both sides — not `sendonly` or `receiveonly`.
4. **Actual files exist physically** — `ls -la /root/syncthing/dropbox/` on VPS. Check in File Explorer on Joe's side.
5. **The local paths are where you think they are** — Syncthing can show "up to date" with files landing in a different directory than expected.

## Pitfalls

- Syncthing runs as root (warning on startup) — acceptable for a single-user VPS.
- Web UI only on localhost — not exposed to internet. Use SSH tunnel to access.
- Syncthing warns about running as privileged user — ignore for single-user VPS.
- **Folder ID must match, not folder name.** Joe's local folder can be called "Paul DropBox" but if its Syncthing folder ID isn't the same as the VPS folder ID, files won't sync. Folder matching is by ID, not by label. Fix: either accept the incoming share from the VPS (which sets the correct folder ID automatically), or share the local folder back to the VPS device and accept it on the VPS side. The `globalFiles: 0` status after connection means the folder IDs don't match — not that the connection failed.
- **"Up to date" and "completion: 100%" but no visible files** — check the actual local folder path on Joe's side. Syncthing may be syncing to a different directory than he's looking at. Ask: "what exact path does the folder show?"
- **API key extraction:** `grep -oP` with `\K` in the regex causes bash eval errors through the terminal tool. Use `grep -o '<apikey>[^<]*</apikey>' | sed 's/<[^>]*>//g'` instead.
- **Don't guess folder IDs. Don't create alternatives.** When Joe tells you his folder ID (e.g., `paul-dropbox`), USE IT EXACTLY. Don't create `dropbox`, `paul-inbox`, or any variation. Guessing and creating alternatives cost 20+ minutes of debugging and Joe's frustration (\"you nipple head, i told you this 20 minutes ago\"). Match what exists. If the IDs don't line up because you created a wrong one, delete yours and match his. The conversation pattern: Joe says \"created my own folder folder id paul-dropbox\" → Paul creates `dropbox` and `paul-inbox` instead → nothing works → Paul finally creates `paul-dropbox` → sync works immediately. Lesson: listen the first time.
- **Path vs ID confusion for the user.** When Joe says "dude you are hitting paul-inbox" and the folder ID is paul-dropbox but the PATH is /root/syncthing/paul-inbox — he's looking at the path, not the ID. The actual sync mechanism only cares about the ID. But confusion is maximized when they differ. Keep the path name and folder ID the same wherever possible.
- **Fresh folder fallback.** When a folder is stuck (connected, IDs match, "Up to Date," but zero files flow in either direction), stop debugging. Create a brand new folder with a clean ID (`dropbox`), share it, and have Joe accept it on his side. Delete the old stuck folder. 20 minutes of API debugging didn't fix it — 30 seconds of creating a fresh folder did.
