# core/tier2_emergence.py — Session-scoped Tier 2 emergence detection
# After each confirmation, check if cross-domain structural intersection
# exceeds threshold. If so, add new Tier 2 pattern to the shared library.
#
# Tier 2 shapes emerge when the same source geometry successfully bridges
# to multiple unrelated domains — proving the geometry is universal, not
# domain-specific. This is the compounding property at work.

# Minimum distinct domains bridged by the same source shape to trigger emergence
CROSS_DOMAIN_THRESHOLD = 3

# Minimum average confidence across the bridged domains
CONFIDENCE_THRESHOLD = 0.40


def emerge_tier2(bridge_history, shared_library, supabase_client=None):
    """
    Check for Tier 2 emergence patterns across bridge history.

    Groups bridges by source shape. If any source shape has successfully
    bridged to CROSS_DOMAIN_THRESHOLD or more distinct target domains
    with sufficient confidence, a Tier 2 intersection pattern is detected.

    Args:
        bridge_history: List of bridge records from the session
                        (each a dict with source_shape, target_domain,
                        geometric_confidence, gap_dims, etc.)
        shared_library: Current shared library dict.
        supabase_client: If provided, writes Tier 2 shapes to database.

    Returns:
        Dict with emergence status and any new Tier 2 shapes added.
    """
    if len(bridge_history) < CROSS_DOMAIN_THRESHOLD:
        return {
            "emergence_detected": False,
            "reason": f"Minimum {CROSS_DOMAIN_THRESHOLD} bridges required",
            "bridge_count": len(bridge_history),
            "new_shapes": [],
        }

    # Group bridges by source shape
    by_source = {}
    for record in bridge_history:
        source = record.get("source_shape", "unknown")
        if source not in by_source:
            by_source[source] = []
        by_source[source].append(record)

    new_shapes = []

    for source_shape, bridges in by_source.items():
        # Get distinct target domains
        domains = {}
        for b in bridges:
            td = b.get("target_domain", "unknown_domain")
            if td != "unknown_domain" and td not in domains:
                domains[td] = b

        if len(domains) < CROSS_DOMAIN_THRESHOLD:
            continue

        # Check average confidence
        confidences = [b.get("geometric_confidence", 0) for b in domains.values()]
        avg_confidence = sum(confidences) / len(confidences)
        if avg_confidence < CONFIDENCE_THRESHOLD:
            continue

        # Tier 2 emergence detected: this source shape bridges universally
        tier2_name = f"tier2_{source_shape}_intersection"

        if tier2_name in shared_library:
            continue

        # Collect the dimensional axes that appear across all bridged domains
        all_dims = {}
        for b in domains.values():
            for axis, value in b.get("gap_dims", {}).items():
                if axis not in all_dims:
                    all_dims[axis] = []
                all_dims[axis].append(value)

        domain_names = list(domains.keys())
        domain_labels = [d.replace("_system", "").replace("_", " ")
                         for d in domain_names]

        tier2_shape = {
            "structure": (
                f"{source_shape.replace('_', ' ')} geometry confirmed across "
                f"{len(domains)} domains: {', '.join(domain_labels[:5])} — "
                f"indicating universal structural pattern"
            ),
            "elements": [source_shape, "cross_domain", "intersection",
                         "universality", "emergence"],
            "keywords_tier1": [source_shape.replace("_", " "), "intersection",
                               "cross-domain", "universal"],
            "keywords_tier2": domain_labels[:8],
            "geometric_prediction": (
                f"{source_shape.replace('_', ' ')} pattern transfers across "
                f"unrelated domains with consistent structural mapping"
            ),
            "implication_type": "conditional",
            "color_dimensions": {k: v[0] for k, v in list(all_dims.items())[:4]},
            "analogs": domain_names[:3],
            "constraints": [
                "requires_cross_domain_evidence",
                "pattern_must_be_structural_not_surface",
            ],
            "_tier2": True,
            "_source_geometry": source_shape,
            "_domains_confirmed": domain_names,
            "_avg_confidence": round(avg_confidence, 4),
        }

        shared_library[tier2_name] = tier2_shape
        new_shapes.append({"name": tier2_name, "definition": tier2_shape})

        if supabase_client:
            try:
                supabase_client.table("confirmed_shapes").upsert({
                    "name": tier2_name,
                    "tier": 2,
                    "structure": tier2_shape["structure"],
                    "elements": tier2_shape["elements"],
                    "keywords_tier1": tier2_shape["keywords_tier1"],
                    "keywords_tier2": tier2_shape["keywords_tier2"],
                    "geometric_prediction": tier2_shape["geometric_prediction"],
                    "implication_type": tier2_shape["implication_type"],
                    "color_dims": tier2_shape["color_dimensions"],
                    "confirmed_via": source_shape,
                    "gap_at_confirmation": avg_confidence,
                }, on_conflict="name").execute()
            except Exception as e:
                print(f"[tier2_emergence] Could not write to Supabase: {e}")

    return {
        "emergence_detected": len(new_shapes) > 0,
        "new_shapes": new_shapes,
        "bridge_count": len(bridge_history),
        "sources_checked": len(by_source),
    }
