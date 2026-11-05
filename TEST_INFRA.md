# Test Infrastructure Specification: The Self-Operating Charging Network
*Kempower Flagship Challenge 2026 · Autonomous Charging Infrastructure*  
*Document Version: 1.0.0 · Track: Independent E2E Testing Architecture*

---

## 1. Test Philosophy & Design Principles

The testing framework for the Self-Operating Charging Network adheres to three non-negotiable architectural tenets:

### 1.1 Opaque-Box & Requirement-Driven Testing
- **Black-Box Invariant Enforcement**: Tests treat system modules (`src/core`, `src/sim`, `src/commercial`) strictly as black boxes defined by the interface contracts in `PROJECT.md § Interface Contracts`. Tests verify observable state transitions, mathematical correctness, physical law adherence, and domain invariants rather than internal implementation quirks.
- **Authoritative Expected Output Derivation**: Every test case references ground-truth specifications:
  1. The 45 official Kempower challenge CSV datasets (240,635 rows).
  2. Physical and mathematical laws (AC/DC 95.5% inverter efficiency, $10^{-3}$ MILP objective scaling, IEC 61851-23 safety trip thresholds).
  3. The One-Page SLA Specification (MRDT formula, 5-layer anti-fraud gate, piecewise availability fee deduction).

### 1.2 Progressive Testability & Track Independence
- **Zero Inter-Milestone Blocker**: As an independent testing track (E2E), the test harness is self-contained. It incorporates robust contract reference models and data loaders, enabling full test suite execution before, during, and after M1-M5 implementations.
- **Fail-Fast & Zero-Facade Policy**: No test shall pass trivially or assert `True`. Every test asserts strictly computed mathematical values, non-zero differentials, and concrete operational outputs.

### 1.3 Adversarial Verification & Chaos Hardening
- **Encoding & Edge Boundaries**: Comprehensive testing of degenerate cases: 0 kW power requests, zero dwell time, negative spot prices, 799.30 €/MWh price peaks, 75.0°C thermal runaway trips, 72h+ WAN outages, and fraudulent driver claims.

---

## 2. Feature Inventory Mapping (F01–F21)

| Feature ID | Feature Name | Tier Mapping | Target Test Module / Method | Verification Method |
|:---|:---|:---:|:---|:---|
| **F01** | 25 kW DPR Contactor Matrix | Tier 1, 2, 3 | `tests/test_e2e_suite.py::TestTier1Features::test_f01_*` | Discrete module allocation, break-before-make (<500ms) |
| **F02** | 15-min Macro MPC/MILP | Tier 1, 2, 3 | `tests/test_e2e_suite.py::TestTier1Features::test_f02_*` | $10^{-3}$ scaling, CV inequality relaxation, BESS bounds |
| **F03** | Edge Micro FSM | Tier 1, 2, 3 | `tests/test_e2e_suite.py::TestTier1Features::test_f03_*` | State transitions: NORMAL, THERMAL, OFFLINE, CALIBRATED |
| **F04** | Dual-Gun Topology & Multiplexing | Tier 1, 2, 3, 4 | `tests/test_e2e_suite.py::TestTier1Features::test_f04_*` | 12 satellites = 24 plugs, A/B night sequencing, 0 replug |
| **F05** | 95.5% Inverter Loss Constraint | Tier 1, 2, 3 | `tests/test_e2e_suite.py::TestTier1Features::test_f05_*` | $P_{AC} = P_{DC} / 0.955 \le P_{transformer\_max}$ clamp |
| **F06** | Predictive Thermal PdM | Tier 1, 2, 3 | `tests/test_e2e_suite.py::TestTier1Features::test_f06_*` | 1-min telemetry fan RPM drop >20%, 5-min lookahead shift |
| **F07** | S5 Digital Twin Auto-Calibration | Tier 1, 2, 3, 4 | `tests/test_e2e_suite.py::TestTier1Features::test_f07_*` | D5-7 50kW override to 150kW, D5-8 eSIM activation |
| **F08** | 799.30 €/MWh Price Peak BESS | Tier 1, 2, 3, 4 | `tests/test_e2e_suite.py::TestTier1Features::test_f08_*` | BESS peak shaving at 18:00, charge at 27.35 €/MWh |
| **F09** | 2026-11-13 Baseline Runner | Tier 4, R2 | `tests/test_e2e_suite.py::TestTier4RealWorldScenarios` | Replay 21 FTE, 13 missed departures, 29.7% abandoned |
| **F10** | 2026-11-13 Sentinel Runner | Tier 4, R2 | `tests/test_e2e_suite.py::TestTier4RealWorldScenarios` | 0 missed departures, <0.5% abandoned, >40% cost reduction |
| **F11** | One-Page SLA Engine & Anti-Fraud | Tier 1, 2, 4 | `tests/test_e2e_suite.py::TestTier1Features::test_f11_*` | MRDT gate, 5-layer fraud rejection, piecewise fee deduction |
| **F12** | 2029 AEaaS Commercial Model | Tier 4, R4 | `tests/test_e2e_suite.py::TestTier4RealWorldScenarios` | €1.365M/yr 21 FTE elimination, 1.89-month Dual-Gun ROI |
| **F13** | Streamlit Quad 1: KPI Corridor | Tier 4, R3 | `tests/test_e2e_suite.py::TestRequirementsCoverage` | Metric verification: 0 missed, <0.5% drop, >40% savings |
| **F14** | Streamlit Quad 2: 24h Timeline | Tier 4, R2 | `tests/test_e2e_suite.py::TestRequirementsCoverage` | 96-interval power profiles for S1-S5 match CSV bounds |
| **F15** | Streamlit Quad 3: 5-Fault Sandbox | Tier 3, 4 | `tests/test_e2e_suite.py::TestRequirementsCoverage` | 5 faults (F015/F016, G1, outage, F017, config) injected |
| **F16** | Streamlit Quad 4: Sidebar DR | Tier 3, 4 | `tests/test_e2e_suite.py::TestRequirementsCoverage` | Fallback cache integrity, SLA ledger reconciliation |
| **F17** | Hackathon Rails 7 Files Alignment | Tier 4, R1 | `tests/test_e2e_suite.py::TestRequirementsCoverage` | 7 rails documents data point synchronization |
| **F18** | 120-Second Pitch Script | Tier 4, R6 | `tests/test_e2e_suite.py::TestRequirementsCoverage` | DEMO_SCRIPT.md timeline & talking point verification |
| **F19** | `verify_all.py` (<5s) Runner | Tier 4, R6 | `tests/test_e2e_suite.py::TestRequirementsCoverage` | Sub-5-second execution budget validation |
| **F20** | Chaos Perturbation Suite | Tier 3, 4 | `tests/test_e2e_suite.py::TestTier3CrossFeatureCombinations` | Multi-fault simultaneous stress injection |
| **F21** | E2E Integration & Verification | All Tiers | `tests/test_e2e_suite.py` | 100% pass on Tiers 1-4 and R1-R6 verification suite |

---

## 3. 4-Tier Test Architecture

```
                                [ TIER 4: REAL-WORLD SCENARIOS ]
                        - S1 Depot 24-Bus Night Shift (0 Replug / 0 Missed)
                        - S2 Logistics 4-Truck DSO Curtailment (G1 400 kW)
                        - S3 Highway 256-Driver Offline Islanding (<0.5% Drop)
                        - S4 Urban Hub 799.30 €/MWh Peak & D4-2 Cable Trip
                        - S5 Commissioning Digital Twin Self-Healing (D5-7/8)
                                                ▲
                                                │
                                [ TIER 3: CROSS-FEATURE INTERACTIONS ]
                        - Dual-Gun Multiplexing + 95.5% Inverter Clamp
                        - Offline Islanding + Predictive Thermal Shifting
                        - 799.30 €/MWh Peak + BESS Arbitrage + Hard Schedules
                        - Plug & Queue Reservation + CC/CV Dynamic Tapering
                        - S5 Digital Twin Calibration + 25 kW Matrix Pooling
                                                ▲
                                                │
                                [ TIER 2: BOUNDARY & CORNER CASES ]
                        - 0 kW / Negative Power Requests / Max Site Grid Limits
                        - Battery SoC Boundaries (0.0%, 80.0% CC/CV, 100.0%)
                        - Extreme Spot Price Spikes (799.30 €/MWh vs 27.35 €/MWh)
                        - Thermal Runaway & Hard Trip Clamp (65°C / 75°C / 90°C)
                        - Dwell Time Shorter Than Physical MRDT Feasibility
                                                ▲
                                                │
                                [ TIER 1: FEATURE CONTRACT COVERAGE ]
                        - F01: 25 kW Discrete Allocation & Zero-Arc Safety (<500ms)
                        - F02: 15-min Macro MPC ($10^-3$ Scale, Inequality Relaxation)
                        - F03: Edge FSM Deterministic State Machine Transition Loop
                        - F04: Dual-Gun A/B Satellite Dynamic Scheduling
                        - F05: AC Inverter 95.5% Loss ($1.0471 \times P_{DC}$) Calculation
                        - F06: Predictive Thermal Maintenance (Fan RPM Gradient)
                        - F07: Digital Twin Calibration Parameter Reconciliation
                        - F08: BESS Battery Degradation & Capacity Safeguard
                        - F11: One-Page SLA Formula & MRDT 5-Layer Anti-Fraud Gate
```

### Tier 1: Feature Contract Coverage
- Minimum $\ge 5$ discrete unit/contract test cases per feature (F01–F08 + F11).
- Validates the functional input-output contracts, state transitions, and fundamental algorithmic behaviors.

### Tier 2: Boundary & Corner Cases
- Minimum $\ge 5$ boundary/stress test cases per core feature.
- Evaluates degenerate inputs: zero values, maximal saturation values, boundary thresholds (80% CC/CV threshold, 65°C alarm, 75°C hardware trip, 90°C pin trip, 99.50% availability boundary).

### Tier 3: Cross-Feature Combinations (Pairwise & Stress)
- Tests multi-feature interactions where conflicting objectives collide:
  - High spot price vs rigid departure urgency.
  - Reduced grid capacity vs multi-vehicle simultaneous demand.
  - WAN outage vs dynamic load re-balancing.
  - Hardware thermal degradation during peak throughput.

### Tier 4: Real-World Scenarios
- Replays actual operational traces from the 2026-11-13 scenario day across all five focus sites (S1–S5).
- Directly tests against the 45 official CSV files to prove:
  - 13 missed departures in baseline $\rightarrow$ 0 in autonomous sentinel.
  - 29.7% highway abandonment $\rightarrow$ $<0.5\%$.
  - 21 FTE manual workload $\rightarrow$ 0 FTE daily operations.
  - Economic arbitrage and One-Page SLA financial settlements.

---

## 4. Coverage Thresholds & Quality Gates

| Metric | Target Requirement | Strict Enforcement Rule |
|:---|:---:|:---|
| **Tier 1 Feature Tests** | $\ge 40$ test cases | Minimum 5 test cases for each of F01–F08 |
| **Tier 2 Boundary Tests** | $\ge 40$ test cases | Minimum 5 edge cases for each of F01–F08 |
| **Tier 3 Interaction Tests**| $\ge 10$ test cases | Pairwise and multi-variable integration suites |
| **Tier 4 Real-World Tests** | $\ge 5$ scenario tests | Explicit verification across S1, S2, S3, S4, S5 datasets |
| **Requirements R1–R6** | $\ge 6$ audit checks | Explicit mapping to hackathon deliverables |
| **Total Test Count** | **$\ge 100$ test cases** | Must all execute and pass via `pytest tests/test_e2e_suite.py` |
| **Execution Duration** | $\le 5.0$ seconds | Must be fast enough for root verification runner (`verify_all.py`) |
| **Deterministic Seed** | 100% reproducible | Zero flaky tests, zero unseeded random states |

---

## 5. Test Execution & Verification

### Running the Full E2E Test Suite
```powershell
python -m pytest tests/test_e2e_suite.py -v
```

### Running with Execution Timing & Summary
```powershell
python -m pytest tests/test_e2e_suite.py --durations=10
```

### One-Command Full Network Audit
```powershell
python -m pytest tests/ -v
```

---
*Signed by: Independent E2E Testing Track (`e2e_test_writer_1`)*
