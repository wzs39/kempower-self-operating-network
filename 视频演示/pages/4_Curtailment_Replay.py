"""
Grid Curtailment Replay — S2 logistics depot, 2026-11-13 14:00 → 19:30.

Independent scene: *no price spike is shown here*. The DSO caps the site at
400 kW between 16:00 and 19:00. Baseline keeps feeding the overnight trucks;
Sentinel gives the 400 kW to the trucks that must leave at 17:30–18:15.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[2]  # repo root: the demo shares the single authoritative src/ engine
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.sim.fault_replays import (  # noqa: E402
    CURTAIL_END,
    CURTAIL_START,
    build_curtailment_replays,
)
from src.ui.replay_scene import SceneSpec, render_scene  # noqa: E402

st.set_page_config(page_title="Curtailment Replay — Kempower", layout="wide")


@st.cache_data(show_spinner="Simulating the curtailment scene: 8 trucks x 5.5 h x 2 strategies…")
def _build():
    return build_curtailment_replays()


SPEC = SceneSpec(
    key="curtail",
    title="400 kW is not the problem. Who gets it is.",
    subtitle="Kempower self-operating network · S2 logistics depot · 2026-11-13 14:00 → 21:00 · grid event only",
    events=[
        (datetime.fromisoformat("2026-11-13T14:00:00+02:00"), "info",
         "DSO notice arrives", "G1 warning: a 400 kW cap will start at 16:00."),
        (datetime.fromisoformat("2026-11-13T14:20:00+02:00"), "info",
         "8 trucks plug in", "Four leave at 17:30–18:15; four leave the next morning."),
        (CURTAIL_START, "critical",
         "400 kW cap starts", "Station is cut from 800 kW to 400 kW for three hours."),
        (datetime.fromisoformat("2026-11-13T17:30:00+02:00"), "warn",
         "T01 must leave", "Baseline has been feeding the overnight trucks, not the deadline."),
        (CURTAIL_END, "info",
         "Cap lifts", "800 kW returns; the flexible trucks finish the night at full power."),
        (datetime.fromisoformat("2026-11-13T21:00:00+02:00"), "info",
         "Scene closes", "Baseline is still four trucks short. Sentinel has all eight full."),
    ],
    build=_build,
    left_title="Overnight trucks keep the 400 kW",
    right_title="Deadline trucks preempt the flexible",
    jumps={
        "Start": "14:00",
        "Notice": "14:00",
        "Cap": "16:00",
        "T01 leaves": "17:30",
        "Cap ends": "19:00",
        "Close": "21:00",
    },
    footnote=(
        "<b>How honest is this?</b> Both panels replay the same 8 trucks and the same 400 kW cap from "
        "<code>grid_events.csv</code>. The baseline models the operator habit recorded in "
        "<code>sessions_baseline.csv</code> — the overnight trucks that plugged in first simply keep their power "
        "and nobody preempts them — which is what starves T01–T04 on the scenario day. Sentinel re-sorts the same "
        "400 kW by departure urgency. The left panel reproduces the official 4 short departures; the right panel "
        "keeps all 8 trucks on time."
    ),
)

render_scene(SPEC, kind="fleet", cap_kw=800.0)
