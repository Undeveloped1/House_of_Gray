# Vault-as-Brain Audit (2026-06-21)

Session-specific findings from a comprehensive workflow review of Paul's
memory protocols. The audit revealed that the "memory system" is actually
two conflated systems, and the file vault (System 2) — intended as an
Obsidian/NotebookLM-queryable brain — is not functioning as one.

## Vault Inventory

| Metric | Value |
|--------|-------|
| Total markdown files | 282 |
| Total vault size | 14 MB |
| `state.db` (conversation history) | 282 MB |
| Daily Handover files | 17 (5-20 through 6-19) |
| Session Context dirs | 19 dated folders |
| Wiki-links (`[[...]]`) in vault | **0** |
| Obsidian config (`.obsidian/`) | Present (set up at some point) |

## The Core Problem

Joe built the vault to be a "second brain" usable with Obsidian (linking,
graph, backlinks) and NotebookLM (AI querying across documents). The data
accumulated (282 files!) but three things are missing:

1. **No links.** Files reference each other by path ("see `workspace/...`")
   but not by `[[wiki-link]]`. Without links, Obsidian's graph and backlink
   features do nothing. The vault is a file browser, not a brain.

2. **Not on Joe's machine.** Obsidian runs locally. The vault is on the VPS.
   Syncthing syncs `paul-dropbox` (Cursor handoff) but NOT `docs/Paul/` (the
   vault). Joe can't open it in Obsidian without syncing it down.

3. **The pipeline broke.** No Daily Handover since 6-13. No new Session
   Context since 6-13. The vault stopped growing two weeks before this audit.

## Orphan / Duplicate Directory Structure

Three naming conventions coexist in `Brain/`:

- `Long-Term Memory/` (title case) — has Insights/, Lessons/, Patterns/,
  Project Notes/ subdirs. Referenced nowhere in protocols.
- `long_term_memory/` (snake_case) — has Lessons/, Patterns/, Project Notes/
  subdirs (empty). Referenced nowhere.
- `working_memory/` (snake_case, empty) — referenced nowhere.
- `Working Memory/` (title case) — has the stale `Current Working Memory.md`.
  Referenced by Working Memory Update Protocol.
- `Working_Memory.md` (root of Brain) — also exists, also stale (6-06).
- `SPARK.md` — SOUL says "replaces and absorbs" it. Still sitting in Brain/.

Nobody knows which is canonical because no protocol references the orphans.

## Session Context Directory — Half-Migrated

Protocol says `Session Context/YYYY-MM-DD/`. Newer entries comply
(2026-06-11/, 2026-06-12/, 2026-06-13/). But 20+ older entries are flat
files at the root (`Skiver_Complete_Set_v5_Final.md`, `2026-05-22_*.yaml`).
No migration was ever done. Mixed structure.

## Protocol Execution Gap (paper vs. practice)

| Protocol | Status on disk |
|----------|---------------|
| Daily Handover | Last real entry 6-13. 6-19 is a 955-byte stub. No 6-14 through 6-18. |
| Working Memory | Two files, both stale (6-04 and 6-06). Untouched 2+ weeks. |
| Archive | Directory created 5-20. **Empty.** Never executed. |
| Weekly Rollup | No `Archive/Weekly/` dir. **Never executed.** |
| Session Context Copies | Required section ("NOT optional"). Absent from 6-19 handover. |
| DREAM: markers | Zero in recent handovers. System designed 6-07, not used. |
| Kaizen Protocol | "DRAFT — pending Joe review" since 6-07. Referenced as ACTIVE in AGENTS.md. |
| Versioning | Convention defined in Kaizen. **Zero protocols have version numbers.** |

## "Never overwrite" vs "patch" contradiction

AGENTS.md hard rule: "Never overwrite existing files. New file every time."
Kaizen Protocol: "Patch the file — targeted edits, not rewrites." These
directly contradict. The never-overwrite rule was meant for design drafts
but is stated as blanket — meaning Paul literally cannot maintain protocol
files without breaking a hard rule. Needs a carveout: never overwrite
*working design docs*; protocol files are maintained in-place via patch.

## Actionable Fix List (prioritized)

### Fix the config first (root cause of duplicate identity)
- [x] Kill duplicate SOUL/AGENTS from prefill.json (done 2026-06-21)
- [x] Merge unique old AGENTS content into VPS Edition (done 2026-06-21)

### Fix the memory system
- [x] Rewire Memory Lifecycle Protocol from file-based to `memory()` tool store (done 2026-06-21)
- [x] Fix AGENTS.md memories path from orphan vault copy to real symlink (done 2026-06-21)
- [x] Remove orphan vault MEMORY.md (done 2026-06-21)

### Make the vault function as a brain (System 2 — not yet done)
1. **Sync the vault to Joe's laptop** — point Syncthing at `docs/Paul/` so it
   mirrors locally. Open that local copy in Obsidian.
2. **Start linking** — new Daily Handovers and docs use `[[wiki-links]]` to
   reference related docs. Existing docs get linkified over time.
3. **Fix the handover pipeline** — actually write Daily Handovers again so
   the vault keeps growing.
4. **For NotebookLM** — export the vault (or a subset) and upload. Or use an
   Obsidian AI plugin (Smart Connections) for local RAG.
5. **Clean up orphan directories** — delete `working_memory/`,
   `long_term_memory/`, `Working_Memory.md` root file, `SPARK.md`. One
   canonical location per concept.
6. **Migrate flat Session Context files** into dated subfolders, or accept
   the flat structure and update the protocol.
7. **Either run Archive + Weekly Rollup or delete them** — dead protocols
   are worse than no protocols.

### Fix the execution gap
- Add a Session Start checklist that's hard to skip (literal 3-item checklist
  with file path spelled out, not a paragraph).
- Reconcile compression threshold (pick one number: 60k or 80k, put in one place).
- Resolve "never overwrite" vs "patch" contradiction with a carveout.
- Decide git: does Paul commit or not? (Two AGENTS files disagreed — now
  resolved to one, which says Paul commits + pushes.)

## Joe's Answer (2026-06-21)

**Joe rejected the Obsidian/NotebookLM brain vision.** His exact words: "why
would I want to manually search Obsidian? The entire reason I want this memory
is so that when I say 'we're going to work on Trigger 4V' you already know
what I'm talking about, where to find the corresponding information and get up
to speed without me doing warmup docs and prompting."

The vault is NOT a browsable brain. Paul is the interface. The fix is not
wiki-links or Obsidian sync — it's Paul showing up ready. The dock/working-
state/corpus architecture (documented in the SKILL.md) and the RAG system
(vault_rag.py) are the actual solutions. The "make the vault function as a
brain" items below (wiki-links, Obsidian sync, NotebookLM) are MOOT — do not
pursue them.

The orphan directory and protocol execution gap findings below are still
valid and should be cleaned up.
