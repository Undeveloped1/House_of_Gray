# YouTube Video Extraction via browser_console

Use `browser_navigate` to land on a YouTube search results page or channel page, then extract video data with `browser_console`. This is faster and more reliable than reading accessibility snapshots for bulk extraction.

## Working JavaScript selectors

### Search results page (`/results?search_query=...`)

The working renderer is `ytd-video-renderer` — NOT `ytd-rich-item-renderer` (returns empty):

```js
(() => {
    const results = [];
    document.querySelectorAll('ytd-video-renderer').forEach(item => {
        const titleEl = item.querySelector('#video-title');
        const viewsEl = item.querySelector('#metadata-line span:first-child');
        const timeEl = item.querySelector('#metadata-line span:nth-child(3)');
        const channelEl = item.querySelector('ytd-channel-name a');
        if (titleEl) {
            const m = (titleEl.href || '').match(/[?&]v=([a-zA-Z0-9_-]{11})/);
            results.push({
                title: titleEl.textContent.trim(),
                videoId: m ? m[1] : '',
                views: viewsEl?.textContent.trim() || '',
                age: timeEl?.textContent.trim() || '',
                channel: channelEl?.textContent.trim() || ''
            });
        }
    });
    return results;
})()
```

### Channel page (`/@handle/videos`)

For channel pages, the renderer is `ytd-rich-item-renderer`. Extract from the more generic `a[href*="watch?v="]`:

```js
(() => {
    const results = [];
    document.querySelectorAll('a[href*="watch?v="]').forEach(a => {
        const m = a.href.match(/[?&]v=([a-zA-Z0-9_-]{11})/);
        if (m && a.textContent.trim()) {
            results.push({title: a.textContent.trim(), videoId: m[1]});
        }
    });
    return results.slice(0, 30);
})()
```

Note: `a#video-title-link`, `a#video-title`, and `a.ytd-rich-grid-media` may also work but `a[href*="watch?v="]` is the most reliable fallback.

### Channel search (`/@handle/search?query=...`)

Works the same as search results — use `ytd-video-renderer`.

## Extracting subscriber count

Look for the channel info block in the search results or channel page snapshot. It appears as: `"@handle•XXX subscribers"`

Alternatively, navigate to `/@handle/about` and read the subscriber count from the snapshot.

## Known aggregator channels (BJJ instructors without personal channels)

Many BJJ legends don't run their own YouTube channels or have inactive ones. Their best technique content lives on these aggregators:

| Aggregator Channel | Handle | Common Instructors |
|---|---|---|
| Bernardo Faria BJJ Fanatics | @BernardoFariaBJJFanatics | Gordon Ryan, John Danaher, Craig Jones |
| BJJ Fanatics | @BJJFanatics | Gordon Ryan, John Danaher, Dean Lister |
| JiuJitsuMag | @JiuJitsuMag | Josh Barnett, various |
| Gold BJJ | @GoldBJJ | Dean Lister |
| Scientific Wrestling | @ScientificWrestling | Josh Barnett |
| Less Impressed More Involved | @LessImpressedMoreInvolved | Gordon Ryan (match analysis) |
| Grapplers Paradise | @GrapplersParadise | Dean Lister |

When researching these instructors, search YouTube broadly (`/results?search_query=<name>+technique`) rather than navigating to their personal channel — the best content will be across multiple channels.

## Video type filtering for technique density

YouTube search results for BJJ instructors mix several content types. Filter aggressively:

| Type | Keep? | Why |
|---|---|---|
| Technique instruction / breakdown | ✅ YES | The target content |
| Rolling commentary with technique analysis | ✅ YES | If it includes instruction, not just match footage |
| Full seminars / masterclasses | ✅ YES | Long-form, chaptered — ideal |
| Podcast clips (Lex Fridman, etc.) | ❌ NO | Philosophy, not technique |
| Match highlights | ❌ NO | No instruction |
| Promo / Shorts under 30 sec | ❌ DEPENDS | Only if technique-dense (Jordan Teaches Jiu Jitsu style) |
| "How to" / "tips for" titled videos | ✅ YES | Usually pure technique |

## Chapter extraction reminder

Videos with chapters show a "N chapters" button in the accessibility snapshot. Long-form BJJ videos (20+ min, especially masterclasses) often have chapter markers. Extract them for timestamped links — use the `ytInitialData` curl approach from the main skill's Step 2.
