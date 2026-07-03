# Gateway Troubleshooting

Common issues when setting up a profile Telegram gateway.

## "Telegram bot token already in use (PID X)"

**Meaning:** The gateway tried to claim the bot token's scoped lock, but
found PID X already holds it. Hermes prevents two gateway processes from
polling the same bot.

**Causes:**

1. **Old standalone script still running.** If the profile previously had
   a `hans_bot.py` or similar standalone script, it's still polling the
   token. Kill it and disable its service.
   ```bash
   systemctl stop <name>-bot        # If it has an old service
   systemctl disable <name>-bot
   pkill -f "<name>_bot.py"         # Kill any leftover processes
   systemctl restart hermes-gateway-<name>
   ```

2. **Wrong `.env` file.** The gateway reads `$HERMES_HOME/.env`. If
   `HERMES_HOME=/root/.hermes/profiles/<name>`, it reads
   `/root/.hermes/profiles/<name>/.env`. If that file has the wrong token
   (or the main profile's token), it will conflict with the main gateway.
   ```bash
   cat /root/.hermes/profiles/<name>/.env  # Verify token
   ```
   Check against the token from @BotFather.

3. **Missing EnvironmentFile.** Without `EnvironmentFile=` in the systemd
   service, the gateway may fall back to the wrong token. Add:
   ```ini
   EnvironmentFile=/root/.hermes/profiles/<name>/.env
   ```
   to `/etc/systemd/system/hermes-gateway-<name>.service` under `[Service]`,
   then:
   ```bash
   systemctl daemon-reload
   systemctl restart hermes-gateway-<name>
   ```

4. **Stale gateway state.** If the gateway crashed and was killed hard,
   its scoped lock file may persist. Lock files live at:
   `~/.local/state/hermes/gateway-locks/telegram-bot-token-*.lock`
   Restarting the service should auto-resolve (systemd sends SIGTERM first).

## "Gateway already running (PID X)"

**Meaning:** The systemd service can't start because a direct-run gateway
process is still alive. This happens when migrating the default profile
or any profile whose gateway was started manually (not via systemd).

**Symptoms:**
- `systemctl status` shows `activating (auto-restart)` with exit code 1
- Journal shows: "Gateway already running (PID X)"
- `ps -p <PID>` confirms the process is still alive

**Fix:**
```bash
# First try SIGTERM
kill <PID>
sleep 1
ps -p <PID> && echo "Still alive — escalate to SIGKILL"

# SIGTERM often fails on a busy gateway — use SIGKILL
kill -9 <PID>
sleep 2
systemctl status hermes-gateway    # Should be active (running)
```

**Important:** `kill -9` is immediate — the old conversation drops instantly.
If you're running commands from within that gateway's session, use a cron
job or subagent to execute the kill, so the old gateway finishes delivering
your final message before dying.

## Gateway Starts Then Exits (status=1/FAILURE)

**Meaning:** The gateway process started but exited quickly with an error.

**Check:**
```bash
journalctl -u hermes-gateway-<name> -n 30 --no-pager
```
Common causes:
- **No `.env` file** — gateway starts but Telegram can't find a token
- **Corrupted `.env`** — file has garbage content. Rewrite it fresh
- **Token already in use** — see above
- **"Gateway already running"** — see above (stale direct process)

## "Chat not found" Errors After Bot Swap

**Meaning:** The new bot is connected and polling, but can't send messages
to Joe's chat ID. Log shows:
```
ERROR [Telegram] Failed to send Telegram message: Chat not found
```

**Cause:** The new bot has never received a message from Joe. Telegram bots
can only send messages to users who have initiated a conversation. Until
Joe sends the first message, `chat_id=7239715879` doesn't exist for this bot.

**Fix:** Joe must open the new bot (**t.me/<BotName>**) and send any message
("hello" is enough). Once the chat is established, the gateway can respond.

**Note:** The old bot still works for the existing conversation. This is
expected — the old gateway process (if still alive) serves the old bot,
while the new gateway waits for the new bot's first message.

## "No user allowlists configured" Warning

This is normal for a first-time setup. The gateway runs with
deny-by-default. To allow your Telegram ID:
```bash
echo "TELEGRAM_ALLOWED_USERS=<your-telegram-id>" >> /root/.hermes/profiles/<name>/.env
systemctl restart hermes-gateway-<name>
```

## Gateway Shows "connected" But Bot Doesn't Respond

- Check that `allowed_chats` in the profile's config.yaml includes your
  Telegram user ID or is empty (allows all)
- Check the profile has a `SOUL.md` — without a soul, the agent has no
  identity and may respond generically or not at all
- Check journal for "inbound message" entries to confirm Telegram is
  delivering messages to the gateway
- If this is a brand-new bot, the user must send the first message
  (see "Chat not found" above)

## "401: Authentication Fails" (DeepSeek API key invalid)

**Symptom:** Bot connects to Telegram but every message gets a generic error
response. Agent log shows:
```
HTTP 401: Authentication Fails, Your api key: ****7a5c is invalid
```

**Cause:** The profile's `.env` has a wrong, expired, or redacted DeepSeek
API key. This usually happens when the key was typed manually from a
redacted tool output (Hermes masks keys as `sk-2a9...7a5c`).

**Fix:**
```bash
# Copy the real key from the main .env
DEEPSEEK_KEY=$(grep '^DEEPSEEK_API_KEY=' /root/.hermes/.env | head -1)
sed -i "s|^DEEPSEEK_API_KEY=.*|${DEEPSEEK_KEY}|" /root/.hermes/profiles/<name>/.env

# Restart
systemctl daemon-reload && systemctl restart hermes-gateway-<name>
```

## Duplicate `.env` Entries

**Symptom:** Gateway behaves inconsistently — sometimes works, sometimes
fails. Or uses the wrong credentials.

**Cause:** `.env` was built by appending (`>>`) to an existing file,
creating duplicate entries like:
```
DEEPSEEK_API_KEY=sk-real-abc123
DEEPSEEK_API_KEY=sk-old-xyz789   # <-- stale duplicate
TELEGRAM_BOT_TOKEN=bot1
TELEGRAM_BOT_TOKEN=bot2          # <-- conflict!
```

**Fix:**
```bash
# Check for duplicates
wc -l /root/.hermes/profiles/<name>/.env  # Should be exactly 3
grep -c 'DEEPSEEK_API_KEY' /root/.hermes/profiles/<name>/.env  # Should be 1

# Rewrite clean
DEEPSEEK_KEY=$(grep '^DEEPSEEK_API_KEY=' /root/.hermes/.env | head -1)
cat > /root/.hermes/profiles/<name>/.env << ENVEOF
${DEEPSEEK_KEY}
TELEGRAM_BOT_TOKEN=<correct-token>
TELEGRAM_ALLOWED_USERS=7239715879
ENVEOF
```

## Forced Gateway Reset (last resort)

If the gateway is stuck in a restart loop and won't come up cleanly:
```bash
# Kill the stuck process
pkill -9 -f "profile <name> gateway"

# Remove stale lock files
rm -f /root/.local/state/hermes/gateway-locks/telegram-bot-token-*.lock

# Kill the old systemd service
systemctl stop hermes-gateway-<name>
systemctl disable hermes-gateway-<name>

# Reinstall fresh
hermes -p <name> gateway install --system --run-as-user root
```
