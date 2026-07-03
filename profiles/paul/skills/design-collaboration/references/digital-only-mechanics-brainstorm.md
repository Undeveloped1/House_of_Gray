# Digital-Only Mechanics Brainstorm

**Status:** Reference — methodology + worked example  
**Session:** 2026-06-04 (Paul + Joe Trigger brainstorm)  
**Fits under:** design-collaboration § Mechanics Brainstorming Methodology (alternate lens)

---

## When to Use This Lens

When Joe asks "what abilities or mechanics don't currently exist in MTG or Hearthstone because it would be too hard to make work — but since we're digital, we can?"

This is NOT the standard "brainstorm mechanics from functions" pipeline step. It's a constraint-first approach: start from what's impossible in paper, then filter for faction fit.

---

## Core Insight

Paper TCGs have two hard constraints that digital removes:

1. **Nothing can be truly hidden from both players.** Someone has to track it. Morph and foretell let the player who made the choice peek. True hidden state — secret from BOTH players — requires an engine to track.
2. **Nothing can require remembering more than ~3-4 pieces of game state across turns.** Complex cumulative tracking, cross-zone memory, causal chains — all require the engine, not player memory.

---

## Methodology

1. **Read existing faction workups first.** Design Bible, character roster, crew structure, keyword locks, blind spots. You must know what the faction IS before proposing new mechanics.
2. **Identify the faction's core identity in one phrase.** Professional detachment? Information asymmetry? Muscle that won't stay down? This is your filter.
3. **Brainstorm from the digital constraint, not the faction.** "What can paper NOT do?" produces a menu. Then filter for faction fit.
4. **Present 6-7 mechanic categories with 2-3 worked examples each.** Categories should be conceptually distinct (hidden state, cross-zone memory, reality warping, etc.).
5. **Anchor each to the faction's existing mechanics.** "This is an evolution of Marked→Contract" lands better than "here's a new keyword."
6. **Sort by buildability.** Tier picks that slot into the existing engine first; the truly radical ideas second.

---

## Mechanic Categories (from 2026-06-04 Trigger session)

### 1. True Hidden Contract (hidden state, engine-tracked)
Secret from BOTH players after placement. The game tracks the Contract; the player forgets which minion was marked. Evolves the existing Marked→Contract→Paid→Loot loop by changing visibility rules.

### 2. Ghost Permanents (invisible enchantments)
Opponent suspects something is wrong but can't see the source. Counterspells: "Expose all Ghosts." Management/Intel tier flavor.

### 3. Cleaner (exile + erase causal links)
Exile a card AND remove all triggered abilities referencing it from the stack. Contracts on wiped targets evaporate with no penalty. Requires the engine to track causal chains.

### 4. Deep Contract / Sticky Markers
Invisible markers that survive zone changes (death, bounce, shuffle). The Contract counter moves with the card through hand, deck, graveyard, and battlefield.

### 5. Simultaneous Hidden Choice (prisoner's dilemma)
Both players secretly commit, then reveal simultaneously. The game is the neutral arbiter. Street/racket tier flavor.

### 6. Cumulative Game Tracking (The Ledger)
Track cross-game stats (Contracts completed, minion types killed, damage dealt) with threshold unlocks. Quest-like but faction-flavored.

---

## Filter Questions

For each proposed mechanic, answer:

- **Which crew tier does this belong to?** (Street, Professionals, Court, Ghosts, Management, Help)
- **Does it fit the existing keyword ecosystem or conflict?** (Hidden Contract = Marked evolution, not replacement)
- **Is it a core loop twist or a card-level addition?** (Hidden Contract = loop twist, Ghost Permanents = card additions)
- **What's the counterplay?** (Expose Ghosts, Cleaner-erasing Cleaners, etc.)
- **Could any other faction use this?** (If yes, it might need to be universal or neutral)

---

## Worked Example: Trigger (2026-06-04)

Full session transcript available. Key takeaways:

- **Hidden Contract** was the strongest fit — evolves the existing Contract loop without replacing it, is thematically locked to Trigger's professional detachment, and is genuinely impossible in paper.
- **Ghost Permanents** pair with Management's intel theme and Cloak (both = "you don't see us coming").
- **Cleaner** maps directly to Mr. Fox's existing role in the roster.
- **Loan Shark** (temporary theft with compensation) was discussed but landed in "fits Bruiser better" — Trigger doesn't borrow, they kill.
- Joe's response to the brainstorm was "let's keep going" — the lens was productive enough to continue a second round.

---

## Anti-Patterns

- **Don't start with MTG keywords as the first pass.** "What paper can't do" ≠ "what MTG does, digitally." Build from the constraint, not the existing game.
- **Don't propose mechanics without reading the faction workups.** A mechanic that sounds cool but contradicts a locked blind spot is wasted effort.
- **Don't present all mechanics as equal.** Tier them: "this one changes the faction's identity at the mechanical level" vs. "this is a card-level addition."
