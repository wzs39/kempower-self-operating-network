# Autonomous Charging Network Industrial Service Level Agreement & 2029 Customer Story
## One-Page Service Level Agreement (SLA) & Operating Specification: Autonomous Energy Certainty
*Contract Form No: KEMP-AUTO-2029-SLA-V2 · Applicable to Commercial Fleets & High-Power Charging Infrastructure*  
*Jurisdiction: Republic of Finland / European Union Energy Law · Effective Date: January 1, 2029*

---

## 📖 2029 Flagship Customer Story: The Zero-Touch Blizzard Rollout in Lahti
### A Sub-Zero Winter Night with Pekka Virtanen (Lahti City Transit / Lahden Seudun Liikenne, LSL)

> **Context & Profile**:  
> Pekka Virtanen is the Director of Fleet Operations for Lahti City Transit (Lahden Seudun Liikenne, LSL). In 2026, Pekka’s worst operational nightmare was winter staffing and depot dispatch. In sub-zero Finnish winters (-18°C), deep snowdrifts required 3 to 4 yard attendants every night to drag heavy 400A liquid-cooled charging cables back and forth across 24 articulated electric transit buses (`move_and_replug_vehicle`). If an attendant fell ill or a connector pin iced over, morning rush hour at 06:00 would see 4 to 5 key bus routes cancelled due to stranded, undercharged vehicles — resulting in tens of thousands of euros in municipal delay penalties and hundreds of freezing passengers stranded at transit stops.

> **Friday, January 19, 2029 · Lahti North Bus Depot (Depot S1) · Temperature: -18°C · Blizzard**:
>
> 1. **22:00 — Zero-Touch Arrival & Silent Cryptographic Authorization**:  
>    All 24 articulated 18-meter electric buses return to depot S1 at the end of their evening shifts. Drivers pull into their assigned stalls and plug in the dual-satellite CCS2 cables. Leveraging the **ISO 15118-20 Plug & Charge (PnC)** protocol, the depot edge controller and onboard Vehicle SECC complete bidirectional TLS 1.3 cryptographic mutual authentication based on ECDSA P-256 digital certificates within **1.1 seconds**. Drivers lock their cabs and head home. The depot yard is completely empty of human personnel.
>
> 2. **02:15 — Sub-Zero Preconditioning & Dynamic Power Routing**:  
>    Ambient temperature plunges to -18°C, chilling LFP battery cells below their optimal charge-acceptance threshold. **Sentinel’s Edge Self-Healing Controller** detects low cell temperature telemetry via high-speed CAN bus and instructs the modular 25 kW DPR matrix to dynamically allocate 50 kW to each vehicle's onboard PTC thermal preconditioning circuit. Within **18 minutes**, core cell temperatures reach their optimal 15°C charging window. Fleet charging efficiency surges by 35%, avoiding the cold-weather charging drag that historically delayed morning departures.
>
> 3. **03:40 — Millisecond Break-Before-Make (BBM) Isolation & N-1 Power Re-Pooling**:  
>    Edge telemetry diagnostics detect abnormal fan RPM and an incipient thermal runaway curve on cabinet C1-3 (a dual-threshold thermal model predicted degradation 199 minutes prior, autonomously scheduling scheduled daytime technician servicing: `cleared_by = technician`). The depot's millisecond Break-Before-Make (BBM) relay sequencing (software logic <10 ms, physical relay transition 85 ms) safely isolates the degraded rectifier channel. Healthy cabinets C1-1 and C1-2 pool their remaining 720 kW capacity across the 24 dual-satellite connection points (backed by the Titanium Tier hardware architecture), silently sustaining charging without dropping a single bus.
>
> 4. **05:30 — 100% On-Time Full-Charge Departure & The Morning Coffee**:  
>    At 05:30, all 24 electric transit buses display solid green SoC indicators (100.0% required energy delivered). Morning shift drivers board pre-warmed cabs, turn on the auxiliary power, and roll out through the snowy depot gates on schedule.  
>    Pekka Virtanen wakes up in his downtown Lahti apartment, sips his morning coffee, and glances at a silent notification on his smartphone:  
>    *“Lahti North Depot (S1): 24/24 scheduled departures completed with 100.0% required energy delivered. Overnight human interventions: 0. Autonomous self-healing events resolved: 1 sub-zero thermal preconditioning, 1 cabinet N-1 dynamic derate. Monthly SLA fulfillment: 99.98% (Titanium Green Compliant).”*
>
> **This is commercial charging in 2029: Charging is no longer a labor-intensive maintenance burden, but an outcome-based energy certainty service (Charging-as-a-Service, CaaS).**

---

## 🏛️ 0. Preamble & Legal Binding

This Autonomous Charging Network Service Level Agreement ("SLA") is entered into in Lahti, Finland, by and between:
1. **Autonomous Operator / Service Provider**: Kempower Autonomous Energy Services Oy (transitioning from pure hardware manufacturing to an Outcome-Based Energy Certainty-as-a-Service provider, operating modular DPR matrices, edge microgrid gateways, and autonomous dispatch algorithms);
2. **Contracted Client**: Commercial transit authority (e.g., Lahti City Transit / LSL), long-haul electric freight logistics fleet, or high-throughput public charging hub operator (collectively, the "Client").

**Core Subject Matter**: The Client entrusts the operational management and dispatch of charging infrastructure to the Autonomous Control Central Core. Both parties agree that continuous human dispatch and manual operations are eliminated, replaced by an **autonomous, outcome-based energy delivery architecture**.

---

## 🎖️ 1. Three-Tier Commercial Service Levels

To accommodate varying operational tolerances and mission-critical profiles, the service provides three distinct contractual tiers:

| Commercial Dimension | Titanium Tier (Core Transit / Freight) | Gold Tier (Standard Commercial / Public) | Silver Tier (Auxiliary Fleet / Destination) |
|---|---|---|---|
| **Primary Use Cases** | Urban transit depots (S1/S5), zero-tolerance freight corridors (S2) | High-throughput public hubs (S3/S4), regional logistics depots | Corporate campuses, secondary overnight passenger car parking |
| **On-Time Full-Charge SLO (SLO-1)** | **$\ge 99.90\%$** ($\le 3$ missed trips/year) | **$\ge 99.50\%$** (Standard industrial guarantee) | **$\ge 99.00\%$** (Commercial baseline) |
| **Dispenser Service Availability (SLO-2)** | **$\ge 99.90\%$** ($\le 43$ min downtime/month) | **$\ge 99.50\%$** ($\le 216$ min downtime/month) | **$\ge 99.00\%$** ($\le 432$ min downtime/month) |
| **Self-Healing Control Latency (SLO-5)** | **$\le 50\text{ ms}$** (<10 ms logic + BBM matrix shift) | **$\le 100\text{ ms}$** (Hardware-grade relay switch) | **$\le 200\text{ ms}$** (Standard contactor cycle) |
| **Islanded Autonomous Runtime (SLO-3)** | **$\ge 72\text{ hours}$** (Full 1,425 kW local DLM) | **$\ge 48\text{ hours}$** (Transformer limit management) | **$\ge 24\text{ hours}$** (Basic static split) |
| **Overnight Replugging Guarantee** | **0 Human Labor** (24 dual-satellite expansion `324,000 €` + cross-tie / 0 deficit; plug-only yields 8 missed) | **0 Human Labor** (0 € pure software urgency waterfilling, S1 deficit cut by 87.8%) | Best-effort automated replug driver notifications |
| **Base Trip Delay Penalty ($P_{\text{base}}$)** | **350.00 € / departure** | **250.00 € / departure** | **150.00 € / departure** |
| **Progressive Delay Penalty ($C_{\text{min}}$)** | **7.50 € / minute** (after 10 min grace) | **5.00 € / minute** (after 15 min grace) | **3.00 € / minute** (after 20 min grace) |
| **Missing Energy Compensation ($C_{\text{energy}}$)** | **2.00 € / kWh** + rental bus reimbursement | **1.50 € / kWh** | **1.00 € / kWh** |
| **Base Management Fee Multiplier** | **$1.25\times$** Base Tariff | **$1.00\times$** Base Tariff (Standard Baseline) | **$0.80\times$** Base Tariff |

---

## ⚡ 2. Guaranteed Service Level Objectives (SLOs)

The Service Provider guarantees the following measurable SLOs during each billing period (Gold Tier baseline, upgraded under Titanium Tier):

| SLO Identifier | Metric Name & Description | Gold Target | Evaluation Window & Scope | Default Breach Condition |
|---|---|---|---|---|
| **SLO-1** | **Fleet On-Time Full-Charge Rate** | **$\ge 99.50\%$** | Evaluated per scheduled departure. Requires actual departure $SoC \ge SoC_{\text{required}}$ and delay $\le 0\text{ min}$, subject to MRDT compliance | Monthly on-time rate drops below 99.50% |
| **SLO-2** | **Dispenser Fleet Availability** | **$\ge 99.50\%$** | Minute-level availability across 720 monthly hours: $\frac{\sum T_{\text{available}}}{\sum T_{\text{total}}} \times 100\%$ | Monthly fleet availability drops below 99.50% |
| **SLO-3** | **Islanded Operational Resilience** | **$\ge 72\text{ hours}$** | Commences upon WAN cellular/fiber loss; edge maintains 100% rated capacity dynamic load allocation | Unplanned stall shutdown or grid limit breach during outage |
| **SLO-4** | **Grid Limit Compliance Rate** | **100.0%** (Absolute) | Second-level current telemetry: $P_{\text{grid}}(t) \le P_{\text{limit}}(t)$ (including 95.5% rectifier efficiency buffer) | Any instantaneous breach of transformer capacity |
| **SLO-5** | **Self-Healing Control Latency** | **$\le 100\text{ ms}$** | End-to-end latency from anomaly trigger to relay isolation and power reconfiguration | Dynamic response latency exceeds 200 ms |

---

## 🎛️ 3. Explicit Decision Boundaries Matrix

To establish legal and technical certainty, the boundary between autonomous algorithmic authority and mandatory human intervention is strictly defined:

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                               Autonomous Authority vs. Mandatory Human Action Boundary                          │
├───────────────────────────────┬────────────────────────────────────────────────┬────────────────────────────────┤
│ Operational Scenario          │ Algorithm Direct Authority                     │ Mandatory Human Escalation     │
├───────────────────────────────┼────────────────────────────────────────────────┼────────────────────────────────┤
│ 1. Dynamic Power Routing      │ Fully Autonomous: Reallocates 25 kW DPR blocks │ Human intervention prohibited  │
│    and Virtual Replugging     │ based on departure countdown and SoC deficit.  │ (prevents load disruption).    │
├───────────────────────────────┼────────────────────────────────────────────────┼────────────────────────────────┤
│ 2. Spot Price Spikes and      │ Fully Autonomous: Pre-charges flexible loads;  │ Escalates only if DSO issues a │
│    Grid Curtailment (G1-G3)   │ derates low-urgency stalls (0.0 kW during G1). │ mandatory grid cut-off order.  │
├───────────────────────────────┼────────────────────────────────────────────────┼────────────────────────────────┤
│ 3. Module Thermal Anomaly &   │ Fully Autonomous: Millisecond BBM isolation;   │ Automatically logs work order; │
│    Secondary Hardware Faults  │ N-1 power pooling sustains operation.          │ technician dispatches in day.  │
├───────────────────────────────┼────────────────────────────────────────────────┼────────────────────────────────┤
│ 4. Electrical Insulation &    │ Fully Autonomous: Millisecond contactor trip;  │ Escalates to field crew after  │
│    Grounding Breakdown (IMD)  │ isolates gun and locks out connector.          │ 3 consecutive failed retries.  │
├───────────────────────────────┼────────────────────────────────────────────────┼────────────────────────────────┤
│ 5. Total WAN Cellular/Fiber   │ Fully Autonomous: Local edge takes over        │ Escalates to telecom provider  │
│    Loss (Network Outage)      │ 1,500 kW local dynamic load balancing (DLM).   │ if outage exceeds 72 hours.    │
├───────────────────────────────┼────────────────────────────────────────────────┼────────────────────────────────┤
│ 6. Physical Vehicle Crash,    │ Fully Autonomous: Physical trip opens master   │ Mandatory on-site inspection & │
│    Fire, or Emergency Stop    │ substation breaker within 10 ms.               │ certified manual breaker reset.│
└───────────────────────────────┴────────────────────────────────────────────────┴────────────────────────────────┘
```

---

## 🔒 4. Hard Physical Safety Trip Thresholds

Autonomous optimization algorithms are strictly subordinated to underlying electrical safety interlocks. The following thresholds are permanently locked in cabinet and dispenser MCU firmware and cannot be overridden by software or cloud commands:

$$\begin{cases}
T_{\text{cabinet\_internal}} \ge 65.0^{\circ}\text{C} & \implies \text{Linear derate (50\% load reduction, fault alarm, reverse fan pulse)} \\
T_{\text{cabinet\_internal}} \ge 75.0^{\circ}\text{C} & \implies \text{Hardware Trip (forces open master AC contactor within 100 ms)} \\
T_{\text{connector\_pin}} \ge 90.0^{\circ}\text{C} & \implies \text{DC Disconnect (disconnects and locks DC contactor within 50 ms)} \\
R_{\text{insulation}} < 100\,\Omega/\text{V} & \implies \text{IMD Fault (immediate session termination; inhibits high-voltage closure)} \\
I_{\text{residual\_DC}} \ge 30\,\text{mA} & \implies \text{RCD Trip (disconnects circuit within 40 ms per IEC 61851-23)} \\
P_{\text{site\_grid}} > 1.00 \times P_{\text{transformer\_limit}} & \implies \text{Overload Clamp (clamps non-urgent DPR modules within 20 ms)}
\end{cases}$$

---

## 💰 5. Liquidated Damages, Moral Hazard Gates & Liability Caps

### 5.1 Minimum Required Dwell Time (MRDT) Pre-Condition & Penalty Equation
**Physical Feasibility Gate (MRDT)**:  
To prevent moral hazard and predatory claims, fleet vehicles must respect the laws of physics regarding minimum charging dwell time. For each departure $j$, the system calculates the Minimum Required Dwell Time ($\text{MRDT}_j$):

$$\text{MRDT}_j = \left( \frac{\frac{\text{SoC}_{\text{req}, j} - \text{SoC}_{\text{arrive}, j}}{100.0} \times \text{Cap}_{\text{batt}, j}}{\min(P_{\text{charger\_max}}, P_{\text{vehicle\_max}, j}) \cdot \eta_{\text{system}}} \right) \times 60 + T_{\text{buffer}} \quad [\text{minutes}]$$

- System round-trip efficiency: $\eta_{\text{system}} = 0.95$.
- Safety handshake, insulation test, and dynamic matrix routing buffer: $T_{\text{buffer}} = 15.0\text{ minutes}$.
- **Liability Activation**: Liquidated damages for delayed or undercharged departures apply **if and only if** the actual on-site dwell time $\Delta t_{\text{dwell}, j} = (t_{\text{depart\_sched}, j} - t_{\text{arrive\_actual}, j}) \ge \text{MRDT}_j$. If a vehicle arrives late ($\Delta t_{\text{dwell}, j} < \text{MRDT}_j$), the Service Provider is fully indemnified and provides best-effort charging only.

**Fleet Penalty Equation (Gold Tier Baseline)**:  
Subject to MRDT compliance, liquidated damages are calculated rigidly as follows:

$$\text{Penalty}_{\text{fleet}} = \sum_{i \in \text{delayed\_trips}} \left[ P_{\text{base}} + \max(0, t_{\text{delay\_min}, i} - 15) \times C_{\text{min}} \right] + \sum_{j \in \text{undercharged}} \left[ \frac{\max(0, SoC_{\text{req}, j} - SoC_{\text{dep}, j})}{100.0} \times \text{Cap}_{\text{batt}, j} \times C_{\text{energy}} \right]$$

- **Base Delay Penalty ($P_{\text{base}}$)**: **250.00 € / departure** (triggers instantly upon delay $t_{\text{delay}} > 0$).
- **Progressive Delay Penalty ($C_{\text{min}}$)**: **5.00 € / minute** beyond the 15-minute grace window.
- **Missing Energy Compensation ($C_{\text{energy}}$)**: **1.50 € / kWh** for unfulfilled energy deficits below target.

### 5.2 Progressive Monthly Availability Fee Deduction Schedule
Monthly management fee deductions follow a strict piecewise closed function:

$$\text{Fee}_{\text{deduction}} = \begin{cases}
0, & \text{if } \text{Availability}_{\text{actual}} \ge 99.50\% \\
\text{Monthly Base Fee} \times \min\left(90.0\%, \, \left\lceil \frac{99.50\% - \text{Availability}_{\text{actual}}}{0.10\%} \right\rceil \times 2.0\% \right), & \text{if } 95.00\% \le \text{Availability}_{\text{actual}} < 99.50\% \\
\text{Monthly Base Fee} \times 100.0\%, & \text{if } \text{Availability}_{\text{actual}} < 95.00\% \quad (\text{Service Default Trip})
\end{cases}$$

- **Progressive Deduction Range ($95.00\% \le \text{Availability} < 99.50\%$)**: For each 0.10% decrement below the 99.50% commitment, 2.0% of the monthly fee is deducted (up to 90.0%).
- **Service Default Trip ($\text{Availability} < 95.00\%$)**: If availability drops below 95.00%, the entire monthly fee is waived (100.0% deduction).

### 5.3 Aggregate Liability Cap & Non-Negative Billing Guarantee
1. **Fee Deduction Ceiling**: $\text{Fee}_{\text{deduction}} \le 100.0\% \times \text{Monthly Base Fee}$ (fee waiver only; no negative management fees).
2. **Monthly Fleet Liquidated Damages Cap**: Total fleet penalties ($\sum \text{Penalty}_{\text{fleet}}$) for a single depot in a calendar month cannot exceed **100.0% of that depot's monthly service management fee**.
3. **Aggregate Liability Ceiling & Non-Negative Billing Guarantee**: Under no circumstances shall total monthly payouts exceed **150.0% of the Monthly Base Fee**:
   $$\text{Total Monthly Payout} = \text{Fee}_{\text{deduction}} + \sum \text{Penalty}_{\text{fleet}} \le 1.50 \times \text{Monthly Base Fee}$$
   Generated monthly statements strictly satisfy $\text{Net Payable} = \max(0.0, \text{Monthly Base Fee} - \text{Credits})$, with excess credits rolling over into next month’s service vouchers, ensuring commercial balance-sheet solvency.
4. **Consequential Damages Carve-Out**: The Service Provider’s financial liability is strictly limited to the direct liquidated damages above. The Service Provider shall not be liable for indirect damages, lost commercial business revenue, or punitive claims.

---

## 🛡️ 6. Force Majeure & Liability Carve-Outs

The Service Provider is relieved of penalty liability and availability penalties exclusively upon objective black-box evidentiary proof of the following events:
1. **Utility Grid Blackouts & Unannounced DSO Curtailment**:
   - For sites equipped with Battery Energy Storage Systems (BESS, 20 sites across the network), grid outages exceeding the 2-hour design discharge buffer.
   - For **sites without BESS storage (including detailed inspection sites S1, S2, S3, S5)**, external medium-voltage grid outages or unannounced DSO curtailment directives grant **immediate and total indemnification** from the moment of occurrence; outage hours are excluded from SLO-1 and SLO-2 calculations.
2. **Vehicle BMS Non-Compliance & Internal Battery Faults**: Proven via ISO 15118 protocol diagnostic dumps where charging halts due to vehicle-side BMS errors, contactor weld faults, internal cell insulation breakdown, or battery thermal overtemperature.
3. **Client Non-Compliance with MRDT**: Vehicle dwell time is shorter than the physically calculated $\text{MRDT}_j$ charging window.
4. **External Mechanical Sabotage or Impact**: Physical vehicle collisions with satellite dispensers, deliberate vandalism, or severed cables.

---

## 🔍 7. Automated Black-Box Dispute Settlement

1. **1-Second High-Frequency Telemetry Audit**: The edge gateway continuously records voltage, current, connector pin temperature, fan RPM, and CAN/BMS protocol frames at **1-second resolution**, secured by a local NVMe circular buffer with 72-hour power-loss write-ahead logging (WAL).
2. **SHA-256 Cryptographic Merkle Proofs**: Telemetry streams generate periodic SHA-256 Merkle root hashes, anchored to cloud ledgers in real time or within 15 minutes of WAN restoration.
3. **Automated Root-Cause Attribution & Self-Clearing**: Following any anomalous incident, the offline discrete-event simulator performs automated root-cause analysis (RCA) within **15 minutes** of network connectivity. Verified liquidated damages are credited automatically on the next billing invoice, eliminating commercial legal disputes.

---

## ✍️ 8. Execution & Cryptographic Verification Seal

```
PARTY A (Autonomous Service Provider):                  PARTY B (Contracted Client):
Kempower Autonomous Energy Services Oy                 Lahden Seudun Liikenne (Lahti City Transit)
                                                       & European Logistics Depot Alliance

Authorized Signatory: [Kempower System Chief Architect] Authorized Signatory: [Pekka Virtanen, Fleet Operations Director]
Execution Date: January 1, 2029                        Execution Date: January 1, 2029
Smart Contract Root Hash: 0x8F9C4A12E8B907D3E2F4A5C6718293A4B5C6D7E8F90123456789ABCDEF012345
Verification Gateway: https://sentinel.kempower.com/verify/contract/2029-LSL-DEPOT-01
```
