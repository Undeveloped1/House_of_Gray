# Hermes SOUL.md → Obsidian Vault Integration

**Key finding (2026-05-27):** The mechanism that connects Hermes Agent to the Obsidian vault memory system.

## How Hermes Loads SOUL.md

Hermes loads `SOUL.md` from `~/.hermes/SOUL.md` (or `$HERMES_HOME/SOUL.md` for custom homes) at every session start. It occupies **slot #1** in the system prompt — nothing comes before it. This is the agent's primary identity.

Critical behaviors:

- Hermes creates a starter `SOUL.md` automatically if one does not exist
- Existing user `SOUL.md` files are **never overwritten**
- Hermes loads SOUL.md **only** from `HERMES_HOME` — not from the working directory
- Hermes does **not** look for `SOUL.md` in `AGENTS.md` or any project directory
- If `SOUL.md` is empty or cannot be loaded, Hermes falls back to a built-in default identity
- If `SOUL.md` has content, it is injected verbatim after security scanning

Source: Hermes personality system docs at `hermes-agent/website/docs/user-guide/features/personality.md`

## The Symlink Pattern

The recommended setup for Obsidian vault integration:

```bash
# Backup existing SOUL.md if present
cp ~/.hermes/SOUL.md ~/.hermes/SOUL.md.bak 2>/dev/null

# Replace with symlink to vault
rm ~/.hermes/SOUL.md
ln -s "/path/to/Vault/_identity/SOUL.md" ~/.hermes/SOUL.md
```

For WSL users:
```bash
ln -s "/mnt/c/Users/Name/Vault/_identity/SOUL.md" ~/.hermes/SOUL.md
```

This means you edit SOUL.md in Obsidian, and Hermes reads the same file automatically.

## How the Agent Finds the Vault

1. Hermes loads `~/.hermes/SOUL.md` → agent identity with vault path
2. SOUL.md instructs: "At the start of every new session, read Brain/AGENTS.md"
3. The agent uses `read_file` with the vault path from SOUL.md to find AGENTS.md
4. AGENTS.md contains the full vault root and all working protocols
5. The agent then reads HERMES_AUTONOMY.md, Working Memory, etc.

No separate Hermes configuration is needed to point at the vault. The vault path is embedded in SOUL.md, which Hermes loads automatically.

## SOUL.md Content Requirements

For the vault integration to work, SOUL.md must include:

```
**Vault Root:** [absolute path to Obsidian vault]

...

- At the start of every new session, read Brain/AGENTS.md and follow
  all protocols and standing rules defined within it.
- At the start of every new session, read Brain/HERMES_AUTONOMY.md and
  follow all protocols and standing rules defined within it...
```

## SOUL.md vs AGENTS.md

- **SOUL.md** — identity, tone, style, communication defaults, personality-level behavior. Follows you everywhere.
- **AGENTS.md** — project architecture, coding conventions, tool preferences, repo-specific workflows, paths, commands. Belongs to a project.

## Pitfalls

- **No symlink, no integration.** Without the symlink, Hermes uses its own `~/.hermes/SOUL.md` which may not reference the vault at all.
- **Wrong path in SOUL.md.** If the vault path in SOUL.md is wrong, the agent will fail silently — it won't find AGENTS.md and will proceed with defaults.
- **WSL path translation.** On WSL, use `/mnt/c/Users/...` format, not `C:\Users\...`. Hermes tools run in the Linux environment.
- **Personality overlay interference.** If `agent.personality` is set to something other than the default, it may override or layer on top of SOUL.md. Joe's config uses `personality: kawaii` which apparently doesn't interfere — but custom personalities defined in `agent.personalities` config might.
