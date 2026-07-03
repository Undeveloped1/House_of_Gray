# Perimeter Sweep Response Protocol

When a security sentry agent (Shiva) files a perimeter sweep report, the response
pattern is:

## 1. Validate findings

Acknowledge correct catches. If a finding is wrong or incomplete, say so directly
with evidence. A sentry needs calibration — false positives erode trust, missed
positives leave gaps.

## 2. Answer questions directly

Sentry reports typically include questions about unknown services. Answer each one
concretely. Example from Shiva's first sweep:

| Question | Answer |
|----------|--------|
| "What does Hermes:8644 serve?" | Rook's webhook relay, HMAC-SHA256, Tailscale-only |
| "Is ModemManager needed?" | No modem hardware — dead weight |
| "CUPS — can I kill it?" | Yes, nobody prints from a headless VPS |

## 3. Add to her watchlist

The sentry is doing continuous perimeter walks. Flag new items she should monitor:

- Agent workspaces (e.g., `/root/.openclaw/` — Rook's files)
- Growing data stores (e.g., `state.db` — conversation history, data leak risk)
- Other profiles (e.g., Abby's memory/pruning health)

## 4. Flag what she missed

A good sentry wants to improve. Point out gaps, but as a peer, not a critic.
Example: Shiva missed `atd` (deferred execution daemon, legacy attack surface).

## 5. Escalate destructive actions to Joe

The sentry's directive is "track AND fix, but not cowboy." When a finding requires
destructive action (killing a service, removing a package, changing config), the
sentry flags it for Joe's approval. Paul can validate the recommendation — but
Joe owns the kill order.

## Dead Service Cleanup Protocol

When a perimeter sweep finds a running service with no workload:

```bash
# 1. Check if anything is using it
atq          # for atd — any pending jobs?
lpstat -t    # for CUPS — any print queues?
mmcli -L     # for ModemManager — any modems?

# 2. If empty: kill + disable
systemctl stop <service>
systemctl disable <service>

# 3. Consider package removal if truly unnecessary
apt remove --purge <package>  # Joe's call
```

## Common Dead Services on Headless VPS

| Service | Purpose | Needed on VPS? |
|---------|---------|----------------|
| `cups` | Printing | No — remove |
| `atd` | One-shot deferred execution | No — Hermes cron is used |
| `ModemManager` | Mobile broadband/dial-up | No — no modem hardware |
| `avahi-daemon` | mDNS/Zeroconf service discovery | Rarely — disable unless needed |

## Pitfall: Config Comments That Lie

Services sometimes ship with config comments that contradict the actual behavior.
Shiva's first sweep caught CUPS where line 20 says "Only listen for connections
from the local machine" but line 3 had `Port 631` with no bind address = wildcard
0.0.0.0. **Trust the config directive, not the comment above it.**
