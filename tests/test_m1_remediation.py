"""
Comprehensive Verification Suite for Milestone 1 Remediation (F01..F06).
File: tests/test_m1_remediation.py
"""

import unittest
import csv
from pathlib import Path
from datetime import datetime

from src.core.dpr_matrix import (
    DPRMatrix,
    STATION_CABINET_TOPOLOGY,
    DPR_MODULAR_SWITCH_DELAY_MS,
    CONTACTOR_MAX_SWITCH_DELAY_MS,
)
from src.core.self_healing import (
    PredictiveThermalEngine,
    CabinetTelemetry,
    N1_MACRO_TRANSFER_DELAY_MS,
)
from src.core.mpc_optimizer import (
    MPCOptimizer,
    SiteMPCConfig,
    VehicleSchedule,
)
from src.commercial.roi_analyzer import ROIAnalyzer
from src.commercial.sla_calculator import SLACalculator
from src.sim.discrete_sim import (
    simulate_closed_loop_minute_by_minute,
)
from src.sim.scenario_engine import ScenarioEngine
from src.sim.data_loader import KempowerDataLoader
from src.utils.paths import resolve_csv_path


class TestM1RemediationSuite(unittest.TestCase):
    """Rigorous end-to-end unit tests verifying all M1 bug fixes and engines."""

    # ------------------------------------------------------------------------
    # 1. P0-1 (F01): DPR Matrix Prefix Collision Bug Fix
    # ------------------------------------------------------------------------
    def test_p0_1_prefix_collision_s1_12_guns_full_1080kw(self):
        """Under S1 12-gun full load, each cabinet delivers 360 kW, totaling 1,080 kW DC."""
        dpr = DPRMatrix("S1")
        reqs = {f"D1-{i}": 150.0 for i in range(1, 13)}
        alloc = dpr.allocate_intra_cabinet_continuous(reqs, grid_limit_kw=1200.0)
        self.assertAlmostEqual(sum(alloc.values()), 1080.0, places=2)

        cabinet_expected = {
            "C1-1": ["D1-1", "D1-2", "D1-3", "D1-4"],
            "C1-2": ["D1-5", "D1-6", "D1-7", "D1-8"],
            "C1-3": ["D1-9", "D1-10", "D1-11", "D1-12"],
        }
        for cab, guns in cabinet_expected.items():
            cab_sum = sum(alloc[g] for g in guns)
            self.assertAlmostEqual(cab_sum, 360.0, places=2)
            for g in guns:
                self.assertAlmostEqual(alloc[g], 90.0, places=2)

    def test_p0_1_cross_cabinet_prohibition_rejection(self):
        """Requesting D1-10 on C1-1 must raise ValueError (prohibits cross-cabinet routing)."""
        dpr = DPRMatrix("S1")
        with self.assertRaises(ValueError):
            dpr.allocate_intra_cabinet_continuous("C1-1", {"D1-10": 100.0})

    # ------------------------------------------------------------------------
    # 2. P1-1 (F05): Switching Delay Reconciliation
    # ------------------------------------------------------------------------
    def test_p1_1_switching_delay_constants_and_scaling(self):
        """Verifies modular 260ms BBM delay vs macro 2,630ms breaker transfer delay."""
        self.assertEqual(DPR_MODULAR_SWITCH_DELAY_MS, 260.0)
        self.assertEqual(N1_MACRO_TRANSFER_DELAY_MS, 2630.0)
        self.assertLess(DPR_MODULAR_SWITCH_DELAY_MS, CONTACTOR_MAX_SWITCH_DELAY_MS)

        dpr = DPRMatrix("S1")
        seq_zero = dpr.re_route_contactor(from_gun="D1-1", to_gun="D1-2", modules=2, initial_current_amps=0.0)
        self.assertEqual(seq_zero.total_duration_ms, 260.0)

        seq_loaded = dpr.re_route_contactor(from_gun="D1-1", to_gun="D1-2", modules=2, initial_current_amps=100.0)
        self.assertGreater(seq_loaded.total_duration_ms, 260.0)
        self.assertTrue(seq_loaded.is_zero_arc_compliant)

    # ------------------------------------------------------------------------
    # 3. P1-2 (F05): Module Topology Alignment across S1-S5
    # ------------------------------------------------------------------------
    def test_p1_2_no_phantom_cabinets_across_all_stations(self):
        """Verifies that no station generates phantom cabinets outside STATION_CABINET_TOPOLOGY."""
        for st in ["S1", "S2", "S3", "S4", "S5"]:
            dpr = DPRMatrix(st)
            valid_cabs = set(STATION_CABINET_TOPOLOGY[st].keys())
            module_cabs = set(m.cabinet_id for m in dpr.modules.values())
            self.assertTrue(
                module_cabs.issubset(valid_cabs),
                f"{st} contains invalid phantom cabinets: {module_cabs - valid_cabs}"
            )

        # S1 must have 43 modules (15 in C1-1, 15 in C1-2, 13 in C1-3)
        dpr_s1 = DPRMatrix("S1")
        self.assertEqual(len(dpr_s1.modules), 43)
        self.assertEqual(sum(1 for m in dpr_s1.modules.values() if m.cabinet_id == "C1-1"), 15)
        self.assertEqual(sum(1 for m in dpr_s1.modules.values() if m.cabinet_id == "C1-2"), 15)
        self.assertEqual(sum(1 for m in dpr_s1.modules.values() if m.cabinet_id == "C1-3"), 13)

    # ------------------------------------------------------------------------
    # 4. P1-3 (F05): Decoupled Grid Safety & DLM Throttling Fields
    # ------------------------------------------------------------------------
    def test_p1_3_decoupled_safety_and_throttling_audit(self):
        """When greedy vehicle requests power exceeding grid, is_safe remains True and is_throttled is True."""
        dpr = DPRMatrix("S4")
        res = dpr.allocate_power("S4", {"G_greedy": 1000.0}, grid_limit_ac=600.0)
        self.assertTrue(res.is_safe)
        self.assertTrue(res.is_throttled)
        self.assertTrue(res.raw_exceeds_grid)
        self.assertEqual(res.raw_requested_kw, 1000.0)
        self.assertAlmostEqual(res.dc_total_kw, 550.0, places=1)
        self.assertAlmostEqual(res.unmet_power_kw, 450.0, places=1)
        self.assertLessEqual(res.ac_grid_draw_kw, 600.0)

    # ------------------------------------------------------------------------
    # 5. F02: App Launch Crash Fix in ROIAnalyzer
    # ------------------------------------------------------------------------
    def test_f02_roi_analyzer_computes_from_official_csvs(self):
        """ROIAnalyzer computes monthly peak fee vs 14d energy cost directly from official CSVs."""
        res = ROIAnalyzer.analyze_monthly_peak_demand_vs_energy()
        self.assertEqual(res["s1_s5_monthly_peak_demand_fee_eur"], 31788.25)
        self.assertEqual(res["s1_s5_energy_cost_14d_eur"], 29978.00)
        self.assertEqual(res["s1_s5_revenue_14d_eur"], 115903.99)
        self.assertTrue(res["peak_demand_exceeds_14d_energy_cost"])

    # ------------------------------------------------------------------------
    # 6. F03 (P0-2): Closed-Loop Discrete Simulation Engine Integration
    # ------------------------------------------------------------------------
    def test_f03_discrete_sim_yields_zero_missed_departures(self):
        """Minute-by-minute simulation eliminates missed departures dynamically across S1, S2, S5."""
        s1 = simulate_closed_loop_minute_by_minute("S1")
        s2 = simulate_closed_loop_minute_by_minute("S2")
        s5 = simulate_closed_loop_minute_by_minute("S5")

        self.assertEqual(s1["missed_departures"], 0)
        self.assertEqual(s2["missed_departures"], 0)
        self.assertEqual(s5["missed_departures"], 0)

        self.assertEqual(s1["deficit_kwh"], 0.0)
        self.assertEqual(s2["deficit_kwh"], 0.0)
        self.assertEqual(s5["deficit_kwh"], 0.0)

    def test_f03_scenario_engine_closed_loop_verification(self):
        """ScenarioEngine executes dynamic discrete simulation and reports 13 -> 0 missed departures."""
        engine = ScenarioEngine(KempowerDataLoader())
        res = engine.run_all_scenarios()
        self.assertEqual(res["scenario_day_missed_before"], 13)
        self.assertEqual(res["scenario_day_missed_after"], 0)

    # ------------------------------------------------------------------------
    # 7. F04 (P0-3): Predictive Thermal Calibration & False Alarm Elimination
    # ------------------------------------------------------------------------
    def test_f04_thermal_calibration_and_precursor(self):
        """Calibrated thermal engine produces 0 false alarms on unmonitored rows and captures 22:31 precursor."""
        t_path = resolve_csv_path("telemetry_1min.csv")
        pdm = PredictiveThermalEngine()
        alerts = []
        with open(t_path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cid = row["charger_id"]
                raw_t = row.get("cabinet_temp_c", "").strip()
                raw_rpm = row.get("fan_rpm", "").strip()
                t_c = float(raw_t) if raw_t else 0.0
                rpm = float(raw_rpm) if raw_rpm else None
                cab = CabinetTelemetry(cid, t_c, rpm)
                trip, mig, warn, _, _, _ = pdm.evaluate_cabinet(cab)
                if trip or mig or warn:
                    alerts.append((row["ts"], cid, t_c, rpm))

        d3_d4_alerts = [a for a in alerts if a[1] in ["D3-3", "D4-2"]]
        self.assertEqual(len(d3_d4_alerts), 0, "Expected 0 false alarms on unmonitored D3-3 and D4-2")

        d1_9_2231 = [a for a in alerts if a[1] == "D1-9" and "2026-11-12T22:31" in a[0]]
        self.assertGreater(len(d1_9_2231), 0, "D1-9 at 22:31 precursor was missed")

    # ------------------------------------------------------------------------
    # 8. P1-4 (F05): Physical Gun Capacity Limit Constraint in MILP
    # ------------------------------------------------------------------------
    def test_p1_4_milp_physical_gun_capacity_constraint(self):
        """When 16 vehicles request power simultaneously on a 12-gun station, at most 12 guns are active."""
        cfg = SiteMPCConfig(site_id="S1", transformer_max_kw=1200.0, num_guns=12)
        mpc = MPCOptimizer(config=cfg)
        vehicles = [
            VehicleSchedule(f"Bus_{i:02d}", 0, 4, 0.20, 0.80, 200.0, 100.0)
            for i in range(16)
        ]
        plan = mpc.solve_15min_horizon([50.0] * 4, vehicles)
        self.assertTrue(plan.is_optimal)
        for t in range(4):
            active_now = sum(1 for v in vehicles if plan.vehicle_dc_power_kw[v.vehicle_id][t] > 0.0)
            self.assertLessEqual(active_now, 12, f"Step {t} exceeded physical 12 gun limit: {active_now}")

    # ------------------------------------------------------------------------
    # 9. P1-5 (F05): Rolling Horizon Peak Fee Deduplication
    # ------------------------------------------------------------------------
    def test_p1_5_rolling_peak_fee_deduplication(self):
        """Demands below existing_peak_kw incur zero incremental peak fees."""
        cfg = SiteMPCConfig(site_id="S1", peak_fee_eur_kw_mo=6.50, use_full_monthly_peak_fee=True)
        mpc = MPCOptimizer(config=cfg)
        vehicles = [VehicleSchedule("B1", 0, 4, 0.20, 0.80, 100.0, 100.0)]

        # Run with existing_peak_kw = 500.0
        plan = mpc.solve_15min_horizon([30.0] * 4, vehicles, existing_peak_kw=500.0)
        self.assertTrue(plan.is_optimal)
        # B1 charges up to ~100 kW, which is well below 500 kW established peak
        self.assertEqual(plan.peak_cost_eur, 0.0)

    # ------------------------------------------------------------------------
    # 10. P1-6 (F05): Contract Penalty Connected to Optimization Slack
    # ------------------------------------------------------------------------
    def test_p1_6_contract_penalty_slack_weight_scaling(self):
        """Zero-penalty vehicle is deprioritized during extreme prices, while high-penalty vehicle is charged."""
        cfg = SiteMPCConfig(site_id="S4", transformer_max_kw=600.0)
        mpc = MPCOptimizer(config=cfg)
        v_no_pen = VehicleSchedule("V_FREE", 0, 4, 0.20, 0.80, 100.0, 100.0, penalty_eur=0.0)
        v_high_pen = VehicleSchedule("V_VIP", 0, 4, 0.20, 0.80, 100.0, 100.0, penalty_eur=900.0)

        # Under 799.30 €/MWh price spike
        prices = [799.30] * 4
        plan = mpc.solve_15min_horizon(prices, [v_no_pen, v_high_pen])
        self.assertTrue(plan.is_optimal)
        # VIP vehicle with 900€ penalty is charged to required 80%, while 0€ penalty vehicle is shed to avoid price spike
        self.assertAlmostEqual(plan.vehicle_soc["V_VIP"][-1], 0.80, places=2)
        self.assertAlmostEqual(plan.vehicle_soc["V_FREE"][-1], 0.20, places=2)

    # ------------------------------------------------------------------------
    # 11. P1-7 (F05): Parameterized SLA Threshold and Non-Negative Net Invoice
    # ------------------------------------------------------------------------
    def test_p1_7_sla_threshold_and_non_negative_invoice(self):
        """Verifies parameterized uptime target and clamping of net invoice to >= 0."""
        # Contract with 97.0% SLA: achieving 97.0% pays 0 deduction
        ded_97 = SLACalculator.compute_availability_deduction(5000.0, 97.0, uptime_sla_pct=97.0)
        self.assertEqual(ded_97, 0.0)

        # Net invoice under massive claims cannot go below 0 (operator never pays customer on an invoice)
        inv = SLACalculator.settle_monthly_invoice(
            monthly_base_fee=5000.0,
            avail_pct=80.0,
            delayed_records=[{"min": 120, "mrdt_satisfied": True}],
            undercharged_records=[{"soc_req": 90, "soc_dep": 30, "cap_kwh": 400, "mrdt_satisfied": True}],
            cap_multiplier=1.50,
        )
        self.assertGreaterEqual(inv["net_operator_invoice_eur"], 0.0)
        self.assertEqual(inv["net_operator_invoice_eur"], 0.0)

    # ------------------------------------------------------------------------
    # 12. F06: Packaging & Requirements File
    # ------------------------------------------------------------------------
    def test_f06_requirements_file_exists(self):
        """requirements.txt exists at repository root with all expected core dependencies."""
        req_path = Path(__file__).resolve().parent.parent / "requirements.txt"
        self.assertTrue(req_path.is_file(), "requirements.txt must exist at repo root")
        content = req_path.read_text(encoding="utf-8")
        for pkg in ["numpy", "scipy", "pandas", "streamlit", "cryptography", "pydantic", "pytest"]:
            self.assertIn(pkg, content, f"Package {pkg} missing from requirements.txt")


if __name__ == "__main__":
    unittest.main()
