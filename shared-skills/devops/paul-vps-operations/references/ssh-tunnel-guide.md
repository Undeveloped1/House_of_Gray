# SSH Tunnel Guide (Paul VPS Access for Joe)

Pattern for securely accessing VPS-hosted services through encrypted SSH tunnels. Every service runs on localhost — no ports exposed to the internet. The SSH pipe is the only door.

## Joe's VPS

- **Host:** 2.25.163.205 (public) / 100.94.19.72 (Tailscale)
- **SSH alias:** `paul` in WSL/Mac `~/.ssh/config`
- **Key:** `~/.ssh/hostinger_key` (MacBook) / `~/.ssh/id_ed25519_tailscale` (WSL)
- **Services all bound to 127.0.0.1 (localhost only)**

## Active Services & Ports

| Service | Port | Access |
|---------|------|--------|
| Hermes Dashboard | 9119 | `http://localhost:9119` after tunnel. No token/auth required when bound to 127.0.0.1 — the SSH tunnel IS the authentication layer. |
| Chrome Remote Debug | 9222 | `http://localhost:9222` for headless browser auth |
| SSH | 22 | Direct (only open port) |

## SSH Config (Joe's Setup)

Joe prefers everything consolidated into the `Host paul` entry — no separate aliases for tunnels:

```
Host paul
    HostName 100.94.19.72
    User root
    IdentityFile ~/.ssh/hostinger_key
    LocalForward 9119 localhost:9119
    LocalForward 9222 localhost:9222
```

All services on one line: `ssh paul` — tunnel auto-negotiated, dashboard available at `http://localhost:9119`.

If you need the tunnel without the terminal session: `ssh -fN paul` (backgrounds it).

## Adding a New Service

When a new service needs tunnel access:

1. Add `LocalForward <local_port> localhost:<vps_port>` to the `Host paul` entry
2. Service must be running on the VPS bound to `127.0.0.1`
3. Verify with `ss -tlnp | grep <port>` on VPS

Joe adds the line himself — give him the exact `LocalForward` line to paste.

## WSL Terminal Pitfalls

Joe's WSL (`thegreybeard@NAUTILUS-3`) mangles multi-line pastes:
- **Heredocs (`<< 'EOF'`) break** — line ending issues, user gets stuck at `>` prompt
- **`printf` with `\n` escapes also breaks** — produces fragmented lines
- **Solution:** Line-by-line `echo` commands, one per line, no multi-line constructs

Bad:
```bash
cat >> ~/.ssh/config << 'EOF'
Host paul-dash
    ...
EOF
```

Good:
```bash
echo 'Host paul' >> ~/.ssh/config
echo '    HostName 100.94.19.72' >> ~/.ssh/config
echo '    User root' >> ~/.ssh/config
```

Never give Joe heredocs, `printf` with `\n`, or any multi-line shell construct. Single `echo` commands or `sed` one-liners only.

### `sed` Append (Adding One Line to Existing Entry)

When adding a single line to an existing SSH config block, `sed` "a`" (append after match) is cleaner than reconstructing the entire file:

```bash
# Linux/WSL:
sed -i '/IdentityFile ~\/.ssh\/hostinger_key/a\    LocalForward 9119 localhost:9119' ~/.ssh/config
# macOS (BSD sed requires backup extension):
sed -i '' '/IdentityFile ~\/.ssh\/hostinger_key/a\
    LocalForward 9119 localhost:9119' ~/.ssh/config
```

This appends the LocalForward line right after the IdentityFile line inside the `Host paul` block. No heredoc, no `printf` — safe for WSL.

**macOS sed pitfall:** macOS uses BSD sed, which requires `sed -i ''` (empty backup extension) instead of Linux `sed -i`. Getting this wrong produces `invalid command code` errors. On Mac, prefer the `echo` append pattern instead — it's portable and harder to break.

## Joe's Communication Preference for Technical Instructions

Joe: "treat me as though I was a small child when it comes to these technical aspects, I have the brainpower to understand, but I'm simple when it comes to code execution, and backend management — this is greek."

Practical rules:
- One command at a time
- No bash scripting, no heredocs, no pipelines with multiple steps
- Verify after each step before giving the next
- Explain what the command does in plain English, not what the syntax means
- If a command produces no output, warn him that's expected
- Never give a multi-line paste block — it will break in WSL
