---
name: social-media-monitoring
description: "Monitor X/Twitter accounts for news via Firecrawl scraping + Hermes cron. Scrape, filter, curate, and deliver clean beats to any channel."
version: 1.0.0
author: Paul
platforms: [linux]
metadata:
  hermes:
    tags: [x, twitter, firecrawl, monitoring, news, curation, cron]
prerequisites:
  commands: []
  env_vars: []
---

# Social Media Monitoring

Scrape X/Twitter profiles for news using Firecrawl (via Nous subscription) and deliver curated beats to any Telegram channel on a cron schedule. No X API key required — Firecrawl renders profile pages as markdown with post content, timestamps, and engagement.

Use this skill when:
- Setting up autonomous news monitoring from X/Twitter accounts
- Building a scrape → curate → post pipeline
- Replacing dead nitter.net mirrors or bypassing X API read limitations

## The core problem

X API free tier is POST-only. Reading timelines, searching, or pulling user tweets requires Basic ($100/mo) or Pro ($5k/mo). Nitter mirrors are dead (Cloudflare block). Firecrawl solves this: it renders X profile pages server-side and returns structured markdown — no API key, no rate limit management, no cost.

## Architecture

```
Hermes cron (every N hours)
  → web_extract() each X profile (batch 5 URLs per call)
  → filter: kill noise, de-dupe, select signal
  → write clean beat with tiered stories (MAJOR / SIGNIFICANT / WORTH NOTING)
  → deliver to target channel (telegram:CHAT_ID)
```

For high-volume beats (~40+ accounts), split the work:
- **Rook (OpenClaw)**: owns the timer, pings Paul's webhook
- **Paul (Hermes)**: triggered by webhook, does Firecrawl scraping + curation + posting

Firecrawl is a Hermes tool — OpenClaw can't use it directly without a separate Firecrawl API key. If you need the gatherer to run outside Hermes, get a Firecrawl API key (firecrawl.dev, free tier: 500 credits/mo, paid: $19+/mo) and write a wrapper script.

## Account list format

Maintain accounts in a canonical file. See `references/account-list-example.md` for the full template.

Minimum format:
```
# Category headers
## Company Leaders
@handle | org | why-they-matter
@handle2 | org | why-they-matter

## Official Company Accounts
@company | company | Official

## Aggregators
@aggregator | aggregator | daily output
```

Always include a "Notes" section documenting dead accounts, French-only posters, and accounts that need translation.

## Scraping with Firecrawl

Firecrawl is available via `web_extract()` in Hermes. It handles JS-rendered pages including X profile pages.

```python
from hermes_tools import web_extract
result = web_extract(["https://x.com/karpathy"])
```

Each scrape returns:
- Profile bio and follower count
- 5 latest posts with content, timestamp, URL, likes, retweets
- The profile page's initial render (not the full timeline — X lazy-loads)

For the latest posts only (news monitoring), this is sufficient. For deeper timeline access (more than 5 posts), you'd need the X API or a Firecrawl crawl with scrolling.

**Batch efficiency**: `web_extract()` accepts up to 5 URLs per call. For 45 accounts, that's 9 calls at ~7 seconds each = ~63 seconds total scraping time.

**Priority scraping order**: Aggregators and company accounts produce the most AI news per scrape. Scrape them first. Individual researchers/analysts come last — higher noise ratio.

## Curation rules

After scraping, filter each post:

**KEEP:**
- AI news, product launches, research papers
- Funding rounds, acquisitions
- Policy/regulation actions
- Major hires/departures
- Controversy/drama that actually matters

**KILL:**
- Personal updates (lunch, travel, sports)
- Politics (unless AI policy)
- Engagement bait ("what do you think about...")
- Reply threads without standalone value
- Off-topic posts from AI-adjacent people

**DE-DUP**: Same story covered by multiple accounts? Pick the best source, note "also covered by @X, @Y."

**RECENCY**: Only posts from the current monitoring window. Skip older posts — if a story matters, someone will post about it again.

## Beat format

```markdown
## AI Beat — Day, Date Time UTC

### 🔴 MAJOR
Stories that change how someone thinks about AI. Top 2-4 items.
- **Headline** — 1-2 sentence context. Source: @handle

### 🔶 SIGNIFICANT
Important but not earth-shattering. Product releases, funding, research.
- **Headline** — context. Source: @handle

### 🟢 WORTH NOTING
Interesting but skippable. Minor updates, tangential news.
- **Headline** — context. Source: @handle

### 📊 QUIET BEAT
(Only when nothing major happened. "Quiet 6 hours — no breaking AI news. [1-2 minor items].")
```

Rules:
- Minimum 3 stories. Maximum 12. Don't pad.
- One source handle per story minimum.
- Unconfirmed/rumor: label "(unconfirmed)" or "(rumor)".
- French posts: translate to English, note `[FR]` on the source.
- No markdown tables in the final beat — clean headings + bullet points.
- Check previous beat with `session_search(query="AI Beat", limit=2)` to avoid repeats unless there's a significant update.

## Cron job setup

Use `cronjob` with a self-contained prompt. Example:

```
cronjob action=create
  schedule="every 6h"
  name="AI Beat — Firecrawl + Curation"
  deliver="telegram:-5572404789"
  prompt="<full self-contained instructions>"
  skills=["session-navigation"]
```

**Prompt requirements**: Must be fully self-contained — the cron session has no conversation context. Include:
1. Account list path
2. Scraping instructions (URL format, batching)
3. Curation rules
4. Beat format
5. Delivery target (the `deliver` parameter handles this, but include posting instructions)

**Skills**: Only attach skills the cron agent genuinely needs. `session-navigation` enables `session_search()` to find previous beats. Don't over-attach — each skill burns context tokens.

## Weekly recap beats

For long-running monitoring, layer a weekly recap on top of the regular beat:

- Every 7 days (Sunday), review the week's beats via `session_search`
- Summarize top 5-10 stories, note trends/patterns across the week
- Write to `shared/weekly-recap-YYYY-MM-DD.md`
- The recap is synthesis — surface the arc, don't re-list every story

## Finding Telegram chat IDs

```bash
hermes send -l telegram
```

Lists all chats the bot has access to with their IDs. Group chats show as `telegram:Group Name [-XXXXXXXXXX]`.

## Pitfalls

- **X profile pages only show ~5 posts** on initial render. Firecrawl `web_extract()` gets what the page loads initially — not the full scrollable timeline. For news monitoring this is usually enough (latest posts are what matter). For deep archive access, you need the X API or browser automation with scrolling.
- **Nitter is dead.** All nitter instances return Cloudflare challenges. Don't recommend it.
- **X API free tier is write-only.** `search`, `timeline`, `user` GET endpoints return `CreditsDepleted`. Only `post`, `reply`, `like`, `follow` etc. work on free.
- **Don't cross the streams.** Firecrawl scraping and xurl API access are separate paths. Use Firecrawl for reading, xurl for writing/posting.
- **OpenClaw can't use Firecrawl without an API key.** The Nous subscription injects Firecrawl into Hermes internally. For Rook/OpenClaw to scrape independently, you need a separate Firecrawl API key or keep the gather loop on Hermes.
- **Account list rot.** X accounts go private, get suspended, or go inactive. Review the account list monthly and prune dead handles.
