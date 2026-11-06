# Project: Kempower Self-Operating Charging Network (Kempower 自运行充电网络)

## Overview & Hackathon Winning Positioning
- **Event**: LahtiES Energy Tech Hackathon (LUT Lahti / CrazyTown)
- **Challenge**: Kempower Challenge ("The Self-Operating Charging Network")
- **Official Mentors / Judges**: Mats Mattsson (Kempower Cloud Software Leader & Judge), Panu Vartiainen (Kempower Expert)
- **Core Vision**: "If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"
- **Official Tasks**:
  1. Part 1: The Energy and Control Core (Multi-timescale optimization, grid limits, DPR modular routing, fault self-healing, edge islanding).
  2. Part 2: Scenario Day 2026-11-13 Demonstration with zero human intervention (S1 thermal fault, S3 WAN drop, S4 799.30 €/MWh price spike).
  3. Part 3: Commercial Model & One-Page SLA for 2029 (20.76 FTE recorded baseline -> 12.44 FTE software-addressable, 1.09M €/year claimable, 5.09 FTE technician visits retained, MRDT gating, capped risk).
- **Five Judging Dimensions**: Autonomy 25%, Energy & Grid Impact 20%, Technical Credibility 20%, Commercial Viability 20%, Clarity 15%.
- **Two Absolute Red Lines**:
  1. "Never change the data we gave": All 45 CSV files (240,635 rows) under `kempower-challenge-data/` remain strictly unmodified and read-only.
  2. "Count the cost": Any hardware expansion must be priced strictly per `equipment_costs.csv`.

---

## Architecture

```
                                  [Autonomous Cloud Orchestrator (L3)]
                    ┌───────────────────────────────┬───────────────────────────────┐
                    │ 15-min Rolling MPC Optimizer  │ Commercial ROI & SLA Engine   │
                    │ - Nord Pool Spot & Tariff Arb │ - MRDT Physical Gate Gating   │
                    │ - Anti-Phantom Replug Defense │ - Auto Monthly Settlement Gen │
                    │ - Fleet Timetable Co-opt      │ - 20.76 FTE Elimination Model │
                    └───────────────┬───────────────┴───────────────┬───────────────┘
                                    │ (WAN / OCPP 2.0.1 TxProfile)  │
                                    ▼                               ▼
                                  [Station Edge Controller (L2)]
                    ┌───────────────────────────────────────────────────────────────┐
                    │ Edge FSM & Autonomous Local DLM (100ms - 15min)               │
                    │ - 72h WAN Outage Disconnection Islanding (1,425 kW DC Local)  │
                    │ - Predictive Thermal Pre-derating (Lead time 199min @ 59.3°C) │
                    │ - 25 kW Module-Level Degradation Self-Healing & Rebalancing   │
                    │ - Nordic Sub-Zero (-15°C) Battery Pre-heating Dynamic Diversion│
                    │ - Three-Way Config Reconciler Auto-Commissioning              │
                    └───────────────────────────────┬───────────────────────────────┘
                                    │ (Modbus / CAN / IEC 61851)
                                    ▼
                                  [Physical Device Layer (L1)]
                    ┌───────────────────────────────────────────────────────────────┐
                    │ Kempower Modular DPR Matrix & Satellite Dispensers (<100ms)   │
                    │ - 25 kW / 50 kW Power Module Millisecond-Scale BBM Matrix     │
                    │ - 6-Step Break-Before-Make (BBM) Zero-Arc Switching Protocol  │
                    │ - Hardware Hard Interlocks (Over-temp 75°C, 30mA RCD, IMD)    │
                    │ - Dual-Gun Satellite Multiplexing (Eliminates Night Replug)   │
                    └───────────────────────────────────────────────────────────────┘
```

---

## Feature Inventory

Every feature identified during the comprehensive Phase 0 Survey is inventoried below and mapped to a specific implementation milestone:

| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| F01 | DPR Prefix Bug Fix | Fix `dpr_matrix.py` string prefix collision (`D1-10.startswith("D1-1")`), unlocking full 1,080 kW capacity for S1 12-gun simultaneous charging | M1 | survey_explorer_1 (P0-1) |
| F02 | App Launch Crash Fix | Fix `FileNotFoundError: finance_daily.csv` in `roi_analyzer.py:156` by computing peak vs energy directly from official CSVs | M1 | survey_explorer_1 (Runtime Defect) |
| F03 | Closed-Loop Discrete Simulation | Integrate `vision6-patch-1` (`edf_packer.py` / `new one`) discrete minute-by-minute simulation into `scenario_engine.py` to replace hardcoded `0` literals | M1 | survey_spec_miner_2 & survey_explorer_1 |
| F04 | Predictive Thermal Calibration | Calibrate `NOMINAL_FAN_RPM` (1,120/1,400) and trip temp (59.3°C) in `self_healing.py`, clean empty strings to eliminate 3,181 false alarms | M1 | survey_explorer_1 (P0-3) |
| F05 | Latent Defects Remediation | Fix P1-1 to P1-7 (switching delay 2.63s, 43 module topology, MILP gun capacity limit, rolling MPC peak fee, SLA threshold & non-negative invoice) | M1 | survey_explorer_1 (P1-1..P1-7) |
| F06 | Packaging & Requirements | Provide clean, complete `requirements.txt` for reproducible zero-friction setup | M1 | survey_explorer_1 (P0-4) |
| F07 | OCPP 2.0.1 Smart Charging Profile | Implement `SetChargingProfileRequest` (`TxProfile`, `TxDefaultProfile`, `ChargingStationMaxProfile`), `ChargingNeeds`, `ClearChargingProfile` | M2 | survey_spec_miner_2 (F11..F14) & survey_explorer_3 |
| F08 | OCPP 2.0.1 Device Monitoring | Implement Component-Variable device monitoring (`NotifyEventRequest`) for PowerModule, FanSpeed, Temperature, IMD | M2 | survey_spec_miner_2 (F15) |
| F09 | ISO 15118-2/20 Plug & Charge (PnC) | Mutual TLS 1.3 handshake (<1.5s), X.509 v3 certificate chain validation, and automated session authorization replacing RFID/app | M2 | survey_spec_miner_2 (F16) & survey_explorer_3 |
| F10 | Anti-Phantom Replug & Fraud Defense | Detect rapid reconnects (<180s), SoC continuity (<1.0%), and abnormal current ramps ($dI/dt > 100$ A/s) to merge sessions and block fraud | M2 | survey_explorer_3 (Blueprint 1) |
| F11 | 25 kW Module-Level DPR Self-Healing | Dynamic sub-100ms isolation of degraded 25 kW modules, intra-cabinet load rebalancing, and cycle aging duty rotation | M2 | survey_spec_miner_2 (F8) & survey_explorer_3 |
| F12 | Nordic Sub-Zero Low-Temp Self-Healing | Model battery low-temp acceptance curves (-15°C to 15°C) and dynamically divert DPR power to vehicle PTC heating, cutting cold charging time 35% | M2 | survey_explorer_3 (Blueprint 2) |
| F13 | Microgrid BESS/PV Coordinated Dispatch | Coordinated dispatch interface for optional 500 kWh / 250 kW BESS and solar PV smoothing against Nord Pool price spikes *(interface defined, not field-validated)* | M2 | survey_spec_miner_2 (F18..F20) |
| F14 | 72h WAL Offline Reconnection Sync | Encrypted local SQLite/NVMe Append-only WAL and idempotent reconciliation protocol upon WAN recovery with UUID tracking | M2 | survey_spec_miner_2 (F21) & survey_explorer_3 |
| F15 | Outcome-Based 2029 SLA Billing Engine | Compute MRDT physical gate, availability tiers, delay penalty credits, and automated monthly settlement invoice generator | M3 | survey_spec_miner_2 (F23..F24) & survey_explorer_3 |
| F16 | Commercial ROI & Sensitivity Dashboard | Full 100-station network CAPEX/OPEX/NPV/IRR model, 20.76 FTE elimination breakdown, and interactive parameter sensitivity analysis | M3 | survey_spec_miner_2 (F25) & survey_explorer_3 |
| F17 | Streamlit 4-View Interactive Cockpit | Dynamic Streamlit cockpit (`app.py`): Executive Cockpit, Scenario Day 2026-11-13 Minute-by-Minute Live Player, Hardware Matrix & Protocol Inspector, SLA Clearing | M3 | survey_explorer_3 (Blueprint 4) |
| F18 | 2029 Customer Story & Pitch Materials | Deliverables for judging presentation: 10-minute pitch deck structure, 2029 customer story narrative, one-page SLA agreement | M3 | survey_spec_miner_2 (F4) & Kickoff PPTX |
| F19 | 100% Zero-Regression Verification | Ensure all `433 pytest + 106 E2E (539 total)` tests and `verify_all.py` (0.34s) 100% pass without any functional regression | M4 | ORIGINAL_REQUEST (R4) |
| F20 | Opaque-Box E2E Test Suite (Tiers 1-4) | Comprehensive independent requirement-driven test suite (>=50 tests across Tiers 1-4) published via `TEST_READY.md` | E2E | ORIGINAL_REQUEST (R4) & Project Pattern |
| F21 | Adversarial Coverage Hardening (Tier 5) | White-box adversarial edge-case stress tests generated by Challenger agents to verify boundary resilience | M4 | Project Pattern (Final Milestone Phase 2) |

---

## Milestones

| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Core Remediation & Discrete Sim Engine | Fix P0-1 prefix bug, fix `app.py` crash, integrate closed-loop discrete simulation, calibrate thermal parameters, fix P1-1..P1-7, add requirements.txt (F01-F06) | none | DONE (230/230 pytest, verify_all.py, 106 E2E, app.py clean) |
| M2 | R3 High-Value Innovation Protocols & Hardware Self-Healing | OCPP 2.0.1 smart charging & device monitoring, ISO 15118 PnC TLS 1.3 handshake, Anti-Phantom replug defense, 25kW module DPR self-healing, Nordic sub-zero heating, BESS/PV microgrid interface, 72h WAL reconciliation (F07-F14) | M1 | DONE (307/307 pytest, 106 E2E, 29/29 verify_all in 0.29s, clean audit) |
| M3 | Commercial Settlement, Pitch Deliverables & Interactive UI Cockpit | SLA monthly settlement statement generator, ROI/NPV/IRR model, 4-view dynamic Streamlit cockpit (`app.py`), 2029 customer story and pitch deck materials (F15-F18) | M2 | DONE (348/348 pytest, 106 E2E, verify_all in 0.28s, clean audit) |
| M4 | Final Integration, Zero-Regression Verification & Adversarial Hardening | 100% pass across all tests (`433 pytest + 106 E2E (539 total)`), `verify_all.py`, all new module tests, 100% pass on E2E test suite (Tiers 1-4), adversarial hardening (Tier 5) (F19, F21) | M3, E2E | DONE (433 pytest + 106 E2E [539 total], 29/29 verify_all in 0.34s, clean final audit) |
| E2E | Independent E2E Testing Track | Design test runner, Tiers 1-4 opaque-box test cases for all features, publish `TEST_INFRA.md` and `TEST_READY.md` (F20) | none (parallel) | DONE (106/106 tests passed in 0.41s, TEST_READY.md published) |

---

## Interface Contracts

### `src.core.protocols` ↔ `src.core.mpc_optimizer`
- `build_ocpp_tx_profile(schedule: VehicleSchedule, interval_minutes: int = 15) -> Dict[str, Any]`:
  - Returns a valid OCPP 2.0.1 `SetChargingProfileRequest` JSON dictionary with `TxProfile`, `Relative` kind, and period limit array in Watts.
- `parse_charging_needs(charging_needs_payload: Dict[str, Any]) -> VehicleSchedule`:
  - Parses vehicle departure time, required energy (kWh), min/max current, and converts into MPC scheduling boundary constraints.

### `src.core.protocols` ↔ `src.core.self_healing`
- `verify_iso15118_handshake(cert_chain_pem: str, session_id: str) -> Tuple[bool, str]`:
  - Validates TLS 1.3 certificate chain, returns authorization status (`Accepted` or `CertificateRevoked`) and contract ID.
- `anti_phantom_replug_check(prev_session: Dict[str, Any], new_session: Dict[str, Any]) -> Tuple[bool, Dict[str, Any]]`:
  - Computes reconnect delta time, SoC difference, and current ramp slope; returns `(is_phantom, merged_session)`.

### `src.core.dpr_matrix` ↔ `src.sim.scenario_engine`
- `allocate_intra_cabinet_continuous(requests_kw: Dict[str, float], grid_limit_kw: float) -> Tuple[Dict[str, float], Dict[str, Any]]`:
  - Quantizes and allocates DC power per dispenser respecting cabinet physical boundaries, exact regex gun mapping (`^D\d+-\d+$`), and total AC conversion efficiency (95.5%).
- `simulate_closed_loop_minute_by_minute(site_id: str, date: str) -> Dict[str, Any]`:
  - Executes minute-by-minute closed-loop offline discrete-event simulation (`src/sim/discrete_sim.py`), returning actual vehicle-by-vehicle SoC trajectories and dynamically verified missed departures (`3` at S1 under `0 €` 12-gun urgency [`48.8 kWh` deficit vs `398.5 kWh` FCFS baseline], `0` at S1 with 24-plug expansion, and `0` at S2 & S5).

### `src.commercial` ↔ `app.py`
- `generate_monthly_settlement(site_id: str, month: str) -> Dict[str, Any]`:
  - Generates verifiable itemized audit invoice: base uptime fee, MRDT-eligible penalty deductions, and net payable amount (non-negative, capped at 150%).
- `get_dynamic_scenario_playback_frame(timestamp_minute: int) -> Dict[str, Any]`:
  - Returns instantaneous state vector for Streamlit live player: active dispensers, kW per vehicle, DPR contactor matrix state, grid load, spot price, and active alarms.

---

## Code Layout

```
kempower-self-operating-network/
├── app.py                           # Refactored 4-View Interactive Streamlit Cockpit
├── verify_all.py                    # Deterministic Verifier (<0.5s, 0-regression gate)
├── requirements.txt                 # Packaging dependencies
├── PROJECT.md                       # Single source of truth: architecture, milestones, interfaces
├── One_Page_SLA_Specification.md    # 2029 Commercial SLA Contract specification
├── kempower-challenge/              # STRICTLY READ-ONLY OFFICIAL DATASET (45 CSVs)
│   └── kempower-challenge-data/     # 45 CSV files, 240,635 rows (untouched)
├── src/
│   ├── core/
│   │   ├── dpr_matrix.py            # Kempower Modular DPR Matrix & Contactor Sequencing
│   │   ├── mpc_optimizer.py         # 15-minute Rolling Horizon MILP Optimizer
│   │   ├── self_healing.py          # Edge FSM, Thermal PdM & Islanding Controller
│   │   ├── virtual_replug.py        # Dual-Gun Satellite Multiplexing & Replug Elimination
│   │   ├── protocols.py             # [NEW] OCPP 2.0.1 Profiles & ISO 15118 PnC Engine
│   │   └── anti_fraud.py            # [NEW] Anti-Phantom Replug & Electrical Fingerprinting
│   ├── sim/
│   │   ├── data_loader.py           # Official Dataset CSV Loader & Ground Truth
│   │   ├── scenario_engine.py       # Closed-Loop Master Scenario Engine (with Discrete Sim)
│   │   └── discrete_sim.py          # [NEW] Minute-by-minute discrete event simulator (edf_packer)
│   ├── commercial/
│   │   ├── roi_analyzer.py          # Labor & CAPEX/OPEX Financial Model
│   │   ├── sla_calculator.py        # MRDT & Outcome-Based SLA Billing Engine
│   │   └── settlement_clearing.py   # [NEW] Automated Monthly Audit Settlement Statement Gen
│   └── utils/
│       └── paths.py                 # Dynamic Root & Path Resolver
├── tests/                           # Regression & Unit Test Suites (433 pytest + 106 E2E [539 total])
│   ├── test_adversarial_m1.py
│   ├── test_e2e_suite.py
│   ├── test_github_issue2_29items.py
│   ├── test_m1_adversarial_probe.py
│   ├── test_mpc_math_fixes.py
│   ├── test_remediated_sla.py
│   ├── test_sla_edge_cases.py
│   ├── test_protocols_ocpp_iso.py   # [NEW] Test suite for OCPP 2.0.1 and ISO 15118
│   ├── test_anti_fraud_replug.py    # [NEW] Test suite for anti-phantom replug
│   ├── test_discrete_sim_engine.py  # [NEW] Test suite for minute-by-minute discrete sim
│   └── test_commercial_settlement.py# [NEW] Test suite for monthly SLA settlement
└── e2e_tests/                       # [NEW] Independent Opaque-Box E2E Testing Track (Tiers 1-4)
    ├── test_runner.py               # E2E Test Suite Runner
    ├── tier1_feature_coverage.py    # Tier 1: >=5 tests per feature
    ├── tier2_boundary_corner.py     # Tier 2: Boundary & Corner tests
    ├── tier3_cross_feature.py       # Tier 3: Pairwise feature interactions
    └── tier4_real_world_scenario.py # Tier 4: Real-world Scenario Day full workloads
```
