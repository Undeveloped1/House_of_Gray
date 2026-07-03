# Vault Git Hygiene

The Hermes vault at `/root/.hermes/` has its own git repo for tracking config,
identity files, skills, and profile data. Without a `.gitignore`, it will track
everything — including sensitive and high-churn files.

## What Must Never Be Tracked

| Path | Why |
|------|-----|
| `whatsapp/` | WhatsApp session crypto keys — private key material |
| `logs/` | High-churn, auto-generated, rotated |
| `audio_cache/` | TTS output, regenerable |
| `cache/` | Model catalogs, delegation cache, regenerable |
| `lsp/` | Auto-installed node_modules, regenerable |
| `state-snapshots/` | Pre-update backups, regenerable |
| `node/` | Auto-installed Node runtime |
| `cron/output/` | Cron job output, regenerable |
| `*.db-wal`, `*.db-shm` | SQLite WAL/journal files — regenerable, conflict-prone |
| `.update_check`, `gateway.lock`, `gateway.pid` | Runtime state |
| `rag-venv/` | Removed legacy RAG system |
| `docs/Paul/` | Nested git repo (Syncthing vault) — add as submodule or ignore |
| `profiles/*/docs/` | Per-profile nested vaults |
| `.env` | Contains API keys — consider `.env.example` for tracked version |

## Recommended `.gitignore`

```gitignore
# Cache / temp
audio_cache/
cache/
image_cache/
document_cache/
video_cache/
state-snapshots/

# Logs
logs/
*.log
*.log.*

# Gateway runtime
gateway.lock
gateway.pid
gateway_state.json
channel_directory.json
channel_aliases.json

# Cron runtime
cron/output/
cron/.jobs.lock
cron/.tick.lock
cron/ticker_heartbeat
cron/ticker_last_success

# Build artifacts
desktop-build-stamp.json
context_length_cache.yaml

# LSP (auto-installed)
lsp/

# WhatsApp (crypto keys)
whatsapp/

# Misc runtime
.update_check
.install_method
.skills_prompt_snapshot.json
auth.lock
interrupt_debug.log
kanban.db
kanban.db.*.lock
kanban/
processes.json
response_store.db
memory_store.db
verification_evidence.db
projects.db

# Node runtime
node/

# Legacy
rag-venv/

# Nested repos
docs/Paul/
profiles/*/docs/

# Sandboxes
sandboxes/
pastes/
```

## After Adding `.gitignore`

Already-tracked noise files need `git rm --cached` to stop appearing in status:

```bash
cd /root/.hermes
git rm -r --cached whatsapp/ logs/ lsp/ audio_cache/ cache/ '*.db-wal' '*.db-shm'
git add .gitignore
git commit -m "add .gitignore, untrack runtime noise"
```

## Pitfall: `.env` in Git

The `.env` file contains API keys. If it's already committed, removing it from
tracking doesn't remove it from history. Consider:
- `git rm --cached .env` + add to `.gitignore` for going forward
- Rotate exposed keys if the repo is pushed to a shared remote
- Keep `.env.example` tracked with placeholder values for setup reference
