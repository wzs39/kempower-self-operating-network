# Autonomous Charging Network — One-Page Service Level Agreement & Operating Specification

**Autonomous Energy Certainty · Outcome-based Charging-as-a-Service (CaaS) · Project Sentinel**

Contract Form No: KEMP-AUTO-2029-SLA-V2 · Jurisdiction: Republic of Finland / EU Energy Law · Effective: January 1, 2029 · Parties: Kempower Autonomous Energy Services Oy (Service Provider) · Lahden Seudun Liikenne (Lahti City Transit) & European Logistics Depot Alliance (Client)

> Printable version: [`One_Page_SLA_Specification.pdf`](./One_Page_SLA_Specification.pdf) — verified to render as **exactly 1 A4 page**.
> Complete tier tables, the 2029 flagship customer story, every equation and the full boundary definitions live in the companion annex: [`SLA_Specification_Annex_Full.pdf`](./SLA_Specification_Annex_Full.pdf) (4 pages). This file is the markdown twin of the one-page PDF.

---

## 1 · What is promised — Guaranteed SLOs

| SLO | Gold target | Titanium tier upgrade · breach trigger |
|---|---|---|
| **SLO-1** Fleet on-time full-charge rate | ≥ 99.50 % | ≥ 99.90 % (≤ 3 missed trips/yr) · monthly on-time rate below target |
| **SLO-2** Dispenser fleet availability | ≥ 99.50 % | ≥ 99.90 % (≤ 43 min down/mo) · minute-level ΣT_avail/ΣT_total over 720 h |
| **SLO-3** Islanded operational resilience | ≥ 72 h | Full 1,425 kW local DLM · unplanned stall or grid-limit breach during WAN loss |
| **SLO-4** Grid-limit compliance | 100.0 % | Absolute — incl. 95.5 % rectifier buffer · any instantaneous transformer breach |
| **SLO-5** Self-healing control latency | ≤ 100 ms | ≤ 50 ms (<10 ms logic + BBM shift) · response latency > 200 ms |

Silver tier baselines: 99.00 % / 99.00 % (≤ 432 min) / 24 h / 100 % / ≤ 200 ms. **Carve-outs from the measurement window** (clock suspends, bar never lowers): unannounced medium-voltage outages or DSO hard curtailment at non-BESS sites, vehicle-side BMS faults, MRDT-short dwell, sabotage. Announced curtailment (e.g. G1) stays inside the promise.

## 2 · What the system decides — Autonomous authority

| Operational scenario | Algorithm direct authority | Mandatory human escalation |
|---|---|---|
| 1 · Dynamic power routing & virtual replugging | Full — reallocates 25 kW DPR blocks on departure countdown & SoC deficit | Human intervention prohibited |
| 2 · Spot-price spikes & grid curtailment (G1–G3) | Full — pre-charges flexible loads, derates low-urgency stalls (0.0 kW in G1) | Only a mandatory DSO grid cut-off order |
| 3 · Module thermal anomaly & hardware faults | Full — millisecond BBM isolation; N-1 power pooling sustains operation | Work order auto-logged; technician dispatched in day |
| 4 · Insulation / grounding breakdown (IMD) | Full — contactor trip, gun isolated, connector locked out | Field crew after 3 failed retries |
| 5 · Total WAN loss (network outage) | Full — local edge takes over, 1,500 kW local DLM | Telecom provider if outage > 72 h |
| 6 · Vehicle crash, fire, emergency stop | Full — master substation breaker opens within 10 ms | Mandatory on-site inspection & certified manual reset |

**Hard physical safety trips — firmware-locked, no software or cloud override:** cabinet ≥ 65 °C → linear derate + reverse fan pulse; ≥ 75 °C → hardware trip, master AC contactor opens ≤ 100 ms; connector pin ≥ 90 °C → DC disconnect ≤ 50 ms; insulation < 100 Ω/V → IMD fault, HV closure inhibited; residual DC ≥ 30 mA → RCD trip ≤ 40 ms (IEC 61851-23); P_grid > 1.00 × transformer limit → overload clamp on non-urgent modules ≤ 20 ms.

## 3 · What it costs — Fees, penalties & the physics gate

| 250 € | 5.00 €/min | 1.50 €/kWh | ≤ 150 % |
|---|---|---|---|
| base delayed-departure penalty (Ti 350 · Ag 150) | progressive delay after 15 min grace (7.50 / 3.00; 10 / 20 min) | missing-energy compensation (2.00 + rental / 1.00) | aggregate monthly liability cap of base fee |

**Fleet penalty (MRDT-compliant departures):**

```
Penalty = Σ_delayed [ P_base + max(0, t_delay − 15 min)·C_min ]
        + Σ_undercharged [ ΔSoC/100 · Cap_batt · C_energy ]
```

**Availability fee deduction:** 0 if ≥ 99.50 % · **2.0 % of monthly fee per 0.1 pp** shortfall (max 90 %) if 95.00–99.50 % · **100 % waiver** if < 95.00 % (service default trip).

**MRDT physics gate (moral-hazard shield):** before any credit is paid, the minimum physically required dwell time is computed per departure:

```
MRDT_j = ( ΔSoC_j/100 · Cap_batt,j ) ÷ ( min(P_charger_max, P_vehicle_max,j) · η_system=0.95 ) × 60 + T_buffer=15 min
```

Liquidated damages apply **if and only if** actual dwell ≥ MRDT_j. A late-arriving vehicle (dwell < MRDT) is charged best-effort and the provider is fully indemnified — the gate that kills the "arrived 10 min late with 200 kWh to go" claim.

**Caps & billing integrity:** fleet penalties per depot ≤ 100 % of its monthly fee; aggregate monthly payout ≤ **150 %** of base fee; invoices strictly non-negative (Net Payable = max(0, Fee − Credits), excess credits roll over); no indirect or consequential damages.

## 4 · Who is accountable when it decides wrong

**Black-box evidence, no disputes:** (1) edge gateway records voltage, current, pin temperature, fan RPM, CAN/BMS frames at **1-second resolution** on NVMe with **72 h** power-loss WAL; (2) telemetry streams emit periodic **SHA-256 Merkle** root hashes anchored to cloud ledgers in real time or ≤ 15 min after WAN restoration; (3) after any anomaly, the offline discrete-event simulator performs automated root-cause attribution within **15 minutes** of reconnection and verified liquidated damages are **auto-credited on the next invoice**.

**Provider is relieved of liability** only upon objective black-box proof of: utility blackout / unannounced DSO curtailment (BESS sites beyond the 2 h design buffer; non-BESS sites S1–S3, S5 fully indemnified from the moment of occurrence, hours excluded from SLO-1/2); vehicle BMS non-compliance or internal battery faults (ISO 15118 diagnostic dumps); client MRDT non-compliance; external mechanical sabotage or impact.

**Kept human by design:** the system never overrides a firmware safety interlock; hardware faults that need hands (73 dispatches = 5.09 FTE) are retained as costed technician service inside the fee — software does not turn wrenches, and the zero-miss busbar path that is absent from the official price list is handed back unpriced rather than invented.

## 5 · Execution & verification seal

| Party A — Service Provider | Party B — Contracted Client |
|---|---|
| Kempower Autonomous Energy Services Oy — Signatory: Kempower System Chief Architect | Lahden Seudun Liikenne (Lahti City Transit) & European Logistics Depot Alliance — Signatory: Pekka Virtanen, Fleet Operations Director |

Execution date: January 1, 2029 · Smart-contract root hash: `0x8F9C4A12E8B907D3E2F4A5C6718293A4B5C6D7E8F90123456789ABCDEF012345` · Verification gateway: https://sentinel.kempower.com/verify/contract/2029-LSL-DEPOT-01

---

*Complete contractual summary. Full tier tables, derivations, 2029 customer story & equations: `SLA_Specification_Annex_Full.pdf` · Every figure traces to the unmodified official dataset (45 CSVs / 240,635 rows), re-verified by `verify_all.py`.*
