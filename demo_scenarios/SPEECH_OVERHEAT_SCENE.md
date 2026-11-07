# S1 Night Replay Deep-Dive · Spoken Script & Operator Guide

> Companion script for `demo_scenarios/pages/1_Night_Replay.py`.  
> All numbers are derived from the 45 official CSV files and minute-by-minute discrete simulations in `src/sim/discrete_sim.py`.
> Includes a 30-second elevator pitch, key numerical anchors, anticipated judge Q&A, and prohibited claims.

---

## 0. Executive Architecture: Six Pages ↔ Six Problems ↔ One Core Philosophy

The demonstration is organized as **one operational crisis per independent Streamlit page**. Each page presents a direct counterfactual comparison between the legacy system and Project Sentinel under identical conditions:

| # | Page Entry | Operational Crisis | Underlying Principle | Empirical Result |
|---|---|---|---|---|
| **1** | `1_Night_Replay` | Cabinet Overheat (02:25) & Replug | Having fewer plugs than vehicles forces midnight replugging; expanding connection points eliminates the task | 4 missed departures / 9 human moves → **0 missed / 0 moves** |
| **2** | `2_Outage_Replay` | 2-Hour WAN Loss (11:00–13:00) | An outage severs central decision authority, not power; move DLM logic to the edge | Drops to 500 kW → **Sustains 1,425 kW locally** |
| **3** | `3_Price_Spike_Replay` | Spot Price Peak 799.30 €/MWh (18:00) | Prioritize departure deadlines before evaluating electricity prices | 1 missed / 342.66 € → **0 missed / 179.90 €** |
| **4** | `4_Curtailment_Replay` | 400 kW Grid Curtailment (16:00–19:00) | Curtailment is a rationing priority problem: urgent departures charge first | 4 missed / 2,162 kWh → **0 missed / 2,783 kWh** |
| **5** | `5_Cable_Fault_Replay` | Cable Damage F017 (21:30) | Local hardware loop triggers 40 ms lockout with zero cloud round-trip delay | 30s cloud dispatch → **<0.1s local lockout** |
| **6** | `6_Commissioning_Replay` | Three-Way Config Mismatch | Automated configuration reconciler cross-verifies nameplates and ratings | 5 missed departures → **0 missed departures** |

**The Unifying Message**: We did not develop six disjointed patches. We engineered a single unified operating framework:
- When a vehicle arrives, prioritize by its departure deadline.
- When hardware overheats, route power around degraded modules.
- When energy prices spike, defer flexible overnight loads.
- When cables fail, lock out faulty circuits in milliseconds.
- When configurations conflict, reconcile registers autonomously.

**The goal is not an imaginary world where machines never break, but an industrial architecture where broken machines no longer require human triage.**

---

## 1. Core Thesis to Remember

**"We are not demonstrating how clever our AI is; we are proving that an entire human workflow has been rendered obsolete."**

That workflow is: *A human worker waking up at midnight in freezing snow to unplug charging cables from full buses and move them to empty ones.*  
It exists for exactly one reason: **there are fewer plugs than vehicles**.  
Project Sentinel eliminates that bottleneck by ensuring 1:1 stall-to-connection availability and intelligent urgency routing.

---

## 2. Provenance of the Animation Data (693 Minute-by-Minute Frames)

The simulation reconstructs the actual historical night recorded in the official dataset:  
**November 12, 2026, 18:58 to November 13, 2026, 06:30** at municipal bus depot **S1**, tracking **24 overnight transit buses**.

The dwell period is sliced into **693 discrete one-minute frames**. In each frame, every bus occupies one of five operational states:

| Vehicle State | Visual Representation | Physical Meaning |
|---|---|---|
| **Charging** | Blue card, displaying active kW | Cable connected, actively drawing power |
| **Queued** | Grey card, marked `queue` | Bus is in the depot, but no plug is available |
| **Full** | Green card, marked `full` | Has achieved target departure SoC |
| **Undercharged** | Red card, marked `SHORT` | Reached departure time without sufficient charge |
| **Not Arrived** | Dim grey, marked `—` | Still on daytime transit route |

- **Left Column (Baseline)**: 12 single-cable dispensers. At 00:30, an operator manually performs 9 replug trips.
- **Right Column (Project Sentinel Hardware Tier 3b)**: 24 dual-satellite connection points + cross-cabinet busbar tie, **zero human intervention all night**.

**Both columns process the identical 24 buses, identical 1,080 kW grid connection, and identical 02:25 thermal fault.** The sole differences are connection point topology and autonomous edge dispatch.

---

## 3. Verbatim Pitch Narration for S1 Night Replay

### Section 1: The Midnight Baseline Bottleneck (0:00 – 0:45)
"Look at the left column. It is 19:30 on November 12th. Twelve buses have returned to depot S1 and occupied all 12 dispensers. 
Notice what happens when the 13th bus arrives at 20:00: it cannot charge. It parks in an unpowered stall. 

By 23:00, the first 12 buses are already 90% full, but they remain plugged in because no human is on site. 
Finally, at 00:30, a night-shift operator arrives. In the baseline log, this worker takes 72 minutes to complete 9 cable replugs. 

Notice the fatal flaw of human batch replugging: because humans batch their rounds to sleep between shifts, late-arriving buses B04, B18, and B20 miss the window entirely and receive zero charge all night."

### Section 2: The Thermal Fault at 02:25 (0:45 – 1:30)
"At 02:25, watch cabinet C1-3. Its internal telemetry exceeds thermal thresholds, and the cabinet trips offline. 
In the baseline, four dispensers go completely dead. Buses B09, B10, B11, and B12 are stranded mid-charge. 

Now look at the right column under Project Sentinel. 
First, all 24 buses have a physical connection point from the moment they arrive. 
Second, our edge urgency scheduler allocates power using Earliest Deadline First waterfilling. 
By 02:25—the exact moment cabinet C1-3 trips—the entire fleet is already 98.5% charged. 
When the fault occurs, power seamlessly routes through cabinets C1-1 and C1-2 via the cross-cabinet busbar tie. 
By 02:31, every single bus in the depot is 100% fully charged."

### Section 3: Morning Tally & Reconciliation (1:30 – 2:00)
"At 06:30 morning roll-out, we inspect the ledger:
- Legacy Baseline: 4 buses depart undercharged (B04, B18, B20 short by 328 kWh each; B09 short by 28 kWh), burning 9 human replug interventions.
- Project Sentinel: 0 undercharged buses, 0 minutes of human intervention, completed 4 hours ahead of schedule.

Zero human labor is not an abstract software promise; it is an engineered operational reality."

---

## 4. 30-Second Elevator Pitch Summary

"Depot S1 had 24 buses but only 12 plugs, forcing a midnight operator to swap cables. At 02:25, a charging cabinet overheated. The legacy system stranded 4 buses undercharged and logged 9 human interventions. We expanded the dispensers into dual-cable outputs, allowing evening drivers to self-plug upon arrival, and prioritized power by departure deadlines. By 02:31, the entire fleet was fully charged. When the cabinet tripped, the depot was already done charging. Result: zero missed departures, zero human moves, and four hours of operational safety buffer."

---

## 5. Numerical Fact Sheet for Q&A Defense

| Metric | Baseline Value | Project Sentinel Value | Source Reference |
|---|---|---|---|
| **Total Fleet Size** | 24 buses (32 daily departures) | 24 buses | `fleet_schedule.csv` |
| **Grid Power Limit** | 1,200 kW | 1,200 kW (1,080 kW rectifiers) | `grid_capacity.csv` |
| **Baseline Replug Events** | 9 events at S1 (5,596 network-wide) | 0 events | `operations_log.csv` |
| **Cabinet Overheat Timestamp** | 02:25:00 on 2026-11-13 | 02:25:00 on 2026-11-13 | `faults.csv` (F015/F016) |
| **Predictive Alert Lead Time** | Baseline: 0 min (reactive) | 199 minutes prior (22:31) | Telemetry fan slope model |
| **Fleet Full Charge Timestamp** | 06:30 (with 4 deficits) | **02:31:00** (100% full) | `run_s1.py` deterministic output |
| **Single-Depot Hardware CAPEX** | 0 € (status quo) | **216,000 €** (conservative full unit) | `equipment_costs.csv` |

---

## 6. Judge Q&A Defense Strategies

### Question 1: "Does your software alone achieve zero missed departures at S1?"
**Direct Answer**:  
"No, and anyone claiming pure software can achieve zero missed departures at S1 is ignoring physical constraints. With 24 buses and only 12 physical plugs, 12 buses physically cannot draw power simultaneously. 
Under pure 0-CAPEX software with 12 plugs, Sentinel reduces missed departures from 4 to 3 (saving bus B20) and cuts the energy deficit by 87.8% (from 398.5 kWh down to 48.8 kWh). 
To achieve absolute 0 missed departures, you must eliminate the physical bottleneck by adding 12 connection points (216,000 €) and a cross-cabinet busbar tie."

### Question 2: "If drivers plug in their own buses, doesn't that violate the 'zero human' rule?"
**Direct Answer**:  
"No. The competition brief asks: *'If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?'*  
A bus driver plugging in their vehicle upon parking at the end of their driving shift is regular equipment usage, exactly like plugging in a mobile phone. It is not charging network operations and maintenance. What the rule eliminates is dedicated operations staff waking up at midnight to move cables."
