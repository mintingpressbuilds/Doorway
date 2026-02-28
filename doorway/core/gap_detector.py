# core/gap_detector.py — Component 2
# Two-tier keyword scoring. Passes 1+3 of four-pass architecture.
# Gap score is NOT confidence. It measures how much maximum potential
# is pressing against the boundary of known geometry.

from .shape_library import get_all_shapes

TIER1_WEIGHT = 0.75
TIER2_WEIGHT = 0.50
FIRE_THRESHOLD = 0.35


def score_shape(input_text, shape):
    input_lower = input_text.lower()
    tier1_hits = sum(1 for kw in shape["keywords_tier1"] if kw in input_lower)
    tier1_score = min(tier1_hits / max(len(shape["keywords_tier1"]) * 0.4, 1), 1.0)
    tier2_hits = sum(1 for kw in shape["keywords_tier2"] if kw in input_lower)
    tier2_score = min(tier2_hits / max(len(shape["keywords_tier2"]) * 0.35, 1), 1.0)
    combined = (tier1_score * TIER1_WEIGHT) + (tier2_score * TIER2_WEIGHT)
    return round(min(combined, 1.0), 3)


def run(input_text):
    library = get_all_shapes()
    scores = {name: score_shape(input_text, shape) for name, shape in library.items()}
    sorted_shapes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_name, best_score = sorted_shapes[0]
    second_name, second_score = sorted_shapes[1] if len(sorted_shapes) > 1 else (None, 0)
    gap_score = round(1 - best_score, 3)
    fires = gap_score > FIRE_THRESHOLD
    best_shape = library[best_name]
    return {
        "closest_shape": best_name,
        "geometric_confidence": best_score,
        "geometric_prediction": best_shape["geometric_prediction"],
        "implication_type": best_shape["implication_type"],
        "second_shape": second_name,
        "second_confidence": second_score,
        "gap_score": gap_score,
        "fires": fires,
        "all_scores": dict(sorted_shapes[:5])
    }
