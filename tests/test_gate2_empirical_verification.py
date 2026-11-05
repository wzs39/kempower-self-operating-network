"""
Empirical Verification Suite for Gate 2 Review (Zero-Tautology, Production-Wired)
Kempower Self-Operating Charging Network
Verifies physical CSV inventory, operations_log labor & FTE reconciliation,
MILP mathematical invariants, S1-S5 scenario resolutions, and SLA piece-wise rigor.
"""

import glob
import os
import pandas as pd
import numpy as np

from src.utils.paths import get_repo_root, get_data_dir, resolve_csv_path
from src.core.dpr_matrix import DPRMatrix
from src.core.mpc_optimizer import MPCOptimizer, SiteMPCConfig, VehicleSchedule
from src.core.self_healing import EdgeFSM, EdgeState, InverterEfficiencyGuard, PredictiveThermalEngine
from src.sim.scenario_engine import ScenarioEngine
from src.commercial.roi_analyzer import ROIAnalyzer
from src.commercial.sla_calculator import SLACalculator

WORKSPACE = str(get_repo_root())
DATA_DIR = str(get_data_dir())

def test_csv_inventory_and_section_6_1():
    physical_csvs = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    assert len(physical_csvs) == 45, f"Expected 45 CSVs, got {len(physical_csvs)}"

    physical_counts = {}
    for p in physical_csvs:
        fname = os.path.basename(p)
        with open(p, "r", encoding="utf-8", errors="ignore") as f:
            physical_counts[fname] = len(f.readlines()) - 1

    total_physical_rows = sum(physical_counts.values())
    assert total_physical_rows == 240635, f"Expected 240,635 rows, got {total_physical_rows}"
    assert physical_counts["network_site_power.csv"] == 134400
    assert physical_counts["operations_log.csv"] == 1601

def test_operations_log_reconciliation():
    labor = ROIAnalyzer.analyze_network_operations_labor()
    assert labor["total_ops_biweekly"] == 8852
    assert labor["total_minutes_biweekly"] == 93412.0
    assert labor["replug_ops_biweekly"] == 5596
    assert labor["replug_minutes_biweekly"] == 44768.0
    assert labor["replug_share_by_count_pct"] == 63.22
    assert labor["replug_share_by_duration_pct"] == 47.93
    assert labor["total_network_fte"] == 20.76
    assert labor["replug_network_fte"] == 9.95
    assert labor["non_replug_network_fte"] == 10.81
    assert labor["staff_hourly_rate_eur"] == 45.0
    assert labor["annual_cost_per_fte_eur"] == 87750.0
    assert labor["total_network_annual_labor_eur"] == 1821534.0
    assert labor["replug_network_annual_labor_eur"] == 872976.0
    assert labor["s1_replug_ops_biweekly"] == 156
    assert labor["s1_replug_share_of_network_pct"] == 2.79
    assert labor["s1_replug_annual_labor_eur"] == 24336.0

def test_mpc_mathematical_formulation():
    # 1. Verify 1e-3 EUR/MWh -> EUR/kWh objective scaling on real MPCOptimizer
    cost_scaled = MPCOptimizer.compute_objective_cost(
        spot_price_mwh=799.30,
        tariff_mwh=24.00,
        power_kw=100.0,
        dt_hours=0.25,
        penalty_eur=250.0,
        abandoned=False,
    )
    assert round(cost_scaled, 5) == round((799.30 + 24.00) * 1e-3 * 100.0 * 0.25, 5)

    # 2. Verify CC/CV taper relaxation below 25 kW module capacity
    p_50_soc95 = MPCOptimizer.evaluate_cv_taper(rated_kw=50.0, soc=0.95)
    p_150_soc99 = MPCOptimizer.evaluate_cv_taper(rated_kw=150.0, soc=0.99)
    assert 0.0 < p_50_soc95 < 25.0
    assert 0.0 < p_150_soc99 < 25.0

    # 3. Verify real HiGHS MILP solve under 799.30 €/MWh does not abandon feasible vehicle (Issue C1)
    #    and applies full monthly peak demand rate (Issue C2)
    cfg = SiteMPCConfig(site_id="S1", transformer_max_kw=1200.0, peak_fee_eur_kw_mo=6.50, use_full_monthly_peak_fee=True)
    mpc = MPCOptimizer(config=cfg, dt_hours=0.25)
    veh = VehicleSchedule(
        vehicle_id="B18",
        arrive_step=0,
        depart_step=12,
        arrive_soc=0.08,
        required_soc=0.90,
        battery_kwh=400.0,
        max_charge_kw=150.0,
        penalty_eur=250.0,
    )
    plan = mpc.solve_15min_horizon(
        spot_prices_eur_mwh=[799.30] * 12,
        fleet_schedules=[veh],
        grid_tariffs_eur_mwh=[24.0] * 12,
    )
    assert plan.is_optimal
    assert len(plan.unmet_vehicles) == 0
    assert plan.vehicle_soc["B18"][-1] >= 0.90 - 1e-4
    assert round(plan.peak_cost_eur, 2) == round(6.50 * plan.peak_power_kw, 2)

def test_scenario_2_lookahead_precharging():
    """
    Verifies S2 afternoon missed departure deficit from departures_baseline.csv (Issues A5, A8, B5):
    - T01: 61.7% -> 70.0% (44.82 kWh)
    - T02: 49.4% -> 70.0% (111.24 kWh)
    - T03: 60.9% -> 70.0% (49.14 kWh)
    - T04: 55.5% -> 70.0% (78.30 kWh)
    Total S2 deficit = 283.50 kWh (reallocated from overnight trucks T05-T08 within 800/400 kW limits).
    """
    eng = ScenarioEngine()
    s2 = eng.run_s2_scenario()
    assert s2["baseline_missed_departures"] == 4
    assert s2["baseline_deficit_kwh"] == 283.50
    assert s2["truck_deficits_kwh"] == {
        "T01": 44.82,
        "T02": 111.24,
        "T03": 49.14,
        "T04": 78.30,
    }
    assert s2["true_grid_headroom_1420_1600_kwh"] == 33.3
    assert s2["overnight_trucks_t05_t08_afternoon_kwh"] > 1800.0
    assert sum(s2["c2_1_continuous_alloc_kw"].values()) <= 400.0
    assert sum(s2["c2_2_continuous_alloc_kw"].values()) <= 400.0
    assert s2["optimized_missed_departures"] == 0

def test_scenario_1_two_stage_n1_shedding():
    df_sp = pd.read_csv(resolve_csv_path("site_power_baseline.csv"))
    s1_sp = df_sp[(df_sp["site_id"] == "S1") & (df_sp["ts"].str.startswith("2026-11-13"))]
    s1_pre_trip = s1_sp[(s1_sp["ts"] >= "2026-11-13T01:00:00+02:00") & (s1_sp["ts"] <= "2026-11-13T02:15:00+02:00")]
    mean_pre_load = float(s1_pre_trip["power_kw"].mean())
    assert round(mean_pre_load, 1) == 870.0

    n1_audit = PredictiveThermalEngine.evaluate_s1_n1_post_fault_dispatch()
    assert n1_audit["f016_duration_minutes"] == 246
    assert n1_audit["f016_cleared_by"] == "technician"
    assert n1_audit["post_fault_n1_capacity_kw"] == 720.0
    assert n1_audit["healthy_cabinet_shed_kw"] == 0.0

def test_scenario_3_inverter_efficiency():
    safe_dc_kw, n_modules, ac_draw_steady = InverterEfficiencyGuard.max_safe_dc_kw(1500.0)
    assert n_modules == 57
    assert safe_dc_kw == 1425.0
    assert round(ac_draw_steady, 2) == 1492.15
    assert ac_draw_steady <= 1500.0

def test_sla_piecewise_mrdt_liability_cap():
    mrdt = SLACalculator.compute_mrdt(
        soc_req=80.0, soc_arrive=30.0, batt_kwh=200.0, p_charger_max=150.0, p_veh_max=150.0
    )
    assert round(mrdt, 2) == 57.11

    base_fee = 100.0
    test_cases = [
        (99.55, 0.0),
        (99.50, 0.0),
        (99.41, 2.0),
        (99.40, 2.0),
        (99.39, 4.0),
        (95.05, 90.0),
        (95.00, 90.0),
        (94.99, 100.0),
        (90.00, 100.0),
    ]
    for avail, expected in test_cases:
        actual = SLACalculator.compute_availability_deduction(base_fee, avail)
        assert actual == expected, f"Failed at {avail}%: expected {expected}, got {actual}"

    invoice = SLACalculator.settle_monthly_invoice(
        monthly_base_fee=5000.0,
        avail_pct=94.0,
        delayed_records=[{"delay_min": 60.0, "mrdt_satisfied": True}] * 10,
        undercharged_records=[],
    )
    assert invoice["capped_payout_eur"] == 7500.0
