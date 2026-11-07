# ⚡ Project Sentinel · The Self-Operating Charging Network
### Autonomous Energy Certainty-as-a-Service (CaaS) for Heavy Fleets & High-Power Hubs
*Kempower Challenge · LahtiES Energy Tech Hackathon 2026 (Thu 5.11. – Sat 7.11.2026 @ LUT University Lahti / CrazyTown)*  
*Official Challenge Lead & Mentors: Mats Mattsson (Kempower Cloud Software Leader & Judge), Panu Vartiainen (Kempower Expert)*

> **Design Perspective**: As required by the challenge brief (*"Pick the perspective you design from… and say which one you chose"*; kickoff slide 15 defines this row as `Manufacturer — Builds the chargers / Often services them`), Project Sentinel designs from the **equipment supplier / service provider** perspective — the party that delivers and services charging networks across all sites. In `contracts.csv`, **18 of 29 contracts include service scope**, and a separate **18 carry non-zero contractual penalty clauses** (150 €/late departure at C1, up to 250 €). Every performance metric is denominated in field-service hours and contractual penalties across the three layers the supplier controls: dispenser firmware (`L1`), site controller (`L2`), and cloud orchestrator (`L3`). Our counterparties include `C1` City Bus Operator (`S1; S5`), `C2` Logistics Fleet (`S2`), and `C3` Charge Point Operator (`S3; S4`).
>
> **Data Notice**: All metrics in this repository are deterministically computed from the official **synthetic** `kempower-challenge-data` pack (45 CSV files, 240,635 rows).

---

[![Pytest Tests](https://img.shields.io/badge/pytest-462%20passed%20(100%25)-success?style=for-the-badge&logo=pytest)](./tests/)
[![E2E Tests](https://img.shields.io/badge/E2E%20Runner-106%20passed%20(568%20total)-success?style=for-the-badge&logo=shield)](./e2e_tests/)
[![Deterministic Verifier](https://img.shields.io/badge/verify__all.py-0.38s%20Deterministic%20Pass-blue?style=for-the-badge&logo=python)](./verify_all.py)
[![Official Dataset Integrity](https://img.shields.io/badge/Official%20CSVs-45%2F45%20Strictly%20Read--Only-green?style=for-the-badge&logo=git)](./kempower-challenge/kempower-challenge-data/)
[![Scenario Day Autonomy](https://img.shields.io/badge/Scenario%20Day%20(0%E2%82%AC)-S1%204%E2%86%923%20%C2%B7%20S2%204%E2%86%920%20%C2%B7%20S5%205%E2%86%920-brightgreen?style=for-the-badge)](./src/sim/scenario_engine.py)
[![Labor Reduction](https://img.shields.io/badge/Human%20Baseline-20.76%20FTE%20(12.44%20software--able)-orange?style=for-the-badge)](./src/commercial/roi_analyzer.py)
[![Zero-CJK Compliance](https://img.shields.io/badge/Zero--CJK%20Audit-100%25%20Pure%20English%20Verified-purple?style=for-the-badge)](./tools/cjk_audit.py)

---

## 🎯 The Core Mission: Redesigning for Zero Continuous Human Intervention

> **The Kempower Question**:  
> *"If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"*

Today, modern charging networks are tethered to an invisible army of human workers: dispatchers constantly monitoring setpoints, call-center operators rebooting stalled chargers, and depot staff wandering frozen yards at 2 AM to unplug and replug buses. 

**Project Sentinel** fundamentally re-architects charging infrastructure into an autonomous, closed-loop operating system. Built directly upon Kempower's modular **Dynamic Power Routing (DPR)** technology, Sentinel unifies a **15-minute rolling Mixed-Integer Linear Program (MILP)** in the cloud with a **sub-100ms autonomous Edge Finite State Machine (FSM)**. It guarantees that every commercial vehicle departs on time with full energy, strictly respects electrical grid boundaries with zero transformer overcurrents, and translates autonomous reliability into an enforceable, bankable **Outcome-Based Service Level Agreement (One-Page SLA)**.

---

## 🏛️ System Architecture: Three-Layered Hierarchy

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                      L3: AUTONOMOUS CLOUD ORCHESTRATOR (15-min horizon)                │
│  - 15-Minute Rolling Horizon MILP Optimizer (SciPy HiGHS Solver Backend)               │
│  - 15-min Spot Arbitrage (official synthetic prices.csv) & Monthly Peak Demand Shaving │
│  - Multi-Site Fleet Schedule Coordination & Outcome-Based SLA Clearing Engine         │
│  - Continuous SoC Slack (z_v in [0, 1], 10,000 € penalty) Preventing Divergence at 799.30 €/MWh│
└───────────────────────────────────────────┬────────────────────────────────────────────┘
                                            │ (WAN: OCPP 2.0.1 Smart Charging TxProfile)
                                            ▼
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                   L2: STATION EDGE AUTONOMOUS CONTROLLER (100ms - 15min)               │
│  - Local Dynamic Load Management (DLM): 1,425 kW DC / 1,492.15 kW AC Inverter Guard    │
│  - 72-Hour Full Offline Islanding (Encrypted Append-Only WAL SQLite/NVMe)              │
│  - Predictive Thermal PdM: 199-minute lead-time threshold + slope extrapolation (59.3°C)│
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

## 🔬 6 Battle-Tested Failure Scenarios Benchmark Results

Project Sentinel was rigorously evaluated against the 6 critical operational failure scenarios defined in the challenge, reproducing official baseline failures and proving autonomous self-healing:

| Scenario & Target Station | Operational Challenge & Physical Anomaly | Official Baseline Result | Project Sentinel Autonomous Result | Key Architectural Mechanism |
|---|---|---|---|---|
| **Scenario 1: S1 Bus Depot North** | Sub-zero (-18°C) overnight charging with Cabinet C1-3 thermal trip at 02:25 | 4 missed bus departures (`B04, B09, B18, B20`), 398.5 kWh deficit | **3 missed departures (`-87.8%` deficit, B20 rescued)** under 0-CAPEX software; **0 missed** with 24-point busbar | 199-min lead time PdM alert (59.3°C / 702 RPM), 260ms BBM relay transfer, urgency waterfilling |
| **Scenario 2: S2 Logistics Depot East** | DSO grid curtailment to 400 kW during 16:00–19:00 afternoon rush | 4 missed truck departures (`T01–T04`), 283.50 kWh deficit | **0 missed departures (100% on-time departures)** | Dynamic preemption: throttles overnight trucks T05–T08, releasing 1,857.06 kWh pool to afternoon trucks |
| **Scenario 3: S3 Highway Public Hub** | Complete 2-hour cellular WAN outage (11:00–13:00) during peak traffic | Fallback throttles to 50 kW/gun (500 kW site total), 29.69% abandonment | **1,425 kW DC sustained output (2.85× capacity gain)** | Autonomous edge islanding, local DLM enforcing $\eta=0.955$ AC ceiling (1,492.15 kW AC $\le$ 1,500 kW) |
| **Scenario 4: S4 Urban Public Hub** | Extreme wholesale spot electricity price spike to **799.30 €/MWh** at 18:00 | Uncontrolled charging incurred massive spot tariffs; naive MILPs drop vehicles | **0 dropped vehicles, 100% departure SoC $\ge 90\%$** | HiGHS MILP with continuous SoC slack ($z_v \in [0, 1]$, 10,000 € penalty) and $10^{-3}$ dimensional scaling |
| **Scenario 5: S5 New Bus Depot** | Commissioning misconfiguration: `site_config.csv` capped grid limit to 600 kW vs 900 kW physical | 5 missed bus departures (`508.95 kWh` uncharged deficit) | **0 missed departures (100% deficit recovered)** | Three-Way Config Reconciler auto-detects discrepancy, restores 900 kW rating and awakens D5-8 eSIM |
| **Scenario 6: S1 Hardware Expansion** | Evaluating 12 $\to$ 24 dispenser expansion under 1,080 kW cabinet limit | Doubling plugs alone yields **8 missed departures** (worse!) due to power starvation | **0 missed departures** achieved via cross-cabinet busbar tie | Proves hardware expansion requires cross-cabinet dynamic power routing rather than redundant plugs |

---

## 💼 SLA Commercial Model & Economics

### 1. 20.76 FTE Labor Deconstruction
Analysis of all 8,852 intervention rows in `operations_log.csv` reveals total human labor of 93,412 minutes (1,556.87 hours / 2 weeks), equivalent to **20.76 FTE** (Finnish statutory 37.5 h/wk) costing **1,821,534 €/year** (@ 45.00 €/h):

```
Total Labor Baseline: 20.76 FTE (1,821,534 €/year)
├── [CLAIMED] Software-Addressable: 12.44 FTE (59.95% / 1,091,850 €/year)
│   ├── Midnight Yard Replugging: 9.95 FTE (5,596 events, 47.93% labor time)
│   ├── Manual Grid Load Adjustments: 2.28 FTE (684 events, 10.98% labor time)
│   ├── Remote System Resets: 0.16 FTE (73 events)
│   └── Manual Price Updates: 0.05 FTE (8 events)
├── [RETAINED] Field Technician Dispatches: 5.09 FTE (24.52% / 446,667 €/year)
│   └── 73 physical technician rollouts (cleared_by=technician, component swaps)
└── [RETAINED] Customer Service Contact: 3.22 FTE (15.53% / 282,558 €/year)
    └── 2,418 inbound user inquiries, addressed via self-service kiosk app
```

### 2. The One-Page Service Level Agreement (One-Page SLA)
Project Sentinel delivers an outcome-based commercial contract backed by mathematical verification:
- **Titanium Tier**: $\ge 99.90\%$ Service Level Objective (SLO), $< 50\text{ ms}$ switching reaction, 0-touch autonomous replug.
- **Gold Tier**: $\ge 99.50\%$ SLO, $< 100\text{ ms}$ reaction.
- **Silver Tier**: $\ge 99.00\%$ SLO.
- **Minimum Required Dwell Time (MRDT §5.1) Anti-Moral-Hazard Gate**: Protects operators against fraudulent claims:
  $$\text{MRDT}_j = \left( \frac{\frac{\text{SoC}_{\text{req}} - \text{SoC}_{\text{arrive}}}{100} \cdot E_{\text{batt}}}{\min(P_{\text{charger}}, P_{\text{veh}}) \cdot 0.95} \right) \cdot 60 + 15.0 \text{ min}$$
- **150% Monthly Liability Cap**: Operators are protected by an absolute monthly payout ceiling ($\le 1.50 \times \text{Monthly Base Fee}$) and guaranteed non-negative monthly billing.
- **2029 Customer Story**: Features Pekka Virtanen, Fleet Operations Director at Lahti City Transit (LSL), operating 24 electric articulated buses through sub-zero blizzards with zero depot staff.

---

## ⚡ Quick Start & Reproduction Commands

### 1. Environment Setup
```bash
# Recommended: Python 3.10+
pip install -r requirements.txt
```

### 2. Run the Deterministic Verifier (< 0.5s timed execution)
Executes 29 forensic validation routines across all 45 unedited official CSV files and 134,400 power rows:
```bash
python verify_all.py
```
*(Produces deterministic 100% PASS across S1–S5 scenarios, grid invariants, and ROI models in 0.38s of timed computation).*

### 3. Run the S1 Overnight Bus Depot Simulation
Compares ground truth baseline vs. autonomous counterfactual scheduling and cross-cabinet busbar redundancy:
```bash
python run_s1.py
```

### 4. Run the Independent Opaque-Box E2E Test Suite (106 Tests)
Validates contract coverage, boundary conditions, cross-feature stress, and Scenario Day workloads:
```bash
python -m e2e_tests.test_runner
```
*(106/106 passed in 0.73s).*

### 5. Run the Comprehensive Pytest Suite (462 Tests)
Executes all unit, integration, protocol, and adversarial simulation tests:
```bash
pytest tests/ -q
```
*(462 passed, 0 failures across 24 test suites).*

### 6. Launch the Interactive 4-View Streamlit Command Center
```bash
streamlit run app.py
```
- **View 1: Executive Cockpit**: 2029 Customer Story, 20.76 FTE Waterfall & Portfolio SLA.
- **View 2: Scenario Day Live Player**: 00:00–23:45 Scrubber, Live Incidents & Dynamic DPR Matrix.
- **View 3: Hardware Matrix & Protocol Inspector**: 25kW Module Matrix, 260ms BBM Relays & OCPP/ISO Logs.
- **View 4: Commercial SLA & Dispute Clearing**: Interactive MRDT Calculator & Monthly Invoice Export.

### 7. Launch the 6-Fault Micro-Replay Center
```bash
streamlit run demo_scenarios/app.py
```

---

## 📂 File Tree & Component Functional Dictionary

```
hackson/
├── app.py                                    # Master 4-View Interactive Streamlit Command Cockpit
├── verify_all.py                             # Deterministic verifier running 29 Issue #2 checks in < 0.5s
├── run_s1.py                                 # S1 Bus Depot overnight simulation & CAPEX/OPEX accounting
├── requirements.txt                          # Python packaging dependencies
├── pytest.ini                                # Pytest test runner configuration
├── PROJECT.md                                # Single source of engineering truth & technical architecture
├── HACKATHON.md                              # Challenge alignment, competition boundaries & judging rules
├── ZERO_HUMAN_DESIGN.md                      # Zero-human operational design specification
├── One_Page_SLA_Specification.md             # Long-form outcome-based CaaS SLA specification & 2029 story
├── Project_Sentinel_12pages_final.pptx       # 12-page championship presentation pitch deck
├── PITCH_DECK_OUTLINE_v2.md                  # Comprehensive pitch deck structure & jury defense guide
├── SUBMISSION_MANIFEST.md                    # SHA-256 cryptographic verification manifest
│
├── kempower-challenge/                       # STRICTLY READ-ONLY OFFICIAL CHALLENGE DATASET
│   └── kempower-challenge-data/              # 45 CSV files, 240,635 rows (unmodified, hash-verified)
│
├── src/                                      # Production core engine & models
│   ├── edf_packer.py                         # Continuous Earliest Deadline First (EDF) discrete simulator
│   ├── core/
│   │   ├── dpr_matrix.py                     # Kempower 25kW DPR dynamic routing matrix & contactor FSM
│   │   ├── mpc_optimizer.py                  # 15-minute rolling horizon HiGHS MILP optimizer with slack
│   │   ├── self_healing.py                   # 199-min thermal PdM, 260ms BBM sequencer & edge islanding
│   │   ├── virtual_replug.py                 # S1 Strategy A (0 € software) & Strategy B (324k € hardware)
│   │   ├── protocols.py                      # OCPP 2.0.1 Smart Charging & ISO 15118 PnC protocol stack
│   │   └── anti_fraud.py                     # Anti-phantom replug & MRDT §5.1 electrical fingerprint gate
│   ├── sim/
│   │   ├── data_loader.py                    # Official 45 CSV data loader & SHA-256 integrity verifier
│   │   ├── scenario_engine.py                # Closed-loop master scenario execution engine
│   │   ├── discrete_sim.py                   # High-fidelity minute-by-minute discrete event simulator
│   │   ├── night_replay.py                   # S1 overnight charging replay engine
│   │   ├── outage_replay.py                  # S3 highway hub WAN outage islanding replay engine
│   │   └── fault_replays.py                  # Multi-station fault injection & recovery harnesses
│   ├── commercial/
│   │   ├── roi_analyzer.py                   # 20.76 FTE labor accounting & CAPEX/OPEX payback models
│   │   ├── sla_calculator.py                 # Tiered SLA deduction & MRDT anti-moral-hazard engine
│   │   ├── settlement_clearing.py            # B2B monthly billing settlement & invoice clearing
│   │   └── sensitivity_analyzer.py           # Multi-axis NPV/IRR financial sensitivity engine
│   ├── ui/
│   │   └── replay_scene.py                   # Streamlit interactive visualization & rendering components
│   └── utils/
│       └── paths.py                          # Cross-platform deterministic dataset path resolver
│
├── docs/                                     # System whitepapers, reports & audit specifications
│   ├── PROJECT_AUDIT_REPORT.md               # Forensic system audit report across 5 evaluation dimensions
│   ├── energy_impact.md                      # Station-by-station energy ledger & 95-site network proof
│   ├── attribution_matrix.md                 # 16-cell S1/S2/S5 causal attribution matrix
│   ├── assumptions_and_additions.md          # Comprehensive dictionary of 20 engineering assumptions
│   ├── one_page_agreement.html               # Formatted One-Page SLA agreement (strictly 1 A4 page)
│   ├── one_page_agreement.md                 # Markdown source of One-Page SLA agreement
│   ├── demo_day/                             # Complete Demo Day operational & stage defense manual
│   │   ├── README.md                         # Demo Day master handbook index
│   │   ├── 00_pocket_cheat_sheet.md          # On-stage pocket reference card & golden quotes
│   │   ├── 01_stage_schedule_and_setup.md    # Minute-by-minute stage timing & hardware layout
│   │   ├── 02_team_roles_and_coordination.md # 4-person role matrix, handoff cues & console SOP
│   │   ├── 03_judge_personas_and_question_bank.md # 3 juror profiles & 14 hardcore questions
│   │   ├── 04_structured_defense_and_crisis_manual.md # 3-part structured defense & crisis protocols
│   │   ├── 05_live_demo_operational_sop.md   # Live console operator step-by-step SOP
│   │   └── 06_code_proof_and_authenticity_guide.md # Code-level proof & data authenticity guide
│   └── hackathon/                            # Official hackathon requirements, rules & submission guides
│       ├── BRIEF.md                          # Official challenge brief transcription
│       ├── BUILD_PLAN.md                     # Engineering build & delivery plan
│       ├── DECISIONS.md                      # Architectural decision log
│       ├── DEMO_SCRIPT.md                    # 120-second live presentation script
│       ├── JUDGING.md                        # Official evaluation criteria & weights
│       ├── RULES.md                          # Competition rules & perspective declaration
│       └── SUBMISSION.md                     # Deliverables checklist & submission criteria
│
├── demo_scenarios/                           # Battle-tested failure scenarios & micro-replay videos
│   ├── 1.Night replay.mp4                    # S1 overnight charging & thermal trip replay (1080p)
│   ├── 2.Outage replay.mp4                   # S3 cellular WAN outage & edge islanding replay (1080p)
│   ├── 3.Price spike replay.mp4              # S4 spot price spike (799.30 €/MWh) peak shaving replay
│   ├── 4.Curtailment replay.mp4              # S2 DSO curtailment (400 kW) preemption replay (1080p)
│   ├── 5.Cable fault replay.mp4              # S1 dispenser cable fault & BBM rerouting replay (1080p)
│   ├── 6.Commissioning replay.mp4            # S5 configuration reconciliation replay (1080p)
│   ├── presentation 1.mp4                    # Stage presentation rehearsal video part 1
│   ├── presentation 2.mp4                    # Stage presentation rehearsal video part 2
│   ├── app.py                                # Dedicated 6-scenario micro-replay Streamlit app
│   ├── SPEECH_SIX_SCENES.md                  # Comprehensive verbal presentation script for all 6 scenes
│   └── SPEECH_OVERHEAT_SCENE.md              # Deep-dive speech script for S1 thermal trip
│
├── tests/                                    # 462 Pytest automated unit, integration & adversarial tests
│   ├── test_commercial_settlement.py         # SLA calculations, MRDT & monthly clearing tests
│   ├── test_protocols_ocpp_iso.py            # OCPP 2.0.1 smart charging & ISO 15118 PnC tests
│   ├── test_anti_fraud_replug.py             # Anti-phantom replug & electrical fingerprint tests
│   ├── test_discrete_sim_engine.py           # Discrete-event simulation validation tests
│   ├── test_github_issue2_29items.py         # 29-item GitHub Issue #2 audit verification tests
│   ├── test_demo_day_simulation.py           # Demo Day operational manual & role matrix tests
│   ├── test_remediated_sla.py                # SLA piecewise deduction & MRDT tests
│   ├── test_m1_adversarial_probe.py          # Boundary conditions & electrical safety tests
│   ├── test_mpc_math_fixes.py                # HiGHS MILP slack & convex convergence tests
│   └── ...                                   # Additional integration & stress testing modules
│
├── e2e_tests/                                # Independent opaque-box end-to-end testing suite
│   ├── test_runner.py                        # Standalone E2E runner executing all 4 tiers
│   ├── tier1_feature_coverage.py             # Tier 1: Core feature contract tests (45 tests)
│   ├── tier2_boundary_corner.py              # Tier 2: Boundary, stress & corner cases (40 tests)
│   ├── tier3_cross_feature.py                # Tier 3: Pairwise cross-feature interactions (12 tests)
│   └── tier4_real_world_scenario.py          # Tier 4: Scenario Day real-world workloads (9 tests)
│
└── tools/                                    # Engineering analysis & auditing scripts
    ├── cjk_audit.py                          # Automated CJK character scanner guaranteeing zero CJK
    ├── s1_multicabinet_sim.py                # S1 multi-cabinet discrete simulation script
    ├── export_deck_ledger.py                 # Presentation deck data ledger generator
    └── check_demo_artifacts.py               # Video & presentation asset validator
```

---

## 👥 Competition Team & Acknowledgments

- **Event**: LahtiES Energy Tech Hackathon (LUT University Lahti / CrazyTown, Nov 5–7, 2026)
- **Challenge Sponsor**: Kempower Oyj (Lahti, Finland)
- **Mentors & Jury**: Mats Mattsson, Panu Vartiainen, Iiro Kinnunen, Thet Zin, Chuong Pham, Paul Carlson
- **Integrity Statement**: All 45 official CSV files under `kempower-challenge-data/` remain strictly read-only and hash-verified. All hardware pricing is grounded strictly in `equipment_costs.csv`.
