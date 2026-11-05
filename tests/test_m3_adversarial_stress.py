"""
tests/test_m3_adversarial_stress.py

Adversarial Empirical Stress Testing Suite for:
1. Commercial Settlement & Dispute Clearing Engine (settlement_clearing.py)
2. Financial Sensitivity & Pure Python NPV/IRR Engine (sensitivity_analyzer.py)

Authored by M3 Challenger 1.
"""

import hashlib
import time
import pytest
from typing import Dict, Any

from src.commercial.settlement_clearing import (
    ContractTier,
    ExemptionReason,
    TIER_CONFIGS,
    SettlementClearingEngine,
    MonthlyInvoiceStatement,
    DepartureAuditRecord,
    generate_monthly_settlement,
)
from src.commercial.sensitivity_analyzer import (
    FinancialSensitivityEngine,
    OFFICIAL_EQUIPMENT_COSTS,
)


# ============================================================================
# 1. Commercial Settlement Adversarial Stress Tests
# ============================================================================

class TestCommercialSettlementAdversarial:
    """Adversarial boundary and edge testing for commercial settlement clearing."""

    def test_settlement_zero_and_negative_dwell(self):
        """Zero and negative dwell times must trigger CUSTOMER_DWELL_SHORTFALL without crashing."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]

        # Zero dwell
        trip_zero = {
            "trip_id": "T_ZERO_01",
            "dwell_actual_min": 0.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 80.0,
            "battery_kwh": 400.0,
            "delay_min": 60.0,
            "soc_dep_pct": 20.0,
        }
        rec_zero = SettlementClearingEngine.evaluate_mrdt_and_trip(trip_zero, cfg)
        assert not rec_zero.mrdt_satisfied
        assert rec_zero.exemption_reason == ExemptionReason.CUSTOMER_DWELL_SHORTFALL
        assert rec_zero.delay_penalty_eur == 0.0
        assert rec_zero.energy_penalty_eur == 0.0
        assert rec_zero.total_penalty_eur == 0.0

        # Negative dwell
        trip_neg = {
            "trip_id": "T_NEG_01",
            "dwell_actual_min": -50.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 80.0,
            "battery_kwh": 400.0,
            "delay_min": 60.0,
            "soc_dep_pct": 20.0,
        }
        rec_neg = SettlementClearingEngine.evaluate_mrdt_and_trip(trip_neg, cfg)
        assert not rec_neg.mrdt_satisfied
        assert rec_neg.exemption_reason == ExemptionReason.CUSTOMER_DWELL_SHORTFALL
        assert rec_neg.total_penalty_eur == 0.0

    def test_settlement_massive_dwell(self):
        """Massive dwell (10,000 min) must satisfy MRDT and compute penalties correctly without overflow."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip_massive = {
            "trip_id": "T_MASSIVE_01",
            "dwell_actual_min": 10000.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 80.0,
            "soc_dep_pct": 70.0,  # 10% deficit = 40 kWh
            "battery_kwh": 400.0,
            "delay_min": 45.0,     # 45 min delay -> 30 min beyond 15m grace
            "end_reason": "completed",
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip_massive, cfg)
        assert rec.mrdt_satisfied
        assert rec.exemption_reason == ExemptionReason.NONE
        # Delay penalty: p_base (250) + (45-15)*5 = 400 €
        assert rec.delay_penalty_eur == 400.0
        # Energy penalty: 40 kWh * 1.50 €/kWh = 60 €
        assert rec.energy_penalty_eur == 60.0
        assert rec.total_penalty_eur == 460.0

    def test_settlement_extreme_demand_tiny_dwell(self):
        """Massive battery demand with short dwell (500 kWh in 10 min) must be safely exempted."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip_extreme = {
            "trip_id": "T_EXTREME_01",
            "battery_kwh": 1000.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 70.0,  # 500 kWh needed
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "dwell_actual_min": 10.0,
            "delay_min": 120.0,
            "soc_dep_pct": 20.0,
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip_extreme, cfg)
        assert not rec.mrdt_satisfied
        assert rec.exemption_reason == ExemptionReason.CUSTOMER_DWELL_SHORTFALL
        assert rec.total_penalty_eur == 0.0

    def test_settlement_zero_hardware_power_infinite_mrdt(self):
        """Zero charger or vehicle power must yield infinite MRDT and safe exemption without ZeroDivisionError."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]
        trip_zero_p = {
            "trip_id": "T_ZERO_KW",
            "battery_kwh": 400.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 80.0,
            "p_charger_max_kw": 0.0,
            "p_veh_max_kw": 150.0,
            "dwell_actual_min": 600.0,
        }
        rec = SettlementClearingEngine.evaluate_mrdt_and_trip(trip_zero_p, cfg)
        assert not rec.mrdt_satisfied
        assert rec.exemption_reason == ExemptionReason.CUSTOMER_DWELL_SHORTFALL
        assert rec.mrdt_min == float("inf")

    def test_settlement_exact_mathematical_boundary_dwell(self):
        """Verify behavior at exact rounded (2 decimals) MRDT boundary."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]
        # Rounded MRDT: round((50 / 100 * 1000) / (150 * 0.95) * 60 + 15, 2) = 225.53 min
        needed_kwh = 500.0
        eff_kw = 150.0 * 0.95
        exact_mrdt = round(needed_kwh / eff_kw * 60.0 + 15.0, 2)

        # MRDT - 0.001 min: must NOT satisfy
        r_below = SettlementClearingEngine.evaluate_mrdt_and_trip({
            "battery_kwh": 1000.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 70.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "dwell_actual_min": exact_mrdt - 0.001,
            "delay_min": 30.0,
        }, cfg)
        assert not r_below.mrdt_satisfied
        assert r_below.exemption_reason == ExemptionReason.CUSTOMER_DWELL_SHORTFALL
        assert r_below.total_penalty_eur == 0.0

        # Exact MRDT: must satisfy
        r_exact = SettlementClearingEngine.evaluate_mrdt_and_trip({
            "battery_kwh": 1000.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 70.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "dwell_actual_min": exact_mrdt,
            "delay_min": 30.0,
            "soc_dep_pct": 70.0,
        }, cfg)
        assert r_exact.mrdt_satisfied
        assert r_exact.exemption_reason == ExemptionReason.NONE
        assert r_exact.delay_penalty_eur > 0.0

        # MRDT + 0.001 min: must satisfy
        r_above = SettlementClearingEngine.evaluate_mrdt_and_trip({
            "battery_kwh": 1000.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 70.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "dwell_actual_min": exact_mrdt + 0.001,
            "delay_min": 30.0,
            "soc_dep_pct": 70.0,
        }, cfg)
        assert r_above.mrdt_satisfied
        assert r_above.exemption_reason == ExemptionReason.NONE

    def test_settlement_massive_claim_spikes_and_liability_cap(self):
        """Massive claims (> €1,000,000) must be capped at 150% base fee and maintain net invoice >= 0.0."""
        for tier in [ContractTier.TITANIUM, ContractTier.GOLD, ContractTier.SILVER]:
            cfg = TIER_CONFIGS[tier]
            trips = [
                {
                    "trip_id": f"TRIP_{i:04d}",
                    "dwell_actual_min": 500.0,
                    "soc_arrive_pct": 10.0,
                    "soc_req_pct": 90.0,
                    "soc_dep_pct": 10.0,
                    "battery_kwh": 500.0,
                    "delay_min": 1000.0,
                    "end_reason": "completed",
                }
                for i in range(500)
            ]
            stmt = SettlementClearingEngine.generate_monthly_settlement(
                site_id="S1",
                month="2026-11",
                tier=tier,
                actual_availability_pct=90.0,
                trips=trips,
            )
            # Verify fleet penalties capped at base fee
            assert stmt.capped_fleet_penalties_eur == stmt.monthly_base_fee_eur
            # Verify availability deduction capped at base fee
            assert stmt.availability_deduction_eur == stmt.monthly_base_fee_eur
            # Verify gross claims = 200% base fee before aggregate cap
            assert stmt.gross_total_claims_eur == stmt.monthly_base_fee_eur * 2.0
            # Verify strictly capped at 150%
            assert stmt.max_liability_cap_eur == stmt.monthly_base_fee_eur * 1.50
            assert stmt.final_payout_deduction_eur == stmt.monthly_base_fee_eur * 1.50
            # Verify strictly non-negative net invoice payable
            assert stmt.net_invoice_payable_eur >= 0.00
            assert stmt.net_invoice_payable_eur == 0.00
            # Verify excess credit carryforward
            assert stmt.credit_carryforward_eur == stmt.monthly_base_fee_eur * 0.50

    def test_settlement_tampered_payload_sha256_detection(self):
        """Any tampering with invoice fields must trigger SHA-256 hash validation failure."""
        stmt = SettlementClearingEngine.generate_monthly_settlement(
            site_id="S1",
            month="2026-11",
            tier=ContractTier.GOLD,
            actual_availability_pct=98.5,
        )

        def verify_seal(s: MonthlyInvoiceStatement) -> bool:
            payload = f"{s.site_id}|{s.billing_period}|{s.contract_tier}|{s.monthly_base_fee_eur:.2f}|{s.actual_availability_pct:.4f}|{s.final_payout_deduction_eur:.2f}|{s.net_invoice_payable_eur:.2f}"
            expected = hashlib.sha256(payload.encode("utf-8")).hexdigest()
            return expected == s.audit_hash

        assert verify_seal(stmt)

        # Adversary tamper 1: decrease net invoice payable
        t1 = SettlementClearingEngine.generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, actual_availability_pct=98.5)
        t1.net_invoice_payable_eur = 0.0
        assert not verify_seal(t1)

        # Adversary tamper 2: increase final payout
        t2 = SettlementClearingEngine.generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, actual_availability_pct=98.5)
        t2.final_payout_deduction_eur += 1000.0
        assert not verify_seal(t2)

        # Adversary tamper 3: forge site_id
        t3 = SettlementClearingEngine.generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, actual_availability_pct=98.5)
        t3.site_id = "S2"
        assert not verify_seal(t3)

        # Adversary tamper 4: alter reported availability
        t4 = SettlementClearingEngine.generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, actual_availability_pct=98.5)
        t4.actual_availability_pct = 99.9
        assert not verify_seal(t4)

        # Adversary tamper 5: forge hash string
        t5 = SettlementClearingEngine.generate_monthly_settlement("S1", "2026-11", ContractTier.GOLD, actual_availability_pct=98.5)
        t5.audit_hash = "0" * 64
        assert not verify_seal(t5)

    def test_settlement_exemption_coverage(self):
        """Verify all standard exemption aliases waive liquidated damages completely."""
        cfg = TIER_CONFIGS[ContractTier.GOLD]

        premature_reasons = ["unplugged_by_operator", "premature_unplug", "driver_unplug", "unplugged_by_driver", "unplugged_early"]
        for reason in premature_reasons:
            rec = SettlementClearingEngine.evaluate_mrdt_and_trip({
                "dwell_actual_min": 180.0,
                "delay_min": 45.0,
                "soc_dep_pct": 30.0,
                "end_reason": reason,
            }, cfg)
            assert rec.exemption_reason == ExemptionReason.PREMATURE_UNPLUG
            assert rec.total_penalty_eur == 0.0

        bms_reasons = ["bms_abort", "vehicle_fault", "charger_fault_vehicle_induced", "bms_error", "vehicle_bms_abort"]
        for reason in bms_reasons:
            rec = SettlementClearingEngine.evaluate_mrdt_and_trip({
                "dwell_actual_min": 180.0,
                "delay_min": 45.0,
                "soc_dep_pct": 30.0,
                "end_reason": reason,
            }, cfg)
            assert rec.exemption_reason == ExemptionReason.VEHICLE_BMS_FAULT
            assert rec.total_penalty_eur == 0.0

        # Grid force majeure
        rec_grid = SettlementClearingEngine.evaluate_mrdt_and_trip({
            "dwell_actual_min": 180.0,
            "delay_min": 45.0,
            "soc_dep_pct": 30.0,
            "grid_outage_force_majeure": True,
        }, cfg)
        assert rec_grid.exemption_reason == ExemptionReason.GRID_FORCE_MAJEURE
        assert rec_grid.total_penalty_eur == 0.0


# ============================================================================
# 2. Financial Sensitivity Engine Adversarial Stress Tests
# ============================================================================

class TestFinancialSensitivityAdversarial:
    """Adversarial stress testing for financial sensitivity and NPV/IRR models."""

    def test_sensitivity_extreme_pricing_scenarios(self):
        """Extreme negative pricing (50%, 100%) and massive price spikes (200x) must compute cleanly."""
        # 50% negative hours
        res_50 = FinancialSensitivityEngine.evaluate_sensitivity(negative_price_freq=0.50)
        assert res_50["npv_eur"] > 30000000.0
        assert res_50["annual_spot_arbitrage_savings_eur"] > 4000000.0

        # 100% negative hours
        res_100 = FinancialSensitivityEngine.evaluate_sensitivity(negative_price_freq=1.00)
        assert res_100["npv_eur"] > 60000000.0

        # 200x price spike (10,000 €/MWh spot price equivalent)
        res_spike = FinancialSensitivityEngine.evaluate_sensitivity(spot_spike_multiplier=200.0)
        assert res_spike["npv_eur"] > 200000000.0
        assert res_spike["annual_spot_arbitrage_savings_eur"] > 25000000.0

    def test_sensitivity_extreme_discount_rates(self):
        """Pure Python NPV must handle zero, high, and massive discount rates deterministically."""
        # 0.0% discount rate: exact sum of cash flows
        res_dr0 = FinancialSensitivityEngine.evaluate_sensitivity(discount_rate=0.0)
        assert res_dr0["npv_eur"] == sum(res_dr0["cash_flows"])

        # 100.0% discount rate
        res_dr100 = FinancialSensitivityEngine.evaluate_sensitivity(discount_rate=1.0)
        assert res_dr100["npv_eur"] > 0.0

        # 10,000% discount rate: future cash flows vanish, NPV approaches initial software cost
        res_dr_huge = FinancialSensitivityEngine.evaluate_sensitivity(discount_rate=100.0)
        assert -150000.0 <= res_dr_huge["npv_eur"] <= -100000.0

    def test_sensitivity_all_negative_cash_flows(self):
        """All-negative cash flows must compute negative NPV and return safe 0.0% IRR without hanging."""
        cfs_all_neg = [-100000.0, -50000.0, -50000.0, -50000.0]
        npv_val = FinancialSensitivityEngine._compute_npv(0.08, cfs_all_neg)
        assert npv_val < -100000.0

        irr_val = FinancialSensitivityEngine._compute_irr(cfs_all_neg)
        assert irr_val == 0.0

    def test_sensitivity_unconventional_cash_flow_irr_bug(self):
        """
        Adversarial challenger oracle test:
        Baseline project yields €9,569,953 NPV at 8% WACC on an initial €150k software investment.
        The economic internal rate of return MUST be positive (> 0%).
        """
        res = FinancialSensitivityEngine.evaluate_sensitivity()
        assert res["irr_pct"] > 0.0, (
            f"Expected positive IRR for highly profitable project (+€9.57M NPV), "
            f"got negative IRR: {res['irr_pct']}% due to bisection search capturing spurious negative root!"
        )

    def test_sensitivity_catastrophic_loss_irr_bug(self):
        """
        Adversarial challenger oracle test:
        Catastrophic loss (-€10,000,000 initial, €100/yr return) MUST NOT report 500% IRR!
        """
        cfs_loss = [-10000000.0, 100.0, 100.0, 100.0]
        irr_loss = FinancialSensitivityEngine._compute_irr(cfs_loss)
        assert irr_loss <= 0.0, (
            f"Expected non-positive IRR for catastrophic loss project (-10M cost, 300 return), "
            f"got: {irr_loss * 100.0}%!"
        )

    def test_sensitivity_monte_carlo_performance(self):
        """1,000 sensitivity evaluations must execute in < 300ms (<0.3ms per evaluation)."""
        t0 = time.perf_counter()
        for i in range(1000):
            FinancialSensitivityEngine.evaluate_sensitivity(
                spot_spike_multiplier=1.0 + (i % 10) * 0.1,
                negative_price_freq=0.01 + (i % 5) * 0.02,
                discount_rate=0.06 + (i % 4) * 0.02,
            )
        elapsed_ms = (time.perf_counter() - t0) * 1000.0
        assert elapsed_ms < 300.0, f"Expected < 300ms, took {elapsed_ms:.1f}ms"
