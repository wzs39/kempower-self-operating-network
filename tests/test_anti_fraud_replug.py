"""
Unit & Integration Test Suite for Anti-Phantom Replug & Fraud Defense Subsystem
Test File: tests/test_anti_fraud_replug.py

Verifies:
- F10: Three-pillar criteria (Delta t < 180s, |Delta SoC| <= 1.0%, dI/dt > 100 A/s)
- Automated session stitching and energy accumulation
- Duplicate base connection fee waiver (€2.50)
- Legitimate new vehicle arrival classification
- Electrical current ramp rate anomaly protection
"""

import unittest
from src.core.anti_fraud import (
    PhantomReplugDetector,
    ReplugFraudType,
    AntiFraudConfig,
    ReplugEvaluation,
    anti_phantom_replug_check,
)

class TestAntiPhantomReplug(unittest.TestCase):
    """F10: Anti-Phantom Replug & Electrical Fingerprinting Tests."""

    def setUp(self):
        self.prev_session = {
            "session_id": "SE0001",
            "charger_id": "D1-1",
            "vehicle_id": "B01",
            "start_ts": "2026-11-13T01:00:00+02:00",
            "end_ts": "2026-11-13T01:30:00+02:00",
            "start_soc": 20.0,
            "end_soc": 55.0,
            "energy_kwh": 80.0,
            "max_kw": 150.0,
            "base_fee_eur": 2.50,
        }
        # Reconnected 45 seconds later, same vehicle, SoC changed by only 0.2%
        self.new_session_phantom = {
            "session_id": "SE0002",
            "charger_id": "D1-1",
            "vehicle_id": "B01",
            "start_ts": "2026-11-13T01:30:45+02:00",
            "end_ts": "2026-11-13T02:15:00+02:00",
            "start_soc": 55.2,
            "end_soc": 85.0,
            "energy_kwh": 65.0,
            "max_kw": 140.0,
            "base_fee_eur": 2.50,
        }

    def test_phantom_replug_stitching(self):
        """Verify rapid reconnect (<180s) and continuous SoC (<=1.0%) triggers stitching."""
        is_phantom, merged = anti_phantom_replug_check(
            self.prev_session, self.new_session_phantom
        )

        self.assertTrue(is_phantom)
        self.assertEqual(merged["session_id"], "SE0001")  # Preserves root ID
        self.assertEqual(merged["start_ts"], "2026-11-13T01:00:00+02:00")  # Preserves arrival
        self.assertEqual(merged["end_ts"], "2026-11-13T02:15:00+02:00")
        self.assertEqual(merged["energy_kwh"], 145.0)  # 80.0 + 65.0
        self.assertEqual(merged["duplicate_base_fee_waived_eur"], 2.50)
        self.assertEqual(merged["reconnect_delta_sec"], 45.0)
        self.assertTrue(merged["stitched"])
        self.assertEqual(merged["fraud_type"], "PHANTOM_REPLUG_STITCHED")

    def test_genuine_new_vehicle_arrival(self):
        """Verify new vehicle arriving with different SoC is classified as genuine new session."""
        new_car = {
            "session_id": "SE0003",
            "charger_id": "D1-1",
            "vehicle_id": "B02",
            "start_ts": "2026-11-13T01:31:00+02:00",
            "end_ts": "2026-11-13T02:30:00+02:00",
            "start_soc": 15.0,  # 15% vs 55% end_soc -> delta 40% >> 1%
            "end_soc": 80.0,
            "energy_kwh": 120.0,
            "max_kw": 150.0,
        }
        is_phantom, result = anti_phantom_replug_check(self.prev_session, new_car)
        self.assertFalse(is_phantom)
        self.assertEqual(result["session_id"], "SE0003")
        self.assertFalse(result.get("stitched", False))

    def test_delayed_reconnect_exceeding_threshold(self):
        """Verify reconnect after 250s (> 180s threshold) is treated as separate session."""
        delayed_session = dict(self.new_session_phantom)
        delayed_session["start_ts"] = "2026-11-13T01:34:10+02:00"  # 250s gap
        is_phantom, result = anti_phantom_replug_check(self.prev_session, delayed_session)
        self.assertFalse(is_phantom)
        self.assertEqual(result["session_id"], "SE0002")

    def test_abnormal_current_ramp_fraud_detection(self):
        """Verify dI/dt > 100 A/s triggers abnormal current ramp defense and contactor lockout."""
        detector = PhantomReplugDetector()
        # 0A to 250A in 1.0s -> 250 A/s (> 100 A/s threshold)
        samples = [
            {"time_s": 0.0, "current_a": 0.0},
            {"time_s": 1.0, "current_a": 250.0},
        ]
        eval_res = detector.evaluate_reconnect(
            self.prev_session, self.new_session_phantom, current_samples=samples
        )

        self.assertTrue(eval_res.is_phantom)
        self.assertEqual(eval_res.fraud_type, ReplugFraudType.ABNORMAL_CURRENT_RAMP)
        self.assertEqual(eval_res.current_ramp_rate, 250.0)
        self.assertEqual(eval_res.action_taken, "CLAMP_CURRENT_LOCKOUT_CONTACTOR")

    def test_anti_fraud_config_customization(self):
        """Verify AntiFraudConfig parameters can be calibrated."""
        custom_cfg = AntiFraudConfig(
            reconnect_time_threshold_sec=60.0,  # Stricter 1 min
            soc_continuity_threshold_pct=0.5,
            abnormal_ramp_threshold_a_per_sec=50.0,
            base_connection_fee_eur=5.00,
        )
        detector = PhantomReplugDetector(custom_cfg)
        # 75s reconnect exceeds 60s threshold
        session_75s = dict(self.new_session_phantom)
        session_75s["start_ts"] = "2026-11-13T01:31:15+02:00"
        eval_res = detector.evaluate_reconnect(self.prev_session, session_75s)
        self.assertFalse(eval_res.is_phantom)

if __name__ == "__main__":
    unittest.main()
