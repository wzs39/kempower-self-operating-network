# Project Brief · Project Sentinel - The Self-Operating Charging Network

**Challenge Track**: Kempower Challenge (LahtiES Energy Tech Hackathon 2026, LUT University)  
**Core Question**: *"If humans are not allowed to operate the charging network, how do we design an autonomous system?"*  
**Sponsor Technologies**: Kempower Dynamic Power Routing (DPR), 25 kW Modular Power Units, Satellite Dispensers, ChargEye Cloud / Edge Architecture.  

---

## 1. Ground Truth Problem Statement

From the official 45 CSV dataset (`kempower-challenge-data/`, 240,635 rows):
- **Baseline Labor**: Over 14 days, the network generated 8,852 manual operations totaling 93,412 staff-minutes (1,557 staff-hours). Under Finnish labor regulations (37.5 h/week), this equals **20.76 FTE $\approx$ 21 FTE** costing **1,365,000 €/year**.
- **Labor Breakdown**:
  - `move_and_replug_vehicle`: 5,596 occurrences, 44,768 minutes (**9.95 FTE / 47.93%** of all labor). Drivers and depot staff spend hours physically shuffling plugs.
  - Fault dispatch, technician site visits, telephone support, manual setpoint adjustments: 3,256 occurrences, 48,644 minutes (**10.81 FTE / 52.07%**).
- **Crisis Matrix (Friday 2026-11-13 Scenario Day)**:
  - **S1 (Bus Depot North)**: 24 buses vs 12 posts; Power Cabinet C1-3 overheats (F015 $\to$ F016 critical trip at 02:25).
  - **S2 (Logistics Depot East)**: DSO issues 400 kW curtailment from 16:00 to 20:00; baseline results in 13 trucks departing with uncharged batteries.
  - **S3 (Highway Hub)**: 2-hour cellular outage (10:00–12:00) during heavy transit traffic; naive fallback strangles throughput.
  - **S4 (Urban Hub)**: Nord Pool spot price spikes to **799.30 €/MWh** at 18:00 (baseline site has 0 kWh BESS).
  - **S5 (Retail Hub)**: Commissioning errors leave D5-7 throttled and D5-8 with an unactivated eSIM.

---

## 2. Sentinel Solution Architecture

1. **Hardware-Feasible Virtual Replugging**:
   - Retrofit S1's 12 single-gun posts with dual-gun satellites (24 CCS2 plugs) for 32,400 € CAPEX.
   - All 24 buses connect upon arrival. Edge software orchestrates Phase A (22:00–02:00) and Phase B (02:00–05:30) via sub-500ms zero-arc contactor switching.
2. **Deterministic Edge FSM & Self-Healing**:
   - Continuous N-1 thermal monitoring: shed 180 kW in 260 ms to keep site within safe 720 kW limit without hazardous back-feeding to tripped cabinets.
   - Autonomous offline islanding: local SQLite WAL cache and pre-cached Day-Ahead electricity prices enable 72+ hours of disconnected operation.
   - Digital twin auto-calibration: automatically corrects throttled power configurations and activates dormant eSIMs.
3. **HiGHS MILP Optimizer**:
   - $10^{-3}$ spot price dimensional scaling factor (€/MWh $\to$ €/kWh).
   - Strict AC inverter efficiency guard ($P_{\text{AC}} = P_{\text{DC}} / 0.955 \le P_{\text{grid}}$).
   - Continuous DPR CC/CV power envelope relaxation.
4. **Commercial CaaS Model & One-Page SLA**:
   - 99.5% availability and on-time departure guarantee.
   - Minimum Required Dwell Time (MRDT) anti-fraud formulation.
   - Full hardware payback in **1.89 months**.
