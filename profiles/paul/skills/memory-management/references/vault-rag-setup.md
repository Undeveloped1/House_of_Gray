# Vault RAG — Implementation Guide

**Created:** 2026-06-21
**Status:** LIVE — vault_rag.py is installed, indexed, and tested

---

## What This Is

Local semantic retrieval over Paul's markdown vault. Instead of reading 50k of
files to find an answer, embed the question, search all ~7,000 chunk vectors,
and get back the 5 most relevant sections in seconds.

## Architecture

```
Markdown Vault + TCG Corpus (656 files, ~45MB)
    │
    ▼
Chunker (header-aware, ~800 char max)
    │  Splits by ## headers, sub-splits big sections by paragraph
    ▼
Embedding Model (BAAI/bge-small-en-v1.5, 384-dim, CPU-only)
    │  sentence-transformers, ~1GB RAM during operation
    ▼
sqlite-vec (SQLite extension, one .db file)
    │  HNSW vector index, no daemon, no service
    ▼
Query CLI (vault_rag.py)
    │  Paul calls via terminal or execute_code
    ▼
Top-K relevant chunks returned as text or JSON
```

## What's Indexed

The index spans TWO source directories — Paul's vault (working files) and the tcg-engine corpus core (canonical game docs). Both are needed: the vault has session records, handovers, and working drafts; the corpus has the canonical lore, faction files, and design playbooks.

**INDEX_DIRS** (defined in vault_rag.py):
- `/root/.hermes/docs/Paul` — Paul's vault (handovers, workspace, protocols, session context)
- `/root/tcg-engine/docs/Five_Crests` — World corpus (factions, core lore, design, art, game rules)
- `/root/tcg-engine/docs/Paul_Handoff` — Paul→Cursor handoff drafts
- `/root/tcg-engine/docs/engineering` — Engine/channel/canvas docs
- `/root/tcg-engine/docs/playbooks` — Design playbooks and checklists
- `/root/tcg-engine/docs/sets` — Card set docs
- `/root/tcg-engine/docs/hermes` — Hermes workflow docs
- `/root/tcg-engine/docs` — Root-level docs (HANDOVER.md, CANONICAL_REFERENCE.md)

**EXCLUDE_PATTERNS** (filtered out):
- `/.git/`, `/node_modules/`, `/deps/`, `/__pycache__/`, `/.obsidian/`
- `/docs/archive/` — 4,413 archived files, not corpus core
- `/docs/bridge/` — Retired bridge directory
- `/Five_Crests/archive_promotion/` — Promotion workflow archive
- `/Brain/Session Context/` — Compression backups (redundancy, not knowledge)
- `/Paul_Handoff/incoming/` — Stale Cursor handoff drafts

These last two dropped ~4,100 duplicate chunks from the index (2026-06-22). Session
Context is intentional redundancy per protocol — keep the files, exclude from search.
Paul_Handoff drafts are dead after Cursor merges them into canon.

**The corpus is a git repo owned by Cursor.** The index reads files, never writes to them. When Cursor updates the corpus (git pull/commit), run `reindex` — it only re-embeds changed files by mtime. No git interaction. The repo stays read-only.

## Installed Components

| Component | Location | Notes |
|-----------|----------|-------|
| Python venv | `/root/.hermes/rag-venv/` | 5.4GB (torch CUDA libs — ONNX optimization pending to drop to ~250MB) |
| Script | `/root/.hermes/docs/Paul/vault_rag.py` | ~150 lines, CLI with index/reindex/query/search/stats |
| Index DB | `/root/.hermes/docs/Paul/vault_index.db` | 15.62 MB, one file, backup = copy |
| Model cache | `~/.cache/huggingface/` | bge-small-en-v1.5, ~130MB |

## Usage

### Activate the venv
```bash
source /root/.hermes/rag-venv/bin/activate
```

### Query (human-readable output)
```bash
python /root/.hermes/docs/Paul/vault_rag.py query "how do trigger contracts work" -k 5
```

### Query (JSON output, for programmatic use)
```bash
python /root/.hermes/docs/Paul/vault_rag.py search "duster villium relationship" -k 3
```

### Re-index after vault changes (incremental by mtime)
```bash
python /root/.hermes/docs/Paul/vault_rag.py reindex
```

### Full re-index (rebuilds everything)
```bash
python /root/.hermes/docs/Paul/vault_rag.py index
```

### Show index statistics
```bash
python /root/.hermes/docs/Paul/vault_rag.py stats
```

## Pitfalls

- **Iterate on queries — do not quit after one bad result.** A query returning
  the wrong section (e.g. timeline origin story instead of a roster table) is a
  query formulation problem, not a tool failure. Try different phrasing, add entity
  names, use keywords from the expected answer. Two queries minimum before falling
  back to search_files + read_file. The data is indexed — your query just did not
  find it. (2026-06-22: "Who are the Court members" returned founding families from
  the timeline. "Bunny Gallagher Sidney Lark Julian St. Clair roster" would have
  hit Inner_Circle.md directly.)

- **Short ambiguous queries favor whoever has the most indexed real estate.**
  "Who is Sal" matched Salt (Kenneth Randall, Bruiser ink keeper, 5 dedicated chunks)
  instead of Sal Brocco (Hastings crew muscle, one paragraph in First Family). The
  embedding model does not know that "Sal" ≠ "Salt." For short name queries, add
  context: "Sal Brocco" or "Sal from the Hastings crew." A future exact-match
  check could filter substring false positives from top results.

- **Do not go raw SQL against vault_index.db unless the CLI is broken.** The
  chunks table uses columns `file`, `header`, `text` — not `content` or
  `source_file`. The vec_chunks virtual table uses `embedding`, not `v`. The
  CLI script (vault_rag.py query / vault_rag.py search) already knows the
  schema. For programmatic access, use vault_rag.py search "..." -k 5 (JSON
  output via stdout). Only drop to raw Python+sqlite3 if the CLI genuinely
  cannot do what you need — and if you do, read the schema with PRAGMA
  table_info(chunks) first. (2026-06-22: burned time on this during a live
  query.)

- **index (full rebuild) drops tables first.** Fixed 2026-06-22: init_db was
  using CREATE TABLE IF NOT EXISTS, which left old chunks from excluded
  directories in the DB after a full reindex. Now index (reindex=False) calls
  init_db(conn, fresh=True) to DROP tables before CREATE. reindex still keeps
  the schema intact and deletes/reinserts per-file.

- **Full reindex takes ~13 minutes and exceeds the default terminal foreground
  timeout (600s).** Always run `python vault_rag.py index` in background with
  notify_on_complete=true. It will saturate 2 CPU cores (~188% CPU) during the
  embedding pass. Do not run foreground — it will time out at 600s around 45%
  complete. (2026-06-22: timed out twice before switching to bg.)

## Query Pipeline (v2 — 2026-06-22)

The query pipeline now has three post-retrieval stages beyond raw vector search:

1. **Fetch 4× candidates** — retrieves `max(k*4, 20)` results instead of `k`, giving
   reranking headroom to find answers that embed poorly but match structurally.
2. **Deduplicate** — collapses identical chunks across directories (workspace, Session
   Context, Paul_Handoff often contain copies of the same document). First 120 chars
   of text + header used as fingerprint.
3. **Structural boosting** — adjusts scores based on query intent signals:
   - **Entity queries** (containing "who," "members," "roster," "list," "names"):
     markdown tables get 1.5×, 3+ proper nouns get 1.3×, header matches get up to 1.2×
   - **Source priority** (always applied): canonical faction files 1.15×, core 1.10×,
     handoff 1.05×, workspace 0.95×, Session Context 0.90×, Daily handovers 0.88×
4. **Rerank by adjusted score** — `score = distance / boost`, lower is better.
   Top `k` returned.

This fixes the failure mode where canonical roster tables (e.g., Inner_Circle.md
§ The Court) were crowded out by duplicate narrative drafts from workspace/Session
Context. The table chunk at distance 0.86 now scores ~0.44 after 1.95× boost,
beating the unboosted narrative at 0.74 → 0.74.

## Query Performance

- **Model load:** ~6 seconds (cold start — loads bge-small into memory)
- **Vector search:** instant (<50ms for 7,000 vectors)
- **Total query time:** ~6 seconds from CLI call to results
- **RAM peak:** ~1GB during model load + query
- **Future optimization:** daemon mode to keep model in memory → instant queries

## Index Statistics (as of 2026-06-22, after consolidation)

- Total chunks: 10,350
- Files indexed: 526
- DB size: 55 MB
- Model: BAAI/bge-small-en-v1.5
- Full index time: ~13 minutes (CPU-only, 324 batches, 2 cores @ ~188%)
- Sources: Paul's vault + tcg-engine corpus core (Session Context and Paul_Handoff excluded)

## Test Results (2026-06-21)

Five scenario queries validated — 4 of 5 passed on vault-only index, all 5 passed after corpus was added:

1. **"Let's finish Trigger 4V card design band"** → Found Card Design Warmup (design rules, session mode) + 6-11 handover (3V status). ✅
2. **"Let's work on Duster lore"** → Found Task Readiness Index + Duster Lore Pass + June 6-8 retrospective. ✅
3. **"What's the Bruiser stage system?"** → Initially FAILED (vault-only) — the stage system lives in the corpus, not the vault. FIXED by adding corpus to index. Now returns S1/S2/S3 stages from Set_Design_Framework_v6_2.md, familiar tokens from the compendium checklist, and stage discipline from the Bruiser compendium. ✅
4. **"How do Dusters and Skivers relate?"** → Found Duster vs Skiver contrast anchor — "partners, complementary opposites." ✅
5. **"What did we lock about Bullet Time?"** → Found F10 Bullet Time mechanics doc + function registry + naming fix. ✅

**Key lesson:** The corpus (tcg-engine canonical docs) MUST be in the index. Without it, canonical lore questions (stage systems, faction mechanics, hero cards) fail because the answers live in corpus files, not vault files. The vault has working drafts and session records; the corpus has the canonical answers.

## bge-small Query Prefix

bge-small-en-v1.5 requires queries to be prefixed with:
`"Represent this sentence for searching relevant passages: "`

This is handled automatically in `vault_rag.py`'s `query_vault()` function.
The prefix is NOT applied during indexing (only to queries). This asymmetry
is required by the model — omitting the prefix degrades retrieval quality.

## Maintenance

### After vault changes (new handovers, new design docs, etc.)
```bash
python vault_rag.py reindex
```
This only re-embeds files whose mtime is newer than the last index. Fast for
incremental changes.

### After Cursor updates the corpus (git pull/commit on tcg-engine)
```bash
python vault_rag.py reindex
```
The corpus is a git repo owned by Cursor. When Cursor pushes new lore or design changes, the files appear on the VPS (via git pull or sync). Run `reindex` — it scans both vault and corpus, finds the ~3 files that changed by mtime, re-embeds only those. Takes seconds, not minutes. No git interaction — the index reads files, never writes to them. The repo stays read-only.

### Backup
Copy `vault_index.db`. That's it. The index is fully derived from source files
and rebuildable in ~9 minutes.

## Removal (if useless)

```bash
rm -rf /root/.hermes/rag-venv
rm /root/.hermes/docs/Paul/vault_index.db
rm /root/.hermes/docs/Paul/vault_rag.py
```

Three commands. Clean. Nothing touched the vault source files. The index is a
derived artifact — deleting it loses nothing that can't be rebuilt in 9 minutes.

## Future: Path A (Auto-Prefetch via memory.provider)

The current system is Path B (active retrieval — Paul calls the tool when he
knows he needs to search). Path A would wire the same query function into the
Hermes `memory.provider` plugin's `prefetch(query)` hook so relevant context
auto-injects before each turn based on what Joe says.

**LanceDB memory provider plugin** (`lancedb/hermes-agent-memory`) is the
production-grade option for Path A. It plugs into the `memory.provider` config
slot and has the `prefetch(query)` hook built in. Would need a vault ingestion
adapter (chunk → `lancedb_remember` each chunk).

**Effort to Path A:** ~1 day (install plugin, write vault ingestion script,
configure `memory.provider: lancedb` in config.yaml).

## Research Reports

- Full research report: `workspace/RAG_Research_Report_2026-06-21_Paul.md`
- Local RAG research: `workspace/Local_RAG_Research_2026-06-21_Paul.md`
- Rook's spike report: `/root/.openclaw/agents/rook/workspace/rag_spike_report.md`
- Condensed findings: `references/rag-research-findings.md`

## Changelog

- **2026-06-22 (short-name pitfall)** — Documented "Sal" vs "Salt" ambiguity: short queries match whoever has the most indexed surface area. Add context to name queries.
- **2026-06-22 (foreground timeout)** — Documented that full reindex exceeds 600s foreground limit. Always use background + notify.
- **2026-06-22 (consolidation)** — Excluded Session Context and Paul_Handoff from index. Dropped 4,110 duplicate chunks (14,460 → 10,350), 130 duplicate files (656 → 526). DB grew to 55MB (SQLite doesn't shrink after DROP TABLE — vacuum pending).
- **2026-06-22 (query v2)** — Major query pipeline upgrade: fetch 4× candidates (dedup headroom), content-based deduplication (120-char fingerprint), structural boosting (table/proper noun/header signals for entity queries, source priority for canonical files), and adjusted-score reranking. Fixes the "canonical roster table buried by duplicate workspace drafts" failure mode. See § Query Pipeline.
- **2026-06-22** — Added Pitfalls section: don't go raw SQL against the index (column names are `file`/`header`/`text`, not `content`/`source_file`). Use CLI `search` command for programmatic access.
- **2026-06-21 (corpus added)** — Index expanded from vault-only (6,938 chunks / 285 files) to vault + corpus core (14,460 chunks / 656 files). Added INDEX_DIRS config with 8 source directories, EXCLUDE_PATTERNS to filter archive/bridge/git. Bruiser stage system test (previously failed) now passes — canonical lore lives in the corpus, not the vault. Full reindex: ~17 minutes. DB: 33 MB.
- **2026-06-21 (initial)** — vault_rag.py built, indexed (6,938 chunks), and tested with 3 queries. All passed. System is live.
