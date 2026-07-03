# Profile Migration — Moving Between Hermes Profiles

Moving the default profile (or any profile) into a new named profile, preserving
config, skills, memory, cron jobs, AND session history.

## Background: Profile Storage Layout

| Profile | Config/Skills/Memory | Session DB |
|---------|---------------------|------------|
| `default` | `~/.hermes/` (root) | `~/.hermes/state.db` |
| Named profiles | `~/.hermes/profiles/<name>/` | `~/.hermes/profiles/<name>/state.db` |

The `default` profile is the only one that stores everything in the root
`~/.hermes/` directory. All named profiles use `~/.hermes/profiles/<name>/`
with an identical subdirectory layout.

## What `hermes profile create --clone-all` Copies

```bash
hermes profile create <newname> --clone-all
```

Copies: `config.yaml`, `.env`, `SOUL.md`, `USER.md`, skills (profile-level),
memory entries, cron jobs, auth, gateway config, channel directory, pairing
data, plugins, pets, skins, workspace.

**Does NOT copy:** session history (`state.db`). The `--clone-all` flag
explicitly excludes "per-profile history."

## Full Migration (Config + Sessions)

### Step 1: Create the new profile

```bash
# From the active profile:
hermes profile create <newname> --clone-all

# Or from a specific source profile:
hermes profile create <newname> --clone-from default --clone-all
```

### Step 2: Copy sessions

**Critical: stop the gateway first.** The running gateway holds `state.db`
open (SQLite WAL mode). Copying while the gateway is running may produce an
incomplete snapshot.

```bash
hermes gateway stop                          # or: hermes --profile default gateway stop
cp ~/.hermes/state.db ~/.hermes/profiles/<newname>/state.db
```

SQLite WAL/SHM files (`state.db-wal`, `state.db-shm`) don't need copying —
SQLite recreates them on first open in the new location.

### Step 3: Switch

```bash
hermes profile use <newname>                 # sticky default for all future sessions
hermes --profile <newname>                   # one-off launch
```

### Step 4: Restart gateway under new profile (if used)

```bash
hermes --profile <newname> gateway start
```

## Verification

```bash
# Confirm sessions came over
hermes --profile <newname> sessions list
hermes --profile <newname> sessions stats

# Confirm config is correct
hermes --profile <newname> config

# Confirm memory loaded
hermes --profile <newname> chat -q "what do you know about me?"
```

## Gotchas

- **Gateway lock:** the running gateway holds `state.db` open. Stop it first or
  the copy may be incomplete. Verify with `hermes gateway status`.
- **Default profile stays intact:** this is a copy, not a move. The old profile
  remains fully usable.
- **Cross-profile skills:** skills in `~/.hermes/skills/` are shared across all
  profiles (global). Profile-specific skills live in
  `~/.hermes/profiles/<name>/skills/`. `--clone-all` copies profile-level ones
  but global skills are already available to the new profile.
- **Cron jobs:** `--clone-all` copies cron job definitions. If jobs reference
  profile-specific paths or delivery targets, review them after migration.
- **Large state.db:** the default profile's session database can grow large
  (100s of MB). Consider pruning before copying:
  ```bash
  hermes sessions prune --older-than 90   # drop sessions older than N days
  ```
- **Provider credentials:** if the profile uses OAuth tokens in `auth.json`,
  they are copied. API keys in `.env` are copied. Verify with
  `hermes --profile <newname> auth list`.
- **Running cron scheduler:** if cron is active on the source profile, the new
  profile's cron scheduler won't auto-start. Start it explicitly if needed:
  ```bash
  hermes --profile <newname> cron resume --all   # if supported; check `hermes cron --help`
  ```

## Related

- `vps-migration.md` — moving Hermes between machines
- `profile-isolation.md` — preventing cross-profile context bleed
- `ephemeral-profile-pattern.md` — zero-trace profiles
