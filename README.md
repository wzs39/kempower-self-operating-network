# ⚡ Project Sentinel · The Self-Operating Charging Network
### Autonomous Energy Certainty-as-a-Service (CaaS) for Heavy Fleets & High-Power Hubs
*Kempower Challenge · LahtiES Energy Tech Hackathon 2026 (Thu 5.11. – Sat 7.11.2026 @ LUT University Lahti / CrazyTown)*  
*Official Challenge Lead & Mentor: Mats Mattsson (Kempower Cloud Software Leader & Judge), Panu Vartiainen (Kempower Expert)*

> **Design perspective (stated as required by the brief):** We design from the **CPO (Charge Point Operator) perspective** — the party that owns the operating cost and carries the SLA liability. That is why our primary metric is **staff-hours eliminated and energy certainty delivered**, not kWh sold and not driver-app engagement. Every other module (OCPP 2.0.1, ISO 15118, anti-fraud, BESS interface) is a by-product of this single line, not a separate goal.
>
> **Data notice:** All figures in this repository are computed from the **synthetic** `kempower-challenge-data` pack supplied for this hackathon. None of it is real Kempower or customer data. The "2029 bus operator" story is a **fictional scenario**, not an actual customer.

---

[![Pytest Tests](https://img.shields.io/badge/pytest-431%20passed%20(100%25)-success?style=for-the-badge&logo=pytest)](./tests/)
[![E2E Tests](https://img.shields.io/badge/E2E%20Runner-106%20passed%20(537%20total)-success?style=for-the-badge&logo=shield)](./e2e_tests/)
[![Deterministic Verifier](https://img.shields.io/badge/verify__all.py-0.34s%20Deterministic%20Pass-blue?style=for-the-badge&logo=python)](./verify_all.py)
[![Official Dataset Integrity](https://img.shields.io/badge/Official%20CSVs-45%2F45%20Strictly%20Read--Only-green?style=for-the-badge&logo=git)](./kempower-challenge/kempower-challenge-data/)
[![Scenario Day Autonomy](https://img.shields.io/badge/Scenario%20Day%2011--13-13%20%E2%86%92%203%20(0%E2%82%AC%20software)-brightgreen?style=for-the-badge)](./src/sim/scenario_engine.py)
[![Labor Reduction](https://img.shields.io/badge/Human%20Baseline-20.76%20FTE%20Continuous%20Ops%20Eliminated-orange?style=for-the-badge)](./src/commercial/roi_analyzer.py)

---

## 🎯 The Core Mission: Redesigning for Zero Continuous Human Intervention

> **The Kempower Question**:  
> *"If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"*

Today, modern charging networks are tethered to an invisible army of human workers: dispatchers constantly monitoring setpoints, call-center operators rebooting stalled chargers, and depot staff wandering frozen yards at 2 AM to unplug and replug buses. 

**Project Sentinel** fundamentally re-architects charging infrastructure into an autonomous, closed-loop operating system. Built directly upon Kempower's modular **Dynamic Power Routing (DPR)** technology, Sentinel unifies a **15-minute rolling Mixed-Integer Linear Program (MILP)** in the cloud with a **sub-100ms autonomous Edge Finite State Machine (FSM)**. It guarantees that every commercial vehicle departs on time with full energy, strictly respects electrical grid boundaries with zero transformer overcurrents, and translates autonomous reliability into an enforceable, bankable **Outcome-Based Service Level Agreement (One-Page SLA)**.

---

## 📊 The Empirical Ground Truth: The 20.76 FTE Crisis (100 Sites = 95 Network + 5 Detailed)

All architecture decisions and financial models in Project Sentinel are derived directly from the official 45 CSV files (`kempower-challenge-data/`, 240,635 rows across **100 commercial and public sites**: `95` network-level sites in `network_kpis.csv` delivering `13,368.6 MWh` with `2,096.1 hours` of `hours_demand_above_grid_limit` across `72` sites where `peak_grid_kw == grid_limit_kw`, plus `5` detailed high-resolution sites `S1–S5`):

| Operational Metric | Official Baseline Ground Truth | Project Sentinel Autonomous Result |
|---|---|---|
| **Two-Week Human Interventions** | **8,852 manual operations** across 100 sites (`operations_log.csv`) | **0 continuous operations** (autonomous closed-loop; physical technician visits retained strictly for hard component replacement e.g. `F016` `cleared_by=technician`) |
| **Total Human Labor Time** | **93,412 minutes (1,556.87 hours / 2 weeks)** | **0 minutes continuous triage / midnight replugging** |
| **Full-Time Equivalent (FTE) Baseline** | **20.76 FTE $\approx$ 21 FTE** (Finnish statutory 37.5 h/wk) | **9.95 FTE midnight replug (`5,596` events) + 10.81 FTE remote triage (`3,256` events) automated** |
| **Annual Continuous Labor OPEX** | **1,821,534 € / year** (@ 45 €/h in `equipment_costs.csv`) | **1,821,534 € saved annually** (1.98M € with 80 €/h tech visits) |
| **Depot Midnight Replugging** | **5,596 events (63.22% count / 47.93% labor duration = 9.95 FTE)** | **0 human moves**: Tier 2 (`0 €` software urgency). Tier 3 (`324,000 €` 24-plug expansion @ S1) does **not** reach `0` on its own — see the corrected Tier 3 row below |
| **Scenario Day Crisis (Friday 13.11)** | **13 missed departures** (`S1=4, S2=4, S5=5`), **29.69% S3 abandoned** | **Tier 2 (`0 €`, 0 moves): 3 missed (`10` saved: `S1: 4→3`, `S2: 4→0`, `S5: 5→0` — ⚠️ see footnote †) · Tier 3 (`324k €` @ S1): 0 missed only with an unpriced cross-cabinet busbar tie; plugs alone = 8 missed** |
| **Grid Transformer Violations** | `0` official `grid_kw` overlimits (`9,644` rows under `delivered_kw/0.955` basis) | **0 violations** (`100.00%` compliance under 95.5% AC inverter guard; see [`docs/energy_impact.md`](./docs/energy_impact.md)) |

> **Engineering Honesty on S1 (`24` Overnight Buses on `12` Single-Gun Dispensers)**:  
> *"Zero missed departures is reachable in our model — but **not by buying more plugs**. Doubling S1 to 24 plug points (`324,000 EUR`, `13.31-year` standalone payback) actually makes it **worse**: `8` missed departures, because cabinet power stays at `1,080 kW` and each gun drops from `90 kW` to `45 kW`. Raising cabinet power to `3×450 kW` does reach zero, but the resulting `1,350 kW` peak exceeds the `1,200 kW` grid limit. The only zero-miss configuration that stays inside your grid limit is a cross-cabinet busbar tie on the existing 12 guns (peak stays `1,080 kW`) — and that component has no price in `equipment_costs.csv`, so we do not invent one. Our zero-CAPEX software closes 87.8% of the energy gap with zero manual replugs."*

| Scenario Day (`2026-11-13`) Tier | S1 Missed (`24` Night / `32` Total) | S1 Same-Engine Deficit (kWh) | S2 Missed | S5 Missed | Total Missed (`S1+S2+S5`) | CAPEX (€) | Human Replugs |
|---|---|---|---|---|---|---|---|
| **Tier 1: Official / FCFS Baseline** | `4` (`B04, B09, B18, B20`) | `398.5 kWh` *(Official 0-session gap: `1,012.00 kWh`)* | `4` (`283.50 kWh`) | `5` (`508.95 kWh`) | **13** | `0 €` | Baseline manual |
| **Tier 2: Zero-CAPEX Software (`urgency`)** | **3** (`B04, B09, B18`; `B20` saved) | **48.8 kWh (`-87.8%`)** | **0** (`0.0 kWh`) | **0** (`0.0 kWh`) | **3 (`10` saved)** | **0 €** | **0 moves** |
| **Tier 3a: +12 dispensers only (`24` plugs, no busbar)** | **8** (**worse**) | **1,040.1 kWh** | — | — | — | **324,000 €** (`13.31 yr` payback) | **0 moves** |
| **Tier 3b: +12 dispensers **and** cross-cabinet busbar tie** | **0** | **0.0 kWh (`-100.0%`)** | 0 | 0 | **0** | **324,000 € + unpriced busbar** | **0 moves** |
| **Tier 3c: cabinet upsizing `3×450 kW` (12 guns kept)** | **0** | **0.0 kWh** | — | — | — | **75,600 €** (`280 €/kW`) | 0 moves — ❌ peak `1,350 kW` > `1,200 kW` grid limit |

*(Note: A counterfactual `01:30` manual batch swap [Track A2 in `src/core/virtual_replug.py`] would require 11–12 human yard moves at 01:30 AM, violating Rule 3 zero-touch autonomy; it is retained solely as a theoretical stress test and excluded from autonomous claims.)*

---

## 🏛️ System Architecture: Three-Layered Hierarchy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      L3: AUTONOMOUS CLOUD ORCHESTRATOR (15-min horizon)                │
│  - 15-Minute Rolling Horizon MILP Optimizer (SciPy HiGHS Solver)                       │
│  - Nord Pool Day-Ahead Spot Arbitrage & Monthly Peak Demand Shaving (6.50/7.50 €/kW/mo)│
│  - Multi-Site Fleet Schedule Coordination & Outcome-Based SLA Clearing Engine         │
│  - Continuous SoC Slack ($z_v \in [0, 1]$) Preventing False Dropping at 799.30 €/MWh   │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ (WAN: OCPP 2.0.1 Smart Charging TxProfile)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   L2: STATION EDGE AUTONOMOUS CONTROLLER (100ms - 15min)               │
│  - Local Dynamic Load Management (DLM): 1,425 kW DC / 1,492.15 kW AC Inverter Guard    │
│  - 72-Hour Full Offline Islanding (Encrypted Append-Only WAL SQLite/NVMe)              │
│  -Predictive Thermal PdM: 199-minute lead-time threshold + slope extrapolation (59.3°C)│
│  - Sub-Zero (-18°C) Low-Temp Battery Pre-Heating Dynamic Diversion                     │
│  - Anti-Phantom Replug & Electrical Fingerprint Fraud Engine (<180s, ΔSoC < 1%, dI/dt) │
│  - Three-Way Config Reconciler (sites.csv vs power_cabinets.csv vs site_config.csv)    │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ (Local Bus: Modbus / CAN / Break-Before-Make)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   L1: PHYSICAL POWER HARDWARE & KEMPOWER DPR MATRIX                    │
│  - Kempower 25 kW / 50 kW Power Module Matrix with Millisecond-Scale BBM Relays        │
│  - Strict 1:N Power Cabinet Wiring (C1-1..C1-3 -> D1-1..D1-12, Zero Illegal Backfeeds) │
│  - 6-Step Break-Before-Make Zero-Arc Relay Sequencing (< 260ms Switching Envelope)    │
│  - Hard Physical Safety Interlocks: 65°C de-rate, 75°C trip, 90°C pin, 30mA RCD, IMD  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Technological & Architectural Innovations

### 1. Zero-Intervention Crisis Resolution on Scenario Day (Friday 2026-11-13)
- **S1 (Bus Depot North · 24 overnight buses / 32 total departures / 12 single-gun dispensers)**: 
  - **199-Minute Lead-Time Thermal PdM Alert**: At `2026-11-12T22:31:00+02:00`, Sentinel's threshold + slope extrapolation detector identifies Cabinet C1-3 fan bearing degradation (`59.3°C / 702 RPM`), **3 hours 19 minutes before warning F015** and 3h 54m before trip F016 (`246 min` physical technician replacement, `cleared_by = technician`).
  - **Tier 2 — Zero-CAPEX Software (`0 €` CAPEX, `0` human moves)**: Urgency-weighted MILP scheduling (`strategy="urgency"`) across the existing 12 single-gun posts (`cross_tie=False`) reduces missed departures from **`4` (`B04, B09, B18, B20`) to `3` (`B04, B09, B18` — `B20` rescued)** and cuts the same-engine energy deficit from **`398.5 kWh` to `48.8 kWh` (`-87.8%`)** (`7,473.5 -> 7,823.0 kWh` delivered, gun-hour utilization `45.38% -> 47.50%`, cabinet-hour utilization `68.03% -> 71.21%`).
  - **Tier 3 — 2029 Hardware Dual-Gun Expansion (`324,000 €` CAPEX, `0` human moves)**: Upgrading all 12 bays to dual-gun satellites (`24` simultaneous plug points @ `18,000 €` satellite + `9,000 €` civil works = `27,000 €/gun`, total `324,000 €` CAPEX strictly per `equipment_costs.csv`, `13.31-year` standalone payback against S1's `24,336 €/year` replug labor) **does not, by itself, achieve zero.** Tested alone it yields **`8` missed departures (`1,040.1 kWh`)** — worse than the 12-gun baseline — because cabinet power stays at `1,080 kW` and each gun drops from `90 kW` to `45 kW`. `0` missed requires **additionally** a cross-cabinet busbar tie (`cross_tie=True`), which is absent from `chargers.csv` and has **no price in `equipment_costs.csv`**. Cabinet upsizing is not an alternative: `3×450 kW` reaches `0` but peaks at `1,350 kW`, **above the `1,200 kW` grid limit**. **The only zero-miss configuration inside the grid limit is the busbar tie on the existing 12 guns (peak stays `1,080 kW`)** — see [`docs/attribution_matrix.md`](./docs/attribution_matrix.md) Option 2/3/5.
- **S2 (Logistics Depot East · 400 kW DSO Curtailment)**:
  - Dynamically throttles overnight trucks `T05–T08` to 1 kW, liberating an **1,857.06 kWh afternoon pool** to supply **283.50 kWh** to afternoon trucks `T01–T04`. All 4 trucks depart 100% on schedule (`4 -> 0` missed departures) despite the severe curtailment.
- **S3 (Highway Public Hub · 2-Hour Cellular Outage)**:
  - Overrides the naive `50 kW` fallback (`400 kW` total) by autonomously islanding at the edge to deliver **1,425 kW DC** (`1,492.15 kW AC <= 1,500 kW`). Crushes driver abandonment from **29.69% down to < 0.5%** (saving 76 stranded drivers).
- **S4 (Urban Public Hub · 799.30 €/MWh Spot Price Spike)**:
  - Employs dimensional scaling ($10^{-3}$) and continuous SoC slack ($z_v \in [0, 1]$, weight $10,000 \text{ €}$) to prevent vehicle abandonment during the Nord Pool price spike, keeping charging costs optimized without stranding drivers (same-engine shift-window simulation shows `-17.43%` energy cost and `-300 kW` peak reduction; see [`docs/energy_impact.md`](./docs/energy_impact.md)).
- **S5 (New Bus Depot · Three-Way Configuration Discrepancy)**:
  - Three-Way Config Reconciler detects that `site_config.csv` capped `grid_limit_kw` at `600 kW` while `sites.csv` and `power_cabinets.csv` specified `900 kW`. Auto-reconciliation unlocks **900 kW (+750 kWh)**, restores `D5-7` from 50 kW to 150 kW, and activates `D5-8`'s eSIM, turning 5 missed buses into **`0` missed departures (`0.0 kWh` deficit)**.

### 2. Industrial Standards & Open Protocols
- **OCPP 2.0.1 Smart Charging (`src/core/protocols.py`)**: Full support for `SetChargingProfileRequest` with `TxProfile`, `TxDefaultProfile`, and `ChargingStationMaxProfile`, plus Component-Variable telemetry via `NotifyEventRequest` for fan RPM, module temperatures, and insulation resistance.
- **ISO 15118-2/20 Plug & Charge (`src/core/protocols.py`)**: Mutual TLS 1.3 handshake completed in **< 1.5 seconds**, with ECDSA P-256 certificate path verification executed in **< 10 ms**. Eliminates physical RFID cards and mobile apps.
- **Anti-Phantom Replug & Fraud Defense (`src/core/anti_fraud.py`)**: Detects rapid reconnect intervals ($t < 180 \text{ s}$), SoC continuity ($\Delta \text{SoC} < 1.0\%$), and current ramp slew rates ($dI/dt > 100 \text{ A/s}$) to merge split sessions and prevent phantom billing.
- **Offline Discrete-Event Simulator (`src/sim/discrete_sim.py`)**: High-fidelity minute-by-minute offline discrete-event simulator modeling realistic battery charging acceptance curves, contactor state transitions, strict 1:N intra-cabinet boundaries (`cross_tie=False`), and dynamic power distribution.

### 3. Commercial CaaS Model & One-Page SLA Specification
- **The One-Page SLA (`One_Page_SLA_Specification.md`)**:
  - **Three Commercial Tiers**: **Titanium** ($\ge 99.90\%$ SLO, $< 50\text{ ms}$ reaction, 0-touch replug), **Gold** ($\ge 99.50\%$ SLO, $< 100\text{ ms}$ reaction), and **Silver** ($\ge 99.00\%$ SLO).
  - **Minimum Required Dwell Time (MRDT) Anti-Moral-Hazard Gate**: Protects CPOs from fraudulent delay claims by requiring:
    $$\text{MRDT}_j = \left( \frac{\frac{\text{SoC}_{\text{req}} - \text{SoC}_{\text{arrive}}}{100} \cdot E_{\text{batt}}}{\min(P_{\text{charger}}, P_{\text{veh}}) \cdot 0.95} \right) \cdot 60 + 15.0 \text{ min}$$
  - **150% Monthly Liability Cap**: Operators are protected by an absolute monthly payout ceiling ($\le 1.50 \times \text{Monthly Base Fee}$) and non-negative settlement invoicing.
  - **2029 Customer Story**: Features Pekka Virtanen, Fleet Operations Director at Lahti City Transit (LSL), running 24 electric articulated buses through a -18°C blizzard with zero on-site staff.

---

## ⚖️ Official Judging Dimension Alignment

| Criteria | Weight | Sentinel Technical Deliverable & Empirical Proof |
|---|---|---|
| **Degree of Autonomy** | **25%** | • **Scenario Day 3-Tier Autonomy**: Official `13` missed $\to$ **Tier 2 (`0 €` software, 0 moves): `3` missed (`10` saved; S1 `398.5 -> 48.8 kWh`, `-87.8%`)** $\to$ **Tier 3 (`324,000 €` S1 dual-gun expansion **+ unpriced cross-cabinet busbar tie**): `0` missed (`0.0 kWh` deficit) — plugs alone give `8`, worse)**.<br>• **199-minute lead-time thermal PdM** (`59.3°C / 702 rpm`, threshold + slope extrapolation).<br>• **Millisecond-scale BBM relay sequencing** (`< 10 ms` software decision, `85 ms` physical break-before-make) and 72-hour offline edge islanding.<br>• **20.76 FTE continuous human operations (`9.95 FTE` midnight replugs + `10.81 FTE` triage) eliminated**, while explicitly retaining scheduled physical technician replacement (`cleared_by = technician`). |
| **Energy & Grid Impact** | **20%** | • **0 official `grid_kw` overlimit violations across 134,400 rows** (`9,644` rows under `delivered_kw / 0.955` AC basis reconciled; see [`docs/energy_impact.md`](./docs/energy_impact.md)).<br>• **95-Site Network Evidence (`network_kpis.csv`)**: addresses `2,096.1 hours` of `hours_demand_above_grid_limit` across `72` sites where `peak_grid_kw == grid_limit_kw`.<br>• **Use of Available Energy**: S1 gun-hour utilization `45.38% -> 47.50%` (`+2.12 pp`), cabinet-hour `68.03% -> 71.21%` (`+3.18 pp`).<br>• **799.30 €/MWh price spike arbitrage** with continuous SoC slack; BESS/PV cost interface defined via `equipment_costs.csv` *(interface defined, not field-validated)*. |
| **Technical Credibility** | **20%** | • **OCPP 2.0.1 Smart Charging** & **ISO 15118 PnC TLS 1.3** (`< 10 ms` ECDSA PKI).<br>• **Anti-phantom replug defense** and **offline discrete-event simulator** (`src/sim/discrete_sim.py`).<br>• Strict 1:N cabinet-to-dispenser physical wiring (`cross_tie=False`) & 6-step BBM zero-arc sequencing.<br>• **431 pytest + 106 E2E (537 total)** automated tests with 100% pass rate. |
| **Commercial Viability** | **20%** | • **20.76 FTE continuous ops elimination saves 1,821,534 €/year** across 100 sites (`24,336 €/yr` at S1).<br>• Honest CAPEX: Tier 2 (`0 €` CAPEX, `-87.8%` S1 deficit) vs Tier 3 (`324,000 €`, `13.31-yr` standalone payback) — **and the finding that `324,000 €` of extra dispensers makes S1 worse (`8` missed), while the only zero-miss path inside the `1,200 kW` grid limit is an unpriced busbar tie.**<br>• **One-Page SLA** with Titanium/Gold/Silver tiers and MRDT anti-fraud gate.<br>• **150% monthly liability cap** and guaranteed non-negative settlement invoicing. |
| **Clarity** | **15%** | • **Interactive 4-View Streamlit Cockpit (`app.py`)** with live minute playback.<br>• **10-Minute Championship Pitch Deck (`PITCH_DECK_OUTLINE.md`)** with jury defense.<br>• Sub-second deterministic verifier (`verify_all.py` in **0.34s**) & dedicated [`docs/energy_impact.md`](./docs/energy_impact.md).<br>• Compelling 2029 customer story anchored in Lahti City Transit. |

---

## ⚡ Quick Start & Verification Commands

### 1. Environment Setup
```bash
# Recommended: Python 3.10+
pip install -r requirements.txt
```

### 2. Run the Deterministic Sub-Second Verifier (< 0.5s)
Runs the zero-regression gate verifying all S1–S5 scenarios, 29 GitHub Issue #2 items, and 134,400 grid power rows:
```bash
python verify_all.py
```
*(Executes in ~0.34 seconds with 100% PASS)*

### 3. Run the Full Pytest Suite (`431 pytest + 106 E2E (537 total)`)
Executes all unit, integration, protocol, and mathematical verification tests:
```bash
python -m pytest tests/ -q
```
*(431 passed in ~42 seconds)*

### 4. Run the Independent Opaque-Box E2E Test Suite (106 Tests)
Runs 106 independent tests across Tiers 1–4 (Feature coverage, boundaries, stress, scenarios):
```bash
python -m e2e_tests.test_runner
```
*(106/106 passed in ~0.65 seconds — unified total: `431 pytest + 106 E2E (537 total)`)*

### 5. Launch the Streamlit 4-View Command Center
Launches the interactive executive and engineering live cockpit:
```bash
streamlit run app.py
```
- **View 1: Executive Cockpit**: 2029 Customer Story, 20.76 FTE Elimination Waterfall & Portfolio SLA
- **View 2: Scenario Day Live Player**: 00:00–23:45 Scrubber, Live Incidents & Dynamic DPR Matrix
- **View 3: Hardware Matrix & Protocol Inspector**: 25kW Module Matrix, 2.63s Contactor BBM & OCPP/ISO Logs
- **View 4: Commercial SLA & Clearing**: Interactive MRDT Moral Hazard Calculator & Monthly Invoice Export

---

## 📂 Repository File Structure

```
hackson/
├── app.py                                    # 4-Quadrant Interactive Streamlit Command Center
├── verify_all.py                             # Sub-second (0.29s) deterministic verifier
├── requirements.txt                          # Packaging dependencies
├── PROJECT.md                                # Single source of engineering truth
├── PITCH_DECK_OUTLINE.md                     # 10-Minute Championship Pitch Deck & Jury Defense
├── One_Page_SLA_Specification.md             # 2029 Customer Story & Tiered One-Page SLA
├── README.md                                 # Main project documentation & quickstart
├── kempower-challenge/                       # STRICTLY READ-ONLY OFFICIAL DATASET
│   └── kempower-challenge-data/              # 45 CSV files, 240,635 rows (untouched)
├── src/                                      # Production core engine & models
│   ├── core/
│   │   ├── dpr_matrix.py                     # Kempower DPR Matrix & BBM Contactor Sequencing
│   │   ├── mpc_optimizer.py                  # 15-min Rolling Horizon HiGHS MILP Optimizer
│   │   ├── self_healing.py                   # Edge FSM, 199-min Thermal PdM & Islanding
│   │   ├── virtual_replug.py                 # S1 Strategy A (0 €) & Strategy B (324k €, plugs alone = 8)
│   │   ├── protocols.py                      # OCPP 2.0.1 Smart Charging & ISO 15118 PnC
│   │   └── anti_fraud.py                     # Anti-Phantom Replug & Electrical Fingerprinting
│   ├── sim/
│   │   ├── data_loader.py                    # Official 45 CSV Data Loader & Hash Verifier
│   │   ├── scenario_engine.py                # Closed-Loop Master Scenario Engine
│   │   └── discrete_sim.py                   # Minute-by-minute discrete event simulator
│   ├── commercial/
│   │   ├── roi_analyzer.py                   # 20.76 FTE Labor & CAPEX/OPEX Financial Model
│   │   ├── sla_calculator.py                 # MRDT & Outcome-Based SLA Billing Engine
│   │   ├── settlement_clearing.py            # B2B Tiered Monthly Settlement Engine & Hash Audit
│   │   └── sensitivity_analyzer.py           # Multi-Axis Sensitivity & Pure Python NPV/IRR Solver
│   └── utils/
│       └── paths.py                          # Cross-platform dynamic path resolver
├── docs/
│   ├── attribution_matrix.md                 # 16-cell S1/S2/S5 same-engine causal attribution matrix
│   └── energy_impact.md                      # Station-by-station energy, grid & utilization ledger
├── tests/                                    # 431 Pytest Unit & Integration Tests (537 total with E2E)
│   ├── test_commercial_settlement.py         # Commercial settlement, MRDT & sensitivity tests
│   ├── test_protocols_ocpp_iso.py            # OCPP 2.0.1 & ISO 15118 PnC tests
│   ├── test_anti_fraud_replug.py             # Anti-phantom replug & fraud tests
│   ├── test_discrete_sim_engine.py           # Discrete simulation validation tests
│   ├── test_github_issue2_29items.py         # 29-item GitHub Issue #2 audit tests
│   ├── test_scenario_verification.py         # S1–S5 Scenario Day crisis verification
│   ├── test_remediated_sla.py                # SLA piecewise deduction & MRDT tests
│   ├── test_m1_adversarial_probe.py          # Boundary, electrical & inverter tests
│   └── test_mpc_math_fixes.py                # MILP continuous slack & scaling tests
└── e2e_tests/                                # Independent Opaque-Box E2E Testing Track
    ├── test_runner.py                        # Standalone E2E Test Suite Runner
    ├── tier1_feature_coverage.py             # Tier 1: Feature Contract Coverage (45 tests)
    ├── tier2_boundary_corner.py              # Tier 2: Boundary & Corner Cases (40 tests)
    ├── tier3_cross_feature.py                # Tier 3: Pairwise Cross-Feature Interactions (12 tests)
    └── tier4_real_world_scenario.py          # Tier 4: Real-World Scenario Day Workloads (9 tests)
```

---

## 👥 Competition Team & Acknowledgments
- **Event**: LahtiES Energy Tech Hackathon (LUT University Lahti / CrazyTown, Nov 5–7, 2026)
- **Challenge Sponsor**: Kempower Oyj (Lahti, Finland)
- **Mentors & Jury**: Mats Mattsson, Panu Vartiainen, Iiro Kinnunen, Thet Zin, Chuong Pham, Paul Carlson
- **Integrity Statement**: All 45 official CSV files under `kempower-challenge-data/` remain strictly read-only and hash-verified. All hardware pricing is grounded strictly in `equipment_costs.csv`.

---

### † Baseline provenance for S2 / S5 (read this before quoting the numbers)

Only **S1** is same-engine calibrated: our discrete-event engine, run on the 12 physical CCS2 guns with FCFS, reproduces the official `departures_baseline.csv` **vehicle-for-vehicle** (`B04, B09, B18, B20`, `398.5 kWh`, peak `1,080 kW`). The `4 → 3` claim is therefore a **controlled A/B on one engine**.

**S2 and S5 are not calibrated in this way**, and we do not pretend otherwise:

| Station | Official record (`departures_baseline.csv`) | Our engine, FCFS (same engine) | Our engine, urgency | What the gain really is |
|---|---|---|---|---|
| S1 | 4 missed / 398.5 kWh | **4 missed / 398.5 kWh** (exact match) | 3 missed / 48.8 kWh | **Scheduling** (−87.8% deficit, B20 rescued) |
| S2 | 4 missed / 283.50 kWh | 1 missed / 24.0 kWh (T02) | 0 missed | **Scheduling** on our model (1 → 0); the `4` is the official record, not our baseline |
| S5 | 5 missed / 508.95 kWh | 0 missed at 900 kW; 1 missed / 21.5 kWh at 600 kW | 0 missed | **Configuration fix** (`600 → 900 kW`), not scheduling |

So when we say "`10` saved", `S1`'s one vehicle is proven end-to-end; `S2` and `S5` are the official record minus our optimized result, and their engines under-reproduce the official baseline. We treat this as an open item, not as a result.
