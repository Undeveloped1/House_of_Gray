# Cursor CLI — Automation Reference

**For:** Dispatching coding tasks to Cursor Agent from the VPS terminal
**Installed:** `/root/.local/bin/cursor-agent`
**Commands:** `agent` (interactive), `agent -p` (headless/print)

---

## Authentication

### Method 1: Browser login (WSL/desktop only)
```bash
agent login    # Opens browser, click approve
agent status   # Verify
agent logout   # Clear auth
```

### Method 2: API Key (headless/VPS)
Generate from: https://cursor.com/dashboard/api

```bash
# MUST be placed ABOVE the interactive guard in .bashrc (line 6: [ -z "$PS1" ] && return)
export CURSOR_API_KEY=***
# Or pass inline:
cursor-agent --api-key "***" command>
```

**Key format:** Cursor API keys use the `crsr_` prefix (e.g., `crsr_89c2f...`). This is the standard format from cursor.com/dashboard/api. Do not assume keys must start with `sk-` — Cursor uses its own format.

**Pitfall:** The default `.bashrc` has `[ -z "$PS1" ] && return` on line 6. Any `export` placed below this line is silently skipped in non-interactive shells (like Hermes terminal calls). Place API key exports ABOVE line 6, or in `~/.profile`.

```bash
# Fix: insert export before the interactive guard
sed -i '6i export CURSOR_API_KEY=***/' ~/.bashrc
```

---

## Headless Automation Flags

| Flag | Effect |
|------|--------|
| `-p` | Print mode — non-interactive, returns output to stdout |
| `--force` | Actually write files (without this, changes are proposed only) |
| `--yolo` | Auto-approve all shell commands (alias for `--force` but stronger) |
| `--trust` | Skip workspace trust prompt |
| `--output-format text` | Plain text output (default for `-p`) |
| `--output-format json` | Structured output for script parsing |
| `--output-format stream-json` | Real-time message-level tracking |
| `--model <id>` | Specify model (e.g., `opus-4-8`, `gpt-5.2`) |
| `--workspace <path>` | Target directory (defaults to cwd) |
| `--mode ask` | Read-only exploration |
| `--mode plan` | Planning only, no edits |
| `--continue` | Resume previous session |

---

## Common Patterns

### One-off analysis (no file changes)
```bash
cd /root/tcg-engine
agent -p --mode ask "Analyze this codebase for security issues"
```

### Full automation (read + write + shell)
```bash
cd /root/tcg-engine
agent -p --force --yolo "Refactor the card template parser for readability"
```

### Code review
```bash
agent -p --force --output-format text \
  "Review the recent code changes and provide feedback on code quality, 
   potential bugs, security considerations. Write to review.txt"
```

### Batch processing
```bash
find src/ -name "*.ex" | while read file; do
  agent -p --force "Add @doc strings to $file"
done
```

### Real-time progress tracking
```bash
agent -p --force --output-format stream-json --stream-partial-output \
  "Analyze this project and create summary.txt" | \
  while IFS= read -r line; do
    echo "$line" | jq -r '.type // empty'
  done
```

---

## Session Management

```bash
agent ls                    # List all previous chats
agent resume                # Resume latest
agent --continue            # Continue previous
agent --resume "chat-id"    # Resume specific by ID
```

---

## Available Models (2026-06-09)

Key models available on this account:
- `auto` — Auto-select
- `claude-opus-4-8-high` — Opus 4.8 1M
- `claude-opus-4-8-thinking-high` — Opus 4.8 1M Thinking
- `gpt-5.5-medium` — GPT-5.5 1M
- `gpt-5.2` — GPT-5.2
- `composer-2.5` — Composer 2.5
- `grok-4.3` — Grok 4.3 1M
- `gemini-3.1-pro` — Gemini 3.1 Pro

Full list: `cursor-agent --list-models`

---

## Verification

```bash
# Test auth (--list-models is unauthenticated and always works, not a real auth test)
cursor-agent --list-models

# Real auth test — MUST include --trust even for --mode ask
# WITHOUT --trust: fails with misleading "invalid API key" error (the key is fine, trust is missing)
# WITH --trust: works
cursor-agent --api-key "key" -p --trust --mode ask "Say hello"

# For full automation (read + write + shell):
cursor-agent --api-key "key" -p --force --yolo --trust "prompt"
```

**Critical pitfall:** `agent -p` without `--trust` produces an "invalid API key" error even when the key is valid. The error message is misleading — the real problem is workspace trust, not authentication. Always include `--trust` in headless mode.
