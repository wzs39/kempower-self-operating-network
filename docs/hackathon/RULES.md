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

2. **Rule 2 — Strict Hardware Cost Accounting**:
   - *"New batteries or chargers? Price them: equipment_costs.csv."*
   - Any added asset must be accounted for in the financial model:
     - BESS Energy Capacity: 320 €/kWh
     - BESS Power Electronics: 110 €/kW
     - Power Cabinet 360 kW: 280 €/kW
     - Satellite Charger Post: 18,500 €/unit
     - Dual-Gun Retrofit Upgrade: 18,000 € equipment + 9,000 € installation per post.

3. **Rule 3 — Zero Human Intervention on Scenario Day**:
   - The network must autonomously navigate Friday 2026-11-13 from 00:00 to 24:00 with 0 human touches.
   - All events must be resolved programmatically:
     - 799.30 €/MWh spot price spike (17:15–18:45);
     - S1 C1-3 thermal overtemperature fault (F015 / F016);
     - S2 DSO 400 kW power curtailment (G1, 16:00–20:00);
     - S3 2-hour cellular outage (10:00–12:00);
     - S5 commissioning configuration errors (D5-7 power throttled, D5-8 inactive eSIM).

4. **Rule 4 — Deliverables Package**:
   - 10-minute presentation pitch (anchored around a 2029 customer story);
   - Live working prototype or deterministic replay on the dataset;
   - One-page Service Level Agreement (SLA) contract document;
   - Public GitHub repository with clean reproducibility instructions.

---

## 2. Infrastructure & Execution Environment

- **Runtime**: Python 3.13 + NumPy, Pandas, SciPy (HiGHS MILP solver) + Streamlit UI.
- **Offline Autonomy**: Zero external cloud API dependencies. The system operates fully self-contained using local SQLite WAL storage and edge-cached Day-Ahead electricity prices.
- **Verification Gate**: Full test suite (`pytest tests/`) must pass 100% with sub-2-second total execution time.
