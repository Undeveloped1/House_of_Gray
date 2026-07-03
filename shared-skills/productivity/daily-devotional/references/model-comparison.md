# Model Comparison via Cron Pin-Toggling

**Use case:** Compare two models on the same task (e.g., DeepSeek Pro vs Flash on a devotional or persona check-in) to decide which performs better for a specific class of work.

## Technique

The cron job's `model` parameter can be toggled between runs without touching the prompt or schedule. This lets you run the exact same task on two different models and compare outputs side by side.

### Steps

1. **Pin to Model A, run, capture output:**
   ```
   cronjob action=update job_id=<id> model='{"model":"deepseek-v4-pro","provider":"deepseek"}'
   cronjob action=run job_id=<id>
   ```
   Read output from `/root/.hermes/cron/output/<job_id>/<latest>.md`.

2. **Pin to Model B, run, capture output:**
   ```
   cronjob action=update job_id=<id> model='{"model":"deepseek-v4-flash","provider":"deepseek"}'
   cronjob action=run job_id=<id>
   ```

3. **Restore preferred model.**
   ```
   cronjob action=update job_id=<id> model=<preferred>
   ```

### What to compare

| Dimension | What to look for |
|-----------|-----------------|
| **Pairing quality** | Does the model find an inevitable thematic connection, or are the pairings forced/stretched? |
| **Reflection depth** | Are the questions probing or shallow? Do they create tension or just ask comprehension? |
| **Variety** | Does the model vary themes, books, and Stoics as instructed, or repeat patterns? |
| **Voice adherence** | Does persona work (Lyra, Nova) stay in character? |
| **Format compliance** | Does the model follow the output format exactly or introduce drift? |
| **Latency** | How fast does each model respond? |
| **Cache efficiency** | What % cache hit rate does each model show? |

### Real example: Bible+Stoic Devotional (2026-06-30)

Two runs on identical prompt, same cron:

**DeepSeek Pro:**
- Theme: "Stewardship and the Common Good"
- Scripture: 1 Peter 4:10 (ESV)
- Stoic: Marcus Aurelius, Meditations 8.59
- Reflection: 3 questions — including a sharp edge on enabling vs serving

**DeepSeek Flash (first run):**
- Theme: "The Thief of Time"
- Scripture: Ephesians 5:15-16 (ESV)
- Stoic: Seneca, On the Brevity of Life
- Reflection: 3 questions — shorter but landed harder ("6 months to live" question)

**Verdict:** Flash was ~90% of Pro for creative/devotional work. Handles format and structure fine; Pro edges ahead on unusual verse picks and sharper tension questions. For persona-driven check-ins (Lyra, Nova), Flash likely closes the gap since those are character/script delivery, not creative pairing.

### When to use

- Evaluating a new model tier (Pro vs Flash, Opus vs Sonnet)
- Testing whether a cheaper model can handle a task
- Before migrating cron jobs from one model to another
- Debugging quality complaints ("this was better last week")

### Pitfalls

- **Order bias:** Run model A first, then model B, to control for prompt freshness
- **Topic repetition:** On a devotional cron, the second run may pick a different theme because the first theme was "used" — this is a feature (more variety), not a confound
- **Output file overwrite:** Each `cronjob action=run` appends a new file; the latest is by timestamp
- **Config drift:** Ensure the job is pinned before running. An unpinned job on a drifted config will fail
