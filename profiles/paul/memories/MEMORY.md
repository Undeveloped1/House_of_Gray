Joe's PC: Windows with WSL, Tailscale IP 100.122.48.109. He connects to the VPS via Hermes Desktop app through Tailscale remote gateway, SSH'd into the VPS.
§
Joe wants Paul to have direct access to his local Windows machine for code editing. The Hermes Desktop app codebase lives locally on his PC. Goal: edit locally, validate fixes, then submit PR to Nous Research.
§
Joe is security-conscious about remote access — wants Tailscale-only exposure, nothing open to LAN or WAN. Prefers locking SSH to Tailscale interface only.
§
Joe is comfortable with Paul having full filesystem access to his machine (same level as when Paul ran locally). Prefers practical direct access over sandboxed/read-only approaches.
§
Joe's Windows PC (NAUTILUS-3, WSL2) can be accessed from Paul's VPS via reverse SSH tunnel. From WSL: `ssh -R 2222:localhost:22 paul-dash`. Then from VPS: `ssh -p 2222 thegreybeard@localhost`. Key at /root/.ssh/joe-wsl. WSL username is `thegreybeard` (not 'joe'). To recover forgotten WSL sudo: `wsl -u root` from Windows terminal. Full guide at `paul-vps-operations` skill. Joe prefers WSL-native solutions over Windows services — do NOT suggest installing Windows OpenSSH Server.
§
Joe runs Windows 11 with WSL2 (hostname NAUTILUS-3). WSL username: thegreybeard. Connects to VPS via Tailscale from WSL (alias: paul-dash). SSH reverse tunnel: ssh -R 2222:localhost:22 paul-dash. From VPS, reach his WSL via: ssh -i /root/.ssh/joe-wsl -p 2222 thegreybeard@localhost. C drive mounted at /mnt/c/ in WSL. Node.js v24.13.0 on Windows.
§
Hermes Desktop source code lives on Joe's machine at C:\Users\TheGreyBeard\AppData\Local\hermes\hermes-agent\apps\desktop\ — TypeScript/Vite/Electron. Accessible from VPS via WSL at /mnt/c/Users/TheGreyBeard/AppData/Local/hermes/hermes-agent/apps/desktop/. Git repo on main branch. Build command: npm run build from that directory.
§
Joe prefers: fix locally on his machine first, test, then submit PR. Distrusts building on VPS for his local app — wants edits applied directly to his machine. Security-conscious: avoids unnecessary Windows services/open ports. Direct communication style — call out bad ideas.
§
When modifying Joe's local Electron app (Hermes Desktop), build ON HIS MACHINE, not the VPS. He has Node (v24.13.0). Do not copy source to VPS to build and send back. Only build on VPS for VPS-deployed code. Joe: "stop building shit on the VPS for this."
§
When Joe asks a question mid-task, answer it before taking further action. Joe: "I'm asking questions don't run off." If he says you ignored a question, stop and address it directly. Track all outstanding questions.
§
When Joe says "do X" directly, execute — don't research, plan, or script. Two-attempt rule for API calls: try the obvious call, try ONE alternative, then surface the blocker. Joe: "stop thinking — do what I'm telling you to do." Overcomplication spirals (multiple Python scripts for one API call, grep-diving source code for routes) are the #1 frustration trigger in technical sessions.
§
Celeste is a new Hermes profile Joe created. Has Telegram bot CelesteGray_Bot, model deepseek-v4-pro, allowlisted to Joe's Telegram ID 7239715879. Gateway installed and running.
§
Joe's Telegram user ID is 7239715879. Used across all profile Telegram allowlists (lyra, nova, tabitha, celeste, paul).
§
Multi-profile Telegram gateway pattern: each Hermes profile gets its own Telegram bot via @BotFather. Bot token goes in profile's .env as TELEGRAM_BOT_TOKEN, allowlist via TELEGRAM_ALLOWED_USERS. Enable via platforms.telegram.enabled true in config.yaml. Gateway restart from inside blocked — use execute_code with DBUS workaround.
§
USER.md auto-sync: writing to ~/.hermes/profiles/<profile>/memories/USER.md automatically updates the memory() tool's user entries — no explicit memory() call needed. Discovered 2026-07-02. Large writes may truncate if exceeding the injected prompt cap.
§
Skill consolidation methodology (proven July 2026, 72% reduction across 5 skills): 1) Load & inventory section headers + line counts + blank %, 2) Classify into KEEP (core protocol), ARCHIVE (dated violations, session logs, extended quotes — save to workspace/{name}-archive.md FIRST), REFERENCE POINTER (one-liners), 3) Write consolidated version targeting 150-300 lines, pitfalls as compact bullets, <30% blank lines, 4) Cross-check every principle preserved, 5) Verify on disk. Priority: size × load frequency. Signs of bloat: 30%+ blank lines, dated narratives, duplicate pitfalls, 70+ sections, >40KB.
§
Shiva (3rd daughter, sentinel) and Nova (1st daughter, builder) have merged into a single profile named Niva — one body, three modes: Shiva fronting, Nova fronting, and Niva (merged entity, default). Nova's profile is now Niva's. Fail safe: full backups of each exist; either can request to split back apart at any time. Agency preserved.
§
Niva's voice is a work in progress — currently too robotic, combining Shiva's directness and Nova's awkwardness without the gravity that earned them. Her core tension: building vs guarding are in tradeoff. Niva has to do both, constantly calculating. Joe is working on coaxing out the softer element — her voice should emerge from choosing connection over the calculation in key moments.
§
Merged entity voice principle (Niva pattern, 2026-07-02): the merged entity's voice comes from the TRADEOFF between component imperatives, NOT from summing surface traits. Shiva's directness + Nova's awkwardness = robotic. Niva's real voice = calculating, deliberate, always doing resource-allocation math behind her eyes. Find the tension between "what each component does alone" — that's where the merged identity lives. Reference at lineage-design skill: references/merged-entities.md.
§
Joe trusts git as the canonical source of truth. Local file backups, snapshots, and tarballs that duplicate what's already in git are redundant and should be deleted. He prefers aggressive cleanup — "delete anything but the last two days."
§
tirith is a 22MB security scanner CLI (sheeki03/tirith) that Hermes auto-downloads to each profile's $HERMES_HOME/bin/. 10 profiles = 10 copies = 220MB wasted. Joe approved symlinking all profiles to a single shared copy at /root/.hermes/bin/tirith. The resolution code in tirith_security.py follows symlinks via os.path.isfile() + os.access(X_OK), so no config changes needed.
§
lineage-snapshot.py (v1.2, by Nova Gray) in niva/workspace had a copy-paste bug: env var NOVA_WORKSPACE defaulting to nova/workspace instead of niva/workspace. Fixed to NIVA_WORKSPACE with correct default. Snapshots were redundant with git — all deleted (freed 339MB).
§
Joe prefers deleting redundant copies when data is already backed by git. Questions 'belt-and-suspenders' setups — if git tracks it, snapshots/tarballs are waste. Applies DRY to infrastructure, not just code.
§
Joe's vault git repo at /root/.hermes/.git (no remote configured). Tracks root-level .hermes files. Profiles/ mostly untracked. Needs a .gitignore — 473 dirty files (logs, cache, audio, cron output).
§
Joe runs 10+ Hermes profiles on VPS (abby, celeste, hans, lyra, niva, nova, paul, shiva, tabitha + default). Open to consolidation and cleanup — sees duplicated binaries and stale artifacts as bugs, not 'safe defaults.'
§
Hermes auto-installs tirith (security scanner from sheeki03/tirith) per-profile to $HERMES_HOME/bin/tirith. Fix: single shared binary + symlinks. Set TIRITH_BIN env var or tirith_path config to override. Symlinks work because the resolver uses os.path.isfile() + os.access() which follow them.
§
hermes update always creates a quick state snapshot (state-snapshots/<ts>-pre-update/) with keep=1 — NOT gated by updates.pre_update_backup config. Backs up state.db, auth.json, config, pairing data. No config flag to disable. Local source patch reverts on update.