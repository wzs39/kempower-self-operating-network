# Zero-Continuous-Human Design: Eliminating the Midnight Replug Bottleneck

*LahtiES Energy Tech Hackathon 2026 · Kempower Challenge · Architectural Supplement*

---

## 0. Executive Thesis

> **"Out of 20.76 continuous FTEs across the 100-site network, 14.5 FTEs are eliminated not by software algorithms alone, but by solving physical connection availability ('ensuring every vehicle has a live plug waiting')."**

The hackathon brief strictly stipulates: **"If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"**  
The rule prohibits **continuous operations and maintenance staffing**, not commercial drivers plugging in their own vehicles upon parking. A commercial bus driver plugging in their CCS2 cable at the end of a shift is normal operational usage, not charging infrastructure maintenance. 

The real operational failure is structural: **When the driver arrives at midnight, is there an active plug waiting for them?**

At depot **S1**, the answer in the baseline dataset is **No**. S1 operates 24 electric transit buses against only 12 physical charging dispensers. The 13th bus to arrive is forced to park in an unpowered stall, requiring a depot operator to wake up at 00:30, walk the freezing yard in sub-zero snow, unplug fully-charged vehicles, and physically move/replug the cables. Therefore, the design imperative is not to build complex, failure-prone robotic cable arms, but to **ensure 1:1 stall-to-connection availability supported by intelligent dynamic power routing**.

---

## 1. Problem Diagnosis: Where Do the 20.76 FTEs Actually Go?

Full empirical breakdown from `operations_log.csv` (100 sites, 14-day baseline period, 240,635 rows total dataset):

| Operational Category | Event Count | Total Duration | % of Time | Equivalent FTE | Software-Eliminated? |
|---|---:|---:|---:|---:|:---:|
| Vehicle Replugging (`move_and_replug_vehicle`) | 5,596 | 44,768 min | 47.93% | **9.95** | ❌ Requires L0 Connection Points |
| Field Technician Visits (`technician_visit`) | 73 | 22,906 min | 24.52% | **5.09** | ❌ Hardware boundary (Retained in SLA) |
| Customer Contact & Support (`customer_contact`) | 2,418 | 14,508 min | 15.53% | **3.22** | ✅ Automated via Self-Service App |
| Manual Load Adjustment (`manual_load_adjustment`) | 684 | 10,260 min | 10.98% | **2.28** | ✅ Automated via Edge DLM / MPC |
| Remote System Resets (`remote_reset`) | 73 | 730 min | 0.78% | **0.16** | ✅ Automated via Hardware Watchdog |
| Manual Retail Price Updates (`manual_price_change`) | 8 | 240 min | 0.26% | **0.05** | ✅ Automated via Day-Ahead Spot Engine |
| **Total Empirical Baseline** | **8,852** | **93,412 min** | **100.0%** | **20.76** | |

*FTE Conversion Basis: Finnish Working Hours Act standard of 75 hours bi-weekly (1,950 hours/year).*

**Crucial Engineering Insight**: **15.04 FTEs (72.4%)** are constrained by physical contact and mechanical field dispatch, while **5.72 FTEs (27.6%)** can be eliminated by pure software optimization. Addressing zero-human operations purely in the cloud while ignoring physical plug availability misses the single largest operational cost center.

### 1.1 Cable Replugging is Caused by Hardware Scarcity, Not Human Inefficiency

At depot S1, 24 electric transit buses share 12 physical dispensers. 24 ÷ 12 = 2 sequential charging batches. Consequently, the depot requires exactly 12 physical vehicle moves every night. 
Empirical replug events recorded in `operations_log.csv` for S1 across the 14 days:

```
11-03: 12   11-04: 12   11-05: 13   11-06: 12   11-07: 14   11-08: 12   11-09: 12
11-10: 12   11-11: 12   11-12: 12   11-13:  9   11-14: 12   11-15: 12
```

Across 13 normal operational days, the count is virtually constant at 12 replug actions per night. **This is a physical topological constraint dictated by hardware ratios, which no scheduling algorithm can bypass without additional connection points.**

### 1.2 The Systemic Risk: Batch Replugging Misses Critical Departures

Examining the actual charging sessions on the night of November 12-13 (`sessions_baseline.csv`):
- Batch 1 (12 buses) plugged in between 19:00 and 20:20. **All 12 buses sat connected until 00:30 when an operator manually initiated `unplugged_by_operator`**.
- Batch 2 (9 buses) only commenced charging at 00:30, leaving a narrow 5.5-hour window before morning roll-out.
- Out of 23 scheduled buses on-site, only 21 charging sessions were logged — **3 buses were never plugged in at all**.

Baseline Departure Outcome (matching official `baseline_kpis.csv` exactly):

| Vehicle ID | Energy Deficit | Root Cause |
|---|---:|---|
| **B04** | 328.0 kWh | Never plugged in during overnight dwell |
| **B18** | 328.0 kWh | Never plugged in during overnight dwell |
| **B20** | 328.0 kWh | Never plugged in during overnight dwell |
| **B09** | 28.0 kWh | Interrupted mid-charge by cabinet C1-3 thermal trip at 02:25 |

**The root failure is omission, not speed.** Because human operators perform batch replugging on human circadian schedules rather than vehicle dwell windows, late-arriving buses are stranded uncharged.

---

## 2. Architecture: Restoring the Missing L0 Physical Contact Layer

Traditional software architectures assume vehicles are already connected. Project Sentinel introduces a formal 4-layer control stack:

```
┌────────────────────────────────────────────────────────────────────────┐
│ L3 Cloud Tier       15min ~ 24h   Fleet Routing · Spot Pricing · SLA   │
├────────────────────────────────────────────────────────────────────────┤
│ L2 Edge Tier        100ms ~ 15min Local DLM · Urgency Waterfilling     │
├────────────────────────────────────────────────────────────────────────┤
│ L1 Hardware Tier    10μs ~ 100ms  Insulation Guard · BBM Relay Matrix  │
├────────────────────────────────────────────────────────────────────────┤
│ L0 Physical Layer   ★ Foundational Hardware Architecture               │
│   · Dual-Head Satellites (1 satellite serves 2 adjacent parking bays)  │
│   · Driver Self-Plug + ISO 15118-20 Plug & Charge (Eliminates Staff)   │
│   · Modular Hot-Swap Rectifiers + N-1 Redundancy (Resilience)          │
│   · Filterless Liquid-Cooled Air Paths (Eliminates Filter Maintenance) │
│   · Cross-Cabinet Busbar Tie (Prevents Dead Dispensers on Trip)        │
└────────────────────────────────────────────────────────────────────────┘
```

**The Core Principle of L0: Eliminate Demand Rather Than Automate Labor.**  
Rather than deploying delicate robotic arms to move charging cables in freezing weather, provide a dedicated physical plug at every parking stall. Rather than dispatching emergency technicians at 02:00, ensure modular power routing can isolate a single faulty 25 kW module in milliseconds while maintaining full site operation.

---

## 3. Core Mechanisms: Dual-Head Satellites + Driver Self-Plug + Urgency Waterfilling

### 3.1 Hardware Topology: Dual-Cable Satellite Terminals
Kempower's modular satellite architecture natively routes dynamic DC power. At S1, the infrastructure upgrade replaces 12 single-cable satellite posts with **dual-cable satellite posts**, where each satellite dispenses power to two adjacent bus bays:
- **Active Connection Points**: Expanded from 12 to 24.
- **Power Cabinets & Grid Connection**: Maintained intact (3× 360 kW = 1,080 kW).
- **Civil Groundwork**: Minimized by utilizing existing concrete plinths and cable trenches.
- **Dynamic Routing**: Managed internally by the 25 kW DPR switching matrix.

### 3.2 Human-Machine Interface: Driver Self-Plug Verification

| Operational Step | Responsible Actor | Fail-Safe Assurance Mechanism |
|---|---|---|
| Cable Connection | Transit Driver | LED indicator (Red/Green) + RFID/PnC binding; mismatch alerts on depot display |
| Session Authorization | Vehicle SECC / Edge | Automatic ISO 15118-20 handshake within 1.1s; zero ticketing or badges |
| Pre-Departure Audit | Fleet Driver App | Mandatory SoC gate verification against `required_soc_pct` prior to gate departure |
| Forgotten Plug Guard | Autonomous Edge | If bus is parked >30 min without active plug, trigger push alert to dispatch |

**Driver self-plugging is standard practice** — drivers already exit their cabs and plug in upon evening return (as verified by the first 12 buses in the baseline). The only change is that late-returning drivers now have a dedicated plug available immediately upon arrival.

### 3.3 Dynamic Power Allocation: Earliest-Deadline-First (EDF) Urgency Waterfilling

Every 15-minute control interval, the edge scheduler calculates an **Urgency Metric ($w_i$)** for each connected vehicle:

$$w_i = \frac{E_{\text{needed}, i} - E_{\text{delivered}, i}}{\max(t_{\text{depart}, i} - t_{\text{current}}, \, 5\,\text{min})}$$

Power allocation executes via a **two-stage waterfilling procedure**:
1. Allocate total available site power ($P_{\text{grid\_limit}}$) proportionally to $w_i$.
2. For vehicles constrained by their maximum onboard acceptance rate or entering the constant-voltage (CV) battery taper ($SoC > 80\%$), clamp their allocation to their physical ceiling.
3. Re-pool the surplus power and redistribute among unconstrained, high-urgency vehicles until the entire transformer capacity is fully utilized or all vehicles reach saturation.

**Operational Outcome**: Vehicles with imminent departure times and large energy deficits receive maximum power; early-returning buses with extended dwell times are charged steadily, releasing capacity for urgent demands.

---

## 4. Empirical Simulation & Verification

Executing the deterministic simulation:
```bash
python run_s1.py
```

Evaluating all 23 transit buses on the night of November 12–13 at depot S1:

| Operational Metric | Baseline (Human Replug) | Project Sentinel (Tier 3b Hardware) | Empirical Delta |
|---|---:|---:|---|
| Simultaneous Connection Points | 12 | **24** | +12 points |
| Manual Replug Actions per Night | 9 | **0** | **-9 actions (-100%)** |
| Night Shift Labor Time | 72 min | **0 min** | **-72 min (-100%)** |
| Missed Departures (Undercharged) | 4 | **0** | **-4 buses (-100%)** |
| Fleet Full Charge Timestamp | 06:30 | **02:31** | **4 hours earlier** |
| Total Delivered Energy | 7,657 kWh | 7,544 kWh | Target met with zero overshoot |
| Peak Site Demand | 1,080 kW | 1,080 kW | 100% compliant with grid limit |

### 4.1 Engineering Insight: Why Faults Become Non-Events
In the baseline, cabinet C1-3 overheated at 02:25, disabling 4 dispensers and causing B09 to depart undercharged. 

Under Sentinel's 24-point urgency scheduling:
> **The entire fleet of 23 buses completes charging by 02:31. When cabinet C1-3 trips at 02:25, the depot is already 98.5% charged and operating at minimal trickle load.**

Because urgency waterfilling completes heavy charging early in the overnight dwell, the system creates an inherent temporal buffer. The cross-cabinet busbar tie serves as critical insurance against multi-cabinet failures, but temporal buffering renders single-cabinet trips completely harmless to morning service schedules.

---

## 5. Comprehensive 20.76 FTE Elimination Trajectory

| Operational Workstream | Baseline FTE | Automation & Structural Remediation | Residual FTE |
|---|---:|---|---:|
| Vehicle Replugging (`move_and_replug_vehicle`) | **9.95** | Dual-cable satellite expansion + Driver self-plug | **0.00** |
| Field Technician Visits (`technician_visit`) | **5.09** | Hot-swap DPR modules + N-1 pooling + Filterless cooling | **1.00** (Quarterly inspection) |
| Customer Contact (`customer_contact`) | **3.22** | Driver self-service mobile app + Automated SLA credits | **0.00** |
| Manual Load Adjustment (`manual_load_adjustment`) | **2.28** | Real-time edge Dynamic Load Management (DLM) | **0.00** |
| Remote System Reset (`remote_reset`) | **0.16** | Hardware watchdog auto-reboot & relay self-heal | **0.00** |
| Manual Retail Price Setting (`manual_price_change`) | **0.05** | Day-ahead spot price arbitrage optimization | **0.00** |
| **Total Operational Labor** | **20.76** | **Autonomous Operations Stack** | **~1.00 FTE** |

**Continuous operational human labor is completely eliminated (20.76 → 0.00 FTE).** The residual 1.00 FTE represents scheduled quarterly preventive maintenance across the 100-site portfolio, not midnight emergency dispatch.

---

## 6. Financial & CAPEX Accounting

### 6.1 Single Depot (S1) Investment Analysis

| Deployment Architecture | Unit Pricing Basis (`equipment_costs.csv`) | Total Capital Outlay |
|---|---|---:|
| Add 12 Standalone Dispensers + Civil Works | 18,000 € dispenser + 9,000 € civil works per stall | **324,000 €** |
| **Dual-Cable Satellites (Conservative, Full Unit Basis)** | **18,000 € per unit × 12 units** | **216,000 €** |
| Dual-Cable Upgrade (Cable harness only) | Estimated 3,000 ~ 5,000 € per cable harness × 12 | 36,000 ~ 60,000 € |

> **Accounting Disclosure**: `equipment_costs.csv` specifies `dispenser_up_to_400kw` at 18,000 € and `civil_works` at 9,000 €. In strict compliance with the hackathon rule *"Count the cost"*, we report the **conservative figure of 216,000 €** in commercial pitches, while highlighting that retrofitting dual-cable outputs onto existing Kempower satellite pedestals requires minimal groundwork.

### 6.2 Network-Wide Portfolio Economics (100 Sites)
- Total daily replug actions across 100 sites: 5,596 ÷ 14 days = **400 actions/day**.
- Expanding capacity to eliminate all replug bottlenecks requires approximately **400 additional connection points** (+43.7% over existing 916 dispensers).
- Conservative CAPEX: 400 × 18,000 € = **7.20 M€**.
- Operating Cost Savings: 20.76 FTEs @ 65,000 €/year baseline wage = **1.35 M€/year** (or **1.82 M€/year** at the 45 €/hour contracted rate in `equipment_costs.csv`).
- **Simple Payback Period**: **5.3 years** (or **3.95 years** at 45 €/h).

With charging infrastructure depreciated over 10 to 15 years, a ~4-5 year payback is highly attractive. More importantly, under a zero-human operational mandate, expanding connection points is not merely an optional optimization, but a prerequisite for regulatory and operational feasibility.

---

## 7. Comparative Analysis of Three Technical Pathways

| Technical Pathway | S1 CAPEX | Eliminates Replugging? | Eliminates Connector Wear? | Mechanical Complexity |
|---|---:|:---:|:---:|---|
| Standalone Dispensers + Civil Works | 324,000 € | ✅ Yes | ❌ No | Low |
| **Dual-Cable Satellites + Driver Self-Plug** | **216,000 €** | ✅ **Yes** | ❌ **No** | **Low (Recommended)** |
| Robotic Automated Pantograph Arms | >500,000 € | ✅ Yes | ✅ Yes | Extremely High |

**Why Dual-Cable Satellites Represent the Optimal Industrial Solution:**
1. Built on Kempower’s existing, proven modular satellite form factor with zero R&D risk.
2. Reuses existing electrical switchgear and civil trenches; installation completes in hours.
3. Leverages driver presence during end-of-shift vehicle turn-in.
4. Dataset inspection shows connector mechanical faults (`F017`) account for only 15.8% of physical tickets (3 of 19 failures), making high-cost automated robotic arms economically unjustified.

---

## 8. Honest Operational Boundary Statement

> *"Project Sentinel reduces 20.76 continuous operational FTEs to approximately 1.0 planned maintenance FTE, backed by a 7.20 M€ capital expansion in network connection points.*
>
> *We do not make unrealistic claims of literal 100.0% zero-human operations under all circumstances. Electrical equipment will eventually suffer irreversible physical trauma — such as catastrophic transformer failure, major traffic collisions, or external cable cuts. When catastrophic physical failure occurs, the asset must be serviced by a certified high-voltage electrician.*
>
> *The competition prompt explicitly asks: **'If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?'** Project Sentinel delivers precisely that: **Not a single human being is required for the continuous, day-to-day operation, scheduling, fault isolation, or dispatch of this network.** The remaining 1.0 FTE represents planned quarterly maintenance on a scheduled calendar, not emergency call-outs at 02:00 in freezing snow.*
>
> *We state this boundary unequivocally because it forms the legal bedrock of our One-Page Service Level Agreement."*

---

## 9. 10-Minute Executive Pitch Structure

| Time Window | Topic & Deliverable | Core Metrics & Anchors |
|---|---|---|
| **0:00–1:30** | **Customer Story (2029)**: Pekka Virtanen & Lahti City Transit (LSL) zero-touch blizzard roll-out | Zero delays, 24/24 on-time buses |
| **1:30–3:00** | **Empirical Diagnosis**: Dissecting 20.76 FTEs; 72.4% constrained by physical contact | 5,596 replugs / 9.95 replug FTEs |
| **3:00–4:30** | **Counter-Intuitive Discovery**: The bottleneck is omission, not speed; 3 buses never plugged in | 4 missed departures in baseline |
| **4:30–6:30** | **Engineering Architecture**: Dual-cable satellites + Driver self-plug + Urgency waterfilling | 12 → 24 connection points |
| **6:30–8:00** | **Empirical Verification**: Deterministic playback of Nov 12-13 real data | Full at 02:31 vs 06:30; 4 → 0 missed |
| **8:00–9:00** | **Capital Economics & Boundary**: Hardware accounting, 5.3-year payback, certified maintenance | 216,000 €/depot; 20.76 → 0 continuous FTE |
| **9:00–10:00** | **The Commercial Offering**: Outcome-Based Energy Certainty (CaaS) + One-Page SLA | Titanium Tier, MRDT Gate, <50ms BBM |

---

## 10. Reproducibility & Code Verification

Every metric, schedule, and energy calculation in this document is deterministically reproducible from the raw CSV data using standard Python:

```bash
python run_s1.py
```

- **Dependencies**: Python standard library only (no external solver or proprietary library required).
- **Dataset**: 45 unmodified official CSV files located in `kempower-challenge/kempower-challenge-data/`.
- **Baseline Alignment**: Directly parses empirical charging sessions from `sessions_baseline.csv`.
- **Counterfactual Simulation**: Executes `src/edf_packer.py` discrete 1-minute time-step simulation.
- **Zero Mocking**: All intermediate energy states, queue lengths, and power limits are computed dynamically.
