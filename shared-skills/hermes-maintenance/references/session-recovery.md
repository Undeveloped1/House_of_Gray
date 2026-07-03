# Session Recovery After Deletion

`hermes sessions delete` does a **hard delete** — removes the row from the `sessions` table, all associated rows from `messages`, and wipes on-disk transcript files (`.json`/`.jsonl`/`request_dump_*`) via `_remove_session_files()`. There is no built-in trash, soft-delete, undo, or recovery command.

Source: `hermes_state.py` → `delete_session()` (line ~4175), `_remove_session_files()`.

## What's Destroyed

| Layer | What happens |
|-------|-------------|
| `sessions` table | Row deleted (hard `DELETE FROM sessions WHERE id = ?`) |
| `messages` table | All rows for that session deleted |
| FTS indexes | Triggers auto-remove entries on `DELETE` |
| Transcript files | `.json`/`.jsonl`/`request_dump_*` removed from `sessions/` dir |
| WAL | Typically checkpointed immediately — `PRAGMA wal_checkpoint` returns `(0,0,0)` after deletion, meaning no un-applied frames remain |

**Delegate children** are cascade-deleted. Branch/compression children are orphaned (`parent_session_id → NULL`) and survive independently.

## `hermes sessions repair` Does NOT Recover Deleted Data

`hermes sessions repair` fixes a **malformed schema** (e.g., "table messages_fts already exists") so hidden sessions reappear in Desktop/Dashboard. It rebuilds FTS indexes and vacuums. It does **not** recover deleted rows. It makes a timestamped backup of the broken DB before repairing — that backup may be useful if the DB was corrupted *before* a delete, but won't contain data that was manually deleted via the CLI.

## Pre-Flight: `strings` Quick-Probe (Always Run First)

Before attempting any heavy recovery method, probe the WAL and main DB with `strings` — it's zero-cost and tells you immediately whether the deleted session's content is even present in recoverable form:

```bash
# 1. Find the session ID (if you know it)
strings /root/.hermes/profiles/<profile>/state.db-wal | grep -E "202[0-9]{5}_[0-9]+_[a-z0-9]+" | sort -u
strings /root/.hermes/profiles/<profile>/state.db | grep -E "202[0-9]{5}_[0-9]+_[a-z0-9]+" | sort -u

# 2. Search for message content fragments
strings /root/.hermes/profiles/<profile>/state.db-wal | grep -v "^[[:space:]]*$" | grep -E ".{40,}" | head -50
```

**Interpreting results:**
- Session ID in WAL but NOT in main DB → was deleted, fragments may exist in WAL free pages
- Session ID in neither → fully overwritten; skip to agent log extraction (option 2) or gateway platform history (option 1)
- Message content fragments in WAL → worth attempting forensic carving
- Only system prompt / config strings → free pages have been recycled with non-session data

**If strings finds the session ID but no content:** Immediately try agent.log extraction (option 2) before attempting forensic carving. It's zero-cost and often yields results even when WAL pages are fully recycled.

**Worked example (2026-06-26):** Abby session `20260624_113029_ef1013` — `strings` on the WAL found the session ID and metadata (`tuigrok-4.3{"model": "grok-4.3", "provider": "xai-oauth"}`) plus user messages from the *current* session discussing the deletion, but no message content from the deleted session itself. `.recover` confirmed zero recoverable INSERT statements. This told us the free pages had been fully recycled by new writes — no point attempting the full Python carving method.

## Recovery Options (in order of likelihood)

### 1. Gateway Platform History (BEST)

If the session happened over a messaging platform (Telegram, Discord, Slack, WhatsApp, etc.), **the conversation is still in the chat history on that platform**. The platform is an independent record — Hermes deleting from its state.db doesn't touch the platform's message store.

Check the platform directly: scroll back in the Telegram chat, Discord channel, etc. The messages are still there unless the user also deleted them from the platform.

### 2. Agent Log Turn Extraction (FAST, NO DEPENDENCIES)

Even when state.db is hard-deleted and WAL free pages are recycled, **agent.log records every user message** in `agent.turn_context` log lines with the `msg=` field. This is the fastest recovery method for any session that ran through a profile with logging enabled.

```bash
# Extract all user messages for a session
grep "agent.turn_context" /root/.hermes/logs/agent.log | grep "msg=" | grep "<session_id>"

# Also check rotated logs
grep "agent.turn_context" /root/.hermes/logs/agent.log.1 | grep "msg=" | grep "<session_id>" 2>/dev/null
```

**What each line contains:**
- Timestamp, session ID, model, provider, platform
- `history=N` — message count at that point in the conversation
- `msg='...'` — the user's message text (may be truncated for long messages)

**What you get:** Every user message with timestamps and turn ordering. This reconstructs the conversation arc (Joe's side) even when Abby's responses are lost.

**What you don't get:** Assistant responses (those are in separate `conversation_loop` lines as `response_len=N`), tool outputs, or the full context.

**Limitations:**
- `msg=` values are truncated at ~120 chars for long messages (visible as `...` suffix)
- Requires the session ID (recoverable from WAL with `strings` even after deletion)
- Only works if agent logging was enabled (it is by default)
- Per-profile logs live at `~/.hermes/profiles/<name>/logs/agent.log`

**Worked example (2026-06-26):** Recovered all 107 user messages from deleted Abby session `20260624_113029_ef1013` despite hard delete + WAL page recycling. Extracted from default profile's agent.log (the session ran as a TUI session via the default profile's agent process). Produced a turn summary markdown table showing timestamp, history count, and message text per turn. Saved to Abby's `docs/sessions/` and Syncthing box for cold storage.

**Post-recovery: where to save recovered data**

When you recover session data, save it to multiple locations so deletion can't wipe all copies:

1. **Profile's docs directory:** `~/.hermes/profiles/<name>/docs/sessions/recovered_<session_id>_*.md`
2. **Syncthing / cold storage:** `/root/syncthing/paul-dropbox/` (or equivalent) — survives VPS loss
3. **User's vault:** if the user has a `~/vault/` or `~/docs/` structure, add a copy there

### 3. Forensic SQLite Recovery from Free Pages

SQLite doesn't zero out deleted pages — it marks them as free in the B-tree. Rows linger in free pages until overwritten by new data. The `state.db` file's "free pages" count from `PRAGMA freelist_count` or `sqlite3_analyzer` output indicates how much unreclaimed deleted data may still be recoverable.

**Prerequisites:**
- The DB file must NOT have been `VACUUM`ed — VACUUM rebuilds the DB from scratch and zeros out free pages
- New writes since the deletion may have overwritten some free pages — recover immediately, don't keep using the profile
- The DB's WAL must be checkpointed (flushed to main file) before carving — if WAL still has frames, checkpoint first: `PRAGMA wal_checkpoint(TRUNCATE)`

**Tool options (ordered by likelihood of being available):**

| Method | Requires | Quality |
|--------|----------|---------|
| **Python stdlib carving** | Python 3 only (no deps) | Extracts readable ASCII text from free pages — best for recovering human-authored content (design docs, conversation fragments). Won't reconstruct exact SQL rows but gets the actual content. |
| `sqlite3` CLI `.recover` | sqlite3 package (`apt install sqlite3`) | Attempts to reconstruct complete SQL rows from all pages including free ones |
| `undark` | Third-party tool | Specialized SQLite forensic carver |
| `foremost`/`scalpel` | Third-party | General file carvers for raw disk images |

#### Method A: Python stdlib carving (no dependencies)

This is the go-to when `sqlite3` isn't installed and you need results fast. It reads page headers to identify free pages, then extracts all printable ASCII runs from those pages:

```python
import struct

DB_PATH = '/root/.hermes/profiles/<profile>/state.db'

with open(DB_PATH, 'rb') as f:
    raw = f.read()

# Parse page size from SQLite header (bytes 16-17, big-endian)
page_size = struct.unpack('>H', raw[16:18])[0]
if page_size == 1:
    page_size = 65536  # SQLite3 uses 1 to mean 65536

# Iterate every page. Page type is byte 0:
#   0x0D = leaf-table, 0x05 = interior-table
#   0x0A = leaf-index, 0x02 = interior-index
#   0x00 = free page (our target)
all_text = []
for pg in range(len(raw) // page_size):
    offset = pg * page_size
    if raw[offset] != 0x00:
        continue  # skip non-free pages

    page_data = raw[offset:offset + page_size]
    body = page_data[4:]  # skip 4-byte freelist trunk header

    # Skip near-empty pages (no meaningful data)
    non_zero = sum(1 for b in body if b != 0)
    if non_zero < 100:
        continue

    # Extract printable ASCII runs > 30 chars
    current = b''
    for byte in body:
        if 32 <= byte < 127 or byte in (10, 13):
            current += bytes([byte])
        else:
            if len(current) > 30:
                all_text.append((pg, current.decode('ascii', errors='replace')))
            current = b''
    if len(current) > 30:
        all_text.append((pg, current.decode('ascii', errors='replace')))

print(f"Found {len(all_text)} text chunks across free pages")

# Filter for relevant content
for pg, text in all_text:
    if 'session_id' in text.lower() or 'role' in text.lower():
        print(f"\n--- Page {pg} ---\n{text[:500]}")
```

**What you'll find:** System prompt fragments (harmless noise), conversation turns (role-labeled), tool call JSON payloads, and any documents or creative content the agent generated during the session. The content is interleaved with SQLite row structure bytes, so it won't reconstruct perfect transcripts — but you'll recover the intellectual content: design decisions, code snippets, document text, etc.

**What you won't get:** Exact message ordering, timestamps, tool output fidelity. Free pages are reassigned by SQLite's B-tree allocator with no ordering guarantee. The goal is content recovery, not transcript reconstruction.

#### Method B: sqlite3 `.recover` (when sqlite3 is available)

```bash
# 1. Stop using the profile immediately — every new message overwrites free pages
# 2. Make a copy of the DB
cp /root/.hermes/profiles/<profile>/state.db /tmp/state_recovery.db
# 3. Install sqlite3 if not present
apt install sqlite3
# 4. Attempt recovery (dumps all reconstructable rows to SQL)
sqlite3 /tmp/state_recovery.db ".recover" > /tmp/recovered.sql
# 5. Search recovered SQL for session rows and messages
grep "INSERT INTO sessions" /tmp/recovered.sql
grep "INSERT INTO messages" /tmp/recovered.sql
```

This is **not guaranteed** — free pages get fragmented and overwritten. Speed matters: the longer the profile is used after deletion, the more free pages get recycled.

#### Worked example: Digital Girlfriends design doc recovery (2026-06-26)

Paul deleted Abby's session via `hermes -p abby sessions prune --older-than 0 --yes`. The profile had `memory_enabled: false` so nothing was in memory. Abby had created a full game design document with 10 archetypes, 4-stage progression tables, memory architecture, and messaging layer specs.

**Recovery process:**
1. Checked `~/.hermes/state-snapshots/` — found a pre-update snapshot but it was for the default profile, not Abby
2. Checked WAL — already checkpointed, `(0,0,0)`  
3. Used the Python stdlib carving method above — extracted text from 69 free pages
4. Filtered for design content (keywords: archetype, girlfriend, memory, progression, intimacy)
5. Reconstructed a 308-line, 18.5KB game design document from the fragments
6. Saved recovered doc to the vault: `/root/.hermes/docs/Paul/projects/<project>/`

**Key lessons from this recovery:**
- The Python method worked despite no `sqlite3` on the system
- Content was recoverable because only ~2 sessions had been written since deletion — free pages hadn't been heavily recycled
- The `state-snapshots` directory only contains the **default** profile's state, not other profiles
- `memory_enabled: false` on Abby's profile meant there was zero secondary storage — memory + state.db deletion = total loss without forensic recovery

### 4. Filesystem Snapshots / Backups

Check for:
- LVM snapshots: `lvs` or `lvdisplay`
- Btrfs/ZFS snapshots: `btrfs subvolume list /` or `zfs list -t snapshot`
- System backups (restic, borg, rsync, etc.)
- `~/.hermes/` tarballs or exports

**Profile-specific pitfall — backup scripts often only target the default profile.** The daily session backup at `/root/.hermes/scripts/session_backup.sh` runs `hermes sessions export` without `--profile`, which only exports the default profile's state.db. Non-default profiles (abby, paul, etc.) have **no automated backup** unless explicitly configured. Check any cron jobs or backup scripts for `--profile` flags before assuming they cover the profile you need.

### 5. Reconstruct from Session Search Across Profiles

If the deleted session's content was referenced or repeated in another profile's sessions (e.g., Paul discussing something Abby said), `session_search()` across profiles may surface fragments. This can't recover the full transcript but can reconstruct key decisions and context.

### 6. Curator Backups (Skills Only)

The curator backs up `~/.hermes/skills/` before archival operations (tarball in `.curator-backups/`). It does **not** back up `state.db`. Only useful if the deleted session contained skill-related context that was then encoded into a skill file that still exists.

## Prevention: Profile Hardening Checklist

Apply these three changes to any profile that creates intellectual property. This session's Abby profile disaster (all design work lost to a single `prune --older-than 0`) is the canonical case for hardening.

### 1. Enable persistent memory

Without memory, deleted sessions leave zero secondary storage. Memory saves key facts across sessions:

```bash
hermes -p <profile> config set memory.memory_enabled true
hermes -p <profile> config set memory.user_profile_enabled true
```

### 2. Enable filesystem checkpoints

Checkpoints give you `/rollback` safety during a session — if something goes wrong mid-session, you can rewind. Without them, there's no undo:

```bash
hermes -p <profile> config set checkpoints.enabled true
```

### 3. Remove destructive scripts

Shell scripts wrapping `hermes sessions prune --older-than 0 --yes` or equivalent nuclear commands are accidents waiting to happen. Find and delete them:

```bash
find ~/.hermes/scripts/ -name "*purge*" -o -name "*prune*" -o -name "*clean*" 2>/dev/null
# Delete any that nuke sessions without confirmation
```

### Manual backups (belt-and-suspenders)

```bash
# Export important sessions before deleting
hermes sessions export ~/session-backups/ --profile abby

# Set up a cron job to periodically back up state.db
cp /root/.hermes/profiles/abby/state.db /root/backups/abby-state-$(date +%Y%m%d).db
```

**For profiles that create intellectual property:** All three hardening steps should be applied at profile creation time. When memory is off and checkpoints are disabled and a purge script exists, a single command can destroy everything — and forensic SQLite carving is the only recovery path.

## Pitfall: `prune --older-than 0` Is Nuclear

`hermes sessions prune --older-than 0 --yes` deletes **every session** in the profile. The `--older-than` flag uses days, and 0 means "older than 0 days" = all sessions. This is commonly wrapped in shell scripts (e.g., `abby_purge.sh`) and can be triggered accidentally.

**Before running prune with aggressive thresholds:**
```bash
# Always dry-run first
hermes -p <profile> sessions list

# Export before pruning
hermes -p <profile> sessions export /tmp/<profile>-backup-$(date +%Y%m%d).jsonl
```

## Provider-Specific: xAI / Grok Server-Side Conversation Storage

When sessions ran through xAI's API (grok-4.3, etc.), xAI **does** store conversations on their servers. The OAuth scopes include `conversations:read` and `conversations:write`, confirming server-side persistence.

**What we actually found (2026-06-26):** Tested with a live xAI OAuth bearer token (valid, confirmed working against `/v1/models`). Every conversation endpoint returned 404 (not 403):
- `api.x.ai/v1/conversations` → 404
- `api.x.ai/v1/threads` → 404  
- `api.x.ai/v1/chat/conversations` → 404
- `api.x.ai/v1/chat/list` → 404
- `grok.x.ai/api/conversations` → Cloudflare 301 (redirects to web frontend, not an API)

xAI's API is strictly OpenAI-compatible for chat completions only. No REST endpoint for conversation history retrieval exists. The `conversations:read` scope in the OAuth token is a red herring — the server-side storage exists but is only accessible through browser login at `grok.com`.

**What this means for recovery:**
- Conversation data **exists** on xAI's servers tied to the authenticated account
- It **cannot** be retrieved via CLI, API key, or OAuth token alone — requires browser-based login
- The user must log into `grok.com` with their Google account to view and potentially export history
- `conversations:read` scope is present in the OAuth token but the endpoint is web-gated, not API-gated

**Account identification (2026-06-26):** OAuth userinfo endpoint (`auth.x.ai/oauth2/userinfo`) confirmed the account as `joseph.s.grayii@gmail.com` (Joseph Gray II).

**Other providers:** This pattern may apply to other OAuth-based providers. Check the OIDC discovery doc at `<auth-server>/.well-known/openid-configuration` for scopes like `conversations:read` — if present, the provider stores conversations but likely gates them behind web auth.

## Pitfall: `state-snapshots` Only Cover the Default Profile

Hermes pre-update snapshots at `~/.hermes/state-snapshots/` only capture the **default** profile's state. Other profiles (abby, paul, etc.) are not snapshotted during updates. If you deleted a session from a non-default profile, the snapshot won't help — you need forensic recovery or platform history.
