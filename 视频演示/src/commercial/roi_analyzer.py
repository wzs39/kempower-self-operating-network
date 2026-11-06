"""
Kempower Self-Operating Charging Network - Empirical Labor, CAPEX & ROI Analyzer
Module: src/commercial/roi_analyzer.py

Audits operations_log.csv, equipment_costs.csv, tariffs.csv, network_sites.csv and
network_site_power.csv x prices.csv to provide 100% transparent, auditable ROI and labor
figures (Issues A7, B1, B2, B6, B9, B10, C2).

NOTE (v1.3): `finance_daily.csv` was removed from this module — it is not one of the 45
official CSVs. Energy cost is now integrated from the 15-min power timeseries instead.
"""

import csv
from typing import Dict, Any

from src.utils.paths import resolve_csv_path

class ROIAnalyzer:
    """Empirical Labor, Equipment CAPEX, and Payback Period Analyzer."""

    STAFF_HOURLY_RATE_EUR: float = 45.0        # Official dataset README rate (45 €/h)
    BIWEEKLY_HOURS_PER_FTE: float = 75.0       # 37.5 h/week * 2 weeks
    BIWEEKS_PER_YEAR: float = 26.0             # 52 weeks / 2 = 1,950 h/yr -> 87,750 €/FTE·yr
    STEP_HOURS: float = 0.25                   # network_site_power.csv is 15-min resolution
    DEPOT_PEAK_FEE_EUR_KW_MONTH: float = 6.5   # tariffs.csv T_DEPOT
    PUBLIC_PEAK_FEE_EUR_KW_MONTH: float = 7.5  # tariffs.csv T_PUBLIC

    @classmethod
    def analyze_network_operations_labor(cls) -> Dict[str, Any]:
        """
        Parses all 8,852 rows of operations_log.csv (Issues A7, B1, B2, B9):
        - Total biweekly duration: 93,412 min = 1,556.87 hours = 20.76 FTE (at 75h/biweek).
        - At 45 €/h (87,750 €/FTE·yr), total 100-site manual labor = 1,821,534.00 €/yr.
        - move_and_replug_vehicle: 5,596 ops (63.22% by count), 44,768 min (47.93% by work time,
          NOT 63.2%), 746.13 h/biweek = 9.95 FTE = 872,976.00 €/yr across all 100 sites.
        - S1 replugs: 156 ops, 1,248 min/biweek = 2.79% of network replugs = 24,336.00 €/yr.
        - S1-S5 replugs: 347 ops, 2,776 min/biweek = 6.20% of network replugs = 54,132.00 €/yr.
        """
        ops_path = resolve_csv_path("operations_log.csv")
        total_ops = 0
        total_min = 0.0
        by_type_count: Dict[str, int] = {}
        by_type_min: Dict[str, float] = {}

        s1_replug_ops = 0
        s1_replug_min = 0.0
        s1_s5_replug_ops = 0
        s1_s5_replug_min = 0.0
        primary_sites = {"S1", "S2", "S3", "S4", "S5"}

        with open(ops_path, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                op_type = row["action"].strip()
                cnt = int(row["count"])
                dur = float(row["staff_minutes"])
                sid = row["site_id"].strip()

                total_ops += cnt
                total_min += dur
                by_type_count[op_type] = by_type_count.get(op_type, 0) + cnt
                by_type_min[op_type] = by_type_min.get(op_type, 0.0) + dur

                if op_type == "move_and_replug_vehicle":
                    if sid == "S1":
                        s1_replug_ops += cnt
                        s1_replug_min += dur
                    if sid in primary_sites:
                        s1_s5_replug_ops += cnt
                        s1_s5_replug_min += dur

        replug_ops = by_type_count.get("move_and_replug_vehicle", 0)
        replug_min = by_type_min.get("move_and_replug_vehicle", 0.0)
        non_replug_min = total_min - replug_min

        total_hours_bw = total_min / 60.0
        replug_hours_bw = replug_min / 60.0
        non_replug_hours_bw = non_replug_min / 60.0

        total_fte = total_hours_bw / cls.BIWEEKLY_HOURS_PER_FTE
        replug_fte = replug_hours_bw / cls.BIWEEKLY_HOURS_PER_FTE
        non_replug_fte = non_replug_hours_bw / cls.BIWEEKLY_HOURS_PER_FTE

        annual_cost_per_fte = cls.BIWEEKLY_HOURS_PER_FTE * cls.BIWEEKS_PER_YEAR * cls.STAFF_HOURLY_RATE_EUR  # 87,750 €
        total_annual_labor_eur = round(total_hours_bw * cls.BIWEEKS_PER_YEAR * cls.STAFF_HOURLY_RATE_EUR, 2)
        replug_annual_labor_eur = round(replug_hours_bw * cls.BIWEEKS_PER_YEAR * cls.STAFF_HOURLY_RATE_EUR, 2)
        non_replug_annual_labor_eur = round(non_replug_hours_bw * cls.BIWEEKS_PER_YEAR * cls.STAFF_HOURLY_RATE_EUR, 2)

        s1_replug_annual_eur = round((s1_replug_min / 60.0) * cls.BIWEEKS_PER_YEAR * cls.STAFF_HOURLY_RATE_EUR, 2)
        s1_s5_replug_annual_eur = round((s1_s5_replug_min / 60.0) * cls.BIWEEKS_PER_YEAR * cls.STAFF_HOURLY_RATE_EUR, 2)

        return {
            "staff_hourly_rate_eur": cls.STAFF_HOURLY_RATE_EUR,
            "annual_cost_per_fte_eur": annual_cost_per_fte,
            "total_ops_biweekly": total_ops,
            "total_minutes_biweekly": total_min,
            "total_hours_biweekly": round(total_hours_bw, 2),
            "total_network_fte": round(total_fte, 2),
            "total_network_annual_labor_eur": total_annual_labor_eur,
            "replug_ops_biweekly": replug_ops,
            "replug_minutes_biweekly": replug_min,
            "replug_share_by_count_pct": round(replug_ops / max(1, total_ops) * 100.0, 2),
            "replug_share_by_duration_pct": round(replug_min / max(1.0, total_min) * 100.0, 2),
            "replug_network_fte": round(replug_fte, 2),
            "replug_network_annual_labor_eur": replug_annual_labor_eur,
            "non_replug_minutes_biweekly": non_replug_min,
            "non_replug_share_by_duration_pct": round(non_replug_min / max(1.0, total_min) * 100.0, 2),
            "non_replug_network_fte": round(non_replug_fte, 2),
            "non_replug_network_annual_labor_eur": non_replug_annual_labor_eur,
            "s1_replug_ops_biweekly": s1_replug_ops,
            "s1_replug_minutes_biweekly": s1_replug_min,
            "s1_replug_share_of_network_pct": round(s1_replug_min / max(1.0, replug_min) * 100.0, 2),
            "s1_replug_annual_labor_eur": s1_replug_annual_eur,
            "s1_s5_replug_ops_biweekly": s1_s5_replug_ops,
            "s1_s5_replug_minutes_biweekly": s1_s5_replug_min,
            "s1_s5_replug_share_of_network_pct": round(s1_s5_replug_min / max(1.0, replug_min) * 100.0, 2),
            "s1_s5_replug_annual_labor_eur": s1_s5_replug_annual_eur,
            "breakdown_by_type_count": by_type_count,
            "breakdown_by_type_minutes": by_type_min,
        }

    @classmethod
    def analyze_equipment_and_payback(cls) -> Dict[str, Any]:
        """
        Audits equipment_costs.csv and compares Strategy A (0-CAPEX Software Scheduling)
        vs Strategy B (Hardware Dual-Gun Expansion, Issues B2, B6, B10).
        """
        eq_path = resolve_csv_path("equipment_costs.csv")
        costs: Dict[str, float] = {}
        with open(eq_path, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                val_str = row.get("eur") or row.get("cost_eur") or "0"
                costs[row["item"].strip()] = float(val_str)

        labor = cls.analyze_network_operations_labor()
        sat_eur = costs.get("dispenser_up_to_400kw", costs.get("satellite_dispenser", 18000.0))
        civ_eur = costs.get("civil_works", costs.get("civil_works_per_gun", 9000.0))
        installed_per_gun_eur = sat_eur + civ_eur  # 27,000 €

        s1_12_guns_hw_only_eur = 12 * sat_eur               # 216,000 €
        s1_12_guns_with_civil_eur = 12 * installed_per_gun_eur  # 324,000 €
        s1_replug_annual_eur = labor["s1_replug_annual_labor_eur"]  # 24,336 €

        return {
            "equipment_costs_catalog": costs,
            "satellite_dispenser_eur": sat_eur,
            "civil_works_per_gun_eur": civ_eur,
            "installed_cost_per_gun_eur": installed_per_gun_eur,
            "s1_12_guns_hw_only_capex_eur": s1_12_guns_hw_only_eur,
            "s1_12_guns_total_capex_with_civil_eur": s1_12_guns_with_civil_eur,
            "s1_annual_replug_savings_eur": s1_replug_annual_eur,
            "s1_payback_years_with_civil": round(s1_12_guns_with_civil_eur / s1_replug_annual_eur, 2),
            "s1_payback_years_hw_only": round(s1_12_guns_hw_only_eur / s1_replug_annual_eur, 2),
            "strategy_a_0capex_capex_eur": 0.0,
            "strategy_a_immediate_positive_roi": True,
        }

    @classmethod
    def analyze_monthly_peak_demand_vs_energy(cls) -> Dict[str, Any]:
        """
        Compares S1-S5 monthly peak demand fees against their 14-day energy cost (Issue C2).

        FIX (v1.3): the previous implementation read `finance_daily.csv`, which is NOT one of
        the 45 official CSVs, so this method raised FileNotFoundError and `app.py` could never
        render. Both figures are now re-derived from the dataset itself:

            energy  = sum over 15-min steps of delivered_kw * 0.25 h * (spot + grid tariff)
            demand  = max(grid_kw) * peak_power_fee_eur_kw_month

        The tariff split follows `network_sites.csv` `type`: depot sites pay T_DEPOT
        (24/11 €/MWh, 6.5 €/kW·month), public hubs pay T_PUBLIC (28/13 €/MWh, 7.5 €/kW·month).
        """
        site_ids = {"S1", "S2", "S3", "S4", "S5"}
        depot_types = {"bus_depot", "logistics_depot", "port_truck_depot"}

        site_type: Dict[str, str] = {}
        fee_eur_kw_month: Dict[str, float] = {}
        with open(resolve_csv_path("network_sites.csv"), mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["site_id"] in site_ids:
                    site_type[row["site_id"]] = row["type"]
                    fee_eur_kw_month[row["site_id"]] = (
                        cls.DEPOT_PEAK_FEE_EUR_KW_MONTH
                        if row["type"] in depot_types
                        else cls.PUBLIC_PEAK_FEE_EUR_KW_MONTH
                    )

        # ts -> (spot, depot tariff, public tariff)
        price: Dict[str, Any] = {}
        with open(resolve_csv_path("prices.csv"), mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                price[row["ts"]] = (
                    float(row["spot_eur_mwh"]),
                    float(row["grid_tariff_depot_eur_mwh"]),
                    float(row["grid_tariff_public_eur_mwh"]),
                )

        energy_cost_14d = 0.0
        energy_kwh_14d = 0.0
        peak_grid_kw: Dict[str, float] = {sid: 0.0 for sid in site_ids}
        with open(resolve_csv_path("network_site_power.csv"), mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                sid = row["site_id"]
                if sid not in site_ids:
                    continue
                spot, tariff_depot, tariff_public = price.get(
                    row["ts"], (0.0, 0.0, 0.0)
                )
                is_depot = site_type.get(sid) in depot_types
                eur_mwh = spot + (tariff_depot if is_depot else tariff_public)
                kwh = float(row["delivered_kw"]) * cls.STEP_HOURS
                energy_kwh_14d += kwh
                energy_cost_14d += kwh / 1000.0 * eur_mwh
                peak_grid_kw[sid] = max(peak_grid_kw[sid], float(row["grid_kw"]))

        monthly_peak_fee = sum(
            peak_grid_kw[sid] * fee_eur_kw_month.get(sid, 0.0) for sid in site_ids
        )
        return {
            "s1_s5_energy_cost_14d_eur": round(energy_cost_14d, 2),
            "s1_s5_energy_kwh_14d": round(energy_kwh_14d, 1),
            "s1_s5_unit_price_eur_mwh": round(
                energy_cost_14d / energy_kwh_14d * 1000.0, 2
            ) if energy_kwh_14d else 0.0,
            "s1_s5_monthly_peak_demand_fee_eur": round(monthly_peak_fee, 2),
            "s1_s5_annual_peak_demand_fee_eur": round(monthly_peak_fee * 12.0, 2),
            "s1_s5_peak_grid_kw_by_site": {k: round(v, 1) for k, v in peak_grid_kw.items()},
            "peak_demand_exceeds_14d_energy_cost": monthly_peak_fee > energy_cost_14d,
            "demand_to_energy_ratio": round(monthly_peak_fee / energy_cost_14d, 3)
            if energy_cost_14d else 0.0,
        }
