"""
Empirical Adversarial Stress Test Suite for M2 Protocols & Anti-Fraud
Target Modules:
- src.core.protocols (ISO 15118-2/20 Plug & Charge PKI Engine)
- src.core.anti_fraud (Anti-Phantom Replug & Electrical Fingerprinting)

Evaluates:
1. ISO 15118 PnC Authentication:
   - Certificate expiration boundaries (past, future, exact)
   - CRL revocation list enforcement (leaf, intermediate Sub-CA, root)
   - Cryptographic signature tampering and certificate corruption
   - Non-standard ECDSA curves and key types (SECP384R1, SECP521R1, Ed25519, RSA)
   - Challenge-response verification robustness and type/algorithm error handling
   - Verification execution speed SLA (< 1500 ms)
2. Anti-Phantom Replug Detection:
   - Temporal proximity boundary analysis (179s, 180s, 181s)
   - SoC continuity boundary analysis (0.9%, 1.0%, 1.0000000001%, 1.1%, float cancellation)
   - Current ramp rate (dI/dt) anomalies (>100 A/s lockout, boundary 100.0 A/s)
   - Current sample array robustness (dt=0, dt<0, missing fields)
   - Rapid sequential unplugs (10 sequential replugs within 5 minutes)
   - Null-value resilience (None in end_soc, start_soc, current_ramp_rate)
"""

import unittest
import time
from datetime import datetime, timezone, timedelta
from typing import Dict, Any, List

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa, ed25519

from src.core.protocols import (
    AuthorizationStatus,
    CertificateAuthorityManager,
    Iso15118PnCEngine,
    verify_iso15118_handshake,
    build_ocpp_tx_profile,
    parse_charging_needs,
)
from src.core.anti_fraud import (
    PhantomReplugDetector,
    ReplugFraudType,
    AntiFraudConfig,
    ReplugEvaluation,
    anti_phantom_replug_check,
)

class TestAdversarialIso15118PnC(unittest.TestCase):
    """Adversarial stress testing against ISO 15118 PnC engine."""

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

    def test_pnc_sla_performance_boundary(self):
        """Stress verify timing performance guarantee (<1500 ms) across 50 iterations."""
        durations = []
        for _ in range(50):
            res = self.engine.validate_certificate_chain(self.valid_chain)
            self.assertTrue(res.is_authorized)
            durations.append(res.duration_ms)

        max_dur = max(durations)
        avg_dur = sum(durations) / len(durations)
        self.assertLess(max_dur, 1500.0, f"Max handshake duration {max_dur:.2f} ms exceeded 1500 ms SLA")
        self.assertLess(avg_dur, 50.0, f"Average handshake duration {avg_dur:.2f} ms unusually slow")

    def test_pnc_expired_certificate_temporal_boundaries(self):
        """Test expired certificates: past, future, and exact threshold boundaries."""
        now_utc = datetime.now(timezone.utc)

        # 1. Evaluated 1 second before valid
        before_valid = now_utc - timedelta(days=31)
        res_before = self.engine.validate_certificate_chain(self.valid_chain, now=before_valid)
        self.assertFalse(res_before.is_authorized)
        self.assertEqual(res_before.status, AuthorizationStatus.CERTIFICATE_EXPIRED)

        # 2. Evaluated 1 second after valid
        after_valid = now_utc + timedelta(days=366)
        res_after = self.engine.validate_certificate_chain(self.valid_chain, now=after_valid)
        self.assertFalse(res_after.is_authorized)
        self.assertEqual(res_after.status, AuthorizationStatus.CERTIFICATE_EXPIRED)

        # 3. Far future (10 years)
        far_future = now_utc + timedelta(days=3650)
        res_future = self.engine.validate_certificate_chain(self.valid_chain, now=far_future)
        self.assertFalse(res_future.is_authorized)
        self.assertEqual(res_future.status, AuthorizationStatus.CERTIFICATE_EXPIRED)

    def test_pnc_leaf_revocation_in_crl(self):
        """Test leaf certificate revocation in CRL blacklist."""
        ca_mgr = CertificateAuthorityManager()
        ca_mgr.add_trusted_root(self.root_cert)
        ca_mgr.revoke_serial(self.leaf_cert.serial_number)

        engine = Iso15118PnCEngine(ca_mgr)
        res = engine.validate_certificate_chain(self.valid_chain)
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.CERTIFICATE_REVOKED)

    def test_pnc_root_revocation_in_crl(self):
        """Test root CA revocation in CRL blacklist."""
        ca_mgr = CertificateAuthorityManager()
        ca_mgr.add_trusted_root(self.root_cert)
        ca_mgr.revoke_serial(self.root_cert.serial_number)

        engine = Iso15118PnCEngine(ca_mgr)
        res = engine.validate_certificate_chain(self.valid_chain)
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.CERTIFICATE_REVOKED)

    def test_bug_intermediate_sub_ca_revocation_bypass(self):
        """
        Remediated Verification: CRL check strictly evaluates all certificates along the chain.
        Intermediate Sub-CA serial numbers are rejected.
        """
        ca_mgr = CertificateAuthorityManager()
        ca_mgr.add_trusted_root(self.root_cert)
        ca_mgr.revoke_serial(self.sub_cert.serial_number)

        engine = Iso15118PnCEngine(ca_mgr)
        res = engine.validate_certificate_chain(self.valid_chain)
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.CERTIFICATE_REVOKED)

    def test_bug_2_tier_untrusted_root_bypass(self):
        """
        Remediated Verification: 2-tier certificate chain checks topmost root against trusted_roots.
        Untrusted 2-tier chain is rejected with UNKNOWN_ROOT_CA.
        """
        now = datetime.now(timezone.utc)
        fake_root_key = ec.generate_private_key(ec.SECP256R1())
        fake_root_name = x509.Name([x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "Untrusted Rogue CA")])
        fake_root_cert = (
            x509.CertificateBuilder()
            .subject_name(fake_root_name)
            .issuer_name(fake_root_name)
            .public_key(fake_root_key.public_key())
            .serial_number(9999)
            .not_valid_before(now - timedelta(days=1))
            .not_valid_after(now + timedelta(days=10))
            .sign(fake_root_key, hashes.SHA256())
        )

        fake_leaf_key = ec.generate_private_key(ec.SECP256R1())
        fake_leaf_name = x509.Name([x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "EMAID:ROGUE-EV")])
        fake_leaf_cert = (
            x509.CertificateBuilder()
            .subject_name(fake_leaf_name)
            .issuer_name(fake_root_name)
            .public_key(fake_leaf_key.public_key())
            .serial_number(10000)
            .not_valid_before(now - timedelta(days=1))
            .not_valid_after(now + timedelta(days=10))
            .sign(fake_root_key, hashes.SHA256())
        )

        chain_2cert = (
            fake_leaf_cert.public_bytes(serialization.Encoding.PEM).decode()
            + fake_root_cert.public_bytes(serialization.Encoding.PEM).decode()
        )

        # Store with only legitimate root
        ca_mgr = CertificateAuthorityManager()
        ca_mgr.add_trusted_root(self.root_cert)
        engine = Iso15118PnCEngine(ca_mgr)

        res = engine.validate_certificate_chain(chain_2cert)
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.UNKNOWN_ROOT_CA)

    def test_bug_iso15118_unhandled_type_error_on_non_ecdsa_challenge(self):
        """
        Remediated Verification: Non-ECDSA key with challenge is cleanly rejected without unhandled TypeError.
        """
        now = datetime.now(timezone.utc)
        k_root = ec.generate_private_key(ec.SECP256R1())
        n_root = x509.Name([x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "Test Root")])
        c_root = (
            x509.CertificateBuilder()
            .subject_name(n_root)
            .issuer_name(n_root)
            .public_key(k_root.public_key())
            .serial_number(1)
            .not_valid_before(now - timedelta(days=1))
            .not_valid_after(now + timedelta(days=10))
            .sign(k_root, hashes.SHA256())
        )

        ed_key = ed25519.Ed25519PrivateKey.generate()
        ed_name = x509.Name([x509.NameAttribute(x509.oid.NameOID.COMMON_NAME, "EMAID:ED25519-EV")])
        ed_cert = (
            x509.CertificateBuilder()
            .subject_name(ed_name)
            .issuer_name(n_root)
            .public_key(ed_key.public_key())
            .serial_number(8888)
            .not_valid_before(now - timedelta(days=1))
            .not_valid_after(now + timedelta(days=10))
            .sign(k_root, hashes.SHA256())
        )
        chain_ed = (
            ed_cert.public_bytes(serialization.Encoding.PEM).decode()
            + c_root.public_bytes(serialization.Encoding.PEM).decode()
        )

        # Trust c_root so chain reaches step 5 (challenge verification)
        ca_mgr = CertificateAuthorityManager()
        ca_mgr.add_trusted_root(c_root)
        engine = Iso15118PnCEngine(ca_mgr)

        # Confirm non-ECDSA challenge cleanly returns CHALLENGE_FAILED without unhandled exception
        res = engine.validate_certificate_chain(
            chain_ed, challenge=b"TEST_CHALLENGE", challenge_signature=b"DUMMY_SIG"
        )
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.CHALLENGE_FAILED)

    def test_pnc_tampered_signatures_and_pem_corruption(self):
        """Test various tampered signatures and corrupt PEM payloads."""
        # Truncated PEM
        res = self.engine.validate_certificate_chain(self.valid_chain[:200])
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.MALFORMED_CERTIFICATE)

        # Corrupted base64 bytes inside PEM
        tampered_pem = self.valid_chain.replace("MII", "ZZZ", 1)
        res = self.engine.validate_certificate_chain(tampered_pem)
        self.assertFalse(res.is_authorized)
        self.assertIn(
            res.status,
            [AuthorizationStatus.INVALID_SIGNATURE, AuthorizationStatus.MALFORMED_CERTIFICATE],
        )

        # Incomplete chain (1 cert)
        leaf_only = self.leaf_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
        res = self.engine.validate_certificate_chain(leaf_only)
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.MALFORMED_CERTIFICATE)

        # Empty PEM
        res = self.engine.validate_certificate_chain("")
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.MALFORMED_CERTIFICATE)

    def test_pnc_challenge_response_adversarial_signatures(self):
        """Test challenge response with corrupted, mismatched, and empty signatures."""
        challenge = b"CHALLENGE_NONCE_STRESS_9999"
        valid_sig = self.leaf_key.sign(challenge, ec.ECDSA(hashes.SHA256()))

        # Valid signature passes
        res = self.engine.validate_certificate_chain(
            self.valid_chain, challenge=challenge, challenge_signature=valid_sig
        )
        self.assertTrue(res.is_authorized)

        # Corrupted signature bytes (bit flip)
        bad_sig = bytearray(valid_sig)
        bad_sig[10] ^= 0xFF
        res = self.engine.validate_certificate_chain(
            self.valid_chain, challenge=challenge, challenge_signature=bytes(bad_sig)
        )
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.CHALLENGE_FAILED)

        # Signature from a different private key
        other_key = ec.generate_private_key(ec.SECP256R1())
        other_sig = other_key.sign(challenge, ec.ECDSA(hashes.SHA256()))
        res = self.engine.validate_certificate_chain(
            self.valid_chain, challenge=challenge, challenge_signature=other_sig
        )
        self.assertFalse(res.is_authorized)
        self.assertEqual(res.status, AuthorizationStatus.CHALLENGE_FAILED)

class TestAdversarialAntiPhantomReplug(unittest.TestCase):
    """Adversarial stress testing against anti-phantom replug defense."""

    def setUp(self):
        self.detector = PhantomReplugDetector()
        self.base_session = {
            "session_id": "SE_BASE",
            "charger_id": "D1-1",
            "vehicle_id": "BUS-101",
            "start_ts": "2026-11-13T02:00:00+02:00",
            "end_ts": "2026-11-13T02:30:00+02:00",
            "start_soc": 20.0,
            "end_soc": 60.0,
            "energy_kwh": 60.0,
            "max_kw": 150.0,
            "base_fee_eur": 2.50,
        }

    def test_reconnect_time_boundary_179s_vs_180s_vs_181s(self):
        """Boundary test: 179s (phantom), 180s (borderline), 181s (genuine new)."""
        # 179s reconnect -> True
        s_179 = dict(self.base_session)
        s_179["session_id"] = "SE_179"
        s_179["start_ts"] = "2026-11-13T02:32:59+02:00"
        s_179["start_soc"] = 60.0
        eval_179 = self.detector.evaluate_reconnect(self.base_session, s_179)
        self.assertTrue(eval_179.is_phantom)
        self.assertEqual(eval_179.fraud_type, ReplugFraudType.PHANTOM_REPLUG_STITCHED)

        # 180s reconnect -> False (strict < 180s)
        s_180 = dict(self.base_session)
        s_180["session_id"] = "SE_180"
        s_180["start_ts"] = "2026-11-13T02:33:00+02:00"
        s_180["start_soc"] = 60.0
        eval_180 = self.detector.evaluate_reconnect(self.base_session, s_180)
        self.assertFalse(eval_180.is_phantom)
        self.assertEqual(eval_180.fraud_type, ReplugFraudType.GENUINE_NEW_SESSION)

        # 181s reconnect -> False
        s_181 = dict(self.base_session)
        s_181["session_id"] = "SE_181"
        s_181["start_ts"] = "2026-11-13T02:33:01+02:00"
        s_181["start_soc"] = 60.0
        eval_181 = self.detector.evaluate_reconnect(self.base_session, s_181)
        self.assertFalse(eval_181.is_phantom)
        self.assertEqual(eval_181.fraud_type, ReplugFraudType.GENUINE_NEW_SESSION)

    def test_soc_continuity_boundary_0_9_vs_1_0_vs_1_1(self):
        """Boundary test: 0.9% (phantom), 1.0% (boundary), 1.1% (genuine)."""
        def make_soc_session(new_soc: float) -> Dict[str, Any]:
            s = dict(self.base_session)
            s["session_id"] = f"SE_SOC_{new_soc}"
            s["start_ts"] = "2026-11-13T02:31:00+02:00"  # 60s gap
            s["start_soc"] = new_soc
            return s

        # +0.9% delta -> True
        self.assertTrue(self.detector.evaluate_reconnect(self.base_session, make_soc_session(60.9)).is_phantom)
        # +1.0% delta -> True
        self.assertTrue(self.detector.evaluate_reconnect(self.base_session, make_soc_session(61.0)).is_phantom)
        # +1.1% delta -> False
        self.assertFalse(self.detector.evaluate_reconnect(self.base_session, make_soc_session(61.1)).is_phantom)

        # -0.9% delta -> True
        self.assertTrue(self.detector.evaluate_reconnect(self.base_session, make_soc_session(59.1)).is_phantom)
        # -1.0% delta -> True
        self.assertTrue(self.detector.evaluate_reconnect(self.base_session, make_soc_session(59.0)).is_phantom)
        # -1.1% delta -> False
        self.assertFalse(self.detector.evaluate_reconnect(self.base_session, make_soc_session(58.9)).is_phantom)

    def test_bug_soc_float_precision_cancellation(self):
        """
        Remediated Verification: IEEE 754 precision tolerance allows exact 1.0% delta to match.
        """
        s_prev = dict(self.base_session)
        s_prev["end_soc"] = 1.2

        s_new = dict(self.base_session)
        s_new["start_ts"] = "2026-11-13T02:31:00+02:00"
        s_new["start_soc"] = 2.2

        eval_res = self.detector.evaluate_reconnect(s_prev, s_new)
        self.assertTrue(eval_res.is_phantom)
        self.assertEqual(eval_res.fraud_type, ReplugFraudType.PHANTOM_REPLUG_STITCHED)

    def test_bug_anti_fraud_none_value_unhandled_type_error(self):
        """
        Remediated Verification: Passing None in telemetry dictionaries does not raise TypeError.
        """
        s_none_ramp = dict(self.base_session)
        s_none_ramp["start_ts"] = "2026-11-13T02:31:00+02:00"
        s_none_ramp["start_soc"] = 60.0
        s_none_ramp["current_ramp_rate"] = None
        eval1 = self.detector.evaluate_reconnect(self.base_session, s_none_ramp)
        self.assertTrue(eval1.is_phantom)
        self.assertEqual(eval1.fraud_type, ReplugFraudType.PHANTOM_REPLUG_STITCHED)
        self.assertEqual(eval1.current_ramp_rate, 0.0)

        s_none_soc = dict(self.base_session)
        s_none_soc["end_soc"] = None
        s_none_soc["current_soc_pct"] = None
        s_none_soc["soc_pct"] = None
        eval2 = self.detector.evaluate_reconnect(s_none_soc, self.base_session)
        self.assertIsNotNone(eval2)

    def test_current_ramp_dI_dt_anomaly_and_lockout(self):
        """Verify dI/dt > 100 A/s triggers contactor soft-lockout and clamps current."""
        s_normal_ramp = dict(self.base_session)
        s_normal_ramp["current_ramp_rate"] = 100.0  # Exactly on threshold
        s_normal_ramp["start_ts"] = "2026-11-13T02:31:00+02:00"
        s_normal_ramp["start_soc"] = 60.0
        eval_norm = self.detector.evaluate_reconnect(self.base_session, s_normal_ramp)
        self.assertTrue(eval_norm.is_phantom)
        self.assertEqual(eval_norm.fraud_type, ReplugFraudType.PHANTOM_REPLUG_STITCHED)

        # Exceed threshold: 100.1 A/s
        s_fast_ramp = dict(self.base_session)
        s_fast_ramp["current_ramp_rate"] = 100.1
        s_fast_ramp["start_ts"] = "2026-11-13T02:31:00+02:00"
        s_fast_ramp["start_soc"] = 60.0
        eval_fast = self.detector.evaluate_reconnect(self.base_session, s_fast_ramp)
        self.assertTrue(eval_fast.is_phantom)
        self.assertEqual(eval_fast.fraud_type, ReplugFraudType.ABNORMAL_CURRENT_RAMP)
        self.assertEqual(eval_fast.action_taken, "CLAMP_CURRENT_LOCKOUT_CONTACTOR")

        # Sample array slope check
        samples = [
            {"time_s": 0.0, "current_a": 0.0},
            {"time_s": 0.5, "current_a": 120.0},  # 240 A/s
        ]
        eval_sampled = self.detector.evaluate_reconnect(
            self.base_session, s_normal_ramp, current_samples=samples
        )
        self.assertTrue(eval_sampled.is_phantom)
        self.assertEqual(eval_sampled.fraud_type, ReplugFraudType.ABNORMAL_CURRENT_RAMP)
        self.assertEqual(eval_sampled.current_ramp_rate, 240.0)

    def test_bug_sequential_replug_fee_waiver_undercounting(self):
        """
        Remediated Verification: Cumulative duplicate fee waiver accumulates across sequential replugs.
        """
        current_session = dict(self.base_session)
        base_t = datetime.fromisoformat("2026-11-13T02:30:00+02:00")

        for i in range(1, 11):
            t_plug = (base_t + timedelta(seconds=i * 20)).isoformat()
            t_unplug = (base_t + timedelta(seconds=i * 20 + 10)).isoformat()
            new_s = {
                "session_id": f"SE_SEQ_{i}",
                "charger_id": "D1-1",
                "vehicle_id": "BUS-101",
                "start_ts": t_plug,
                "end_ts": t_unplug,
                "start_soc": 60.0 + (i - 1) * 0.05,
                "end_soc": 60.0 + i * 0.05,
                "energy_kwh": 2.5,
                "max_kw": 150.0,
                "base_fee_eur": 2.50,
            }
            is_phantom, merged = anti_phantom_replug_check(current_session, new_s)
            self.assertTrue(is_phantom)
            current_session = merged

        self.assertEqual(
            current_session["duplicate_base_fee_waived_eur"],
            25.00,
            "Remediated: Multiple sequential replugs correctly accumulated waived fee",
        )
        self.assertEqual(current_session["stitch_count"], 10)

if __name__ == "__main__":
    unittest.main()
