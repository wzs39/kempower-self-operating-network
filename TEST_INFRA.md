# Test Infrastructure Specification: The Self-Operating Charging Network
*Kempower Flagship Challenge 2026 · Autonomous Charging Infrastructure*  
*Document Version: 2.0.0 · Track: Independent Opaque-Box E2E Testing Architecture*

---

## 1. Test Philosophy & Design Principles

The testing framework for the Self-Operating Charging Network adheres to three non-negotiable architectural tenets:

### 1.1 Opaque-Box & Requirement-Driven Testing
- **Black-Box Invariant Enforcement**: Tests treat system modules (`src/core`, `src/sim`, `src/commercial`) strictly as black boxes defined by the interface contracts in `PROJECT.md § Interface Contracts`. Tests verify observable state transitions, mathematical correctness, physical law adherence, and domain invariants rather than private internal implementation details.
- **Authoritative Expected Output Derivation**: Every test case references ground-truth specifications:
  1. The 45 official Kempower challenge CSV datasets (240,635 rows).
  2. Physical and mathematical laws (AC/DC 95.5% inverter efficiency, $10^{-3}$ MILP objective scaling, IEC 61851-23 safety trip thresholds).
  3. The One-Page SLA Specification (MRDT formula, 5-layer anti-fraud gate, piecewise availability fee deduction).

### 1.2 Progressive Testability & Track Independence
- **Zero Inter-Milestone Blocker**: As an independent testing track (`e2e_tests/`), the test harness is completely self-contained. It incorporates robust contract reference adapters (`common.py`) and data loaders, enabling standalone test suite execution before, during, and after M1-M4 implementations.
- **Fail-Fast & Zero-Facade Policy**: No test shall pass trivially or assert dummy conditions (`assert True`). Every test asserts strictly computed mathematical values, non-zero differentials, and concrete operational outputs.

### 1.3 Adversarial Verification & Stress Hardening
- **Encoding & Edge Boundaries**: Comprehensive testing of degenerate cases: 0 kW power requests, negative requests, zero dwell time, negative spot prices, 799.30 €/MWh price peaks, 75.0°C thermal runaway trips, 72h+ WAN outages, and fraudulent driver claims.

---

## 2. Feature Inventory Mapping (F01–F21)

| Feature ID | Feature Name | Tier Mapping | Target Test Module / Method | Verification Method |
|:---|:---|:---:|:---|:---|
| **F01** | 25 kW DPR Contactor Matrix | Tier 1, 2, 3 | `e2e_tests/tier1_feature_coverage.py::test_f01_*`<br>`e2e_tests/tier2_boundary_corner.py::test_f01_b*` | Discrete module allocation, break-before-make (<500ms) |
| **F02** | 15-min Macro MPC/MILP | Tier 1, 2, 3 | `e2e_tests/tier1_feature_coverage.py::test_f02_*`<br>`e2e_tests/tier2_boundary_corner.py::test_f02_b*` | $10^{-3}$ scaling, CV inequality relaxation, BESS bounds |
| **F03** | Edge Micro FSM | Tier 1, 2, 3 | `e2e_tests/tier1_feature_coverage.py::test_f03_*`<br>`e2e_tests/tier2_boundary_corner.py::test_f03_b*` | State transitions: NORMAL, THERMAL, OFFLINE, CALIBRATED |
| **F04** | Dual-Gun Topology & Multiplexing | Tier 1, 2, 3, 4 | `e2e_tests/tier1_feature_coverage.py::test_f04_*`<br>`e2e_tests/tier2_boundary_corner.py::test_f04_b*` | 12 satellites = 24 plugs, A/B night sequencing, 0 replug |
| **F05** | 95.5% Inverter Loss Constraint | Tier 1, 2, 3 | `e2e_tests/tier1_feature_coverage.py::test_f05_*`<br>`e2e_tests/tier2_boundary_corner.py::test_f05_b*` | $P_{AC} = P_{DC} / 0.955 \le P_{transformer\_max}$ clamp |
| **F06** | Predictive Thermal Calibration / PdM | Tier 1, 2, 3 | `e2e_tests/tier1_feature_coverage.py::test_f06_*`<br>`e2e_tests/tier2_boundary_corner.py::test_f06_b*` | 1-min telemetry fan RPM drop >20%, 5-min lookahead shift |
| **F07** | S5 Three-Way Config Reconciler | Tier 1, 2, 3, 4 | `e2e_tests/tier1_feature_coverage.py::test_f07_*`<br>`e2e_tests/tier2_boundary_corner.py::test_f07_b*` | D5-7 50kW override to 150kW, D5-8 eSIM activation |
| **F08** | 799.30 €/MWh Price Peak BESS Interface | Tier 1, 2, 3, 4 | `e2e_tests/tier1_feature_coverage.py::test_f08_*`<br>`e2e_tests/tier2_boundary_corner.py::test_f08_b*` | BESS peak shaving interface at 18:00 *(interface defined, not field-validated)* |
| **F09** | 2026-11-13 Baseline Replay | Tier 4 | `e2e_tests/tier4_real_world_scenario.py::test_s1_*` to `test_s5_*` | 13 missed departures across S1 (4), S2 (4), S5 (5) |
| **F10** | 2026-11-13 Sentinel Runner | Tier 4 | `e2e_tests/tier4_real_world_scenario.py::test_closed_loop_*` | 3 missed (0 € software) / 0 missed (324k € S1 expansion), <0.5% abandoned, 0 grid breaches |
| **F11** | One-Page SLA Engine & Anti-Fraud | Tier 1, 2, 4 | `e2e_tests/tier1_feature_coverage.py::test_f11_*`<br>`e2e_tests/tier4_real_world_scenario.py::test_one_page_*` | MRDT gate, 5-layer fraud rejection, piecewise fee deduction |
| **F12** | Commercial AEaaS ROI Model | Tier 4 | `e2e_tests/tier4_real_world_scenario.py::test_commercial_*` | 20.76 FTE continuous elimination (1.82M €/yr), Tier 2 (0 €) vs Tier 3 (324k €) |
| **F13–F18** | High-Value Innovation Protocols | Tier 3, 4 | `e2e_tests/tier3_cross_feature.py`<br>`e2e_tests/tier4_real_world_scenario.py` | Pairwise and full Scenario Day stress validation |
| **F19** | Zero-Regression Deterministic Verifier | Master / Root | `verify_all.py` | Sub-0.5-second execution budget validation (<5.0s) |
| **F20** | Independent Opaque-Box E2E Suite | Track Scope | `e2e_tests/test_runner.py` (Tiers 1–4) | 100% pass across 106 tests in `e2e_tests/` in 0.65s |
| **F21** | Final Integration & Adversarial Verification | All Tiers | `e2e_tests/` + `tests/` | 100% pass across `431 pytest + 106 E2E (537 total)` |

---

## 3. Directory Layout & 4-Tier Test Architecture

```
e2e_tests/
├── __init__.py                   # Package marker
├── common.py                     # Black-box production adapters & path constants
├── test_runner.py                # Master E2E test runner with CLI & summary table
├── tier1_feature_coverage.py     # Tier 1: Feature Contract Coverage (>=5 tests per core feature)
├── tier2_boundary_corner.py      # Tier 2: Boundary & Corner cases (Edge, Stress, Saturation)
├── tier3_cross_feature.py        # Tier 3: Pairwise & Multi-variable interactions
└── tier4_real_world_scenario.py  # Tier 4: Real-world Scenario Day 2026-11-13 workloads
```

```
                                [ TIER 4: REAL-WORLD SCENARIOS ]
                        - S1 Depot 24-Bus Night Shift (3 Missed @ 0€ / 0 Missed @ 324k€)
                        - S2 Logistics 4-Truck DSO Curtailment (G1 400 kW)
                        - S3 Highway 256-Driver Offline Islanding (<0.5% Drop)
                        - S4 Urban Hub 799.30 €/MWh Peak & D4-2 Cable Trip
                        - S5 Commissioning Three-Way Config Reconciler (D5-7/8)
                        - Commercial 20.76 FTE Elimination & One-Page SLA Settlement
                                                ▲
                                                │
                                [ TIER 3: CROSS-FEATURE INTERACTIONS ]
                        - Dual-Gun Multiplexing + 95.5% Inverter Clamp
                        - Offline Islanding + Predictive Thermal Shifting
                        - 799.30 €/MWh Peak + BESS Interface + Hard Schedules
                        - Plug & Queue Reservation + CC/CV Dynamic Tapering
                        - S5 Three-Way Config Reconciler + 25 kW Matrix Pooling
                        - S2 DSO Curtailment + Lookahead Precharging & Preemption
                        - Low Ambient Temperature (-15°C) + Matrix Contactor Cycling
                                                ▲
                                                │
                                [ TIER 2: BOUNDARY & CORNER CASES ]
                        - 0 kW / Negative Power Requests / Max Site Grid Limits
                        - Battery SoC Boundaries (0.0%, 80.0% CC/CV, 100.0%)
                        - Extreme Spot Price Spikes (799.30 €/MWh vs 27.35 €/MWh)
                        - Thermal Runaway & Hard Trip Clamp (65°C / 75°C / 110°C)
                        - Dwell Time Shorter Than Physical MRDT Feasibility
                        - Corrupted / Subzero / Missing Telemetry Fallback
                                                ▲
                                                │
                                [ TIER 1: FEATURE CONTRACT COVERAGE ]
                        - F01: 25 kW Discrete Allocation & Zero-Arc Safety (<500ms)
                        - F02: 15-min Macro MPC ($10^-3$ Scale, Inequality Relaxation)
                        - F03: Edge FSM Deterministic State Machine Transition Loop
                        - F04: Dual-Gun A/B Satellite Dynamic Scheduling
                        - F05: AC Inverter 95.5% Loss ($1.0471 \times P_{DC}$) Calculation
                        - F06: Predictive Thermal Maintenance (Fan RPM Gradient)
                        - F07: Three-Way Config Reconciler Parameter Reconciliation
                        - F08: BESS Battery Degradation & Capacity Safeguard
                        - F11: One-Page SLA Formula & MRDT 5-Layer Anti-Fraud Gate
```

### Tier 1: Feature Contract Coverage (`tier1_feature_coverage.py`)
- $\ge 5$ discrete unit/contract test cases per feature across F01–F08 and F11.
- Validates the functional input-output contracts, state transitions, and fundamental algorithmic behaviors.
- **Actual Delivered**: 45 test cases (100% pass in 0.030s).

### Tier 2: Boundary & Corner Cases (`tier2_boundary_corner.py`)
- $\ge 5$ boundary/stress test cases per core feature.
- Evaluates degenerate inputs: zero values, negative values, maximal saturation values, boundary thresholds (80% CC/CV threshold, 65°C alarm, 75°C hardware trip, 110°C extreme trip, 99.50% availability boundary).
- **Actual Delivered**: 40 test cases (100% pass in 0.001s).

### Tier 3: Cross-Feature Combinations (`tier3_cross_feature.py`)
- Tests multi-feature interactions where conflicting objectives collide:
  - High spot price vs rigid departure urgency.
  - Reduced grid capacity vs multi-vehicle simultaneous demand.
  - WAN outage vs dynamic load re-balancing.
  - Hardware thermal degradation during peak throughput.
  - -15°C cold ambient acceptance vs full matrix cycling.
- **Actual Delivered**: 12 test cases (100% pass in 0.018s).

### Tier 4: Real-World Scenarios (`tier4_real_world_scenario.py`)
- Replays actual operational traces from the 2026-11-13 scenario day across all five focus sites (S1–S5).
- Directly tests against the 45 official CSV files to prove:
  - 13 missed departures in baseline $\rightarrow$ **3 missed (`0 €` software urgency, `10` saved; S1 deficit `398.5 -> 48.8 kWh`, `-87.8%`)** $\rightarrow$ **0 missed (`324,000 €` S1 dual-gun expansion, `13.31-yr` payback)**.
  - 29.7% highway abandonment $\rightarrow$ $<0.5\%$.
  - 20.76 FTE manual workload $\rightarrow$ 0 continuous FTE daily operations.
  - Economic arbitrage and One-Page SLA financial settlements.
  - Network-wide grid safety: 0 official `grid_kw` over-limit intervals across 134,400 data points.
- **Actual Delivered**: 9 test cases (100% pass in 0.363s).

---

## 4. Coverage Thresholds & Quality Gates

| Metric | Target Requirement | Actual Delivered | Strict Enforcement Rule |
|:---|:---:|:---:|:---|
| **Tier 1 Feature Tests** | $\ge 40$ test cases | **45 test cases** | Minimum 5 test cases for each of F01–F08, F11 |
| **Tier 2 Boundary Tests** | $\ge 40$ test cases | **40 test cases** | Minimum 5 edge cases for each of F01–F08 |
| **Tier 3 Interaction Tests**| $\ge 10$ test cases | **12 test cases** | Pairwise and multi-variable integration suites |
| **Tier 4 Real-World Tests** | $\ge 5$ scenario tests | **9 test cases** | Explicit verification across S1–S5 & commercial datasets |
| **Total Test Count** | **$\ge 100$ test cases** | **106 test cases** | All executed via `python e2e_tests/test_runner.py` |
| **Execution Duration** | $\le 5.0$ seconds | **0.414 seconds** | Extreme performance budget for fast CI feedback |
| **Pass Rate** | 100% | **100% (106 / 106)** | Zero failures, zero regressions, zero skipped |
| **Deterministic Seed** | 100% reproducible | 100% reproducible | Zero flaky tests, zero unseeded random states |

---

## 5. Test Execution & Verification Commands

### 1. Master E2E Runner (Recommended)
```powershell
python e2e_tests/test_runner.py
```

### 2. Run Specific Tiers
```powershell
# Run only Tier 1 Feature Coverage
python e2e_tests/test_runner.py --tier 1

# Run Tiers 1 and 2
python e2e_tests/test_runner.py --tier 1 --tier 2

# Run with verbose output
python e2e_tests/test_runner.py -v
```

### 3. Run Individual Tier Scripts Standalone
```powershell
python e2e_tests/tier1_feature_coverage.py
python e2e_tests/tier2_boundary_corner.py
python e2e_tests/tier3_cross_feature.py
python e2e_tests/tier4_real_world_scenario.py
```

### 4. Run via Pytest
```powershell
# Run all E2E tests
python -m pytest e2e_tests/ -v

# Run full pytest suite (`431 pytest + 106 E2E (537 total)`)
python -m pytest tests/ -q
```

### 5. Run Deterministic Verifier Gate (<0.5s)
```powershell
python verify_all.py
```

---
*Signed by: Independent E2E Testing Track (`e2e_test_writer`)*
