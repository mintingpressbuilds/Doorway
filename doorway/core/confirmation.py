# core/confirmation.py — Confirmation Loop
# Extracts the geometry of the unknown domain B from a bridge.
# What enters the library is B's geometry — NOT a copy of the source shape.
# Deduplicates against existing library. Writes to shared confirmed_shapes
# table in Supabase (no user_id — shared across all users).

from .gap_detector import score_shape

# ── Signals scanned in input_text to determine B's implication_type ──
# These are properties of B's domain, not of the source shape.
_THRESHOLD_SIGNALS = [
    "threshold", "critical", "tipping", "phase transition", "rupture",
    "breaking point", "saturation", "boiling", "melting", "capacity",
    "limit", "cliff", "snap", "collapse", "decoherence", "coherence",
    "error threshold", "tolerance", "fault tolerance",
]
_INCREASE_SIGNALS = [
    "compound", "exponential", "growth", "accumulate", "amplif",
    "accelerat", "scaling", "multiply", "spread", "viral",
    "compound interest", "snowball", "reinvest",
]
_DECREASE_SIGNALS = [
    "decay", "deplet", "erosion", "degradat", "attrition", "dissipat",
    "entropy", "decline", "fade", "wither", "half-life", "depreciat",
]

# Words that carry structural meaning in the input — kept as B's elements
_STRUCTURAL_WORDS = frozenset([
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "during", "before", "after", "between", "out", "off", "over", "under",
    "again", "then", "here", "there", "when", "where", "why", "how",
    "all", "both", "each", "some", "no", "not", "very", "just", "now",
    "and", "but", "or", "if", "that", "this", "what", "which", "who",
    "its", "it", "about", "work", "works", "make", "makes", "does",
    "describe", "many", "much", "more", "most",
])

# Minimum gap_score for a bridge to be confirmable
CONFIRM_GAP_THRESHOLD = 0.35

# Maximum keyword overlap with any existing shape before we call it a duplicate
DEDUP_OVERLAP_THRESHOLD = 0.70


def _extract_domain_words(input_text):
    """Pull meaningful words from input — these describe B's domain."""
    words = [w.strip("?.,!\"'()") for w in input_text.lower().split()]
    return [w for w in words if w.isalpha() and len(w) > 2
            and w not in _STRUCTURAL_WORDS]


def extract_geometry(bridge):
    """
    Extract the geometry of the unknown domain B from a bridge result.

    Uses bridge["target_domain"], bridge["gap_dims"], and
    bridge["input_text"] to produce a genuinely new geometric pattern.
    The new shape describes what B actually IS — not what the source
    shape is.

    Returns a shape definition dict, or None if extraction fails.
    """
    target_domain = bridge.get("target_domain", "unknown_domain")
    gap_dims = bridge.get("gap_dims", {})
    source_shape = bridge.get("shape_name", "unknown")
    input_text = bridge.get("input_text", "")
    gap_score = bridge.get("gap_score", 0)

    if target_domain == "unknown_domain":
        return None

    # ── B's words — extracted from what the user actually asked about ──
    domain_words = _extract_domain_words(input_text)
    domain_label = target_domain.replace("_system", "").replace("_", " ")

    # ── Implication type — inferred from B's domain text, NOT from source ──
    impl_type = _infer_implication_type(input_text, gap_dims)

    # ── Structure — describes B's geometric pattern from the destination side ──
    # The source shape's prediction is deliberately excluded.
    structure = _derive_structure(domain_label, domain_words, impl_type, gap_dims)

    # ── Elements — structural components of B ──
    elements = _derive_elements(domain_words, gap_dims)

    # ── Keywords — from B's domain, not from source shape ──
    keywords_tier1 = domain_words[:5]
    # tier2: additional context words + gap_dims axis names
    keywords_tier2 = domain_words[5:13] + list(gap_dims.keys())

    # ── Color dims — axes relevant to B's domain ──
    # Start from gap_dims (the bridge's dimensional texture),
    # then reinterpret axes toward B where possible.
    color_dims = dict(gap_dims) if gap_dims else {}

    # ── Geometric prediction — what B's geometry predicts ──
    geometric_prediction = _derive_prediction(domain_label, impl_type, elements)

    return {
        "name": target_domain,
        "tier": 1,
        "structure": structure,
        "elements": elements,
        "keywords_tier1": keywords_tier1,
        "keywords_tier2": keywords_tier2,
        "geometric_prediction": geometric_prediction,
        "implication_type": impl_type,
        "color_dims": color_dims,
        "confirmed_via": source_shape,
        "gap_at_confirmation": gap_score,
    }


def _infer_implication_type(input_text, gap_dims):
    """
    Determine B's implication type from the input text and dimensional
    texture. Scans for domain-specific signals. This is B's own
    geometry — not copied from the source shape.
    """
    text = input_text.lower()
    # Also consider gap_dims axis names as secondary signal
    dim_text = " ".join(list(gap_dims.keys()) + list(gap_dims.values())).lower()
    combined = text + " " + dim_text

    threshold_score = sum(1 for s in _THRESHOLD_SIGNALS if s in combined)
    increase_score = sum(1 for s in _INCREASE_SIGNALS if s in combined)
    decrease_score = sum(1 for s in _DECREASE_SIGNALS if s in combined)

    if threshold_score >= 2:
        return "threshold"
    if threshold_score == 1 and increase_score == 0 and decrease_score == 0:
        return "threshold"
    if increase_score > decrease_score and increase_score >= 1:
        return "increases"
    if decrease_score > increase_score and decrease_score >= 1:
        return "decreases"
    return "conditional"


def _derive_structure(domain_label, domain_words, impl_type, gap_dims):
    """
    Build a structure description for B from B's domain words and
    inferred implication type. Does NOT reference the source shape.
    """
    # Describe the core structural relationship
    core_words = domain_words[:6]
    if not core_words:
        return f"{domain_label} exhibits {impl_type} geometric pattern"

    noun_phrase = " ".join(core_words[:3])
    verb_phrase = " ".join(core_words[3:6]) if len(core_words) > 3 else ""

    parts = [f"{noun_phrase}"]
    if verb_phrase:
        parts.append(verb_phrase)

    dim_description = ""
    if gap_dims:
        axes = list(gap_dims.items())[:2]
        dim_parts = [f"{k.replace('_', ' ')} varying from {v.replace('_', ' ')}"
                     for k, v in axes]
        dim_description = " with " + " and ".join(dim_parts)

    structure = (
        f"{' '.join(parts)} — "
        f"{impl_type} pattern where {domain_label} "
        f"geometry operates{dim_description}"
    )
    return structure


def _derive_elements(domain_words, gap_dims):
    """
    Extract B's structural elements from domain words and gap_dims.
    Elements are the building blocks of B's geometry.
    """
    elements = []
    # Primary elements from B's domain
    for w in domain_words:
        if len(elements) >= 5:
            break
        if w not in elements:
            elements.append(w)
    # Fill remaining from dimensional axes
    for axis in gap_dims:
        if len(elements) >= 5:
            break
        if axis not in elements:
            elements.append(axis)
    return elements if elements else ["structure", "pattern", "relationship"]


def _derive_prediction(domain_label, impl_type, elements):
    """
    Generate geometric prediction for B based on its inferred type
    and structural elements.
    """
    elem_str = ", ".join(elements[:3]) if elements else domain_label

    predictions = {
        "threshold": (
            f"{domain_label} maintains stability until critical threshold — "
            f"{elem_str} collapse or transform beyond that point"
        ),
        "increases": (
            f"{elem_str} compound over time producing non-linear growth "
            f"in {domain_label}"
        ),
        "decreases": (
            f"{elem_str} degrade over time following predictable decay "
            f"in {domain_label}"
        ),
        "conditional": (
            f"{domain_label} behavior depends on interaction between "
            f"{elem_str} — outcome conditional on configuration"
        ),
    }
    return predictions.get(impl_type, predictions["conditional"])


def _is_duplicate(new_shape, shared_library):
    """
    Check if a shape with high keyword overlap already exists.
    Exact name match OR high keyword overlap = duplicate.
    """
    name = new_shape["name"]
    if name in shared_library:
        return True

    new_kw = set(new_shape["keywords_tier1"] + new_shape["keywords_tier2"])
    if not new_kw:
        return False

    for existing in shared_library.values():
        existing_kw = set(
            existing.get("keywords_tier1", []) + existing.get("keywords_tier2", [])
        )
        if not existing_kw:
            continue
        overlap = len(new_kw & existing_kw) / max(len(new_kw), 1)
        if overlap >= DEDUP_OVERLAP_THRESHOLD:
            return True

    return False


def _write_to_supabase(shape, supabase_client):
    """Write a confirmed shape to the shared confirmed_shapes table."""
    supabase_client.table("confirmed_shapes").upsert({
        "name": shape["name"],
        "tier": shape.get("tier", 1),
        "structure": shape["structure"],
        "elements": shape["elements"],
        "keywords_tier1": shape["keywords_tier1"],
        "keywords_tier2": shape["keywords_tier2"],
        "geometric_prediction": shape["geometric_prediction"],
        "implication_type": shape["implication_type"],
        "color_dims": shape.get("color_dims", {}),
        "confirmed_via": shape["confirmed_via"],
        "gap_at_confirmation": shape["gap_at_confirmation"],
    }, on_conflict="name").execute()


def confirm(bridge, shared_library, supabase_client=None):
    """
    Confirm a bridge and extract B's geometry into the shared library.

    Args:
        bridge: Bridge result dict (must include target_domain, gap_dims).
        shared_library: Current shared library dict (static + confirmed).
        supabase_client: If provided, writes confirmed shape to database.

    Returns:
        The new shape definition if genuinely new, or None if duplicate/invalid.
    """
    if not bridge or bridge.get("status") != "provisional":
        return None

    gap_score = bridge.get("gap_score", 0)
    if gap_score < CONFIRM_GAP_THRESHOLD:
        return None

    new_shape = extract_geometry(bridge)
    if new_shape is None:
        return None

    if _is_duplicate(new_shape, shared_library):
        return None

    # Add to in-memory shared library for this session
    shape_for_library = {
        "structure": new_shape["structure"],
        "elements": new_shape["elements"],
        "keywords_tier1": new_shape["keywords_tier1"],
        "keywords_tier2": new_shape["keywords_tier2"],
        "geometric_prediction": new_shape["geometric_prediction"],
        "implication_type": new_shape["implication_type"],
        "color_dimensions": new_shape.get("color_dims", {}),
        "analogs": [],
        "constraints": [],
        "_confirmed": True,
        "_confirmed_via": new_shape["confirmed_via"],
        "_gap_at_confirmation": new_shape["gap_at_confirmation"],
    }
    shared_library[new_shape["name"]] = shape_for_library

    # Persist to Supabase if available
    if supabase_client:
        try:
            _write_to_supabase(new_shape, supabase_client)
        except Exception as e:
            print(f"[confirmation] Could not write to Supabase: {e}")

    return new_shape
