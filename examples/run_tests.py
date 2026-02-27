# examples/run_tests.py — Phase 8: Test Suite (20 Inputs)
# Target: 15 of 20 passing.

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import run

TEST_INPUTS = [
    # Known territory — gap quiet or content leads
    ("How does compound interest work?", "GROUND"),
    ("What is the boiling point of water?", "GROUND"),
    ("How does a supply chain work?", "GROUND"),
    ("What time is it?", "GROUND"),
    ("Is the sky blue?", "GROUND"),
    # Adjacent territory — gap fires, bridge built
    ("How does a startup's reputation compound in a new market?", "BRIDGE"),
    ("How does trust spread through an organization?", "BRIDGE"),
    ("How does a technology platform achieve critical mass?", "BRIDGE"),
    ("How does knowledge accumulate in a research field?", "BRIDGE"),
    ("Describe the dynamics of a coral reef ecosystem.", "BRIDGE"),
    ("How does a political movement gain momentum?", "BRIDGE"),
    ("How does a language evolve over generations?", "BRIDGE"),
    ("How does an immune system learn from exposure?", "BRIDGE"),
    ("How does consciousness emerge from neurons?", "BRIDGE"),
    ("Should I take this job offer?", "BRIDGE"),
    ("Describe the internal logic of a system nobody has studied.", "BRIDGE"),
    # Conflict territory — content and structure disagree
    ("More features always make software better.", "CONFLICT"),
    ("Bigger teams always produce better results.", "CONFLICT"),
    ("More data always improves AI models.", "CONFLICT"),
    ("More choice always leads to better outcomes.", "CONFLICT"),
]


def run_test_suite():
    passed = 0
    failed = 0
    results = []

    print("=" * 70)
    print("Doorway AGI — Test Suite (20 Inputs)")
    print("=" * 70)

    for i, (input_text, expected) in enumerate(TEST_INPUTS, 1):
        try:
            result = run(input_text, verbose=False)
            actual = result["status"]
            ok = actual == expected
            if ok:
                passed += 1
                marker = "PASS"
            else:
                failed += 1
                marker = "FAIL"
            results.append((input_text, expected, actual, ok))
            gap = result["structure"]["gap_score"]
            shape = result["structure"]["closest_shape"]
            conf = result["content"].get("confidence", 0)
            print(f"  [{marker}] {i:>2}. {input_text[:55]:<57} "
                  f"expected={expected:<12} got={actual:<12} "
                  f"gap={gap:.3f} conf={conf:.2f} shape={shape}")
        except Exception as e:
            failed += 1
            results.append((input_text, expected, f"ERROR: {e}", False))
            print(f"  [FAIL] {i:>2}. {input_text[:55]:<57} ERROR: {e}")

    print(f"\n{'=' * 70}")
    print(f"  RESULT: {passed}/{passed + failed} passing (target: 15/20)")
    target_met = passed >= 15
    print(f"  TARGET {'MET' if target_met else 'NOT MET'}")
    print(f"{'=' * 70}")

    if failed > 0:
        print(f"\n  Failed tests:")
        for input_text, expected, actual, ok in results:
            if not ok:
                print(f"    - '{input_text[:60]}' expected={expected} got={actual}")

    return passed, failed, target_met


if __name__ == "__main__":
    passed, failed, target_met = run_test_suite()
    sys.exit(0 if target_met else 1)
