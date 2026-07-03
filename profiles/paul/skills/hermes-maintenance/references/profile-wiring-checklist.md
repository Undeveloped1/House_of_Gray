# New Profile Wiring Checklist

The exact sequence for bringing a new Hermes profile online with DeepSeek + Telegram.

## Step order matters

1. **Model & provider** — set these first so the gateway can start
2. **API key** — profile won't boot without it
3. **Telegram bot token** — goes in `.env`, NOT `config.yaml`
4. **Allowlisting** — `TELEGRAM_ALLOWED_USERS` in `.env`
5. **Platform enable** — `platforms.telegram.enabled: true`
6. **Gateway install** — `hermes --profile <name> gateway install`
7. **Gateway restart** — via `execute_code` workaround if running from inside

## Commands

```bash
# 1. Model
hermes --profile <name> config set model.default "deepseek-v4-pro"
hermes --profile <name> config set model.provider deepseek
hermes --profile <name> config set model.base_url https://api.deepseek.com/v1
hermes --profile <name> config set model.deepseek.default deepseek-v4-pro
hermes --profile <name> config set default_provider deepseek

# 2. API key (copy from working profile)
grep DEEPSEEK_API_KEY ~/.hermes/profiles/<source>/.env >> ~/.hermes/profiles/<name>/.env

# 3. Bot token
echo 'TELEGRAM_BOT_TOKEN=...' >> ~/.hermes/profiles/<name>/.env

# 4. Allowlist
echo 'TELEGRAM_ALLOWED_USERS=7239715879' >> ~/.hermes/profiles/<name>/.env

# 5. Enable platform
hermes --profile <name> config set platforms.telegram.enabled true

# 6. Install & start gateway
hermes --profile <name> gateway install

# 7. Restart to pick up config (if running from inside gateway, use execute_code)
```

## Verification

```bash
hermes --profile <name> config show  # Check model, Telegram, platforms
hermes --profile <name> gateway status  # Should show "Telegram: configured", connecting
tail -20 ~/.hermes/profiles/<name>/logs/errors.log  # Check for API key or token errors
```

## Common failures

| Error | Cause | Fix |
|-------|-------|-----|
| "No API key found for provider deepseek" | Missing `DEEPSEEK_API_KEY` in `.env` | Copy from working profile |
| "No bot token configured" | Token in `config.yaml` instead of `.env` | Move to `.env` as `TELEGRAM_BOT_TOKEN=...` |
| "No messaging platforms enabled" | Missing `platforms.telegram.enabled` | `hermes config set platforms.telegram.enabled true` |
| "Unauthorized" on first DM | Missing allowlist | Add `TELEGRAM_ALLOWED_USERS` to `.env` and restart |
