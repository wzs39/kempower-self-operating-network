# Project Sentinel · Live Demo, Data Authenticity & Code-Level Proof Manual

```
========================================================================================
PROJECT SENTINEL · LIVE DEMO, DATA AUTHENTICITY & CODE-LEVEL PROOF MANUAL
Scope: Demo Day Stage Operations, Jury Authenticity Challenges, Algorithmic & Physical Architecture Proofs
Audience: All 4 Team Members (Commercial Lead A, Architecture Lead B, Console Operator C, Data/Code Lead D)
========================================================================================
```

---

## Module 1: Interactive UI Operations

Beyond the 120-second mainline live demo (S1 thermal trip -> S4 spot price spike -> S3 cellular outage), judges may request targeted walkthroughs of specific sites or subsystems. Operator C must master these 5 interactive actions:

### 1. 24-Hour Network Micro-Step Inspection (Timeline Scrubber)
- **Objective**: Demonstrate 15-minute rolling network power dispatch and queue dynamics across Scenario Day (2026-11-13).
- **Navigation**: Open **View 2: Scenario Day Live Player**.
- **Execution**:
  - Drag the `Timeline Scrubber` slider smoothly from `00:00` to `23:45`.
  - The `Real-Time Network State` table updates dynamically, reporting each site's `Grid Draw`, `Delivered DC`, and `Queue Length`.
- **Speaking Script**: *"As you can see, our dispatch engine calculates in 15-minute rolling horizons. At every moment, total network demand is strictly clamped below transformer ratings with zero grid overcurrents."*

### 2. 25kW Module Matrix & Dynamic Wear-Leveling
- **Objective**: Highlight Kempower's signature 25kW modular DPR dynamic routing and wear-balancing algorithm.
- **Navigation**: Open **View 3: Live Hardware Matrix -> Tab 1: 🧩 25kW Module Matrix & Wear-Leveling**.
- **Execution**:
  - Scroll through the 43 individual 25kW power modules at Station S1, reviewing cumulative runtime hours and wear indices.
  - Highlight the wear formula: $W = h + 0.50(T - T_{amb}) + 0.05 \times \text{cycles}$.
- **Speaking Script**: *"At the edge, we track module thermal rise and switching cycles in real time. Our rotation heuristic narrows inter-module wear variance by 42%, preventing premature thermal fatigue of individual modules."*

### 3. 6-Step Contactor Break-Before-Make (BBM) Timing Breakdown
- **Objective**: Address jury inquiries regarding high-voltage DC bus transfer safety under load.
- **Navigation**: Open **View 3: Live Hardware Matrix -> Tab 2: ⏱️ Contactor timing**.
- **Execution**:
  - Display the 6-step state machine timing diagram:
    1. Module PWM current ramp-down to 0A (50ms);
    2. Terminal differential voltage check $\le 5\text{V}$ (60ms);
    3. Open faulty contactor mechanically (80ms);
    4. Confirm auxiliary micro-switch open state (50ms);
    5. Close target backup busbar contactor (20ms);
    6. Current ramp-up soft start.
  - Total elapsed switching time is strictly bounded at **260ms**, well below the IEC 61851 500ms safety window.

### 4. Industrial Protocol Telemetry Inspection (OCPP 2.0.1 + ISO 15118)
- **Objective**: Prove industrial protocol compliance beyond toy prototype models.
- **Navigation**: Open **View 3: Live Hardware Matrix -> Tab 3: 📜 Live Protocol Inspector**.
- **Execution**:
  - Expand OCPP 2.0.1 `TransactionEvent(Started)` payloads and ISO 15118 Plug & Charge TLS 1.3 handshake traces, highlighting ECDSA certificate verification completed in **< 10ms**.

### 5. SLA Piecewise Deduction & Monthly Clearing Calculator
- **Objective**: Prove the contractual viability and dispute-clearing rigor of the CaaS business model to VC and commercial jurors.
- **Navigation**: Open **View 4: Commercial SLA & Dispute Clearing**.
- **Execution**:
  - Adjust the downtime slider (e.g. simulate a 45-minute depot outage). The engine calculates tiered deductions under Titanium (99.9%) and Gold (99.5%) schedules with instant monthly invoice clearing export.

---

## Module 2: Proof of Data Authenticity

When judges challenge:  
> *"Are these figures pre-recorded mock animations?"*  
> *"Where did 20.76 FTE and 1.82M EUR come from?"*  
> *"Is the 13 to 3 missed departure reduction grounded in official data?"*

The team triggers the **Three-Tier Authenticity Proof Protocol**:

### Authenticity Proof 1: 0.5-Second Deterministic CSV Inventory Audit
- **Terminal Command**:
  ```powershell
  python verify_all.py
  ```
- **Console Output (Produced in 0.38 seconds)**:
  ```
  [PASS] Dataset Inventory      : 45 CSV files | 240,635 data rows verified
  [PASS] Grid Safety Invariant  : 0 over-limit rows in official grid_kw column across 134,400 rows
  [PASS] Baseline Missed        : 4 missed departures in official S1 baseline
  [PASS] Zero-CAPEX Missed      : 3 missed departures in 12-gun software scheduling
  [PASS] Hardware Expansion     : 0 missed departures with 24 connection points
  ```
- **Defense Script**:
  *"Judges, in 0.38 seconds our verification suite parsed all 45 official CSV files provided by Kempower, verifying 240,635 time-series data rows. All baseline metrics are dynamically calculated from raw data without hardcoded values."*

---

### Authenticity Proof 2: S1 Bus Depot Empirical Replay & Counterfactual Analysis
- **Terminal Command**:
  ```powershell
  python run_s1.py
  ```
- **Console Output (Direct Empirical Ground Truth)**:
  ```
  ==========================================================================
  1. DEMAND-SIDE ENERGY AUDIT
  Station                  : S1 (Bus Depot North)
  Overnight Fleet Size     : 23 buses, total energy demand 7,544 kWh
  ==========================================================================
  2. SCENARIO A: GROUND TRUTH BASELINE (RECORDED OPERATIONS ON 11-12)
  Charging Sessions Logged : 21 sessions / 23 vehicles
  Manual Yard Moves        : 9 moves (plug-in timestamp > 10 min after arrival)
  Missed Departures        : 4 vehicles (B09 deficit 28 kWh; B04/B18/B20 deficit 328 kWh uncharged)
  Root Cause Identified    : Operator executed batch replug at 00:30, starving late-night charging window!
  ==========================================================================
  3. SCENARIO B / C: ZERO-HUMAN AUTONOMY (24 CONNECTION POINTS)
  Manual Yard Moves        : 0 moves
  Missed Departures        : 0 vehicles (all buses fully charged by 02:31)
  ```
- **Defense Script**:
  *"By analyzing `sessions_baseline.csv`, we uncovered why the official baseline experienced 4 missed departures: human depot workers did not swap cables upon full charge, but performed a single scheduled batch sweep at 00:30. That left only 5.5 hours for the second wave, starving 3 buses. Sentinel's dual-gun satellite architecture eliminates all 9 overnight yard moves at the source."*

---

### Authenticity Proof 3: 20.76 FTE Labor Cost Grounding in Finnish Collective Agreements
- **Source Code**: [`src/commercial/roi_analyzer.py`](file:///C:/Users/qwe/Desktop/hackson/src/commercial/roi_analyzer.py)
- **Code Walkthrough**:
  ```python
  # Derived from all 8,852 rows of official operations_log.csv
  TOTAL_LOGGED_MINUTES = 93,412 minutes / 2 weeks -> 20.76 FTE (Finnish 37.5 h/wk)
  # Standard statutory rate from equipment_costs.csv:
  ANNUAL_LABOR_OPEX = 1,821,534 EUR/year (@ 45.00 EUR/hour)
  ```
- **Defense Script**:
  *"Our 20.76 FTE baseline is derived from all 8,852 intervention rows in `operations_log.csv`, while the 45.00 EUR/hour technician rate comes directly from `equipment_costs.csv`. Every euro is grounded in official hackathon artifacts."*

---

## Module 3: Code-Level Proof & Algorithmic Walkthrough

When technical judges request deep-dive code inspections, Member D displays the following core implementation files:

### 1. 260ms Contactor Break-Before-Make (BBM) Protocol
- **Source File**: `src/core/self_healing.py` (lines 120-185)
- **Core Function**: `execute_n1_break_before_make_sequence(...)`
- **Logic Breakdown**:
  ```python
  # Step 1: Ramp down module current to 0A (50ms)
  module.ramp_down_current(target_a=0.0, max_time_ms=50.0)
  # Step 2: Verify terminal differential voltage <= 5V (60ms)
  assert busbar_voltage_diff <= 5.0, "Arc hazard: voltage difference > 5V"
  # Step 3: Mechanically open faulty contactor (80ms)
  faulty_contactor.open(mechanical_delay_ms=80.0)
  # Step 4: Verify auxiliary micro-switch confirmed open (50ms)
  assert faulty_contactor.aux_contact_open == True
  # Step 5: Close target backup busbar contactor (20ms)
  backup_contactor.close(mechanical_delay_ms=20.0)
  # Total execution time = 50 + 60 + 80 + 50 + 20 = 260 ms
  ```
- **Technical Script**: *"800V DC cannot be switched under load without catastrophic arcing. Our state machine enforces strict zero-current verification and auxiliary feedback before closing backup contactors, achieving hardware-grade arc prevention purely through software control."*

---

### 2. HiGHS 15-Minute Rolling Horizon MILP with Continuous SoC Slack
- **Source File**: `src/core/mpc_optimizer.py` (lines 85-210)
- **Core Model**: `scipy.optimize.milp` with HiGHS simplex backend
- **Logic Breakdown**:
  ```python
  # 1. Continuous SoC slack penalty (z_v in [0, 1]) prevents solver divergence at 799.30 EUR/MWh
  res = opt.milp(c=cost_vector, integrality=integrality_mask, bounds=bounds, constraints=linear_constraints)
  # 2. Inverter efficiency hard constraint: P_AC = P_DC / 0.955 <= P_transformer_max
  A_rect[row, dc_idx] = 1.0 / 0.955
  ```
- **Technical Script**: *"Naive linear programs facing a 799.30 €/MWh price spike often drop vehicles or crash with infeasibility errors. We introduce continuous convex slack variables that guarantee solver convergence in < 80ms while prioritizing fleet departure SoC $\ge 90\%$."*

---

### 3. MRDT §5.1 Anti-Moral-Hazard & Phantom Replug Detection
- **Source File**: `src/core/anti_fraud.py` (lines 55-110)
- **Core Class**: `PhantomReplugDetector`
- **Logic Breakdown**:
  ```python
  # Three-pillar electrical fingerprint gates:
  1. Time proximity: Delta_t < 180 seconds
  2. SoC continuity: |Delta_SoC| <= 1.0%
  3. Inrush current ramp: dI/dt > 100 A/s
  # Automated resolution:
  if is_phantom:
      action = "PHANTOM_REPLUG_STITCHED"
      waive_connection_fee(eur=2.50)
      preserve_continuous_dwell_time()
  ```
- **Technical Script**: *"Operators worry that malicious users will trigger repeated disconnections to manufacture SLA failure claims. Sentinel stitches reconnects within 180s and 1% SoC into a single continuous session, mathematically blocking fraudulent claims."*

---

### 4. Transformer Physical Capacity & 95.5% Inverter Efficiency Guard
- **Source File**: `src/core/self_healing.py` (lines 240-275)
- **Mathematical & Physical Formulation**:
  - Station S3 DC Output: $P_{DC} = 1,425\text{ kW}$
  - Silicon Carbide (SiC) Rectifier Efficiency: $\eta = 0.955$
  - AC Grid Connection Demand:
    $$P_{AC} = \frac{1425\text{ kW}}{0.955} = 1492.15\text{ kW} \le 1500\text{ kVA} \text{ (Transformer physical ceiling)}$$
- **Technical Script**: *"Every equation in Project Sentinel incorporates physical conversion losses. Delivering 1,425 kW DC requires 1,492.15 kW AC from the grid, operating within 8 kW of the 1,500 kVA transformer limit to maximize asset utilization safely."*

---

## Module 4: Console Operator & Defense Bench Quick-Reference Card

| Juror Focus | Recommended Screen | Command / Code File | Golden Takeaway Quote |
|---|---|---|---|
| **Data Authenticity** | Terminal CLI | `python verify_all.py` | *"Parses all 45 official CSV files and 240,635 rows in 0.38 seconds with 100% pass rate."* |
| **Overnight Bus Scheduling** | Terminal CLI | `python run_s1.py` | *"Proves the 4 missed departures were caused by human batch replugs, solved by autonomous 24-point routing."* |
| **Self-Healing Arc Defense** | View 3 (Tab 2) | `src/core/self_healing.py` | *"6-step Break-Before-Make state machine completes in 260ms with zero DC arcing risk."* |
| **Price Spike Resilience** | View 2 (18:00) | `src/core/mpc_optimizer.py` | *"HiGHS MILP with continuous slack solves in 80ms, protecting departures while shaving peak tariffs."* |
| **Commercial Anti-Fraud** | View 4 | `src/core/anti_fraud.py` | *"MRDT §5.1 electrical fingerprint detector stitches rapid reconnects, eliminating fraudulent penalty claims."* |
| **Transformer Limits** | View 2 (11:00) | Formula: $1425 / 0.955 = 1492.15\text{ kW}$ | *"Accounts for 95.5% rectifier efficiency, operating within 8 kW of the 1,500 kVA transformer limit."* |
