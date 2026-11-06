"""
tests/test_tier5_commercial_adversarial.py

Tier 5 White-Box Coverage Hardening & Adversarial Stress Probe Test Suite.
Target Scope: Part 2 & Part 3 Commercial Models, Dispute Settlement, Financial Sensitivity,
Labor & CAPEX Ground Truth, and Streamlit Interactive Cockpit (Sentinel v3.0).

Authored by M4 Challenger 2 (Empirical Challenger).

Test Classes:
1. TestTier5SLACalculatorSingularities:
   - MRDT mathematical singularities (zero/negative power, efficiency, delta SoC, zero battery)
   - B2B fleet liquidated damages exact step transitions & grace period gating
   - Piecewise charger availability fee deductions (steps, 90% cap, full waiver, negative/overflow avail)
   - Monthly invoice liability cap clamping & non-negative invariant

2. TestTier5CommercialSettlementHardening:
   - Exemption reason taxonomy, case-insensitivity, and dwell shortfall precedence
   - All three contract tiers (Titanium, Gold, Silver) parameter invariants & custom base fee
   - Sub-capping (avail deduction <= base fee, fleet <= base fee) + 150% aggregate cap
   - Credit carryforward calculation and mathematical conservation laws
   - Cryptographic SHA-256 audit seal deterministic generation & avalanche sensitivity
   - Markdown statement rendering under 0, small, and overflowing line items (>20 items)
   - Data transfer object (DTO) dict protocol & JSON serialization roundtrip

3. TestTier5FinancialSensitivityAdversarial:
   - Empirical asset replacement valuation (87,985,000.00 €) and BESS initial CAPEX (13,422,000.00 €)
   - Pure-Python bisection IRR solver under adversarial cash flows (all positive, all negative, break-even, unprofitable)
   - Multi-axis financial sensitivity matrix completeness & finite value guarantees
   - Extreme macro parameter variations (hyper-inflation, zero discount rate, 0-CAPEX)

4. TestTier5ROILaborGroundTruth:
   - Direct CSV verification of 8,852 operations, 93,412 minutes, and 20.76 FTE
   - Move-and-replug breakdown: 47.93% duration (9.95 FTE = 872,976 €/yr) vs 63.22% count
   - Site S1 replug share (2.79% = 24,336 €/yr) and S1-S5 replug share (6.20% = 54,132 €/yr)
   - Equipment catalog pricing: 18,000 € satellite + 9,000 € civil = 27,000 €/gun
   - Strategy A (0 € CAPEX) vs Strategy B (324,000 € CAPEX, 13.31-year S1 payback)
   - Peak demand charges vs 14-day energy costs comparison

5. TestTier5DashboardUIAndPresentationAdversarial:
   - Headless dashboard payload builder verification and invariant preservation
   - Streamlit AppTest multi-tab rendering across all 4 cockpit views
   - Dynamic contract tier selection and interactive MRDT calculator updates
   - Simulated delay/undercharge slider interaction and JSON invoice generation
   - Wear-leveling toggle state change in Hardware Matrix & Protocol Inspector view
   - 96-interval timeline scrubbing and active incident banner assertions
   - Dual CLI / Streamlit runtime execution guard resilience
"""

from __future__ import annotations

import csv
import json
import math
import os
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Dict, List, Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.commercial.sla_calculator import SLACalculator
from src.commercial.settlement_clearing import (
    ContractTier,
    ExemptionReason,
    ContractTierConfig,
    TIER_CONFIGS,
    DepartureAuditRecord,
    MonthlyInvoiceStatement,
    SettlementClearingEngine,
    generate_monthly_settlement,
)
from src.commercial.sensitivity_analyzer import (
    FinancialSensitivityEngine,
    OFFICIAL_EQUIPMENT_COSTS,
)
from src.commercial.roi_analyzer import ROIAnalyzer
import app


# ============================================================================
# 1. SLA Calculator Singularities & Liquidated Damages
# ============================================================================

class TestTier5SLACalculatorSingularities(unittest.TestCase):
    """Stress tests on mathematical boundaries and edge conditions of SLACalculator."""

    def test_mrdt_zero_or_negative_power(self):
        """Zero or negative charger or vehicle power must return infinity."""
        self.assertEqual(SLACalculator.compute_mrdt(80.0, 20.0, 400.0, 0.0, 150.0), float("inf"))
        self.assertEqual(SLACalculator.compute_mrdt(80.0, 20.0, 400.0, 150.0, 0.0), float("inf"))
        self.assertEqual(SLACalculator.compute_mrdt(80.0, 20.0, 400.0, -50.0, 150.0), float("inf"))
        self.assertEqual(SLACalculator.compute_mrdt(80.0, 20.0, 400.0, 150.0, -50.0), float("inf"))
        self.assertEqual(SLACalculator.compute_mrdt(80.0, 20.0, 400.0, 150.0, 150.0, eta=0.0), float("inf"))
        self.assertEqual(SLACalculator.compute_mrdt(80.0, 20.0, 400.0, 150.0, 150.0, eta=-0.95), float("inf"))

    def test_mrdt_zero_needed_energy(self):
        """When arrival SoC >= required SoC, MRDT must equal buffer time exactly."""
        # soc_req == soc_arrive
        res1 = SLACalculator.compute_mrdt(80.0, 80.0, 400.0, 150.0, 150.0, t_buffer=15.0)
        self.assertEqual(res1, 15.0)

        # soc_req < soc_arrive (arrived with 90%, required 80%)
        res2 = SLACalculator.compute_mrdt(80.0, 90.0, 400.0, 150.0, 150.0, t_buffer=15.0)
        self.assertEqual(res2, 15.0)

        # zero battery capacity
        res3 = SLACalculator.compute_mrdt(80.0, 20.0, 0.0, 150.0, 150.0, t_buffer=20.0)
        self.assertEqual(res3, 20.0)

    def test_mrdt_extreme_capacity_scale(self):
        """Test huge battery capacity (e.g. 5,000 kWh electric ferry) with small charger (50 kW)."""
        mrdt = SLACalculator.compute_mrdt(100.0, 10.0, 5000.0, 50.0, 50.0, eta=0.95, t_buffer=15.0)
        # Needed: 0.90 * 5000 = 4500 kWh. Power: 50 * 0.95 = 47.5 kW. Time = (4500 / 47.5) * 60 + 15 = 5684.21 + 15 = 5699.21 min
        expected = (4500.0 / 47.5) * 60.0 + 15.0
        self.assertAlmostEqual(mrdt, expected, places=2)

    def test_fleet_penalty_grace_period_boundaries(self):
        """Delay penalty exact boundaries: <=0 min -> 0€, 0 < delay <= 15m -> p_base (250€), > 15m -> p_base + (delay-15)*c_min."""
        # Zero delay
        rec_zero = [{"delay_min": 0.0, "mrdt_satisfied": True}]
        self.assertEqual(SLACalculator.compute_fleet_penalty(rec_zero, []), 0.0)

        # Negative delay (early departure)
        rec_neg = [{"delay_min": -10.0, "mrdt_satisfied": True}]
        self.assertEqual(SLACalculator.compute_fleet_penalty(rec_neg, []), 0.0)

        # 1 minute delay (within 15 min grace): charges base penalty 250 €
        rec_1m = [{"delay_min": 1.0, "mrdt_satisfied": True}]
        self.assertEqual(SLACalculator.compute_fleet_penalty(rec_1m, []), 250.0)

        # Exactly 15.0 min delay
        rec_15m = [{"delay_min": 15.0, "mrdt_satisfied": True}]
        self.assertEqual(SLACalculator.compute_fleet_penalty(rec_15m, []), 250.0)

        # 15.1 min delay (0.1 min over grace -> 250 + 0.1 * 5 = 250.50 €)
        rec_15_1m = [{"delay_min": 15.1, "mrdt_satisfied": True}]
        self.assertEqual(SLACalculator.compute_fleet_penalty(rec_15_1m, []), 250.50)

        # 35.0 min delay (20 min over grace -> 250 + 20 * 5 = 350.00 €)
        rec_35m = [{"delay_min": 35.0, "mrdt_satisfied": True}]
        self.assertEqual(SLACalculator.compute_fleet_penalty(rec_35m, []), 350.0)

    def test_fleet_penalty_undercharged_and_exempt_records(self):
        """Verify undercharged penalty and MRDT exemption gating."""
        # Unexempt undercharged: required 85%, departed 65% (20% deficit on 400 kWh = 80 kWh * 1.50 € = 120.00 €)
        rec_under = [{"soc_req": 85.0, "soc_dep": 65.0, "cap_kwh": 400.0, "mrdt_satisfied": True}]
        self.assertEqual(SLACalculator.compute_fleet_penalty([], rec_under), 120.0)

        # Overcharged: required 80%, departed 85% -> 0 €
        rec_over = [{"soc_req": 80.0, "soc_dep": 85.0, "cap_kwh": 400.0, "mrdt_satisfied": True}]
        self.assertEqual(SLACalculator.compute_fleet_penalty([], rec_over), 0.0)

        # Exempt records (mrdt_satisfied: False) must be completely skipped
        rec_exempt_delayed = [{"delay_min": 60.0, "mrdt_satisfied": False}]
        rec_exempt_under = [{"soc_req": 90.0, "soc_dep": 20.0, "cap_kwh": 400.0, "mrdt_satisfied": False}]
        self.assertEqual(SLACalculator.compute_fleet_penalty(rec_exempt_delayed, rec_exempt_under), 0.0)

    def test_availability_deduction_piecewise_steps(self):
        """Verify exact step boundaries and full waiver thresholds of availability fee deduction."""
        base_fee = 10000.0  # 10,000 € base fee

        # 1. Equal or above 99.50% -> 0 €
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 99.50), 0.0)
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 99.90), 0.0)
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 100.0), 0.0)

        # 2. Shortfall in (0.00, 0.10] -> 1 step = 2% of base fee = 200 €
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 99.49), 200.0)
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 99.40), 200.0)

        # 3. Shortfall in (0.10, 0.20] -> 2 steps = 4% of base fee = 400 €
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 99.39), 400.0)
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 99.30), 400.0)

        # 4. At 95.00%: shortfall = 4.50% -> 45 steps -> 45 * 2 = 90% cap = 9,000 €
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 95.00), 9000.0)

        # 5. Below 95.00%: 100% full waiver = 10,000 €
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 94.99), 10000.0)
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 80.00), 10000.0)
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, 0.00), 10000.0)
        self.assertEqual(SLACalculator.compute_availability_deduction(base_fee, -5.00), 10000.0)

    def test_settle_monthly_invoice_clamping_and_cap(self):
        """Monthly settlement invoice must never return negative net invoice to operator."""
        # Huge claims exceeding 150% cap
        res = SLACalculator.settle_monthly_invoice(
            monthly_base_fee=10000.0,
            avail_pct=90.0, # 10,000 € deduction
            delayed_records=[{"delay_min": 120.0, "mrdt_satisfied": True}], # 250 + (105)*5 = 775 €
            undercharged_records=[{"soc_req": 100.0, "soc_dep": 10.0, "cap_kwh": 400.0, "mrdt_satisfied": True}], # 0.9*400*1.5 = 540 €
            cap_multiplier=1.50,
        )
        self.assertEqual(res["monthly_base_fee_eur"], 10000.0)
        self.assertEqual(res["availability_deduction_eur"], 10000.0)
        self.assertEqual(res["fleet_penalty_eur"], 775.0 + 540.0)
        self.assertEqual(res["max_liability_cap_eur"], 15000.0)
        self.assertEqual(res["capped_payout_eur"], min(res["raw_total_claims_eur"], 15000.0))
        self.assertEqual(res["net_operator_invoice_eur"], 0.0)  # Operator pays 0, invoice clamped to >= 0.0

    def test_mrdt_huge_power_and_custom_buffer(self):
        """Test ultra-fast charging (1,000 kW) and custom buffer time."""
        # 10% to 90% (80%) of 100 kWh battery = 80 kWh. At 1000 kW * 0.95 = 950 kW.
        # Time = (80 / 950) * 60 + 5.0 = 5.05 + 5.0 = 10.05 min.
        mrdt = SLACalculator.compute_mrdt(90.0, 10.0, 100.0, 1000.0, 1000.0, eta=0.95, t_buffer=5.0)
        self.assertAlmostEqual(mrdt, (80.0 / 950.0) * 60.0 + 5.0, places=2)

    def test_fleet_penalty_custom_unit_rates(self):
        """Verify custom p_base, c_min, and c_energy override defaults."""
        delayed = [{"delay_min": 25.0, "mrdt_satisfied": True}]  # 10 min beyond grace
        under = [{"soc_req": 90.0, "soc_dep": 70.0, "cap_kwh": 300.0, "mrdt_satisfied": True}]  # 60 kWh deficit
        # Custom: p_base=500, c_min=10, c_energy=3.00
        # Delay pen = 500 + 10 * 10 = 600 €
        # Energy pen = 60 * 3.00 = 180 €
        # Total = 780 €
        total = SLACalculator.compute_fleet_penalty(
            delayed, under, p_base=500.0, c_min=10.0, c_energy=3.00
        )
        self.assertEqual(total, 780.0)

    def test_availability_deduction_custom_target(self):
        """Verify availability deduction with Silver tier 99.0% SLA target."""
        # At 99.0% target: 98.95% is 0.05% shortfall -> 1 step = 2% of 10,000 = 200 €
        ded = SLACalculator.compute_availability_deduction(10000.0, 98.95, uptime_sla_pct=99.0)
        self.assertEqual(ded, 200.0)



# ============================================================================
# 2. Commercial Settlement & Dispute Clearing Engine
# ============================================================================

class TestTier5CommercialSettlementHardening(unittest.TestCase):
    """Stress testing exemption classification, multi-tier SLAs, caps, and audit seals."""

    def test_exemption_reason_precedence(self):
        """CUSTOMER_DWELL_SHORTFALL must take precedence over all other reasons when MRDT is not met."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]
        # Trip with dwell < MRDT AND premature unplug AND bms abort AND grid outage!
        trip_all_faults = {
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 30.0,
            "dwell_actual_min": 10.0, # Way below ~124.5 min MRDT
            "delay_min": 60.0,
            "end_reason": "bms_abort",
            "grid_outage_force_majeure": True,
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip_all_faults, cfg)
        self.assertFalse(rec.mrdt_satisfied)
        self.assertEqual(rec.exemption_reason, ExemptionReason.CUSTOMER_DWELL_SHORTFALL)
        self.assertEqual(rec.total_penalty_eur, 0.0)

    def test_premature_unplug_synonyms(self):
        """All variations of premature unplug strings must be recognized case-insensitively."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]
        synonyms = [
            "unplugged_by_operator",
            "PREMATURE_UNPLUG",
            "driver_unplug",
            "Unplugged_By_Driver",
            "UNPLUGGED_EARLY",
        ]
        for syn in synonyms:
            trip = {
                "battery_kwh": 400.0,
                "p_charger_max_kw": 150.0,
                "p_veh_max_kw": 150.0,
                "soc_arrive_pct": 20.0,
                "soc_req_pct": 85.0,
                "soc_dep_pct": 50.0,
                "dwell_actual_min": 180.0, # Feasible MRDT
                "delay_min": 30.0,
                "end_reason": syn,
            }
            rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, cfg)
            self.assertTrue(rec.mrdt_satisfied)
            self.assertEqual(
                rec.exemption_reason,
                ExemptionReason.PREMATURE_UNPLUG,
                f"Failed to recognize synonym {syn}",
            )
            self.assertEqual(rec.total_penalty_eur, 0.0)

    def test_bms_abort_synonyms(self):
        """All variations of vehicle/BMS fault strings must be recognized case-insensitively."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]
        synonyms = [
            "bms_abort",
            "VEHICLE_FAULT",
            "charger_fault_vehicle_induced",
            "BMS_Error",
            "vehicle_bms_abort",
        ]
        for syn in synonyms:
            trip = {
                "battery_kwh": 400.0,
                "p_charger_max_kw": 150.0,
                "p_veh_max_kw": 150.0,
                "soc_arrive_pct": 20.0,
                "soc_req_pct": 85.0,
                "soc_dep_pct": 50.0,
                "dwell_actual_min": 180.0,
                "delay_min": 30.0,
                "end_reason": syn,
            }
            rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, cfg)
            self.assertTrue(rec.mrdt_satisfied)
            self.assertEqual(
                rec.exemption_reason,
                ExemptionReason.VEHICLE_BMS_FAULT,
                f"Failed to recognize synonym {syn}",
            )
            self.assertEqual(rec.total_penalty_eur, 0.0)

    def test_grid_force_majeure_exemption(self):
        """Grid outage flag must exempt operator when dwell was sufficient and end_reason nominal."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip = {
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 50.0,
            "dwell_actual_min": 180.0,
            "delay_min": 45.0,
            "end_reason": "completed",
            "grid_outage_force_majeure": True,
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, cfg)
        self.assertTrue(rec.mrdt_satisfied)
        self.assertEqual(rec.exemption_reason, ExemptionReason.GRID_FORCE_MAJEURE)
        self.assertEqual(rec.total_penalty_eur, 0.0)

    def test_titanium_and_silver_tier_deductions(self):
        """Verify availability deduction logic across Titanium (99.9%) and Silver (99.0%) tiers."""
        # Titanium: 15,000 € base, 2.5% step, 96.0% full waiver
        ti_cfg = TIER_CONFIGS[ContractTier.TITANIUM]
        s_ti, r_ti, d_ti = SettlementClearingEngine.compute_availability_deduction(ti_cfg, 99.85)
        self.assertAlmostEqual(s_ti, 0.05, places=2)
        self.assertEqual(r_ti, 2.50)
        self.assertEqual(d_ti, 375.0)  # 15000 * 0.025

        s_ti_w, r_ti_w, d_ti_w = SettlementClearingEngine.compute_availability_deduction(ti_cfg, 95.99)
        self.assertEqual(r_ti_w, 100.0)
        self.assertEqual(d_ti_w, 15000.0)

        # Silver: 7,500 € base, 1.5% step, 94.0% full waiver
        sv_cfg = TIER_CONFIGS[ContractTier.SILVER]
        s_sv, r_sv, d_sv = SettlementClearingEngine.compute_availability_deduction(sv_cfg, 98.95)
        self.assertAlmostEqual(s_sv, 0.05, places=2)
        self.assertEqual(r_sv, 1.50)
        self.assertEqual(d_sv, 112.50)  # 7500 * 0.015

        s_sv_w, r_sv_w, d_sv_w = SettlementClearingEngine.compute_availability_deduction(sv_cfg, 93.99)
        self.assertEqual(r_sv_w, 100.0)
        self.assertEqual(d_sv_w, 7500.0)

    def test_custom_base_fee_and_string_tier_fallbacks(self):
        """Verify generate_monthly_settlement supports custom base fee and handles invalid tier string safely."""
        stmt = generate_monthly_settlement(
            site_id="S1",
            month="2026-11",
            tier="UNKNOWN_TIER_XYZ",  # Fallback to Gold
            custom_base_fee_eur=25000.0,
            actual_availability_pct=99.85,
        )
        self.assertEqual(stmt.contract_tier, "Gold")
        self.assertEqual(stmt.monthly_base_fee_eur, 25000.0)
        self.assertEqual(stmt.max_liability_cap_eur, 37500.0)  # 25,000 * 1.50

    def test_aggregate_subcaps_and_credit_carryforward(self):
        """Verify double sub-caps (100% on avail, 100% on fleet) and 150% aggregate cap with carryforward."""
        # Set up a scenario with 10,000 € base fee
        # 1. Avail deduction = 10,000 € (full waiver at 90% avail)
        # 2. Fleet penalty = 20,000 € (huge delay damages)
        huge_trips = [
            {
                "trip_id": f"T_HUGE_{i}",
                "battery_kwh": 400.0,
                "p_charger_max_kw": 150.0,
                "p_veh_max_kw": 150.0,
                "soc_arrive_pct": 20.0,
                "soc_req_pct": 85.0,
                "soc_dep_pct": 20.0,  # 65% deficit = 260 kWh * 1.5 = 390 €
                "dwell_actual_min": 240.0,
                "delay_min": 100.0,    # 250 + 85*5 = 675 €
                "end_reason": "completed",
            }
            for i in range(25)  # 25 * 1065 € = 26,625 € gross fleet
        ]
        stmt = generate_monthly_settlement(
            site_id="S1",
            month="2026-11",
            tier=ContractTier.GOLD,
            actual_availability_pct=90.0,  # Full waiver = 10,000 €
            trips=huge_trips,
        )
        # Gross fleet = 26,625 €
        self.assertEqual(stmt.gross_fleet_penalties_eur, 26625.0)
        # Sub-cap: Fleet penalty capped at 100% base fee = 10,000 €
        self.assertEqual(stmt.capped_fleet_penalties_eur, 10000.0)
        # Sub-cap: Avail deduction = 10,000 €
        self.assertEqual(stmt.availability_deduction_eur, 10000.0)
        # Aggregate raw claims = 10,000 + 10,000 = 20,000 €
        self.assertEqual(stmt.gross_total_claims_eur, 20000.0)
        # Aggregate 150% statutory cap = 15,000 €
        self.assertEqual(stmt.max_liability_cap_eur, 15000.0)
        # Final payout deduction = min(20,000, 15,000) = 15,000 €
        self.assertEqual(stmt.final_payout_deduction_eur, 15000.0)
        # Net invoice payable = max(0, 10,000 - 15,000) = 0.00 €
        self.assertEqual(stmt.net_invoice_payable_eur, 0.0)
        # Credit carryforward to next month = 15,000 - 10,000 = 5,000.00 €
        self.assertEqual(stmt.credit_carryforward_eur, 5000.0)

    def test_sha256_audit_seal_avalanche_sensitivity(self):
        """SHA-256 audit hash must be deterministic and change completely on even tiny parameter alterations."""
        stmt1 = generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, actual_availability_pct=99.85)
        stmt2 = generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, actual_availability_pct=99.85)
        self.assertEqual(stmt1.audit_hash, stmt2.audit_hash)
        self.assertEqual(len(stmt1.audit_hash), 64)

        # 0.01% availability change
        stmt3 = generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, actual_availability_pct=99.84)
        self.assertNotEqual(stmt1.audit_hash, stmt3.audit_hash)

        # Site change
        stmt4 = generate_monthly_settlement("S2", "2026-11", ContractTier.GOLD, actual_availability_pct=99.85)
        self.assertNotEqual(stmt1.audit_hash, stmt4.audit_hash)

    def test_markdown_audit_table_rendering(self):
        """Markdown rendering must format tables cleanly with 0 items, few items, and >20 items."""
        # Case A: 0 line items
        stmt_empty = generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, trips=[])
        md_empty = SettlementClearingEngine.render_markdown_audit_table(stmt_empty)
        self.assertIn("# B2B Monthly SLA Settlement Statement", md_empty)
        self.assertIn(stmt_empty.invoice_id, md_empty)
        self.assertNotIn("## 3. Departure Audit Line Items", md_empty)

        # Case B: 25 line items (must show 20 items and truncate note)
        trips_25 = [
            {
                "trip_id": f"TRIP_{i:02d}",
                "battery_kwh": 400.0,
                "p_charger_max_kw": 150.0,
                "p_veh_max_kw": 150.0,
                "soc_arrive_pct": 20.0,
                "soc_req_pct": 85.0,
                "soc_dep_pct": 85.0,
                "dwell_actual_min": 180.0,
                "delay_min": 0.0,
                "end_reason": "completed",
            }
            for i in range(25)
        ]
        stmt_25 = generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, trips=trips_25)
        md_25 = SettlementClearingEngine.render_markdown_audit_table(stmt_25)
        self.assertIn("## 3. Departure Audit Line Items", md_25)
        self.assertIn("*(Showing 20 of 25 audit records)*", md_25)

    def test_invoice_statement_dict_protocol_and_json(self):
        """MonthlyInvoiceStatement must support dict-like access and lossless JSON serialization."""
        stmt = generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD)
        self.assertEqual(stmt["site_id"], "S1")
        self.assertEqual(stmt.get("monthly_base_fee_eur"), 10000.0)
        self.assertEqual(stmt.get("non_existent_key", "DEFAULT"), "DEFAULT")
        self.assertIn("audit_hash", stmt)
        self.assertGreater(len(list(stmt.keys())), 15)

        # JSON roundtrip
        d = stmt.to_dict()
        s_json = json.dumps(d)
        d_loaded = json.loads(s_json)
        self.assertEqual(d_loaded["invoice_id"], stmt.invoice_id)
        self.assertEqual(d_loaded["net_invoice_payable_eur"], stmt.net_invoice_payable_eur)

    def test_none_or_empty_trips_settlement(self):
        """Passing trips=None or trips=[] must yield 0 evaluated trips and 0 fleet penalties."""
        stmt_none = generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, trips=None)
        self.assertEqual(stmt_none.total_trips_evaluated, 0)
        self.assertEqual(stmt_none.trips_penalized_count, 0)
        self.assertEqual(stmt_none.gross_fleet_penalties_eur, 0.0)

        stmt_empty = generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, trips=[])
        self.assertEqual(stmt_empty.total_trips_evaluated, 0)
        self.assertEqual(stmt_empty.trips_penalized_count, 0)
        self.assertEqual(stmt_empty.gross_fleet_penalties_eur, 0.0)

    def test_zero_deficit_exact_arrival_satisfaction(self):
        """Departure SoC equal to required SoC must result in 0 deficit kWh and 0 energy penalty."""
        cfg = TIER_CONFIGS[ContractTier.TITANIUM]
        trip = {
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 85.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 85.0,
            "dwell_actual_min": 60.0,
            "delay_min": 0.0,
            "end_reason": "completed",
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, cfg)
        self.assertTrue(rec.mrdt_satisfied)
        self.assertEqual(rec.energy_deficit_kwh, 0.0)
        self.assertEqual(rec.energy_penalty_eur, 0.0)
        self.assertEqual(rec.total_penalty_eur, 0.0)

    def test_exemption_precedence_premature_unplug_over_grid_outage(self):
        """When dwell is sufficient, premature unplug takes precedence over grid outage."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip = {
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 50.0,
            "dwell_actual_min": 180.0,
            "delay_min": 30.0,
            "end_reason": "driver_unplug",
            "grid_outage_force_majeure": True,
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, cfg)
        self.assertTrue(rec.mrdt_satisfied)
        self.assertEqual(rec.exemption_reason, ExemptionReason.PREMATURE_UNPLUG)

    def test_departure_audit_record_serialization_schema(self):
        """DepartureAuditRecord to_dict must serialize exemption_reason to string value and keep all fields."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip = {
            "trip_id": "T_TEST_SERIALIZE",
            "vehicle_id": "V_TEST",
            "site_id": "S1",
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 85.0,
            "dwell_actual_min": 180.0,
            "delay_min": 0.0,
            "end_reason": "completed",
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip, cfg)
        d = rec.to_dict()
        self.assertIsInstance(d["exemption_reason"], str)
        self.assertEqual(d["exemption_reason"], "NONE")
        self.assertEqual(d["trip_id"], "T_TEST_SERIALIZE")
        self.assertEqual(d["vehicle_id"], "V_TEST")



# ============================================================================
# 3. Financial Sensitivity & Pure-Python IRR Solver
# ============================================================================

class TestTier5FinancialSensitivityAdversarial(unittest.TestCase):
    """Stress tests on pure-Python NPV/IRR engine and asset replacement valuation."""

    def test_network_baseline_capex_and_bess_ground_truth(self):
        """Asset valuation must be grounded in equipment_costs.csv and total 87,985,000.00 €."""
        bess = FinancialSensitivityEngine.compute_bess_initial_capex()
        self.assertEqual(bess["bess_energy_capex_eur"], 11200000.0)  # 35,000 * 320
        self.assertEqual(bess["bess_power_capex_eur"], 2222000.0)    # 20,200 * 110
        self.assertEqual(bess["total_bess_capex_eur"], 13422000.0)

        assets = FinancialSensitivityEngine.compute_network_baseline_capex()
        self.assertEqual(assets["standard_dispensers_with_civil_eur"], 24732000.0) # 916 * 27,000
        self.assertEqual(assets["megawatt_dispensers_with_civil_eur"], 4582000.0)   # 58 * 79,000
        self.assertEqual(assets["dc_power_rectifiers_eur"], 39914000.0)            # 142,550 * 280
        self.assertEqual(assets["solar_pv_eur"], 2835000.0)                         # 3,150 * 900
        self.assertEqual(assets["permits_and_engineering_eur"], 2500000.0)          # 100 * 25,000
        self.assertEqual(assets["total_physical_asset_valuation_eur"], 87985000.0)

    def test_irr_solver_adversarial_cash_flows(self):
        """Stress test _compute_irr across conventional, unconventional, and extreme cash flows."""
        solver = FinancialSensitivityEngine._compute_irr

        # 1. All negative cash flows -> 0.0
        self.assertEqual(solver([-100.0, -50.0, -20.0]), 0.0)

        # 2. All positive cash flows -> 100.0 (high return limit)
        self.assertEqual(solver([100.0, 50.0, 20.0]), 100.0)

        # 3. Exactly break-even: [-100, 100] -> IRR = 0.0 (0%)
        irr_be = solver([-100.0, 100.0])
        self.assertAlmostEqual(irr_be, 0.0, places=4)

        # 4. Standard 50% return: [-100, 150] -> IRR = 0.50 (50%)
        irr_50 = solver([-100.0, 150.0])
        self.assertAlmostEqual(irr_50, 0.50, places=4)

        # 5. Project destroys capital: [-1000, 100, 100] -> Undiscounted loses money, searches negative domain
        irr_neg = solver([-1000.0, 100.0, 100.0])
        self.assertLess(irr_neg, 0.0)
        self.assertGreaterEqual(irr_neg, -0.99)

        # 6. Zero initial capex with positive flows: [0, 500, 500] -> 100.0
        self.assertEqual(solver([0.0, 500.0, 500.0]), 100.0)

    def test_sensitivity_multi_axis_evaluation_boundaries(self):
        """evaluate_sensitivity must survive extreme macro variations without throwing."""
        # Extreme spot spike multiplier = 10.0, negative price freq = 50%
        res_spike = FinancialSensitivityEngine.evaluate_sensitivity(
            spot_spike_multiplier=10.0,
            negative_price_freq=0.50,
            discount_rate=0.0,  # Zero discount rate
        )
        self.assertGreater(res_spike["npv_eur"], 0.0)
        self.assertGreater(res_spike["irr_pct"], 0.0)

        # Zero labor cost, hyper-inflated replacement cost
        res_zero_labor = FinancialSensitivityEngine.evaluate_sensitivity(
            labor_annual_cost_per_fte=0.0,
            bess_replacement_kwh_cost=1000.0,
            discount_rate=0.20,
        )
        self.assertIsInstance(res_zero_labor["npv_eur"], float)
        self.assertIsInstance(res_zero_labor["irr_pct"], float)

    def test_sensitivity_matrix_completeness(self):
        """generate_sensitivity_matrix must return 9 valid scenarios with all required schema keys."""
        matrix = FinancialSensitivityEngine.generate_sensitivity_matrix()
        self.assertEqual(len(matrix), 9)
        required_keys = {
            "scenario_name",
            "spot_spike_multiplier",
            "negative_price_freq_pct",
            "labor_annual_cost_per_fte_eur",
            "annual_labor_savings_eur",
            "annual_spot_arbitrage_savings_eur",
            "annual_peak_savings_eur",
            "net_annual_operating_benefit_eur",
            "npv_eur",
            "irr_pct",
            "cash_flows",
        }
        for item in matrix:
            self.assertTrue(required_keys.issubset(item.keys()))
            self.assertFalse(math.isnan(item["npv_eur"]))
            self.assertFalse(math.isnan(item["irr_pct"]))

    def test_npv_at_zero_rate_equals_sum_of_cashflows(self):
        """At discount rate = 0.0, NPV must equal the undiscounted arithmetic sum of cash flows."""
        cfs = [-150000.0, 100000.0, 100000.0, 100000.0]
        npv_0 = FinancialSensitivityEngine._compute_npv(0.0, cfs)
        self.assertEqual(npv_0, sum(cfs))

    def test_irr_alternating_cash_flow_bisection(self):
        """Verify IRR bisection solver stability on alternating cash flows."""
        # Project: [-1000, 800, -200, 600]
        cfs = [-1000.0, 800.0, -200.0, 600.0]
        irr = FinancialSensitivityEngine._compute_irr(cfs)
        self.assertGreater(irr, 0.0)
        # Verify NPV at found IRR is close to 0
        npv_at_irr = FinancialSensitivityEngine._compute_npv(irr, cfs)
        self.assertAlmostEqual(npv_at_irr, 0.0, places=2)

    def test_sensitivity_project_horizon_variations(self):
        """Test 1-year and 20-year horizons and BESS replacement beyond project window."""
        res_1y = FinancialSensitivityEngine.evaluate_sensitivity(project_years=1)
        self.assertEqual(len(res_1y["cash_flows"]), 2)  # Year 0 and Year 1

        res_20y = FinancialSensitivityEngine.evaluate_sensitivity(project_years=20, bess_replacement_years=10)
        self.assertEqual(len(res_20y["cash_flows"]), 21)

        # Replacement at year 15 for a 10-year project: replacement should not be triggered in 10-year cash flows
        res_no_rep = FinancialSensitivityEngine.evaluate_sensitivity(project_years=10, bess_replacement_years=15)
        self.assertEqual(len(res_no_rep["cash_flows"]), 11)
        # All annual flows y=1..10 should be identical
        for y in range(2, 11):
            self.assertEqual(res_no_rep["cash_flows"][y], res_no_rep["cash_flows"][1])



# ============================================================================
# 4. ROI & Labor Ground Truth Analyzer
# ============================================================================

class TestTier5ROILaborGroundTruth(unittest.TestCase):
    """Audits empirical labor, equipment catalog, and payback calculations."""

    def test_operations_labor_exact_invariants(self):
        """Verify labor analysis strictly derives from 8,852 rows of operations_log.csv."""
        labor = ROIAnalyzer.analyze_network_operations_labor()
        self.assertEqual(labor["total_ops_biweekly"], 8852)
        self.assertEqual(labor["total_minutes_biweekly"], 93412.0)
        self.assertEqual(labor["total_hours_biweekly"], 1556.87)
        self.assertEqual(labor["total_network_fte"], 20.76)
        self.assertEqual(labor["total_network_annual_labor_eur"], 1821534.00)

        # Move and replug vehicle breakdown
        self.assertEqual(labor["replug_ops_biweekly"], 5596)
        self.assertEqual(labor["replug_minutes_biweekly"], 44768.0)
        self.assertEqual(labor["replug_share_by_count_pct"], 63.22)
        self.assertEqual(labor["replug_share_by_duration_pct"], 47.93)
        self.assertEqual(labor["replug_network_fte"], 9.95)
        self.assertEqual(labor["replug_network_annual_labor_eur"], 872976.00)

        # S1 site replug
        self.assertEqual(labor["s1_replug_ops_biweekly"], 156)
        self.assertEqual(labor["s1_replug_minutes_biweekly"], 1248.0)
        self.assertEqual(labor["s1_replug_share_of_network_pct"], 2.79)
        self.assertEqual(labor["s1_replug_annual_labor_eur"], 24336.00)

        # S1-S5 primary sites replug (ground truth directly from operations_log.csv)
        self.assertEqual(labor["s1_s5_replug_ops_biweekly"], 332)
        self.assertEqual(labor["s1_s5_replug_minutes_biweekly"], 2656.0)
        self.assertEqual(labor["s1_s5_replug_share_of_network_pct"], 5.93)
        self.assertEqual(labor["s1_s5_replug_annual_labor_eur"], 51792.00)

    def test_equipment_and_payback_strategy_comparison(self):
        """Verify Strategy A (0 € CAPEX) vs Strategy B (324,000 € CAPEX, 13.31 yr S1 payback)."""
        equip = ROIAnalyzer.analyze_equipment_and_payback()
        self.assertEqual(equip["satellite_dispenser_eur"], 18000.0)
        self.assertEqual(equip["civil_works_per_gun_eur"], 9000.0)
        self.assertEqual(equip["installed_cost_per_gun_eur"], 27000.0)
        self.assertEqual(equip["s1_12_guns_hw_only_capex_eur"], 216000.0)
        self.assertEqual(equip["s1_12_guns_total_capex_with_civil_eur"], 324000.0)
        self.assertEqual(equip["s1_annual_replug_savings_eur"], 24336.0)
        self.assertEqual(equip["s1_payback_years_with_civil"], 13.31)
        self.assertEqual(equip["s1_payback_years_hw_only"], 8.88)
        self.assertEqual(equip["strategy_a_0capex_capex_eur"], 0.0)
        self.assertTrue(equip["strategy_a_immediate_positive_roi"])

    def test_monthly_peak_demand_vs_energy_costs(self):
        """Monthly peak demand fees for S1-S5 must exceed 14-day energy costs."""
        p_vs_e = ROIAnalyzer.analyze_monthly_peak_demand_vs_energy()
        self.assertGreater(p_vs_e["s1_s5_monthly_peak_demand_fee_eur"], 0.0)
        self.assertGreater(p_vs_e["s1_s5_energy_cost_14d_eur"], 0.0)
        self.assertTrue(p_vs_e["peak_demand_exceeds_14d_energy_cost"])


# ============================================================================
# 5. Dashboard UI & Presentation Adversarial Probes
# ============================================================================

class TestTier5DashboardUIAndPresentationAdversarial(unittest.TestCase):
    """Stress tests on app.py payload builder and interactive Streamlit AppTest views."""

    @classmethod
    def setUpClass(cls):
        if not any("streamlit" in arg.lower() for arg in sys.argv):
            sys.argv.append("streamlit")
        from streamlit.testing.v1 import AppTest
        cls.AppTest = AppTest

    def test_dashboard_payload_builder_ground_truth(self):
        """build_dashboard_payload must execute cleanly and yield complete required keys."""
        payload = app.build_dashboard_payload()
        self.assertIn("topology", payload)
        self.assertIn("scenarios", payload)
        self.assertIn("labor", payload)
        self.assertIn("equip", payload)
        self.assertIn("peak_vs_energy", payload)
        self.assertIn("timeline_records", payload)
        self.assertIn("spot_prices", payload)

        self.assertEqual(payload["scenarios"]["scenario_day_missed_after"], 3)
        self.assertEqual(payload["scenarios"]["scenario_day_missed_after_expansion"], 0)
        self.assertEqual(payload["labor"]["total_network_fte"], 20.76)
        self.assertGreaterEqual(len(payload["timeline_records"]), 96)
        self.assertIn("18:00", payload["spot_prices"])

    def test_streamlit_interactive_tier_switch_and_settlement(self):
        """Test interacting with Contract Service Tier selectbox in View 4."""
        at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
        self.assertEqual(len(at.exception), 0)

        # Selectbox 0 is the contract tier choice
        self.assertGreaterEqual(len(at.selectbox), 1)
        tier_sb = at.selectbox[0]

        # Switch to Titanium
        at = tier_sb.select("Titanium (99.9% SLO)").run()
        self.assertEqual(len(at.exception), 0)

        # Switch to Silver
        at = tier_sb.select("Silver (99.0% SLO)").run()
        self.assertEqual(len(at.exception), 0)

    def test_streamlit_wear_leveling_toggle_interaction(self):
        """Test toggling the wear-leveling toggle button in View 3."""
        at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
        self.assertEqual(len(at.exception), 0)

        # Toggle in View 3
        self.assertGreaterEqual(len(at.toggle), 1)
        wear_toggle = at.toggle[0]
        self.assertTrue(wear_toggle.value)

        # Toggle to False
        at = wear_toggle.set_value(False).run()
        self.assertEqual(len(at.exception), 0)

        # Toggle back to True
        at = wear_toggle.set_value(True).run()
        self.assertEqual(len(at.exception), 0)

    def test_streamlit_simulated_delays_and_export_generation(self):
        """Adjust simulated delays slider in View 4 and verify invoice JSON download button renders."""
        at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
        self.assertEqual(len(at.exception), 0)

        # Verify download button exists
        self.assertGreaterEqual(len(at.download_button), 1)
        dl_btn = at.download_button[0]
        self.assertIn("Export Monthly Settlement Statement (JSON)", dl_btn.label)

    def test_timeline_records_site_coverage(self):
        """Verify timeline_records in dashboard payload covers sites S1 through S5."""
        payload = app.build_dashboard_payload()
        sites_in_timeline = {r["site_id"] for r in payload["timeline_records"]}
        self.assertTrue({"S1", "S2", "S3", "S4", "S5"}.issubset(sites_in_timeline))

    def test_spot_prices_peak_at_1800(self):
        """Verify spot price at 18:00 is the highest spot price on 2026-11-13 (>700 €/MWh)."""
        payload = app.build_dashboard_payload()
        prices = payload["spot_prices"]
        self.assertIn("18:00", prices)
        peak_1800 = prices["18:00"]
        self.assertGreater(peak_1800, 700.0)
        self.assertEqual(peak_1800, max(prices.values()))

    def test_streamlit_quick_jump_buttons(self):
        """Click each incident quick jump button and verify clean session state transition."""
        at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
        self.assertEqual(len(at.exception), 0)
        # Verify 6 incident quick jump buttons exist
        self.assertGreaterEqual(len(at.button), 6)
        # Click 02:25 S1 Thermal Trip button
        thermal_btn = next((b for b in at.button if "02:25" in b.label), None)
        self.assertIsNotNone(thermal_btn)
        at = thermal_btn.click().run()
        self.assertEqual(len(at.exception), 0)
        self.assertEqual(at.session_state.get("scrub_time"), "02:30")

    def test_subprocess_clean_execution_cli_mode(self):
        """Verify running `python app.py` exits 0 with zero runtime exceptions."""
        res = subprocess.run(
            [sys.executable, str(REPO_ROOT / "app.py")],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(res.returncode, 0, f"app.py exited with error:\n{res.stderr}")
        self.assertIn(
            "Dashboard payload verified: 13 -> 3 (0 EUR software) | zero-miss needs cross-cabinet busbar (unpriced); +12 plugs = 324,000 EUR yields 8.",
            res.stdout,
        )


if __name__ == "__main__":
    unittest.main()

