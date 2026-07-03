# USER.md Format & Compression Technique

## Where it lives

For profile-based Hermes setups: `~/.hermes/profiles/<name>/memories/USER.md`

This is NOT the same as `~/.hermes/USER.md` (used by the default profile).

## Format

Plain prose, `§` (section sign, U+00A7) as entry delimiter. Each §-separated block
becomes a separate `memory()` user entry. Writing to this file auto-syncs to the
memory tool store — no manual `memory()` calls needed.

No markdown headers (`##`), no bullets (`-`), no blank lines between entries.
The file is injected into the system prompt's USER PROFILE section, not rendered
as a markdown document.

Example structure:
```
Joe (TheGreyBeard) — solo developer, lifelong creative. Facts about identity and background.
§
ADHD + light autism. Thinks in patterns. Communication preferences.
§
Windows PC with WSL/Ubuntu. Environment facts.
```

## Compression technique: markdown portrait → §-delimited prose

When a full narrative user portrait exists in markdown (headers, bullets,
blank lines), it can be condensed into the §-delimited injection format without
losing facts. The technique:

1. **Group related facts** — each § block covers one theme (identity, neurodivergence,
   environment, workflow, communication style, principles)
2. **Strip structure** — remove markdown headers, bullets, blank lines. Collapse
   into continuous prose.
3. **Eliminate redundancy** — if two sources say the same thing, merge once.
4. **Preserve all facts** — every sentence from the source survives. Nothing cut.

**Result:** 80-line markdown portrait → 11-line §-delimited file (~75% line
reduction), zero information loss. The memory tool auto-splits on `§` into
separate entries.

## The auto-sync behavior

When `memories/USER.md` is written to disk (via `write_file`), the `memory()`
tool immediately picks up the changes — each § block becomes a separate entry
in the user target. This was observed: writing a 6-block file produced 6
`memory()` user entries within the same session. No manual `memory()` calls
needed.

## Pitfalls

- **Don't use markdown in this file.** Headers, bullets, and blank lines are
  structural waste in a plain-text injection format. The system renders this as
  USER PROFILE text, not formatted markdown.
- **§ is the only delimiter.** Don't use other separators. The memory tool
  splits on `§` specifically.
- **Verify the right file.** Profile-based paths use `profiles/<name>/memories/`,
  not the root `~/.hermes/memories/`. Writing to the wrong path won't load.
