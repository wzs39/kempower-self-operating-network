"""
Adversarial Empirical Challenge Probe for Milestone 1 Core Engine
Target Codebase:
  - src/core/dpr_matrix.py
  - src/core/virtual_replug.py
  - src/core/mpc_optimizer.py

Auditor / Author: m1_challenger_1 (Critic / Specialist)
Date: 2026-11-05
"""

import math
import random
import time
import unittest
from typing import Dict, List

import numpy as np

import src.core as sc
from src.core.dpr_matrix import (
    DPRMatrix,
    MODULE_POWER_KW,
    INVERTER_EFFICIENCY,
    CONTACTOR_MAX_SWITCH_DELAY_MS,
    ContactorState,
)
from src.core.virtual_replug import (
    VirtualReplugManager,
    PlugAndQueueHub,
    BusState,
    PlugType,
    PlugState,
    DualGunDispatchResult,
)
from src.core.mpc_optimizer import (
    MPCOptimizer,
    VehicleSchedule,
    BESSConfig,
    SiteMPCConfig,
    DispatchPlan,
)


class TestDPRMatrixAdversarial(unittest.TestCase):
    """Adversarial stress testing of Kempower 25 kW DPR Contactor Matrix."""

    def setUp(self):
        self.dpr_s1 = DPRMatrix(station_id="S1")  # 43 modules, 1075 kW DC
        self.dpr_s3 = DPRMatrix(station_id="S3")  # 57 modules, 1425 kW DC
        self.dpr_s4 = DPRMatrix(station_id="S4")  # 24 modules, 600 kW DC

    def test_zero_power_request(self):
        """Zero requested power across all dispensers must yield zero DC/AC draw safely."""
        res = self.dpr_s1.allocate_power("S1", {"G1": 0.0, "G2": 0.0, "G3": 0.0}, 1200.0)
        self.assertTrue(res.is_safe)
        self.assertEqual(res.dc_total_kw, 0.0)
        self.assertEqual(res.ac_grid_draw_kw, 0.0)
        self.assertEqual(res.unmet_power_kw, 0.0)
        for g in ["G1", "G2", "G3"]:
            self.assertEqual(res.allocated_power[g], 0.0)
            self.assertEqual(res.modules_per_gun[g], 0)

    def test_negative_power_request(self):
        """Negative power requests must be filtered out as non-active, preventing reverse injection."""
        res = self.dpr_s1.allocate_power("S1", {"G_neg": -150.0, "G_pos": 75.0}, 1200.0)
        self.assertTrue(res.is_safe)
        self.assertEqual(res.allocated_power["G_neg"], 0.0)
        self.assertEqual(res.modules_per_gun["G_neg"], 0)
        self.assertEqual(res.allocated_power["G_pos"], 75.0)
        self.assertEqual(res.modules_per_gun["G_pos"], 3)  # 3 * 25 kW = 75 kW

    def test_single_dispenser_extreme_request(self):
        """Single dispenser requesting 1000 kW at S4 (limit 600 kW AC, 24 modules)."""
        # S4: grid_limit_ac = 600 kW. Max allowable DC = 600 * 0.955 = 573 kW -> 22 modules = 550 kW DC.
        res = self.dpr_s4.allocate_power("S4", {"G_greedy": 1000.0}, 600.0)
        self.assertTrue(res.is_safe)
        self.assertLessEqual(res.ac_grid_draw_kw, 600.0 + 1e-4)
        self.assertEqual(res.modules_per_gun["G_greedy"], 22)
        self.assertEqual(res.allocated_power["G_greedy"], 550.0)
        self.assertAlmostEqual(res.ac_grid_draw_kw, 550.0 / INVERTER_EFFICIENCY, places=4)
        self.assertEqual(res.unmet_power_kw, 450.0)

    def test_transformer_capacity_saturation_s3(self):
        """10 guns requesting 350 kW each (3500 kW DC) on S3 (1500 kW AC transformer)."""
        # S3: 57 modules = 1425 kW DC. 1425 / 0.955 = 1492.15 kW AC <= 1500 kW AC limit.
        reqs = {f"G_{i+1:02d}": 350.0 for i in range(10)}
        res = self.dpr_s3.allocate_power("S3", reqs, 1500.0)
        self.assertTrue(res.is_safe)
        self.assertEqual(res.dc_total_kw, 1425.0)
        self.assertAlmostEqual(res.ac_grid_draw_kw, 1492.1466, places=2)
        self.assertLessEqual(res.ac_grid_draw_kw, 1500.0)
        headroom = 1500.0 - res.ac_grid_draw_kw
        self.assertGreater(headroom, 7.8)  # 7.85 kW safety buffer
        total_mods = sum(res.modules_per_gun.values())
        self.assertEqual(total_mods, 57)

    def test_zero_and_negative_grid_limits(self):
        """Grid limits <= 0 must instantly cut all power to 0 kW safely."""
        res_zero = self.dpr_s1.allocate_power("S1", {"G1": 150.0}, 0.0)
        self.assertTrue(res_zero.is_safe)
        self.assertEqual(res_zero.dc_total_kw, 0.0)
        self.assertEqual(res_zero.allocated_power["G1"], 0.0)

        res_neg = self.dpr_s1.allocate_power("S1", {"G1": 150.0}, -500.0)
        self.assertTrue(res_neg.is_safe)
        self.assertEqual(res_neg.dc_total_kw, 0.0)
        self.assertEqual(res_neg.allocated_power["G1"], 0.0)

    def test_rapid_oscillating_demands(self):
        """50 rapid cycles of randomized volatile demands must never breach AC limits."""
        random.seed(1337)
        for cycle in range(50):
            num_guns = random.randint(1, 15)
            reqs = {
                f"Gun_{i}": (random.uniform(5.0, 350.0) if random.random() > 0.25 else 0.0)
                for i in range(num_guns)
            }
            grid_lim = random.choice([600.0, 800.0, 1000.0, 1200.0, 1500.0])
            res = self.dpr_s3.allocate_power("S3", reqs, grid_lim)
            self.assertTrue(res.is_safe, f"Cycle {cycle} unsafe: AC {res.ac_grid_draw_kw} > {grid_lim}")
            self.assertLessEqual(res.ac_grid_draw_kw, grid_lim + 1e-4)
            self.assertLessEqual(res.dc_total_kw, grid_lim * INVERTER_EFFICIENCY + 1e-4)

    def test_cabinet_isolation_n1(self):
        """Hardware fault containment: isolating C1-1 (15 modules) dynamically reduces pool."""
        dpr = DPRMatrix(station_id="S1")
        self.assertEqual(len(dpr.get_healthy_modules()), 43)

        # Isolate cabinet C1-1 (15 modules)
        isolated = dpr.isolate_cabinet("C1-1")
        self.assertEqual(isolated, 15)
        self.assertEqual(len(dpr.get_healthy_modules()), 28)

        # Request 1000 kW: available is only 28 * 25 = 700 kW DC
        res = dpr.allocate_power("S1", {"G1": 1000.0}, 1200.0)
        self.assertEqual(res.dc_total_kw, 700.0)
        self.assertEqual(res.modules_per_gun["G1"], 28)
        self.assertTrue(res.is_safe)

        # Restore cabinet
        restored = dpr.restore_cabinet("C1-1")
        self.assertEqual(restored, 15)
        self.assertEqual(len(dpr.get_healthy_modules()), 43)

    def test_contactor_zero_arc_compliance(self):
        """Zero-arc contactor sequence: 6 steps, <500ms delay, verify zero current at break."""
        seq = self.dpr_s1.re_route_contactor(from_gun="G1", to_gun="G2", modules=5)
        self.assertTrue(seq.is_zero_arc_compliant)
        self.assertEqual(seq.total_duration_ms, 260.0)
        self.assertLess(seq.total_duration_ms, CONTACTOR_MAX_SWITCH_DELAY_MS)
        self.assertEqual(seq.transferred_modules, 5)

        # Verify physical step sequence
        step_names = [s.step_name for s in seq.steps]
        expected_steps = [
            "RAMP_DOWN_CURRENT",
            "VERIFY_ZERO_CURRENT",
            "BREAK_SOURCE",
            "DEAD_TIME_INTERLOCK",
            "MAKE_DESTINATION",
            "RAMP_UP_CURRENT",
        ]
        self.assertEqual(step_names, expected_steps)

        # Check current at break step is 0.0 A
        break_step = [s for s in seq.steps if s.step_name == "BREAK_SOURCE"][0]
        self.assertLessEqual(break_step.current_amps, 0.05)
        self.assertEqual(break_step.current_amps, 0.0)

    def test_contactor_invalid_module_counts(self):
        """Zero or negative module counts must be rejected with compliance flag False."""
        seq_zero = self.dpr_s1.re_route_contactor(from_gun="G1", to_gun="G2", modules=0)
        self.assertFalse(seq_zero.is_zero_arc_compliant)
        self.assertEqual(seq_zero.transferred_modules, 0)

        seq_neg = self.dpr_s1.re_route_contactor(from_gun="G1", to_gun="G2", modules=-3)
        self.assertFalse(seq_neg.is_zero_arc_compliant)
        self.assertEqual(seq_neg.transferred_modules, 0)


class TestMPCOptimizerAdversarial(unittest.TestCase):
    """Adversarial stress testing of 15-minute Macro MPC / MILP Optimizer."""

    def setUp(self):
        self.bess_cfg = BESSConfig(
            capacity_kwh=500.0,
            max_power_kw=200.0,
            initial_soc=0.50,
            min_soc=0.10,
            max_soc=0.90,
            deg_cost_eur_kwh=0.03,
        )
        self.site_cfg = SiteMPCConfig(
            site_id="S1",
            transformer_max_kw=1200.0,
            num_modules=43,
            peak_fee_eur_kw_mo=6.50,
            bess=self.bess_cfg,
        )
        self.opt = MPCOptimizer(self.site_cfg)

    def test_price_surge_1000_eur_bess_shaving(self):
        """Spot price surges up to 1000 €/MWh: BESS must discharge to eliminate/minimize grid import."""
        prices = [50.0, 1000.0, 50.0, 50.0]
        # Vehicle needs 80 kWh (0.2 -> 0.6 of 200 kWh battery), achievable across 4 steps
        vehicles = [
            VehicleSchedule(
                "V1",
                arrive_step=0,
                depart_step=4,
                arrive_soc=0.20,
                required_soc=0.60,
                battery_kwh=200.0,
                max_charge_kw=100.0,
            )
        ]
        plan = self.opt.solve_15min_horizon(prices, vehicles)
        self.assertTrue(plan.is_optimal)
        self.assertEqual(len(plan.unmet_vehicles), 0)
        # Step 1 is the 1000 EUR/MWh surge: BESS should discharge and grid power should be 0
        self.assertGreater(plan.bess_power_kw[1], 0.0)
        self.assertAlmostEqual(plan.grid_power_kw[1], 0.0, places=4)
        self.assertGreaterEqual(plan.vehicle_soc["V1"][4], 0.60 - 1e-4)

    def test_price_surge_no_bess_load_shifting(self):
        """Spot price surges to 1000 €/MWh without BESS: when schedule slack exists, halt charging during surge."""
        site_no_bess = SiteMPCConfig(site_id="S1", transformer_max_kw=1200.0, num_modules=43, bess=None)
        opt_no_bess = MPCOptimizer(site_no_bess)

        prices = [50.0, 1000.0, 50.0, 50.0]
        # V1 needs 60 kWh (0.2 -> 0.5 of 200 kWh battery), can be satisfied in 3 non-spike steps
        vehicles = [
            VehicleSchedule(
                "V1",
                arrive_step=0,
                depart_step=4,
                arrive_soc=0.20,
                required_soc=0.50,
                battery_kwh=200.0,
                max_charge_kw=100.0,
            )
        ]
        plan = opt_no_bess.solve_15min_horizon(prices, vehicles)
        self.assertTrue(plan.is_optimal)
        self.assertEqual(len(plan.unmet_vehicles), 0)
        # Charging power at step 1 (spike) should be completely zero
        self.assertAlmostEqual(plan.vehicle_dc_power_kw["V1"][1], 0.0, places=4)
        self.assertAlmostEqual(plan.grid_power_kw[1], 0.0, places=4)
        self.assertGreaterEqual(plan.vehicle_soc["V1"][4], 0.50 - 1e-4)

    def test_negative_spot_prices_deep(self):
        """Deep negative spot prices (-500 €/MWh): BESS charges at maximum rate, grid power remains safe."""
        # When spot price is -500 EUR/MWh, even after peak demand charge, charging is highly profitable
        prices = [-500.0, -500.0, 50.0, 50.0]
        plan = self.opt.solve_15min_horizon(prices, [])
        self.assertTrue(plan.is_optimal)
        # BESS must charge (negative power) at max power 200 kW during step 0 and 1
        self.assertAlmostEqual(plan.bess_power_kw[0], -200.0, places=2)
        self.assertAlmostEqual(plan.bess_power_kw[1], -200.0, places=2)
        self.assertAlmostEqual(plan.grid_power_kw[0], 200.0, places=2)
        self.assertLessEqual(plan.grid_power_kw[0], 1200.0)
        self.assertLessEqual(plan.bess_soc[2], 0.90 + 1e-5)

    def test_bess_soc_boundary_clamps(self):
        """BESS must strictly respect min_soc (0.10) and max_soc (0.90) bounds."""
        # Test 1: BESS starts at min_soc (0.10) under 1000 EUR/MWh spike
        bess_min = BESSConfig(
            capacity_kwh=500.0,
            max_power_kw=200.0,
            initial_soc=0.10,
            min_soc=0.10,
            max_soc=0.90,
        )
        site_min = SiteMPCConfig(site_id="S1", bess=bess_min)
        opt_min = MPCOptimizer(site_min)
        plan_min = opt_min.solve_15min_horizon([1000.0, 1000.0], [])
        self.assertTrue(plan_min.is_optimal)
        self.assertTrue(np.all(plan_min.bess_soc >= 0.10 - 1e-5))
        self.assertTrue(np.all(plan_min.bess_power_kw <= 1e-5))  # Cannot discharge

        # Test 2: BESS starts at max_soc (0.90) under negative prices
        bess_max = BESSConfig(
            capacity_kwh=500.0,
            max_power_kw=200.0,
            initial_soc=0.90,
            min_soc=0.10,
            max_soc=0.90,
        )
        site_max = SiteMPCConfig(site_id="S1", bess=bess_max)
        opt_max = MPCOptimizer(site_max)
        plan_max = opt_max.solve_15min_horizon([-500.0, -500.0], [])
        self.assertTrue(plan_max.is_optimal)
        self.assertTrue(np.all(plan_max.bess_soc <= 0.90 + 1e-5))
        self.assertTrue(np.all(plan_max.bess_power_kw >= -1e-5))  # Cannot charge

    def test_urgent_departure_impossible_slack_relaxation(self):
        """Physically impossible deadline: 1 step (15 min) to charge 450 kWh with 100 kW max rate."""
        prices = [50.0, 50.0]
        vehicles = [
            VehicleSchedule(
                "V_impossible",
                arrive_step=0,
                depart_step=1,
                arrive_soc=0.05,
                required_soc=0.95,
                battery_kwh=500.0,
                max_charge_kw=100.0,
                penalty_eur=250.0,
            )
        ]
        plan = self.opt.solve_15min_horizon(prices, vehicles)
        # Solver must remain optimal (NOT crash or fail with INFEASIBLE) due to Big-M slack relaxation
        self.assertTrue(plan.is_optimal)
        self.assertIn("V_impossible", plan.unmet_vehicles)
        self.assertEqual(plan.penalty_cost_eur, 250.0)

    def test_urgent_departure_edf_priority_under_peak_price(self):
        """Vehicle departs in 1 interval, price is 800 €/MWh: must charge to fulfill SLA despite peak price."""
        prices = [800.0, 20.0]
        # Needs 20 kWh in 15 min: 100 kW in 0.25h * 0.95 = 23.75 kWh >= 20 kWh
        vehicles = [
            VehicleSchedule(
                "V_urgent_depart",
                arrive_step=0,
                depart_step=1,
                arrive_soc=0.50,
                required_soc=0.70,
                battery_kwh=100.0,
                max_charge_kw=100.0,
            )
        ]
        plan = self.opt.solve_15min_horizon(prices, vehicles)
        self.assertTrue(plan.is_optimal)
        self.assertEqual(len(plan.unmet_vehicles), 0)
        self.assertGreater(plan.vehicle_dc_power_kw["V_urgent_depart"][0], 80.0)
        self.assertAlmostEqual(plan.vehicle_soc["V_urgent_depart"][1], 0.70, places=2)

    def test_hard_ac_inverter_constraint_extreme_saturation(self):
        """10 vehicles demanding 350 kW each (3500 kW DC) on 1200 kW transformer with 60 modules (1500 kW DC)."""
        site_saturated = SiteMPCConfig(
            site_id="S_Sat",
            transformer_max_kw=1200.0,
            num_modules=60,
            eta_rect=0.955,
            bess=None,
        )
        opt_sat = MPCOptimizer(site_saturated)
        prices = [50.0] * 8
        vehicles = [
            VehicleSchedule(
                f"V_{i}",
                arrive_step=0,
                depart_step=8,
                arrive_soc=0.20,
                required_soc=0.80,
                battery_kwh=300.0,
                max_charge_kw=350.0,
            )
            for i in range(10)
        ]
        plan = opt_sat.solve_15min_horizon(prices, vehicles)
        self.assertTrue(plan.is_optimal)
        # Hard AC invariant: P_AC = P_DC / 0.955 <= transformer_max_kw
        self.assertLessEqual(np.max(plan.grid_power_kw), 1200.0 + 1e-4)
        self.assertLessEqual(np.max(plan.ac_load_kw), 1200.0 + 1e-4)
        total_dc = np.sum([plan.vehicle_dc_power_kw[v.vehicle_id] for v in vehicles], axis=0)
        self.assertLessEqual(np.max(total_dc) / 0.955, 1200.0 + 1e-4)

    def test_empty_and_zero_step_inputs(self):
        """Empty spot price list or empty fleet schedule must return clean empty/optimal plan."""
        plan_empty = self.opt.solve_15min_horizon([], [])
        self.assertTrue(plan_empty.is_optimal)
        self.assertEqual(plan_empty.horizon_steps, 0)

        plan_no_veh = self.opt.solve_15min_horizon([50.0, 50.0], [])
        self.assertTrue(plan_no_veh.is_optimal)
        self.assertEqual(len(plan_no_veh.unmet_vehicles), 0)

    def test_rolling_horizon_convergence_speed(self):
        """Standard rolling horizons (K=4, 8, 12, 16) with 12 buses must solve in <1.0s."""
        for K in [4, 8, 12, 16]:
            prices = [50.0] * K
            vehicles = [
                VehicleSchedule(
                    f"Bus_{i}",
                    arrive_step=0,
                    depart_step=K,
                    arrive_soc=0.20,
                    required_soc=0.80,
                    battery_kwh=400.0,
                    max_charge_kw=150.0,
                )
                for i in range(12)
            ]
            t0 = time.time()
            plan = self.opt.solve_15min_horizon(prices, vehicles)
            solve_time = time.time() - t0
            self.assertTrue(plan.is_optimal)
            self.assertLess(solve_time, 1.0, f"Horizon K={K} took {solve_time:.2f}s (exceeded 1.0s)")


class TestVirtualReplugAdversarial(unittest.TestCase):
    """Adversarial stress testing of Dual-Gun Virtual Replug & Plug & Queue."""

    def setUp(self):
        self.vr = VirtualReplugManager(depot_id="S1", num_posts=12)
        self.hub = PlugAndQueueHub(station_id="S3")

    def test_24_bus_night_shift_cycle(self):
        """24 electric buses across 3-phase night cycle (Phase A -> Phase B -> Top-Off)."""
        buses = []
        for i in range(12):
            b = BusState(bus_id=f"Bus_A_{i+1:02d}", current_soc_pct=15.0, group="A")
            self.vr.register_bus_arrival(b, f"D1-{i+1}", PlugType.GUN_A)
            buses.append(b)
        for i in range(12):
            b = BusState(bus_id=f"Bus_B_{i+1:02d}", current_soc_pct=15.0, group="B")
            self.vr.register_bus_arrival(b, f"D1-{i+1}", PlugType.GUN_B)
            buses.append(b)

        # 1. Phase A at 22:00
        res_a = self.vr.manage_dual_gun_night_cycle("S1", buses, hour=22.0)
        self.assertEqual(res_a.active_group, "A")
        self.assertEqual(res_a.phase, "PHASE_A_FAST_CHARGE")
        self.assertTrue(res_a.zero_jockey_confirmed)
        self.assertTrue(res_a.all_connected)
        self.assertEqual(res_a.replug_actions_needed, 0)
        # Group A buses are receiving power
        for b in buses[:12]:
            self.assertGreater(res_a.bus_allocations[b.bus_id], 0.0)

        # 2. Phase B at 02:00 (Boundary transition)
        res_b = self.vr.manage_dual_gun_night_cycle("S1", buses, hour=2.0)
        self.assertEqual(res_b.active_group, "B")
        self.assertEqual(res_b.phase, "PHASE_B_FAST_CHARGE")
        self.assertEqual(res_b.replug_actions_needed, 0)
        self.assertGreaterEqual(len(res_b.contactor_switches), 1)
        self.assertTrue(res_b.contactor_switches[0]["zero_arc"])

        # 3. Phase 3 Top-Off at 05:30
        res_top = self.vr.manage_dual_gun_night_cycle("S1", buses, hour=5.5)
        self.assertEqual(res_top.active_group, "TOP_OFF_EDF")
        self.assertEqual(res_top.phase, "PHASE_BALANCED_TOP_OFF")
        self.assertEqual(res_top.replug_actions_needed, 0)

    def test_bus_already_full_arrival(self):
        """Bus arriving with 95% SoC (target 90%) must be placed in COMPLETED state with 0 kW draw."""
        b_full = BusState(
            bus_id="Bus_Full",
            current_soc_pct=95.0,
            required_soc_pct=90.0,
            group="A",
        )
        self.vr.register_bus_arrival(b_full, "D1-1", PlugType.GUN_A)
        res = self.vr.manage_dual_gun_night_cycle("S1", [b_full], hour=22.0)
        self.assertEqual(res.bus_allocations["Bus_Full"], 0.0)
        self.assertEqual(b_full.plug_state, PlugState.COMPLETED)

    def test_boundary_hour_transitions(self):
        """Test exact minute boundary transitions (21.99, 22.0, 1.99, 2.0, 5.49, 5.5)."""
        b_a = BusState(bus_id="B_A", current_soc_pct=20.0, group="A")
        b_b = BusState(bus_id="B_B", current_soc_pct=20.0, group="B")
        self.vr.register_bus_arrival(b_a, "D1-1", PlugType.GUN_A)
        self.vr.register_bus_arrival(b_b, "D1-1", PlugType.GUN_B)

        res_2199 = self.vr.manage_dual_gun_night_cycle("S1", [b_a, b_b], hour=21.99)
        self.assertEqual(res_2199.active_group, "TOP_OFF_EDF")

        res_2200 = self.vr.manage_dual_gun_night_cycle("S1", [b_a, b_b], hour=22.0)
        self.assertEqual(res_2200.active_group, "A")

        res_0199 = self.vr.manage_dual_gun_night_cycle("S1", [b_a, b_b], hour=1.99)
        self.assertEqual(res_0199.active_group, "A")

        res_0200 = self.vr.manage_dual_gun_night_cycle("S1", [b_a, b_b], hour=2.0)
        self.assertEqual(res_0200.active_group, "B")

        res_0549 = self.vr.manage_dual_gun_night_cycle("S1", [b_a, b_b], hour=5.49)
        self.assertEqual(res_0549.active_group, "B")

        res_0550 = self.vr.manage_dual_gun_night_cycle("S1", [b_a, b_b], hour=5.5)
        self.assertEqual(res_0550.active_group, "TOP_OFF_EDF")

    def test_plug_and_queue_public_hub(self):
        """Public hub queueing: Gun A busy -> driver queued; Gun A tapers -> <500ms handover."""
        # Primary vehicle arrives and charges on Gun A
        res_arr1 = self.hub.on_driver_arrival("D3-1", "V01", req_kwh=50.0, is_gun_a_busy=False)
        self.assertEqual(res_arr1["status"], "CHARGING_STARTED")

        # Second vehicle arrives while Gun A is busy -> queued on Gun B
        res_arr2 = self.hub.on_driver_arrival("D3-1", "V02", req_kwh=40.0, is_gun_a_busy=True)
        self.assertEqual(res_arr2["status"], "QUEUED_AUTHORIZED")
        self.assertIn("D3-1", self.hub.queue_state)

        # Primary vehicle enters CV trickle or finishes -> DPR contactor hands over to V02
        res_handover = self.hub.on_primary_taper_or_finish("D3-1")
        self.assertEqual(res_handover["status"], "HANDOVER_COMPLETE")
        self.assertEqual(res_handover["vehicle_id"], "V02")
        self.assertTrue(res_handover["zero_arc_compliant"])
        self.assertLess(res_handover["delay_ms"], 500.0)
        self.assertNotIn("D3-1", self.hub.queue_state)

        # Subsequent taper with empty queue returns NO_QUEUE
        res_empty = self.hub.on_primary_taper_or_finish("D3-1")
        self.assertEqual(res_empty["status"], "NO_QUEUE")


if __name__ == "__main__":
    unittest.main()
