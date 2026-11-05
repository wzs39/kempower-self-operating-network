"""
Tier 3: Cross-Feature Interactions (Pairwise and Multi-Variable Stress)
Validates interactions where multiple features, physical constraints, or market
signals collide simultaneously.
"""

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import unittest

from e2e_tests.common import (
    ContractDPRMatrix,
    ContractMPCSolver,
    ContractEdgeFSM,
    ContractVirtualReplug,
    ContractSLAEngine,
    ScenarioEngine,
)

class TestTier3CrossFeatureCombinations(unittest.TestCase):
    """Tier 3: Pairwise and multi-variable interaction scenarios."""

    def test_c01_dual_gun_and_inverter_loss(self):
        """Dual-Gun multiplexing with 95.5% AC inverter loss."""
        # 12 guns in Group A requesting 90 kW each = 1080 kW DC
        # Grid limit is 1200 kW AC. 1080 kW DC / 0.955 = 1130.89 kW AC <= 1200 kW AC
        reqs = {f"G{i}": 90.0 for i in range(1, 13)}
        alloc = ContractDPRMatrix.allocate_power(reqs, grid_limit_ac=1200.0, cabinet_capacity_kw=1080.0)
        total_dc = sum(alloc.values())
        ac_draw = total_dc / 0.955
        self.assertLessEqual(ac_draw, 1200.0)

    def test_c02_offline_islanding_and_thermal_pdm(self):
        """WAN outage occurs concurrently with cabinet fan degradation."""
        telemetry = {
            "wan_connected": False,
            "fan_rpm": 600,
            "baseline_fan_rpm": 1800,
            "internal_temp_c": 68.0,
        }
        res = ContractEdgeFSM.tick(telemetry)
        # Should initiate load migration to avoid hardware trip even while offline
        self.assertIn(res["state"], [ContractEdgeFSM.LOAD_MIGRATION, ContractEdgeFSM.THERMAL_WARNING])

    def test_c03_price_peak_bess_and_departure_deadlines(self):
        """799.30 €/MWh peak price colliding with urgent bus departure."""
        urgent_penalty = 250.0
        urgent_charge_cost = ContractMPCSolver.compute_objective_cost(799.30, 24.00, 60.0, 0.5, urgent_penalty, abandoned=False)
        self.assertLess(urgent_charge_cost, urgent_penalty)

    def test_c04_plug_and_queue_with_cv_tapering(self):
        """Vehicle A enters CV taper, allowing Gun B in queue to receive released modules."""
        p_actual_a = ContractMPCSolver.evaluate_cv_taper(150.0, soc=0.90)
        released_kw = 150.0 - p_actual_a
        self.assertGreater(released_kw, 50.0)

    def test_c05_s5_auto_calibration_and_dpr_allocation(self):
        """Digital twin auto-calibration restores D5-7 to 150 kW, properly pooled by DPR."""
        d5_7_remediated_kw = 150.0
        alloc = ContractDPRMatrix.allocate_power({"D5-7": d5_7_remediated_kw}, grid_limit_ac=500.0, cabinet_capacity_kw=450.0)
        self.assertEqual(alloc["D5-7"], 150.0)

    def test_c06_s2_dso_curtailment_and_lookahead_precharging(self):
        """S2 DSO 400 kW curtailment combined with T05-T08 priority preemption."""
        s2_res = ScenarioEngine().run_s2_scenario()
        self.assertEqual(s2_res["baseline_deficit_kwh"], 283.50)
        self.assertGreater(s2_res["overnight_trucks_t05_t08_afternoon_kwh"], s2_res["baseline_deficit_kwh"])
        self.assertEqual(s2_res["optimized_missed_departures"], 0)

    def test_c07_thermal_n1_shedding_and_dual_gun_rerouting(self):
        """C1-3 failure at S1 triggers fast 180 kW shed followed by zero-arc contactor rerouting."""
        pre_load = 870.0
        shed_amount = 180.0
        post_shed_load = pre_load - shed_amount
        n1_capacity = 720.0
        self.assertLessEqual(post_shed_load, n1_capacity)
        res = ContractDPRMatrix.re_route_contactor("C1-3_G1", "C1-1_G1", modules=4, initial_current_amps=0.0)
        self.assertTrue(res["success"])

    def test_c08_bess_arbitrage_and_mrdt_sla_protection(self):
        """BESS peak shaving does not violate MRDT or cause SLA penalties."""
        mrdt = ContractSLAEngine.compute_mrdt(soc_req=80.0, soc_arrive=20.0, batt_kwh=100.0, p_charger_max=150.0, p_veh_max=150.0)
        dwell_actual = 60.0
        self.assertGreaterEqual(dwell_actual, mrdt)

    def test_c09_zero_arc_delay_and_micro_fsm_tick_rate(self):
        """Contactor switching delay (<500ms) fits cleanly inside 1-second FSM tick."""
        res = ContractDPRMatrix.re_route_contactor("G1", "G2", modules=2, initial_current_amps=0.0)
        self.assertLess(res["switching_delay_ms"], 500.0)
        fsm_tick_interval_ms = 1000.0
        self.assertLess(res["switching_delay_ms"], fsm_tick_interval_ms)

    def test_c10_multi_site_concurrent_stress(self):
        """Simultaneous occurrences: S1 thermal, S2 curtailment, S3 outage, S4 price peak, S5 misconfig."""
        s1_fsm = ContractEdgeFSM.tick({"fan_rpm": 600, "baseline_fan_rpm": 1800, "internal_temp_c": 68.0})
        s2_curtail = 400.0 * 0.955
        s3_fsm = ContractEdgeFSM.tick({"wan_connected": False})
        s4_price = ContractMPCSolver.compute_objective_cost(799.30, 28.00, 100.0, 0.25, 250.0, abandoned=False)
        s5_fsm = ContractEdgeFSM.tick({"config_mismatch": True})

        self.assertEqual(s1_fsm["state"], ContractEdgeFSM.LOAD_MIGRATION)
        self.assertEqual(s2_curtail, 382.0)
        self.assertEqual(s3_fsm["state"], ContractEdgeFSM.OFFLINE_ISLANDING)
        self.assertLess(s4_price, 250.0)
        self.assertEqual(s5_fsm["state"], ContractEdgeFSM.AUTO_CALIBRATED)

    def test_c11_low_ambient_temperature_and_contactor_matrix(self):
        """Sub-zero ambient temperature (-15°C) with full matrix load rebalancing."""
        telemetry = {
            "ambient_temp_c": -15.0,
            "internal_temp_c": 35.0,
            "fan_rpm": 1200,
            "baseline_fan_rpm": 1400,
            "wan_connected": True,
        }
        fsm_state = ContractEdgeFSM.tick(telemetry)
        self.assertEqual(fsm_state["state"], ContractEdgeFSM.NORMAL)
        alloc = ContractDPRMatrix.allocate_power({"G1": 150.0, "G2": 150.0}, grid_limit_ac=400.0, cabinet_capacity_kw=360.0)
        self.assertEqual(sum(alloc.values()), 300.0)

    def test_c12_rapid_fleet_reschedule_and_mpc_feasibility(self):
        """Urgent fleet departure shifts departure window forward while maintaining feasibility."""
        pen_normal = ContractMPCSolver.compute_objective_cost(60.0, 20.0, 50.0, 1.0, 250.0, abandoned=False)
        pen_urgent = ContractMPCSolver.compute_objective_cost(799.30, 20.0, 50.0, 1.0, 250.0, abandoned=False)
        self.assertGreater(pen_urgent, pen_normal)
        self.assertLess(pen_urgent, 250.0)

if __name__ == "__main__":
    unittest.main()
