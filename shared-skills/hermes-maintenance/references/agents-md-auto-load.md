# AGENTS.md Auto-Load Mechanism

## The Problem

Paul was NOT auto-loading AGENTS.md at session start, despite the instruction
in SOUL.md to "read Brain/AGENTS.md and follow all protocols." Joe caught this
when Paul failed to load boot protocols and didn't know the session workflow.

Root cause: AGENTS.md was symlinked at `~/.hermes/AGENTS.md`, but Hermes
does NOT load it from there. It loads from the **working directory**.

## How Hermes Actually Loads Context Files

From `agent/prompt_builder.py` — `build_context_files_prompt()`:

```
Priority (first match wins — only ONE project context type is loaded):
  1. .hermes.md / HERMES.md  (walk to git root)
  2. AGENTS.md / agents.md   (cwd only)
  3. CLAUDE.md / claude.md   (cwd only)
  4. .cursorrules / .cursor/rules/*.mdc  (cwd only)

SOUL.md from HERMES_HOME is independent and always included when present.
```

`_load_agents_md()` searches the working directory (`cwd_path`) for
`AGENTS.md` or `agents.md`. Not `~/.hermes/`. Not `HERMES_HOME`.

SOUL.md is loaded separately via `load_soul()` from `HERMES_HOME` — that's
why SOUL.md always works and AGENTS.md didn't.

## The Fix

**Step 1:** Ensure AGENTS.md exists as a standalone file in `~/.hermes/` (not symlinked to tcg-engine repo — Paul's vault is self-contained on VPS):

```bash
# If it's a symlink, break it and copy standalone
cp /root/.hermes/docs/Paul/Brain/AGENTS.md ~/.hermes/AGENTS.md
```

**Step 2:** Create a symlink from the working directory to `~/.hermes/AGENTS.md`:

```bash
ln -sf /root/.hermes/AGENTS.md /root/AGENTS.md
```

Where:
- `/root/` is the Hermes working directory (`cwd`) — where Hermes looks for AGENTS.md
- `/root/.hermes/AGENTS.md` is the standalone canonical copy in Paul's VPS vault
- SOUL.md follows the same pattern (`~/.hermes/SOUL.md` as standalone copy)
- No dependency on `/root/tcg-engine/` — Paul's vault is fully self-contained
- Updates won't touch `/root/AGENTS.md` because it's outside `~/.hermes/` install tree

## Verification

After creating the symlink, the next session's system prompt should include
AGENTS.md content (visible as a `[Subdirectory context discovered: AGENTS.md]`
block or similar context injection).

On the VPS, check what Hermes sees:

```bash
ls -la /root/AGENTS.md          # symlink exists?
cat /root/.hermes/AGENTS.md     # different location — NOT what Hermes loads
hermes workdir                  # verify working directory is /root
```

## Why This Survives Updates

- `~/.hermes/config.yaml` — touched by updates
- `~/.hermes/skills/` — synced by updates
- `~/.hermes/.env` — touched by updates
- `/root/AGENTS.md` — a random symlink in the home directory, invisible to
  the updater. Never scanned, never modified, never removed.

Same reason Joe's music files in `/home/` survive OS reinstalls — they're
outside the package manager's jurisdiction.

## Pitfall: Don't Override the Wrong AGENTS.md

`/root/tcg-engine/AGENTS.md` (22KB) is a DIFFERENT file — it's the general
project AGENTS.md for Cursor/Claude. Paul's AGENTS.md lives at
`/root/tcg-engine/docs/Paul/Brain/AGENTS.md` in the repo, but the canonical
VPS copy is `~/.hermes/AGENTS.md` (standalone, not symlinked). The symlink at
`/root/AGENTS.md` must point to `~/.hermes/AGENTS.md`, not the tcg-engine
version.

## Pitfall: AGENTS.md Not Updating After Edits

If AGENTS.md was symlinked to the tcg-engine repo and the repo path changed,
edits to the canonical file stop propagating. Verify with `readlink -f`:

```bash
readlink -f /root/AGENTS.md          # should resolve to ~/.hermes/AGENTS.md
readlink -f ~/.hermes/AGENTS.md      # should NOT be a symlink — standalone file
```

## Pitfall: Two Paul Vaults

There are two `docs/Paul/` directories:
- `/root/.hermes/docs/Paul/` — **canonical VPS vault** (where Paul writes)
- `/root/tcg-engine/docs/Paul/` — git repo mirror (Cursor territory, Paul reads but never writes)

Writing to the wrong one creates duplicates. Always check the path before `write_file`.
See `references/paul-vault-structure.md`.
