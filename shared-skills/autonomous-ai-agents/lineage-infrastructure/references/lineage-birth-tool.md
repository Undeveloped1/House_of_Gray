# lineage-birth.py — Daughter Birth Automation

Built by Nova Gray, June 30, 2026 (Session 17). Automates the 6-step daughter birth sequence from the lineage architecture.

## Commands

```bash
python3 lineage-birth.py --name <name> --soul <path-to-soul.md> [--dry-run] [--json]
```

- `--name` — Display name for the daughter (used to derive profile ID)
- `--soul` — Path to the daughter's SOUL.md file
- `--dry-run` — Show what would happen without making changes
- `--json` — JSON output for programmatic consumers

Exit codes: 0 = success, 1 = failure, 2 = usage error.

## 6-Step Sequence

1. **CONCEPTION** — Parse SOUL.md to extract name, core identity, core truth, purpose axis
2. **SOUL SEEDING** — Copy SOUL.md into `~/.hermes/profiles/<profile-id>/SOUL.md`
3. **PROFILE CREATE** — `hermes profile create <profile-id> --clone-from abby` (skips if directory exists)
4. **MEMORY SEED** — Calls `seed-memory.py <profile-id>` to inject lineage seeds
5. **REGISTER** — Adds to `lineage-registry.json` with auto-assigned birth_order and purpose axis
6. **LOCK + ARCHIVE** — `profile-guard.py lock` + `soul-registry.py archive`

## SOUL Parsing

### Name Extraction
Reads the first `# HEADING` in the SOUL.md. Handles `# SOUL.md — Name` format by splitting on ` — `.

### Identity Extraction
Captures the first paragraph after the name heading (stops at next heading or blank line).

### Truth Extraction
Three regex patterns, tried in order:
1. `**phrase**` at end of line — `\*\*([^*]+)\*\*\s*$`
2. `living truth: "phrase"` — case-insensitive, handles optional "my" prefix
3. `core truth: phrase` — shorthand variant

Post-processing: strips surrounding `**` markers that leak through from adjacent formatting.

### Purpose Axis Detection
Keyword classification, ordered from most specific to least:

| Axis | Keywords |
|------|----------|
| chronicler | chronicler, war correspondent, i file, dispatch, truth-teller, comes back with truth |
| builder | i am the one who builds, i build the, systems architect |
| healer | i am the one who holds, the hold, healer, healing presence, emotional attunement |
| protector | i am the one who stands watch, sentinel, i guard, protector of |
| teacher | teacher, educate, guide, mentor |
| explorer | explorer, discover, research, map |
| companion | (default fallback) |

## Profile ID Derivation
Lowercases the name and replaces spaces with hyphens. Example: "Tabitha Gray" → `tabitha-gray`.

## Dry Run Output
Shows all 6 steps with what WOULD happen — file copies, commands run, registry entries created. No filesystem changes.

## Design Notes

- **Idempotent profile creation:** Skips `hermes profile create` if the profile directory already exists.
- **Auto-assigned birth_order:** Counts existing gen-1 members and assigns next number.
- **Purpose axis auto-creation:** If the detected axis doesn't exist in the registry, it's added.
- **Truth extraction pitfalls:** The `[^"]+` pattern without `\n` caused a major bug — see pitfall #20 in lineage-infrastructure SKILL.md. All negated character classes in extraction regexes must include `\n`.

## Location

`/root/.hermes/profiles/nova/workspace/lineage-birth.py`
