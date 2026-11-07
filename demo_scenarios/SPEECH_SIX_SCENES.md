# Six Problem Replay Demonstrations · Master English Pitch Script

> Total Duration: ~10 Minutes. Six autonomous self-healing replay scenes mapped 1:1 to the Streamlit interactive dashboard (`demo_scenarios/app.py`).
> Language: Professional, spoken technical English.
> Each scene provides operator cues ("Where to click") followed by verbatim spoken narration.
> All numbers are derived directly from the official 45 CSV files and deterministic simulations in `src/sim/`.

---

## Opening Narration (0:30)

"Good afternoon, judges and colleagues. Over the next ten minutes, we will demonstrate six real-world operational crises that occurred on Friday, November 13th across the European charging network. 

Each screen demonstrates one clear contrast: first, how the legacy system behaves with humans in the loop; second, how Project Sentinel autonomously resolves the exact same crisis with zero human intervention. 

On both sides of the screen, you are looking at the exact same vehicles, the exact same power limits, and the exact same timestamps. The only difference is the autonomous decision intelligence running on the edge. 

We do not make unrealistic claims that electrical machinery will never fail. What we prove is: when hardware fails, grid limits drop, or prices spike, no human operator ever has to step in."

---

## Scene 1 · S1 Bus Depot: Overnight Cabinet Overheating & Replug Elimination (~2:00)

> **Dashboard Page**: `1_Night_Replay.py`  
> **Interactive Actions**: Click **Restart**, then click **Jump to → Fault (02:25)**. Conclude by clicking **Morning Summary** to inspect final departure energy and labor tallies.

**Verbatim Narration**:  
"S1 is a high-frequency municipal electric bus depot. Every night, 24 articulated transit buses return to base, but the facility has only 12 physical charging dispensers. Because dispensers are scarce, the legacy network relies on midnight human labor: at 00:30, a yard attendant must physically walk the depot yard, unplug fully charged buses, and move cables to plug in the remaining vehicles. In the historical log, this attendant made 9 separate trips.

At 02:25, charging cabinet C1-3 overheated and suffered a hardware trip. In the legacy system, all four dispensers connected to that cabinet went completely dead. The charging cables remained physically plugged into the buses, no human was awake to swap them, and four critical transit buses sat unpowered on dead plugs until sunrise.

Project Sentinel re-architects this depot:
First, we expand the 12 single-cable pedestals into dual-cable satellite outputs, giving all 24 parking bays dedicated connection points so evening drivers self-plug upon parking.
Second, a cross-cabinet busbar tie interconnects the DC power pool. When cabinet C1-3 overheats, power routes around the fault through healthy cabinets C1-1 and C1-2. The dispensers remain energized, while total site capacity derates smoothly from 1,080 kW to 720 kW.

At morning roll-out: the legacy system stranded 4 buses undercharged and burned 9 human replug actions. Project Sentinel delivers 0 undercharged buses and 0 human actions.

We eliminated labor not because we worked faster, but because the midnight replug action no longer has any structural reason to exist."

---

## Scene 2 · S3 Highway Hub: Islanded Grid Resilience During 2-Hour WAN Loss (~2:00)

> **Dashboard Page**: `2_Outage_Replay.py`  
> **Interactive Actions**: Click **Jump to → Outage (11:00)**, view local DLM activation at **Mid-Outage (12:00)**, then click **Restored (13:00)** to verify state sync.

**Verbatim Narration**:  
"At Station S3—a high-throughput highway corridor hub—cellular wide-area communications collapsed completely between 11:00 and 13:00.

Notice what failed: the station lost its wide-area data link, not its utility power. What was lost was the answer to: 'Who decides how many kilowatts each dispenser receives?'

In cloud-dependent architectures, dynamic load management runs centrally. When cloud connectivity drops, the local hub cannot safely calculate load without risking transformer overload. Consequently, it retreats to a fail-safe turtle mode: capping each dispenser at a flat 50 kW. Across 10 active dispensers, total delivery plunged from 1,425 kW down to 500 kW.

A commercial heavy-duty truck needing 224 kWh normally charges in 45 minutes; under 50 kW, dwell time ballooned to 269 minutes. In the empirical data, highway drivers will wait at most 46 minutes. Drivers saw the backing-up queue and drove away, resulting in a 44.8% customer abandonment rate.

Project Sentinel embeds an autonomous Dynamic Load Management engine directly on the edge controller. When cloud connectivity drops, the edge microgrid controller takes over instantly. It dynamically juggles dispenser loads while rigidly enforcing the 1,500 kW transformer ceiling (operating at 1,425 kW DC to account for the 95.5% rectifier efficiency margin).

Same outage, same vehicles: Sentinel keeps all 10 dispensers operating at maximum dynamic capacity. Drivers charged at full speed without even realizing the cloud was offline.

The takeaway: A communication outage severs telemetry, not electrical energy. Push decision authority to the edge, and a network blackout becomes a background notification."

---

## Scene 3 · S2 Truck Depot: Mitigating the 799.30 €/MWh Spot Price Spike (~1:30)

> **Dashboard Page**: `3_Price_Spike_Replay.py`  
> **Interactive Actions**: Click **Jump to → Peak (18:00)** to inspect the spot price spike to 799.30 €/MWh and dynamic load shifting.

**Verbatim Narration**:  
"In this scenario, no hardware broke and no grid event occurred. Only one variable shifted: wholesale electricity price.

Between 17:15 and 18:45, Nordic spot prices surged tenfold, skyrocketing from 69 €/MWh to a peak of 799.30 €/MWh. 

Under the uncoordinated First-Come-First-Served approach, eight heavy trucks shared 800 kW equally during peak price hours. One commercial truck, T02, was scheduled for immediate evening departure at 17:45. Because available power was diluted across all vehicles, T02 ran out of time and departed undercharged. Worse, the depot burned 342.66 € in peak-rate electricity.

Project Sentinel executes a two-tier priority dispatch: it reconciles departure deadlines before evaluating electricity prices. Trucks T01 through T04 had mandatory departures between 17:30 and 18:15; Sentinel prioritizes them to ensure 100% full-charge departure. Conversely, trucks T05 through T08 were scheduled to dwell overnight until morning; Sentinel autonomously pauses their charging during the 90-minute price peak, resuming charging at 22:00 when spot prices drop back to 52 €/MWh.

The result: All 8 trucks depart on time with 100% required energy, while net electricity procurement drops from 342.66 € to 179.90 €—a 47.5% direct cost reduction.

Our priority order never waivers: Physical safety first, grid capacity limits second, departure deadlines third, and energy market arbitrage fourth."

---

## Scene 4 · S2 Logistics Hub: Navigating a 400 kW DSO Grid Curtailment (~1:30)

> **Dashboard Page**: `4_Curtailment_Replay.py`  
> **Interactive Actions**: Click **Jump to → Cap (16:00)** to trigger the 400 kW grid clamp, then click **Cap Ends (19:00)**.

**Verbatim Narration**:  
"Here, market prices are stable, but the local distribution system operator (DSO) issues a mandatory curtailment order: from 16:00 to 19:00, depot S2’s grid capacity is clamped from 800 kW down to 400 kW.

The baseline system allocated power based on arrival time. Because overnight trucks arrived early and had high battery capacity, they consumed almost the entire 400 kW allotment. Consequently, the four urgent trucks scheduled to depart at 17:30, 17:45, 18:00, and 18:15 received virtually zero energy. All four suffered missed departures, accumulating 278.9 kWh in fleet energy deficits.

Project Sentinel operates under the same 400 kW restriction, but replaces arrival-order charging with Urgency Waterfilling. Urgent departures get primary claim on the 400 kW budget. Overnight trucks yield their power and pause temporarily. At 19:00, the moment the DSO restriction lifts, the system opens up full 800 kW capacity to recharge the overnight fleet.

The outcome: All 8 trucks achieve 100% on-time departure. 

Grid curtailment is not an energy deficit problem—it is a power rationing priority problem. Allocate the clamped kilowatts by departure urgency, and zero departures are compromised."

---

## Scene 5 · S4 Urban Charging Hub: Millisecond Cable Fault Isolation (~1:00)

> **Dashboard Page**: `5_Cable_Fault_Replay.py`  
> **Interactive Actions**: Click **Jump to → Fault (21:30)** to watch dispenser D4-2 trip and verify neighboring dispenser continuity.

**Verbatim Narration**:  
"At 21:30 at city hub S4, a CCS2 charging cable sustained internal insulation breakdown (fault code F017).

Under standard cloud management, the fault is signaled upstream to a cloud operations center, verified against alarm thresholds, and queued for manual operator ticket dispatch—a process taking 30 to 60 seconds.

Project Sentinel’s edge controller executes hardware safety interlocks locally. Within 40 milliseconds, the local protection circuit isolates the faulty contactor, locks out the damaged connector pin, and automatically generates a field maintenance ticket in the background. The remaining seven dispensers continue uninterrupted charging without a flicker.

To maintain complete engineering honesty: at 21:30, the hub had spare charging capacity, so total delivered energy is comparable. The core achievement here is response velocity and human elimination: 30 seconds of human alarm triage is replaced by a 40-millisecond autonomous safety trip."

---

## Scene 6 · S5 Bus Depot: Self-Healing Commissioning Configuration Mismatch (~1:30)

> **Dashboard Page**: `6_Commissioning_Replay.py`  
> **Interactive Actions**: Click **Jump to → Mismatch (00:00)** to display the 600 kW vs 900 kW configuration conflict, then click **Unlock (03:30)**.

**Verbatim Narration**:  
"In this final scenario, not a single piece of hardware failed. The failure was a silent human configuration error.

Depot S5 was newly commissioned with two 450 kW power cabinets and a 900 kW utility transformer. However, in `site_config.csv`, an operator mistakenly keyed the site capacity limit as 600 kW. Furthermore, dispenser D5-7 was throttled to 50 kW, and dispenser D5-8’s communication SIM card was left unactivated. Operating under this misconfigured bottleneck, 5 out of 12 morning buses departed undercharged.

Project Sentinel includes an automated Three-Way Configuration Reconciler. Upon boot, it cross-references equipment nameplate registers, grid interconnection contracts, and dynamic telemetry. It instantly detects the contradiction between the 900 kW physical transformer and the 600 kW software cap, automatically elevating the operating ceiling to 900 kW, unthrottling dispenser D5-7 to 150 kW, and cycling D5-8’s backup eSIM profile.

With identical buses and identical hardware, missed departures drop from 5 to exactly zero.

Autonomous networks must do more than recover from broken hardware—they must detect and reconcile human configuration errors."

---

## Closing Summary (0:30)

"Across these six operational scenarios, we have not presented six disconnected patches. We have demonstrated one coherent autonomous control framework:

When vehicles arrive, schedule them by departure urgency.  
When cabinets overheat, route power through healthy modular channels.  
When spot prices surge, defer flexible overnight loads.  
When cables break, trigger 40-millisecond safety lockouts.  
When configurations conflict, reconcile data automatically.

Our objective is not an imaginary world where machines never break. Our objective is an industrial reality where broken machines no longer require human triage.

That is Project Sentinel. Thank you."

---

## Master Timing & Rehearsal Guide (10:00 Total Budget)

| Scene Index | Topic & Page | Allocated Duration | Running Timestamp |
|---|---|---|---|
| **Opening** | System Thesis & Integrity Statement | 0:30 | 0:00 – 0:30 |
| **Scene 1** | S1 Bus Depot: Overnight Overheat & Replug | 2:00 | 0:30 – 2:30 |
| **Scene 2** | S3 Highway Hub: 2-Hour Islanded WAN Loss | 2:00 | 2:30 – 4:30 |
| **Scene 3** | S2 Freight Depot: 799.30 €/MWh Spot Peak | 1:30 | 4:30 – 6:00 |
| **Scene 4** | S2 Logistics Hub: 400 kW DSO Curtailment | 1:30 | 6:00 – 7:30 |
| **Scene 5** | S4 Urban Hub: Millisecond Cable Fault Trip | 1:00 | 7:30 – 8:30 |
| **Scene 6** | S5 Bus Depot: Config Mismatch Self-Heal | 1:30 | 8:30 – 10:00 |
| **Closing** | Executive Synthesis & Vision Statement | 0:30 | 10:00 – 10:30 |
| **Total** | **End-to-End Demo Narration** | **10:30** | *Flexible to 10:00* |
