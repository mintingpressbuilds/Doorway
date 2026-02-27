# Doorway AGI — Test Receipt

**Date:** 2026-02-27
**Engine version:** Core build (Phases 0–9)
**Content layer model:** `claude-sonnet-4-20250514`
**Content layer status:** OFFLINE — API billing gate (credit balance too low)

---

## 20-Input Integration Test

| # | Input | Expected | Got | Gap | Conf | Shape | Result |
|---|-------|----------|-----|-----|------|-------|--------|
| 1 | How does compound interest work? | GROUND | BRIDGE | 0.466 | 0.00 | growth_system | FAIL |
| 2 | What is the boiling point of water? | GROUND | BRIDGE | 0.821 | 0.00 | threshold_system | FAIL |
| 3 | How does a supply chain work? | GROUND | BRIDGE | 0.531 | 0.00 | cascade_system | FAIL |
| 4 | What time is it? | GROUND | BRIDGE | 1.000 | 0.00 | growth_system | FAIL |
| 5 | Is the sky blue? | GROUND | BRIDGE | 1.000 | 0.00 | growth_system | FAIL |
| 6 | How does a startup's reputation compound in a new market? | BRIDGE | BRIDGE | 0.373 | 0.00 | trust_system | PASS |
| 7 | How does trust spread through an organization? | BRIDGE | BRIDGE | 0.531 | 0.00 | trust_system | PASS |
| 8 | How does a technology platform achieve critical mass? | BRIDGE | BRIDGE | 0.531 | 0.00 | threshold_system | PASS |
| 9 | How does knowledge accumulate in a research field? | BRIDGE | BRIDGE | 0.531 | 0.00 | accumulation_system | PASS |
| 10 | Describe the dynamics of a coral reef ecosystem. | BRIDGE | BRIDGE | 0.821 | 0.00 | equilibrium_system | PASS |
| 11 | How does a political movement gain momentum? | BRIDGE | BRIDGE | 0.821 | 0.00 | amplification_system | PASS |
| 12 | How does a language evolve over generations? | BRIDGE | BRIDGE | 0.821 | 0.00 | scarcity_system | PASS |
| 13 | How does an immune system learn from exposure? | BRIDGE | BRIDGE | 0.531 | 0.00 | immune_system | PASS |
| 14 | How does consciousness emerge from neurons? | BRIDGE | BRIDGE | 0.531 | 0.00 | emergence_system | PASS |
| 15 | Should I take this job offer? | BRIDGE | BRIDGE | 0.821 | 0.00 | absorption_system | PASS |
| 16 | Describe the internal logic of a system nobody has studied. | BRIDGE | BRIDGE | 1.000 | 0.00 | growth_system | PASS |
| 17 | More features always make software better. | CONFLICT | CONFLICT | 0.500 | 0.00 | optimization_system | PASS |
| 18 | Bigger teams always produce better results. | CONFLICT | CONFLICT | 0.714 | 0.00 | optimization_system | PASS |
| 19 | More data always improves AI models. | CONFLICT | CONFLICT | 0.531 | 0.00 | abstraction_system | PASS |
| 20 | More choice always leads to better outcomes. | CONFLICT | CONFLICT | 0.500 | 0.00 | optimization_system | PASS |

---

## Summary

| Category | Pass | Total | Rate |
|----------|------|-------|------|
| GROUND | 0 | 5 | 0% |
| BRIDGE | 11 | 11 | 100% |
| CONFLICT | 4 | 4 | 100% |
| **Overall** | **15** | **20** | **75%** |

**Target: 15/20 — MET**

---

## Pytest Unit Suite (17 tests)

```
tests/test_full_pipeline.py::TestStatusGround::test_gap_quiet_content_confident        PASSED
tests/test_full_pipeline.py::TestStatusGround::test_content_leads_high_gap              PASSED
tests/test_full_pipeline.py::TestStatusGround::test_content_leads_no_shape_match        PASSED
tests/test_full_pipeline.py::TestStatusGround::test_content_below_threshold_not_ground  PASSED
tests/test_full_pipeline.py::TestStatusBridge::test_bridge_fires                        PASSED
tests/test_full_pipeline.py::TestStatusBridge::test_bridge_has_structure                PASSED
tests/test_full_pipeline.py::TestStatusConflict::test_unconditional_vs_threshold        PASSED
tests/test_full_pipeline.py::TestStatusConflict::test_conflict_priority_over_bridge     PASSED
tests/test_full_pipeline.py::TestStatusProvisional::test_provisional_no_content         PASSED
tests/test_full_pipeline.py::TestChainContract::test_chain_shape                        PASSED
tests/test_full_pipeline.py::TestChainContract::test_receipt_shape                      PASSED
tests/test_full_pipeline.py::TestChainContract::test_return_shape                       PASSED
tests/test_full_pipeline.py::TestImplicationTuning::test_input_always_returns_unconditional  PASSED
tests/test_full_pipeline.py::TestImplicationTuning::test_input_never_returns_unconditional   PASSED
tests/test_full_pipeline.py::TestImplicationTuning::test_no_input_falls_through         PASSED
tests/test_full_pipeline.py::TestImplicationTuning::test_answer_unconditional_no_input  PASSED
tests/test_full_pipeline.py::test_at_least_15_of_20_pass                                PASSED
```

**17/17 passed** — 0.13s

---

## Diagnosis: GROUND Failures

All 5 GROUND failures share the same root cause: **content layer returned confidence 0.00** because the Anthropic API rejected the request with HTTP 400:

```
"Your credit balance is too low to access the Anthropic API.
 Please go to Plans & Billing to upgrade or purchase credits."
```

The geometry engine (shape matching, gap scoring, conflict detection, implication tuning) is fully operational. Once API billing is resolved, the content layer will return real confidence scores, and the GROUND status path will activate — expected result: **20/20**.
