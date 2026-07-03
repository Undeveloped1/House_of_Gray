# WSL Reverse SSH Tunnel — Joe's Windows Machine Access

## When to use

Joe needs Paul to edit files on his Windows machine, but:
- No Windows services should be installed (no OpenSSH Server on Windows)
- WSL is already running and SSH-capable
- Tailscale connects both machines
- Joe prefers using existing infrastructure over installing new things

## Architecture

```
Joe's Windows PC ← WSL (NAUTILUS-3) → SSH → Paul's VPS
                                       ↑
                                  Reverse tunnel
                                  -R 2222:localhost:22
```

Joe's WSL already has SSH outbound to the VPS. Adding `-R` creates a reverse tunnel: port 2222 on the VPS forwards to port 22 inside WSL. Paul SSH's into `localhost:2222` on the VPS and lands in Joe's WSL, with full access to the Windows filesystem via `/mnt/c/`.

## One-time setup (on Joe's WSL)

```bash
# Install SSH server inside WSL (if not already present)
sudo apt update && sudo apt install openssh-server -y
sudo service ssh start

# Reset forgotten WSL password (from Windows, as root)
wsl -u root
passwd thegreybeard
```

## Key-based auth (from Paul's VPS, one-time)

```bash
# Generate a dedicated key pair on the VPS
ssh-keygen -t ed25519 -f /root/.ssh/joe-wsl -N "" -C "paul-vps->joe-wsl"

# Joe adds the public key to WSL (as root in WSL):
mkdir -p /home/thegreybeard/.ssh
echo "ssh-ed25519 AAAAC3..." >> /home/thegreybeard/.ssh/authorized_keys
chown -R thegreybeard:thegreybeard /home/thegreybeard/.ssh
chmod 700 /home/thegreybeard/.ssh
chmod 600 /home/thegreybeard/.ssh/authorized_keys
```

## Establishing the tunnel (Joe runs from WSL)

```bash
ssh -R 2222:localhost:22 paul-dash
```

This reconnects to the VPS (same alias Joe normally uses) with the reverse tunnel. Paul then accesses Joe's WSL via:

```bash
ssh -i /root/.ssh/joe-wsl -p 2222 thegreybeard@localhost "whoami && hostname"
```

## Accessing Windows files through WSL

Once connected, Windows drives are at `/mnt/c/`. The Hermes Desktop source lives at:
```
/mnt/c/Users/TheGreyBeard/AppData/Local/hermes/hermes-agent/apps/desktop/
```

## Persistent tunnel (autossh)

The tunnel drops when Joe's SSH session disconnects. For persistence:

```bash
autossh -M 0 -R 2222:localhost:22 paul-dash
```

Or as a WSL systemd service (WSL2 supports systemd).

## Remote multi-file patching via SSH+Python

When coordinated multi-file edits are needed on Joe's remote machine, use SSH + Python inline scripts rather than many individual `sed` commands:

```bash
ssh -i /root/.ssh/joe-wsl -p 2222 thegreybeard@localhost "python3 -c \"
path = '/mnt/c/Users/.../file.ts'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('old_string', 'new_string')
content = content.replace('pattern2', 'replacement2')

with open(path, 'w') as f:
    f.write(content)
print('Done')
\""
```

This is faster and less error-prone than multiple SSH+sed invocations.

## Pitfalls

- **The tunnel drops silently.** The VPS port 2222 disappears. Check with `ss -tlnp | grep 2222`. Joe needs to reconnect with `ssh -R`.
- **WSL's `/mnt/c/` is slow for git operations.** `git status` can time out on large repos. Be patient or work file-by-file.
- **`passwd` requires knowing the WSL username.** Use `wsl -u root` from Windows to bypass, then `ls /home/` to find the username.
- **Don't install Windows OpenSSH Server.** Joe prefers keeping services minimal. The reverse tunnel through existing WSL SSH is cleaner and more secure.
- **The tunnel is only as secure as the SSH connection.** No ports are exposed to the internet — the VPS's `localhost:2222` is only reachable from within the VPS.
