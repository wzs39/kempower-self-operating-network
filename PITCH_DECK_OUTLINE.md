# 🏆 Project Sentinel: Championship Pitch Deck Outline & Speaker Script
## 10-Minute Championship Presentation for Kempower Challenge 2026
*LahtiES Energy Tech Hackathon 2026 @ LUT University Lahti / CrazyTown*  
*Theme: "The Self-Operating Charging Network" · Final Presentation (Saturday 07.11.2026)*  
*Target Scoring Dimensions: Autonomy (25%) · Grid Impact (20%) · Technical Credibility (20%) · Commercial Viability (20%) · Clarity (15%)*

---

## ⏱️ Executive Presentation Roadmap (10:00 Total)

```
[00:00 - 00:45] Slide 1: The Core Question & The Sentinel Vision
[00:45 - 01:45] Slide 2: The Empirical Ground Truth: The 20.76 FTE Crisis
[01:45 - 02:45] Slide 3: Two-Tier Architecture: Cloud (L3) & Edge FSM (L2) over Kempower DPR (L1)
[02:45 - 04:00] Slide 4: Dimension 1 (25%): Degree of Autonomy & 0-Intervention Scenario Day
[04:00 - 05:15] Slide 5: Dimension 2 (20%): Energy & Grid Impact (0 Overlimits, 1,425 kW DLM, 799.30 € Spike)
[05:15 - 06:30] Slide 6: Dimension 3 (20%): Technical Credibility (OCPP 2.0.1, ISO 15118 PnC, Anti-Fraud, 454 Tests)
[06:30 - 07:45] Slide 7: Dimension 4 (20%): Commercial Viability & The One-Page SLA (CaaS & MRDT Gate)
[07:45 - 08:45] Slide 8: The 2029 Customer Story: A Sub-Zero Night with Pekka Virtanen
[08:45 - 09:30] Slide 9: Dimension 5 (15%): Clarity & Live Interactive Command Center (Streamlit)
[09:30 - 10:00] Slide 10: Conclusion & The Path to 2029 Commercial Deployment
[10:00+]         Defense: Rapid-Fire Q&A Defense Cards for Jury Technical Mentors
```

---

## Slide 1: The Core Question & The Sentinel Vision (00:00 – 00:45)
**Official Judging Focus: Clarity (15%) & Autonomy (25%)**

### Slide Content & Visual Layout
- **Header**: **Project Sentinel: The Self-Operating Charging Network**
- **Tagline**: *"If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"*
- **Visuals**:
  - Left: Traditional CPO Depot (Flashlight, chaotic cable tangles, orange error cones, sleep-deprived night staff moving buses at 02:00).
  - Right: Sentinel Autonomous Depot (Dark depot, sub-zero snow, silent 25 kW modular power routing, green status LEDs, 100% on-time fleet dispatch).
- **Core Thesis**: Moving from reactive hardware vending to **Outcome-Based Autonomous Energy Certainty (CaaS)**.

### Speaker Script (Verbatim)
> "Good morning, Mats, Panu, and esteemed members of the jury.
>
> The challenge Kempower put to us was radical and uncompromising:
> *'If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?'*
>
> Today, across Europe, EV charging relies on an invisible army of humans: dispatchers tweaking kilowatt limits, call center operators rebooting stalled chargers, and night shift staff walking freezing bus yards at 2 AM just to unplug bus #12 and plug in bus #13.
>
> We built **Project Sentinel**. Sentinel is not another monitoring dashboard; it is a full-stack, autonomous operating core that eliminates continuous human intervention. It guarantees that every commercial vehicle leaves on time with 100% required energy, protects the power grid with zero transformer violations, and turns charging infrastructure into an unshakeable commercial SLA.
>
> Let’s look at the hard empirical data that drove our engineering."

---

## Slide 2: The Empirical Ground Truth: The 20.76 FTE Crisis (00:45 – 01:45)
**Official Judging Focus: Technical Credibility (20%) & Commercial Viability (20%)**

### Slide Content & Visual Layout
- **Header**: **The Baseline: 20.76 Full-Time Employees Running in Place**
- **Data Source**: Official Kempower Challenge Dataset (45 CSVs, 240,635 rows across 100 commercial & public sites).
- **Key Metrics Table**:
  | Metric | Value from Official 45 CSVs | Annualized Impact |
  |---|---|---|
  | **Manual Interventions** | 8,852 events / 14 days | 230,152 human actions / year |
  | **Total Labor Duration** | 93,412 minutes (1,556.87 hours) | **20.76 FTE** (based on 37.5 h/wk Finnish law) |
  | **Annual Labor Cost** | 45.00 €/h base (`equipment_costs.csv`) | **1,821,534 € / year** (1.98M € with 80 €/h technician rate) |
  | **Midnight Replugging** | **5,596 events (63.22% count)** | **44,768 min (47.93% duration = 9.95 FTE = 872,976 €/yr)** |
  | **Scenario Day Crisis** | Friday 2026-11-13 (S1–S5) | **13 missed departures, 1,804.45 kWh deficit, 29.69% abandonment** |

- **Visual Callout Box**:
  > **The Replug Bottleneck**: Moving and replugging vehicles is not an edge case—it is **47.93% of all human labor time in the entire network**. At Site S1 alone, 24 buses share 12 dispensers. Without autonomous dynamic routing, operators burn 24,336 €/year at a single depot just playing musical chairs with charging cables.

### Speaker Script (Verbatim)
> "To solve the problem, we did not guess—we audited every single one of the 240,635 rows across all 45 official CSV files.
>
> Here is what the real world looks like: in just two weeks, this 100-site network generated 8,852 manual operations consuming 93,412 staff-minutes. Under Finnish statutory working hours, that represents **20.76 full-time employees** costing **1.82 million euros every single year**.
>
> Look at the breakdown: nearly half of all labor hours—47.93%—is spent on a single repetitive task: `move_and_replug_vehicle`. That is 9.95 full-time workers walking through depots at night to manually swap cables because stations lack dynamic power routing.
>
> And when crisis hit on Scenario Day—Friday, November 13th—the human system collapsed: 13 fleet vehicles missed departure, over 1,800 kWh of energy was stranded, and public hub S3 suffered a 29.7% driver abandonment rate.
>
> We engineered Sentinel to eliminate all 20.76 FTEs of continuous human labor. Here is the architecture."

---

## Slide 3: Two-Tier Architecture: Cloud (L3) & Edge FSM (L2) over Kempower DPR (L1) (01:45 – 02:45)
**Official Judging Focus: Technical Credibility (20%) & Clarity (15%)**

### Slide Content & Visual Layout
- **Header**: **Two-Tier Layered Architecture: Physics-Grounded & Cloud-Orchestrated**
- **Architecture Diagram**:
  ```
  [L3: Autonomous Cloud Orchestrator] (15-min horizon)
  ├── 15-min Rolling MILP Optimizer (SciPy HiGHS)
  ├── Spot Arbitrage (Nord Pool) & Dynamic Peak Demand Shaving (6.50/7.50 €/kW/mo)
  └── Outcome-Based SLA Engine & MRDT Gate Clearing
          │ (OCPP 2.0.1 Smart Charging TxProfile / TLS 1.3 WAN)
          ▼
  [L2: Station Edge Controller] (100ms - 15min autonomous loop)
  ├── Local Dynamic Load Management (DLM) (1,425 kW DC / 1,492.15 kW AC Inverter Guard)
  ├── 72-Hour Offline Islanding Engine (Zero Cloud Dependency)
  ├── Predictive Thermal PdM (199-minute lead time fan degradation alert)
  └── Anti-Phantom Replug & Electrical Fingerprint Fraud Engine
          │ (Modbus / CAN / Break-Before-Make Relay Protocol)
          ▼
  [L1: Physical Hardware & DPR Contactor Matrix] (10μs - 100ms)
  ├── Kempower 25 kW / 50 kW Power Module High-Speed Relay Matrix
  ├── Strict 1:N Power Cabinet Wiring (C1-1..C1-3 -> D1-1..D1-12)
  └── Hard Physical Safety Interlocks: 65°C de-rate, 75°C trip, 90°C pin, 30mA RCD, IMD
  ```

### Speaker Script (Verbatim)
> "Sentinel is built around a fundamental engineering principle: **Never rely on the cloud for physical safety, but never rely on local heuristics for global economic optimality.**
>
> At Layer 3, our Autonomous Cloud Orchestrator solves a rolling 15-minute Mixed-Integer Linear Program (MILP) using the SciPy HiGHS solver. It arbitrates Nord Pool day-ahead spot prices, optimizes Finnish monthly peak demand charges, and compiles vehicle departure deadlines into OCPP 2.0.1 `TxProfiles`.
>
> At Layer 2, our Station Edge Controller runs an autonomous Finite State Machine (FSM). It executes sub-100ms local dynamic load management, anti-phantom replug fraud screening, and predictive thermal health checks. If the WAN fiber is severed, the Edge Controller instantly islands the station for up to 72 hours with zero degradation in local capacity.
>
> At Layer 1, we respect Kempower’s physical hardware: 25 kW modular rectifiers, 1:N copper busbar topology, and a 6-step Break-Before-Make zero-arc switching sequence that completes in 260 milliseconds—well within the 500ms safety envelope.
>
> Now let's see how this performs on the official Scenario Day."

---

## Slide 4: Dimension 1 (25% Autonomy): Zero-Intervention Scenario Day (02:45 – 04:00)
**Official Judging Focus: Degree of Autonomy (25%)**

### Slide Content & Visual Layout
- **Header**: **Autonomy in Action: Scenario Day 2026-11-13 (13 $\to$ 0 Missed Departures)**
- **Scenario Day Resolution Matrix**:
  | Station | Scenario Incident | Baseline Human Outcome | Sentinel Autonomous Action | Sentinel Outcome |
  |---|---|---|---|---|
  | **S1 (Depot North)** | 24 buses on 12 guns; Cabinet C1-3 fan fails (`F015`/`F016` 246m) | 4 buses missed (`B04, B09, B18, B20`), 1,012 kWh deficit | **199-min predictive alert** at 22:31 (`59.3°C/702 rpm`); Strategy A 01:30 wave swap onto C1-1/C1-2 (720 kW N-1) | **0 missed departures** (1,012 kWh fully recovered, 0 € CAPEX) |
  | **S2 (Logistics East)**| DSO 400 kW curtailment (16:00–20:00) | 4 trucks missed (`T01–T04`), 283.50 kWh deficit | Priority preemption: shifts 283.5 kWh from overnight trucks `T05–T08` (1,857 kWh pool) via continuous OCPP | **0 missed departures** (100% on-time dispatch) |
  | **S3 (Highway Hub)** | 2-hour cellular WAN drop (10:00–12:00) | Static 50 kW fallback drops throughput; **29.69% driver abandonment** | Edge controller islands locally; maintains full **1,425 kW DC** load allocation with 0 cloud calls | **Abandonment < 0.5%** (76 drivers saved) |
  | **S4 (Urban Hub)** | **799.30 €/MWh spot price spike** at 18:00 + cable fault | System abandons charging or incurs ruinous cost | MILP lookahead pre-charges buffer; continuous SoC slack prevents false drop; isolates `D4-2` | **0 abandoned vehicles**, 0 overlimit |
  | **S5 (New Depot)** | 3-way config mismatch (600 vs 900 kW) + throttled D5-7/D5-8 | 5 buses missed, 508.95 kWh deficit | Digital twin 3-way reconciliation unlocks **900 kW (+750 kWh)**, unthrottles D5-7 (150kW), activates D5-8 | **0 missed departures** (508.95 kWh recovered) |

- **Autonomy Highlights**:
  - **Predictive Lead Time**: 199 minutes ahead of failure (`2026-11-12T22:31:00+02:00`, `59.3°C / 702 rpm`).
  - **Self-Healing Response**: Sub-100ms contactor isolation; zero cross-cabinet backfeeding.
  - **Fleet Certainty**: **13 $\to$ 0 missed departures**, **1,804.45 kWh total deficit eliminated**.

### Speaker Script (Verbatim)
> "This slide represents the core of the 25% Autonomy score.
>
> On Friday the 13th, the network was hit by five simultaneous compounding crises. In the baseline dataset, humans failed at every single station.
>
> At Bus Depot S1, Cabinet C1-3 overheated and tripped for over 4 hours. But look at Sentinel: our predictive thermal health model detected the degraded fan bearing **199 minutes before the fault occurred**—at 10:31 PM the previous night, when the temperature reached 59.3°C at only 702 RPM. Sentinel automatically scheduled a maintenance ticket, shifted the bus charging wave onto healthy cabinets C1-1 and C1-2 operating at 720 kW N-1 capacity, and cleared all 1,012 kWh of energy.
>
> At Logistics Depot S2, the grid operator cut capacity by 400 kW. Sentinel realized that overnight trucks T05 through T08 had an 1,857 kWh flexibility pool. It throttled them to 1 kW and rerouted 283.5 kWh to afternoon trucks T01 through T04. All four departed on schedule.
>
> At Highway Hub S3, a 2-hour cellular outage triggered the naive 50 kW fallback in baseline, causing 29.7% of public drivers to drive away in disgust. Sentinel’s edge islanding maintained 1,425 kW of local capacity, crushing abandonment to under 0.5%.
>
> And at Depot S5, our automated digital-twin reconciler caught a human configuration error in `site_config.csv` where a 900 kW site was throttled to 600 kW. It restored full 900 kW capacity, unlocking 750 kWh of headroom and eliminating all 5 missed buses.
>
> From 13 missed departures down to exactly zero. 100% autonomous."

---

## Slide 5: Dimension 2 (20% Energy & Grid Impact): 0-Overlimit Invariant & Spot Optimization (04:00 – 05:15)
**Official Judging Focus: Energy and Grid Impact (20%)**

### Slide Content & Visual Layout
- **Header**: **Grid Safety Invariant: Absolute Compliance Across 134,400 Rows**
- **Data Chart / Proof**:
  - **Grid Overlimit Violations**: **0 rows out of 134,400 15-minute intervals** across all 100 sites ($P_{\text{grid}} \le P_{\text{limit}}$ 100.00% compliance).
  - **Inverter Efficiency Invariant**: Rigorous AC-to-DC conversion model:
    $$P_{\text{AC}} = \frac{P_{\text{DC}}}{\eta_{\text{inverter}}} = \frac{1,425.0 \text{ kW}}{0.955} = 1,492.15 \text{ kW} \le 1,500.0 \text{ kW}_{\text{transformer}}$$
    *(Leaves 7.85 kW safety margin; never overcurrents the transformer).*
- **Spot Price Spike Defense (S4 @ 799.30 €/MWh)**:
  - Dimensional scaling: $10^{-3}$ factor converting €/MWh to €/kWh.
  - Continuous SoC slack variable: $z_v \in [0, 1]$ with $10,000 \text{ €}$ penalty prevents solver from discarding viable vehicles during extreme price spikes.
  - Full monthly peak capacity rate: Charged at 6.50 €/kW/mo (depot) and 7.50 €/kW/mo (public) to avoid false localized demand spikes.
- **Microgrid BESS & PV Co-Optimization**:
  - 500 kWh / 250 kW BESS model strictly costed via `equipment_costs.csv` (`320 €/kWh` + `110 €/kW`).
  - Coordinated peak shaving during price spikes and dynamic FCR-N/D auxiliary grid frequency balancing.

### Speaker Script (Verbatim)
> "Next, the 20% Energy and Grid Impact score.
>
> Rule #1 in power engineering: never blow up the substation. Across 134,400 rows of site power telemetry in the official dataset, Sentinel maintains a **100.0% zero-overlimit invariant**. Not once does site load penetrate the transformer ceiling.
>
> Many teams assume that 1,500 kW of DC charging equals 1,500 kW on the AC grid. That is an electrical fallacy. With a 95.5% inverter efficiency, 1,425 kW of DC output draws exactly 1,492.15 kW of AC power from the grid. Sentinel’s Dynamic Load Manager bakes the inverter loss guard directly into its math, keeping site load strictly below 1,500 kW with a 7.85 kW reserve margin.
>
> On Scenario Day, the Nord Pool spot price exploded to 799.30 €/MWh at 18:00. Naive MILP models often drop vehicles because the raw electricity cost exceeds the 250 € contractual penalty. We introduced a continuous SoC slack variable weighted at 10,000 € inside our HiGHS solver, alongside dimensional scaling of spot prices. Sentinel pre-charges vehicles prior to the spike, dynamically shaves the peak, and never leaves a customer stranded."

---

## Slide 6: Dimension 3 (20% Technical Credibility): Standards, Simulation & 454 Tests (05:15 – 06:30)
**Official Judging Focus: Technical Credibility (20%)**

### Slide Content & Visual Layout
- **Header**: **Technical Credibility: Industrial Protocols & Verifiable Proof**
- **Standards & Protocol Implementations**:
  1. **OCPP 2.0.1 Smart Charging**:
     - `SetChargingProfileRequest` with `TxProfile`, `TxDefaultProfile`, and `ChargingStationMaxProfile`.
     - Device Model component-variable telemetry via `NotifyEventRequest` for fan RPM, module temperature, and IMD insulation resistance.
  2. **ISO 15118-2/20 Plug & Charge (PnC)**:
     - Mutual TLS 1.3 handshake verified in **< 1.5 seconds**.
     - ECDSA P-256 certificate chain validation with OpenSSL EVP crypto in **< 10 ms**.
     - Automated OEM provisioning contract authorization; 0 RFID or mobile apps needed.
  3. **Anti-Phantom Replug & Fraud Defense**:
     - Detects reconnect delta $t < 180 \text{ s}$, SoC continuity $\Delta \text{SoC} < 1.0\%$, and current ramp rate $dI/dt > 100 \text{ A/s}$.
     - Merges split sessions, prevents false turnover billing, and protects against spoofed disconnects.
  4. **Closed-Loop Discrete Event Simulation**:
     - Minute-by-minute discrete simulator (derived from teammate `vision6`'s `edf_packer.py`).
     - Replaces hardcoded literals with true dynamic SoC curves, contactor state transitions, and battery acceptance profiles.
- **Verification Proof Table**:
  | Verification Track | Scope | Execution Time | Pass Rate |
  |---|---|---|---|
  | **Deterministic Verifier (`verify_all.py`)** | All S1–S5 Scenarios, 29 GitHub Issue #2 items | **0.29 seconds** | **100% (29/29)** |
  | **Pytest Unit & Integration Suite** | Protocols, DPR, MILP, Self-Healing, SLA | **32.78 seconds** | **100% (348/348)** |
  | **Independent E2E Suite (Tiers 1–4)** | Feature coverage, boundaries, stress, scenarios | **0.606 seconds** | **100% (106/106)** |
  | **Official Dataset Integrity** | 45 CSV files under `kempower-challenge-data/` | Hash Verified | **100% UNTOUCHED** |

### Speaker Script (Verbatim)
> "Judges, in a hackathon, anyone can draw a PowerPoint diagram or hardcode a 'zero missed departures' return value. Technical credibility means proving every single claim with executable code and industrial standards.
>
> We implemented full OCPP 2.0.1 smart charging profiles and ISO 15118 Plug & Charge. Using ECDSA P-256 cryptography, mutual TLS 1.3 handshake authentication executes in under 1.5 seconds, with certificate path validation completing in under 10 milliseconds.
>
> We built an Anti-Phantom Replug and Fraud Defense engine that inspects reconnect time intervals, battery SoC continuity, and current slew rates to eliminate phantom billing.
>
> And we validated our entire system through a true closed-loop discrete event simulation engine that models vehicle charging curves minute-by-minute.
>
> Look at our test numbers:
> - `verify_all.py` executes all 29 audit checks across S1 to S5 in **0.29 seconds**.
> - Our pytest suite has **348 passing tests**.
> - Our independent 4-tier E2E test suite adds another **106 passing tests** in 0.6 seconds.
> - That is **454 automated tests** with 100% pass rate, and zero bytes of the official 45 CSV files were modified. That is technical credibility."

---

## Slide 7: Dimension 4 (20% Commercial Viability): 20.76 FTE Elimination & One-Page SLA (06:30 – 07:45)
**Official Judging Focus: Commercial Viability (20%)**

### Slide Content & Visual Layout
- **Header**: **Commercial Viability: Outcome-Based CaaS & Enforceable SLA**
- **The Financial Transformation**:
  - **OPEX Elimination**: 20.76 FTEs $\times$ 87,750 €/yr = **1,821,534 €/year saved** across 100 sites.
  - **S1 Replug Strategy Comparison (Transparently Grounded in `equipment_costs.csv`)**:
    - **Strategy A (0 € CAPEX Software Coordinated Batch Swap)**:
      - Uses existing 12 dispensers; coordinates a single scheduled 01:30 cable rotation.
      - **CAPEX: 0 €** · Solves all 4 missed buses (`1,012 kWh`) · **Immediate Infinite ROI**.
    - **Strategy B (2029 Hardware Expansion to 24 Guns)**:
      - 12 additional dispensers (`18,000 €`) + civil works (`9,000 €`) = `27,000 €/gun` $\to$ **324,000 € CAPEX**.
      - S1 replug labor savings: 24,336 €/year (156 replugs / 2 weeks).
      - **Standalone Payback Period: 13.31 years** (honest payback; we do not commit the fallacy of attributing 100 sites of labor to 1 site).
- **The One-Page Service Level Agreement (SLA)**:
  - **Outcome-Based Charging-as-a-Service (CaaS)**: Customers pay for guaranteed energy delivery, not kW availability.
  - **Minimum Required Dwell Time (MRDT) Anti-Moral-Hazard Gate**:
    $$\text{MRDT}_j = \left( \frac{\frac{\text{SoC}_{\text{req}} - \text{SoC}_{\text{arrive}}}{100} \cdot E_{\text{batt}}}{\min(P_{\text{charger}}, P_{\text{veh}}) \cdot \eta_{\text{system}}} \right) \cdot 60 + 15.0 \text{ min}$$
    *(If customer arrives later than MRDT, SLA defaults to best-effort; prevents fraudulent delay claims).*
  - **Enforceable Penalties & Caps**:
    - Delayed departure: 250 € base + 5 €/min (>15m) + 1.50 €/kWh deficit.
    - Tiered Availability: Titanium (99.9%), Gold (99.5%), Silver (99.0%).
    - **150% Monthly Liability Cap**: Operators never face ruinous upside losses; non-negative invoicing.

### Speaker Script (Verbatim)
> "Now let's examine the commercial model.
>
> If humans are removed, what is the customer buying? They are not buying a charger; they are buying **Energy Certainty as a Service**.
>
> We grounded all financials strictly in `equipment_costs.csv`. Across 100 sites, eliminating 20.76 FTEs of continuous labor frees up **1.82 million euros annually**.
>
> Look at our treatment of Site S1: many teams claimed that installing 12 new chargers would pay for itself in 6 weeks by falsely applying all 21 FTEs of network labor to S1. That is commercially fraudulent. At S1, replugging costs exactly 24,336 € per year. Installing 12 new dispensers at 27,000 € per gun costs 324,000 €, yielding an honest 13.3-year payback.
>
> That is why Sentinel offers **Strategy A**: a zero-euro CAPEX software solution that schedules a single 01:30 cable swap, eliminating all 4 missed departures tonight with **zero capital expense**.
>
> Furthermore, we authored the **One-Page SLA Specification**. It features our Minimum Required Dwell Time (MRDT) gate, which calculates whether a truck has physically arrived with enough time to receive its energy. If a driver arrives 10 minutes before departure demanding 200 kWh, the MRDT gate protects the CPO from extortion. And our 150% monthly liability cap guarantees that the operator can never lose more than 1.5 times the monthly base fee."

---

## Slide 8: The 2029 Customer Story: A Sub-Zero Night with Pekka Virtanen (07:45 – 08:45)
**Official Judging Focus: Clarity (15%) & Commercial Viability (20%)**

### Slide Content & Visual Layout
- **Header**: **Customer Narrative 2029: A Sub-Zero Winter Night in Lahti**
- **Character**: Pekka Virtanen, Fleet Operations Director, Lahti City Transit (Lahden Seudun Liikenne - LSL).
- **Setting**: Friday, January 19, 2029 · -18°C sub-zero blizzard · Depot North (24 Electric Articulated Buses).
- **The Story Arc in 3 Beats**:
  1. **22:00 – Hands-Free Depot Ingestion**: Driver plugs in bus with ISO 15118 PnC. Mutual TLS 1.3 handshake authenticates vehicle in 1.1s. Driver walks home. No night shift crew on site.
  2. **02:15 – Sub-Zero Thermal Self-Healing**: Temperature drops to -18°C. Battery cell acceptance drops 40%. Sentinel’s Nordic Low-Temp Self-Healing redirects 50 kW to onboard PTC battery pack pre-heating, restoring maximum charge acceptance rate in 18 minutes.
  3. **05:30 – 100% Punctual Morning Rollout**: All 24 buses roll out onto Lahti’s snow-covered streets at 100% target SoC. Pekka wakes up at 06:00, glances at his phone, and sees a single green badge: *"All 24 routes dispatched on time. Zero interventions. Monthly SLA: 99.98%."*

### Speaker Script (Verbatim)
> "Let's bring this to life through a customer story from January 2029.
>
> Meet Pekka Virtanen. Pekka is the Fleet Operations Director for Lahti City Transit. In 2026, Pekka’s hardest job was hiring night shift staff willing to work in sub-zero Finnish blizzards at 2 AM, dragging frozen 400-amp cables through slush to swap plugs.
>
> Fast-forward to January 2029. It is -18°C in Lahti. At 10 PM, 24 electric city buses return to Depot North. Drivers simply plug in the cables. Thanks to ISO 15118 Plug & Charge, the handshake takes 1.1 seconds. The drivers go home. The yard is completely dark and empty.
>
> At 2:15 AM, the freeze sets in. Lithium-ion acceptance rates plunge. Sentinel's Nordic sub-zero self-healing controller detects the battery cold-soak, and dynamically diverts 50 kW of modular power to the buses' PTC battery thermal pre-heaters. Within 18 minutes, the packs reach optimal charging temperature, cutting total session time by 35%.
>
> At 5:30 AM, when the citizens of Lahti step out to catch Bus Line 1 to the University, all 24 buses depart with full batteries, to the exact second.
>
> Pekka wakes up at 6 AM, sips his morning coffee, and looks at his phone. There are no emergency calls, no missed runs, and no disputed invoices. That is what Sentinel delivers."

---

## Slide 9: Dimension 5 (15% Clarity): Live Interactive Command Center (08:45 – 09:30)
**Official Judging Focus: Clarity (15%)**

### Slide Content & Visual Layout
- **Header**: **Interactive Command Center: The 4-Quadrant Streamlit Cockpit**
- **Live UI Visual Walkthrough (`app.py`)**:
  - **Quadrant 1 (Executive Summary)**: Network-wide 20.76 FTE elimination breakdown, 1.82M € savings tracker, 100-site live health status.
  - **Quadrant 2 (Scenario Day 2026-11-13 Minute-by-Minute Live Player)**: Time-slider scrubbing through S1–S5 crises, showing dynamic power allocation and 13 $\to$ 0 missed departures in real time.
  - **Quadrant 3 (2029 Commercial SLA & MRDT Calculator)**: Interactive MRDT boundary calculator, automated monthly invoice clearing statement, Titanium/Gold/Silver tier toggles.
  - **Quadrant 4 (29-Item GitHub Issue #2 Audit & Verification Engine)**: Live sub-second verification runner, instant test execution pass badges.
- **Clarity Metric**: Fully transparent, reproducible with a single command: `streamlit run app.py`.

### Speaker Script (Verbatim)
> "To ensure that non-technical judges and CPO executives have complete visibility, we packaged the entire system into a 4-quadrant interactive Streamlit cockpit.
>
> In Quadrant 1, executives track the exact labor hours and FTE savings across all 100 sites.
>
> In Quadrant 2, you can scrub the minute-by-minute timeline of Friday November 13th. You can watch the fan on Cabinet C1-3 begin to vibrate at 22:31, see Sentinel reroute power across the DPR matrix, and watch the missed departures counter stay firmly at zero.
>
> In Quadrant 3, fleet operators can plug in arrival SoCs and vehicle battery capacities to inspect their exact MRDT thresholds and download audited monthly settlement invoices.
>
> And in Quadrant 4, any auditor can click 'Run Deterministic Audit' and verify all 29 GitHub Issue #2 claims in 0.29 seconds.
>
> The code is clean, modular, and available in this repository today."

---

## Slide 10: Conclusion & The Path to 2029 Deployment (09:30 – 10:00)
**Official Judging Focus: All 5 Scoring Dimensions**

### Slide Content & Visual Layout
- **Header**: **Summary: Why Project Sentinel Wins the Kempower Challenge**
- **Five-Dimension Scorecard**:
  | Judging Dimension | Weight | Project Sentinel Deliverable |
  |---|---|---|
  | **Degree of Autonomy** | **25%** | **13 $\to$ 0 Missed Departures** · 199-min PdM · 85ms DPR Self-Healing · 72h Edge Islanding |
  | **Energy & Grid Impact** | **20%** | **0 Overlimits across 134,400 rows** · 1,425 kW DLM with Inverter Guard · 799.30 € Spike Arbitrage |
  | **Technical Credibility** | **20%** | **OCPP 2.0.1 + ISO 15118 PnC** · Discrete Simulation · Anti-Phantom Defense · **454 Passing Tests** |
  | **Commercial Viability** | **20%** | **20.76 FTE (1.82M €/yr) Eliminated** · Grounded CAPEX · MRDT Gate · 150% Capped SLA |
  | **Clarity** | **15%** | **4-Quadrant Streamlit Live Player** · 2029 Pekka Virtanen Story · Sub-second Deterministic Verifier |

- **Closing Call to Action**:
  > *"Kempower built the world's most flexible DC charging hardware. Sentinel provides the autonomous brain it deserves. Together, we make 2029 zero-touch charging an industrial reality."*

### Speaker Script (Verbatim)
> "In conclusion:
> Kempower already manufactures the finest modular DC fast charging hardware on earth. What the industry needed was an autonomous brain capable of running that hardware without human babysitting.
>
> Project Sentinel delivers that brain.
> We eliminated 20.76 FTEs of human labor.
> We turned 13 missed departures into zero.
> We maintained 100% grid compliance across 134,400 intervals.
> And we backed it all with industrial protocols, 454 automated tests, and an enforceable commercial SLA.
>
> Thank you, and we look forward to your questions."

---

## 🛡️ Appendix: Rapid-Fire Q&A Defense Cards for Judges

### Question 1 (Mats Mattsson - Cloud & Architecture):
*"You claim to operate S1 with 0 missed departures during the 4-hour fan trip on C1-3. But C1-3 powers dispensers D1-9 to D1-12. How did you charge 24 buses on only 8 remaining dispensers without violating cabinet wiring?"*
- **Defense Card**:
  1. We respected strict 1:N cabinet topology (`STATION_CABINET_TOPOLOGY` in `dpr_matrix.py`). We never cross-backfeed power into tripped Cabinet C1-3.
  2. Because our thermal predictive model flagged C1-3 at 22:31 (199 minutes prior to `F015`), Sentinel adjusted the wave scheduling in advance.
  3. Healthy cabinets C1-1 and C1-2 provided 720 kW N-1 continuous power to dispensers D1-1 through D1-8.
  4. Under Strategy A, buses were dispatched in two synchronized waves with a single coordinated 01:30 cable swap, providing 1,012 kWh of total energy and finishing by 05:15.
  5. Verified deterministically in `test_scenario_verification.py` and `verify_all.py` check #3.

### Question 2 (Panu Vartiainen - Hardware & Electrical Engineering):
*"In S3, you claim to run 1,425 kW DC during the 2-hour cellular outage. What prevents this from tripping the 1,500 kW grid transformer when converter losses are included?"*
- **Defense Card**:
  1. We enforce an explicit inverter conversion efficiency of $\eta = 0.955$ ($95.5\%$).
  2. Total AC power drawn is $P_{\text{AC}} = 1,425.0 \text{ kW} / 0.955 = 1,492.15 \text{ kW}$.
  3. This is strictly less than the 1,500.0 kW transformer limit, leaving a 7.85 kW safety buffer.
  4. In contrast, the baseline naive fallback dropped power to 50 kW per dispenser (400 kW total), causing 29.69% driver abandonment. Sentinel’s autonomous local DLM kept throughput at 1,425 kW safely.
  5. Verified in `test_m1_adversarial_probe.py` and `tier2_boundary_corner.py`.

### Question 3 (Commercial Judge):
*"How does your One-Page SLA prevent a fleet customer from gaming the system and claiming liquidated damages for an unavoidable delay?"*
- **Defense Card**:
  1. Section 4.1 of `One_Page_SLA_Specification.md` embeds the Minimum Required Dwell Time (MRDT) gate:
     $$\text{MRDT}_j = \left( \frac{\Delta \text{SoC} \cdot E_{\text{batt}}}{\min(P_{\text{charger}}, P_{\text{veh}}) \cdot 0.95} \right) \cdot 60 + 15.0 \text{ min}$$
  2. If a customer plugs in late such that their dwell time is less than MRDT, the contract explicitly classifies the session as 'Best-Effort Service' and waives all liquidated damages.
  3. Furthermore, total monthly damages are hard-capped at 150% of the monthly base fee, and invoices are mathematically non-negative.
  4. Verified in `test_remediated_sla.py` and `sla_calculator.py`.

### Question 4 (Software & Testing Mentor):
*"How do we know your test suite isn't just testing mock data?"*
- **Defense Card**:
  1. Every single test imports from `src.sim.data_loader`, which directly reads the 45 unedited CSV files from `kempower-challenge/kempower-challenge-data/`.
  2. We run 348 unit/integration tests and 106 opaque-box E2E tests across 4 tiers.
  3. We also provide `verify_all.py`, an independent, standalone zero-dependency Python script that reads the CSV files and evaluates the mathematical invariants directly in 0.29 seconds.
  4. You can clone the repo, run `python verify_all.py`, and inspect every calculation line by line.
