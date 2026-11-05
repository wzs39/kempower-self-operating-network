"""
tests/test_commercial_settlement.py

Comprehensive Unit & Integration Test Suite for:
1. Commercial Settlement & Dispute Clearing Engine (F15)
2. Financial Sensitivity & NPV/IRR Engine (F16)
"""

import unittest
import hashlib
from src.commercial.settlement_clearing import (
    ContractTier,
    ExemptionReason,
    ContractTierConfig,
    TIER_CONFIGS,
    SettlementClearingEngine,
    MonthlyInvoiceStatement,
    generate_monthly_settlement,
)
from src.commercial.sensitivity_analyzer import (
    FinancialSensitivityEngine,
    OFFICIAL_EQUIPMENT_COSTS,
)

class TestCommercialSettlementClearing(unittest.TestCase):
    """Test suite for B2B AEaaS Contract & Settlement Clearing Engine."""

    def test_tier_configurations(self):
        """Verify Titanium (99.9%), Gold (99.5%), and Silver (99.0%) tier specifications."""
        ti = TIER_CONFIGS[ContractTier.TITANIUM]
        self.assertEqual(ti.uptime_target_pct, 99.90)
        self.assertEqual(ti.monthly_base_fee_eur, 15000.0)
        self.assertEqual(ti.step_penalty_pct, 2.50)
        self.assertEqual(ti.full_waiver_threshold_pct, 96.00)
        self.assertEqual(ti.mrdt_buffer_min, 10.0)
        self.assertEqual(ti.p_base_eur, 350.0)
        self.assertEqual(ti.c_min_eur, 7.50)
        self.assertEqual(ti.c_energy_eur, 2.00)

        gd = TIER_CONFIGS[ContractTier.GOLD]
        self.assertEqual(gd.uptime_target_pct, 99.50)
        self.assertEqual(gd.monthly_base_fee_eur, 10000.0)
        self.assertEqual(gd.step_penalty_pct, 2.00)
        self.assertEqual(gd.full_waiver_threshold_pct, 95.00)
        self.assertEqual(gd.mrdt_buffer_min, 15.0)
        self.assertEqual(gd.p_base_eur, 250.0)
        self.assertEqual(gd.c_min_eur, 5.00)
        self.assertEqual(gd.c_energy_eur, 1.50)

        sv = TIER_CONFIGS[ContractTier.SILVER]
        self.assertEqual(sv.uptime_target_pct, 99.00)
        self.assertEqual(sv.monthly_base_fee_eur, 7500.0)
        self.assertEqual(sv.step_penalty_pct, 1.50)
        self.assertEqual(sv.full_waiver_threshold_pct, 94.00)
        self.assertEqual(sv.mrdt_buffer_min, 20.0)
        self.assertEqual(sv.p_base_eur, 150.0)
        self.assertEqual(sv.c_min_eur, 3.00)
        self.assertEqual(sv.c_energy_eur, 1.00)

    def test_mrdt_dwell_shortfall_exemption(self):
        """Customer dwell shorter than physical MRDT must trigger moral hazard exemption."""
        tier_cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip = {
            "trip_id": "T_SHORTFALL_01",
            "vehicle_id": "B01",
            "site_id": "S1",
            "arrive_ts": "2026-11-13T01:00:00+02:00",
            "depart_sched_ts": "2026-11-13T01:10:00+02:00",
            "depart_actual_ts": "2026-11-13T01:10:00+02:00",
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 30.0,
            "dwell_actual_min": 10.0, # Way below ~124 min MRDT
            "delay_min": 30.0,
            "end_reason": "completed",
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, tier_cfg)
        self.assertFalse(rec.mrdt_satisfied)
        self.assertEqual(rec.exemption_reason, ExemptionReason.CUSTOMER_DWELL_SHORTFALL)
        self.assertEqual(rec.delay_penalty_eur, 0.0)
        self.assertEqual(rec.energy_penalty_eur, 0.0)
        self.assertEqual(rec.total_penalty_eur, 0.0)

    def test_premature_unplug_exemption(self):
        """Driver or operator premature cable disconnect must be exempt from liquidated damages."""
        tier_cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip = {
            "trip_id": "T_UNPLUG_01",
            "vehicle_id": "B02",
            "site_id": "S1",
            "arrive_ts": "2026-11-13T01:00:00+02:00",
            "depart_sched_ts": "2026-11-13T05:30:00+02:00",
            "depart_actual_ts": "2026-11-13T05:30:00+02:00",
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 50.0,
            "dwell_actual_min": 270.0,
            "delay_min": 20.0,
            "end_reason": "unplugged_by_operator",
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, tier_cfg)
        self.assertTrue(rec.mrdt_satisfied)
        self.assertEqual(rec.exemption_reason, ExemptionReason.PREMATURE_UNPLUG)
        self.assertEqual(rec.total_penalty_eur, 0.0)

    def test_vehicle_bms_fault_exemption(self):
        """Vehicle internal BMS abort must be classified as vehicle fault with 0 operator penalty."""
        tier_cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip = {
            "trip_id": "T_BMS_01",
            "vehicle_id": "B03",
            "site_id": "S1",
            "arrive_ts": "2026-11-13T01:00:00+02:00",
            "depart_sched_ts": "2026-11-13T05:30:00+02:00",
            "depart_actual_ts": "2026-11-13T05:30:00+02:00",
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 60.0,
            "dwell_actual_min": 270.0,
            "delay_min": 0.0,
            "end_reason": "bms_abort",
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, tier_cfg)
        self.assertEqual(rec.exemption_reason, ExemptionReason.VEHICLE_BMS_FAULT)
        self.assertEqual(rec.total_penalty_eur, 0.0)

    def test_grid_force_majeure_exemption(self):
        """External utility blackout without BESS must be classified as grid force majeure."""
        tier_cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip = {
            "trip_id": "T_GRID_01",
            "vehicle_id": "B04",
            "site_id": "S1",
            "arrive_ts": "2026-11-13T01:00:00+02:00",
            "depart_sched_ts": "2026-11-13T05:30:00+02:00",
            "depart_actual_ts": "2026-11-13T05:30:00+02:00",
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 55.0,
            "dwell_actual_min": 270.0,
            "delay_min": 25.0,
            "end_reason": "completed",
            "grid_outage_force_majeure": True,
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, tier_cfg)
        self.assertEqual(rec.exemption_reason, ExemptionReason.GRID_FORCE_MAJEURE)
        self.assertEqual(rec.total_penalty_eur, 0.0)

    def test_legitimate_operational_delay_and_deficit_penalty(self):
        """Legitimate operator fault must compute exact liquidated damages per SLA formula."""
        tier_cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip = {
            "trip_id": "T_PENALTY_01",
            "vehicle_id": "B05",
            "site_id": "S1",
            "arrive_ts": "2026-11-13T01:00:00+02:00",
            "depart_sched_ts": "2026-11-13T05:30:00+02:00",
            "depart_actual_ts": "2026-11-13T05:55:00+02:00",
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 70.0, # 15% deficit = 60 kWh
            "dwell_actual_min": 295.0,
            "delay_min": 25.0, # 10 min beyond 15 min buffer
            "end_reason": "completed",
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, tier_cfg)
        self.assertEqual(rec.exemption_reason, ExemptionReason.NONE)
        # Delay: 250 € + (25 - 15) * 5.00 € = 300.00 €
        self.assertEqual(rec.delay_penalty_eur, 300.00)
        # Energy: 60 kWh * 1.50 €/kWh = 90.00 €
        self.assertEqual(rec.energy_deficit_kwh, 60.00)
        self.assertEqual(rec.energy_penalty_eur, 90.00)
        # Total: 300 + 90 = 390.00 €
        self.assertEqual(rec.total_penalty_eur, 390.00)

    def test_piecewise_availability_waiver(self):
        """Verify piecewise step deductions and 100% full waiver threshold."""
        tier_cfg = TIER_CONFIGS[ContractTier.GOLD]
        # Target: 99.50%, Step: 2.0% per 0.1%, Threshold: 95.00%, Base: 10,000 €

        # Case 1: 99.60% (above target) -> 0 €
        s1, r1, d1 = SettlementClearingEngine.compute_availability_deduction(tier_cfg, 99.60)
        self.assertEqual(d1, 0.0)

        # Case 2: 99.40% (0.10% shortfall) -> 1 step -> 2.0% of 10,000 = 200 €
        s2, r2, d2 = SettlementClearingEngine.compute_availability_deduction(tier_cfg, 99.40)
        self.assertAlmostEqual(s2, 0.10, places=4)
        self.assertEqual(r2, 2.0)
        self.assertEqual(d2, 200.0)

        # Case 3: 95.00% (4.50% shortfall) -> 45 steps -> 90.0% of 10,000 = 9,000 €
        s3, r3, d3 = SettlementClearingEngine.compute_availability_deduction(tier_cfg, 95.00)
        self.assertAlmostEqual(s3, 4.50, places=4)
        self.assertEqual(r3, 90.0)
        self.assertEqual(d3, 9000.0)

        # Case 4: 94.50% (< 95.00%) -> Full Waiver -> 100.0% of 10,000 = 10,000 €
        s4, r4, d4 = SettlementClearingEngine.compute_availability_deduction(tier_cfg, 94.50)
        self.assertEqual(r4, 100.0)
        self.assertEqual(d4, 10000.0)

    def test_aggregate_150_percent_cap_and_non_negative_invoice(self):
        """Aggregate liability must be capped at 150% of base fee, and invoice clamped to >= 0 €."""
        # 10,000 € base fee; 150% cap = 15,000.00 €
        huge_trips = [
            {
                "trip_id": f"T_HUGE_{i}",
                "vehicle_id": f"V{i}",
                "battery_kwh": 600.0,
                "p_charger_max_kw": 150.0,
                "p_veh_max_kw": 150.0,
                "soc_arrive_pct": 10.0,
                "soc_req_pct": 90.0,
                "soc_dep_pct": 20.0, # 70% deficit = 420 kWh -> 630 €
                "dwell_actual_min": 300.0,
                "delay_min": 120.0, # 250 + 105*5 = 775 €
                "end_reason": "completed",
            }
            for i in range(25) # 25 * 1405 € = 35,125 € claims
        ]

        stmt = SettlementClearingEngine.generate_monthly_settlement(
            site_id="S1",
            month="2026-11",
            tier=ContractTier.GOLD,
            actual_availability_pct=94.00, # 10,000 € availability deduction
            trips=huge_trips,
        )

        self.assertEqual(stmt.monthly_base_fee_eur, 10000.0)
        self.assertEqual(stmt.max_liability_cap_eur, 15000.0)
        self.assertEqual(stmt.final_payout_deduction_eur, 15000.0)
        # Net invoice payable clamped to 0.00 € (operator never pays customer on an invoice)
        self.assertEqual(stmt.net_invoice_payable_eur, 0.0)
        # Excess 5,000 € carried forward as credit
        self.assertEqual(stmt.credit_carryforward_eur, 5000.0)

    def test_sha256_audit_trail_integrity(self):
        """Every generated monthly statement must contain a valid, reproducible SHA-256 seal."""
        stmt = SettlementClearingEngine.generate_monthly_settlement(
            site_id="S1",
            month="2026-11",
            tier=ContractTier.GOLD,
            actual_availability_pct=99.85,
        )
        expected_payload = f"S1|2026-11|Gold|{stmt.monthly_base_fee_eur:.2f}|{stmt.actual_availability_pct:.4f}|{stmt.final_payout_deduction_eur:.2f}|{stmt.net_invoice_payable_eur:.2f}"
        expected_hash = hashlib.sha256(expected_payload.encode("utf-8")).hexdigest()
        self.assertEqual(stmt.audit_hash, expected_hash)
        self.assertEqual(len(stmt.audit_hash), 64)

    def test_render_markdown_audit_table(self):
        """Markdown audit table generator must produce structured report containing audit hash."""
        stmt = SettlementClearingEngine.generate_monthly_settlement(
            site_id="S1",
            month="2026-11",
            tier=ContractTier.TITANIUM,
            actual_availability_pct=99.95,
        )
        md = SettlementClearingEngine.render_markdown_audit_table(stmt)
        self.assertIn("# B2B Monthly SLA Settlement Statement", md)
        self.assertIn("Titanium", md)
        self.assertIn(stmt.audit_hash, md)
        self.assertIn("Net Operator Invoice Payable", md)

    def test_module_level_interface_contract(self):
        """Module-level generate_monthly_settlement must satisfy PROJECT.md:117 contract."""
        res = generate_monthly_settlement("S1", "2026-11")
        self.assertIsInstance(res, MonthlyInvoiceStatement)
        self.assertEqual(res["site_id"], "S1")
        self.assertIn("net_invoice_payable_eur", res)
        self.assertGreaterEqual(res["net_invoice_payable_eur"], 0.0)


class TestFinancialSensitivityEngine(unittest.TestCase):
    """Test suite for 100-Station Financial Sensitivity & Pure Python NPV/IRR Solver."""

    def test_bess_hardware_cost_grounding(self):
        """BESS initial CAPEX must strictly equal 13,422,000.00 € per equipment_costs.csv."""
        bess = FinancialSensitivityEngine.compute_bess_initial_capex()
        self.assertEqual(bess["bess_sites_count"], 20)
        self.assertEqual(bess["bess_energy_kwh"], 35000.0)
        self.assertEqual(bess["bess_power_kw"], 20200.0)
        # 35,000 * 320 = 11,200,000 €
        self.assertEqual(bess["bess_energy_capex_eur"], 11200000.0)
        # 20,200 * 110 = 2,222,000 €
        self.assertEqual(bess["bess_power_capex_eur"], 2222000.0)
        # Total = 13,422,000 €
        self.assertEqual(bess["total_bess_capex_eur"], 13422000.0)

    def test_network_baseline_asset_valuation(self):
        """Physical asset replacement valuation must strictly ground in unit catalog."""
        baseline = FinancialSensitivityEngine.compute_network_baseline_capex()
        self.assertIn("standard_dispensers_with_civil_eur", baseline)
        self.assertIn("bess_total_capex_eur", baseline)
        self.assertEqual(baseline["bess_total_capex_eur"], 13422000.0)
        self.assertGreater(baseline["total_physical_asset_valuation_eur"], 50000000.0)

    def test_npv_irr_solver_robustness(self):
        """Deterministic pure Python solver must compute exact analytical NPV and IRR."""
        # Simple benchmark: Cash outflow -100, Inflow +110 in Year 1 -> IRR is exactly 10.0% (0.10)
        simple_cfs = [-100.0, 110.0]
        npv_at_10 = FinancialSensitivityEngine._compute_npv(0.10, simple_cfs)
        self.assertAlmostEqual(npv_at_10, 0.0, places=4)

        irr_val = FinancialSensitivityEngine._compute_irr(simple_cfs)
        self.assertAlmostEqual(irr_val, 0.10, places=4)

    def test_multi_axis_sensitivity_matrix(self):
        """Evaluate sensitivity matrix across spot price spikes, wage variations, and BESS cycles."""
        matrix = FinancialSensitivityEngine.generate_sensitivity_matrix()
        self.assertEqual(len(matrix), 9)

        by_name = {m["scenario_name"]: m for m in matrix}

        # Spot volatility comparison: +50% spike yields higher savings than baseline
        base_spot = by_name["Spot Volatility: Baseline"]
        spike_spot = by_name["Spot Volatility: +50% Peak Spike"]
        self.assertGreater(spike_spot["annual_spot_arbitrage_savings_eur"], base_spot["annual_spot_arbitrage_savings_eur"])

        # Labor inflation comparison: 95k € yields higher savings than 75k €
        wage_75 = by_name["Labor Inflation: 75,000 € / FTE"]
        wage_95 = by_name["Labor Inflation: 95,000 € / FTE (+8.3%)"]
        self.assertGreater(wage_95["annual_labor_savings_eur"], wage_75["annual_labor_savings_eur"])

        # BESS cycle: 10-year replacement has higher NPV than 7-year replacement
        bess_10 = by_name["BESS Replacement: 10-Year (Baseline 320 €/kWh)"]
        bess_7 = by_name["BESS Replacement: 7-Year High-Cycling"]
        self.assertGreater(bess_10["npv_eur"], bess_7["npv_eur"])


if __name__ == "__main__":
    unittest.main()
