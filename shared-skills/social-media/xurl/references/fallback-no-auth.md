# Fallback: Reading X Posts Without API Auth

When `xurl` isn't installed or X API credentials aren't configured, you can still extract public tweet data by curling the post page and parsing the `__INITIAL_STATE__` JSON blob embedded in the HTML.

## Command

```bash
curl -sL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36" \
  "https://x.com/HANDLE/status/TWEET_ID" | \
  python3 -c "
import re, sys, json
html = sys.stdin.read()
m = re.search(r'window\.__INITIAL_STATE__\s*=\s*(\{.*?\});', html, re.DOTALL)
if m:
    data = json.loads(m.group(1))
    tweets = data.get('entities', {}).get('tweets', {}).get('entities', {})
    users = data.get('entities', {}).get('users', {}).get('entities', {})
    print(json.dumps({'tweets': tweets, 'users': users}, indent=2))
"
```

## What You Get

- **Tweet data:** `full_text`, engagement counts (likes, retweets, replies, quotes, bookmarks), creation time, source, conversation ID
- **URL entities:** `display_url`, `expanded_url` (follow to see linked content)
- **User data:** bio, follower/following counts, profile image URL, pinned tweet IDs, website
- **Article indicator:** If the tweet text is just a `t.co` link and `expanded_url` contains `/i/article/`, it's an X Article (long-form post)

## What You DON'T Get

- Article/long-form content (behind auth wall — only the link is visible)
- Replies, threaded context (separate API/page needed)
- Write operations (post, like, reply)
- Private/protected accounts

## Limitations

- t.co redirects may timeout from VPS environments — use `expanded_url` from the JSON instead of following the short link
- Heavy rate-limiting on repeated curl requests to the public page
- Auth walls block everything except the embedded `__INITIAL_STATE__` blob
- **Auth-walled content:** X Articles (long-form posts), replies threads, and protected accounts cannot be reached via public scrape. See "Beyond the Auth Wall" below.

## Beyond the Auth Wall: Cookie-Based Browser Auth

When the user needs auth-walled content (X Articles, threads, DMs) but has explicitly rejected the paid API / xurl setup, the correct path is:

1. **User exports X cookies** from their local browser (EditThisCookie extension, or DevTools → Application → Cookies → x.com → export as JSON)
2. **Drop into Syncthing** — lands on VPS at `/root/syncthing/paul-dropbox/`
3. **Playwright with persistent profile** — launch Chromium with `--user-data-dir=/root/.x-profile`, load cookies, navigate as authenticated user
4. **Single auth session:** User auths once via `ssh -L 9222:localhost:9222 paul` → `http://localhost:9222` → log into X → cookies persist in `--user-data-dir`. After that, no further user involvement needed.

Critical Playwright launch flags for headless VPS:
```
--headless=new --no-sandbox --disable-gpu --remote-debugging-port=9222
```
**Do NOT** forget `--headless=new` — Chromium will fail with "Missing X server or $DISPLAY."

**Do NOT** bind remote debugging to `0.0.0.0` — it exposes the browser to the public internet. Keep it on localhost and use SSH tunneling.

**Pivot rule:** If the user says "I'm not paying for the API" or rejects xurl setup, offer the cookie-based approach immediately. Don't spend additional cycles trying to make the API work.

## When to Use This Fallback

- Quick research on a public post when API creds aren't available
- Checking engagement stats before deciding whether to set up full API access
- Verifying a tweet exists and is public before attempting API operations
