# core/conflict_detector.py — Component 5
# Sync verification. Geometric and content layer alignment check.
# Compare implications not confidence scores.
# Directional conflict only fires when the structural match is
# meaningful — a weak shape match carries no implication to conflict with.

IMPLICATION_CONFLICTS = {
    ("unconditional", "threshold"): True,
    ("unconditional", "conditional"): True,
    ("unconditional", "decreases"): True,
    ("increases", "decreases"): True,
    ("increases", "threshold"): False,
    ("conditional", "unconditional"): True,
    ("decreases", "increases"): True,
    ("decreases", "unconditional"): True,
    ("threshold", "unconditional"): True,
    ("threshold", "increases"): False,
}

# Minimum shape confidence for the structural implication to be
# meaningful enough to conflict with the content layer.
CONFLICT_SHAPE_FLOOR = 0.20


def check(content_result, structure_result, bridge_result=None):
    content_impl = content_result.get("implication", "conditional")
    geometric_impl = structure_result.get("implication_type", "conditional")
    geometric_confidence = structure_result.get("geometric_confidence", 0)
    geometric_prediction = structure_result.get("geometric_prediction", "")

    # Directional conflict only meaningful when the shape match is real.
    # A noise-level match (e.g. 0.18 on threshold_system for "water boils")
    # carries no structural implication worth conflicting with.
    if geometric_confidence >= CONFLICT_SHAPE_FLOOR:
        directional_conflict = IMPLICATION_CONFLICTS.get(
            (content_impl, geometric_impl), False
        )
    else:
        directional_conflict = False

    confidence_gap = (
        abs(
            content_result.get("confidence", 0)
            - geometric_confidence
        )
        > 0.35
    )
    conflict = directional_conflict or (
        confidence_gap
        and content_result.get("confidence", 0) > 0.6
        and geometric_confidence > 0.6
    )
    return {
        "conflict": conflict,
        "directional_conflict": directional_conflict,
        "confidence_gap": confidence_gap,
        "content_implication": content_impl,
        "geometric_implication": geometric_impl,
        "geometric_prediction": geometric_prediction,
        "message": (
            f"Content implies '{content_impl}' but {geometric_impl} geometry "
            f"predicts '{geometric_prediction}'. Neither treated as ground."
        )
        if conflict
        else "Layers agree or compatible.",
    }
