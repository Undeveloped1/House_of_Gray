# Syncthing File Sync Setup (Paul VPS ↔ Joe Local)

Set up Syncthing for bidirectional file transfer between Paul's VPS and Joe's local machine. No cloud, no credentials — peer-to-peer over the existing network connection.

## Trigger

Use this when:
- Setting up file sync for the first time on a VPS
- Joe says "how do I get files to you" or similar
- Debugging a Syncthing sync failure between VPS and local machine

## Install (VPS side)

```bash
apt-get install -y syncthing
```

## Systemd User Service

Syncthing must survive reboots. Create the service file:

```bash
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
```

Enable and start:
```bash
loginctl enable-linger root
systemctl --user daemon-reload
systemctl --user enable syncthing.service
systemctl --user start syncthing.service
```

## Get Device ID

```bash
grep -oP '<device id="\K[^"]+' /root/.local/state/syncthing/config.xml | head -1
```

## Headless API Configuration

Syncthing on VPS has no GUI. All folder and device management goes through the REST API on `localhost:8384`.

Get the API key:
```bash
APIKEY=$(grep -oP '<apikey>\K[^<]+' /root/.local/state/syncthing/config.xml)
```

### Add a remote device
```bash
curl -s -X POST http://localhost:8384/rest/config/devices \
  -H "X-API-Key: $APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"deviceID": "DEVICE-ID-HERE", "name": "joe"}'
```

### Create a shared folder
```bash
mkdir -p /root/syncthing/<folder-id>
curl -s -X POST http://localhost:8384/rest/config/folders \
  -H "X-API-Key: $APIKEY" \
  -H "Content-Type: application/json" \
  -d '{
    "id": "<folder-id>",
    "label": "Human-Readable Label",
    "path": "/root/syncthing/<folder-id>",
    "type": "sendreceive",
    "rescanIntervalS": 10,
    "fsWatcherEnabled": true,
    "devices": [
      {"deviceID": "VPS-DEVICE-ID"},
      {"deviceID": "JOE-DEVICE-ID"}
    ]
  }'
```

### Remove a folder
```bash
curl -s -X DELETE http://localhost:8384/rest/config/folders/<folder-id> \
  -H "X-API-Key: $APIKEY"
```

### Check folder status
```bash
curl -s "http://localhost:8384/rest/db/status?folder=<folder-id>" \
  -H "X-API-Key: $APIKEY"
```
Key fields: `globalFiles`, `localFiles`, `needFiles`. If `needFiles > 0`, sync is in progress.

### Check device completion
```bash
curl -s "http://localhost:8384/rest/db/completion?folder=<folder-id>&device=<device-id>" \
  -H "X-API-Key: $APIKEY"
```
`completion: 100` means Syncthing believes the remote device has all files.

### Force rescan
```bash
curl -s -X POST "http://localhost:8384/rest/db/scan?folder=<folder-id>" \
  -H "X-API-Key: $APIKEY"
```

### Restart service
```bash
systemctl --user restart syncthing
```

## Pairing Flow (two devices)

1. **Both install Syncthing.** Joe installs locally (Windows: `winget install syncthing` or download from syncthing.net; WSL: `apt install syncthing`; Mac: `brew install syncthing`).
2. **Exchange device IDs.** VPS ID from `grep` above. Joe gets his from his local Syncthing GUI (top-left of web UI at `http://localhost:8384`).
3. **Add devices on both sides.** VPS via API. Joe via GUI (Add Remote Device → paste VPS device ID).
4. **Create folder on VPS** via API (see above). Include both device IDs.
5. **Joe accepts the share.** Appears in his GUI. He picks a local folder path.
6. **Verify.** Drop a test file on one side, check the other.

## Accepting Pending Device Requests

When another machine adds the VPS's device ID, it shows up as a pending request. The correct endpoint to check is:

```bash
curl -s -H "X-API-Key: $APIKEY" http://localhost:8384/rest/cluster/pending/devices
```

Output shows device ID, human-readable name (e.g., `Joss-MacBook-Air.local`), timestamp, and address. If empty `{}`, no pending requests.

**Do NOT use** `/rest/system/pending` — it returns 404. The working endpoint is `/rest/cluster/pending/devices`.

### Accept the pending device

Once identified, POST the device to the config:

```bash
curl -s -X POST http://localhost:8384/rest/config/devices \
  -H "X-API-Key: $APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"deviceID":"<PENDING-DEVICE-ID>","name":"<human-name>","addresses":["dynamic"],"compression":"metadata","introducer":false,"paused":false}'
```

The device is now trusted but won't sync anything until a folder is shared with it.

### List configured devices

```bash
curl -s -H "X-API-Key: $APIKEY" http://localhost:8384/rest/config/devices | python3 -m json.tool
```

## Adding a Device to an Existing Folder

When a device is already trusted but not yet receiving any folder, PATCH the folder's device list:

```bash
curl -s -X PATCH "http://localhost:8384/rest/config/folders/<folder-id>" \
  -H "X-API-Key: $APIKEY" \
  -H "Content-Type: application/json" \
  -d '{"devices":[
    {"deviceID":"<EXISTING-DEVICE-1>"},
    {"deviceID":"<EXISTING-DEVICE-2>"},
    {"deviceID":"<NEW-DEVICE-ID>"}
  ]}'
```

**Important:** The PATCH replaces the entire devices array. Include ALL existing device IDs, not just the new one — otherwise you'll silently drop existing shares.

## CRITICAL: Folder ID Matching

**Syncthing matches folders by ID, not by label or path.** The folder `id` field in the config MUST be identical on both devices. Labels are cosmetic only.

If Joe creates a folder with ID `paul-dropbox` and the VPS has `paul-inbox`, they will NOT sync — even if labels match. This is the #1 failure mode.

**Fix:** Either change the VPS folder ID to match Joe's (delete old folder config, create new one), or Joe changes his folder ID to match the VPS. Prefer matching Joe's naming since he's the one with the GUI and can see what he named things.

## Pitfalls

- **Folder ID mismatch** — The #1 cause of "connected but no files sync." Both sides show "Up to Date" but zero files flow. Verify folder IDs match exactly (case-sensitive).
- **Path confusion** — The folder `label` and `path` are not the `id`. Joe sees the label in his GUI. The `id` is the technical match key. When debugging, always ask "what's the folder ID, not the label?"
- **Windows path corruption** — On Windows, Syncthing can mangle folder paths if quotes or special characters are involved. The path should be clean: `C:\Users\...\FolderName` with no extra quotes or program paths.
- **Desktop spillover** — If Joe points his Syncthing folder at Desktop or a parent directory, all Desktop contents sync to VPS. Use a dedicated folder like `C:\Users\<user>\PaulSync\`.
- **Never delete the VPS data directory.** The Syncthing index database is in `/root/.local/state/syncthing/`. Wiping it forces a full rescan but loses sync state. Only do this if sync is completely broken — and restart the service afterward.
- **Corrupted config entries** — If you see empty folder IDs (`id=""`) in the config, remove them via API DELETE. They can block new folder creation.
- **Connection resets are normal.** Syncthing reconnects automatically. Don't chase "connection reset by peer" in the logs unless sync has stopped entirely.
- **Don't guess folder IDs.** Ask Joe. He can see them in his GUI. Guessing wastes 20 minutes.

## Logs

```bash
journalctl --user -u syncthing --no-pager --since "5 min ago" | grep -i -E "folder-id|YC32|error|warn|index"
```

## Verification

After setup:
1. `ls -la /root/syncthing/<folder-id>/` — files should appear
2. API status check shows `globalFiles > 0` and `needFiles == 0` when synced
3. Joe sees the test file in his local folder
