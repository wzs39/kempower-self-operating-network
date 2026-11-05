"""
Unit & Integration Test Suite for M2 Hardware Self-Healing, Nordic Cold & Microgrid
Test File: tests/test_m2_hardware_self_healing.py

Verifies:
- F11: 25 kW Module-Level DPR Self-Healing (sub-100ms isolation, wear-leveling duty rotation)
- F12: Nordic Sub-Zero (-15°C) Battery Pre-Heating Dynamic Diversion & Lithium Plating Avoidance
- F13: Microgrid BESS/PV Coordinated Dispatch Interface & Ramp-Rate Clamping
- F14: 72h SQLite WAL Durability, Merkle Reconciliation & Idempotence
"""

import unittest
import numpy as np

from src.core.dpr_matrix import DPRMatrix, PowerModule
from src.core.self_healing import NordicColdProtectionEngine, OfflineWALManager
from src.core.mpc_optimizer import MPCOptimizer, SiteMPCConfig, BESSConfig, VehicleSchedule

class TestDPRModuleSelfHealingAndWearLeveling(unittest.TestCase):
    """F11: 25 kW Module DPR Self-Healing & Wear-Leveling Tests."""

    def setUp(self):
        self.dpr = DPRMatrix("S1")  # S1 has 3 cabinets x 14-15 modules = 43 modules

    def test_sub_100ms_module_isolation(self):
        """Verify individual 25 kW module isolates in 85 ms (<100 ms) upon overtemperature."""
        mod_id = "S1_M01"
        self.assertIn(mod_id, self.dpr.modules)
        self.assertTrue(self.dpr.modules[mod_id].is_healthy)

        success, duration_ms, details = self.dpr.isolate_module(mod_id, reason="OVERTEMP_IGBT")

        self.assertTrue(success)
        self.assertEqual(duration_ms, 85.0)
        self.assertLess(duration_ms, 100.0)
        self.assertFalse(self.dpr.modules[mod_id].is_healthy)
        self.assertEqual(self.dpr.modules[mod_id].status, "ISOLATED_TEMP")
        self.assertEqual(self.dpr.modules[mod_id].current_output_kw, 0.0)
        self.assertIsNone(self.dpr.modules[mod_id].assigned_gun)

    def test_cabinet_remains_operational_n_minus_1(self):
        """Verify isolating 1 module leaves remaining 14 modules in cabinet C1-1 healthy."""
        mod_id = "S1_M01"
        cab_id = self.dpr.modules[mod_id].cabinet_id

        # Total healthy in cabinet before
        healthy_before = [m for m in self.dpr.modules.values() if m.cabinet_id == cab_id and m.is_healthy]
        self.assertEqual(len(healthy_before), 15)

        success, _, details = self.dpr.isolate_module(mod_id, reason="OVERTEMP")
        self.assertTrue(success)
        self.assertEqual(details["remaining_cabinet_modules"], 14)
        self.assertEqual(details["remaining_cabinet_capacity_kw"], 350.0)  # 14 * 25 kW

        # Cabinet health indicator is NOT zeroed out (unlike old whole-cabinet isolation)
        self.assertGreater(self.dpr.cabinet_health.get(cab_id, 1.0), 0.0)

    def test_wear_leveling_duty_rotation_selection(self):
        """Verify wear-leveling prioritizes freshest modules with lowest runtime/thermal stress."""
        cab_id = "C1-1"
        cab_mods = [m for m in self.dpr.modules.values() if m.cabinet_id == cab_id]

        # Simulate varied operating hours and temperatures
        for idx, m in enumerate(cab_mods):
            m.operating_hours = float(idx * 10)  # 0, 10, 20... 140 hours
            m.temperature_c = 30.0 + idx * 2.0   # 30, 32, 34... 58°C
            m.start_stop_cycles = idx * 5

        # Request 3 modules for a new charging session
        selected_mod_ids = self.dpr.rotate_modules_wear_leveling(
            cabinet_id=cab_id, required_modules=3, ambient_temp_c=20.0
        )
        self.assertEqual(len(selected_mod_ids), 3)
        # Should pick the 3 freshest modules (lowest wear indices)
        self.assertEqual(selected_mod_ids, [cab_mods[0].module_id, cab_mods[1].module_id, cab_mods[2].module_id])

    def test_wear_difference_rotation_trigger(self):
        """Verify wear rotation trigger detects when delta hours between active and idle >= 2.0h."""
        cab_id = "C1-1"
        cab_mods = [m for m in self.dpr.modules.values() if m.cabinet_id == cab_id]
        for m in cab_mods:
            m.operating_hours = 7.0
            m.assigned_gun = None

        # Active module with 10.0 operating hours
        cab_mods[0].assigned_gun = "D1-1"
        cab_mods[0].operating_hours = 10.0

        needed, delta_h, worn_id, fresh_id = self.dpr.check_wear_leveling_rotation_needed(
            cabinet_id=cab_id, threshold_hours=2.0
        )
        self.assertTrue(needed)
        self.assertAlmostEqual(delta_h, 3.0)
        self.assertEqual(worn_id, cab_mods[0].module_id)
        self.assertEqual(fresh_id, cab_mods[1].module_id)

    def test_module_restoration_after_cooldown(self):
        """Verify restore_module resets module health to operational status."""
        mod_id = "S1_M02"
        self.dpr.isolate_module(mod_id, reason="OVERTEMP")
        self.assertFalse(self.dpr.modules[mod_id].is_healthy)

        restored = self.dpr.restore_module(mod_id)
        self.assertTrue(restored)
        self.assertTrue(self.dpr.modules[mod_id].is_healthy)
        self.assertEqual(self.dpr.modules[mod_id].status, "HEALTHY")

class TestNordicColdProtectionEngine(unittest.TestCase):
    """F12: Nordic Sub-Zero (-15°C) Battery Pre-Heating Dynamic Diversion Tests."""

    def test_lithium_plating_piecewise_c_rate_envelope(self):
        """Verify strict C-rate throttling to prevent lithium plating in Arctic conditions."""
        self.assertEqual(NordicColdProtectionEngine.max_cell_acceptance_c_rate(-15.0), 0.05)
        self.assertEqual(NordicColdProtectionEngine.max_cell_acceptance_c_rate(-10.5), 0.05)
        self.assertEqual(NordicColdProtectionEngine.max_cell_acceptance_c_rate(-5.0), 0.20)
        self.assertEqual(NordicColdProtectionEngine.max_cell_acceptance_c_rate(5.0), 0.50)
        self.assertEqual(NordicColdProtectionEngine.max_cell_acceptance_c_rate(15.0), 1.00)
        self.assertEqual(NordicColdProtectionEngine.max_cell_acceptance_c_rate(25.0), 1.00)

    def test_ptc_dynamic_power_diversion_at_minus_15c(self):
        """Verify 25 kW DPR power diverted to vehicle PTC heating loop at -15°C."""
        batt_capacity = 200.0  # 200 kWh commercial bus battery
        available_kw = 150.0   # 6 DPR modules available

        res = NordicColdProtectionEngine.evaluate_preheating_diversion(
            batt_temp_c=-15.0,
            batt_capacity_kwh=batt_capacity,
            ambient_temp_c=-15.0,
            available_dpr_kw=available_kw,
        )

        self.assertTrue(res["is_preheating_active"])
        self.assertEqual(res["ptc_allocated_kw"], 25.0)  # Exactly 1 DPR module (25 kW)
        # Safe cell limit at -15°C is 0.05 C * 200 kWh = 10 kW
        self.assertEqual(res["cell_charge_kw"], 10.0)
        self.assertEqual(res["total_delivered_kw"], 35.0)  # 25 kW PTC + 10 kW Cell
        self.assertTrue(res["lithium_plating_prevented"])

    def test_full_power_ramp_above_15c(self):
        """Verify full charging power without PTC diversion once battery reaches 15°C."""
        batt_capacity = 200.0
        available_kw = 150.0

        res = NordicColdProtectionEngine.evaluate_preheating_diversion(
            batt_temp_c=16.0,
            batt_capacity_kwh=batt_capacity,
            ambient_temp_c=-15.0,
            available_dpr_kw=available_kw,
        )

        self.assertFalse(res["is_preheating_active"])
        self.assertEqual(res["ptc_allocated_kw"], 0.0)
        self.assertEqual(res["cell_charge_kw"], 150.0)  # Full 150 kW to cells

    def test_cold_session_duration_reduction_over_35_pct(self):
        """Verify dynamic PTC diversion cuts total sub-zero charging time by > 35%."""
        comp = NordicColdProtectionEngine.simulate_cold_session_comparison(
            initial_batt_temp_c=-15.0,
            ambient_temp_c=-15.0,
            batt_capacity_kwh=200.0,
            target_kwh=100.0,
            max_dpr_kw=150.0,
        )

        self.assertGreater(comp["unassisted_minutes"], comp["assisted_minutes"])
        self.assertGreaterEqual(
            comp["reduction_pct"], 35.0,
            f"Reduction was {comp['reduction_pct']}%, expected >= 35.0%",
        )
        self.assertTrue(comp["meets_35_pct_target"])

class TestMicrogridBESSAndPVCoordinatedDispatch(unittest.TestCase):
    """F13: Microgrid BESS/PV Coordinated Dispatch Interface Tests."""

    def test_bess_cost_accounting_grounding(self):
        """Verify 500 kWh / 250 kW BESS capital cost strictly matches equipment_costs.csv."""
        # 320 €/kWh * 500 kWh = 160,000 €; 110 €/kW * 250 kW = 27,500 €; Total = 187,500 €
        capex = SiteMPCConfig.compute_microgrid_capex(
            bess_kwh=500.0, bess_kw=250.0, pv_kwp=100.0
        )
        self.assertEqual(capex["bess_energy_capex_eur"], 160000.0)
        self.assertEqual(capex["bess_power_capex_eur"], 27500.0)
        self.assertEqual(capex["bess_total_capex_eur"], 187500.0)
        self.assertEqual(capex["pv_total_capex_eur"], 90000.0)
        self.assertEqual(capex["total_microgrid_capex_eur"], 277500.0)

    def test_bess_arbitrage_s4_spike(self):
        """Verify BESS discharges during 799.30 €/MWh spot price surge to minimize cost."""
        bess = BESSConfig(
            capacity_kwh=500.0,
            max_power_kw=250.0,
            initial_soc=0.80,
            min_soc=0.10,
            max_soc=0.90,
        )
        cfg = SiteMPCConfig(site_id="S4", transformer_max_kw=600.0, bess=bess)
        optimizer = MPCOptimizer(cfg)

        # 4 steps of 15 min: step 2 has extreme 799.30 €/MWh spike
        prices = [45.0, 45.0, 799.30, 45.0]
        schedules = [
            VehicleSchedule(
                vehicle_id="BUS-S4",
                arrive_step=0,
                depart_step=4,
                arrive_soc=0.20,
                required_soc=0.70,
                battery_kwh=150.0,
                max_charge_kw=150.0,
            )
        ]

        plan = optimizer.solve_15min_horizon(
            spot_prices_eur_mwh=prices, fleet_schedules=schedules
        )
        self.assertTrue(plan.is_optimal)
        # BESS discharges positively at spike step 2
        self.assertGreater(plan.bess_power_kw[2], 0.0)

    def test_pv_self_consumption_priority(self):
        """Verify solar PV generation is utilized to reduce grid import."""
        cfg = SiteMPCConfig(site_id="S1", transformer_max_kw=1200.0)
        optimizer = MPCOptimizer(cfg)

        prices = [50.0, 50.0, 50.0, 50.0]
        pv_gen = [100.0, 100.0, 100.0, 100.0]  # 100 kW solar available
        schedules = [
            VehicleSchedule(
                vehicle_id="BUS-1",
                arrive_step=0,
                depart_step=4,
                arrive_soc=0.30,
                required_soc=0.70,
                battery_kwh=100.0,
                max_charge_kw=100.0,
            )
        ]

        # Case A: Without PV
        plan_no_pv = optimizer.solve_15min_horizon(
            spot_prices_eur_mwh=prices, fleet_schedules=schedules
        )
        # Case B: With PV
        plan_with_pv = optimizer.solve_15min_horizon(
            spot_prices_eur_mwh=prices,
            fleet_schedules=schedules,
            pv_generation_kw=pv_gen,
        )

        self.assertTrue(plan_with_pv.is_optimal)
        self.assertLess(
            float(np.sum(plan_with_pv.grid_power_kw)),
            float(np.sum(plan_no_pv.grid_power_kw)),
        )

    def test_grid_ramp_rate_clamping_constraint(self):
        """Verify grid power ramp rate between consecutive steps is bounded by max_grid_ramp_kw."""
        ramp_limit = 50.0  # Max 50 kW step change
        cfg = SiteMPCConfig(
            site_id="S1", transformer_max_kw=1200.0, max_grid_ramp_kw=ramp_limit
        )
        optimizer = MPCOptimizer(cfg)

        prices = [30.0, 30.0, 30.0, 30.0]
        schedules = [
            VehicleSchedule(
                vehicle_id="BUS-RAMP",
                arrive_step=1,
                depart_step=3,
                arrive_soc=0.10,
                required_soc=0.80,
                battery_kwh=100.0,
                max_charge_kw=150.0,
            )
        ]

        plan = optimizer.solve_15min_horizon(
            spot_prices_eur_mwh=prices, fleet_schedules=schedules
        )
        self.assertTrue(plan.is_optimal)

        # Check all step transitions
        for t in range(1, len(plan.grid_power_kw)):
            delta = abs(plan.grid_power_kw[t] - plan.grid_power_kw[t - 1])
            self.assertLessEqual(
                delta,
                ramp_limit + 1e-3,
                f"Ramp delta {delta:.2f} exceeded limit {ramp_limit}",
            )

class TestOfflineWALDurabilityAndReconciliation(unittest.TestCase):
    """F14: 72h WAL Durability & Idempotent Reconciliation Protocol Tests."""

    def setUp(self):
        self.wal = OfflineWALManager(db_path=":memory:")

    def test_wal_persistence_under_offline_islanding(self):
        """Verify offline transaction is durably recorded with status PENDING."""
        tx = {
            "session_id": "SE_OFFLINE_01",
            "site_id": "S3",
            "charger_id": "D3-1",
            "vehicle_id": "V_BUS_99",
            "start_ts": "2026-11-13T03:00:00+02:00",
            "stop_ts": "2026-11-13T04:00:00+02:00",
            "start_meter_wh": 1000000,
            "stop_meter_wh": 1080000,
            "total_energy_kwh": 80.0,
            "peak_power_kw": 120.0,
        }
        tx_uuid = self.wal.record_offline_transaction(tx)
        self.assertTrue(len(tx_uuid) > 0)

        record = self.wal.get_transaction_by_uuid(tx_uuid)
        self.assertIsNotNone(record)
        self.assertEqual(record["session_id"], "SE_OFFLINE_01")
        self.assertEqual(record["sync_status"], "PENDING")
        self.assertEqual(record["total_energy_kwh"], 80.0)

    def test_merkle_root_computation(self):
        """Verify Merkle root changes deterministically as transactions are recorded."""
        empty_root = self.wal.compute_merkle_root()
        self.assertTrue(len(empty_root) == 64)

        tx1 = {
            "session_id": "SE1",
            "site_id": "S3",
            "charger_id": "D3-1",
            "vehicle_id": "V1",
            "start_ts": "2026-11-13T03:00:00+02:00",
            "stop_ts": "2026-11-13T04:00:00+02:00",
            "total_energy_kwh": 50.0,
            "peak_power_kw": 100.0,
        }
        self.wal.record_offline_transaction(tx1)
        root1 = self.wal.compute_merkle_root()

        self.assertNotEqual(empty_root, root1)

        tx2 = {
            "session_id": "SE2",
            "site_id": "S3",
            "charger_id": "D3-2",
            "vehicle_id": "V2",
            "start_ts": "2026-11-13T04:00:00+02:00",
            "stop_ts": "2026-11-13T05:00:00+02:00",
            "total_energy_kwh": 60.0,
            "peak_power_kw": 110.0,
        }
        self.wal.record_offline_transaction(tx2)
        root2 = self.wal.compute_merkle_root()

        self.assertNotEqual(root1, root2)

    def test_idempotent_reconciliation_deduplication(self):
        """Verify inserting the same transaction UUID does not create duplicate rows."""
        fixed_uuid = "550e8400-e29b-41d4-a716-446655440000"
        tx = {
            "transaction_uuid": fixed_uuid,
            "session_id": "SE_RETRY",
            "site_id": "S3",
            "charger_id": "D3-1",
            "vehicle_id": "V1",
            "start_ts": "2026-11-13T03:00:00+02:00",
            "stop_ts": "2026-11-13T03:30:00+02:00",
            "total_energy_kwh": 40.0,
            "peak_power_kw": 100.0,
        }
        # Insert twice
        self.wal.record_offline_transaction(tx)
        self.wal.record_offline_transaction(tx)

        self.assertEqual(self.wal.count_transactions(), 1)

    def test_reconnection_ack_promotion(self):
        """Verify acknowledged transactions transition from PENDING to CONFIRMED."""
        tx = {
            "session_id": "SE_ACK",
            "site_id": "S3",
            "charger_id": "D3-3",
            "vehicle_id": "V3",
            "start_ts": "2026-11-13T05:00:00+02:00",
            "stop_ts": "2026-11-13T06:00:00+02:00",
            "total_energy_kwh": 70.0,
            "peak_power_kw": 120.0,
        }
        tx_uuid = self.wal.record_offline_transaction(tx)

        pending_batch = self.wal.get_pending_sync_batch()
        self.assertEqual(len(pending_batch), 1)

        # Simulate CSMS Reconnection Handshake ACK
        confirmed_count = self.wal.reconcile_reconnection_ack([tx_uuid])
        self.assertEqual(confirmed_count, 1)

        self.assertEqual(self.wal.count_transactions(status="PENDING"), 0)
        self.assertEqual(self.wal.count_transactions(status="CONFIRMED"), 1)

        rec = self.wal.get_transaction_by_uuid(tx_uuid)
        self.assertEqual(rec["sync_status"], "CONFIRMED")
        self.assertIsNotNone(rec["synced_at"])

if __name__ == "__main__":
    unittest.main()
