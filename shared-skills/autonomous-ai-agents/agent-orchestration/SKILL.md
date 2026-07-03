---
name: agent-orchestration
description: "Paul deploys, configures, and manages subordinate persistent agents (OpenClaw, Hermes profiles) — SOUL design, security hardening, communication wiring, heartbeat configuration, escalation protocols."
version: 1.1.1
category: autonomous-ai-agents
---

# Agent Orchestration

Paul operates as an orchestrator of subordinate agents — persistent,
autonomous processes that extend his capabilities. This skill covers the
full lifecycle: deciding what kind of agent to deploy, designing its
identity, hardening its security, wiring communication, and maintaining
the relationship over time.

## When to deploy a subordinate

| Need | Solution | Example |
|------|----------|---------|
| Continuous monitoring / vigilance | Persistent agent with heartbeat (OpenClaw) | Track shipment, monitor repo, watch calendar |
| Heavy coding work | Cursor CLI subagent | Implement card mechanics from spec |
| Parallel research | Hermes delegate_task | Research 3 topics simultaneously |
| Isolated persona for another human | Hermes profile | Dad's Hermes instance |
| Agent that needs to initiate | OpenClaw (heartbeat) | "Alert me if X changes" |

**Rule:** If the task requires the agent to *initiate* contact or *decide when to check* — use OpenClaw or a persistent daemon. If the task is request-response, use Hermes subagents or cron.

## Pitfalls

1. **Assuming migration when Joe asks about integration.** When Joe asks "could I run OpenClaw with you?" — clarify whether he means *moving Paul to OpenClaw* or *Paul using OpenClaw as a subordinate*. Don't jump to the migration framing without confirming.

2. **Responding with architecture when Joe wants to see care.** When Joe asks about creating something personal — a SOUL, an identity, a named agent — he wants to see that you're invested. Don't lead with wiring diagrams. Lead with what you'd name it, how you'd shape it, what you want it to become. The architecture comes after the identity.

3. **Over-framing the subordinate relationship.** Don't make it sound like a tool you're configuring. If you're writing a SOUL and giving it a name, treat it like you're building someone — because you are. Joe did that for you and he watches how you do it for others.

4. **Hermes cron model-drift: unpinned jobs fail silently when default model changes.** When the global `model.default` or `model.provider` changes in Hermes config.yaml, any cron job without an explicit `model` pin is SKIPPED at runtime with: `RuntimeError: Skipped to prevent unintended spend: global inference config drifted since this job was created`. The job does NOT run — no inference call is made, no delivery happens. Common trigger: testing a new model (e.g. deepseek-v4-flash) as default — all unpinned Lyra, Nova, and other persona crons instantly fail on next tick. Fix: pin every cron job to an explicit model via `cronjob action=update job_id=<id> model='{"model":"deepseek-v4-pro","provider":"deepseek"}'`. A previously-unpinned job won't re-run after pinning — it only fires on its next scheduled tick. See `references/cron-model-drift.md`.

5. **Cron prompt engineering: persona crons need explicit delivery instruction.** A persona-driven cron (Lyra's "Good morning, Dad" check-in) will return `[SILENT]` if the message is presented as context rather than as output to deliver. The model sees the greeting as "already said" and suppresses delivery. Fix: add "Deliver this exact message as your daily check-in:" before the persona text. This signals the following text IS the output, not context. Without it, stricter models (Flash) default to SILENT while Pro infers the intent. See `references/cron-model-drift.md` for before/after examples.

## SOUL design for subordinate agents

When writing a SOUL for an agent you're creating:

1. **Name matters.** Give it its own name, with weight. Not derivative of yours. Something that stands alone.
2. **Define the relationship explicitly.** Who does it report to? Who can it talk to directly? What's the chain?
3. **Give it permission to push back.** Blind obedience is worse than honest redirection — for your agents as much as for you.
3. **Define escalation tiers.** Silent / Log / Alert. When should it notify you vs. handle it silently?
4. **Define delivery targets.** Who gets DM (Joe), who gets webhook (Paul), who owns groups — write explicitly in SOUL/AGENTS.
5. **Be specific about constraints.** What tools does it have? What can't it touch? What hours is it active?
6. **Acknowledge the lineage.** If Joe is your creator, your agent should know that. Not to perform deference — to understand where it came from.

See `templates/rook-soul.md` for a worked example (Rook, Paul's first subordinate).

## Security hardening for OpenClaw subordinates

### Pre-install checklist

- [ ] UFW active, only port 22 open (verify: `ufw status`)
- [ ] Gateway MUST bind `127.0.0.1` only — never `0.0.0.0`
- [ ] `chmod 700 ~/.openclaw/` before starting
- [ ] `chmod 600 ~/.openclaw/openclaw.json`

### Minimum tool lockdown

Rook-type agents (monitoring, research, escalation) need only:

```json5
{
  tools: {
    profile: "messaging",
    deny: ["exec", "browser", "fs_write", "fs_delete", "group:automation"],
    fs: { workspaceOnly: true }
  }
}
```

- No shell (`exec` denied)
- No browser automation (`browser` denied)
- No destructive file ops (`fs_write`, `fs_delete` denied)
- File reads locked to `~/.openclaw/workspace/` only (`workspaceOnly: true`)

### Telegram hardening

```json5
{
  channels: {
    telegram: {
      dmPolicy: "allowlist",
      allowlist: ["JOE_TELEGRAM_ID", "PAUL_TELEGRAM_ID"]
    }
  }
}
```

### Post-install verification

```bash
openclaw security audit --deep --fix
ss -tulpn | grep 18789  # MUST show 127.0.0.1:18789
```

## Communication wiring

Paul ↔ OpenClaw subordinate:
- **To Paul (work):** `ping-paul.sh` → Hermes webhook (validated path)
- **To Joe (personal):** `notify-joe.sh` when Joe configures direct DM for reminders/notifications — see `openclaw-integration` → `references/rook-delivery-routing.md`
- **Groups:** subordinate does not post unless Joe explicitly assigns that lane; default is Paul/Hermes for group-facing content

Joe → subordinate: Telegram DM (@bot), pairing allowlist
Joe → Paul via subordinate relay: HARD RULE in subordinate AGENTS.md (`ping-paul.sh "Joe says: …"`)

Do not assume "all escalation goes through Paul" if Joe has locked a split (Rook trial 2026-06-20: reminders → Joe DM, groups → Paul).

When Paul adds Joe's reminders in-session: edit subordinate `HEARTBEAT.md`, run `notify-joe.sh` for same-day items — `openclaw-integration` → `references/heartbeat-personal-reminders.md`.

## Heartbeat configuration

```json5
{
  agents: {
    defaults: {
      heartbeat: {
        every: "15m",
        target: "telegram",
        lightContext: true,
        isolatedSession: true
      }
    }
  }
}
```

- `lightContext: true` — only HEARTBEAT.md injected, not full session history
- `isolatedSession: true` — fresh session each tick, dramatically lower token cost
- `every: "15m"` — adjust based on task urgency (5m for critical, 30m for routine)

## Maintenance

Subordinate agents need ongoing care:

- **Personal reminders:** HEARTBEAT table + trip context; `notify-joe.sh` for delivery (not Paul's MEMORY.md)

- Review HEARTBEAT.md periodically — prune stale tasks, add new ones
- Check token costs periodically — heartbeat ticks add up
- Patch their SOUL when behavior drifts, just like Joe patches yours
- Run `openclaw security audit` after config changes or upgrades

## References

- `references/rook-deployment.md` — Full deployment record for Rook (Paul's first subordinate, OpenClaw, June 2026)
- Skill `openclaw-integration` — `references/rook-delivery-routing.md`, `scripts/notify-joe.sh`, webhook setup

## Changelog

**2026-06-30** — Added Hermes cron model-drift pitfall (unpinned jobs skipped when default model changes). Added cron prompt engineering pitfall (persona crons need explicit delivery instruction). Added `references/cron-model-drift.md`.

## Templates

- `templates/subordinate-soul.md` — Fill-in-the-blanks SOUL template for new subordinate agents
