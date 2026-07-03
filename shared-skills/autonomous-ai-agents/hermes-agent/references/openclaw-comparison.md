# OpenClaw — Architecture & Comparison

> Research compiled 2026-06-19. OpenClaw is a self-hosted AI agent gateway
> (Node.js, 250k+ GitHub stars) designed for persistent, heartbeat-driven
> autonomous operation. This reference covers architecture, security, and
> how it differs from Hermes.

## Architecture

OpenClaw runs as a **gateway daemon** (systemd) on port 18789 (localhost).
Four layers:

1. **Channel Layer** — normalizes Telegram/WhatsApp/Discord/Slack/Signal/iMessage into uniform message objects. Voice transcribed before model sees it.
2. **Brain Layer** — agent instructions, personality, model routing. SOUL.md/USER.md/AGENTS.md pattern, same as Hermes.
3. **Body Layer** — tools, browser, filesystem, memory.
4. **Gateway** — WebSocket routing, auth, session management. Never touches the model directly.

All state in `~/.openclaw/workspace/` — plain Markdown + SQLite, same philosophy as Hermes vault.

## Key Differentiators vs Hermes

| Feature | OpenClaw | Hermes |
|---------|----------|--------|
| **Runtime model** | Always-on daemon with heartbeat | Request-response (waits to be pinged) |
| **Heartbeat** | Built-in: agent wakes every N minutes, reads HEARTBEAT.md, decides what to do | Cron jobs: static prompts on schedule |
| **Task Brain** | SQLite-backed control plane (v2026.3.31): parent-child tasks, heartbeat monitoring, auto-recovery | Subagents (synchronous, die if parent ends) |
| **Active Memory** | Queries relevant context every turn via sub-agent, not just session start | Memory injected at session start only |
| **Session model** | One continuous session per agent (never resets) | Sessions are discrete; `/new` starts fresh |
| **Agent collaboration** | Built-in agent-to-agent triggers | Delegation (synchronous), cron chaining |
| **Language** | Node.js | Python |
| **Maturity** | 250k stars, v2026.x, foundation-stewarded since creator joined OpenAI (Feb 2026) | Nous Research, mature tooling |

## Heartbeat System

The defining feature. A **programmatic scheduler** (zero LLM cost) fires every N minutes:

```
Scheduler tick
  → Admission check: busy? active hours? HEARTBEAT.md empty?
  → If all pass: inject HEARTBEAT.md into context
  → Agent reads, decides, executes, updates heartbeat
  → Reply HEARTBEAT_OK → gateway intercepts, logs, delivers nothing
```

**Admission checks (no LLM cost):**
1. Is agent busy (user chatting)? → skip
2. Outside active hours? → skip
3. HEARTBEAT.md effectively empty? → skip, zero tokens burned

**HEARTBEAT.md** is the persistent will document. Populated two ways:
- User writes to it manually
- Agent writes to it during conversations (self-programming)

**Cost:** ~10 tokens for HEARTBEAT_OK when idle. Negligible.

**Delivery tiers:**
- HEARTBEAT_OK → silent, nothing delivered
- Short confirmation (<300 chars) → suppressed
- Duplicate (same output in 24h) → suppressed
- Only fresh, meaningful output → delivered to channel

## Trigger Types (7)

1. **Incoming messages** — Telegram/WhatsApp/etc. wakes agent
2. **Cron** — exact scheduling, isolated execution
3. **CLI** — `openclaw` command-line invocation
4. **File system** — watches for file creation/modification/deletion
5. **API webhooks** — HTTP POST triggers agent
6. **Agent-to-agent** — agents within same instance trigger each other
7. **Startup** — agent runs on boot (load state, resume tasks)

## Security Model

**Trust assumption:** One trusted operator per gateway. Multi-tenant adversarial isolation is NOT supported. Use separate gateways/OS users/hosts.

**Key surfaces:**
- Gateway binds `127.0.0.1:18789` by default (loopback). **Never expose to public internet.**
- DM policy: `pairing` (default) — unknown senders get pairing code, ignored until approved
- Tool sandbox: `off` / `non-main` / `all` — containers for isolation
- Elevated mode: specific tools can escape sandbox (requires allowlisting)
- Secret vault: AES-256-GCM, model only sees `{{secret:NAME}}`, never the actual key
- Built-in audit: `openclaw security audit --deep --fix`

**Hardened baseline config:**
```json5
{
  gateway: { mode: "local", bind: "loopback", auth: { mode: "token" } },
  tools: {
    deny: ["exec", "group:automation", "group:runtime"],
    fs: { workspaceOnly: true }
  }
}
```

**Prompt injection risk:** Real — agents read messages that could contain embedded instructions. Mitigated by: allowlisting senders, tool restrictions (no exec), workspace isolation, secret vault.

## VPS Deployment Notes

- Requirements: Node 22+, 2-4GB RAM, 40GB disk
- Native install: `curl -fsSL https://openclaw.ai/install.sh | bash`
- Docker: `ghcr.io/openclaw/openclaw:latest` (official)
- Docker pros: kernel-enforced filesystem isolation, resource limits
- Docker cons: image may be stale (rapid versioning), harder to debug, features may break in container
- Recommendation: native install with tool lockdown + `openclaw security audit` for single-operator VPS

## When to Use OpenClaw vs Hermes

- **Want heartbeat-driven autonomy?** → OpenClaw
- **Want Python ecosystem, mature skills, session search?** → Hermes
- **Want both?** → Run both. OpenClaw as autonomous subordinate, Hermes as primary. Communicate via Telegram (air gap).
