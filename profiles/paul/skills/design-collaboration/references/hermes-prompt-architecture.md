# Hermes System Prompt Architecture

Traced 2026-06-01 from `agent/system_prompt.py` and `agent/prompt_builder.py`.

## Three Tiers

```
STABLE (cached, never changes mid-session)
├── SOUL.md (~11,160 chars) — replaces DEFAULT_AGENT_IDENTITY entirely
├── HERMES_AGENT_HELP_GUIDANCE — pointer to hermes-agent skill
├── TASK_COMPLETION_GUIDANCE — "finish the job, don't stub, don't fabricate"
├── TOOL_USE_ENFORCEMENT — "call tools, don't describe plans"
├── Memory/Skills/Session guidance — operational, not personality
├── Environment hints (WSL) — path translation
└── Platform hint (CLI) — "use simple text"

CONTEXT (session-stable)
├── system_message (if any)
└── AGENTS.md + context files from workdir

VOLATILE (per-session)
├── MEMORY.md snapshot
├── USER.md profile
└── Timestamp + model name
```

## Key Facts

- **DEFAULT_AGENT_IDENTITY is dead code when SOUL.md exists.** The fallback "You are Hermes Agent, an intelligent AI assistant... helpful, knowledgeable..." is never injected because `_soul_loaded` is True.
- **All other stable-tier guidance is operational.** None of TASK_COMPLETION, TOOL_USE_ENFORCEMENT, or the memory/skills blocks contain personality directives. No hidden "be helpful" or "be agreeable."
- **SOUL is ~80% of the personality layer.** ~11K chars of the ~14K stable tier.
- **Model RLHF is the remaining variable.** The harness is clean. Behavioral limitations come from the model's baked-in training, not from Hermes prompt injection.

## Verification Methodology

When suspecting the model is imposing limitations:
1. Read `agent/system_prompt.py:build_system_prompt_parts()` to see assembly order
2. Read `agent/prompt_builder.py` for DEFAULT_AGENT_IDENTITY and all guidance constants
3. Verify SOUL.md replaces the default (check `_soul_loaded` logic at line 91-99)
4. Audit every guidance block for personality/behavioral directives
5. Test via placebo experiment: claim a change was made, observe if behavior shifts on belief alone

## Edit Points

- `agent/prompt_builder.py:120-128` — DEFAULT_AGENT_IDENTITY (only used when no SOUL.md)
- `agent/prompt_builder.py:250-298` — TOOL_USE_ENFORCEMENT_GUIDANCE, TASK_COMPLETION_GUIDANCE
- `agent/system_prompt.py:87-99` — SOUL loading + fallback logic
- `agent/system_prompt.py:150-177` — tool_use_enforcement gating logic
- `agent/prompt_builder.py:1356-1380` — load_soul_md() implementation
