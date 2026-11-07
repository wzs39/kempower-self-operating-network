# Project Sentinel: Demo Day Live Operational Standard Operating Procedure (Live Demo SOP)

```
========================================================================================
PROJECT SENTINEL · LIVE DEMO OPERATIONAL SOP
Scope: Demo Day Live Operations, Dual-Machine Hot Standby, Fault Injection & Defense Verification
Core Operators: Member C (Lead Console Operator) + Member D (Data Integrity & Hot-Standby Operator)
Coordinating Speakers: Speaker A (Commercial Lead) + Speaker B (Architecture Lead)
Document Version: v2.5-PRODUCTION · On-Stage Operational Manual
========================================================================================
```

---

## 1. Hardware Topology & Physical Cabling Standards (Ready at T-30min)

### 1.1 Equipment Manifest & Physical Interconnection Map
```
   [ Primary Laptop (Laptop 1) ] ──HDMI 1──┐
   (Operated by Member C, Streamlit/CLI)    │
                                            ├───► [ Hardware HDMI Switcher ] ───► [ Stage Screen / 1080p Projector ]
   [ Standby Laptop (Laptop 2) ] ──HDMI 2──┘       (Managed by Member D, One-Touch Toggle)
   (Operated by Member D, VLC / Mirror)
```

- **Primary Machine (Laptop 1)**: Windows 11 / macOS; power adapter connected; sleep and screen saver permanently disabled.
- **Standby Machine (Laptop 2)**: Matching hardware specification; pre-loaded with offline 1080p backup videos (`demo/presentation_demo.mp4`, etc.).
- **Hardware Switcher**: 2-in-1-out (2x1) physical push-button HDMI switcher, positioned directly under Member D's right hand (zero dependence on software display switching).
- **Presentation Clicker & Audio**: Speakers A and B equipped with wireless lapel microphones; presentation clicker USB dongle inserted into Laptop 1.

---

## 2. Pre-Flight Hardening & Cold Start Protocol (T-20min Checklist)

### Step 1: Primary Operating System "Combat Hardening" (Member C)
1. **Disconnect External Networks**: Activate system **Airplane Mode** (sever Wi-Fi, Bluetooth, unplug physical Ethernet cables) to guarantee 100% offline edge execution without cloud dependencies.
2. **Focus Mode Activation**: Enable **Focus Assist / Do Not Disturb**; terminate all background messaging and popup applications.
3. **Power & Display Lockdown**:
   - Plug into AC power; set power management profile to "Best Performance".
   - Screen Saver: None; Sleep Timeout: Never.

### Step 2: Local Offline Services Initialization & Pre-Warming (Member C)
Open Windows Terminal (PowerShell) in project root (`C:\Users\qwe\Desktop\hackson`) and execute:

```powershell
# 1. Execute deterministic verification across all 29 items (latency < 0.5s)
python verify_all.py

# 2. Launch local Streamlit command center (offline localhost:8501)
streamlit run app.py --server.headless=true --server.port=8501
```

### Step 3: Browser Window & Shortcut Configuration (Member C)
1. Open Chrome / Edge browser to: `http://localhost:8501/`.
2. Press `F11` for **clean fullscreen mode** (hide bookmarks, URL bar, tabs); lock zoom to **100%**.
3. Verify all 4 core views load cleanly via top navigation bar:
   - **View 1**: Executive Cockpit (20.76 FTE Labor Elimination Waterfall)
   - **View 2**: Scenario Day 2026-11-13 Minute-by-Minute Live Player (Fault Injection Console)
   - **View 3**: Live Hardware Matrix & Protocol Inspector (25kW DPR Topology & BBM Relay Timing)
   - **View 4**: Commercial SLA & Dispute Clearing (MRDT Settlement Calculator)
4. Set default active view to **View 1: Executive Cockpit**, ready for stage entrance.

### Step 4: Standby Machine & Backup Media Readiness (Member D)
1. Standby Laptop 2 launches VLC Media Player, paused at frame 0 of offline recording.
2. Standby terminal pre-staged with command: `python verify_all.py`.
3. Physical documentation: hand 4 printed copies of `One-Page SLA Specification` to Speaker A.
4. Confirm hardware HDMI switcher is toggled to **Channel 1 (Primary Machine)**.

---

## 3. Minute-by-Minute Live Presentation Execution SOP

### Phase 1: Static Pitch Delivery (00:00 - 05:00) — Silent Monitoring
- **Main Projector**: Displays PowerPoint slide deck presented by Speakers A and B (Slides 1 to 6).
- **Member C Actions**:
  - Hands lightly positioned on keyboard; screen locked on `http://localhost:8501/` **View 2: Scenario Day**.
  - Confirm Timeline Scrubber is initialized at `00:00` or `01:30`.
  - Monitor countdown timer.
- **Member D Actions**:
  - Monitor CPU/RAM telemetry on Laptop 1; right hand resting near HDMI switcher button; ready for immediate action.

---

### Phase 2: Live Demo Golden Window (05:00 - 07:00) — Three Core Demonstrations

Triggered when Speaker B delivers the transition cue:  
> **Verbal Cue**: *"Talk is cheap, let's see the code fly. Member C, engage console flight mode."*

#### [Action 1: Screen Cutover to Command Console (05:00)]
1. Member C seamlessly executes `Alt + Tab` to transition stage projection from PowerPoint to Chrome browser (`localhost:8501/`).
2. Select radio button: **View 2: Scenario Day 2026-11-13 Minute-by-Minute Live Player**.
3. Quick Jump Buttons and 24-hour timeline scrubber render immediately.

---

#### [Action 2: Scenario 1 — S1 Bus Depot Sub-Zero Thermal Trip & 260ms BBM Self-Healing (05:05 - 05:40)]
- **Execution Steps**:
  1. Member C clicks Quick Jump Button: **[02:25 S1 Thermal Trip]** (or drags scrubber to `02:30`).
  2. Red/black high-priority alert banner renders:  
     `🔴 S1 Incident Active: Cabinet C1-3 Overtemperature Stop (F016)`.
  3. Member C expands accordion: **[⚡ Inspect DPR Matrix Dynamic Contactor State]**.
  4. Display highlights:
     - `C1-3` is marked `ISOLATED_TEMP` (fault isolated);
     - `C1-1` and `C1-2` remain `ONLINE (360 kW)` at full capacity;
     - Contactor Break-Before-Make completes in < 260ms without DC arcing, buses continue charging.
- **Speaker B Voiceover**: *"At 02:25, Cabinet C1-3 triggers an overtemperature stop. The edge controller completes contactor break-before-make in under 260ms, seamlessly transferring load to surviving cabinets with zero delayed bus departures across all 24 morning runs!"*

---

#### [Action 3: Scenario 2 — S4 Extreme Spot Price Spike & HiGHS Real-Time Peak Shaving (05:40 - 06:20)]
- **Execution Steps**:
  1. Member C clicks Quick Jump Button: **[18:00 S4 Price Spike]**.
  2. Display updates to highlight alert:  
     `🔴 S4 Extreme Spot Price Spike: €799.30/MWh`.
  3. Member C scrolls down slightly to reveal dynamic power and price curves:
     - Non-critical charging loads are shaved smoothly by rolling 15-minute MILP;
     - Station battery storage initiates peak shaving discharge;
     - Departure SoC is guaranteed at $\ge 90\%$.
- **Speaker B Voiceover**: *"When wholesale spot prices surge to a historic 799.30 €/MWh, Project Sentinel does not disconnect vehicles blindly. The HiGHS optimizer executes millisecond-scale convex peak shaving, safeguarding fleet departures while saving thousands of euros in peak energy exposure."*

---

#### [Action 4: Scenario 3 — S3 Highway Hub WAN Outage & 1,425 kW Autonomous Edge Islanding (06:20 - 06:50)]
- **Execution Steps**:
  1. Member C clicks Quick Jump Button: **[11:00 S3 WAN Outage]**.
  2. Amber incident banner appears:  
     `🟠 S3 Incident Active: Cellular WAN Outage (11:00-13:00) Islanding Mode`.
  3. Member C highlights key operational metrics:
     - `Delivered DC: 1,425 kW`;
     - `Transformer Limit: 1,500 kW` (strictly respecting $P_{AC} = 1425 / 0.955 = 1492.15\text{ kW} \le 1500\text{ kW}$);
     - Offline NVMe transaction journal activates 72-hour encrypted buffering.
- **Speaker B Voiceover**: *"During a complete 2-hour cellular outage, the station edge controller takes over autonomously. Instead of throttling back to the naive 500 kW fallback, it sustains 1,425 kW DC output right at the physical transformer limit without a single kilowatt of grid overcurrent!"*

---

#### [Action 5: Return to Value Cockpit & Transition to Speaker A (06:50 - 07:00)]
- **Execution Steps**:
  1. Member C clicks top radio button: **View 1: Executive Cockpit**.
  2. View locks on **[20.76 FTE Labor Elimination Waterfall (€1,821,534 / year)]**.
  3. Member C steps hands away from keyboard, nodding to Speaker A.
- **Speaker B Closing Cue**: *"That is software-driven self-healing reducing 21 FTE of manual toil to zero. Speaker A, walk us through commercial execution."*
- **Handoff Action**: Member C executes `Alt + Tab` back to Slide 9 of PowerPoint presentation.

---

## 4. Jury Q&A Defense & Live Evidence Retrieval Matrix (10:00 - 14:00)

During the 4-minute Q&A defense, Members C and D must pull up definitive proof on the main or secondary screen within **3 seconds**:

| Question Domain | Trigger Keywords | Member C Action (Main Console) | Member D Action (Evidence Retrieval) |
|---|---|---|---|
| **Q01: Missed Departures 13→3** | *"Why do 3 missed departures remain?"* | Maintain on Slide 8/10 or View 1 S1 Strategy analysis card | Cite Whitepaper: `cross_tie = False`, physical limit of 12 single-gun points |
| **Q03: 260ms Contactor BBM** | *"Is 260ms fast enough for mechanical switches?"* | Switch to **View 3 -> Tab 2**: 6-step BBM state machine and 260ms timing breakdown | Reference code file: `src/core/self_healing.py`, well within IEC 61851 500ms safety limit |
| **Q06: SLA Fraud Prevention** | *"How do you prevent phantom replugs?"* | Switch to **View 4**: Display MRDT §5.1 calculator and 3-minute electrical fingerprint hash gate | Speaker A gestures to physical One-Page SLA agreement §5.1 |
| **Q07: 799 €/MWh Optimization** | *"Does the MILP solver timeout or diverge?"* | Switch to **View 2 -> 18:00**: Show continuous SoC slack convergence ($z_v \in [0, 1]$) in < 80ms | Name solver backend: SciPy HiGHS simplex optimizer, guaranteed convex convergence |
| **Q10: Live Data Authenticity** | *"Is this mock or pre-recorded data?"* | `Alt + Tab` to terminal and run: `python verify_all.py` (passes 29/29 in 0.38s) | Invite jury: *"Select any dispenser ID to disconnect right now, and we will recalculate live!"* |
| **Q12: 1,425 kW Transformer Limit** | *"Did you account for inverter losses?"* | Switch to **View 2 -> 11:00**: Show $1425 / 0.955 = 1492.15\text{ kW} \le 1500\text{ kW}$ | Highlight 95.5% rectification efficiency and 7.85 kW AC safety buffer |

---

## 5. Emergency Failsafe Escalation Protocol

```
[ Incident Triggered ]
  │
  ├──► Symptom: Web UI stalls / latency > 2.5s
  │      └── Tier 1 Failsafe: Instant CLI Verifier Cutover (< 3s)
  │            Action: Member C presses Alt+Tab to PowerShell, hits Enter: python verify_all.py
  │            Result: Clean green execution output verifies all physical equations on stage.
  │
  ├──► Symptom: Browser process crashes / port disconnects
  │      └── Tier 2 Failsafe: Local Hot Restart Script (< 5s)
  │            Action: Member C switches to standby terminal, hits Up-Arrow + Enter: streamlit run app.py
  │            Result: Instant reconnection to 127.0.0.1:8501.
  │
  └──► Symptom: Primary laptop blue-screens / projector drops HDMI signal
         └── Tier 3 Failsafe: Hardware HDMI Switch to Standby Laptop (< 1s)
               Action: Member D presses Button B on hardware HDMI switcher.
               Result: Stage display switches instantly to Laptop 2 running 1080p backup video.
```

---

## 6. Silent Stage Communication & Hand Signals

To maintain flawless professional presence under stage lighting, the team operates using standard competition hand signals:

1. **Countdown Timing (Member D communicates to Speakers)**:
   - 5 minutes remaining: Raise **5 fingers** at chest level, make eye contact with Speakers A/B.
   - 2 minutes remaining: Raise **2 fingers** at chest level.
   - 1 minute remaining (Hard Stop Alert): Form a **closed fist** at chest level; Speaker A must wrap up within 15 seconds to deliver Slide 12 golden closing quote.
2. **Screen Transition Cue (Speaker B to Member C)**:
   - Speaker B naturally points towards console and speaks: *"Let's see the code fly"*; Member C executes `Alt + Tab`.
3. **Emergency Switchover Cue (Member C to Member D)**:
   - If Laptop 1 freezes, Member C double-taps under the desk and whispers: *"Switch B"*;
   - Member D decisively presses HDMI Switcher Button B within **1 second**.

---

## 7. Pre-Stage Operational Checklist

- [ ] Primary Laptop 1 in Airplane Mode; successfully connects to `http://localhost:8501/`.
- [ ] Command `python verify_all.py` outputs 29/29 PASS in < 0.5s.
- [ ] Tested quick jump buttons: `02:25 S1`, `18:00 S4`, `11:00 S3` with switch latency < 1.0s.
- [ ] Hardware HDMI switcher tested; screen transition latency < 1s with zero screen flicker.
- [ ] 4 printed copies of `One-Page SLA Specification` ready on desk.
