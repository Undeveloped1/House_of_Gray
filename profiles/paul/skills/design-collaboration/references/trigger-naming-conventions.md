# Trigger Faction Naming Conventions (LOCKED 2026-06-08)

Joe's naming rule across every faction: names must pass the **street-fight callout test** — could someone on either side of a street fight shout it and everyone knows exactly who they mean?

## Crew Naming Rules

| Crew | Rule | Examples (from v7) | Violation Examples |
|------|------|--------------------|--------------------|
| **Street** | Nicknames or first-name-only. One syllable. What the corner shouts. | Rook, Butch, Moose, Junior, Ox, Rocco | — |
| **Professionals** | **Epithets or role-names ONLY. NO SURNAMES.** If it sounds like a birth certificate, it's wrong. One syllable preferred. | Hammer, Ghost, Wolf, Collector, Sculptor, Finger Man, Button Man, Bagman, Heavy, Primer | Ricci, Caruso, Lupo, Reyes |
| **Court (Mgmt)** | Full formal names. Power through respect. | Gerald Ashworth, Bunny Gallagher, Harold Kemp, Victor Crane, Augustine Webb | — |
| **Management (Analyst)** | Role-based names. What they do, not who they are. | Lookout, Surveyor | — |
| **Help** | First names or trade names. One name is enough. | Sal, Mickey, Franco, The Range | — |
| **Legendaries** | Full names (people) or trade names (objects). | Lucy Greenwald, Carlo's Piece | — |
| **Spells** | Verbs or nouns describing the action. No people names. | Final Notice, Payday, Snap Decision, Termination | — |

## Why Sub-Agents Get This Wrong

Sub-agents default to surnames because:
1. Italian surnames (Ricci, Caruso, Lupo) feel "correct" for a mob faction
2. They're easier to generate — just pick a surname from a list
3. Epithets require creative work — what WOULD the crew actually shout?

**The spec must say "NO SURNAMES" explicitly.** "Last names or epithets" is interpreted by sub-agents as "last names are fine." Ambiguity favors the easier path.

## Street-Fight Callout Test

Every Professional name must answer: what do the other hitters yell when this person walks into the Continental?

- "Hammer's here!" ✓ — everyone knows the guy with the ball-peen hammer
- "Ricci's here!" ✗ — nobody knows who that is
- "Ghost is on the job!" ✓ — the invisible hitter
- "Reyes is on the job!" ✗ — sounds like a cop

If the name could appear on a driver's license, it's wrong for a Professional.
