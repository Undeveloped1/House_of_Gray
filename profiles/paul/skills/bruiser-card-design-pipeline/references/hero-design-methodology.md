# Hero Design Methodology

## Starting Point: Character Moment, Not Mechanics

When designing hero (Capo) cards, start from the character's personal moment — "what does this Capo do that nobody else can?" — not from faction keywords or mechanical role.

- Silver = the metal man whose Villium rune activates, becoming indestructible
- Tommy = the last man standing, clears the room to a one-on-one fistfight
- Moses = the undertow, quiet water that resets the board one-sided

Starting from "Dock Tax faction keyword" produced lazy, oppressive designs (passive enemy Villium loss every turn, opponent can't play). Starting from "what does the quiet brother DO when he acts?" produced Undertow — one-sided mass bounce + discard. The character-first prompt unlocks the design.

**Optimal prompt:** "What is [character]'s personal moment — the one thing only they can do?" Mechanics follow character, not the other way.

**Joe's words (2026-05-31):** "You have two very clear examples of what makes a great legendary card with Tommy and with Silver. I'm reading this and it's like, yeah whenever they do something they lose a Villium."

## Ultimate Design Gate (LOCKED 2026-05-31)

**An Ultimate cannot be an effect that could appear on a regular card — including Legendary cards.** The Ultimate is the Capo personally intervening in a way that breaks normal game rules. If you could print it on a minion or spell, it's not an Ultimate.

Test: "Is this effect beyond anything a card can do?"

| Capo | Ultimate | Gate check |
|------|----------|------------|
| Silver | Silver Steps In — becomes 5/5 Indestructible Hustle minion, +1/+1 per minion in play, bounce = replay-or-lose, exile = lose | ✓ Hero becomes minion, game-loss stakes |
| Tommy | No One Walks — each player sacrifices to 1 minion, they fight, survivor gets +3/+3 permanently | ✓ Board rewrites into 1v1 duel |
| Moses | Undertow — return all enemy minions to hand, opponent discards random per returned | ✓ One-sided mass bounce + mass discard |

## Design Process per Capo

1. Read the character's Inner Circle profile — origin, personality, defining moment
2. Identify their personal moment — the one thing only they do
3. Design the Ultimate first — it's the fireworks display, the thing that can't be on a card
4. Design passive and active to feed that gameplan
5. **Check canonical card file** (not memory) for faction mechanic density before finalizing passives/actives
6. **Check recent Daily Handovers** for existing locks — don't propose abilities already locked

## Hero Output Format

Every hero card should include these sections, not just the ability table:

- **Identity:** One sentence — who they are, what they do.
- **HP:** Value with rationale (higher = less explosive; lower = more aggressive).
- **Ability table:** Passive, Active (2V), Ultimate, Coup de Grâce.
- **Design rationale:** One paragraph per slot explaining why this ability, how it connects to the character's lore, and how it passes the Ultimate design gate.
- **Play pattern:** Turns 1-5, 5-8, 9/10 — how a player pilots this hero through a game.
- **Lore alignment:** One sentence connecting the hero's mechanics to their backstory, with a signature quote where available.

After all three heroes, include a **Hero Comparison Table:**

| Axis | Hero A | Hero B | Hero C |
|------|--------|--------|--------|
| Playstyle | | | |
| Faction Pillar | | | |
| HP | | | |
| Passive | | | |
| Active | | | |
| Ultimate | | | |
| Win Condition | | | |
| When You Lose | | | |

And a **Synergy note:** One paragraph explaining how the three heroes share the core pool — which hero's strengths cover another's weaknesses.

## Trigger v2 Hero Example

A complete, proven hero document (Gerald, Lucy, Bunny with full rationale, play patterns, lore alignment, comparison table, and synergy note) is at:
`/root/.hermes/docs/Paul/workspace/Trigger_Heroes_v2_2026-06-05_Paul.md`

Reference it for format and depth.

## Hero Card System Spec (LOCKED 2026-05-31)

- **Slots:** Passive · Active (2V) · Ultimate (T9/T10, no V cost) · Coup de Grâce (cosmetic)
- **Deck select:** Player picks Passive OR Active before game
- **Ultimate timing:** T10 if going first (no T1 draw), T9 if going second (draws T1)
- **HP:** 20-25, inversely correlated to kit explosiveness
- **Hero-to-minion:** Hustle + Indestructible, on-board card cost 7V, bounce = auto-replay-or-lose, exile = lose
- **One per faction** has the "become a minion" pattern — not all three
