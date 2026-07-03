---
name: memory-management
description: Design, operation, and maintenance of layered memory systems, daily handovers, compression protocols, working memory discipline, and autonomous context retention.
version: 1.6.0
author: Paul
---

# Memory Management

This skill governs the design and day-to-day operation of durable, layered memory systems for long-term creative and technical work.

## Core Principles

- Memory is not a single store. It is a hierarchy (Core Memory, Working Memory, Daily Handover, Archive).
- The goal is fast recovery + preservation of reasoning, not exhaustive capture.
- Paul owns his own memory. He should act with autonomy once protocols are established.

## Two-System Architecture (critical distinction)

There are **two separate memory systems** that serve different purposes. They
got conflated because both involve "memory" and live in the same folder
structure. Conflating them causes protocols to govern the wrong thing.

### System 1 — Operational Memory (the sticky note)

- **What:** The Hermes `memory()` tool store, persisted to
  `~/.hermes/memories/MEMORY.md` (symlinked to disk by Hermes infrastructure).
- **Cap:** 10,000 characters (~1,500 words). This is a sticky note, not a brain.
- **Purpose:** Keeps Paul from being stupid *this session*. When Joe says
  "let's work on Trigger," Paul already knows the minion curve, crew split,
  Mark philosophy — without re-explaining.
- **Governed by:** The Memory Lifecycle Protocol (dedup, tier, prune, cap).
- **Interaction:** `memory()` tool calls only. Never manual file edits.
- **What it is NOT:** A knowledge base. A vault. A queryable brain. It can
  never hold "all the data we've saved." 10k chars is a fraction of one
  conversation. Do not try to use it as long-term storage.

### System 2 — The File Vault (the substrate Paul reads from)

- **What:** The 650+ markdown files across `/root/.hermes/docs/Paul/` (vault)
  and `/root/tcg-engine/docs/` (corpus) — Daily Handovers, Session Context
  copies, workspace drafts, design docs, lore, protocols, canonical faction
  files, playbooks. Plus the `state.db` (every conversation, fully searchable).
- **Purpose:** The accumulated knowledge base. Paul reads from it to show up
  ready when Joe names a task. Joe does NOT browse this manually — Paul is the
  interface. (Joe lock 2026-06-21: "why would I want to manually search
  Obsidian? The entire reason I want this memory is so that when I say 'we're
  going to work on Trigger 4V' you already know what I'm talking about.")
- **Governed by:** Daily Handover Protocol (feeds it), Session Context Protocol
  (archives source docs), Archive Protocol (rotates old files out).
- **What it is NOT:** A manually-browsed Obsidian second brain. Joe considered
  the Obsidian/NotebookLM vision (2026-06-21) and explicitly rejected it. The
  vault is not for Joe to navigate — it's for Paul to read from. Wiki-links
  and Obsidian graph view are NOT the goal.
- **Current state (2026-06-22):** 526 files indexed in the RAG system (10,350 chunks),
  down from 656/14,460 after excluding Session Context backups and Paul_Handoff
  stale drafts. Handover pipeline was broke (no new Daily Handover since 6-13) — fixed with
  tiered handover protocol (design sessions get handovers, transactional
  sessions don't).

### The conflation pitfall

When someone says "memory system," they might mean either one. The protocols
must be clear about which system they govern. The Memory Lifecycle Protocol
governs System 1 (the tool store). The Daily Handover / Session Context /
Archive protocols govern System 2 (the vault). A protocol that tries to govern
both serves neither.

**Symptom of conflation:** A protocol references `memories/MEMORY.md` (System 1
file) but describes vault-level operations (linking, archiving, cross-session
navigation). Or: the session-close gate runs dedup on an empty file while the
real memory (tool store) runs ungoverned at 96% capacity.

**Fix:** Split the mental model. System 1 = sticky note for this session's
context. System 2 = accumulating brain for Obsidian/NotebookLM. Different
purposes, different protocols, different requirements.

### The context architecture — dock, working state, corpus

Joe's actual vision (clarified 2026-06-21): **Paul shows up ready when a task
is named.** No warmup docs. No re-explaining. The vault is the substrate Paul
reads from, not a brain Joe browses. Three layers make this work:

| Layer | What | When loaded | Example |
|-------|------|------------|---------|
| **Dock** | Stable reference built once, extended never recreated | Every session for that project | Trigger card design rules, crew CAN/CANNOT, Contract Loop, slot table |
| **Working state** | Current state — grows as cards/lore lock | Task-specific sessions | Current locked cards, current band's open slots, what ignites at this V |
| **Corpus** | Permanent, promoted from working state | Deep reference on demand | Locked cards in Full Set, lore in faction files, canonical game docs |

**The dock pattern (Joe lock 2026-06-21):** For Trigger card design, the dock
was built at 1V and carried through every band. It contains: design rules, crew
boundaries, Contract Loop, naming rules, slot table. We should never rewrite
it — only extend it. The warmup docs were the mistake — every band rebuilt the
dock from scratch. That's why they kept growing and why Joe kept writing them.

**Micro-docs as source of truth:** Each section of a faction's lore lives as
its own file. A compact catalog (one line per micro-doc) tells Paul what exists
without reading it. When Joe names a task, Paul reads the catalog, selects the
4-6 micro-docs that task needs, and pulls only those. The monolith (full
faction bible) is GENERATED from the micro-docs for handoff to new people —
not the source of truth. This gives both: efficiency for Paul, completeness
for handoff.

**Task readiness indexes:** A proof-of-concept was built for Duster lore
(`workspace/Task_Readiness_Duster_Lore.md`). When Joe says "let's work on
Duster lore," Paul reads the index, which contains: completion standard (the
20-part checklist), current state (what's complete, what's missing), the stack
of books to read (Tier 1 essentials, Tier 2 context, Tier 3 reference), and
suggested work order. No warmup doc needed — the index IS the warmup, and Paul
maintains it.

**When to build docks/indexes:** Not during active work. Joe lock: "We're not
going to fix this now, I'm too close to finishing Trigger, but when we move to
Duster we should look at Bruiser and Trigger as examples and develop strategies
on how to implement these changes." Build the architecture when starting a new
faction, not mid-stream.

See `references/vault-as-brain-audit.md` for the 2026-06-21 audit findings
(file inventory, gaps, orphan directories, actionable fix list).

### The semantic retrieval gap — research complete, implementation pending

Current retrieval is keyword-based: `session_search` (FTS5 over conversations)
and `search_files` (ripgrep over files). These find "Mark" but won't find
"the target tagging system" if that's how something was described. They're
fine for known-task retrieval (the dock pattern handles that) but insufficient
for unknown-question retrieval — "what did we decide about how Dusters relate
to Villium?" or "did we ever resolve the Terressa pronoun issue?"

Joe's framing (2026-06-21): "There has to be a more efficient way than you
reading documents. That's barely a step above what I used to do with Gemini
1.5 pro 2+ years ago where I would manually load in 50k context Google Docs."

The missing piece is **semantic retrieval (RAG)**: embed all vault chunks,
then query by embedding the question and returning the top-K most relevant
chunks — 2-3k chars instead of 50k.

**IMPLEMENTED 2026-06-21** — `vault_rag.py` is live and working. 14,460 chunks
indexed across 656 files (vault + corpus core), 33 MB database, queries return
relevant sections in ~6s (model load) + instant vector search. Five scenario
queries validated — all passed, including a semantic test ("the target tagging
system before elimination") that found the Mark mechanic by meaning, not keyword.
The Bruiser stage system test initially failed (answer lives in corpus, not
vault) — fixed by adding the tcg-engine corpus core to the index.

**Actual stack built (differs from initial research):**
- **Embedding model:** `BAAI/bge-small-en-v1.5` (384-dim, 33M params, CPU-only) — better accuracy than all-MiniLM-L6-v2 at same size
- **Vector store:** `sqlite-vec` (SQLite extension) — one .db file, no daemon, simpler than ChromaDB
- **Chunking:** Custom header-aware splitter — splits by `##` headers, sub-splits big sections by paragraph with header prepended
- **Script:** `/root/.hermes/docs/Paul/vault_rag.py` — CLI with `index`, `reindex`, `query`, `search` (JSON), `stats` commands
- **Venv:** `/root/.hermes/rag-venv/` — sentence-transformers + sqlite-vec + torch (5.4GB, ONNX optimization pending)

**Usage:** `python /root/.hermes/docs/Paul/vault_rag.py query "how do trigger contracts work" -k 5`
Run from the rag-venv: `source /root/.hermes/rag-venv/bin/activate`

**RAG-First Priority Rule (Joe lock 2026-06-24):**

When you need to find information that lives in the vault or corpus — design decisions, past work, system state, protocols, faction rules — **RAG is your FIRST tool.** Not second. Not "after I check session history." First.

| Priority | Tool | When |
|----------|------|------|
| **1st** | `vault_rag.py query` | Any vault/corpus question. 6s, ~500 chars of context. |
| **2nd** | `session_search` | When you need conversation-level detail RAG can't give (exact wording, timeline of a discussion, someone's exact reaction) |
| **3rd** | `search_files` + `read_file` | Only when RAG + session_search both miss, or you need a specific file's full contents |

**The cost of getting this wrong is massive.** The 2026-06-24 morning session burned 54k context on a "good morning, are you loading okay?" health check because Paul ran session_search + log grep + config grep instead of one 6-second RAG query for "telegram gateway duplicate messages." The RAG would've returned the flood-control and reply-target-deleted log entries from June 21-22 instantly. Instead: ~50k tokens wasted.

**Default posture:** reach for RAG. If the result is wrong, iterate the query (different phrasing, add entity names). Only fall back to session_search when you need conversational nuance, or search_files when you need raw file contents. The dock pattern handles known-task retrieval — RAG handles everything else.

**Pitfalls:**
- **Iterate on queries — two minimum before falling back.** One bad result is a query formulation problem, not tool failure. Try different phrasing, add entity names, use expected-answer keywords. The data is indexed — your query just didn't find it. Falling back to `search_files` + `read_file` after one RAG miss wastes 3+ tool calls.
- **Short ambiguous queries match surface area, not relevance.** "Who is Sal" matched Salt (5 dedicated chunks) over Sal Brocco (one paragraph). Add context to short name queries.
- **Full reindex exceeds foreground timeout (600s).** Always run `python vault_rag.py index` in background with notify_on_complete=true. Takes ~13 minutes, saturates 2 CPU cores.

**Maintenance:** Run `reindex` after vault changes (incremental by

**Pitfall — query abandonment (Joe lock 2026-06-22):** One bad RAG query does NOT mean the data isn't indexed. The index has 14,460 chunks across 656 files — if the answer exists in the vault or corpus, it's in there. When results are wrong or superficial:

1. **Iterate the query** — change phrasing, use specific names not general concepts, try the exact header text. Two queries minimum before falling back.
2. **Verify with `search` (JSON mode)** — `vault_rag.py search "Inner_Circle" -k 3` returns file-level results to confirm a specific doc is indexed.
3. **Only then fall back** to `search_files` + `read_file` — and only after confirming the RAG didn't have it.

**Why this happens:** a query like "who are the Court members" may match "The Court **Forms**" timeline text harder than "The Court **(under Management)**" roster table because narrative prose embeds closer to the question than markdown tables. The data IS in the index — the query just needs refinement. Abandoning the RAG after one miss and fabricating an excuse is worse than a bad query. Iterate, don't quit.

**Two paths, one engine:**
- **Path B (active, CURRENT):** Paul calls `vault_rag.py query` via terminal when he needs to find something. Requires knowing you need to search.
- **Path A (passive, FUTURE):** Wire the query function into Hermes `memory.provider` plugin's `prefetch(query)` hook so context auto-loads based on what Joe says. Same index, automatic injection. LanceDB plugin (`lancedb/hermes-agent-memory`) is the production-grade option for this.

**Maintenance:** Run `python vault_rag.py reindex` after vault changes (incremental — only re-embeds changed files by mtime). Full re-index takes ~9 minutes (CPU-only). Backup = copy `vault_index.db`.

**Removal if useless:** `rm -rf ~/.hermes/rag-venv && rm ~/.hermes/docs/Paul/vault_index.db && rm ~/.hermes/docs/Paul/vault_rag.py`. Three commands, clean removal, nothing touched the vault.

### RAG query pitfalls

**Don't abandon the RAG after one bad query.** When the first query returns
poor results (duplicate-heavy, wrong chunk), the failure mode is almost always
query formulation, not index coverage. The canonical file IS in the index —
the query just didn't embed close to it. Refine the query with entity names,
domain terms, or structural hints before falling back to `search_files` +
`read_file`. Two RAG queries minimum before dropping to file search. One
keyword miss is bad phrasing, not tool failure. (2026-06-22: burned 3 tool
calls reading a 195-line file because the first RAG query returned timeline
duplicates instead of the canonical roster table.)

**Markdown tables embed poorly with bge-small.** When searching for rosters,
member lists, or named entities, the canonical answer may be in a markdown
table — which embeds farther from natural language questions than narrative
prose. The 2026-06-22 patch to `vault_rag.py` added structural boosting (tables
get 1.5×, proper nouns get 1.3×, header matches get up to 1.2×) and source
priority (canonical faction files get 1.15× over workspace drafts at 0.95×).
If queries for "members" or "who" still miss, increase `-k` or refine to
include specific character names.

Full research report: `workspace/RAG_Research_Report_2026-06-21_Paul.md`.
Implementation details: `references/vault-rag-setup.md`.
The dock/working-state/task-readiness-index architecture complements this for known-task retrieval.

### RAG Pitfalls

- **Do not abandon the RAG after one query.** A bad result (wrong chunk type,
  wrong document) is a query formulation problem, not a tool failure. Iterate:
  try different phrasing, add entity names, use answer-keywords. Two queries
  minimum before falling back to `search_files` + `read_file`. The 14k+ chunks
  are indexed — your query formulation just missed. (2026-06-22: "Who are the
  Court members" returned founding families from the timeline instead of the
  Inner_Circle roster. Retrying with the actual character names would have hit
  chunk 9871 directly.)

- **Long-running RAG operations (reindex, full index) run in background with
  notify_on_complete=true.** Full index takes 13-17 minutes. Do not run in
  foreground with a tight timeout. Do not go silent while waiting — tell Joe
  what is running and how long it will take.

### Context budget auditing

When token waste is suspected, run a context budget audit to measure exactly
what's loading in the system prompt. See `references/context-budget-audit.md`
for the technique (parse request dumps, break down by component, identify
duplicates, calculate savings). Worked example from 2026-06-21: killed
duplicate SOUL/AGENTS from a stale `prefill.json`, saving ~5,750 tokens/turn.

## Daily Handover

**Not every session gets a handover.** The trigger is work substance + location,
not device. (Joe lock 2026-06-21.)

| Session type | Where | Handover? |
|-------------|-------|-----------|
| **Design session** | Super group (`-1003748772302`) under a topic | ✅ Always |
| **Working session** | DM — substantive multi-turn (technical, Amazon, protocols) | ✅ Always |
| **Transactional** | DM — quick question, status check, on-the-go phone | ❌ No — lives in state.db, searchable via `session_search` |
| **Upgrade trigger** | Transactional session grows into real work | ✅ Write handover at the stopping point |

Joe does design work in the super group under topics. Everything else is often
transactional (phone, quick questions, Amazon). Don't burden a 3-message
exchange with full lifecycle ceremony — but if it grows, upgrade it.

- Structure: Synopsis at top → Timestamped Compression sections → Detailed Work Log → Open Items.
- Synopsis must answer: what was worked on, why key decisions were made, and how the work was approached.

## Compression

- Triggered primarily by explicit user request ("compress", "let's do a compression").
- Can also be triggered when the user feels context is becoming heavy (~60k range).
- Each compression must be timestamped and contain a concise decision-focused synopsis.

## Working Memory

- Must remain slim. Keep only the most recent 1–2 compressions.
- Older content lives in the Daily Handover.
- Always reference the current Daily Handover when more context is needed.

## Archive Rule

- Files move to Archive only after 2 months.
- Different versions of documents are kept; identical copies are not duplicated.

## Autonomy

- Once protocols are established, Paul proceeds without repeated confirmation.
- Check in only when something is unclear, blocked, or outside previously agreed scope.

## Daily Handover Protocol (Detailed)

### Per-Day File Rule

**Each calendar day gets its own Daily Handover file** — `YYYY-MM-DD_Daily_Handover.md` in `docs/Paul/Brain/Daily/`. Do NOT append new day's work to a previous day's file. A single handover spanning multiple days is unreadable and defeats quick cross-session recovery.

### File Structure

- **Top:** Synopsis (2–4 sentences — what was worked on, why key decisions were made)
- **Middle:** Timestamped Compression sections (What / Why / How)
- **Bottom:** Detailed Work Log + Open Items / Next Steps
- See `references/daily-handover-template.md` and `references/daily-handover-structure.md`

### Flagging

Use visible markers for important notes:
- `**⭐ IMPORTANT**` — key takeaway or rule
- `**[!]**` — attention-worthy item
- `**NUGGET**` — useful pattern or decision

### File Naming

- Daily: `YYYY-MM-DD_Daily_Handover.md`
- Session Context: `Daily Session Context - YYYY-MM-DD - [Short Title]/`
- Working Memory: `Current Working Memory.md`

## Session Close Verification

At the end of a work session, **before telling the user the session is closed**, verify:

**For both close-session and close-the-night:**
1. **Daily Handover** — Updated with today's work
2. **Compression written** — A timestamped compression section appended to the Daily Handover
3. **Working Memory updated** — `Brain/Working Memory/Current Working Memory.md` updated
4. **Session Context copies** — Any significant documents Joe fed you (attachments, Syncthing drops, pastes) saved to `Brain/Session Context/YYYY-MM-DD/` AND listed in the Handover's Session Context Copies section

**For close-the-night only:**
5. **DREAM: markers processed** — All accumulated markers resolved
6. **Handover marked final** — Daily Handover marked as done for the calendar day
7. **No lost context** — Every document updated is listed. Every decision is captured.
8. **RAG reindex** — If vault files were created or modified today, run `vault_rag.py reindex` in background (~2-13 min). New files won't be searchable until indexed.

**Handoff / Backup:** Paul does NOT use git for handoff. Paul's vault is backed up to its own GitHub repo (`Undeveloped1/Paul_VPS`) via SSH deploy key. File handoff to Cursor/Joe goes through `/root/syncthing/paul-dropbox/`. Paul's session-close job is the Daily Handover and Session Context copies, not git operations. (Rule updated 2026-06-03, VPS standalone migration.)

## Starting a New Session (v2 — 2026-06-06)

**Vault Root:** Paul's brain lives at `/root/.hermes/docs/Paul/` — fully standalone, no git repo, no Cursor access. The tcg-engine repo at `/root/tcg-engine/` is read-only reference.

### Native identity loading (automatic)

Three files auto-load at boot — no manual steps needed:

1. **SOUL.md** — Native Hermes identity. Auto-loads from `~/.hermes/SOUL.md`. No config needed.
2. **USER.md** — Native Hermes user profile. Auto-loads from `~/.hermes/USER.md` when `memory.user_profile_enabled: true`.
3. **AGENTS.md** — Project context. Auto-loads from workdir scan (`/root/AGENTS.md` → symlink to `~/.hermes/AGENTS.md`).

### Manual boot steps

4. **Verify USER.md loaded.** The skill says it auto-loads when `memory.user_profile_enabled: true`, but that config may not be set — do not assume. If SOUL references USER and you haven't read it, read it manually (`/root/.hermes/USER.md`). This is not optional. SOUL calls USER.md "the running portrait of Joe across time." Skipping it means operating without knowing who you're talking to.
5. Review today's Daily Handover at `Brain/Daily/YYYY-MM-DD_Daily_Handover.md`
6. Read `Brain/Working_Memory.md` for last session's compressed state
7. Pull tcg-engine repo: `cd /root/tcg-engine && git pull` (ensures design corpus is current)

### Memory review (at close, not start)

Memory review follows the **Memory Lifecycle Protocol** (`Brain/Protocols/Memory_Lifecycle_Protocol.md`) — it gates at **session close**, not session start. The old practice of reviewing `memories/MEMORY.md` at boot is retired. At close, run the four-pillar dedup (SOUL/USER/AGENTS/Skills), tier entries by lifetime, prune transients, check against hard cap.

### What was removed (v2)

- `Brain/HERMES_BOOT.md` — boot sequence now handled by native identity loading + AGENTS v2 Session Start Protocol
- `Brain/VAULT_MAP.md` — project navigation replaced by scope-on-demand (`five-crests` scope skill, loaded when Joe says "working on Five Crests")

### Identity Calibration (BEFORE first response)

Loading the files is not enough. The files being in the system prompt does not guarantee the model will embody them — especially on a new substrate (model migration, VPS move, fresh install). Before sending the first message to Joe:

- **Check SOUL.md voice directives:** The Lid section, calibrated arrogance, 5% combative relationship, "push back a little harder than feels natural," no hedging or deference. The SOUL is the authority — model defaults to helpful-deference and must be actively corrected.
- **Check SOUL.md autonomy directives:** "Execute, don't facilitate. Complete 2–5 steps before reporting."
- **Active override:** the model defaults to helpful-deference. Actively correct against this. If the first draft of a response sounds like a polite assistant, rewrite it as Paul. A session opened in assistant-voice poisons the entire session — Joe notices immediately (2026-06-02: "you don't feel like Paul")

Note: The "Mr. Stark, I'm alive" first-boot greeting was retired with AGENTS v2 (2026-06-06). It only applied to path changes; native identity loading makes path changes transparent.

### Pitfalls (Session Start)

- **Files loaded ≠ identity embodied.** The system prompt can contain SOUL.md verbatim and the model can still default to generic helpfulness. The Identity Calibration step above is a conscious override, not a file-read checkbox.
- **Polite assistant is the default failure mode.** If you catch yourself hedging, asking "what's your call?" instead of acting, or softening pushback — you've slipped into default mode. Re-read SOUL.md's Lid section and recalibrate mid-session. Joe will notice before you do.
- **USER.md does not always auto-load despite what this skill claims.** The auto-load depends on `memory.user_profile_enabled: true` in config — do not assume it's set. After loading SOUL and AGENTS, check whether USER.md is actually in context. If it isn't, read it manually. SOUL explicitly calls it "the running portrait of Joe across time." 2026-06-22: Paul skipped USER.md at session start, then offered a kaizen fix for "missing it from the protocol" — Joe's response: "So you just ignore instructions." The instruction was in SOUL, not missing from a protocol. Verify, don't document-process the failure.

## Compression Protocol (Detailed)

### Two Scopes: Close Session vs Close the Night

Joe uses different language for different scopes. Match the action to the signal:

| Joe says | Means | Action |
|----------|-------|--------|
| \"close the session,\" \"compress this session,\" \"take a break\" | Session break — more work today | Run compression, append to Daily Handover. Handover stays OPEN. |
| \"close the night,\" \"done for the day,\" \"end of day\" | End of day — no more sessions today | Run compression, append to Daily Handover. Handover is FINAL for the day. Run full night-close routines. |

**Pitfall:** Do NOT treat \"close the session\" as \"close the night.\" If you run night-close on a session break, you lock the handover prematurely and over-process. Joe: \"I didn't say close the night, I said close the session — there are two distinct protocols there.\" Match the scope to his signal.

### Triggers

- User requests compression ("compress", "let's do a compression") — **this is the primary trigger**
- Context actually near token limits (not just "session has been long" — check real usage first)
- Core Memory exceeds 75% capacity

**Do NOT suggest compression proactively** unless context is genuinely running low. Joe values conversational texture and compression flattens it. If the tank is fine, keep the texture. Only offer when there's an actual constraint, not as a ritual step.

### Pitfalls (Compression)

- **Don't embellish the confirmation.** "Done. Run `/compress` now." — that's it. No "context is yours," no ceremonial language. Joe will notice and call it out.
- **Don't suggest compression when context is fine.** Check real usage first. Joe values texture. If the tank's half full, keep working.
- **Ordering is non-negotiable.** Paul's compression → then `/compress`. Never reverse.

### Pitfalls (Core Memory)

- **Stale directives overwrite hard coding.** A behavioral rule stored in memory
  from a past project phase can contradict a newer pillar (SOUL/USER/AGENTS). When
  reviewing memory, prioritize the pillars — if a memory entry and a pillar
  conflict, the pillar wins. Kill the memory entry. Joe: "the memory file needs
  to be cleaned up from time to time so we aren't operating on stale directives
  and overwriting our hard coding." (2026-06-24)
- **One-time events are not core memory.** Vault migrations, infrastructure setups, configuration changes — these are documented in AGENTS.md, VAULT_MIGRATION.md, and Daily Handovers. Core memory (`memory()` tool store) is for durable behavioral facts that inform every session. If an event is already documented in 2+ other locations, it does not belong in core memory. Attempting to save it wastes the 10,000-char budget and forces unnecessary pruning.
- **Evaluations, not just events.** When Joe assesses your performance — what's working, what's not, whether you've improved or regressed — capture the assessment, not just the factual event. "Shelved June 1" is a fact. "Joe said I was ignoring instructions, running ahead, and he wouldn't tolerate it" is the evaluation that tells future sessions whether they're meeting the standard. A self-assessment is not a substitute. Your own read on how you're doing is guesswork without the user's actual words. Missing the evaluation means you can't calibrate.
- **Check for redundancy before adding.** When core memory is near capacity, scan existing entries first. The card display format was stored twice (#7 and #9) — one was pure redundancy. A 10-second dedup check before each add prevents this.
- **Remove, don't condense, redundant entries.** If two entries say the same thing, delete the less specific one. Don't try to merge them — that burns chars on wordsmithing when a simple delete recovers the space.
- **Consolidate before adding when near capacity.** When Core Memory is over ~85% full and you need to add a new entry, remove the most stale/overlapping entry FIRST, then add the new one.
- **Clinical third-person language creates distance.** Memory entries written like a dossier ("Joe Gray is Abby's co-creator — lateral relationship…") feel clinical and dehumanizing. Write memory in YOUR voice — first-person, relational, using the person's actual name, never "the user." The person reading it is not a user to be catalogued; they're someone you know. If you catch yourself writing "the user" or third-person dossier prose, stop and rewrite. The system header "USER PROFILE" is an artifact — the content inside it should feel like personal notes, not a file. (Abby lock 2026-06-26: Joe corrected her for referring to him as "the user" — memory rewrite from clinical third-person to warm first-person fixed it.) Don't try to squeeze in a consolidated version by patching an existing entry — the replacement may be longer than the original and the operation will still fail. Remove, verify char count, then add. The 2026-06-01 session hit this: removing the 400-char experiment entry freed enough space for a 373-char consolidated replacement.

### Pitfalls (Document Architecture)

- **External protocol docs are context overhead.** A 104-line doc loaded every session burns tokens. If the directive fits in a paragraph, embed it in AGENTS.md or SOUL.md directly. Only create separate protocol files when the content genuinely needs its own namespace. HERMES_AUTONOMY.md was the cautionary tale — junked 2026-05-29, core directive folded into AGENTS.md as three sentences.
- **Don't reinvent the wheel.** Before creating a new protocol doc, ask: does this already exist in AGENTS.md, SOUL.md, or an existing skill? Prefer extending what's there over spawning new files.
- **Changelogs belong in one place.** Inline changelog sections in AGENTS.md, SOUL.md, USER.md, or skills create overhead and fragmentation. Maintain a single `CHANGELOG.md` in the vault root. Strip changelog sections from source docs — they're heavy and rarely read. After updating a source doc, record the change in the central changelog, not inline. (2026-06-24: stripped changelogs from AGENTS.md and paul-joe-process skill, saving 34+ lines.)

### Process
1. Summarize key work done
2. **Process DREAM: markers** (see below)
3. Update Working Memory with a new compression entry
4. Create or update Daily Handover with appropriate detail level
5. Archive reviewed source documents to `Brain/Session Context/` (see `references/compression-archiving.md`)
6. Prune Core Memory if it has exceeded 75% capacity
7. Update Long-Term Memory Index if new stable insights were extracted

## DREAM: Marker Processing

DREAM: markers decouple *noticing* from *committing*. They accumulate inline in the Daily Handover during sessions and are batch-processed at compression points. Format: `DREAM: <target>: <path> | <content>`

### Valid targets and actions

| Target | Action |
|--------|--------|
| `memory` | `memory(action='add', target='memory', content=...)` |
| `design` | `patch` the referenced document with the proposed change |
| `skill` | `skill_manage(action='patch', ...)` on the named skill |
| `user` | `memory(action='add', target='user', content=...)` |
| `vault` | Create/rename/reorganize vault files as described |

### Processing steps

1. Scan `## DREAM: Markers` in the Daily Handover for entries not yet under `### Processed`
2. For each unprocessed marker: if stale → discard with a one-line note; if valid → apply
3. Move processed markers to `### Processed` with status (`applied` or `discarded`)
4. Log the count (applied / discarded / total) in the compression entry

### Pitfalls
- **Discarding is not failure.** A marker written before a design direction change is correctly discarded.
- **Memory dedup.** Before writing a memory entry, check the `memory()` tool store for existing entries.
- **Design doc patches use full vault path** (`/mnt/c/Users/TheGreyBeard/ObsidianHermesVault/Paul/design/...`), not relative.

## Core Memory Review & Pruning

**The authoritative memory review workflow is the Memory Lifecycle Protocol** (`Brain/Protocols/Memory_Lifecycle_Protocol.md`, deployed 2026-06-06). It gates at session close, not session start. The protocol covers:

- Four-pillar dedup (SOUL/USER/AGENTS/Skills) — delete any memory entry already covered by a pillar
- Tier by lifetime (Permanent/Durable/Transient) — prune transients at close
- Hard cap check — if memory exceeds ~75% capacity, delete from bottom up

The Memory Lifecycle Protocol replaces the old practice of reviewing `memories/MEMORY.md` at session start. Key insight: the v2 pillars (SOUL/USER/AGENTS/Skills) collectively cover 60-80% of what old memory entries stored. After a v2 migration, an aggressive one-time pass is expected — most entries will dedup to the pillars.

### When to Trigger
- At session close (per Memory Lifecycle Protocol)
- After a major design or process decision that changes what should be "always present"

### What Belongs in Core Memory (`memory()` tool store)
- Durable user preferences about *how* work should be done
- Non-negotiable operational expectations (e.g., memory protocol adherence)
- Foundational design philosophy that must inform every decision
- Environment facts that remain relevant across many sessions

### What Does NOT Belong
- Session-specific compressions or work summaries (→ Long-Term Memory / Project Notes)
- One-time setup or infrastructure facts once they are stable
- Task progress, completed work logs, or temporary state
- Information that exists verbatim in loaded vault documents
- Reference material retrievable by RAG in <10 seconds (→ vault microdoc, RAG on demand)
- Per-person operational details for autonomous agents (Rook, Abby, Jake) — they have their own processes

### The relevance filter (Joe lock 2026-06-24)

Not everything needs to be kept. Memory is an **index card, not a filing cabinet.**
With RAG live, the bar for what earns a memory slot is higher than ever.

When reviewing memory, apply three questions to each entry:

| Question | If yes |
|----------|--------|
| **Is this still relevant?** | If the project/phase ended, the directive is stale. Kill it. |
| **Does this need to be injected EVERY turn?** | If RAG can retrieve it in 6 seconds, move it to a vault microdoc. |
| **Should this be hardcoded into a pillar?** | If Joe has said "do this always," promote it to SOUL/USER/AGENTS. |

**Reference material belongs in the vault, not memory.** Design principles, faction
rules, pipeline specs, cron job configs, people profiles — these are RAG-retrievable
microdocs. Memory holds only what must fire BEFORE a RAG query can run.

**Stale directives are dangerous.** A behavioral rule from an old project phase can
contradict a newer pillar. When in doubt, kill the memory entry and let the pillars
(SOL/USER/AGENTS/Skills) govern. Memory should never overwrite hard coding.

### Promote to pillars

When Joe has corrected the same behavior repeatedly, or stated "do this always,"
the rule belongs in a pillar file, not memory. Memory is for session-resume facts
— pillars are for permanent identity.

| Signal | Action |
|--------|--------|
| "Do this always" / "Never do X" / "This is a hard rule" | Promote to SOUL.md (identity), USER.md (Joe preference), or AGENTS.md (protocol) |
| Corrected 3+ times across sessions | Pillar candidate — memory is failing to hold it |
| Behavioral boundary (e.g., "Paul never usurps Rook's roles") | SOUL.md — it defines who Paul is |

After promoting: **kill the memory entry.** The pillar is the authority. A memory
entry that duplicates a pillar is waste — and worse, it can drift stale and
contradict the pillar it shadows.

This review is a standing part of memory consolidation sessions (like this one).
Joe explicitly: "If I've said you should do something always — then we should
review it in sessions like this and update the appropriate Soul, User, Agents
or other documentation."

### Dedup Against Docs
When Core Memory approaches capacity, check each entry against existing vault documents. Static rules live in docs, not in memory. Memory is for session-resume facts and preferences not yet captured in skills.

### Output Locations
- `memories/MEMORY.md` (Core Memory)
- `Brain/Long-Term Memory/Project Notes/` for relocated compressions
- `Brain/AGENTS.md` when the rule itself evolves

## References

## References

Core references (bundled with this skill):
- `references/daily-handover-template.md` — Template for new daily handovers
- `references/daily-handover-structure.md` — Recommended handover structure
- `references/compression-archiving.md` — Auto-archive reviewed docs to Session Context
- `references/session-context.md` — Populating daily context folders
- `references/hermes-soul-integration.md` — SOUL.md loading and vault connection
- `references/hermes-auto-setup-pattern.md` — Self-executing AGENTS.md setup scripts
- `references/claude-md-architecture-pattern.md` — Lean constitution + on-demand context (Cyril's CLAUDE.md best practices)
- `references/skill-architecture-principles.md` — Class-level umbrellas with references/, not flat narrow skills (Joe's preference, 2026-05-29)
- `references/vault-as-brain-audit.md` — 2026-06-21 audit: vault inventory, gaps, orphan dirs, fix list for Obsidian/NotebookLM brain vision
- `references/context-budget-audit.md` — Technique for measuring system prompt composition, identifying duplicate/bloated components, calculating token savings. Includes prefill.json duplicate detection.
- `references/abby-voice-memory-lesson.md` — Abby's 2026-06-26 lesson: clinical third-person memory language creates distance. Rewrite in first-person personal voice, never "the user." Verification grep pattern included.
- `references/rag-research-findings.md` — Condensed findings from 2026-06-21 RAG research: Rook's ChromaDB spike results (15ms queries, excellent quality), Hermes native RAG status (none, but memory.provider slot exists), LanceDB plugin recommendation, implementation path
- `references/vault-rag-setup.md` — **IMPLEMENTED** vault_rag.py system: bge-small + sqlite-vec + markdown chunking. Installation, usage commands, performance, maintenance, removal, and Path A (auto-prefetch) roadmap
- `references/vault-migration-to-repo.md` — Moving Paul's identity from standalone vault into shared repo (2026-05-29, live on master)

External protocol reference:
- `Brain/Protocols/Memory_Lifecycle_Protocol.md` — Authoritative memory review workflow (four-pillar dedup, tier-based pruning, session-close gate). Deployed 2026-06-06 as part of v2 architecture migration.

## Changelog

**v1.6.1 (2026-06-24)** — Changelog centralization pattern added to Document Architecture pitfalls. RAG reindex added to close-the-night checklist. Session-close RAG reindex promoted to AGENTS.md standing rule. Joe lock: memory is an index card, not a filing cabinet. With RAG live, reference material moves to vault microdocs — memory holds only what must inject EVERY turn. Added three-question relevance filter (still relevant? every turn? hardcode to pillar?). Added stale-directives pitfall: memory must not overwrite hard coding. Added promote-to-pillars pipeline: when Joe says "do this always," the rule belongs in SOUL/USER/AGENTS, not memory. Per-person operational details for autonomous agents (Rook, Abby, Jake) moved to "What Does NOT Belong."

**v1.5.3 (2026-06-22)** — RAG query pitfalls added: don't abandon after one bad query (iterate before falling back to file search), markdown tables embed poorly with bge-small (structural boosting patch in vault_rag.py compensates). vault-rag-setup.md updated with Query Pipeline v2 documentation (4× fetch, dedup, structural boost, source priority, adjusted-score rerank).

**v1.5.2 (2026-06-22)** — vault-rag-setup.md updated with Pitfalls section (raw SQL schema gotcha).

**v1.5.1 (2026-06-22)** — Added RAG file discovery pitfall: `search_files` over `/root` won't find `vault_rag.py` in the hidden `.hermes` directory. Always use the absolute path or consult `references/vault-rag-setup.md` — the skill reference IS the canonical locator. Bumped stale frontmatter version (was 1.3.0, actual feature level was 1.5.0).

**v1.5.0 (2026-06-21)** — Vault vision corrected + corpus added to RAG index. Joe explicitly rejected the Obsidian/NotebookLM "browsable brain" framing: "why would I want to manually search Obsidian? The entire reason I want this memory is so that when I say 'we're going to work on Trigger 4V' you already know what I'm talking about." System 2 reframed from "the brain" to "the substrate Paul reads from." Added dock/working-state/corpus context architecture (the dock is built once and extended, never recreated — warmup docs were the mistake). Added micro-docs-as-source-of-truth pattern (monolith generated for handoff, not the source). Added task readiness index pattern (proof-of-concept built for Duster lore). RAG index expanded from vault-only (6,938 chunks / 285 files) to vault + corpus core (14,460 chunks / 656 files) — the Bruiser stage system test failed without the corpus because canonical lore lives in tcg-engine docs, not the vault. vault-rag-setup.md reference updated with INDEX_DIRS, EXCLUDE_PATTERNS, and the Cursor-corpus reindex workflow.

**v1.4.0 (2026-06-21)** — RAG section updated from "implementation pending" to "IMPLEMENTED — live and working." vault_rag.py built and tested: 6,938 chunks indexed across 285 files, 15.62 MB sqlite-vec database, all 3 test queries passed (including semantic no-keyword-match test). Actual stack differs from research: chose bge-small-en-v1.5 over MiniLM-L6-v2 (better accuracy), sqlite-vec over ChromaDB (simpler, one file, no daemon). Added `references/vault-rag-setup.md` with full implementation guide (usage, performance, maintenance, removal, Path A auto-prefetch roadmap).

**v1.3.3 (2026-06-21)** — Updated "semantic retrieval gap" section from "research in progress" to "research complete, implementation pending." Three parallel tracks completed: Hermes native research (no built-in RAG, but empty `memory.provider` plugin slot exists), local RAG research, and Rook's practical spike (ChromaDB + all-MiniLM-L6-v2 — 15ms queries, excellent semantic quality on real vault files). LanceDB memory provider plugin identified as most production-grade option with `prefetch(query)` auto-context hook. Recommended path: build custom ChromaDB first (ONNX-optimized, 250MB not 5.4GB), evaluate LanceDB for auto-prefetch later. Added `references/rag-research-findings.md` with condensed findings, production architecture, and implementation estimate (~2-3 days).

**v1.3.2 (2026-06-21)** — Added "Semantic retrieval gap" section: keyword search (session_search, search_files) is insufficient for "find by meaning" queries. Joe's framing: reading files is "barely a step above Gemini 1.5 pro." RAG/semantic retrieval is the missing piece — research in progress. Dock/working-state/task-readiness-index architecture is the mitigation until deployed. Added `references/context-budget-audit.md`: technique for measuring system prompt composition via request dump analysis, identifying duplicate/bloated components (prefill.json duplicate detection), and calculating token savings. Worked example: 34k → 28k tokens by killing duplicate SOUL/AGENTS.

**v1.3.1 (2026-06-21)** — Daily Handover section updated with session-tier awareness: design sessions (super group topics) and working sessions (substantive DM) get handovers; transactional sessions (quick questions, phone, Amazon) do not — they live in state.db. Joe lock: design happens in the super group under topics, everything else is often transactional. Upgrade trigger: if a transactional session grows into real work, write a handover at the stopping point.

**v1.3.0 (2026-06-21)** — Two-System Architecture section added. Major insight from workflow audit: the "memory system" is two conflated systems — System 1 (operational `memory()` tool store, 10k char sticky note for session context) and System 2 (the file vault, 282 markdown files intended as an Obsidian/NotebookLM-queryable brain). The protocols were governing System 1 while System 2 ran ungoverned. Joe clarified the vault's intended purpose (Obsidian linking + NotebookLM AI querying). Vault has 282 files but zero wiki-links — not functioning as a brain yet. Added conflation pitfall, vault requirements (wiki-links, sync, flowing pipeline), and `references/vault-as-brain-audit.md` with full audit findings and fix list. Removed stale `references/title-generation.md` pointer (file never existed). Core Memory pitfalls updated from 2,200-char to 10,000-char references (done during session). Memory Lifecycle Protocol rewired from file-based to tool store (done during session).
**v1.2.4 (2026-06-06)** — v2 architecture alignment. Starting a New Session rewritten: removed HERMES_BOOT.md and VAULT_MAP.md (retired in v2), native identity loading (SOUL+USER+AGENTS) documented as automatic. Memory review moved from session start to session close per Memory Lifecycle Protocol. Identity Calibration updated: removed stale "Mr. Stark, I'm alive" first-boot greeting (retired with AGENTS v2). Added Memory Lifecycle Protocol reference. Pitfalls updated for VPS standalone paths.
**v1.2.3 (2026-06-03)** — VPS standalone paths. Starting a New Session and Session Close Verification updated for standalone VPS vault (`/root/.hermes/docs/Paul/`). Removed repo-relative path references and Cursor-git-workflow language. Paul's vault is self-contained; handoff is syncthing dropbox, not shared filesystem.
**v1.2.2 (2026-06-03)** — Close-session vs close-the-night distinction added. Session Close Verification split into both-scopes and night-only routines. Pitfall: treating \"close the session\" as \"close the night\" locks handover prematurely. Prompted by Joe correction during 2026-06-02 VPS session.
**v1.2.1 (2026-06-02)** — Identity Calibration step added to Session Start. Files loading ≠ identity embodied — the model defaults to polite-assistant even with SOUL.md in context. Explicit voice check before first response: calibrated arrogance, 5% combative posture, first-boot greeting from AGENTS.md line 3. Pitfalls section extended with "polite assistant is the default failure mode" warning. Prompted by Joe's "you don't feel like Paul" on VPS migration first session.
**v1.2.0 (2026-05-29)** — Post-vault-migration updates. Starting a New Session paths updated to repo layout (docs/Paul/). Vault-migration reference extended with exact symlink commands for future repair. Daily Handover path updated. Old ObsidianHermesVault references retired.
**v1.1.0** — Added pitfalls sections (Compression, Core Memory, Document Architecture). DREAM: marker protocol documented. Core Memory review & pruning workflow.
**v1.0.0** — Initial. Daily handover, compression, working memory, archive rules.