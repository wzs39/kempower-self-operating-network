"""
Unit & Integration Test Suite for OCPP 2.0.1 and ISO 15118-2/20 Plug & Charge Subsystems
Test File: tests/test_protocols_ocpp_iso.py

Verifies:
- F07: OCPP 2.0.1 Smart Charging Profiles (SetChargingProfile, ClearChargingProfile, ChargingNeeds, CostUpdated)
- F08: OCPP 2.0.1 Device Model Monitoring (NotifyEventRequest, Component-Variable model)
- F09: ISO 15118-2/20 Plug & Charge Mutual TLS 1.3 PKI, X.509 v3 verification (<1.5s), MCS & V2G
"""

import datetime
import unittest
import numpy as np

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
    X509CertValidationResult,
    MCSChargeParameters,
    CertificateAuthorityManager,
    Iso15118PnCEngine,
    build_ocpp_tx_profile,
    parse_charging_needs,
    build_notify_event_from_snapshot,
    build_cost_updated_request,
    verify_iso15118_handshake,
)
from src.core.mpc_optimizer import VehicleSchedule
from src.core.self_healing import CabinetTelemetry, ChargerTelemetry, TelemetrySnapshot


class TestOCPP201ProtocolEngine(unittest.TestCase):
    """F07 & F08: OCPP 2.0.1 Smart Charging and Device Model Tests."""

    def test_set_charging_profile_tx_profile_serialization(self):
        """Verify standard TxProfile serialization conforms to OCPP 2.0.1 schema."""
        period = ChargingSchedulePeriod(startPeriod=0, limit=150000.0)
        sched = ChargingSchedule(
            id=101,
            chargingRateUnit=ChargingRateUnitEnum.W,
            chargingSchedulePeriod=[period],
            duration=3600,
        )
        profile = ChargingProfile(
            id=201,
            stackLevel=1,
            chargingProfilePurpose=ChargingProfilePurposeEnum.TX_PROFILE,
            chargingProfileKind=ChargingProfileKindEnum.RELATIVE,
            chargingSchedule=sched,
            transactionId="TX-9988",
        )
        req = SetChargingProfileRequest(evseId=1, chargingProfile=profile)
        payload = req.to_dict()

        self.assertEqual(payload["evseId"], 1)
        self.assertEqual(payload["chargingProfile"]["id"], 201)
        self.assertEqual(payload["chargingProfile"]["chargingProfilePurpose"], "TxProfile")
        self.assertEqual(payload["chargingProfile"]["chargingProfileKind"], "Relative")
        self.assertEqual(payload["chargingProfile"]["transactionId"], "TX-9988")
        self.assertEqual(len(payload["chargingProfile"]["chargingSchedule"]), 1)
        self.assertEqual(payload["chargingProfile"]["chargingSchedule"][0]["chargingRateUnit"], "W")
        self.assertEqual(
            payload["chargingProfile"]["chargingSchedule"][0]["chargingSchedulePeriod"][0]["limit"],
            150000.0,
        )

    def test_set_charging_profile_round_trip(self):
        """Verify from_dict correctly deserializes SetChargingProfileRequest."""
        period = ChargingSchedulePeriod(startPeriod=900, limit=200000.0)
        sched = ChargingSchedule(
            id=102,
            chargingRateUnit=ChargingRateUnitEnum.W,
            chargingSchedulePeriod=[period],
            duration=1800,
        )
        profile = ChargingProfile(
            id=202,
            stackLevel=2,
            chargingProfilePurpose=ChargingProfilePurposeEnum.CHARGING_STATION_MAX_PROFILE,
            chargingProfileKind=ChargingProfileKindEnum.ABSOLUTE,
            chargingSchedule=sched,
        )
        req = SetChargingProfileRequest(evseId=0, chargingProfile=profile)
        d = req.to_dict()

        reconstructed = SetChargingProfileRequest.from_dict(d)
        self.assertEqual(reconstructed.evseId, 0)
        self.assertEqual(reconstructed.chargingProfile.id, 202)
        self.assertEqual(
            reconstructed.chargingProfile.chargingProfilePurpose,
            ChargingProfilePurposeEnum.CHARGING_STATION_MAX_PROFILE,
        )
        self.assertEqual(
            reconstructed.chargingProfile.chargingProfileKind,
            ChargingProfileKindEnum.ABSOLUTE,
        )

    def test_clear_charging_profile(self):
        """Verify ClearChargingProfileRequest and response payload formats."""
        req = ClearChargingProfileRequest(
            chargingProfileId=202,
            chargingProfileCriteria={"evseId": 1, "chargingProfilePurpose": "TxProfile"},
        )
        d = req.to_dict()
        self.assertEqual(d["chargingProfileId"], 202)
        self.assertEqual(d["chargingProfileCriteria"]["evseId"], 1)

        resp = ClearChargingProfileResponse(status=ClearChargingProfileStatusEnum.ACCEPTED)
        self.assertEqual(resp.to_dict()["status"], "Accepted")

    def test_build_ocpp_tx_profile_from_mpc_schedule(self):
        """Verify build_ocpp_tx_profile constructs valid profile in Watts."""
        sched = VehicleSchedule(
            vehicle_id="B01",
            arrive_step=0,
            depart_step=4,
            arrive_soc=0.20,
            required_soc=0.85,
            battery_kwh=150.0,
            max_charge_kw=150.0,
        )
        power_array = [100.0, 150.0, 150.0, 50.0]  # kW per 15-min interval
        payload = build_ocpp_tx_profile(
            schedule=sched,
            interval_minutes=15,
            power_array=power_array,
            evse_id=2,
            transaction_id="TX-B01-S1",
        )

        self.assertEqual(payload["evseId"], 2)
        cp = payload["chargingProfile"]
        self.assertEqual(cp["transactionId"], "TX-B01-S1")
        periods = cp["chargingSchedule"][0]["chargingSchedulePeriod"]
        self.assertEqual(len(periods), 4)
        self.assertEqual(periods[0]["limit"], 100000.0)  # 100 kW -> 100,000 W
        self.assertEqual(periods[1]["limit"], 150000.0)
        self.assertEqual(periods[3]["limit"], 50000.0)

    def test_parse_charging_needs_conversion(self):
        """Verify parse_charging_needs converts ISO 15118 EV needs into MPC VehicleSchedule."""
        payload = {
            "evseId": 3,
            "vehicleId": "TRUCK-44",
            "departureTime": "2026-11-13T04:00:00+02:00",
            "dcChargingParameters": {
                "evMaxCurrent": 300.0,
                "evMaxVoltage": 800.0,
                "evEnergyCapacity": 200000.0,  # 200 kWh in Wh
                "stateOfCharge": 25.0,
                "fullSoC": 90.0,
            },
        }
        current_time = "2026-11-13T02:00:00+02:00"  # 2 hours dwell = 8 steps (15-min)
        schedule = parse_charging_needs(payload, current_time_iso=current_time)

        self.assertEqual(schedule.vehicle_id, "TRUCK-44")
        self.assertEqual(schedule.arrive_step, 0)
        self.assertEqual(schedule.depart_step, 8)
        self.assertAlmostEqual(schedule.arrive_soc, 0.25)
        self.assertAlmostEqual(schedule.required_soc, 0.90)
        self.assertEqual(schedule.battery_kwh, 200.0)
        self.assertEqual(schedule.max_charge_kw, 240.0)  # 300A * 800V / 1000 = 240 kW

    def test_notify_event_from_snapshot(self):
        """Verify build_notify_event_from_snapshot formats Component-Variable events."""
        snap = TelemetrySnapshot(
            site_id="S1",
            timestamp="2026-11-13T02:30:00+02:00",
            cabinets={
                "C1-1": CabinetTelemetry(
                    cabinet_id="C1-1",
                    cabinet_temp_c=62.5,  # >= 59.3°C triggers PreAlert
                    fan_rpm=1100.0,
                    nominal_fan_rpm=1400.0,  # 21.4% drop triggers FanSpeed warning
                ),
                "C1-2": CabinetTelemetry(
                    cabinet_id="C1-2",
                    cabinet_temp_c=76.2,  # >= 75.0°C triggers Emergency trip
                    fan_rpm=1380.0,
                ),
            },
            chargers={},
            active_faults=[
                {"fault_category": "insulation_ground_fault", "cabinet_id": "C1-1"}
            ],
        )

        event_req = build_notify_event_from_snapshot(snap, seq_no=42)
        self.assertEqual(event_req["seqNo"], 42)
        events = event_req["eventData"]
        self.assertGreaterEqual(len(events), 3)

        comps = [e["component"]["name"] for e in events]
        self.assertIn("CoolingSystem", comps)
        self.assertIn("FanSpeed", comps)
        self.assertIn("IsolationMonitoringDevice", comps)

    def test_cost_updated_request_streaming(self):
        """Verify dynamic electricity tariff streaming payload."""
        req = build_cost_updated_request(
            total_cost=42.75,
            transaction_id="TX-55",
            spot_price_mwh=799.30,  # Scenario Day peak price
            tariff_eur_kwh=0.024,
        )
        self.assertEqual(req["transactionId"], "TX-55")
        self.assertEqual(req["totalCost"], 42.75)
        self.assertEqual(req["currency"], "EUR")
        expected_rate = (799.30 / 1000.0) + 0.024  # 0.8233 EUR/kWh
        self.assertAlmostEqual(req["currentRateEurKwh"], expected_rate, places=4)


class TestISO15118PlugAndCharge(unittest.TestCase):
    """F09: ISO 15118-2/20 Plug & Charge Handshake & PKI Tests."""

    @classmethod
    def setUpClass(cls):
        (
            cls.pem_chain,
            cls.leaf_key,
            cls.leaf_cert,
            cls.sub_cert,
            cls.root_cert,
        ) = CertificateAuthorityManager.generate_test_pki_hierarchy()
        cls.ca_manager = CertificateAuthorityManager()
        cls.ca_manager.add_trusted_root(cls.root_cert)

    def test_pnc_valid_chain_handshake_speed(self):
        """Verify authentic 3-tier X.509 v3 chain validates successfully in < 1500 ms."""
        engine = Iso15118PnCEngine(self.ca_manager)
        res = engine.validate_certificate_chain(self.pem_chain)

        self.assertTrue(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.ACCEPTED)
        self.assertEqual(res.emaid, "FI-KEM-C12345678-X")
        self.assertLess(
            res.duration_ms,
            1500.0,
            f"Handshake took {res.duration_ms} ms, exceeding 1500 ms SLA",
        )

    def test_verify_iso15118_handshake_public_api(self):
        """Verify public contract verify_iso15118_handshake() returns (True, emaid)."""
        is_auth, contract_id = verify_iso15118_handshake(self.pem_chain, "SESS-001")
        self.assertTrue(is_auth)
        self.assertEqual(contract_id, "FI-KEM-C12345678-X")

    def test_pnc_revoked_certificate(self):
        """Verify revoked certificate in CRL blacklist is rejected."""
        ca_mgr = CertificateAuthorityManager()
        ca_mgr.add_trusted_root(self.root_cert)
        ca_mgr.revoke_serial(self.leaf_cert.serial_number)

        engine = Iso15118PnCEngine(ca_mgr)
        res = engine.validate_certificate_chain(self.pem_chain)
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.CERTIFICATE_REVOKED)

    def test_pnc_expired_certificate(self):
        """Verify expired certificate is rejected."""
        engine = Iso15118PnCEngine(self.ca_manager)
        # Evaluate 5 years in the future
        future_time = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=1825)
        res = engine.validate_certificate_chain(self.pem_chain, now=future_time)
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.CERTIFICATE_EXPIRED)

    def test_pnc_tampered_signature(self):
        """Verify corrupted signature is caught and rejected."""
        tampered_pem = self.pem_chain.replace("A", "B", 1)
        engine = Iso15118PnCEngine(self.ca_manager)
        res = engine.validate_certificate_chain(tampered_pem)
        self.assertFalse(res.is_authorized)
        self.assertIn(
            res.status,
            [
                AuthorizationStatus.INVALID_SIGNATURE,
                AuthorizationStatus.MALFORMED_CERTIFICATE,
            ],
        )

    def test_pnc_untrusted_root_ca(self):
        """Verify untrusted Root CA is flagged when trust store is active."""
        empty_ca_mgr = CertificateAuthorityManager()
        # Do not add root_cert to trusted store
        engine = Iso15118PnCEngine(empty_ca_mgr)
        # Add a different dummy root to enable checking
        dummy_key = ec.generate_private_key(ec.SECP256R1())
        dummy_name = x509.Name([
            x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "Other Root CA"),
        ])
        now = datetime.datetime.now(datetime.timezone.utc)
        dummy_cert = (
            x509.CertificateBuilder()
            .subject_name(dummy_name)
            .issuer_name(dummy_name)
            .public_key(dummy_key.public_key())
            .serial_number(9999)
            .not_valid_before(now - datetime.timedelta(days=10))
            .not_valid_after(now + datetime.timedelta(days=100))
            .sign(dummy_key, hashes.SHA256())
        )
        empty_ca_mgr.add_trusted_root(dummy_cert)

        res = engine.validate_certificate_chain(self.pem_chain)
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.UNKNOWN_ROOT_CA)

    def test_pnc_challenge_response(self):
        """Verify optional GenChallenge vehicle signature validation."""
        engine = Iso15118PnCEngine(self.ca_manager)
        challenge = b"CHALLENGE_KEMPOWER_RANDOM_NONCE_12345"
        valid_signature = self.leaf_key.sign(challenge, ec.ECDSA(hashes.SHA256()))

        res = engine.validate_certificate_chain(
            self.pem_chain, challenge=challenge, challenge_signature=valid_signature
        )
        self.assertTrue(res.is_authorized)

        # Invalid challenge signature
        bad_sig = b"CORRUPTED_SIGNATURE_BYTES"
        res_bad = engine.validate_certificate_chain(
            self.pem_chain, challenge=challenge, challenge_signature=bad_sig
        )
        self.assertFalse(res_bad.is_authorized)
        self.assertEqual(res_bad.status, AuthorizationStatus.CHALLENGE_FAILED)

    def test_mcs_and_v2g_parameters(self):
        """Verify Megawatt Charging System (MCS) and V2G bidirectional transfer envelope."""
        params = MCSChargeParameters(
            ev_max_voltage_v=1250.0,
            ev_max_current_a=3000.0,
            ev_max_power_kw=3750.0,
            v2g_bpt_enabled=True,
            v2g_max_discharge_kw=250.0,
            v2g_min_soc_pct=25.0,
            reactive_power_var=50000.0,
        )
        self.assertEqual(params.ev_max_voltage_v, 1250.0)
        self.assertEqual(params.ev_max_current_a, 3000.0)
        self.assertEqual(params.ev_max_power_kw, 3750.0)
        self.assertTrue(params.v2g_bpt_enabled)
        self.assertEqual(params.v2g_max_discharge_kw, 250.0)


if __name__ == "__main__":
    unittest.main()
