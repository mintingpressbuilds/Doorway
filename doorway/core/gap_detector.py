# core/gap_detector.py — Component 2
# Two-tier keyword scoring. Passes 1+3 of four-pass architecture.
# Gap score is NOT confidence. It measures how much maximum potential
# is pressing against the boundary of known geometry.

from .shape_library import get_all_shapes

TIER1_WEIGHT = 0.75
TIER2_WEIGHT = 0.50
FIRE_THRESHOLD = 0.35

# Below this score, the shape match is too weak to be meaningful.
# The matcher returns the closest shape but marks confidence as 0.0
# so the status classifier knows no shape is geometrically relevant.
MINIMUM_SHAPE_CONFIDENCE = 0.10

# ── Domain familiarity dampening ──
# The keyword-based gap detector cannot distinguish "water boils at 100C"
# from "why do startups collapse" — both score similarly low on keywords.
# When the content layer is very confident on factual material, that is
# a strong signal that the input is in well-established territory and the
# gap score should be reduced. This prevents textbook facts from getting
# high gap scores just because their vocabulary doesn't match shape keywords.
DOMAIN_DAMPENING_THRESHOLD = 0.90  # Content confidence must be at least this
DOMAIN_DAMPENING_FACTOR = 0.62     # Reduce gap by this fraction


def score_shape(input_text, shape):
    input_lower = input_text.lower()
    tier1_hits = sum(1 for kw in shape["keywords_tier1"] if kw in input_lower)
    tier1_score = min(tier1_hits / max(len(shape["keywords_tier1"]) * 0.4, 1), 1.0)
    tier2_hits = sum(1 for kw in shape["keywords_tier2"] if kw in input_lower)
    tier2_score = min(tier2_hits / max(len(shape["keywords_tier2"]) * 0.35, 1), 1.0)
    combined = (tier1_score * TIER1_WEIGHT) + (tier2_score * TIER2_WEIGHT)
    return round(min(combined, 1.0), 3)


def run(input_text, shape_library=None):
    if shape_library is None:
        library = get_all_shapes()
    else:
        library = shape_library
    scores = {name: score_shape(input_text, shape) for name, shape in library.items()}
    sorted_shapes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    best_name, best_score = sorted_shapes[0]
    second_name, second_score = sorted_shapes[1] if len(sorted_shapes) > 1 else (None, 0)

    # Enforce minimum shape confidence — below this, the match is noise
    if best_score < MINIMUM_SHAPE_CONFIDENCE:
        effective_confidence = 0.0
    else:
        effective_confidence = best_score

    gap_score = round(1 - effective_confidence, 3)
    fires = gap_score > FIRE_THRESHOLD
    best_shape = library[best_name]
    return {
        "closest_shape": best_name,
        "geometric_confidence": effective_confidence,
        "geometric_prediction": best_shape["geometric_prediction"],
        "implication_type": best_shape["implication_type"],
        "second_shape": second_name,
        "second_confidence": second_score,
        "gap_score": gap_score,
        "fires": fires,
        "all_scores": dict(sorted_shapes[:5])
    }


def apply_domain_dampening(gap_score, content_result):
    """
    Pre-check for domain familiarity. Called after both the gap detector
    and content layer have run.

    The keyword-based gap detector treats "water boils at 100C" the same
    as "why do startups collapse" because neither matches shape keywords.
    But the content layer knows "water boils" is textbook knowledge.

    When content confidence is very high AND the content succeeded, dampen
    the gap score. The geometric analysis still ran — this just weights
    the result by the domain familiarity signal.

    Returns the dampened gap score. The original gap_score in the structure
    dict is preserved for reporting; this dampened value is used only for
    status classification.
    """
    content_confidence = content_result.get("confidence", 0)
    content_success = content_result.get("success", False)

    if content_confidence >= DOMAIN_DAMPENING_THRESHOLD and content_success:
        return round(gap_score * (1.0 - DOMAIN_DAMPENING_FACTOR), 3)

    return gap_score
