# Official Judging Criteria & Alignment · Kempower Challenge 2026

**Challenge**: *The Self-Operating Charging Network*  
**Host**: Kempower & LahtiES (Lahti Energy Tech Hackathon 2026, LUT University)  
**Reference Document**: `Kempower-challenge-brief.pdf` (Pages 2–3) & Kickoff Keynote Slide 17  

---

## 1. Official Five-Dimensional Scoring Rubric

| Criteria | Weight | Hackathon Focus | Sentinel Alignment & Defense Evidence |
|---|---|---|---|
| **Degree of Autonomy** | **25%** | How completely does the system eliminate human intervention? Does it handle edge cases and degraded states gracefully? | • Eliminates **20.76 FTE $\approx$ 21 FTE** baseline (€1,365,000/yr saved across 8,852 biweekly operations).<br>• Zero-touch night bus charging (5,596 replugs $\to$ 0) via Dual-Gun time-sharing.<br>• Millisecond-level Edge FSM self-healing across thermal trip, offline islanding, and auto-commissioning. |
| **Energy & Grid Impact** | **20%** | Peak shaving, grid constraint respect, inverter efficiency, spot price reaction, DSO curtailment handling. | • Strict AC-to-DC $\eta = 0.955$ inverter constraint ($P_{\text{AC}} = P_{\text{DC}} / 0.955 \le P_{\text{grid}}$) preventing transformer overcurrent.<br>• 799.30 €/MWh peak avoidance via lookahead pre-charging and low-priority fleet pause (0 BESS required).<br>• S2 400 kW DSO curtailment lookahead pre-charging (1,102.10 kWh pre-charged, 13 missed departures eliminated). |
| **Technical Credibility** | **20%** | Mathematical rigor, electrical and physical feasibility, realistic contactor switching, compliance with official data. | • Kempower 25 kW modular rectifier physics with continuous CC/CV taper relaxation.<br>• 6-step zero-arc break-before-make sequence (260 ms < 500 ms threshold) with zero current verified before open.<br>• Safe N-1 thermal degradation (rejects illegal contactor back-feeding to tripped cabinets).<br>• HiGHS MILP optimizer with $10^{-3}$ spot price dimension scaling factor. |
| **Commercial Viability** | **20%** | Realistic CAPEX/OPEX, payback period, CaaS business model, enforceable SLA contract. | • Transparent hardware CAPEX: 12 Dual-gun satellites retrofit at S1 = 32.4k €; payback period < 1.89 months against 9.95 FTE night jockeying.<br>• Outcome-based Charging-as-a-Service (CaaS) with One-Page SLA.<br>• Minimum Required Dwell Time (MRDT) formula and 150% monthly liability cap protecting against frivolous claims. |
| **Clarity** | **15%** | 10-min pitch structure, 2-min live scenario replay, clear 2029 customer narrative. | • 10-minute pitch anchored in a 2029 Lahti City Transit customer story.<br>• 2-minute scenario day (Friday 13.11) deterministic replay covering S1-S5 crisis matrix.<br>• Clean 4-quadrant Streamlit UI with real-time DPR modular grid view. |

---

## 2. Competitive Edge & Falsification Hardening

1. **No Ghost Hardware**: S1–S5 baseline has 0 kWh BESS in `network_sites.csv`. Our primary peak-shaving relies entirely on load shifting and intelligent pre-charging; any optional BESS retrofit is explicitly costed at 320 €/kWh & 110 €/kW per `equipment_costs.csv`.
2. **Realistic Labor Displacement**: We truthfully acknowledge that replug jockeying constitutes 9.95 FTE (47.93% of labor), and demonstrate how the remaining 10.81 FTE is systematically eliminated via Edge FSM self-healing and automated ticket triage.
3. **Deterministic Verification**: All 126 unit and end-to-end assertions in `tests/` execute deterministically within 1.5 seconds, providing indisputable empirical evidence for the judging panel.
