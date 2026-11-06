# Live Demo Script (120 Seconds) · Project Sentinel

**Challenge**: *The Self-Operating Charging Network*  
**Theme**: Friday 13.11 Scenario Day Autonomy & 20.76 FTE Human Baseline Elimination  
**Target Audience**: Kempower Jury, Technical Mentors, CPO Executives  

---

## 1. Timeline & Spoken Narrative

| Time | Phase | Spoken Narrative | Visual Action |
|---|---|---|---|
| **00:00 - 00:20** | **The Hook: The 21 FTE Crisis** | "Over a single two-week period, Kempower's 100-site charging network required 8,852 manual human interventions—costing 93,412 staff-minutes. At 45 euros per hour under Finnish labor law, that is **20.76 full-time employees** costing **1.82 million euros a year**—with 47.93% of labor duration spent walking through dark depots to unplug and replug buses at midnight. If humans are no longer allowed to babysit chargers, how does the network operate itself?" | Display `operations_log.csv` analysis card: 20.76 FTE baseline (`1,821,534 €/yr`), 5,596 replugs (`63.22%` count / `47.93%` duration = `9.95 FTE` = `872,976 €/yr`). |
| **00:20 - 00:45** | **The Architecture: Intra-Cabinet DPR & Three-Tier S1 Strategy** | "Meet **Project Sentinel**. Built directly on Kempower's 25 kW modular Dynamic Power Routing architecture with strict 1:N cabinet-to-dispenser physical wiring (`cross_tie=False`). For S1's 24 overnight buses on 12 single-gun posts, Sentinel offers **Tier 2**—a **0 € CAPEX** software urgency scheduler with 0 human moves that rescues `B20` (`4 -> 3` missed) and closes **87.8% of the energy gap** (`398.5 -> 48.8 kWh`). On **Tier 3**, one thing we want to say plainly: **buying 12 more dispensers does not get you to zero — it gets you to eight**, because cabinet power stays at 1,080 kW and every gun drops from 90 to 45 kW. Zero is reachable only by adding a cross-cabinet busbar tie, which isn't in `chargers.csv` and has no price in your cost list. So that number we hand back to you." | Switch to Streamlit UI (`app.py`): Show DPR Matrix visualizer with 25 kW intra-cabinet module routing and the Tier 2 (`0 €`, `3` missed) vs Tier 3 (plugs alone `8` missed) vs busbar-tie (`0` missed, `1,080 kW`, unpriced) comparison. |
| **00:45 - 01:20** | **Live Crisis Playback: Friday 13.11** | "Now let's stress-test Friday the 13th across S1–S5 with zero humans:<br>1. **At S1**: Sentinel detects Cabinet C1-3 fan degradation **199 minutes before F015** (`59.3°C / 702 rpm` at `22:31` on Nov 12), dispatches a technician for F016 (`246 min`, `cleared_by=technician`), and runs 720 kW N-1 on C1-1/C1-2 with 0 kW self-harm.<br>2. **At S2**: Facing a 400 kW DSO cut at 16:00, Sentinel preempts overnight trucks `T05–T08`, eliminating all 4 missed truck departures (`283.50 kWh` deficit).<br>3. **At S3**: During a 2-hour cellular outage, the edge gateway overrides the 50 kW fallback to maintain 1,425 kW DC (`1,492.15 kW AC`), cutting abandonment from 29.69% (14d baseline 14.36%) to < 0.5%.<br>4. **At S5**: Three-way config reconciler unlocks `grid_limit_kw` from 600 to 900 kW (`+750 kWh > 508.95 kWh` deficit), unthrottles D5-7 to 150 kW, and activates D5-8's eSIM (`5 -> 0` missed)." | Click through Quadrant 2 (`Scenario Day 2026-11-13 Replay`) in `app.py`, showing S1–S5 baseline vs Sentinel results (`13` missed $\to$ `3` [`0 €`] / `0` [`324k €`]). |
| **01:20 - 01:45** | **The Mathematical & Electrical Rigor** | "Behind this UI is hardened physics: an AC inverter loss guard ($P_{\text{AC}} = P_{\text{DC}} / 0.955$), 6-step zero-arc contactor sequencing (`260 ms < 500 ms`), and a HiGHS MILP optimizer with continuous SoC slack (`z_v in [0, 1]`) so feasible vehicles are never abandoned during the 799.30 €/MWh price spike." | Show test verification: `433 pytest + 106 E2E (539 total)` assertions passed, `verify_all.py` in `< 0.5s`. |
| **01:45 - 02:00** | **Commercial Closure & 2029 Vision** | "Backed by our One-Page SLA with Minimum Required Dwell Time anti-fraud protection and a 150% liability cap, Sentinel transforms Kempower from an equipment vendor into an autonomous Charging-as-a-Service powerhouse." | Display Quadrant 4 (`2029 Commercial & One-Page SLA`): Tier 2 (`0 €` CAPEX, immediate), the plug-only Tier 3 trade-off (`324,000 €` → `8` missed), the busbar-tie path (`0` missed, unpriced), 99.5% SLA, MRDT interactive calculator. |

---

## 2. Emergency Backup & Failsafe Triad

1. **Local Offline Execution**: The entire pipeline runs locally against the 45 official CSV files in offline mode. No venue Wi-Fi required.
2. **Deterministic Sub-Second Verifier**: Run `python verify_all.py` on stage to verify all S1–S5 scenario checks in `< 0.5s`.
3. **Interactive 4-Quadrant Dashboard**: Launch `streamlit run app.py` for live parameter inspection across all 4 quadrants.
