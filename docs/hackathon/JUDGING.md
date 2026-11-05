# Official Judging Criteria & Alignment · Kempower Challenge 2026

**Challenge**: *The Self-Operating Charging Network*  
**Host**: Kempower & LahtiES (Lahti Energy Tech Hackathon 2026, LUT University)  
**Reference Document**: `Kempower-challenge-brief.pdf` (Pages 2–3) & Kickoff Keynote Slide 17  

---

## 1. Official Five-Dimensional Scoring Rubric

| Criteria | Weight | Hackathon Focus | Sentinel Alignment & Defense Evidence |
|---|---|---|---|
| **Degree of Autonomy** | **25%** | How completely does the system eliminate human intervention? Does it handle edge cases and degraded states gracefully? | • Eliminates **20.76 FTE $\approx$ 21 FTE** baseline (**1,821,534 €/yr** at `45 €/h = 87,750 €/FTE/yr` across 8,852 biweekly operations; **1,982,229 €/yr** with `80 €/h` technician rate).<br>• Zero-touch S1 scheduling (Strategy A: `0 €` CAPEX single `01:30` batch swap; Strategy B: 24-gun expansion).<br>• Millisecond-level Edge FSM self-healing across `199 min` early thermal detection, `720 kW` N-1 degradation, offline islanding, and 3-way S5 auto-commissioning (`600 -> 900 kW`). |
| **Energy & Grid Impact** | **20%** | Peak shaving, grid constraint respect, inverter efficiency, spot price reaction, DSO curtailment handling. | • Strict AC-to-DC $\eta = 0.955$ inverter constraint ($P_{\text{AC}} = P_{\text{DC}} / 0.955 \le P_{\text{grid}}$) preventing transformer overcurrent.<br>• `799.30 €/MWh` peak avoidance via lookahead pre-charging and continuous SoC slack (`z_v in [0, 1]`) with `0 kWh` BESS required.<br>• S2 `400 kW` DSO curtailment lookahead pre-charging (`1,102.10 kWh` pre-charged, eliminating 4 missed truck departures and `283.50 kWh` deficit). |
| **Technical Credibility** | **20%** | Mathematical rigor, electrical and physical feasibility, realistic contactor switching, compliance with official data. | • Kempower 25 kW modular rectifier physics with strict 1:N cabinet-to-dispenser topology (`power_cabinets.csv` & `chargers.csv`).<br>• 6-step zero-arc break-before-make sequence (`260 ms < 500 ms` threshold) with zero current verified before open.<br>• Safe N-1 thermal degradation (rejects illegal cross-cabinet contactor back-feeding to tripped `C1-3`).<br>• HiGHS MILP optimizer with $10^{-3}$ spot price scaling and full monthly peak demand rate (`6.50 / 7.50 €/kW/mo`). |
| **Commercial Viability** | **20%** | Realistic CAPEX/OPEX, payback period, CaaS business model, enforceable SLA contract. | • Transparent dual-strategy CAPEX: Strategy A (`0 €` CAPEX immediate payback) vs Strategy B (`18,000 + 9,000 = 27,000 €/gun` = `324,000 €` for 12 guns, `13.31-yr` standalone payback vs S1's `24,336 €/yr` replug labor).<br>• Outcome-based Charging-as-a-Service (CaaS) with One-Page SLA, MRDT anti-fraud formula, and 150% monthly liability cap. |
| **Clarity** | **15%** | 10-min pitch structure, 2-min live scenario replay, clear 2029 customer narrative. | • 10-minute pitch anchored in a 2029 Lahti City Transit customer story.<br>• 2-minute scenario day (Friday 13.11) deterministic replay covering S1–S5 crisis matrix.<br>• Clean 4-quadrant Streamlit UI (`app.py`) with real-time DPR modular grid view. |

---

## 2. Competitive Edge & Falsification Hardening

1. **No Ghost Hardware**: S1–S5 baseline has `0 kWh` BESS in `network_sites.csv`. Our primary peak-shaving relies entirely on load shifting and intelligent pre-charging; any optional BESS retrofit is explicitly costed at `320 €/kWh` & `110 €/kW` per `equipment_costs.csv` (`7.33-yr` payback with FCR-N/D).
2. **Realistic Labor Displacement**: We truthfully distinguish event count (**63.22%**, `5,596 / 8,852`) from labor duration (**47.93%**, `44,768 / 93,412 min` = `9.95 FTE` = `872,976 €/yr`), and demonstrate how the remaining `10.81 FTE` (`52.07%`) is systematically eliminated via Edge FSM self-healing and automated ticket triage.
3. **Deterministic Verification**: All **179** unit, empirical, and GitHub Issue #2 (`A1–D5`) assertions in `tests/` execute deterministically in ~2.1 seconds, and `verify_all.py` completes in `< 0.5s`.
