# S1 / S2 / S5 Same-Engine Causal Attribution Matrix (`docs/attribution_matrix.md`)

> **Reproducibility**: All 16 S1 cells and 8 S2/S5 cells below are generated directly from [`src/sim/discrete_sim.py`](../src/sim/discrete_sim.py) (`load_fleet_jobs(..., depart_date="2026-11-13")` and `run_discrete_event_simulation(...)`) against the unmodified [`fleet_schedule.csv`](../kempower-challenge/kempower-challenge-data/fleet_schedule.csv), [`chargers.csv`](../kempower-challenge/kempower-challenge-data/chargers.csv), and [`power_cabinets.csv`](../kempower-challenge/kempower-challenge-data/power_cabinets.csv).

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

## 4. S2 and S5 Same-Engine Verification (`depart_date="2026-11-13"`)

Evaluating `S2` (`18` total departures on `2026-11-13`, `2×400 kW` cabinets, `8` guns @ `300 kW`, `cross_tie=False`) and `S5` (`12` total departures on `2026-11-13`, `2×450 kW` cabinets, `8` guns @ `150 kW`, `cross_tie=False`) under the exact same `depart_date="2026-11-13"` filter:

| Site | Filter (`depart_date="2026-11-13"`) | Total Jobs | Strategy | Cross-Cabinet Tie | Missed Departures | Simulated Deficit (kWh) | Manual Moves (`moves`) | Notes |
|:---:|:---:|:---:|:---:|:---:|:---:|---:|:---:|:---|
| **S2** | Full Day (`night_only=False`) | **18** | `fcfs` | `False` | `1` | `24.0 kWh` | `0` | Afternoon/full-day contention under naive FCFS |
| **S2** | Full Day (`night_only=False`) | **18** | **`urgency`** | `False` | **`0`** | **`0.0 kWh`** | **`0`** | **100% on-time (`4 -> 0` vs official baseline)** |
| **S2** | Night Window (`night_only=True`) | **18** | **`urgency`** | `False` | **`0`** | **`0.0 kWh`** | **`0`** | **100% on-time** |
| **S5** | Full Day (`night_only=False`) | **12** | `fcfs` | `False` | `0` | `0.0 kWh` | **`4`** | Requires 4 manual moves under FCFS |
| **S5** | Full Day (`night_only=False`) | **12** | **`urgency`** | `False` | **`0`** | **`0.0 kWh`** | **`0`** | **0 missed, 0 manual moves under reconciled 900 kW** |
| **S5** | Night Window (`night_only=True`) | **12** | **`urgency`** | `False` | **`0`** | **`0.0 kWh`** | **`0`** | **0 missed, 0 manual moves** |
