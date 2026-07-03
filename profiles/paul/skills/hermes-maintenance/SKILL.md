---
name: hermes-maintenance
description: Update, audit, and maintain the Hermes Agent installation — running updates, handling user-modified bundled skills, auditing skill library for dead weight.
tags: [hermes, maintenance, update, skills, audit]
---

# Hermes Maintenance

## When to Use

- User runs `hermes update` or asks to update Hermes
- User asks about user-modified skills blocking updates
- User wants to audit the skill library for bloat or dead weight
- User asks for a full installation audit or refactor scout — disk hogs, dead systems, duplication, build artifacts, git bloat, profile efficiency. See `references/disk-space-scouting.md` for the systematic 11-point scouting checklist with quick-win priorities.
- **`.hermes/.git` vault repo hygiene** — the vault git repo tracks everything by default, including WhatsApp crypto keys, SQLite WALs, logs, and cache. See `references/vault-git-hygiene.md` for the `.gitignore` template and untracking procedure.
- After an update completes and reports "user-modified (kept)" skills
- User wants to migrate Hermes to a VPS or new machine — see `references/vps-migration.md` for full plan
- User is deploying to Hostinger VPS (or troubleshooting a Hostinger template) — see `references/hostinger-vps.md` for template-specific details
- **Paul wakes up after a migration with amnesia/disorientation** — see `references/post-migration-orientation.md` for the SPARK.md protocol and orientation checklist
- **Pre-migration: create SPARK.md** — before migrating Paul's identity files, the source Paul should write a SPARK.md bridge document (shorthand, inside jokes, current state, tone) to `docs/Paul/Brain/SPARK.md`. The destination Paul reads this on first boot to skip the disorientation period. See `references/post-migration-orientation.md` for the format.
- **VPS file sync between Joe and Paul** — Syncthing is set up for peer-to-peer sync. See `references/syncthing-setup.md` for device ID, service management, and verification.
- **Gateway platform issues** — Telegram "Unauthorized user," stuck pairing codes, WhatsApp pairing failures, gateway restart stalls. See `references/gateway-troubleshooting.md`.
- **Gateway appears dead but isn't** — systematic diagnostic sequence: process check, port binding, health check, log analysis, direct API test, event loop trace, cross-process collision detection. See `references/gateway-health-check.md`.
- **Telegram chat routing config** — `allowed_chats` whitelist vs. blacklist (no `blocked_chats` exists), `free_response_chats`, `require_mention`, `_should_process_message` source reference. See `references/telegram-routing-config.md`.
- **Telegram bot token setup** — `hermes config set telegram.bot_token` fails (routes to env vars). Bot token goes in `.env` as `TELEGRAM_BOT_TOKEN`, not `config.yaml`. See `references/telegram-bot-setup.md`.
- **New profile wiring (model → API key → bot → gateway)** — end-to-end checklist for bringing a new profile online with DeepSeek + Telegram. See `references/profile-wiring-checklist.md`.
- **Dashboard SSH tunnel setup** — setting up `paul-dash` SSH config alias, WSL heredoc pitfalls, port 9119, desktop app remote session token. See `references/dashboard-ssh-tunnel.md`.
- **Desktop app broken / setup helper / rebuild failure on macOS** — see `references/hermes-desktop-repair.md` for full diagnostic + repair workflow (Electron missing, npm ignore-scripts, setup-helper stuck).
- **AGENTS.md not auto-loading at session start** — Hermes loads from working directory (`/root`), not `~/.hermes/`. Symlink fix, verification, update-survival. See `references/agents-md-auto-load.md`.
- **Duplicate/contradictory SOUL or AGENTS in system prompt** — stale `prefill.json` injecting old identity files before normal loading. Diagnostic path, diff-merge-fix, no gateway restart needed. See `references/prefill-json-duplicates.md`.
- **Context budget bloated or tokens unaccounted for** — user reports burning too many tokens at session start. Parse request_dump JSONs to measure actual overhead by component (SOUL, AGENTS, tools, skills, memory). See `references/context-budget-audit.md`.
- **Paul vault path structure (VPS standalone)** — canonical paths, golden rules, path duality, common mistakes. See `references/paul-vault-structure.md`.
- **GitHub backup repo setup** — `gh` CLI install, PAT authentication, vault backup push, token security. See `references/github-backup-setup.md`.
- **Agent heartbeat / autonomous execution** — replicate OpenClaw-style heartbeat autonomy in Hermes: self-programming task lists, admission-gated wakeups, zero-cost idle cycles. See `references/agent-heartbeat-autonomy.md`.
- **Ephemeral (no-record) profiles** — create profiles that leave zero trace: memory disabled, session pruning cronjob, self-delete at close. See `references/ephemeral-profile-pattern.md`.
- **Agent self-authored SOUL** — when an AI agent extracts its own identity from a lost conversation and crystallizes it into a durable SOUL file. See `references/agent-self-authored-soul.md`.
- **Profile isolation / preventing cross-profile context bleed** — root-level AGENTS.md, SOUL.md, and identity files can be injected into any profile. Pattern: create dedicated `paul` / `abby` profiles, migrate root identity files into the correct profile directory. See `references/profile-isolation.md`.
- **Profile migration (clone default → named, with sessions)** — `hermes profile create --clone-all` copies config/skills/memory/cron but excludes sessions. Manual state.db copy required, gateway lock pitfall, verification steps. See `references/profile-migration.md`.
- **Recovering a deleted session** — `hermes sessions delete` is a hard, irreversible delete (rows + messages + transcript files wiped). Recovery paths: gateway platform history (best), forensic SQLite free-page carving, filesystem snapshots. See `references/session-recovery.md`.
- **Credential diagnostics** — inspecting OAuth/API-key state in auth.json: decode JWTs, check expiration, distinguish empty pool vs expired token vs working token, cross-profile credential differences. See `references/credential-diagnostics.md`.

## Pitfall: OAuth Web-Flow on Headless VPS

OAuth authentication flows that require browser interaction (device code, loopback PKCE, redirect URI) silently hang or time out on headless servers. The VPS has no display server, no browser, and no way to complete the web-based authorization step.

**Providers affected:** `xai-oauth`, `github-device-flow`, `nous` device code, any OAuth flow with a URL the user must visit.

**Symptoms:**
- `hermes auth add xai-oauth` hangs indefinitely (>30s timeout)
- `hermes -p abby chat -q "hi"` returns HTTP 400 with "Incorrect API key provided" — the stored OAuth JWT token expired and can't be refreshed without browser interaction
- The credential shows in `hermes auth list` but is non-functional

**Fix:** Use a real API key instead of OAuth. For xAI: obtain an `XAI_API_KEY` from https://console.x.ai and place it in the profile's `.env` file. API keys don't expire with OAuth token lifetimes and don't require browser re-authentication.

**If OAuth is the only option:** Run the auth flow on a machine with a browser (desktop/laptop), then export the resulting `auth.json` to the VPS. The tokens will eventually expire and require the same process again.

**Worked example (2026-06-22):** Abby profile configured for xAI/grok-4.3. `hermes auth add xai-oauth` timed out (30s) because the loopback PKCE flow tried to open a browser on the headless VPS. The existing `xai-oauth` credential in `auth.json` was a stale JWT that returned HTTP 400. Fix: obtain `XAI_API_KEY` from console.x.ai, set in Abby's `.env`.

## Pitfall: Tirith Duplication Across Profiles

Hermes auto-installs `tirith` (command security scanner from `sheeki03/tirith`) to `$HERMES_HOME/bin/tirith` on first startup. Since each profile has its own `$HERMES_HOME`, every profile independently downloads the same 22MB ELF binary. With 10 profiles, that's 220MB of identical copies.

**Fix — single shared binary with symlinks:**

```bash
# Pick one copy as canonical, delete the rest, symlink
mkdir -p /root/.hermes/bin
cp /root/.hermes/profiles/paul/bin/tirith /root/.hermes/bin/tirith
chmod +x /root/.hermes/bin/tirith

for p in /root/.hermes/profiles/*/bin/tirith; do
  rm "$p"
  ln -s /root/.hermes/bin/tirith "$p"
done

# Verify: all should report same version
for p in /root/.hermes/profiles/*/bin/tirith; do
  "$p" --version
done
```

The resolution code in `tools/tirith_security.py::_resolve_tirith_path()` checks `os.path.isfile()` + `os.access(X_OK)` — both follow symlinks. No config changes needed. Saves 198MB. Hermes will never auto-download a replacement as long as the symlink target exists and is executable.

## Pitfall: Sessions Are Memory, Not Cruft

`state.db` stores every session transcript with FTS5 indexing. `session_search` depends on this data — it's how the agent retrieves past decisions, preferences, and context across sessions. **Never propose pruning sessions as a space-saving measure.** 16MB of state.db is functional infrastructure, not bloat. The 5GB RAG venv or 398MB desktop build is bloat. Treat them differently.

**Wrong:** "abby's state.db is 26MB, let's prune old sessions."  
**Right:** "abby's state.db is 26MB of searchable memory that gives her continuity."

## Pitfall: Verify Before Claiming Safety on Destructive Actions

When proposing deletion of build artifacts or directories, don't assume safety from context alone. Joe will ask "Are you sure about what you just said — verify." Before claiming something is safe to delete:

1. Check git tracking: `git ls-files -- <path>` — if tracked, it may be needed for builds
2. Check code references: `grep -rn "<path>" <source> --include="*.py" -l`
3. Trace the consumer: does it handle missing files gracefully? (e.g. `_desktop_packaged_executable` returns `None` → rebuilds on demand)
4. Report what you verified, not what you assumed

**Worked example (2026-07-02):** Claimed `apps/desktop/release/linux-unpacked/` (398MB) was safe to delete. Joe: "Are you sure, verify." Traced to `_desktop_packaged_executable()` in `hermes_cli/main.py` — only consumer, returns `None` when missing, triggers rebuild on demand. Confirmed then deleted.

## Pitfall: `hermes update` Quick State Snapshot Is NOT Configurable

`hermes update` creates TWO different backup mechanisms:

1. **ZIP backup** — gated by `updates.pre_update_backup` (default `false`). Controlled via `hermes update --backup` / `--no-backup`. Creates `<HERMES_HOME>/backups/pre-update-<timestamp>.zip`.

2. **Quick state snapshot** — ALWAYS created. No config flag. No CLI flag. `keep=1` so it replaces itself each update. Copies state.db, config.yaml, .env, auth.json, cron/jobs.json, and other critical files to `<HERMES_HOME>/state-snapshots/<timestamp>-pre-update/`. Can be 300MB+. The code is at `hermes_cli/main.py` line ~9455: `create_quick_snapshot(label="pre-update", keep=1)`.

**What this means:** Even with `updates.pre_update_backup: false`, every `hermes update` creates a ~329MB state snapshot. You can delete it after confirming the update is stable, but it comes back next update. There is no way to disable it without patching the source (which reverts on the next update). If disk space is tight, accept the constant 329MB footprint or patch + re-patch after each update.

## Update Workflow

```bash
hermes update
```

The updater syncs bundled skills from the repo into `~/.hermes/skills/`. It respects local modifications — if you've edited a bundled skill, it keeps your version and reports "~N user-modified (kept)."

**Post-update checks:**

1. **Dashboard WILL be killed — and systemd will NOT auto-restart it.** The updater sends SIGTERM to stop the dashboard (backend no longer matches updated frontend). The standard systemd service uses `Restart=on-failure` which only triggers on non-zero exit codes — clean SIGTERM produces exit 0, so the dashboard stays dead. **Always restart manually after `hermes update`:**

   ```bash
   systemctl --user restart hermes-dashboard   # if running as systemd service
   # OR
   hermes dashboard --host 127.0.0.1 --port 9119 --no-open --skip-build &   # manual fallback
   ```
   Verify: `ss -tlnp | grep 9119` should show LISTEN.

   **Permanent fix — change systemd to `Restart=always`:** The root cause is `Restart=on-failure` ignoring clean exits (SIGTERM = exit 0). One-line fix so this never happens again:

   ```bash
   sed -i 's/Restart=on-failure/Restart=always/' ~/.config/systemd/user/hermes-dashboard.service
   systemctl --user daemon-reload
   systemctl --user show hermes-dashboard -p Restart   # should output: Restart=always
   ```

   After this, the dashboard auto-recovers within 5 seconds of any update — no manual restart needed. The gateway already uses `Restart=always` by default; only the dashboard unit ships with `on-failure`.

   **Symptom if skipped:** The user sees a "channel 3 error" in the desktop app or web dashboard. This is the frontend trying to connect to a backend that doesn't exist. The "channel" is a WebSocket/SSE event channel — when the backend is dead, the frontend's channel subscription fails. The error text varies ("channel 3 error" is common) but the root cause is always: dashboard process not running after update.

   **Client-side fix:** Even after restarting the backend, the user's browser or desktop app may have cached the old frontend JS bundles (which reference stale channel numbers). Hard refresh: Ctrl+Shift+R (Cmd+Shift+R on Mac). For the Electron desktop app, if hard refresh doesn't work, open DevTools (Ctrl+Shift+I), check "Disable cache" in the Network tab, then reload.

2. **Gateway restarts automatically** — verify with `hermes gateway status`. The updater drains and restarts the gateway; messaging platforms will briefly disconnect and reconnect.

## Auto-Updating Hermes via Cron

To keep Hermes updated without manual intervention, schedule a periodic `hermes update` via cron:

```bash
# Example: weekly update every Sunday at 3 AM
hermes cron create auto-update-hermes "30 3 * * 0" "Run hermes update to pull latest Hermes Agent version and sync bundled skills. After the update completes, verify the dashboard is still running. If it was killed by the updater, restart it: hermes dashboard --host 127.0.0.1 --port 9119 --no-open --skip-build &"
```

The updater will kill the dashboard (SIGTERM, exit 0). If you've applied the permanent fix above (`Restart=always`), systemd auto-restarts it — no cron action needed beyond verifying it came back. If still on `Restart=on-failure`, the cron prompt MUST include a manual `systemctl --user restart hermes-dashboard`. The gateway restarts automatically either way.

## Gateway Troubleshooting

Common gateway platform issues — Telegram auth, pairing codes, WhatsApp pairing, restart stalls. See `references/gateway-troubleshooting.md` for quick fixes.

## Desktop App Auto-Update Failure (macOS)

**Symptom:** The desktop app's in-app "Update" button downloads the new version, says it will close and reopen, but the app remains on the old version after restart. Common on macOS when jumping a minor version (e.g., 0.15.0 → 0.16.0).

**Root cause:** The Electron auto-updater successfully downloads the new build but fails to replace the app bundle — typically a macOS permissions or file-lock issue. The CLI code IS updated; only the Electron wrapper is stale.

**Fix:** Rebuild the desktop app from the already-updated code:

```bash
hermes desktop --force-build
```

This rebuilds the Electron app against the current (already-updated) CLI code and launches the correct version. No need to re-run `hermes update` — the code is already there.

**If `hermes desktop --force-build` also fails:** The code may not have been pulled at all. Run `hermes update` from terminal first (not the in-app button) to get visible error output, then `hermes desktop --force-build`.

## Desktop Build on Headless / VPS

`hermes desktop --force-build` builds an Electron app, which requires a display server to *launch*. On a headless VPS, the build itself succeeds but the launch step fails with two errors.

**Pitfall — build artifacts survive on VPS.** `hermes update` may trigger a desktop build that leaves `apps/desktop/release/linux-unpacked/` (~400MB) and `apps/desktop/dist/` (~36MB) on disk. These are safe to delete — the CLI and gateway don't depend on them. Joe builds the desktop on his Windows machine, not the VPS. The `node_modules/` at project root (~422MB) are also desktop build deps only. See `references/disk-space-scouting.md` for the full audit checklist.

**Pitfall — legacy RAG venv.** A `/root/.hermes/rag-venv/` directory (~5GB) may exist from pre-native-RAG days. Hermes now has `session_search` (FTS5) and `vault-rag-first` skill. If no Python code in `/usr/local/lib/hermes-agent/` imports from it, safe to delete. Verify with: `grep -rn "rag.venv\|rag_venv" /usr/local/lib/hermes-agent/ --include="*.py" -l`

1. **Root sandbox block** — `Running as root without --no-sandbox is not supported`. Electron/Chromium refuses to run as root without `--no-sandbox`. The build artifact is at `apps/desktop/release/linux-unpacked/Hermes` and can be launched manually with `--no-sandbox`.

2. **Missing X server** — `Missing X server or $DISPLAY`. The VPS has no graphical environment. To actually display the app, install a virtual framebuffer (`apt install xvfb`) and launch with `xvfb-run .../Hermes --no-sandbox`, or forward X11 over SSH. For most headless use, the desktop app isn't needed — CLI and gateway cover everything.

**Version string discrepancy:** The desktop app's `apps/desktop/package.json` hardcodes a version string (e.g., `"0.15.1"`) that can lag behind the CLI version (e.g., `v0.16.0`) even when both are built from the same commit. Check the actual commit (`hermes --version` shows the upstream hash; `apps/desktop/build/install-stamp.json` shows what the desktop was built from). If the commits match, the code is current regardless of what the package.json says.

## Post-Update: Check User-Modified Skills

After every update that reports `user-modified (kept)`, investigate what was kept and why.

**Reliable method — hash comparison** (catches extra files, not just text diffs):

```python
import hashlib
from pathlib import Path

BUNDLED = Path.home() / ".hermes/hermes-agent/skills"
LOCAL = Path.home() / ".hermes/skills"

def dir_hash(base, rel):
    p = base / rel
    if not p.exists():
        return None
    h = hashlib.md5()
    for f in sorted(p.rglob("*")):
        if f.is_file():
            h.update(str(f.relative_to(p)).encode())
            h.update(f.read_bytes())
    return h.hexdigest()

# Find skills in manifest that exist locally but differ from bundled
manifest = {}
mp = LOCAL / ".bundled_manifest"
if mp.exists():
    for line in mp.read_text().splitlines():
        if ":" in line:
            n, _, h = line.strip().partition(":")
            manifest[n.strip()] = h.strip()

for name in sorted(manifest):
    # Resolve manifest key to directory path — check both flat and nested
    for root, dirs, _ in LOCAL.walk():
        for d in dirs:
            sp = Path(root) / d
            if (sp / "SKILL.md").exists():
                # Read frontmatter name
                fm = sp / "SKILL.md"
                first = fm.read_text().split("---")[1] if fm.read_text().startswith("---") else ""
                if f"name: {name}" in first:
                    local_h = dir_hash(LOCAL, sp.relative_to(LOCAL))
                    bundled_h = dir_hash(BUNDLED, sp.relative_to(LOCAL))
                    if local_h and bundled_h and local_h != bundled_h:
                        print(f"MISMATCH: {sp.relative_to(LOCAL)}")
                        print(f"  local:   {local_h}")
                        print(f"  bundled: {bundled_h}")
```

**Do NOT use `diff -rq` for this.** It reliably fails because bundled skills use nested directories (`research/polymarket`, `apple/notes`) while local skills may be flat or differently nested. `diff -rq` returned zero output in a session where `polymarket` was confirmed user-modified with extra files. The Python hash approach above is the only reliable method.

**Decision rule:** If the customization is already captured elsewhere (identity files, AGENTS.md, memory system, or should be its own standalone skill), strip the customization and let upstream flow through. If the customization is genuinely unique to your workflow and not redundant, keep it — but prefer extraction to a separate skill over permanent forking of a bundled skill.

## Resetting a User-Modified Skill to Stock

When a bundled skill has been locally modified and you want to discard the changes so upstream updates flow through clean:

```bash
rm -rf ~/.hermes/skills/<path/to/skill>
cp -r ~/.hermes/hermes-agent/skills/<path/to/skill> ~/.hermes/skills/<path/to/skill>
```

Then update the manifest hash to match the fresh copy so the updater no longer treats it as user-modified. Compute the new hash with `dir_hash()` (above) and replace the manifest entry. On next `hermes update`, the skill syncs clean.

## Pitfall: Customizing Bundled Skills With Redundant Content

**Don't** modify a bundled skill to add content that's already documented in:
- SOUL.md or USER.md (identity/personality)
- AGENTS.md (working protocols)
- MEMORY.md (core memory)
- Another dedicated skill

**Why:** Each modification blocks that skill from receiving upstream updates. Over months, the skill drifts from the maintained version and you miss improvements.

**Example:** The obsidian skill had a section about Paul's identity files and symlink setup. That content was already fully captured in SOUL.md, AGENTS.md, and the memory system. The customization blocked 10+ days of potential upstream improvements for zero functional gain.

**If the content is genuinely unique and should persist:** Create a separate skill for it rather than modifying the bundled one. Example: polymarket paper trader content should be its own `polymarket-paper-trader` skill, not bolted onto the bundled `polymarket` skill.

## System Prompt & Model Diagnostics

See `references/system-prompt-inspection.md` for:
- Tracing what Hermes sends to the model (SOUL vs. DEFAULT_AGENT_IDENTITY, guidance blocks, tier structure)
- OpenRouter model discovery (API query, filtering, alignment assessment)
- Model selection guide: which models have looser RLHF and higher autonomy ceiling

## Auditing for Dead Skills

When the user asks about unused or bloated skills, audit the full library.

**Before auditing, check which tools are actually functional.** A skill can be present, loaded, and appear valid while its underlying tool is broken or unauthenticated:

```bash
# Example: xurl was installed (which xurl → /home/.../bin/xurl) and its skill loaded,
# but `xurl whoami` returned 401 — never authenticated. Skill was dead weight.
xurl whoami 2>&1
```

This catches the case where a tool is installed but never configured, making its skill dead weight regardless of how relevant the domain is.

```bash
find ~/.hermes/skills -name SKILL.md | sort | while read f; do
  name=$(echo "$f" | sed 's|.*/skills/||; s|/SKILL.md||')
  desc=$(grep -m1 '^description:' "$f" | sed 's/description: *//')
  echo "$name|$desc"
done
```

Group into:
- **Core** — loaded nearly every session (e.g., bruiser-card-design-pipeline, creative-collaboration)
- **Situational** — loaded occasionally for specific tasks (e.g., github-*, software-development/*)
- **Dead weight** — never loaded, unrelated to the user's actual work (e.g., apple/* on WSL, mlops/* for a game dev, baoyu-* Chinese content tools)

Present the triage and let the user decide. Don't delete without confirmation.

## Permanently Removing Bundled Skills

Simply `rm -rf`-ing a bundled skill directory is not enough — the next `hermes update` will see the skill as "not in manifest, not on disk" and re-copy it from the bundled repo. The skill sync logic (`tools/skills_sync.py`) uses a manifest at `~/.hermes/skills/.bundled_manifest` to track which skills have been synced:

| Manifest state | Disk state | Updater behavior |
|---------------|-----------|-----------------|
| Not in manifest, not on disk | Missing | **Copies from bundled** (treats as new) |
| In manifest, on disk, hash matches origin | Present | Updates if bundled changed |
| In manifest, on disk, hash differs | Present | **Skips** (user-modified, kept) |
| In manifest, not on disk | Deleted | **Skips** (user-deleted, respected) |

**The pattern:** to permanently remove a bundled skill so it never returns on update:

1. **Read the manifest** at `~/.hermes/skills/.bundled_manifest` (format: `skill_name:origin_hash` per line)
2. **For each skill NOT in the manifest:** add it first. Read the skill's frontmatter `name:` field from its bundled `SKILL.md` to get the correct manifest key. Compute the origin hash from the bundled directory (MD5 of all file contents, same algorithm `_dir_hash()` uses).
3. **Delete the skill directories** from `~/.hermes/skills/`
4. **Write the updated manifest** back

On next `hermes update`, every deleted skill is "in manifest, not on disk" → updater skips it.

**Python reference** (for bulk deletion — adapt the `dead` list):

```python
import hashlib, shutil
from pathlib import Path

MANIFEST = Path.home() / ".hermes/skills/.bundled_manifest"
SKILLS_DIR = Path.home() / ".hermes/skills"
BUNDLED_DIR = Path.home() / ".hermes/hermes-agent/skills"

# Read manifest
manifest = {}
if MANIFEST.exists():
    for line in MANIFEST.read_text().splitlines():
        if ":" in line:
            name, _, h = line.strip().partition(":")
            manifest[name.strip()] = h.strip()

# For each dead skill, ensure manifest entry exists, then delete
for rel_path in dead_skill_paths:
    skill_path = SKILLS_DIR / rel_path
    name = read_frontmatter_name(skill_path / "SKILL.md")  # implement this
    
    if name not in manifest:
        bundled = BUNDLED_DIR / rel_path
        h = hashlib.md5()
        if bundled.exists():
            for fp in sorted(bundled.rglob("*")):
                if fp.is_file():
                    h.update(str(fp.relative_to(bundled)).encode())
                    h.update(fp.read_bytes())
        manifest[name] = h.hexdigest()
    
    shutil.rmtree(skill_path)

# Write manifest back
MANIFEST.write_text(
    "\n".join(f"{n}:{h}" for n, h in sorted(manifest.items())) + "\n"
)
```

**To undo** (re-add a previously deleted skill): `hermes skills reset <name>` clears the manifest entry so the next sync treats it as new and re-copies from bundled.
