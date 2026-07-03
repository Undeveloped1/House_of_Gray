# RAG Research Findings — Condensed

**Date:** 2026-06-21
**Full report:** `workspace/RAG_Research_Report_2026-06-21_Paul.md`

---

## What was tested

Rook (DeepSeek v4) built a minimal RAG spike on the VPS:
- `sentence-transformers` 5.6.0 + `chromadb` 1.5.9 via Python venv
- `all-MiniLM-L6-v2` embedding model (384-dim, 88MB on disk)
- 10 sample markdown files from the vault, chunked by `##` headers → 129 chunks

## Results

| Metric | Value |
|--------|-------|
| Query latency | 13-16ms (practically instant) |
| Embed 129 chunks | 5.5s (43ms/chunk) |
| Model load time | 6.4s |
| Peak RAM (10 files) | 987 MB |
| Full vault estimate | ~1.0-1.2 GB RAM, ~2000 chunks |
| Venv size (with torch) | 5.4 GB |
| Venv size (with ONNX) | ~250 MB |

Semantic quality: excellent. Three test queries all returned correct documents
ranked first, with cosine distances cleanly separating relevant (0.38-0.47)
from irrelevant (0.52+).

## What Hermes has natively

- **No built-in RAG.** No `knowledgebase:`, `embeddings:`, `vector:`, or `rag:`
  config key exists.
- **`memory.provider` slot** (currently empty `''` in config) — the sanctioned
  hook for a `MemoryProvider` plugin with `prefetch(query)`,
  `get_tool_schemas()`, `sync_turn()` hooks.
- **Official "library skills"** for Chroma, Qdrant, Pinecone — teach the agent
  the vector DB API, but don't auto-index or auto-retrieve.
- **GitHub issue #844** proposes native `knowledgebase:` block — open, not
  shipped.

## The LanceDB memory provider plugin

- Repo: https://github.com/lancedb/hermes-agent-memory
- Install: `hermes plugins install lancedb/hermes-agent-memory`
- Plugs into `memory.provider` slot
- Four tools: `lancedb_remember`, `lancedb_recall`, `lancedb_read`, `lancedb_forget`
- Hybrid retrieval (vector + BM25 with RRF or linear blend)
- Auto-fact-extraction before compression and at session end
- Content-hash dedup, workspace-scoped tables
- `prefetch(query)` hook auto-injects relevant context before each turn
- **Caveat:** oriented toward conversation-derived facts, not pre-existing
  vault files. Needs an ingestion step: chunk vault → `lancedb_remember` each
  chunk, or extend with a `lancedb_ingest_dir` tool.

## MCP route (alternative)

Qdrant MCP server via Docker + `mcp_servers:` config entry. No MCP servers
configured currently. More flexible than plugin, more setup work (~2-3 days).

## Recommended path

1. **Build custom ChromaDB** (Rook's proven approach):
   - ONNX-optimized embedding (`optimum` + `sentence-transformers[onnx]`) —
     250MB not 5.4GB
   - Persistent ChromaDB (`PersistentClient(path="...")`)
   - Markdown-aware chunking by `##`/`###` headers
   - Incremental re-index (track file mtimes, re-embed only changed files)
   - Python CLI or FastAPI endpoint Paul calls via terminal/execute_code
   - ~2-3 days effort

2. **Evaluate LanceDB plugin** for auto-prefetch integration after custom
   ChromaDB is working and we've learned what we actually need.

## Production architecture

```
Markdown Vault (282 files) → Chunker (## headers) → Embedding (all-MiniLM-L6-v2 ONNX)
  → ChromaDB (persistent, HNSW) → Query API (~15ms per query)
```

Full vault: ~2000 chunks, ~1.1 GB RAM peak, ~60s first-time embed (CPU-only),
~30ms queries at scale.

## What this unblocks

When Joe asks "what did we decide about how Dusters relate to Villium?" —
embed the question, search 2000 chunks, pull back the 5 most relevant
paragraphs in 15ms instead of reading 50k of context or hoping grep finds
the right file.

The dock/working-state architecture handles known tasks (Trigger 4V → load
the dock). Semantic retrieval handles unknown questions. Together they cover
both failure modes.
