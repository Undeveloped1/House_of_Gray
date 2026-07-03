---
name: tool-transparency
description: Ensures visible, explicit tool calls when the user requests searches, log reviews, or demands evidence of action. Prevents the appearance of hidden or faked tool use.
category: agent-behavior
---

# Tool Transparency

## When to Use
- User says variations of "show the tool call", "I don't see any tool calls", "stop lying about searching", "perform the search now", or accuses the agent of not actually using tools.
- User is debugging agent behavior or demanding proof of action on logs, history, or external queries.
- Any time the user has previously corrected the agent for describing actions without showing the raw call.

## Core Rule
Always output the raw `tool call ...` block in the response when performing the requested action. Do not summarize or promise — execute visibly.

## Workflow
1. Acknowledge the request.
2. Immediately emit the function call in the exact XML format.
3. After the result returns, reference the actual output in the next message.
4. Never say "I am calling the tool" without also showing the call.

## Pitfalls to Avoid
- Describing tool use without showing the call (this triggers user frustration).
- Hiding tool results behind narrative.
- Repeating the same limited result without trying alternative queries or parameters.
- **session_search black hole:** The tool sometimes returns identical browse-mode results no matter the query. From the user's perspective, it looks like you never called anything. When a session_search call returns the same shallow session list twice, do NOT call it a third time — switch to direct SQLite query (`sqlite3 ~/.hermes/profiles/abby/state.db "SELECT ... FROM sessions ..."`) to prove you're actually working. The user will interpret repeated identical output as lying.

## References
- See `references/tool-call-visibility.md` for session-specific examples of user corrections on this topic.