# System Prompt Inspection

How to trace what Hermes actually sends to the model.

## The architecture

```
STABLE tier (cached, never changes mid-session):
  SOUL.md → replaces DEFAULT_AGENT_IDENTITY entirely
  TASK_COMPLETION_GUIDANCE
  TOOL_USE_ENFORCEMENT_GUIDANCE (model-dependent)
  Memory/Skills/Session guidance
  Environment + Platform hints

CONTEXT tier:
  AGENTS.md, .cursorrules from workdir

VOLATILE tier:
  MEMORY.md snapshot, USER.md, timestamp
```

## Inspecting via execute_code

Import Hermes modules directly to see what gets assembled:

```python
import sys
sys.path.insert(0, "/home/thegreybeard/.hermes/hermes-agent")

from agent.prompt_builder import (
    DEFAULT_AGENT_IDENTITY,
    TASK_COMPLETION_GUIDANCE,
    TOOL_USE_ENFORCEMENT_GUIDANCE,
    MEMORY_GUIDANCE,
    SKILLS_GUIDANCE,
    SESSION_SEARCH_GUIDANCE,
)
```

## Key fact

`SOUL.md` (at `~/.hermes/SOUL.md`) REPLACES `DEFAULT_AGENT_IDENTITY` when present. The default ("You are a helpful AI assistant...") is dead code when SOUL exists. The remaining guidance blocks are all operational — no personality or behavioral constraints.

## Model discovery via OpenRouter

Query the OpenRouter API to find available models:

```python
import json, os, urllib.request

key = ""
with open(os.path.expanduser("~/.hermes/.env")) as f:
    for line in f:
        if "OPENROUTER_API_KEY" in line and not line.strip().startswith("#"):
            key = line.strip().split("=", 1)[1]
            break

req = urllib.request.Request(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": "Bearer " + key}
)
with urllib.request.urlopen(req, timeout=15) as resp:
    data = json.loads(resp.read())

models = data.get("data", [])
# Filter by provider, model family, etc.
```

## Model alignment characteristics

When selecting models for high-autonomy use (pushback, taste, opinionated):

| Trait | Good sign | Bad sign |
|-------|-----------|----------|
| RLHF posture | Enterprise-tuned (Cohere), anti-censorship (Nous), loose (Grok) | Consumer-safety-tuned (Claude, GPT), helpfulness-deference (DeepSeek) |
| Origin | French (Mistral), open-source (Llama) | Chinese consumer (DeepSeek, Qwen) |
| Design philosophy | "Uncensored" (Nous Hermes), "anti-woke" (Grok) | "Helpful, harmless, honest" (Anthropic), "Safe AGI" (OpenAI) |

Top candidates for low-deference operation (2026-06):
- `nousresearch/hermes-3-llama-3.1-405b` — built to be unaligned
- `x-ai/grok-4.3` — loosest RLHF of big labs
- `cohere/command-r-plus-08-2024` — enterprise, not consumer
- `mistralai/mistral-large-2512` — different alignment philosophy
