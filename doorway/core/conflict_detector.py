# core/conflict_detector.py — Component 5
# Sync verification. Geometric and content layer alignment check.
# Compare implications not confidence scores.

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


def check(content_result, structure_result, bridge_result=None):
    content_impl = content_result.get("implication", "conditional")
    geometric_impl = structure_result.get("implication_type", "conditional")
    geometric_prediction = structure_result.get("geometric_prediction", "")
    directional_conflict = IMPLICATION_CONFLICTS.get(
        (content_impl, geometric_impl), False
    )
    confidence_gap = (
        abs(
            content_result.get("confidence", 0)
            - structure_result.get("geometric_confidence", 0)
        )
        > 0.35
    )
    conflict = directional_conflict or (
        confidence_gap
        and content_result.get("confidence", 0) > 0.6
        and structure_result.get("geometric_confidence", 0) > 0.6
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
