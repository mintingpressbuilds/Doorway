# core/bridge_history.py — Per-user bridge history persistence
# Saves bridge records to bridge_history table in Supabase (per-user).
# Loads a user's prior bridge history at session start.


def save_bridge(bridge, user_id, session_name="doorway_agi",
                input_text="", supabase_client=None):
    """
    Save a bridge record to the per-user bridge_history table.

    Args:
        bridge: Bridge result dict from bridge_builder.
        user_id: The user who produced this bridge.
        session_name: Session identifier.
        input_text: Original input text.
        supabase_client: Supabase client. If None, no-op.

    Returns:
        The saved record dict, or None if no client.
    """
    if not supabase_client or not bridge:
        return None

    record = {
        "user_id": user_id,
        "input_text": input_text,
        "source_shape": bridge.get("shape_name", "unknown"),
        "target_domain": bridge.get("target_domain", "unknown_domain"),
        "bridge_text": bridge.get("bridge", ""),
        "gap_score": bridge.get("gap_score", 0),
        "geometric_confidence": bridge.get("confidence", 0),
        "implication_type": bridge.get("implication_type", "conditional"),
        "gap_dims": bridge.get("gap_dims", {}),
        "status": bridge.get("status", "provisional"),
        "session_name": session_name,
    }

    try:
        result = supabase_client.table("bridge_history") \
            .insert(record).execute()
        return record
    except Exception as e:
        print(f"[bridge_history] Could not save bridge: {e}")
        return None


def load_bridge_history(user_id, supabase_client=None, limit=100):
    """
    Load a user's prior bridge history from Supabase.

    Args:
        user_id: The user whose history to load.
        supabase_client: Supabase client. If None, returns empty list.
        limit: Maximum number of records to load.

    Returns:
        List of bridge history records, newest first.
    """
    if not supabase_client:
        return []

    try:
        result = supabase_client.table("bridge_history") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()
        return result.data or []
    except Exception as e:
        print(f"[bridge_history] Could not load history: {e}")
        return []
