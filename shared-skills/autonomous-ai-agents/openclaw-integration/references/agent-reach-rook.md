# Agent Reach + Rook Integration

Agent Reach (`github.com/Panniantong/Agent-Reach`) is a CLI tool that gives AI agents
read/search access to 13 internet platforms with zero API fees. Installed 2026-06-22
on the VPS alongside Rook in a virtualenv at `/tmp/Agent-Reach/.venv/`.

## What It Provides Rook

**Twitter/X via cookie-based auth — no API key, no expiring OAuth tokens.** This is
Rook's backup/alternative when xAI OAuth tokens expire (which happens within days).

### Installation path

| What | Where |
|------|-------|
| Tool | `/tmp/Agent-Reach/.venv/bin/agent-reach` |
| Config | `~/.agent-reach/config.yaml` (0o600) |
| Skill file | `/root/.agents/skills/agent-reach/SKILL.md` |
| Twitter backend | `twitter-cli` (pipx) |

## Activating the venv

```bash
source /tmp/Agent-Reach/.venv/bin/activate
```

## Twitter Auth Setup

Agent Reach uses cookie-based auth (no API key). Two methods:

### Method 1: Auto-extract from browser (laptop + logged into x.com)

```bash
agent-reach configure --from-browser chrome
```

### Method 2: Manual cookie injection (VPS — from laptop F12 → Application → Cookies → x.com)

```bash
agent-reach configure twitter-cookies <auth_token> <ct0>
```

Get the values from Chrome DevTools → Application → Cookies → x.com:
- `auth_token` — long hex string
- `ct0` — shorter CSRF token

### Verify

```bash
agent-reach doctor | grep -i twitter
# Should show: ✅ Twitter/X 推文
```

## Rook Usage

Rook calls twitter-cli directly (Agent Reach installed it):

```bash
# Search tweets
twitter-cli search "query" --count 10

# Read a specific tweet
twitter-cli tweet https://x.com/user/status/123456

# From a specific account
twitter-cli timeline --user account_name
```

Rook's AGENTS.md should reference twitter-cli as fallback when x_search tokens are dead.

## Channels Active (2026-06-22)

7/13 channels: GitHub, YouTube, V2EX, RSS, Exa semantic search, web reading, BiliBili.
Twitter/X — now configured ✅. Remainder (Reddit, XiaoHongShu, Xiaoyuzhou, Xueqiu, LinkedIn) unlockable.

## Troubleshooting

- **"Twitter cookies not configured"** — rerun `agent-reach configure twitter-cookies <auth_token> <ct0>`
- **Tokens expired** — Twitter invalidates cookies periodically. Re-extract from browser.
- **Doctor shows Twitter as "optional"** — ignore; the configure command's own test confirmation ("Twitter access works!") is authoritative. The doctor may not reflect cookie-based auth state.
- **xAI OAuth dead AND cookies expired** — both auth paths are down. Joe must re-auth xai-oauth or re-extract cookies from laptop.
