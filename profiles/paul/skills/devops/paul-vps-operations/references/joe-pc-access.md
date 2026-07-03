# Joe's PC Access — WSL Reverse SSH Tunnel

## Architecture

Joe's primary dev machine is a Windows PC running WSL2 (hostname: `NAUTILUS-3`).
It connects to the VPS via Tailscale (IP: `100.122.48.109`).
To reach Joe's machine from the VPS, use a reverse SSH tunnel through WSL —
no Windows services, no open ports, no firewall changes.

```
Joe's PC                              VPS (Paul)
┌────────────────────────┐            ┌──────────────────┐
│ WSL (NAUTILUS-3)       │            │                  │
│  sshd :22              │◄──tunnel───│  localhost:2222   │
│  /mnt/c/... (C: drive) │            │  -> SSH in        │
└────────────────────────┘            │  -> SSHFS mount   │
                                      └──────────────────┘
```

## Establishing the tunnel

From a WSL terminal on Joe's PC:

```bash
ssh -R 2222:localhost:22 paul-dash
```

- `paul-dash` is Joe's SSH alias for the VPS (already in `~/.ssh/config`)
- `-R 2222:localhost:22` creates a reverse tunnel: VPS port 2222 → WSL port 22
- No ports exposed to the internet — Tailscale is already private, and the tunnel listens only on VPS localhost

Keep this session alive. For persistence across drops, use `autossh` or a systemd timer.

## Prerequisites on Joe's WSL

SSH server must be installed and running inside the WSL distro:

```bash
sudo apt install openssh-server -y
sudo service ssh start
```

WSL username: `thegreybeard` (NOT `joe`)

## VPS-side key auth

Generate a dedicated keypair on the VPS (one-time):

```bash
ssh-keygen -t ed25519 -f /root/.ssh/joe-wsl -N "" -C "paul-vps->joe-wsl"
```

Copy the public key to Joe's WSL `authorized_keys` — Joe runs this from WSL:

```bash
mkdir -p /home/thegreybeard/.ssh
echo "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIBA3CX/wrNRvsaUO2fDQZlGc87UxvBDY1glC5Kqzd0kD paul-vps->joe-wsl" >> /home/thegreybeard/.ssh/authorized_keys
chown -R thegreybeard:thegreybeard /home/thegreybeard/.ssh
chmod 700 /home/thegreybeard/.ssh
chmod 600 /home/thegreybeard/.ssh/authorized_keys
```

Then SSH in without password:

```bash
ssh -i /root/.ssh/joe-wsl -o StrictHostKeyChecking=no -p 2222 thegreybeard@localhost
```

## Accessing Joe's C: drive

WSL mounts Windows drives at `/mnt/<letter>/`:

```bash
ssh -p 2222 thegreybeard@localhost "ls /mnt/c/Users/TheGreyBeard/"
```

For full filesystem access via SSHFS (lets Paul's native tools work on Joe's files):

```bash
sshfs -p 2222 thegreybeard@localhost:/mnt/c/Users/TheGreyBeard/projects /mnt/joe-pc
```

## Escaping a forgotten WSL sudo password

From a **Windows** terminal (PowerShell or CMD, NOT WSL):

```cmd
wsl -u root
```

Drops into WSL as root with no password prompt. Then:

```bash
passwd thegreybeard    # reset the forgotten password
```

## Pitfalls

- **Tunnel drops silently.** If the WSL terminal closes or the SSH session times out, port 2222 disappears from the VPS. Check with `ss -tlnp | grep 2222`. For persistence, use `autossh`.
- **Wrong username.** Joe's WSL username is `thegreybeard`, not `joe`. SSH with the wrong username will fail immediately.
- **No SSH server in WSL.** Fresh WSL installs don't include `openssh-server`. Install it before attempting the tunnel.
- **Do NOT install Windows OpenSSH Server.** Joe prefers WSL-native solutions over Windows services. The `Add-WindowsCapability` route adds a listening service to the Windows host, which is unnecessary since WSL already has SSH.
- **`Connection reset by peer` during SSH handshake** means the tunnel reached port 22 but no SSH server answered — install and start `sshd` inside WSL.
- **SSHFS over the tunnel** is slower than local — mount only the project directory, not the entire C: drive.
