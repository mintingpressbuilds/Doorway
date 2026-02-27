# main.py — Phase 7: Main Pipeline
# Status logic includes content-leads path for GROUND.

import os
from dotenv import load_dotenv
from pruv import xy_wrap
from core import gap_detector, bridge_builder, content_layer, conflict_detector, chain as chain_module
load_dotenv()

PRUV_API_KEY = os.getenv("PRUV_API_KEY")

@xy_wrap(
    chain_name="doorway_agi", auto_redact=True,
    **({"api_key": PRUV_API_KEY} if PRUV_API_KEY else {})
)
def _reasoning_core(input_text):
    content = content_layer.run(input_text)
    structure = gap_detector.run(input_text)
    bridge = bridge_builder.build(structure) if structure["fires"] else None
    conflict = conflict_detector.check(content, structure, bridge)

    # Status determination with content-leads path
    if not structure["fires"] and not conflict["conflict"] and content["confidence"] > 0.75:
        status = "GROUND"
    elif (structure["gap_score"] > 0.8 and not conflict["conflict"]
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


def run(input_text, verbose=True):
    wrapped = _reasoning_core(input_text)
    result = wrapped.output
    receipt = chain_module.extract_receipt_info(wrapped)
    if verbose:
        print(f"\n{'█'*60}")
        print(f"  STATUS: {result['status']}")
        print(f"  Input: {input_text[:80]}")
        print(f"  Gap score: {result['structure']['gap_score']} | Fired: {result['structure']['fires']}")
        print(f"  Closest: {result['structure']['closest_shape']} ({result['structure']['geometric_confidence']})")
        if result["bridge"]:
            print(f"  Bridge: {result['bridge']['bridge'][:120]}...")
            print(f"  Assumptions: {result['bridge']['assumptions']}")
        if result["conflict"]["conflict"]:
            print(f"  CONFLICT: {result['conflict']['message']}")
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
