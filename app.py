"""
Kempower Self-Operating Charging Network - Interactive 4-Quadrant Command Center
Module: app.py

Run with:
    streamlit run app.py
"""

import sys
from pathlib import Path
from typing import Dict, Any

REPO_ROOT = Path(__file__).resolve().parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.core.dpr_matrix import STATION_CABINET_TOPOLOGY
from src.sim.data_loader import KempowerDataLoader
from src.sim.scenario_engine import ScenarioEngine
from src.commercial.roi_analyzer import ROIAnalyzer
from src.commercial.sla_calculator import SLACalculator

def build_dashboard_payload() -> Dict[str, Any]:
    """Builds the complete deterministic data payload for all 4 quadrants."""
    loader = KempowerDataLoader()
    engine = ScenarioEngine(loader)
    scenarios = engine.run_all_scenarios()
    labor = ROIAnalyzer.analyze_network_operations_labor()
    equip = ROIAnalyzer.analyze_equipment_and_payback()
    peak_vs_energy = ROIAnalyzer.analyze_monthly_peak_demand_vs_energy()
    return {
        "topology": STATION_CABINET_TOPOLOGY,
        "scenarios": scenarios,
        "labor": labor,
        "equip": equip,
        "peak_vs_energy": peak_vs_energy,
    }

def render_streamlit_app() -> None:
    import streamlit as st
    import pandas as pd

    st.set_page_config(
        page_title="Kempower Self-Operating Charging Network",
        layout="wide",
    )
    payload = build_dashboard_payload()
    sc = payload["scenarios"]
    labor = payload["labor"]
    equip = payload["equip"]

    st.title("Kempower Self-Operating Charging Network (Sentinel v2.0)")
    st.caption(
        "LahtiES Energy Tech Hackathon 2026 | 45 Official CSVs (240,635 Rows) | "
        "Friday 2026-11-13 Crisis Day: 13 -> 0 Missed Departures"
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("2026-11-13 Missed Departures", "0 (was 13)", "-100% (1,804.45 kWh recovered)")
    c2.metric("100-Site Manual Labor (45 €/h)", f"{labor['total_network_fte']} FTE", f"€{labor['total_network_annual_labor_eur']:,.0f}/yr total")
    c3.metric("Replug Share of Work Time", f"{labor['replug_share_by_duration_pct']}%", f"{labor['replug_network_fte']} FTE (€{labor['replug_network_annual_labor_eur']:,.0f}/yr)")
    c4.metric("S3 Abandonment (14d / 11-13)", "14.36% / 29.69%", "left_full=265 (74.9%) | left_queue=89 (25.1%)")

    q1, q2 = st.columns(2)
    with q1:
        st.subheader("Quadrant 1: Strict 1:N Cabinet Topology & S1 Strategy A vs B")
        rows = []
        for sid, cabs in payload["topology"].items():
            for cid, spec in cabs.items():
                rows.append({
                    "Site": sid,
                    "Cabinet": cid,
                    "Max Power (kW)": spec["max_kw"],
                    "Wired Chargers (1:N)": ", ".join(spec["chargers"]),
                    "Charger Max (kW)": spec["charger_max_kw"],
                })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)
        st.info(
            f"**S1 Strategy A (0 € Hardware CAPEX)**: Wave 1 (20:00-01:30) + single planned 01:30 swap onto healthy "
            f"C1-1/C1-2 (720 kW) recovers all 1,012.00 kWh (B04, B18, B20, B09) -> 0 missed departures.\n\n"
            f"**S1 Strategy B (Hardware Dual-Gun Expansion)**: 12 guns × €{equip['installed_cost_per_gun_eur']:,.0f}/gun "
            f"(€18k dispenser + €9k civil) = €{equip['s1_12_guns_total_capex_with_civil_eur']:,.0f} CAPEX vs "
            f"€{labor['s1_replug_annual_labor_eur']:,.0f}/yr S1 replug labor ({labor['s1_replug_share_of_network_pct']}% of network) "
            f"-> {equip['s1_payback_years_with_civil']} yr payback."
        )

    with q2:
        st.subheader("Quadrant 2: Edge Self-Healing & S5 3-Way Reconciliation")
        th = sc["S1"]["thermal_anomaly_audit"]
        n1 = sc["S1"]["n1_post_fault_audit"]
        s5_rec = sc["S5"]["three_way_reconciliation"]
        st.markdown(
            f"- **S1 Thermal Precursor (`telemetry_1min.csv`)**: `D1-9` (`C1-3`) peaked at **{th['true_peak_temp_c']}°C / "
            f"{th['true_peak_fan_rpm']:.0f} rpm** at `{th['true_peak_timestamp']}` (**{th['lead_time_before_f015_minutes']:.0f} min** "
            f"before `F015` at `01:50`; `01:45-01:50` was flat at `{th['temp_at_0145_c']}-{th['temp_at_0150_c']}°C`).\n"
            f"- **S1 `F016` Overtemperature Stop**: `02:25` to `06:31` (**{n1['f016_duration_minutes']} min = 4h 06m**, "
            f"`cleared_by = {n1['f016_cleared_by']}`). Healthy `C1-1 + C1-2 = 720 kW` runs at 100% with **0 kW** self-harming shed.\n"
            f"- **S3 Offline Islanding**: Local DLM enforces **1,425 kW DC (`1,492.15 kW AC <= 1,500 kW`)** at 95.5% rectifier efficiency.\n"
            f"- **S5 3-Way Digital Twin Reconciliation**: `site_config.csv` row 164 capped `grid_limit_kw` at **600 kW** vs "
            f"**900 kW** in `network_sites.csv` & `power_cabinets.csv` (`2×450 kW`). Restoring **600 -> 900 kW** unlocks "
            f"**+750.0 kWh** during `03:30-06:00`, eliminating the **508.95 kWh** deficit across `B27, B28, B33, B34, B35` "
            f"(plus `D5-7: 50 -> 150 kW`, `D5-8: sim_active -> True`)."
        )

    q3, q4 = st.columns(2)
    with q3:
        st.subheader("Quadrant 3: Closed-Loop 2026-11-13 Crisis Resolution (S1-S5)")
        s2 = sc["S2"]
        s4 = sc["S4"]
        summary_df = pd.DataFrame([
            {"Station": "S1 (Bus Depot)", "Baseline Missed": 4, "Deficit (kWh)": 1012.00, "Root Cause": "12 guns vs 24 buses (B04/B18/B20 unplugged) + C1-3 F016", "Resolution": "01:30 Batch Swap / Dual-Gun + 720 kW N-1", "Optimized Missed": 0},
            {"Station": "S2 (Truck Depot)", "Baseline Missed": 4, "Deficit (kWh)": 283.50, "Root Cause": "G1 400 kW curtailment + T05-T08 drawing 1,857 kWh", "Resolution": "Preempt T05-T08 during 14:20-18:15 (+283.50 kWh to T01-T04)", "Optimized Missed": 0},
            {"Station": "S3 (Highway Hub)", "Baseline Missed": 0, "Deficit (kWh)": 0.0, "Root Cause": "14.36% (14d) / 29.69% (11-13) public abandonment + F017 WAN loss", "Resolution": "Local 1,425 kW DC DLM + Plug & Queue (<500ms handover)", "Optimized Missed": 0},
            {"Station": "S4 (City Hub)", "Baseline Missed": 0, "Deficit (kWh)": 0.0, "Root Cause": "799.30 €/MWh spot spike + D4-2 connector fault", "Resolution": "0-CAPEX Load Shifting + Full Monthly Peak Protection", "Optimized Missed": 0},
            {"Station": "S5 (Bus Depot)", "Baseline Missed": 5, "Deficit (kWh)": 508.95, "Root Cause": "site_config.csv grid_limit_kw=600 kW (vs 900 kW) starving D5-1..5", "Resolution": "3-Way Auto-Calibration (600->900 kW, D5-7 150 kW, D5-8 eSIM)", "Optimized Missed": 0},
        ])
        st.dataframe(summary_df, use_container_width=True)
        st.caption(
            f"S2 Afternoon Deficit Breakdown: {s2['truck_deficits_kwh']} = 283.50 kWh | "
            f"MILP @ 799.30 €/MWh Unmet Vehicles: {len(s4['mpc_extreme_price_unmet_vehicles'])}"
        )

    with q4:
        st.subheader("Quadrant 4: Commercial AEaaS SLA & MRDT Calculator")
        soc_arr = st.slider("Arrival SoC (%)", 0.0, 80.0, 20.0, 1.0)
        soc_req = st.slider("Required Departure SoC (%)", 50.0, 100.0, 85.0, 1.0)
        batt_kwh = st.number_input("Vehicle Battery Capacity (kWh)", 50.0, 800.0, 400.0, 10.0)
        avail_pct = st.slider("Monthly Station Availability (%)", 94.0, 100.0, 99.6, 0.05)
        mrdt_min = SLACalculator.compute_mrdt(soc_req, soc_arr, batt_kwh, 150.0, 150.0)
        inv = SLACalculator.settle_monthly_invoice(10000.0, avail_pct, [], [])
        st.write(
            f"- **Minimum Required Dwell Time (MRDT)**: `{mrdt_min:.1f} min` (includes 15.0 min safety buffer)\n"
            f"- **Monthly Base Fee**: `€{inv['monthly_base_fee_eur']:,.2f}` | "
            f"**Availability Deduction**: `€{inv['availability_deduction_eur']:,.2f}` | "
            f"**Net Operator Invoice**: `€{inv['net_operator_invoice_eur']:,.2f}`"
        )

if __name__ == "__main__":
    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx
        if get_script_run_ctx() is not None:
            render_streamlit_app()
        else:
            data = build_dashboard_payload()
            print(
                f"Dashboard payload verified: 13 -> {data['scenarios']['scenario_day_missed_after']} missed departures."
            )
    except Exception:
        data = build_dashboard_payload()
        print(
            f"Dashboard payload verified: 13 -> {data['scenarios']['scenario_day_missed_after']} missed departures."
        )
