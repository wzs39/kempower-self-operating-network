# Competition Rules & Ground Truth Constraints · Kempower Challenge 2026

**Challenge**: *The Self-Operating Charging Network*  
**Host**: Kempower & LahtiES (Lahti Energy Tech Hackathon 2026, LUT University)  
**Submission Deadline**: Saturday 2026-11-07 12:00 EET  
**Official Rule Set**: Keynote Slide 17 by Mats Mattsson (Head of Cloud Software, Kempower)  

---

## 1. Confirmed Competition Constraints & Red Lines

1. **Rule 1 — Absolute Data Immutability**:
   - *"Never change the data we gave. Baseline and scenario day are the same for every team."*
   - Official dataset consists of 45 CSV files (240,635 rows) in `kempower-challenge-data/`.
   - Modifying row entries, timestamps, or site parameters in the official data directory is strictly prohibited.

2. **Rule 2 — Strict Hardware Cost Accounting (`equipment_costs.csv`)**:
   - *"New batteries or chargers? Price them: equipment_costs.csv."*
   - Any added asset must be accounted for in the financial model:
     - BESS Energy Capacity (`bess_energy`): `320 €/kWh`
     - BESS Power Electronics (`bess_power`): `110 €/kW`
     - Power Cabinet up to 360 kW: `280 €/kW`
     - Dispenser up to 400 kW (`dispenser_up_to_400kw`): `18,000 €/unit`
     - Civil Works per Dispenser (`civil_works`): `9,000 €/unit` (`27,000 €/gun` total installed cost; `324,000 €` for 12 guns)
     - Operations Staff (`operations_staff`): `45 €/h` (`87,750 €/FTE/yr` at 37.5 h/wk)
     - Technician Labour (`technician_labour`): `80 €/h`

3. **Rule 3 — Zero Human Intervention on Scenario Day**:
   - The network must autonomously navigate Friday 2026-11-13 from 00:00 to 24:00 with 0 human touches.
   - All events must be resolved programmatically:
     - `799.30 €/MWh` spot price spike (ramp from 17:15; only 17:45/18:00/18:15 exceed 600 €/MWh, peak 799.30 at 18:00);
     - S1 `C1-3` thermal overtemperature fault (`F015` at 01:50, predictable `199 min` earlier at `2026-11-12T22:31:00+02:00`; `F016` at 02:25 for `246 min`, `cleared_by = technician`);
     - S2 DSO `400 kW` power curtailment (`G1`, **16:00–19:00**, `4` missed trucks / `283.50 kWh` deficit);
     - S3 2-hour cellular outage (**11:00–13:00**, `29.69%` scenario-day abandonment vs `14.36%` 14-day baseline);
     - S5 three-way commissioning configuration errors (`grid_limit_kw: 600 -> 900 kW`, `D5-7` throttled to `50 kW`, `D5-8` inactive eSIM, `5` missed buses / `508.95 kWh` deficit).

4. **Rule 4 — Deliverables Package**:
   - 10-minute presentation pitch (anchored around a 2029 customer story);
   - Live working prototype (`app.py`) and deterministic verifier (`verify_all.py`) on the dataset;
   - One-page Service Level Agreement (SLA) contract document (`One_Page_SLA_Specification.md`);
   - Public GitHub repository with clean reproducibility instructions and zero hardcoded paths.

---

## 2. Infrastructure & Execution Environment

- **Runtime**: Python 3.10+ with NumPy, Pandas, SciPy (HiGHS MILP solver), Pytest, and Streamlit UI.
- **Offline Autonomy**: Zero external cloud API dependencies. The system operates fully self-contained using local SQLite WAL storage and edge-cached Day-Ahead electricity prices.
- **Verification Gate**: Full test suite (`434 pytest + 106 E2E (540 total)`) passes 100%, and `python verify_all.py` executes in `< 1 s`.
