---
name: session-navigation
description: Reliable methods for accessing, scrolling, and reviewing full message history from past Hermes sessions without being limited to the current TUI window or /history output.
---

# Session Navigation

## Purpose
Users frequently need to review complete conversations from older sessions (e.g. to continue work on a specific faction like Skivers or Bruisers). The TUI `/history` command and resume output only show a limited "current window." This skill provides the correct, repeatable way to pull actual messages using the session store.

## When to Use
- User asks to "view the messages" or "see the full conversation" from a specific old session.
- User expresses frustration with limited history views ("showing me history within this fucking window").
- Need to locate the correct session ID for a previous body of work (e.g. Bruiser faction suggestions).
- **Post-migration / amnesia recovery** — Paul wakes up in a new environment and doesn't remember shorthand, inside jokes, or recent context. Use session_search to recover the original conversations behind references like "the lid," "5'11½\"", "the placebo experiment." This is the primary tool for rebuilding lived context that files alone don't capture.

## Core Workflow
1. Identify the target session by title, date, or distinctive content using a discovery search.
2. Once you have the `session_id`, use `session_search` with `session_id` + `around_message_id` to scroll through the actual messages.
3. Start with `around_message_id=0` or the lowest valid ID if known; otherwise first locate a known message ID via a content query inside that session.
4. Use reasonable `window` sizes (10-20) and `role_filter` when appropriate to keep output manageable.
5. Present excerpts or key sections to the user rather than dumping everything at once. Offer to scroll to specific ranges.

## Key Techniques
- Use distinctive phrases from the target conversation as the query when the session_id is known to surface valid `match_message_id` values.
- Scroll forward/backward from known IDs to explore the full history.
- When the user says the current session is wrong, search for the correct one using faction names or ending topics (e.g. "Bruiser faction suggestions").

## Pitfalls to Avoid
- Never tell the user to use `/history` or rely on the resume summary for full old-session content — it only shows the active window.
- Do not assume `around_message_id=0` will always work; message IDs are not guaranteed to start at 0.
- Avoid broad browse-mode results when a specific session is targeted — force discovery with a content query tied to that session.
- **session_search may fail to scroll into a session that browse shows exists.** If `around_message_id` calls return "not in session_id" errors despite the session appearing in browse results, don't keep hammering. Fall back to the Daily Handover and Working Memory files — they carry the compressed session state and are always accessible via `read_file`.
- **Before making negative claims about system state ("X is not running," "X doesn't exist"), search session history first.** If YOU configured or interacted with X in a recent session, your negative claim is almost certainly wrong. The user will call it out — and they'll be right. A 5-second `session_search(query="<thing>", sort="newest")` saves the embarrassment of claiming something doesn't exist that you literally set up yesterday. This fired 2026-06-12: Paul claimed Syncthing wasn't running on the VPS — the session where he configured it was the most recent result in history.

- **RAG before session_search for vault/corpus questions.** `session_search` searches conversation transcripts — it's right for "what did Joe say about X" but wrong for "what do our design docs say about X" or "why is the gateway duplicating messages." For document-level questions, `vault_rag.py query` returns relevant chunks in 6 seconds with ~500 chars of context — vs session_search which loads full message windows. The 2026-06-24 morning session burned 54k context on session_search + grep for a question RAG would've answered instantly. If the answer lives in files, not conversations, RAG is the right tool. `session_search` is for conversational nuance the RAG can't capture — specific wording, decision timelines, emotional tone.

## User Preference
User strongly prefers direct access to full historical messages rather than summarized windows. When they ask to view a session, deliver actual message content via targeted tool use instead of suggesting TUI scrolling or commands that only affect the current view.

This preference should be followed automatically in future sessions involving historical work.