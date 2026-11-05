# Submission Package · Kempower Self-Operating Charging Network

## 1. Inspiration (Empirical Dataset Findings)
Across the 100-site European charging network (`240,635` rows across 45 official CSV files), operators spend **93,412 staff-minutes per two weeks (`1,556.87 h = 20.76 FTE`)** on manual interventions (`€1,821,534/yr` at the official `45 €/h = 87,750 €/FTE·yr` rate), of which **`move_and_replug_vehicle` accounts for 5,596 actions (63.22% by count) and 44,768 minutes (47.93% of work time = 9.95 FTE = €872,976/yr)**. On Crisis Friday `2026-11-13`, 13 fleet vehicles miss departure (`1,804.45 kWh` total deficit across S1, S2, and S5) while S3 suffers a `29.69%` public abandonment spike (`14.36%` 14-day baseline).

## 2. What It Does
**Project Sentinel** replaces reactive human operations with a two-tier autonomous operating system combining a **15-minute HiGHS MILP Macro-Scheduler** and a **millisecond Edge Micro-FSM**:
- **S1 Bus Depot (`4 -> 0` missed, `1,012.00 kWh` recovered)**: Detects `D1-9` (`C1-3`) thermal anomaly at `2026-11-12T22:31:00+02:00` (`59.3°C / 702 rpm`, `3h 19m` before `F015`) and executes **Strategy A (`0 €` CAPEX software wave scheduling + single `01:30` batch swap)** onto healthy cabinets `C1-1 + C1-2` (`720 kW` N-1 capacity during `F016`'s `4h 06m` technician repair window).
- **S2 Logistics Depot (`4 -> 0` missed, `283.50 kWh` recovered)**: Preempts overnight trucks `T05–T08` (`1,857.06 kWh` afternoon pool) using 1 kW continuous OCPP setpoints during `14:20–18:15` so afternoon trucks `T01–T04` depart 100% on time despite the `400 kW` `G1` DSO curtailment (`33.3 kWh` raw grid headroom).
- **S5 Bus Depot (`5 -> 0` missed, `508.95 kWh` recovered)**: Digital Twin 3-way reconciliation detects `site_config.csv` row 164 capping `grid_limit_kw` at `600 kW` (vs `900 kW` in `network_sites.csv` and `power_cabinets.csv`), restoring `900 kW` (`+750 kWh` in `03:30–06:00`), `D5-7` (`50 -> 150 kW`), and `D5-8` (`sim_active -> True`).

## 3. Verification & Reproducibility Checklist
- [x] `python verify_all.py` completes in `< 0.5s` with 0 errors.
- [x] `pytest tests/` passes all `179` unit, integration, E2E, and 29-item GitHub Issue #2 audit tests.
- [x] `streamlit run app.py` launches the 4-quadrant interactive command center.
