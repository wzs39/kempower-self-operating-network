"""
Test Suite for Closed-Loop Minute-by-Minute Discrete Simulation Engine and F02/F03/F06 fixes.
Location: tests/test_discrete_sim_engine.py
"""

import unittest
from datetime import datetime
from pathlib import Path

from src.sim.discrete_sim import (
    Job,
    taper_limit,
    waterfill_allocate,
    load_fleet_jobs,
    run_discrete_event_simulation,
    simulate_closed_loop_minute_by_minute,
)
from src.sim.data_loader import KempowerDataLoader
from src.sim.scenario_engine import ScenarioEngine
from src.commercial.roi_analyzer import ROIAnalyzer
from app import build_dashboard_payload

class TestDiscreteSimEngine(unittest.TestCase):
    """Test suite for minute-by-minute discrete event simulator & crash fixes."""

    def test_cv_taper_profile(self):
        """Verifies that acceptance power follows constant current up to 80% SoC, then tapers nonlinearly."""
        job = Job(
            vehicle_id="TEST_VEH",
            arrive=datetime.fromisoformat("2026-11-13T00:00:00+02:00"),
            depart=datetime.fromisoformat("2026-11-13T04:00:00+02:00"),
            battery_kwh=400.0,
            soc_in=0.20,
            soc_req=0.90,
            max_kw=150.0,
        )
        self.assertEqual(taper_limit(job, 0.20), 150.0)
        self.assertEqual(taper_limit(job, 0.50), 150.0)
        self.assertEqual(taper_limit(job, 0.80), 150.0)

        taper_85 = taper_limit(job, 0.85)
        taper_90 = taper_limit(job, 0.90)
        taper_95 = taper_limit(job, 0.95)
        taper_100 = taper_limit(job, 1.00)

        self.assertLess(taper_85, 150.0)
        self.assertLess(taper_90, taper_85)
        self.assertLess(taper_95, taper_90)
        self.assertLess(taper_100, taper_95)
        self.assertAlmostEqual(taper_100, 15.0, places=1)  # 150.0 * 0.10 = 15 kW

    def test_waterfill_urgency_allocation(self):
        """Verifies that urgency waterfilling allocates power proportional to urgency weight and respects limits."""
        j1 = Job("V1", datetime.fromisoformat("2026-11-13T00:00:00+02:00"), datetime.fromisoformat("2026-11-13T01:00:00+02:00"), 100.0, 0.2, 0.8, 150.0)
        j2 = Job("V2", datetime.fromisoformat("2026-11-13T00:00:00+02:00"), datetime.fromisoformat("2026-11-13T04:00:00+02:00"), 100.0, 0.2, 0.8, 150.0)

        # j1 has 60 kWh in 1h (weight = 60), j2 has 60 kWh in 4h (weight = 15). Ratio = 4:1.
        alloc = waterfill_allocate(
            items=[j1, j2],
            cap_kw=100.0,
            weight_fn=lambda j: 60.0 if j.vehicle_id == "V1" else 15.0,
            limit_fn=lambda j: 150.0,
        )
        self.assertAlmostEqual(alloc["V1"], 80.0, places=2)
        self.assertAlmostEqual(alloc["V2"], 20.0, places=2)

    def test_s1_closed_loop_discrete_sim(self):
        """Verifies S1 discrete simulation dynamically yields 0 missed departures on Scenario Day."""
        sim = simulate_closed_loop_minute_by_minute(site_id="S1", date="2026-11-13", strategy="urgency", cross_tie=True)
        self.assertEqual(sim["site_id"], "S1")
        self.assertEqual(sim["missed_departures"], 0)
        self.assertEqual(sim["deficit_kwh"], 0.0)
        self.assertEqual(sim["moves"], 0)
        self.assertGreater(sim["total_kwh"], 7000.0)
        self.assertLessEqual(sim["peak_kw"], 1080.0)

    def test_s2_closed_loop_discrete_sim(self):
        """Verifies S2 discrete simulation dynamically yields 0 missed departures for all 8 afternoon trucks."""
        sim = simulate_closed_loop_minute_by_minute(site_id="S2", date="2026-11-13", strategy="urgency", cross_tie=True)
        self.assertEqual(sim["site_id"], "S2")
        self.assertEqual(sim["missed_departures"], 0)
        self.assertEqual(sim["deficit_kwh"], 0.0)
        self.assertEqual(sim["moves"], 0)
        self.assertLessEqual(sim["peak_kw"], 800.0)

    def test_s5_closed_loop_discrete_sim(self):
        """Verifies S5 discrete simulation dynamically yields 0 missed departures under reconciled 900 kW grid limit."""
        sim = simulate_closed_loop_minute_by_minute(site_id="S5", date="2026-11-13", strategy="urgency", cross_tie=True)
        self.assertEqual(sim["site_id"], "S5")
        self.assertEqual(sim["missed_departures"], 0)
        self.assertEqual(sim["deficit_kwh"], 0.0)
        self.assertEqual(sim["moves"], 0)
        self.assertLessEqual(sim["peak_kw"], 900.0)

    def test_scenario_engine_closed_loop_integration(self):
        """Verifies that ScenarioEngine aggregates dynamic discrete simulations to 13 -> 0 missed departures."""
        loader = KempowerDataLoader()
        engine = ScenarioEngine(loader)
        res = engine.run_all_scenarios()
        self.assertEqual(res["scenario_day_missed_before"], 13)
        self.assertEqual(res["scenario_day_missed_after"], 0)
        self.assertEqual(res["S1"]["optimized_missed_departures"], 0)
        self.assertEqual(res["S2"]["optimized_missed_departures"], 0)
        self.assertEqual(res["S5"]["optimized_missed_departures"], 0)

    def test_f02_roi_analyzer_peak_vs_energy_zero_crash(self):
        """Verifies that ROIAnalyzer.analyze_monthly_peak_demand_vs_energy runs without finance_daily.csv."""
        res = ROIAnalyzer.analyze_monthly_peak_demand_vs_energy()
        self.assertEqual(res["s1_s5_monthly_peak_demand_fee_eur"], 31788.25)
        self.assertEqual(res["s1_s5_energy_cost_14d_eur"], 29978.00)
        self.assertEqual(res["s1_s5_revenue_14d_eur"], 115903.99)
        self.assertTrue(res["peak_demand_exceeds_14d_energy_cost"])

    def test_app_build_dashboard_payload_zero_crash(self):
        """Verifies that app.py build_dashboard_payload runs cleanly without exceptions."""
        payload = build_dashboard_payload()
        self.assertIn("scenarios", payload)
        self.assertIn("labor", payload)
        self.assertIn("equip", payload)
        self.assertIn("peak_vs_energy", payload)
        self.assertEqual(payload["scenarios"]["scenario_day_missed_after"], 0)

if __name__ == "__main__":
    unittest.main()
