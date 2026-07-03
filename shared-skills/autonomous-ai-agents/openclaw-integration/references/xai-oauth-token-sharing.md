# xAI OAuth Token Sharing: Paul → Rook

## Problem

Rook (OpenClaw) needs xAI API access for x_search but has no independent
OAuth flow. Paul (Hermes) has working xAI OAuth with refresh tokens in
`~/.hermes/auth.json`. The access token expires; Paul's Hermes auto-refreshes
it. Rook needs the live token without duplicating the OAuth setup.

## Solution: Wrapper script

`get-xai-token.sh` in Rook's workspace reads the live bearer token from Paul's
auth.json at runtime. Rook always gets a fresh token — no separate OAuth flow,
no separate API key.

```bash
#!/bin/bash
# get-xai-token.sh — extract live xAI bearer token from Paul's auth.json
# Checks both auth.json layers: providers (raw) and credential_pool (managed)
python3 -c "
import json
with open('/root/.hermes/auth.json') as f:
    auth = json.load(f)

# Layer 1: providers (raw tokens)
provs = auth.get('providers', {})
xai_prov = provs.get('xai-oauth', {})
tok = xai_prov.get('tokens', {}).get('access_token', '')
if tok:
    print(tok)
    exit(0)

# Layer 2: credential_pool (managed — check both direct and .data wrapper)
pool = auth.get('credential_pool', {})
xai = pool.get('xai-oauth', [])
for cred in xai:
    # Direct access (newer format)
    token = cred.get('access_token', '')
    # .data wrapper (older format)
    if not token:
        token = cred.get('data', {}).get('access_token', '')
    if token:
        print(token)
        exit(0)

# Neither layer had a token
exit(1)
"
```

Rook's `.env` or environment references this script to get the token at
runtime. The token refreshes whenever Paul uses xAI (x_search, image_generate
with xAI backend), which triggers Hermes to refresh the OAuth token in
auth.json.

## Fallback

If the token isn't valid (Paul hasn't used xAI in a while, token expired),
Rook's x_search will fail. Fix: Paul runs one x_search call, which refreshes
the shared token. In practice this is rare — Paul uses xAI regularly.

## Diagnostics

- Paul's token status: check `~/.hermes/auth.json` for both layers:
  - `providers.xai-oauth.tokens.access_token` — raw token storage (may have refresh_token here)
  - `credential_pool.xai-oauth[0].access_token` — managed pool (may have token directly or nested under `.data`)
  - If the pool is an **empty list `[]`**, the token was cleared — even if the key exists as a placeholder
- Paul refreshes token: run any x_search query → Hermes auto-refreshes if expired
- Rook's token: `./get-xai-token.sh | wc -c` should return ~800+ chars for a live JWT
- OAuth vs API key: Paul uses OAuth (`credential_source: xai-oauth`), NOT an API key. `hermes status` shows "✗ xAI" because it only checks env vars — ignore this.
- **Token can be in two layers** — auth.json has both `providers.xai-oauth` (raw tokens) and `credential_pool.xai-oauth` (managed pool with status tracking). The extraction script should check both. See `hermes-maintenance` skill → `references/credential-diagnostics.md` for full inspection technique.
