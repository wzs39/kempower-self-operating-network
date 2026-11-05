"""
Kempower Self-Operating Charging Network - Commercial AEaaS & SLA Settlement Engine
Module: src/commercial/sla_calculator.py

Implements:
1. Minimum Required Dwell Time (MRDT) anti-fraud boundary formula.
2. Fleet delayed & undercharged departure liquidated damages (250 € base + 5 €/min + 1.50 €/kWh).
3. Piecewise charger availability fee deduction (99.5% threshold, 2% per 0.1% shortfall, 95.0% full waiver).
4. 150% Monthly Base Fee maximum liability cap.
"""

import math
from typing import Dict, List, Any

class SLACalculator:
    """Authoritative AEaaS SLA & MRDT Settlement Calculator."""

    @classmethod
    def compute_mrdt(
        cls,
        soc_req: float,
        soc_arrive: float,
        batt_kwh: float,
        p_charger_max: float,
        p_veh_max: float,
        eta: float = 0.95,
        t_buffer: float = 15.0,
    ) -> float:
        """
        Computes Minimum Required Dwell Time (minutes):
            MRDT = ((SoC_req - SoC_arrive)/100 * E_batt) / (min(P_ch, P_veh) * eta) * 60 + t_buffer
        """
        delta_soc = max(0.0, soc_req - soc_arrive) / 100.0
        needed_energy = delta_soc * batt_kwh
        eff_power = min(p_charger_max, p_veh_max) * eta
        if eff_power <= 0.0:
            return float("inf")
        return (needed_energy / eff_power) * 60.0 + t_buffer

    @classmethod
    def compute_fleet_penalty(
        cls,
        delayed_records: List[Dict[str, Any]],
        undercharged_records: List[Dict[str, Any]],
        p_base: float = 250.0,
        c_min: float = 5.0,
        c_energy: float = 1.50,
    ) -> float:
        """
        Computes B2B fleet departure liquidated damages for records satisfying MRDT.
        """
        total = 0.0
        for r in delayed_records:
            if not r.get("mrdt_satisfied", True):
                continue
            delay_min = float(r.get("delay_min", 0.0))
            if delay_min > 0.0:
                total += p_base + max(0.0, delay_min - 15.0) * c_min
        for r in undercharged_records:
            if not r.get("mrdt_satisfied", True):
                continue
            delta_soc = max(0.0, float(r["soc_req"]) - float(r["soc_dep"])) / 100.0
            total += delta_soc * float(r["cap_kwh"]) * c_energy
        return round(total, 2)

    @classmethod
    def compute_availability_deduction(
        cls,
        monthly_base_fee: float,
        avail_pct: float,
        uptime_sla_pct: float = 99.50,
    ) -> float:
        """
        Piecewise availability fee deduction:
        - avail >= uptime_sla_pct: 0 €
        - (uptime_sla_pct - 4.50)% <= avail < uptime_sla_pct: ceil((uptime_sla_pct - avail)/0.10) * 2% of base fee (capped at 90%)
        - avail < (uptime_sla_pct - 4.50)%: 100% of monthly_base_fee
        """
        avail = round(avail_pct, 4)
        if avail >= uptime_sla_pct:
            return 0.0
        elif avail >= (uptime_sla_pct - 4.50):
            shortfall = round(uptime_sla_pct - avail, 4)
            steps = int(math.ceil(shortfall / 0.10))
            pct = min(90.0, steps * 2.0)
            return round(monthly_base_fee * (pct / 100.0), 2)
        else:
            return round(monthly_base_fee * 1.0, 2)

    @classmethod
    def settle_monthly_invoice(
        cls,
        monthly_base_fee: float,
        avail_pct: float,
        delayed_records: List[Dict[str, Any]],
        undercharged_records: List[Dict[str, Any]],
        cap_multiplier: float = 1.50,
        uptime_sla_pct: float = 99.50,
    ) -> Dict[str, Any]:
        """Settles monthly invoice with 150% maximum liability cap."""
        avail_ded = cls.compute_availability_deduction(monthly_base_fee, avail_pct, uptime_sla_pct=uptime_sla_pct)
        fleet_pen = cls.compute_fleet_penalty(delayed_records, undercharged_records)
        raw_claims = round(avail_ded + fleet_pen, 2)
        max_liability = round(monthly_base_fee * cap_multiplier, 2)
        capped_payout = min(raw_claims, max_liability)
        # Clamp net invoice to non-negative: operator never pays customer on an invoice
        net_invoice = max(0.0, round(monthly_base_fee - capped_payout, 2))
        return {
            "monthly_base_fee_eur": monthly_base_fee,
            "availability_deduction_eur": avail_ded,
            "fleet_penalty_eur": fleet_pen,
            "raw_total_claims_eur": raw_claims,
            "max_liability_cap_eur": max_liability,
            "capped_payout_eur": capped_payout,
            "net_operator_invoice_eur": net_invoice,
        }
