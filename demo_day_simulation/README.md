# Project Sentinel: Demo Day Master Operations Guide & Simulation Playbook

```
========================================================================================
PROJECT SENTINEL · THE SELF-OPERATING CHARGING NETWORK
Demo Day Master Operations System: Architecture, Deliverables Index & Stage Playbook
Competition: LahtiES Energy Tech Hackathon 2026 · Kempower Flagship Challenge
Auditorium: LUT University Lahti Campus · Saturday 07.11.2026
Standard: Strict 10:00 (600s) Pitch Limit + 04:00 (240s) Jury Cross-Examination Defense
Document ID: SIM-00-MASTER-README-INDEX · Release Version: 2.4-PRODUCTION
========================================================================================
```

---

## 1. System Overview & Mission Context

**Project Sentinel** is an enterprise-grade, autonomous charging network orchestration platform purpose-built for the **Kempower Flagship Challenge** at the **LahtiES Energy Tech Hackathon 2026**. 

In high-stakes hackathon finals, world-class engineering must be matched by flawless stage execution, synchronized team choreography, and ironclad defense under adversarial cross-examination. Kempower's evaluation criteria rigorously test:
1. **Degree of Autonomy (25%)**: True zero-human-in-the-loop operation under physical faults, sub-zero weather, and dynamic spot pricing.
2. **Energy and Grid Impact (20%)**: Transformer capacity management, peak shaving, 95.5% rectification loss accounting, and local grid resilience.
3. **Technical Credibility (20%)**: 25 kW modular Dynamic Power Routing (DPR), 260ms Break-Before-Make (BBM) contactor safety, mathematical solver stability, and adherence to physical hardware boundaries (`cross_tie = False`).
4. **Commercial Viability (20%)**: Clear ROI, transition from 21 FTE (€1,365,000/yr) manual triage to software autonomy, and a legally sound One-Page Charging-as-a-Service (CaaS) / AEaaS agreement.
5. **Clarity & Stage Presentation (15%)**: Strict adherence to the 10-minute stage cutoff, seamless speaker handoffs, and an interactive, failsafe-hardened live flight control console.

The `demo_day_simulation/` operational suite establishes the definitive operating system for Project Sentinel's stage appearance, arming the 4-person team with minute-by-minute scripts, failsafe protocols, psychological judge profiles, and quantitative defense proofs.

---

## 2. Master Deliverables Directory & Reading Roadmap

The simulation package is organized into six interconnected, authoritative manuals. Every deliverable is mirrored 1:1 in `docs/demo_day/` for production distribution and offline auditorium access:

```
demo_day_simulation/  (Mirrored to: docs/demo_day/)
├── README.md                                  # [THIS FILE] Master index, architecture & navigation guide
├── 00_pocket_cheat_sheet.md                   # 1-page ultra-condensed on-stage quick reference card
├── 01_stage_schedule_and_setup.md             # R1: Minute-by-minute 600s pitch + 240s Q&A timeline & stage setup
├── 02_team_roles_and_coordination.md          # R2: 4-Person roles, verbatim relay scripts & console SOP
├── 03_judge_personas_and_question_bank.md     # R3: Tripartite judge profiles & 14 hardcore question bank
└── 04_structured_defense_and_crisis_manual.md # R4: 14 3-part structured defense answers & emergency crisis SOPs
```

### Document Index & Functional Specification

| Document | Feature Inventory | Primary Audience & Stage Function | Key Deliverables & Methodologies |
|---|---|---|---|
| **[`00_pocket_cheat_sheet.md`](./00_pocket_cheat_sheet.md)** | Master Cheat Sheet | **All 4 Team Members**<br>Laminated pocket card & lectern reference | • 600s + 240s timeline cheat sheet<br>• Role assignments & Q&A routing map<br>• 5 Iron Invariant numbers<br>• Emergency cutover hotkeys & rescue cues |
| **[`01_stage_schedule_and_setup.md`](./01_stage_schedule_and_setup.md)** | **F1 & F2** (R1)<br>Stage Schedule & Setup | **Stage Manager, Speakers A & B, Member C**<br>Pre-flight & pitch flight control | • T-30m to T-0m pre-flight verification ledger<br>• Second-by-second 600s pitch breakdown (Slides P1–P12)<br>• 240s Q&A timing & buffer allocations<br>• ASCII stage setup & physical line-of-sight layout<br>• 3-Tier Offline Failsafe Triad protocol |
| **[`02_team_roles_and_coordination.md`](./02_team_roles_and_coordination.md)** | **F3, F4 & F5** (R2)<br>Roles & Coordination | **All 4 Members, Live Console Operator**<br>Team choreography & console execution | • 4 distinct member profiles & behavioral codes<br>• Verbatim Speaker A $\leftrightarrow$ B relay transitions<br>• Member C Live Console SOP (Tabs, hotkeys, triggers)<br>• Fallback cutover trigger decision matrix |
| **[`03_judge_personas_and_question_bank.md`](./03_judge_personas_and_question_bank.md)** | **F6 & F7** (R3)<br>Personas & Questions | **All 4 Members**<br>Adversarial cross-examination prep | • 3 Tripartite judge profiles (Mats/Panu, VC, Host)<br>• Psychological archetypes, technical lenses & red flags<br>• 14 Hardcore Questions (Q01–Q14) with metadata<br>• Cross-disciplinary coverage of physics, code & ROI |
| **[`04_structured_defense_and_crisis_manual.md`](./04_structured_defense_and_crisis_manual.md)** | **F8, F9 & F10** (R4)<br>Defense & Crisis | **All 4 Members, Technical Lead D**<br>Live defense & black-swan emergency | • 14 structured 3-part defense answers (Assertion $\to$ Proof $\to$ Takeaway)<br>• Exact citations of 45 CSVs, math formulas & code lines<br>• Team defense synergy, handoff bridge tags & interjections<br>• 6 Black-Swan stage crisis recovery SOPs |

---

## 3. High-Level Stage Timeline & Flight Path

```
T-30m               T-0m      00:30               03:45        05:00       07:00       07:30        09:30   10:00        14:00
  │                   │         │                   │            │           │           │            │       │            │
  ▼                   ▼         ▼                   ▼            ▼           ▼           ▼            ▼       ▼            ▼
┌───────────────────┬─────────┬───────────────────┬────────────┬───────────┬───────────┬────────────┬───────┬────────────┐
│ Pre-Stage         │ Cold    │ Business Pain &   │ System     │ Live Demo │ Outcome   │ Customer   │ Close │ Jury Q&A   │
│ Hardware, OS &    │ Open    │ 21 FTE (€1.365M)  │ Arch & DPR │ Console   │ CaaS SLA  │ Story 2029 │ & CTA │ 14 Defense │
│ A/V Verification  │ (30s)   │ Labor Audit (195s)│ 25kW (75s) │ (120s max)│ (30s)     │ & S1 (120s)│ (30s) │ Answers    │
│ (Member C & D)    │ Spk A   │ Speaker A         │ Speaker B  │ Spk B + C │ Speaker A │ Speaker A  │ Spk A │ (All 4)    │
└───────────────────┴─────────┴───────────────────┴────────────┴───────────┴───────────┴────────────┴───────┴────────────┘
                      P1        P1 -> P2            P3 -> P6     P7 Console  P9          P8 -> P10    P12     Auditorium
```

### Core Presentation Milestones (Total: 600s / 10:00)
- **00:00 – 00:30 (P1)**: *Cold Open & Hook* (Speaker A) — Sub-zero Finland depot at 2:15 AM; 360 kW power trip with zero humans on site.
- **00:30 – 03:45 (P1–P2)**: *Commercial Reality & Pain Points* (Speaker A) — Mats Mattsson's 21 FTE baseline (€1,365,000/yr @ €65k/yr) vs 20.76 FTE statutory baseline (€1.82M/yr @ €45/h); handing laminated SLA to judges.
- **03:45 – 05:00 (P3–P6)**: *Technical Architecture & Physical Invariants* (Speaker B) — L1 Physical, L2 Edge, L3 Cloud decoupling; 25 kW modular DPR matrix; 260ms BBM contactor sequencing; 95.5% inverter loss invariant ($1,425\text{ kW DC} = 1,492.15\text{ kW AC} \le 1,500\text{ kW}$).
- **05:00 – 07:00 (P7)**: *Live Flight Control Console* (Speaker B + Member C) — 120s real-time demonstration in Streamlit; resolving S1 depot trip, S2 dynamic tariff spike, and S3 highway islanding with zero human touches.
- **07:00 – 07:30 (P9)**: *Outcome-Based CaaS Agreement* (Speaker A) — One-Page SLA with 99.5% uptime commitment, penalty structures, and MRDT §5.1 anti-fraud dwell time gate.
- **07:30 – 09:30 (P8–P10)**: *The 2029 Customer Story & Busbar Truth* (Speaker A) — Pekka Virtanen's uncrewed depot; confronting S1 busbar reality (13 → 3 software triage for 0 € vs 13 → 0 requiring unpriced DC busbar hardware tie).
- **09:30 – 10:00 (P12)**: *Grand Close & Call to Action* (Speaker A) — Autonomous charging is not a 2035 dream; Sentinel runs it today on existing Kempower hardware.
- **10:00 – 14:00**: *Jury Rapid-Fire Defense* (All 4) — 240s structured cross-examination across Technical, Commercial, and Kempower Challenge domains.

---

## 4. 4-Person Role Division & Q&A Routing Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE SENTINEL 4-PERSON TEAM                                │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ Role & Member            │ Primary Pitch Focus      │ Primary Q&A Defense Domains      │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ **Speaker A**            │ Business Pain, Customer  │ • Q04: 21 FTE (€1.365M) Cost     │
│ Chief Commercial Officer │ Story 2029, SLA, Close   │ • Q05: 2-Month Payback & CaaS    │
│ (Front Stage Left)       │ (Slides P1, P2, P8–P10)  │ • Q14: S2 Dynamic Tariffs        │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ **Speaker B**            │ Architecture, DPR Matrix,│ • Q01: 13→3 vs 13→0 Busbar Truth │
│ Chief Systems Architect  │ Live Demo Voiceover      │ • Q02: Dual-Gun & S1 Topology    │
│ (Front Stage Center)     │ (Slides P3–P7, P11)      │ • Q08: Thermal PdM Warnings      │
│                          │                          │ • Q09: S3 Islanding & Local DLM  │
│                          │                          │ • Q13: S5 Custom Site Deploy     │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ **Member C**             │ Live Flight Control,     │ • Q10: Live Telemetry Proof      │
│ Lead Demo Engineer       │ UI Cockpit, Hotkeys      │ • Real-time UI scenario triggers │
│ (Stage Right Console)    │ (Laptop 1: Streamlit)    │ • Live data inspection & drills  │
├──────────────────────────┼──────────────────────────┼──────────────────────────────────┤
│ **Member D**             │ Offline Verification,    │ • Q03: 260ms BBM Contactor Relay │
│ Chief Applied Scientist  │ Forensic Math & Code     │ • Q06: MRDT & Anti-Fraud Gate    │
│ (Stage Right Tech Pod)   │ (Laptop 2: Pytest / CLI) │ • Q07: 799.30€ Spot Price Slack  │
│                          │                          │ • Q11: Sub-Zero Battery PTC Math │
│                          │                          │ • Q12: 95.5% Inverter Rectify    │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

---

## 5. Offline Failsafe Triad Protocol

Project Sentinel operates under a strict **Zero-Cloud-Dependency** mandate in the auditorium. The presentation environment implements a **3-Tier Failsafe Triad**:

```
[Tier 1: Interactive Dashboard] ──(Latency > 2.5s / Crash)──> [Tier 2: Deterministic CLI] ──(Laptop Freeze)──> [Tier 3: 1080p Video]
  Streamlit local cockpit                                       PowerShell `verify_all.py`                         VLC `presentation_demo.mp4`
  Port 8501, 100% offline                                       29/29 checks in < 0.5s                             Instant HDMI switch toggle
```

1. **Tier 1 (Primary)**: Local Streamlit interactive flight cockpit (`app.py` on port 8501). Full parameter manipulation and interactive scenario replays.
2. **Tier 2 (Secondary)**: Deterministic CLI verification runner (`python verify_all.py`). Executes all 29 mathematical and physical checks in $< 0.5\text{ s}$ with color-coded ANSI terminal output.
3. **Tier 3 (Tertiary)**: Pre-rendered 1080p30 backup video recording (`demo/presentation_demo.mp4`). Mirrored on Laptop 2 and pre-loaded in VLC; accessible via an instantaneous hardware HDMI switcher toggle ($< 1.0\text{ s}$).

**Cutover Rule**: If Streamlit server response time exceeds **2.5 seconds** or throws an unhandled exception, Member C immediately issues the verbal cue *"Executing CLI flight verification"* and switches to Tier 2 without pausing the speaker.

---

## 6. The Five Non-Negotiable Quantitative Invariants

Every member of the Sentinel team is drilled on the **Five Iron Numbers** derived directly from the hackathon challenge brief, kickoff keynote, and repository ground truth:

1. **Labor Baseline**: **21 FTE** (€1,365,000/yr @ €65,000/yr) based on Mats Mattsson's keynote baseline, or **20.76 FTE** (€1.82M/yr @ €45/h statutory Finnish overtime rates) for 100-site uncrewed operation.
2. **The Busbar Truth**: **13 → 3 vs 13 → 0**. Sentinel's zero-CAPEX software triage cuts missed departures from 13 to 3 on existing physical wiring (`cross_tie = False`). Reaching 0 missed departures physically requires an inter-cabinet DC busbar tie, which has 0 € pricing in Kempower's official `equipment_costs.csv`.
3. **Contactor Relay Envelope**: **260ms BBM** (Break-Before-Make). Six-step contactor switching protocol in `src/core/self_healing.py` guarantees zero DC arcing under high inductive loads and finishes well within the 500ms safety envelope.
4. **Spot Tariff Spike**: **799.30 €/MWh**. S2 synthetic spot price spike handled gracefully via continuous battery state-of-charge (SoC) slack variables $z \in [0, 1]$ in the rolling 15-minute HiGHS MILP solver, guaranteeing feasibility under extreme financial stress.
5. **Edge Islanding & Inverter Physics**: **1,425 kW DC** edge islanding capacity at S3 Highway Hub. Correctly applying the $\eta = 0.955$ rectification efficiency yields $P_{AC} = 1425 / 0.955 = 1492.15\text{ kW}$, respecting the $1,500\text{ kW}$ utility transformer physical limit.

---

## 7. Verification & Audit Guide

The integrity of this entire simulation package is validated through independent, automated end-to-end tests:

```powershell
# Run the complete Demo Day Simulation test suite (28 assertions)
python -m pytest tests/test_demo_day_simulation.py -v

# Run targeted checks by requirement group
python -m pytest tests/test_demo_day_simulation.py -k "TestR1" -v
python -m pytest tests/test_demo_day_simulation.py -k "TestR2" -v
python -m pytest tests/test_demo_day_simulation.py -k "TestR3" -v
python -m pytest tests/test_demo_day_simulation.py -k "TestR4" -v
python -m pytest tests/test_demo_day_simulation.py -k "TestMaster" -v
```

All 28/28 tests are designed to prevent facades and enforce genuine structural, textual, and mathematical rigor across all deliverables.
