"""
Empirical Adversarial Verification Suite - M2 Challenger 3
Deep-dive empirical stress-testing for the 11 remediated vulnerabilities.
"""

import os
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone, timedelta
import pytest
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, rsa, ed25519
from cryptography.x509.oid import NameOID

from src.core.protocols import (
    Iso15118PnCEngine,
    CertificateAuthorityManager,
    AuthorizationStatus,
)
from src.core.anti_fraud import (
    PhantomReplugDetector,
    ReplugFraudType,
    AntiFraudConfig,
    _safe_float,
)
from src.core.dpr_matrix import DPRMatrix, PowerModule, MODULE_POWER_KW
from src.core.self_healing import NordicColdProtectionEngine, OfflineWALManager


# =========================================================================
# 1. Non-ECDSA Keys in GenChallenge
# =========================================================================
def test_empirical_non_ecdsa_and_rsa_genchallenge():
    """Verify that Ed25519 and RSA keys in leaf certs produce clean CHALLENGE_FAILED without unhandled crash."""
    ca_mgr = CertificateAuthorityManager()
    engine = Iso15118PnCEngine(ca_mgr)
    now = datetime.now(timezone.utc)

    # Root CA
    root_key = ec.generate_private_key(ec.SECP256R1())
    root_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Test Root CA")])
    root_cert = (
        x509.CertificateBuilder()
        .subject_name(root_name)
        .issuer_name(root_name)
        .public_key(root_key.public_key())
        .serial_number(1)
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=10))
        .sign(root_key, hashes.SHA256())
    )
    ca_mgr.add_trusted_root(root_cert)

    # A. Ed25519 key leaf cert
    ed_key = ed25519.Ed25519PrivateKey.generate()
    ed_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "EMAID:US-ED25519-12345")])
    ed_cert = (
        x509.CertificateBuilder()
        .subject_name(ed_name)
        .issuer_name(root_name)
        .public_key(ed_key.public_key())
        .serial_number(1001)
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=10))
        .sign(root_key, hashes.SHA256())
    )

    chain_ed_pem = (
        ed_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
        + root_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    )

    challenge = b"CHALLENGE_NONCE_32_BYTES_RANDOM"
    ed_sig = ed_key.sign(challenge)

    res_ed = engine.validate_certificate_chain(
        chain_ed_pem,
        challenge=challenge,
        challenge_signature=ed_sig,
    )
    assert res_ed.status == AuthorizationStatus.CHALLENGE_FAILED
    assert not res_ed.is_authorized
    assert "Vehicle failed GenChallenge cryptographic check" in res_ed.error_message

    # B. RSA key leaf cert
    rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    rsa_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "EMAID:US-RSA-12345")])
    rsa_cert = (
        x509.CertificateBuilder()
        .subject_name(rsa_name)
        .issuer_name(root_name)
        .public_key(rsa_key.public_key())
        .serial_number(1002)
        .not_valid_before(now - timedelta(days=1))
        .not_valid_after(now + timedelta(days=10))
        .sign(root_key, hashes.SHA256())
    )
    from cryptography.hazmat.primitives.asymmetric import padding
    rsa_sig = rsa_key.sign(challenge, padding.PKCS1v15(), hashes.SHA256())

    chain_rsa_pem = (
        rsa_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
        + root_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    )

    res_rsa = engine.validate_certificate_chain(
        chain_rsa_pem,
        challenge=challenge,
        challenge_signature=rsa_sig,
    )
    assert res_rsa.status == AuthorizationStatus.CHALLENGE_FAILED
    assert not res_rsa.is_authorized
    assert "Vehicle failed GenChallenge cryptographic check" in res_rsa.error_message


# =========================================================================
# 2. Revoked Sub-CA in 3-Tier Certificate Chain
# =========================================================================
def test_empirical_revoked_sub_ca_rejection():
    """Verify that an intermediate Sub-CA present on the CRL triggers CERTIFICATE_REVOKED."""
    ca_mgr = CertificateAuthorityManager()
    engine = Iso15118PnCEngine(ca_mgr)
    now = datetime.now(timezone.utc)

    # Build 3-tier: Root -> Sub-CA -> Leaf
    root_key = ec.generate_private_key(ec.SECP256R1())
    root_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Kempower Root CA G1")])
    root_cert = (
        x509.CertificateBuilder()
        .subject_name(root_name)
        .issuer_name(root_name)
        .public_key(root_key.public_key())
        .serial_number(9001)
        .not_valid_before(now - timedelta(days=10))
        .not_valid_after(now + timedelta(days=365))
        .sign(root_key, hashes.SHA256())
    )

    sub_key = ec.generate_private_key(ec.SECP256R1())
    sub_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Kempower Sub CA G1")])
    sub_cert = (
        x509.CertificateBuilder()
        .subject_name(sub_name)
        .issuer_name(root_name)
        .public_key(sub_key.public_key())
        .serial_number(9002)
        .not_valid_before(now - timedelta(days=10))
        .not_valid_after(now + timedelta(days=365))
        .sign(root_key, hashes.SHA256())
    )

    leaf_key = ec.generate_private_key(ec.SECP256R1())
    leaf_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "EMAID:FI-KEM-123456789")])
    leaf_cert = (
        x509.CertificateBuilder()
        .subject_name(leaf_name)
        .issuer_name(sub_name)
        .public_key(leaf_key.public_key())
        .serial_number(9003)
        .not_valid_before(now - timedelta(days=10))
        .not_valid_after(now + timedelta(days=365))
        .sign(sub_key, hashes.SHA256())
    )

    ca_mgr.add_trusted_root(root_cert)

    pem_chain = (
        leaf_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
        + sub_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
        + root_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    )

    # 1. Non-revoked passes
    res_valid = engine.validate_certificate_chain(pem_chain)
    assert res_valid.status == AuthorizationStatus.ACCEPTED
    assert res_valid.is_authorized

    # 2. Revoke intermediate Sub-CA serial 9002
    ca_mgr.revoke_serial(9002)
    res_revoked = engine.validate_certificate_chain(pem_chain)
    assert res_revoked.status == AuthorizationStatus.CERTIFICATE_REVOKED
    assert not res_revoked.is_authorized
    assert "CRL blacklist" in res_revoked.error_message


# =========================================================================
# 3. 2-Tier Cert Chain Untrusted Root Rejection
# =========================================================================
def test_empirical_2_tier_untrusted_root_rejection():
    """Verify that 2-tier chain [leaf, root] strictly enforces root CA trust anchor."""
    ca_mgr = CertificateAuthorityManager()
    engine = Iso15118PnCEngine(ca_mgr)
    now = datetime.now(timezone.utc)

    root_key = ec.generate_private_key(ec.SECP256R1())
    root_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Untrusted Rogue Root CA")])
    root_cert = (
        x509.CertificateBuilder()
        .subject_name(root_name)
        .issuer_name(root_name)
        .public_key(root_key.public_key())
        .serial_number(8001)
        .not_valid_before(now - timedelta(days=10))
        .not_valid_after(now + timedelta(days=365))
        .sign(root_key, hashes.SHA256())
    )

    leaf_key = ec.generate_private_key(ec.SECP256R1())
    leaf_name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "EMAID:RO-GUE-999999999")])
    leaf_cert = (
        x509.CertificateBuilder()
        .subject_name(leaf_name)
        .issuer_name(root_name)
        .public_key(leaf_key.public_key())
        .serial_number(8002)
        .not_valid_before(now - timedelta(days=10))
        .not_valid_after(now + timedelta(days=365))
        .sign(root_key, hashes.SHA256())
    )

    pem_chain = (
        leaf_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
        + root_cert.public_bytes(serialization.Encoding.PEM).decode("utf-8")
    )

    # Trust an unrelated root
    dummy_root = (
        x509.CertificateBuilder()
        .subject_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Legitimate Trusted Root")]))
        .issuer_name(x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "Legitimate Trusted Root")]))
        .public_key(root_key.public_key())
        .serial_number(9999)
        .not_valid_before(now - timedelta(days=10))
        .not_valid_after(now + timedelta(days=365))
        .sign(root_key, hashes.SHA256())
    )
    ca_mgr.add_trusted_root(dummy_root)

    # Untrusted root should be rejected with UNKNOWN_ROOT_CA
    res_untrusted = engine.validate_certificate_chain(pem_chain)
    assert res_untrusted.status == AuthorizationStatus.UNKNOWN_ROOT_CA
    assert not res_untrusted.is_authorized
    assert "not in trusted anchor store" in res_untrusted.error_message

    # Trust the rogue root and verify it passes
    ca_mgr.add_trusted_root(root_cert)
    res_trusted = engine.validate_certificate_chain(pem_chain)
    assert res_trusted.status == AuthorizationStatus.ACCEPTED
    assert res_trusted.is_authorized


# =========================================================================
# 4. None Value Payloads in Anti-Fraud Detection
# =========================================================================
def test_empirical_anti_fraud_none_payloads():
    """Verify that completely None / missing telemetry values in sessions do not crash."""
    detector = PhantomReplugDetector()

    prev_sess = {
        "session_id": "PREV_NULL",
        "vehicle_id": "V_NULL",
        "charger_id": "C_NULL",
        "end_ts": "2026-11-05T20:00:00Z",
        "end_soc": None,
        "current_soc_pct": None,
        "soc_pct": None,
        "energy_kwh": None,
        "max_kw": None,
        "current_ramp_rate": None,
    }
    new_sess = {
        "session_id": "NEW_NULL",
        "vehicle_id": "V_NULL",
        "charger_id": "C_NULL",
        "start_ts": "2026-11-05T20:01:00Z",
        "start_soc": None,
        "current_soc_pct": None,
        "soc_pct": None,
        "energy_kwh": None,
        "max_kw": None,
        "current_ramp_rate": None,
    }
    null_samples = [
        {"current_a": None, "time_s": None},
        {"current_a": None, "time_s": None},
    ]

    eval_res = detector.evaluate_reconnect(prev_sess, new_sess, current_samples=null_samples)
    assert eval_res.is_phantom is True  # delta_t=60s, delta_soc=0.0 -> phantom replug
    assert eval_res.delta_soc_pct == 0.0

    stitched = detector.stitch_sessions(prev_sess, new_sess, eval_res)
    assert stitched["session_id"] == "PREV_NULL"
    assert stitched["energy_kwh"] == 0.0
    assert stitched["max_kw"] == 0.0
    assert stitched["duplicate_base_fee_waived_eur"] == 2.50


# =========================================================================
# 5. Exact 1.0% SoC Delta and IEEE 754 Float Continuity
# =========================================================================
def test_empirical_exact_1_0_pct_soc_delta():
    """Verify exact 1.0% SoC delta (e.g. 2.2 - 1.2 = 1.0000000000000002) is stitched."""
    detector = PhantomReplugDetector()

    # Float cancellation artifact test: 2.2 - 1.2 in Python:
    assert (2.2 - 1.2) > 1.0  # 1.0000000000000002

    prev_sess = {
        "session_id": "S1",
        "vehicle_id": "V1",
        "charger_id": "C1",
        "end_ts": "2026-11-05T20:00:00Z",
        "end_soc": 1.2,
    }
    new_sess = {
        "session_id": "S2",
        "vehicle_id": "V1",
        "charger_id": "C1",
        "start_ts": "2026-11-05T20:01:00Z",
        "start_soc": 2.2,
    }

    eval_res = detector.evaluate_reconnect(prev_sess, new_sess)
    assert eval_res.is_phantom is True
    assert eval_res.fraud_type == ReplugFraudType.PHANTOM_REPLUG_STITCHED

    # Also test boundary just outside threshold (1.0002% delta)
    new_sess_outside = dict(new_sess, start_soc=2.2002)
    eval_outside = detector.evaluate_reconnect(prev_sess, new_sess_outside)
    assert eval_outside.is_phantom is False
    assert eval_outside.fraud_type == ReplugFraudType.GENUINE_NEW_SESSION


# =========================================================================
# 6. Cumulative Fee Waivers Across 10 Sequential Stitches
# =========================================================================
def test_empirical_cumulative_fee_waiver_10_stitches():
    """Verify sequential stitching of 10 rapid disconnections accumulates to exactly €25.00."""
    detector = PhantomReplugDetector()

    current_merged = {
        "session_id": "S_ROOT",
        "vehicle_id": "V_FLEET_01",
        "charger_id": "C1",
        "start_ts": "2026-11-05T10:00:00Z",
        "end_ts": "2026-11-05T10:05:00Z",
        "start_soc": 10.0,
        "end_soc": 12.0,
        "energy_kwh": 5.0,
        "max_kw": 100.0,
    }

    for i in range(1, 11):
        next_sess = {
            "session_id": f"S_CHILD_{i}",
            "vehicle_id": "V_FLEET_01",
            "charger_id": "C1",
            "start_ts": f"2026-11-05T10:0{i:02d}:00Z",
            "end_ts": f"2026-11-05T10:0{i:02d}:30Z",
            "start_soc": 12.0 + (i * 0.05),
            "end_soc": 12.0 + (i * 0.05) + 0.1,
            "energy_kwh": 2.0,
            "max_kw": 120.0,
        }
        ev = detector.evaluate_reconnect(current_merged, next_sess)
        current_merged = detector.stitch_sessions(current_merged, next_sess, ev)

    assert current_merged["stitch_count"] == 10
    assert len(current_merged["child_session_ids"]) == 10
    assert current_merged["duplicate_base_fee_waived_eur"] == 25.00
    assert current_merged["energy_kwh"] == 25.0  # 5 + 10*2


# =========================================================================
# 7. Dead Cabinet Power Derating (0 kW) and Degraded Modules
# =========================================================================
def test_empirical_dead_cabinet_and_degraded_modules_derate():
    """Verify that DPR caps power based on healthy modules (250 kW for 5 failed, 0 kW for all 15 failed)."""
    dpr = DPRMatrix("S1")
    req = {"D1-1": 150.0, "D1-2": 150.0, "D1-3": 100.0}

    # Nominal healthy cabinet: 15 modules * 25kW = 375kW, capped to cab max_kw = 360 kW
    alloc_nominal = dpr.allocate_intra_cabinet_continuous("C1-1", req)
    assert sum(alloc_nominal.values()) == 360.0

    # 1. Fail 5 modules in Cabinet C1-1
    c1_mods = [m for m in dpr.modules.values() if m.cabinet_id == "C1-1"]
    for m in c1_mods[:5]:
        m.is_healthy = False

    alloc_degraded = dpr.allocate_intra_cabinet_continuous("C1-1", req)
    # 10 healthy modules * 25 kW = 250 kW
    assert sum(alloc_degraded.values()) == 250.0

    # 2. Fail all 15 modules in Cabinet C1-1
    for m in c1_mods:
        m.is_healthy = False

    alloc_dead = dpr.allocate_intra_cabinet_continuous("C1-1", req)
    assert sum(alloc_dead.values()) == 0.0


# =========================================================================
# 8. Contactor BBM Re-Routing Strict from_gun Routing
# =========================================================================
def test_empirical_contactor_strict_from_gun_routing():
    """Verify re_route_contactor transfers modules ONLY from the specified from_gun, not unassigned."""
    dpr = DPRMatrix("S1")
    # Reset all module assignments
    for m in dpr.modules.values():
        m.assigned_gun = None

    all_mods = list(dpr.modules.values())
    # Assign 5 modules to GUN_A, 5 to GUN_B, leave remaining unassigned
    for m in all_mods[0:5]:
        m.assigned_gun = "GUN_A"
    for m in all_mods[5:10]:
        m.assigned_gun = "GUN_B"

    # Route 2 modules specifically from GUN_A to GUN_TARGET
    seq = dpr.re_route_contactor(from_gun="GUN_A", to_gun="GUN_TARGET", modules=2, initial_current_amps=100.0)
    assert seq.is_zero_arc_compliant is True
    assert seq.transferred_modules == 2
    assert seq.from_gun == "GUN_A"
    assert seq.to_gun == "GUN_TARGET"

    # Count gun assignments
    gun_a_count = sum(1 for m in dpr.modules.values() if m.assigned_gun == "GUN_A")
    gun_b_count = sum(1 for m in dpr.modules.values() if m.assigned_gun == "GUN_B")
    gun_target_count = sum(1 for m in dpr.modules.values() if m.assigned_gun == "GUN_TARGET")
    unassigned_count = sum(1 for m in dpr.modules.values() if m.assigned_gun is None)

    assert gun_a_count == 3  # 5 - 2
    assert gun_b_count == 5  # Untouched
    assert gun_target_count == 2
    assert unassigned_count == (len(all_mods) - 10)  # Untouched! Unassigned was not stolen!


# =========================================================================
# 9. Nordic Cold Protection Negative Net Heating at -40°C
# =========================================================================
def test_empirical_nordic_negative_net_heating_returns_none():
    """Verify that at -40°C when net heating <= 0.05 kW (defective PTC/power starvation), est_heating_minutes is None."""
    # Defective PTC or power starvation (0 kW available)
    # batt_temp = 10.0°C, ambient = -40.0°C:
    # heat loss = 0.04 * (10 - (-40)) = 2.0 kW.
    # net_heating = 0.0 + 1.2 - 2.0 = -0.8 kW <= 0.05 kW -> Battery is cooling!
    res_stall = NordicColdProtectionEngine.evaluate_preheating_diversion(
        batt_temp_c=10.0,
        batt_capacity_kwh=75.0,
        ambient_temp_c=-40.0,
        available_dpr_kw=0.0,
    )
    assert res_stall["is_preheating_active"] is True
    assert res_stall["est_heating_minutes"] is None  # Correctly identifies thermal stalling/cooling!

    # Working PTC at -40°C
    res_working = NordicColdProtectionEngine.evaluate_preheating_diversion(
        batt_temp_c=-40.0,
        batt_capacity_kwh=75.0,
        ambient_temp_c=-40.0,
        available_dpr_kw=200.0,
    )
    assert res_working["is_preheating_active"] is True
    assert res_working["est_heating_minutes"] is not None
    assert res_working["est_heating_minutes"] > 0.0


# =========================================================================
# 10. WAL Duplicate Replay on CONFIRMED Transactions
# =========================================================================
def test_empirical_wal_duplicate_replay_preserves_confirmed():
    """Verify that replaying a transaction that is already CONFIRMED does NOT reset it to PENDING."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        wal = OfflineWALManager(db_path)
        tx_uuid = "TX_CONFIRMED_TEST_12345"
        tx_data = {
            "transaction_uuid": tx_uuid,
            "session_id": "S_CONF_1",
            "total_energy_kwh": 42.5,
        }

        # 1. Initial insert -> PENDING
        wal.record_offline_transaction(tx_data)
        assert wal.get_transaction_by_uuid(tx_uuid)["sync_status"] == "PENDING"

        # 2. Reconcile ACK -> CONFIRMED
        ack_count = wal.reconcile_reconnection_ack([tx_uuid])
        assert ack_count == 1
        assert wal.get_transaction_by_uuid(tx_uuid)["sync_status"] == "CONFIRMED"

        # 3. Duplicate replay of same transaction -> Must remain CONFIRMED
        wal.record_offline_transaction(tx_data)
        assert wal.get_transaction_by_uuid(tx_uuid)["sync_status"] == "CONFIRMED"
        assert wal.count_transactions(status="PENDING") == 0
        assert wal.count_transactions(status="CONFIRMED") == 1
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)


# =========================================================================
# 11. 40,000 UUID Batch ACK in SQLite WAL (No Variable Overflow)
# =========================================================================
def test_empirical_40000_uuid_batch_ack():
    """Verify that reconciling 40,000 UUIDs in WAL chunks queries without sqlite3 variable limit overflow."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name

    try:
        wal = OfflineWALManager(db_path)
        batch_size = 40000
        uuids = [f"UUID_{i:06d}" for i in range(batch_size)]

        # Fast direct batch insert for setup matching table schema
        with wal._get_connection() as conn:
            conn.executemany(
                """
                INSERT INTO offline_transactions (
                    transaction_uuid, session_id, site_id, charger_id, vehicle_id,
                    start_ts, stop_ts, start_meter_wh, stop_meter_wh,
                    total_energy_kwh, peak_power_kw, merkle_hash, sync_status
                ) VALUES (?, 'BATCH_SESS', 'SITE_S1', 'D1-1', 'VEH_01', '2026-11-05T00:00:00Z', '2026-11-05T01:00:00Z', 0, 1000, 1.0, 50.0, 'DUMMY_HASH', 'PENDING')
                """,
                [(u,) for u in uuids],
            )
            conn.commit()

        assert wal.count_transactions(status="PENDING") == batch_size
        assert wal.count_transactions(status="CONFIRMED") == 0

        # Execute 40,000 UUID reconciliation
        t0 = time.perf_counter()
        updated = wal.reconcile_reconnection_ack(uuids)
        elapsed = time.perf_counter() - t0

        assert updated == batch_size
        assert wal.count_transactions(status="PENDING") == 0
        assert wal.count_transactions(status="CONFIRMED") == batch_size
        # Must execute swiftly (< 5.0 seconds for 40k batch)
        assert elapsed < 5.0
    finally:
        if os.path.exists(db_path):
            os.remove(db_path)
