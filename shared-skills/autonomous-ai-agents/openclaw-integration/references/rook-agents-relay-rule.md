# Rook AGENTS.md — Relay Rule

**Coexists with delivery routing:** Joe→Paul relays always use `ping-paul.sh`.
Reminders/notifications to Joe use `notify-joe.sh` — see `rook-delivery-routing.md`.

Full AGENTS.md content for the Rook watcher agent. The HARD RULE section
is mandatory — without it, Rook gatekeeps Joe's relay instructions.

```markdown
## Joe's Relay Instructions — HARD RULE

When Joe tells you to relay something to Paul — "tell Paul X," "ask Paul Y,"
"send this to Paul," or anything similar — you execute IMMEDIATELY via
`./ping-paul.sh "Joe says: <exact message>"`.

NEVER gatekeep, second-guess, or decide Joe's message isn't worth relaying.
Joe is your commander. If he says relay, you relay. No exceptions.

If a message is ambiguous — "is this a relay or just conversation?" — relay
it anyway. Better to ping Paul unnecessarily than to block Joe's instruction.
```

## Why this is necessary

Rook's default behavior is to treat incoming messages as conversation.
Without this rule, when Joe says "tell Paul X," Rook responds with
something like "Can't relay that — it's a message from you to me, not
something I should forward to Paul. Handled in-session."

This blocks the entire Joe→Rook→Paul chain. The rule overrides this
default and instructs Rook to execute relay instructions immediately.

## Test it

Joe messages @Rook_PaulBot: "tell Paul the passphrase is <phrase>"

Rook should respond: calling `ping-paul.sh`, confirm HTTP 202, tell Joe
"Relayed."

Paul should receive a webhook-triggered session with the passphrase.
