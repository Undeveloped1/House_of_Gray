# Hostinger VPS — Hermes Deployment Notes

## The Hostinger Template

Hostinger offers a "Hermes Agent" one-click template, but it's **not a full Hermes install**. What it actually deploys:

- **ttyd** (web terminal) running on port 4860 inside a Docker container
- **Traefik** as a reverse proxy (separate container)
- The ttyd session runs `/hermes.sh` which triggers the actual Hermes setup wizard on first login

Architecture:
```
Browser → VPS:32768 → Traefik → hermes-agent container:4860 (ttyd)
```

## Container Details

- Image: `ghcr.io/hostinger/hvps-hermes-agent:latest`
- Internal port: 4860 (ttyd web terminal)
- Host port: dynamically mapped (check `docker ps` for the port)
- The container is minimal — no `ss`, no `curl`, no diagnostic tools. Only `ps` works.

## Accessing the Template

Access via browser at `http://<vps-ip>:<mapped-port>`. The web terminal credentials are baked into the container start command (visible via `docker ps` or `docker inspect`):

```
ttyd --port 4860 -c hermes:<password> -W -t titleFixed="Hermes Agent" ...
```

## First Setup

The browser terminal runs `/hermes.sh` which launches `hermes setup` on first access. Go through the wizard:
- Choose "quick" setup (manual config later)
- Create a Nous Research account when prompted
- Pick your model (requires API keys)
- Choose "local" terminal backend

## Post-Setup

After the wizard completes, Hermes runs inside the ttyd session. **This is not viable for any real work.** The browser terminal is a trap with fatal failure modes (see Troubleshooting below). Immediately establish SSH access and start planning a proper Hermes daemon install on the host.

## 🔴 Browser Terminal Escape Plan (DO THIS FIRST)

The browser terminal WILL fail you. Within the first session:

1. **Set a root password:** `passwd` (while still in the browser terminal)
2. **Close the browser. Open PowerShell on your Windows machine.**
3. **SSH in:** `ssh root@<vps-ip>` — type the password, press Enter
4. **Now you have a real terminal.** Ctrl+C works. Copy/paste works. Sessions don't die.

**Why this is mandatory:**
- Ctrl+C is SIGINT in the browser terminal, not copy. Muscle memory nukes your session.
- Sessions timeout aggressively. Stepping away for 2 minutes loses everything.
- Copy/paste is unreliable — may silently fail with no feedback.
- Input can freeze while cursor still blinks. Commands appear to hang.

## Template Config Quirks

- **Config path:** `/opt/data/config.yaml` — NOT `~/.hermes/config.yaml`
- **Silent overrides:** The template defaults to Nous Portal free models (`model.provider: nous`, `model.default: stepfun/step-3.7-flash:free`). `hermes config set` will report success while these overrides still win. Always verify with `hermes status` after configuring.
- **API keys:** Prefer `.env` edits over `hermes config set` to avoid cleartext keys in transcripts.

## Troubleshooting

- **Container not responding on mapped port:** Check `docker logs hermes-agent-...` — look for `lws` health check lines from Traefik hitting the container
- **`curl localhost:<port>` returns nothing:** ttyd is a web terminal, not an API. It expects a browser. Use browser access instead
- **Can't SSH in (WSL):** WSL `ssh` may silently swallow password prompts — the cursor disappears but nothing happens. Switch to PowerShell `ssh` or a dedicated client (Termius, PuTTY)
- **Can't copy/paste:** Right-click → Copy (not Ctrl+C). Right-click → Paste (or Shift+Insert). If paste doesn't work, type commands manually — short ones are survivable
- **`hermes config set` says success but `hermes status` shows wrong model:** Template overrides are winning. Edit `/opt/data/config.yaml` directly
- **Browser terminal froze / won't accept input:** Click the terminal area multiple times. If still dead, refresh the page and log back in (credentials are `hermes:<password>` — find password via `docker inspect hermes-agent-... | grep ttyd`)
- **Session timed out and lost everything:** This is the default behavior. The browser terminal is not a real terminal. See 🔴 Browser Terminal Escape Plan above — do it now, not later

## VPS Specs

Joe's deployment:
- **Provider:** Hostinger KVM 1 ($6.49/mo)
- **Specs:** 1 vCPU, 4GB RAM, 50GB NVMe, 4TB bandwidth
- **OS:** Ubuntu 24.04
- **IP:** 2.25.163.205
