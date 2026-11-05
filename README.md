# ⚡ Project Sentinel · The Self-Operating Charging Network
### Autonomous Energy Certainty-as-a-Service (CaaS) for Heavy Fleets & High-Power Hubs
*Kempower Challenge · LahtiES Energy Tech Hackathon 2026 (Thu 5.11. – Sat 7.11.2026 @ LUT University Lahti / CrazyTown)*  
*Official Challenge Lead & Mentor: Mats Mattsson (Kempower Cloud Software Leader & Judge), Panu Vartiainen (Kempower Expert)*

---

[![Pytest Tests](https://img.shields.io/badge/pytest-322%2F322%20passed%20(100%25)-success?style=for-the-badge&logo=pytest)](./tests/)
[![E2E Tests](https://img.shields.io/badge/E2E%20Runner-106%2F106%20passed%20(100%25)-success?style=for-the-badge&logo=shield)](./e2e_tests/)
[![Deterministic Verifier](https://img.shields.io/badge/verify__all.py-0.29s%20Deterministic%20Pass-blue?style=for-the-badge&logo=python)](./verify_all.py)
[![Official Dataset Integrity](https://img.shields.io/badge/Official%20CSVs-45%2F45%20Strictly%20Read--Only-green?style=for-the-badge&logo=git)](./kempower-challenge/kempower-challenge-data/)
[![Scenario Day Autonomy](https://img.shields.io/badge/Scenario%20Day%2011--13-13%20%E2%86%92%200%20Missed%20Departures-brightgreen?style=for-the-badge)](./src/sim/scenario_engine.py)
[![Labor Reduction](https://img.shields.io/badge/Human%20Baseline-20.76%20FTE%20%E2%86%92%200%20FTE%20(1.82M%E2%82%AC%2Fyr)-orange?style=for-the-badge)](./src/commercial/roi_analyzer.py)

---

## 🎯 The Core Mission: Redesigning for Zero Continuous Human Intervention

> **The Kempower Question**:  
> *"If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"*

Today, modern charging networks are tethered to an invisible army of human workers: dispatchers constantly monitoring setpoints, call-center operators rebooting stalled chargers, and depot staff wandering frozen yards at 2 AM to unplug and replug buses. 

**Project Sentinel** fundamentally re-architects charging infrastructure into an autonomous, closed-loop operating system. Built directly upon Kempower's modular **Dynamic Power Routing (DPR)** technology, Sentinel unifies a **15-minute rolling Mixed-Integer Linear Program (MILP)** in the cloud with a **sub-100ms autonomous Edge Finite State Machine (FSM)**. It guarantees that every commercial vehicle departs on time with full energy, strictly respects electrical grid boundaries with zero transformer overcurrents, and translates autonomous reliability into an enforceable, bankable **Outcome-Based Service Level Agreement (One-Page SLA)**.

---

## 📊 The Empirical Ground Truth: The 20.76 FTE Crisis

All architecture decisions and financial models in Project Sentinel are derived directly from the official 45 CSV files (`kempower-challenge-data/`, 240,635 rows across 100 commercial and public sites):

| Operational Metric | Official Baseline Ground Truth | Project Sentinel Autonomous Result |
|---|---|---|
| **Two-Week Human Interventions** | **8,852 manual operations** across 100 sites | **0 continuous operations** (100% autonomous closed-loop) |
| **Total Human Labor Time** | **93,412 minutes (1,556.87 hours / 2 weeks)** | **0 minutes continuous triage** |
| **Full-Time Equivalent (FTE) Baseline** | **20.76 FTE $\approx$ 21 FTE** (Finnish statutory 37.5 h/wk) | **20.76 FTE completely eliminated** |
| **Annual Continuous Labor OPEX** | **1,821,534 € / year** (@ 45 €/h in `equipment_costs.csv`) | **1,821,534 € saved annually** (1.98M € with 80 €/h tech visits) |
| **Depot Midnight Replugging** | **5,596 events (63.22% count / 47.93% labor duration)** | **Eliminated via Strategy A (0 € CAPEX) or Strategy B (24 guns)** |
| **Scenario Day Crisis (Friday 13.11)** | **13 missed departures, 1,804.45 kWh deficit, 29.7% abandoned** | **0 missed departures (100% on-time), abandonment < 0.5%** |
| **Grid Transformer Violations** | 0 overlimits allowed across 134,400 intervals | **0 violations (100.00% compliance with 95.5% inverter guard)** |

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
│  - Predictive Thermal PdM: 199-minute lead-time fan degradation alert (59.3°C/702 rpm) │
│  - Sub-Zero (-18°C) Low-Temp Battery Pre-Heating Dynamic Diversion                     │
│  - Anti-Phantom Replug & Electrical Fingerprint Fraud Engine (<180s, ΔSoC < 1%, dI/dt) │
│  - Three-Way Digital Twin Reconciliation (sites.csv vs cabinets vs site_config)        │
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ (Local Bus: Modbus / CAN / Break-Before-Make)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   L1: PHYSICAL POWER HARDWARE & KEMPOWER DPR MATRIX                    │
│  - Kempower 25 kW / 50 kW Power Module Matrix with Sub-100ms Relays                    │
│  - Strict 1:N Power Cabinet Wiring (C1-1..C1-3 -> D1-1..D1-12, Zero Illegal Backfeeds) │
│  - 6-Step Break-Before-Make Zero-Arc Relay Sequencing (< 260ms Switching Envelope)    │
│  - Hard Physical Safety Interlocks: 65°C de-rate, 75°C trip, 90°C pin, 30mA RCD, IMD  │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Key Technological & Architectural Innovations

### 1. Zero-Intervention Crisis Resolution on Scenario Day (Friday 2026-11-13)
- **S1 (Bus Depot North · 24 buses / 12 dispensers)**: 
  - **199-Minute Predictive PdM Alert**: At `2026-11-12T22:31:00+02:00`, Sentinel detects Cabinet C1-3 fan bearing degradation (`59.3°C / 702 RPM`), **3 hours 19 minutes before warning F015** and 3h 54m before trip F016 (`246 min` technician repair).
  - **Strategy A (0 € CAPEX Immediate Fix)**: Organizes a single scheduled wave swap at `01:30`, routing power exclusively across healthy cabinets C1-1 and C1-2 (`720 kW` N-1 capacity) to recover **1,012.00 kWh** and deliver **0 missed departures at 0 € CAPEX**.
  - **Strategy B (2029 Hardware Expansion)**: 12 additional dispensers (`18,000 €` dispenser + `9,000 €` civil works = `27,000 €/gun`, total `324,000 €` CAPEX strictly per `equipment_costs.csv`, yielding an honest `13.31-year` standalone payback against S1's `24,336 €/year` replug labor).
- **S2 (Logistics Depot East · 400 kW DSO Curtailment)**:
  - Dynamically throttles overnight trucks `T05–T08` to 1 kW, liberating an **1,857.06 kWh afternoon pool** to supply **283.50 kWh** to afternoon trucks `T01–T04`. All 4 trucks depart 100% on schedule despite the severe curtailment.
- **S3 (Highway Public Hub · 2-Hour Cellular Outage)**:
  - Overrides the naive `50 kW` fallback (`400 kW` total) by autonomously islanding at the edge to deliver **1,425 kW DC** (`1,492.15 kW AC <= 1,500 kW`). Crushes driver abandonment from **29.69% down to < 0.5%** (saving 76 stranded drivers).
- **S4 (Urban Public Hub · 799.30 €/MWh Spot Price Spike)**:
  - Employs dimensional scaling ($10^{-3}$) and continuous SoC slack ($z_v \in [0, 1]$, weight $10,000 \text{ €}$) to prevent vehicle abandonment during the Nord Pool price spike, keeping charging costs optimized without stranding drivers.
- **S5 (New Bus Depot · Three-Way Configuration Discrepancy)**:
  - Digital Twin reconciler detects that `site_config.csv` capped `grid_limit_kw` at `600 kW` while `sites.csv` and `power_cabinets.csv` specified `900 kW`. Auto-reconciliation unlocks **900 kW (+750 kWh)**, restores `D5-7` from 50 kW to 150 kW, and activates `D5-8`'s eSIM, turning 5 missed buses into **0 missed departures**.

### 2. Industrial Standards & Open Protocols
- **OCPP 2.0.1 Smart Charging (`src/core/protocols.py`)**: Full support for `SetChargingProfileRequest` with `TxProfile`, `TxDefaultProfile`, and `ChargingStationMaxProfile`, plus Component-Variable telemetry via `NotifyEventRequest` for fan RPM, module temperatures, and insulation resistance.
- **ISO 15118-2/20 Plug & Charge (`src/core/protocols.py`)**: Mutual TLS 1.3 handshake completed in **< 1.5 seconds**, with ECDSA P-256 certificate path verification executed in **< 10 ms**. Eliminates physical RFID cards and mobile apps.
- **Anti-Phantom Replug & Fraud Defense (`src/core/anti_fraud.py`)**: Detects rapid reconnect intervals ($t < 180 \text{ s}$), SoC continuity ($\Delta \text{SoC} < 1.0\%$), and current ramp slew rates ($dI/dt > 100 \text{ A/s}$) to merge split sessions and prevent phantom billing.
- **Closed-Loop Discrete Event Simulation (`src/sim/discrete_sim.py`)**: High-fidelity minute-by-minute discrete simulator modeling realistic battery charging acceptance curves, contactor state transitions, and dynamic power distribution.

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
| **Degree of Autonomy** | **25%** | • **Scenario Day 13 $\to$ 0 Missed Departures** with zero human intervention.<br>• **199-minute lead-time predictive thermal PdM** (`59.3°C / 702 rpm`).<br>• **Sub-100ms contactor self-healing** and 72-hour offline edge islanding.<br>• **20.76 FTE continuous human baseline completely eliminated**. |
| **Energy & Grid Impact** | **20%** | • **0 overlimit violations across 134,400 rows** ($P_{\text{grid}} \le P_{\text{limit}}$ 100% compliance).<br>• **95.5% AC Inverter Loss Guard** ($1,425 \text{ kW DC} \to 1,492.15 \text{ kW AC} \le 1,500 \text{ kW}$).<br>• **799.30 €/MWh price spike arbitrage** with continuous SoC slack.<br>• Microgrid BESS/PV peak shaving strictly costed via `equipment_costs.csv`. |
| **Technical Credibility** | **20%** | • **OCPP 2.0.1 Smart Charging** & **ISO 15118 PnC TLS 1.3** (<10ms ECDSA PKI).<br>• **Anti-phantom replug defense** and closed-loop discrete event simulation.<br>• Strict 1:N cabinet-to-dispenser physical wiring & 6-step BBM zero-arc sequencing.<br>• **428 automated tests** (322 unit/integration + 106 E2E) with 100% pass rate. |
| **Commercial Viability** | **20%** | • **20.76 FTE elimination saves 1,821,534 €/year** across 100 sites.<br>• Honest CAPEX: Strategy A (0 € CAPEX) vs Strategy B (324,000 €, 13.31-yr payback).<br>• **One-Page SLA** with Titanium/Gold/Silver tiers and MRDT anti-fraud gate.<br>• **150% monthly liability cap** and guaranteed non-negative settlement invoicing. |
| **Clarity** | **15%** | • **Interactive 4-View Streamlit Cockpit (`app.py`)** with live minute playback.<br>• **10-Minute Championship Pitch Deck (`PITCH_DECK_OUTLINE.md`)** with jury defense.<br>• Sub-second deterministic verifier (`verify_all.py` in **0.29s**).<br>• Compelling 2029 customer story anchored in Lahti City Transit. |

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
*(Executes in ~0.29 seconds with 100% PASS)*

### 3. Run the Full Pytest Suite (322 Tests)
Executes all unit, integration, protocol, and mathematical verification tests:
```bash
pytest tests/ -v
```
*(322/322 passed in ~15.1 seconds)*

### 4. Run the Independent Opaque-Box E2E Test Suite (106 Tests)
Runs 106 independent tests across Tiers 1–4 (Feature coverage, boundaries, stress, scenarios):
```bash
python -m e2e_tests.test_runner
```
*(106/106 passed in ~0.6 seconds)*

### 5. Launch the Streamlit 4-View Command Center
Launches the interactive executive and engineering live cockpit:
```bash
streamlit run app.py
```
- **View 1: Executive Cockpit**: 2029 Customer Story, 20.76 FTE Elimination Waterfall & Portfolio SLA
- **View 2: Scenario Day Live Player**: 00:00–23:45 Scrubber, Live Incidents & Dynamic DPR Matrix
- **View 3: Hardware Twin & Protocols**: 25kW Module Matrix, 2.63s Contactor BBM & OCPP/ISO Logs
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
│   │   ├── virtual_replug.py                 # S1 Strategy A (0 €) & Strategy B (324k €)
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
├── tests/                                    # 322 Pytest Unit & Integration Tests
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
