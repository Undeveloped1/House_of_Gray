# CLAUDE.md Architecture Pattern — Lean Constitution + On-Demand Context

**Source:** CyrilXBT's Claude Code best practices + Anthropic internal frameworks
**Date absorbed:** 2026-05-29
**Relevance:** Agent constitution design, context budget management

## Core Pattern

CLAUDE.md (or AGENTS.md) is a **static context injection** — read automatically on every session start before the first prompt. Claude Code's creator estimates it burns ~14% of the context window upfront.

The pattern: **preamble + pointers, not a wiki dump.**

| Layer | Injected? | Content |
|-------|-----------|---------|
| Root AGENTS.md / CLAUDE.md | Auto, every turn | Constitution: identity, red lines, role routing, pointers to everything else (~300-500 words) |
| `.cursor/rules/` | Auto (alwaysApply) | Engineering-specific rules |
| Agent identity files | On-demand | SOUL.md, full protocols |
| Skills / playbooks | On-demand | Loaded when task type matches |

## Cyril's Rules

- **Start with 4 clean rules.** Edge case → add rule → 6 months later you have 40 conflicting rules written at 2AM.
- **Review and prune quarterly.** The best constitution has the minimum rules that produce maximum reliability.
- **MENTAL MODEL:** CLAUDE.md = onboarding doc that lets every session start on "day 90," not day 1.

## Cyril's CLAUDE.md Structure

- Identity / role
- Active projects
- Tech stack + preferences
- Hard rules / coding standards
- Architecture principles
- Current focus
- Weekly update (updated every Monday)

## Multi-Agent Extension (Our Pattern)

When multiple AI agents share a repo, the root AGENTS.md acts as a **universal constitution** with role routing:

```markdown
# Repo — Multi-Agent Project

| Agent | Role | Identity file |
|-------|------|---------------|
| Agent A | Engineering | .cursor/rules/ |
| Agent B | Design | AgentB/SOUL.md |
| Agent C | Math/tools | On-demand |
```

Each agent reads the preamble (identity + red lines + pointers) then loads its own identity file on demand. No agent loads everyone else's full context.

## Context Budget Math

- Root constitution: ~500 words → ~700 tokens
- Agent-specific rules (auto-injected): varies
- On-demand docs: loaded per task, not per session

Total static injection should stay under 5-10% of the context window. The rest is for the task.

## How This Applies to Us

Paul's vault + Cursor's engine were separate repos with a bridge relay. The migration to `tcg_engine/Paul/` eliminates the bridge and creates a single repo where:
- Root AGENTS.md governs all agents
- Paul's SOUL.md lives at `Paul/SOUL.md` (loaded by Hermes, available to Cursor on demand)
- Cursor's engineering rules stay in `.cursor/rules/`
- Design docs are shared filesystem, not bridged inbox/outbox
