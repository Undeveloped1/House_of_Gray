# Lock Pass Reconciliation Procedure

When Joe makes design decisions in conversation that change card placements, renames, stat adjustments, or status changes — and those decisions are recorded in the Daily Handover but NOT written back to canonical files — the next session's first task is reconciliation.

## When This Applies

- Joe locked/moved/renamed cards in conversation
- Session ended before canonical files were patched
- Daily Handover records decisions; roster JSON / cascade roster / LIVE web are stale
- Or: Joe returns after a break and says "let's keep going where we left off"

## Procedure

1. **Load all canonical sources:**
   - `tools/card_scorer/roster_bruiser.json` (master roster)
   - `Bruiser_Cascade_Pass_Roster_*.md` (latest cascade roster)
   - `Bruiser_SYNERGY_WEB_LIVE.md` (slot map)
   - `Bruiser_Design_Bible.md` (design rules)

2. **Cross-reference against Daily Handover:**
   - Read the full handover for the last session
   - Identify every decision: renames, stat changes, V-band moves, rarity flips, status changes, new cards added, cards zeroed
   - Compare each against the canonical files

3. **Build a lock audit:**
   - **Locked** — cards Joe confirmed, no changes needed
   - **Decided but stale** — decisions not in canonical files
   - **Proposed** — cards Joe hasn't locked yet
   - **Open** — slots with no card assigned
   - **New** — cards named but not yet worked up

4. **Present cleanly:**
   - Table of what's actually locked (ground truth)
   - Table of decisions not yet in files
   - Table of what's still proposed
   - Flag count issues (over/under 33)

5. **Apply changes to NEW files:**
   - NEVER overwrite existing canonical files
   - Create new dated roster file (e.g., `Bruiser_Lock_Pass_Roster_2026-05-29.md`)
   - Create new scorer JSON (`roster_bruiser_lockpass.json`)
   - Log all changes in the changelog section

6. **Update Daily Handover:**
   - Append session work to the existing day's handover
   - List all files created/modified
   - Capture key decisions

## Pitfalls

- **Don't assume old files are current.** Always cross-reference against the handover first.
- **Don't overwrite.** New file every time. Joe will merge later.
- **Don't silently renumber.** If cards move between bands, keep original numbers and note the moves.
- **Flag overcount immediately.** If new names push past 33, say so before Joe locks anything.

## Example

Session Part 2 made these decisions in conversation: Leg Breaker→Hammer, Hammer→Bully, Smooth 4V→3V, Collector 3V→4V, Slab 6V→5V, Ringside→6V. None were written to `roster_bruiser.json`. The cascade roster still showed the old state. The next session's first task was reconciling all six changes against three stale canonical files — producing the Lock Pass Roster as a new file.
