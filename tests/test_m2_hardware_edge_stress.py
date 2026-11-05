"""
Empirical Adversarial Stress Test Suite for DPR Module Isolation, Nordic Cold & 72h WAL Durability
Test File: tests/test_m2_hardware_edge_stress.py

Auditor: M2 Challenger 2 (critic / specialist)
Focus:
1. Stress test DPR 25 kW module isolation:
   - Multiple simultaneous module failures in a single cabinet (5 modules fail at once).
   - Total module exhaustion in a cabinet (15 modules fail).
   - Module restoration under load and contactor re-routing anomaly.
   - Wear-leveling duty rotation with extreme run-hour differences (0 hours vs 50,000 hours).
2. Stress test Nordic sub-zero dynamic diversion:
   - Arctic extreme temperature (-40°C, -20°C, 0°C, 35°C).
   - Zero-heating and defective PTC resistance scenarios.
   - Negative heat drift thermal prediction masking under extreme frost.
3. Stress test 72h WAL durability:
   - 10,000 offline transaction commits in SQLite WAL.
   - Out-of-order reconciliation and Merkle root invariance.
   - Duplicate UUID replays and idempotency demotion flaw.
   - Single-bit tamper detection in 10,000 transactions.
   - Large batch ACK SQL variable overflow (40,000 UUIDs).
"""

import hashlib
import random
import sqlite3
import sys
import unittest
from pathlib import Path
from typing import Dict, List

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.dpr_matrix import DPRMatrix, PowerModule, MODULE_POWER_KW
from src.core.self_healing import NordicColdProtectionEngine, OfflineWALManager


class TestDPRModuleIsolationStress(unittest.TestCase):
    """Adversarial stress testing of DPR 25 kW modular self-healing and contactor routing."""

    def setUp(self):
        self.dpr = DPRMatrix("S1")  # S1 has C1-1 (15 mods), C1-2 (15 mods), C1-3 (13 mods)

    def test_five_simultaneous_module_failures_in_single_cabinet(self):
        """
        Adversarial Scenario: 5 power modules fail simultaneously in cabinet C1-1.
        Evaluates remaining capacity, isolation duration, and allocation behavior.
        """
        c1_1_mods = [m.module_id for m in self.dpr.modules.values() if m.cabinet_id == "C1-1"]
        self.assertEqual(len(c1_1_mods), 15)

        # Isolate 5 modules concurrently
        isolated_ids = c1_1_mods[:5]
        for mod_id in isolated_ids:
            success, dur_ms, diag = self.dpr.isolate_module(mod_id, reason="CRITICAL_IGBT_OVERTEMP")
            self.assertTrue(success)
            self.assertEqual(dur_ms, 85.0)
            self.assertFalse(self.dpr.modules[mod_id].is_healthy)
            self.assertEqual(self.dpr.modules[mod_id].status, "ISOLATED_TEMP")

        # Check remaining healthy count in cabinet C1-1
        remaining_healthy = [m for m in self.dpr.modules.values() if m.cabinet_id == "C1-1" and m.is_healthy]
        self.assertEqual(len(remaining_healthy), 10)
        healthy_capacity_kw = len(remaining_healthy) * MODULE_POWER_KW
        self.assertEqual(healthy_capacity_kw, 250.0)

        # Remediated Verification:
        # allocate_intra_cabinet_continuous automatically derates to healthy physical module capacity
        reqs = {"D1-1": 100.0, "D1-2": 100.0, "D1-3": 100.0, "D1-4": 100.0}
        alloc = self.dpr.allocate_intra_cabinet_continuous("C1-1", reqs)
        total_allocated = sum(alloc.values())

        # Physical limit enforced: exactly 250 kW allocated across healthy hardware
        self.assertLessEqual(total_allocated, healthy_capacity_kw)
        self.assertEqual(total_allocated, 250.0)

    def test_total_cabinet_module_exhaustion(self):
        """
        Adversarial Scenario: All 15 modules in C1-1 fail.
        Remaining healthy hardware in C1-1 drops to 0 kW.
        """
        c1_1_mods = [m.module_id for m in self.dpr.modules.values() if m.cabinet_id == "C1-1"]
        for mod_id in c1_1_mods:
            self.dpr.isolate_module(mod_id, reason="TOTAL_COOLING_PUMP_FAILURE")

        remaining = [m for m in self.dpr.modules.values() if m.cabinet_id == "C1-1" and m.is_healthy]
        self.assertEqual(len(remaining), 0)

        # Remediated: Dead cabinet with 0 healthy modules allocates 0 kW even without explicit deratings
        reqs = {"D1-1": 150.0, "D1-2": 150.0}
        alloc = self.dpr.allocate_intra_cabinet_continuous("C1-1", reqs)
        self.assertEqual(sum(alloc.values()), 0.0)

        # Explicit parameter continues to curtail safely to 0
        safe_alloc = self.dpr.allocate_intra_cabinet_continuous("C1-1", reqs, cabinet_deratings={"C1-1": 0.0})
        self.assertEqual(sum(safe_alloc.values()), 0.0)

    def test_module_restoration_under_load_and_reroute_contactor(self):
        """
        Adversarial Scenario: An isolated module cools down and is restored while dispensers are active.
        Tests restore_module() and verifies strict from_gun matching in re_route_contactor.
        """
        mod_id = "S1_M01"
        self.dpr.isolate_module(mod_id, reason="TEMP")
        self.assertFalse(self.dpr.modules[mod_id].is_healthy)

        # Restore module
        restored = self.dpr.restore_module(mod_id)
        self.assertTrue(restored)
        self.assertTrue(self.dpr.modules[mod_id].is_healthy)
        self.assertIsNone(self.dpr.modules[mod_id].assigned_gun)

        # Setup scenario: S1_M01 is idle (assigned_gun=None). S1_M02 is assigned to D1-1.
        self.dpr.modules["S1_M01"].assigned_gun = None
        self.dpr.modules["S1_M02"].assigned_gun = "D1-1"

        # Reroute request specifically asks to transfer 1 module from D1-1 to D1-2
        seq = self.dpr.re_route_contactor(from_gun="D1-1", to_gun="D1-2", modules=1)
        self.assertTrue(seq.is_zero_arc_compliant)

        # Remediated: S1_M02 assigned to D1-1 is transferred to D1-2. S1_M01 remains idle.
        self.assertIsNone(self.dpr.modules["S1_M01"].assigned_gun)
        self.assertEqual(self.dpr.modules["S1_M02"].assigned_gun, "D1-2")

    def test_wear_leveling_extreme_run_hour_differences(self):
        """
        Adversarial Scenario: 0 hours (brand new module) vs 50,000 hours (end-of-life)
        under severe thermal excess (65°C vs 20°C).
        """
        cab_id = "C1-1"
        cab_mods = [m for m in self.dpr.modules.values() if m.cabinet_id == cab_id]

        # 5 worn modules (50,000h, 65°C, 10,000 cycles)
        for m in cab_mods[:5]:
            m.operating_hours = 50000.0
            m.temperature_c = 65.0
            m.start_stop_cycles = 10000

        # 10 pristine modules (0h, 20°C, 0 cycles)
        for m in cab_mods[5:]:
            m.operating_hours = 0.0
            m.temperature_c = 20.0
            m.start_stop_cycles = 0

        # Request 5 modules for duty rotation
        selected = self.dpr.rotate_modules_wear_leveling(cab_id, required_modules=5, ambient_temp_c=20.0)

        # Must strictly select the pristine modules (M06-M10)
        expected = [m.module_id for m in cab_mods[5:10]]
        self.assertEqual(selected, expected)

        # Verify wear indices
        worn_index = cab_mods[0].calculate_wear_index(ambient_temp_c=20.0)
        pristine_index = cab_mods[5].calculate_wear_index(ambient_temp_c=20.0)
        self.assertAlmostEqual(pristine_index, 0.0)
        self.assertGreater(worn_index, 50000.0)

        # Verify rotation needed trigger with extreme delta
        cab_mods[0].assigned_gun = "D1-1"
        cab_mods[5].assigned_gun = None
        needed, delta_h, worn_id, fresh_id = self.dpr.check_wear_leveling_rotation_needed(cab_id, threshold_hours=2.0)
        self.assertTrue(needed)
        self.assertAlmostEqual(delta_h, 50000.0)
        self.assertEqual(worn_id, cab_mods[0].module_id)
        self.assertEqual(fresh_id, cab_mods[5].module_id)

    def test_wear_leveling_oversubscription(self):
        """Adversarial Scenario: Requesting more modules than exist in cabinet."""
        selected = self.dpr.rotate_modules_wear_leveling("C1-1", required_modules=999)
        self.assertEqual(len(selected), 15)  # Clamped gracefully to max available


class TestNordicColdProtectionStress(unittest.TestCase):
    """Adversarial stress testing of Nordic low-temperature dynamic diversion."""

    def test_arctic_extreme_temperature_envelope(self):
        """
        Adversarial Scenario: Sweep temperatures across [-40°C, -20°C, 0°C, 35°C].
        Verifies strict C-rate piecewise limits and PTC diversion power split.
        """
        batt_cap = 200.0
        avail_dpr = 150.0

        # -40°C: Arctic deep freeze
        res_m40 = NordicColdProtectionEngine.evaluate_preheating_diversion(
            batt_temp_c=-40.0, batt_capacity_kwh=batt_cap, ambient_temp_c=-40.0, available_dpr_kw=avail_dpr
        )
        self.assertTrue(res_m40["is_preheating_active"])
        self.assertEqual(res_m40["ptc_allocated_kw"], 25.0)
        self.assertEqual(res_m40["cell_charge_kw"], 10.0)  # 0.05 C * 200 kWh = 10 kW
        self.assertEqual(res_m40["total_delivered_kw"], 35.0)
        self.assertTrue(res_m40["lithium_plating_prevented"])

        # -20°C: Sub-zero frost
        res_m20 = NordicColdProtectionEngine.evaluate_preheating_diversion(
            batt_temp_c=-20.0, batt_capacity_kwh=batt_cap, ambient_temp_c=-20.0, available_dpr_kw=avail_dpr
        )
        self.assertTrue(res_m20["is_preheating_active"])
        self.assertEqual(res_m20["ptc_allocated_kw"], 25.0)
        self.assertEqual(res_m20["cell_charge_kw"], 10.0)

        # 0°C: Freezing point transition
        res_0 = NordicColdProtectionEngine.evaluate_preheating_diversion(
            batt_temp_c=0.0, batt_capacity_kwh=batt_cap, ambient_temp_c=0.0, available_dpr_kw=avail_dpr
        )
        self.assertTrue(res_0["is_preheating_active"])
        self.assertEqual(res_0["ptc_allocated_kw"], 25.0)
        self.assertEqual(res_0["cell_charge_kw"], 100.0)  # 0.50 C * 200 kWh = 100 kW
        self.assertEqual(res_0["total_delivered_kw"], 125.0)

        # 35°C: Hot summer / pre-warmed battery
        res_35 = NordicColdProtectionEngine.evaluate_preheating_diversion(
            batt_temp_c=35.0, batt_capacity_kwh=batt_cap, ambient_temp_c=35.0, available_dpr_kw=avail_dpr
        )
        self.assertFalse(res_35["is_preheating_active"])
        self.assertEqual(res_35["ptc_allocated_kw"], 0.0)
        self.assertEqual(res_35["cell_charge_kw"], 150.0)  # Full 150 kW to cells

    def test_zero_heating_available_power_starvation(self):
        """Adversarial Scenario: Grid / DPR power starvation (0 kW available)."""
        res = NordicColdProtectionEngine.evaluate_preheating_diversion(
            batt_temp_c=-15.0, batt_capacity_kwh=200.0, ambient_temp_c=-15.0, available_dpr_kw=0.0
        )
        self.assertTrue(res["is_preheating_active"])
        self.assertEqual(res["ptc_allocated_kw"], 0.0)
        self.assertEqual(res["cell_charge_kw"], 0.0)
        self.assertEqual(res["total_delivered_kw"], 0.0)

    def test_defective_ptc_negative_thermal_drift_masking(self):
        """
        Adversarial Scenario: Defective PTC resistance (0 kW heat output) with ambient at -40°C.
        Evaluates formula est_heating_minutes and uncovers max(1.0, net_heating_kw) clamping.
        """
        # Battery at 10°C, ambient at -40°C, PTC output = 0 kW
        # Physical heat loss: 0.050 kW/K * (10 - (-40)) = 2.5 kW
        # Internal gain: 1.2 kW. Net heat rate: 1.2 - 2.5 = -1.3 kW (battery is cooling!)
        res = NordicColdProtectionEngine.evaluate_preheating_diversion(
            batt_temp_c=10.0, batt_capacity_kwh=200.0, ambient_temp_c=-40.0, available_dpr_kw=0.0
        )
        # Remediated: When battery is cooling/stalled (net_heating_kw <= 0.05 kW), est_heating_minutes is None
        self.assertIsNone(res["est_heating_minutes"])

    def test_cold_session_simulation_arctic_divergence(self):
        """
        Adversarial Scenario: Simulate 100 kWh charging session at -40°C vs 35°C.
        Assisted charging cuts -40°C duration from 600m (timeout) to 74m (>85% reduction).
        """
        comp_m40 = NordicColdProtectionEngine.simulate_cold_session_comparison(
            initial_batt_temp_c=-40.0, ambient_temp_c=-40.0, batt_capacity_kwh=200.0, target_kwh=100.0, max_dpr_kw=150.0
        )
        self.assertEqual(comp_m40["unassisted_minutes"], 600.0)
        self.assertLess(comp_m40["assisted_minutes"], 80.0)
        self.assertGreater(comp_m40["reduction_pct"], 80.0)
        self.assertTrue(comp_m40["meets_35_pct_target"])

        # Boundary at 35°C
        comp_35 = NordicColdProtectionEngine.simulate_cold_session_comparison(
            initial_batt_temp_c=35.0, ambient_temp_c=35.0, batt_capacity_kwh=200.0, target_kwh=100.0, max_dpr_kw=150.0
        )
        self.assertEqual(comp_35["unassisted_minutes"], 40.0)
        self.assertEqual(comp_35["assisted_minutes"], 40.0)
        self.assertEqual(comp_35["reduction_pct"], 0.0)
        self.assertFalse(comp_35["meets_35_pct_target"])


class TestOfflineWALDurabilityStress(unittest.TestCase):
    """Adversarial stress testing of 72h WAL engine, Merkle trees, and synchronization."""

    def setUp(self):
        self.wal = OfflineWALManager(db_path=":memory:")

    def test_10000_offline_transaction_commits(self):
        """
        Adversarial Stress Test: Durably record 10,000 offline transaction commits.
        Verify consistency, transaction count, and Merkle root calculation performance.
        """
        for i in range(10000):
            tx = {
                "transaction_uuid": f"tx-uuid-{i:05d}",
                "session_id": f"SESS_{i:05d}",
                "site_id": "S3",
                "charger_id": f"D3-{(i % 10) + 1}",
                "vehicle_id": f"VEH_{i:05d}",
                "start_ts": "2026-11-13T01:00:00+02:00",
                "stop_ts": "2026-11-13T02:00:00+02:00",
                "start_meter_wh": 1000000 + i * 50000,
                "stop_meter_wh": 1050000 + i * 50000,
                "total_energy_kwh": 50.0 + (i % 25),
                "peak_power_kw": 120.0,
            }
            self.wal.record_offline_transaction(tx)

        self.assertEqual(self.wal.count_transactions(), 10000)
        self.assertEqual(self.wal.count_transactions(status="PENDING"), 10000)

        # Merkle root computation over all 10,000 entries
        root = self.wal.compute_merkle_root()
        self.assertEqual(len(root), 64)

    def test_duplicate_uuid_replay_demotes_confirmed_transaction(self):
        """
        Adversarial Scenario: A network retry queue replays a previously confirmed transaction.
        Uncovers idempotency vulnerability where INSERT OR REPLACE resets CONFIRMED back to PENDING.
        """
        tx = {
            "transaction_uuid": "idempotent-uuid-9999",
            "session_id": "SESS_ACK_TEST",
            "site_id": "S3",
            "charger_id": "D3-1",
            "total_energy_kwh": 75.0,
        }
        self.wal.record_offline_transaction(tx)

        # Handshake ACK from cloud confirms the transaction
        self.wal.reconcile_reconnection_ack(["idempotent-uuid-9999"])
        confirmed_rec = self.wal.get_transaction_by_uuid("idempotent-uuid-9999")
        self.assertEqual(confirmed_rec["sync_status"], "CONFIRMED")
        self.assertIsNotNone(confirmed_rec["synced_at"])

        # Replay the identical transaction
        self.wal.record_offline_transaction(tx)
        replayed_rec = self.wal.get_transaction_by_uuid("idempotent-uuid-9999")

        # Remediated: Status remains CONFIRMED, synced_at is preserved
        self.assertEqual(replayed_rec["sync_status"], "CONFIRMED")
        self.assertIsNotNone(replayed_rec["synced_at"])

    def test_out_of_order_insertion_merkle_root_invariance(self):
        """
        Adversarial Scenario: Transactions arrive out of order at the cloud.
        Assert that ORDER BY transaction_uuid provides deterministic root invariance.
        """
        wal1 = OfflineWALManager(db_path=":memory:")
        wal2 = OfflineWALManager(db_path=":memory:")

        tx_list = [
            {"transaction_uuid": f"uuid-{i:03d}", "session_id": f"s-{i}", "total_energy_kwh": float(i * 5)}
            for i in range(500)
        ]

        # Insert sequentially in wal1
        for t in tx_list:
            wal1.record_offline_transaction(t)

        # Insert randomly shuffled in wal2
        shuffled = list(tx_list)
        random.seed(42)
        random.shuffle(shuffled)
        for t in shuffled:
            wal2.record_offline_transaction(t)

        root1 = wal1.compute_merkle_root()
        root2 = wal2.compute_merkle_root()

        self.assertEqual(root1, root2)

    def test_merkle_root_single_bit_tamper_detection(self):
        """
        Adversarial Scenario: Detect subtle corruption (0.001 kWh delta) in 1 of 1,000 transactions.
        """
        wal_clean = OfflineWALManager(db_path=":memory:")
        wal_tampered = OfflineWALManager(db_path=":memory:")

        for i in range(1000):
            tx = {
                "transaction_uuid": f"uuid-{i:04d}",
                "site_id": "S3",
                "charger_id": "D3-1",
                "total_energy_kwh": 50.0,
                "stop_ts": "2026-11-13T02:00:00Z",
            }
            wal_clean.record_offline_transaction(tx)
            if i == 500:
                tx_tampered = dict(tx)
                tx_tampered["total_energy_kwh"] = 50.001
                wal_tampered.record_offline_transaction(tx_tampered)
            else:
                wal_tampered.record_offline_transaction(tx)

        self.assertNotEqual(wal_clean.compute_merkle_root(), wal_tampered.compute_merkle_root())

    def test_large_batch_ack_sqlite_variable_overflow(self):
        """
        Remediated Scenario: Cloud CSMS returns an ACK containing 40,000 UUIDs in one reconciliation payload.
        Verifies chunking in batches of 500 prevents sqlite3.OperationalError: too many SQL variables.
        """
        uuids_40k = [f"uuid-{i:05d}" for i in range(40000)]
        self.wal.record_offline_transaction({"transaction_uuid": uuids_40k[0]})
        self.wal.record_offline_transaction({"transaction_uuid": uuids_40k[39999]})

        updated = self.wal.reconcile_reconnection_ack(uuids_40k)
        self.assertEqual(updated, 2)
        rec0 = self.wal.get_transaction_by_uuid(uuids_40k[0])
        self.assertEqual(rec0["sync_status"], "CONFIRMED")


if __name__ == "__main__":
    unittest.main()
