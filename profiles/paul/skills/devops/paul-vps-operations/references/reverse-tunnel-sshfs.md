# Reverse SSH Tunnel + SSHFS (VPS → Joe's PC)

How Paul edits code on Joe's Windows machine from the VPS — securely, with no new services or open ports.

## Architecture

```
Joe's Windows PC (WSL)                 VPS (Paul)
┌────────────────────────┐            ┌──────────────────┐
│  WSL: sshd on :22      │            │                  │
│  /mnt/c/Users/         │◄─SSHFS────►│  /mnt/joe-pc/    │
│      TheGreyBeard/     │  over      │  (native tools)  │
│                        │  tunnel    │                  │
│  ssh -R 2222:loc:22 ──────────────►│  localhost:2222   │
│  (Joe initiates)       │            │  (Paul connects)  │
└────────────────────────┘            └──────────────────┘
```

The reverse tunnel piggybacks on Joe's outbound SSH connection. No ports open on Joe's machine. No Windows services. No firewall rules. The only listening port (2222) is on the VPS's localhost.

## Prerequisites

- Joe's WSL has `sshd` installed and running
- SSHFS installed on VPS: `apt install sshfs`
- Joe can SSH to VPS (already works via `ssh paul-dash`)
- Tailscale provides the network between them

## Step 1: Verify WSL SSH server

Joe runs in a **local** WSL terminal (not the one SSH'd into the VPS):

```bash
which sshd && sudo service ssh status
```

If not installed: `sudo apt install openssh-server -y && sudo service ssh start`

## Step 2: Joe opens the reverse tunnel

In a **new** WSL terminal (keep the main SSH session alive):

```bash
ssh -R 2222:localhost:22 paul-dash
```

This tells the VPS: "create port 2222 on your localhost, and route anything that connects to it back through me to my WSL's port 22."

Leave this terminal open. It carries the tunnel.

## Step 3: Paul verifies the tunnel

```bash
ss -tlnp | grep 2222
# Should show: LISTEN 127.0.0.1:2222
```

Then test SSH through it:

```bash
ssh -o StrictHostKeyChecking=no -p 2222 joe@localhost "whoami && hostname"
```

## Step 4: Paul mounts Joe's filesystem

```bash
mkdir -p /mnt/joe-pc
sshfs -p 2222 joe@localhost:/mnt/c/Users/TheGreyBeard/projects /mnt/joe-pc
```

Now Paul's native tools work on Joe's files:

```bash
search_files pattern="hermes" target="files" path=/mnt/joe-pc
read_file /mnt/joe-pc/hermes-desktop/src/main.ts
patch /mnt/joe-pc/hermes-desktop/src/renderer.ts ...
```

## Accessing the full C drive

WSL mounts Windows drives under `/mnt/`. To mount the entire C drive:

```bash
sshfs -p 2222 joe@localhost:/mnt/c /mnt/joe-pc
```

But prefer mounting only the project directory — less blast radius, faster.

## Teardown

```bash
fusermount -u /mnt/joe-pc    # unmount SSHFS
# Joe closes the reverse-tunnel SSH session
```

## Persistence (surviving disconnects)

The tunnel drops when Joe's SSH session ends. For long-running access:

### autossh (recommended)

Joe installs `autossh` in WSL, then:

```bash
autossh -M 0 -R 2222:localhost:22 paul-dash
```

`-M 0` disables the monitoring port (uses SSH's built-in keepalive instead). autossh restarts the tunnel if it dies.

### systemd timer

A systemd user timer in WSL that runs the reverse tunnel on a schedule. Overkill for interactive sessions — use autossh.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| `Connection refused` on port 2222 | Tunnel dropped. Joe's reverse-SSH session died. | Joe reconnects: `ssh -R 2222:localhost:22 paul-dash` |
| `Connection reset by peer` during handshake | Something listening on WSL:22 but not SSH | Check `sudo service ssh status` in WSL |
| `kex_exchange_identification: read: Connection reset` | SSH server in WSL is running but misconfigured | `sudo sshd -t` to check config; restart with `sudo service ssh restart` |
| SSHFS mount hangs or is slow | Tailscale latency or packet loss | Mount a smaller directory; use `-o reconnect` flag |
| `read: Connection reset by peer` on SSHFS after idle | SSHFS connection timed out | Remount; add `-o ServerAliveInterval=15` to the tunnel's SSH config |
| WSL2 IP changes after reboot | WSL2 gets a new IP each restart | Doesn't matter — the tunnel uses `localhost` in WSL, not an IP |

## Why not Windows OpenSSH Server?

Joe is right to be wary. Installing `sshd` on Windows means:

- A new service running with SYSTEM privileges
- A new listening port on the Windows network stack
- Windows Firewall rules to manage
- Potential exposure if misconfigured

The reverse tunnel avoids all of this. WSL's `sshd` is already there (Joe uses SSH daily). The tunnel rides an outbound connection Joe initiated. Nothing new to secure.

## Why not direct SSH to WSL?

WSL2 runs in a lightweight VM with its own virtual network adapter. Joe's Tailscale IP (`100.122.48.109`) belongs to the Windows host, not the WSL VM. So `ssh joe@100.122.48.109` hits Windows, not WSL. The reverse tunnel is the only clean path in.
