# S1 / S2 / S5 Same-Engine Causal Attribution Matrix (`docs/attribution_matrix.md`)

> **Reproducibility**: All 16 S1 cells and calibrated S2/S5 cells below are generated directly from [`src/sim/discrete_sim.py`](../src/sim/discrete_sim.py) (`load_fleet_jobs(..., depart_date="2026-11-13")` and `run_discrete_event_simulation(...)`) against the unmodified [`fleet_schedule.csv`](../kempower-challenge/kempower-challenge-data/fleet_schedule.csv), [`chargers.csv`](../kempower-challenge/kempower-challenge-data/chargers.csv), [`power_cabinets.csv`](../kempower-challenge/kempower-challenge-data/power_cabinets.csv), [`grid_events.csv`](../kempower-challenge/kempower-challenge-data/grid_events.csv), and [`site_config.csv`](../kempower-challenge/kempower-challenge-data/site_config.csv).

---

## 1. Executive Finding: Why S1 Misses 4 Buses on Scenario Day (`2026-11-13`)

In [`departures_baseline.csv`](../kempower-challenge/kempower-challenge-data/departures_baseline.csv), Station S1 has **32 total departures** on `2026-11-13` (including `B15`, which arrives at `2026-11-12T18:58:00+02:00` with `8%` SoC and departs at `2026-11-13T05:40:00+02:00` requiring `90%` SoC), of which **4 buses (`B04, B09, B18, B20`) depart undercharged**.

Evaluating the full **16-cell causal attribution matrix** (`cross_tie` $\in \{\text{False}, \text{True}\} \times \text{strategy} \in \{\text{fcfs}, \text{urgency}\} \times \text{F016 fault} \in \{\text{Yes}, \text{No}\} \times \text{plug points} \in \{12, 24\}$) reveals three fundamental engineering truths:

1. **The Root Cause is Single-Cabinet Fault `F016`, Not Gun Count**:
   - Under S1's physical 12-gun topology (`points_per_cabinet=4`, `cross_tie=False`, matching `chargers.csv` where `C1-1 -> D1-1..4`, `C1-2 -> D1-5..8`, `C1-3 -> D1-9..12`), **removing the 246-minute `F016` thermal trip on Cabinet C1-3 results in `0` missed departures (`0.0 kWh` deficit) even under naive `fcfs`**.
2. **Zero-CAPEX Software (`strategy="urgency"`) Eliminates All 12 Manual Moves While Closing 87.8% of the Energy Deficit**:
   - With `F016` active on 12 guns (`cross_tie=False`), `fcfs` requires **12 manual cable moves** (`moves = 12`) and still leaves **4 missed departures (`B04, B09, B18, B20`, `398.5 kWh` deficit)**.
   - Switching to `urgency` scheduling (`0 €` CAPEX) reduces **manual cable moves from `12` to `0` (`moves = 0`)**, rescues `B20` (**`4 -> 3` missed departures**), and cuts the simulated energy deficit from **`398.5 kWh` to `48.8 kWh` (`-87.8%`)**.
3. **Eliminating the Final 3 Missed Departures (`48.8 kWh`) is an Electrical Redundancy Decision, Not a Software Defect**:
   - Because `chargers.csv` binds `D1-9..D1-12` exclusively to Cabinet `C1-3` (`cross_tie=False`), when `C1-3` trips at `02:25` for `246 minutes` (`cleared_by = technician`), any bus plugged into `C1-3` is physically isolated from `C1-1` and `C1-2`.
   - Adding 12 guns *without* cross-cabinet busbar ties (`cross_tie=False, points=24, fault=True`) actually **worsens** missed departures to `8` (`1,040.1 kWh` deficit) because 8 overnight buses lock onto `C1-3` at arrival and are stranded when `C1-3` trips!
   - Conversely, enabling **cross-cabinet busbar tie (`cross_tie=True`) on the existing 12 guns** achieves **`0` missed departures (`0.0 kWh` deficit, `0` moves) with the peak still at `1,080 kW`** — i.e. fully inside the `1,200 kW` grid limit and with **no new dispensers at all** (Cell 5).
   - ⚠️ **The busbar, not the plugs, is what reaches zero.** `324,000 €` of 12 extra dispensers buys Cells 7/8's *plug points*; only the `cross_tie=True` half of Cell 8 produces the `0`. Quoting `324,000 € → 0 missed departures` is therefore **wrong** — plugs alone are Cell 7 (`8` missed).
   - Cabinet upsizing was also tested (see Option 5): `3×450 kW` reaches `0` but peaks at `1,350 kW`, **over the `1,200 kW` grid limit**; `3×400 kW` is exactly at the limit and still misses `4`. So no hardware purchase inside the grid limit reaches zero.

---

## 2. S1 16-Cell Causal Attribution Matrix (`32` Departures on `2026-11-13`, `3×360 kW` Cabinets, `150 kW` Guns)

| Cell | Cross-Cabinet Tie (`cross_tie`) | Strategy | C1-3 Fault (`F016` @ `02:25`) | Plug Points | Missed Departures | Simulated Deficit (kWh) | Peak Power (kW) | Delivered (kWh) | Manual Moves (`moves`) | Undercharged Vehicle IDs |
|:---:|:---:|:---:|:---:|:---:|:---:|---:|---:|---:|:---:|:---|
| **1** | **No (`False`)** | **`fcfs`** | **Yes** | **12** | **4** | **398.5** | **1,080.0** | **7,473.5** | **12** | **`B04, B09, B18, B20`** *(Exact Official Match)* |
| **2** | **No (`False`)** | **`urgency`** | **Yes** | **12** | **3** | **48.8** | **1,080.0** | **7,823.0** | **0** | **`B04, B09, B18`** *(`B20` Saved, `-87.8%` Deficit)* |
| **3** | **No (`False`)** | **`fcfs`** | **No** | **12** | **0** | **0.0** | **1,080.0** | **7,872.0** | **12** | — *(Proves `F016` is the root cause)* |
| **4** | **No (`False`)** | **`urgency`** | **No** | **12** | **0** | **0.0** | **1,080.0** | **7,872.0** | **0** | — *(0 moves, 0 missed when no hardware trip)* |
| **5** | **Yes (`True`)** | **`urgency`** | **Yes** | **12** | **0** | **0.0** | **1,080.0** | **7,872.0** | **0** | — *(Cross-cabinet tie alone solves all 4 buses)* |
| **6** | **Yes (`True`)** | **`fcfs`** | **Yes** | **12** | **3** | **309.0** | **1,080.0** | **7,563.0** | **16** | `B04, B18, B20` |
| **7** | **No (`False`)** | **`urgency`** | **Yes** | **24** | **8** | **1,040.1** | **1,080.0** | **6,832.0** | **0** | `B03, B04, B06, B09, B13, B17, B18, B20` *(8 buses trapped on C1-3)* |
| **8** | **Yes (`True`)** | **`urgency`** | **Yes** | **24** | **0** | **0.0** | **1,080.0** | **7,872.0** | **0** | — *(24 plugs + cross-tie = `324,000 €`, `13.31 yr`)* |
| 9 | No (`False`) | `fcfs` | Yes | 24 | 8 | 1,278.4 | 1,080.0 | 6,593.6 | 0 | `B03, B04, B06, B09, B13, B17, B18, B20` |
| 10 | No (`False`) | `fcfs` | No | 24 | 5 | 116.8 | 1,080.0 | 7,755.2 | 0 | `B04, B09, B17, B18, B20` |
| 11 | No (`False`) | `urgency` | No | 24 | 0 | 0.0 | 1,080.0 | 7,872.0 | 0 | — |
| 12 | Yes (`True`) | `fcfs` | Yes | 24 | 7 | 1,153.6 | 1,080.0 | 6,718.4 | 8 | `B04, B06, B09, B13, B17, B18, B20` |
| 13 | Yes (`True`) | `fcfs` | No | 12 | 0 | 0.0 | 1,080.0 | 7,872.0 | 12 | — |
| 14 | Yes (`True`) | `fcfs` | No | 24 | 5 | 116.8 | 1,080.0 | 7,755.2 | 0 | `B04, B09, B17, B18, B20` |
| 15 | Yes (`True`) | `urgency` | No | 12 | 0 | 0.0 | 1,080.0 | 7,872.0 | 0 | — |
| 16 | Yes (`True`) | `urgency` | No | 24 | 0 | 0.0 | 1,080.0 | 7,872.0 | 0 | — |

---

## 3. Four-Way Engineering Trade-Off Table for Station S1

| Option | Hardware Configuration | Software Strategy | Human Moves on Scenario Day | S1 Missed Departures | S1 Simulated Deficit (kWh) | CAPEX & Commercial Trade-Off |
|---|---|---|---|---|---|---|
| **Option 1 (Deployed Software Core)** | Existing 12 guns, `cross_tie=False` | **`urgency` MILP** | **`0` moves** *(vs `12` in FCFS)* | **`3`** (`B20` saved) | **`48.8 kWh` (`-87.8%`)** | **`0 €` CAPEX** · Immediate deployment · Respects strict `chargers.csv` wiring |
| **Option 2 (Cross-Cabinet Busbar Tie)** | Existing 12 guns + inter-cabinet DC tie (`cross_tie=True`) | **`urgency` MILP** | **`0` moves** | **`0`** | **`0.0 kWh` (`-100%`)** | Requires factory inter-cabinet busbar tie (not priced in `equipment_costs.csv`) |
| **Option 3 (24-Plug Dual-Gun + Tie)** | 24 dual-gun points (`+12` guns) **AND** `cross_tie=True` | **`urgency` MILP** | **`0` moves** | **`0`** | **`0.0 kWh` (`-100%`)** | **`324,000 €` CAPEX** (`27,000 €/gun` per `equipment_costs.csv`, `13.31-yr` standalone payback vs `24,336 €/yr` S1 replug labor). ⚠️ **The `324,000 €` buys dispensers only. Without the busbar tie it is Cell 7: `8` missed (WORSE). Never quote `324,000 € -> 0 missed` as if plugs alone did it.** |
| **Option 4 (Counterfactual Manual Swap)** | Existing 12 guns, `cross_tie=False` | `01:30` batch swap | `11–12` moves | `0` | `0.0 kWh` | **Violates Rule 3 (Zero Human Intervention)** — retained only as counterfactual stress test in `virtual_replug.py` |
| **Option 5 (Cabinet Upsizing, 12 guns kept)** | 12 guns, `cross_tie=False`, cabinets `3×400` / `3×450` kW | **`urgency` MILP** | `0` moves | **`4`** / **`0`** | `130.4` / `0.0 kWh` | `dc_charging_power = 280 €/kW` → `33,600 €` / `75,600 €`. **`3×450` reaches `0` but peaks at `1,350 kW`, exceeding the `1,200 kW` grid limit → physically infeasible.** `3×400` sits exactly at the limit and still misses `4`. |

**Why Option 5 matters**: it closes the last loophole. Adding hardware can only reach zero by breaking the grid limit, so **the only zero-miss configuration that stays legal is Option 2 (busbar tie on the existing 12 guns)** — and the busbar has no price in `equipment_costs.csv`. This is a *stated capability boundary*, not a defect.

---

## 4. S2 and S5 Same-Engine Calibration Results (`Scenario Day 2026-11-13`)

Both S2 and S5 discrete event simulation engines are now fully calibrated against the physical topology, hardware commissioning constraints, and DSO grid events recorded in the official dataset:

### Station S2 (Logistics Depot East, 2×400 kW Cabinets, 8 Guns @ 300 kW, Grid Limit 800 kW)
- **Official Crisis Factor**: Grid curtailment event `G1` (`grid_events.csv`) caps site import from `800 kW` to **`400 kW`** between `16:00:00` and `19:00:00+02:00`.
- **Contention Window**: Between `14:20` and `14:45`, 8 trucks arrive simultaneously:
  - 4 short-dwell trucks (`T01, T02, T03, T04`) departing between `17:30` and `18:15` (`need_kwh = 1,250.1 kWh` total, req SoC `70%`);
  - 4 overnight long-dwell trucks (`T05, T06, T07, T08`) departing next day at `06:00` (`need_kwh = 1,533.1 kWh` total, req SoC `85%`).
- **Same-Engine Simulation Results**:
  - **Baseline (`fcfs`, unmanaged equal power sharing under G1 400 kW cap)**:
    - Missed departures: **4 trucks (`T01, T02, T03, T04`)**
    - Undercharged vehicles: `T01 (44.8 kWh), T02 (109.7 kWh), T03 (51.4 kWh), T04 (73.0 kWh)`
    - Simulated energy deficit: **`278.9 kWh`** (matches official recorded deficit of **`283.50 kWh`** within 1.6%!)
    - Peak power: `800.0 kW` (capped to `400.0 kW` during 16:00–19:00)
    - Manual moves: `0`
  - **Optimized (`urgency`, continuous priority preemption under G1 400 kW cap)**:
    - Missed departures: **`0`** (all 4 trucks `T01–T04` reach `70%` SoC on time before departure!)
    - Simulated energy deficit: **`0.0 kWh`** (`-100%`)
    - Peak power: `800.0 kW` (strictly respects `400.0 kW` during 16:00–19:00)
    - Manual moves: **`0`**
    - Overnight trucks `T05–T08` are deprioritized during 14:20–18:15 and finish charging overnight before 06:00.

### Station S5 (Suburban Bus Depot, 2×450 kW Cabinets = 900 kW, 8 Guns @ 150 kW)
- **Official Commissioning Defects** (`site_config.csv` rows 164, 191–196):
  - Misconfigured `grid_limit_kw = 600 kW` (instead of `900 kW` in `sites.csv` and `power_cabinets.csv`);
  - Dispenser `D5-7` throttled to `max_kw = 50 kW`;
  - Dispenser `D5-8` inactive (`sim_active = false` -> `0 kW`).
  - In official baseline, 12 buses arrive overnight; because only 7 guns are active, 5 buses (`B27, B28, B33, B34, B35`) miss departure with **`508.95 kWh`** recorded deficit due to operator manual replug delay until 03:30.
- **Same-Engine Simulation Results**:
  - **Baseline (`fcfs`, unreconciled: 600 kW grid limit, D5-7@50kW, D5-8 inactive)**:
    - Missed departures: **`1`** (`B35`) under unconstrained continuous simulation (**`5`** under official delayed batch swap)
    - Simulated energy deficit: **`365.4 kWh`** (official recorded: `508.95 kWh`)
    - Peak power: `600.0 kW` (clamped by misconfigured grid limit)
    - Manual moves: **`4` moves**
  - **Optimized (`urgency`, Three-Way Config Reconciler: 900 kW grid limit, 8×150 kW guns)**:
    - Missed departures: **`0`** (all 12 buses satisfied on time!)
    - Simulated energy deficit: **`0.0 kWh`** (`-100%`)
    - Peak power: `900.0 kW` (fully utilizes commissioned cabinet capacity)
    - Manual moves: **`0` moves** (zero human touches, eliminates all 4 moves!)

---

## 5. Master Scenario Day Calibration Summary (Same-Engine A/B Comparison)

| Site | Same-Engine Baseline (FCFS) | Optimized (Zero-CAPEX Urgency) | Improvement | Official Record |
|:---:|:---:|:---:|:---:|:---:|
| **S1** | **4 missed** (`B04, B09, B18, B20`, 398.5 kWh, 12 moves) | **3 missed** (`B04, B09, B18`, 48.8 kWh, **0 moves**) | **`B20` saved, `-87.8%` deficit, 0 moves** | 4 missed (1,012.0 kWh absolute gap) |
| **S2** | **4 missed** (`T01, T02, T03, T04`, 278.9 kWh, 0 moves) | **0 missed** (`0.0 kWh`, **0 moves**) | **`-100%` deficit (all 4 trucks saved)** | 4 missed (283.50 kWh recorded deficit) |
| **S5** | **1–5 missed** (`B35`, 365.4 kWh, 4 moves) | **0 missed** (`0.0 kWh`, **0 moves**) | **`-100%` deficit, 0 moves** | 5 missed (508.95 kWh recorded deficit) |
