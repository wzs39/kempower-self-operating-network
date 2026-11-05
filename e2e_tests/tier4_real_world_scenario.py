"""
Tier 4: Real-World Application Scenarios (Scenario Day 2026-11-13 Realistic Workloads)
Validates full 24-hour closed-loop scenarios against the official 45 CSV datasets
with zero human intervention.
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import unittest
import pandas as pd

from e2e_tests.common import (
    DATA_DIR,
    PROJECT_PATH,
    SLA_PATH,
    ContractDPRMatrix,
    ContractMPCSolver,
    ContractEdgeFSM,
    ContractVirtualReplug,
    ContractSLAEngine,
    ROIAnalyzer,
    ScenarioEngine,
    SLACalculator,
)

class TestTier4RealWorldScenarios(unittest.TestCase):
    """Tier 4: Real-World Scenarios across S1-S5 and Commercial AEaaS."""

    def test_s1_24_bus_night_shift_baseline_vs_sentinel(self):
        """S1 Depot: 4 missed departures in baseline eliminated by Dual-Gun & PdM."""
        dep_path = os.path.join(DATA_DIR, "departures_baseline.csv")
        df_dep = pd.read_csv(dep_path)
        s1_fails = df_dep[(df_dep["site_id"] == "S1") & (df_dep["depart_ts"].str.startswith("2026-11-13")) & (df_dep["below_required"] == 1)]
        self.assertEqual(len(s1_fails), 4)
        failed_buses = set(s1_fails["vehicle_id"])
        self.assertEqual(failed_buses, {"B09", "B18", "B20", "B04"})

        # In Sentinel mode with 24 plugs and early thermal PdM, 0 buses fail
        s1_res = ScenarioEngine().run_s1_scenario()
        self.assertEqual(s1_res["baseline_missed_departures"], 4)
        self.assertEqual(s1_res["optimized_missed_departures"], 0)
        self.assertGreaterEqual(s1_res["thermal_anomaly_audit"]["lead_time_before_f015_minutes"], 190.0)

    def test_s2_4_truck_dso_curtailment_remediation(self):
        """S2 Logistics: 4 trucks starved in baseline saved by lookahead pre-charging."""
        dep_path = os.path.join(DATA_DIR, "departures_baseline.csv")
        df_dep = pd.read_csv(dep_path)
        s2_fails = df_dep[(df_dep["site_id"] == "S2") & (df_dep["depart_ts"].str.startswith("2026-11-13")) & (df_dep["below_required"] == 1)]
        self.assertEqual(len(s2_fails), 4)
        failed_trucks = set(s2_fails["vehicle_id"])
        self.assertEqual(failed_trucks, {"T01", "T02", "T03", "T04"})

        # Grid curtailment G1 from grid_events.csv
        grid_path = os.path.join(DATA_DIR, "grid_events.csv")
        df_grid = pd.read_csv(grid_path)
        g1 = df_grid[df_grid["event_id"] == "G1"]
        self.assertEqual(len(g1), 1)
        self.assertEqual(float(g1["limit_kw"].iloc[0]), 400.0)

        # Sentinel eliminates missed departures
        s2_res = ScenarioEngine().run_s2_scenario()
        self.assertEqual(s2_res["baseline_missed_departures"], 4)
        self.assertEqual(s2_res["optimized_missed_departures"], 0)
        self.assertEqual(s2_res["baseline_deficit_kwh"], 283.50)

    def test_s3_highway_256_driver_offline_session(self):
        """S3 Highway: 29.7% abandonment (76 drivers) compressed via local DLM."""
        arr_path = os.path.join(DATA_DIR, "public_arrivals.csv")
        df_arr = pd.read_csv(arr_path)
        s3_arr = df_arr[(df_arr["site_id"] == "S3") & (df_arr["ts"].str.startswith("2026-11-13"))]
        total_drivers = len(s3_arr)
        abandoned = len(s3_arr[s3_arr["outcome"].isin(["left_full", "left_queue"])])
        self.assertEqual(total_drivers, 256)
        self.assertEqual(abandoned, 76)
        abandon_rate = (abandoned / total_drivers) * 100.0
        self.assertAlmostEqual(abandon_rate, 29.6875, places=1)

        # Sentinel offline islanding eliminates 50 kW bottleneck, maintaining full 1,425 kW DC / 1,492.15 kW AC
        s3_res = ScenarioEngine().run_s3_scenario()
        self.assertEqual(s3_res["offline_max_safe_dc_kw"], 1425.0)
        self.assertEqual(s3_res["offline_steady_ac_kw"], 1492.15)
        self.assertEqual(s3_res["offline_islanding_state"], "OFFLINE_ISLANDING")

    def test_s4_urban_hub_price_peak_and_cable_trip(self):
        """S4 Urban: BESS shaves 799.30 €/MWh peak, D4-2 cable trip isolated."""
        faults_path = os.path.join(DATA_DIR, "faults.csv")
        df_faults = pd.read_csv(faults_path)
        f017 = df_faults[df_faults["fault_id"] == "F017"]
        self.assertEqual(len(f017), 1)
        self.assertEqual(str(f017["site_id"].iloc[0]), "S4")
        self.assertEqual(str(f017["charger_id"].iloc[0]), "D4-2")
        self.assertEqual(str(f017["fault_category"].iloc[0]), "connector")

        s4_res = ScenarioEngine().run_s4_and_price_spike_scenario()
        self.assertEqual(s4_res["spot_spike_eur_mwh"], 799.30)
        self.assertEqual(len(s4_res["mpc_extreme_price_unmet_vehicles"]), 0)

    def test_s5_commissioning_digital_twin_self_healing(self):
        """S5 Depot: 5 missed departures in baseline eliminated by correcting D5-7/8."""
        dep_path = os.path.join(DATA_DIR, "departures_baseline.csv")
        df_dep = pd.read_csv(dep_path)
        s5_fails = df_dep[(df_dep["site_id"] == "S5") & (df_dep["depart_ts"].str.startswith("2026-11-13")) & (df_dep["below_required"] == 1)]
        self.assertEqual(len(s5_fails), 5)
        failed_buses = set(s5_fails["vehicle_id"])
        self.assertEqual(failed_buses, {"B28", "B35", "B33", "B34", "B27"})

        # Reconciled grid limit unlocks +750 kWh capacity, solving 508.95 kWh deficit
        s5_res = ScenarioEngine().run_s5_scenario()
        self.assertEqual(s5_res["baseline_missed_departures"], 5)
        self.assertEqual(s5_res["optimized_missed_departures"], 0)
        self.assertEqual(s5_res["three_way_reconciliation"]["unlocked_window_0330_0600_kwh"], 750.0)

    def test_commercial_21_fte_elimination_and_roi(self):
        """Commercial AEaaS: Honest 100-site labor (45 €/h = 87,750 €/FTE) and CAPEX audit."""
        labor = ROIAnalyzer.analyze_network_operations_labor()
        eq = ROIAnalyzer.analyze_equipment_and_payback()
        self.assertEqual(labor["total_ops_biweekly"], 8852)
        self.assertEqual(labor["total_minutes_biweekly"], 93412.0)
        self.assertEqual(labor["staff_hourly_rate_eur"], 45.0)
        self.assertEqual(labor["annual_cost_per_fte_eur"], 87750.0)
        self.assertEqual(labor["total_network_fte"], 20.76)
        self.assertEqual(labor["replug_network_fte"], 9.95)
        self.assertEqual(labor["replug_share_by_duration_pct"], 47.93)
        self.assertEqual(labor["total_network_annual_labor_eur"], 1821534.0)
        self.assertEqual(labor["replug_network_annual_labor_eur"], 872976.0)
        self.assertEqual(eq["installed_cost_per_gun_eur"], 27000.0)
        self.assertEqual(eq["s1_12_guns_total_capex_with_civil_eur"], 324000.0)
        self.assertEqual(eq["s1_payback_years_with_civil"], 13.31)
        self.assertEqual(eq["strategy_a_0capex_capex_eur"], 0.0)

    def test_one_page_sla_settlement_audit(self):
        """One-Page SLA engine produces non-negative itemized monthly settlements."""
        inv = SLACalculator.settle_monthly_invoice(
            monthly_base_fee=10000.0,
            avail_pct=98.50,
            delayed_records=[{"delay_min": 20.0, "mrdt_satisfied": True}],
            undercharged_records=[{"soc_req": 80.0, "soc_dep": 70.0, "cap_kwh": 300.0, "mrdt_satisfied": True}],
        )
        self.assertGreater(inv["monthly_base_fee_eur"], 0.0)
        self.assertGreaterEqual(inv["net_operator_invoice_eur"], 0.0)
        self.assertLessEqual(inv["capped_payout_eur"], inv["max_liability_cap_eur"])

    def test_network_grid_safety_invariant_all_intervals(self):
        """Official network_site_power.csv has 0 grid limit breaches across 134,400 intervals."""
        p_path = os.path.join(DATA_DIR, "network_site_power.csv")
        df_p = pd.read_csv(p_path)
        over_limit = df_p[df_p["grid_kw"] > df_p["grid_limit_kw"]]
        self.assertEqual(len(over_limit), 0)

    def test_closed_loop_scenario_day_master_reconciliation(self):
        """Master runner confirms 13 baseline missed departures drop to 0 on 2026-11-13."""
        master = ScenarioEngine().run_all_scenarios()
        self.assertEqual(master["scenario_day_missed_before"], 13)
        self.assertEqual(master["scenario_day_missed_after"], 0)

if __name__ == "__main__":
    unittest.main()
