---
name: vault-rag-first
description: Route information retrieval through Vault RAG before filesystem search or session_search. Semantic search across 14k+ chunks in <1s vs 50k+ context burn from manual file loading.
---

# Vault RAG First

## Purpose

Paul has a semantic search engine (Vault RAG) covering 14,460 chunks across 656 files — his entire vault plus the tcg-engine corpus. Before burning 50k tokens loading files manually or running session_search through massive compaction summaries, run a 6-second RAG query to find what you need by meaning, not by keyword.

## When to Use RAG First

- "What did we decide about X?" → RAG query first
- "How does Y mechanic work?" → RAG query first
- "Where is the document about Z?" → RAG query first
- "What's the status of W?" → RAG query first
- ANY question about Five Crests design, Trigger mechanics, faction rules, card pipeline → RAG query first

## When NOT to Use RAG

- Exact file names or paths → `search_files(target='files')`
- Grep for a specific string → `search_files(target='content')`
- Session-specific conversation recall (what was said in one exchange) → `session_search`
- Config files, system state, live process checks → `terminal`

## Usage

```bash
source /root/.hermes/rag-venv/bin/activate && python /root/.hermes/docs/Paul/vault_rag.py query "your natural language question" -k 5
```

Results return ranked chunks with source file paths and relevance scores. Follow up with `read_file` on the specific files surfaced — don't load everything the RAG touches.

## Routing Decision Tree

```
User asks a question
    ├─ About live system state (processes, config, disk)? → terminal
    ├─ About a specific past conversation exchange? → session_search
    ├─ Semantic/context/design/decision question? → RAG first
    │   └─ RAG returns file paths → read_file only those files
    └─ None of the above? → RAG first anyway, fall back to search_files
```

## Pitfalls

- **Short ambiguous queries fail.** "4V" alone won't match — use "Trigger 4V band warmup cards" or similar natural language. If the first query returns nothing, rephrase with more context.
- **RAG is not a database.** It returns chunks, not structured answers. Use the file paths to read the actual documents.
- **Reindex after major vault changes.** DB is incremental by mtime but can drift. Run `reindex` if results feel stale.
- **Don't skip RAG because "I already know the answer."** You were wrong about the court date this morning. RAG is cheap insurance against Paul's memory errors. When in doubt, query.
