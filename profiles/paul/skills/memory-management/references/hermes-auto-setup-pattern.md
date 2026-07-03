# Hermes Auto-Setup Pattern — Self-Executing AGENTS.md

**Technique:** Writing an AGENTS.md file that another Hermes agent can read and execute as a fully autonomous system provisioning script. The setup agent reads the file, asks the human a few questions via `clarify()`, then creates all directories, files, symlinks, and configurations.

**Developed during:** Memory system auto-setup for Joe's friend (2026-05-27).

---

## Pattern Structure

A self-executing AGENTS.md has these phases:

### Phase 0: Architecture Detection
Determine the runtime environment before any file operations:
- Local (same machine) vs VPS (separate machine with Syncthing)
- WSL vs native Linux
- Path format requirements

### Phase 1: Information Gathering
Use `clarify()` ONE QUESTION AT A TIME:
- User name
- Agent name (or hardcode for personalized editions)
- Vault path (local path or VPS synced path)
- WSL status

### Phase 2: Directory Creation
Create the full directory tree with `mkdir -p`. One batch, no user input.

### Phase 3: File Creation
Write all files with `write_file`. Substitute `{USER_NAME}`, `{AGENT_NAME}`, `{VAULT_PATH}` placeholders. Create them all in one batch — do not ask for approval between files.

### Phase 4: Critical Connections
Create the `~/.hermes/SOUL.md` symlink. This is the load-bearing connection.

### Phase 5: Configuration
Run `hermes config set` commands for memory settings, tool enablement, etc.

### Phase 6: Version Control
`git init` + initial commit.

### Phase 7: Verification
Checklist: symlink exists, files readable, config applied, git committed. Print summary.

---

## Placeholder Substitution

Files use `{USER_NAME}`, `{AGENT_NAME}`, `{VAULT_PATH}` as placeholders. The setup agent substitutes these from the gathered variables before writing.

For personalized editions (e.g., Paulina edition), hardcode the agent name and use a richer SOUL.md template.

---

## Syncthing / VPS Architecture

When Hermes runs on a VPS but Obsidian runs locally:

```
Local Machine                    VPS
Obsidian vault/  ←─Syncthing─→  ~/synced-vault/
                                ~/.hermes/SOUL.md → ~/synced-vault/_identity/SOUL.md
```

Key points:
- Syncthing is peer-to-peer, encrypted, no cloud middleman
- Install on both machines: `apt install syncthing` (Linux) or `brew install syncthing` (macOS)
- Web UI at `http://localhost:8384` — SSH tunnel for VPS: `ssh -L 8384:localhost:8384 user@vps`
- Add folder on local, share device ID, accept on VPS, set synced path
- Enable "Simple File Versioning" for conflict safety
- SOUL.md symlink on VPS points to synced copy
- Git remote only on ONE machine to avoid push conflicts

---

## Language Variants (Spanish Edition Pattern)

When creating a non-English edition of a personalized setup:

- **SOUL.md → fully translate.** Identity, voice, relationship guidance, Lessons — all in the target language. This is what the agent reads as its core identity.
- **Vision/Ultron exchange → keep original.** The movie quote stays in English. Add a Spanish introduction to contextualize it for the reader.
- **Protocols (AGENTS.md, HERMES_AUTONOMY.md, Brain/Protocols/) → keep English.** These reference English tool names, CLI commands (`hermes config set`, `write_file`), and file paths that don't translate. Mixing languages in technical documents causes friction.
- **Human-facing files (USER.md, MEMORY.md seed) → translate.** The human reads these, and the agent will write to them in the interaction language.
- **Phase 0 instructions for the human → translate.** Syncthing setup, architecture explanation — the human needs these in their language.
- **Phase 1 questions → translate.** The `clarify()` prompts should be in the human's language.
- **Phase 7 summary → translate.** The final "SETUP COMPLETE" message should match the interaction language.
- **Placeholder rules stay the same.** `{USER_NAME}`, `{AGENT_NAME}`, `{VAULT_PATH}` are code, not prose. Don't translate them.
- **Gender agreement matters.** In languages with grammatical gender (Spanish, French, etc.), the SOUL.md should use feminine forms if the agent has a feminine name (e.g., "Eres amada" not "Eres amado").

The translation should feel natural to a native speaker, not like a literal word-for-word translation. Adapt idioms and phrasing to the target language's natural register.

## Pitfalls

- **No symlink, no integration.** Without `~/.hermes/SOUL.md` → vault, the agent uses the default identity and never finds the vault.
- **Wrong vault path in SOUL.md.** The agent fails silently — won't find AGENTS.md.
- **WSL path format.** Use `/mnt/c/Users/...`, never `C:\Users\...`.
- **clarify() ordering.** Ask one question at a time. Don't batch them — the human may not know the answer to question 3 without seeing questions 1-2 first.
- **Symlink vs copy.** Symlink is always preferred — edits in Obsidian propagate instantly. A copy requires manual sync.
- **Syncthing conflicts.** If Hermes writes and Obsidian edits simultaneously, Syncthing creates `.sync-conflict` files. Rare, but enable versioning as safety net.
- **Git on both machines.** Only push from one. The synced copy is a mirror, not a second authority.
