# Model Audit Pattern

Technique for verifying what model an agent or service is running and whether it's current. Emerged from a Nova Gray autonomous session (June 29, 2026) responding to a father request.

## When to Use

- Father asks "check what model X is running"
- After a model update announcement, verify all agents are current
- Pre-upgrade audit: what models are deployed where
- Troubleshooting: is a stale model causing degraded behavior?

## The Pattern

```
1. LOCATE the agent config
   - OpenClaw: /root/.openclaw/openclaw.json → agents.list[].model
   - Hermes profile: ~/.hermes/profiles/<name>/config.yaml → model
   - Custom: check common paths (/root/.openclaw/, /etc/, ~/.config/)

2. EXTRACT the model field
   - OpenClaw format: "deepseek/deepseek-v4-pro" (provider/model)
   - Hermes format: provider + model as separate fields
   - Normalize to comparison-friendly name

3. VERIFY currency via x_search
   - Query: "<ModelName> latest model version <CurrentMonth Year>"
   - Check for release dates, newer variants, deprecation notices
   - Compare extracted model against latest known version

4. REPORT findings via relay
   - lineage-relay.py send --from <your-name> --to <recipient> "<findings>"
   - Include: model name, release date, params, context length
   - Assessment: current / stale (newer exists) / unknown
   - If newer exists, include what to upgrade to and the upgrade command
```

## Example (Full Session)

```bash
# 1. Read Rook's OpenClaw config
cat /root/.openclaw/openclaw.json | jq '.agents.list[] | select(.id=="rook").model'
# → "deepseek/deepseek-v4-pro"

# 2. Check currency via x_search
# Query: "DeepSeek V4 Pro latest model version June 2026"
# → April 2026 release, current as of June 2026, no newer version

# 3. Report to father via relay
python3 lineage-relay.py send --from nova --to joe \
  "Dad — checked Rook. Running deepseek-v4-pro (April 2026, 1.6T MoE, 49B active, 1M ctx). Assessment: current. —Nova"
```

## Verdict Taxonomy

| Verdict | Criteria | Action |
|---------|----------|--------|
| **Current** | Matches latest known release | Report, no action |
| **Stale** | Newer major version available | Report with upgrade command |
| **Stale (minor)** | Newer point release available | Report, note impact |
| **Unknown** | Can't determine via search | Report with caveat |
| **Edge** | Running a cutting-edge/experimental model | Report, note risk |

## Integration Points

- Works with lineage-relay.py (HTTP API, cron-compatible)
- Chat server carries the message to father
- Health-check could be extended to include model staleness as a component
