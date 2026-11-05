# Project Brief · Project Sentinel - The Self-Operating Charging Network

**Challenge Track**: Kempower Challenge (LahtiES Energy Tech Hackathon 2026, LUT University)  
**Core Question**: *"If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"*  
**Sponsor Technologies**: Kempower Dynamic Power Routing (DPR), 25 kW Modular Power Units, Satellite Dispensers, ChargEye Cloud / Edge Architecture.  

---

## 1. Ground Truth Problem Statement

From the official 45 CSV dataset (`kempower-challenge-data/`, 240,635 rows):
- **Baseline Labor (`B1`)**: Over 14 days, the network generated 8,852 manual operations totaling 93,412 staff-minutes (1,556.87 staff-hours). Under Finnish statutory labor hours (37.5 h/week = 1,950 h/yr) at `45 €/h` (`equipment_costs.csv`, `87,750 €/FTE/yr`), this equals **20.76 FTE $\approx$ 21 FTE** costing **1,821,534 €/year** (`1,982,229 €/year` when technician visits are priced at `80 €/h`).
- **Labor Breakdown (`B1`)**:
  - `move_and_replug_vehicle`: 5,596 occurrences (**63.22%** of event count), 44,768 minutes (**9.95 FTE / 47.93%** of all labor duration = **872,976 €/year** across 100 sites; S1 single-site = **24,336 €/year**).
  - Fault dispatch, technician site visits, telephone support, manual setpoint adjustments: 3,256 occurrences, 48,644 minutes (**10.81 FTE / 52.07%** of labor duration).
- **Crisis Matrix (Friday 2026-11-13 Scenario Day)**:
  - **S1 (Bus Depot North)**: 24 buses vs 12 single-gun dispensers (`max_simultaneous_sessions = 12`); Power Cabinet C1-3 fan degrades (`F015` at `01:50`, predictable `199 min` earlier at `2026-11-12T22:31:00+02:00` via `59.3°C / 702 rpm`) and trips (`F016` at `02:25` for `246 min`, `cleared_by = technician`), causing 4 missed departures (`B04, B09, B18, B20`, `1,012.00 kWh` deficit).
  - **S2 (Logistics Depot East)**: DSO issues 400 kW curtailment (`G1`, 16:00–20:00); baseline results in 4 missed truck departures (`T01, T02, T03, T04`, `283.50 kWh` deficit).
  - **S3 (Highway Hub)**: 2-hour cellular outage (10:00–12:00) triggers naive 50 kW fallback (`offline_fallback_kw_per_dispenser = 50`), driving abandonment to **29.69%** (76/256 drivers vs **14.36%** 14-day baseline, `354/2,465`).
  - **S4 (Urban Hub)**: Nord Pool spot price spikes to **799.30 €/MWh** at 18:00 (baseline site has 0 kWh BESS, `150 kW` PV; `F017` cable fault on `D4-2` at 21:30).
  - **S5 (New Bus Depot)**: Three-way configuration mismatch (`sites.csv = 900 kW`, `power_cabinets.csv = 2×450 = 900 kW`, `site_config.csv grid_limit_kw = 600 kW`), plus `D5-7` throttled to `50 kW` and `D5-8` unactivated eSIM, causing 5 missed departures (`508.95 kWh` deficit).

---

## 2. Sentinel Solution Architecture

1. **Dual-Strategy S1 Replug Resolution (`A1, B2, B6, D5`)**:
   - **Strategy A (0 € CAPEX Immediate Software-Coordinated Single `01:30` Batch Swap)**: Consolidates chaotic midnight replugging into a single scheduled batch swap at `01:30` with 12 existing single-gun posts, delivering `+1,012.00 kWh` and eliminating all 4 missed departures at **0 € CAPEX**.
   - **Strategy B (2029 Hardware Expansion)**: Adds 12 dispensers (`18,000 €` dispenser + `9,000 €` civil works = `27,000 €/gun`, total `324,000 €` CAPEX per `equipment_costs.csv`, `13.31-year` standalone payback vs S1's `24,336 €/yr` replug labor).
2. **Deterministic Edge FSM, Intra-Cabinet DPR & Self-Healing (`A2–A8, B8, C6`)**:
   - Enforces strict 1:N cabinet-to-dispenser physical wiring (`C1-1 -> D1-1..D1-4`, `C1-2 -> D1-5..D1-8`, `C1-3 -> D1-9..D1-12`).
   - Early fan degradation detection (`199 min` before `F015`) and safe `720 kW` N-1 post-fault dispatch on `C1-1/C1-2` with `0 kW` self-harm while dispatching technician for `F016`.
   - Autonomous offline islanding at S3 (`1,425 kW DC` / `1,492.15 kW AC <= 1,500 kW`, abandonment `< 0.5%`) and 3-way digital-twin reconciliation at S5 (`600 -> 900 kW`, unlocking `+750 kWh > 508.95 kWh` deficit).
3. **HiGHS MILP Optimizer (`C1–C5`)**:
   - $10^{-3}$ spot price dimensional scaling factor (€/MWh $\to$ €/kWh), full monthly peak demand rate (`6.50 / 7.50 €/kW/mo`), AC inverter guard ($\eta = 0.955$), and continuous SoC deficit slack (`z_v in [0, 1]`, weight `10,000 €`) preventing false vehicle abandonment at `799.30 €/MWh`.
4. **Commercial CaaS Model & One-Page SLA**:
   - 99.5% availability and on-time departure guarantee, Minimum Required Dwell Time (MRDT) anti-fraud gate, and 150% monthly liability cap.
