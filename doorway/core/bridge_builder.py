# core/bridge_builder.py — Component 3
# Geometric bridging. Builds new structure from the gap.
# Only called when gap fires. Bridge is always provisional.

from .shape_library import get_shape


def build(gap_result):
    shape = get_shape(gap_result["closest_shape"])
    if not shape:
        return None
    assumptions = []
    if gap_result["geometric_confidence"] < 0.6:
        assumptions.append(f"assuming {gap_result['closest_shape'].replace('_', ' ')} geometry transfers to this domain")
    if gap_result["second_confidence"] > 0.35:
        assumptions.append(f"secondary {gap_result['second_shape'].replace('_', ' ')} geometry may also apply")
    assumptions.append("bridge held as provisional until confirmed against domain evidence")
    bridge_description = (
        f"{gap_result['closest_shape'].replace('_', ' ')} geometry applies: {shape['structure']}. "
        f"Key transferring elements: {', '.join(shape['elements'][:3])}. "
        f"Known analogs: {', '.join(shape['analogs'][:2])}. "
        f"Geometric prediction: {shape['geometric_prediction']}."
    )
    confidence = round(gap_result["geometric_confidence"] * 0.90, 3)
    return {
        "bridge": bridge_description,
        "assumptions": assumptions,
        "confidence": confidence,
        "status": "provisional",
        "geometric_prediction": gap_result["geometric_prediction"],
        "implication_type": gap_result["implication_type"],
    }
