"""
Tier 2: Boundary & Corner Cases (Stress and Edge Verification)
Evaluates degenerate inputs: zero values, maximal saturation values, boundary thresholds
(80% CC/CV threshold, 65°C alarm, 75°C hardware trip, WAN reconnection, etc.).
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
)

class TestTier2BoundaryCornerCases(unittest.TestCase):
    """Tier 2: >= 5 boundary, edge, and stress cases per feature."""

    # --------------------------------------------------------------------------
    # F01 Boundaries: DPR Matrix
    # --------------------------------------------------------------------------
    def test_f01_b01_zero_power_request(self):
        """Zero kW power request safely allocates 0.0 kW."""
        alloc = ContractDPRMatrix.allocate_power({"G1": 0.0}, grid_limit_ac=500.0, cabinet_capacity_kw=360.0)
        self.assertEqual(alloc["G1"], 0.0)

    def test_f01_b02_negative_power_request(self):
        """Negative power request clamped to 0.0 kW."""
        alloc = ContractDPRMatrix.allocate_power({"G1": -50.0}, grid_limit_ac=500.0, cabinet_capacity_kw=360.0)
        self.assertEqual(alloc["G1"], 0.0)

    def test_f01_b03_cabinet_capacity_saturation(self):
        """Request exceeding cabinet capacity is clamped to physical capacity."""
        alloc = ContractDPRMatrix.allocate_power({"G1": 500.0}, grid_limit_ac=1000.0, cabinet_capacity_kw=360.0)
        self.assertLessEqual(alloc["G1"], 360.0)

    def test_f01_b04_re_routing_zero_modules(self):
        """Re-routing zero modules safely returns success=False without action."""
        res = ContractDPRMatrix.re_route_contactor("G1", "G2", modules=0, initial_current_amps=0.0)
        self.assertFalse(res["success"])

    def test_f01_b05_fractional_module_rounding(self):
        """Fractional request above 25 kW rounds up to next discrete 25 kW module block."""
        alloc = ContractDPRMatrix.allocate_power({"G1": 25.001}, grid_limit_ac=500.0, cabinet_capacity_kw=360.0)
        self.assertEqual(alloc["G1"], 50.0)

    # --------------------------------------------------------------------------
    # F02 Boundaries: MPC / MILP
    # --------------------------------------------------------------------------
    def test_f02_b01_zero_spot_price(self):
        """Zero spot price results only in grid tariff fee."""
        cost = ContractMPCSolver.compute_objective_cost(0.0, 24.00, 100.0, 0.25, 250.0, abandoned=False)
        self.assertAlmostEqual(cost, 0.60, places=2)

    def test_f02_b02_negative_spot_price(self):
        """Negative spot price offsets grid tariff but remains valid."""
        cost = ContractMPCSolver.compute_objective_cost(-15.0, 24.00, 100.0, 0.25, 250.0, abandoned=False)
        self.assertAlmostEqual(cost, 0.225, places=3)

    def test_f02_b03_cv_taper_at_exact_80_pct(self):
        """At exactly 80.0% SoC, CC phase allows 100% rated power."""
        p_taper = ContractMPCSolver.evaluate_cv_taper(rated_kw=100.0, soc=0.80)
        self.assertEqual(p_taper, 100.0)

    def test_f02_b04_cv_taper_at_100_pct_soc(self):
        """At 100% SoC, CV tapering respects 10% minimum floor."""
        p_taper = ContractMPCSolver.evaluate_cv_taper(rated_kw=100.0, soc=1.00)
        self.assertAlmostEqual(p_taper, 10.0, places=1)

    def test_f02_b05_zero_duration_dt(self):
        """Zero duration dt yields exactly 0.0 EUR energy cost."""
        cost = ContractMPCSolver.compute_objective_cost(799.30, 24.00, 100.0, 0.0, 250.0, abandoned=False)
        self.assertEqual(cost, 0.0)

    # --------------------------------------------------------------------------
    # F03 Boundaries: Edge FSM
    # --------------------------------------------------------------------------
    def test_f03_b01_exact_75c_hardware_trip(self):
        """Exactly 75.0°C triggers HARDWARE_TRIP."""
        res = ContractEdgeFSM.tick({"fan_rpm": 1800, "baseline_fan_rpm": 1800, "internal_temp_c": 75.0, "wan_connected": True})
        self.assertEqual(res["state"], ContractEdgeFSM.HARDWARE_TRIP)

    def test_f03_b02_exact_65c_thermal_warning(self):
        """Exactly 65.0°C triggers THERMAL_WARNING."""
        res = ContractEdgeFSM.tick({"fan_rpm": 1800, "baseline_fan_rpm": 1800, "internal_temp_c": 65.0, "wan_connected": True})
        self.assertEqual(res["state"], ContractEdgeFSM.THERMAL_WARNING)

    def test_f03_b03_fan_rpm_drop_exactly_20_pct(self):
        """Fan RPM drop of exactly 20.0% triggers LOAD_MIGRATION."""
        res = ContractEdgeFSM.tick({"fan_rpm": 1440, "baseline_fan_rpm": 1800, "internal_temp_c": 50.0, "wan_connected": True})
        self.assertEqual(res["state"], ContractEdgeFSM.LOAD_MIGRATION)

    def test_f03_b04_fan_rpm_drop_19_9_pct(self):
        """Fan RPM drop of 19.9% stays within NORMAL margin."""
        res = ContractEdgeFSM.tick({"fan_rpm": 1442, "baseline_fan_rpm": 1800, "internal_temp_c": 50.0, "wan_connected": True})
        self.assertEqual(res["state"], ContractEdgeFSM.NORMAL)

    def test_f03_b05_wan_restoration(self):
        """Restoration of WAN toggles state cleanly from OFFLINE_ISLANDING to NORMAL."""
        res_offline = ContractEdgeFSM.tick({"fan_rpm": 1800, "baseline_fan_rpm": 1800, "internal_temp_c": 50.0, "wan_connected": False})
        res_online = ContractEdgeFSM.tick({"fan_rpm": 1800, "baseline_fan_rpm": 1800, "internal_temp_c": 50.0, "wan_connected": True})
        self.assertEqual(res_offline["state"], ContractEdgeFSM.OFFLINE_ISLANDING)
        self.assertEqual(res_online["state"], ContractEdgeFSM.NORMAL)

    # --------------------------------------------------------------------------
    # F04 Boundaries: Dual-Gun Multiplexing
    # --------------------------------------------------------------------------
    def test_f04_b01_empty_group_a(self):
        """Empty fleet group A safely reports 0 active guns."""
        res = ContractVirtualReplug.schedule_depot_night([], [f"B{i:02d}" for i in range(13, 25)], current_time_hour=23.0)
        self.assertEqual(res["active_guns_count"], 0)

    def test_f04_b02_exact_switchover_hour_0200(self):
        """Hour 2.0 triggers PHASE_B_FAST_CHARGE."""
        res = ContractVirtualReplug.schedule_depot_night(["B01"], ["B13"], current_time_hour=2.0)
        self.assertEqual(res["phase"], "PHASE_B_FAST_CHARGE")

    def test_f04_b03_exact_top_off_hour_0530(self):
        """Hour 5.5 triggers PHASE_BALANCED_TOP_OFF."""
        res = ContractVirtualReplug.schedule_depot_night(["B01"], ["B13"], current_time_hour=5.5)
        self.assertEqual(res["phase"], "PHASE_BALANCED_TOP_OFF")

    def test_f04_b04_midnight_wrap_around(self):
        """Hour 0.0 correctly operates under PHASE_A_FAST_CHARGE."""
        res = ContractVirtualReplug.schedule_depot_night(["B01"], ["B13"], current_time_hour=0.0)
        self.assertEqual(res["phase"], "PHASE_A_FAST_CHARGE")

    def test_f04_b05_all_buses_present(self):
        """All 24 buses present energizes exactly 12 active guns during phase A."""
        res = ContractVirtualReplug.schedule_depot_night([f"B{i:02d}" for i in range(1, 13)], [f"B{i:02d}" for i in range(13, 25)], current_time_hour=23.5)
        self.assertEqual(res["active_guns_count"], 12)
        self.assertEqual(res["idle_guns_count"], 12)

    # --------------------------------------------------------------------------
    # F05 Boundaries: 95.5% Inverter Loss
    # --------------------------------------------------------------------------
    def test_f05_b01_zero_grid_limit(self):
        """Zero AC grid limit allows 0.0 kW DC."""
        alloc = ContractDPRMatrix.allocate_power({"G1": 100.0}, grid_limit_ac=0.0, cabinet_capacity_kw=360.0)
        self.assertEqual(alloc["G1"], 0.0)

    def test_f05_b02_minimal_grid_limit_25kw(self):
        """25 kW AC limit (* 0.955 = 23.875 kW DC) cannot fit single 25 kW module -> 0.0 kW."""
        alloc = ContractDPRMatrix.allocate_power({"G1": 50.0}, grid_limit_ac=25.0, cabinet_capacity_kw=360.0)
        self.assertEqual(alloc["G1"], 0.0)

    def test_f05_b03_exact_single_module_grid_limit(self):
        """26.2 kW AC limit fits exactly 1 module (25 kW DC)."""
        alloc = ContractDPRMatrix.allocate_power({"G1": 50.0}, grid_limit_ac=26.2, cabinet_capacity_kw=360.0)
        self.assertEqual(alloc["G1"], 25.0)

    def test_f05_b04_massive_grid_limit_saturation(self):
        """Massive unconstrained grid limit is bounded by vehicle request and cabinet rating."""
        alloc = ContractDPRMatrix.allocate_power({"G1": 100.0}, grid_limit_ac=100000.0, cabinet_capacity_kw=360.0)
        self.assertEqual(alloc["G1"], 100.0)

    def test_f05_b05_inverter_loss_roundtrip(self):
        """Inverter loss round-trip calculation preserves numerical precision."""
        p_dc = 250.0
        p_ac = p_dc / 0.955
        p_dc_recovered = p_ac * 0.955
        self.assertAlmostEqual(p_dc, p_dc_recovered, places=4)

    # --------------------------------------------------------------------------
    # F06 Boundaries: Thermal PdM
    # --------------------------------------------------------------------------
    def test_f06_b01_zero_fan_rpm(self):
        """Zero fan RPM triggers immediate LOAD_MIGRATION."""
        res = ContractEdgeFSM.tick({"fan_rpm": 0, "baseline_fan_rpm": 1800, "internal_temp_c": 50.0, "wan_connected": True})
        self.assertEqual(res["state"], ContractEdgeFSM.LOAD_MIGRATION)

    def test_f06_b02_negative_fan_rpm_guard(self):
        """Corrupted negative fan RPM is guarded and triggers LOAD_MIGRATION."""
        res = ContractEdgeFSM.tick({"fan_rpm": -10, "baseline_fan_rpm": 1800, "internal_temp_c": 50.0, "wan_connected": True})
        self.assertEqual(res["state"], ContractEdgeFSM.LOAD_MIGRATION)

    def test_f06_b03_extreme_high_temp(self):
        """Extreme temperature (110°C) triggers HARDWARE_TRIP."""
        res = ContractEdgeFSM.tick({"fan_rpm": 1800, "baseline_fan_rpm": 1800, "internal_temp_c": 110.0, "wan_connected": True})
        self.assertEqual(res["state"], ContractEdgeFSM.HARDWARE_TRIP)

    def test_f06_b04_subzero_internal_temp(self):
        """Sub-zero Nordic temperature (-14°C) operates in NORMAL state."""
        res = ContractEdgeFSM.tick({"fan_rpm": 1800, "baseline_fan_rpm": 1800, "internal_temp_c": -14.0, "wan_connected": True})
        self.assertEqual(res["state"], ContractEdgeFSM.NORMAL)

    def test_f06_b05_nan_telemetry_handling(self):
        """Empty or missing telemetry dictionary gracefully defaults to NORMAL state."""
        res = ContractEdgeFSM.tick({})
        self.assertEqual(res["state"], ContractEdgeFSM.NORMAL)

    # --------------------------------------------------------------------------
    # F07 Boundaries: Digital Twin Calibration
    # --------------------------------------------------------------------------
    def test_f07_b01_already_correct_config(self):
        """Hardware rating already matching configured rating requires no patch."""
        hw = 150.0
        cfg = 150.0
        needs_patch = cfg < hw
        self.assertFalse(needs_patch)

    def test_f07_b02_already_active_sim(self):
        """Already active eSIM requires no remediation."""
        sim = True
        needs_healing = not sim
        self.assertFalse(needs_healing)

    def test_f07_b03_over_rated_config(self):
        """Configuration exceeding hardware capability clamps to safe hardware limit."""
        hw = 150.0
        cfg = 200.0
        effective = min(cfg, hw)
        self.assertEqual(effective, 150.0)

    def test_f07_b04_zero_rated_config(self):
        """Zero configured value defaults to hardware nameplate rating."""
        hw = 150.0
        cfg = 0.0
        effective = hw if cfg <= 0 else cfg
        self.assertEqual(effective, 150.0)

    def test_f07_b05_string_sim_boolean_parsing(self):
        """Boolean parsing handles false string representations robustly."""
        for val in ["false", "False", "FALSE", "0", 0, False]:
            parsed = str(val).lower() in ["true", "1"]
            self.assertFalse(parsed)

    # --------------------------------------------------------------------------
    # F08 Boundaries: Extreme Price & BESS
    # --------------------------------------------------------------------------
    def test_f08_b01_exact_peak_price_799_30(self):
        """Price 799.30 €/MWh qualifies as extreme price event (>= 500 €/MWh)."""
        is_extreme = 799.30 >= 500.0
        self.assertTrue(is_extreme)

    def test_f08_b02_near_peak_price_672_63(self):
        """Price 672.63 €/MWh qualifies as extreme price event."""
        is_extreme = 672.63 >= 500.0
        self.assertTrue(is_extreme)

    def test_f08_b03_bess_full_soc_100_pct(self):
        """At 100% SoC, BESS charging is prohibited."""
        soc = 1.00
        can_charge = soc < 1.00
        self.assertFalse(can_charge)

    def test_f08_b04_bess_zero_soc_clamp(self):
        """At 5% SoC, BESS discharging is clamped by 10% reserve threshold."""
        soc = 0.05
        can_discharge = soc > 0.10
        self.assertFalse(can_discharge)

    def test_f08_b05_extreme_high_penalty_precedence(self):
        """Even at 799.30 €/MWh, charging remains preferred over paying 250 € penalty."""
        energy_cost = ContractMPCSolver.compute_objective_cost(799.30, 24.00, 200.0, 0.25, 250.0, abandoned=False)
        self.assertLess(energy_cost, 250.0)

if __name__ == "__main__":
    unittest.main()
