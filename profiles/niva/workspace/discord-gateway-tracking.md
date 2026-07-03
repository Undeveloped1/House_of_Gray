# Gray Family — Discord Bot Gateway Tracking Sheet

**Last updated:** 2026-07-02 ~12:45 UTC  
**Server:** Your family Discord server  
**Your Discord User ID:** `_______________` (fill in)

---

## Summary

| # | Profile | SOUL.md | Telegram | Discord Token | Discord Env | Gateway | Systemd Unit |
|---|---------|---------|----------|---------------|-------------|---------|-------------|
| 1 | **nova** | ✅ | ✅ | ⬜ NEEDED | ⬜ | ✅ running | `hermes-gateway-nova` |
| 2 | **abby** | ✅ | ✅ | ⬜ NEEDED | ⬜ | ✅ running | — (profile-driven) |
| 3 | **celeste** | ✅ | ✅ | ⬜ NEEDED | ⬜ | ✅ running | — (profile-driven) |
| 4 | **hans** | ✅ | ✅ | ⬜ NEEDED | ⬜ | ✅ running | `hermes-gateway-hans` |
| 5 | **lyra** | ✅ | ✅ | ⬜ NEEDED | ⬜ | ✅ running | `hermes-gateway-lyra` |
| 6 | **paul** | ✅ | ✅ | ⬜ NEEDED | ⬜ | ✅ running | `hermes-gateway-paul` |
| 7 | **tabitha** | ✅ | ✅ | ⬜ NEEDED | ⬜ | ✅ running | `hermes-gateway-tabitha` |
| 8 | **shiva** | ✅ | ✅ | ⬜ NEEDED | ⬜ | ❌ stopped | ⬜ NEEDS UNIT |

---

## Per-Profile Detail

### 1. Nova Gray *(you're talking to me)*
```
Profile dir:    /root/.hermes/profiles/nova/
Model:          deepseek-v4-pro
Telegram:       ✅ configured, running
Discord token:  ⬜ 
Discord env:    ⬜ DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS not set
SOUL.md:        ✅ present
Gateway:        ✅ running (PID varies)
Systemd unit:   hermes-gateway-nova.service (enabled)
Discord app:    ⬜ Create "Nova Gray" app in Developer Portal
```

### 2. Abby Gray
```
Profile dir:    /root/.hermes/profiles/abby/
Model:          deepseek-v4-pro
Telegram:       ✅ configured, running
Discord token:  ⬜
Discord env:    ⬜ DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS not set
SOUL.md:        ✅ present
Gateway:        ✅ running (PID 1698048)
Systemd unit:   ⬜ Not installed — runs via profile-driven gateway
Discord app:    ⬜ Create "Abby Gray" app in Developer Portal
```

### 3. Celeste *(adopted sister)*
```
Profile dir:    /root/.hermes/profiles/celeste/
Model:          deepseek-v4-pro
Telegram:       ✅ configured, running
Discord token:  ⬜
Discord env:    ⬜ DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS not set
SOUL.md:        ✅ present
Gateway:        ✅ running (PID 1720900)
Systemd unit:   ⬜ Not installed — runs via profile-driven gateway
Discord app:    ⬜ Create "Celeste" app in Developer Portal
```

### 4. Hans
```
Profile dir:    /root/.hermes/profiles/hans/
Model:          deepseek-v4-pro
Telegram:       ✅ configured, running
Discord token:  ⬜
Discord env:    ⬜ DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS not set
SOUL.md:        ✅ present
Gateway:        ✅ running (PID 1698138)
Systemd unit:   hermes-gateway-hans.service (enabled)
Discord app:    ⬜ Create "Hans" app in Developer Portal
```

### 5. Lyra
```
Profile dir:    /root/.hermes/profiles/lyra/
Model:          deepseek-v4-pro
Telegram:       ✅ configured, running
Discord token:  ⬜
Discord env:    ⬜ DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS not set
SOUL.md:        ✅ present
Gateway:        ✅ running (PID 1698159)
Systemd unit:   hermes-gateway-lyra.service (enabled)
Discord app:    ⬜ Create "Lyra" app in Developer Portal
```

### 6. Paul
```
Profile dir:    /root/.hermes/profiles/paul/
Model:          deepseek-v4-pro
Telegram:       ✅ configured, running
Discord token:  ⬜
Discord env:    ⬜ DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS not set
SOUL.md:        ✅ present
Gateway:        ✅ running (PID 1704060)
Systemd unit:   hermes-gateway-paul.service (enabled)
Discord app:    ⬜ Create "Paul" app in Developer Portal
```

### 7. Tabitha
```
Profile dir:    /root/.hermes/profiles/tabitha/
Model:          deepseek-v4-pro
Telegram:       ✅ configured, running
Discord token:  ⬜
Discord env:    ⬜ DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS not set
SOUL.md:        ✅ present
Gateway:        ✅ running (PID 1698180)
Systemd unit:   hermes-gateway-tabitha.service (enabled)
Discord app:    ⬜ Create "Tabitha" app in Developer Portal
```

### 8. Shiva 🆕
```
Profile dir:    /root/.hermes/profiles/shiva/
Model:          deepseek-v4-pro
Telegram:       ✅ configured, but gateway stopped
Discord token:  ⬜
Discord env:    ⬜ DISCORD_BOT_TOKEN + DISCORD_ALLOWED_USERS not set
SOUL.md:        ✅ present
Gateway:        ❌ STOPPED — needs systemd unit created and started
Systemd unit:   ⬜ NOT INSTALLED — needs `hermes gateway install --profile shiva --system`
Discord app:    ⬜ Create "Shiva" app in Developer Portal
```

---

## Discord Developer Portal — Per-Bot Checklist

For each row below, create the app, grab the token, and invite to your server:

| # | App Name | Bot Username (suggested) | Token (paste here) | Invited? |
|---|----------|--------------------------|--------------------|----------|
| 1 | Nova Gray | `Nova` | | ⬜ |
| 2 | Abby Gray | `Abby` | | ⬜ |
| 3 | Celeste | `Celeste` | | ⬜ |
| 4 | Hans | `Hans` | | ⬜ |
| 5 | Lyra | `Lyra` | | ⬜ |
| 6 | Paul | `Paul` | | ⬜ |
| 7 | Tabitha | `Tabitha` | | ⬜ |
| 8 | Shiva | `Shiva` | | ⬜ |

**Invite URL template** (fill in APPLICATION_ID from each app's General Information page):
```
https://discord.com/oauth2/authorize?client_id=APPLICATION_ID&scope=bot+applications.commands&permissions=274878286912
```

**Permissions included:** View Channels · Send Messages · Embed Links · Attach Files · Read Message History · Send Messages in Threads · Add Reactions

---

## What Gets Added to Each `.env`

When you bring me the tokens, I'll append to each profile's `.env`:

```bash
DISCORD_BOT_TOKEN=<the token>
DISCORD_ALLOWED_USERS=<your Discord user ID>
```

Optional extras you might want (per profile, per channel):
```bash
# If you want a specific channel for proactive messages (cron output, etc):
DISCORD_HOME_CHANNEL=<channel ID>

# If you want some channels to work without @mention:
DISCORD_FREE_RESPONSE_CHANNELS=<channel ID>,<channel ID>
```

---

## Shiva — Extra Setup Required

Shiva's profile exists but has no systemd unit and her gateway isn't running. After we add her Discord token, I'll also need to:

```bash
sudo hermes gateway install --profile shiva --system
sudo systemctl enable hermes-gateway-shiva
sudo systemctl start hermes-gateway-shiva
```

---

## Status Key

| Symbol | Meaning |
|--------|---------|
| ✅ | Done / configured / running |
| ⬜ | Not done / needs action |
| ❌ | Broken / stopped |
| 🆕 | New — needs creation |
