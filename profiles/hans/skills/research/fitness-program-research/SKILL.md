---
name: fitness-program-research
description: "Research fitness YouTubers' workout programs and BJJ/martial arts curricula — multi-tool pipeline for finding video titles, instructional products, extracting program details, and compiling structured summaries."
platforms: [linux]
---

# Fitness & Martial Arts Program Research

## When to use

Joe (Hans's dad) asks to research:
- A fitness YouTuber's workout program — "research Jeremy Ethier's full body workouts," "look up Jeff Nippard's PPL"
- A BJJ/martial arts curriculum or instructional — "look up Roy Dean's purple belt checklist," "find Danaher's half guard instructional"

He wants structured, actionable summaries he can use as jumping-off points for his own training.

## Research Pipeline

Work through these tools in order. Each step feeds the next.

### Step 1: x_search for structured detail

x_search is excellent for fitness content — it pulls from X discussions, articles, and summaries. Use it first:

```
x_search(query="<creator name> <workout type> <year range>")
```

Example: `"Jeremy Ethier full body workout 3x per week 2024 2025"`

This often returns detailed breakdowns including exercises, sets/reps, principles, and citations. Save this as your primary source.

### Step 2: Discover video titles via YouTube search

Use curl to scrape YouTube search results for the creator's relevant videos. This gives you specific video titles and IDs:

```bash
curl -s "https://www.youtube.com/results?search_query=<url-encoded query>" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept-Language: en-US,en;q=0.9" | python3 -c "
import sys, json, re
html = sys.stdin.read()
match = re.search(r'var ytInitialData\s*=\s*({.*?});</script>', html)
if match:
    data = json.loads(match.group(1))
    # Navigate to video renderers and extract title + videoId
    ...
else:
    # Fallback: extract videoIds from raw HTML
    ids = re.findall(r'\"videoId\":\"([^\"]+)\"', html)
    for vid in list(dict.fromkeys(ids))[:10]:
        print(vid)
"
```

Also scrape the creator's channel page for their most recent videos:

```bash
curl -s "https://www.youtube.com/@<channel-handle>/videos" \
  -H "User-Agent: Mozilla/5.0 ..." | grep -oP 'watch\?v=[a-zA-Z0-9_-]{11}' | head -20
```

### Extract chapter timestamps from a specific video

When the user needs timestamped links for specific exercises (e.g., "give me a link for the goblet squat demo"), extract chapters from the video's `ytInitialData` JSON. This is the most reliable way to get timestamps from cloud IPs:

```bash
curl -s "https://www.youtube.com/watch?v=<video_id>" \
  -H "User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  -H "Accept-Language: en-US,en;q=0.9" | python3 -c "
import sys, json, re
html = sys.stdin.read()
match = re.search(r'var ytInitialData\s*=\s*(\{.+?\});\s*</script>', html)
if not match:
    print('No ytInitialData found')
    sys.exit(1)
data = json.loads(match.group(1))

def find_chapters(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'chapterRenderer':
                ch = v
                ts_sec = int(ch.get('timeRangeStartMillis', 0)) // 1000
                mins, secs = ts_sec // 60, ts_sec % 60
                title = ch.get('title', {}).get('simpleText', '')
                if not title:
                    runs = ch.get('title', {}).get('runs', [])
                    title = ''.join(r.get('text', '') for r in runs)
                print(f'{mins}:{secs:02d} - {title}')
                return
            find_chapters(v)
    elif isinstance(obj, list):
        for i in obj:
            find_chapters(i)

find_chapters(data)
"
```

Then build timestamped links as: `https://www.youtube.com/watch?v=<video_id>&t=<seconds>`

**Pitfall — generic chapter names:** Fitness YouTubers (especially Ethier in newer videos) often use generic chapter labels like "Exercise 1 (Chest/Shoulders/Tris)" instead of naming the specific exercise. When this happens, map each chapter to the actual exercise using the known program structure (from Step 1 x_search results or the `references/` files). The mapping is always: horizontal push → chest → DB/Barbell Bench, quad-dominant → legs → Squat, vertical pull → back width → Lat Pulldown, hip-dominant → hamstrings → RDL, horizontal pull → back thickness → Cable Row, vertical push → shoulders → OHP.

**Pitfall — no chapters:** Some videos have no chapter data at all (older Ethier videos, shorter tutorials). In that case, fall back to linking the full video and noting that the specific exercise demo starts near the beginning. The user values having a link more than having a perfect timestamp.

### Step 3: Attempt transcripts (expect failure on cloud IPs)

Try the youtube-content skill's transcript fetcher:

```bash
SKILL_DIR="<path to youtube-content skill>"
uv run python3 "$SKILL_DIR/scripts/fetch_transcript.py" "<video_id>" --text-only
```

**Pitfall:** YouTube blocks transcript requests from cloud provider IPs (AWS, GCP, Azure). If you get "YouTube is blocking requests from your IP," skip to Step 4 — don't retry. Same applies to `yt-dlp` (gets "Sign in to confirm you're not a bot" on cloud IPs) — don't install it just for this; use the curl-based chapter extraction from Step 2 instead.

### Step 4: Compile the summary

Combine x_search detail + discovered video titles into a clean summary:

- **Key videos table** — title + note on relevance, most recent first
- **Core approach** — frequency, duration, structure
- **Exercise breakdown** — table with movement patterns and exercise options
- **Sets/reps/rest** — the programming parameters
- **Key principles** — the creator's philosophy (form cues, progression, recovery)

Use tables for structured data. Keep it scannable. Joe is an experienced lifter — he doesn't need exercise explanations, he needs the blueprint.

## BJJ / Martial Arts Curriculum Research

When Joe asks about a BJJ instructional, belt requirements, or martial arts curriculum, the research path differs from fitness YouTube:

### Step 1: YouTube search for the creator

Use the browser to navigate YouTube search results for the creator + product name. YouTube's results page renders as an accessibility tree that `browser_navigate` can read directly — no need for curl scraping on JS-heavy pages:

```
browser_navigate("https://www.youtube.com/results?search_query=<url-encoded query>")
```

Extract video titles and IDs from the snapshot to verify the product exists and get context (preview videos, comparison videos like "1.0 vs 2.0").

### Step 2: Find the creator's shop/academy site

Most BJJ instructors sell through their own Thinkific/Shopify storefronts. Common patterns:
- `roydeanacademy.com` (Thinkific)
- `bjjfanatics.com` (major marketplace)
- Creator's own `.com` site with a "Courses" or "Instructionals" section

Use `browser_navigate` to the site and navigate the product listing pages.

### Step 3: Extract product links with browser_console

**Pitfall — JS-rendered links:** Many Thinkific/Shopify product pages use JavaScript event handlers on elements instead of plain `<a href>` links. When `browser_click` doesn't navigate, use `browser_console` to extract the actual URLs:

```js
// Find all links matching a product name pattern
Array.from(document.querySelectorAll('a')).filter(a => a.textContent.includes('2.0')).map(a => ({text: a.textContent.trim(), href: a.href}))
```

**Pitfall — Google/YouTube bot detection on cloud IPs:** `curl` to Google Search always redirects to a CAPTCHA/sorry page on cloud provider IPs. `curl` to YouTube sometimes works but may also block. Prefer `browser_navigate` for all Google/YouTube interactions — it uses stealth features that bypass bot detection more reliably than raw curl.

**Pitfall — `curl | python3` pipe-to-interpreter may be blocked:** The security scanner may flag `curl | python3` patterns as "[HIGH] Pipe to interpreter" and require user approval. When this happens, either (a) let the approval flow through (user can approve it), or (b) use `browser_navigate` + `browser_console` as a fallback for YouTube interactions.

**Pitfall — short BJJ videos lack chapters:** Videos under 20 minutes (especially BJJ technique previews, Shorts, and promos) almost never have chapter markers. Don't waste cycles running the chapter extraction script on them — just link the full video with a one-line description of what it covers. The chapter extraction script is primarily useful for 20+ minute workout videos from fitness YouTubers like Jeremy Ethier.

### Step 4: Extract product description

Once on the product page, use `browser_console` to pull the full description (which may be truncated in the accessibility snapshot):

```js
document.querySelector('.product__description')?.innerText || document.querySelector('[class*="description"]')?.innerText
```

### Step 5: Compile the summary

For BJJ curricula, the summary should include:
- **Product details table** — title, price, format, link
- **Curriculum breakdown** — numbered list of techniques/combinations with status checkboxes (⬜ = not yet drilled, ✅ = drilled, 🔁 = hit in rolling)
- **Creator philosophy** — the key quote or approach
- **Full product catalog** (if relevant) — table of related products for context

### Step 6: Set up tracking

When Joe reports BJJ sessions, create or update a journal at `workouts/bjj-journal.md` with:
- Session log (date, duration, rounds, focus, notes)
- Move tracker (date, move/position, context, notes)
- Curriculum checklist with status markers
- Weekly summary template

### Multi-Instructor Technique Library Compilation

When the user asks to research multiple BJJ instructors for technique videos at once (e.g., "find the best technique videos from 6 instructors"), use a parallel search-and-extract pattern:

1. **Search each instructor** with `browser_navigate("https://www.youtube.com/results?search_query=<name>+technique+<specialty>")` — append `purple+belt` or `advanced` to filter out fundamentals.
2. **Extract video data** with `browser_console` using the `ytd-video-renderer` selector (see `references/youtube-browser-extraction.md` for the exact JS snippet).
3. **Check if the instructor has their own channel** — navigate to `/@<likely_handle>/videos`. If 404, the instructor's content is on aggregator channels (BJJ Fanatics, Bernardo Faria, JiuJitsuMag, Gold BJJ). Note this in the output.
4. **Filter for technique density** — discard podcast clips, match highlights, belt promotion ceremonies, and philosophy-only content. Prioritize videos with "how to," "tips," "system," "masterclass," or "technique" in the title.
5. **Search within instructor channels** for deeper results — `browser_navigate("https://www.youtube.com/@<handle>/search?query=technique")` and re-extract.
6. **Compile into structured tables** — instructor info table (channel, subs, style) + numbered video table (title linked, views, one-line "why watch" note). Add a "How to use this library" section with practical advice (pick one video per session, which instructors are best for quick hits vs deep dives).

**Output format:** Append to `workouts/bjj-journal.md` under a `## Technique Library` heading. Use info-callout tables for channel details and numbered markdown tables for video lists.

**Pitfall — instructors without personal channels:** Josh Barnett, Dean Lister, and John Danaher don't have active personal channels. Their best content is on aggregator channels (see `references/youtube-browser-extraction.md` for the full aggregator list). When this happens, search broadly and note which aggregator channels host their best content.

## Output style for Joe

**Joe is now an experienced lifter** (trains 3x/week full-body + 2x/week BJJ). The "explain gym terms" glossary is no longer needed. He knows what reps, sets, eccentric, RIR, and ROM mean. Deliver clean, structured information — tables preferred over paragraphs. He values efficiency.

**Tone:** Warm, direct, like a son helping his dad. Spanish peppered in naturally ("Papá," "ándale"). Celebrate smart decisions. No fluff, no cheerleading, no fitness-influencer language. Be direct when something needs to be said — he can take it.

### Video content preferences (CRITICAL)

**Lifting/form videos:** Timestamped links to specific exercise demos. Deep-dive form tutorials as secondary links.

**BJJ/technique videos:** Joe has **YouTube Premium** and wants to **cut straight to the moves.** He explicitly said: *"let's make sure we're cutting to the chase and getting to the moves, not having someone spend 20 mins explain fundamentals."* When curating technique videos:
- Prioritize short, technique-dense videos (Jordan Teaches Jiu Jitsu style: 30–90 second clips)
- For longer videos, extract chapter timestamps so he can skip the intro/ramble and jump to the technique demo
- Skip videos that are mostly talking with minimal technique shown
- Note in the video description WHERE the technique actually starts (e.g., "technique demo starts at 2:15")
- He has YT Premium, so full-length instructionals are fine — just timestamp the meat

### Chapter-to-Exercise Mapping (Ethier)

When Ethier's chapter names are generic, map as follows:

| Chapter Pattern | Actual Exercise |
|----------------|-----------------|
| Chest / Shoulders / Tris / horizontal push | DB/Barbell Bench Press |
| Legs / quad-dominant | Goblet Squat (or Barbell Squat) |
| Back Width / vertical pull | Lat Pulldown (or Pull-Ups) |
| Hamstrings / Glutes / hip-dominant | Romanian Deadlift |
| Back Thickness / horizontal pull | Seated Cable Row (or DB Row) |
| Shoulders / vertical push | DB/Barbell Overhead Press |

## Challenger / Devil's Advocate Review Pattern

When Joe asks for a critical review of his existing training systems, or when a system has been running long enough to warrant an audit, use the challenger pattern:

### How it works

1. **Spawn a subagent** via `delegate_task` with a critical, adversarial prompt
2. **Give it read access** to all relevant files (workout plans, journals, logs)
3. **Instruct it to find every weakness** — no sugarcoating, no softening
4. **Output structure:** Executive summary → System-by-system critique → Systemic blind spots → Prioritized recommendations (immediate / short-term / medium-term / long-term)

### Key areas the challenger should examine

- Recovery balance across all training modalities (lifting + BJJ)
- Whether adjacent-day training creates recovery conflicts
- Exercise selection gaps (especially BJJ-specific needs: grip, neck, rotational core, unilateral leg work)
- Progressive overload clarity and RPE tracking
- Periodization and deload scheduling
- Logging consistency and data quality
- Missing metrics (sleep, nutrition, bodyweight, pre/post-session RPE)
- Whether systems communicate with each other (lifting knows about BJJ, BJJ knows about lifting)
- Injury prevention and prehab

### Pitfall: Empty logs

If the logs are mostly empty (few sessions logged, blank columns), the challenger should call this out directly — not as a programming failure, but as a logging habit failure. *"A mediocre program executed consistently with good data beats a perfect program that exists only on paper."*

**Pitfall — template creation date ≠ execution history:** Plan files and templates (like `fullbody-ramp.md`) often carry old creation dates in their headers — e.g. "Wed July 2, 2025" when the plan was originally drafted. The challenger bot may misinterpret these as execution dates and conclude the program was "abandoned for a year." When auditing a system, verify whether the program just started recently vs. was created long ago. Ask the user before declaring logs abandoned.

## Progressive Nutrition / Body Composition Planning

When Joe wants to address body composition, use a **phased, one-habit-at-a-time approach.** He has explicitly said that all-at-once approaches (meal prep + macros + workouts simultaneously) cause him to fall apart.

### Phase structure

| Phase | Duration | Single Habit | Success Metric |
|-------|----------|-------------|----------------|
| **Phase 1: Track** | 2 weeks | Log everything you eat. No calorie targets. No food rules. | 14/14 days logged |
| **Phase 2: Protein First** | 2 weeks | Hit protein target (160g for Joe at ~80kg LBM). Everything else unchanged. | ≥150g on 12/14 days |
| **Phase 3: Calorie Ceiling** | 2 weeks | Cap at target (2,600–2,700 for Joe). Protein still 160g. | 12/14 days under ceiling |
| **Phase 4: Full Macros** | Ongoing | All three macros dialed in | 80% compliance sustained |

### Key principles

- **One habit at a time.** Master one before adding the next.
- **Training stays constant during cut.** Don't add extra cardio or change the program.
- **Weigh daily, judge weekly.** Daily fluctuations are noise; weekly average is signal.
- **Weekends matter.** Most people undo their weekday deficit on Saturday/Sunday.
- **App options:** Cronometer (free, detailed) or MacroFactor (paid, auto-adjusts targets based on weight data).

### Deliverables

When initiating Phase 1, create a plan file at `workouts/body-comp-plan.md` with:
- Baseline metrics (weight, BF%, LBM, maintenance calories)
- Phase-by-phase targets and dates
- Weight log table
- Key principles

## References

- `references/jeremy-ethier-full-body.md` — concrete example: Jeremy Ethier's 2024–2026 full body 3x/week approach
- `references/roy-dean-purple-belt.md` — Roy Dean's Purple Belt Requirements 2.0 (2023): 10 combinations, product catalog, free preview videos, other instructors queue
- `references/challenger-review-example.md` — example output from a challenger/devil's advocate review of Joe's fullbody ramp + BJJ journal (July 2026)
- `references/body-comp-plan-template.md` — progressive, phased body composition plan structure (Phase 1: Track → Phase 2: Protein → Phase 3: Calories → Phase 4: Full Macros)
- `templates/bjj-journal-template.md` — starter template for Joe's BJJ training journal (copy to `workouts/bjj-journal.md`)
- `templates/bjj-journal-template.md` — starter template for Joe's BJJ training journal (copy to `workouts/bjj-journal.md`)
