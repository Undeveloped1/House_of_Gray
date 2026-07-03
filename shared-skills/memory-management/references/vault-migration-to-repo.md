# Vault Migration to Shared Repo

Pattern for moving Paul's identity files from standalone Obsidian vault into a shared git repo where Cursor can see them directly.

## When to use

- Consolidating Paul + Cursor into single-source-of-truth repo
- Retiring the bridge/sync layer
- Any move where Paul's SOUL, MEMORY, USER, AGENTS, and protocols need to live in a shared filesystem

## Target layout (Joe's corrected layout)

Joe rejected Cursor's flat `docs/hermes/paul/` migration. The correct target is a 1:1 vault replication at `docs/Paul/`:

```
tcg_engine/docs/Paul/
├── .obsidian/              ← Obsidian config lives here, not docs/.obsidian/
├── _identity/
│   ├── SOUL.md
│   └── USER.md
├── memories/
│   └── MEMORY.md
├── Brain/
│   ├── AGENTS.md
│   ├── Daily/
│   ├── Protocols/
│   ├── Session Context/
│   ├── Working Memory/
│   ├── Long-Term Memory/
│   └── Archive/
├── design/                 ← LEGACY — real work in Joe-assigned folders
├── bridge/                 ← LEGACY — bridge being retired
└── README.md
```

Key architectural principle: **docs/Paul/ is Paul's brain only** (identity + memory + protocols). Real design work happens in Joe-assigned shared folders like `docs/bridge/paul_design/bruiser_revisions/`. Paul's brain and Paul's workshop are separate locations.

## Hermes boot config (post-migration)

- **Hermes workdir:** `C:\\Users\\TheGreyBeard\\tcg_engine` (repo root) — lets Paul read/write any path in docs/ without special casing
- **SOUL.md path:** `docs/Paul/_identity/SOUL.md`
- **AGENTS.md path:** `docs/Paul/Brain/AGENTS.md`
- **MEMORY.md path:** `docs/Paul/memories/MEMORY.md`
- **Obsidian vault:** Open `tcg_engine/docs` — sees Paul/, Five_Crests/, playbooks/, all in one graph

### Symlink commands (the actual flip)

These are the exact commands that wire Hermes to load from the repo instead of the old vault. Run from WSL:

```bash
# SOUL.md — loaded from ~/.hermes/ each session
ln -sf /mnt/c/Users/TheGreyBeard/tcg_engine/docs/Paul/_identity/SOUL.md ~/.hermes/SOUL.md

# AGENTS.md — loaded from /home/thegreybeard/ each session
ln -sf /mnt/c/Users/TheGreyBeard/tcg_engine/docs/Paul/Brain/AGENTS.md /home/thegreybeard/AGENTS.md

# MEMORY.md — loaded from /home/thegreybeard/ each session
ln -sf /mnt/c/Users/TheGreyBeard/tcg_engine/docs/Paul/memories/MEMORY.md /home/thegreybeard/MEMORY.md

# Verify all three point to repo
readlink -f ~/.hermes/SOUL.md
readlink -f /home/thegreybeard/AGENTS.md
readlink -f /home/thegreybeard/MEMORY.md
```

Old symlink targets (for rollback reference):
- `~/.hermes/SOUL.md` → `ObsidianHermesVault/Paul/_identity/SOUL.md`
- `/home/thegreybeard/AGENTS.md` → `ObsidianHermesVault/Paul/Brain/AGENTS.md`
- `/home/thegreybeard/MEMORY.md` → `ObsidianHermesVault/Paul/memories/MEMORY.md`

Canonical boot doc: `docs/Paul/Brain/HERMES_BOOT.md`

## Steps (Joe's corrected approach)

1. Cursor/Joe runs `scripts/migrate-paul-vault.ps1` — does full 1:1 replication
2. Paul verifies: `docs/Paul/` exists with Brain/, _identity/, memories/, .obsidian/
3. Joe updates Hermes workdir to repo root
4. Paul stops writing to old `ObsidianHermesVault/Paul/` (frozen, rollback only)
5. Clean up Cursor's flat duplicate at `docs/hermes/paul/` if it exists

## Pitfalls

- **Cursor's flat layout is WRONG.** `docs/hermes/paul/` with flat SOUL/MEMORY/USER and no Brain/ tree — Joe rejected this. The correct layout is 1:1 vault replication at `docs/Paul/`. If `docs/hermes/paul/` exists after migration, it's a duplicate artifact to be cleaned up.
- **Git user config may be missing in WSL:** `git config user.email + user.name` before commit
- **The vault migration itself is a one-time event** — do NOT save it to core memory. It's documented in VAULT_MIGRATION.md, AGENTS.md, and the Daily Handover. Core memory is for durable behavioral facts.
- **Obsidian `.obsidian/` goes in `docs/Paul/.obsidian/`**, not `docs/.obsidian/`. Joe opens `tcg_engine/docs` as vault — Obsidian finds the config inside Paul/.
- **`docs/Paul/design/` is legacy.** Real Bruiser work happens in `docs/bridge/paul_design/bruiser_revisions/`. Don't write new design work under Paul/design/.
- **`.lock` and `.bak.*` files are transient.** Obsidian creates `MEMORY.md.lock`, `USER.md.lock` (0-byte) and timestamped `USER.md.bak.*` backups during editing. These are filesystem artifacts, not content. Do NOT migrate them — they'll show as "missing" in file comparisons but are correctly excluded.
- **Hermes workdir is set via config, not symlink.** The exact command: `hermes config set terminal.cwd /mnt/c/Users/TheGreyBeard/tcg_engine`. This is separate from the symlink chain for SOUL/AGENTS/MEMORY. Without it, terminal commands default to the launch directory and may not resolve repo-relative paths.

## Post-migration verification

After migration + symlink flip, run this checklist:

```bash
# 1. Verify all three symlinks point to repo
readlink -f ~/.hermes/SOUL.md
readlink -f /home/thegreybeard/AGENTS.md
readlink -f /home/thegreybeard/MEMORY.md

# 2. Verify workdir
grep 'cwd:' ~/.hermes/config.yaml

# 3. File count comparison (exclude .git, .obsidian, .bak, .lock)
OLD=$(find /mnt/c/Users/TheGreyBeard/ObsidianHermesVault/Paul -type f \
  -not -path '*/.git/*' -not -name '*.bak.*' -not -name '*.lock' | wc -l)
NEW=$(find /mnt/c/Users/TheGreyBeard/tcg_engine/docs/Paul -type f \
  -not -path '*/.obsidian/*' | wc -l)
echo "Old: $OLD  New: $NEW"

# 4. Critical directory counts (spot-check)
echo "Daily: $(ls docs/Paul/Brain/Daily/*.md | wc -l)"
echo "Protocols: $(ls docs/Paul/Brain/Protocols/*.md | wc -l)"
echo "Session Context: $(find docs/Paul/Brain/Session\ Context -type f | wc -l)"
```

All counts should match exactly. If they don't, the migration is incomplete and the old vault should remain the rollback target.
