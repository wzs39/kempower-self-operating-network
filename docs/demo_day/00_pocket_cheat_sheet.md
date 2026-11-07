# Project Sentinel: On-Stage Pocket Cheat Sheet (1-Page Quick Reference Card)

```
========================================================================================
PROJECT SENTINEL · ON-STAGE POCKET REFERENCE CARD (LAMINATED 1-PAGER)
Auditorium: LUT University Lahti Campus · Saturday 07.11.2026
Pitch Limit: 10:00 (600s Hard Cutoff) | Defense Window: 04:00 (240s Rapid-Fire Q&A)
Document ID: SIM-00-POCKET-CHEAT-SHEET · Release Version: 2.4-PRODUCTION
========================================================================================
```

---

## 1. 600s Pitch Timeline & Slide Pacing Cheat Sheet

| Time Window | Slide | Presenter | Key Focus & Stage Action | Hard Time Gate |
|---|---|---|---|---|
| **00:00 – 00:30** | **P1** | **Speaker A** | **Cold Open**: 2:15 AM January 2029, -18°C Lahti depot, 360 kW trip with 0 humans. | Pass 00:30 on pace |
| **00:30 – 03:45** | **P1–P2** | **Speaker A** | **Business Pain & Labor Audit**: 21 FTE (€1.365M/yr) vs 20.76 FTE. Hand SLA to jury at 00:30. | Relay B @ 03:45 |
| **03:45 – 05:00** | **P3–P6** | **Speaker B** | **Architecture & Physics**: L1/L2/L3, 25kW modular DPR, 260ms BBM, $\eta=0.955$ loss. | Demo cut @ 05:00 |
| **05:00 – 07:00** | **P7** | **Spk B + C** | **Live Flight Control (Streamlit)**: 120s max. S1 depot trip, S2 tariff spike, S3 islanding. | Hard cut @ 07:00 |
| **07:00 – 07:30** | **P9** | **Speaker A** | **Outcome CaaS SLA**: 99.5% uptime commitment, late penalties, MRDT §5.1 anti-fraud gate. | On pace |
| **07:30 – 09:30** | **P8–P10**| **Speaker A** | **Customer Story 2029 & S1 Busbar**: Pekka Virtanen depot; 13→3 software vs 13→0 busbar. | Final slide @ 09:30 |
| **09:30 – 10:00** | **P12** | **Speaker A** | **Grand Close & CTA**: "Zero-human charging is solved today on existing Kempower hardware." | **STOP @ 09:55** |
| **10:00 – 14:00** | **All** | **All 4** | **Jury Defense**: 240s rapid-fire answers. 15s bottom line $\to$ hard numbers $\to$ takeaway. | Exit @ 14:00 |

---

## 2. The 5 Non-Negotiable Hard Numbers ("Iron Invariants")

1. **Labor Baseline**: **21 FTE** (€1,365,000 / €1.365M / yr @ €65,000/yr) Mats Mattsson keynote baseline; **20.76 FTE** (€1.82M/yr @ €45/h statutory Finnish overtime rates) for 100-site uncrewed operation.
2. **The Busbar Truth**: **13 → 3 vs 13 → 0**. Sentinel 0 € CAPEX software triage cuts missed departures from 13 to 3 on existing physical wiring (`cross_tie = False`). Reaching 0 missed departures physically requires an inter-cabinet DC busbar tie, which has no price in `equipment_costs.csv`.
3. **Contactor Relay Envelope**: **260ms BBM** (Break-Before-Make). Six-step contactor switching protocol in `src/core/self_healing.py` (< 500 ms safety envelope, zero DC arcing).
4. **Spot Tariff Spike**: **799.30 €/MWh**. Handled gracefully via continuous battery state-of-charge (SoC) slack variables $z \in [0, 1]$ in HiGHS MILP, avoiding infeasibilities under extreme financial stress.
5. **Edge Islanding & Inverter Physics**: **1,425 kW DC** at S3 Highway Hub. $P_{AC} = 1425 / 0.955 = 1492.15\text{ kW} \le 1500\text{ kW}$ utility transformer physical limit ($\eta = 0.955$).

---

## 3. 4-Person Role Division & Q&A Routing Matrix

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              RAPID-FIRE Q&A ROUTING MAP                                │
├─────────────────────┬─────────────────────┬────────────────────┬───────────────────────┤
│ SPEAKER A           │ SPEAKER B           │ MEMBER C           │ MEMBER D              │
│ Commercial & Story  │ Systems Architect   │ Live Flight Pilot  │ Forensic Math & Code  │
├─────────────────────┼─────────────────────┼────────────────────┼───────────────────────┤
│ • Q04: 21 FTE Cost  │ • Q01: 13→3 Busbar  │ • Q10: Live Tele-  │ • Q03: 260ms BBM Relays│
│ • Q05: 2-Month ROI  │ • Q02: Dual-Gun Top │   metry Proof      │ • Q06: MRDT & SLA Gate│
│ • Q14: S2 Dynamic   │ • Q08: Thermal PdM  │ • Trigger UI drill │ • Q07: 799.30€ MILP   │
│   Flexibility       │ • Q09: S3 Islanding │   on Laptop 1      │ • Q11: Sub-Zero Batt  │
│                     │ • Q13: S5 Config    │                    │ • Q12: 95.5% Inverter │
└─────────────────────┴─────────────────────┴────────────────────┴───────────────────────┘
```

### Response Golden Rule:
1. **First 15s**: Direct, unequivocal bottom-line conclusion (Speaker A or B).
2. **Next 45s**: Concrete empirical data citation, mathematical formula, or CSV row (Speaker B or Member D).
3. **Last 15s**: Strategic takeaway, SLA guarantee, or commercial protection (Speaker A).

---

## 4. Member C Live Console SOP & Hotkeys

- **Primary URL**: `http://localhost:8501/` (Locked at 100% zoom, Fullscreen `F11`).
- **Tab Setup**:
  - `Tab 1`: Executive Cockpit (Real-time telemetry, 5 site map, L1-L3 status).
  - `Tab 2`: Scenario Day Replay (S1 depot trip, S2 tariff spike, S3 highway islanding).
- **Console Hotkey Actions**:
  - `1`: Inject S1 Cabinet Trip (`F016` @ 02:25, 246 min outage) $\to$ Show 260ms BBM self-healing.
  - `2`: Inject S2 Spot Price Spike (799.30 €/MWh) $\to$ Show HiGHS MILP peak shaving & BESS dispatch.
  - `3`: Inject S3 Grid Islanding (Transformer trip) $\to$ Show 1,425 kW DC local DLM throttling.
  - `F11`: Fullscreen toggle.
  - `Ctrl + R`: Hard refresh if UI websocket drops.

---

## 5. Failsafe Triad Cutover & Emergency Protocols

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              THE 3-TIER FAILSAFE TRIAD                                 │
├────────────────────────────┬─────────────────────────────┬─────────────────────────────┤
│ TIER 1: STREAMLIT COCKPIT  │ TIER 2: DETERMINISTIC CLI   │ TIER 3: PRE-RENDERED VIDEO  │
│ localhost:8501 (Laptop 1)  │ PowerShell: verify_all.py   │ VLC: presentation_demo.mp4  │
│ Latency < 2.5s, 100% local │ 29/29 checks in < 0.5s      │ Laptop 2 via HDMI Switch B  │
└────────────────────────────┴─────────────────────────────┴─────────────────────────────┘
```

### Black-Swan Emergency Action Drills:
- **Streamlit Freezes / Latency > 2.5s**: Member C whispers *"CLI cutover"*; presses `Alt+Tab` to PowerShell; runs `python verify_all.py`. Speaker B seamlessly says: *"Let us verify the mathematical invariants directly in our offline verification engine..."*
- **Laptop 1 Crashes / Blue Screen**: Member D flips HDMI hardware switch to **Input B**; Laptop 2 displays pre-rendered 1080p demo video in VLC. Speaker B narrates over video without missing a beat.
- **Judge Interrupts / Challenges Aggressively**: Speaker A maintains warm eye contact: *"Thank you, Mats. The exact answer in 15 seconds is [Assertion]. Speaker B, explain the contactor mechanics."* Never argue; pivot to data.
- **1-Minute Time Warning (09:00)**: Speaker A immediately skips secondary examples and advances to Slide P12: *"To summarize Project Sentinel in three words..."*
- **Question Completely Outside Scope**: Speaker A: *"Under Kempower's hackathon dataset boundary, that specific metric is uninstrumented. However, in our One-Page SLA §4.2, we model that exact risk by..."*

---

## 6. Verbatim Verbal Transition Cues

- **Speaker A $\to$ Speaker B (03:45)**:  
  *"To explain how Sentinel solves this at the physical wire, without a single human on site, here is our Chief Systems Architect, Speaker B."*
- **Speaker B $\to$ Member C (05:00)**:  
  *"Let's stop talking and see the code fly. Member C, take flight control."*
- **Speaker B $\to$ Speaker A (07:00)**:  
  *"And that is how software replaces 21 FTEs of manual dispatch. Speaker A, show us how this transforms the business."*
