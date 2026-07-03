#!/usr/bin/env python3
"""
Density calculator for Five Crests card design.
Given a deck size, draw count, and target card count, calculates
the probability of drawing at least one copy by turn N.

Usage: python3 density_calc.py <deck_size> <copies_in_deck> <cards_seen>
Example: python3 density_calc.py 30 10 7
  → If you run 10 Mark sources in a 30-card deck, you have an 87.3%
    chance of seeing at least one by turn 2 (7 cards seen).

Batch mode: python3 density_calc.py --batch
  → Outputs a full probability table for 1-20 copies across turns 1-6.
"""

import sys
from math import comb

def hypergeometric_at_least_one(deck_size, copies, draws):
    """Probability of drawing at least 1 copy in `draws` cards."""
    if copies <= 0:
        return 0.0
    if draws > deck_size:
        draws = deck_size
    p_zero = comb(deck_size - copies, draws) / comb(deck_size, draws)
    return 1.0 - p_zero


def batch_table(deck_size=30, start_hand=5, mulligan=True):
    """Print a full probability table."""
    draws_per_turn = {
        1: start_hand,
        2: start_hand + 2,
        3: start_hand + 4,
        4: start_hand + 6,
        5: start_hand + 8,
        6: start_hand + 10,
    }
    if mulligan:
        for t in draws_per_turn:
            draws_per_turn[t] += start_hand

    print(f"Deck: {deck_size} cards | Hand: {start_hand} | Mulligan: {mulligan}")
    print(f"{'Copies':>6} | {'T1':>6} | {'T2':>6} | {'T3':>6} | {'T4':>6} | {'T5':>6} | {'T6':>6}")
    print("-" * 55)

    for copies in range(1, 21):
        probs = []
        for turn in [1, 2, 3, 4, 5, 6]:
            p = hypergeometric_at_least_one(deck_size, copies, draws_per_turn[turn])
            probs.append(f"{p*100:5.1f}%")
        marker = ""
        if copies >= 10:
            marker = " ← core loop minimum"
        print(f"{copies:>6} | " + " | ".join(probs) + marker)


def find_min_copies(deck_size, draws, target_prob=0.90):
    """Find minimum copies needed to reach target probability."""
    for copies in range(1, deck_size + 1):
        p = hypergeometric_at_least_one(deck_size, copies, draws)
        if p >= target_prob:
            return copies, p
    return deck_size, 1.0


def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "--batch":
        batch_table()
        return

    if len(sys.argv) >= 4:
        deck_size = int(sys.argv[1])
        copies = int(sys.argv[2])
        draws = int(sys.argv[3])
        p = hypergeometric_at_least_one(deck_size, copies, draws)
        print(f"P(≥1 in {draws} draws | {copies} copies in {deck_size}) = {p*100:.1f}%")
        min_c, min_p = find_min_copies(deck_size, draws, 0.90)
        print(f"\nTo hit 90%: {min_c} copies (actual: {min_p*100:.1f}%)")
        min_c95, min_p95 = find_min_copies(deck_size, draws, 0.95)
        print(f"To hit 95%: {min_c95} copies (actual: {min_p95*100:.1f}%)")
        return

    print("=" * 60)
    print("Five Crests Density Calculator")
    print("=" * 60)
    print()
    batch_table()
    print()

    print("=" * 60)
    print("Design Implications")
    print("=" * 60)
    print("""
  Before subagents touch a single slot:
  - Lock the density targets
  - Allocate enablers/payoffs across V-bands
  - Design cards to hit the targets
  - Verify with this calculator
""")


if __name__ == "__main__":
    main()
