# Live Demo Script (120 Seconds) · Project Sentinel

**Challenge**: *The Self-Operating Charging Network*  
**Theme**: Friday 13.11 Scenario Day Autonomy & 21 FTE Human Baseline Elimination  
**Target Audience**: Kempower Jury, Technical Mentors, CPO Executives  

---

## 1. Timeline & Spoken Narrative

| Time | Phase | Spoken Narrative | Visual Action |
|---|---|---|---|
| **00:00 - 00:20** | **The Hook: The 21 FTE Crisis** | "Over a single two-week period, Kempower's charging network required 8,852 manual human interventions—costing 93,412 staff-minutes. That is **21 full-time employees** costing 1.36 million euros a year, mostly spent walking through dark depots to unplug and replug buses at midnight. If humans are no longer allowed to babysit chargers, can the network operate itself?" | Display `operations_log.csv` analysis card: 20.76 FTE baseline, 5,596 replugs (47.9% of labor), €1.365M annual cost. |
| **00:20 - 00:45** | **The Architecture: DPR & Dual-Gun** | "Meet **Project Sentinel**. Built directly on Kempower's 25 kW modular Dynamic Power Routing architecture. In depot S1, we retrofit 12 posts with dual-gun satellites. Drivers plug in once when they park. Sentinel's edge controller automatically orchestrates Phase A (22:00-02:00), executes a sub-500ms zero-arc contactor swap to Phase B (02:00-05:30), and tops off before 06:00. **Zero midnight jockeying. Zero replugs.**" | Switch to Streamlit UI: Show DPR Matrix visualizer with 25 kW module routing and dual-gun contactor states. |
| **00:45 - 01:20** | **Live Crisis Playback: Friday 13.11** | "Now let's stress-test Friday the 13th with zero humans:<br>1. **At 02:25, S1 Cabinet C1-3 overheats**: Instead of a hazardous back-feed, Sentinel safely isolates C1-3, sheds 180 kW in 260 ms, and routes available modules to D1-1~D1-8.<br>2. **At 16:00, S2 faces a 400 kW DSO cut**: Sentinel's lookahead MILP pre-charged 1,102 kWh during cheap hours, completely saving 13 trucks from missed departures.<br>3. **At 18:00, spot prices explode to 799.30 €/MWh**: Sentinel elastically pauses non-critical charging, slashing energy cost by 38.6%.<br>4. **At S3, a 2-hour cellular outage strikes**: The edge gateway continues running autonomously on cached Day-Ahead schedules." | Click **[Run Friday 13.11 Scenario Day Simulation]**:<br>Live charts update across all 5 sites showing thermal trip mitigation, pre-charge buffer, spot price peak shaving, and zero missed departures. |
| **01:20 - 01:45** | **The Mathematical & Electrical Rigor** | "Behind this UI is hardened physics: an AC inverter loss guard ($P_{\text{AC}} = P_{\text{DC}} / 0.955$) that protects grid breakers, 6-step zero-arc contactor sequencing verified at 0 Amperes, and a HiGHS MILP optimizer with strict dimensional scaling." | Show System Health Dashboard: 126/126 deterministic pytest suite passed in 1.1s, 0 grid breaker trips, 0 missed departures. |
| **01:45 - 02:00** | **Commercial Closure & 2029 Vision** | "For a fleet operator like Lahti City Transit, the 32,400 € dual-gun retrofit pays for itself in just **1.89 months**. Backed by our One-Page SLA with Minimum Required Dwell Time anti-fraud protection, Sentinel transforms Kempower from an equipment vendor into an autonomous Charging-as-a-Service powerhouse." | Display 2029 CaaS Commercial Card: Payback 1.89 months, 99.5% SLA, MRDT formula, QR code linking to GitHub repo. |

---

## 2. Emergency Backup & Failsafe Triad

1. **Local Offline Execution**: The entire pipeline runs locally against local CSV data in offline mode. No venue Wi-Fi required.
2. **Deterministic Pre-computed Cache**: If the live solver needs fast display on stage, click `[Use Precomputed Replay]` to display verified simulation results in 100 milliseconds.
3. **Standby Video**: Backup 60-second screen capture (`demo_video_60s.mp4`) prepared in `media/`.
