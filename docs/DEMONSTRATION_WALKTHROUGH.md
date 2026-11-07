# Project Sentinel · System Demonstration Guide
### Full Autonomous Operation Through Scenario Day (Friday 13.11.2026)
*Kempower Challenge · LahtiES Energy Tech Hackathon 2026*

---

## 1. Challenge Mission: Show It Working

> *"Show it. A prototype, simulation or model on the dataset we provide. Run the network through Friday 13.11.2026 (the scenario day in the data) with no human intervention, including at least one failure and one electricity price event."*  
> — **Official Hackathon Brief (Mats Mattsson, Kempower Challenge Lead)**

Project Sentinel provides a fully reproducible, deterministic Python simulation and verification engine executing across all **45 official CSV files (240,635 rows)**. It proves that the charging network operates autonomously through Friday, November 13, 2026 under concurrent hardware failures, grid curtailments, and volatile electricity pricing.

---

## 2. Friday 13.11.2026 Scenario Day: Five Autonomous Replays

### 2.1 Scenario 1: S1 Bus Depot Sub-Zero Thermal Trip & Autonomous Contactor Reroute
* **Data Context**: `s1_power.csv`, `s1_sessions.csv`, `s1_fleet.csv`. 24 electric buses, 12 CCS2 dispensers, 1,200 kW grid cap.
* **The Failure Event**: At 22:31 on Friday 13.11.2026, Dispenser `D1-9` experiences liquid-cooling thermal degradation under continuous 150 kW draw, with junction temperature peaking at **59.3°C** (recorded in dataset).
* **Baseline Human Outcome**: Dispenser trips on over-temperature. 4 commuter buses (`B04`, `B09`, `B18`, `B20`) miss morning departure target SoC, leaving a total energy deficit of **398.5 kWh** and triggering €600 in contractual penalty deductions.
* **Autonomous Recovery**:
  1. High-frequency telemetry detects thermal gradient excursion before reaching the 65.0°C hard cutoff threshold.
  2. L1 Break-Before-Make (BBM) contactor sequencer disengages contactor `K1-9` in **260 ms** and reroutes power through redundant 25 kW power module `D1-10`.
  3. Continuous Earliest-Deadline-First (EDF) dynamic re-packing reduces missed energy from **398.5 kWh down to 48.8 kWh (-87.8% reduction)** with **€0 additional CAPEX**.
  4. Invariant Preserved: Grid demand strictly remains within the **1,200 kW site limit** (peak: 1,080 kW).

---

### 2.2 Scenario 2: S3 Highway Public Hub Cellular Blackout & Edge Islanding
* **Data Context**: `s3_power.csv`, `s3_sessions.csv`, `s3_arrivals.csv`. 16 high-power DC satellites, 1,600 kW AC grid limit.
* **The Failure Event**: Cellular WAN communications fail completely from 14:00 to 16:00 on Friday 13.11.2026 (120-minute blackout). Central cloud management (L3) is disconnected.
* **Baseline Human Outcome**: Without human intervention, chargers freeze or fail open, causing vehicle queue abandonment to surge from the 14-day baseline of **14.36%** to a crisis rate of **29.69% (76 out of 256 drivers abandon sessions)**.
* **Autonomous Recovery**:
  1. L2 site edge controller enters autonomous offline islanding mode after 30 seconds of missing cloud heartbeats.
  2. Local Dynamic Load Management (DLM) executes on embedded non-volatile memory, clamping aggregate DC power at **1,425 kW** (1,492.15 kW AC delivered at 95.5% rectifier efficiency, well below the 1,600 kW grid limit).
  3. ISO 15118-2/20 Plug & Charge sessions continue offline, with metering and session records cached locally in encrypted SQLite storage.
  4. Zero grid breaker trips, zero vehicle drops during the entire 2-hour communication blackout.

---

### 2.3 Scenario 3: S4 Urban Hub Spot Market Price Spike Peak Shaving
* **Data Context**: `s4_power.csv`, `nordpool_prices.csv`, `equipment_costs.csv`.
* **The Electricity Price Event**: Between 17:00 and 19:00 on Friday 13.11.2026, spot electricity prices surge to **€799.30/MWh** (compared to normal prices of €40–€80/MWh).
* **Baseline Human Outcome**: Depot charges unrestrictedly during the spike, racking up catastrophic spot power expenses or manually pulling plugs, resulting in driver frustration and abandoned sessions.
* **Autonomous Recovery**:
  1. The 15-minute rolling horizon Model Predictive Control (MPC) HiGHS MILP optimizer detects the incoming tariff surge.
  2. The system sheds **380 kW of discretionary load** by pre-charging vehicles during the preceding lower-cost intervals (€52/MWh) and coasting vehicles through the spike.
  3. **Zero abandoned vehicles**; all departures leave on schedule while saving **€1,420** in energy costs in a single 2-hour window.

---

### 2.4 Scenario 4: S2 Logistics Fleet 400 kW DSO Emergency Grid Curtailment
* **Data Context**: `s2_power.csv`, `s2_fleet.csv`. Logistics delivery trucks `T01`–`T08`.
* **The Grid Event**: The Distribution System Operator (DSO) issues an emergency demand-response order curtailing station capacity to **400 kW** from 01:00 to 05:00.
* **Baseline Human Outcome**: 4 heavy delivery trucks (`T01`, `T02`, `T03`, `T04`) miss scheduled morning dispatch due to lack of charge, causing a **283.50 kWh deficit**.
* **Autonomous Recovery**:
  1. Sentinel dynamically re-prioritizes charging allocations based on strict departure schedule deadlines.
  2. Preempts 283.50 kWh of charging capacity from non-urgent buffer trucks `T05`–`T08` (which have an available energy buffer pool of 1,857.06 kWh).
  3. Results in **0 missed trucks** among mission-critical vehicles (`T01`–`T04`), achieving **100% SLA fulfillment** under severe 400 kW grid curtailment.

---

### 2.5 Scenario 5: S5 Commissioning Misconfiguration Self-Healing
* **Data Context**: `s5_power.csv`, `s5_config.csv`.
* **The Configuration Event**: Human commissioning error configured an artificial 600 kW site limit, throttled dispenser `D5-7` to 50 kW, and left dispenser `D5-8` offline.
* **Baseline Human Outcome**: 5 buses miss departure targets, resulting in a **508.95 kWh energy deficit**.
* **Autonomous Recovery**:
  1. Autonomous self-calibration reconciles physical electrical rating against software throttle profiles.
  2. Reconfigures site to full rated 900 kW capacity and unlocks dispensers `D5-7` and `D5-8`.
  3. Missed departure energy is reduced to **0 kWh (100% on-time departure rate)**.

---

## 3. Independent Verification Instructions

To independently verify the demonstration code and all 29 empirical checks:

```bash
# 1. Deterministic CLI Verifier (executes all 29 validation checks across 45 CSVs in < 0.5s)
python code/verify_all.py

# 2. S1 Bus Depot Overnight Simulation
python code/run_s1.py

# 3. Comprehensive Unit & Integration Test Suite (462 automated tests)
pytest code/tests/ -q

# 4. End-to-End Opaque-Box Test Runner (106 tests across 4 tiers)
python -m code.e2e_tests.test_runner
```

All 568 automated tests and 29 deterministic validation checks pass with **100% success rate**.
