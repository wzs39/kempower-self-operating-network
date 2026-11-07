# Project Sentinel: Demo Day Tripartite Judge Personas & 14 Hardcore Question Bank

**Document ID**: `SIM-03-JUDGE-PERSONAS-QUESTION-BANK`  
**Feature Inventory**: F6 (Tripartite Judge Persona Profiles) & F7 (14 Core Hardcore Question Bank)  
**Milestone**: M3  
**Competition Date**: Saturday 07.11.2026, LUT University Lahti Campus (Kempower Challenge · LahtiES Energy Tech Hackathon)  
**Perspective**: Equipment Manufacturer / Turnkey Service Provider (`contracts.csv`), holding service scope, SLA performance commitments, and late-departure penalty liabilities.

---

## Executive Overview

Demo Day at the LahtiES Energy Tech Hackathon puts Project Sentinel in front of a multidisciplinary judging panel representing power electronics hardware engineers, cloud system architects, early-stage venture investors, and industrial challenge hosts. To win 1st place across all five official criteria (**Degree of Autonomy 25%**, **Energy and Grid Impact 20%**, **Technical Credibility 20%**, **Commercial Viability 20%**, and **Clarity 15%**), the team must withstand rigorous cross-examination that tests the boundaries of physics, code, economics, and data integrity.

This document establishes:
1. **Three Tripartite Judge Personas**: Detailed psychological archetypes, technical lenses, red-flag triggers, and evaluation scorecards for Technical/Architect, Commercial/VC, and Kempower Challenge custodians.
2. **14 Core Hardcore Questions Bank (Q01–Q14)**: The definitive repository of aggressive, edge-probing, and cross-disciplinary questions designed to expose superficial claims and test every aspect of the 45-CSV dataset (240,635 rows), mathematical formulations, and electrical hardware realities.

---

# Section 1: Tripartite Judge Persona Profiles (Feature F6)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE TRIPARTITE JURY BENCH                                 │
├──────────────────────────┬────────────────────────────┬────────────────────────────────┤
│ 1. HARDCORE ARCHITECT    │ 2. COMMERCIAL STRATEGIST   │ 3. KEMPOWER CHALLENGE CUSTODIAN│
│    "The Physics & Code"  │    "The Money & Liability" │    "The Rules & 2029 Story"    │
├──────────────────────────┼────────────────────────────┼────────────────────────────────┤
│ • Archetype: Mats & Panu │ • Archetype: VC / CFO      │ • Archetype: Challenge Host    │
│ • Focus: L1-L3, DPR, BBM │ • Focus: AEaaS, 2-mo ROI,  │ • Focus: 3 Ground Rules,       │
│   inverter loss, offline │   SLA risk, 21 FTE ledger  │   5.09 FTE truck, 2029 story   │
│ • Red Flag: Hand-waving, │ • Red Flag: Conflating S1  │ • Red Flag: Altered CSVs,      │
│   1,500kW DC=AC, mocks   │   with 100-site economics │   unpriced assets, 100% no-man │
└──────────────────────────┴────────────────────────────┴────────────────────────────────┘
```

---

## 1.1 Persona 1: The Hardcore Technical & Systems Architect

### Archetype Profile
- **Representative Jurors**: **Mats Mattsson** (Head of Cloud Software, Kempower; Kickoff Keynote Speaker) and **Panu Vartiainen** (Kempower Lead Technical Mentor; Power Electronics & Hardware Systems).
- **Professional Background**: Senior Principal Cloud Architects, Industrial Power Electronics Designers, and LUT University Energy Systems Faculty. They have spent decades designing high-power DC rectifiers, real-time CAN/Modbus bus masters, and high-concurrency cloud charging platforms.
- **Psychological Mindset**: Deeply skeptical of AI buzzwords, slide animations, and magic "zero-touch" claims. They view charging stations as harsh electrical systems operating under sub-zero temperatures, high inductive loads, and transformer thermal limits. They respect strict boundary definitions, deterministic algorithms, physical invariants, and clean separation of concerns.

### Technical Lens & Evaluation Priorities (Technical Credibility 20%, Energy & Grid Impact 20%)
1. **Dynamic Power Routing (DPR) & Contactor Physics**: Does the team understand Kempower's patented modular 25 kW routing topology? Do they enforce Break-Before-Make (BBM) contactor sequencing to prevent DC arcing ($< 500\text{ ms}$ envelope), or do they assume instantaneous continuous multiplexing?
2. **Layered Separation (L1 Physical vs L2 Edge vs L3 Cloud)**: Is the safety loop independent of cloud connectivity? What happens if the WAN connection drops for 72 hours? Does the edge maintain local dynamic load management (Local DLM) without violating transformer ratings?
3. **Electrical Conversion Invariants**: Do they acknowledge inverter rectification losses ($\eta = 0.955$), or do they commit the rookie fallacy of equating $1,500\text{ kW DC}$ with $1,500\text{ kW AC}$ draw?
4. **Mathematical Formulation**: Is the rolling 15-minute MILP solvable in real-time? How are extreme tariff spikes (e.g. 799.30 €/MWh) handled without creating infeasibilities or dropping fleet vehicles?
5. **Protocol Fidelity**: Are smart charging profiles formatted per OCPP 2.0.1 (`SetChargingProfileRequest` with `TxProfile`), and are digital signatures verified via ISO 15118-20 Plug & Charge ECDSA cryptography?

### Red-Flag Triggers & Pet Peeves
- **Buzzword Hiding**: Using phrases like "AI agent autonomously optimizes power" without specifying solver type (e.g. HiGHS MILP), state variables, objective function, and constraints.
- **Electrical Hallucination**: Assuming power can flow freely between power cabinets without copper busbars (`cross_tie = False` in `chargers.csv`).
- **Ignoring Inductive Arcing**: Switching contactors under full DC current without ramping down to 0A first.
- **Mocked Test Suites**: Presenting test results that do not load raw CSV files or bypass hardware constraints.

### Signature Cross-Examination Style
> *"You claim 260 ms contactor switching. Walk me through the six discrete physical steps from current ramp-down to relay verification. If the zero-current sensor fails to confirm 0A at step 2, what hardware safety interlock engages?"*

---

## 1.2 Persona 2: The Commercial Strategist & Venture Capitalist

### Archetype Profile
- **Representative Jurors**: Early-Stage Climate Tech VC General Partner, Energy Transition Fund Principal, Corporate CFO, and LahtiES Commercial Mentor.
- **Professional Background**: Ex-investment bankers, enterprise SaaS founders, and energy infrastructure asset managers who finance 10-year municipal concession contracts and commercial fleet electrifications.
- **Psychological Mindset**: Laser-focused on unit economics, gross margins, customer willingness to pay, risk allocation, and downside protection. They don't care how elegant the code is if the business model goes bankrupt after one bad month or if the ROI calculations rely on fraudulent accounting tricks.

### Commercial Lens & Evaluation Priorities (Commercial Viability 20%, Clarity 15%)
1. **AEaaS Revenue Model**: How does Autonomous Energy Certainty as a Service (AEaaS) monetize? Who pays the bill, what is the unit of transaction (guaranteed MWh delivered at departure vs hardware markup), and how does the operator capture value?
2. **FTE Cost Attribution & Economic Honesty**: Does the team understand who actually incurs the 20.76 FTE (€1.82M/yr) labor cost? Are they claiming to save money for the manufacturer when the cost is actually borne by the fleet customer's night jockeys?
3. **Payback Integrity (2-Month Network vs 13.31-Year Standalone)**: Did the team fall into the classic hackathon trap of dividing a single site's hardware upgrade cost by the entire 100-site network's labor pool (claiming a fake "6-week payback")? Can they cleanly defend the 13.31-year S1 standalone payback while proving a 2-month network transformation?
4. **Contractual Risk & Liquidated Damages**: What happens when things go wrong? Under the One-Page SLA, do penalties (€250 base + €5/min + €1.50/kWh) create unbounded liability that could wipe out annual revenue during a transformer failure?
5. **Anti-Fraud & Moral Hazard Controls**: What prevents a fleet customer from gaming the SLA—such as plugging in an empty 400 kWh battery 10 minutes before departure and demanding €500 in delay penalties?

### Red-Flag Triggers & Pet Peeves
- **Market Size Hand-Waving**: Quoting "$100 Billion TAM by 2030" without explaining the customer acquisition cost (CAC) or lifetime value (LTV) of a single bus depot contract.
- **Uncapped Liabilities**: Proposing SLA guarantees without a hard monthly liability cap or moral hazard gate.
- **Double Counting Savings**: Claiming electricity arbitrage savings, demand charge savings, and labor elimination without modeling the capital costs required to achieve them.
- **Confusing CAPEX with OPEX**: Treating software development as zero-cost while failing to price civil works and conduit installation.

### Signature Cross-Examination Style
> *"On Scenario Day, your SLA incurred €1,350 in penalties at Site S1 against a daily base fee of €263. If a 3-day blizzard knocks out grid power across five depots, does your operating company face insolvency? Where is the liability circuit breaker in your contract?"*

---

## 1.3 Persona 3: The Kempower Challenge & Host Custodian

### Archetype Profile
- **Representative Jurors**: **Mats Mattsson**, **Panu Vartiainen**, Kempower Product Managers, and LahtiES Organizing Committee Directors.
- **Professional Background**: Custodians of the Kempower brand, guardians of the competition rules, and ambassadors for the City of Lahti (European Green Capital) and LUT University.
- **Psychological Mindset**: Deeply committed to the competition's core mission: *"If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"* They are vigilant about rules compliance, data integrity, intellectual honesty, and compelling human-centric storytelling that non-technical city councilors and fleet directors can grasp.

### Challenge Lens & Evaluation Priorities (Degree of Autonomy 25%, Clarity 15%, Rubric Adherence)
1. **Adherence to the 3 Ground Rules**:
   - **Rule 1 (Data Immutability)**: Did the team touch, alter, filter, or fabricate even a single row of the 45 official CSV files (240,635 rows)?
   - **Rule 2 (Hardware Costing Rigor)**: Are all added assets (dispensers, rectifiers, batteries, civil foundations) priced strictly from `equipment_costs.csv`? Did they invent "free" hardware or price unlisted equipment?
   - **Rule 3 (Disclosure of Assumptions)**: Did they provide a complete, transparent register of all engineering assumptions (`docs/assumptions_and_additions.md`)?
2. **Honesty on the Limits of Autonomy**: Did the team heed the brief's explicit instruction: *"Where humans still stay in the loop, and why"*? Teams claiming 100% elimination of all humans will be penalized because blown fans (`F016`) and severed cables (`F017`) physically require a human technician with a wrench and multimeter.
3. **Declared Perspective**: Did the team explicitly declare their operating perspective (Equipment Manufacturer / Service Provider from `contracts.csv`) as mandated by Kickoff Slide 15?
4. **The 2029 Customer Story**: Is the presentation anchored in a clear, compelling 2029 customer narrative (Pekka Virtanen at Lahti City Transit or CEO Milla)? Does it clearly articulate what changed in their daily life between 2026 and 2029?
5. **Stage Discipline & Team Cohesion**: Did the team respect the strict 10:00 stage limit? Did all four members demonstrate clear division of labor without tripping over each other?

### Red-Flag Triggers & Pet Peeves
- **Modifying the Raw CSVs**: Disqualification offense.
- **Utopian "No Humans Ever" Claims**: Claiming that software can replace a technician replacing a blown semiconductor or physically repairing a vandalized charging coupler.
- **Going Over Time**: Running past the 10:00 stage cutoff into the jury's Q&A time.
- **One-Page SLA Overflow**: Producing an agreement that spans multiple pages instead of fitting onto a single, printable A4 page.

### Signature Cross-Examination Style
> *"Your pitch opened with a promise of zero human intervention. But when Cabinet C1-3 suffers an F016 fan seizure at 02:25, who physically replaces the fan motor? If you sent an autonomous drone, where is it priced in equipment_costs.csv? Be completely honest: where do humans remain in your network?"*

---

# Section 2: 14 Core Hardcore Questions Bank (Feature F7)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        14 CORE HARDCORE QUESTIONS INVENTORY                            │
├─────┬──────────────────────────────────────────┬────────────────────────┬──────────────┤
│ #   │ Question Title & Theme                   │ Target Domain          │ Primary Juror│
├─────┼──────────────────────────────────────────┼────────────────────────┼──────────────┤
│ Q01 │ 13 → 3 vs 13 → 0 Missed Departures & Bus │ Autonomy / Electrical  │ Architect    │
│ Q02 │ 24 Plugs Dual-Gun & 2:1 Depot Ratio      │ Hardware Topology      │ Host         │
│ Q03 │ 25 kW DPR Arcing & BBM Contactor Timing  │ Power Electronics      │ Architect    │
│ Q04 │ 21 FTE (€1.365M vs €1.82M) & Truck Rolls │ Labor Economics        │ VC / Host    │
│ Q05 │ 2-Month Network ROI vs 13.31-Year S1 ROI │ Financial Modeling     │ Commercial/VC│
│ Q06 │ SLA Liability & MRDT Anti-Fraud Gate     │ Contractual Risk       │ Commercial/VC│
│ Q07 │ 799.30 €/MWh Spot Spike & Continuous SoC │ Mathematical Solvers   │ Architect    │
│ Q08 │ S1 C1-3 Thermal Recovery & 199-min PdM   │ Predictive Maintenance │ Architect    │
│ Q09 │ S3 Cellular Outage & 72h Edge Islanding  │ Edge Distributed FSM   │ Architect    │
│ Q10 │ Offline Demo Proof & 539 Test Suite Pass │ Software Credibility   │ Architect    │
│ Q11 │ Sub-Zero (-18°C) Battery Wear & Dynamic  │ Chemical / Thermal     │ Host         │
│ Q12 │ Inverter Invariant (95.5%) & Transformer │ Grid Physics           │ Architect    │
│ Q13 │ S5 Three-Way Commissioning Reconciliation│ Operational Self-Heal  │ Host         │
│ Q14 │ S2 DSO 400 kW Grid Cut & Flexibility Pool│ Fleet Energy Balance   │ Commercial/VC│
└─────┴──────────────────────────────────────────┴────────────────────────┴──────────────┘
```

---

### Q01: 13 → 3 vs 13 → 0 Missed Departures & The Busbar Truth
**Juror Category**: Hardcore Technical Architect (Mats Mattsson / Panu Vartiainen)  
**Question Statement**:
> *"On your summary slides, you highlight '13 → 0 missed departures', but your deterministic verifier and engineering ledger explicitly print '13 → 3' for zero-CAPEX software. Furthermore, in your simulation code, installing 12 additional dual dispensers (€324,000) without a busbar actually causes 8 missed departures—worse than the baseline of 4! Why does your software leave 3 buses stranded, why does adding €324k of hardware make things worse, and which number is the real truth?"*

**Core Evaluation Dimensions**:
- Autonomy (25%), Technical Credibility (20%).
- Testing whether the team understands intra-cabinet vs inter-cabinet electrical routing (`cross_tie = False` in `chargers.csv`), the physical limitations of software-only scheduling, and the discipline of not promising unpriced hardware assets.

---

### Q02: 24 Plugs Dual-Gun Topology & The 2:1 Depot Ratio
**Juror Category**: Kempower Challenge Custodian & Host (Panu Vartiainen / Challenge PM)  
**Question Statement**:
> *"At Depot S1, 24 buses share 12 dispensers—a 2:1 ratio. You propose replacing 12 single-gun dispensers with 12 dual-gun satellites to create 24 connection points, claiming this eliminates midnight cable replugging entirely. But if all 24 buses plug in at 22:00, why doesn't the station immediately breach its 1,200 kW grid connection? And how does your dispenser topology physically route power between the two plugs on a single satellite?"*

**Core Evaluation Dimensions**:
- Degree of Autonomy (25%), Energy and Grid Impact (20%).
- Probing whether the team understands Kempower's satellite dispenser switching (alternating or shared 25 kW granular blocks), Earliest Deadline First (EDF) urgency allocation, and why adding plugs does not increase peak grid demand.

---

### Q03: 25 kW DPR Modular Arcing Prevention & Break-Before-Make (BBM) Timing
**Juror Category**: Hardcore Technical Architect (Panu Vartiainen)  
**Question Statement**:
> *"DC contactors will undergo catastrophic plasma arcing and weld shut if switched under high inductive load. You claim a 260 ms Break-Before-Make (BBM) sequence for dynamic power routing, yet in another place you cite 2,630 ms for N-1 macro isolation. Walk me through the exact sub-millisecond physical timing of your 6-step BBM sequence. What standard governs it, what happens if zero-current cannot be confirmed, and why is there a 10x difference between your two timing numbers?"*

**Core Evaluation Dimensions**:
- Technical Credibility (20%), Electrical Safety & Physics.
- Verifying the mathematical implementation in `src/core/dpr_matrix.py`, IEC 61851 zero-arc compliance, current ramp-down ramps, and the physical distinction between solid-state/module contactor relays vs motorized macro circuit breakers.

---

### Q04: 21 FTE (€1.365M vs €1.82M) & Honest Truck Rolls Attribution
**Juror Category**: Commercial / Venture Capitalist & Kempower Custodian (VC Partner / Mats Mattsson)  
**Question Statement**:
> *"Mats Mattsson's kickoff keynote cited 21 FTE (€1.365M/yr) of manual operations, while your empirical analysis claims 20.76 FTE (€1.82M/yr) across the 45 CSVs. Where does this discrepancy come from? More importantly, Kempower's brief explicitly ordered: 'Where humans still stay in the loop, and why.' If a charging cabinet fan seizes up at 2 AM, does your software magically replace the fan? Exactly which human hours did you eliminate, and which did you retain?"*

**Core Evaluation Dimensions**:
- Degree of Autonomy (25%), Commercial Viability (20%), Rule 3 Adherence.
- Reconciling Finnish statutory labor law (37.5 h/wk) and `equipment_costs.csv` labor rates (€45/h base vs €65k salary), while proving that 5.09 FTE of physical technician truck rolls (`cleared_by = technician`) are honestly retained for hardware repairs like `F016`.

---

### Q05: 2-Month Network ROI vs 13.31-Year S1 Standalone Payback
**Juror Category**: Commercial Strategist & Venture Capitalist (VC Partner / Investment Mentor)  
**Question Statement**:
> *"In your commercial pitch, you boast a rapid 2-month payback for dual-gun upgrades. But when we audit Depot S1 individually, installing 12 dual-gun dispensers costs €324,000 (or €216,000 net of civil foundations), while S1's own manual replug labor is only €24,336 per year. That yields a standalone payback of 13.31 years! Did you deliberately use network-wide labor savings from 100 sites to mask the terrible economics of upgrading a single depot?"*

**Core Evaluation Dimensions**:
- Commercial Viability (20%), Financial Modeling Rigor.
- Testing the team's integrity in distinguishing between network-wide portfolio transformation (reusing conduit and civil works across 100 sites against an €873k–€1.365M labor pool = ~2 months) versus depot-specific standalone unit economics (13.31 years for S1), completely dismantling fraudulent "6-week depot payback" claims.

---

### Q06: One-Page SLA Liability, Penalties & The MRDT Anti-Fraud Gate
**Juror Category**: Commercial / VC & Challenge Custodian (Corporate Attorney / CFO)  
**Question Statement**:
> *"Your One-Page Service Agreement establishes aggressive liquidated damages: €250 base penalty, €5 per minute of delay past 15 minutes, and €1.50 per kWh of deficit energy. What stops a bus operator from intentionally plugging in 10 minutes before a 5:30 AM departure requiring 200 kWh, and then claiming a €500 cash payout when the laws of physics prevent full charging? And what protects the charging operator from bankruptcy during a major multi-day grid outage?"*

**Core Evaluation Dimensions**:
- Commercial Viability (20%), Legal & Contractual Defensibility.
- Evaluating the mathematical formulation of the Minimum Required Dwell Time (MRDT) gate in `src/commercial/sla_calculator.py`, the 150% monthly liability cap, and the non-negative net invoice invariant.

---

### Q07: S4 799.30 €/MWh Spot Price Spike & Continuous SoC Deficit Slack
**Juror Category**: Hardcore Technical Architect (LUT University Academic / Optimization Expert)  
**Question Statement**:
> *"On Friday 13.11 at 18:00, electricity spot prices spike to 799.30 €/MWh at Site S4. If your MILP optimizer strictly minimizes energy costs, it would immediately shed load and refuse to charge vehicles, leaving buses and logistics trucks stranded. Conversely, if you enforce a rigid binary delivery constraint, the problem becomes computationally intractable or incurs ruinous cost. How does your solver mathematically guarantee vehicle departure without blowing the operator's budget?"*

**Core Evaluation Dimensions**:
- Technical Credibility (20%), Energy and Grid Impact (20%).
- Evaluating the rolling HiGHS MILP formulation in `src/core/mpc_optimizer.py`, continuous SoC deficit slack variables ($z_v \in [0, 1]$), priority penalty weighting (€10,000/MWh), and dimensional scaling from €/MWh to €/kWh.

---

### Q08: S1 C1-3 Thermal Recovery & 199-Minute Predictive Fan Maintenance
**Juror Category**: Hardcore Technical Architect (Panu Vartiainen / Hardware Specialist)  
**Question Statement**:
> *"At Site S1, Cabinet C1-3 experiences a catastrophic fan seizure (fault F016) at 02:25, knocking out 360 kW for 246 minutes. You claim your predictive engine gave an early warning 199 minutes in advance. Where in the raw telemetry is this evidence, what exact threshold did you trigger on, and why didn't you model the 35-minute F015 de-rating fault that preceded it?"*

**Core Evaluation Dimensions**:
- Technical Credibility (20%), Data Integrity, Predictive Maintenance (PdM).
- Verifying exact telemetry values from `telemetry_cabinets.csv` at 22:31 (59.3°C, 702 RPM), fan speed degradation criteria ($< 480\text{ RPM}$ or $\ge 20\%$ drop), 5-minute linear lookahead to 75°C trip, and transparently explaining the F015 assumption documented in `docs/assumptions_and_additions.md`.

---

### Q09: S3 2-Hour Cellular Blackout & 72-Hour Autonomous Edge Islanding
**Juror Category**: Hardcore Technical Architect (Mats Mattsson / Cloud Software Head)  
**Question Statement**:
> *"At Highway Hub S3, a cellular WAN blackout strikes from 11:00 to 13:00 on Scenario Day. In the baseline dataset, the station drops into a naive 50 kW per charger safe-mode, collapsing total station power to 500 kW and causing 29 drivers to abandon charging. You claim Sentinel maintains 1,425 kW DC locally. How does your station make dynamic load decisions with zero cloud connectivity, and how do you ensure the 1,500 kW transformer limit is never breached?"*

**Core Evaluation Dimensions**:
- Degree of Autonomy (25%), Technical Credibility (20%).
- Explaining the L2 Station Edge Controller's autonomous Micro-FSM, offline SQLite WAL telemetry persistence, Local Dynamic Load Management (Local DLM), and why local edge control is inherently superior to cloud-dependent microservices.

---

### Q10: Offline Demonstration Proof & 539 Test Suite Integrity
**Juror Category**: Hardcore Technical Architect & Host (Quality Assurance / Systems Mentor)  
**Question Statement**:
> *"Hackathon live demos are notorious for connecting to live cloud APIs that fail when the venue Wi-Fi drops, or worse, replaying fake mock assertions that pass trivially. Can you prove right now that your system runs 100% offline? How do we know your 539 passing tests aren't simply validating hardcoded mock responses?"*

**Core Evaluation Dimensions**:
- Technical Credibility (20%), Stage Readiness & Reproducibility.
- Demonstrating the Stage Failsafe Triad: `localhost:8501` Streamlit cockpit, zero network socket calls, raw CSV SHA-256 hash validation via `data_loader.py`, and running `verify_all.py` live in 0.34s timed work.

---

### Q11: Sub-Zero (-18°C) Battery Wear, Thermal Conditioning & Winter Degradation
**Juror Category**: Kempower Challenge Custodian & Host (Nordic Operations Expert)  
**Question Statement**:
> *"In a Finnish winter at -18°C, charging cold lithium iron phosphate (LFP) or NMC batteries at high C-rates causes irreversible lithium plating, dendrite growth, and fire hazards. Does your autonomous scheduler dump 150 kW into frozen bus batteries at 2 AM, or does it account for battery pre-conditioning and constant-voltage taper curves? How is this reflected in your charging models?"*

**Core Evaluation Dimensions**:
- Technical Credibility (20%), Energy and Grid Impact (20%), Nordic Domain Fidelity.
- Explaining the dynamic PTC cabin/pack pre-heating allocation (50 kW diversion for 18 minutes), constant-current constant-voltage (CC-CV) taper modeling beginning at 80% SoC with exponent 1.2 in `src/sim/discrete_sim.py`, and battery health preservation.

---

### Q12: Inverter Invariant (95.5%) & Substation Transformer Protection
**Juror Category**: Hardcore Technical Architect (Panu Vartiainen / Power Systems Lead)  
**Question Statement**:
> *"Site S3 has a 1,500 kW AC grid connection limit. You claim to allocate 1,425 kW DC across 10 charging dispensers. An uneducated engineer would say you have 75 kW of spare headroom. Why did you stop at 1,425 kW DC instead of allocating the full 1,500 kW DC, and what mathematical invariant ensures you never blow the distribution transformer fuse across all 134,400 intervals in the dataset?"*

**Core Evaluation Dimensions**:
- Energy and Grid Impact (20%), Technical Credibility (20%).
- Rigorously proving the Inverter Efficiency Invariant: $P_{\text{AC}} = P_{\text{DC}} / 0.955 = 1,425.0 / 0.955 = 1,492.15\text{ kW AC} \le 1,500\text{ kW}$, preserving an exact 7.85 kW safety buffer, and citing 0 overlimit violations across 134,400 intervals in `network_site_power.csv`.

---

### Q13: S5 Three-Way Commissioning Reconciliation & Configuration Healing
**Juror Category**: Kempower Challenge Custodian & Host (Mats Mattsson / Commissioning PM)  
**Question Statement**:
> *"At Depot S5, baseline operations suffered 5 missed departures and a 508.95 kWh deficit. You claim Sentinel solved this through 'automated three-way configuration reconciliation.' What was the actual root cause of this failure in the official dataset, is it realistic to claim software can fix a misconfigured site, and did you modify the dataset to fix it?"*

**Core Evaluation Dimensions**:
- Degree of Autonomy (25%), Technical Credibility (20%), Rule 1 Compliance.
- Detailing the three-way discrepancy between `site_config.csv` (misconfigured at 600 kW), `power_cabinets.csv` (2x 450 kW = 900 kW DC), and `chargers.csv` (D5-7 throttled to 50 kW, D5-8 dead SIM), proving automated runtime patch resolution without altering the raw CSVs.

---

### Q14: S2 DSO 400 kW Grid Curtailment & Fleet Flexibility Pooling
**Juror Category**: Commercial Strategist & Venture Capitalist (Energy Trader / Grid Architect)  
**Question Statement**:
> *"At Logistics Hub S2, the Distribution System Operator (DSO) issues a 400 kW curtailment order from 16:00 to 19:00, cutting station capacity in half right during peak operational hours. In the baseline, 4 heavy-duty freight trucks (T01–T04) missed departure with a 283.50 kWh deficit. Where did Sentinel find the energy to charge those trucks without violating the DSO limit or incurring peak demand penalties?"*

**Core Evaluation Dimensions**:
- Energy and Grid Impact (20%), Commercial Viability (20%).
- Demonstrating the 1,857 kWh overnight flexibility pool from trucks T05–T08 (which don't depart until 06:00–08:00 next morning), dynamic throttling to 1 kW trickle, shifting 283.50 kWh to priority trucks T01–T04, and achieving 100% on-time rollout.

---

# Section 3: Rubric Mapping & Question Distribution Matrix

The following matrix maps each of the 14 core questions directly to the five official judging criteria, demonstrating comprehensive coverage across all competition requirements:

| # | Question Focus | Degree of Autonomy (25%) | Energy & Grid Impact (20%) | Technical Credibility (20%) | Commercial Viability (20%) | Clarity & Story (15%) |
|---|---|:---:|:---:|:---:|:---:|:---:|
| **Q01** | 13 → 3 vs 13 → 0 Missed Departures | **Primary** | Secondary | **Primary** | Secondary | Secondary |
| **Q02** | 24 Plugs Dual-Gun & 2:1 Depot Ratio | **Primary** | **Primary** | Secondary | Secondary | — |
| **Q03** | 25 kW DPR Arcing & BBM Timing | — | Secondary | **Primary** | — | — |
| **Q04** | 21 FTE (€1.365M vs €1.82M) & Truck Rolls | **Primary** | — | Secondary | **Primary** | Secondary |
| **Q05** | 2-Mo Network ROI vs 13.31-Yr S1 ROI | — | — | Secondary | **Primary** | Secondary |
| **Q06** | SLA Liability & MRDT Anti-Fraud Gate | Secondary | — | **Primary** | **Primary** | Secondary |
| **Q07** | 799.30 €/MWh Spot Spike & Continuous Slack | — | **Primary** | **Primary** | Secondary | — |
| **Q08** | S1 C1-3 Thermal Recovery & 199-min PdM | **Primary** | — | **Primary** | — | Secondary |
| **Q09** | S3 Cellular Outage & 72h Edge Islanding | **Primary** | **Primary** | **Primary** | — | — |
| **Q10** | Offline Demo Proof & 539 Test Suite Pass | — | — | **Primary** | — | **Primary** |
| **Q11** | Sub-Zero (-18°C) Battery Wear & Dynamic PTC| — | **Primary** | **Primary** | — | Secondary |
| **Q12** | Inverter Invariant (95.5%) & Transformer | — | **Primary** | **Primary** | — | — |
| **Q13** | S5 Commissioning Mismatch & Three-Way Rec | **Primary** | Secondary | **Primary** | — | Secondary |
| **Q14** | S2 DSO 400 kW Grid Cut & Flexibility Pool | **Primary** | **Primary** | Secondary | **Primary** | — |

---

*End of Document SIM-03. Proceed to `demo_day_simulation/04_structured_defense_and_crisis_manual.md` for the corresponding 14 structured answers, team synergy protocol, and emergency crisis runbooks.*
