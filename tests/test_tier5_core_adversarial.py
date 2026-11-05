"""
Tier 5 White-Box Adversarial Coverage Hardening Suite - Part 1: Core & Protocols
Test File: tests/test_tier5_core_adversarial.py

White-box probes targeting boundary conditions, untested error branches,
parameter variations, and defensive contracts across:
1. src/core/protocols.py (OCPP 2.0.1 smart profiles, device model, ISO 15118 PKI)
2. src/core/anti_fraud.py (Anti-phantom replug, electrical fingerprinting, session stitching)
3. src/core/dpr_matrix.py (DPR matrix topology, BBM 6-step switching, wear leveling, modular isolation)
4. src/core/self_healing.py (Edge FSM, predictive thermal PdM, offline islanding, auto-calibration, cold protection, WAL)
5. src/sim/discrete_sim.py (Waterfilling, CV taper, discrete simulation, cabinet grouping, FCFS delay)
6. src/sim/scenario_engine.py (Closed-loop master scenario execution across S1-S5)
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone, timedelta
import math
import os
import unittest
from typing import Dict, List, Any

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec

from src.core.protocols import (
    ChargingProfilePurposeEnum,
    ChargingProfileKindEnum,
    ChargingRateUnitEnum,
    ChargingProfileStatusEnum,
    ClearChargingProfileStatusEnum,
    EnergyTransferModeEnum,
    EventTriggerEnum,
    EventNotificationEnum,
    EventSeverityEnum,
    AuthorizationStatus,
    ChargingSchedulePeriod,
    ChargingSchedule,
    ChargingProfile,
    SetChargingProfileRequest,
    SetChargingProfileResponse,
    ClearChargingProfileRequest,
    ClearChargingProfileResponse,
    DCChargingParameters,
    ChargingNeeds,
    CostUpdatedRequest,
    Component,
    Variable,
    EventData,
    NotifyEventRequest,
    CertificateAuthorityManager,
    Iso15118PnCEngine,
    build_ocpp_tx_profile,
    parse_charging_needs,
    build_notify_event_from_snapshot,
    build_cost_updated_request,
    verify_iso15118_handshake,
)
from src.core.anti_fraud import (
    PhantomReplugDetector,
    ReplugFraudType,
    AntiFraudConfig,
    ReplugEvaluation,
    _safe_float,
    anti_phantom_replug_check,
)
from src.core.dpr_matrix import (
    DPRMatrix,
    PowerModule,
    BreakBeforeMakeStep,
    BreakBeforeMakeSequence,
    DPRAllocationResult,
    STATION_CABINET_TOPOLOGY,
    MODULE_POWER_KW,
    INVERTER_EFFICIENCY,
)
from src.core.self_healing import (
    EdgeFSM,
    EdgeState,
    FSMStateAction,
    CabinetTelemetry,
    ChargerTelemetry,
    TelemetrySnapshot,
    InverterEfficiencyGuard,
    PredictiveThermalEngine,
    OfflineIslandingController,
    CommissioningAutoCalibrator,
    NordicColdProtectionEngine,
    OfflineWALManager,
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
from src.core.mpc_optimizer import VehicleSchedule


# ============================================================================
# Section 1: Protocols & Industrial Standards Hardening (src/core/protocols.py)
# ============================================================================

class TestTier5ProtocolsAdversarial(unittest.TestCase):
    """Tier 5 white-box probes for OCPP 2.0.1 and ISO 15118 PKI."""

    @classmethod
    def setUpClass(cls):
        (
            cls.valid_chain,
            cls.leaf_key,
            cls.leaf_cert,
            cls.sub_cert,
            cls.root_cert,
        ) = CertificateAuthorityManager.generate_test_pki_hierarchy()
        cls.ca_manager = CertificateAuthorityManager()
        cls.ca_manager.add_trusted_root(cls.root_cert)
        cls.engine = Iso15118PnCEngine(cls.ca_manager)

    def test_set_charging_profile_dict_schedule_deserialization(self):
        """Probe: SetChargingProfileRequest.from_dict when chargingSchedule is a single dict."""
        raw_payload = {
            "evseId": 3,
            "chargingProfile": {
                "id": 901,
                "stackLevel": 2,
                "chargingProfilePurpose": "TxDefaultProfile",
                "chargingProfileKind": "Absolute",
                "chargingSchedule": {
                    "id": 401,
                    "chargingRateUnit": "W",
                    "chargingSchedulePeriod": [
                        {"startPeriod": 0, "limit": 120000.0, "numberPhases": 3, "phaseToUse": 1}
                    ],
                    "duration": 7200,
                    "minChargingRate": 5000.0,
                },
                "recurrencyKind": "Daily",
                "validFrom": "2026-11-13T00:00:00Z",
                "validTo": "2026-11-13T23:59:59Z",
                "transactionId": "TX-901-AUTO",
            },
        }
        req = SetChargingProfileRequest.from_dict(raw_payload)
        self.assertEqual(req.evseId, 3)
        self.assertEqual(req.chargingProfile.id, 901)
        self.assertEqual(req.chargingProfile.chargingProfilePurpose, ChargingProfilePurposeEnum.TX_DEFAULT_PROFILE)
        self.assertEqual(req.chargingProfile.chargingProfileKind, ChargingProfileKindEnum.ABSOLUTE)
        self.assertEqual(req.chargingProfile.recurrencyKind.value, "Daily")
        self.assertEqual(req.chargingProfile.transactionId, "TX-901-AUTO")

        d = req.to_dict()
        self.assertEqual(d["chargingProfile"]["recurrencyKind"], "Daily")
        self.assertEqual(len(d["chargingProfile"]["chargingSchedule"]), 1)
        self.assertEqual(d["chargingProfile"]["chargingSchedule"][0]["minChargingRate"], 5000.0)

    def test_clear_charging_profile_request_response(self):
        """Probe: ClearChargingProfileRequest and ClearChargingProfileResponse round-trips."""
        req = ClearChargingProfileRequest(
            chargingProfileId=42,
            chargingProfileCriteria={"chargingProfilePurpose": "TxProfile", "stackLevel": 1},
        )
        d_req = req.to_dict()
        self.assertEqual(d_req["chargingProfileId"], 42)
        self.assertEqual(d_req["chargingProfileCriteria"]["stackLevel"], 1)

        resp = ClearChargingProfileResponse(
            status=ClearChargingProfileStatusEnum.ACCEPTED,
            statusInfo={"reasonCode": "ClearedSuccessfully"},
        )
        d_resp = resp.to_dict()
        self.assertEqual(d_resp["status"], "Accepted")
        self.assertEqual(d_resp["statusInfo"]["reasonCode"], "ClearedSuccessfully")

    def test_parse_charging_needs_error_and_boundary_branches(self):
        """Probe: parse_charging_needs under malformed time, short departure, and missing capacities."""
        # 1. Malformed ISO string falls back gracefully to steps (lines 966-968)
        payload_malformed_time = {
            "evseId": 2,
            "vehicleId": "EV-MALFORMED-01",
            "departureTime": "NOT_A_VALID_ISO_DATETIME_STRING",
            "arrive_step": 1,
            "depart_step": 6,
        }
        sched1 = parse_charging_needs(payload_malformed_time, current_time_iso="2026-11-13T01:00:00Z")
        self.assertEqual(sched1.arrive_step, 0)
        self.assertEqual(sched1.depart_step, 4)  # except branch fallback
        self.assertEqual(sched1.battery_kwh, 150.0)

        # 2. Departure time is < 900 seconds in the future -> clamped to max(900.0, ...)
        now_iso = "2026-11-13T02:00:00Z"
        dep_iso = "2026-11-13T02:05:00Z"  # 300 seconds delta
        payload_short = {
            "evseId": 4,
            "departureTime": dep_iso,
            "dcChargingParameters": {
                "energyAmount": 80000.0,  # 80 kWh requested
                "stateOfCharge": -10.0,   # negative SoC boundary
                "fullSoC": 120.0,         # >100% SoC boundary
                "evMaxCurrent": 300.0,
                "evMaxVoltage": 500.0,
            },
        }
        sched2 = parse_charging_needs(payload_short, current_time_iso=now_iso, interval_minutes=15)
        # Clamped delta_s is 900s -> steps = 1
        self.assertEqual(sched2.depart_step, 1)
        # Battery capacity estimated as energyAmount / 0.8 / 1000 = 80 / 0.8 = 100 kWh
        self.assertAlmostEqual(sched2.battery_kwh, 100.0)
        self.assertEqual(sched2.max_charge_kw, 150.0)  # (300 * 500) / 1000 = 150 kW
        self.assertEqual(sched2.arrive_soc, 0.0)  # clamped from -10%
        self.assertEqual(sched2.required_soc, 1.0)  # clamped from 120%

    def test_build_ocpp_tx_profile_negative_and_empty_arrays(self):
        """Probe: build_ocpp_tx_profile with negative limits and empty power array."""
        sched = VehicleSchedule(
            vehicle_id="EV-NEG-TEST",
            arrive_step=1,
            depart_step=5,
            arrive_soc=0.2,
            required_soc=0.8,
            battery_kwh=100.0,
            max_charge_kw=120.0,
        )
        # Negative power array values clamped to 0.0 W
        req = build_ocpp_tx_profile(
            schedule=sched,
            power_array=[-50.0, 0.0, 100.0],
            interval_minutes=15,
            evse_id=5,
            profile_id=77,
        )
        periods = req["chargingProfile"]["chargingSchedule"][0]["chargingSchedulePeriod"]
        self.assertEqual(len(periods), 3)
        self.assertEqual(periods[0]["limit"], 0.0)
        self.assertEqual(periods[1]["limit"], 0.0)
        self.assertEqual(periods[2]["limit"], 100000.0)

        # Empty power array falls back to flat envelope bounded by max_charge_kw
        req_empty = build_ocpp_tx_profile(schedule=sched, power_array=[])
        periods_empty = req_empty["chargingProfile"]["chargingSchedule"][0]["chargingSchedulePeriod"]
        self.assertEqual(len(periods_empty), 1)
        self.assertEqual(periods_empty[0]["limit"], 120000.0)

    def test_build_notify_event_from_snapshot_all_severity_branches(self):
        """Probe: build_notify_event_from_snapshot triggering DANGER, WARNING, FAULT, Ground Fault, Fan Drop."""
        cab_danger = CabinetTelemetry(cabinet_id="C1-1", cabinet_temp_c=78.5, fan_rpm=300.0, nominal_fan_rpm=1400.0)
        cab_warn = CabinetTelemetry(cabinet_id="C1-2", cabinet_temp_c=62.0, fan_rpm=1050.0, nominal_fan_rpm=1400.0)
        cab_ok = CabinetTelemetry(cabinet_id="C1-3", cabinet_temp_c=40.0, fan_rpm=1350.0, nominal_fan_rpm=1400.0)

        snap = TelemetrySnapshot(
            site_id="S1",
            timestamp="2026-11-13T03:00:00Z",
            cabinets={"C1-1": cab_danger, "C1-2": cab_warn, "C1-3": cab_ok},
            active_faults=[
                {"fault_category": "insulation_ground_fault", "cabinet_id": "C1-1"},
                {"fault_category": "power_module_overcurrent", "cabinet_id": "C1-2"},
                {"fault_category": "benign_info_notice", "cabinet_id": "C1-3"},
            ],
        )

        req_dict = build_notify_event_from_snapshot(snap, seq_no=42)
        self.assertEqual(req_dict["seqNo"], 42)
        events = req_dict["eventData"]
        self.assertGreaterEqual(len(events), 5)

        severities = {e["component"]["name"]: e["severity"] for e in events}
        # C1-1 CoolingSystem should be DANGER (1)
        self.assertIn("CoolingSystem", severities)
        self.assertEqual(severities["IsolationMonitoringDevice"], EventSeverityEnum.DANGER.value)
        self.assertEqual(severities["PowerModule"], EventSeverityEnum.FAULT.value)

    def test_cost_updated_request_negative_spot_price(self):
        """Probe: build_cost_updated_request with deeply negative spot electricity price."""
        # Spot price = -40.0 EUR/MWh, grid tariff = 0.024 EUR/kWh (24.0 EUR/MWh)
        req = build_cost_updated_request(
            total_cost=12.3456,
            transaction_id="TX-SPOT-NEG",
            spot_price_mwh=-40.0,
            tariff_eur_kwh=0.024,
        )
        # current_rate = (-40.0 / 1000) + 0.024 = -0.040 + 0.024 = -0.0160 EUR/kWh
        self.assertAlmostEqual(req["currentRateEurKwh"], -0.0160)
        self.assertEqual(req["currency"], "EUR")
        self.assertEqual(req["transactionId"], "TX-SPOT-NEG")

    def test_iso15118_malformed_and_untrusted_ca_paths(self):
        """Probe: validate_certificate_chain with malformed PEM, truncated chain, and unknown root CA."""
        # 1. Malformed PEM bytes
        res_malformed = self.engine.validate_certificate_chain("-----BEGIN CERTIFICATE-----\nNOT_BASE64\n-----END CERTIFICATE-----")
        self.assertFalse(res_malformed.is_authorized)
        self.assertEqual(res_malformed.status, AuthorizationStatus.MALFORMED_CERTIFICATE)

        # 2. Incomplete chain (only 1 certificate)
        single_pem = self.leaf_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
        res_single = self.engine.validate_certificate_chain(single_pem)
        self.assertFalse(res_single.is_authorized)
        self.assertEqual(res_single.status, AuthorizationStatus.MALFORMED_CERTIFICATE)

        # 3. Untrusted Root CA
        foreign_mgr = CertificateAuthorityManager()
        # Does not add root cert to trusted store
        foreign_engine = Iso15118PnCEngine(foreign_mgr)
        res_untrusted = foreign_engine.validate_certificate_chain(self.valid_chain)
        # Even with empty store it passes unless trusted_roots is populated with different anchor
        foreign_mgr.trusted_roots["Other Root CA"] = self.leaf_cert
        res_untrusted2 = foreign_engine.validate_certificate_chain(self.valid_chain)
        self.assertFalse(res_untrusted2.is_authorized)
        self.assertEqual(res_untrusted2.status, AuthorizationStatus.UNKNOWN_ROOT_CA)

        # 4. Challenge-response failure
        bogus_sig = b"totally_invalid_signature_bytes_for_ec"
        res_challenge = self.engine.validate_certificate_chain(
            self.valid_chain,
            challenge=b"auth_challenge_nonce_1234",
            challenge_signature=bogus_sig,
        )
        self.assertFalse(res_challenge.is_authorized)
        self.assertEqual(res_challenge.status, AuthorizationStatus.CHALLENGE_FAILED)

        # 5. verify_iso15118_handshake wrapper function
        ok, res_id = verify_iso15118_handshake(self.valid_chain, "SESS-PNC-99")
        self.assertTrue(ok)
        self.assertTrue("FI-KEM-C12345678-X" in res_id or "CONTRACT" in res_id)


# ============================================================================
# Section 2: Anti-Fraud & Replug Detection Hardening (src/core/anti_fraud.py)
# ============================================================================

class TestTier5AntiFraudAdversarial(unittest.TestCase):
    """Tier 5 white-box probes for Anti-Phantom Replug and Session Stitching."""

    def test_safe_float_extreme_inputs(self):
        """Probe: _safe_float against corrupted and complex object types."""
        self.assertEqual(_safe_float(None, 42.0), 42.0)
        self.assertEqual(_safe_float("123.45", 0.0), 123.45)
        self.assertEqual(_safe_float("not_a_float", 99.0), 99.0)
        self.assertEqual(_safe_float(["list"], -1.0), -1.0)
        self.assertEqual(_safe_float({"dict": 1}, 0.5), 0.5)
        self.assertEqual(_safe_float(True, 0.0), 1.0)
        self.assertEqual(_safe_float(False, 0.0), 0.0)

    def test_missing_and_inverted_timestamps(self):
        """Probe: evaluate_reconnect with missing timestamps or negative reconnect delta."""
        detector = PhantomReplugDetector()
        prev = {"session_id": "S1", "vehicle_id": "V1", "charger_id": "D1"}
        curr = {"session_id": "S2", "vehicle_id": "V1", "charger_id": "D1"}

        # 1. Missing end_ts in prev
        res1 = detector.evaluate_reconnect(prev, curr)
        self.assertFalse(res1.is_phantom)
        self.assertEqual(res1.delta_time_sec, float("inf"))

        # 2. Inverted timestamps (curr start is earlier than prev end)
        prev["end_ts"] = "2026-11-13T02:10:00Z"
        curr["start_ts"] = "2026-11-13T02:08:00Z"  # -120s delta
        res2 = detector.evaluate_reconnect(prev, curr)
        self.assertEqual(res2.delta_time_sec, 0.0)  # clamped to 0.0
        self.assertTrue(res2.is_phantom)  # Delta t = 0 < 180s, SoC delta = 0 <= 1%

    def test_current_samples_edge_cases(self):
        """Probe: evaluate_reconnect with zero or negative dt in current samples."""
        detector = PhantomReplugDetector()
        prev = {
            "session_id": "S1", "vehicle_id": "V1", "charger_id": "D1",
            "end_ts": "2026-11-13T01:00:00Z", "end_soc": 50.0
        }
        curr = {
            "session_id": "S2", "vehicle_id": "V1", "charger_id": "D1",
            "start_ts": "2026-11-13T01:01:00Z", "start_soc": 50.2
        }

        # Samples with dt <= 0 should be ignored without dividing by zero
        samples_zero_dt = [{"current_a": 10.0, "time_s": 5.0}, {"current_a": 50.0, "time_s": 5.0}]
        res_zero = detector.evaluate_reconnect(prev, curr, current_samples=samples_zero_dt)
        self.assertEqual(res_zero.current_ramp_rate, 0.0)

        # Single element sample list
        res_single = detector.evaluate_reconnect(prev, curr, current_samples=[{"current_a": 10.0, "time_s": 1.0}])
        self.assertEqual(res_single.current_ramp_rate, 0.0)

        # Valid violent current ramp (>100 A/s) triggers lockout
        samples_violent = [{"current_a": 0.0, "time_s": 0.0}, {"current_a": 250.0, "time_s": 1.0}]
        res_violent = detector.evaluate_reconnect(prev, curr, current_samples=samples_violent)
        self.assertTrue(res_violent.is_phantom)
        self.assertEqual(res_violent.fraud_type, ReplugFraudType.ABNORMAL_CURRENT_RAMP)
        self.assertEqual(res_violent.action_taken, "CLAMP_CURRENT_LOCKOUT_CONTACTOR")

    def test_spatial_decoupling_fraud_classification(self):
        """Probe: Two different vehicles on two different chargers within 60s and 0% SoC delta."""
        detector = PhantomReplugDetector()
        prev = {
            "session_id": "S1", "vehicle_id": "BUS_ALPHA", "charger_id": "D1-1",
            "end_ts": "2026-11-13T02:00:00Z", "end_soc": 60.0
        }
        curr = {
            "session_id": "S2", "vehicle_id": "BUS_BETA", "charger_id": "D1-8",
            "start_ts": "2026-11-13T02:00:30Z", "start_soc": 60.0
        }
        # Neither vehicle nor charger match -> MUST be genuine new session
        res = detector.evaluate_reconnect(prev, curr)
        self.assertFalse(res.is_phantom)
        self.assertEqual(res.fraud_type, ReplugFraudType.GENUINE_NEW_SESSION)

    def test_multi_stage_sequential_stitching(self):
        """Probe: Stitching multiple sequential replugs into the root transaction."""
        detector = PhantomReplugDetector()
        s0 = {
            "session_id": "ROOT_001", "vehicle_id": "B01", "charger_id": "D1-1",
            "start_ts": "2026-11-13T01:00:00Z", "end_ts": "2026-11-13T01:30:00Z",
            "start_soc": 20.0, "end_soc": 40.0, "energy_kwh": 80.0, "max_kw": 120.0
        }
        s1 = {
            "session_id": "CHILD_002", "vehicle_id": "B01", "charger_id": "D1-1",
            "start_ts": "2026-11-13T01:31:00Z", "end_ts": "2026-11-13T02:00:00Z",
            "start_soc": 40.1, "end_soc": 60.0, "energy_kwh": 70.0, "max_kw": 140.0
        }
        s2 = {
            "session_id": "CHILD_003", "vehicle_id": "B01", "charger_id": "D1-1",
            "start_ts": "2026-11-13T02:01:00Z", "end_ts": "2026-11-13T02:30:00Z",
            "start_soc": 60.2, "end_soc": 80.0, "energy_kwh": 65.0, "max_kw": 110.0
        }

        ok1, m1 = anti_phantom_replug_check(s0, s1)
        self.assertTrue(ok1)
        self.assertEqual(m1["stitch_count"], 1)
        self.assertEqual(m1["duplicate_base_fee_waived_eur"], 2.50)
        self.assertAlmostEqual(m1["energy_kwh"], 150.0)

        ok2, m2 = anti_phantom_replug_check(m1, s2)
        self.assertTrue(ok2)
        self.assertEqual(m2["stitch_count"], 2)
        self.assertEqual(m2["duplicate_base_fee_waived_eur"], 5.00)
        self.assertAlmostEqual(m2["energy_kwh"], 215.0)
        self.assertEqual(m2["max_kw"], 140.0)
        self.assertEqual(m2["child_session_ids"], ["CHILD_002", "CHILD_003"])


# ============================================================================
# Section 3: DPR Matrix & Physical Contactor Hardening (src/core/dpr_matrix.py)
# ============================================================================

class TestTier5DPRMatrixAdversarial(unittest.TestCase):
    """Tier 5 white-box probes for Kempower DPR Matrix Contactor Sequencing."""

    def test_power_module_wear_index_and_attributes(self):
        """Probe: calculate_wear_index with cold ambient and zero cycles."""
        pm = PowerModule(
            module_id="TEST_MOD_01",
            cabinet_id="C1-1",
            temperature_c=10.0,
            operating_hours=100.0,
            start_stop_cycles=20,
        )
        # ambient 25°C > temperature 10°C -> thermal_excess = 0
        w = pm.calculate_wear_index(ambient_temp_c=25.0)
        self.assertEqual(w, 100.0 + 0.05 * 20)  # 101.0

    def test_break_before_make_sequence_dict_and_bool_protocol(self):
        """Probe: BreakBeforeMakeSequence dict indexing, boolean conversion, and KeyErrors."""
        step = BreakBeforeMakeStep("STEP1", duration_ms=20.0, current_amps=0.0)
        seq = BreakBeforeMakeSequence(
            module_id="MOD_01",
            from_gun="D1-1",
            to_gun="D1-2",
            steps=[step],
            total_duration_ms=20.0,
            is_zero_arc_compliant=True,
            transferred_modules=2,
        )
        self.assertTrue(bool(seq))
        self.assertEqual(seq["switching_delay_ms"], 20.0)
        self.assertEqual(seq["transferred_modules"], 2)
        self.assertEqual(seq.get("non_existent_key", "DEFAULT"), "DEFAULT")
        with self.assertRaises(KeyError):
            _ = seq["illegal_key"]

    def test_dpr_allocation_result_dict_interface(self):
        """Probe: DPRAllocationResult full dict interface implementation."""
        res = DPRAllocationResult(
            station_id="S1",
            allocated_power={"D1-1": 100.0, "D1-2": 50.0},
            modules_per_gun={"D1-1": 4, "D1-2": 2},
            ac_grid_draw_kw=157.07,
            dc_total_kw=150.0,
            grid_limit_kw=1200.0,
            is_safe=True,
            unmet_power_kw=0.0,
        )
        self.assertEqual(len(res), 2)
        self.assertIn("D1-1", res)
        self.assertNotIn("D1-99", res)
        self.assertEqual(res["D1-1"], 100.0)
        self.assertEqual(res.get("D1-99", 0.0), 0.0)
        self.assertEqual(list(res.keys()), ["D1-1", "D1-2"])
        self.assertEqual(list(res.values()), [100.0, 50.0])
        self.assertEqual(len(list(iter(res))), 2)

    def test_is_charger_match_strict_prefix_boundaries(self):
        """Probe: _is_charger_match across exact, sub-gun, and false prefix collisions."""
        # Exact match
        self.assertTrue(DPRMatrix._is_charger_match("D1-1", "D1-1"))
        # Legal sub-guns
        self.assertTrue(DPRMatrix._is_charger_match("D1-1A", "D1-1"))
        self.assertTrue(DPRMatrix._is_charger_match("D1-1_B", "D1-1"))
        self.assertTrue(DPRMatrix._is_charger_match("D1-1:1", "D1-1"))
        # Rejection of numerical extensions (the P0-1 bug!)
        self.assertFalse(DPRMatrix._is_charger_match("D1-10", "D1-1"))
        self.assertFalse(DPRMatrix._is_charger_match("D1-11", "D1-1"))
        self.assertFalse(DPRMatrix._is_charger_match("D1-12", "D1-1"))
        self.assertFalse(DPRMatrix._is_charger_match("D1-19", "D1-1"))
        # Unrelated charger
        self.assertFalse(DPRMatrix._is_charger_match("D1-2", "D1-1"))

    def test_custom_topology_and_unknown_station_fallback(self):
        """Probe: _init_topology with custom cabinet configs and generic fallback."""
        custom_cabs = [
            {"cabinet_id": "C_TEST_1", "modules": 8},
            {"cabinet_id": "C_TEST_2", "modules": 6},
        ]
        dpr_custom = DPRMatrix(station_id="S_UNKNOWN", cabinet_configs=custom_cabs)
        self.assertEqual(len(dpr_custom.modules), 14)

        # Unknown station without custom cabs
        dpr_fallback = DPRMatrix(station_id="S_UNKNOWN_2", total_modules=10)
        self.assertEqual(len(dpr_fallback.modules), 10)

    def test_allocate_intra_cabinet_continuous_cross_cabinet_prohibition(self):
        """Probe: allocate_intra_cabinet_continuous raising ValueError on cross-cabinet requests."""
        dpr = DPRMatrix(station_id="S1")
        # D1-9 is physically wired to C1-3, NOT C1-1!
        with self.assertRaises(ValueError) as ctx:
            dpr.allocate_intra_cabinet_continuous(
                cabinet_id="C1-1",
                requests_kw={"D1-9": 100.0},
            )
        self.assertIn("Cross-cabinet routing prohibited", str(ctx.exception))

        # Unknown cabinet name
        with self.assertRaises(ValueError) as ctx2:
            dpr.allocate_intra_cabinet_continuous(
                cabinet_id="C1-999",
                requests_kw={"D1-1": 50.0},
            )
        self.assertIn("Unknown cabinet", str(ctx2.exception))

    def test_allocate_intra_cabinet_continuous_zero_grid_limit_and_derating(self):
        """Probe: allocate_intra_cabinet_continuous with 0 kW grid limit or 0 health."""
        dpr = DPRMatrix(station_id="S1")
        # 0 kW grid limit
        res_zero = dpr.allocate_intra_cabinet_continuous(
            requests_kw={"D1-1": 100.0, "D1-2": 50.0},
            grid_limit_kw=0.0,
        )
        self.assertEqual(res_zero["D1-1"], 0.0)
        self.assertEqual(res_zero["D1-2"], 0.0)

        # Total derating on C1-1
        res_derated = dpr.allocate_intra_cabinet_continuous(
            requests_kw={"D1-1": 100.0, "D1-5": 100.0},
            cabinet_deratings={"C1-1": 0.0, "C1-2": 1.0, "C1-3": 1.0},
        )
        self.assertEqual(res_derated["D1-1"], 0.0)   # C1-1 offline
        self.assertEqual(res_derated["D1-5"], 100.0) # C1-2 online

    def test_re_route_contactor_invalid_modules_and_current_scaling(self):
        """Probe: re_route_contactor with 0 or negative modules and high current."""
        dpr = DPRMatrix(station_id="S1")
        # 0 modules
        seq_zero = dpr.re_route_contactor(from_gun="D1-1", to_gun="D1-2", modules=0)
        self.assertFalse(seq_zero.is_zero_arc_compliant)
        self.assertEqual(seq_zero.transferred_modules, 0)

        # High current ramp scaling
        seq_high_i = dpr.re_route_contactor(from_gun=None, to_gun="D1-1", modules=2, initial_current_amps=150.0)
        self.assertTrue(seq_high_i.is_zero_arc_compliant)
        self.assertLess(seq_high_i.total_duration_ms, 500.0)
        # Ramp down was lengthened by initial_current_amps
        self.assertGreater(seq_high_i.steps[0].duration_ms, 35.0)

    def test_isolate_and_restore_module_lifecycle(self):
        """Probe: isolate_module and restore_module including non-existent module."""
        dpr = DPRMatrix(station_id="S1")
        # Non-existent module
        ok_fake, _, err = dpr.isolate_module("S1_M_DOES_NOT_EXIST")
        self.assertFalse(ok_fake)
        self.assertEqual(err.get("error"), "MODULE_NOT_FOUND")

        # Restore non-existent
        self.assertFalse(dpr.restore_module("S1_M_DOES_NOT_EXIST"))

        # Valid module isolate & restore
        mod_id = list(dpr.modules.keys())[0]
        ok, dur, diag = dpr.isolate_module(mod_id, reason="OVERTEMP_CRITICAL")
        self.assertTrue(ok)
        self.assertEqual(dur, 85.0)
        self.assertEqual(dpr.modules[mod_id].status, "ISOLATED_TEMP")
        self.assertFalse(dpr.modules[mod_id].is_healthy)

        # Restore
        self.assertTrue(dpr.restore_module(mod_id))
        self.assertTrue(dpr.modules[mod_id].is_healthy)
        self.assertEqual(dpr.modules[mod_id].status, "HEALTHY")

    def test_wear_leveling_rotation_needed_check(self):
        """Probe: check_wear_leveling_rotation_needed with empty idle or runtime delta."""
        dpr = DPRMatrix(station_id="S1")
        # All modules idle initially -> no active modules
        needed, _, _, _ = dpr.check_wear_leveling_rotation_needed("C1-1")
        self.assertFalse(needed)

        # Assign one module and give it 5 hours runtime
        cab_mods = [m for m in dpr.modules.values() if m.cabinet_id == "C1-1"]
        for m in cab_mods:
            m.operating_hours = 1.0  # initialize all idle to 1.0
        cab_mods[0].assigned_gun = "D1-1"
        cab_mods[0].operating_hours = 5.0

        needed2, delta, worn, fresh = dpr.check_wear_leveling_rotation_needed("C1-1", threshold_hours=2.0)
        self.assertTrue(needed2)
        self.assertEqual(delta, 4.0)
        self.assertEqual(worn, cab_mods[0].module_id)
        self.assertEqual(fresh, cab_mods[1].module_id)


# ============================================================================
# Section 4: Self-Healing, Edge FSM & Islanding Hardening (src/core/self_healing.py)
# ============================================================================

class TestTier5SelfHealingAdversarial(unittest.TestCase):
    """Tier 5 white-box probes for Edge Micro FSM, PdM, and Offline Islanding."""

    def test_fsm_state_action_dict_access(self):
        """Probe: FSMStateAction indexing and KeyErrors."""
        action = FSMStateAction(
            site_id="S1",
            timestamp="2026-11-13T01:00:00Z",
            current_state=EdgeState.NORMAL,
            previous_state=EdgeState.NORMAL,
            action="NONE",
            safe=True,
        )
        self.assertEqual(action["current_state"], "NORMAL")
        self.assertEqual(action["safe"], True)
        self.assertEqual(action.get("unknown_key", "FALLBACK"), "FALLBACK")
        with self.assertRaises(KeyError):
            _ = action["bad_key"]

    def test_inverter_efficiency_guard_zero_and_empty_requests(self):
        """Probe: InverterEfficiencyGuard under 0 kW AC grid limit and empty requests."""
        safe_dc, mods, steady_ac = InverterEfficiencyGuard.max_safe_dc_kw(0.0)
        self.assertEqual(safe_dc, 0.0)
        self.assertEqual(mods, 0)
        self.assertEqual(steady_ac, 0.0)

        clamped = InverterEfficiencyGuard.clamp_dc_requests({}, 1200.0)
        self.assertEqual(clamped, {})

        clamped_zero_req = InverterEfficiencyGuard.clamp_dc_requests({"D1": 0.0}, 1200.0)
        self.assertEqual(clamped_zero_req["D1"], 0.0)

    def test_predictive_thermal_engine_buffer_trimming_and_low_gradient(self):
        """Probe: record_telemetry trims at 30 items, and low gradient produces 999m time_to_trip."""
        pdm = PredictiveThermalEngine()
        cab = CabinetTelemetry(cabinet_id="C1-1", cabinet_temp_c=35.0, fan_rpm=1400.0)
        for i in range(40):
            pdm.record_telemetry(cab, f"2026-11-13T01:{i:02d}:00Z")

        # Buffer capped at 30
        self.assertEqual(len(pdm.history["C1-1"]), 30)

        # Flat temp produces time_to_trip = 999.0
        trip, mig, warn, lookahead, drop, _ = pdm.evaluate_cabinet(cab)
        self.assertFalse(trip)
        self.assertFalse(mig)
        self.assertFalse(warn)
        self.assertEqual(lookahead, 999.0)

    def test_edge_fsm_dict_telemetry_all_state_transitions(self):
        """Probe: EdgeFSM._tick_from_dict covering all 5 state branches."""
        fsm = EdgeFSM(site_id="S1")

        # 1. Hardware cutoff >= 75°C
        res1 = fsm.tick({"internal_temp_c": 76.0})
        self.assertEqual(res1.current_state, EdgeState.HARDWARE_TRIP)
        self.assertEqual(res1.action, "TRIP_MAIN_BREAKER")

        # 2. Fan drop >= 20% -> LOAD_MIGRATION
        res2 = fsm.tick({"internal_temp_c": 60.0, "fan_rpm": 1200.0, "baseline_fan_rpm": 1800.0, "active_load_kw": 200.0})
        self.assertEqual(res2.current_state, EdgeState.LOAD_MIGRATION)
        self.assertEqual(res2.action, "SHIFT_LOAD_TO_PARALLEL_CABINETS")
        self.assertEqual(res2.power_shed_kw, 180.0)  # capped at 180 kW

        # 3. High temp 66°C without fan drop -> THERMAL_WARNING
        res3 = fsm.tick({"internal_temp_c": 66.0, "fan_rpm": 1800.0, "baseline_fan_rpm": 1800.0})
        self.assertEqual(res3.current_state, EdgeState.THERMAL_WARNING)
        self.assertEqual(res3.action, "DERATE_50_PCT")

        # 4. Config mismatch -> AUTO_CALIBRATED
        res4 = fsm.tick({"internal_temp_c": 40.0, "config_mismatch": True})
        self.assertEqual(res4.current_state, EdgeState.AUTO_CALIBRATED)
        self.assertEqual(res4.action, "APPLY_CONFIG_OVERRIDE")

        # 5. WAN outage -> OFFLINE_ISLANDING
        res5 = fsm.tick({"internal_temp_c": 40.0, "wan_connected": False})
        self.assertEqual(res5.current_state, EdgeState.OFFLINE_ISLANDING)
        self.assertEqual(res5.action, "ENGAGE_LOCAL_DLM_FULL_POWER")
        self.assertIsNone(res5.fallback_kw)  # naive 50 kW rejected

        # 6. Return to NORMAL
        res6 = fsm.tick({"internal_temp_c": 40.0, "wan_connected": True})
        self.assertEqual(res6.current_state, EdgeState.NORMAL)

    def test_edge_fsm_connector_cable_damage_lockout(self):
        """Probe: TelemetrySnapshot with critical connector damage trips contactor in <40ms."""
        fsm = EdgeFSM(site_id="S4")
        snap = TelemetrySnapshot(
            site_id="S4",
            active_faults=[
                {"fault_category": "connector", "severity": "critical", "charger_id": "D4-2"}
            ],
        )
        res = fsm.tick(snap)
        self.assertEqual(len(res.contactor_commands), 1)
        cmd = res.contactor_commands[0]
        self.assertEqual(cmd.action, "TRIP_SAFETY")
        self.assertEqual(cmd.target_charger, "D4-2")
        self.assertEqual(cmd.duration_ms, 40.0)

    def test_commissioning_auto_calibrator_non_s5_and_string_booleans(self):
        """Probe: CommissioningAutoCalibrator returns false for non-S5 and handles string booleans."""
        cal = CommissioningAutoCalibrator()
        ok_s1, _, _ = cal.audit_and_calibrate("S1", {"D1-1": {"max_kw": 50.0}})
        self.assertFalse(ok_s1)

        # S5 with string booleans
        s5_cfg = {
            "D5-7": {"max_kw": 50.0, "sim_active": "true"},
            "D5-8": {"max_kw": 150.0, "sim_active": "false"},
        }
        ok_s5, overrides, msgs = cal.audit_and_calibrate("S5", s5_cfg)
        self.assertTrue(ok_s5)
        self.assertEqual(overrides["D5-7"]["max_kw"], 150.0)
        self.assertEqual(overrides["D5-8"]["sim_active"], True)

    def test_nordic_cold_protection_preheating_and_simulation(self):
        """Probe: NordicColdProtectionEngine under cold soak (-15°C) and warm battery (20°C)."""
        # Warm battery (20°C >= 15°C) -> preheating inactive
        eval_warm = NordicColdProtectionEngine.evaluate_preheating_diversion(
            batt_temp_c=20.0,
            batt_capacity_kwh=400.0,
            ambient_temp_c=-10.0,
            available_dpr_kw=150.0,
        )
        self.assertFalse(eval_warm["is_preheating_active"])
        self.assertEqual(eval_warm["ptc_allocated_kw"], 0.0)

        # Sub-zero battery (-15°C < -10°C) -> c-rate limit 0.05
        eval_cold = NordicColdProtectionEngine.evaluate_preheating_diversion(
            batt_temp_c=-15.0,
            batt_capacity_kwh=400.0,
            ambient_temp_c=-15.0,
            available_dpr_kw=150.0,
        )
        self.assertTrue(eval_cold["is_preheating_active"])
        self.assertEqual(eval_cold["ptc_allocated_kw"], 25.0)  # 1 module diverted to PTC
        self.assertEqual(eval_cold["cell_charge_kw"], 20.0)    # 0.05 * 400 kWh = 20 kW

        # Simulation comparison meeting >= 35% time reduction target
        sim_cold = NordicColdProtectionEngine.simulate_cold_session_comparison(
            initial_batt_temp_c=-15.0,
            ambient_temp_c=-15.0,
            batt_capacity_kwh=400.0,
            target_kwh=100.0,
            max_dpr_kw=150.0,
        )
        self.assertTrue(sim_cold["meets_35_pct_target"])
        self.assertGreater(sim_cold["reduction_pct"], 35.0)

    def test_offline_wal_manager_batch_ack_and_empty_merkle(self):
        """Probe: OfflineWALManager multi-chunk reconciliation (>500 items) and empty Merkle root."""
        wal = OfflineWALManager(db_path=":memory:")
        # Empty DB Merkle root
        merkle_empty = wal.compute_merkle_root()
        self.assertIsInstance(merkle_empty, str)
        self.assertEqual(len(merkle_empty), 64)

        # Record 550 mock transactions
        uuids = []
        for i in range(550):
            tx_id = wal.record_offline_transaction({
                "session_id": f"OFFLINE_SESS_{i}",
                "site_id": "S3",
                "charger_id": "D3-1",
                "vehicle_id": f"V_{i}",
                "total_energy_kwh": 35.5,
            })
            uuids.append(tx_id)

        self.assertEqual(wal.count_transactions("PENDING"), 550)

        # Idempotent re-recording does not duplicate
        wal.record_offline_transaction({"transaction_uuid": uuids[0], "session_id": "OFFLINE_SESS_0"})
        self.assertEqual(wal.count_transactions("PENDING"), 550)

        # Reconcile all 550 in one call (tests lines 909-915 chunking in batches of 500)
        reconciled_count = wal.reconcile_reconnection_ack(uuids)
        self.assertEqual(reconciled_count, 550)
        self.assertEqual(wal.count_transactions("CONFIRMED"), 550)
        self.assertEqual(wal.count_transactions("PENDING"), 0)

        # Non-empty Merkle root changes
        merkle_full = wal.compute_merkle_root()
        self.assertNotEqual(merkle_full, merkle_empty)


# ============================================================================
# Section 5: Discrete Event Simulation & Physics Hardening (src/sim/discrete_sim.py)
# ============================================================================

class TestTier5DiscreteSimAdversarial(unittest.TestCase):
    """Tier 5 white-box probes for waterfilling, CV taper, and discrete simulation."""

    def test_job_properties_edge_conditions(self):
        """Probe: Job need_kwh and window_h with identical arrival/departure times."""
        t0 = datetime.fromisoformat("2026-11-13T01:00:00Z")
        job_zero_window = Job(
            vehicle_id="J_ZERO_WIN",
            arrive=t0,
            depart=t0,  # 0 second window
            battery_kwh=100.0,
            soc_in=0.5,
            soc_req=0.8,
        )
        self.assertEqual(job_zero_window.window_h, 0.05)  # clamped to 0.05h minimum
        self.assertAlmostEqual(job_zero_window.need_kwh, 30.0)

        job_satisfied = Job(
            vehicle_id="J_SAT",
            arrive=t0,
            depart=t0 + timedelta(hours=1),
            battery_kwh=100.0,
            soc_in=0.9,
            soc_req=0.8,  # in > req
        )
        self.assertEqual(job_satisfied.need_kwh, 0.0)

    def test_waterfill_allocate_zero_pool_and_capped_limits(self):
        """Probe: waterfill_allocate with zero capacity pool or zero weights."""
        t0 = datetime.fromisoformat("2026-11-13T01:00:00Z")
        j1 = Job("J1", t0, t0 + timedelta(hours=1), 100.0, 0.2, 0.8, 150.0)
        j2 = Job("J2", t0, t0 + timedelta(hours=1), 100.0, 0.2, 0.8, 150.0)

        # Pool <= 0
        alloc_zero = waterfill_allocate([j1, j2], cap_kw=0.0, weight_fn=lambda x: 1.0, limit_fn=lambda x: 150.0)
        self.assertEqual(alloc_zero["J1"], 0.0)
        self.assertEqual(alloc_zero["J2"], 0.0)

        # Total weight <= 0
        alloc_zero_w = waterfill_allocate([j1, j2], cap_kw=100.0, weight_fn=lambda x: 0.0, limit_fn=lambda x: 150.0)
        self.assertEqual(alloc_zero_w["J1"], 0.0)

    def test_discrete_sim_fcfs_with_movement_delay(self):
        """Probe: run_discrete_event_simulation under FCFS strategy with 10-minute move delay."""
        t0 = datetime.fromisoformat("2026-11-13T01:00:00Z")
        jobs = [
            Job("J_A", t0, t0 + timedelta(hours=1), 100.0, 0.2, 0.8, 150.0),
            Job("J_B", t0, t0 + timedelta(hours=1), 100.0, 0.2, 0.8, 150.0),
        ]
        res = run_discrete_event_simulation(
            jobs=jobs,
            site_id="S_FCFS",
            date="2026-11-13",
            cabinet_kw=[300.0],
            points_per_cabinet=1,  # Only 1 point for 2 vehicles!
            strategy="fcfs",
            move_delay_min=10.0,
        )
        self.assertEqual(res.strategy, "fcfs")
        self.assertGreaterEqual(res.moves, 1)

    def test_discrete_sim_without_cross_tie_fault_stranding(self):
        """Probe: Fault injection with cross_tie=False stranding vehicles on dead cabinet."""
        t0 = datetime.fromisoformat("2026-11-13T01:00:00Z")
        jobs = [
            Job("J_CAB0", t0, t0 + timedelta(hours=2), 100.0, 0.2, 0.8, 150.0),
            Job("J_CAB1", t0, t0 + timedelta(hours=2), 100.0, 0.2, 0.8, 150.0),
        ]
        # Cabinet 0 trips at 01:10
        fault_ts = t0 + timedelta(minutes=10)
        res = run_discrete_event_simulation(
            jobs=jobs,
            site_id="S_NOCROSSTIE",
            date="2026-11-13",
            cabinet_kw=[150.0, 150.0],
            points_per_cabinet=1,
            strategy="urgency",
            fault=(fault_ts, [0]),
            cross_tie=False,  # NO cross-tie!
        )
        self.assertGreater(res.points_lost, 0)

    def test_simulate_closed_loop_minute_by_minute_generic_fallback(self):
        """Probe: simulate_closed_loop_minute_by_minute on non-S1/S2/S5 station (lines 506-517)."""
        res_generic = simulate_closed_loop_minute_by_minute(site_id="S4", date="2026-11-13")
        self.assertEqual(res_generic["site_id"], "S4")
        self.assertIn("missed_departures", res_generic)
        self.assertIn("vehicle_records", res_generic)


# ============================================================================
# Section 6: Master Scenario Engine Integration Hardening (src/sim/scenario_engine.py)
# ============================================================================

class TestTier5ScenarioEngineMasterRollup(unittest.TestCase):
    """Tier 5 white-box probes for master closed-loop scenario verification."""

    @classmethod
    def setUpClass(cls):
        cls.engine = ScenarioEngine()

    def test_s1_scenario_detailed_structure(self):
        """Probe: run_s1_scenario outputs and invariants."""
        s1 = self.engine.run_s1_scenario()
        self.assertEqual(s1["site_id"], "S1")
        self.assertEqual(s1["baseline_missed_departures"], 4)
        self.assertEqual(s1["baseline_deficit_kwh"], 1012.00)
        self.assertEqual(s1["optimized_missed_departures"], 0)
        self.assertEqual(s1["optimized_deficit_kwh"], 0.0)
        self.assertEqual(s1["n1_post_fault_audit"]["post_fault_n1_capacity_kw"], 720.0)

    def test_s2_scenario_detailed_structure(self):
        """Probe: run_s2_scenario outputs and invariants."""
        s2 = self.engine.run_s2_scenario()
        self.assertEqual(s2["site_id"], "S2")
        self.assertEqual(s2["baseline_missed_departures"], 4)
        self.assertEqual(s2["baseline_deficit_kwh"], 283.50)
        self.assertEqual(s2["optimized_missed_departures"], 0)
        self.assertEqual(s2["optimized_deficit_kwh"], 0.0)

    def test_s3_scenario_detailed_structure(self):
        """Probe: run_s3_scenario outputs and invariants."""
        s3 = self.engine.run_s3_scenario()
        self.assertEqual(s3["site_id"], "S3")
        self.assertEqual(s3["offline_islanding_state"], "OFFLINE_ISLANDING")
        self.assertEqual(s3["offline_max_safe_dc_kw"], 1425.0)

    def test_s4_and_price_spike_scenario_detailed_structure(self):
        """Probe: run_s4_and_price_spike_scenario outputs and invariants."""
        s4 = self.engine.run_s4_and_price_spike_scenario()
        self.assertEqual(s4["spot_spike_eur_mwh"], 799.30)
        self.assertEqual(len(s4["mpc_extreme_price_unmet_vehicles"]), 0)
        self.assertEqual(s4["zero_capex_load_shifting_enabled"], True)

    def test_s5_scenario_detailed_structure(self):
        """Probe: run_s5_scenario outputs and invariants."""
        s5 = self.engine.run_s5_scenario()
        self.assertEqual(s5["site_id"], "S5")
        self.assertEqual(s5["baseline_missed_departures"], 5)
        self.assertEqual(s5["baseline_deficit_kwh"], 508.95)
        self.assertEqual(s5["optimized_missed_departures"], 0)
        self.assertEqual(s5["optimized_deficit_kwh"], 0.0)

    def test_run_all_scenarios_deterministic_roll_up(self):
        """Probe: run_all_scenarios master roll-up verifies 13 -> 0 scenario day missed departures."""
        res = self.engine.run_all_scenarios()
        self.assertEqual(res["scenario_day_missed_before"], 13)
        self.assertEqual(res["scenario_day_missed_after"], 0)
        self.assertTrue(res["network_zero_over_limit"])


if __name__ == "__main__":
    unittest.main()
