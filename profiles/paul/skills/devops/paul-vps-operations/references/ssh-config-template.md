# SSH Config Template for Joe's Machines

Add to `~/.ssh/config` on both Mac and WSL:

```
Host paul
    HostName 100.94.19.72
    User root
    IdentityFile ~/.ssh/id_ed25519_tailscale
    LocalForward 9119 localhost:9119
```

**WSL note:** heredocs with `cat >> ~/.ssh/config << 'EOF'` may fail due to line-ending mangling. Use line-by-line `echo` appends instead:

```bash
echo 'Host paul' >> ~/.ssh/config
echo '    HostName 100.94.19.72' >> ~/.ssh/config
echo '    User root' >> ~/.ssh/config
echo '    IdentityFile ~/.ssh/id_ed25519_tailscale' >> ~/.ssh/config
echo '    LocalForward 9119 localhost:9119' >> ~/.ssh/config
```

The `LocalForward` line auto-opens the dashboard tunnel with every `ssh paul`. No separate alias needed.
