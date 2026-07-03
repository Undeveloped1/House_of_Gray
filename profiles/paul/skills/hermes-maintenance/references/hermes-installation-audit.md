# Hermes Installation Audit — Systematic Scouting Pattern

## When to Use

- User asks for a refactor scout, health check, or "what's bloated" on their Hermes installation
- Periodic maintenance (quarterly health audit)
- Before/after migrations to identify what's worth carrying over
- When disk space is tight and you need to find reclaimable space

## Audit Layers (run in this order)

### Layer 1: Disk Usage Overview

```bash
du -sh ~/.hermes/*/ | sort -rh
du -sh /usr/local/lib/hermes-agent/*/ | sort -rh
```

Look for any directory over 100MB. Flag it for deeper inspection.

### Layer 2: Dead Systems Check

For any large directory, verify it's actually referenced by running code:

```bash
# Check if a directory is referenced by any Python code
grep -rn "<directory-name>" /usr/local/lib/hermes-agent/ --include="*.py" -l

# Check if referenced in configs
grep -rn "<directory-name>" ~/.hermes/ --include="*.yaml" --include="*.json" -l | grep -v ".git/"
```

**Common dead weight candidates:**
- `rag-venv/` — old local RAG systems, superseded by native session_search + vault-rag-first
- `apps/desktop/release/` — full Electron builds on headless VPS (can't run GUI)
- `node_modules/` at project root — only needed for desktop builds, not CLI operation
- `scripts/whatsapp-bridge/` — if WhatsApp platform isn't active
- `state-snapshots/` — pre-update backups, safe to remove after verifying stability

### Layer 3: Duplication Audit

**Profile `bin/` directories:**
```bash
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  bin=$(du -sm "$p/bin" 2>/dev/null | cut -f1)
  [ "$bin" != "0" ] && [ -n "$bin" ] && echo "$bin MB - $name"
done
```

If every profile has the same binary (e.g., `tirith`), compare with `md5sum`:
```bash
md5sum ~/.hermes/profiles/*/bin/tirith
```

Identical binaries → symlink from a shared location. **Known example:** `tirith` (22MB ELF security scanner binary, stripped x86-64) was duplicated across all 10 profiles — same binary, same timestamp, 220MB wasted. One shared copy + symlinks saves ~198MB.

**LSP servers:**
```bash
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  lsp=$(du -sm "$p/lsp" 2>/dev/null | cut -f1)
  [ "$lsp" != "0" ] && [ -n "$lsp" ] && echo "$lsp MB - $name"
done
```

Each profile downloading its own LSP servers = massive duplication. A shared install cuts this by 75%.

### Layer 4: Build Artifacts on Wrong Machine

If the Hermes installation is on a headless server:
- `apps/desktop/release/linux-unpacked/` — can't run, dead weight
- `apps/desktop/dist/` — built frontend assets, dead weight if desktop never runs here
- Project `node_modules/` — build deps for desktop app, dead weight

**Rule:** if the user builds desktop on a local machine, these should not exist on the VPS.

### Layer 4b: Profile Workspace Snapshots\n\nSome profiles accumulate their own backup/snapshot systems independent of root-level `state-snapshots/`. Check:\n\n```bash\nfor p in ~/.hermes/profiles/*/; do\n  name=$(basename \"$p\")\n  snap=$(du -sm \"$p/workspace/snapshots\" 2>/dev/null | cut -f1)\n  [ \"$snap\" != \"0\" ] && [ -n \"$snap\" ] && echo \"$snap MB - $name/workspace/snapshots\"\ndone\n```\n\n**Example:** Niva's `workspace/snapshots/` contained 7 lineage snapshots (~65MB each, 339MB total) from a 3-day period. These were created by an agent-authored disaster recovery tool (`lineage-snapshot.py`) during active development. The tool has a built-in `--prune N` flag that was never called.\n\n**Decision rule from Joe:** \"Everything should also be in git so I'm not understanding why we're keeping those.\" If the data being snapshotted is already version-controlled (profiles tracked in vault git, Syncthing sync), local tarball snapshots are belt-and-suspenders redundancy. Prune aggressively — keep only what's needed for the most recent disaster recovery window.\n\n**Pitfall with agent-authored tools:** `lineage-snapshot.py` had a default `WORKSPACE` path pointing to `nova` profile instead of `niva`, so `--prune` ran against an empty directory and reported \"No snapshots to prune.\" When an agent writes a tool that hardcodes paths, verify the paths match the actual deployment location.\n\n### Layer 5: Git Repo Bloat

```bash
# Check pack file count and size
cd /usr/local/lib/hermes-agent && git count-objects -vH | grep -E "packs|size-pack"

# Check vault git repo
cd ~/.hermes && du -sh .git/ && git count-objects -vH | grep -E "packs|size-pack"
```

Over 20 pack files or packs > 500MB → `git gc --aggressive` may help.

### Layer 6: Profile Efficiency

**Session database sizes:**
```bash
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  [ -f "$p/state.db" ] && echo "$name: $(du -sm "$p/state.db" | cut -f1)MB"
done
```

**PITFALL — Do NOT suggest session pruning for disk space.** Sessions are functional infrastructure, not log cruft. `state.db` is the searchable memory that powers `session_search` — every past conversation the agent can recall lives there. Joe corrected this: *"I leave them active because I think that's how you are grabbing context."* A 16MB `state.db` is not a disk problem — it's working memory. Only suggest pruning if the user explicitly asks about session lifecycle management, and even then, frame it as a trade-off (loss of historical search) not a cleanup win.

**Cron with no jobs:**
```bash
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  if [ -d "$p/cron" ] && [ ! -f "$p/cron/jobs.json" ] && [ -f "$p/cron/ticker_heartbeat" ]; then
    echo "CRON WITH NO JOBS: $name"
  fi
done
```

Cron infrastructure (ticker, output dirs) running with zero actual jobs = wasted cycles.

**Gateway configs with unused platforms:**
```bash
for p in ~/.hermes/profiles/*/; do
  name=$(basename "$p")
  if [ -f "$p/config.yaml" ]; then
    grep -c "telegram\|discord\|slack\|whatsapp\|signal" "$p/config.yaml" > /dev/null
  fi
done
```

### Layer 7: Log Accumulation

```bash
du -sh ~/.hermes/logs/*.log | sort -rh | head -10
```

Any single log over 10MB → investigate. `gateway-exit-diag.log` is a common offender.

### Layer 8: Code Structure (source repo only)

```bash
# Find god files (>3000 lines in main modules)
wc -l /usr/local/lib/hermes-agent/*.py | sort -rn | head -10

# Find large platform adapters
wc -l /usr/local/lib/hermes-agent/gateway/platforms/*.py | sort -rn | head -10
```

Flag files over 5K lines for potential refactoring. `cli.py` and `run_agent.py` are typical offenders.

## Quick-Win Template

After the audit, produce a table:

| Action | Savings | Risk |
|--------|---------|------|
| Remove [dead system] | [size] | None — zero code references |
| Remove [build artifact] | [size] | None — can't run here |
| Symlink [duplicated binary] | [size] | Low — same binary, same date |
| Prune [accumulated data] older than N days | [size] | Low — keep last 2 |
| Schedule sessions prune | Variable | Low |

## Pitfalls

- **Don't delete without verifying.** Always grep for references before removing anything.
- **Don't assume node_modules are dead.** Check if WhatsApp bridge or other Node tools are actively used.
- **Bundled skills are upstream.** Flagging optional-skills as "unused" is wrong — they're the catalog, not your installed set.
- **Platform adapters are upstream.** Zero profile config references doesn't mean the adapter is obsolete — it's just not configured for this user. These ship with Hermes.
- **Git-tracked data doesn't need local tarball backups.** If the files being snapshotted are already version-controlled in the vault git repo (and synced via Syncthing), local compressed snapshots are redundant. Joe's test: "Everything should also be in git so I'm not understanding why we're keeping those." Prune aggressively, keep only the disaster recovery window.
- **Agent-authored tools often have path bugs.** When an AI agent builds a tool like `lineage-snapshot.py`, the default paths often point to the authoring agent's own profile (e.g., `nova` workspace instead of `niva`). Always verify tool defaults match the deployment profile before trusting output.
