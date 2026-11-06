"""
Cable Fault Replay — S4 city hub, 2026-11-13 20:00 → 23:59.

Independent scene: the D4-2 cable is damaged at 21:30. The difference is not
throughput — the hub is not saturated at that hour — it is the response time and
the recovery workflow. Both panels lock the gun out; only Sentinel does it in
40 ms, opens the service ticket itself, and keeps the other 7 guns running.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.sim.fault_replays import CABLE_FAULT_TS, build_cable_replays  # noqa: E402
from src.ui.replay_scene import SceneSpec, render_scene  # noqa: E402

st.set_page_config(page_title="Cable Fault Replay — Kempower", layout="wide")


@st.cache_data(show_spinner="Simulating the cable scene: 17 arrivals x 4 h x 2 strategies…")
def _build():
    return build_cable_replays()


SPEC = SceneSpec(
    key="cable",
    title="A damaged cable is a 40 ms decision, not a 30 s wait",
    subtitle="Kempower self-operating network · S4 city hub · 2026-11-13 20:00 → 23:59 · connector fault only",
    events=[
        (datetime.fromisoformat("2026-11-13T20:15:00+02:00"), "info",
         "Evening arrivals", "Cars and taxis keep coming through the 8-gun city hub."),
        (CABLE_FAULT_TS, "critical",
         "D4-2 cable damage", "F017: connector fault, dispenser locked out for safety."),
        (datetime.fromisoformat("2026-11-13T21:31:00+02:00"), "warn",
         "Seven guns stay alive", "Station keeps 600 kW available; only one post is dark."),
        (datetime.fromisoformat("2026-11-13T22:00:00+02:00"), "info",
         "Service continues", "Both panels complete the same 14 of 17 arrivals; the fault adds no extra loss."),
        (datetime.fromisoformat("2026-11-13T23:59:00+02:00"), "info",
         "Scene closes", "Technician ticket is already in the system; nothing else to do tonight."),
    ],
    build=_build,
    left_title="Cloud ticket, manual follow-up",
    right_title="40 ms local lockout + reroute",
    jumps={
        "Start": "20:00",
        "Fault": "21:30",
        "After fault": "21:31",
        "Late peak": "22:30",
        "Close": "23:59",
    },
    show_response_ms=True,
    footnote=(
        "<b>How honest is this?</b> Both panels replay the same 17 arrivals from "
        "<code>public_arrivals.csv</code> and the same D4-2 lockout from <code>faults.csv</code>. "
        "Throughput is identical because the hub is not saturated at 21:30 — that is the honest result. "
        "Both panels complete the same 14 of 17 arrivals; the remaining 3 are limited by driver patience at the "
        "late-evening queue, not by the cable fault. The difference we are showing is the response time and the "
        "recovery workflow: 30 s of cloud round-trip versus 40 ms of local safety lockout, plus the automatic "
        "service ticket. This scene is about <i>autonomy</i>, not about extra kWh."
    ),
)

render_scene(SPEC, kind="public", fault_ts=CABLE_FAULT_TS)
