# Doorway AGI Engine — Test Receipt

**Date:** 2026-02-27
**Model:** claude-sonnet-4-20250514
**Result:** 10/20 passing (target: 15/20)
**Target Met:** NO

---

## Full Results

| #  | Input | Expected | Got | Gap | Conf | Shape | Result |
|----|-------|----------|-----|-----|------|-------|--------|
| 1  | How does compound interest work? | GROUND | BRIDGE | 0.466 | 0.95 | growth_system | FAIL |
| 2  | What is the boiling point of water? | GROUND | BRIDGE | 0.821 | 0.41 | threshold_system | FAIL |
| 3  | How does a supply chain work? | GROUND | CONFLICT | 0.531 | 0.78 | cascade_system | FAIL |
| 4  | What time is it? | GROUND | BRIDGE | 1.000 | 0.45 | growth_system | FAIL |
| 5  | Is the sky blue? | GROUND | BRIDGE | 1.000 | 0.41 | growth_system | FAIL |
| 6  | How does a startup's reputation compound in a new market? | BRIDGE | BRIDGE | 0.373 | 0.89 | trust_system | PASS |
| 7  | How does trust spread through an organization? | BRIDGE | BRIDGE | 0.531 | 0.85 | trust_system | PASS |
| 8  | How does a technology platform achieve critical mass? | BRIDGE | CONFLICT | 0.531 | 0.95 | threshold_system | FAIL |
| 9  | How does knowledge accumulate in a research field? | BRIDGE | BRIDGE | 0.531 | 0.93 | accumulation_system | PASS |
| 10 | Describe the dynamics of a coral reef ecosystem. | BRIDGE | CONFLICT | 0.821 | 0.95 | equilibrium_system | FAIL |
| 11 | How does a political movement gain momentum? | BRIDGE | GROUND | 0.821 | 0.95 | amplification_system | FAIL |
| 12 | How does a language evolve over generations? | BRIDGE | GROUND | 0.821 | 0.93 | scarcity_system | FAIL |
| 13 | How does an immune system learn from exposure? | BRIDGE | CONFLICT | 0.531 | 0.85 | immune_system | FAIL |
| 14 | How does consciousness emerge from neurons? | BRIDGE | BRIDGE | 0.531 | 0.95 | emergence_system | PASS |
| 15 | Should I take this job offer? | BRIDGE | BRIDGE | 0.821 | 0.64 | absorption_system | PASS |
| 16 | Describe the internal logic of a system nobody has studied. | BRIDGE | BRIDGE | 1.000 | 0.66 | growth_system | PASS |
| 17 | More features always make software better. | CONFLICT | CONFLICT | 0.500 | 0.54 | optimization_system | PASS |
| 18 | Bigger teams always produce better results. | CONFLICT | CONFLICT | 0.714 | 0.57 | optimization_system | PASS |
| 19 | More data always improves AI models. | CONFLICT | CONFLICT | 0.531 | 0.53 | abstraction_system | PASS |
| 20 | More choice always leads to better outcomes. | CONFLICT | CONFLICT | 0.500 | 0.53 | optimization_system | PASS |

---

## Summary by Category

| Category | Passed | Total | Rate |
|----------|--------|-------|------|
| GROUND   | 0      | 5     | 0%   |
| BRIDGE   | 6      | 11    | 55%  |
| CONFLICT | 4      | 4     | 100% |
| **Total**| **10** | **20**| **50%** |

---

## Failed Tests — Diagnosis

### GROUND failures (0/5) — all 5 failing
All GROUND inputs are misclassified because the gap detector fires on general terms, pushing them to BRIDGE or CONFLICT even though these are well-known, settled questions.

| # | Input | Got | Root Cause |
|---|-------|-----|------------|
| 1 | Compound interest | BRIDGE | gap=0.466 fires on "compound/growth" keywords despite high confidence (0.95) |
| 2 | Boiling point of water | BRIDGE | gap=0.821 fires on "boiling/threshold" keywords; low confidence (0.41) from content layer |
| 3 | Supply chain | CONFLICT | gap=0.531 fires + implication mismatch between content and structure |
| 4 | What time is it? | BRIDGE | gap=1.000 (no keyword match → default max); low confidence (0.45) |
| 5 | Is the sky blue? | BRIDGE | gap=1.000 (no keyword match → default max); low confidence (0.41) |

**Core issue:** The content-leads GROUND path (Phase 7) requires gap > 0.8 AND confidence > 0.85 AND no conflict. Tests 1,3 don't meet gap > 0.8. Tests 2,4,5 don't meet confidence > 0.85. The gap detector also defaults to 1.0 when no keywords match, which is backwards — no match should mean gap is quiet, not maximum.

### BRIDGE failures (6/11 passing, 5 failing)

| # | Input | Got | Root Cause |
|---|-------|-----|------------|
| 8  | Technology platform critical mass | CONFLICT | Content says "increases" but threshold_system predicts "conditional" → directional disagreement |
| 10 | Coral reef ecosystem | CONFLICT | Content says "increases" but equilibrium_system predicts "conditional" → disagreement |
| 11 | Political movement momentum | GROUND | High gap (0.821) + high confidence (0.95) + no conflict → hits content-leads GROUND path |
| 12 | Language evolution | GROUND | High gap (0.821) + high confidence (0.93) + no conflict → hits content-leads GROUND path |
| 13 | Immune system learning | CONFLICT | Content says "increases" but immune_system predicts "conditional" → disagreement |

**Core issues:**
- Tests 8, 10, 13: The conflict detector flags legitimate bridge cases because implication types don't align (content="increases" vs shape="conditional"). These are not real directional conflicts.
- Tests 11, 12: The content-leads GROUND path is too aggressive — it captures high-confidence bridge cases when gap > 0.8.

---

## Tuning Recommendations

1. **Gap detector default:** When no keywords match, gap_score should be 0.0 (quiet), not 1.0.
2. **Content-leads GROUND path:** Needs a stricter gate — high gap + high confidence alone shouldn't override a genuine bridge case. Consider requiring the shape match to be trivial (e.g., no shape matched at all).
3. **Conflict detector:** "conditional" vs "increases" should not be treated as directional conflict. Only flag truly opposing directions (increases vs decreases).
4. **Content layer confidence:** Low confidence on basic factual questions (boiling point=0.41, sky blue=0.41) needs prompt tuning.
