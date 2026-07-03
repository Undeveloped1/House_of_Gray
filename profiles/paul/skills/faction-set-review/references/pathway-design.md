# Pathway Design & Crew Identity Profiles

**Phase:** Between Synergy Web and Slot Table. Slot filling establishes boundaries. Pathway building determines what goes in the box and why.

## Core Principle

**Slot filling = the box.** "This 3V Professional slot can be Mark, Paid, Cloak, or Intel. Stats fall within this curve band."

**Pathway building = what goes in the box and why.** "The Contract pathway needs a Mark source at 2V so it's online by turn 3. It needs a kill effect at 3V. It needs a Paid payoff at 4V. These three cards are a T2→T3→T4 sequence."

## Crew Identity Profiles

Each crew is a mini-faction. Every card filtered through faction AND crew blind spots.

| Crew | Job | Owns | Cannot Do | % |
|------|-----|------|-----------|---|
| Management | Control flow. Initiate work, intel, disrupt. | Mark, Intel, Silence, Contract scaling | Kill minions. Carry weapons. Fight. | 10% |
| Professionals | Execute work. Complete Contracts, carry weapons, collect. | Paid, Armed, Contract completion, removal | Initiate Contracts. Disrupt (Silence is Court). | 50% |
| Street | Feed engine. Pressure, soften targets, tempo. | Hustle, combat damage, kill rewards | Complete Contracts (Paid). Draw cards. Disrupt. | 20% |
| Help | Enable Arsenal. Maintain weapons, reload, supply. | Reload, weapon support, durability | Fire guns. Draw cards. Initiate or complete Contracts. | 20% |

## Pathway Definition + Density Targets

| Pathway | What It Does | % of 55 |
|---------|-------------|---------|
| The Contract | Mark → Complete → Paid | 55-60% |
| The Arsenal | Weapons and ammo management | 20-25% |
| The Court | Silence disruption + intel | 10-15% |

## Archetype Turn Map

| Turn | Contract | Arsenal |
|------|----------|---------|
| T1 | Hustle 1-drop | Equip weapon |
| T2 | Mark target | Armed body |
| T3 | Kill → Paid fires | Reload / Special Ammo |
| T4 | Second cycle + Scaling | Weapon payoff |
| T5 | Cascade / legendary | Carlo's Piece |

Work backwards: "If Paid fires T3, need X Mark sources at 1-2V and Y kill effects at 3V."

## Density Calculator

`python3 tools/density_calc.py` — Hypergeometric distribution. Before any card: "I need a Mark source by Turn 2 in 30-card deck with mulligan" → "6 copies for 90% draw consistency." Answers "how many" before "what does it do."

## Daily Life Context

If you know Management routes three phones, codes death in newspaper columns, has never met a Hitter, and doesn't carry a gun — you cannot give a Management card "Armed" or "deal 2 damage." Daily Life docs prevent lazy crew assumptions.
