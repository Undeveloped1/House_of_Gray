# Telegram Profile Isolation — Per-Profile Bot Routing

**Problem:** Multiple Hermes profiles with separate gateway processes all receive
and respond to the same Telegram messages. Joe sends a DM to the bot and Paul,
Abby, Tabitha, and Hans all see it and might respond. The chats are one shared
soup rather than being isolated per profile.

**Root cause:** A single Telegram bot token serves all profiles. Telegram's API
delivers all updates for a bot to exactly **one webhook endpoint**. Hermes
distributes incoming messages to every profile whose `allowed_chats` config
includes that chat ID. Since all profiles share the same bot token and have the
same `allowed_chats` (or inherit the global config), they all see the same
messages.

This is **not a bug** — it's the logical consequence of one bot mapping to many
profiles. The bot is one entity; Hermes fans out to all matching gateways.

## Diagnostic: which profiles are receiving Telegram messages?

Count Telegram messages per profile's gateway log:

```bash
for profile in default abby hans lyra tabitha paul; do
  count=$(grep -c "platform=telegram" \
    /root/.hermes/profiles/$profile/logs/gateway.log 2>/dev/null || echo 0)
  echo "$profile: $count"
done
```

Also check the global gateway log (serves the `default` profile):

```bash
grep -c "platform=telegram" /root/.hermes/logs/gateway.log
```

If multiple profiles show non-zero counts for the same chat ID, you have the
shared-soup problem. To see WHICH chats are landing:

```bash
grep "platform=telegram" /root/.hermes/logs/gateway.log \
  | grep -oP "chat=\K\d+(-\d+)?" | sort | uniq -c | sort -rn
```

## Diagnostic: which profiles claim which chats?

```bash
for profile in default paul abby hans lyra tabitha; do
  cfg="/root/.hermes/profiles/$profile/config.yaml"
  [ "$profile" = "default" ] && cfg="/root/.hermes/config.yaml"
  chats=$(grep "allowed_chats:" "$cfg" 2>/dev/null | grep -v "^#" | head -1)
  echo "$profile: $chats"
done
```

When every profile shows the same `allowed_chats: 7239715879,-1003748772302`,
any message from those chats reaches ALL profiles' gateway processes.

## Solutions

### Option A: Separate Telegram bots per profile (cleanest)

Create a distinct Telegram bot for each profile via @BotFather, then configure
each profile's `.env` with its own `TELEGRAM_BOT_TOKEN`:

```bash
# Paul's bot
echo 'TELEGRAM_BOT_TOKEN=123456:paul_bot_token' >> /root/.hermes/profiles/paul/.env

# Abby's bot
echo 'TELEGRAM_BOT_TOKEN=789012:abby_bot_token' >> /root/.hermes/profiles/abby/.env
```

After restarting gateways, each profile only receives messages sent to its own bot.
`@PaulBot` → Paul. `@AbbyBot` → Abby. Natural isolation without config hacking.

**Caveat:** Joe needs to switch between bot DMs on Telegram. One chat per bot.

### Option B: Chat-based routing with one bot

Give each profile a distinct `allowed_chats` list. Only one profile gets Joe's
personal DM chat ID; other profiles get their own group/channel chat IDs:

```bash
# Paul gets Joe's DM + the game group
hermes config set telegram.allowed_chats "7239715879,-1003748772302" --profile paul

# Abby gets her own group chat
hermes config set telegram.allowed_chats "-1001234567890" --profile abby

# Tabitha gets her group
hermes config set telegram.allowed_chats "-1009876543210" --profile tabitha
```

**Caveat:** Joe's personal DM can only go to ONE profile. All other communication
needs separate Telegram groups, channels, or forum topics per profile.

### Option C: Chat-to-profile routing (if implemented)

Check if Hermes supports explicit chat-to-profile binding (as of 2026-07, the
gateway source does NOT have a `chat_to_profile` mapping — `allowed_chats` is
the only routing mechanism):

```bash
grep -r "chat.*profile\|profile.*chat\|bind_chat" \
  ~/.hermes/hermes-agent/gateway/platforms/telegram.py
```

If empty, this feature doesn't exist yet.

## Architectural constraint

Per the Telegram Bot API: one bot token → one webhook URL → one delivery
endpoint. There is no native way to say "messages from chat A go to profile X,
messages from chat B go to profile Y" within a single bot. Hermes would need to
implement its own dispatcher layer on top of the shared webhook, routing
incoming messages to the correct profile's session store based on config.

Until that exists, separate bots (Option A) are the only path to true per-profile
Telegram isolation.

## Verification after fix

After applying a fix, send a test message and verify only the intended profile
sees it:

```bash
# Send a Telegram message, then immediately check:
for p in paul abby hans tabitha; do
  echo "=== $p ==="
  tail -3 /root/.hermes/profiles/$p/logs/gateway.log 2>/dev/null | grep telegram
done
```

Only the targeted profile should show the inbound message.
