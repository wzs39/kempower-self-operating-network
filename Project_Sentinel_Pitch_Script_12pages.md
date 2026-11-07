# Project Sentinel — 10-Minute Pitch Script
### Re-segmented for the 12-page deck (`Project_Sentinel_12pages_final.pptx`)

| | |
|---|---|
| Total budget | 10:00 (600 s) |
| Word count | **1,284 words** |
| Timecodes assume | 128 wpm (deliberate, non-native-safe) |
| If you speak 140 wpm | you land at **9:10** — 50 s of air in hand |
| If you speak 150 wpm | you land at **8:33** — too fast, use the pauses |

**Page map:** cover → 2029 night → bottleneck → stack → L2 edge → L1 hardware → gauntlet → S1 honesty → S3+S4 shocks → SLA → ROI ledger → close.

Each block gives you: timecode, word count, what is on screen, the words, and **the line to cut** if you are running long. Cut the marked line; never improvise a new number.

---

## P1 · 0:00 – 0:40 · 87 words · Cover
**On screen:** title, DESIGN PERSPECTIVE block, OUR CUSTOMERS block.

> Good morning. Project Sentinel — the autonomous self-operating charging network.
>
> Three declarations before I start. We are taking the **Manufacturer** row of this challenge: we build the chargers, we service them, we carry the late-departure penalty. Every figure you will see comes from the forty-five synthetic CSVs you supplied — zero bytes modified, twenty assumptions documented and handed to the jury. And our customers are three: city bus operators, logistics fleets, and public charge point operators.
>
> Sentinel is not a monitoring dashboard. It is the operating system underneath one.

**Cut if long:** the customer sentence. (It is on screen; the jury can read it.)
**Do not:** open with "hello my name is" — that burns eight seconds. Name, then the three declarations.

---

## P2 · 0:40 – 1:25 · 84 words · The 2029 night
**On screen:** frozen depot, 24 buses / 12 dispensers, banner "13 of 62 departures below required SoC".

> Friday, the thirteenth of November, 2029. Two fifteen in the morning. Lahti, Finland. Minus eighteen, blizzard.
>
> Twenty-four articulated electric buses parked overnight. Twelve single-gun dispensers. Four to six staff on site — awake, at two a.m., doing manual resets and chasing connection faults.
>
> By six, thirteen of the sixty-two departures leave below required state of charge. The grid limit gets violated. The result, in your own brief: system failure, frequent manual intervention.
>
> This is the night we design against. Not a demo — a Friday shift.

**Pause here.** Two full seconds of silence after "a Friday shift." The room needs to feel the temperature drop. This is the only planned silence in the talk.
**Cut if long:** the "four to six staff" sentence — it is printed bottom-right.

---

## P3 · 1:25 – 2:15 · 113 words · The bottleneck
**On screen:** telemetry chart with the orange "ground truth anomaly" box; 8,852 / 93,412 / 20.76 FTE.

> Here is what that night costs when you multiply it out. Two weeks, one hundred benchmark sites: eight thousand eight hundred and fifty-two manual interventions. Ninety-three thousand four hundred and twelve staff-minutes of midnight replugging, remote resetting, setpoint adjustment. Twenty point seven six full-time equivalents. One point eight two million euros a year.
>
> Now the orange box — this is the honest part. Zero measured violations, **because** three point two five FTE were manually holding the load down. Two thousand and ninety-six hours of demand sat above the limit. The system did not comply. People made it comply.
>
> That is the mission: take the human out of the loop, not out of the payroll.

**Cut if long:** "setpoint adjustment" and "one point eight two million euros a year" — the euro figure repeats on P11.
**Emphasis:** "because" — this sentence buys you credibility for the next nine minutes.

---

## P4 · 2:15 – 3:00 · 100 words · The stack
**On screen:** three-layer pyramid, L1 / L2 / L3.

> One principle, three layers. Physical safety must never depend on the cloud. Global economics must never depend on a local heuristic.
>
> L3, cloud, fifteen-minute rolling horizon: a MILP solved with SciPy HiGHS, day-ahead arbitrage against Nord Pool, and a slack variable priced at ten thousand euros per vehicle — so the optimiser knows what a missed bus is worth.
>
> L2, edge, one hundred milliseconds to fifteen minutes: seventy-two hours of full offline islanding, predictive thermal maintenance, anti-phantom fraud.
>
> L1, hardware, sub-millisecond: the DPR matrix and a six-step break-before-make sequence.
>
> Each layer can fail alone. None of them takes the site down.

**Do not** read the boxes. The jury reads faster than you speak. Say the layer name and the one number that matters.
**Cut if long:** the Nord Pool clause.

---

## P5 · 3:00 – 3:55 · 122 words · L2 edge
**On screen:** left, islanding topology; right, thermal PdM curve 22:00–02:30.

> Two failures L2 has to survive alone.
>
> Left: the WAN dies. A naive system falls back to fifty kilowatts — a safe default that strands seventy-six drivers. Sentinel keeps an append-only encrypted SQLite log on NVMe, goes islanded, and holds one thousand four hundred and twenty-five kilowatts DC locally. Seventy-two hours. Zero downtime.
>
> Right: a fan bearing starts to go. At fifty-nine point three degrees and seven hundred and two RPM, slope extrapolation flags it — one hundred and ninety-nine minutes before the F015 hardware trip. Three hours and nineteen minutes of warning, in the middle of the night. That turns an emergency dispatch into a scheduled visit.
>
> Predictive maintenance is not a feature here. It is how you stop paying for two a.m.

**Emphasis:** "one hundred and ninety-nine minutes" — slow it down, it is the most concrete number in the deck.
**Cut if long:** the RPM figure.

---

## P6 · 3:55 – 4:40 · 102 words · L1 hardware
**On screen:** cabinet, unidirectional flow, 6-step timeline, hard interlocks.

> This is the page that matters most to a manufacturer.
>
> Twelve guns, twenty-four buses. The obvious move is to double the guns. The physics says otherwise — and I will show you that arithmetic in two pages.
>
> What we do instead is **switch**. Six steps: disconnect, discharge, verify, configure, engage, power flow. Software decides in under ten milliseconds. The physical break-before-make completes in eighty-five milliseconds, inside a two-hundred-and-sixty-millisecond envelope. Zero illegal backfeeds — unidirectional by wiring, not by software promise.
>
> And the interlocks are hardware: sixty-five degree de-rate, seventy-five degree trip, thirty milliamp RCD, IMD protection. Nothing here asks the cloud for permission.

**Bridge line:** "in two pages" — it creates a debt the audience wants paid. Pay it on P8.

---

## P7 · 4:40 – 5:40 · 132 words · The gauntlet
**On screen:** S1–S5 table, baseline vs Sentinel, bottom line 0.34 s / 539 tests / 0 CSV bytes.

> Five crises, one day. Friday the thirteenth, replayed against the baseline.
>
> S1, depot cable cap: baseline misses four departures. Sentinel misses **three**, with eighty-seven point eight percent less energy deficit. Not zero — three.
>
> S2, four hundred kilowatt curtailment: four missed becomes zero. Overnight trucks drop to one kilowatt; one thousand eight hundred and fifty-seven kilowatt-hours come back.
>
> S3, WAN loss: twenty-nine point six percent of sessions abandoned becomes under half a percent, holding one thousand four hundred and twenty-five kilowatts locally.
>
> S4, a seven-hundred-and-ninety-nine euro price spike: absorbed, no SLA breach.
>
> S5, a config conflict — six hundred against nine hundred kilowatts: five missed becomes zero, plus seven hundred and fifty kilowatts unlocked.
>
> Bottom line: zero point three four seconds to verify, five hundred and thirty-nine tests, and not one CSV byte changed.

**This is a list. Do not read it like a list.** Beat after every row, eyes on the Sentinel column, not the text.
**Cut if long:** S2's 1,857 kWh detail, then S5's +750 kW. Never cut S1 or S4.

---

## P8 · 5:40 – 6:45 · 140 words · Engineering honesty (S1)
**On screen:** three tiers, €324,000 failure, unpriced busbar path.

> Now the page I would attack if I were sitting where you are.
>
> S1: twenty-four buses, twelve guns, twelve hundred kilowatt cap. Baseline, four missed departures. Tier two is our software, zero capex: urgency-weighted scheduling cuts the energy deficit by eighty-seven point eight percent and takes four down to three. Zero human replugs.
>
> Tier three: add twelve more plugs. Three hundred and twenty-four thousand euros of capex. The cabinet power splits — ninety kilowatt guns become forty-five — and it gets **worse**. Eight missed departures.
>
> So the only monotone path to zero misses is a cross-cabinet busbar tie, to hold one thousand and eighty kilowatts across twenty-four guns. It is not on your price list. We are not going to invent a number for it.
>
> We sell the eighty-seven point eight percent, and we say out loud what we cannot sell.

**Slowest page in the deck.** 65 seconds for 140 words means deliberate pauses at each "Tier".
**The strategic point:** you are the only team that will stand here and say "adding guns makes it worse." That is the whole pitch. Do not rush it.
**Cut if long:** nothing. If you must, shorten the busbar sentence to "and it is not on your price list."

---

## P9 · 6:45 – 7:40 · 117 words · External shocks
**On screen:** left S3 power hold, right S4 real price curve with the 18:00 peak.

> Two external shocks, in detail.
>
> Left, S3. The cellular link drops at a highway hub. The naive fallback is fifty kilowatts. We override it: one thousand four hundred and twenty-five kilowatts DC, one thousand four hundred and ninety-two AC, under the fifteen-hundred ceiling, continuously. Seventy-six stranded drivers do not happen.
>
> Right, S4. Look at the clock — the spike is at eighteen hundred: seven hundred and ninety-nine euros thirty per megawatt-hour. Fourteen times the day's median of fifty-six fifty-five. A binary system cuts power and abandons the car.
>
> We do not cut. The SoC slack variable — z-v between zero and one — scales demand down smoothly. Seventeen point four three percent lower energy cost, and not one abandoned session.

**Point at the peak.** Physically raise a hand toward the 18:00 spike. The chart is real data; make the jury notice that.
**Cut if long:** the median figure.

---

## P10 · 7:40 – 8:30 · 105 words · What we sell
**On screen:** one-page SLA cube, Titanium tier, 150% cap, MRDT gate.

> So what do we actually sell? Not chargers. Energy certainty, as a contract.
>
> Titanium tier: ninety-nine point nine zero service level, zero-touch replugging, sub-fifty-millisecond reaction. Liability capped at one hundred and fifty percent of the monthly fee — we put our money behind the number.
>
> And the clause that makes it survivable: the anti-moral-hazard gate. A customer cannot claim a penalty if they unplug early. The MRDT algorithm computes the physical minimum dwell time for the energy they requested — battery capacity, charger constraint, plus a fifteen-minute buffer. It prices the promise against physics, not against optimism.
>
> That is the difference between an SLA and a slogan.

**Tone shift:** this is the commercial page. Slow down, drop the engineering cadence.
**Cut if long:** the fifteen-minute buffer detail.

---

## P11 · 8:30 – 9:30 · 133 words · ROI ledger
**On screen:** 20.76 → 12.44 (9.95 + 2.50) / 5.09 / bottom reconciliation line.

> Which brings the ledger. Honest attribution.
>
> Twenty point seven six FTE is the total bottleneck, one point eight two million a year. Software can only eat part of it.
>
> Twelve point four four FTE is software-addressable — fifty-nine point nine five percent. Inside that: nine point nine five from eliminating midnight replugging and yard moves, five thousand five hundred and ninety-six events; two point five from remote load, reset and price commands.
>
> What we do **not** claim: five point zero nine FTE of technician dispatches — seventy-three of them. Software does not turn wrenches. We keep that cost and price it into the SLA. And three point two two FTE of customer contact.
>
> Twenty point seven six equals twelve point four four, plus five point zero nine, plus three point two two. The arithmetic closes.

**Point at the bottom line** on "the arithmetic closes." Most teams hand-wave this split; you close it in public.
**Cut if long:** the 5,596 events figure.

---

## P12 · 9:30 – 10:00 · 49 words · Close
**On screen:** 100% SoC, depot lit up, bottom-left "Pekka wakes up / No calls."

> Kempower already builds the best modular DC hardware in the market. What is missing is a brain that does not need a night shift.
>
> Lahti. January 2029. Six in the morning. Pekka wakes up.
>
> *(beat — two seconds)*
>
> No calls.
>
> Thirteen missed departures become three. Zero capital expenditure. Zero additional headcount. Thank you.

**Do not** say "No calls" fast. It is the last thing they hear. Land it, stop moving, hold the slide for three seconds before you invite questions. This block is deliberately only 49 words — the silence is the content.

---

## Timing control

| If you are at | and the clock says | do this |
|---|---|---|
| P5 | past 4:00 | skip the RPM figure, drop the PdM "feature" line |
| P7 | past 5:50 | read only S1, S3, S4 — say "S2 and S5 are on the page" |
| P8 | past 6:55 | compress to: "Tier three costs 324k and makes it worse. We sell 87.8%." |
| P11 | past 9:05 | say only "12.44 is ours, 5.09 is technicians, 3.22 is contact — it closes" |

**Never cut:** P8 (honesty), P12 (Pekka). Those two are why this deck wins instead of ties.

## Numbers you must not improvise

- S1: **4 → 3 missed**, −87.8% energy deficit. Never "zero missed."
- S1 Tier 3a: €324,000, **8 missed — worse**. 90 kW guns drop to 45 kW.
- S3: 1,425 kW DC / 1,492 kW AC, ceiling 1,500. Abandonment 29.6% → <0.5%.
- S4: peak **€799.30/MWh at 18:00**, median 56.55, 14×, −17.43% cost.
- BBM: <10 ms decision, **85 ms** physical, **<260 ms** envelope.
- PdM: 199 min lead, 59.3 °C / 702 RPM, window 22:00–02:30.
- ROI: 20.76 = 12.44 + 5.09 + 3.22. Software share 59.95%.
- Tests: 0.34 s verify, 539 tests (433 pytest + 106 E2E), 0 CSV bytes modified.

## Q&A — three answers to have loaded

1. **"Where is the AI?"** — It is not a trained model, and we will not pretend it is. It is a closed loop: a MILP re-solved every 15 minutes against a real price series, plus an edge finite-state machine that decides in under 10 ms. The intelligence is in the objective function and the slack pricing, not in a neural net. `docs/assumptions_and_additions.md` lists what is modelled and what is not.
2. **"Why not just add guns?"** — Page 8 is the answer: €324k, cabinet power splits, 4 missed becomes 8. Gun count is not the constraint; cabinet power and cable topology are.
3. **"Is 20.76 FTE real?"** — It is your own telemetry, 14 days, 100 sites. We only claim 12.44 of it. The other 8.31 we hand back to you unpriced.
