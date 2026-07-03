# Trigger — Full Pipeline Case Study (v2 → v6, 2026-06-07)

**Final set:** `/root/.hermes/docs/Paul/workspace/Trigger_Full_Set_v6_2026-06-07_Paul.md`
**Synergy web:** `/root/.hermes/docs/Paul/workspace/Trigger_Synergy_Web_Warmup_2026-06-06_Paul.md`

## Score Progression

| Version | Score | What Changed |
|---------|-------|-------------|
| v2 | C− | Initial build. 5 criticals. |
| v3 | B | Keyword sidebar, Locked On 2→6, Contract Scaling 3→6, Cage redesign, Il Trio nerf, heroes reworked |
| v4 | B+ | Contract auto-cycling, Locked On 6 three-tier, healing, Cage/Il Trio curve swap, Car Bomb fix |
| v5 | B+ | Locked On→Overkill rename, Loader added (E08→2), Settled added, Bearcat Overkill 2, edge audit restored |
| v6 | A | The Professional (thesis card), Numbers Runner (deck-peek trick), Francis Cage (text-theft), Excessive Force (Paid doubles on Overkill 6), Settled unconditional |

Two letter grades across four iterations. C− → A.

## Key Learnings (Updated)

1. **pre_review_audit.py catches everything mechanical.** v2 would have failed 6+ checks. Running it first eliminates one full review cycle.

2. **Automated gate before critic. Always.** Script catches counts, rarity, keywords, edges, curve, blind spots, removal, vanillas, healing, naming conflicts. Critic only sees sets that pass.

3. **Phonetic collision is real.** "Paid" + "Payoff" = draft confusion. "Reload" keyword + "Reload" spell = naming conflict. Check new names against ALL existing keywords.

4. **Keyword name swap is a valid pattern.** Overkill (trample) → Overkill (Trigger mechanic) + Blast (trample). Repurpose good words rather than invent new ones.

5. **A-tier = memorable moments.** The Professional, Francis Cage text-theft, Numbers Runner deck-peek — these create stories. The mechanical skeleton got the set to B+. The moments got it to A.

6. **Naming: curated > comprehensive.** Joe wants 2-5 picks with reasoning, not dictionaries. See creative-collaboration skill § Dictionary Pitfall.
