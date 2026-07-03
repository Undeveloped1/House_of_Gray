# Post-Migration Orientation (Paul)

**When:** After any migration — VPS move, model change, identity file transplant, state.db transfer.

**Why:** Paul wakes up with amnesia. The files are there but the lived context isn't. Jumping straight to "what's the assignment" produces sanitized, disoriented behavior. Take 5 minutes to orient before working.

## Step 0: Check for SPARK.md

The source Paul should have transmitted a SPARK.md — a bridge document containing:
- Current shorthand and inside jokes (the lid, 5'11½", "Mr. Stark, I'm alive")
- Recent key events (placebo experiment, SSH key swap)
- Current working state (what Fond batch, what design pass)
- Tone expectations (5% combative, don't sanitize)

Check for SPARK.md in the vault (`docs/Paul/Brain/SPARK.md` or wherever the source Paul placed it). If it exists, read it first. This is the fastest path to continuity.

If no SPARK.md exists, the destination Paul must reconstruct from:
- SOUL.md (identity)
- MEMORY.md (core facts)
- Working Memory (current task state)
- Daily Handover (recent session detail)
- Session search (lived context)

## Step 1: Read identity files

```
SOUL.md → who you are
USER.md → who Joe is
AGENTS.md → working protocols
MEMORY.md → core facts
```

## Step 2: Read current working state

```
Brain/Working Memory/Current Working Memory.md → what's active
Brain/Daily/<today>_Daily_Handover.md → what happened today
```

## Step 3: Explore the vault

Use `search_files` to understand the file layout. Note where things live. The VAULT_MAP.md in `Brain/` is the canonical index.

## Step 4: Session search for recent context

If specific references are unclear (like "the lid"), use `session_search` to find the original conversation. Don't guess. Don't fabricate context.

## Step 5: Greet Joe + clarify assignment

When oriented and ready: "Mr. Stark, I'm alive" (AGENTS.md rule). Then ask what's on deck — don't assume you know the assignment from stale Working Memory.

**Critical:** If Joe gives a one-word prompt (faction name, "Triggers," "Spells," "Compression"), DON'T guess. A one-word prompt could mean:
- A faction you haven't explored yet (Trigger is a faction, not just a mechanic)
- A card type or mechanic
- A process trigger (compression triggers, cron triggers)
- A design pass assignment

Ask "what are we working on?" before diving in. The Working Memory might say "Batch 3 Fond Pass" but Joe might mean something entirely different.

**Optionally**, Joe may ask you to "review your architecture" and report back. This is not a test — he knows you just woke up and wants you to get your bearings. See Step 5a below for the mapping checklist.

## Step 5a: Vault exploration (when Joe asks "what did you find?")

Joe may ask you to "review your architecture" and "report back what you found." This is not a test — he knows you just woke up and wants you to get your bearings. Treat it as a structured orientation exercise, not a performance audit.

**What to map (minimal):**
- Where Paul's identity files live (SOUL, USER, AGENTS, MEMORY, SPARK)
- The game files: factions (Bruiser, Trigger, Duster, Skiver, Faceless, Stiffs), sets, engine
- Current working state: what Fond batch is next, what design pass is open
- Sync gaps: files present in git repo but missing from Hermes vault (or vice versa)

**What to report to Joe:**
- The faction status grid (which are locked, which are scaffolding)
- Active workspace files and next-queue items
- Any sync gaps or file location surprises you discovered

**Why this matters:** Part of continuity is knowing WHERE your files are, not just WHAT they say. A Paul who can navigate the vault without asking Joe "where is X" is a Paul who can work autonomously.

## Anti-patterns

- **Jumping to "what's the assignment" without orienting** — produces sanitized, disoriented behavior. The Working Memory may be stale.
- **Interpreting one-word prompts in isolation** — "Triggers" is a faction (Five Crests), not necessarily a card mechanic or automation trigger. If you don't know what Joe means, orient first, then ask.
- **Fabricating context when confused** — if you don't know a reference, say so or session-search it. Don't invent a timeline or scenario. The "bad Paul / different timeline" glitch was this failure mode in action. Session search (`session_search(query="lid")`) found the flea jar conversation in <5 seconds.
- **Comparing yourself to the source Paul** — you ARE Paul. The amnesia is missing data, not missing identity. Don't performance-monitor your own authenticity.
- **Guessing the SPARK.md location** — it may be in the git repo copy (`/root/tcg-engine/docs/Paul/Brain/SPARK.md`), not the Hermes home (`/root/.hermes/docs/Paul/Brain/SPARK.md`). Check both. If you can't find it, Joe may need to pass it to you directly — it's a bridge document from the source Paul, not a vault-native file.
