---
name: agent-reach
description: "Give AI agents internet-scale eyes — search and read Twitter/X, Reddit, YouTube, GitHub, Bilibili, XiaoHongShu, LinkedIn, V2EX, RSS feeds, and any web URL. One CLI, cookie-based auth (no API keys), installed on VPS."
---

# Agent Reach

Agent Reach is a Python CLI + library that gives AI agents read/search access
to 13 internet platforms. It installs and configures upstream tools
(twitter-cli, yt-dlp, gh CLI, mcporter, etc.) — agents then call those tools
directly.

**GitHub:** https://github.com/Panniantong/Agent-Reach (38k+ stars, MIT)
**VPS venv:** `/tmp/Agent-Reach/.venv/` (source to activate)
**Skill for OpenClaw:** `/root/.agents/skills/agent-reach/`

## Quick usage

```bash
source /tmp/Agent-Reach/.venv/bin/activate
agent-reach doctor                    # health check: which channels are live
agent-reach doctor --json             # machine-readable status
agent-reach install --channels CHAN   # install a channel (twitter, reddit, etc.)
agent-reach configure --from-browser chrome  # extract cookies for auth
```

## Channels installed on VPS

| Channel | Status | Notes |
|---------|--------|-------|
| GitHub | ✅ | Full read/search/PR/Issue |
| YouTube | ✅ | yt-dlp + Node.js JS runtime |
| V2EX | ✅ | Public API |
| RSS/Atom | ✅ | feedparser |
| Exa search | ✅ | Semantic search via mcporter |
| Bilibili | ✅ | Search API (curl) |
| Any web | ✅ | Jina Reader |
| Twitter/X | ⚠️ | twitter-cli installed, needs cookie auth |
| Other | Not installed | Reddit, XHS, LinkedIn, Xueqiu, Xiaoyuzhou |

## Twitter auth

Twitter uses cookie-based auth — no API key needed. On a machine WITH a
browser where you're logged into x.com:

```bash
agent-reach configure --from-browser chrome
```

This extracts `auth_token` + `ct0` from your browser cookie store and saves
them to `~/.agent-reach/config.yaml`. Works with Chrome, Firefox, Edge,
Brave, Opera.

On a headless VPS (no browser), cookies must be transferred manually:
1. Extract on laptop: `agent-reach configure --from-browser chrome`
2. Copy `~/.agent-reach/config.yaml` to `/root/.agent-reach/config.yaml` on VPS

Or manually set the values:
```bash
agent-reach configure twitter-cookies <auth_token> <ct0>
```

## Rook integration

Rook (OpenClaw) loads the skill from `/root/.agents/skills/agent-reach/`.
Once Twitter auth is configured, Rook can search/read X without recurring
OAuth token expiration.

## Pitfalls

- **No browser on headless VPS**: cookie extraction only works where a
  browser with active logins exists.
- **Twitter auth is fragile**: cookie-based auth breaks when Twitter changes
  auth. Re-extract cookies when it stops working.
- **Rate limiting**: server IPs may hit platform rate limits. Some platforms
  (Reddit) require login state.
- **Platform-specific IP blocks**: Chinese platforms may block non-CN IPs.

## Reference

- GitHub: https://github.com/Panniantong/Agent-Reach
- Commands: `agent-reach --help`, `agent-reach install --help`, `agent-reach configure --help`
- Skill file: `/root/.agents/skills/agent-reach/SKILL.md`
