# core/bridge_builder.py — Component 3
# Geometric bridging. Builds new structure from the gap.
# Only called when gap fires. Bridge is always provisional.

from .shape_library import get_shape

_STOP_WORDS = frozenset([
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "during", "before", "after", "between", "out", "off", "over", "under",
    "again", "then", "here", "there", "when", "where", "why", "how", "all",
    "both", "each", "few", "more", "most", "other", "some", "such", "no",
    "nor", "not", "only", "own", "same", "so", "than", "too", "very",
    "just", "now", "and", "but", "or", "if", "while", "that", "this",
    "what", "which", "who", "whom", "these", "those", "its", "it", "about",
    "work", "works", "make", "makes", "does", "describe", "many", "much",
])


def extract_target_domain(input_text):
    """Extract the target domain name from input text."""
    words = [w.strip("?.,!\"'()") for w in input_text.lower().split()]
    meaningful = [w for w in words if w.isalpha() and len(w) > 2
                  and w not in _STOP_WORDS]
    if not meaningful:
        return "unknown_domain"
    # Take up to 3 most meaningful words, form system name
    name = "_".join(meaningful[:3]) + "_system"
    return name


def build(gap_result, input_text=None):
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

    target_domain = extract_target_domain(input_text) if input_text else "unknown_domain"
    gap_dims = dict(shape.get("color_dimensions", {}))

    return {
        "bridge": bridge_description,
        "assumptions": assumptions,
        "confidence": confidence,
        "status": "provisional",
        "geometric_prediction": gap_result["geometric_prediction"],
        "implication_type": gap_result["implication_type"],
        "shape_name": gap_result["closest_shape"],
        "target_domain": target_domain,
        "gap_dims": gap_dims,
        "gap_score": gap_result["gap_score"],
    }
