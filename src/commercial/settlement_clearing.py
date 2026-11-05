"""
src/commercial/settlement_clearing.py

Authoritative B2B Autonomous Monthly SLA Settlement & Clearing Engine.
Implements Contract Form No: KEMP-AUTO-2029-SLA-V1 / KEMP-AUTO-2029-SLA-V2.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
import hashlib
import json
import math
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Union

try:
    from src.utils.paths import resolve_csv_path
except ImportError:
    def resolve_csv_path(filename: str) -> Path:
        return Path(__file__).resolve().parents[2] / "kempower-challenge" / "kempower-challenge-data" / filename


class ContractTier(str, Enum):
    TITANIUM = "Titanium"
    GOLD = "Gold"
    SILVER = "Silver"


class ExemptionReason(str, Enum):
    NONE = "NONE"
    CUSTOMER_DWELL_SHORTFALL = "CUSTOMER_DWELL_SHORTFALL"
    PREMATURE_UNPLUG = "PREMATURE_UNPLUG"
    VEHICLE_BMS_FAULT = "VEHICLE_BMS_FAULT"
    GRID_FORCE_MAJEURE = "GRID_FORCE_MAJEURE"


@dataclass(frozen=True)
class ContractTierConfig:
    tier: ContractTier
    uptime_target_pct: float
    monthly_base_fee_eur: float
    step_penalty_pct: float
    full_waiver_threshold_pct: float
    mrdt_buffer_min: float
    delay_grace_min: float = 15.0
    p_base_eur: float = 250.0
    c_min_eur: float = 5.00
    c_energy_eur: float = 1.50
    liability_cap_multiplier: float = 1.50


TIER_CONFIGS: Dict[ContractTier, ContractTierConfig] = {
    ContractTier.TITANIUM: ContractTierConfig(
        tier=ContractTier.TITANIUM,
        uptime_target_pct=99.90,
        monthly_base_fee_eur=15000.0,
        step_penalty_pct=2.50,
        full_waiver_threshold_pct=96.00,
        mrdt_buffer_min=10.0,
        delay_grace_min=10.0,
        p_base_eur=350.0,
        c_min_eur=7.50,
        c_energy_eur=2.00,
        liability_cap_multiplier=1.50,
    ),
    ContractTier.GOLD: ContractTierConfig(
        tier=ContractTier.GOLD,
        uptime_target_pct=99.50,
        monthly_base_fee_eur=10000.0,
        step_penalty_pct=2.00,
        full_waiver_threshold_pct=95.00,
        mrdt_buffer_min=15.0,
        delay_grace_min=15.0,
        p_base_eur=250.0,
        c_min_eur=5.00,
        c_energy_eur=1.50,
        liability_cap_multiplier=1.50,
    ),
    ContractTier.SILVER: ContractTierConfig(
        tier=ContractTier.SILVER,
        uptime_target_pct=99.00,
        monthly_base_fee_eur=7500.0,
        step_penalty_pct=1.50,
        full_waiver_threshold_pct=94.00,
        mrdt_buffer_min=20.0,
        delay_grace_min=20.0,
        p_base_eur=150.0,
        c_min_eur=3.00,
        c_energy_eur=1.00,
        liability_cap_multiplier=1.50,
    ),
}


@dataclass
class DepartureAuditRecord:
    trip_id: str
    vehicle_id: str
    site_id: str
    arrive_ts: str
    depart_sched_ts: str
    depart_actual_ts: str
    battery_kwh: float
    p_charger_max_kw: float
    p_veh_max_kw: float
    soc_arrive_pct: float
    soc_req_pct: float
    soc_dep_pct: float
    dwell_actual_min: float
    mrdt_min: float
    mrdt_satisfied: bool
    exemption_reason: ExemptionReason
    delay_min: float
    delay_penalty_eur: float
    energy_deficit_kwh: float
    energy_penalty_eur: float
    total_penalty_eur: float

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["exemption_reason"] = self.exemption_reason.value if isinstance(self.exemption_reason, ExemptionReason) else str(self.exemption_reason)
        return d


@dataclass
class MonthlyInvoiceStatement:
    invoice_id: str
    billing_period: str
    site_id: str
    customer_id: str
    contract_tier: str
    monthly_base_fee_eur: float
    target_availability_pct: float
    actual_availability_pct: float
    availability_shortfall_pct: float
    availability_deduction_rate_pct: float
    availability_deduction_eur: float
    total_trips_evaluated: int
    trips_penalized_count: int
    trips_exempt_count: int
    gross_delay_penalty_eur: float
    gross_energy_penalty_eur: float
    gross_fleet_penalties_eur: float
    capped_fleet_penalties_eur: float
    gross_total_claims_eur: float
    max_liability_cap_eur: float
    final_payout_deduction_eur: float
    net_invoice_payable_eur: float
    credit_carryforward_eur: float
    audit_hash: str
    line_items: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def __contains__(self, key: str) -> bool:
        return hasattr(self, key)

    def keys(self):
        return asdict(self).keys()

    def values(self):
        return asdict(self).values()

    def items(self):
        return asdict(self).items()


class SettlementClearingEngine:
    """Audit-grade Monthly Settlement Clearing Engine for AEaaS Fleets."""

    @classmethod
    def evaluate_mrdt_and_trip(
        cls,
        trip_data: Dict[str, Any],
        tier_cfg: ContractTierConfig,
        eta: float = 0.95,
    ) -> DepartureAuditRecord:
        """
        Evaluates single trip with MRDT physical gating and exemption attribution:
            MRDT = ((SoC_req - SoC_arr)/100 * Batt_kWh) / (min(P_ch, P_veh) * eta) * 60 + T_buffer
        """
        soc_arr = float(trip_data.get("soc_arrive_pct", trip_data.get("soc_arrive", 20.0)))
        soc_req = float(trip_data.get("soc_req_pct", trip_data.get("soc_req", 85.0)))
        soc_dep = float(trip_data.get("soc_dep_pct", trip_data.get("soc_dep", soc_req)))
        batt_kwh = float(trip_data.get("battery_kwh", trip_data.get("cap_kwh", 400.0)))
        p_ch = float(trip_data.get("p_charger_max_kw", trip_data.get("p_ch", 150.0)))
        p_veh = float(trip_data.get("p_veh_max_kw", trip_data.get("p_veh", 150.0)))
        dwell_min = float(trip_data.get("dwell_actual_min", trip_data.get("dwell_min", 120.0)))
        delay_min = max(0.0, float(trip_data.get("delay_min", 0.0)))
        end_reason = str(trip_data.get("end_reason", "completed")).lower()
        grid_outage = bool(trip_data.get("grid_outage_force_majeure", False))

        # 1. Compute MRDT
        delta_soc = max(0.0, soc_req - soc_arr) / 100.0
        needed_kwh = delta_soc * batt_kwh
        eff_kw = min(p_ch, p_veh) * eta
        mrdt_min = round(needed_kwh / eff_kw * 60.0 + tier_cfg.mrdt_buffer_min, 2) if eff_kw > 0 else float("inf")
        mrdt_satisfied = bool(dwell_min >= mrdt_min)

        # 2. Exemption Classification
        exemption = ExemptionReason.NONE
        if not mrdt_satisfied:
            exemption = ExemptionReason.CUSTOMER_DWELL_SHORTFALL
        elif end_reason in ("unplugged_by_operator", "premature_unplug", "driver_unplug", "unplugged_by_driver", "unplugged_early"):
            exemption = ExemptionReason.PREMATURE_UNPLUG
        elif end_reason in ("bms_abort", "vehicle_fault", "charger_fault_vehicle_induced", "bms_error", "vehicle_bms_abort"):
            exemption = ExemptionReason.VEHICLE_BMS_FAULT
        elif grid_outage:
            exemption = ExemptionReason.GRID_FORCE_MAJEURE

        # 3. Penalties (Strictly waived if exempt)
        delay_pen = 0.0
        energy_pen = 0.0
        deficit_kwh = 0.0
        if exemption == ExemptionReason.NONE:
            if delay_min > 0.0:
                grace = tier_cfg.delay_grace_min
                delay_pen = tier_cfg.p_base_eur + max(0.0, delay_min - grace) * tier_cfg.c_min_eur
            if soc_dep < soc_req:
                deficit_kwh = (soc_req - soc_dep) / 100.0 * batt_kwh
                energy_pen = deficit_kwh * tier_cfg.c_energy_eur

        total_pen = round(delay_pen + energy_pen, 2)
        return DepartureAuditRecord(
            trip_id=str(trip_data.get("trip_id", "TRIP_001")),
            vehicle_id=str(trip_data.get("vehicle_id", "VEH_001")),
            site_id=str(trip_data.get("site_id", "S1")),
            arrive_ts=str(trip_data.get("arrive_ts", "2026-11-13T01:00:00+02:00")),
            depart_sched_ts=str(trip_data.get("depart_sched_ts", "2026-11-13T05:30:00+02:00")),
            depart_actual_ts=str(trip_data.get("depart_actual_ts", "2026-11-13T05:30:00+02:00")),
            battery_kwh=batt_kwh,
            p_charger_max_kw=p_ch,
            p_veh_max_kw=p_veh,
            soc_arrive_pct=soc_arr,
            soc_req_pct=soc_req,
            soc_dep_pct=soc_dep,
            dwell_actual_min=dwell_min,
            mrdt_min=round(mrdt_min, 2),
            mrdt_satisfied=mrdt_satisfied,
            exemption_reason=exemption,
            delay_min=delay_min,
            delay_penalty_eur=round(delay_pen, 2),
            energy_deficit_kwh=round(deficit_kwh, 2),
            energy_penalty_eur=round(energy_pen, 2),
            total_penalty_eur=total_pen,
        )

    @classmethod
    def compute_availability_deduction(
        cls,
        tier_cfg: ContractTierConfig,
        actual_avail_pct: float,
    ) -> Tuple[float, float, float]:
        """
        Calculates (shortfall_pct, deduction_rate_pct, deduction_eur) in piecewise closed-form.
        """
        avail = round(actual_avail_pct, 4)
        target = tier_cfg.uptime_target_pct
        if avail >= target:
            return 0.0, 0.0, 0.0
        shortfall = round(target - avail, 4)
        if avail < tier_cfg.full_waiver_threshold_pct:
            return shortfall, 100.0, round(tier_cfg.monthly_base_fee_eur * 1.0, 2)
        steps = int(math.ceil(shortfall / 0.10))
        rate_pct = min(90.0, steps * tier_cfg.step_penalty_pct)
        deduction_eur = round(tier_cfg.monthly_base_fee_eur * (rate_pct / 100.0), 2)
        return shortfall, rate_pct, deduction_eur

    @classmethod
    def generate_monthly_settlement(
        cls,
        site_id: str,
        month: str,
        tier: Union[ContractTier, str] = ContractTier.GOLD,
        actual_availability_pct: Optional[float] = None,
        custom_base_fee_eur: Optional[float] = None,
        trips: Optional[List[Dict[str, Any]]] = None,
    ) -> MonthlyInvoiceStatement:
        """
        Generates auditable B2B monthly settlement statement implementing 150% liability cap,
        non-negative invoicing, and SHA-256 cryptographic audit seal.
        """
        if isinstance(tier, str):
            tier_key = tier.capitalize()
            tier_enum = ContractTier(tier_key) if tier_key in [t.value for t in ContractTier] else ContractTier.GOLD
        else:
            tier_enum = tier

        tier_cfg = TIER_CONFIGS[tier_enum]
        if custom_base_fee_eur is not None:
            tier_cfg = ContractTierConfig(
                tier=tier_cfg.tier,
                uptime_target_pct=tier_cfg.uptime_target_pct,
                monthly_base_fee_eur=custom_base_fee_eur,
                step_penalty_pct=tier_cfg.step_penalty_pct,
                full_waiver_threshold_pct=tier_cfg.full_waiver_threshold_pct,
                mrdt_buffer_min=tier_cfg.mrdt_buffer_min,
                delay_grace_min=tier_cfg.delay_grace_min,
                p_base_eur=tier_cfg.p_base_eur,
                c_min_eur=tier_cfg.c_min_eur,
                c_energy_eur=tier_cfg.c_energy_eur,
                liability_cap_multiplier=tier_cfg.liability_cap_multiplier,
            )

        # 1. Availability Deduction
        avail_pct = actual_availability_pct if actual_availability_pct is not None else 99.85
        shortfall_pct, rate_pct, avail_ded_eur = cls.compute_availability_deduction(tier_cfg, avail_pct)

        # 2. Trip Evaluation
        records: List[DepartureAuditRecord] = []
        if trips:
            for t in trips:
                records.append(cls.evaluate_mrdt_and_trip(t, tier_cfg))

        gross_delay = sum(r.delay_penalty_eur for r in records)
        gross_energy = sum(r.energy_penalty_eur for r in records)
        gross_fleet = round(gross_delay + gross_energy, 2)

        # 3. Apply Sub-Caps and Aggregate 150% Cap
        base_fee = tier_cfg.monthly_base_fee_eur
        capped_avail_ded = min(avail_ded_eur, base_fee)
        capped_fleet = min(gross_fleet, base_fee)

        raw_claims = round(capped_avail_ded + capped_fleet, 2)
        max_cap = round(base_fee * tier_cfg.liability_cap_multiplier, 2)
        final_payout = min(raw_claims, max_cap)

        # 4. Strictly Non-Negative Net Invoice Guarantee
        net_payable = max(0.00, round(base_fee - final_payout, 2))
        credit_carry = max(0.00, round(final_payout - base_fee, 2))

        # 5. Cryptographic SHA-256 Audit Seal
        payload_for_hash = f"{site_id}|{month}|{tier_enum.value}|{base_fee:.2f}|{avail_pct:.4f}|{final_payout:.2f}|{net_payable:.2f}"
        audit_hash = hashlib.sha256(payload_for_hash.encode("utf-8")).hexdigest()

        return MonthlyInvoiceStatement(
            invoice_id=f"INV-{month.replace('-', '')}-{site_id}-{tier_enum.value[:3].upper()}",
            billing_period=month,
            site_id=site_id,
            customer_id=f"CUST-{site_id}",
            contract_tier=tier_enum.value,
            monthly_base_fee_eur=base_fee,
            target_availability_pct=tier_cfg.uptime_target_pct,
            actual_availability_pct=avail_pct,
            availability_shortfall_pct=shortfall_pct,
            availability_deduction_rate_pct=rate_pct,
            availability_deduction_eur=avail_ded_eur,
            total_trips_evaluated=len(records),
            trips_penalized_count=sum(1 for r in records if r.total_penalty_eur > 0),
            trips_exempt_count=sum(1 for r in records if r.exemption_reason != ExemptionReason.NONE),
            gross_delay_penalty_eur=round(gross_delay, 2),
            gross_energy_penalty_eur=round(gross_energy, 2),
            gross_fleet_penalties_eur=gross_fleet,
            capped_fleet_penalties_eur=capped_fleet,
            gross_total_claims_eur=raw_claims,
            max_liability_cap_eur=max_cap,
            final_payout_deduction_eur=final_payout,
            net_invoice_payable_eur=net_payable,
            credit_carryforward_eur=credit_carry,
            audit_hash=audit_hash,
            line_items=[r.to_dict() for r in records],
        )

    @classmethod
    def render_markdown_audit_table(cls, stmt: MonthlyInvoiceStatement) -> str:
        """Renders an auditable Markdown statement table."""
        lines = [
            f"# B2B Monthly SLA Settlement Statement: `{stmt.invoice_id}`",
            f"**Site ID**: `{stmt.site_id}` | **Customer**: `{stmt.customer_id}` | **Billing Period**: `{stmt.billing_period}`",
            f"**Contract Tier**: `{stmt.contract_tier}` (Target Availability: `{stmt.target_availability_pct:.2f}%`)",
            "",
            "## 1. Executive Summary & Billing Reconciliation",
            "| Line Item | Value | Commercial Rule / Reference |",
            "|---|---|---|",
            f"| Monthly Base Service Fee | **€{stmt.monthly_base_fee_eur:,.2f}** | Contract Base Rate |",
            f"| Actual Station Availability | **{stmt.actual_availability_pct:.2f}%** | Telemetry Sampling |",
            f"| Availability Shortfall | {stmt.availability_shortfall_pct:.2f}% | Target - Actual |",
            f"| Availability Deduction Rate | {stmt.availability_deduction_rate_pct:.1f}% | Piecewise Step Deduction |",
            f"| Availability Deduction Fee | -€{stmt.availability_deduction_eur:,.2f} | Capped at 100% Base Fee |",
            f"| Total Fleet Trips Evaluated | {stmt.total_trips_evaluated} trips | Departures Evaluated |",
            f"| Trips Exempt from Penalties | {stmt.trips_exempt_count} trips | Dwell shortfall, unplug, BMS abort |",
            f"| Trips with Liquidated Damages | {stmt.trips_penalized_count} trips | Operator Operational Fault |",
            f"| Gross Delay Liquidated Damages | €{stmt.gross_delay_penalty_eur:,.2f} | Base + Per-Minute Delay |",
            f"| Gross Energy Deficit Damages | €{stmt.gross_energy_penalty_eur:,.2f} | Deficit kWh * Energy Rate |",
            f"| Gross Fleet Penalties | €{stmt.gross_fleet_penalties_eur:,.2f} | Delay + Deficit Damages |",
            f"| Capped Fleet Penalties | -€{stmt.capped_fleet_penalties_eur:,.2f} | Capped at 100% Base Fee |",
            f"| Gross Total Claims | €{stmt.gross_total_claims_eur:,.2f} | Availability + Fleet Claims |",
            f"| 150% Statutory Aggregate Cap | €{stmt.max_liability_cap_eur:,.2f} | 1.50 x Monthly Base Fee |",
            f"| Final Settlement Deduction | -€{stmt.final_payout_deduction_eur:,.2f} | Min(Gross Claims, 150% Cap) |",
            f"| **Net Operator Invoice Payable** | **€{stmt.net_invoice_payable_eur:,.2f}** | **Non-Negative Guarantee (≥ 0.00 €)** |",
            f"| Credit Carryforward to Next Month | €{stmt.credit_carryforward_eur:,.2f} | Excess Payout Credit |",
            "",
            "## 2. Cryptographic Audit Seal",
            f"```text\nSHA-256 Audit Seal: {stmt.audit_hash}\n```",
            "",
        ]
        if stmt.line_items:
            lines.extend([
                "## 3. Departure Audit Line Items",
                "| Trip ID | Vehicle | Dwell (m) | MRDT (m) | Satisfied | Exemption | Delay (m) | Deficit (kWh) | Penalty (€) |",
                "|---|---|---|---|---|---|---|---|---|",
            ])
            for it in stmt.line_items[:20]:
                lines.append(
                    f"| {it['trip_id']} | {it['vehicle_id']} | {it['dwell_actual_min']:.1f} | "
                    f"{it['mrdt_min']:.1f} | {'✅' if it['mrdt_satisfied'] else '❌'} | "
                    f"`{it['exemption_reason']}` | {it['delay_min']:.1f} | {it['energy_deficit_kwh']:.1f} | "
                    f"€{it['total_penalty_eur']:.2f} |"
                )
            if len(stmt.line_items) > 20:
                lines.append(f"\n*(Showing 20 of {len(stmt.line_items)} audit records)*")
        return "\n".join(lines)


# Top-level module alias conforming to PROJECT.md:117
def generate_monthly_settlement(
    site_id: str,
    month: str,
    tier: Union[ContractTier, str] = ContractTier.GOLD,
    actual_availability_pct: Optional[float] = None,
    custom_base_fee_eur: Optional[float] = None,
    trips: Optional[List[Dict[str, Any]]] = None,
) -> MonthlyInvoiceStatement:
    """Module-level entry point for monthly settlement clearing."""
    return SettlementClearingEngine.generate_monthly_settlement(
        site_id=site_id,
        month=month,
        tier=tier,
        actual_availability_pct=actual_availability_pct,
        custom_base_fee_eur=custom_base_fee_eur,
        trips=trips,
    )
