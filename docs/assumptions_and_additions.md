# What We Added, and Every Assumption We Made

> **Why this file exists.** The brief asks, verbatim: *"Saturday: one list of all you added and every assumption."* This is that list. It is intentionally unflattering: anything a judge can challenge is written down here first, with the direction of the error and how to check it.
>
> **Scope.** The 45 official CSV files under `kempower-challenge-data/` are read-only and unmodified (`git status` on that directory is empty; `verify_all.py` asserts 45 files / 240,635 rows). Everything below is either (a) an assumption made *on top of* that data, or (b) an artefact *we added* to the repository.

---

## 1. Assumptions (22)

Legend for **Direction** — `optimistic` means our headline result would get *worse* if the assumption is wrong; `neutral` means it does not move the S1/S2/S5 ledger.

| # | Assumption | Value used | Basis / reason | Direction | Where |
|---|---|---|---|---|---|
| **A1** | CV taper above 80% SoC | `SOC_TAPER_START=0.80`, `TAPER_EXP=1.2`, `TAPER_DEPTH=0.90` | Kempower DC charging is roughly constant-current to ~80% SoC, then CV; exact cell curve is not in the dataset | optimistic (a flatter taper would deliver more kWh) | `src/sim/discrete_sim.py` |
| **A2** | AC↔DC inverter efficiency | `η = 0.955` | Used to reconcile S3's `1,425 kW DC` against the `1,500 kW AC` transformer and to audit `delivered_kw/0.955` | neutral | `docs/energy_impact.md` §2.1 |
| **A3** | Simulation time step | 1 min; official 15-min series linearly interpolated | `prices.csv` / `site_power_baseline.csv` are 15-min; minute resolution is needed for departure deadlines | neutral | `src/sim/discrete_sim.py` |
| **A4** | **No cross-cabinet busbar at S1** (`cross_tie=False` on the verified path) | 12 guns, 3×360 kW, 1:1 gun→cabinet | `chargers.csv` binds every charger to exactly one cabinet; no official file describes a busbar | neutral (it is why Tier 2 stops at 3 missed) | `src/sim/discrete_sim.py` |
| **A5** | Every S1 gun rated 150 kW | `gun_kw=150` | `chargers.csv max_kw = 150` for `D1-1..D1-12`; cabinet total 1,080 kW < 1,200 kW grid | neutral | `chargers.csv` |
| **A6** | S1 job set = **32 shifts departing 2026-11-13** | incl. 24 buses arriving 19:00–23:59 the previous night | Selection is by `depart_ts` date, not arrival hour — filtering by arrival hour silently dropped `B15` (arrives 18:58, SoC 8%) | neutral (corrected) | `load_fleet_jobs(..., depart_date="2026-11-13")` |
| **A7** | `F016` removes cabinet `C1-3` from 02:25 for 246 min | site capacity 1,080 → 720 kW | `faults.csv` F016 `cleared_by=technician`, cleared 06:31 | neutral | `verify_all.py` |
| **A8** | **`F015` (C1-3 de-rated 50% for 35 min from 01:50) is NOT modelled** | — | Two overlapping faults on the same cabinet inside 35 min; we model the trip only | **optimistic ≈ 105 kWh** | not modelled — this row |
| **A9** | S2 job scope = **8 trucks arriving 14:20–14:45** | `T01–T08`, `need = 2,784 kWh` | The G1 curtailment crisis is an afternoon-departure problem; `T09–T14` and the 23:00 repeats depart 06:00 next day | optimistic (sim covers ≈47% of S2's 5.96 MWh day) | `simulate_closed_loop_minute_by_minute("S2")` |
| **A10** | S2 electrical topology | 2×400 kW cabinets, 8 guns @ 300 kW, grid 800 kW, `G1` cap 400 kW `16:00–19:00` | `power_cabinets.csv`, `vehicles.csv max_charge_kw`, `grid_events.csv G1` | neutral | `src/sim/discrete_sim.py` |
| **A11** | S5 job set = **12 buses arriving 2026-11-12 19:44–23:04**, departing 05:30–06:15 | — | `fleet_schedule.csv` for S5 on those dates | neutral | `load_fleet_jobs("S5", night_only=True, depart_date="2026-11-13")` |
| **A12** | S5 misconfiguration = `grid_limit 600 kW` + `D5-7 @ 50 kW` + `D5-8 inactive` | 7 usable guns | `site_config.csv` rows 164 & 191–196 | neutral | `src/sim/discrete_sim.py` |
| **A13** | **S5 plug-queueing / operator batch-swap delay is NOT modelled** | engine reproduces **1 of the 5** official failures (`B35`) | The official record shows 5 buses below required SoC; our engine grants any free gun immediately, so it is less pessimistic than reality | **optimistic** — this is why S5 is labelled a *config fix*, not a same-engine A/B | `README.md` † table |
| **A14** | Fleet vehicles never abandon; they queue for a free gun | — | Fleet buses/trucks wait; only `public_arrivals.csv` records abandonment | neutral | `src/sim/discrete_sim.py` |
| **A15** | Power is allocated continuously (1 kW resolution) | no 25 kW module quantisation inside a cabinet | `DPRMatrix` modules are 25 kW, but intra-cabinet DPR is modelled as a continuous budget | optimistic | `docs/attribution_matrix.md` |
| **A16** | FTE annualisation | `93,412 min / (37.5 h × 2 wk)` = **20.76 FTE**; 1,950 h/yr; `45 €/h` = `87,750 €/FTE/yr` | Finnish statutory 37.5 h/week, `equipment_costs.csv` | neutral | `src/commercial/roi_analyzer.py` |
| **A17** | Tier-3 hardware price | `27,000 €/gun` = `18,000` dispenser + `9,000` civil → `324,000 €` for 12 guns | `equipment_costs.csv`; **the cross-cabinet busbar is not priced anywhere in the dataset, so the monotone zero-miss path has no quote** (the priced alternative, `3×450 kW` = `270 kW × 280 €/kW` = `75,600 €`, reaches `0` only when the `1,200 kW` cap is enforced, and is non-monotonic) | neutral | `verify_all.py`, `docs/attribution_matrix.md` Option 5 |
| **A18** | Energy price = supplied `prices.csv` spot + `tariffs.csv` grid tariff, 15-min (the brief states prices are **synthetic**; we consume the provided series, not a live exchange feed) | no taxes, no DSO variable fees, no imbalance settlement | Only these two series exist in the dataset | neutral | `docs/energy_impact.md` Table 1A |
| **A19** | **Every undercharged departure counts as one `penalty_eur_per_late_departure` event** | `150 € × 4 (S1) + 150 € × 5 (S5)` = **`1,350 €`** vs `263 €` daily fee | `contracts.csv` `C1` gives the rate (`150 €`) and `baseline_kpis.csv` gives `departures_below_required_soc` (4 / 5), but **no file states the trigger clause** — we read "left below required SoC" as "left late" | **optimistic** — if the contract only pays on clock-time lateness, this number is an upper bound | `PITCH_DECK_OUTLINE.md` slide 7 |
| **A20** | **The penalty is payable by the supplier, not by the site owner** | the exposure sits on our side of the contract | `contracts.csv` gives a rate per customer but **names no payer**. The data README says the supplier `delivers and services the chargers at all sites`, so we read the penalty as its liability. Note **`7` of the `18` penalty-bearing contracts are pure `hardware`** — the exposure is not tied to the service tier, which strengthens this reading | **optimistic** for us — if the penalty actually falls on the fleet, our commercial case loses its cash-flow anchor and only the `5.09 FTE` technician line remains | `README.md` design-perspective block, `PITCH` slide 7 |
| **A21** | **One basis per claim for S3 abandonment** — the day figure `29.69 %` (`76/256`) and the in-window figure `44.83 %` (`13/29`) are both **row-level** `public_arrivals.csv` and may be quoted together; the `15`-min aggregate `network_site_power.csv` gives `46.88 %` (`15/32`) for the same window and is reported separately | `44.83 %` in-window (row level) | Two official files count arrivals on different grids (per-session vs per-15-min bucket); they differ by 2 events | neutral (it is a presentation-basis guard, not a result) | `tools/export_deck_ledger.py` → `sites.S3.window_basis`, `README.md`, `docs/hackathon/DEMO_SCRIPT.md` |
| **A22** | **One timer per sentence: the verifier's own timed section vs the process wall clock are different numbers and are never blended** | timed section **0.36-0.38 s** warm / **0.49 s** cold; `python verify_all.py` **wall clock 1.5-1.8 s** (Python interpreter + pandas import dominate). Pytest **45-46 s** for 434 tests; E2E **0.7-1.3 s** for 106. Measured, not inherited | `0.38 s` and `1.5 s` are both true answers to different questions, and a jury that times us with `time python verify_all.py` will not read 0.38 s. Any earlier figure quoted here without saying which timer it came from is the mistake this row exists to stop | **neutral** (it moves no ledger row, only what we are allowed to say out loud) | this row; `verify_all.py` prints its own section timer, README/HACKATHON/TEST_READY quote both |

Not modelled, stated rather than hidden: **`F015`** (A8), **S5 queueing** (A13), **BESS** (`bess_kwh = 0` at all five sites — we do not claim storage arbitrage), **protocol conformance on real hardware** (OCPP 2.0.1 / ISO 15118 code paths are implemented and unit-tested, never field-validated), and the **`< 10 ms` / `85 ms` BBM envelope** (a design target from the DPR module spec, not a measurement).

---

## 2. What We Added

### 2.1 Code (all of it ours; no dataset file is written to)

| Artefact | What it is | Why it is not "the dataset" |
|---|---|---|
| `src/sim/discrete_sim.py` | Minute-by-minute closed-loop discrete-event simulator (taper, DPR, waterfilling, BBM replug, SoC trajectories) | The dataset has no simulator; every kWh number we publish comes from here |
| `src/sim/scenario_engine.py` | S1–S5 scenario harness + ledger | Scenario logic, not data |
| `src/sim/data_loader.py` | Read-only CSV loader + invariant checks | — |
| `src/core/dpr_matrix.py` | Kempower 25 kW module matrix, intra/inter-cabinet allocation, break-before-make sequencing | — |
| `src/core/self_healing.py` | Edge FSM: thermal PdM, N-1 degradation, offline islanding | — |
| `src/core/virtual_replug.py` | 0-CAPEX virtual replug (Tier 1/2/3) | — |
| `src/core/mpc_optimizer.py` | 15-min rolling-horizon MILP (SciPy HiGHS) | — |
| `src/commercial/*` | SLA calculator (MRDT, liquidated damages) + ROI/labour analyser | — |
| `app.py` | 4-view Streamlit cockpit with minute playback | — |
| `verify_all.py` | Deterministic < 1 s verifier (the entry point a judge should run) | — |
| `tests/` (434) + `e2e_tests/` (106) | 540 tests, including an opaque-box E2E suite | — |

### 2.2 Documents and narrative

- `docs/energy_impact.md` (energy/grid ledger), `docs/attribution_matrix.md` (16-cell fault × strategy × topology matrix), `docs/hackathon/*` (submission pack).
- **Two SLA documents with different roles, stated so they are never confused**: `docs/one_page_agreement.md` / `.html` is the **one-page service agreement handed to the jury** (verified to print on exactly one A4 page); `One_Page_SLA_Specification.md` is the **long-form 2029 story + tiered SLA specification** behind it and is *not* the one-pager.
- **A fictional 2029 customer story** (Pekka Virtanen / Lahti City Transit). It is a narrative device, **not a reference customer**, and no number in it is a forecast.

### 2.3 Explicitly *not* added

- No hardware, no extra chargers on the verified path, **no BESS** (`bess_kwh = 0` everywhere in `network_sites.csv`).
- No modification of the 45 official CSVs, and no derived CSV committed as if it were official.
- The `324,000 €` / 24-plug Tier 3 is a **priced counterfactual** (it makes S1 *worse*: 8 missed). It is not part of our result.

---

## 3. The one number that is an estimate, not a simulation output

`docs/energy_impact.md` Table 1A reports S2 at **429.01 €/day** (`−260.06 €`). That figure is an analytic estimate, not engine output:  `600 kWh × [(485.63 + 24.00) − (52.20 + 24.00)] €/MWh`. The engine emits kWh only (`Table 1B`: `278.9 → 0.0 kWh`, `4 → 0 missed`). Every other € in Table 1A is an integral of the official price and baseline series.
