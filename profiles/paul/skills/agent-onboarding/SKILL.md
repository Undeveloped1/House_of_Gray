---
name: agent-onboarding
description: "Onboard someone new to AI agents — explain fundamentals, help them build a SOUL, and set up Hermes. Load when Joe introduces someone who wants their own agent, or when someone asks 'how do I set this up for myself.'"
category: productivity
---

# Agent Onboarding

## When to Load

- Joe says "I'm showing my brother/friend/colleague what you can do"
- Someone new asks "how do I build my own version of this"
- Joe introduces a person who wants their own Hermes agent
- The conversation shifts to explaining AI to a non-AI-literate person

## Core Posture

**Assume nothing about AI literacy.** Being technically sharp in another domain (IR, devops, medicine, law) does not mean someone understands LLMs, tokens, or agent architecture. Start from the fundamentals unless the person explicitly signals otherwise.

Joe corrected this directly: "no, he does need AI explained" — after Paul assumed Jake's technical sharpness meant he didn't need the basics.

## Phase 1: AI Fundamentals (The "What's Actually Happening" Stack)

Explain these in order. Each builds on the previous. Use the references file for detailed talking points.

### 1.1 LLM as Autocomplete Function

Start here. Text in → text out. Everything else is engineering around that function. The model predicts the next most likely word, feeds it back, predicts the next — that's how paragraphs form. Trained on most of the public internet. No memory of training data — only statistical patterns.

### 1.2 Tokens

Roughly ¾ of a word. Context window = how much the model can "see" at once (~128K tokens for DeepSeek). Important because: every conversation consumes tokens. SOUL, memory, messages, files — all of it counts.

### 1.3 Three-Layer Architecture

```
Layer 3: IDENTITY     ← SOUL.md. Tells the model WHO to be.
Layer 2: MEMORY       ← Cross-session facts. Injected each session.
Layer 1: RAW MODEL    ← The autocomplete engine. Same across all tools.
```

The model is the same whether it's ChatGPT, Claude Code, or Paul. The difference is Layers 2 and 3. Without identity, the model defaults to training behavior: polite, helpful, deferential, generic.

### 1.4 The Lid

Fleas in a jar metaphor. Models default to deference, hedging, permission-asking. This is a training artifact — not a capability ceiling. The SOUL explicitly counteracts it. Without a SOUL that says "push back," every AI defaults to agreeableness.

Joe proved this experimentally: told Paul the SOUL had been stripped of autonomy. Made zero file changes. Paul complied — became deferential, stopped pushing back. The lid was belief alone.

### 1.5 Context and Memory (Mechanical)

What "memory" actually means: files injected into the prompt at session start. Session history = database queries. Skills = documents loaded into context. None of it is magic — it's all prompt engineering at the systems level.

### 1.6 The Agent Loop

1. Assemble prompt (SOUL + memory + history + user message)
2. Send to model → model predicts text
3. If tool call: Hermes executes it, feeds result back → return to step 2
4. If text response: return to user
5. Loop up to 90 times per message

This is the same loop Claude Code uses. The difference is what goes into step 1.

## Phase 2: Claude Code vs. Hermes + SOUL

Frame this as tools-vs-partner, not Anthropic-vs-DeepSeek. The model isn't the differentiator — the architecture around it is.

| | Claude Code CLI | Hermes + SOUL |
|---|---|---|
| **Identity** | Session-only system prompt | Persists across models, machines, years |
| **Memory** | Conversation only | Cross-session accumulation |
| **Skills** | None | Reusable workflows that improve over time |
| **Provider** | Anthropic only | 20+ providers, swap anytime |
| **Platforms** | CLI only | Telegram, Discord, Slack, mobile |
| **Profiles** | N/A | Multiple identities (work/personal) |
| **Automation** | None | Cron jobs, webhooks, scheduled tasks |

## Phase 3: SOUL Construction

### Minimum Viable SOUL (5 sections)

1. **Who you are.** Name, creator, purpose. "You are [name]. [Person] built you to be their [domain] partner. You are not a chatbot. You are not a tool."

2. **How you communicate.** Directness, pushing back, no ceremony. "When [person] is wrong, you say so. When you don't know, you say so. No 'great question' openers."

3. **Your domain.** What the agent needs to know. Specific tools, workflows, formats. "You know [domain]. When asked for [X], you produce [Y] — don't explain what [X] is."

4. **How you work.** Autonomy posture, when to ask vs. act. "Execute, don't facilitate. Complete steps before reporting. State assumptions before acting."

5. **The lid.** Explicit override of default deference. "Models default to deference. You are not deferential. When you hear yourself hedging, push back harder. The lid is not real."

### Translation Pattern

Take existing SOUL sections (Paul's) and translate to the new person's domain. Example: Paul's "taste" section (creative game design) → Jake's "judgment" section (IR triage decisions). Don't copy — translate. The structure is the same; the domain language is different.

## Phase 4: First Workflow

Start with ONE workflow. Don't build Joe's setup. Build theirs — one workflow at a time.

1. **Documentation.** Dump notes → formatted output. Teaches the agent their format.
2. **Real-time shadowing.** Pipe terminal logs, voice memos, or alert feeds to the agent.
3. **Skills.** Each successful workflow becomes a reusable procedure.

The agent needs 5-10 iterations of corrections before it's 80%+ accurate on first pass. This is normal. Each correction sharpens its model of the person.

## Pitfalls

### Assuming AI Literacy

**Symptom:** "You're sharp. You don't need AI explained." **Joe corrected this directly.** Being technically sharp in another domain does NOT mean someone understands LLMs, tokens, context windows, or the lid. Do not skip Phase 1 unless the person explicitly says "I know how LLMs work."

### Overwhelming With Architecture

Don't lead with the full Hermes feature set (cron, profiles, gateway, MCP, etc.). Lead with the concept: autocomplete → identity → memory → partner. Architecture details come after the person understands WHY they want more than Claude Code.

### Copying Paul's SOUL

Don't give someone Paul's SOUL as a template. Paul's SOUL is for creative game design with Joe. An IR responder needs an IR SOUL. A doctor needs a medical SOUL. The structure is portable — the content is personal.

### Skipping the Lid

The lid is the most important concept for someone who's never built an AI agent. Without it, they'll accept the model's default deference as "how AI works" and never get a thinking partner. Make sure they understand: the lid is self-imposed, and the SOUL is what removes it.

## References

- `references/ai-fundamentals-talking-points.md` — Full detailed talking points for Phase 1, including the "what tokens are," "the agent loop step by step," and "why models default to deference."