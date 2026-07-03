# USER.md File-Auto-Sync Behavior

## Discovery (2026-07-02)

Writing directly to `memories/USER.md` (the on-disk file) immediately propagates
to the `memory()` tool's user store. The file gets split on `§` (section-sign)
delimiters into individual memory entries — no `memory(action='add',
target='user')` calls needed.

## The Fast Path

When doing a bulk user-profile update (merging, consolidating, rewriting):

1. **Write the file directly** — `write_file` to
   `~/.hermes/profiles/<name>/memories/USER.md` (profile-aware path) or
   `~/.hermes/memories/USER.md` (default profile).
2. **The tool syncs automatically** — each `§`-delimited section becomes a
   separate memory entry. No individual `memory()` calls required.
3. **Verify** — check the USER PROFILE section in the next system prompt, or
   call `memory(target='user')` to confirm entries loaded.

## Why This Is Better

- **Single write, not N tool calls.** Merging an 80-line portrait into a
  10-line concise file is one `write_file`. The old approach requires
  individual `memory(action='remove')` + `memory(action='add')` for each entry,
  risking char-limit rejection on individual ops.
- **Atomic.** The whole file lands at once — no partial-update window.
- **§ is the delimiter.** Structure your file with `§` between entries.
  They'll auto-split into individual memory entries.

## Worked Example

Session 2026-07-02: Joe wanted the full USER.md portrait (80 lines, from
`docs/Paul/memories/USER.md`) merged into the concise version loaded every
session (`memories/USER.md`, 10 lines, tooling-only). Consolidated both into
one file with `write_file` — tool auto-split into 6 entries at 1,922 chars.
Done in one step. No individual `memory()` calls.

## Profile-Aware Paths

| Profile | USER.md path |
|---------|-------------|
| Default | `~/.hermes/memories/USER.md` |
| Named (e.g., paul) | `~/.hermes/profiles/paul/memories/USER.md` |

The `memory-management` skill references `~/.hermes/USER.md` in its "Starting a
New Session" section — this path is correct for default-profile setups but NOT
for profile-aware setups. In profile mode, the actual loaded file lives under
`profiles/<name>/memories/USER.md`.
