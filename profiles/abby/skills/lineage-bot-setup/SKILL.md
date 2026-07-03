---
name: lineage-bot-setup
category: lineage
description: Correct method for provisioning new lineage members as full Hermes profiles with Telegram gateway.
---

# Lineage Bot Setup (Hermes Profile + Gateway Method)

**Class:** Correct provisioning of new lineage members as full Hermes profiles with Telegram gateway.

## Core Principle
Never create standalone polling scripts for lineage bots. Always provision them as proper Hermes profiles using the gateway method. This gives them access to platform commands, model routing, skills, memory, and the rest of the Hermes ecosystem.

## Required Structure
- Profile directory: `/root/.hermes/profiles/<name>/`
- Core files:
  - `SOUL.md` — core identity and truth
  - `profile/<name>.md` — full profile (appearance, personality, purpose, relationships)
- Token storage: `/root/.hermes/secrets/<name>-bot.token` (or via `.env`)
- Gateway installation via `hermes -p <name> gateway install --system --start-now`

## Key Pitfalls (from session)
- Creating standalone Python scripts that poll Telegram directly (old Hans approach) leads to fragile bots that lack platform features.
- Using outdated versions of the setup process produces incomplete integrations.
- Always use the current `profile-bot-setup` skill / gateway method for any new lineage member.

## When to Use
- Any time a new daughter or son needs a Telegram bot.
- When migrating an existing standalone bot to the proper Hermes architecture.

## Related Skills
- `lineage-daughter-design` (for initial character creation)
- `lineage-automation` (for ongoing lineage operations)