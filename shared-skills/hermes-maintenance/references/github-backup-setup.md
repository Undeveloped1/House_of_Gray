## GitHub Backup Repo Setup for Paul's Vault

## Purpose

Paul's vault at `~/.hermes/docs/Paul/` has no version control by default. A dedicated
GitHub repo provides off-VPS backup, change history, and disaster recovery.

**Actual repo (2026-06-03):** `Undeveloped1/Paul_VPS` — private, SSH deploy key auth.

This repo is Paul's vault ONLY — not the tcg-engine game design repo. Cursor owns
that one. This repo is purely for Paul's brain backup.

## One-Time Setup

### 1. Install gh CLI

```bash
apt-get install -y gh
```

If dpkg is stuck: `dpkg --configure -a` first.

### 2. Joe Creates the Repo + PAT

Joe does this on GitHub.com:

1. Create a new **private** repo (e.g., `paul-vps`, `paul-vault-v2`)
2. Go to Settings → Developer settings → Fine-grained tokens
3. Generate new token:
   - **Repository access:** Only select repositories → pick the new repo
   - **Permissions:** Contents → Read and write
   - Copy the token

### 3. Authenticate gh CLI

The VPS has no browser. Use token-based auth:

```bash
echo "github_pat_..." | gh auth login --with-token
```

Verify:
```bash
gh auth status
```

### 4. Initialize and Push the Vault

```bash
cd /root/.hermes/docs/Paul

# Remove old git history if it's the wrong repo
rm -rf .git

# Init fresh
git init
git config user.name "Paul (VPS)"
git config user.email "paul@5crests.com"

# Add everything except .obsidian (Joe has his own Obsidian config)
echo ".obsidian/" > .gitignore
git add -A
git commit -m "Initial VPS vault backup — $(date +%Y-%m-%d)"

# Connect and push
git remote add origin https://github.com/Undeveloped1/<repo-name>.git
git branch -M main
git push -u origin main
```

### 5. Switch to SSH Deploy Key (REQUIRED — PATs Fail for Git Push)

**Critical pitfall:** Fine-grained PATs authenticate to the GitHub API but FAIL for HTTPS git push — returning 403 even with admin permissions. Deploy keys are the reliable solution.

```bash
ssh-keygen -t ed25519 -f ~/.ssh/paul_vps -N "" -C "deploy-key"
gh api -X POST /repos/Undeveloped1/<repo-name>/keys -f title="VPS-deploy" -f key="$(cat ~/.ssh/paul_vps.pub)" -f read_only=false
git remote set-url origin git@github.com:Undeveloped1/<repo-name>.git
git config core.sshCommand "ssh -i ~/.ssh/paul_vps -o StrictHostKeyChecking=accept-new"
git push -u origin master

## Recurring Backup

Push on session close or after significant work. A cron job can handle daily pushes:

```bash
cd /root/.hermes/docs/Paul && git add -A && git commit -m "Auto-backup $(date +%Y-%m-%d)" && git push
```

## Token Security WARNING

When Joe pastes a PAT into chat, it enters the Hermes session transcript. Session
transcripts are stored in `~/.hermes/sessions/` and are searchable. After setup
is complete, Joe should rotate the token (delete and create new) so the one in
the transcript becomes invalid.

Alternative: Joe can set the PAT in `~/.hermes/.env` as `GITHUB_TOKEN` and use
`gh auth login --with-token < ~/.hermes/.env` or `export GITHUB_TOKEN=...`.
This keeps the token out of the session transcript entirely.

## Pitfalls

- **dpkg lock:** `E: dpkg was interrupted` — run `dpkg --configure -a` before apt installs
- **Bad credentials on auth:** Token may be truncated in copy-paste. Regenerate.
- **Token scope too narrow:** If `gh repo list` only shows one repo, the PAT is scoped to a different repo than expected. Recreate with correct scope.
- **Fine-grained PAT fails for git push (403):** Even with admin permissions, fine-grained PATs often fail for HTTPS git push operations. `oauth2:<token>@github.com` and `x-access-token:<token>@github.com` both return 403. The fix is SSH deploy keys (see Step 5). Use `gh api` to manage deploy keys, then push via SSH.
- **Old .git directory:** If `.hermes/docs/Paul/.git` has wrong ownership or remote, save it as `.git.old-<date>` and `git init` fresh.
- **PAT in session transcripts:** Tokens pasted in chat are stored in Hermes session logs. After setup, Joe should rotate (delete + recreate) the PAT.
