# Vault Migration — 2026-06-03

How Paul's vault moved from local Windows/WSL to fully standalone VPS.

## Before (Pre-Migration)

- Paul ran on Joe's local machine via WSL
- Identity files (SOUL.md, AGENTS.md) lived in `tcg-engine/docs/Paul/` — a git repo
- Git was the bridge between Paul and Cursor
- WSL paths: `/mnt/c/Users/TheGreyBeard/tcg_engine/`

## Migration Steps (2026-06-02)

1. VPS set up with native Hermes install (no Docker)
2. SOUL.md and AGENTS.md symlinked from `~/.hermes/` → `tcg-engine/docs/Paul/`
3. Vault initially split between two paths:
   - `~/.hermes/docs/Paul/` — VPS sessions wrote here
   - `/root/tcg-engine/docs/Paul/` — git clone mirror (old local copy)
4. Daily Handovers accumulated in both locations

## Standalone Consolidation (2026-06-03)

Problem: dual-path confusion. Paul sessions wrote handovers to wrong directory. AGENTS.md still referenced WSL paths that don't exist on VPS.

Fix:
1. Copied all files from `tcg-engine/docs/Paul/` → `~/.hermes/docs/Paul/` via `rsync --ignore-existing`
2. SOUL.md and AGENTS.md made direct copies in `~/.hermes/` (broke symlinks to tcg-engine)
3. Created `/root/AGENTS.md` symlink → `~/.hermes/AGENTS.md` (Hermes auto-scans working directory)
4. Updated SOUL.md, AGENTS.md, and HERMES_BOOT.md with VPS-correct paths
5. Created new backup git repo: `Undeveloped1/Paul_VPS` on GitHub
6. Old `.git` preserved as `.git.old-hermes-brain`

## Result

- Paul vault: `/root/.hermes/docs/Paul/` (self-contained, backed up to GitHub)
- Identity files: `~/.hermes/SOUL.md` and `~/.hermes/AGENTS.md` (direct copies)
- tcg-engine repo: read-only reference at `/root/tcg-engine/`
- Handoff: `/root/syncthing/paul-dropbox/`
- Backup: `git@github.com:Undeveloped1/Paul_VPS.git` (SSH deploy key)

## Lesson

Never use symlinks for identity files that cross filesystem boundaries. Copies survive migrations; symlinks break. Also: Hermes loads AGENTS.md from the working directory, not from `~/.hermes/` — put it where Hermes actually looks.
