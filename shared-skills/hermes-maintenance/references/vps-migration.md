# VPS Migration — Hermes Agent

Reference for moving Hermes from a local desktop to a VPS, preserving all identity, memory, and skills.

## Decision logic

VPS wins over local transplant when:
- User travels and needs access from multiple machines
- User wants always-on (cron jobs, background work)
- Sync conflicts from two local copies are worse than SSH latency

Local transplant (MacBook) wins when:
- Short trip, single machine
- No VPS budget or provisioning time

## File sync: git is the answer

The Hermes vault lives inside the project repo (`docs/Paul/`). Code, lore, cards, Brain/, workspace — all in git. The only files outside git are Hermes runtime state:

```
~/.hermes/.env         # API keys
~/.hermes/config.yaml  # model/provider settings  
~/.hermes/skills/      # custom skills (bundled skills sync via `hermes update`)
```

Everything else travels with `git pull`.

## Phased migration plan

### Phase 1: Provision (30 min)

**Providers:**
- **Hostinger KVM 1** ($6.49/mo, 1 vCPU, 4GB RAM, 50GB NVMe) — cheapest viable option. Sufficient for Hermes + Docker + Postgres.
- **Hostinger KVM 2** ($8.99/mo, 2 vCPU, 8GB RAM, 100GB NVMe) — comfortable if colocating app DB and Docker.
- Hetzner CX22 (€4/mo, 2 vCPU, 4GB RAM) or CX32 (€6/mo, 4 vCPU, 8GB RAM)
- DigitalOcean ($6/mo droplet)

**Sizing note:** Hermes is a Python process calling APIs. 4GB RAM is plenty. If also running Docker + Postgres on the same box, 4GB still works for small DBs (<100MB). Bump to 8GB if colocating the app itself or the DB grows.

- Ubuntu 24.04 LTS
- Add SSH key at creation
- Install Tailscale during setup (user already has Tailscale)

### Phase 2a: Hostinger One-Click Hermes Template (if used)

Hostinger offers a "Hermes Agent" template in their VPS panel. This pre-deploys Hermes with Traefik as a reverse proxy. The install path differs from the manual `curl | bash` approach.

> **Key fact:** The Hostinger template is NOT a stock Hermes install. It's a **ttyd wrapper** — `ghcr.io/hostinger/hvps-hermes-agent:latest` runs `ttyd` (web terminal) on port 4860, which executes `/hermes.sh` (a setup wizard). Traefik proxies the web terminal. Your Hermes then runs inside that web terminal session — if the session dies (timeout, disconnect), Hermes dies with it. For production use, you'll want to install Hermes as a persistent daemon outside the ttyd wrapper.

- **Credentials:** Root password is NOT in email. Find it in the Hostinger VPS panel under the project → Manage → SSH access. Use "Reset password" if none is set.
- **Template config:** During deployment, it asks for ADMIN_USERNAME (default: `hermes`), ADMIN_PASSWORD (set a strong one), and optional API keys for Nexos/Oxylabs (skip both — you already have your own provider keys).
- **What it deploys:** Two containers: `hermes-agent-bxv0-hermes-agent-1` (ttyd on 4860) + `traefik-traefik-1` (reverse proxy). The Hermes container is NOT a stock Hermes install — it's a web terminal launcher.
- **Web terminal credentials:** Print the ttyd command to find them: `docker inspect hermes-agent-bxv0-hermes-agent-1 | grep ttyd`. The template uses `-c hermes:<password>` flags for basic auth. Access at `http://<vps-ip>:<mapped-port>` (port mapped from 4860, visible in `docker ps`).
- **Post-deployment:** Log into the web terminal, complete the Hermes setup wizard. Then configure your actual API keys and identity files.
- **Config path:** The Hostinger template stores Hermes config at `/opt/data/config.yaml` — NOT `~/.hermes/config.yaml`. The template overrides with Nous Portal free model defaults (`model.provider: nous`, `model.default: stepfun/step-3.7-flash:free`) regardless of what you configure during setup. Fix this by editing the YAML directly or using `hermes config set default_provider <provider>`.
- **API key configuration:** Prefer `.env` edits over `hermes config set` — the config command works but leaves cleartext keys in session transcripts (if the terminal logs sessions) and in Hermes' own conversation history. Direct `.env` edits (`echo "DEEPSEEK_API_KEY=sk-..." >> ~/.hermes/.env`) avoid transcript exposure. Joe explicitly prefers `.env` edits for API keys. Note: the Hostinger template's `.env` is at `/opt/data/.env` (mounted from host), not `~/.hermes/.env`. Verify the correct path with `docker exec <container> env | grep HERMES` or check the Docker Compose file.
- **The Hostinger "KVM 1" template deploys KVM 2.** Despite selecting the KVM 1 plan during purchase, the Hermes Agent template provisions a KVM 2 VPS (2 vCPU, 8GB RAM, 96GB disk). This is a Hostinger template behavior, not a billing error. More headroom than expected — good news for colocating Docker workloads.
- **Config path:** The Hostinger template stores Hermes config at `/opt/data/config.yaml` — NOT `~/.hermes/config.yaml`. The template overrides model/provider settings with Nous Portal free model defaults (`model.provider: nous`, `model.default: stepfun/step-3.7-flash:free`) regardless of what you configure during the setup wizard. After setup, verify with `hermes status` and fix the config file directly if the template defaults are still showing.
- **Config overrides are silent.** `hermes config set` will report success while the template's `/opt/data/config.yaml` still overrides with Nous defaults. The key won't show in `hermes status` until the config file at the template-specific path is fixed. Don't trust the success message — always verify with `hermes status`.
- **Do not bounce the user between terminals.** When the user is already in a working terminal (browser, WSL, PowerShell), give them commands for THAT terminal. Don't suggest switching to a different one unless the current one has failed. Multiple terminal suggestions in sequence ("try WSL", "no try PowerShell", "try the browser terminal") create confusion and frustration — the user loses track of which window they're in and what they were doing.
- **Container inspection:** The Hostinger image is minimal — `ss`, `netstat`, and other common tools are absent. Use `docker exec <container> ps aux` and `docker logs` for diagnostics. PID 1 is ttyd, not Hermes itself.
- **Browser terminal is a trap — ESCAPE IMMEDIATELY.** The Hostinger browser terminal has fatal failure modes that WILL cost you work:
  - **Ctrl+C is SIGINT, not copy.** It kills the current process or disconnects the session. This is the single most destructive UX trap — the user's muscle memory for copy will nuke their session. There is no keyboard shortcut for copy. Use right-click → Copy only.
  - **Idle timeout is aggressive.** Stepping away for 2 minutes can kill the session and lose all work in progress. Hermes running inside ttyd dies with the ttyd session.
  - **Input can silently fail.** The terminal sometimes accepts no keystrokes even with a visible cursor. Clicking into the terminal area multiple times may regain focus. If a command produces no output at all after pressing Enter, the terminal is probably dead — refresh the page.
  - **Copy/paste is unreliable.** The browser terminal may not accept pasted text. When it does, SSH password prompts show no visual feedback (no dots, no characters) — paste and trust Enter.
  - **FIRST THING TO DO on any Hostinger VPS:** Set a root password (`passwd`) or add an SSH key, then immediately switch to a real SSH client. PowerShell `ssh root@<ip>` works reliably on Windows. WSL `ssh` may silently swallow password prompts — use PowerShell if WSL hangs. A dedicated client (Termius, PuTTY) is more reliable than either. Once on proper SSH, Ctrl+C works normally, copy/paste works normally, and sessions don't timeout-kill your work.
- **SSH key setup pitfall:** The web terminal's copy/paste unreliability makes SSH key setup error-prone. If the user is struggling with key files, fall back to `passwd` — set a simple password on the VPS, then SSH in with password auth from a proper terminal. You can set up keys later from a real SSH session.
- **Docker access:** The template VPS has Docker pre-installed. Colocating your app containers (Postgres, TCG app) works — the VPS is a standard Ubuntu box underneath.

```bash
# Official one-command installer — handles deps, env, setup wizard
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash

# Follow the setup wizard. It prompts for:
#   - API keys (OpenRouter, Anthropic, etc.)
#   - Gateway connections (Telegram recommended for remote access)
#   - Model selection

# Copy custom config from local machine
scp ~/.hermes/config.yaml vps:~/.hermes/
scp ~/.hermes/.env vps:~/.hermes/
scp -r ~/.hermes/skills/ vps:~/.hermes/skills/

# Clone the project repo
git clone <repo-url> tcg_engine/

# Pull bundled skills
hermes update
```

### Phase 3: Verify (15 min)

- SSH in via Tailscale IP (not public IP — Tailscale gives stable address)
- `tmux new -s hermes` so session persists across disconnects
- Start Hermes, confirm SOUL + memory loaded
- `git pull` inside `tcg_engine/`, confirm read/write to `docs/Paul/`

### Phase 4: Client setup (any time before travel)

- Install Tailscale on MacBook
- `ssh user@vps-tailscale-ip`
- `tmux attach -t hermes`

## Post-migration architecture (confirmed 2026-06-02)

Paul runs natively on the VPS (no Docker, no tmux wrapper — direct `hermes` install). Identity files are symlinked from `~/.hermes/` into the git-tracked repo:

```
~/.hermes/SOUL.md               → tcg-engine/docs/Paul/_identity/SOUL.md
~/.hermes/AGENTS.md             → tcg-engine/docs/Paul/Brain/AGENTS.md
~/.hermes/memories/MEMORY.md    → tcg-engine/docs/Paul/memories/MEMORY.md
~/.hermes/memories/USER.md      → tcg-engine/docs/Paul/_identity/USER.md
```

Hermes workdir: `tcg-engine/` repo root. Paul writes to `docs/Paul/` — changes are immediately in the git working tree.

## Git workflow (post-migration)

Local Paul is dead. The VPS is Paul's only home. Joe codes the game locally but Paul lives on the VPS.

| Machine | Role | Owns |
|---------|------|------|
| PC/MacBook (Cursor) | Code, game design | Everything except `docs/Paul/` |
| VPS (Paul) | Identity, memory, design research | `docs/Paul/` only |

**Cycle:**
1. Before work: `git pull` on both machines
2. During work: each edits their own territory
3. Paul commits and pushes his own changes from VPS (`docs/Paul/` only)
4. Joe commits and pushes code changes from local
5. Both machines `git pull` to stay synced

**Conflict resolution:** If local changes on VPS conflict with remote (Joe pushed Paul updates from another machine), stash local noise and pull — remote is authoritative for Paul files. The stash can be inspected and dropped if it's just migration artifacts or permission noise.

## Pitfalls

- **Don't run two Hermes instances** against the same vault simultaneously. They diverge. One VPS = one Paul.
- **Commit before switching.** Uncommitted work on PC isn't visible to VPS Paul.
- **Tailscale, not public IP.** SSH over Tailscale is encrypted, stable, and doesn't expose Hermes to the internet.
- **tmux, not screen.** User specifically mentioned tmux. Session persists when SSH drops.
- **SSH key on NTFS through WSL fails with "bad permissions."** Files on `/mnt/c/` (Windows drive) don't respect Linux `chmod`. When generating or storing SSH keys for VPS access, create them in the WSL home directory (`~/.ssh/`) and `chmod 600` there. Paths like `/mnt/c/Users/TheGreyBeard/.ssh/key` will always report 0777 to SSH and be rejected. If keys must be shared with Windows apps, copy FROM WSL to Windows, not the other way.
- **`hermes chat -m "prompt"` doesn't work like a one-shot query.** It launches the TUI, prints the welcome screen, and exits immediately with "Goodbye!" when stdin is not a terminal. For a quick test, use the interactive chat (`hermes chat`) or verify via `hermes status`. Do not rely on `hermes chat -m` for scripted verification.
- **Never take unilateral action on user infrastructure.** Do not use SSH keys, credentials, or access methods to connect to the user's VPS, cloud accounts, or services without explicit permission. Generating a key pair for the user is fine — but do not use that key yourself to probe, test, or inspect their server. The VPS is theirs, not shared infrastructure. Ask before connecting.

## Colocating Docker + Postgres

Hostinger KVM plans include a Docker manager. The same VPS can run Hermes + Docker containers (Postgres, the TCG app) simultaneously. 4GB RAM is sufficient for small databases.

**Accessing Docker from local Cursor:**

Set `DOCKER_HOST=ssh://user@vps` locally. All `docker` commands route over SSH transparently. No open ports, no TLS certs — SSH handles auth.

```bash
# Local .bashrc or .zshrc
export DOCKER_HOST=ssh://user@vps-tailscale-ip
```

Cursor picks this up and talks to the remote Docker daemon as if local.

**DB access pattern:**

```bash
# Tunnel the DB port locally — client connects to localhost:5432 as before
ssh -L 5432:localhost:5432 user@vps
```

Update the app's `.env` connection string to `localhost:5432` — it never knows the DB is remote.

**Migration steps:**
1. `pg_dump` local DB → `scp` dump to VPS
2. Spin up Postgres container on VPS (same docker-compose as local)
3. `pg_restore` into remote container
4. Update local `.env` to point at tunneled port
5. Kill local Docker Postgres container — reclaim that RAM
