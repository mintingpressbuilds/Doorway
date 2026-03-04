# main.py — Phase 7: Main Pipeline
# Status logic includes content-leads path for GROUND.
# Confirmation loop and Tier 2 emergence run on bridge + no conflict.

import os
from dotenv import load_dotenv
from pruv import xy_wrap
from .core import gap_detector, bridge_builder, content_layer, conflict_detector, chain as chain_module
from .core.confirmation import confirm
from .core.tier2_emergence import emerge_tier2
from .core.bridge_history import save_bridge
load_dotenv()

_raw_key = os.getenv("PRUV_API_KEY")
PRUV_API_KEY = _raw_key if _raw_key and _raw_key != "pv_live_your_key_here" else None

# ── Status classification thresholds ──
PROVISIONAL_GAP_THRESHOLD = 0.80    # Gap must be at least this high for PROVISIONAL
PROVISIONAL_CONF_CEILING = 0.15     # Shape confidence must be below this for PROVISIONAL
GROUND_GAP_CEILING = 0.30           # Gap must be below this for structure-based GROUND
GROUND_SHAPE_FLOOR = 0.70           # Shape confidence must be at least this for GROUND
GROUND_CONTENT_FLOOR = 0.75         # Content confidence floor for quiet-gap GROUND
CONTENT_LEADS_CONFIDENCE = 0.85     # Content confidence for content-leads GROUND path
CONTENT_LEADS_GAP_CEILING = 0.40    # Dampened gap must be below this for content-leads GROUND


def _classify_status(gap_score, shape_confidence, conflict_detected,
                     content_confidence, content_success, fires):
    """
    Status classification — applied in priority order:

    1. CONFLICT takes priority if the conflict detector fired
    2. PROVISIONAL if gap is high AND shape confidence is below minimum
    3. GROUND if gap is low AND shape confidence is high (structure-confirmed)
    4. GROUND via content-leads: content confident AND gap is low
    5. BRIDGE for everything in between
    """
    # Rule 1: Conflict always wins
    if conflict_detected:
        return "CONFLICT"

    # Rule 2: PROVISIONAL — genuinely unknown territory
    # Gap fired hard AND no usable shape match. Content confidence
    # cannot override this — a gap of 1.0 with confidence 0.0 is
    # PROVISIONAL regardless of what the content layer thinks.
    if gap_score >= PROVISIONAL_GAP_THRESHOLD and shape_confidence < PROVISIONAL_CONF_CEILING:
        return "PROVISIONAL"

    # Rule 3: GROUND — confirmed territory (structure agrees)
    # Low gap + high shape confidence + content didn't fail
    if (gap_score < GROUND_GAP_CEILING and shape_confidence >= GROUND_SHAPE_FLOOR
            and content_success):
        return "GROUND"
    # Gap quiet (didn't fire) + content confident
    if not fires and content_confidence > GROUND_CONTENT_FLOOR:
        return "GROUND"

    # Rule 4: Content-leads GROUND — content very confident AND the
    # dampened gap is low. Both layers must agree: content says "known
    # territory" and the dampened gap confirms it's close enough.
    # Content confident + high gap → BRIDGE (geometry is unfamiliar).
    if (content_confidence >= CONTENT_LEADS_CONFIDENCE and content_success
            and gap_score < CONTENT_LEADS_GAP_CEILING):
        return "GROUND"

    # Rule 5: BRIDGE — everything else where gap fired
    if fires:
        return "BRIDGE"

    # Fallback: gap didn't fire, content not confident enough for GROUND
    return "PROVISIONAL"

@xy_wrap(
    chain_name="doorway_agi", auto_redact=True,
    **({"api_key": PRUV_API_KEY} if PRUV_API_KEY else {})
)
def _reasoning_core(input_text, history=None, shape_library=None):
    content = content_layer.run(input_text, history=history)
    structure = gap_detector.run(input_text, shape_library=shape_library)
    bridge = bridge_builder.build(structure, input_text=input_text) if structure["fires"] else None
    conflict = conflict_detector.check(content, structure, bridge)

    # Domain familiarity dampening: adjust gap score using content layer
    # signal before status classification. The raw gap_score in structure
    # is preserved for reporting — dampened_gap is used only for status.
    dampened_gap = gap_detector.apply_domain_dampening(
        structure["gap_score"], content)

    # Status determination — applied in priority order.
    status = _classify_status(
        gap_score=dampened_gap,
        shape_confidence=structure["geometric_confidence"],
        conflict_detected=conflict["conflict"],
        content_confidence=content.get("confidence", 0),
        content_success=content.get("success", False),
        fires=structure["fires"],
    )

    return {"status": status, "content": content, "structure": structure,
            "bridge": bridge, "conflict": conflict}


def run(input_text, verbose=True, history=None,
        shape_library=None, bridge_history=None,
        supabase_client=None, user_id=None, session_name="doorway_agi"):
    wrapped = _reasoning_core(input_text, history=history,
                              shape_library=shape_library)
    result = wrapped.output
    receipt = chain_module.extract_receipt_info(wrapped)

    confirmation_result = None
    emergence_result = None

    # Confirmation trigger: bridge built AND status != CONFLICT
    if result["bridge"] and result["status"] != "CONFLICT":
        # Save bridge to per-user history
        if bridge_history is not None:
            bridge_record = {
                "source_shape": result["bridge"].get("shape_name", "unknown"),
                "target_domain": result["bridge"].get("target_domain", "unknown_domain"),
                "geometric_confidence": result["bridge"].get("confidence", 0),
                "gap_dims": result["bridge"].get("gap_dims", {}),
                "gap_score": result["bridge"].get("gap_score", 0),
            }
            bridge_history.append(bridge_record)
            save_bridge(result["bridge"], user_id=user_id,
                        session_name=session_name, input_text=input_text,
                        supabase_client=supabase_client)

        # Run confirmation — extracts B's geometry, writes to shared library
        if shape_library is not None:
            confirmation_result = confirm(
                result["bridge"], shape_library,
                supabase_client=supabase_client)

        # Check Tier 2 emergence across session bridge history
        if bridge_history and shape_library is not None:
            emergence_result = emerge_tier2(
                bridge_history, shape_library,
                supabase_client=supabase_client)

    if verbose:
        print(f"\n{'█'*60}")
        print(f"  STATUS: {result['status']}")
        print(f"  Input: {input_text[:80]}")
        print(f"  Gap score: {result['structure']['gap_score']} | Fired: {result['structure']['fires']}")
        print(f"  Closest: {result['structure']['closest_shape']} ({result['structure']['geometric_confidence']})")
        if result["bridge"]:
            print(f"  Bridge: {result['bridge']['bridge'][:120]}...")
            print(f"  Assumptions: {result['bridge']['assumptions']}")
            print(f"  Target domain: {result['bridge'].get('target_domain', 'N/A')}")
        if result["conflict"]["conflict"]:
            print(f"  CONFLICT: {result['conflict']['message']}")
        if confirmation_result:
            print(f"  CONFIRMED: {confirmation_result['name']} absorbed into shared library")
        if emergence_result and emergence_result.get("emergence_detected"):
            for s in emergence_result["new_shapes"]:
                print(f"  TIER 2 EMERGENCE: {s['name']}")
        if shape_library is not None:
            print(f"  Library: {len(shape_library)} shapes")
        print(f"  Chain ID: {receipt['chain_id']}")
        print(f"  Verified: {receipt['chain_verified']}")
        print(f"{'█'*60}\n")

    return {
        "status": result["status"], "content": result["content"],
        "structure": result["structure"], "bridge": result["bridge"],
        "conflict": result["conflict"],
        "chain": {"id": wrapped.chain.id, "root": wrapped.chain.root,
                  "length": wrapped.chain.length, "verified": wrapped.verified},
        "receipt": receipt,
    }
