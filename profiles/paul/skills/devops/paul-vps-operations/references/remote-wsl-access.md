# Remote WSL Access via Reverse SSH Tunnel

How Paul (VPS) reaches Joe's Windows PC through WSL — no Windows services, no open ports, no firewall changes.

## Architecture

```
Joe's PC (Windows + WSL)              VPS (Paul)
┌─────────────────────────┐           ┌──────────────────┐
│ WSL: ssh -R 2222:l:22   │──Tailscale──► SSH server      │
│      paul-dash          │           │                  │
│                         │           │ Paul SSHs back:   │
│ sshd listening :22      │◄──tunnel─── ssh -p 2222       │
│ /mnt/c/ → C:\           │           │ thegreybeard@     │
└─────────────────────────┘           │ localhost         │
                                      └──────────────────┘
```

## Prerequisites

- Tailscale on both machines (already set up)
- WSL with OpenSSH server installed
- SSH key from VPS authorized in WSL

## One-Time Setup (WSL side)

### 1. Install OpenSSH Server in WSL

```bash
# If sudo password forgotten: wsl -u root from Windows PowerShell
sudo apt update && sudo apt install openssh-server -y
sudo service ssh start
```

### 2. Authorize VPS Key

On VPS:
```bash
ssh-keygen -t ed25519 -f /root/.ssh/joe-wsl -N "" -C "paul-vps->joe-wsl"
cat /root/.ssh/joe-wsl.pub
```

In WSL (as root if sudo password forgotten):
```bash
mkdir -p /home/thegreybeard/.ssh
echo "<public key>" >> /home/thegreybeard/.ssh/authorized_keys
chown -R thegreybeard:thegreybeard /home/thegreybeard/.ssh
chmod 700 /home/thegreybeard/.ssh
chmod 600 /home/thegreybeard/.ssh/authorized_keys
```

## Opening the Tunnel (Joe runs each session)

From a WSL terminal:
```bash
ssh -R 2222:localhost:22 paul-dash
```

Keep this terminal open. This is NOT the same terminal as the one talking to Paul — it's a second WSL window.

## Paul's Side: Connecting Through the Tunnel

```bash
ssh -i /root/.ssh/joe-wsl -p 2222 thegreybeard@localhost
```

Verify:
```bash
ssh -i /root/.ssh/joe-wsl -p 2222 thegreybeard@localhost "whoami && hostname"
# Expected: thegreybeard \n NAUTILUS-3
```

## Accessing Windows Filesystem from WSL

WSL auto-mounts Windows drives:
- `C:\` → `/mnt/c/`
- Joe's home: `/mnt/c/Users/TheGreyBeard/`

Hermes Desktop source on Joe's machine:
```
/mnt/c/Users/TheGreyBeard/AppData/Local/hermes/hermes-agent/apps/desktop/
```

## Persistence (autossh)

Tunnel drops when the SSH session disconnects. For persistent access:
```bash
autossh -M 0 -R 2222:localhost:22 paul-dash
```

Or systemd timer in WSL to auto-reconnect.

## Security Properties

- No ports open on Joe's machine
- No Windows services running
- No firewall rules
- Tunnel rides existing authenticated Tailscale connection
- VPS localhost:2222 is the only listening port — not reachable from outside the VPS
- SSH key auth only — no password exchange

## Recovery: Forgot WSL sudo Password

From Windows PowerShell or CMD:
```cmd
wsl -u root
```
Drops into WSL as root — no password needed. Then:
```bash
passwd thegreybeard    # reset user password
service ssh start      # start SSH if needed
```

## Pitfalls

- **Tunnel drops silently.** Port 2222 on VPS disappears. Check with `ss -tlnp | grep 2222`. Joe must reconnect.
- **SSH handshake reset on first attempt:** usually means `sshd` isn't running in WSL. Install with `apt install openssh-server`.
- **SSH asks for password instead of using key:** `authorized_keys` permissions too open or wrong ownership. `chmod 600 ~/.ssh/authorized_keys`.
- **Windows SSH Server (sshd on Windows, not WSL) was suggested but Joe vetoed it** — "skeeving me out." Stick to WSL SSH server only.
- **`ssh -R` requires the tunnel session to stay alive.** If Joe closes that terminal, the tunnel dies. Use autossh or a second terminal kept open.
