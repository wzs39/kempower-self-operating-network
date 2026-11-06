# Project Sentinel · Kempower Self-Operating Charging Network Command Center

> **Track**: Kempower Challenge — *The Self-Operating Charging Network* (LahtiES Energy Tech Hackathon 2026)  
> **Design Perspective**: Stated per the brief's first actor — the **equipment supplier / service provider** (`contracts.csv`), the party holding the hardware+service contracts and carrying departure penalties, transitioning to autonomous Energy Certainty-as-a-Service (CaaS).

## Core Verification Commands (< 5 Seconds)
1. **Deterministic End-to-End Verifier** (timed section `0.36-0.39 s` warm / `0.49 s` cold; wall clock `1.5-1.8 s`):
   ```bash
   python verify_all.py
   ```
2. **Full Automated Test Suite (`434 pytest + 106 E2E (540 total)`, including all 29 GitHub Issue #2 items `A1–D5`)**:
   ```bash
   python -m pytest tests/ -q
   python -m e2e_tests.test_runner
   ```
3. **Interactive 4-Quadrant Streamlit Dashboard**:
   ```bash
   streamlit run app.py
   ```

## Ground-Truth Empirical Summary (45 CSVs, 240,635 Rows across 100 Sites = 95 Network + 5 Detailed)
- **Scenario Day (`2026-11-13`) 3-Tier Missed Departures**:
  - **Tier 1 (Official Baseline)**: **`13` missed** (`S1=4, S2=4, S5=5`).
  - **Tier 2 (`0 €` CAPEX Software Urgency, 0 human moves)**: **`3` missed (`10` saved)** — S1 `4 -> 3` (`B20` saved, same-engine deficit `398.5 -> 48.8 kWh` [`-87.8%`]; official 0-session gap `1,012.00 kWh`), S2 `4 -> 0` (`283.50 kWh` saved), S5 `5 -> 0` (`508.95 kWh` saved).
  - **Tier 3 (`324,000 €` S1 Dual-Gun Hardware Expansion, 0 human moves)**: **`0` missed at S1 (`4 -> 0`) — but only together with a cross-cabinet busbar tie.** 12 dual-gun dispensers (`24` plugs @ `27,000 €/gun`, `13.31-yr` standalone payback) give 24 plug points; **the plugs alone are worse, not better** (`8` missed, `1,040.1 kWh`), because cabinet power stays `1,080 kW` and each gun drops `90 -> 45 kW`. `0` requires adding `cross_tie=True`, which is **not in `chargers.csv` and has no price in `equipment_costs.csv`** — so the `324,000 €` figure is a lower bound on hardware, not the price of zero.
- **100-Site Network Manual Labor (`operations_log.csv` + `equipment_costs.csv`)**: `8,852` ops / `93,412` min biweekly = **`20.76 FTE`** (`€1,821,534/yr` at official `45 €/h = €87,750/FTE·yr`). `move_and_replug_vehicle` = `5,596` ops (`63.22%` count) / `44,768` min (**`47.93%` work time = `9.95 FTE = €872,976/yr`**; S1 = `2.79% = €24,336/yr`), while retaining physical technician replacement (`cleared_by = technician`) for hardware trips (`F016`).
- **Grid Safety Invariant (`network_site_power.csv` & `network_kpis.csv`)**: `0` official `grid_kw` over-limit intervals across all `134,400` rows (`9,644` rows under `delivered_kw / 0.955` AC basis reconciled; `2,096.1 hours` over grid limit across `72` network sites in `network_kpis.csv`; see [energy_impact.md](docs/energy_impact.md)).

## Documentation Index
- [energy_impact.md](docs/energy_impact.md): Station-by-station energy cost, peak shaving, `network_kpis.csv` 95-site proof, and gun-hour / cabinet-hour utilization ledger.
- [BRIEF.md](docs/hackathon/BRIEF.md): Problem statement, target users, and empirical baseline.
- [RULES.md](docs/hackathon/RULES.md): Official dataset physics vs modeling assumptions.
- [JUDGING.md](docs/hackathon/JUDGING.md): Evaluation criteria mapped to verifiable code modules.
- [BUILD_PLAN.md](docs/hackathon/BUILD_PLAN.md): Delivered architecture and module checklist.
- [DEMO_SCRIPT.md](docs/hackathon/DEMO_SCRIPT.md): 2-minute live demonstration script.
- [SUBMISSION.md](docs/hackathon/SUBMISSION.md): Submission summary and verification checklist.
- [DECISIONS.md](docs/hackathon/DECISIONS.md): Engineering trade-off and audit resolution log.
