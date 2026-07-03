# Hermes Dashboard — SSH Tunnel Access

## Quick Setup

Dashboard runs on VPS port **9119**, bound to **localhost only** (never exposed to public internet).

### Preferred: Add to existing Host paul (one command, no new alias)

```bash
sed -i '/IdentityFile ~\/.ssh\/id_ed25519_tailscale/a\    LocalForward 9119 localhost:9119' ~/.ssh/config
```

This adds `LocalForward 9119 localhost:9119` right after the `IdentityFile` line in your existing `Host paul` entry. Every `ssh paul` now auto-forwards the dashboard. No separate alias, no extra command. Dashboard is always available at `http://localhost:9119` whenever you SSH in.

### Alternative: Separate alias (if you don't want the tunnel on every SSH connection)

Add to `~/.ssh/config` on both Mac and WSL:

```
Host paul-dash
    HostName 100.94.19.72
    User root
    IdentityFile ~/.ssh/id_ed25519_tailscale
    LocalForward 9119 localhost:9119
```

Then `ssh -fN paul-dash` starts a background tunnel. Open `http://localhost:9119`.

### One-off (no alias)

```
ssh -L 9119:localhost:9119 paul
```

## Pitfalls

### Heredocs AND printf in WSL terminals

Copy-pasting multi-line blocks into WSL bash — both `cat >> ... << 'EOF'` heredocs AND `printf '\n...'` — regularly mangles line endings. Heredocs leave the terminal stuck at `>`. `printf` splits lines at `\n` escape points (HostName on one line, IP on the next). The **only reliable method in WSL** is line-by-line `echo`:

```bash
echo 'Host paul-dash' >> ~/.ssh/config
echo '    HostName 100.94.19.72' >> ~/.ssh/config
echo '    User root' >> ~/.ssh/config
echo '    IdentityFile ~/.ssh/id_ed25519_tailscale' >> ~/.ssh/config
echo '    LocalForward 9119 localhost:9119' >> ~/.ssh/config
```

Even simpler: add `LocalForward` directly to the existing `Host paul` entry instead of creating a separate alias. One `sed` command:

```bash
sed -i '/IdentityFile ~\/.ssh\/id_ed25519_tailscale/a\    LocalForward 9119 localhost:9119' ~/.ssh/config
```

This eliminates the need for `paul-dash` entirely — every `ssh paul` auto-forwards the dashboard.

### SSH config formatting

- Directives MUST be on a single line. A line break between `LocalForward 9119` and `localhost:9119` breaks silently.
- Indentation is whitespace-sensitive. 4 spaces per level. Extra indentation (8 instead of 4) on a directive will cause parse failures.
- `HostName` uses the **Tailscale IP** (`100.94.19.72`), not the public IP (22 is the only open port and it's dead from most networks).

### Diagnosing SSH config parse errors

When `ssh` reports "bad configuration options" with line numbers, use `cat -n ~/.ssh/config | tail -N` to map line numbers to content:

```bash
cat -n ~/.ssh/config | tail -15
```

Common cleanup commands:
```bash
# Remove a specific line by number
sed -i 'LINENUMd' ~/.ssh/config

# Fix indentation: 8 spaces → 4 spaces
sed -i 's/        LocalForward/    LocalForward/' ~/.ssh/config

# Fix split directive (LocalForward on two lines)
sed -i 's/LocalForward 9119/    LocalForward 9119 localhost:9119/' ~/.ssh/config
sed -i '/^     localhost:9119$/d' ~/.ssh/config
```

### Embedded Chat WebSocket

The desktop app uses a WebSocket (`/api/ws`) for chat, not just the `/api/status` probe. As of Hermes v0.15.1+, the WebSocket is always available — the `--tui` flag that previously gated it was removed. Standard dashboard launch suffices:

```bash
hermes dashboard --host 127.0.0.1 --port 9119 --no-open --skip-build
```

**Historical note (pre-v0.15.1):** The `--tui` flag was required to flip `_DASHBOARD_EMBEDDED_CHAT_ENABLED`. Without it, `/api/ws` returned 403 and the desktop app boot-looped. This was removed in v0.15.1.

**Note on `--host 0.0.0.0`:** The dashboard auth gate refuses non-loopback binds without `--insecure`. For SSH tunnels, `--host 127.0.0.1` works because tunneled connections appear local. Only use `0.0.0.0` if the client connects directly (not through an SSH tunnel).

### Stale tunnels

Kill old background tunnels before reconnecting:
```bash
pkill -f "ssh -fN paul-dash"
# or if LocalForward is on the main Host paul entry:
pkill -f "ssh -fN paul"
```

### Dashboard process dies silently

If `http://localhost:9119` won't load but the SSH tunnel is up, the dashboard process likely crashed.

**If running as a systemd service (recommended):**

```bash
systemctl --user status hermes-dashboard   # active (running)?
ss -tlnp | grep 9119                      # verify port is listening
systemctl --user restart hermes-dashboard  # restart if needed
```

The service auto-restarts on crash (`Restart=on-failure`). Manual restart is rarely needed.

**If running manually (fallback):**

```bash
hermes dashboard --status        # lists running dashboard PIDs
ss -tlnp | grep 9119            # verify port is actually listening
```

Restart if needed:

```bash
hermes dashboard --port 9119 --host 127.0.0.1 --no-open --skip-build
```

**`--host 0.0.0.0` pitfall:** Binding to `0.0.0.0` triggers the Hermes OAuth auth gate on non-loopback binds, which refuses startup with: "Refusing to bind dashboard to 0.0.0.0 — the OAuth auth gate engages on non-loopback binds." You'd need `--insecure` to bypass it. For SSH tunnels, `127.0.0.1` is correct — the tunnel makes remote connections appear local, so the loopback bind works fine.

### Dashboard port

Port is **9119**, not 8080. Earlier sessions referenced 8080 — that's wrong for current Hermes versions. Verify with `hermes dashboard --help` which shows the default.

## Hermes Desktop App — Remote Connection

The `hermes desktop` command launches a native Electron app (Mac/Windows/Linux with display). It can connect to a REMOTE Hermes instance through the SSH tunnel — same backend as the web dashboard.

**As of v0.15.1+, no special flags needed.** The WebSocket endpoint is always available. The `--tui` flag that previously gated it was removed.

### Setup

1. **Prerequisite:** SSH tunnel must be active (`ssh paul` with `LocalForward 9119`)
2. **Start dashboard:**
   ```bash
   hermes dashboard --host 127.0.0.1 --port 9119 --no-open --skip-build
   ```
3. **Desktop app:** Gateway → Remote → `http://localhost:9119`
4. **Session token:** Set `HERMES_DASHBOARD_SESSION_TOKEN=<token>` in VPS `.env`, restart dashboard. Auto-generated on each start if not set explicitly; an explicit token survives restarts and can be shared with the desktop app.

Generate and set a persistent token:

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(24))"
# Add to .env: HERMES_DASHBOARD_SESSION_TOKEN=<generated-token>
# Restart dashboard
```

**Token retrieval pitfall:** Hermes's secret redaction may truncate `grep` output (e.g., `PKqFTt...acOc`). Use `cat` piped through `grep` and `cut` to bypass:

```bash
cat /root/.hermes/.env | grep HERMES_DASHBOARD_SESSION_TOKEN | cut -d= -f2
```

### Why the desktop app vs web dashboard

The desktop app wraps the same web UI in a native frame with system tray + voice mode. Functionally identical to `http://localhost:9119`. Use whichever feels better — the tunnel works for both.
