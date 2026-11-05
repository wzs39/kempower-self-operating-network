"""
Master Test Runner: The Self-Operating Charging Network E2E Test Suite
Track: Independent Opaque-Box E2E Testing Architecture (Tiers 1-4)
Location: e2e_tests/test_runner.py

Executes all 4 test tiers, outputs structured progress and metrics,
and enforces zero-regression quality gates.
"""

import os
import sys
import time
import argparse
import unittest
from pathlib import Path

# Ensure repo root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

# Import tier test classes
from e2e_tests.tier1_feature_coverage import TestTier1FeatureCoverage
from e2e_tests.tier2_boundary_corner import TestTier2BoundaryCornerCases
from e2e_tests.tier3_cross_feature import TestTier3CrossFeatureCombinations
from e2e_tests.tier4_real_world_scenario import TestTier4RealWorldScenarios

TIER_MAP = {
    1: {
        "name": "Tier 1: Feature Contract Coverage (>=5 tests per core feature)",
        "module": "e2e_tests.tier1_feature_coverage",
        "case_cls": TestTier1FeatureCoverage,
    },
    2: {
        "name": "Tier 2: Boundary & Corner Cases (Stress, Edge & Saturation)",
        "module": "e2e_tests.tier2_boundary_corner",
        "case_cls": TestTier2BoundaryCornerCases,
    },
    3: {
        "name": "Tier 3: Cross-Feature Interactions (Pairwise & Multi-Variable)",
        "module": "e2e_tests.tier3_cross_feature",
        "case_cls": TestTier3CrossFeatureCombinations,
    },
    4: {
        "name": "Tier 4: Real-World Scenarios (2026-11-13 Scenario Day & 45 CSVs)",
        "module": "e2e_tests.tier4_real_world_scenario",
        "case_cls": TestTier4RealWorldScenarios,
    },
}

def run_suite(tiers=None, verbosity=1) -> int:
    """Runs designated tiers and outputs structured report."""
    target_tiers = tiers if tiers else [1, 2, 3, 4]

    print("=" * 80)
    print("KEMPOWER SELF-OPERATING CHARGING NETWORK — INDEPENDENT E2E TEST RUNNER")
    print("=" * 80)
    print(f"Target Tiers : {', '.join(f'Tier {t}' for t in target_tiers)}")
    print(f"Repository   : {REPO_ROOT}")
    print(f"Python Exec  : {sys.executable}")
    print("-" * 80)

    total_tests = 0
    total_failures = 0
    total_errors = 0
    total_skipped = 0
    suite_start = time.perf_counter()
    tier_results = []

    loader = unittest.TestLoader()

    for t_id in target_tiers:
        tier_info = TIER_MAP[t_id]
        tier_name = tier_info["name"]
        suite = loader.loadTestsFromTestCase(tier_info["case_cls"])
        n_tests = suite.countTestCases()

        print(f"\n[START] {tier_name} ({n_tests} test cases)")
        t_start = time.perf_counter()

        # Run with string stream or stdout depending on verbosity
        stream = sys.stdout if verbosity > 1 else None
        runner = unittest.TextTestRunner(stream=stream, verbosity=verbosity)
        result = runner.run(suite)
        t_duration = time.perf_counter() - t_start

        failures = len(result.failures)
        errors = len(result.errors)
        skipped = len(result.skipped)
        passed = result.testsRun - failures - errors - skipped

        total_tests += result.testsRun
        total_failures += failures
        total_errors += errors
        total_skipped += skipped

        status = "PASSED" if (failures == 0 and errors == 0) else "FAILED"
        tier_results.append({
            "tier_id": t_id,
            "name": tier_name,
            "total": result.testsRun,
            "passed": passed,
            "failed": failures,
            "errors": errors,
            "duration": t_duration,
            "status": status,
        })

        color_status = f"\033[92m{status}\033[0m" if status == "PASSED" else f"\033[91m{status}\033[0m"
        print(f"[{status}] Tier {t_id} complete: {passed}/{result.testsRun} passed in {t_duration:.3f}s")
        if failures > 0 or errors > 0:
            for f in result.failures:
                print(f"  [-] FAILURE: {f[0]}: {f[1]}")
            for e in result.errors:
                print(f"  [-] ERROR: {e[0]}: {e[1]}")

    total_duration = time.perf_counter() - suite_start

    print("\n" + "=" * 80)
    print("E2E SUITE EXECUTION SUMMARY TABLE")
    print("=" * 80)
    print(f"{'Tier':<8} | {'Tier Name':<42} | {'Count':<6} | {'Passed':<6} | {'Failed':<6} | {'Time (s)':<8} | {'Status':<7}")
    print("-" * 80)
    for r in tier_results:
        print(f"Tier {r['tier_id']:<3} | {r['name'][:42]:<42} | {r['total']:<6} | {r['passed']:<6} | {r['failed'] + r['errors']:<6} | {r['duration']:<8.3f} | {r['status']:<7}")
    print("-" * 80)
    total_failed = total_failures + total_errors
    overall_status = "ALL PASSED (100%)" if total_failed == 0 else f"FAILED ({total_failed} issues)"
    print(f"{'TOTAL':<8} | {'All Target Tiers Combined':<42} | {total_tests:<6} | {total_tests - total_failed:<6} | {total_failed:<6} | {total_duration:<8.3f} | {overall_status}")
    print("=" * 80)

    if total_failed == 0:
        print(f"\n>> SUCCESS: 100% Pass Rate ({total_tests}/{total_tests} passed in {total_duration:.3f}s). All quality gates green.\n")
        return 0
    else:
        print(f"\n>> FAILURE: {total_failed} tests failed or errored across suite.\n")
        return 1

def main():
    parser = argparse.ArgumentParser(description="Kempower Independent E2E Test Suite Runner")
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3, 4],
        action="append",
        help="Specify which tier(s) to execute (e.g. --tier 1 --tier 2). Defaults to all 4 tiers.",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable detailed verbose output for individual test cases.",
    )
    args = parser.parse_args()
    verbosity = 2 if args.verbose else 1
    exit_code = run_suite(tiers=args.tier, verbosity=verbosity)
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
