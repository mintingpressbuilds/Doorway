# core/shape_library_loader.py — Load full shared library
# 50 static shapes + all confirmed shapes from Supabase.
# Used by both AGI and ASI on session start.

from .shape_library import get_all_shapes as get_static_shapes


def load_full_library(supabase_client=None):
    """
    Load the complete shape library: 50 static + all confirmed shapes.
    Used by both AGI and ASI on session start.

    Args:
        supabase_client: If provided, loads confirmed shapes from database.
                         If None, returns static shapes only (offline mode).

    Returns:
        Dictionary of all available shapes.
    """
    library = dict(get_static_shapes())

    if supabase_client:
        try:
            result = supabase_client.table("confirmed_shapes") \
                .select("name, structure, elements, keywords_tier1, "
                        "keywords_tier2, geometric_prediction, "
                        "implication_type, color_dims, confirmed_via, "
                        "gap_at_confirmation") \
                .eq("tier", 1) \
                .execute()

            if result.data:
                for row in result.data:
                    shape_def = {
                        "structure": row["structure"],
                        "elements": row["elements"],
                        "keywords_tier1": row["keywords_tier1"],
                        "keywords_tier2": row["keywords_tier2"],
                        "geometric_prediction": row["geometric_prediction"],
                        "implication_type": row["implication_type"],
                        "color_dimensions": row["color_dims"] or {},
                        "analogs": [],
                        "constraints": [],
                        "_confirmed": True,
                        "_confirmed_via": row["confirmed_via"],
                        "_gap_at_confirmation": row["gap_at_confirmation"],
                    }
                    library[row["name"]] = shape_def

        except Exception as e:
            print(f"[shape_library] Could not load confirmed shapes: {e}")

    return library
