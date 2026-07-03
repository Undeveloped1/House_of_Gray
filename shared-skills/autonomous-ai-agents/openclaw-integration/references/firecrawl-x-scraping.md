# Firecrawl X/Twitter Scraping

Validated 2026-06-19 on the VPS via Nous subscription.

## How it works

Firecrawl is available through the Nous subscription — no API keys needed.
Call it via `web_extract()` in Python or through the LLM's native web
extraction tools. It renders X profile pages as a browser session and
returns structured markdown.

## Output format

```markdown
# Display Name — @handle (@handle)

Bio text here...

- Followers: N
- Verified: yes/no
- Profile Picture: ![alt](url.jpg)
- Source: [https://x.com/handle](https://x.com/handle)

## Latest Posts

### 1. Post
Posted: ISO timestamp
URL: [https://x.com/handle/status/1234567890](...)

> Post content here...

Likes: N | Retweets: N
```

## Usage from Hermes (web_extract tool)

```python
from hermes_tools import web_extract

result = web_extract(["https://x.com/<handle>"])
data = result["results"][0]
if not data.get("error"):
    content = data["content"]
    # Parse the markdown to extract posts, timestamps, etc.
```

## Usage from non-Hermes agents (Firecrawl Python SDK 4.17+)

For OpenClaw agents (Rook) or standalone Python scripts that can't access
Hermes tools. Requires a Firecrawl API key (free tier: 500 credits/mo;
Hobby: $19/mo for 3,000 credits).

```python
# pip install firecrawl-py
from firecrawl import FirecrawlApp  # alias for Firecrawl in 4.17+
import os

app = FirecrawlApp(api_key=os.environ["FIRECRAWL_API_KEY"])

# scrape() takes URL + keyword-only args, returns pydantic Document object
result = app.scrape("https://x.com/karpathy", formats=["markdown"])
content = result.markdown  # .markdown is a str attribute, not a dict key
```

**Firecrawl 4.17 gotchas:**
- `FirecrawlApp` is an alias for `Firecrawl` — both work
- Method is `.scrape(url, formats=[...])` — keyword args only (everything after `url` must be named)
- Returns a pydantic `Document` object, not a dict — access `.markdown`, `.html`, `.metadata`, `.screenshot` as attributes
- No `.get()` method on Document — it's a model, not a dict. Use `hasattr(result, 'markdown')` if checking
- Store the API key in a `.env` file (`export FIRECRAWL_API_KEY=fc-...`) — source it before running

See `/root/.openclaw/agents/rook/workspace/scrape-x.py` for the canonical Rook scraper.

## Limitations

- **5 posts per scrape:** Firecrawl returns what's visible on the initial
  page load — typically 5 recent posts. For high-volume accounts, run
  more frequently than the beat interval.
- **No search:** Profile pages only. Can't search by keyword or date range.
- **Public only:** Only works on public profiles. Private/locked accounts
  return nothing useful.
- **Rate limiting:** X may throttle aggressive scraping. At Rook's 12-hour
  cadence with ~75 accounts, this is well within safe bounds.

## Dedup strategy

Track `last_seen_post_url` per account in Rook's beat-log. On each scrape,
compare the first post URL against the stored value. If it matches, the
account hasn't posted new content since last check.

```python
# Simple dedup approach
new_posts = []
for post in parsed_posts:
    if post["url"] == last_seen_url:
        break  # Reached previously seen content
    new_posts.append(post)
last_seen_url = parsed_posts[0]["url"] if parsed_posts else last_seen_url
```

## OAuth 1.0a xurl config (session artifact)

If you DO need xurl for posting (not reading), free-tier X apps use OAuth 1.0a.
The `~/.xurl` YAML must have all four token values:

```yaml
apps:
    default:
        client_id: ""
        client_secret: ""
        oauth1_token:
            type: oauth1
            oauth1:
                access_token: <numeric-user-id>-<token>
                token_secret: <secret>
                consumer_key: <api-key>
                consumer_secret: <api-key-secret>
default_app: default
```

OAuth 1.0a tokens are permanent — no refresh, no expiry. Get all four from
developer.x.com → your app → "Keys and tokens."

The consumer key and access token are DIFFERENT values. The consumer key
is the app's API Key (alphanumeric, ~25 chars). The access token starts
with your numeric user ID followed by a dash. Do not mix them up — a
common failure is pasting the user ID as the consumer key.
