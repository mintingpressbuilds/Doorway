# core/confirmation.py — Confirmation Loop
# Extracts the geometry of the unknown domain B from a bridge.
# What enters the library is B's geometry — NOT a copy of the source shape.
# Deduplicates against existing library. Writes to shared confirmed_shapes
# table in Supabase (no user_id — shared across all users).

from .gap_detector import score_shape

# Dimensional axes that suggest specific implication types
_THRESHOLD_SIGNALS = ["threshold", "critical", "rupture", "breaking", "saturation",
                      "limit", "capacity", "tipping"]
_INCREASE_SIGNALS = ["rate", "gain", "growth", "amplification", "accumulation",
                     "compounding", "scaling"]
_DECREASE_SIGNALS = ["decay", "depletion", "erosion", "degradation", "loss",
                     "dissipation", "attrition"]

# Minimum gap_score for a bridge to be confirmable
CONFIRM_GAP_THRESHOLD = 0.35

# Maximum keyword overlap with any existing shape before we call it a duplicate
DEDUP_OVERLAP_THRESHOLD = 0.70


def extract_geometry(bridge):
    """
    Extract the geometry of the unknown domain B from a bridge result.

    Uses bridge["target_domain"] and bridge["gap_dims"] to produce a
    genuinely new geometric pattern. The new shape describes what B
    actually IS — not what the source shape is.

    Returns a shape definition dict, or None if extraction fails.
    """
    target_domain = bridge.get("target_domain", "unknown_domain")
    gap_dims = bridge.get("gap_dims", {})
    source_shape = bridge.get("shape_name", "unknown")
    bridge_text = bridge.get("bridge", "")
    gap_score = bridge.get("gap_score", 0)

    if target_domain == "unknown_domain":
        return None

    # Derive B's implication_type from gap_dims analysis — NOT from source
    impl_type = _infer_implication_type(gap_dims, bridge_text)

    # Derive B's structure from the bridge (reoriented toward B)
    domain_label = target_domain.replace("_system", "").replace("_", " ")
    structure = (
        f"{domain_label} exhibits geometric pattern where "
        f"{bridge.get('geometric_prediction', 'structural relationship holds')}"
    )

    # Extract B's elements from the target domain name
    domain_words = [w for w in target_domain.replace("_system", "").split("_") if w]
    elements = domain_words[:5]
    # Pad with structural elements derived from gap_dims axes
    for axis in gap_dims:
        if len(elements) < 5 and axis not in elements:
            elements.append(axis)

    # Keywords come from B's domain, not from the source shape
    keywords_tier1 = domain_words[:4]
    if len(keywords_tier1) < 4:
        keywords_tier1.extend(list(gap_dims.keys())[:4 - len(keywords_tier1)])
    keywords_tier2 = list(gap_dims.keys()) + [domain_label]

    # Color dims come from the gap_dims analysis
    color_dims = dict(gap_dims) if gap_dims else {}

    # Geometric prediction oriented toward B
    geometric_prediction = (
        f"{domain_label} follows {impl_type} pattern — "
        f"{bridge.get('geometric_prediction', 'structural relationship holds')}"
    )

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


def _infer_implication_type(gap_dims, bridge_text):
    """
    Determine B's implication type from dimensional analysis.
    This is B's own geometry — not copied from the source shape.
    """
    combined = " ".join(list(gap_dims.keys()) + list(gap_dims.values())).lower()
    combined += " " + bridge_text.lower()

    threshold_score = sum(1 for s in _THRESHOLD_SIGNALS if s in combined)
    increase_score = sum(1 for s in _INCREASE_SIGNALS if s in combined)
    decrease_score = sum(1 for s in _DECREASE_SIGNALS if s in combined)

    if threshold_score >= 2:
        return "threshold"
    if increase_score > decrease_score and increase_score >= 2:
        return "increases"
    if decrease_score > increase_score and decrease_score >= 2:
        return "decreases"
    return "conditional"


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
