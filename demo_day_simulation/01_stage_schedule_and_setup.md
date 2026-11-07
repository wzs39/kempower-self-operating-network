# Project Sentinel: Demo Day Master Stage Schedule, Physical Layout & Failsafe Protocol
## 01_stage_schedule_and_setup.md — Feature Inventory F1 & F2

```
========================================================================================
PROJECT SENTINEL · THE SELF-OPERATING CHARGING NETWORK
Demo Day Master Operations Manual: 600s Pitch Timeline, Stage Setup & Failsafe Triad
Competition: LahtiES Energy Tech Hackathon 2026 · Kempower Flagship Challenge
Target Stage Time: Exactly 10:00 (600 Seconds Hard Limit) + 04:00 (240 Seconds Q&A)
Location: LUT University Lahti Campus Auditorium · Saturday 07.11.2026
Document Version: 2.4-PRODUCTION · Authoritative Master Release
========================================================================================
```

---

## 1. Executive Overview & Stage Strategy

In competitive hackathon judging—particularly under Kempower's rigorous industrial evaluation criteria (25% Autonomy, 20% Grid Impact, 20% Technical Credibility, 20% Commercial Viability, 15% Clarity)—time management, stage presence, and live demonstration reliability separate winning teams from disqualified contenders.

The stage moderator enforces a **strict 10:00 (600 seconds) hard cutoff**. If a team reaches 10:01, microphones are cut, commercial proposals are lost, and judges penalize the team on Clarity and Completeness. 

This document defines:
1. **The T-Minus Pre-Flight Operations (T-30m to T-0m)**: Complete hardware, software, display, and audio verification checklists.
2. **The 600-Second Stage Master Timeline (00:00 to 10:00)**: Second-by-second delivery pacing, slide progression, verbatim stage cues, and buffer margins.
3. **The 240-Second Jury Q&A Protocol (10:00 to 14:00)**: Defensive routing, triangular body language, and graceful stage exits.
4. **The Physical Stage Layout (ASCII Architecture)**: Equipment placement, A/V topology, team positioning, line-of-sight triangles, and movement corridors.
5. **The Offline Failsafe Triad Protocol (Level 1 $\to$ Level 2 $\to$ Level 3)**: A three-tier contingency system guaranteeing uninterrupted demonstration even in the event of complete local runtime crashes.

---

## 2. Pre-Stage Preparation & T-Minus Checklist (T-30m to T-0m)

All technology and stage assets must be verified during the preceding team's pitch and intermission.

```
T-30m               T-20m               T-10m          T-5m        T-2m     T-0m
  │                   │                   │              │           │        │
  ▼                   ▼                   ▼              ▼           ▼        ▼
[A/V & Display] ──> [OS & Software] ──> [Handout Prep] ─> [Audio] ──> [Staging] ─> [Curtain Up]
(1080p, HDMI Sw)    (Streamlit, CLI)    (SLA, Assumptions)(Mics/Click)(Standby)  (00:00 Start)
```

### 2.1 Chronological T-Minus Action Ledger

| Time | Responsibility | Operational Checklist & Verification Actions | Verification Criteria |
|---|---|---|---|
| **T-30m** | Member C & D | **A/V & Video Feed Connection**:<br>1. Connect Master Laptop (Laptop 1) to Stage HDMI Input A via hardware HDMI Switcher.<br>2. Connect Backup Laptop (Laptop 2) to Stage HDMI Input B.<br>3. Verify projector resolution locks at **1920×1080 @ 60Hz** (16:9 aspect ratio).<br>4. Verify text legibility from 15 meters back in the auditorium. | Projector displays high-contrast basalt slate background without stretching, cropping, or color distortion. |
| **T-25m** | Member C | **Host OS Environment Hardening (Laptop 1)**:<br>1. Activate OS *Focus Assist* / *Do Not Disturb* (mute all notifications, Slack, Telegram, Email).<br>2. Disable screen saver, display sleep timer, and power-saving battery throttling (set to "High Performance / Never Sleep").<br>3. Disconnect Wi-Fi and Bluetooth networking (Airplane Mode ON) to prove 100% offline autonomy.<br>4. Close all non-essential background processes (Spotify, Docker, IDEs, browser tabs). | OS taskbar auto-hides; 0 background popups; CPU idle usage $< 5\%$; memory headroom $> 8\text{ GB}$. |
| **T-20m** | Member C | **Local Software & Live Console Initialization**:<br>1. Launch local Streamlit server: `streamlit run app.py --server.headless=true --server.port=8501`.<br>2. Open Chrome in Fullscreen (`F11`), zoom locked at **100%**, window width $\ge 1400\text{ px}$.<br>3. Pre-load Tab 1 (`localhost:8501/` Executive Cockpit), Tab 2 (`localhost:8501/` Scenario Day Replay).<br>4. Verify second browser instance loaded with `demo_scenarios/app.py` for micro-fault replay.<br>5. Open Windows Terminal (PowerShell) with large font (Consolas 20pt), pre-staged with command `python verify_all.py`. | Streamlit renders instantly; terminal runs `python verify_all.py` passing 29/29 items in $< 0.5\text{ s}$. |
| **T-15m** | Member D | **Backup Laptop & Secondary Failsafe Standby (Laptop 2)**:<br>1. Boot Laptop 2 running identical software environment and mirrored screen.<br>2. Open VLC Media Player with `demo/presentation_demo.mp4` (1080p30, 75s) paused at frame 0.<br>3. Open `presentation.html` in secondary browser (zero-dependency static offline presentation deck).<br>4. Stage printed copies of `docs/assumptions_and_additions.md` and `One_Page_SLA_Specification.md`. | Laptop 2 displays identical output on HDMI Input B; HDMI hardware switch toggle tested ($< 1\text{ s}$ latency). |
| **T-10m** | Speaker A & B | **Audio & Presentation Controller Verification**:<br>1. Speaker A tests wireless hand-held microphone; verifies audio gain and absence of feedback.<br>2. Speaker B tests lavalier/headset microphone; verifies breath isolation.<br>3. Test wireless presentation remote (slide clicker) with presentation deck: Forward, Backward, Blank Screen.<br>4. Verify battery level of clicker ($> 80\%$) and pack fresh backup AAA batteries in Speaker A's pocket. | Sound is crisp and intelligible at auditorium back row; clicker advances slides with zero lag. |
| **T-5m** | Speaker A | **Judge Handout Inspection**:<br>1. Inspect physical presentation folder containing 4 sets of double-sided, laminated printouts:<br>   - Document 1: `docs/assumptions_and_additions.md` (Mandatory Rule 3 Assumption Register).<br>   - Document 2: `One_Page_SLA_Specification.md` (Signed 1-page outcome-based contract).<br>2. Place folder in Speaker A's left hand, ready for ceremonial delivery at 00:30. | 4 pristine handout packets prepared for Lead Juror Mats Mattsson, Panu Vartiainen, and 2 VIP judges. |
| **T-2m** | Entire Team | **Stage Alignment & Standby in Wing**:<br>1. Team assembles at Stage Right wing.<br>2. Speaker A stands first in line; Speaker B second; Member C moves to console desk; Member D stands adjacent to Member C.<br>3. Synchronize stage wristwatches to 00:00; confirm visual contact with downstage timer monitor. | Team in position; heart rates settled; game faces on; ready for immediate walk-on. |
| **T-0m** | Moderator | **Stage Call**:<br>Moderator announces: *"Next up, Project Sentinel addressing the Kempower Flagship Challenge."*<br>Team steps onto stage. Timer starts immediately upon Speaker A's first word. | Clock running: 00:00. |

---

## 3. Master 600-Second Stage Schedule (00:00 to 10:00)

```
00:00 ── 00:30 ───────────── 03:45 ──────── 05:00 ──────────── 07:00 ── 07:30 ──────────── 09:30 ── 10:00 ──── 14:00
┌────────┬────────────────────┬──────────────┬──────────────────┬───────┬────────────────────┬───────┬──────────────┐
│ Cold   │ Business Pain &    │ Tech Arch &  │ Live Demonstration│ Outcome│ Customer Story &   │ Close │ Jury Rapid-  │
│ Open   │ 20.76 FTE Audit    │ DPR Matrix   │ 5 Crises Resolved│ CaaS  │ Honest Economics   │ & CTA │ Fire Defense │
│ (30s)  │ (195s)             │ (75s)        │ (120s max)       │ SLA   │ & S1 Busbar Truth  │ (30s) │ (240s)       │
│ Spk A  │ Speaker A          │ Speaker B    │ Spk B + Member C │ Spk A │ Spk A              │ Spk A │ All 4 On Stage│
└────────┴────────────────────┴──────────────┴──────────────────┴───────┴────────────────────┴───────┴──────────────┘
Slide P1   Slides P1 -> P2      Slides P3 -> P6 Slide P7 (Console)Slide P9 Slides P8 -> P10   Slide P12 Q&A Stance
```

### 3.1 Detailed Second-by-Second Segment Ledger

#### Segment 1: Cold Open & The Hook [00:00 – 00:30] · 30 Seconds
- **Slide**: Slide P1 (`Cover: 02:15 AM, January 2029: The Night Begins`)
- **Primary Presenter**: **Speaker A** (Business & Commercial Lead)
- **Secondary Role**: Speaker B (Center stage standby), Member C & D (Hands poised on console).
- **Core Narrative**: Set a gripping, cinematic scene in sub-zero Finland. Present the existential challenge: uncrewed fleet depot under a critical equipment trip.
- **Verbatim Opening Line**:
  > *"Good morning, Mats, Panu, and members of the jury. It is 2:15 AM on a January night in 2029, in Lahti, Finland. Minus eighteen degrees. A depot of 24 electric buses is silent and dark—because no human is there. And at that exact moment, a 360 kW power cabinet overheats and trips. At 5:30 AM, twenty-four routes must launch. Who fixes it, when no one is on site?"*
- **Stage Action & Choreography**:
  - Speaker A steps to Downstage Right, holds eye contact directly with Lead Juror Mats Mattsson.
  - At **00:25**, Speaker A walks three paces to the jury table, lays the laminated *Assumption Register* (`docs/assumptions_and_additions.md`) and *One-Page SLA* on the desk in front of Mats Mattsson:
    > *"Per Rule 3, here is our audited assumption register and signed one-page SLA."*
- **Hard Pacing Checkpoint**: At **00:30**, Slide P1 transitions to Slide P2. Speaker A is back at Downstage Center.

---

#### Segment 2: Problem, Business Pain & Baseline Audit [00:30 – 03:45] · 195 Seconds
- **Slides**: Slide P1 stats $\to$ Slide P2 (`The Baseline: 20.76 Full-Time Employees Running in Place`)
- **Primary Presenter**: **Speaker A**
- **Core Narrative**: Grounded empirical analysis of the official dataset. Dismantling the status quo: 20.76 FTEs of manual labor across 100 sites, dominated by night cable replugging, resulting in Scenario Day collapse.
- **Detailed Step-by-Step Breakdown**:
  - **[00:30 – 01:15] (45s) The Empirical Data Audit**:
    - Focus on slide visual: Giant typography **20.76 FTE** and **45 CSVs / 240,635 rows**.
    - Speaker A: *"We did not speculate. We audited every single row of the 45 official CSV files. In two weeks, 100 sites generated 8,852 manual interventions consuming 93,412 minutes. Under Finnish statutory working hours (37.5 hours per week), that represents exactly 20.76 Full-Time Employees. At the official base labor rate of 45 euros per hour, operators burn 1.82 million euros every year just to keep chargers alive."*
  - **[01:15 – 02:00] (45s) The Midnight Replug Bottleneck**:
    - Highlight horizontal red bar: `move_and_replug_vehicle` accounts for **47.93% of all labor time** (44,768 minutes, 5,596 events).
    - Speaker A: *"Look at where that human time is wasted: nearly half—47.93%—is spent on a single task: move_and_replug_vehicle. That is 9.95 full-time workers walking through freezing depots at 2:00 AM playing musical chairs with charging cables because the hardware lacks dynamic intelligence. Operators are paying people to do what software and contactors should do automatically."*
  - **[02:00 – 02:45] (45s) The Scenario Day Collapse (Baseline Failure)**:
    - Speaker A highlights Friday 13.11 baseline outcomes: **13 missed departures, 1,804.45 kWh stranded, 29.69% driver abandonment at Hub S3**.
    - Speaker A: *"And when crisis hit on Friday the 13th, the human system broke down. Across five sites, 13 commercial fleet vehicles were stranded below target SoC, 1,804 kilowatt-hours were left undelivered, and at highway hub S3, nearly 30% of public drivers abandoned the station in frustration. The manual model cannot scale to 2029 fleet expansion."*
  - **[02:45 – 03:45] (60s) Introducing Sentinel & The AEaaS Paradigm**:
    - Transition to Slide P3 (`Meet Sentinel: An Autonomous Operating Core`).
    - Speaker A introduces **Autonomous Energy Certainty as a Service (AEaaS)**:
      - Pillar 1: Energy Certainty (guaranteed departure kWh).
      - Pillar 2: Grid Safety (zero transformer overloads).
      - Pillar 3: Hands-Free Operations (72-hour edge autonomy).
    - **Handoff Cue (03:40)**: Speaker A turns toward Speaker B at Center Stage:
      > *"To eliminate continuous human operations, you don't need more monitoring dashboards or more night shift jockeys. You need an autonomous operating core grounded in electrical physics. I hand over to our Chief Systems Architect, [Speaker B], to show how Sentinel actually thinks and executes."*
- **Hard Pacing Checkpoint**: At **03:45**, Speaker B has the floor; Slide P4 appears.

---

#### Segment 3: Technology Architecture & Electrical Physics [03:45 – 05:00] · 75 Seconds
- **Slides**: Slide P4 (`Layered Architecture`) $\to$ Slide P5 (`Scenario Day Matrix`) $\to$ Slide P6 (`The Physics That Holds`)
- **Primary Presenter**: **Speaker B** (Chief Systems Architect)
- **Core Narrative**: Demonstrate industrial engineering rigor. Clean separation of Cloud L3, Edge L2, and Hardware L1/L0. Rigorous contactor timing and mathematical grid invariants.
- **Detailed Step-by-Step Breakdown**:
  - **[03:45 – 04:15] (30s) Three-Tier Layered Architecture (L3 / L2 / L1)**:
    - Slide P4 schematic displayed.
    - Speaker B: *"Thank you, [Speaker A]. Our engineering philosophy is strict: Never rely on the cloud for physical safety, but never rely on local heuristics for global economic optimality. At Layer 3, our cloud orchestrator runs a rolling 15-minute MILP via the HiGHS solver, arbitrating Nord Pool spot prices and demand peaks into OCPP 2.0.1 TxProfiles. At Layer 2, our station edge controller runs an autonomous Finite State Machine. If the cellular fiber is cut, it islands locally for 72 hours without cloud connection. At Layer 1, we control Kempower's patented Dynamic Power Routing: 25 kW modular rectifiers, strict 1:N wiring, and a 6-step Break-Before-Make contactor sequence completing in 260 milliseconds—well below the 500 millisecond zero-arc safety threshold."*
  - **[04:15 – 04:40] (25s) The Five Compounding Crises (Scenario Day Resolution)**:
    - Slide P5 Matrix displayed.
    - Speaker B: *"On Scenario Day, Sentinel faced five compounding crises: at S1, a fan failure on Cabinet C1-3; at S2, a 400 kW DSO curtailment; at S3, a 2-hour cellular blackout; at S4, a 799.30 euro spot price spike; and at S5, a commissioning parameter mismatch. In baseline, humans caused 13 missed departures. Sentinel cuts missed departures from 13 down to 3 with zero euros of CAPEX and zero human cable replugs, and unlocks the monotone path to 0."*
  - **[04:40 – 05:00] (20s) Electrical Invariants & Inverter Guard**:
    - Slide P6 displayed: **0 overlimits out of 134,400 intervals**.
    - Speaker B: *"Rule number one in power engineering: never blow up the substation. Across 134,400 telemetry intervals across 100 sites, Sentinel maintains a strict 100% zero-overlimit invariant. Furthermore, many assume 1,500 kW DC equals 1,500 kW AC. That is an electrical fallacy. At 95.5% inverter efficiency, 1,425 kW DC pulls exactly 1,492.15 kW AC from the grid. Our local DLM enforces this loss guard, keeping AC intake strictly below the 1,500 kW grid cap with a 7.85 kW safety buffer."*
- **Handoff Cue to Live Demo (04:55)**: Speaker B signals Member C at the console desk:
  > *"You have seen the equations on paper. Now watch the autonomous core run in real time. Member C, take us to the live console."*
- **Hard Pacing Checkpoint**: At **05:00**, Slide P7 is live; screen switches to console feed.

---

#### Segment 4: Live Demonstration & Scenario Replay [05:00 – 07:00] · 120 Seconds Max
- **Slide / Screen**: Slide P7 (`Watch the Solution Work — Scenario Day Live`) $\to$ Live Streamlit UI (`localhost:8501`) / MP4 Failsafe
- **Primary Operators**: **Speaker B** (Verbal Guide) + **Member C** (Console Pilot)
- **Support**: Member D (Verifying verifier terminal output).
- **Core Narrative**: Dynamic, high-cadence walkthrough of the 5 crises being programmatically resolved on Scenario Day.
- **Detailed Step-by-Step Console Walkthrough**:
  - **[05:00 – 05:25] (25s) Scene 0 & Scene 1: Depot S1 Night Replay & Fan Failure**:
    - Member C action: Clicks `Jump to → Precursor (22:31)` on `1_Night_Replay`.
    - Screen visual: Telemetry graph shows Cabinet C1-3 temperature rising to **59.3°C** while fan RPM drops to **702 RPM**.
    - Speaker B: *"At 22:31, three hours before the physical trip, our edge predictive maintenance flags fan bearing degradation—giving operators a 199-minute early warning. At 02:25, Cabinet C1-3 trips. Look at the split screen: in baseline on the left, 4 buses are stranded and an employee walks 9 trips in the snow. On the right, Sentinel isolates the dead cabinet in 85 milliseconds, reconfigures healthy cabinets C1-1 and C1-2 via 25 kW DPR routing, and delivers power to all 24 connected buses without a single human move."*
  - **[05:25 – 05:50] (25s) Scene 2: Logistics S2 — DSO 400 kW Grid Curtailment**:
    - Member C action: Switches to `4_Curtailment_Replay`, clicks `Jump to → 16:00`.
    - Screen visual: Grid intake clamped at 400 kW. Trucks T05–T08 throttled to 1 kW; T01–T04 boosted to 150 kW.
    - Speaker B: *"At 16:00, the DSO issues an emergency 400 kW grid curtailment at freight terminal S2. Baseline charged arriving trucks indiscriminately, causing trucks T01 through T04 to miss afternoon departures. Sentinel detects the 1,857 kWh overnight flexibility pool of long-stay trucks T05 through T08, throttling them back to 1 kW, and shifting 283.5 kWh to urgent trucks. Result: 4 to 0 missed departures, zero grid violations."*
  - **[05:50 – 06:15] (25s) Scene 3: Highway Hub S3 — 2-Hour Cellular Blackout**:
    - Member C action: Switches to `2_Outage_Replay`, clicks `Jump to → Outage 11:00`.
    - Screen visual: WAN indicator goes RED. Power output holds steady at **1,425 kW DC / 1,492.15 kW AC**.
    - Speaker B: *"At 11:00, public highway station S3 loses all cellular WAN connectivity for two solid hours. In baseline, chargers dropped to a naive 50 kW limp mode, causing 29 drivers to abandon the station. Sentinel's edge controller instantly islands, takes local control of the DPR matrix, and maintains full 1,425 kW DC throughput while respecting the 1,500 kW grid limit. Driver abandonment during the outage drops by half, and local SQLite WAL transactions sync back to cloud within 15 minutes of recovery."*
  - **[06:15 – 06:40] (25s) Scene 4 & Scene 5: Urban S4 Price Spike & Depot S5 Config Mismatch**:
    - Member C action: Switches to `3_Price_Spike_Replay`, highlights 18:00 spot spike (**799.30 €/MWh**); then triggers `python verify_all.py` in terminal.
    - Screen visual: Terminal prints `[PASS] Station S4 & MILP Peak`, `[PASS] Station S5 (Auto-Calib)`, `VERIFICATION SUCCEEDED: 29/29 Items Verified in 0.37s`.
    - Speaker B: *"At 18:00, Nord Pool spot electricity spikes to 799.30 euros per megawatt-hour. Our MILP solver uses continuous SoC deficit slack variables to pre-charge vehicles during cheap hours, cutting energy costs by 47.5%. And at S5, our 3-way configuration reconciler corrects an onboarding error from 600 to 900 kW, unlocking 750 kWh of suppressed capacity and turning 5 missed buses into 0. Look at our terminal: 29 out of 29 verification invariants pass deterministically in 0.37 seconds."*
  - **[06:40 – 07:00] (20s) Demo Wrap-Up & Return to Commercials**:
    - Member C returns display to Slide P8 (`What It's Worth: Honest Economics`).
    - **Handoff Cue (06:55)**: Speaker B gestures to Speaker A:
      > *"The technology runs, the code passes, and the physics holds. But technology without commercial honesty is just an expensive science experiment. I hand back to [Speaker A] to reveal the honest economics and our enforceable One-Page SLA."*
- **Hard Pacing Checkpoint**: At **07:00**, Live Demo concludes; Slide P8/P9 is active.

---

#### Segment 5: Commercial Contract — Outcome CaaS & The One-Page SLA [07:00 – 07:30] · 30 Seconds
- **Slide**: Slide P9 (`Energy Certainty as a Service — with an Enforceable SLA`)
- **Primary Presenter**: **Speaker A**
- **Core Narrative**: Define the commercial breakthrough. Shift from hardware uptime vending to guaranteed energy delivery backed by a legally enforceable contract with anti-gaming gates.
- **Detailed Step-by-Step Breakdown**:
  - Focus on left card: **MRDT Anti-Gaming Gate Equation**:
    $$\text{MRDT}_j = \left( \frac{\frac{\text{SoC}_{\text{req}} - \text{SoC}_{\text{arrive}}}{100} \cdot E_{\text{batt}}}{\min(P_{\text{charger}}, P_{\text{veh}}) \cdot 0.95} \right) \cdot 60 + 15.0\text{ min}$$
  - Speaker A: *"Under traditional contracts, vendors sell hardware uptime. If a charger is electrically available but a bus cannot charge because all cables are occupied or a human forgot to plug it in, the operator is fined and the vendor gets blamed. Sentinel introduces Outcome-Based Charging-as-a-Service (AEaaS). Operators pay for guaranteed departure kWh. To prevent commercial moral hazard, our One-Page SLA features the Minimum Required Dwell Time (MRDT) gate: if a driver arrives 10 minutes before departure demanding 200 kWh, the gate classifies it as Best-Effort, protecting operators from extortion. If we fail when MRDT is met, penalties have teeth: 250 euros base, 5 euros per minute beyond 15, and 1.50 euros per deficit kWh. Backed by a hard 150% monthly liability cap and non-negative invoice guarantee, business ruin is impossible while performance is guaranteed."*
- **Hard Pacing Checkpoint**: At **07:30**, Slide P9 transitions to Slide P8 / P10.

---

#### Segment 6: Resolution — Customer Story & Honest Economics [07:30 – 09:30] · 120 Seconds
- **Slides**: Slide P8 (`Honest Economics for the Operator`) $\to$ Slide P10 (`02:15 AM: The Night, Resolved`)
- **Primary Presenter**: **Speaker A**
- **Core Narrative**: Connect high-level executive economics (CEO Milla / 2-month ROI) with unshakeable depot engineering reality (Pekka Virtanen / S1 13.31-yr payback & busbar tie truth).
- **Detailed Step-by-Step Breakdown**:
  - **[07:30 – 08:15] (45s) The Honest Labor Attribution Ledger (20.76 FTE Truth)**:
    - Slide P8 displayed.
    - Speaker A: *"Let's talk about what this is worth—honestly. Eliminating 20.76 FTEs saves 1.82 million euros across 100 sites. But we attribute that labor with complete forensic honesty: 9.95 FTE is customer depot replugging—that is the commercial value we sell to operators, not a cost we carry internally. 5.09 FTE is technician truck rolls for physical hardware failures like blown fans (F016)—we deliberately retain this because physical components require physical humans. 2.50 FTE of remote operations is automated, and 3.22 FTE of customer support is retained. We automate exactly 12.44 FTEs of continuous drudgery."*
  - **[08:15 – 08:50] (35s) The S1 Standalone Payback & The Busbar Trap**:
    - Speaker A exposes the hardware expansion fallacy:
      - S1 standalone manual replug savings: **€24,336 / year**.
      - 12 new dual dispensers list price: $12 \times \text{€}27,000 = \text{€}324,000$.
      - Standalone hardware payback: $324,000 / 24,336 = \mathbf{13.31\text{ years}}$ (refuting fraudulent 6-week claims).
      - Speaker A: *"Furthermore, look at the engineering reality of Site S1. Claiming a 6-week payback by applying all 100 sites' labor savings to a single depot is commercially fraudulent. S1's own replugging costs 24,336 euros a year; standalone hardware payback is 13.31 years. Even worse: spending 324,000 euros to add 12 dispensers without an inter-cabinet busbar tie makes S1 worse—8 missed departures instead of 4, because buses get locked to the dead cabinet! Software alone (Tier 2) cuts missed departures from 4 to 3 and energy deficit by 87.8% for zero euros. Reaching zero missed within the 1,200 kW grid cap requires an inter-cabinet busbar tie. That tie has no price in Kempower's official equipment catalog—so we hand that number back to you to price together."*
  - **[08:50 – 09:30] (40s) The 2029 Story Climax (Pekka Virtanen & CEO Milla)**:
    - Slide P10 displayed: Cinematic 3-beat resolution.
    - Speaker A: *"Now let's bring it back to the cold night we opened with. Meet Pekka Virtanen, fleet director at Lahti City Transit, and Milla, his CEO. In 2026, Pekka struggled to hire night staff willing to drag frozen 400A cables through slush at 2:00 AM, while Milla faced municipal delay fines. In 2029, under Sentinel, 24 buses pull in at 10:00 PM. Drivers plug in; ISO 15118 Plug & Charge authenticates in 1.1 seconds. Drivers go home. At 2:15 AM, the cabinet trips. But no one is woken. The edge controller re-routes 25 kW power modules across remaining healthy guns. At 5:30 AM, all 24 buses roll out 100% on time. Pekka wakes at 6:00 AM, sips his morning coffee, and sees a single green notification on his phone: '24 of 24 routes dispatched on time. Zero human interventions. Monthly SLA: 99.98%.' That is why Sentinel exists."*
- **Handoff Cue to Final Slide (09:25)**: Speaker A gestures to Speaker B for the final technical signoff:
  > *"And behind Pekka's coffee stands an unbreakable wall of industrial verification."*
- **Hard Pacing Checkpoint**: At **09:30**, Slide P11/P12 is on screen.

---

#### Segment 7: Standards, Verification & Closing Call to Action [09:30 – 10:00] · 30 Seconds
- **Slides**: Slide P11 (`Technical Credibility: Standards & 539 Tests`) $\to$ Slide P12 (`The Path to Deployment`)
- **Primary Presenters**: **Speaker B** (10s on standards) $\to$ **Speaker A** (20s on close)
- **Detailed Step-by-Step Breakdown**:
  - **[09:30 – 09:40] (10s) Standards & Test Coverage (Speaker B)**:
    - Speaker B: *"Native OCPP 2.0.1 smart charging profiles, ISO 15118-20 Plug & Charge with sub-10ms ECDSA certificate verification, and 539 automated regression tests passing at 100%. Our code is open, verified, and reproducibility takes 0.37 seconds."*
  - **[09:40 – 10:00] (20s) The Three Next Steps & Call to Action (Speaker A)**:
    - Slide P12 displayed: Three actionable cards:
      1. *01 · Pilot the 0 € Software Tier* (urgency scheduling on one depot, 13 $\to$ 3 missed).
      2. *02 · Co-Price the Inter-Cabinet Busbar Tie* (monotone zero-miss path).
      3. *03 · Adopt Outcome-Based CaaS SLA* (MRDT gate + 150% liability cap).
    - **Closing Climax Line (Speaker A)**:
      > *"At 2:15 AM in 2029, a cabinet fails—and nothing happens. No late buses, no blown transformers, no panicked phone calls. Kempower built the world's most modular DC charging hardware. Sentinel provides the autonomous brain it deserves. Thank you, and we welcome your questions."*
- **Hard Pacing Checkpoint**: **09:59**. Clicker presses blank/Q&A screen. Time elapsed: **09:59 / 10:00**.

---

## 4. The 240-Second Jury Q&A Protocol (10:00 to 14:00)

```
10:00               11:00               12:00               13:00               14:00
  │                   │                   │                   │                   │
  ▼                   ▼                   ▼                   ▼                   ▼
[Defensive Stance] ─> [Question 1: Tech] ─> [Question 2: Biz] ─> [Question 3: SLA] ─> [Formal Exit]
(Triangle Formation)  (B + C/D: Math/Code) (A: FTE/ROI/Milla)  (A/D: MRDT/Cap)     (Handshakes)
```

### 4.1 Stage Formation & Body Language Transition
Upon concluding at 10:00, the team executes an immediate, synchronized physical shift:
1. **The Triangle Formation**:
   - Speaker A stands Downstage Right (45° angle toward judges).
   - Speaker B stands Downstage Left-Center (45° angle toward judges).
   - Members C & D step forward from behind the console desk by one pace, standing upright at Upstage Left with laptop screens angled toward judges.
2. **Body Language & Non-Verbal Discipline**:
   - Never huddle or whisper during a judge's question. All four maintain upright posture and open eye contact.
   - When a judge speaks, the primary responder nods subtly to acknowledge comprehension.
   - The primary responder steps forward by **half a step** to claim the question. Other members remain still and attentive.

### 4.2 Immediate Routing Protocol Matrix

| Question Domain | Primary Responder | Supporting Responder | Console / Screen Action | Maximum Target Duration |
|---|---|---|---|---|
| **Commercial Model, AEaaS, FTE Ledger, Pekka/Milla Story** | **Speaker A** | Member D | Member C displays Slide P8 (FTE Ledger) or Slide P9 (SLA). | 60 seconds |
| **System Architecture, L1/L2/L3, DPR Matrix, Inverter Physics** | **Speaker B** | Member D | Member C switches to Architecture Diagram (Slide P4). | 60 seconds |
| **Live Demo Execution, UI Mechanics, Fault Simulation** | **Member C** | Speaker B | Member C scrubs Streamlit time slider directly to cited timestamp. | 45 seconds |
| **Hardcore Physics, 13$\to$3 vs 13$\to$0, Busbar Tie, Code Proof** | **Member D** | Speaker B | Member D executes `verify_all.py` or displays exact line in `src/sim/discrete_sim.py`. | 60 seconds |
| **SLA Terms, MRDT Equation, 150% Liability Cap, Penalties** | **Speaker A** | **Member D** | Member C displays Slide P9; Member D cites exact clause in `One_Page_SLA_Specification.md`. | 60 seconds |

### 4.3 Wrap-Up & Exit Protocol (13:45 – 14:00)
1. At the 13:45 mark (or when the moderator calls "Time!"), Speaker A raises their hand slightly and delivers the standardized closing line:
   > *"Thank you Mats, Panu, and the entire judging panel. The complete codebase, 539 tests, and documentation are public on our GitHub repository. We look forward to building the autonomous charging network together."*
2. All four members bow or nod synchronously.
3. Member C neatly closes laptop lid; Member D unplugs HDMI cable; team exits Stage Left in an orderly file.

---

## 5. Physical Stage Layout & Spatial Architecture (Feature F2)

### 5.1 High-Resolution Stage ASCII Architecture Diagram

```
========================================================================================================================
                                      LUT UNIVERSITY AUDITORIUM — STAGE TOPOLOGY
========================================================================================================================

                                          [ UPSTAGE WALL & PROJECTION SCREEN ]
                               ┌────────────────────────────────────────────────────────┐
                               │             MAIN PROJECTION SCREEN (16:9)              │
                               │               Resolution: 1920 x 1080                  │
                               │        Slide Deck / Live Streamlit / Demo Video        │
                               └────────────────────────────────────────────────────────┘
                                                         ▲
                                                         │ Primary HDMI Feed
                                                         │
               UPSTAGE LEFT                              │                              UPSTAGE RIGHT
       ┌───────────────────────────┐                     │
       │    TECHNICAL CONSOLE DESK │                     │
       │  ┌──────────────────────┐ │                     │
       │  │ LAPTOP 1: MASTER     │ │                     │
       │  │ Member C: Live Demo  │─┼─────────────────────┘
       │  │ (Streamlit / F11)    │ │
       │  └──────────────────────┘ │
       │  ┌──────────────────────┐ │
       │  │ LAPTOP 2: DEFENSE    │ │
       │  │ Member D: Code/Tests │ │
       │  │ (verify_all.py / VLC)│ │
       │  └──────────────────────┘ │
       │  ┌──────────────────────┐ │
       │  │ Hardware HDMI Switch │ │
       │  │ (3s Instant Cutover) │ │
       │  └──────────────────────┘ │
       └───────────────────────────┘
              ▲             ▲
              │             │
        [Member C]    [Member D]
       (Flight Ctrl) (Chief Sci)

               STAGE LEFT                               CENTER STAGE                            STAGE RIGHT
                                                  ┌───────────────────────┐
                                                  │       SPEAKER B       │
                                                  │  Systems Architect    │
                                                  │ (Lavalier Mic / Deck) │
                                                  └───────────────────────┘
                                                              │
                                      ◄── Handoff Corridor ───┤─── Handoff Corridor ──►
                                                              │
                                                              ▼
                                                  ┌───────────────────────┐             ┌───────────────────────┐
                                                  │  DOWNSTAGE CONFIDENCE │             │       SPEAKER A       │
                                                  │  MONITOR & STAGE CLOCK│             │  Commercial & Vision  │
                                                  │   [ 600s Countdown ]  │             │ (Handheld Mic/Clicker)│
                                                  └───────────────────────┘             └───────────────────────┘
                                                                                            │
                                                                                            │ (00:30 Handout Walk)
                                                                                            ▼
────────────────────────────────────────────────── STAGE EDGE ─────────────────────────────────────────────────────────

                                                  [ JURY SEATING ROW ]
                       ┌─────────────────────────────────────────────────────────────────────────┐
                       │  [Mats Mattsson]      [Panu Vartiainen]      [LUT Academic]   [VC Judge]│
                       │  Head of Cloud SW     Lead Tech Expert       Energy Systems   LahtiES   │
                       │  (Kempower Lead)      (Hardware/DPR)         (Grid & Math)    (ROI/SLA) │
                       └─────────────────────────────────────────────────────────────────────────┘

                                                  [ AUDIENCE SEATING ]
                                         LUT Students, Competitors & Industry Observers
========================================================================================================================
```

### 5.2 Team Member Spatial Positioning & Movement Rules

1. **Speaker A (Stage Right / Downstage Right)**:
   - **Role**: Master of Ceremonies, commercial narrative anchor, customer storyteller.
   - **Position**: Anchored at Downstage Right. Holds wireless handheld microphone in right hand and presentation clicker in left hand.
   - **Movement Vector**:
     - At **00:25**, takes 3 controlled paces forward to the edge of the stage to place the physical laminated *Assumption Register* and *One-Page SLA* on the table directly in front of Mats Mattsson.
     - At **01:30**, takes 2 paces toward Center Stage during Transition 1 to yield focus to Speaker B.
     - At **05:45**, steps forward to Downstage Center to reclaim the commercial narrative following the Live Demo.
   - **Gaze Vector**: Maintains eye contact across all four judges, prioritizing Mats Mattsson and VC judges.

2. **Speaker B (Center Stage / Downstage Center)**:
   - **Role**: Systems Architect, electrical engineering defender, live demo narrator.
   - **Position**: Anchored at Center Stage, slightly left of center to maintain an unobstructed line-of-sight to the main projection screen.
   - **Movement Vector**:
     - Uses lavalier/headset microphone, keeping hands free for open architectural gestures.
     - During Slide P4 (Architecture) and Slide P6 (Inverter Guard), turns 30° toward the screen, using hand gestures to trace the L3 $\to$ L2 $\to$ L1 flow.
     - At **04:55**, turns toward Member C at the console desk, gesturing smoothly toward the live screen.
   - **Gaze Vector**: Alternates between Panu Vartiainen (Lead Hardware Expert) and the screen.

3. **Member C (Upstage Left Console Desk — Flight Controller)**:
   - **Role**: Live demo operator, Streamlit UI driver, video failsafe trigger.
   - **Position**: Seated or high-stool posture at the Technical Console Desk. Positioned perpendicular to the audience so hands and screen actions are clearly visible.
   - **Movement Rules**:
     - **Zero Unnecessary Movement**: Hands rest on keyboard/mouse only during designated demo cues (05:00 – 07:00).
     - During Segments 1–3 and 5–7, hands remain flat on the desk or clasped. No typing, no window dragging, no mouse cursor wiggling.
     - Never obstructs the projection screen or turns back entirely to the audience.

4. **Member D (Upstage Left Technical Pod — Chief Scientist & Defense Anchor)**:
   - **Role**: Second laptop operator, deterministic verifier monitor, emergency backup pilot.
   - **Position**: Standing upright immediately adjacent to Member C.
   - **Movement Rules**:
     - Monitors Laptop 2 running identical mirrored terminal and backup video.
     - Manages the hardware HDMI switcher. If Laptop 1 stutters, Member D executes the physical switch within **1.0 second**.
     - During Q&A, steps forward to support deep mathematical or code-level inquiries.

### 5.3 A/V Cabling, Display & Switching Topology

```
┌────────────────────────┐      HDMI 1 (1080p60)
│ Master Laptop 1 (C)    │─────────────────────────┐
│ Streamlit / Terminal   │                         │
└────────────────────────┘                         ▼
                                       ┌───────────────────────┐      Master HDMI Out     ┌───────────────────────┐
                                       │ 2x1 4K HDMI Switcher  │─────────────────────────►│ Stage Main Projector  │
                                       │ (Push-button / <0.5s) │                          │ (1920x1080 @ 60Hz)    │
                                       └───────────────────────┘                          └───────────────────────┘
┌────────────────────────┐                         ▲
│ Defense Laptop 2 (D)   │─────────────────────────┘
│ VLC MP4 / verify_all   │      HDMI 2 (1080p60)
└────────────────────────┘
```

- **Dual-Feed Redundancy**: Both laptops feed into an active, powered 2×1 HDMI switcher located between Member C and Member D.
- **Switch Time**: Mechanical toggle latency is $< 500\text{ ms}$. If Laptop 1 experiences an operating system hang, Member D depresses the Channel B button, instantly routing Laptop 2's pre-rendered 1080p video or terminal to the main screen.

---

## 6. Offline Failsafe Triad Protocol (SOP)

```
                            ┌──────────────────────────────────────┐
                            │      STAGE FAILSAFE TRIAD (SOP)      │
                            └──────────────────────────────────────┘
                                               │
             ┌─────────────────────────────────┼────────────────────────────────┐
             ▼                                 ▼                                ▼
┌─────────────────────────┐       ┌─────────────────────────┐      ┌─────────────────────────┐
│         LEVEL 1         │       │         LEVEL 2         │      │         LEVEL 3         │
│   Live Streamlit UI     │  ───► │  Deterministic Verifier │ ───► │  Prerendered 1080p MP4  │
│     (localhost:8501)    │       │    (verify_all.py CLI)  │      │ (presentation_demo.mp4) │
│  Full interactive UI    │       │   29 issues in 0.37s    │      │  Guaranteed 75s replay  │
└─────────────────────────┘       └─────────────────────────┘      └─────────────────────────┘
```

The presentation must never grind to a halt due to software or operating system crashes. The team enforces a rigid **3-Second Escalation Rule**: if any demonstration asset hangs or produces an unexpected error for $\ge 3$ seconds, the presenter executes immediate cutover to the next failsafe tier without apologizing or attempting live debugging.

### 6.1 The Three Defensive Tiers

#### Tier 1: Primary Live Streamlit Cockpit (`localhost:8501`)
- **Runtime**: Local Python 3.13 process running `streamlit run app.py` and `demo_scenarios/app.py`.
- **Operating Conditions**: 100% offline (Airplane Mode ON). Zero external API calls, zero DNS lookups, zero cloud dependencies.
- **Strengths**: Interactive time sliders, real-time power graphs, live Break-Before-Make contactor state indicators, and on-the-fly parameter adjustments.
- **Operational Rule**: Member C navigates exclusively via pre-programmed `Jump to` radio buttons rather than manual slider scrubbing to guarantee instant frame rendering ($< 50\text{ ms}$).

#### Tier 2: Deterministic CLI Verifier (`verify_all.py`)
- **Runtime**: Local Windows Terminal running standard CPython execution: `python verify_all.py`.
- **Execution Profile**: Runs 29 distinct Issue #2 verification routines across all 45 unedited CSV files.
- **Execution Latency**: Exactly **0.37 seconds of timed work** (wall clock $< 1.5\text{ s}$ including Python startup).
- **Strengths**: 100% deterministic, immune to browser WebGL or JavaScript rendering glitches, outputs crystal-clear ASCII pass tables with exact mathematical proofs.
- **Trigger Scenario**: Triggered if the Streamlit browser process experiences a rendering stall or memory freeze.

#### Tier 3: Prerendered 1080p MP4 Backup Video (`demo/presentation_demo.mp4`)
- **Runtime**: VLC Media Player on Laptop 2, pre-loaded with `demo/presentation_demo.mp4` (75.0s duration, 1920×1080 @ 30fps, 6.06 MB) or individual micro-fault recordings under `demo_scenarios/*.mp4`.
- **Strengths**: Hardware-decoded video stream; 0% chance of computational freeze; perfectly timed to the speaker's rehearsal script.
- **Trigger Scenario**: Triggered if both browser and terminal environments fail, or if stage projector experiences HDMI handshake drops on Laptop 1.

---

### 6.2 Escalation Matrix & Verbal Recovery Scripts

| Trigger Event | Detection Threshold | Technical Execution | Verbal Recovery Script (Speaker B / A) |
|---|---|---|---|
| **Streamlit Browser Stalls or Shows "Connection Lost"** | UI unresponsive for $\ge 3$ seconds after clicking `Jump` | Member C presses `Alt + Tab` to open pre-staged Windows Terminal; presses `Enter` to run `python verify_all.py`. | **Speaker B (Smooth Pivot)**:<br>*"While the local browser re-renders our WebGL canvas, look at our raw deterministic engine in the terminal. In 0.37 seconds, verify_all.py verifies all 29 scenario invariants across 240,000 rows—100% passing."* |
| **Terminal or Python Interpreter Throws Error** | Any unexpected exception or process exit | Member D taps HDMI Switcher Button B; Laptop 2 instantly projects VLC media player; Member D presses `Spacebar` to play `presentation_demo.mp4`. | **Speaker B (Assertive Transition)**:<br>*"To respect our strict 10-minute stage cutoff, let's look at the pre-recorded telemetry stream of this exact Scenario Day run. Notice at 22:31 how the predictive maintenance engine flags the bearing failure..."* |
| **Stage Projector Loses Signal (Black Screen)** | Projector shows blue/black screen or "Searching Signal" | Member D unplugs and reseats master HDMI connector; Member C verifies local laptop screens are active. Speaker A steps to downstage apron. | **Speaker A (Impromptu Authority)**:<br>*"While the stage HDMI syncs, let's talk about the numbers that don't need a screen: 20.76 FTEs, 1.82 million euros, and zero grid overlimits across 134,000 intervals. That is the empirical reality of the Kempower dataset..."* |
| **Slide Clicker Battery Dies or USB Receiver Unpairs** | Slide fails to advance on 2 consecutive clicks | Speaker A immediately lowers clicker to side; uses verbal hand signal to Speaker B / Member C: *"Next slide, please."* Member C presses `Right Arrow` on Laptop 1. | **Speaker A (Zero Hesitation)**:<br>*"Moving to our baseline data on slide two... [glances at screen confirming advance]... we audited all 45 CSVs..."* |
| **Auditorium Wi-Fi Unexpectedly Reconnects or Prompts** | OS pop-up or network captive portal appears | Airplane Mode is permanently locked; if a modal appears, Member C hits `Esc` or `Alt + F4` within $< 1\text{ s}$. | **Speaker B (Uninterrupted)**: Continues speaking without acknowledging the OS artifact. |

---

### 6.3 Post-Demo System Shutdown & Handoff Checklist
Following completion of the Q&A session:
1. Member C archives session logs: `Get-Content streamlit.log | Out-File -Append demo_run.log`.
2. Member D collects physical handout packets if judges leave them behind (or offers them as permanent gifts).
3. Confirm HDMI switcher returned to stage default.
4. Notify orchestrator via `handoff.md` that stage operations executed flawlessly within the 600s boundary.
