# Cron Chaining — Post-Run Archival Scripts

Pattern used for Tabitha's Bible+Stoic cron: a no_agent cleanup script runs
shortly after the main agent cron to strip boilerplate and archive the clean
output.

## Problem

Agent-based cron jobs produce output wrapped in cron boilerplate (job ID,
timestamp, prompt echo). The user wants a clean archive without the cruft,
but adding file-write instructions to the agent prompt triggers the
verification-garbage injection bug.

## Solution — Offset Chaining

Two separate cron jobs, same profile, offset by a few minutes:

| Job | Type | Schedule | What |
|-----|------|----------|------|
| Main job | Agent | `0 11 * * *` | Generates content, delivers to user |
| Archive job | no_agent script | `5 11 * * *` | Reads latest output, strips header, saves clean copy |

## Archive Script Pattern

```python
#!/usr/bin/env python3
import os, re, glob

OUTPUT_DIR = '/path/to/cron/output/<job-name>'
ARCHIVE_DIR = '/path/to/archive'
STATE_FILE = '/path/to/.archive-state'  # prevents double-archiving

def main():
    files = sorted(glob.glob(os.path.join(OUTPUT_DIR, '*.md')))
    if not files:
        return  # silent — no delivery

    latest = files[-1]
    basename = os.path.basename(latest)

    # Track processed files to avoid re-processing
    last = None
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE) as f:
            last = f.read().strip()
    if last == basename:
        return  # already done

    with open(latest) as f:
        content = f.read()

    match = re.search(r'## Response\n(.+)', content, re.DOTALL)
    if not match:
        return

    clean = match.group(1).strip()
    out_path = os.path.join(ARCHIVE_DIR, f'{basename[:10]}.md')

    with open(out_path, 'w') as f:
        f.write(clean + '\n')

    with open(STATE_FILE, 'w') as f:
        f.write(basename)

if __name__ == '__main__':
    main()
```

## Key design decisions

- **Silent on no-op**: prints nothing (empty stdout = silent cron delivery) when
  already archived or nothing to process
- **State file**: tracks last-processed filename so re-triggers don't duplicate
- **No LLM**: runs as no_agent — fast, cheap, never hallucinates
- **Offset schedule**: 5 minutes after the main job leaves enough headroom

Live example at `/root/.hermes/scripts/bible-devotional-archive.py`.
