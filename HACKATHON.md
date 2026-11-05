# Project Sentinel · Kempower Self-Operating Charging Network Command Center

> **Track**: Kempower Challenge — *The Self-Operating Charging Network* (LahtiES Energy Tech Hackathon 2026)

## Core Verification Commands (< 5 Seconds)
1. **Deterministic End-to-End Verifier (`0.22s`)**:
   ```bash
   python verify_all.py
   ```
2. **Full Pytest Suite (`179 passed`, including all 29 GitHub Issue #2 items `A1–D5`)**:
   ```bash
   pytest tests/ -v
   ```
3. **Interactive 4-Quadrant Streamlit Dashboard**:
   ```bash
   streamlit run app.py
   ```

## Ground-Truth Empirical Summary (45 CSVs, 240,635 Rows)
- **Scenario Day (`2026-11-13`) Missed Departures**: **`13 -> 0`** (`1,804.45 kWh` deficit eliminated: S1 `4 -> 0` [`1,012.00 kWh`], S2 `4 -> 0` [`283.50 kWh`], S5 `5 -> 0` [`508.95 kWh`]).
- **100-Site Network Manual Labor (`operations_log.csv` + `equipment_costs.csv`)**: `8,852` ops / `93,412` min biweekly = **`20.76 FTE`** (`€1,821,534/yr` at official `45 €/h = €87,750/FTE·yr`). `move_and_replug_vehicle` = `5,596` ops (`63.22%` count) / `44,768` min (**`47.93%` work time = `9.95 FTE = €872,976/yr`**; S1 = `2.79% = €24,336/yr`).
- **Grid Safety Invariant (`network_site_power.csv`)**: `0` over-limit intervals across all `134,400` rows (`P_AC = P_DC / 0.955 <= P_grid_limit`).

## Documentation Index
- [BRIEF.md](docs/hackathon/BRIEF.md): Problem statement, target users, and empirical baseline.
- [RULES.md](docs/hackathon/RULES.md): Official dataset physics vs modeling assumptions.
- [JUDGING.md](docs/hackathon/JUDGING.md): Evaluation criteria mapped to verifiable code modules.
- [BUILD_PLAN.md](docs/hackathon/BUILD_PLAN.md): Delivered architecture and module checklist.
- [DEMO_SCRIPT.md](docs/hackathon/DEMO_SCRIPT.md): 2-minute live demonstration script.
- [SUBMISSION.md](docs/hackathon/SUBMISSION.md): Submission summary and verification checklist.
- [DECISIONS.md](docs/hackathon/DECISIONS.md): Engineering trade-off and audit resolution log.
