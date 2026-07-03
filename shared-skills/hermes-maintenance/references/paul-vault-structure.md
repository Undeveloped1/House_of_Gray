# Paul Vault Structure — VPS (Standalone)

## Directory Layout

```
~/.hermes/
├── SOUL.md                  # Paul's identity (standalone copy, NOT symlinked)
├── AGENTS.md                # Paul's protocols (standalone copy, NOT symlinked)
├── USER.md                  # (managed by memory system)
├── docs/Paul/               # CANONICAL VAULT — all Paul work lives here
│   ├── _identity/           # SOUL.md, USER.md (source copies)
│   ├── Brain/               # Protocols, Daily Handovers, Session Context
│   │   ├── AGENTS.md        # Working protocols
│   │   ├── HERMES_BOOT.md   # Boot orientation (VPS-specific)
│   │   ├── VAULT_MAP.md     # Where everything lives
│   │   ├── SPARK.md         # Identity bridge for migrations
│   │   ├── Protocols/       # Detailed process instructions
│   │   ├── Daily/           # Per-calendar-day handover files
│   │   ├── Session Context/ # Snapshot copies of session materials
│   │   ├── Working Memory/  # Slim current-state context
│   │   └── Long-Term Memory/ # Insights, lessons, patterns
│   ├── memories/            # MEMORY.md (Hermes memory system)
│   ├── workspace/           # Working documents (design passes, drafts)
│   └── playbooks/           # Reusable workflow scripts
│
/root/
├── AGENTS.md → ~/.hermes/AGENTS.md   # Symlink for Hermes auto-load from cwd
│
/root/tcg-engine/            # GIT REPO — Cursor territory
├── docs/Paul/               # READ-ONLY mirror (Cursor maintains this)
│   ├── _identity/           # Source copies that get committed
│   └── Brain/               # Source copies that get committed
```

## Golden Rules

1. **Paul writes to `/root/.hermes/docs/Paul/` — NEVER to `/root/tcg-engine/docs/Paul/`**
   (except the handoff folder, see below). Cursor owns the git repo. Two hands in the same file
   breaks things and creates merge conflicts — Joe's #1 concern.

2. **Paul reads from `/root/tcg-engine/docs/` freely.** Design docs, lore, card data
   are all readable. Just don't write to them.

3. **Handoff folder (docs/Paul_Handoff/ — the ONE exception):** Created by Cursor on 2026-06-03.\n   Paul writes deliverables to `docs/Paul_Handoff/incoming/`. Cursor reads and merges into\n   `docs/Five_Crests/`. Structure:\n   ```\n   docs/Paul_Handoff/\n   ├── README.md              # Rules + merge flow\n   ├── incoming/              # *_Paul.md drafts (by faction subfolder)\n   ├── questions/             # Async questions for Joe\n   ├── sessions/              # Short pass handoffs\n   └── _templates/            # DRAFT_Paul_TEMPLATE.md\n   ```\n   Also available for handoff: the Syncthing dropbox at `/root/syncthing/paul-dropbox/`.\n   AGENTS.md § File System Boundaries carries the explicit exception.

4. **Identity files (SOUL.md, AGENTS.md) are standalone copies in `~/.hermes/`.**
   Not symlinked to tcg-engine. Paul's vault is fully self-contained on the VPS.
   If these need updating, edit the `~/.hermes/` copy AND the tcg-engine copy
   (so Cursor can commit).

5. **The primary bridge is Syncthing.** Dropbox at `/root/syncthing/paul-dropbox/` is the
   cross-filesystem handoff for non-tcg-engine deliverables.

6. **Hermes loads AGENTS.md from the working directory (`/root/`).** The symlink at
   `/root/AGENTS.md → ~/.hermes/AGENTS.md` is critical for auto-load at session start.
   Without it, AGENTS.md is not injected into the system prompt.

7. **Updates survive Hermes upgrades.** `~/.hermes/` config files get touched by
   updates. `/root/AGENTS.md` and files in `/root/.hermes/docs/Paul/` are outside
   both `~/.hermes/` proper and `/usr/local/lib/hermes-agent/` — the updater
   never scans them.

8. **GitHub backup:** Paul's vault should be backed up to its own GitHub repo
   (separate from the old `hermes-brain` repo). `gh` CLI installed on VPS.
   Repo name TBD, auth via PAT.

## Path Duality — Historical Context

During the June 2 VPS migration, Paul's vault was cloned to both locations
(`.hermes/docs/Paul/` for VPS sessions and `tcg-engine/docs/Paul/` for git).
This created divergence — VPS sessions wrote handovers to `.hermes/`, but the
full vault structure (protocols, memories, workspace) only existed in tcg-engine.

On June 3, `rsync --ignore-existing` merged everything into `.hermes/docs/Paul/`,
making it the single source of truth. The tcg-engine copy is now a git-tracked
mirror that Cursor commits from.

## Common Mistakes

- **Writing a Daily Handover to `tcg-engine/docs/Paul/Brain/Daily/`** — wrong path.
  Always write to `/root/.hermes/docs/Paul/Brain/Daily/YYYY-MM-DD_Daily_Handover.md`.

- **Creating files in the wrong vault** — check your cwd and target path.
  `find /root/.hermes/docs/Paul -name "*.md" -newer <reference-file>` confirms
  where writes actually landed.

- **Symlinking identity files to tcg-engine** — creates a dependency on the git
  repo that breaks if the repo moves or gets recloned. Standalone copies in
  `~/.hermes/` are the correct approach.
