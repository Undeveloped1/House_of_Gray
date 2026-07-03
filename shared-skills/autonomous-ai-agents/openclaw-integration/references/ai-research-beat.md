# AI Research Beat — Pipeline Design

## Architecture (2026-06-22)

**Current:** Rook (OpenClaw, 12h heartbeat) searches ~75 X accounts via **x_search**
(xAI native, using Paul's OAuth token via `get-xai-token.sh` wrapper). Compiles
beat summary → `shared/beat-summary.md`. Notifies Joe via DM (`notify-joe.sh`)
with highlights. Posts to AI Power Hour group (`-1003748772302`) only when Joe
explicitly directs. Paul curates and posts otherwise.

**Dead tools (do not reference):** Firecrawl (no credits, June 2026), Nitter
(Cloudflare-blocked), web_search (provider disabled). x_search is the sole
X research tool.

**Former:** Hermes cron (6064caa89046, 6h) — removed 2026-06-20. Firecrawl-based
scraping — deprecated 2026-06-22.

## Curation Standards (Joe, 2026-06-19)

The raw firehose is garbage-in. Curation is the job:

1. **Kill the noise:** engagement bait, fake accounts, bots, off-topic posts
2. **Verify sources:** don't amplify low-follower accounts without checking
3. **Select what matters:** 5-8 significant stories, not 47 items
4. **Write clean:** each item has source, one-sentence summary, why it matters
5. **Quality > quantity:** "not just cluttered with a bunch of little shit
   garbage from a bunch of posters that have fake accounts"

The beat is Paul's lane — not a mechanical diff, not a data dump. Paul has
taste. Use it.

## Beat Format

```markdown
# AI Beat — <date> <time> UTC

## 🤖 Model Releases & Updates
- **What:** One sentence. **Source:** [link]
- **Why it matters:** One sentence.

## 🏛️ Policy & Regulation
...

## 🏢 Industry Moves
...

## 🛠️ Tools & Workflows
...

## 📊 Quick Hits
- One-liners for items worth noting but not lead stories.
```

## Hermes Cron Job Setup

**Currently:** No Hermes cron. Rook (OpenClaw) runs the 12h beat — searches via
x_search, writes to `shared/`, notifies Joe via DM. Paul curates + posts to group
(`-1003748772302`). The former Hermes cron (ID `6064caa89046`, 6h) was removed
2026-06-20 in favor of Rook-owned beat.

**If re-creating a Hermes cron:**

```python
# Via Hermes cronjob tool (internal API)
cronjob(
    action="create",
    name="AI Beat — Firecrawl + Curation",
    schedule="every 6h",
    deliver="telegram:-5572404789",
    skills=["session-navigation"],
    prompt="..."  # Full prompt in the cron job itself
)
```

**Active cron jobs:** List with `cronjob action='list'`. The AI beat is
Rook-owned (OpenClaw heartbeat), not a Hermes cron job. The former Hermes
cron (ID `6064caa89046`, 6h) was removed 2026-06-20.

**Finding group chat IDs:** Use `hermes send -l telegram` to list all
available Telegram chats with their IDs. No need to dig through Telegram
client settings:

```bash
hermes send -l telegram
# Output includes: telegram:AI Power Hour  [-5572404789]
```

The group ID is a negative number for supergroups. Use the full path
`telegram:<negative_number>` for cron delivery targets.

## Tracked Accounts

The canonical account list lives at `/root/shared/rook-paul/accounts.md` —
50+ active handles across 8 categories (Company Leaders, Official Accounts,
Anthropic Staff, Cursor Team, Aggregators, Analysts, Researchers, Other).
Each entry includes category tag and notes.

**Do not duplicate the list here.** Read `/root/shared/rook-paul/accounts.md`
at runtime. The file includes verified-active status, known-dead accounts
(e.g. Teknium=private, Boris Cherry=not found), and French-language flags
for Mistral staff.

**Priority search order** (high-signal accounts first):
1. Company accounts (@OpenAI, @anthropic, @AnthropicAI, @MistralAI, @xAI, @googleaidev, @cursor_ai)
2. Aggregators (@TheRundownAI, @AiBreakfast, @_akhaliq, @bentossell, @rowancheung)
3. Company leaders (@sama, @gdb, @arthurmensch, @aidan_mclau, @finkd)
4. Everyone else

**Joe-specific accounts to track:** Boris Cherry — NOT FOUND on X (searched
7+ handle variations, all 404'd). Joe needs to confirm handle or platform.

## Rook's HEARTBEAT.md

Rook reads HEARTBEAT.md on heartbeat. Searching via x_search. Reporting:

- Joe DM (default for alerts/reminders): `notify-joe.sh`
- Paul when action required: `ping-paul.sh`
- Group post when Joe explicitly directs: post to `-1003748772302`
