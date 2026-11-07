# SLA Specification Annex — Full Reference

**Companion to the One-Page Service Level Agreement & Operating Specification · Autonomous Energy Certainty · Project Sentinel**

Contract Form No: KEMP-AUTO-2029-SLA-V2 · Jurisdiction: Republic of Finland / EU Energy Law · Effective: January 1, 2029 · Printable version: [`SLA_Specification_Annex_Full.pdf`](./SLA_Specification_Annex_Full.pdf) (4 pages). This annex carries the complete tier tables, the 2029 flagship customer story, every equation and the full boundary definitions behind the one-page agreement. All figures trace to the unmodified official dataset (45 CSVs / 240,635 rows), re-verified by `verify_all.py`.

---

## A · 2029 Flagship Customer Story — The Zero-Touch Blizzard Rollout in Lahti

### A Sub-Zero Winter Night with Pekka Virtanen (Lahti City Transit / Lahden Seudun Liikenne, LSL)

**Context & profile.** Pekka Virtanen is the Director of Fleet Operations for Lahti City Transit (Lahden Seudun Liikenne, LSL). In 2026, Pekka's worst operational nightmare was winter staffing and depot dispatch. In sub-zero Finnish winters (−18 °C), deep snowdrifts required 3 to 4 yard attendants every night to drag heavy 400 A liquid-cooled charging cables back and forth across 24 articulated electric transit buses (`move_and_replug_vehicle`). If an attendant fell ill or a connector pin iced over, morning rush hour at 06:00 would see 4 to 5 key bus routes cancelled due to stranded, undercharged vehicles — resulting in tens of thousands of euros in municipal delay penalties and hundreds of freezing passengers stranded at transit stops.

**Friday, January 19, 2029 · Lahti North Bus Depot (Depot S1) · Temperature: −18 °C · Blizzard.**

**1. 22:00 — Zero-touch arrival & silent cryptographic authorization.** All 24 articulated 18-meter electric buses return to depot S1 at the end of their evening shifts. Drivers pull into their assigned stalls and plug in the dual-satellite CCS2 cables. Leveraging the **ISO 15118-20 Plug & Charge (PnC)** protocol, the depot edge controller and onboard Vehicle SECC complete bidirectional TLS 1.3 cryptographic mutual authentication based on ECDSA P-256 digital certificates within **1.1 seconds**. Drivers lock their cabs and head home. The depot yard is completely empty of human personnel.

**2. 02:15 — Sub-zero preconditioning & dynamic power routing.** Ambient temperature plunges to −18 °C, chilling LFP battery cells below their optimal charge-acceptance threshold. Sentinel's Edge Self-Healing Controller detects low cell-temperature telemetry via high-speed CAN bus and instructs the modular 25 kW DPR matrix to dynamically allocate 50 kW to each vehicle's onboard PTC thermal preconditioning circuit. Within **18 minutes**, core cell temperatures reach their optimal 15 °C charging window. Fleet charging efficiency surges by 35 %, avoiding the cold-weather charging drag that historically delayed morning departures.

**3. 03:40 — Millisecond Break-Before-Make (BBM) isolation & N-1 power re-pooling.** Edge telemetry diagnostics detect abnormal fan RPM and an incipient thermal-runaway curve on cabinet C1-3 (a dual-threshold thermal model predicted the degradation 199 minutes prior, autonomously scheduling daytime technician servicing: `cleared_by = technician`). The depot's millisecond BBM relay sequencing (software logic < 10 ms, physical relay transition 85 ms) safely isolates the degraded rectifier channel. Healthy cabinets C1-1 and C1-2 pool their remaining 720 kW capacity across the 24 dual-satellite connection points (backed by the Titanium Tier hardware architecture), silently sustaining charging without dropping a single bus.

**4. 05:30 — 100 % on-time full-charge departure & the morning coffee.** At 05:30, all 24 electric transit buses display solid green SoC indicators (100.0 % required energy delivered). Morning-shift drivers board pre-warmed cabs, turn on the auxiliary power, and roll out through the snowy depot gates on schedule. Pekka Virtanen wakes up in his downtown Lahti apartment, sips his morning coffee, and glances at a silent notification on his smartphone:

> *"Lahti North Depot (S1): 24/24 scheduled departures completed with 100.0 % required energy delivered. Overnight human interventions: 0. Autonomous self-healing events resolved: 1 sub-zero thermal preconditioning, 1 cabinet N-1 dynamic derate. Monthly SLA fulfilment: 99.98 % (Titanium Green Compliant)."*

**This is commercial charging in 2029:** charging is no longer a labor-intensive maintenance burden, but an outcome-based energy-certainty service (Charging-as-a-Service, CaaS).

---

## B · Preamble & legal binding

This Autonomous Charging Network Service Level Agreement ("SLA") is entered into in Lahti, Finland, by and between: **1. Autonomous Operator / Service Provider:** Kempower Autonomous Energy Services Oy (transitioning from pure hardware manufacturing to an outcome-based Energy-Certainty-as-a-Service provider, operating modular DPR matrices, edge microgrid gateways and autonomous dispatch algorithms); **2. Contracted Client:** commercial transit authority (e.g., Lahti City Transit / LSL), long-haul electric freight logistics fleet, or high-throughput public charging hub operator (collectively, the "Client").

**Core subject matter.** The Client entrusts the operational management and dispatch of charging infrastructure to the Autonomous Control Central Core. Both parties agree that continuous human dispatch and manual operations are eliminated, replaced by an **autonomous, outcome-based energy-delivery architecture**.

---

## C · Three-tier commercial service levels

| Commercial dimension | Titanium Tier (core transit / freight) | Gold Tier (standard commercial / public) | Silver Tier (auxiliary fleet / destination) |
|---|---|---|---|
| Primary use cases | Urban transit depots (S1/S5), zero-tolerance freight corridors (S2) | High-throughput public hubs (S3/S4), regional logistics depots | Corporate campuses, secondary overnight passenger-car parking |
| On-time full-charge SLO (SLO-1) | ≥ 99.90 % (≤ 3 missed trips/year) | ≥ 99.50 % (standard industrial guarantee) | ≥ 99.00 % (commercial baseline) |
| Dispenser service availability (SLO-2) | ≥ 99.90 % (≤ 43 min downtime/month) | ≥ 99.50 % (≤ 216 min downtime/month) | ≥ 99.00 % (≤ 432 min downtime/month) |
| Self-healing control latency (SLO-5) | ≤ 50 ms (< 10 ms logic + BBM matrix shift) | ≤ 100 ms (hardware-grade relay switch) | ≤ 200 ms (standard contactor cycle) |
| Islanded autonomous runtime (SLO-3) | ≥ 72 h (full 1,425 kW local DLM) | ≥ 48 h (transformer-limit management) | ≥ 24 h (basic static split) |
| Overnight replugging guarantee | **0 human labor** (24 dual-satellite expansion €324,000 + cross-tie / 0 deficit; plug-only yields 8 missed) | **0 human labor** (€0 pure-software urgency waterfilling; S1 deficit cut by 87.8 %) | Best-effort automated replug driver notifications |
| Base trip delay penalty (P_base) | 350.00 € / departure | 250.00 € / departure | 150.00 € / departure |
| Progressive delay penalty (C_min) | 7.50 € / min (after 10 min grace) | 5.00 € / min (after 15 min grace) | 3.00 € / min (after 20 min grace) |
| Missing-energy compensation (C_energy) | 2.00 € / kWh + rental-bus reimbursement | 1.50 € / kWh | 1.00 € / kWh |
| Base management-fee multiplier | 1.25 × base tariff | 1.00 × base tariff (standard baseline) | 0.80 × base tariff |

---

## D · Guaranteed service level objectives (SLOs)

The Service Provider guarantees the following measurable SLOs during each billing period (Gold Tier baseline, upgraded under Titanium Tier):

| SLO | Metric | Gold target | Evaluation window & scope | Breach condition |
|---|---|---|---|---|
| SLO-1 | Fleet on-time full-charge rate | ≥ 99.50 % | Evaluated per scheduled departure; requires actual departure SoC ≥ SoC_required and delay ≤ 0 min, subject to MRDT compliance | Monthly on-time rate drops below 99.50 % |
| SLO-2 | Dispenser fleet availability | ≥ 99.50 % | Minute-level availability across 720 monthly hours: ΣT_available / ΣT_total × 100 % | Monthly fleet availability drops below 99.50 % |
| SLO-3 | Islanded operational resilience | ≥ 72 h | Commences upon WAN cellular/fiber loss; edge maintains 100 % rated-capacity dynamic load allocation | Unplanned stall shutdown or grid-limit breach during outage |
| SLO-4 | Grid-limit compliance rate | 100.0 % (absolute) | Second-level current telemetry: P_grid(t) ≤ P_limit(t), including the 95.5 % rectifier-efficiency buffer | Any instantaneous breach of transformer capacity |
| SLO-5 | Self-healing control latency | ≤ 100 ms | End-to-end latency from anomaly trigger to relay isolation and power reconfiguration | Dynamic response latency exceeds 200 ms |

---

## E · Explicit decision-boundaries matrix

To establish legal and technical certainty, the boundary between autonomous algorithmic authority and mandatory human intervention is strictly defined:

| Operational scenario | Algorithm direct authority | Mandatory human escalation |
|---|---|---|
| 1 · Dynamic power routing and virtual replugging | **Fully autonomous:** reallocates 25 kW DPR blocks based on departure countdown and SoC deficit | Human intervention prohibited (prevents load disruption) |
| 2 · Spot-price spikes and grid curtailment (G1–G3) | **Fully autonomous:** pre-charges flexible loads; derates low-urgency stalls (0.0 kW during G1) | Escalates only if the DSO issues a mandatory grid cut-off order |
| 3 · Module thermal anomaly & secondary hardware faults | **Fully autonomous:** millisecond BBM isolation; N-1 power pooling sustains operation | Automatically logs work order; technician dispatches in day |
| 4 · Electrical insulation & grounding breakdown (IMD) | **Fully autonomous:** millisecond contactor trip; isolates gun and locks out connector | Escalates to field crew after 3 consecutive failed retries |
| 5 · Total WAN cellular/fiber loss (network outage) | **Fully autonomous:** local edge takes over 1,500 kW local dynamic load balancing (DLM) | Escalates to telecom provider if outage exceeds 72 hours |
| 6 · Physical vehicle crash, fire, or emergency stop | **Fully autonomous:** physical trip opens master substation breaker within 10 ms | Mandatory on-site inspection & certified manual breaker reset |

---

## F · Hard physical safety trip thresholds

Autonomous optimization algorithms are strictly subordinated to underlying electrical safety interlocks. The following thresholds are permanently locked in cabinet and dispenser MCU firmware and cannot be overridden by software or cloud commands:

| Trigger condition | Locked-in response |
|---|---|
| `T_cabinet_internal ≥ 65.0 °C` | Linear derate — 50 % load reduction, fault alarm, reverse fan pulse |
| `T_cabinet_internal ≥ 75.0 °C` | Hardware trip — forces open the master AC contactor within 100 ms |
| `T_connector_pin ≥ 90.0 °C` | DC disconnect — disconnects and locks the DC contactor within 50 ms |
| `R_insulation < 100 Ω/V` | IMD fault — immediate session termination; inhibits high-voltage closure |
| `I_residual_DC ≥ 30 mA` | RCD trip — disconnects the circuit within 40 ms per IEC 61851-23 |
| `P_site_grid > 1.00 × P_transformer_limit` | Overload clamp — clamps non-urgent DPR modules within 20 ms |

---

## G · Liquidated damages, moral-hazard gates & liability caps

### G.1 Minimum Required Dwell Time (MRDT) pre-condition & penalty equation

**Physical feasibility gate (MRDT).** To prevent moral hazard and predatory claims, fleet vehicles must respect the laws of physics regarding minimum charging dwell time. For each departure *j*, the system calculates the Minimum Required Dwell Time:

```
MRDT_j = ( (SoC_req,j − SoC_arrive,j)/100 × Cap_batt,j )
         ÷ ( min(P_charger_max, P_vehicle_max,j) · η_system ) × 60 + T_buffer   [minutes]
```

- System round-trip efficiency: `η_system = 0.95`.
- Safety-handshake, insulation-test and dynamic matrix-routing buffer: `T_buffer = 15.0 min`.
- **Liability activation:** liquidated damages for delayed or undercharged departures apply **if and only if** the actual on-site dwell time Δt_dwell,j = (t_depart_sched,j − t_arrive_actual,j) ≥ MRDT_j. If a vehicle arrives late (Δt_dwell,j < MRDT_j), the Service Provider is fully indemnified and provides best-effort charging only.

**Fleet penalty equation (Gold Tier baseline).** Subject to MRDT compliance, liquidated damages are calculated rigidly as follows:

```
Penalty_fleet = Σ_{i ∈ delayed_trips}   [ P_base + max(0, t_delay_min,i − 15) × C_min ]
              + Σ_{j ∈ undercharged}    [ max(0, SoC_req,j − SoC_dep,j)/100 × Cap_batt,j × C_energy ]
```

- **Base delay penalty (P_base): 250.00 € / departure** — triggers instantly upon delay t_delay > 0.
- **Progressive delay penalty (C_min): 5.00 € / minute** beyond the 15-minute grace window.
- **Missing-energy compensation (C_energy): 1.50 € / kWh** for unfulfilled energy deficits below target.

### G.2 Progressive monthly availability-fee deduction schedule

Monthly management-fee deductions follow a strict piecewise closed function:

```
Fee_deduction = 0,                                                          if Availability_actual ≥ 99.50 %
              = Monthly Base Fee × min( 90.0 %,
                    ⌈ (99.50 % − Availability_actual) / 0.10 % ⌉ × 2.0 % ),  if 95.00 % ≤ Availability_actual < 99.50 %
              = Monthly Base Fee × 100.0 %,                                  if Availability_actual < 95.00 %   (Service Default Trip)
```

- **Progressive deduction range (95.00 % ≤ Availability < 99.50 %):** for each 0.10 % decrement below the 99.50 % commitment, 2.0 % of the monthly fee is deducted (up to 90.0 %).
- **Service default trip (Availability < 95.00 %):** the entire monthly fee is waived (100.0 % deduction).

### G.3 Aggregate liability cap & non-negative billing guarantee

- **Fee-deduction ceiling:** Fee_deduction ≤ 100.0 % × Monthly Base Fee (fee waiver only; no negative management fees).
- **Monthly fleet liquidated-damages cap:** total fleet penalties (Σ Penalty_fleet) for a single depot in a calendar month cannot exceed **100.0 % of that depot's monthly service management fee**.
- **Aggregate liability ceiling & non-negative billing guarantee:** under no circumstances shall total monthly payouts exceed **150.0 % of the Monthly Base Fee**: Total Monthly Payout = Fee_deduction + Σ Penalty_fleet ≤ 1.50 × Monthly Base Fee. Generated monthly statements strictly satisfy Net Payable = max(0.0, Monthly Base Fee − Credits), with excess credits rolling over into next month's service vouchers, ensuring commercial balance-sheet solvency.
- **Consequential-damages carve-out:** the Service Provider's financial liability is strictly limited to the direct liquidated damages above. The Service Provider shall not be liable for indirect damages, lost commercial business revenue, or punitive claims.

---

## H · Force majeure & liability carve-outs

The Service Provider is relieved of penalty liability and availability penalties exclusively upon objective black-box evidentiary proof of the following events:

- **Utility grid blackouts & unannounced DSO curtailment:** for sites equipped with Battery Energy Storage Systems (BESS, 20 sites across the network), grid outages exceeding the 2-hour design discharge buffer; for sites **without** BESS storage (including detailed-inspection sites S1, S2, S3, S5), external medium-voltage grid outages or unannounced DSO curtailment directives grant immediate and total indemnification from the moment of occurrence; outage hours are excluded from SLO-1 and SLO-2 calculations.
- **Vehicle BMS non-compliance & internal battery faults:** proven via ISO 15118 protocol diagnostic dumps where charging halts due to vehicle-side BMS errors, contactor weld faults, internal cell insulation breakdown, or battery thermal overtemperature.
- **Client non-compliance with MRDT:** vehicle dwell time shorter than the physically calculated MRDT_j charging window.
- **External mechanical sabotage or impact:** physical vehicle collisions with satellite dispensers, deliberate vandalism, or severed cables.

---

## I · Automated black-box dispute settlement

- **1-second high-frequency telemetry audit:** the edge gateway continuously records voltage, current, connector-pin temperature, fan RPM and CAN/BMS protocol frames at **1-second resolution**, secured by a local NVMe circular buffer with 72-hour power-loss write-ahead logging (WAL).
- **SHA-256 cryptographic Merkle proofs:** telemetry streams generate periodic SHA-256 Merkle root hashes, anchored to cloud ledgers in real time or within 15 minutes of WAN restoration.
- **Automated root-cause attribution & self-clearing:** following any anomalous incident, the offline discrete-event simulator performs automated root-cause analysis (RCA) within **15 minutes** of network connectivity. Verified liquidated damages are credited automatically on the next billing invoice, eliminating commercial legal disputes.

---

## J · Execution & cryptographic verification seal

| Party A (Autonomous Service Provider) | Party B (Contracted Client) |
|---|---|
| Kempower Autonomous Energy Services Oy | Lahden Seudun Liikenne (Lahti City Transit) & European Logistics Depot Alliance |
| Authorized signatory: [Kempower System Chief Architect] | Authorized signatory: [Pekka Virtanen, Fleet Operations Director] |
| Execution date: January 1, 2029 | Execution date: January 1, 2029 |

Smart-contract root hash: `0x8F9C4A12E8B907D3E2F4A5C6718293A4B5C6D7E8F90123456789ABCDEF012345` · Verification gateway: https://sentinel.kempower.com/verify/contract/2029-LSL-DEPOT-01
