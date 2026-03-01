# tests/test_shape_growth.py — Tests for shape library growth components
# Covers: bridge_builder additions, confirmation, bridge_history,
# tier2_emergence, and pipeline wiring.

import pytest
from unittest.mock import patch, MagicMock
from doorway.core import gap_detector, bridge_builder, content_layer
from doorway.core.shape_library import get_all_shapes
from doorway.core.shape_library_loader import load_full_library
from doorway.core.confirmation import (
    confirm, extract_geometry, _is_duplicate, _infer_implication_type
)
from doorway.core.bridge_history import save_bridge, load_bridge_history
from doorway.core.tier2_emergence import emerge_tier2
from doorway.main import run


# ── Bridge Builder: target_domain + gap_dims ──

class TestBridgeBuilderAdditions:

    def test_bridge_includes_target_domain(self):
        gap_result = gap_detector.run("How does trust spread through an organization?")
        bridge = bridge_builder.build(gap_result, input_text="How does trust spread through an organization?")
        assert "target_domain" in bridge
        assert bridge["target_domain"] != "unknown_domain"
        assert bridge["target_domain"].endswith("_system")

    def test_bridge_includes_gap_dims(self):
        gap_result = gap_detector.run("How does compound interest work?")
        bridge = bridge_builder.build(gap_result, input_text="How does compound interest work?")
        assert "gap_dims" in bridge
        assert isinstance(bridge["gap_dims"], dict)
        assert len(bridge["gap_dims"]) > 0

    def test_bridge_includes_shape_name(self):
        gap_result = gap_detector.run("How does trust spread?")
        bridge = bridge_builder.build(gap_result, input_text="How does trust spread?")
        assert "shape_name" in bridge
        assert bridge["shape_name"] == gap_result["closest_shape"]

    def test_bridge_includes_gap_score(self):
        gap_result = gap_detector.run("How does trust spread?")
        bridge = bridge_builder.build(gap_result, input_text="How does trust spread?")
        assert "gap_score" in bridge
        assert bridge["gap_score"] == gap_result["gap_score"]

    def test_bridge_without_input_text(self):
        gap_result = gap_detector.run("How does compound interest work?")
        bridge = bridge_builder.build(gap_result)
        assert bridge["target_domain"] == "unknown_domain"

    def test_target_domain_extraction(self):
        domain = bridge_builder.extract_target_domain(
            "How does quantum error correction work?")
        assert "quantum" in domain
        assert domain.endswith("_system")

    def test_target_domain_extraction_empty(self):
        assert bridge_builder.extract_target_domain("") == "unknown_domain"

    def test_existing_bridge_fields_unchanged(self):
        """Existing fields must still be present and correct."""
        gap_result = gap_detector.run("How does trust spread?")
        bridge = bridge_builder.build(gap_result, input_text="How does trust spread?")
        assert "bridge" in bridge
        assert "assumptions" in bridge
        assert "confidence" in bridge
        assert "status" in bridge
        assert bridge["status"] == "provisional"
        assert "geometric_prediction" in bridge
        assert "implication_type" in bridge


# ── extract_geometry ──

class TestExtractGeometry:

    def test_produces_new_shape(self):
        bridge = _make_bridge("trust_system", "startup_reputation_system",
                              gap_dims={"transferability": "local_to_universal",
                                        "fragility": "robust_to_fragile"})
        shape = extract_geometry(bridge)
        assert shape is not None
        assert shape["name"] == "startup_reputation_system"
        assert shape["tier"] == 1
        assert shape["confirmed_via"] == "trust_system"

    def test_implication_type_not_copied_from_source(self):
        """B's implication_type must be derived from B, not from source."""
        bridge = _make_bridge(
            "hierarchy_system", "quantum_error_correction_system",
            gap_dims={"rigidity": "flexible_to_rigid"},
            input_text="How does quantum error correction maintain coherence against decoherence?")
        shape = extract_geometry(bridge)
        # hierarchy_system is "conditional" but input has threshold signals
        # (coherence, decoherence)
        assert shape["implication_type"] == "threshold"

    def test_returns_none_for_unknown_domain(self):
        bridge = _make_bridge("trust_system", "unknown_domain")
        assert extract_geometry(bridge) is None

    def test_elements_are_structural_components(self):
        bridge = _make_bridge(
            "growth_system", "coral_reef_dynamics_system",
            gap_dims={"rate": "slow_to_fast"},
            input_text="Describe the dynamics of a coral reef ecosystem")
        shape = extract_geometry(bridge)
        # Elements must be structural components, not empty
        assert len(shape["elements"]) >= 3
        # Elements should not just be the source shape's elements
        from doorway.core.shape_library import get_shape
        source = get_shape("growth_system")
        assert set(shape["elements"]) != set(source["elements"])

    def test_color_dims_present(self):
        dims = {"stability": "fragile_to_resilient"}
        bridge = _make_bridge("equilibrium_system", "market_pricing_system",
                              gap_dims=dims)
        shape = extract_geometry(bridge)
        assert isinstance(shape["color_dims"], dict)
        assert len(shape["color_dims"]) >= 1


# ── extract_geometry: hierarchy → quantum (growth doc example) ──

class TestExtractGeometryQuantum:
    """
    Verify the growth doc example: hierarchy_system bridges to quantum
    error correction. What enters the library must describe quantum
    computing geometry, NOT hierarchy geometry.
    """

    def _run_quantum_bridge(self):
        from doorway.core.shape_library import get_shape
        h = get_shape("hierarchy_system")
        gap_result = gap_detector.run(
            "How does quantum error correction maintain coherence "
            "against decoherence using redundant qubit encoding?")
        gap_result = dict(gap_result)
        gap_result["closest_shape"] = "hierarchy_system"
        gap_result["geometric_prediction"] = h["geometric_prediction"]
        gap_result["implication_type"] = h["implication_type"]
        bridge = bridge_builder.build(
            gap_result,
            input_text="How does quantum error correction maintain coherence "
                       "against decoherence using redundant qubit encoding?")
        return extract_geometry(bridge), h

    def test_structure_describes_quantum_not_hierarchy(self):
        shape, h = self._run_quantum_bridge()
        # Must NOT contain hierarchy_system's structure
        assert "nested layers of authority" not in shape["structure"]
        assert "dependency flowing downward" not in shape["structure"]
        # Must contain quantum-related terms
        structure_lower = shape["structure"].lower()
        assert "quantum" in structure_lower

    def test_implication_type_is_threshold_not_conditional(self):
        shape, h = self._run_quantum_bridge()
        # hierarchy_system is "conditional"
        assert h["implication_type"] == "conditional"
        # B should be "threshold" (coherence/decoherence signals)
        assert shape["implication_type"] == "threshold"

    def test_elements_are_quantum_not_hierarchy(self):
        shape, h = self._run_quantum_bridge()
        hierarchy_elements = set(h["elements"])
        quantum_elements = set(shape["elements"])
        # Zero overlap with hierarchy elements
        assert hierarchy_elements & quantum_elements == set()
        # Must have structural components (at least 3)
        assert len(quantum_elements) >= 3
        # The combined element text should reference quantum concepts,
        # not hierarchy concepts like "apex", "layers", "enforcement"
        all_elem_text = " ".join(quantum_elements).lower()
        assert not any(w in all_elem_text for w in ["apex", "layers", "enforcement"])

    def test_confirmed_via_is_hierarchy(self):
        shape, _ = self._run_quantum_bridge()
        assert shape["confirmed_via"] == "hierarchy_system"

    def test_name_reflects_target_domain(self):
        shape, _ = self._run_quantum_bridge()
        assert "quantum" in shape["name"]
        assert shape["name"].endswith("_system")


# ── Confirmation ──

class TestConfirmation:

    def test_confirm_adds_to_library(self):
        library = dict(get_all_shapes())
        initial_count = len(library)
        bridge = _make_bridge("trust_system", "startup_reputation_system",
                              gap_dims={"transferability": "local_to_universal",
                                        "fragility": "robust_to_fragile"})
        result = confirm(bridge, library)
        assert result is not None
        assert len(library) == initial_count + 1
        assert "startup_reputation_system" in library

    def test_confirm_deduplicates(self):
        library = dict(get_all_shapes())
        bridge = _make_bridge("trust_system", "startup_reputation_system",
                              gap_dims={"transferability": "local_to_universal"})
        confirm(bridge, library)
        count_after_first = len(library)
        result = confirm(bridge, library)
        assert result is None
        assert len(library) == count_after_first

    def test_confirm_rejects_low_gap(self):
        library = dict(get_all_shapes())
        bridge = _make_bridge("trust_system", "test_system", gap_score=0.1)
        result = confirm(bridge, library)
        assert result is None

    def test_confirm_rejects_non_provisional(self):
        library = dict(get_all_shapes())
        bridge = _make_bridge("trust_system", "test_system")
        bridge["status"] = "confirmed"
        result = confirm(bridge, library)
        assert result is None

    def test_confirm_writes_to_supabase(self):
        library = dict(get_all_shapes())
        mock_sb = MagicMock()
        mock_sb.table.return_value.upsert.return_value.execute.return_value = None
        bridge = _make_bridge("trust_system", "unique_test_domain_system",
                              gap_dims={"axis": "low_to_high"})
        result = confirm(bridge, library, supabase_client=mock_sb)
        assert result is not None
        mock_sb.table.assert_called_with("confirmed_shapes")

    def test_confirmed_shape_has_library_fields(self):
        """Shape added to library must have all fields the gap detector needs."""
        library = dict(get_all_shapes())
        bridge = _make_bridge("growth_system", "viral_adoption_system",
                              gap_dims={"rate": "slow_to_fast"})
        confirm(bridge, library)
        shape = library["viral_adoption_system"]
        for field in ["structure", "elements", "keywords_tier1", "keywords_tier2",
                       "geometric_prediction", "implication_type", "color_dimensions"]:
            assert field in shape, f"Missing field: {field}"


# ── _infer_implication_type ──

class TestInferImplicationType:

    def test_threshold_signals(self):
        assert _infer_implication_type(
            "coherence against decoherence below error threshold",
            {"threshold_proximity": "near", "capacity": "critical"},
        ) == "threshold"

    def test_increase_signals(self):
        assert _infer_implication_type(
            "compounding accumulation exponential growth",
            {"rate": "fast"},
        ) == "increases"

    def test_decrease_signals(self):
        assert _infer_implication_type(
            "radioactive decay and depletion over time",
            {"half_life": "short"},
        ) == "decreases"

    def test_default_conditional(self):
        assert _infer_implication_type(
            "some relationship between variables",
            {"axis": "low_to_high"},
        ) == "conditional"


# ── Bridge History ──

class TestBridgeHistory:

    def test_save_returns_none_without_client(self):
        bridge = _make_bridge("trust_system", "test_system")
        assert save_bridge(bridge, user_id="user1") is None

    def test_save_with_client(self):
        mock_sb = MagicMock()
        mock_sb.table.return_value.insert.return_value.execute.return_value = MagicMock(data=[{}])
        bridge = _make_bridge("trust_system", "test_system")
        result = save_bridge(bridge, user_id="user1", supabase_client=mock_sb)
        assert result is not None
        mock_sb.table.assert_called_with("bridge_history")

    def test_load_returns_empty_without_client(self):
        assert load_bridge_history("user1") == []

    def test_load_with_client(self):
        mock_sb = MagicMock()
        mock_sb.table.return_value.select.return_value.eq.return_value \
            .order.return_value.limit.return_value.execute.return_value = \
            MagicMock(data=[{"source_shape": "trust_system"}])
        result = load_bridge_history("user1", supabase_client=mock_sb)
        assert len(result) == 1


# ── Tier 2 Emergence ──

class TestTier2Emergence:

    def test_no_emergence_with_few_bridges(self):
        result = emerge_tier2([], {})
        assert result["emergence_detected"] is False

    def test_no_emergence_below_threshold(self):
        history = [
            _make_history_record("trust_system", "domain_a_system"),
            _make_history_record("trust_system", "domain_b_system"),
        ]
        result = emerge_tier2(history, dict(get_all_shapes()))
        assert result["emergence_detected"] is False

    def test_emergence_with_cross_domain(self):
        history = [
            _make_history_record("trust_system", "domain_a_system", confidence=0.6),
            _make_history_record("trust_system", "domain_b_system", confidence=0.6),
            _make_history_record("trust_system", "domain_c_system", confidence=0.6),
        ]
        library = dict(get_all_shapes())
        result = emerge_tier2(history, library)
        assert result["emergence_detected"] is True
        assert len(result["new_shapes"]) == 1
        tier2_name = result["new_shapes"][0]["name"]
        assert tier2_name.startswith("tier2_")
        assert tier2_name in library

    def test_emergence_no_duplicate(self):
        history = [
            _make_history_record("trust_system", "domain_a_system", confidence=0.6),
            _make_history_record("trust_system", "domain_b_system", confidence=0.6),
            _make_history_record("trust_system", "domain_c_system", confidence=0.6),
        ]
        library = dict(get_all_shapes())
        emerge_tier2(history, library)
        result2 = emerge_tier2(history, library)
        assert result2["emergence_detected"] is False

    def test_emergence_writes_to_supabase(self):
        mock_sb = MagicMock()
        mock_sb.table.return_value.upsert.return_value.execute.return_value = None
        history = [
            _make_history_record("growth_system", "domain_x_system", confidence=0.6),
            _make_history_record("growth_system", "domain_y_system", confidence=0.6),
            _make_history_record("growth_system", "domain_z_system", confidence=0.6),
        ]
        library = dict(get_all_shapes())
        emerge_tier2(history, library, supabase_client=mock_sb)
        mock_sb.table.assert_called_with("confirmed_shapes")


# ── Loader ──

class TestShapeLibraryLoader:

    def test_load_static_only(self):
        library = load_full_library()
        assert len(library) == 50

    def test_load_with_supabase(self):
        mock_sb = MagicMock()
        mock_sb.table.return_value.select.return_value.eq.return_value \
            .execute.return_value = MagicMock(data=[{
                "name": "confirmed_test_system",
                "structure": "test structure",
                "elements": ["a", "b"],
                "keywords_tier1": ["test"],
                "keywords_tier2": ["test2"],
                "geometric_prediction": "test prediction",
                "implication_type": "conditional",
                "color_dims": {"axis": "low_to_high"},
                "confirmed_via": "trust_system",
                "gap_at_confirmation": 0.5,
            }])
        library = load_full_library(supabase_client=mock_sb)
        assert len(library) == 51
        assert "confirmed_test_system" in library
        assert library["confirmed_test_system"]["_confirmed"] is True

    def test_load_degrades_on_error(self):
        mock_sb = MagicMock()
        mock_sb.table.return_value.select.return_value.eq.return_value \
            .execute.side_effect = Exception("connection failed")
        library = load_full_library(supabase_client=mock_sb)
        assert len(library) == 50


# ── Gap Detector with shape_library ──

class TestGapDetectorLibraryParam:

    def test_default_uses_static(self):
        result = gap_detector.run("How does compound interest work?")
        assert "closest_shape" in result

    def test_custom_library(self):
        library = dict(get_all_shapes())
        result = gap_detector.run("How does compound interest work?",
                                  shape_library=library)
        assert result["closest_shape"] == "growth_system"

    def test_confirmed_shape_found(self):
        library = dict(get_all_shapes())
        library["quantum_error_correction_system"] = {
            "structure": "redundant encoding distributes information",
            "elements": ["redundancy", "entanglement", "error_detection"],
            "keywords_tier1": ["quantum", "qubit", "decoherence", "logical"],
            "keywords_tier2": ["fault", "tolerance", "coherence", "syndrome",
                               "correction", "encoding", "threshold", "stabilizer"],
            "geometric_prediction": "coherence maintained below threshold",
            "implication_type": "threshold",
            "color_dimensions": {},
            "analogs": [],
            "constraints": [],
        }
        result = gap_detector.run(
            "quantum qubit decoherence logical fault tolerance coherence",
            shape_library=library)
        assert result["closest_shape"] == "quantum_error_correction_system"


# ── Pipeline Integration ──

class TestPipelineIntegration:

    def test_pipeline_without_growth_unchanged(self):
        """Calling run() without shape_library works exactly as before."""
        fake = {"answer": "test", "confidence": 0.70,
                "implication": "increases", "success": True}
        with patch.object(content_layer, 'run', return_value=fake):
            r = run("How does compound interest work?", verbose=False)
        assert r["status"] in ("GROUND", "BRIDGE", "CONFLICT", "PROVISIONAL")
        for key in ["status", "content", "structure", "bridge",
                     "conflict", "chain", "receipt"]:
            assert key in r

    def test_pipeline_with_library_grows(self):
        """When shape_library is provided, confirmation adds to it."""
        library = dict(get_all_shapes())
        history = []
        initial = len(library)
        fake = {"answer": "trust compounds over time", "confidence": 0.70,
                "implication": "increases", "success": True}
        with patch.object(content_layer, 'run', return_value=fake):
            r = run("How does trust spread through an organization?",
                    verbose=False, shape_library=library,
                    bridge_history=history)
        if r["status"] == "BRIDGE":
            assert len(library) >= initial + 1
            assert len(history) == 1

    def test_pipeline_conflict_no_confirmation(self):
        """CONFLICT status should NOT trigger confirmation."""
        library = dict(get_all_shapes())
        history = []
        initial = len(library)
        fake = {"answer": "always true", "confidence": 0.80,
                "implication": "unconditional", "success": True}
        with patch.object(content_layer, 'run', return_value=fake):
            r = run("More features always make software better.",
                    verbose=False, shape_library=library,
                    bridge_history=history)
        assert r["status"] == "CONFLICT"
        assert len(library) == initial

    def test_subsequent_turn_sees_larger_library(self):
        """Next turn in the same session should match against grown library."""
        library = dict(get_all_shapes())
        history = []
        fake = {"answer": "trust compounds", "confidence": 0.70,
                "implication": "increases", "success": True}
        with patch.object(content_layer, 'run', return_value=fake):
            run("How does trust spread through an organization?",
                verbose=False, shape_library=library, bridge_history=history)
        count_after_first = len(library)
        with patch.object(content_layer, 'run', return_value=fake):
            run("How does a political movement gain momentum?",
                verbose=False, shape_library=library, bridge_history=history)
        # Library should have grown further (or stayed same if dedup)
        assert len(library) >= count_after_first


# ── Helpers ──

def _make_bridge(source_shape, target_domain, gap_dims=None, gap_score=0.5,
                  input_text=None):
    if input_text is None:
        # Default: derive plausible input from the target domain name
        label = target_domain.replace("_system", "").replace("_", " ")
        input_text = f"How does {label} work in this domain?"
    return {
        "bridge": f"{source_shape} geometry applies: test bridge description.",
        "assumptions": ["provisional"],
        "confidence": 0.5,
        "status": "provisional",
        "geometric_prediction": "structural relationship holds",
        "implication_type": "conditional",
        "shape_name": source_shape,
        "target_domain": target_domain,
        "gap_dims": gap_dims or {},
        "gap_score": gap_score,
        "input_text": input_text,
    }


def _make_history_record(source_shape, target_domain, confidence=0.5):
    return {
        "source_shape": source_shape,
        "target_domain": target_domain,
        "geometric_confidence": confidence,
        "gap_dims": {},
        "gap_score": 0.5,
    }
