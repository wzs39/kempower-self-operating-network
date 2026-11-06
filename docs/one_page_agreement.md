# One-Page Service Agreement — Autonomous Energy Certainty

**Project Sentinel · Kempower Challenge, LahtiES Energy Tech Hackathon 2026**
Service Provider = equipment supplier & service provider (`contracts.csv`, holds 18/29 service-scope contracts) · Client = fleet operator / site owner · Scenario reference day **2026-11-13** · All figures computed from the **synthetic** official dataset; the 2029 customer is fictional.

> Printable single-page version: [`one_page_agreement.html`](./one_page_agreement.html) (verified: renders to **exactly 1 A4 page**).
> This file is the markdown twin of the same text. The 24-article long-form contract is `Team3-…Agreement.docx` and is explicitly **not** the one-pager.

---

## 1 · What we promise

| Commitment | Target | Measured as |
|---|---|---|
| **SLO-1 Departure certainty** | **≥ 99.5 %** (Titanium ≥ 99.9 %, Silver ≥ 99.0 %) | Monthly denominator = all scheduled departures; met when `SoC_dep ≥ required_soc` **and** delay ≤ 0 min, provided MRDT was met. |
| **SLO-2 Terminal availability** | **≥ 99.5 %** | Per-gun minutes available ÷ 720 h/month (per dispenser, not per site). |
| **SLO-3 Off-grid resilience** | **≥ 72 h at full power** | WAN loss per `connectivity_outages.csv`: station holds **1,425 kW DC** (**1,492.15 kW AC ≤ 1,500 kW**, η = 0.955) instead of the 50 kW/dispenser fallback (500 kW). |
| **SLO-4 Grid-limit compliance** | **100 % — no exception** | `P_AC(t) = P_DC(t)/0.955 ≤ P_limit(t)` on the time-varying limit; **0** official over-limit rows in **134,400** intervals is the reference. |
| **SLO-5 Self-healing latency** | **< 10 ms** decide · **85 ms** module · **260 ms** relay | Software decision, intra-cabinet 25 kW module isolation, module relay break-before-make. The macro inter-cabinet re-route is **2.63 s** — a different path, not a faster promise. |

**Carve-outs from the measurement window** (they suspend the clock, they do not lower the bar): an *unannounced* medium-voltage outage or DSO hard curtailment at a site with no storage — `bess_kwh = 0` at all five close-up sites — is excluded from SLO-1/SLO-2 from the instant it occurs; any arrival whose dwell time < MRDT is *best-effort*, not a breach. An *announced* curtailment such as G1 (notified 14:00, active 16:00–19:00) stays inside the promise, because the system has time to re-plan.

**Outside SLO scope by design:** weather, vehicle-side faults, driver arrival lateness below MRDT, and the travel time of a physical module replacement (see §3).

---

## 2 · What the system decides alone

- **How much power each gun gets** — intra-cabinet DPR across 25 kW modules, continuous allocation, strict 1:N wiring as recorded in `chargers.csv`.
- **When and how fast each vehicle charges** — 15-minute rolling MILP (SciPy HiGHS) on `prices.csv` + `fleet_schedule.csv`; the departure deadline is weighted above price, so a feasible vehicle is never dropped to save money.
- **Who gets curtailed when the grid is cut** — e.g. S2 under G1 (notified 14:00, active **16:00–19:00** at 400 kW): overnight trucks T05–T08 throttled with continuous setpoints, **283.50 kWh** shifted to afternoon trucks T01–T04 → **4 → 0** missed.
- **When to isolate, reroute and re-level** — thermal precursor (S1: 59.3 °C / 702 rpm at 22:31, **199 min** lead), N-1 degradation to **720 kW** with 0 kW self-harm, offline islanding.
- **What a station's configured limit actually is** — three-way reconciliation of `network_sites.csv` / `power_cabinets.csv` / `site_config.csv` (S5: 600 → 900 kW, +750 kWh).
- **Whether a claim is payable** — the MRDT gate is evaluated per session before any credit is issued.

`MRDT_j = ΔSoC·E_batt ÷ ( min(P_charger, P_veh)·η_sys ) × 60 + 15 min` → worked example **57.11 min** (`verify_all.py`).

**Human decisions kept by the Client:** site acceptance, tariff/contract parameters, any hardware purchase (§3), and physical repair dispatch. The system never overrides a local safety interlock.

---

## 3 · Accountability when it decides wrong

| Event | Payable by the Service Provider |
|---|---|
| Departure below required SoC / late | **350 €** (Titanium) · **250 €** · **150 €** per trip |
| Delay beyond the tier threshold | **7.50 / 5.00 / 3.00 €/min** (from 10 / 15 / 20 min) |
| Energy shortfall | **2.00 / 1.50 / 1.00 €/kWh** (+ emergency hire in Titanium) |
| Availability below target | **−2 %** of the monthly fee per **0.1 pp** shortfall, capped at **90 %**; **0 %** fee if < 95 % |

- **Hard cap:** aggregate monthly liability = **150 %** of the monthly base fee. Invoices are non-negative; the Client can never be billed back.
- **Client-side guard:** if dwell time < MRDT, the session is *best-effort* and no liquidated damages accrue — the gate that stops an "arrived 10 minutes late with 200 kWh to go" claim.
- **What we do not take liability for:** a cabinet that needs a human on site. `faults.csv` clears **8 of 19** faults with `cleared_by = technician`; those **73** dispatches = **22,906 min** = **5.09 FTE** are **retained, not sold**. Same for **3.22 FTE** of customer contact.
- **Zero-miss boundary, stated:** on 2026-11-13 our zero-CAPEX software takes S1 **4 → 3** missed (**398.5 → 48.8 kWh, −87.8 %**) with **12 → 0** manual replugs. Reaching **0** needs an inter-cabinet busbar tie absent from `chargers.csv` and with **no price** in `equipment_costs.csv` — we hand that number back rather than invent it. Buying 12 dispensers alone (**324,000 €**) yields **8** missed, i.e. worse.

**Why a client signs this:** under the current contracts, three of five close-up sites already breach their own uptime floor — recorded **S1 94.1 %**, **S3 90.0 %**, **S5 87.5 %** vs a **97 %** commitment (`C1`), at **150 €** per undercharged departure = **1,350 €** on the scenario day against a **263 €** daily fee. The penalty is already flowing.

---

**Basis of every number:** unmodified official CSVs — 45 files / 240,635 rows; recomputed by `python verify_all.py` (< 1 s, exit 0) and `tools/export_deck_ledger.py`. Labour baseline **8,852** ops / **93,412** min / **20.76 FTE** at 37.5 h·wk and 45 €/h, of which **12.44 FTE (59.95 %)** is software-addressable. Grid-limit capping is done by a person today — **684** manual load adjustments / **10,260 min**, **100 %** of them at sites breaching their limit (Spearman **0.802**). Assumptions and their error direction: [`assumptions_and_additions.md`](./assumptions_and_additions.md).

| Service Provider | Client |
|---|---|
| name / signature / date | name / signature / date |
