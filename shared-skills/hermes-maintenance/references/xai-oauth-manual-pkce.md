# xAI OAuth Manual PKCE Exchange

When `hermes auth add xai-oauth` can't complete interactively (headless VPS,
no browser, stdin not a TTY), run the PKCE exchange manually in Python.

## When to use

- `hermes auth status xai-oauth` says "logged out"
- `auth.json` shows `last_auth_error` with `xai_refresh_failed` / "Refresh token has been revoked"
- `hermes auth add xai-oauth --no-browser --manual-paste` fails because stdin isn't a TTY
- You're on SSH without X forwarding

## Step 1: Generate PKCE params and authorization URL

```python
import hashlib, secrets, urllib.parse, json, base64

code_verifier = secrets.token_urlsafe(64)[:64]
digest = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()

state = secrets.token_hex(16)
nonce = secrets.token_hex(16)
client_id = "b1a00492-073a-47ea-816f-4c329264a828"
redirect_uri = "http://127.0.0.1:56121/callback"

params = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "scope": "openid profile email offline_access grok-cli:access api:access",
    "code_challenge": code_challenge,
    "code_challenge_method": "S256",
    "state": state,
    "nonce": nonce,
    "plan": "generic",
    "referrer": "hermes-agent",
}

auth_url = f"https://auth.x.ai/oauth2/authorize?{urllib.parse.urlencode(params)}"
print(auth_url)

# Save state for step 3
pkce_state = {
    "code_verifier": code_verifier,
    "code_challenge": code_challenge,
    "state": state,
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "token_endpoint": "https://auth.x.ai/oauth2/token",
}
with open("/tmp/xai_pkce_state.json", "w") as f:
    json.dump(pkce_state, f)
```

## Step 2: User opens URL and pastes authorization code

Give the `auth_url` to the user. They open it in a browser, approve,
and xAI displays the authorization code directly on the page (or redirects
to a localhost URL that fails — copy the `?code=...` parameter from the
address bar).

## Step 3: Exchange code for tokens

```python
import json, httpx

with open("/tmp/xai_pkce_state.json") as f:
    state = json.load(f)

code = "PASTE_USER_CODE_HERE"

data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": state["redirect_uri"],
    "client_id": state["client_id"],
    "code_verifier": state["code_verifier"],
    "code_challenge": state["code_challenge"],
    "code_challenge_method": "S256",
}

response = httpx.post(
    state["token_endpoint"],
    headers={
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    },
    data=data,
    timeout=30.0,
)

if response.status_code != 200:
    raise Exception(f"Token exchange failed: {response.status_code} {response.text}")

tokens = response.json()
with open("/tmp/xai_tokens.json", "w") as f:
    json.dump(tokens, f)
print("Tokens received:", list(tokens.keys()))
```

## Step 4: Save tokens into Hermes auth.json

```python
import json, sys
sys.path.insert(0, "/usr/local/lib/hermes-agent")

from hermes_cli.auth import (
    _save_xai_oauth_tokens,
    _load_auth_store,
    _save_auth_store,
    _load_provider_state,
    _save_provider_state,
    _auth_store_lock,
)

with open("/tmp/xai_tokens.json") as f:
    tokens = json.load(f)

discovery = {
    "authorization_endpoint": "https://auth.x.ai/oauth2/authorize",
    "token_endpoint": "https://auth.x.ai/oauth2/token",
}

_save_xai_oauth_tokens(
    tokens,
    discovery=discovery,
    redirect_uri="http://127.0.0.1:56121/callback",
)

# Clear stale error state
with _auth_store_lock():
    store = _load_auth_store()
    state = _load_provider_state(store, "xai-oauth")
    if state and "last_auth_error" in state:
        del state["last_auth_error"]
        _save_provider_state(store, "xai-oauth", state)
        _save_auth_store(store)

print("Done!")
```

## Step 5: Verify

```bash
hermes auth status xai-oauth   # should say "logged in"
hermes auth list                # should show xai-oauth credential with ←
```

## Cleanup

```bash
rm -f /tmp/xai_pkce_state.json /tmp/xai_tokens.json
```

## Pitfalls

- **Each authorization code is bound to its PKCE challenge.** If you
  generate new PKCE params, you need a new code from the user. You can't
  reuse a code from a previous flow.
- **Code is single-use.** If the exchange fails, you need a fresh code.
- **Provider name:** Always `xai-oauth`, not `xai`. `xai` is the API-key
  provider; `xai-oauth` is the OAuth provider.
- **The `code_challenge` in the token exchange body is defense-in-depth**
  for xAI's server (per Hermes #26990). Include it even though RFC 7636
  only requires `code_verifier`.
