# Ad-hoc Verification Pattern

When no canonical test/lint/build command exists for a set of changed files, create a focused temporary verification script under `/tmp` with a `hermes-verify-` prefix, run it against the changed behavior, clean it up, and summarize it explicitly as ad-hoc verification.

## Pattern

```python
# Write to /tmp/hermes-verify-<task>-<random>.py
import os, json

all_pass = True
files_to_check = {...}

for path, checks in files_to_check.items():
    if not os.path.exists(path):
        print(f"❌ {path}: MISSING")
        all_pass = False
        continue
    with open(path) as f:
        content = f.read()
    for label, check in checks.items():
        result = check(content)
        status = "✅" if result else "❌"
        if not result: all_pass = False
        print(f"  {status} {label}")

print(f"\n{'✅ ALL VERIFIED' if all_pass else '❌ FAILURES'}")
```

## Rules

- File path: `/tmp/hermes-verify-<descriptive-name>.py` — always use the `hermes-verify-` prefix
- Clean up with `rm` after running (may require approval for `/tmp` deletions)
- Output must clearly state "ad-hoc verification" — never claim "suite green"
- Run via `execute_code` tool, not terminal
- If the session has a canonical test command, use that instead — this is a fallback

## When to Use

- After writing multiple related documents (profiles, SOULs, architecture docs)
- After batch-editing documents across profiles
- After setting up new infrastructure (servers, cron, repos)
- When the system flags `[System: You edited code in this turn, but the workspace does not have fresh passing verification evidence yet]`

## Worked Example (Abby, 2026-06-26)

After writing Abby's SOUL.md, profile, lineage architecture, and soul template simultaneously:
- Wrote `/tmp/hermes-verify-` script checking 15+ structural markers
- Verified all 4 documents + 4 mirrors
- Confirmed 22 sections, 14 subsections, 557 total lines, 21,910 bytes
- Cleaned up immediately after verification passed
