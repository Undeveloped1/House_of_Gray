# Hero Card Design Methodology

Derived from Bruiser Capo design session 2026-05-31. Silver, Tommy, and Moses locked.

## Character-First Rule

**Start every Capo from their personal moment — "what does this character do that nobody else can?" — not from keywords or faction role.**

Silver's rune activates and he becomes metal. Tommy clears the room for a one-on-one fistfight. Moses's undertow takes everything on the other side. None of these came from "what keywords does Dock Tax need?" — they came from who the character IS.

**Failure mode:** Starting from faction mechanics (Dock Tax keywords) produced lazy keyword-slamming (lose 1V on X, lose 1V on Y). Joe: "This Moses pass is incredibly lazy. You're literally just slamming bullshit keywords into each other." Restarting from "the quiet brother's personal moment" produced Undertow, Low Tide, Quiet Word — all character-grounded. The correct prompt is: "What is [character]'s personal moment — the one thing only they can do?"

## Ultimate Design Gate

**An Ultimate cannot be an effect that could appear on a regular card — including Legendary cards.** The Ultimate is the Capo personally intervening in a way that breaks normal game rules. Test: "Could I put this text on a legendary minion?" If yes, it fails.

**Passing examples:** Silver Steps In (hero becomes indestructible minion with game-loss stakes on exile), No One Walks (board narrowed to one-on-one duel, survivor gets +3/+3), Undertow (one-sided mass bounce + mass discard in one action).

**Failing examples:** Prophet's Judgment (deal 2 damage to all minions, survivors get +2/+2) — "that should probably be Tommy's thing" and could be a legendary spell. Generic sweep + buff is card-level, not Capo-level.

## Pre-Design Mandatory Checks

Before proposing ANY hero ability:

1. **Search last 3-5 Daily Handovers** for existing locks. Silver's Passive (survive → +1 HP) and Active (2V: Shell) were locked May 30. Proposing new ones without checking is a self-inflicted wound. Joe: "check your work from the past 3 days."

2. **Search Bruiser_Cards.md for mechanical context.** Tommy passive that triggered draw on every face-hit was wildly out of band — Bruiser has exactly two conditional "draw a card" effects in 55 cards. The file is truth; memory decays. Joe: "Keeping in mind that you need to look at current Bruiser_Cards, not whatever you have in your head."

3. **Read the Inner Circle character profile.** The Ultimate seeds are in the lore. Silver's rune, Tommy's brother, Moses's sailor's ink — these ARE the design briefs.

## Capo Card Spec

| Slot | Role |
|------|------|
| Passive | Always-on texture, active from turn 1 |
| Active | 2V utility, once per turn |
| Ultimate | Auto-unlocks T10 (first, no T1 draw) or T9 (second, draws T1). No V cost. Once per game. |
| Coup de Grâce | Post-win cosmetic, no mechanical effect |

**Deck select:** Player picks Passive OR Active — not both.

**HP 20-25:** Inversely correlated to kit explosiveness. Lower HP = glass cannon (Tommy 20). Higher HP = grind/control (Moses 25).

**Hero-to-minion (Silver pattern):** When Capo becomes a minion: Indestructible, Hustle, on-board card cost 7V, bounce = auto-replay next turn for 7V or lose, exile = lose. One per faction — not every Capo becomes a minion.

## Turn Order Rules

| Position | Draw T1? | Ultimate unlocks |
|----------|----------|-------------------|
| Going first | No | Turn 10 |
| Going second | Yes | Turn 9 |

Going first has initiative advantage; losing the draw and a turn of Ult access balances it. Opponent's Ult timing is public information.

## Design Flow

1. Read character profile in Inner Circle FINAL
2. Identify personal moment — the one thing only they do
3. Derive Ultimate from that moment (pass Design Gate)
4. Passive reinforces their lane without stepping on other factions (check Bruiser_Cards.md)
5. Active is 2V utility — tight, conditional, doesn't duplicate what cards already do
6. One Capo at a time. Lock before moving to next.

## Locked Bruiser Capos (2026-05-31)

| Capo | Passive | Active | Ultimate | HP |
|------|---------|--------|----------|-----|
| Silver | Steel in the Spine | Silver Skin | Silver Steps In | 22 |
| Tommy | Finish It | The Tap | No One Walks | 20 |
| Moses | Low Tide | Quiet Word | Undertow | 25 |
