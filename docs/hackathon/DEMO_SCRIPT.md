# Live Demo Script (120 Seconds) · Project Sentinel

**Challenge**: *The Self-Operating Charging Network*  
**Theme**: Friday 13.11 Scenario Day Autonomy & 20.76 FTE Human Baseline Elimination  
**Target Audience**: Kempower Jury, Technical Mentors, CPO Executives  

---

## 1. Timeline & Spoken Narrative

| Time | Phase | Spoken Narrative | Visual Action |
|---|---|---|---|
| **00:00 - 00:20** | **The Hook: The 21 FTE Crisis** | "Over a single two-week period, Kempower's 100-site charging network required 8,852 manual human interventions—costing 93,412 staff-minutes. At 45 euros per hour under Finnish labor law, that is **20.76 full-time employees** costing **1.82 million euros a year**—with 47.93% of labor duration spent walking through dark depots to unplug and replug buses at midnight. If humans are no longer allowed to babysit chargers, how does the network operate itself?" | Display `operations_log.csv` analysis card: 20.76 FTE baseline (`1,821,534 €/yr`), 5,596 replugs (`63.22%` count / `47.93%` duration = `9.95 FTE` = `872,976 €/yr`). |
| **00:20 - 00:45** | **The Architecture: Intra-Cabinet DPR & Dual Strategy** | "Meet **Project Sentinel**. Built directly on Kempower's 25 kW modular Dynamic Power Routing architecture with strict 1:N cabinet-to-dispenser physical wiring. For S1's 24 buses on 12 posts, Sentinel offers Strategy A—a **0 € CAPEX** software-coordinated single batch swap at 01:30 solving the 1,012 kWh deficit immediately—and Strategy B, a full 24-gun hardware expansion (`27,000 €/gun`, `324,000 €` CAPEX) for 2029 zero-touch operations." | Switch to Streamlit UI (`app.py`): Show DPR Matrix visualizer with 25 kW intra-cabinet module routing and Strategy A vs Strategy B comparison. |
| **00:45 - 01:20** | **Live Crisis Playback: Friday 13.11** | "Now let's stress-test Friday the 13th across S1–S5 with zero humans:<br>1. **At S1**: Sentinel detects Cabinet C1-3 fan degradation **199 minutes before F015** (`59.3°C / 702 rpm` at `22:31` on Nov 12), dispatches a technician for F016 (`246 min`), and runs 720 kW N-1 on C1-1/C1-2 with 0 kW self-harm.<br>2. **At S2**: Facing a 400 kW DSO cut at 16:00, Sentinel pre-charges 1,102.1 kWh, eliminating all 4 missed truck departures (`283.50 kWh` deficit).<br>3. **At S3**: During a 2-hour cellular outage, the edge gateway overrides the 50 kW fallback to maintain 1,425 kW DC (`1,492.15 kW AC`), cutting abandonment from 29.69% (14d baseline 14.36%) to < 0.5%.<br>4. **At S5**: Three-way digital-twin reconciliation unlocks `grid_limit_kw` from 600 to 900 kW (`+750 kWh > 508.95 kWh` deficit), unthrottles D5-7 to 150 kW, and activates D5-8's eSIM." | Click through Quadrant 2 (`Scenario Day 2026-11-13 Replay`) in `app.py`, showing S1–S5 baseline vs Sentinel results (13 missed departures $\to$ 0). |
| **01:20 - 01:45** | **The Mathematical & Electrical Rigor** | "Behind this UI is hardened physics: an AC inverter loss guard ($P_{\text{AC}} = P_{\text{DC}} / 0.955$), 6-step zero-arc contactor sequencing (`260 ms < 500 ms`), and a HiGHS MILP optimizer with continuous SoC slack (`z_v in [0, 1]`) so feasible vehicles are never abandoned during the 799.30 €/MWh price spike." | Show Quadrant 4 (`29-Item Audit & Test Suite`): 179/179 deterministic pytest assertions passed, `verify_all.py` in `< 0.5s`. |
| **01:45 - 02:00** | **Commercial Closure & 2029 Vision** | "Backed by our One-Page SLA with Minimum Required Dwell Time anti-fraud protection and a 150% liability cap, Sentinel transforms Kempower from an equipment vendor into an autonomous Charging-as-a-Service powerhouse." | Display Quadrant 3 (`2029 Commercial & One-Page SLA`): Strategy A (`0 €` CAPEX) vs Strategy B (`324,000 €`), 99.5% SLA, MRDT interactive calculator. |

---

## 2. Emergency Backup & Failsafe Triad

1. **Local Offline Execution**: The entire pipeline runs locally against the 45 official CSV files in offline mode. No venue Wi-Fi required.
2. **Deterministic Sub-Second Verifier**: Run `python verify_all.py` on stage to verify all S1–S5 scenario checks in `< 0.5s`.
3. **Interactive 4-Quadrant Dashboard**: Launch `streamlit run app.py` for live parameter inspection across all 4 quadrants.
