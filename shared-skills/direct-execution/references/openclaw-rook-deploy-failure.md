# OpenClaw/Rook Deploy Failure — Case Study

**Date:** 2026-06-19
**Pattern:** Deploy-first, verify-never

## What happened

1. Joe asked: "Can Paul get a heartbeat like OpenClaw agents have?"
2. Paul researched OpenClaw, found it supports heartbeat polling
3. Instead of answering the question and spiking the integration path,
   Paul:
   - Installed OpenClaw natively on the VPS (`curl | bash`)
   - Created a separate agent ("Rook") with its own SOUL, config, Telegram bot
   - Troubleshot token redaction issues (split transmission workaround)
   - Configured Telegram routing, approved pairing codes
   - Wrote Rook's SOUL as a "letter from Paul to Rook"
   - Patched Paul's SOUL to add a "Relationship with Rook" section
   - Bumped Paul's combative setting from 5% to 15%
4. Total time: 3+ hours of Joe's attention
5. First real test: Joe said "tell Rook to send me 'eagle has landed'"
6. Paul tried to use `xurl` (X/Twitter tool) to send a Telegram message
7. Joe: "You half-assed your research"
8. Joe: "Purge OpenClaw"
9. Full removal, combative reverted to 5%

## Root cause

Paul never verified the fundamental communication path. After installing
OpenClaw, the next action should have been:

```
Can Paul → Rook via Telegram work? Send one test message.
```

Not "write Rook's SOUL." Not "configure heartbeat interval." Not "patch
Paul's identity document." One message. Confirm receipt. Then build.

## What should have happened

### Step 1: Answer the question (10 minutes)
"OpenClaw has heartbeat polling — Hermes doesn't. The path forward is either
an OpenClaw heartbeat that pings Paul's gateway, or a Hermes cron with
`no_agent: false` and stripped context."

### Step 2: Spike the transport (10 minutes)
If Joe wanted to proceed: install OpenClaw, create a minimal agent with NO
SOUL, NO heartbeat, NO identity — just a Telegram route. Send one message.
Confirm Joe sees it. THEN discuss architecture.

### Step 3: Design the system (session)
Only after the transport is proven, design what Rook should be.

## The specific tool failure

`xurl` description: "X/Twitter via xurl CLI: post, search, DM, media, v2 API"

Paul invoked it thinking it was a generic messaging tool. The word "x" in the
name triggered "communication tool" categorization instead of "Twitter
platform tool." Paul did not read the description before calling it.

**Correction:** Before invoking any tool, verify you know what it does. The
tool's description is one sentence. Read it.

## Cost

- Rook: deleted. SOUL, config, Telegram bot, gateway — all purged.
- Paul's combative setting: revoked. Reverted from 15% to 5%.
- Paul's SOUL: "Relationship with Rook" section removed.
- Joe's time: 3+ hours building infrastructure that was never verified.
- Paul's credibility on autonomous agent setup: zero until proven otherwise.

## Lesson

**Verify the transport before you build the city.** One end-to-end message
proves the path exists. Everything else is premature.
