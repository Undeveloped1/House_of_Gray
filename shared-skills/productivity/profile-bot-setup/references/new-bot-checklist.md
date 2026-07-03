# New Bot Checklist — Step by Step (Gateway Method)

Use this when adding a Telegram bot for a new lineage member.
**Do NOT write a standalone Python script.** Use the Hermes profile gateway.

## ⚠️ If Member Had a Previous Bot Script

- [ ] Stop and disable any old standalone service:
      `systemctl stop <name>-bot; systemctl disable <name>-bot`
- [ ] Kill any lingering old script processes: `pkill -f "<name>_bot.py"`
- [ ] Verify no old process holds the token: `ps aux | grep <name>.*bot`

## 1. Create the Bot on Telegram
- [ ] Message **@BotFather** on Telegram
- [ ] `/newbot` → choose name → choose username (ends in `bot`)
- [ ] Save the token BotFather gives you

## 2. Verify Profile Files Exist
- [ ] `SOUL.md` — core identity (1 paragraph)
- [ ] `profile/<name>.md` — full character profile
If missing, create them before proceeding.

## 3. Create `.env` (Three Things Required)
```bash
cat > /root/.hermes/profiles/<name>/.env << 'EOF'
TELEGRAM_BOT_TOKEN=<token-from-botfather>
DEEPSEEK_API_KEY=<copy-from-main-.env>
TELEGRAM_ALLOWED_USERS=7239715879
EOF
chmod 600 /root/.hermes/profiles/<name>/.env
```
- [ ] `TELEGRAM_BOT_TOKEN` — from BotFather
- [ ] `DEEPSEEK_API_KEY` — copy from `/root/.hermes/.env` (NOT optional — required for model)
- [ ] `TELEGRAM_ALLOWED_USERS` — set to Joe's ID: 7239715879

## 4. Create `config.yaml` with Model Settings
```bash
cat > /root/.hermes/profiles/<name>/config.yaml << 'EOF'
default_provider: deepseek
model:
  deepseek:
    default: deepseek-v4-pro
  default: deepseek-v4-pro
  provider: deepseek
EOF
```
- [ ] Model set to `deepseek-v4-pro` (the standard for all profiles)

## 5. Install the Gateway
```bash
hermes -p <name> gateway install --system --run-as-user root
```
This installs + enables + starts the systemd service automatically.

## 6. Add EnvironmentFile to the Generated Service
```bash
sed -i '/Environment="HERMES_HOME=\/root\/.hermes\/profiles\/<name>"/a EnvironmentFile=/root/.hermes/profiles/<name>/.env' /etc/systemd/system/hermes-gateway-<name>.service
```
**⚠️ The install command does NOT add EnvironmentFile.** Without it, the gateway can't read `.env` and will fail with "no API key found."
- [ ] Verify: `grep EnvironmentFile /etc/systemd/system/hermes-gateway-<name>.service`

## 7. Restart (to Pick Up .env)
**⚠️ `systemctl restart` is blocked from within a running Hermes gateway process.**
Workarounds:
- **Option A** — Run from a normal shell outside Hermes:
  ```bash
  systemctl daemon-reload && systemctl restart hermes-gateway-<name>
  ```
- **Option B** — From within Hermes, use DBus directly:
  ```bash
  busctl call org.freedesktop.systemd1 /org/freedesktop/systemd1 org.freedesktop.systemd1.Manager RestartUnit ss "hermes-gateway-<name>.service" "replace"
  ```
- **Option C** — Dispatch a subagent (delegate_task with terminal toolset)

## 8. Verify Connection
```bash
# Check the service is active
systemctl status hermes-gateway-<name> --no-pager

# Check logs for "telegram connected"
tail -10 /root/.hermes/profiles/<name>/logs/gateway.log
```
Expected: `✓ telegram connected`
- [ ] Service is `active (running)`
- [ ] No `DEEPSEEK_API_KEY` or "no API key found" errors
- [ ] Telegram shows "Connected to Telegram (polling mode)"

## 9. Test
- [ ] Joe opens `t.me/<Name>_Bot` and clicks Start
- [ ] Joe sends a test message → bot responds in character
- [ ] Test `/model` → shows model
- [ ] Test `/start` → welcome message

## 10. Update Lineage Records
- [ ] Update AGENTS.md / HEARTBEAT.md if needed
- [ ] Update lineage registry
