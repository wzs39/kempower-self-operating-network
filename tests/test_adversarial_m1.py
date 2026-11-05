"""
Adversarial Empirical Challenge Test Suite: Milestone 1 Core Engine & Dual-Gun DPR
Author: m1_challenger_2 (Empirical Challenger & Adversarial Specialist)
Target Modules:
- src/core/self_healing.py (Edge Micro FSM & 5 Hidden Failure Defenses)
- src/core/virtual_replug.py (Dual-Gun Satellite Multiplexing & Virtual Replug)

Probes:
1. Rapid fan speed degradation; verify Two-Stage N-1 shedding occurs BEFORE 75°C hardware trip.
2. Sudden WAN outage; verify local DLM maintains full 1500 kW capacity and rejects naive 50 kW fallback.
3. Corrupted or mismatched site configurations; verify auto-calibration digital twin corrects D5-7 and D5-8.
4. Dual-Gun night cycle under late arrivals, asymmetric battery capacities, and sub-zero cold ambient conditions (-14°C).
5. Public hub Plug & Queue CV trickle handover.
"""

import math
import unittest
from typing import Dict, List, Any

from src.core.self_healing import (
    EdgeFSM,
    EdgeState,
    CabinetTelemetry,
    ChargerTelemetry,
    TelemetrySnapshot,
    InverterEfficiencyGuard,
    PredictiveThermalEngine,
    OfflineIslandingController,
    CommissioningAutoCalibrator,
    ContactorCommand,
)
from src.core.virtual_replug import (
    VirtualReplugManager,
    PlugAndQueueHub,
    BusState,
    PlugType,
    PlugState,
    DualGunDispatchResult,
)
from src.core.dpr_matrix import DPRMatrix, MODULE_POWER_KW


class TestEdgeFSMRapidThermalPdM(unittest.TestCase):
    """Probe 1: Rapid thermal spike & fan speed degradation."""

    def setUp(self):
        self.fsm = EdgeFSM(site_id="S1")

    def test_rapid_fan_speed_degradation_triggers_n1_shedding_before_75c(self):
        """
        Verify that a sudden fan speed drop (>20% drop, e.g. 600 -> 420 RPM)
        triggers Two-Stage N-1 load shedding immediately while cabinet temperature
        remains safely below the 75°C hardware cutoff trip threshold.
        """
        # Step 0: Normal operation at 45.0°C and 600 RPM
        cab0 = CabinetTelemetry(
            cabinet_id="C1-3",
            cabinet_temp_c=45.0,
            fan_rpm=600.0,
            nominal_fan_rpm=600.0,
            power_kw=300.0,
        )
        snap0 = TelemetrySnapshot(
            site_id="S1",
            timestamp="2026-11-13T01:00:00+02:00",
            cabinets={"C1-3": cab0},
        )
        res0 = self.fsm.tick(snap0)
        self.assertEqual(res0.current_state, EdgeState.NORMAL)
        self.assertEqual(res0.action, "NONE")
        self.assertEqual(res0.power_shed_kw, 0.0)

        # Step 1: Rapid fan degradation to 420 RPM (30% drop >= 20%), temp climbs to 58.0°C
        cab1 = CabinetTelemetry(
            cabinet_id="C1-3",
            cabinet_temp_c=58.0,
            fan_rpm=420.0,
            nominal_fan_rpm=600.0,
            power_kw=300.0,
        )
        snap1 = TelemetrySnapshot(
            site_id="S1",
            timestamp="2026-11-13T01:01:00+02:00",
            cabinets={"C1-3": cab1},
        )
        res1 = self.fsm.tick(snap1)

        # Assertions proving N-1 shedding occurred BEFORE 75°C
        self.assertLess(cab1.cabinet_temp_c, 75.0, "Cabinet temperature must be strictly below 75°C trip threshold")
        self.assertEqual(res1.current_state, EdgeState.LOAD_MIGRATION)
        self.assertEqual(res1.action, "SHIFT_LOAD_TO_PARALLEL_CABINETS")
        self.assertGreaterEqual(res1.power_shed_kw, 180.0, "Must execute Stage 1 instant 180 kW shed")
        self.assertEqual(len(res1.contactor_commands), 6, "Must emit 6-step zero-arc contactor sequence")

        # Verify contactor command timings sum to 2630 ms (2.63s)
        total_delay = sum(cmd.duration_ms for cmd in res1.contactor_commands)
        self.assertAlmostEqual(total_delay, 2630.0, places=1)
        self.assertEqual(res1.contactor_commands[0].action, "RAMP_DOWN")
        self.assertEqual(res1.contactor_commands[1].action, "OPEN")
        self.assertEqual(res1.contactor_commands[2].action, "VERIFY_ZERO_VOLTAGE")
        self.assertEqual(res1.contactor_commands[3].action, "CLOSE")
        self.assertEqual(res1.contactor_commands[4].action, "VERIFY_AUX_FEEDBACK")
        self.assertEqual(res1.contactor_commands[5].action, "RAMP_UP")

    def test_thermal_gradient_lookahead_predicts_trip(self):
        """
        Verify that a steep temperature gradient without fan degradation (e.g. dT/dt = 2.5°C/min)
        predicts lookahead trip within 5 minutes and triggers LOAD_MIGRATION at 63.5°C before 75°C.
        """
        temps = [48.0, 51.0, 54.0, 57.0, 60.0, 63.5]
        res = None
        for i, t in enumerate(temps):
            cab = CabinetTelemetry(
                cabinet_id="C1-3",
                cabinet_temp_c=t,
                fan_rpm=600.0,
                nominal_fan_rpm=600.0,
                power_kw=300.0,
            )
            snap = TelemetrySnapshot(
                site_id="S1",
                timestamp=f"2026-11-13T01:0{i}:00+02:00",
                cabinets={"C1-3": cab},
            )
            res = self.fsm.tick(snap)

        self.assertIsNotNone(res)
        self.assertLess(temps[-1], 75.0, "Current temperature 63.5°C must be < 75.0°C")
        self.assertEqual(res.current_state, EdgeState.LOAD_MIGRATION)
        self.assertEqual(res.action, "SHIFT_LOAD_TO_PARALLEL_CABINETS")
        self.assertIn("lookahead trip", res.alarms[0])

    def test_hard_trip_cutoff_at_75c(self):
        """Verify that temperature >= 75.0°C triggers HARDWARE_TRIP and TRIP_MAIN_BREAKER."""
        cab = CabinetTelemetry(
            cabinet_id="C1-3",
            cabinet_temp_c=75.2,
            fan_rpm=300.0,
            nominal_fan_rpm=600.0,
            power_kw=300.0,
        )
        snap = TelemetrySnapshot(
            site_id="S1",
            timestamp="2026-11-13T01:10:00+02:00",
            cabinets={"C1-3": cab},
        )
        res = self.fsm.tick(snap)
        self.assertEqual(res.current_state, EdgeState.HARDWARE_TRIP)
        self.assertEqual(res.action, "TRIP_MAIN_BREAKER")

    def test_multi_cabinet_n1_isolation(self):
        """
        Verify that in a 3-cabinet station (C1-1, C1-2, C1-3), when C1-3 fails,
        the FSM isolates C1-3 and parallel healthy cabinets maintain operation.
        """
        c1 = CabinetTelemetry("C1-1", 42.0, 600.0, 300.0)
        c2 = CabinetTelemetry("C1-2", 44.0, 590.0, 300.0)
        c3 = CabinetTelemetry("C1-3", 64.0, 380.0, 300.0)  # degraded

        snap = TelemetrySnapshot(
            site_id="S1",
            timestamp="2026-11-13T01:15:00+02:00",
            cabinets={"C1-1": c1, "C1-2": c2, "C1-3": c3},
        )
        res = self.fsm.tick(snap)
        self.assertEqual(res.current_state, EdgeState.LOAD_MIGRATION)
        self.assertIn("C1-3", res.alarms[0])
        self.assertIn("C1-1", res.diagnostics["pdm_C1-1"])
        self.assertIn("C1-2", res.diagnostics["pdm_C1-2"])


class TestEdgeFSMOfflineIslanding(unittest.TestCase):
    """Probe 2: Sudden WAN outage & Local DLM Islanding."""

    def setUp(self):
        self.fsm = EdgeFSM(site_id="S3")

    def test_sudden_wan_outage_engages_local_dlm_and_rejects_50kw_fallback(self):
        """
        Verify sudden WAN loss transitions to OFFLINE_ISLANDING, activates
        ENGAGE_LOCAL_DLM_FULL_POWER, and sets fallback_kw to None (rejecting 50 kW).
        """
        chargers = {
            f"D3-{i}": ChargerTelemetry(
                charger_id=f"D3-{i}",
                cabinet_id="C3-1",
                power_kw=150.0,
                is_connected=True,
                soc_pct=40.0,
                bms_requested_kw=150.0,
            )
            for i in range(1, 11)
        }
        snap = TelemetrySnapshot(
            site_id="S3",
            timestamp="2026-11-13T02:00:00+02:00",
            connectivity=False,  # WAN cut
            grid_limit_kw=1500.0,
            chargers=chargers,
        )
        res = self.fsm.tick(snap)

        self.assertEqual(res.current_state, EdgeState.OFFLINE_ISLANDING)
        self.assertEqual(res.action, "ENGAGE_LOCAL_DLM_FULL_POWER")
        self.assertIsNone(res.fallback_kw, "Must explicitly reject 50 kW naive fallback")
        self.assertEqual(res.effective_grid_limit_kw, 1500.0)

    def test_local_dlm_maintains_1500kw_transformer_envelope_with_inverter_losses(self):
        """
        Under 1500 kW grid limit, verify that Local DLM allocates exact discrete
        25 kW modules (57 modules = 1425 kW DC) such that steady-state AC draw
        (1425 / 0.955 = 1492.15 kW AC) never exceeds the 1500 kW transformer limit.
        """
        chargers = {
            f"D3-{i}": ChargerTelemetry(
                charger_id=f"D3-{i}",
                cabinet_id="C3-1",
                power_kw=150.0,
                is_connected=True,
                soc_pct=50.0,
                bms_requested_kw=150.0,
            )
            for i in range(1, 11)  # 10 * 150 = 1500 kW requested
        }
        snap = TelemetrySnapshot(
            site_id="S3",
            timestamp="2026-11-13T02:15:00+02:00",
            connectivity=False,
            grid_limit_kw=1500.0,
            chargers=chargers,
        )
        res = self.fsm.tick(snap)

        allocs = res.diagnostics.get("local_dlm_allocations", {})
        total_dc_kw = sum(allocs.values())
        steady_ac_kw = total_dc_kw / 0.955

        self.assertEqual(res.max_allowable_dc_kw, 1425.0)
        self.assertAlmostEqual(total_dc_kw, 1425.0, delta=1.0)
        self.assertLessEqual(steady_ac_kw, 1500.0, "AC draw must strictly respect 1500 kW transformer limit")
        self.assertAlmostEqual(steady_ac_kw, 1492.15, delta=0.5)

    def test_thermal_safety_overrides_offline_islanding(self):
        """
        If a cabinet suffers severe fan degradation during an offline islanding state,
        thermal protection must strictly override offline islanding to prevent equipment fire.
        """
        cab = CabinetTelemetry(
            cabinet_id="C3-1",
            cabinet_temp_c=68.0,
            fan_rpm=350.0,
            nominal_fan_rpm=600.0,
            power_kw=300.0,
        )
        snap = TelemetrySnapshot(
            site_id="S3",
            timestamp="2026-11-13T02:30:00+02:00",
            connectivity=False,  # offline
            cabinets={"C3-1": cab},
        )
        res = self.fsm.tick(snap)
        self.assertEqual(
            res.current_state,
            EdgeState.LOAD_MIGRATION,
            "Thermal safety must take precedence over offline islanding",
        )
        self.assertEqual(res.action, "SHIFT_LOAD_TO_PARALLEL_CABINETS")


class TestDigitalTwinAutoCalibration(unittest.TestCase):
    """Probe 3: Corrupted or mismatched site configurations."""

    def setUp(self):
        self.fsm = EdgeFSM(site_id="S5")
        self.calibrator = CommissioningAutoCalibrator()

    def test_auto_calibration_detects_and_overrides_d5_7_and_d5_8(self):
        """
        Verify that corrupted site configurations (D5-7 throttled to 50 kW,
        D5-8 dead SIM) are identified and corrected to 150 kW and active SIM.
        """
        corrupted_config = {
            "D5-1": {"max_kw": 150.0, "sim_active": True},
            "D5-2": {"max_kw": 150.0, "sim_active": True},
            "D5-3": {"max_kw": 150.0, "sim_active": True},
            "D5-4": {"max_kw": 150.0, "sim_active": True},
            "D5-5": {"max_kw": 150.0, "sim_active": True},
            "D5-6": {"max_kw": 150.0, "sim_active": True},
            "D5-7": {"max_kw": 50.0, "sim_active": True},    # Corrupted 50 kW throttle
            "D5-8": {"max_kw": 150.0, "sim_active": False},  # Corrupted dead SIM
        }
        snap = TelemetrySnapshot(site_id="S5", timestamp="2026-11-13T03:00:00+02:00")
        res = self.fsm.tick(snap, live_config=corrupted_config)

        self.assertEqual(res.current_state, EdgeState.AUTO_CALIBRATED)
        self.assertEqual(res.action, "APPLY_CONFIG_OVERRIDE")
        self.assertIn("D5-7", res.config_overrides)
        self.assertEqual(res.config_overrides["D5-7"]["max_kw"], 150.0)
        self.assertIn("D5-8", res.config_overrides)
        self.assertTrue(res.config_overrides["D5-8"]["sim_active"])

    def test_string_format_robustness_in_calibration(self):
        """Verify calibration works when parameters are passed as strings."""
        corrupted_str = {
            "D5-7": {"max_kw": "50.0", "sim_active": "true"},
            "D5-8": {"max_kw": "150.0", "sim_active": "false"},
        }
        is_cal, overrides, discs = self.calibrator.audit_and_calibrate("S5", corrupted_str)
        self.assertTrue(is_cal)
        self.assertEqual(overrides["D5-7"]["max_kw"], 150.0)
        self.assertTrue(overrides["D5-8"]["sim_active"])

    def test_non_s5_sites_are_not_calibrated(self):
        """Verify that audit_and_calibrate returns False for sites other than S5."""
        cfg = {"D1-1": {"max_kw": 50.0, "sim_active": False}}
        is_cal, overrides, discs = self.calibrator.audit_and_calibrate("S1", cfg)
        self.assertFalse(is_cal)
        self.assertEqual(overrides, {})
        self.assertEqual(discs, [])


class TestDualGunNightCycleStress(unittest.TestCase):
    """Probe 4: Dual-Gun late arrival, asymmetric battery capacities, cold ambient."""

    def setUp(self):
        self.mgr = VirtualReplugManager(depot_id="S1", num_posts=12)

    def test_asymmetric_batteries_late_arrivals_and_cold_ambient(self):
        """
        Adversarially stress-tests:
        1. 24 buses with asymmetric battery sizes:
           - 8 small feeder buses (300 kWh)
           - 12 standard depot buses (450 kWh)
           - 4 high-capacity articulated buses (600 kWh)
        2. Dynamic late arrivals:
           - Bus_03 arrives late at 23:45 (Phase A)
           - Bus_14 arrives late at 01:30 (Phase A/B boundary)
           - Bus_01 arrives very late at 02:45 (Phase B)
        3. Sub-zero ambient temperature (-14.0°C)
        4. Verifies 100% zero jockeying and 0 replug actions needed across all 33 quarter-hour intervals.
        """
        buses = []
        for i in range(1, 25):
            group = "A" if i <= 12 else "B"
            if i <= 8:
                bat_kwh = 300.0
            elif i <= 20:
                bat_kwh = 450.0
            else:
                bat_kwh = 600.0

            post_idx = (i - 1) % 12 + 1
            post_id = f"D1-{post_idx}"
            gun_type = PlugType.GUN_A if group == "A" else PlugType.GUN_B
            bus = BusState(
                bus_id=f"Bus_{i:02d}",
                battery_kwh=bat_kwh,
                current_soc_pct=15.0 if i % 2 == 0 else 8.0,
                required_soc_pct=90.0,
                max_charge_kw=150.0,
                depart_ts=f"2026-11-13T06:0{i % 10}:00+02:00",
            )
            # Only register on-time buses initially
            if i not in [1, 3, 14]:
                self.mgr.register_bus_arrival(bus, post_id, gun_type)
            buses.append(bus)

        # 33 quarter-hour intervals: 22:00 to 24:00 (8 intervals) and 00:00 to 06:00 (25 intervals)
        hours = [22.0 + i * 0.25 for i in range(8)] + [0.0 + i * 0.25 for i in range(25)]

        dispatch_results: List[DualGunDispatchResult] = []
        for h in hours:
            # Late arrival injections
            if abs(h - 23.75) < 0.05:
                # Bus_03 arrives late at 23:45
                b03 = [b for b in buses if b.bus_id == "Bus_03"][0]
                self.mgr.register_bus_arrival(b03, "D1-3", PlugType.GUN_A)

            if abs(h - 1.50) < 0.05:
                # Bus_14 arrives late at 01:30
                b14 = [b for b in buses if b.bus_id == "Bus_14"][0]
                self.mgr.register_bus_arrival(b14, "D1-2", PlugType.GUN_B)

            if abs(h - 2.75) < 0.05:
                # Bus_01 arrives very late at 02:45 (during Phase B)
                b01 = [b for b in buses if b.bus_id == "Bus_01"][0]
                self.mgr.register_bus_arrival(b01, "D1-1", PlugType.GUN_A)

            res = self.mgr.manage_dual_gun_night_cycle(
                depot_id="S1",
                buses=list(self.mgr.fleet.values()),
                hour=h,
                grid_limit_kw=1200.0,
                dt_hours=0.25,
            )
            dispatch_results.append(res)

        self.assertEqual(len(dispatch_results), 33)

        # Invariant 1: 0 replugs across all 33 intervals
        for r in dispatch_results:
            self.assertEqual(r.replug_actions_needed, 0, f"Replug action needed at hour {r.hour}")
            self.assertTrue(r.zero_jockey_confirmed, f"Zero jockeying failed at hour {r.hour}")

        # Invariant 2: At 02:00 boundary, zero-arc contactor BBM swap occurred
        swap_events = [
            sw
            for r in dispatch_results
            for sw in r.contactor_switches
            if sw.get("action") == "GROUP_A_TO_B_SWAP"
        ]
        self.assertGreaterEqual(len(swap_events), 1)
        self.assertTrue(swap_events[0]["zero_arc"])
        self.assertLess(swap_events[0]["delay_ms"], 500.0)

        # Invariant 3: Standard 300 kWh and 450 kWh buses all reached target SoC
        for b_id, b in self.mgr.fleet.items():
            if b.battery_kwh in [300.0, 450.0] and b_id not in ["Bus_01", "Bus_14"]:
                self.assertGreaterEqual(
                    b.current_soc_pct,
                    90.0,
                    f"Bus {b_id} ({b.battery_kwh}kWh) failed to reach 90% SoC: {b.current_soc_pct:.1f}%",
                )

        # Invariant 4: Late-arriving Bus_01 was picked up in Phase 3 EDF Top-off
        b01 = self.mgr.fleet["Bus_01"]
        self.assertGreater(b01.energy_delivered_kwh, 50.0)
        self.assertGreater(b01.current_soc_pct, 25.0)

    def test_cold_ambient_subzero_telemetry_handling(self):
        """Verify EdgeFSM correctly handles -14.0°C sub-zero cold start without false alarms."""
        fsm = EdgeFSM(site_id="S1")
        cab = CabinetTelemetry(
            cabinet_id="C1-1",
            cabinet_temp_c=-14.0,
            fan_rpm=600.0,
            nominal_fan_rpm=600.0,
            power_kw=0.0,
        )
        snap = TelemetrySnapshot(
            site_id="S1",
            timestamp="2026-11-13T00:00:00+02:00",
            cabinets={"C1-1": cab},
        )
        res = fsm.tick(snap)
        self.assertEqual(res.current_state, EdgeState.NORMAL)
        self.assertEqual(res.action, "NONE")
        self.assertTrue(res.safe)


class TestPublicHubPlugAndQueue(unittest.TestCase):
    """Probe 5: Public Hub Plug & Queue CV trickle handover."""

    def setUp(self):
        self.hub = PlugAndQueueHub(station_id="S3")

    def test_plug_and_queue_reservation_and_cv_trickle_handover(self):
        """
        When primary gun (Gun A) is busy, arriving vehicle connects to Gun B
        and is placed in QUEUED_AUTHORIZED without vehicle repositioning.
        When Gun A enters CV trickle (<25 kW), zero-arc contactor reroutes modules in <500ms.
        """
        # Vehicle 2 arrives at D3-1 while Gun A is charging
        res_arrive = self.hub.on_driver_arrival(
            post_id="D3-1",
            vehicle_id="EV_Beta",
            req_kwh=40.0,
            is_gun_a_busy=True,
        )
        self.assertEqual(res_arrive["status"], "QUEUED_AUTHORIZED")
        self.assertIn("Reserved", res_arrive["message"])

        # Gun A tapers to CV trickle
        res_taper = self.hub.on_primary_taper_or_finish(post_id="D3-1")
        self.assertEqual(res_taper["status"], "HANDOVER_COMPLETE")
        self.assertEqual(res_taper["vehicle_id"], "EV_Beta")
        self.assertLess(res_taper["delay_ms"], 500.0)
        self.assertTrue(res_taper["zero_arc_compliant"])


if __name__ == "__main__":
    unittest.main()
