# core/content_layer.py — Component 4
# Spatial distribution. Dimensional structure expressed in language.
# Model string configurable via DOORWAY_MODEL env var.

import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL = os.getenv("DOORWAY_MODEL", "claude-sonnet-4-20250514")

HEDGING_WORDS = ["might", "could", "possibly", "perhaps", "unclear",
                 "uncertain", "depends", "varies", "sometimes", "generally"]
UNCONDITIONAL_WORDS = ["always", "never", "all", "every", "must",
                       "impossible", "certain", "definitely"]


def extract_implication(answer_text, input_text=None):
    text_lower = answer_text.lower()
    unconditional = any(w in text_lower for w in UNCONDITIONAL_WORDS)
    hedged = any(w in text_lower for w in HEDGING_WORDS)
    # Phase 8 tuning: also check original input for unconditional claims (always/never).
    # If the input itself makes an unconditional claim, the implication is unconditional
    # regardless of whether Claude hedges in the response.
    if input_text:
        input_lower = input_text.lower()
        if any(w in input_lower for w in UNCONDITIONAL_WORDS):
            return "unconditional"
    if unconditional and not hedged:
        return "unconditional"
    elif hedged:
        return "conditional"
    elif any(w in text_lower for w in ["increase", "grow", "rise", "more", "better"]):
        return "increases"
    elif any(w in text_lower for w in ["decrease", "fall", "less", "worse", "decline"]):
        return "decreases"
    else:
        return "conditional"


def run(input_text):
    if not API_KEY:
        return {"answer": "[No API key]", "confidence": 0.0,
                "implication": extract_implication("", input_text), "success": False}
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 300,
        "messages": [{"role": "user", "content":
                      f"Answer this directly and confidently in 2-3 sentences. "
                      f"Do not over-qualify unless genuinely uncertain.\n\n{input_text}"}]
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "x-api-key": API_KEY,
            "anthropic-version": "2023-06-01",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read())
            answer = data["content"][0]["text"]
            word_count = len(answer.split())
            hedge_count = sum(1 for w in HEDGING_WORDS if w in answer.lower())
            confidence = round(max(0.3, min(0.95, (word_count / 80) - (hedge_count * 0.08))), 2)
            return {
                "answer": answer,
                "confidence": confidence,
                "implication": extract_implication(answer, input_text),
                "success": True,
            }
    except Exception as e:
        return {
            "answer": f"[Content layer error: {str(e)[:120]}]",
            "confidence": 0.0,
            "implication": extract_implication("", input_text),
            "success": False,
        }
