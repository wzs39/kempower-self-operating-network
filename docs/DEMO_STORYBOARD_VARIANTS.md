# Demonstration Video Variants: Architectural Evaluation (A Panorama / B Dual-Cut / C Slow-Motion)

**Upstream Document**: [`DEMO_STORYBOARD.md`](DEMO_STORYBOARD.md)  
**Challenge Constraint**: *"Run the scenario day (Fri 13.11.) without human intervention, including at least one failure and one electricity price event"* (Duration window 60–120s selected by team).  
**Common Architecture**: All three versions share the same deterministic `trace` telemetry, the same 6-grid layout, and the same color palette. Switching variants requires only adjusting the render timeline schedule.

---

## 1. Comparative Evaluation Matrix

| Metric | Version A (Panorama) | Version B (Dual-Cut) | Version C (Slow-Motion, Shipped) |
|---|---|---|---|
| **Total Duration** | 92 s · Single file | 90 s + 30 s = **120 s** · Two files | **75 s (Shipped) / 98 s (Extended)** |
| **Shot Count** | 8 shots | 7 + 4 shots | 8 shots (Shot 3 divided into 3 movements) |
| **Station Coverage** | 5 / 5 detailed stations | 3 / 5 detailed stations | 5 / 5 detailed stations |
| **"The Four Hours" Focus** | 18 s (Technician appears for 1 s) | 24 s | **24 s (Final 7 s static focus on technician boundary)** |
| **Hardware Faults** | F015 + F016 + F017 | F016 + F017 | F015 + F016 + F017 |
| **Electricity Price Events** | 18:00 spot peak at 799.30 €/MWh | 18:00 peak in auxiliary video | 18:00 peak in master timeline |
| **S3 Islanded Autonomy** | Included (10 s) | Excluded | Included (10 s) |
| **Key Trade-Off** | Shot 1 too long, key argument thin | Risks jury missing auxiliary video | Tightest focus on core technical thesis |

---

## 2. Version A · Panorama Edition (92 s)

**Design Thesis**: Play through the full 24 hours of Friday 13.11 with equal real estate allocated to all five stations.

| # | Timecode | Duration | Visual Narrative | Subtitle Overlay |
|---|---|---|---|---|
| 0 | 00:00 | 8 s | Fade in from black | `Fri 13.11.2026 · 0 people on shift` |
| 1 | 00:08 | 14 s | Six-grid layout; S1 24 buses arrive; 20:38 first `WAIT` | `18:00 → 00:00 · 24 buses · 12 guns` |
| 2 | 00:22 | 12 s | Zoom into S1: 01:50 derate; 02:25 cabinet trip | `One cabinet = ⅓ of power, ⅓ of guns` |
| 3 | 00:34 | 18 s | The four hours (02:25 → 06:40) | `06:31 technician on site · 4 h 06 min later` |
| 4 | 00:52 | 12 s | Full-screen comparison: 0 / 4 / 3 departures | `same engine · same 12 guns` |
| 5 | 01:04 | 10 s | S3 WAN outage 11:00–13:00; 0 session drops | `the site kept running` |
| 6 | 01:14 | 10 s | S2 DSO curtailment + spot price spike | `400 kW honoured · 600 kWh → 22:00` |
| 7 | 01:24 | 8 s | Summary tally: `13 → 3` + F017 physical boundary | `One thing we did not solve.` |

**Strengths**: Every judging dimension is visually represented in at least one keyframe.  
**Weaknesses**: Shot 1 devotes 14 seconds to setting up the grid, while Shot 3's core argument (human technician arrives 1 minute after the last bus departs) receives only 1 second of screen time.

---

## 3. Version B · Dual-Cut Edition (90 s Master + 30 s Auxiliary)

**Design Thesis**: Focus the master video exclusively on Depot S1's overnight drama, delegating energy market arbitrage and configuration reconciliation to a secondary clip.

- **Master Cut (75–90 s)**: `demo/presentation_demo.mp4` — Dedicated to S1's overnight replug elimination, C1-3 thermal trip, and morning roll-out.
- **Auxiliary Cut (30 s)**: Rapid overview of S2 price spike and S5 configuration auto-calibration.

**Strengths**: Deep, emotional storytelling around the overnight blizzard and technician arrival.  
**Weaknesses**: If evaluators review only the primary file, they miss S3's islanded autonomy and S2's spot price arbitrage.

---

## 4. Version C · Slow-Motion Edition (Selected Shipped Cut: 75 s)

**Design Thesis**: Retain all five stations, but reallocate timing weights to emphasize the core technical breakthrough:
- Shot 1 compressed to 10 seconds to eliminate dead setup time.
- Shot 3 expanded to 24 seconds with a 3-movement breakdown:
  1. Incident onset: C1-3 thermal trip at 02:25.
  2. Autonomous self-healing: BBM busbar relay power transfer in < 260ms.
  3. Physical boundary proof: Technician arrives at 06:31 (`cleared_by = technician`), proving scheduled maintenance is preserved while daily operational reliance is eliminated.
- S3 cellular blackout and S2 spot price peak integrated into crisp 10-second segments.

**Final Certification**: Shipped to `demo/presentation_demo.mp4` (75.0s, 1080p@30fps, H.264, silent) and embedded directly into Slide 6 of `Project_Sentinel_12pages_final.pptx`.
