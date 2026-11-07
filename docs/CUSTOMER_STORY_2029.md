# The Midnight Blizzard of Lahti: November 13, 2029
### A 2029 Customer Story for Autonomous Charging Network Operations
*Project Sentinel · Kempower Challenge · LahtiES Energy Tech Hackathon 2026*

---

## 1. Setting the Scene: 02:15 AM, Lahti, Finland

It is Friday, November 13, 2029, 02:15 AM in Lahti, Finland. Outside, a severe sub-zero Arctic blizzard has driven ambient temperatures down to **-18°C**, with crosswinds whipping wet snow across the Salpausselka ridge.

At Station S1 (the City Transit Bus Depot), **24 heavy electric commuter buses** sit connected to 12 dual-satellite CCS2 dispensers. In four hours, at 06:00 AM sharp, the city's entire morning commute depends on these buses rolling out across regional lines. Every delayed bus carries a contractual penalty of **€150 per occurrence** under the municipal transit concession contract (`contracts.csv`), plus immediate public transit disruption.

Under the legacy 2026 operational model, keeping this depot functional on a night like this required **three night-shift human operators**:
- One dispatcher constantly monitoring charging status and recalculating charging order;
- One yard technician in thermal overalls physically replugging heavy 400A liquid-cooled cables between buses in the freezing gale;
- One on-call electrical engineer ready to drive through the storm if a dispenser faulted.

Tonight, there is **no human operator at the depot**. The yard is dark, silent, and fully autonomous.

---

## 2. Incident 1: Thermal Stress & Contactor Rerouting (02:17 AM)

At 02:17 AM, Bus `B04` is drawing 150 kW on Dispenser `D1-9`. Wet snow combined with sub-zero wind chill has caused thermal cycling stress across the liquid-cooling connector, driving the dispenser terminal junction temperature to **59.3°C**—rapidly approaching the critical 65.0°C thermal runaway safety limit.

In a traditional setup, the charger's hard safety interlock would trip, disconnecting the bus. The bus would sit cold and uncharged until morning, resulting in a missed morning departure.

**What Sentinel Does Autonomously**:
1. **L1 Predictive Degradation Sensing**: The high-frequency firmware telemetry detects an abnormal thermal gradient ($dT/dt = +1.8^\circ\text{C/min}$) at 59.3°C, 5.7°C below the hard safety trip threshold.
2. **Break-Before-Make (BBM) Contactor Switchover**: Within **260 milliseconds**, the L1 controller commands the 25 kW DPR power routing matrix to open contactor `K1-9` and route power from redundant module `D1-10`.
3. **Seamless Load Transfer**: Bus `B04` never disconnects; power is smoothly dialed back, thermal stress dissipates to 38.2°C, and the session continues uninterrupted.

---

## 3. Incident 2: Total Cellular WAN Blackout (02:41 AM)

At 02:41 AM, ice accumulation on the local telecommunications mast causes a **total loss of 4G/5G cellular connectivity**. The cloud central management system (L3) is suddenly unreachable. 

Under standard cloud-managed networks, lost connectivity freezes chargers in either a failsafe zero-power halt or an uncoordinated free-run mode that instantly breaches the **1,200 kW utility grid cap**.

**What Sentinel Does Autonomously**:
1. **L2 Edge Islanding Mode**: The local site controller detects heartbeat timeout ($t > 30\text{s}$) and immediately assumes master control.
2. **Deterministic Local Dynamic Load Management (DLM)**: Operating purely on embedded local non-volatile state, the L2 controller executes a continuous Earliest-Deadline-First (EDF) dispatch loop, enforcing the hard **1,200 kW grid cap** across all 24 connected vehicles with microsecond-level accuracy.
3. **Zero Vehicle Disruption**: Not a single charging session terminates. The local edge records all ISO 15118 metering tuples to cryptographic tamper-evident local storage, ready for batch synchronization when the uplink restores.

---

## 4. Incident 3: Spot Market Price Volatility (03:15 AM)

At 03:15 AM, Finnish Nord Pool day-ahead electricity prices surge due to wind turbine icing, peaking at **€799.30/MWh** for two consecutive 15-minute settlement intervals. 

Charging all 24 buses at full blast during this price peak would impose catastrophic energy costs on the transit agency.

**What Sentinel Does Autonomously**:
1. **Model Predictive Control (MPC) Optimization**: The 15-minute rolling horizon optimizer calculates that buses `B01` through `B16` already have sufficient SoC margin to complete their morning routes.
2. **Strategic Load Curtailment**: Sentinel dials back discretionary charging across low-urgency vehicles, while maintaining full throughput on high-urgency buses `B17` through `B20`.
3. **Financial Protection**: The depot avoids **€1,420** in peak spot energy charges in 30 minutes, without delaying a single vehicle departure.

---

## 5. The Morning After: 06:00 AM

At 06:00 AM, Pekka, the Fleet Operations Director, steps into his warm kitchen with a cup of coffee. He opens his phone.

There are no frantic panic calls, no missed departure alarms, and no contractual penalty notices. The Sentinel executive summary displays three green checkmarks:
- **Fleet Departure Reliability**: 24 / 24 buses ready at target SoC ($\ge 85\%$).
- **Grid Safety**: Peak power capped strictly at 1,080 kW (120 kW below the 1,200 kW grid limit).
- **Service Level Guarantee**: 100% SLA fulfillment; €0 penalties incurred.

Pekka takes a sip of coffee. The buses are already silently rolling out onto the snowy streets of Lahti.

---

## 6. Summary: The 2029 Paradigm Shift

| Operational Dimension | Legacy 2026 Model | Project Sentinel 2029 (CaaS) |
| :--- | :--- | :--- |
| **Depot Staffing** | 3 full-time night operators / site | **Zero on-site night operators** |
| **Thermal Fault Handling** | Hard trip $\to$ cold bus $\to$ missed run | **260ms BBM reroute $\to$ uninterrupted charge** |
| **WAN Uplink Failure** | Freezes charger or trips substation breaker | **Autonomous L2 edge islanding ($1,200\text{ kW}$ cap)** |
| **Grid Price Spikes** | Uncoordinated charging $\to$ massive energy bills | **Rolling MPC load shifting $\to$ 100% SLA at minimum cost** |
| **Commercial Contract** | Hardware warranty + manual technician dispatch | **Outcome-Based Certainty-as-a-Service (Guaranteed Departure SoC)** |
