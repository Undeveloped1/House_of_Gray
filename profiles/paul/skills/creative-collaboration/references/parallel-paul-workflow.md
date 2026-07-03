# Parallel Paul — Multi-Instance Design Workflow

**Discovered:** 2026-06-04. Joe tested two concurrent Paul sessions — both worked. His reaction: "I'm so fucking blown away right now. Like, what do I even need cursor for, bro?"

## What It Is

Hermes supports multiple concurrent sessions with the same profile. Each Paul instance gets its own conversation, terminal, and toolset. They operate independently — no shared context beyond what they read from disk.

## When to Use

| Work Type | Parallel? | Why |
|-----------|-----------|-----|
| **Creative design (lore, characters, names)** | NO (default) | Joe wants to collaborate in real time |
| **Creative design (overnight batch)** | YES (with authorization) | Joe explicitly says "run this overnight" or "spin up instances and go" |
| **Mechanical tasks (audits, reviews, red team)** | YES | Verification, not creation — Joe wants answers, not creative output |
| **Multi-lane research** | YES | Different warmup docs, no collisions |

## The Overnight Pattern

Joe's vision (2026-06-04): "We will make a master prompt that gives you all the access to all the documents and all the things, and I'll let you fucking run it until your wheels fall off. I can start you going before I go to bed and wake up to a fucking duster faction that's start to finish done."

The pipeline is serial even if instances are parallel:
- **Lore MUST lock before cards.** If Paul makes wrong lore calls, everything downstream is compromised.
- **Cards MUST lock before red team.**
- Once lore is locked through collaborative review, Joe can spin up card design, art, and red team Pauls in parallel with warmup docs.

## The Warmup Doc Pattern

Joe drops a warmup doc per instance. Each doc loads:

1. **The source of truth** — which docs to read for context (faction bible, card files, design decisions)
2. **The specific lane** — what this instance does (lore, card design, art, red team)
3. **The deliverable format** — what file to write, where to save it
4. **Hard boundaries** — what NOT to do (don't touch other lanes, don't edit locked files)

### Warmup doc template

```markdown
# Paul — Session Warmup: [Faction] [Lane]

## Where we are
[State of the faction/project. 1-2 paragraphs.]

## Working files (read these)
- [List of docs to load for full context]

## Your lane
[Specific task: "character depth pass" / "card design from function registry" / "red team pass on Bruiser cards"]

## Deliverable
[File path, format, expected sections]

## Hard rules
- Fabrication Is Forbidden — research before claiming
- Stay in your lane — don't touch other factions/docs
- Write to workspace/ only
- [Lane-specific rules]
```

## Collision Avoidance

Multiple Pauls writing to disk simultaneously requires lane discipline:

1. **Separate output files per lane.** Lore Paul writes `Duster_Lore_Paul.md`. Card Paul writes `Duster_Cards_Paul.md`. Never two instances writing to the same file.
2. **Read-only for shared sources.** All instances read the faction bible, card files, and design docs. None edit them.
3. **Dropbox is the handoff.** Completed files go to `syncthing/paul-dropbox/`. Joe/Cursor merge into the repo.

## Known Limitations

- No inter-instance communication. Paul A doesn't know what Paul B is doing.
- If two instances both need Joe feedback, he has to context-switch between them.
- Model/provider behavior may differ between instances depending on config.

## The Solo-Sprint Distinction

**This is NOT a license to replace collaboration.** The 2026-06-04 Trigger session proved the pitfall: Paul interpreted "execute, don't facilitate" as "complete D5, G, H, and all 8 character backstories without Joe." Joe's correction: "We're supposed to be doing these together."

**But Joe was excited, not angry, about the capability.** He wants to deploy it correctly: warmup docs for overnight batch work, collaborative review after. The machine runs hard while he sleeps, then he shapes the output live.

## Changelog

**2026-06-04** — Created from Joe's discovery of concurrent Paul sessions during Trigger lore session. Updated with Joe's excitement, overnight batch pattern, and solo-sprint distinction.

**2026-06-04 (evening)** — First concrete overnight warmup deployed: `Trigger_Overnight_Warmup_2026-06-04_Paul.md` — full 55-card Trigger set + 3 heroes design brief. Points to all lore docs, both mechanics docs, Bruiser_Cards.md format reference. Serves as template for future faction overnight warmups.
