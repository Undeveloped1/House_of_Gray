---
name: public-game-access
description: Temporarily open port 4000 to the public internet for game testing — auto-closes after 1 hour.
---

# Public Game Access

Open port 4000 for game testing with automatic 1-hour timeout. Default state is Tailscale-only at `100.94.19.72:4000`. This skill temporarily punches a hole for external testers.

## Open access (1-hour auto-close)

```bash
iptables -I DOCKER-USER 1 -p tcp --dport 4000 -j ACCEPT && \
echo "iptables -D DOCKER-USER -p tcp --dport 4000 -j ACCEPT" | at now + 1 hour && \
echo "Port 4000 open — closes at $(date -d '+1 hour' '+%H:%M')"
```

Share with tester: `http://2.25.163.205:4000`

## Extend access

```bash
# Remove pending auto-close job
atq | awk '{print $1}' | head -1 | xargs atrm 2>/dev/null
# Schedule new close
echo "iptables -D DOCKER-USER -p tcp --dport 4000 -j ACCEPT" | at now + 2 hour
```

## Close immediately

```bash
iptables -D DOCKER-USER -p tcp --dport 4000 -j ACCEPT && \
atq | awk '{print $1}' | head -1 | xargs atrm 2>/dev/null && \
echo "Port 4000 closed"
```

## Verify

```bash
# Should show rule when open, nothing when closed
iptables -L DOCKER-USER -n | grep 4000
# Check pending close job
atq
```

## Pitfalls

- Only works if `atd` is running (`systemctl start atd` if needed)
- If Tailscale IP changes, the app bind needs updating separately in docker-compose.vps.yml
- `DOCKER-USER` chain sits above Docker's own rules and can't be bypassed — this is the correct chain
- Insert at position 1 so it's evaluated first
