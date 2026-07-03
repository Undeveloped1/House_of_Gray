# Mechanics Synthesis Methodology

**When to use:** After multiple design passes produce different keyword ecosystems, and Joe wants to lock the core mechanics before designing cards.

## Process

1. **Load all passes.** Read every roster/brief/framework doc from previous passes. Don't trust memory — keyword definitions drift.

2. **Extract every keyword and named ability.** Build a master list. Include: keyword name, crew, definition, which passes use it.

3. **Count usage per keyword across all passes.** Programmatic tally preferred (execute_code with Python). Count every card that has, grants, or conditionally gains the ability. Flag cards that use the effect as text-only (not a keyword).

4. **Group by function.** Which keywords overlap mechanically? (Grit and Seasoned = survive→grow. Payback and Intimidation and Sucker Punch = "fighting me is bad.")

5. **Present tensions, not answers.** Format: tension name, the conflict, what's at stake. Let Joe decide.

6. **Joe calls winners.** One keyword wins per mechanical space. Renames are cheap. Consolidation is the goal.

7. **Lock the ecosystem in a spec document.** Output: keyword list with definitions, crew ownership, status (keyword / someday / universal).

8. **Then design cards.** Do not design during synthesis. This is a separate phase.

## Output Format

See `design/bruiser_revisions/Bruiser_Mechanics_Synthesis.md` for the canonical example (2026-05-27 session).

## Pitfalls

- Designing cards during synthesis. Stay in phase. Good card ideas that emerge get parked, not pursued.
- Presenting too many options. Group overlaps into tensions. Joe makes binary calls, not multi-axis evaluations.
- Skipping the usage count. Keywords on 1-2 cards are keyword-someday candidates, not locks. The count reveals this.
