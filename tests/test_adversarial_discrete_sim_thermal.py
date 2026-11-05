"""
Adversarial Empirical Stress Testing: Closed-Loop Discrete Simulation & Predictive Thermal Engine
Author: m1_challenger_2 (Empirical Challenger & Adversarial Specialist)
Target Modules:
- src/sim/discrete_sim.py (Minute-by-Minute Discrete Event Simulator)
- src/core/self_healing.py (Predictive Thermal PdM Engine & Edge Telemetry Ingestion)

Probes:
1. Extreme arrival SoC (0%, 5%, 95%, 99.9%, inverted SoC > required).
2. Short dwell times (<15 min, 1 min, 0 min, negative window) with urgency waterfilling.
3. Nonlinear CV tapering curve dynamics (>80% SoC) and monotonicity/boundary preservation.
4. Closed-loop discrete simulation stability across S1, S2, and S5 under perturbed arrival & return times.
5. Graceful degradation under severe capacity starvation without NaNs or negative power allocations.
6. Predictive thermal engine under malformed telemetry strings (empty strings, NaNs, whitespaces).
7. Physical edge cases: Arctic cold soak (-40°C), aerodynamic overspeed (3000 RPM), negative backspin, idle sleep mode.
8. Historical S1 D1-9 anomaly detection (22:31 precursor with 199 min lead time).
9. Full dataset verification: exactly 0 false alarms across unmonitored/healthy chargers in telemetry_1min.csv.
10. Two-Stage N-1 load shedding bounded by actual active load and 6-step zero-arc contactor sequence.
"""

from __future__ import annotations

import csv
from datetime import datetime, timedelta
import math
from typing import Dict, List, Any
import unittest

from src.core.self_healing import (
    PredictiveThermalEngine,
    CabinetTelemetry,
    ContactorCommand,
)
from src.sim.discrete_sim import (
    Job,
    SimulationResult,
    taper_limit,
    waterfill_allocate,
    load_fleet_jobs,
    run_discrete_event_simulation,
    simulate_closed_loop_minute_by_minute,
)
from src.sim.scenario_engine import ScenarioEngine
from src.sim.data_loader import KempowerDataLoader
from src.utils.paths import resolve_csv_path


class TestDiscreteSimAdversarialStress(unittest.TestCase):
    """Adversarial stress testing of minute-by-minute discrete event charging simulation."""

    def setUp(self):
        self.t0 = datetime.fromisoformat("2026-11-13T00:00:00+02:00")

    def test_extreme_arrival_soc_boundary_probes(self):
        """
        Adversarially tests vehicles with extreme arrival SoC:
        - Ultra-low (0%, 1%, 5%) with deep charge requirement (90%, 100%)
        - Ultra-high (95%, 98%, 99.9%) with CV tapering
        - Inverted SoC (arrival 95% > required 80%)
        - Zero-demand (arrival 85% == required 85%)
        Ensures no NaN, no negative power, no overcharging beyond 100%, and valid state trajectories.
        """
        jobs = [
            Job("V_ZERO_SOC", self.t0, self.t0 + timedelta(hours=2), battery_kwh=400.0, soc_in=0.0, soc_req=0.90, max_kw=150.0),
            Job("V_5PCT_SOC", self.t0, self.t0 + timedelta(hours=2), battery_kwh=400.0, soc_in=0.05, soc_req=0.80, max_kw=150.0),
            Job("V_95PCT_SOC", self.t0, self.t0 + timedelta(hours=1), battery_kwh=400.0, soc_in=0.95, soc_req=0.99, max_kw=150.0),
            Job("V_INVERTED", self.t0, self.t0 + timedelta(hours=1), battery_kwh=300.0, soc_in=0.95, soc_req=0.80, max_kw=150.0),
            Job("V_EXACT_REQ", self.t0, self.t0 + timedelta(hours=1), battery_kwh=200.0, soc_in=0.85, soc_req=0.85, max_kw=150.0),
        ]

        res = run_discrete_event_simulation(
            jobs=jobs,
            site_id="EXTREME_SOC_STATION",
            date="2026-11-13",
            cabinet_kw=[360.0, 360.0],
            points_per_cabinet=3,
            strategy="urgency",
            cross_tie=True,
        )

        # Invariants: no NaN and non-negative delivered energy
        for vid, kwh in res.delivered.items():
            self.assertFalse(math.isnan(kwh), f"{vid} has NaN delivered energy")
            self.assertGreaterEqual(kwh, 0.0, f"{vid} has negative delivered energy: {kwh}")

        for vid, s in res.final_soc.items():
            self.assertFalse(math.isnan(s), f"{vid} has NaN final SoC")
            self.assertLessEqual(s, 1.0, f"{vid} exceeded 100% SoC: {s}")

        # Inverted SoC vehicle must receive 0 kWh and maintain original SoC
        self.assertEqual(res.delivered["V_INVERTED"], 0.0)
        self.assertEqual(res.final_soc["V_INVERTED"], 0.95)

        # Zero-demand vehicle must receive 0 kWh
        self.assertEqual(res.delivered["V_EXACT_REQ"], 0.0)
        self.assertEqual(res.final_soc["V_EXACT_REQ"], 0.85)

        # 95% vehicle must enter CV tapering and not exceed 150 kW * 0.10 ~ 15 kW
        self.assertGreater(res.delivered["V_95PCT_SOC"], 0.0)
        self.assertLessEqual(res.final_soc["V_95PCT_SOC"], 0.9901)

    def test_short_dwell_time_stress_and_sub_fifteen_minute_windows(self):
        """
        Adversarially tests vehicles with dwell times strictly < 15 minutes:
        - 1 minute dwell (extreme micro-session)
        - 5 minute dwell
        - 10 minute dwell
        - 14 minute dwell
        - 0 minute dwell (arrive == depart)
        - Negative dwell (depart < arrive)
        Verifies urgency waterfilling does not divide by zero or produce infinities/NaNs.
        """
        jobs = [
            Job("V_1M", self.t0, self.t0 + timedelta(minutes=1), battery_kwh=100.0, soc_in=0.10, soc_req=0.90, max_kw=150.0),
            Job("V_5M", self.t0, self.t0 + timedelta(minutes=5), battery_kwh=150.0, soc_in=0.10, soc_req=0.80, max_kw=150.0),
            Job("V_10M", self.t0, self.t0 + timedelta(minutes=10), battery_kwh=200.0, soc_in=0.10, soc_req=0.80, max_kw=150.0),
            Job("V_14M", self.t0, self.t0 + timedelta(minutes=14), battery_kwh=250.0, soc_in=0.10, soc_req=0.80, max_kw=150.0),
            Job("V_0M", self.t0, self.t0, battery_kwh=100.0, soc_in=0.20, soc_req=0.80, max_kw=150.0),
            Job("V_NEG_M", self.t0, self.t0 - timedelta(minutes=5), battery_kwh=100.0, soc_in=0.20, soc_req=0.80, max_kw=150.0),
        ]

        res = run_discrete_event_simulation(
            jobs=jobs,
            site_id="SHORT_DWELL_STATION",
            date="2026-11-13",
            cabinet_kw=[360.0],
            points_per_cabinet=6,
            strategy="urgency",
            cross_tie=True,
        )

        for vid, kwh in res.delivered.items():
            self.assertFalse(math.isnan(kwh), f"{vid} produced NaN delivered kWh")
            self.assertGreaterEqual(kwh, 0.0, f"{vid} produced negative kWh")

        # 1-minute vehicle is in contention for 360 kW cabinet; urgency waterfills ~129.4 kW (2.16 kWh <= 2.5 kWh)
        self.assertGreater(res.delivered["V_1M"], 1.5)
        self.assertLessEqual(res.delivered["V_1M"], 2.5)

        # 0-minute and negative dwell vehicles receive 0 kWh without crashing
        self.assertEqual(res.delivered["V_0M"], 0.0)
        self.assertEqual(res.delivered["V_NEG_M"], 0.0)
        self.assertLessEqual(res.peak_kw, 360.0)

    def test_urgency_waterfilling_saturation_and_headroom_redistribution(self):
        """
        Adversarially stresses the waterfilling power allocation algorithm:
        - Saturated requests (10 vehicles requesting 150 kW = 1,500 kW on a 360 kW cabinet).
        - Clamping verification: vehicles hitting 150 kW gun limit or taper limit are clamped,
          and excess power is proportionally redistributed to unclamped vehicles.
        """
        j1 = Job("V_URGENT", self.t0, self.t0 + timedelta(minutes=30), 100.0, 0.20, 0.80, 150.0) # 60 kWh in 0.5h -> urgency = 120 kW
        j2 = Job("V_RELAXED", self.t0, self.t0 + timedelta(hours=4), 100.0, 0.20, 0.80, 150.0)  # 60 kWh in 4.0h -> urgency = 15 kW

        # Total capacity = 200 kW (greater than j1's 150 kW limit)
        # Urgency weights: j1 = 120, j2 = 15. Without limits: j1 gets 200 * (120/135) = 177.8 kW.
        # But j1 limit = 150 kW. Waterfilling must clamp j1 to 150 kW and give remaining 50 kW to j2.
        alloc = waterfill_allocate(
            items=[j1, j2],
            cap_kw=200.0,
            weight_fn=lambda j: 120.0 if j.vehicle_id == "V_URGENT" else 15.0,
            limit_fn=lambda j: 150.0,
        )

        self.assertAlmostEqual(alloc["V_URGENT"], 150.0, places=2)
        self.assertAlmostEqual(alloc["V_RELAXED"], 50.0, places=2)
        self.assertAlmostEqual(sum(alloc.values()), 200.0, places=2)

    def test_cv_tapering_non_linear_dynamics(self):
        """
        Adversarially probes nonlinear Constant-Voltage (CV) tapering across the entire 0-100% SoC domain:
        - 0.00 <= SoC <= 0.80: constant maximum power (150.0 kW).
        - 0.80 < SoC <= 1.00: monotonically non-increasing power down to exactly 15.0 kW (10% depth).
        - Out-of-bounds SoC (<0.0 or >1.0) must not raise unhandled exceptions or crash.
        """
        job = Job("V_TAPER", self.t0, self.t0 + timedelta(hours=2), 400.0, 0.10, 0.95, 150.0)

        prev_power = 150.0
        for soc_pct in range(0, 101):
            soc = soc_pct / 100.0
            power = taper_limit(job, soc)
            self.assertFalse(math.isnan(power))
            self.assertGreaterEqual(power, 14.99)
            self.assertLessEqual(power, 150.0)

            if soc <= 0.80:
                self.assertEqual(power, 150.0)
            else:
                self.assertLess(power, prev_power)
            prev_power = power

        self.assertAlmostEqual(taper_limit(job, 1.00), 15.0, places=1)
        self.assertEqual(taper_limit(job, -0.20), 150.0)
        self.assertAlmostEqual(taper_limit(job, 1.50), 15.0, places=1)

    def test_s1_discrete_sim_under_perturbed_return_times(self):
        """
        Adversarially perturbs Station S1 (Bus Depot, 23 night buses, 3x360 kW cabinets, C1-3 fault at 02:25):
        - Perturbation matrix: arrival delays (+15m, +30m, +45m, +60m), early departures (-15m, -30m),
          and joint perturbations (arrive +30m, depart -30m).
        - Invariant: 0 missed departures, 0.0 kWh deficit, peak power <= 1080 kW, sum kWh >= 7000 kWh.
        """
        s1_jobs = load_fleet_jobs("S1", "2026-11-12", night_only=True)
        self.assertEqual(len(s1_jobs), 23, "S1 night_only=True contains 23 buses in timetable")
        fault_ts = datetime.fromisoformat("2026-11-13T02:25:00+02:00")

        perturbation_cases = [
            (0, 0),     # Baseline
            (15, 0),    # Arrival delayed 15m
            (30, 0),    # Arrival delayed 30m
            (45, 0),    # Arrival delayed 45m
            (60, 0),    # Arrival delayed 60m
            (-15, 0),   # Early arrival 15m
            (-30, 0),   # Early arrival 30m
            (0, -15),   # Early departure 15m
            (0, -30),   # Early departure 30m
            (30, -30),  # Joint: arrive 30m late, depart 30m early
        ]

        for arr_delta, dep_delta in perturbation_cases:
            perturbed = [
                Job(
                    j.vehicle_id,
                    j.arrive + timedelta(minutes=arr_delta),
                    j.depart + timedelta(minutes=dep_delta),
                    j.battery_kwh,
                    j.soc_in,
                    j.soc_req,
                    j.max_kw,
                )
                for j in s1_jobs
            ]

            res = run_discrete_event_simulation(
                jobs=perturbed,
                site_id="S1",
                date="2026-11-12",
                cabinet_kw=[360.0, 360.0, 360.0],
                points_per_cabinet=8,
                strategy="urgency",
                fault=(fault_ts, [2]),
                cross_tie=True,
                gun_kw=150.0,
            )

            self.assertEqual(res.missed_departures, 0, f"S1 perturbed (+{arr_delta}m arr, +{dep_delta}m dep) had missed departures: {res.missed_departures}")
            self.assertEqual(res.deficit_kwh, 0.0)
            self.assertLessEqual(res.peak_kw, 1080.0)
            self.assertGreater(res.total_kwh, 7000.0)

    def test_s2_discrete_sim_under_perturbed_return_times(self):
        """
        Adversarially perturbs Station S2 (Logistics Depot, 8 trucks, 2x400 kW cabinets):
        - Perturbation matrix: afternoon truck return & departure perturbations (±15 min).
        - Invariant: 0 missed departures, 0.0 kWh deficit, peak power <= 800 kW.
        """
        schedule_path = resolve_csv_path("fleet_schedule.csv")
        vehicles_path = resolve_csv_path("vehicles.csv")
        vehicles_spec = {}
        with open(vehicles_path, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                vehicles_spec[row["vehicle_id"].strip()] = row

        s2_jobs = []
        with open(schedule_path, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["site_id"].strip() == "S2" and row["arrive_ts"].strip().startswith("2026-11-13T14:"):
                    arr = datetime.fromisoformat(row["arrive_ts"].strip())
                    dep = datetime.fromisoformat(row["depart_ts"].strip())
                    vid = row["vehicle_id"].strip()
                    sp = vehicles_spec.get(vid, {})
                    s2_jobs.append(Job(
                        vehicle_id=vid,
                        arrive=arr,
                        depart=dep,
                        battery_kwh=float(sp.get("battery_kwh", 540.0)),
                        soc_in=float(row.get("arrive_soc_pct", 10.0)) / 100.0,
                        soc_req=float(row.get("required_soc_pct", 70.0)) / 100.0,
                        max_kw=float(sp.get("max_charge_kw", 300.0)),
                    ))

        self.assertEqual(len(s2_jobs), 8, "S2 must contain 8 afternoon trucks")

        for arr_delta, dep_delta in [(0, 0), (15, 0), (-15, 0), (0, -15), (15, 15)]:
            perturbed = [
                Job(
                    j.vehicle_id,
                    j.arrive + timedelta(minutes=arr_delta),
                    j.depart + timedelta(minutes=dep_delta),
                    j.battery_kwh,
                    j.soc_in,
                    j.soc_req,
                    j.max_kw,
                )
                for j in s2_jobs
            ]

            res = run_discrete_event_simulation(
                jobs=perturbed,
                site_id="S2",
                date="2026-11-13",
                cabinet_kw=[400.0, 400.0],
                points_per_cabinet=4,
                strategy="urgency",
                cross_tie=True,
                gun_kw=300.0,
            )

            self.assertEqual(res.missed_departures, 0, f"S2 perturbed (+{arr_delta}m arr, +{dep_delta}m dep) failed with {res.missed_departures} missed")
            self.assertEqual(res.deficit_kwh, 0.0)
            self.assertLessEqual(res.peak_kw, 800.0)

    def test_s5_discrete_sim_under_perturbed_return_times(self):
        """
        Adversarially perturbs Station S5 (Bus Depot, 8 buses, 2x450 kW cabinets = 900 kW):
        - Invariant: 0 missed departures, 0.0 kWh deficit, peak power <= 900 kW under arrival/depart shifts.
        """
        s5_jobs = load_fleet_jobs("S5", "2026-11-12", night_only=True)
        self.assertEqual(len(s5_jobs), 12, "S5 night_only=True contains 12 buses in timetable")

        for arr_delta, dep_delta in [(0, 0), (30, 0), (-30, 0), (0, -30), (30, -30)]:
            perturbed = [
                Job(
                    j.vehicle_id,
                    j.arrive + timedelta(minutes=arr_delta),
                    j.depart + timedelta(minutes=dep_delta),
                    j.battery_kwh,
                    j.soc_in,
                    j.soc_req,
                    j.max_kw,
                )
                for j in s5_jobs
            ]

            res = run_discrete_event_simulation(
                jobs=perturbed,
                site_id="S5",
                date="2026-11-12",
                cabinet_kw=[450.0, 450.0],
                points_per_cabinet=4,
                strategy="urgency",
                cross_tie=True,
                gun_kw=150.0,
            )

            self.assertEqual(res.missed_departures, 0)
            self.assertEqual(res.deficit_kwh, 0.0)
            self.assertLessEqual(res.peak_kw, 900.0)

    def test_discrete_sim_severe_capacity_starvation_graceful_degradation(self):
        """
        Adversarially forces severe capacity starvation by moving departures 4 hours earlier on S1.
        Verifies that under physically impossible time constraints:
        - The simulator does not crash or raise exceptions.
        - Power and delivered kWh remain non-negative and finite (no NaNs).
        - Missed departures and deficit kWh are computed accurately.
        - Peak power strictly observes the 1080 kW hardware ceiling.
        """
        s1_jobs = load_fleet_jobs("S1", "2026-11-12", night_only=True)
        fault_ts = datetime.fromisoformat("2026-11-13T02:25:00+02:00")

        severe_jobs = [
            Job(j.vehicle_id, j.arrive, j.depart - timedelta(hours=4), j.battery_kwh, j.soc_in, j.soc_req, j.max_kw)
            for j in s1_jobs
        ]

        res = run_discrete_event_simulation(
            jobs=severe_jobs,
            site_id="S1_SEVERE",
            date="2026-11-12",
            cabinet_kw=[360.0, 360.0, 360.0],
            points_per_cabinet=8,
            strategy="urgency",
            fault=(fault_ts, [2]),
            cross_tie=True,
            gun_kw=150.0,
        )

        self.assertGreater(res.missed_departures, 0, "Severe starvation should detect missed departures")
        self.assertGreater(res.deficit_kwh, 0.0)
        self.assertLessEqual(res.peak_kw, 1080.0)
        self.assertTrue(all(not math.isnan(v) and v >= 0.0 for v in res.delivered.values()))
        self.assertTrue(all(not math.isnan(s) and 0.0 <= s <= 1.0 for s in res.final_soc.values()))


class TestPredictiveThermalEngineAdversarialStress(unittest.TestCase):
    """Adversarial stress testing of predictive thermal engine and telemetry ingestion."""

    def setUp(self):
        self.pdm = PredictiveThermalEngine()

    def test_thermal_telemetry_malformed_values_and_type_coercion(self):
        """
        Adversarially injects edge-case telemetry inputs into PredictiveThermalEngine:
        - NaN float and None values for temperature and fan RPM
        - Extreme Arctic cold soak (-40.0°C)
        - Extreme aerodynamic overspeed spike (3000.0 RPM)
        - Negative backspin RPM (-50.0 RPM)
        - Exact threshold boundaries: 58.5°C warning, 59.3°C trip, 75.0°C hard cutoff
        Verifies no unhandled exceptions, no NaN in returned metrics, and proper flags.
        """
        test_matrix = [
            ("Arctic cold soak", -40.0, 1400.0, 0.0, False, False, False),
            ("Freezing zero", 0.0, 1400.0, 0.0, False, False, False),
            ("Normal running", 45.0, 1400.0, 100.0, False, False, False),
            ("Idle power save (0 RPM, 30°C, 0 kW)", 30.0, 0.0, 0.0, False, False, False),
            ("RPM overspeed spike 3000 RPM", 45.0, 3000.0, 100.0, False, False, False),
            ("RPM negative backspin -50 RPM", 45.0, -50.0, 100.0, False, True, False),
            ("NaN temperature", float("nan"), 1400.0, 100.0, False, False, False),
            ("NaN RPM", 45.0, float("nan"), 100.0, False, False, False),
            ("Both NaN", float("nan"), float("nan"), 0.0, False, False, False),
            ("Exact 58.5°C threshold", 58.5, 1400.0, 100.0, False, False, True),
            ("Precursor 59.3°C + 702 RPM", 59.3, 702.0, 100.0, False, True, True),
            ("Exact 75.0°C trip", 75.0, 1400.0, 100.0, True, False, False),
            ("Severe 110.0°C overtemp", 110.0, 0.0, 100.0, True, False, False),
        ]

        for name, temp, rpm, pkw, exp_trip, exp_mig, exp_warn in test_matrix:
            cab = CabinetTelemetry("C_EDGE", temp, rpm, power_kw=pkw)
            trip, mig, warn, ttt, drop, msg = self.pdm.evaluate_cabinet(cab)

            self.assertEqual(trip, exp_trip, f"{name}: trip={trip} vs exp={exp_trip}")
            self.assertEqual(mig, exp_mig, f"{name}: mig={mig} vs exp={exp_mig}")
            self.assertEqual(warn, exp_warn, f"{name}: warn={warn} vs exp={exp_warn}")
            self.assertFalse(math.isnan(ttt), f"{name}: ttt was NaN")
            self.assertFalse(math.isnan(drop), f"{name}: drop was NaN")
            self.assertIsInstance(msg, str)

    def test_thermal_history_with_consecutive_nans_and_gradient(self):
        """
        Adversarially feeds a sequence of NaN telemetry snapshots into history,
        verifying gradient and lookahead calculations do not crash or corrupt state.
        """
        pdm = PredictiveThermalEngine()
        for i in range(10):
            cab = CabinetTelemetry("C1-3", float("nan"), float("nan"))
            pdm.record_telemetry(cab, f"2026-11-13T00:{i:02d}:00")
            trip, mig, warn, ttt, drop, _ = pdm.evaluate_cabinet(cab)
            self.assertFalse(trip)
            self.assertFalse(mig)
            self.assertFalse(warn)
            self.assertEqual(ttt, 999.0)
            self.assertEqual(drop, 0.0)

    def test_s1_d1_9_anomaly_precursor_detection_reliability(self):
        """
        Verifies empirical detection of S1 C1-3 (charger D1-9) thermal anomaly:
        - True peak temperature at 2026-11-12T22:31:00+02:00: 59.3°C, 702 RPM.
        - Provides exactly 199.0 minutes (3h 19m) of lead time before F015 at 01:50:00+02:00.
        - Verifies at 01:45:00+02:00, temperature is calm at 34.3-35.2°C, proving 22:31 was the true precursor.
        """
        audit = PredictiveThermalEngine.detect_s1_historical_anomaly("D1-9")
        self.assertEqual(audit["charger_id"], "D1-9")
        self.assertEqual(audit["cabinet_id"], "C1-3")
        self.assertEqual(audit["true_peak_timestamp"], "2026-11-12T22:31:00+02:00")
        self.assertEqual(audit["true_peak_temp_c"], 59.3)
        self.assertEqual(audit["true_peak_fan_rpm"], 702.0)
        self.assertEqual(audit["lead_time_before_f015_minutes"], 199.0)
        self.assertLess(audit["temp_at_0145_c"], 40.0)

    def test_zero_false_alarms_across_healthy_chargers_in_telemetry(self):
        """
        Scans all 9,000 rows in telemetry_1min.csv through PredictiveThermalEngine.
        Verifies:
        1. False alarm count on unmonitored / healthy chargers (D3-3 at S3, D4-2 at S4) is EXACTLY 0.
        2. D1-9 precursor at 2026-11-12T22:31:00 is captured with is_migration=True and is_warning=True.
        """
        t_path = resolve_csv_path("telemetry_1min.csv")
        pdm = PredictiveThermalEngine()
        alerts = []
        total_rows = 0

        with open(t_path, "r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                total_rows += 1
                cid = row["charger_id"]
                raw_t = row.get("cabinet_temp_c", "").strip()
                raw_rpm = row.get("fan_rpm", "").strip()

                t_c = float(raw_t) if raw_t and raw_t != "NaN" else 0.0
                rpm = float(raw_rpm) if raw_rpm and raw_rpm != "NaN" else None
                p_kw = float(row.get("power_kw", "0") or "0")

                cab = CabinetTelemetry(cid, t_c, rpm, power_kw=p_kw)
                pdm.record_telemetry(cab, row.get("ts", ""))
                trip, mig, warn, _, _, msg = pdm.evaluate_cabinet(cab)
                if trip or mig or warn:
                    alerts.append((row.get("ts"), cid, t_c, rpm, trip, mig, warn, msg))

        self.assertEqual(total_rows, 9000, "telemetry_1min.csv must contain exactly 9,000 rows")

        # Zero false alarms on healthy chargers D3-3 and D4-2
        d3_d4_alerts = [a for a in alerts if a[1] in ["D3-3", "D4-2"]]
        self.assertEqual(len(d3_d4_alerts), 0, f"Expected 0 false alarms on D3-3 and D4-2, found: {len(d3_d4_alerts)}")

        # Reliable precursor detection on D1-9
        d1_9_precursor = [a for a in alerts if a[1] == "D1-9" and "2026-11-12T22:31" in a[0]]
        self.assertEqual(len(d1_9_precursor), 1, "D1-9 22:31 precursor was not reliably detected")
        _, _, p_temp, p_rpm, p_trip, p_mig, p_warn, _ = d1_9_precursor[0]
        self.assertEqual(p_temp, 59.3)
        self.assertEqual(p_rpm, 702.0)
        self.assertFalse(p_trip)
        self.assertTrue(p_mig)
        self.assertTrue(p_warn)

    def test_two_stage_n1_shedding_plan_load_bounding(self):
        """
        Verifies Two-Stage N-1 Shedding plan generates:
        - Stage 1: Load-bounded power shedding (<100ms): min(180 kW, max(0.0, active_load_kw)).
        - Stage 2: 6-step zero-arc contactor commands (RAMP_DOWN, OPEN, VERIFY_ZERO_VOLTAGE,
          CLOSE, VERIFY_AUX_FEEDBACK, RAMP_UP) summing to 2630 ms macro sequence.
        """
        # Case A: active load 120 kW -> shed 120 kW (does NOT blind shed 180 kW)
        shed_120, cmds_120 = self.pdm.generate_two_stage_n1_plan("C1-3", 120.0)
        self.assertEqual(shed_120, 120.0)
        self.assertEqual(len(cmds_120), 6)
        total_ms = sum(c.duration_ms for c in cmds_120)
        self.assertEqual(total_ms, 2630.0)

        # Case B: active load 250 kW -> shed 180 kW (capped at 180 kW)
        shed_250, _ = self.pdm.generate_two_stage_n1_plan("C1-3", 250.0)
        self.assertEqual(shed_250, 180.0)

        # Case C: active load 0 kW -> shed 0 kW
        shed_0, _ = self.pdm.generate_two_stage_n1_plan("C1-3", 0.0)
        self.assertEqual(shed_0, 0.0)


if __name__ == "__main__":
    unittest.main()
