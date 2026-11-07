# Demo Storyboard — Master Keynote Video: `demo/presentation_demo.mp4` (75 s, 1920x1080@30fps, silent)

**Title**: `Five sites, one day · without people in the loop`  
**Duration**: 75 seconds | 1920×1080 Full HD | 30 fps | Zero Voiceover | Silent Minimalist  
**One-Line Positioning**: Rather than a generic system overview, this video replays the crisis events of **Friday 2026-11-13** without human operators on site, visually proving to judges what the autonomous system resolves and honestly identifying physical boundaries.

> This video stands in direct counterpoint to the official kickoff video `Kempower_video1.mp4` (65 s, `Five sites, one night · today, with people in the loop`): processing the exact same data, the exact same site layout, and the exact same night, with the sole difference being that human workers are removed from continuous loops.

---

## 0. Official Challenge Red Lines & Compliance

| Hackathon Constraint | Official Source | Project Sentinel Compliance |
|---|---|---|
| Replay **Scenario Day (Fri 13.11)** | `kempower-challenge-data/README.md:62` | Complete timeline spans 2026-11-13 00:00–23:59 |
| **Zero Human Intervention** | Same as above | Verified `0 manual moves`; all replug fields = 0 |
| At least **one hardware fault** | Same as above | F015 $\to$ F016 (S1 cabinet thermal trip) and F017 (S4 cable insulation failure) |
| At least **one electricity price event** | Same as above | 18:00 spot price peak at 799.30 €/MWh |
| Focus on detailed sites or network | Same as above | Five detailed inspection sites (S1 through S5) |
| Indicate **which architectural layer decides** | Brief p.1 | Explicit visual badges indicating `EDGE` vs. `CLOUD` decision layers |
| Transparently disclose **where humans remain** | Judging Rubric (Autonomy 25%) | Discloses daytime scheduled technician dispatch (4h 06min) and physical cable replacement |

**Production Prohibitions**:
- No intrusive voiceover or distracting music.
- No synthetic marketing animations; every rendered metric is deterministically computed from the 45 CSV files.

---

## 1. Technical Specifications

| Specification | Value |
|---|---|
| Resolution / Frame Rate | 1920×1080 Full HD / 30.0 fps |
| Total Frame Count | 2,250 frames (75.0 s × 30 fps) |
| Codec & Format | H.264, `yuv420p`, CRF 20, Silent (0 audio tracks) |
| Typography | `DejaVu Sans` / `DejaVu Sans Mono` for tabular metrics |
| Deliverable Paths | `demo/presentation_demo.mp4` + `demo/presentation_demo_poster.png` |

### Color Palette

| Semantic Role | Hex Code | Visual Application |
|---|---|---|
| Deep Basalt Background | `#0B1016` | Main canvas background |
| Dark Panel Slate | `#131B24` | Station summary card container |
| Structural Divider | `#1E2A36` | Grid demarcation lines |
| Dynamic Power Active | `#00C2A8` | Power bars, on-target charging status |
| Warning / Derate | `#F5A623` | Predictive thermal derate F015, DSO curtailment |
| Hardware Fault Trip | `#FF4D4F` | Cabinet trip F016, cable trip F017, undercharge alerts |
| Islanded Offline Mode | `#8B5CF6` | S3 cellular WAN loss status indicator |

---

## 2. Master Shot-by-Shot Progression

### Shot 1: The Midnight Baseline (0:00 – 0:12)
- **Visuals**: S1 bus depot overview. 24 electric transit buses returned to base.
- **Narrative Overlay**: S1 operates 24 buses against 12 physical charging dispensers.
- **Autonomous Action**: Dual-satellite topology provides dedicated connection points for all 24 buses; evening drivers self-plug upon parking. Zero midnight replug labor required.

### Shot 2: Sub-Zero Preconditioning & Night Charging (0:12 – 0:25)
- **Visuals**: Ambient temperature drops to -18°C.
- **Autonomous Action**: Edge controller diverts 50 kW per bus to onboard PTC heating circuits, warming LFP cells to 15°C optimal absorption before ramping to full power.

### Shot 3: Cabinet C1-3 Overheating & BBM Power Shift (0:25 – 0:40)
- **Visuals**: 02:25:00. Cabinet C1-3 trips due to overtemperature (predicted 199 minutes prior at 22:31).
- **Autonomous Action**: 260ms Break-Before-Make relay matrix shifts load to healthy cabinets C1-1 and C1-2. Site derates from 1,080 kW to 720 kW. By 02:31, all 24 buses are 100% full.

### Shot 4: S3 Cellular WAN Blackout (0:40 – 0:52)
- **Visuals**: 11:00–13:00. Cellular tower data link fails completely at highway hub S3.
- **Autonomous Action**: Edge controller executes local Dynamic Load Management (DLM), maintaining 1,425 kW DC (1,492.15 kW AC $\le$ 1,500 kW grid cap at $\eta=0.955$). All 10 dispensers remain fully powered; zero drivers stranded.

### Shot 5: S2 Spot Price Peak & DSO Curtailment (0:52 – 1:05)
- **Visuals**: 16:00 DSO clamps grid to 400 kW; 18:00 spot price surges to 799.30 €/MWh.
- **Autonomous Action**: Urgency waterfilling prioritizes departing trucks T01–T04 to 100% full; overnight trucks T05–T08 pause charging and resume at 22:00 (52 €/MWh). Zero missed departures; 47.5% electricity bill savings.

### Shot 6: Morning Roll-Out & Certified SLA Outcome (1:05 – 1:15)
- **Visuals**: 06:30 morning dispatch across all 5 stations.
- **Outcome**: 0 missed departures, 0 grid violations, 0 manual midnight moves. Outcome-based CaaS SLA delivered.
