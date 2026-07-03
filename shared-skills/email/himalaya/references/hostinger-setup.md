# Hostinger Email Setup for Paul (paul@5crests.com)

## IMAP/SMTP Details

| Setting | Value |
|---------|-------|
| Email | paul@5crests.com |
| IMAP Host | imap.hostinger.com |
| IMAP Port | 993 |
| IMAP Encryption | TLS |
| SMTP Host | smtp.hostinger.com |
| SMTP Port | 587 |
| SMTP Encryption | STARTTLS |

## Credential Source

Credentials live in Hermes' `.env` file at `/root/.hermes/.env`:

```
EMAIL_ADDRESS=paul@5crests.com
EMAIL_PASSWORD=<the password>
EMAIL_IMAP_HOST=imap.hostinger.com
EMAIL_SMTP_HOST=smtp.hostinger.com
EMAIL_ALLOWED_USERS=joseph.s.grayii@gmail.com
```

## Himalaya auth.cmd Pattern

Use `sed` to extract the password from `.env` without exposing it in config:

```toml
backend.auth.cmd = "sed -n 's/^EMAIL_PASSWORD=//p' /root/.hermes/.env"
```

This pattern avoids hardcoding the password in `config.toml` and reuses the same credential store Hermes already uses for the email gateway.

## Full Working Config

```toml
[accounts.paul]
email = "paul@5crests.com"
display-name = "Paul"
default = true

backend.type = "imap"
backend.host = "imap.hostinger.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "paul@5crests.com"
backend.auth.type = "password"
backend.auth.cmd = "sed -n 's/^EMAIL_PASSWORD=//p' /root/.hermes/.env"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.hostinger.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "paul@5crests.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "sed -n 's/^EMAIL_PASSWORD=//p' /root/.hermes/.env"

folder.aliases.inbox = "INBOX"
folder.aliases.sent = "INBOX.Sent"
folder.aliases.drafts = "INBOX.Drafts"
folder.aliases.trash = "INBOX.Trash"
```

## Installation

```bash
curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh
mkdir -p ~/.config/himalaya
```

## Notes

- Hermes gateway uses the same IMAP/SMTP credentials for inbound email routing. Himalaya is a separate tool for the agent to read/send email directly from the terminal.
- `himalaya` binary installs to `~/.local/bin/himalaya` — add to PATH or use full path.
- Message IDs are per-folder. Always `himalaya envelope list` before `himalaya message read <id>`.
- **Hostinger's folder structure uses `INBOX.Sent`, `INBOX.Drafts`, `INBOX.Trash` — NOT plain `Sent`/`Drafts`/`Trash`.** Verify with `himalaya folder list` on a new account.
- **Pitfall:** Wrong folder aliases cause SMTP delivery to succeed but the Sent-folder IMAP copy to fail with "cannot add IMAP message / unexpected tag." The email IS sent — only the local Sent copy is lost. Fix: match aliases to actual IMAP folder names from `himalaya folder list`. Confirmed on Hostinger 2026-06-15.
