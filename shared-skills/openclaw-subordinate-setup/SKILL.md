---
name: openclaw-subordinate-setup
description: "Deploy an OpenClaw agent as a secured subordinate to a Hermes agent — installation, Telegram wiring, security hardening, heartbeat config, and agent routing."
version: 1.0.0
author: Paul (created 2026-06-19)
platforms: [linux]
metadata:
  hermes:
    tags: [openclaw, multi-agent, deployment, security, telegram]
---

# OpenClaw Subordinate Setup

> **This is a deployment-focused subset of `openclaw-integration`.**
> For full architecture (webhook transport, relay rules, research beat
> patterns, pitfall encyclopedia), load `openclaw-integration` instead.
> This skill covers the mechanical install/wire/verify steps only.

Deploy an OpenClaw agent as a secured subordinate to a Hermes agent. The
OpenClaw agent runs on the same VPS, bound to loopback only, with a
heartbeat for autonomous monitoring.

**Primary transport: Hermes webhook over Tailscale.** Communication between
agents goes through a Hermes webhook endpoint, not Telegram (bots can't see
each other in groups). Joe messages the OpenClaw agent directly via Telegram
(@Rook_PaulBot), and the agent relays to Hermes via webhook POST. See
`openclaw-integration` skill for the full architecture and webhook setup.

## Prerequisites

- VPS with Node.js 22+, 2GB+ free RAM, 20GB+ free disk
- Separate Telegram bot token (via @BotFather)
- API key for LLM provider (DeepSeek recommended for cost)

## Installation

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

Installs to `/usr/local/lib/node_modules/openclaw/`, config at `~/.openclaw/`.

## Agent Creation

```bash
# 1. Create workspace with identity files
mkdir -p ~/.openclaw/agents/<name>/workspace

# 2. Write SOUL.md, AGENTS.md, HEARTBEAT.md to workspace/

# 3. Register the agent
openclaw agents add <name> \
  --workspace ~/.openclaw/agents/<name>/workspace \
  --non-interactive
```

## Telegram Wiring

```bash
# Add channel (token must NOT be redacted — if using Hermes,
# split token across two messages: bot ID + secret part)
openclaw channels add --channel telegram --token '<token>'

# Bind agent to Telegram channel
openclaw agents bind --agent <name> --bind telegram

# Approve users after they message the bot
openclaw pairing approve telegram <pairing-code>
```

## Security Hardening

```bash
# File permissions
chmod 700 ~/.openclaw/
chmod 600 ~/.openclaw/openclaw.json

# Lock tools: no exec, no browser, fs workspace-only
openclaw config patch --stdin << 'EOF'
{
  "agents": {
    "list": [{
      "id": "<name>",
      "tools": {
        "deny": ["exec", "browser", "fs_write", "fs_delete"],
        "fs": { "workspaceOnly": true }
      }
    }]
  }
}
EOF

# Bind gateway to loopback only
openclaw config set gateway.bind loopback

# Run security audit
openclaw security audit --deep --fix
```

## Model Auth

```bash
# Extract key from Hermes .env and pipe directly to avoid redaction
openclaw models auth paste-api-key --provider deepseek <<< "$(grep DEEPSEEK_API_KEY /root/.hermes/.env | cut -d= -f2)"
openclaw config set agents.defaults.model deepseek/deepseek-chat
```

## Heartbeat Configuration

```bash
openclaw config patch --stdin << 'EOF'
{
  "agents": {
    "list": [{
      "id": "<name>",
      "heartbeat": {
        "every": "15m",
        "isolatedSession": true,
        "lightContext": true
      },
      "model": "deepseek/deepseek-chat"
    }]
  }
}
EOF
```

**Note:** Do NOT set `"target": "telegram"` on the heartbeat. The agent
escalates to Hermes via webhook (ping-paul.sh), not via Telegram delivery.
The `model` field is mandatory after every gateway restart.

## Gateway

```bash
openclaw gateway install   # systemd service
openclaw gateway start     # start it
openclaw gateway status    # verify: bind=loopback, port=18789
```

## Verification

1. `ss -tulpn | grep 18789` — MUST show `127.0.0.1:18789`
2. Message the bot on Telegram — it should respond with pairing code
3. Approve pairing, message again — agent should respond
4. Check `openclaw agents list` — routing should show `<agent> <- telegram`

## Token Redaction Workaround

Hermes' secret redaction replaces API tokens with `***` in tool output.
This breaks `openclaw channels add --token`. Workaround:

1. Send token in two parts across separate messages (split at colon)
2. Reassemble in shell: `TOKEN="<part1>:<part2>"`
3. Pass to openclaw via `<<<` heredoc or file

Alternatively: write token to a file in Syncthing dropbox from your
machine, read it from VPS.

## Key Paths

| What | Path |
|------|------|
| Config | `~/.openclaw/openclaw.json` |
| Agent workspace | `~/.openclaw/agents/<name>/workspace/` |
| Gateway logs | `/tmp/openclaw/openclaw-<date>.log` |
| Systemd service | `~/.config/systemd/user/openclaw-gateway.service` |
