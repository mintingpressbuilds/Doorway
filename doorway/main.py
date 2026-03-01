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

@xy_wrap(
    chain_name="doorway_agi", auto_redact=True,
    **({"api_key": PRUV_API_KEY} if PRUV_API_KEY else {})
)
def _reasoning_core(input_text, history=None, shape_library=None):
    content = content_layer.run(input_text, history=history)
    structure = gap_detector.run(input_text, shape_library=shape_library)
    bridge = bridge_builder.build(structure, input_text=input_text) if structure["fires"] else None
    conflict = conflict_detector.check(content, structure, bridge)

    # Status determination with content-leads path
    if not structure["fires"] and not conflict["conflict"] and content["confidence"] > 0.75:
        status = "GROUND"
    elif (structure["gap_score"] > 0.9 and not conflict["conflict"]
          and content["confidence"] > 0.85 and content["success"]):
        status = "GROUND"  # Content-leads: no shape relevant, content highly confident
    elif conflict["conflict"]:
        status = "CONFLICT"
    elif structure["fires"]:
        status = "BRIDGE"
    else:
        status = "PROVISIONAL"

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
