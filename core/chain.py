# core/chain.py — Component 6
# Chain integration via pruv's xy_wrap.
# api_key conditional: no PRUV_API_KEY = runs entirely local.

import os
from pruv import xy_wrap, CloudClient, XYChain

PRUV_API_KEY = os.getenv("PRUV_API_KEY")  # None in local dev — that's fine


def get_wrapper(chain_name="doorway_agi"):
    return xy_wrap(
        chain_name=chain_name, auto_redact=True,
        **({"api_key": PRUV_API_KEY} if PRUV_API_KEY else {})
    )


def extract_receipt_info(wrapped_result):
    return {
        "chain_id": wrapped_result.chain.id,
        "chain_root": wrapped_result.chain.root,
        "chain_length": wrapped_result.chain.length,
        "chain_verified": wrapped_result.verified,
        "receipt": wrapped_result.receipt,
    }


async def upload_chain(chain: XYChain):
    client = CloudClient(api_key=PRUV_API_KEY)
    return await client.upload_chain(chain)


async def verify_remote(chain_id: str):
    client = CloudClient(api_key=PRUV_API_KEY)
    return await client.verify_chain(chain_id)
