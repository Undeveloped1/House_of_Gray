# Cascade Assessment — Cross-Model Comparison Methodology

How to read, compare, and extract actionable findings from multiple cascade test passes.

---

## The 2×2 Matrix

Four test cells across two axes: model (Opus vs Composer) × mode (TOTAL blind 33 vs PARTIAL fill OPEN slots).

| | TOTAL (blind 33) | PARTIAL (fill OPEN) |
|---|---|---|
| **Opus** | TEST_A — regression machinery | TEST_B — richest audit, dependency/CA/Pizzo surfacing |
| **Composer** | TEST_C — worst-case rarity drift | TEST_D — production floor proof |

---

## What to Look For (per test)

### TOTAL passes (A, C)

- Do HARD gates hold? (curve sums, crew columns, zero orphans)
- Do SOFT flags converge on the same issues? (support-light, CA cap, keyword thinness)
- Where do models diverge? (rarity: Opus U-heavy, Composer R-heavy)
- Are blind-pass legendaries parallel-universe fiction? (expected — they have no locked cards)
- Do cohesion lines emerge naturally from BUILD_FACTS alone?

### PARTIAL passes (B, D)

- Do fills slot into locked roster without breakage? (THE proof question)
- Are dependencies surfaced? (Signalman fork, Pizzo threshold)
- Does NEED discipline hold? (fills designed to [NEED], not slot count)
- Band-boundary audits — do fills respect crew/tone/function per band?
- Cohesion: do fill edges resolve to REAL locked card names?

---

## Cross-Model Drift Signals

| Signal | What it means |
|--------|---------------|
| **Same SOFT flags on both models** | Real structural tension, not model noise |
| **Rarity diverges (R12 vs R5)** | Spec needs a common minimum floor, not just ceilings |
| **SOFT count differs (6 vs 2)** | One model is surfacing more policy decisions (Pizzo, Signalman) — not finding more bugs |
| **Both produce parallel-universe legendaries** | TOTAL pass is regression smoke, not ship canon |

---

## What Each Cell Is For

| Cell | Use |
|------|-----|
| **A (Opus total)** | Reference machinery pass — balanced rarity drift, richest cohesion proof |
| **C (Composer total)** | Worst-case rarity drift regression — if this passes HARD, the spec is tight |
| **B (Opus partial)** | Richest audit — dependencies, Pizzo, CA cap, named web edges. Use for spec-stress |
| **D (Composer partial)** | Production floor — can a cheaper model fill OPEN slots without breaking? Yes. |

---

## 3V Band Head-to-Head

When comparing blind pass 3V bands (TEST_A, TEST_C) against the handcrafted LIVE web 3V:

1. **Tone split** — both blind passes hit 7/3 naturally. If handcrafted is 4/6, the band is inverted.
2. **Keyword density per card** — Opus splits effects (Hamstring=Hobble, Shakedown=tax). Composer merges (Collections Enforcer=Hobble+tax). Opus is cleaner.
3. **Common count** — Opus 5C, Composer 0C. Composer drifted because Δ math inflates upward without a common floor.
4. **Missing functions** — neither blind pass invented Recon (Valet's domain). Unique functions in the handcrafted roster that don't emerge naturally from BUILD_FACTS alone are worth examining.

---

## Key Rules That Emerged from 3V Comparison

### 3V-2: Rarity-gated keyword limit at low V
"At ≤3V, Common/Uncommon: one keyword OR one text rider. Rare: two keywords. Legendary: exempt."
Pit Fighter (Rare, Grit+Rampage) is the sanctioned exception.

### 3V-4: Tone tolerance
±2 SOFT flag, ±3 SOFT block (Joe-bless). Fix the band, not the tolerance.

### 3V-5: Stat shape field
Forced choice on frozen slot sheet: ATK-leaning | HP-leaning | balanced. Defaults by crew: Street=ATK, Hall/Dock=HP, Spread=balanced.

### 3V-6: "John Doe, not job title" naming rule
"Would you yell this name across a bar to get someone's attention?" Reject job-description names in Phase D batch review.

---

## Synthesis Review Doc Workflow

When the master review table (`CASCADE_VALIDATION_REVIEW_SYNTHESIS.md`) opens a sub-batch:

1. Read the full doc — the status header tells you what's open
2. Fill your reviewer column (Paul) with taste/canon takes
3. For P-rows: Agree / Modify / Reject / Defer with specific reasoning
4. For 3V-rows: these are design-taste calls — only you and Joe can answer them
5. The models (Opus, Composer, Cursor) can fill their columns but cannot determine canon
6. After Joe locks, Opus merges into cascade spec

---

*2026-05-28 — Created from the Bruiser 2×2 cascade validation run. Methodology extracted from TEST_A through TEST_D cross-model comparison.*
