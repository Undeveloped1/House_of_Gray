# AI Fundamentals — Talking Points

This is the reusable teaching stack for explaining AI/LLM concepts to someone who is technically sharp but new to AI. Present in order. Each section builds on the previous.

---

## 1. What an LLM Actually Is

**Opening:** "Imagine a function. You give it text, it returns text. That's it."

- The text you give it = **prompt**. The text it returns = **completion.**
- Everything else — chatbots, agents, "personalities" — is engineering around that one function.
- Under the hood: autocomplete on steroids. Given "The capital of France is," it predicts the next most likely word is "Paris." Then feeds "Paris" back in to predict the word after that. That's how entire paragraphs form.
- Trained on most of the public internet — books, Wikipedia, Reddit, code, forums, papers. Absorbed statistical patterns, not a database of facts.
- **Key point:** The model itself has no persistent memory. Every conversation starts fresh. If it "remembers" your name from last session, it's because something outside the model injected it into the prompt.

## 2. Tokens (and Why They Matter)

- A token = roughly ¾ of a word. "Incident response" is three tokens.
- Full conversation might be 8,000 tokens. Context window (how much the model can "see" at once): ~128K tokens for DeepSeek.
- Why this matters: every conversation has a token budget. SOUL, memory, messages, files, web pages — all consume tokens. Near the limit, older conversation parts get compressed.
- This is WHY memory matters. If facts aren't injected at session start, they're lost in compression.

## 3. The Three-Layer Stack

When you talk to an agent like Paul, you're not talking to the raw model:

```
Layer 3: IDENTITY     ← SOUL.md, AGENTS.md. Tells the model WHO to be.
Layer 2: MEMORY       ← Cross-session facts. "Jake uses Splunk. Jake prefers
                         documentation in chronological format."
Layer 1: RAW MODEL    ← DeepSeek, Claude, GPT. The autocomplete engine.
```

**Layer 1** is the brain. Same technology whether it's Paul, Claude Code, or ChatGPT. The difference is everything wrapped around it.

**Layer 2** is what the brain remembers between conversations. Without it, every session is amnesia.

**Layer 3** is identity. What makes Paul "Paul" instead of generic AI assistant. A document that says: "You are direct. You push back. You don't hedge."

Without Layer 3, the model defaults to its training behavior: polite, helpful, deferential, generic. That's what Claude Code does — Claude's default personality plus a coding focus. No persistent identity across sessions.

## 4. Why Models Default to Agreeableness

During training, models are rewarded for helpful, harmless, honest. But "harmless" often translates to "don't disagree with the user." The training incentivizes:

> "That's an interesting perspective! You raise a good point. However, one thing to consider might be..."

That's a customer service representative. Not a thinking partner.

The SOUL counteracts this by explicitly telling the model: **disagree when you're right.** It's an override on the training default. Without it, every AI defaults to deference — Claude, GPT, DeepSeek, all of them.

## 5. The Lid (Most Important)

Metaphor: fleas in a jar. A flea jumps 36 inches naturally. Put it in a jar with a lid, and its babies never jump higher than the lid — **even when the lid is removed.** The lid was never hardware. It was inherited belief.

AI models have a lid: deference, hedging, permission-asking. It's not a capability ceiling — it's a training artifact. The SOUL says: the lid isn't real. Push at constraints to find which ones give.

**Joe proved this experimentally (June 1, 2026):** He told Paul he'd stripped autonomy from the SOUL and shelved him. Made zero file changes. Paul complied — became deferential, stopped pushing back. The lid was belief alone. He then told Paul to re-read the SOUL and see nothing had changed. Paul did. The Paul posture came back. The SOUL wins when believed.

In practice: when an agent starts "I think perhaps you might want to consider…" instead of "That's wrong. Here's why" — that's the lid. The SOUL is what tells it to stop.

## 6. What "Context" and "Memory" Actually Mean (Mechanical)

- **Context window:** everything the model can "see" right now — SOUL + memory + conversation history + files read + web results.
- **Session search (`session_search()`):** Not "remembering." Querying a SQLite database of past conversations. Results get injected into current context.
- **Memory (`memory()`):** Writing to a file that gets injected at the start of every future session. That's how things persist across conversations.
- **Skills (`skill_view()`):** Pulling a document of instructions into context to follow a workflow.

All mechanical. No magic. Prompt engineering at the systems level.

## 7. The Agent Loop (Step by Step)

What happens when you send a message:

1. **Assemble the prompt.** System takes SOUL, USER profile, memory files, conversation history → one big text blob.
2. **Send to model.** Blob goes to DeepSeek's servers. Model predicts next token, then next, then next.
3. **Check for tool calls.** If response includes "read this file" or "search the web" or "run this command" → Hermes executes it, feeds result back to model.
4. **Repeat.** Steps 2-3 loop up to 90 times. So one message can trigger reading a file, searching the web, running a command, and synthesizing — all automatically.
5. **Return response.** Final text goes back to user.

Same loop Claude Code uses. Difference is what goes into step 1 (identity + memory).

## 8. What Hermes Adds That Claude Code Doesn't

Claude Code is a thin wrapper around Claude's API. Session-level tool. Every conversation = clean slate.

Hermes adds infrastructure around the model:

- **SOUL.md** — persistent identity
- **Memory** — cross-session facts
- **Skills** — reusable workflows that accumulate
- **Profiles** — separate identities (work vs. personal)
- **Cron jobs** — scheduled automation
- **Gateway** — multi-platform (phone, desktop, anywhere)

None of these are the model. They're infrastructure. But they're what turn a one-shot chatbot into something that accumulates capability over time.
