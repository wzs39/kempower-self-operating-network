# Interactive Demonstration Suite (Streamlit 6-Scene Operational Replay)

This directory provides the live interactive demonstration suite for Project Sentinel, featuring six dedicated Streamlit pages that present side-by-side counterfactual replay animations ("Legacy Baseline vs. Project Sentinel") across six operational crisis scenarios.

---

## The Six Operational Crisis Scenarios

| Page Script | Scenario & Title | Ground Truth Data Anchor |
|---|---|---|
| `pages/1_Night_Replay.py` | S1 Bus Depot: Cabinet Overheating (C1-3 F016) & Replugging | 2026-11-13 02:25:00 (Right column shows Tier 3b 24-point hardware architecture) |
| `pages/2_Outage_Replay.py` | S3 Highway Hub: 2-Hour Cellular WAN Blackout | 2026-11-13 11:00–13:00 (Local DLM sustains 1,425 kW DC) |
| `pages/3_Price_Spike_Replay.py` | S2 Freight Depot: 799.30 €/MWh Spot Price Peak | 2026-11-13 17:15–18:45 (Peak 799.30 €/MWh at 18:00) |
| `pages/4_Curtailment_Replay.py` | S2 Logistics Hub: 400 kW DSO Grid Curtailment | 2026-11-13 16:00–19:00 (Grid event G1 clamps capacity to 400 kW) |
| `pages/5_Cable_Fault_Replay.py` | S4 Urban Hub: CCS2 Cable Insulation Breakdown (F017) | 2026-11-13 21:30:00 (40 ms local hardware isolation) |
| `pages/6_Commissioning_Replay.py`| S5 Bus Depot: Three-Way Configuration Reconciliation | Full Day (Resolves 600 kW vs 900 kW parameter conflict) |

Each page features interactive controls: ▶ **Play** / ⏸ **Pause** / ⟲ **Restart**, along with a speed slider and quick jump buttons for live stage walkthroughs.

---

## How to Run Locally

```bash
# 1. Install dependencies
pip install -r demo_scenarios/requirements.txt

# 2. Launch the interactive dashboard (from repository root)
python -m streamlit run demo_scenarios/app.py
```

Open `http://localhost:8501` in any modern web browser and navigate between the six scenarios using the sidebar.

---

## Data Provenance

The simulation engine reads directly from the official Kempower dataset (45 unmodified CSV files) located at `kempower-challenge/kempower-challenge-data/`, automatically resolved via `src/utils/paths.py`. No external network access or data preprocessing is required.

---

## Presentation Pitch Scripts

- [`SPEECH_SIX_SCENES.md`](./SPEECH_SIX_SCENES.md) — Comprehensive 10-minute master pitch script covering all six scenarios with UI operational cues and verbatim narration.
- [`SPEECH_OVERHEAT_SCENE.md`](./SPEECH_OVERHEAT_SCENE.md) — Deep-dive narration, 30-second elevator pitch, numerical fact sheet, and judge Q&A defense for the S1 night replay.
