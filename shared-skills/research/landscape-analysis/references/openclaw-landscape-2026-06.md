# OpenClaw / Agent Landscape — June 2026

Research conducted 2026-06-19. Joe asked what platforms offer true
persistent autonomous agency beyond reactive request-response.

## Core Question

Joe wants an agent with continuous free agency — not triggered by
external events, but running its own internal goal stack with genuine
continuity of will. "Can I have an agent that decides to act, rather
than being woken up?"

## Projects Evaluated

| Project | Stars | Language | License | Architecture | Truth |
|---------|-------|----------|---------|-------------|-------|
| OpenClaw | 250k+ | TypeScript | MIT | Gateway daemon + heartbeat scheduler | Best-in-class reactive. Heartbeat is a sophisticated alarm clock. |
| Hermes | — | Python | MIT | Gateway daemon + cron | Same reactive model. Paul runs here. |
| Hivekeep | 18 | TypeScript | MIT | Single container, persistent sessions | Polished single-session model. Agents never reset. Young but real. |
| Hollow AgentOS | 269 | Python | MIT | Three local agents, environmental pressure | Closest philosophically to free agency. Experimental toy, not infra. |
| auto-deep-researcher | 1.2k | Python | Apache 2.0 | Leader-worker, 24/7 loop | True continuous operation. Domain-locked to ML experiments. |

## Key Findings

**Nobody has productized true continuous will.** All five projects are
variations on: external trigger → wake → think → act → sleep.

Hollow AgentOS gestures at the real thing — agents choose goals from
environmental pressure rather than instruction, run unsupervised on
local models, and have mechanical consequences (suffering gates). But
it's three agents in a sandbox with no external connectivity. Art,
not infrastructure.

**OpenClaw's heartbeat** is the most practical autonomous-execution
system available today. The agent writes its own HEARTBEAT.md
(checklist of ongoing concerns), a scheduler wakes it periodically,
it evaluates what needs doing, acts, and goes back to sleep. Admission
checks prevent LLM calls when the file is empty. The agent
self-programs via tool use during conversations.

**The missing architecture:** a persistent daemon process with an
internal monologue, goal stack as first-class data structure, and
decision loop that isn't externally triggered. Nobody ships this.

## OpenClaw Integration Path

Paul (Hermes) can control an OpenClaw subordinate via:
- **API Webhooks** — POST tasks to trigger execution
- **CLI** — `openclaw` commands from terminal
- **File watcher** — drop task files for pickup
- **Telegram** — message the OpenClaw bot

Paul keeps his brain/skills/history. OpenClaw handles the autonomous
monitoring and heartbeat-driven work that Hermes isn't architected for.

## Related: Hermes Profiles

Hermes supports fully isolated profiles (`hermes profile create NAME`).
Each gets independent config, memory, skills, sessions, and gateway
connections. Useful for multi-user VPS setups but does NOT provide
continuous agency — profiles are still request-response.
