# Remote Computer-Use: CuaDriver Bridge Architecture

## Problem

Paul runs on a headless Linux VPS. The `computer_use` tool drives the user's desktop, but the VPS has no desktop, no screen, no accessibility framework. cua-driver must run on **Joe's PC** — the machine with the actual GUI.

Hermes on the VPS needs to connect to cua-driver running on Joe's PC.

## Transport Gap

cua-driver's MCP mode is **stdio only**:

```bash
cua-driver mcp-config --client hermes
# Output:
# mcp_servers:
#   cua-driver:
#     command: "/path/to/cua-driver"
#     args: ["mcp"]
```

Hermes supports both stdio and HTTP (StreamableHTTP) MCP transports. But cua-driver has no built-in HTTP mode — no `--host`, `--port`, or `--url` flags.

## Hermes HTTP MCP Config (target shape)

```yaml
# ~/.hermes/config.yaml on VPS
mcp_servers:
  joe-desktop:
    url: "https://<joe-pc-address>:<port>/mcp"
    headers:
      Authorization: "Bearer <shared-secret>"
    timeout: 120
    connect_timeout: 60
```

## Bridge Options

### Option A: SSH Tunnel + socat (simplest)

On Joe's PC:
```bash
# Start cua-driver MCP and expose via socat on localhost
socat TCP-LISTEN:9223,reuseaddr,fork EXEC:"cua-driver mcp"
```

On VPS, Hermes config:
```yaml
mcp_servers:
  joe-desktop:
    url: "http://localhost:9223/mcp"  # tunneled via SSH -L 9223:localhost:9223
```

Then `ssh -L 9223:localhost:9223 joe-pc` to tunnel the port.

### Option B: Python MCP HTTP Proxy

A lightweight Python script on Joe's PC that:
1. Spawns `cua-driver mcp` as a subprocess (stdio MCP)
2. Exposes a StreamableHTTP endpoint
3. Forwards messages between the HTTP client and the stdio process

### Option C: Tailscale + Proxy

If both VPS and Joe's PC are on Tailscale:
- Joe runs cua-driver + proxy bound to Tailscale IP
- Hermes config points at `http://100.x.y.z:9223/mcp`

## Installation on Joe's PC

Joe needs to install cua-driver and grant permissions:

**macOS:**
```bash
hermes computer-use install
cua-driver permissions status   # check Accessibility + Screen Recording
cua-driver permissions grant    # grant via system dialog
cua-driver doctor               # verify everything works
```

**Windows:**
```bash
hermes computer-use install
cua-driver autostart enable     # register logon scheduled task
cua-driver autostart kick       # start now without re-logging
cua-driver doctor
```

## What Hermes Gains

Once connected, Paul gets the `computer_use` tool and can:
- Capture screenshots (with SOM overlays — numbered clickable elements)
- Click, type, scroll, drag — all in background (doesn't steal Joe's cursor/focus)
- Drive any app: browser, editor, Finder, Figma, terminal, etc.
- Never type passwords, API keys, or secrets (hard rule)

## Session Flow

1. Joe starts cua-driver + bridge on his PC
2. Paul's Hermes session connects via HTTP MCP
3. Paul captures screen → sees what Joe sees → acts
4. Joe can keep working in other windows — cua-driver operates in background
