# Project Sentinel · Commercial Business Model
### Autonomous Energy Certainty-as-a-Service (CaaS)
*Kempower Challenge · LahtiES Energy Tech Hackathon 2026*

---

## 1. Challenge Mission: The Commercial Side

> *"When no one operates the network, who is the customer and what do they buy? Propose a business model and a one-page service agreement: what is promised, what the system decides on its own, and who is accountable when it decides wrong."*  
> — **Official Hackathon Brief (Mats Mattsson, Kempower Challenge Lead)**

---

## 2. Who is the Customer and What Do They Buy?

### 2.1 The Target Customers
Project Sentinel designs from the **equipment manufacturer / charging service provider (Kempower)** perspective (per kickoff slide 15). Our commercial counterparties represent three distinct customer segments:
1. **Public Transit Authorities & Bus Fleet Operators** (e.g., `C1` City Bus Operator at `S1` and `S5`):
   - Mission: Operating fixed-route municipal transit schedules where delayed departures trigger contractual penalties (€150 per bus).
2. **Logistics & Freight Fleet Operators** (e.g., `C2` Logistics Depot at `S2`):
   - Mission: Delivery route fulfillment under strict departure windows and DSO grid curtailment.
3. **High-Power Charge Point Operators (CPOs)** (e.g., `C3` Public Charging Hubs at `S3` and `S4`):
   - Mission: Maximizing vehicle throughput and customer satisfaction while preventing driver queue abandonment and avoiding spot electricity price spikes.

### 2.2 What Do They Buy?
Customers do **not** buy hardware boxes, software licenses, or raw kilowatt-hours. Under Project Sentinel, customers buy **Certainty-as-a-Service (CaaS)**:
* **Energy Certainty**: Guaranteed departure State-of-Charge (SoC $\ge 85\%$) at the designated departure time.
* **Grid Certainty**: Absolute guarantee that site demand never breaches the utility grid limit ($P_{\text{grid}} \le P_{\text{limit}}$).
* **Financial Certainty**: Protection against spot market price spikes and automatic contractual deductions for any unfulfilled service commitments.

---

## 3. The 20.76 FTE Operational Labor Waterfall

In the official dataset (`contracts.csv`, `labor_allocations.csv`), operating a typical 100-site charging network requires **20.76 Full-Time Equivalents (FTEs)**, representing an annual baseline operating expenditure of **€1.82M/year** (at €45/hour, €87,750/FTE):

```
Total Human Baseline Labor: 20.76 FTE (€1.82M/yr)
├── Software-Addressable Overhead: 12.44 FTE (59.95% hours, €1.09M/yr ELIMINATED)
│   ├── Cable Re-plugging & Yard Operations: 9.95 FTE (47.93% hours, €873k/yr)
│   └── Manual Dispatch & Status Monitoring: 2.49 FTE (12.02% hours, €217k/yr)
└── Retained Physical & Customer Roles: 8.32 FTE (40.05% hours, €730k/yr PRESERVED)
    ├── Physical Field Maintenance & Wear: 5.09 FTE (24.52% hours, €446k/yr)
    └── B2B Customer Support & Escalations: 3.22 FTE (15.53% hours, €284k/yr)
```

By transitioning manual replugging to **Virtual Replug (dynamic 25kW contactor rerouting)** and automating dispatch through **L2 Edge Islanding and L3 Rolling MPC**, Sentinel eliminates **€1.09M/year in operational waste** while preserving essential physical maintenance and human customer relationships.

---

## 4. The One-Page Service Agreement Framework

The commercial relationship is codified in the **One-Page Autonomous Charging Services Agreement** (`Team3-One_Page-Autonomous_Charging_Services_Agreement.docx`):

### 4.1 What is Promised (Service Level Objectives)
* **Fleet Readiness**: $99.5\%$ on-time departures with SoC $\ge 85\%$ for all scheduled vehicles.
* **Grid Non-Violation**: Zero grid limit exceedances ($0\text{ kW}$ above contracted limit) across all 15-minute settlement windows.
* **Public Hub Availability**: Maximum vehicle queue abandonment $< 5\%$ under standard operating conditions.

### 4.2 What the System Decides on Its Own (Autonomous Authorities)
* **Dynamic Contactor Routing**: L1/L2 autonomously opens/closes contactors in $260\text{ ms}$ to reallocate power modules between dispensers without human approval.
* **Thermal Derating & Load Shifting**: Autonomously throttles or shifts charging loads when junction temperatures exceed $55^\circ\text{C}$ or spot electricity prices exceed €200/MWh.
* **Edge Islanding Activation**: Autonomously detaches from cloud and enforces local DLM within $30\text{ seconds}$ of communication loss.

### 4.3 Who is Accountable When It Decides Wrong (Liability & Deductions)
* **Tiered Fee Deductions**:
  - Departure SoC $75\%\text{--}84\%$: $15\%$ monthly service fee deduction.
  - Departure SoC $<75\%$ or delayed departure: $50\%$ fee deduction plus reimbursement of municipal contract penalties (€150/bus).
  - Breached grid limit resulting in utility penalty: $100\%$ provider reimbursement.
* **Anti-Moral-Hazard Electric Fingerprinting**:
  - The system utilizes Minimum Required Duration of Telemetry (MRDT) and ISO 15118 cryptographic session verification to prevent fraudulent driver claims.
