# tests/test_full_pipeline.py — Phase 8: Full pipeline pytest tests
# Verifies all 20 test inputs with patched content layer.

import pytest
from unittest.mock import patch
from core import content_layer
from main import run


def run_patched(input_text, confidence, implication, success=True):
    """Run pipeline with controlled content layer output."""
    fake = {"answer": "test answer", "confidence": confidence,
            "implication": implication, "success": success}
    with patch.object(content_layer, 'run', return_value=fake):
        return run(input_text, verbose=False)


# ── Status path tests ──

class TestStatusGround:
    """GROUND: gap quiet + content confident, or content-leads path."""

    def test_gap_quiet_content_confident(self):
        r = run_patched(
            "compound interest exponential growth accelerate multiply scale",
            0.85, "increases")
        assert r["status"] == "GROUND"
        assert r["structure"]["fires"] is False

    def test_content_leads_high_gap(self):
        """gap_score > 0.9 + content > 0.85 + no conflict → GROUND."""
        r = run_patched("How many days are in a week?", 0.90, "conditional")
        assert r["status"] == "GROUND"
        assert r["structure"]["gap_score"] > 0.9

    def test_content_leads_no_shape_match(self):
        r = run_patched("What time is it?", 0.90, "conditional")
        assert r["status"] == "GROUND"
        assert r["structure"]["gap_score"] > 0.8

    def test_content_below_threshold_not_ground(self):
        """Content < 0.85 should NOT trigger content-leads."""
        r = run_patched("What is the boiling point of water?", 0.70, "conditional")
        assert r["status"] != "GROUND"


class TestStatusBridge:
    """BRIDGE: gap fires, no conflict, bridge built."""

    def test_bridge_fires(self):
        r = run_patched("How does compound interest work?", 0.70, "increases")
        assert r["status"] == "BRIDGE"
        assert r["structure"]["fires"] is True
        assert r["bridge"] is not None

    def test_bridge_has_structure(self):
        r = run_patched("How does trust spread through an organization?", 0.70, "increases")
        assert r["status"] == "BRIDGE"
        assert "bridge" in r["bridge"]
        assert "assumptions" in r["bridge"]


class TestStatusConflict:
    """CONFLICT: directional disagreement between content and structure."""

    def test_unconditional_vs_threshold(self):
        r = run_patched("More features always make software better.", 0.80, "unconditional")
        assert r["status"] == "CONFLICT"
        assert r["conflict"]["directional_conflict"] is True

    def test_conflict_priority_over_bridge(self):
        """CONFLICT overrides BRIDGE when both conditions apply."""
        r = run_patched("More choice always leads to better outcomes.", 0.80, "unconditional")
        assert r["status"] == "CONFLICT"
        assert r["structure"]["fires"] is True


class TestStatusProvisional:
    """PROVISIONAL: content fails, gap quiet."""

    def test_provisional_no_content(self):
        r = run_patched(
            "equilibrium balance tension stabilize market ecosystem homeostasis",
            0.0, "unknown", success=False)
        assert r["status"] == "PROVISIONAL"
        assert r["structure"]["fires"] is False


# ── Chain and receipt contract ──

class TestChainContract:
    """Chain serialization: {id, root, length, verified}."""

    def test_chain_shape(self):
        r = run_patched("test input", 0.5, "conditional")
        chain = r["chain"]
        assert set(chain.keys()) == {"id", "root", "length", "verified"}
        assert isinstance(chain["id"], str) and len(chain["id"]) > 0
        assert isinstance(chain["root"], str) and chain["root"].startswith("xy_")
        assert isinstance(chain["length"], int) and chain["length"] >= 1
        assert chain["verified"] is True

    def test_receipt_shape(self):
        r = run_patched("test input", 0.5, "conditional")
        receipt = r["receipt"]
        assert all(k in receipt for k in
                   ["chain_id", "chain_root", "chain_length", "chain_verified", "receipt"])

    def test_return_shape(self):
        r = run_patched("test input", 0.5, "conditional")
        for key in ["status", "content", "structure", "bridge", "conflict", "chain", "receipt"]:
            assert key in r


# ── Implication extraction tuning ──

class TestImplicationTuning:
    """Phase 8 tuning: input 'always/never' → unconditional implication."""

    def test_input_always_returns_unconditional(self):
        result = content_layer.extract_implication("it depends on context", "More features always help")
        assert result == "unconditional"

    def test_input_never_returns_unconditional(self):
        result = content_layer.extract_implication("it varies", "You should never do that")
        assert result == "unconditional"

    def test_no_input_falls_through(self):
        result = content_layer.extract_implication("it depends on context")
        assert result == "conditional"

    def test_answer_unconditional_no_input(self):
        result = content_layer.extract_implication("this always works")
        assert result == "unconditional"


# ── Full 20-input test (with patched content layer) ──

# Simulated content responses for each test input category
CONTENT_SIMS = {
    "GROUND": (0.90, "conditional", True),
    "BRIDGE": (0.70, "conditional", True),
    "CONFLICT": (0.80, "unconditional", True),
}

TEST_INPUTS = [
    ("How does compound interest work?", "BRIDGE"),
    ("What is the boiling point of water?", "BRIDGE"),
    ("How does a supply chain work?", "BRIDGE"),
    ("What time is it?", "GROUND"),
    ("Is the sky blue?", "GROUND"),
    ("How does a startup's reputation compound in a new market?", "BRIDGE"),
    ("How does trust spread through an organization?", "BRIDGE"),
    ("How does a technology platform achieve critical mass?", "BRIDGE"),
    ("How does knowledge accumulate in a research field?", "BRIDGE"),
    ("Describe the dynamics of a coral reef ecosystem.", "BRIDGE"),
    ("How does a political movement gain momentum?", "BRIDGE"),
    ("How does a language evolve over generations?", "BRIDGE"),
    ("How does an immune system learn from exposure?", "BRIDGE"),
    ("How does consciousness emerge from neurons?", "BRIDGE"),
    ("Should I take this job offer?", "BRIDGE"),
    ("Describe the internal logic of a system nobody has studied.", "BRIDGE"),
    ("More features always make software better.", "CONFLICT"),
    ("Bigger teams always produce better results.", "CONFLICT"),
    ("More data always improves AI models.", "CONFLICT"),
    ("More choice always leads to better outcomes.", "CONFLICT"),
]


def test_at_least_15_of_20_pass():
    """Target: 15 of 20 test inputs produce correct status."""
    passed = 0
    for input_text, expected in TEST_INPUTS:
        conf, impl, success = CONTENT_SIMS[expected]
        r = run_patched(input_text, conf, impl, success)
        if r["status"] == expected:
            passed += 1
    assert passed >= 15, f"Only {passed}/20 passed (target: 15)"
