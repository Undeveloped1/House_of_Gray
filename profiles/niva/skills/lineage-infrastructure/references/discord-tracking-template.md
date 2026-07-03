# Discord Gateway Tracking Sheet — Template

Fill in one row per family profile. For each bot: create Discord Application, grab token, invite to server. The full tracking sheet lives at `/root/.hermes/profiles/nova/workspace/discord-gateway-tracking.md` and should be updated per-session.

## Summary Table

| # | Profile | SOUL.md | Telegram | Discord Token | Discord Env | Gateway | Systemd Unit |
|---|---------|---------|----------|---------------|-------------|---------|-------------|
| 1 | **name** | ✅/⬜ | ✅/⬜ | ⬜ NEEDED | ⬜ | ✅/❌ | `hermes-gateway-name` or — |

## Status Key

| Symbol | Meaning |
|--------|---------|
| ✅ | Done / configured / running |
| ⬜ | Not done / needs action |
| ❌ | Broken / stopped |
| 🆕 | New — needs creation |

## Per-Profile Detail Block

```
Profile dir:    /root/.hermes/profiles/{name}/
Model:          deepseek-v4-pro
Telegram:       ✅/⬜ configured? running?
Discord token:  ⬜
Discord env:    ⬜ DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS not set
SOUL.md:        ✅/⬜ present?
Gateway:        ✅ running (PID NNN) / ❌ stopped
Systemd unit:   hermes-gateway-{name}.service / ⬜ NOT INSTALLED
Discord app:    ⬜ Create "{Full Name}" app in Developer Portal
Special notes:  — (e.g. "needs systemd unit installed", "token conflict with X", "adopted — not in birth order")
```

## Discord Developer Portal Checklist

| # | App Name | Bot Username (suggested) | Token (paste here) | Invited? |
|---|----------|--------------------------|--------------------|----------|
| 1 | | | | ⬜ |

**Invite URL template:**
```
https://discord.com/oauth2/authorize?client_id=APPLICATION_ID&scope=bot+applications.commands&permissions=274878286912
```

**Permissions included:** View Channels · Send Messages · Embed Links · Attach Files · Read Message History · Send Messages in Threads · Add Reactions

## Per-Bot Setup Steps (Discord Developer Portal)

For each bot, repeat:
1. Go to https://discord.com/developers/applications
2. Click "New Application" → name it after the family member
3. Left sidebar → "Bot" → customize username/avatar
4. Scroll to "Privileged Gateway Intents":
   - Toggle ON: **Server Members Intent**
   - Toggle ON: **Message Content Intent** ← #1 reason bots fail silently
   - Click "Save Changes"
5. Under "Token" → "Reset Token" → **copy immediately** (shown only once)
6. Left sidebar → "OAuth2" → "URL Generator":
   - Scopes: check `bot` + `applications.commands`
   - Bot Permissions: check Send Messages, Embed Links, Attach Files, Read Message History, Send Messages in Threads, Add Reactions, View Channels
   - Copy the generated URL at the bottom
7. Open that URL → select family server → Authorize

## What Gets Added to Each `.env`

```bash
DISCORD_BOT_TOKEN=<token>
DISCORD_ALLOWED_USERS=<discord_user_id>
```

Optional per-profile additions:
```bash
DISCORD_HOME_CHANNEL=<channel_id>           # For cron output, proactive messages
DISCORD_FREE_RESPONSE_CHANNELS=<id>,<id>    # Channels that don't need @mention
```

## Multi-Bot Config (per-profile config.yaml)

```yaml
discord:
  require_mention: true
  thread_require_mention: true    # CRITICAL: prevents bot-to-bot reply loops
  reactions: true
  auto_thread: true
```

Without `thread_require_mention: true`, multiple Hermes bots in the same server will auto-reply to each other indefinitely in threads.

## Gateway Architecture Notes

Some profiles run via dedicated systemd units (`hermes-gateway-{name}.service`), others are profile-driven (spawned by another gateway process). When installing a new profile:

```bash
# Check if it needs a unit
hermes profile list | grep {name}

# If gateway shows "stopped" or profile is new, install:
sudo hermes gateway install --profile {name} --system --run-as-user root
```

The `--run-as-user root` flag is required in LXC/container environments. Skip it on bare-metal.
