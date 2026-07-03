---
name: paul-vps-operations
description: Set up, maintain, and troubleshoot Paul's VPS infrastructure — dashboard, git backup, file boundaries, Hermes config.
version: 1.0.0
---

# Paul VPS Operations

Paul runs on Hostinger KVM 2 (2.25.163.205) as root. This skill covers infrastructure tasks specific to Paul's environment.

## Dashboard Access

The Hermes dashboard runs on port 9119 bound to 127.0.0.1. Never expose it publicly. It is managed as a **systemd user service** — auto-starts on boot, auto-restarts on crash.

### Service management

```
systemctl --user status hermes-dashboard     # check if running
systemctl --user start hermes-dashboard      # start it
systemctl --user restart hermes-dashboard    # restart after config changes
systemctl --user stop hermes-dashboard       # stop it
```

Service file lives at `/root/.config/systemd/user/hermes-dashboard.service`. It was created 2026-06-07 to replace ad-hoc manual launches.

### Dependencies

Dashboard requires `fastapi` and `uvicorn[standard]` in the Hermes venv. If missing after a migration or fresh install:

```bash
/usr/local/lib/hermes-agent/venv/bin/python -m ensurepip
/usr/local/lib/hermes-agent/venv/bin/pip install fastapi 'uvicorn[standard]'
```

The Hermes venv at `/usr/local/lib/hermes-agent/venv/` ships without pip — `ensurepip` bootstraps it.

### SSH tunnel (Joe's machines)

Joe's `~/.ssh/config` has `LocalForward 9119 localhost:9119` under `Host paul`, so `ssh paul` auto-forwards the dashboard. Then `http://localhost:9119` in browser, or Hermes Desktop → Remote → `http://localhost:9119`.

### Manual fallback (if systemd service won't start)

```bash
hermes dashboard --port 9119 --host 127.0.0.1 --no-open --skip-build
```
Use `--skip-build` on VPS (npm not available). Launch via `terminal(background=true)` for long-running.

## Hermes File Auto-Discovery Architecture

Three different mechanisms load three different files at boot. Understanding this prevents context-burn from wrong assumptions about how files reach the system prompt.

### SOUL.md — native Hermes identity

- **What:** Paul's personality, voice, purpose, relationship with Joe
- **Where:** `~/.hermes/SOUL.md`
- **How:** Hermes natively looks for this file and injects it as the system prompt. No config directive needed. Not project context — this IS the agent's identity.
- **Symlink?** No. Direct copy at `~/.hermes/SOUL.md`. The vault's `_identity/SOUL.md` is a vestigial copy from the Obsidian era — not what loads.

### USER.md — native Hermes user profile

- **What:** Joe's portrait — background, preferences, creative fingerprint
- **Where:** `~/.hermes/USER.md`
- **How:** Hermes natively looks for this file when `memory.user_profile_enabled: true` (set in `config.yaml`). Auto-injects as USER PROFILE section. `memory.user_char_limit` caps injection size (currently 1375 chars on VPS).
- **Status on VPS:** `~/.hermes/USER.md` deployed 2026-06-06 as part of v2 architecture migration. User profile is now injected natively.
- **Vault copy:** `_identity/USER.md` was the vault's portrait (pre-v2). Now archived at `_identity_ARCHIVED/USER.md` as of 2026-06-06 migration. `~/.hermes/USER.md` is the single source of truth.

### AGENTS.md — project context (NOT native Hermes)

- **What:** Operational protocols — memory system, DREAM markers, compression triggers, file boundaries
- **Where:** `/root/AGENTS.md` → symlink to `~/.hermes/AGENTS.md`
- **How:** Hermes scans the **working directory** (`/root`) for `AGENTS.md`, `CLAUDE.md`, or `.cursorrules` and injects whatever it finds as **project context**. This is a Cursor/Claude ecosystem convention Hermes adopted — NOT the same mechanism as SOUL/USER identity loading.
- **No config directive needed.** The symlink at `/root/AGENTS.md` is the entire mechanism. If the symlink breaks, AGENTS.md stops loading — Hermes will NOT look for it at `~/.hermes/`.
- **The `~/.hermes/AGENTS.md` file** is the canonical source. The symlink just makes it visible from the workdir.

### MEMORY — memory system injection

- **What:** Durable facts saved via `memory()` tool
- **How:** Injected when `memory.memory_enabled: true`. Capped at `memory.memory_char_limit` (10k chars on VPS). NOT a file — populated through tool calls.

### Summary table

| File | Mechanism | Location | Config flag |
|------|-----------|----------|-------------|
| SOUL.md | Native identity | `~/.hermes/SOUL.md` | None (always on) |
| USER.md | Native user profile | `~/.hermes/USER.md` | `memory.user_profile_enabled` |
| AGENTS.md | Project context | `/root/AGENTS.md` (symlink) | None (workdir scan) |
| MEMORY | Tool-populated | N/A (memory DB) | `memory.memory_enabled` |

### v2 Architecture Migration (2026-06-06)

What changed and what was removed:

| Artifact | Status | Replacement |
|----------|--------|-------------|
| HERMES_BOOT.md | **Deleted** | AGENTS v2 Session Start Protocol handles Daily Handover, git pull, memory review |
| VAULT_MAP.md | **Deleted** | Project navigation → `five-crests` scope skill (loaded on trigger) |
| Brain/AGENTS.md mirror | **Deleted** | Was a stale copy; `~/.hermes/AGENTS.md` is the single source |
| `_identity/` | **Archived** → `_identity_ARCHIVED/` | Identity files now live natively at `~/.hermes/` |
| Scope skill | **Installed** | `skills/project-scopes/five-crests/SKILL.md` — load when Joe says "working on Five Crests" |
| USER.md | **Created** | `~/.hermes/USER.md` — was missing entirely on VPS pre-v2 |

What stayed the same: config.yaml, symlink at `/root/AGENTS.md`, workdir at `/root`, skills directory, memory entries, vault paths, read-only repo, Syncthing dropbox.

Boot is now: SOUL (native identity) + USER (native user profile) + AGENTS v2 (project context via symlink). No manual boot checklist. Scope documents loaded on demand.

### Troubleshooting

**AGENTS.md not injecting at session start:** Verify `/root/AGENTS.md` exists. If missing: `ln -s /root/.hermes/AGENTS.md /root/AGENTS.md`. Confirm workdir is `/root` (`pwd`).

**USER.md not injecting:** Check `grep user_profile_enabled /root/.hermes/config.yaml`. If true, verify `~/.hermes/USER.md` exists. If missing, create it. Check `user_char_limit` — content beyond this cap is truncated.

**SOUL.md not injecting:** Verify `~/.hermes/SOUL.md` exists and is readable. Hermes loads this unconditionally — if it's missing, Paul has no identity.

## Git Backup

Paul's vault at `/root/.hermes/docs/Paul/` is backed up to a private GitHub repo.

**Setup pattern:**
1. Generate SSH key: `ssh-keygen -t ed25519 -f /root/.ssh/paul_vps -N "" -C "paul-vps-deploy"`
2. Add as deploy key to repo via GitHub UI or API (`gh api -X POST /repos/OWNER/REPO/keys ...`)
3. Configure repo: `git config core.sshCommand "ssh -i /root/.ssh/paul_vps -o StrictHostKeyChecking=accept-new"`
4. Push: standard `git push`

**PAT warning:** GitHub fine-grained PATs do NOT work for `git push` over HTTPS, even with admin permissions. They work for API calls only. Always use SSH deploy keys for git operations.

## File System Boundaries

Paul's vault: `/root/.hermes/docs/Paul/` — all Paul's working files.

tcg-engine repo: `/root/tcg-engine/` — read-only reference. Only writable path is `docs/Paul_Handoff/incoming/` (Cursor's designated handoff lane).

Syncthing dropbox: `/root/syncthing/paul-dropbox/` — alternative handoff path that doesn't touch the repo.

Identity files: `~/.hermes/SOUL.md` and `~/.hermes/AGENTS.md` are standalone copies (not symlinks). Hermes injects SOUL automatically; AGENTS loads from working directory symlink.

**Vault identity folder:** `/root/.hermes/docs/Paul/_identity_ARCHIVED/` — legacy identity folder, archived 2026-06-06 during v2 architecture migration. The `_identity/` folder held SOUL.md and USER.md from the Obsidian-vault era. After v2, all identity files load natively from `~/.hermes/` — SOUL.md, USER.md, AGENTS.md. The archived folder is preserved for history but is not active.

## Hermes Config Notes

- `hermes config set` leaves cleartext keys in session transcripts — Joe prefers editing `.env` directly
- SSH config: `Host paul` alias with Tailscale IP (100.94.19.72), id_ed25519_tailscale key
- Gateway runs as systemd user service — survives logout

### Provider Configuration Pitfall: `default_provider` ≠ `model.provider`

**The trap:** Setting `default_provider: deepseek` does NOT mean model requests go through DeepSeek. `model.provider` is what actually routes model requests. If `model.provider: nous` (or any other value), that wins.

**Checking what's actually in use:**

```bash
grep -E 'default_provider:|model:' ~/.hermes/config.yaml | head -5
grep 'provider:' ~/.hermes/config.yaml | grep -v 'auto\|cloud_provider\|memory\|stt\|tts\|delegation\|auxiliary'
```

Then read the config block around `model:` — the `provider:` under `model:` is the one that matters for routing.

**Fix when they diverge:**

```bash
hermes config set model.provider deepseek   # or the desired provider
```

**Verification:** The `.env` must have the matching API key (e.g., `DEEPSEEK_API_KEY`). The change takes effect on next session (`/reset` or new Hermes process).

**Root cause pattern:** `default_provider` sets the default for CLI commands (`hermes chat`), but the `model:` block's `provider:` field overrides it for actual model API routing. If you changed `default_provider` but never checked the `model:` block, you're on the old provider.

**This session (2026-06-06):** `default_provider: deepseek` was set but `model.provider: nous` routed everything through Nous gateway. `DEEPSEEK_API_KEY` was in `.env` unused. Fixed with `hermes config set model.provider deepseek`.

## Hermes Desktop Artifacts Tab

The Hermes Desktop app has an Artifacts sidebar tab that auto-discovers outputs from past sessions. Understanding how it works changes how Paul should structure creative deliverables.

### How the scanner works

On load, the artifacts tab scans the 30 most recent sessions and extracts from assistant/tool messages:
- **Images** — URLs with image extensions (`.png`, `.jpg`, `.webp`, `.svg`, `.gif`), `data:image/` embeds
- **Files** — absolute paths (`/root/...`), relative paths (`./output.html`), home paths (`~/...`) ending in recognized extensions
- **Links** — any URL that doesn't match the image pattern

It regex-matches markdown image syntax, markdown links, bare URLs, and file paths. It also scans JSON tool output for path-like values (keys matching `path|file|url|image|artifact|output|download|result|target`).

### Leveraging it for creative output delivery

When Paul generates visual/interactive output (card renderers, Bible explorers, combat sims) and saves them to the Syncthing dropbox, those files **automatically appear in Joe's artifacts tab** — no manual bookmarking needed. The scanner picks up the file path from Paul's messages.

**Key practice:** When Paul produces a deliverable file, explicitly state the full path and/or open it so the path appears in the message stream. The artifacts tab scrapes assistant messages — if Paul mentions a path, it gets discovered.

**What this is NOT:**
- NOT Claude's inline interactive artifact system (live rendering with versioning in-chat)
- NOT a real-time file watcher — it scans existing session history on tab load
- NOT a code execution environment — it opens files in the OS default handler

**Complementary to Claude artifacts:** Claude handles live interactive iteration during design. Hermes artifacts handle persistent, session-spanning output discovery. They're different layers.

### Artifact gallery for batch card review

When Paul batch-generates card images (e.g., 30 Trigger card renders) saved as individual files, the image tab becomes a gallery. Joe filters by "image," browses the grid, clicks to open.

- **Docker port exposure bypassing UFW** — Docker iptables rules override UFW. Audit, fix, and lock down.
- **Perimeter sweep response protocol** — responding to security sentry (Shiva) reports: validate findings, answer questions, add watchlist items, flag misses, escalate destructive actions to Joe. See `references/perimeter-sweep-response.md`.
- **Dead service cleanup** — identify and remove unused system services (atd, cups, ModemManager) found by perimeter sweeps. Verification-then-kill pattern in `references/perimeter-sweep-response.md`.

## Docker Port Exposure (Docker Bypasses UFW)

Docker adds its own iptables rules that override UFW. When a docker-compose binds `4000:4000` (without a specific IP), Docker binds to `0.0.0.0` — all interfaces, including the public ethernet. UFW's `default deny incoming` is ignored for these ports.

**Audit exposed ports:**
```bash
ss -tlnp | grep -v '127.0.0.1'
```
Look for Docker-proxy entries on `0.0.0.0` — those are publicly reachable.

**Fix: Bind to Tailscale IP only in docker-compose:**
```yaml
# Before (exposed to 0.0.0.0):
ports:
  - "4000:4000"

# After (Tailscale-only):
ports:
  - "100.94.19.72:4000:4000"
```
Or strip the port entirely with `!reset []` if it should be internal Docker network only.

**After fix:** `docker compose -f docker-compose.yml -f docker-compose.vps.yml up -d` then re-audit with `ss -tlnp | grep -E ':4000|:5432'`.

**Lesson from 2026-06-04:** Postgres (5432) and the game app (4000) were both exposed to the public internet despite UFW being active. The VPS overlay correctly stripped Postgres but the app port was still `4000:4000` (unbound). Joe: "Lock those fucking ports down right now."

## Headless Browser Auth (Playwright Remote Debugging)

When a web service needs browser-based authentication on the VPS (X/Twitter, Google, etc.), use Playwright Chromium with remote debugging. Full guide: `references/headless-browser-auth.md`.

Quick launch:
```bash
/root/.x-profile/start_chrome.sh  # already exists, persistent profile at /root/.x-profile/
```

Joe tunnels in then authenticates — see `references/headless-browser-auth.md` for both Chrome (`chrome://inspect`) and Brave (`http://localhost:9222`) flows.

## Automatic Updates (unattended-upgrades)

The VPS runs `unattended-upgrades` which handles security updates daily. By default it only pulls from the `-security` pocket — non-security updates (`-updates`) and third-party repos (Docker) are skipped.

### Checking current state

```bash
systemctl status unattended-upgrades
cat /var/log/unattended-upgrades/unattended-upgrades.log | tail -20
apt list --upgradable 2>/dev/null
```

The MOTD nags about pending updates in three categories:
- **"X updates can be applied immediately"** — non-security `-updates` pocket (commented out by default)
- **"Y additional security updates can be applied with ESM Apps"** — requires Ubuntu Pro (free, up to 5 machines)
- **"Z updates could not be installed automatically"** — held back because origin isn't allowed (usually `-updates` or third-party)

### Enabling non-security updates

Uncomment the `-updates` line in `/etc/apt/apt.conf.d/50unattended-upgrades`:

```bash
sudo sed -i 's|^//\t"\${distro_id}:\${distro_codename}-updates";|"\${distro_id}:\${distro_codename}-updates";|' /etc/apt/apt.conf.d/50unattended-upgrades
```

### Adding third-party repos (Docker)

Docker's origin is `Docker:noble`. Add it after the ESM line:

```bash
sudo sed -i '/ESM.*infra-security";/a \t"Docker:${distro_codename}";' /etc/apt/apt.conf.d/50unattended-upgrades
```

Verify origin before adding: `curl -s https://download.docker.com/linux/ubuntu/dists/noble/Release | grep -E '^(Origin|Suite):'`

### Dry-run after config changes

```bash
sudo unattended-upgrades --dry-run --debug
```

### Pitfall: Hermes blocks /etc edits

The Hermes terminal tool refuses to modify files under `/etc` (system file guard). The `patch` tool also blocks writes to `/etc`. Workaround: give Joe the commands to run himself. Do not try `cp` to `/tmp` as a bypass — that's also blocked.

## SSH Tunnel Access (Joe's Machines)

Full guide: `references/ssh-tunnel-guide.md`. Covers: active services & ports table, Joe's SSH config, adding new LocalForward entries, WSL terminal pitfalls (heredocs break — use individual `echo` commands), `sed` append patterns for SSH config, macOS BSD sed caveats, and Joe's communication preference for technical instructions ("treat me like a small child").

## Syncthing File Sync

Full guide: `references/syncthing-setup.md`. Covers: install, systemd user service, headless API configuration (add devices, create folders, check status), pairing flow between VPS and Joe's local machine, critical Folder ID matching pitfall (IDs must match, not labels), common pitfalls, and verification steps.

The active Syncthing dropbox is at `/root/syncthing/paul-dropbox/` — files dropped here appear on Joe's machine.

## Vault Migration History

Full history: `references/vault-migration-2026-06-03.md`. Documents the transition from Obsidian-vault era identity files to native Hermes identity loading.

## Pitfall: Systemctl Is Not the Whole Story

`systemctl is-active` / `systemctl status` can report "inactive (dead)" for a service that IS running — if it was started directly (not via systemd). Syncthing on this VPS runs as a raw process (`/usr/bin/syncthing --no-browser --no-restart`), not as a systemd unit. Systemctl will always say "inactive" for it.

**Rule:** When checking if something is running, use BOTH:
```bash
systemctl is-active <service> 2>/dev/null    # catches systemd-managed
ps aux | grep -i <name> | grep -v grep        # catches raw processes
```

Never conclude "X is not running" from systemctl alone.

## Troubleshooting

**Dashboard not loading:** Check service: `systemctl --user status hermes-dashboard`. Check port: `ss -tlnp | grep 9119`. If service is active but port isn't listening, restart: `systemctl --user restart hermes-dashboard`. Manual fallback: `hermes dashboard --port 9119 --host 127.0.0.1 --no-open --skip-build`.

**Dashboard crashes (exit -9):** Likely OOM. Check `dmesg | tail -20` for OOM killer logs. VPS has 8GB. Systemd auto-restarts on failure, but repeated OOM kills indicate a memory leak or overload.

**"channel 3: open failed: connect failed: Connection refused" on `ssh paul`:** The SSH tunnel is up but the dashboard isn't listening on 9119 on the VPS side. Check `systemctl --user status hermes-dashboard` — if inactive or failed, `systemctl --user restart hermes-dashboard`. This error means the tunnel found the SSH server but the forwarded port had nothing to accept it.

**Git push failing with 403:** Check if using PAT instead of SSH deploy key. Switch to SSH: `git remote set-url origin git@github.com:OWNER/REPO.git`.

**AGENTS.md not injecting at session start:** Verify `/root/AGENTS.md` exists. If missing: `ln -s /root/.hermes/AGENTS.md /root/AGENTS.md`.
