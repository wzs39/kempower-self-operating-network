"""
Commissioning Replay — S5 new bus depot, 2026-11-12 19:30 → 11-13 06:20.

Independent scene: nothing is physically broken. The station is simply
misconfigured — 600 kW cap instead of 900 kW, D5-7 throttled to 50 kW and
D5-8 inactive. Sentinel's digital twin reconciles the three config sources and
unlocks the real capacity before the first bus leaves short.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.sim.fault_replays import build_commissioning_replays  # noqa: E402
from src.ui.replay_scene import SceneSpec, render_scene  # noqa: E402

st.set_page_config(page_title="Commissioning Replay — Kempower", layout="wide")


@st.cache_data(show_spinner="Simulating the commissioning scene: 12 buses x 11 h x 2 configs…")
def _build():
    return build_commissioning_replays()


SPEC = SceneSpec(
    key="commission",
    title="The hardware was fine. The config was starving it.",
    subtitle="Kempower self-operating network · S5 new bus depot · 2026-11-12 19:30 → 11-13 06:20 · config error only",
    events=[
        (datetime.fromisoformat("2026-11-12T19:44:00+02:00"), "info",
         "Buses arrive", "12 buses park for the night at the newly commissioned depot."),
        (datetime.fromisoformat("2026-11-13T00:00:00+02:00"), "critical",
         "Three-way config mismatch", "600 kW cap vs 900 kW of installed cabinets; D5-7 at 50 kW; D5-8 inactive."),
        (datetime.fromisoformat("2026-11-13T03:30:00+02:00"), "warn",
         "Sentinel unlocks the real capacity", "900 kW, D5-7 back to 150 kW, D5-8 online."),
        (datetime.fromisoformat("2026-11-13T05:30:00+02:00"), "warn",
         "First departure", "Baseline has already starved five buses; Sentinel has not."),
        (datetime.fromisoformat("2026-11-13T06:20:00+02:00"), "info",
         "Scene closes", "Same buses, same chargers — only the configuration differed."),
    ],
    build=_build,
    left_title="600 kW cap · D5-7 50 kW · D5-8 offline",
    right_title="900 kW · D5-7 150 kW · D5-8 online",
    jumps={
        "Start": "19:44",
        "Mismatch": "00:00",
        "Unlock": "03:30",
        "First bus": "05:30",
        "Close": "06:20",
    },
    footnote=(
        "<b>How honest is this?</b> Both panels run the same 12 buses from <code>fleet_schedule.csv</code> "
        "and the same 8 chargers from <code>chargers.csv</code>. Only the configuration differs, exactly as in "
        "<code>site_config.csv</code> vs <code>network_sites.csv</code>/<code>power_cabinets.csv</code>. "
        "The baseline static share is calibrated so the scene reproduces the official 5 short departures; "
        "the kWh number in this simplified replay is therefore model-derived, not the official 508.95 kWh."
    ),
)

render_scene(SPEC, kind="fleet", cap_kw=900.0)
