# Collaborative V-Band Resume (Partial Band)

Use when Joe says "continue [faction] [band]" or "new session on 4V" after prior beat-by-beat work.

## Source-of-truth order

1. **`/root/syncthing/paul-dropbox/{Faction}_Full_Set_v{N}.md`** — canonical locked cards (Cursor reads this).
2. **Workspace warmup** — e.g. `Trigger_4V_Band_Warmup_YYYY-MM-DD_Paul.md` — may lag; reconcile from Full Set before presenting state.
3. **`session_search`** — `{faction} {band} locked` — catches locks if handover/warmup stale (see Band Design — Session History Gate in SKILL.md).

Present **delta**: `N/M` at this band, which slots are open, next card — not full locked tables.

## Set progress math

- Bands 1–(n−1) complete + partial current band: e.g. 30 cards through 3V + 4 locks in 4V = **34/55**, band line **4/10**.
- Do not reprint locked card text; cite file path only.

## Paul Hermes Telegram forum

- Supergroup: **Paul Hermes** (`-1003748772302`).
- Hermes `channel_directory.json` lists **topic numbers only** (`topic 519`, etc.) — not Telegram's human topic titles.
- Handovers have documented **507**, **519** for other Trigger work; **band-specific threads are not reliably mapped in vault** unless logged at session close.

**At session close after forum work:** add to Daily Handover:

```text
**Source:** Telegram group "Paul Hermes" — thread <ID> ("<human title if Joe named it>")
```

**When resuming:** If Joe asks "do we have a topic to refresh?" — search handovers + `session_search` for thread ID. If none, say so honestly; offer **refresh existing topic Joe recognizes** or **new topic** with kickoff paste below.

## Kickoff paste (new topic or DM)

```text
Load five-crests and design-collaboration. Continuing Trigger 4V collaborative design — partial locks in /root/syncthing/paul-dropbox/Trigger_Full_Set_v7.md. Read Trigger_4V_Band_Warmup_2026-06-13_Paul.md. Beat-by-beat, character-first. Don't reprint locked cards — point to the file. Next open: M23 Management Rare (surgical intel, not Excommunicate).
```

Adjust faction, band, paths, and next open slot per session.

## Trigger 4V snapshot (2026-06-20)

**4/10 locked:** M20 Man at Arms, M21 Specter, M22 Trigger Man, M25 Bullet Time body.

**Open:** M23, M24, S09, S11, W03, W04.

Update this section when band completes or locks change.