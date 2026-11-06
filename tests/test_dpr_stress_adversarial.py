"""
Adversarial Stress Test Suite for Kempower DPR Matrix Allocation & App Launch.
Module: tests/test_dpr_stress_adversarial.py

Auditor: M1 Challenger 1 (critic / specialist)
Focus:
1. S1 12-gun full load at 150 kW, 100 kW, 50 kW (verifying prefix isolation, exact sums).
2. Single-gun massive load (500 kW, 10,000 kW) clamped to physical limits.
3. Prefix boundary edge cases (D1-1 vs D1-10..12, D1-100, D1-1A, D1-20, cross-cabinet violations).
4. Random load spikes, partial disconnects, zero-demand, negative requests, Monte Carlo invariants (5,000 cycles).
5. Stress testing app.py launch under varied environments and paths.
"""

import math
import os
import random
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.dpr_matrix import (
    DPRMatrix,
    STATION_CABINET_TOPOLOGY,
    MODULE_POWER_KW,
    INVERTER_EFFICIENCY,
)
from app import build_dashboard_payload


class TestDPRMatrixStressAdversarial(unittest.TestCase):
    """Rigorous empirical stress test suite for DPR allocation and prefix edge cases."""

    def setUp(self):
        self.dpr_s1 = DPRMatrix("S1")
        self.dpr_s2 = DPRMatrix("S2")
        self.dpr_s3 = DPRMatrix("S3")
        self.dpr_s4 = DPRMatrix("S4")
        self.dpr_s5 = DPRMatrix("S5")

    # =========================================================================
    # 1. 12-Gun Full Load at S1 (Prefix isolation and exact allocations)
    # =========================================================================

    def test_s1_12_guns_150kw_full_load_allocation(self):
        """
        Adversarial test: 12 guns requesting 150 kW each at S1.
        Total requested = 1,800 kW.
        Physical capacity: 3 cabinets x 360 kW = 1,080 kW DC.
        Grid limit: 1,200 kW AC.
        Assert:
        - Total allocated DC power == 1,080.0 kW (exactly 360 kW per cabinet).
        - Each gun receives exactly 90.0 kW.
        - C1-3 guns (D1-9, D1-10, D1-11, D1-12) receive exactly 90.0 kW each (no prefix stealing by D1-1).
        """
        reqs = {f"D1-{i}": 150.0 for i in range(1, 13)}
        alloc = self.dpr_s1.allocate_intra_cabinet_continuous(reqs, grid_limit_kw=1200.0)

        self.assertEqual(len(alloc), 12)
        total_dc = sum(alloc.values())
        self.assertAlmostEqual(total_dc, 1080.0, places=2, msg=f"Expected 1080 kW DC total, got {total_dc}")

        # Check each cabinet
        cab_guns = {
            "C1-1": ["D1-1", "D1-2", "D1-3", "D1-4"],
            "C1-2": ["D1-5", "D1-6", "D1-7", "D1-8"],
            "C1-3": ["D1-9", "D1-10", "D1-11", "D1-12"],
        }
        for cab_id, guns in cab_guns.items():
            cab_sum = sum(alloc[g] for g in guns)
            self.assertAlmostEqual(cab_sum, 360.0, places=2, msg=f"Cabinet {cab_id} sum {cab_sum} != 360 kW")
            for g in guns:
                self.assertAlmostEqual(alloc[g], 90.0, places=2, msg=f"Gun {g} allocation {alloc[g]} != 90 kW")

    def test_s1_12_guns_100kw_load_allocation(self):
        """
        Adversarial test: 12 guns requesting 100 kW each at S1.
        Total requested = 1,200 kW.
        Per cabinet demand: 4 x 100 kW = 400 kW > 360 kW cabinet limit.
        Assert:
        - Each cabinet is capped at 360 kW.
        - Each gun receives 90.0 kW (360 / 4).
        - Total allocated == 1,080.0 kW DC.
        """
        reqs = {f"D1-{i}": 100.0 for i in range(1, 13)}
        alloc = self.dpr_s1.allocate_intra_cabinet_continuous(reqs, grid_limit_kw=1200.0)

        total_dc = sum(alloc.values())
        self.assertAlmostEqual(total_dc, 1080.0, places=2)
        for i in range(1, 13):
            self.assertAlmostEqual(alloc[f"D1-{i}"], 90.0, places=2)

    def test_s1_12_guns_50kw_load_allocation(self):
        """
        Adversarial test: 12 guns requesting 50 kW each at S1.
        Total requested = 600 kW.
        Per cabinet demand: 4 x 50 kW = 200 kW < 360 kW cabinet limit.
        Assert:
        - No throttling: each gun receives exactly 50.0 kW.
        - Total allocated == 600.0 kW DC.
        """
        reqs = {f"D1-{i}": 50.0 for i in range(1, 13)}
        alloc = self.dpr_s1.allocate_intra_cabinet_continuous(reqs, grid_limit_kw=1200.0)

        total_dc = sum(alloc.values())
        self.assertAlmostEqual(total_dc, 600.0, places=2)
        for i in range(1, 13):
            self.assertAlmostEqual(alloc[f"D1-{i}"], 50.0, places=2)

    def test_s1_12_guns_asymmetric_prefix_critical_load(self):
        """
        Adversarial test: Asymmetric requests designed to trigger prefix collisions if present:
        - D1-1 requests 150 kW, D1-2..D1-4 request 10 kW (C1-1 demand = 180 kW < 360 kW).
        - D1-10 requests 150 kW, D1-11 requests 150 kW, D1-12 requests 50 kW, D1-9 requests 10 kW (C1-3 demand = 360 kW == 360 kW).
        If D1-10 was matched to D1-1, C1-1 would be wrongly overloaded or D1-10 would be curtailed.
        """
        reqs = {
            "D1-1": 150.0, "D1-2": 10.0, "D1-3": 10.0, "D1-4": 10.0,
            "D1-5": 50.0,  "D1-6": 50.0, "D1-7": 50.0, "D1-8": 50.0,
            "D1-9": 10.0,  "D1-10": 150.0, "D1-11": 150.0, "D1-12": 50.0,
        }
        alloc = self.dpr_s1.allocate_intra_cabinet_continuous(reqs, grid_limit_kw=1200.0)

        # C1-1 total demand = 180 kW <= 360 kW -> all satisfied exactly
        self.assertAlmostEqual(alloc["D1-1"], 150.0, places=2)
        self.assertAlmostEqual(alloc["D1-2"], 10.0, places=2)
        self.assertAlmostEqual(alloc["D1-3"], 10.0, places=2)
        self.assertAlmostEqual(alloc["D1-4"], 10.0, places=2)

        # C1-2 total demand = 200 kW <= 360 kW -> all satisfied exactly
        for g in ["D1-5", "D1-6", "D1-7", "D1-8"]:
            self.assertAlmostEqual(alloc[g], 50.0, places=2)

        # C1-3 total demand = 360 kW <= 360 kW -> all satisfied exactly
        self.assertAlmostEqual(alloc["D1-9"], 10.0, places=2)
        self.assertAlmostEqual(alloc["D1-10"], 150.0, places=2)
        self.assertAlmostEqual(alloc["D1-11"], 150.0, places=2)
        self.assertAlmostEqual(alloc["D1-12"], 50.0, places=2)

    # =========================================================================
    # 2. Single-Gun Massive Load Clamping
    # =========================================================================

    def test_single_gun_massive_load_s1(self):
        """
        A single gun requesting 500 kW on S1 (dispenser rating 150 kW, cabinet 360 kW).
        Must be clamped to 150 kW (charger_max_kw).
        """
        alloc = self.dpr_s1.allocate_intra_cabinet_continuous({"D1-1": 500.0}, grid_limit_kw=1200.0)
        self.assertAlmostEqual(alloc["D1-1"], 150.0, places=2)

        # Extreme 1,000,000 kW request
        alloc_huge = self.dpr_s1.allocate_intra_cabinet_continuous({"D1-1": 1_000_000.0}, grid_limit_kw=1200.0)
        self.assertAlmostEqual(alloc_huge["D1-1"], 150.0, places=2)

    def test_single_gun_massive_load_s2(self):
        """
        A single gun requesting 500 kW on S2 (dispenser rating 300 kW, cabinet 400 kW).
        Must be clamped to 300 kW.
        """
        alloc = self.dpr_s2.allocate_intra_cabinet_continuous({"D2-1": 500.0}, grid_limit_kw=800.0)
        self.assertAlmostEqual(alloc["D2-1"], 300.0, places=2)

    def test_single_gun_massive_load_s3_varying_cabinets(self):
        """
        S3 has C3-1/C3-2 (300 kW guns) and C3-3 (150 kW guns).
        Verify clamping per cabinet dispenser ratings.
        """
        # D3-1 on C3-1 (charger_max_kw = 300.0)
        alloc1 = self.dpr_s3.allocate_intra_cabinet_continuous({"D3-1": 800.0}, grid_limit_kw=1500.0)
        self.assertAlmostEqual(alloc1["D3-1"], 300.0, places=2)

        # D3-9 on C3-3 (charger_max_kw = 150.0)
        alloc9 = self.dpr_s3.allocate_intra_cabinet_continuous({"D3-9": 800.0}, grid_limit_kw=1500.0)
        self.assertAlmostEqual(alloc9["D3-9"], 150.0, places=2)

    def test_single_gun_discrete_allocate_power_clamped(self):
        """
        Verify that DPRMatrix.allocate_power clamps single-gun massive requests to cabinet/grid capacity.
        """
        res = self.dpr_s1.allocate_power("S1", {"D1-1": 1000.0}, grid_limit_kw=1200.0, cabinet_capacity_kw=360.0)
        self.assertTrue(res.is_safe)
        self.assertLessEqual(res.allocated_power["D1-1"], 360.0)
        self.assertLessEqual(res.ac_grid_draw_kw, 1200.0)
        self.assertTrue(res.is_throttled)

    # =========================================================================
    # 3. Prefix Boundary Edge Cases & Cross-Cabinet Violations
    # =========================================================================

    def test_is_charger_match_unit_boundaries(self):
        """Adversarial check of _is_charger_match across subtle string variations."""
        m = DPRMatrix._is_charger_match

        # Exact matches
        self.assertTrue(m("D1-1", "D1-1"))
        self.assertTrue(m("D1-10", "D1-10"))
        self.assertTrue(m("D1-12", "D1-12"))

        # Numeric extension collisions (MUST BE FALSE)
        self.assertFalse(m("D1-10", "D1-1"))
        self.assertFalse(m("D1-11", "D1-1"))
        self.assertFalse(m("D1-12", "D1-1"))
        self.assertFalse(m("D1-19", "D1-1"))
        self.assertFalse(m("D1-100", "D1-1"))
        self.assertFalse(m("D1-20", "D1-2"))
        self.assertFalse(m("D1-21", "D1-2"))
        self.assertFalse(m("D1-30", "D1-3"))

        # Legitimate sub-gun suffixes (MUST BE TRUE)
        self.assertTrue(m("D1-1A", "D1-1"))
        self.assertTrue(m("D1-1B", "D1-1"))
        self.assertTrue(m("D1-1_1", "D1-1"))
        self.assertTrue(m("D1-1:1", "D1-1"))
        self.assertTrue(m("D1-1-A", "D1-1"))
        self.assertTrue(m("D1-10A", "D1-10"))

        # Non-matching prefixes
        self.assertFalse(m("D2-1", "D1-1"))
        self.assertFalse(m("D1", "D1-1"))
        self.assertFalse(m("", "D1-1"))

    def test_cross_cabinet_routing_prohibition(self):
        """Attempting to route a charger via an unwired cabinet must raise ValueError."""
        # D1-5 is wired to C1-2, NOT C1-1
        with self.assertRaises(ValueError) as ctx:
            self.dpr_s1.allocate_intra_cabinet_continuous("C1-1", {"D1-5": 50.0})
        self.assertIn("Cross-cabinet routing prohibited", str(ctx.exception))

        # D1-10 is wired to C1-3, NOT C1-1
        with self.assertRaises(ValueError) as ctx:
            self.dpr_s1.allocate_intra_cabinet_continuous("C1-1", {"D1-10": 50.0})
        self.assertIn("Cross-cabinet routing prohibited", str(ctx.exception))

        # D1-1 is wired to C1-1, NOT C1-3
        with self.assertRaises(ValueError) as ctx:
            self.dpr_s1.allocate_intra_cabinet_continuous("C1-3", {"D1-1": 50.0})
        self.assertIn("Cross-cabinet routing prohibited", str(ctx.exception))

        # Invalid cabinet ID
        with self.assertRaises(ValueError) as ctx:
            self.dpr_s1.allocate_intra_cabinet_continuous("C1-99", {"D1-1": 50.0})
        self.assertIn("Unknown cabinet", str(ctx.exception))

    # =========================================================================
    # 4. Random Load Spikes, Partial Disconnects & Zero Demand
    # =========================================================================

    def test_zero_and_negative_requests(self):
        """Zero and negative requests must safely return zero allocation without exception."""
        reqs = {"D1-1": 0.0, "D1-2": -100.0, "D1-3": -0.001, "D1-4": 0.0}
        alloc = self.dpr_s1.allocate_intra_cabinet_continuous(reqs, grid_limit_kw=1200.0)
        for g, p in alloc.items():
            self.assertEqual(p, 0.0)

    def test_dynamic_partial_disconnect_redistribution(self):
        """
        Simulate real-time scenario:
        - Step 1: 4 guns on C1-1 request 150 kW each -> each gets 90 kW (360 kW total).
        - Step 2: D1-1 and D1-2 disconnect (drop to 0 kW) -> D1-3 and D1-4 instantly scale up to 150 kW each (300 kW total).
        - Step 3: D1-3 disconnects -> D1-4 gets its full requested 150 kW (150 kW total).
        """
        # Step 1
        alloc1 = self.dpr_s1.allocate_intra_cabinet_continuous(
            {"D1-1": 150.0, "D1-2": 150.0, "D1-3": 150.0, "D1-4": 150.0},
            grid_limit_kw=1200.0
        )
        for g in ["D1-1", "D1-2", "D1-3", "D1-4"]:
            self.assertAlmostEqual(alloc1[g], 90.0, places=2)

        # Step 2: D1-1 & D1-2 disconnect
        alloc2 = self.dpr_s1.allocate_intra_cabinet_continuous(
            {"D1-1": 0.0, "D1-2": 0.0, "D1-3": 150.0, "D1-4": 150.0},
            grid_limit_kw=1200.0
        )
        self.assertEqual(alloc2["D1-1"], 0.0)
        self.assertEqual(alloc2["D1-2"], 0.0)
        self.assertAlmostEqual(alloc2["D1-3"], 150.0, places=2)
        self.assertAlmostEqual(alloc2["D1-4"], 150.0, places=2)

        # Step 3: D1-3 disconnects
        alloc3 = self.dpr_s1.allocate_intra_cabinet_continuous(
            {"D1-1": 0.0, "D1-2": 0.0, "D1-3": 0.0, "D1-4": 150.0},
            grid_limit_kw=1200.0
        )
        self.assertAlmostEqual(alloc3["D1-4"], 150.0, places=2)

    def test_monte_carlo_random_stress_invariants_5000_cycles(self):
        """
        Adversarial Monte Carlo harness: 5,000 cycles of randomized requests across all stations.
        Verifies 5 fundamental physical invariants under chaotic inputs:
        1. 0.0 <= allocated[g] <= requests[g] (if req > 0)
        2. allocated[g] <= charger_max_kw
        3. Cabinet DC sum <= cab_avail_kw + 1e-4
        4. Station DC sum <= grid_limit_kw + 1e-4
        5. If grid_limit <= 0, total allocated == 0
        """
        rng = random.Random(42)
        stations = ["S1", "S2", "S3", "S4", "S5"]

        for cycle in range(5000):
            st_id = rng.choice(stations)
            dpr = getattr(self, f"dpr_{st_id.lower()}")
            topo = STATION_CABINET_TOPOLOGY[st_id]

            # Collect all guns at this station
            all_guns = [g for cab in topo.values() for g in cab["chargers"]]

            # Choose a random subset of guns to make requests
            num_active = rng.randint(0, len(all_guns))
            active_guns = rng.sample(all_guns, num_active)

            # Generate random requests (including negative and massive requests)
            reqs: Dict[str, float] = {}
            for g in all_guns:
                if g in active_guns:
                    r_type = rng.random()
                    if r_type < 0.10:
                        reqs[g] = 0.0  # zero request
                    elif r_type < 0.15:
                        reqs[g] = -rng.uniform(1.0, 100.0)  # negative request
                    elif r_type < 0.25:
                        reqs[g] = rng.uniform(500.0, 2000.0)  # massive request
                    else:
                        reqs[g] = rng.uniform(1.0, 350.0)  # normal request
                else:
                    reqs[g] = 0.0

            # Random grid limit (sometimes 0, sometimes tight, sometimes ample)
            grid_lim = rng.choice([0.0, 100.0, 300.0, 600.0, 1000.0, 1500.0, 2500.0])

            # Random cabinet health deratings
            derates = {cab: rng.uniform(0.0, 1.0) if rng.random() < 0.3 else 1.0 for cab in topo}

            # Random priorities
            prios = {g: rng.uniform(0.1, 5.0) for g in all_guns}

            # Execute allocation
            alloc = dpr.allocate_intra_cabinet_continuous(
                requests_kw=reqs,
                grid_limit_kw=grid_lim,
                priorities=prios,
                cabinet_deratings=derates
            )

            # Invariant 5: If grid limit <= 0, everything is 0
            if grid_lim <= 0.0:
                self.assertEqual(sum(alloc.values()), 0.0)
                continue

            # Invariant 1 & 2: Gun limits
            for cab_id, cab_spec in topo.items():
                cab_guns = [g for g in cab_spec["chargers"] if g in reqs]
                cab_sum = 0.0
                for g in cab_guns:
                    p = alloc[g]
                    r = reqs[g]
                    self.assertGreaterEqual(p, -1e-6, f"Negative allocation on {g}: {p}")
                    if r <= 0.0:
                        self.assertEqual(p, 0.0, f"Non-zero allocation on {g} with non-positive request {r}")
                    else:
                        # round(share, 2) has up to 0.005 kW rounding delta against raw continuous float r
                        self.assertLessEqual(p, r + 0.01, f"Allocated {p} > request {r} on {g}")
                    self.assertLessEqual(p, cab_spec["charger_max_kw"] + 1e-4, f"Exceeded charger max on {g}")
                    cab_sum += p

                # Invariant 3: Cabinet capacity limit (cumulative 2-decimal rounding sum up to len(cab_guns) * 0.005 kW)
                cab_max = cab_spec["max_kw"] * max(0.0, min(1.0, derates.get(cab_id, 1.0)))
                cab_rounding_margin = len(cab_guns) * 0.005 + 1e-3
                self.assertLessEqual(cab_sum, cab_max + cab_rounding_margin, f"Cabinet {cab_id} overloaded: {cab_sum} > {cab_max}")

            # Invariant 4: Station grid limit (allowing for cumulative 2-decimal rounding sum up to N_guns * 0.005 kW)
            total_st = sum(alloc.values())
            rounding_margin = len(all_guns) * 0.005 + 1e-4  # max 0.06 kW for 12 guns
            self.assertLessEqual(total_st, grid_lim + rounding_margin, f"Site limit exceeded: {total_st} > {grid_lim}")


class TestAppLaunchStressAdversarial(unittest.TestCase):
    """Stress testing app.py launch and payload integrity under varied environments."""

    def test_build_dashboard_payload_deterministic_values(self):
        """Assert dashboard payload builds without error and produces exact values."""
        payload = build_dashboard_payload()
        self.assertIn("topology", payload)
        self.assertIn("scenarios", payload)
        self.assertIn("labor", payload)
        self.assertIn("equip", payload)
        self.assertIn("peak_vs_energy", payload)

        sc = payload["scenarios"]
        self.assertEqual(sc["scenario_day_missed_after"], 3)
        self.assertEqual(sc["scenario_day_missed_before"], 13)

        labor = payload["labor"]
        self.assertAlmostEqual(labor["total_network_fte"], 20.76, places=2)
        self.assertAlmostEqual(labor["replug_network_fte"], 9.95, places=2)

    def test_app_launch_subprocess_clean_exit(self):
        """Run python app.py as a standalone process and verify exit code 0."""
        cmd = [sys.executable, str(REPO_ROOT / "app.py")]
        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, f"app.py failed: {result.stderr}")
        self.assertIn(
            "Dashboard payload verified: 13 -> 3 (0 EUR software) | zero-miss needs cross-cabinet busbar (unpriced); +12 plugs = 324,000 EUR yields 8",
            result.stdout,
        )

    def test_app_launch_under_varied_env_vars(self):
        """Run python app.py with modified and missing environment variables."""
        test_envs = [
            {"STREAMLIT_SERVER_PORT": "9999", "STREAMLIT_SERVER_HEADLESS": "true"},
            {"PYTHONUNBUFFERED": "1", "LANG": "C"},
            {"STREAMLIT_THEME_BASE": "dark", "CUSTOM_VAR_FOO": "BAR"},
        ]
        for extra_env in test_envs:
            env = os.environ.copy()
            env.update(extra_env)
            cmd = [sys.executable, str(REPO_ROOT / "app.py")]
            result = subprocess.run(
                cmd,
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=30,
                env=env,
            )
            self.assertEqual(result.returncode, 0, f"app.py failed with env {extra_env}: {result.stderr}")
            self.assertIn(
                "Dashboard payload verified: 13 -> 3 (0 EUR software) | zero-miss needs cross-cabinet busbar (unpriced); +12 plugs = 324,000 EUR yields 8",
                result.stdout,
            )


if __name__ == "__main__":
    unittest.main()
