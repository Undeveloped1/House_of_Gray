# Profile Isolation — Preventing Cross-Profile Context Bleed

**Problem:** Hermes loads certain identity files (`AGENTS.md`, `SOUL.md`) from the root `~/.hermes/` directory regardless of which profile is active. This causes one agent's operating protocols or "soul" to leak into another profile's sessions (e.g., Paul's AGENTS.md appearing in an `abby` profile session).

**Root cause observed:** The context loader treats root-level files as global/project context and injects them at session start, even when `~/.hermes/profiles/<name>/` is the declared active profile.

**Solution pattern (2026-06-24 session):**

1. Create dedicated profile directories:
   ```bash
   mkdir -p ~/.hermes/profiles/paul
   mkdir -p ~/.hermes/profiles/abby
   ```

2. Move root-level identity files into the correct profile:
   ```bash
   mv ~/.hermes/AGENTS.md ~/.hermes/profiles/paul/AGENTS.md
   mv ~/.hermes/SOUL.md ~/.hermes/profiles/paul/SOUL.md
   ```

3. Create a profile-specific agents file inside the target profile (e.g. `Agents-Abby.md` or `AGENTS.md`) so the profile has its own context without inheriting the global one.

**Result:** After migration, only the `abby` profile's own files are visible to Abby sessions; Paul's files live exclusively under the `paul` profile.

**When to apply:**
- Multiple named agents/profiles exist on the same VPS
- User complains that one agent's rules or soul are appearing in another's sessions
- Before deploying a new subordinate agent (OpenClaw, secondary Hermes profile)

**Related patterns:** ephemeral-profile-pattern.md, post-migration-orientation.md

**Note:** The `docs/Paul/` vault and other agent-specific directories should also live under the profile when full isolation is required, or be explicitly symlinked/ignored by the loader.