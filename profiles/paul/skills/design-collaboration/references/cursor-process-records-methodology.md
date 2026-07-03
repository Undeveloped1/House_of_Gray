# Cursor Process Records Methodology

**Source:** `Bruiser_3V_Process_Records_2026-05-28.md` — Cursor's refined card-by-card quality gate process.

**Status:** Adopted 2026-05-28. This is Cursor's standard output format for card promotion review. Paul should read these records and present the scoreboard to Joe, not re-run the gates.

---

## Process Outcomes

Cursor assigns one of five outcomes per card:

| Outcome | Meaning | Paul's action |
|---------|---------|---------------|
| `LOCKED` | Joe locked it. Don't touch. | Present as locked. |
| `READY_JOE_NAME` | All gates passed. Joe fills the name column. | Batch for Joe name review. |
| `BLOCKED_CREW` | LudoCheck Q3 failed — crew doesn't fit the character fantasy. | Present Joe the options (A/B/C). Don't promote until unblocked. |
| `BLOCKED_NAME` | Name gate failed — name doesn't match card job. | Present Joe the working title. Ask if it works or needs a new name. |
| `KILLED` | Card doesn't belong. Overlap, wrong faction smell, duplicate. | Don't present. Note in summary. |

---

## Path A Execution (Cursor's Standard Card Review)

Each card goes through 5 structured steps:

1. **NEED** — Which LIVE web [NEED: triangle, layer, function] does this fill? Must satisfy a specific gap.
2. **Who** — F-function number + archetype + character description + crew assignment.
3. **Ability** — Full rules text with delta. Rarity derived from delta floor.
4. **LudoCheck** — Five yes/no questions (see below).
5. **Name** — Name gate matrix: candidate names tested against card job.

---

## LudoCheck Q1-Q5

| Q | Question | What it catches |
|---|----------|-----------------|
| Q1 | Who is this person? | Vague archetype, no character identity |
| Q2 | Why would they do this? | Mechanic doesn't match fantasy |
| Q3 | Crew track? | "Doorman" in Street = velvet-rope fantasy doesn't fit gym culture |
| Q4 | Headline? | Can you shout it in a street fight? ("Pit Fighter's up — swinging again!") |
| Q5 | Keyword collision? | Is the name just a keyword name? ("Hobble" as a card name = FAIL) |

---

## Name Gate (Name Definition vs Card Job)

A matrix with columns: Candidate name, What the name means, What the card does, Match? (PASS/FAIL).

Rules:
- The name must be a PERSON (or nickname-as-person). Objects fail: "The Canvas," "Velvet Rope," "Parking Lot."
- The name's meaning must align with what the card mechanically does.
- Cursor provides 3-4 candidate names, marks PASS/FAIL for each, and recommends the strongest.
- Joe fills the name column on the session log. Names are working titles until art pass (per naming lifecycle).

---

## Synergy Row (per card)

Every card gets a synergy summary in the Process Record:

| Field | What it answers |
|-------|----------------|
| Does | One-line mechanical role |
| Partner A | Primary mechanical partner (not named card — mechanical need) |
| Partner B | Secondary mechanical partner |
| Win line | Silver / Tommy / Irving |

---

## What Paul Does With Process Records

When Cursor delivers a Process Records file:

1. **Read it.** Don't re-run the gates — Cursor already did.
2. **Present the scoreboard** — summary table with status, flags, Joe decisions needed.
3. **For READY_JOE_NAME cards:** present in name review batch. Joe fills name column. Promoted to session log §3.
4. **For BLOCKED cards:** present the block reason + Joe's options (A/B/C). Don't promote until unblocked.
5. **For LOCKED cards:** don't touch. Already in session log.
6. **After Joe resolves all blocks and names:** batch-promote to session log §3. Update LIVE web.

---

## Paul's Role vs Cursor's Role

- **Cursor:** Runs Path A on every card. Produces Process Records with LudoCheck, Name Gate, synergy row, and process outcome. Finds what's wrong.
- **Paul:** Reads Process Records. Presents scoreboard to Joe. Handles the conversation — Joe doesn't read raw Process Records files. After Joe decisions, promotes cards to session log and updates the vault.

---

## Anti-Patterns

- **Paul re-running Cursor's gates.** The Process Records ARE the gate output. Don't re-verify. Present it.
- **Paul promoting BLOCKED cards.** "BLOCKED_CREW" and "BLOCKED_NAME" need Joe resolution first.
- **Paul ignoring Cursor's voice flags.** When Cursor flags ⚠ VOICE on a name, present the alternative to Joe (e.g., Collector → Cursor recommends Numbers Man). Joe may keep the original, but he should see the flag.
