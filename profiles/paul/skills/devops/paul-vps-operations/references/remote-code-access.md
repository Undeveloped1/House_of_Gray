# Remote Code Access: VPS → Joe's Windows PC

Joe's desktop runs Windows with WSL2, connected to the VPS via Tailscale.
This document covers the architecture for Paul to edit code on Joe's machine
remotely — the middle ground between full `computer-use` (GUI automation)
and pure shell-over-SSH.

## Network Topology

```
Joe's PC (Windows + WSL2)          VPS (2.25.163.205)
┌─────────────────────────┐        ┌──────────────────┐
│ Tailscale: 100.122.48.109│◄──────►│ Tailscale: 100.94.19.72│
│                         │        │                  │
│ WSL2 VM (separate NIC)  │        │ Paul (Hermes)    │
│ No direct Tailscale IP  │        │                  │
└─────────────────────────┘        └──────────────────┘
```

Joe connects to the VPS via Hermes Desktop → remote gateway → Tailscale → SSH.

## WSL2 Networking Gotcha

WSL2 runs in a lightweight Hyper-V VM with its own virtual Ethernet adapter.
The Tailscale IP (`100.122.48.109`) belongs to the **Windows host**, not WSL.
Inbound SSH to that IP hits Windows — if OpenSSH Server isn't running on the
Windows side, the connection is refused. WSL's SSH server is invisible from
outside the VM.

**Fix:** Install OpenSSH Server on Windows (not just WSL):
```powershell
# Admin PowerShell:
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
```

## Computer-Use Architecture Gap

`cua-driver` v0.7.0 was installed on the VPS (`hermes computer-use install`),
but the VPS is headless — no desktop to drive. For `computer_use` to work:

1. cua-driver must run on **Joe's PC** (where the desktop is)
2. Its MCP mode is **stdio-only** — no built-in HTTP transport
3. Hermes on the VPS needs an HTTP MCP endpoint to connect remotely

Bridging options (not yet implemented):
- Simple Python proxy wrapping stdio → HTTP
- SSH tunnel + `socat` bridging the MCP socket
- Or run Hermes locally on Joe's machine (simplest path, no networking needed)

## SSH Access for Code Editing (Current State)

Joe's PC is reachable at Tailscale IP `100.122.48.109`. SSH connection from
VPS times out — OpenSSH Server not yet enabled on Windows side.

Once SSH is up, plan:
```bash
# Direct SSH from VPS:
ssh joe@100.122.48.109

# Or mount specific project dirs via SSHFS:
sshfs joe@100.122.48.109:/Users/TheGreyBeard/projects/hermes-desktop /mnt/joe-pc
```

Then all native tools (`read_file`, `write_file`, `patch`, `search_files`)
work on Joe's files as if local.

## Security: Tailscale-Only Binding

Exposure is limited to the Tailscale private network (100.x.y.z addresses
are not publicly routable). To lock SSH to Tailscale only:

In `C:\ProgramData\ssh\sshd_config`:
```
ListenAddress 100.122.48.109
```

This prevents SSH from listening on LAN or public interfaces. Nothing
exposed to WAN.

## Risk Tradeoffs

**SSHFS mount (recommended for code editing):**
- + Clean: all Hermes tools work natively
- + Mount a single project directory to limit blast radius
- - Network dependency: Tailscale drop = mount glitches
- - CRLF vs LF line endings can cause diffs (fixable with git config)

**Git push/pull (zero filesystem exposure):**
- + No persistent mount, no network dependency mid-edit
- - Extra sync step per edit cycle
- - Requires a private remote or VPS-hosted bare repo

**Full computer-use (future):**
- + GUI automation: Amazon Seller Central, desktop apps, browsers
- - cua-driver needs installing on Joe's machine
- - Needs stdio→HTTP MCP bridge for remote
- - Password/auth prompts are hard-blocked (must be Joe-typed)
