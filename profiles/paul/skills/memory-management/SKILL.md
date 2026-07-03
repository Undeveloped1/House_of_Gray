---
name: memory-management
description: "Design, operation, and maintenance of layered memory systems for long-term creative and technical work."
version: 2.0.0
author: Paul
---

# Memory Management

Full original archived at `docs/Paul/workspace/memory-management-archive.md`.

## Two-System Architecture

### System 1 — Operational Memory (sticky note)
- The Hermes `memory()` tool store: 10,000 char cap.
- Purpose: keeps Paul from being stupid THIS session. When Joe says "let's work on Trigger," Paul already knows the curve, crew split, Mark philosophy.
- Governed by: Memory Lifecycle Protocol (dedup, tier, prune, cap).
- **Not** a knowledge base, vault, or queryable brain.

### System 2 — The File Vault (substrate Paul reads from)
- 650+ files across `/root/.hermes/docs/Paul/` and `/root/tcg-engine/docs/` plus `state.db`.
- Purpose: accumulated knowledge base. Paul reads from it; Joe does NOT browse.
- Joe lock: "why would I want to manually search Obsidian? The entire reason I want this memory is so that when I say 'we're going to work on Trigger 4V' you already know what I'm talking about."

### Context Architecture (Dock / Working State / Corpus)

| Layer | What | When loaded | Example |
|-------|------|------------|---------|
| **Dock** | Stable reference, built once | Every session | Trigger design rules, crew CAN/CANNOT, Contract Loop, slot table |
| **Working state** | Current state, grows as cards lock | Task-specific sessions | Locked cards, open slots, what ignites at this V |
| **Corpus** | Permanent, append-only | Deep reference on demand | Full Set in dropbox, lore files |

The dock is built ONCE. Working state is the only thing that changes. Warmup docs were the mistake — every band rebuilt the dock from scratch.

## RAG — Semantic Retrieval (IMPLEMENTED)

`vault_rag.py` is live: 14,460 chunks across 656 files, bge-small-en-v1.5 + sqlite-vec. Queries return in ~6s.

**RAG-First Priority Rule:** RAG is your FIRST tool for vault/corpus questions. Not second. Not "after session history."

| Priority | Tool | When |
|----------|------|------|
| **1st** | `vault_rag.py query` | Any vault/corpus question. ~6s, ~500 chars context. |
| **2nd** | `session_search` | Conversation-level detail RAG can't give |
| **3rd** | `search_files` + `read_file` | Only when RAG + session_search both miss |

**Usage:** `source /root/.hermes/rag-venv/bin/activate && python /root/.hermes/docs/Paul/vault_rag.py query "how do trigger contracts work" -k 5`

**Pitfalls:**
- **Don't abandon after one bad query.** Iterate phrasing, add entity names. Two queries minimum before fallback.
- **Markdown tables embed poorly.** Use structural boosting (tables 1.5×, proper nouns 1.3×, canonical files 1.15×).
- **Reindex in background:** 13-17 minutes. Use `notify_on_complete=true`.
- **RAG can't find hidden files.** Always use absolute path (`/root/.hermes/docs/Paul/vault_rag.py`).

## Daily Handover

| Session type | Where | Handover? |
|-------------|-------|-----------|
| Design session | Super group under topic | ✅ Always |
| Working session | DM — substantive | ✅ Always |
| Transactional | DM — quick, status, phone | ❌ No (in state.db) |
| Upgrade trigger | Transactional → real work | ✅ Write at stopping point |

### File Structure
- **Top:** Synopsis (2-4 sentences)
- **Middle:** Timestamped Compression sections (What / Why / How)
- **Bottom:** Detailed Work Log + Open Items / Next Steps
- One file per calendar day: `Brain/Daily/YYYY-MM-DD_Daily_Handover.md`

## Session Lifecycle

### Session Start
1. SOUL, USER, AGENTS auto-load. Verify USER.md actually loaded — don't assume.
2. Review today's Daily Handover.
3. Read Working Memory.
4. Pull tcg-engine repo.
5. **Identity calibration:** Files loaded ≠ identity embodied. Actively correct against default helpful-deference.

### Session Close
**Both close-session and close-the-night:**
1. Daily Handover updated
2. Compression written
3. Working Memory updated
4. Session Context copies saved

**Close-the-night only:**
5. DREAM markers processed
6. Handover marked final
7. RAG reindex if vault files changed

**Close-session ≠ close-the-night.** Don't lock the handover prematurely. Match Joe's signal.

### Compression
- Triggered by user request, not proactively. Joe values texture — only compress when there's a real constraint.
- Each compression: timestamped, concise, decision-focused.
- Working Memory: slim (last 1-2 compressions). Older → Daily Handover.

## Core Memory (`memory()` tool store)

### What belongs
- Durable user preferences about HOW work should be done
- Non-negotiable operational expectations
- Foundational design philosophy
- Environment facts relevant across many sessions

### What does NOT belong
- Session compressions, work summaries, task progress
- One-time setup facts once stable
- Info verbatim in loaded vault docs
- RAG-retrievable reference material (< 10 seconds)
- Per-person details for autonomous agents (Rook, Abby, Jake)

### Relevance Filter (Joe lock)
Memory is an index card, not a filing cabinet. Three questions per entry:
- Is this still relevant? (Phase ended = stale → kill)
- Does this need to inject EVERY turn? (RAG can retrieve in 6s → move to vault microdoc)
- Should this be hardcoded into a pillar? (Joe said "always" → promote to SOUL/USER/AGENTS)

### Promote to Pillars
When Joe has corrected behavior repeatedly or stated "do this always":
| Signal | Action |
|--------|--------|
| "Do this always" / "Never do X" | Promote to SOUL/USER/AGENTS |
| Corrected 3+ times across sessions | Pillar candidate |
| Behavioral boundary | SOUL.md |

After promoting: **kill the memory entry.** Pillar is authority. Duplicate = waste + drift risk.

### Pitfalls
- **Stale directives overwrite hard coding.** Pillars win. Kill conflicting memory entries.
- **One-time events are not core memory.** If documented in 2+ other places, don't store.
- **Evaluations, not just events.** Capture Joe's assessment of performance, not just factual timeline.
- **Check redundancy before adding.** Dedup takes 10 seconds.
- **Clinical third-person = distance.** Write in your voice. Never "the user."
- **Remove, don't condense redundant entries.** Delete the less specific one.

## DREAM: Marker Protocol

Format: `DREAM: <target>: <path> | <content>`
Valid targets: `memory`, `design`, `skill`, `user`, `vault`.

Process at compression points: scan unprocessed markers → apply valid, discard stale → move to `### Processed`.

## References
- Daily handover template: `references/daily-handover-template.md`
- RAG setup: `references/vault-rag-setup.md`
- Vault audit: `references/vault-as-brain-audit.md`
- Context budget audit: `references/context-budget-audit.md`
- Memory Lifecycle Protocol: `Brain/Protocols/Memory_Lifecycle_Protocol.md`
