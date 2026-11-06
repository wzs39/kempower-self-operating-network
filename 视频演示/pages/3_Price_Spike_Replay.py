"""
Price Spike Replay — S2 logistics depot, 2026-11-13 14:00 → 11-14 06:00.

Independent scene: *no grid event happens here*. Only the spot price moves.
Baseline charges whoever is plugged in. Sentinel protects deadlines first and
defers the flexible overnight trucks through the 17:15–18:45 spike.
"""
from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.sim.fault_replays import (  # noqa: E402
    PRICE_PEAK_TS,
    PRICE_SPIKE_END,
    PRICE_SPIKE_START,
    build_price_replays,
    load_price_series,
)
from src.ui.replay_scene import SceneSpec, render_scene  # noqa: E402

st.set_page_config(page_title="Price Spike Replay — Kempower", layout="wide")


@st.cache_data(show_spinner="Simulating the price scene: 8 trucks x 16 h x 2 strategies…")
def _build():
    return build_price_replays()


PRICES = load_price_series("2026-11-13T14:00:00+02:00", "2026-11-14T06:00:00+02:00")

SPEC = SceneSpec(
    key="price",
    title="The most expensive 90 minutes of the week",
    subtitle="Kempower self-operating network · S2 logistics depot · 2026-11-13 14:00 → 11-14 06:00 · price only, no grid event",
    events=[
        (datetime.fromisoformat("2026-11-13T14:20:00+02:00"), "info",
         "Trucks plug in", "T01–T08 arrive between 14:20 and 14:45."),
        (datetime.fromisoformat("2026-11-13T17:15:00+02:00"), "warn",
         "Spot price starts climbing", "204.28 €/MWh and rising; the extreme window opens."),
        (PRICE_PEAK_TS, "critical",
         "799.30 €/MWh", "Peak of the day. Sentinel defers the flexible trucks, not the deadlines."),
        (PRICE_SPIKE_END, "info",
         "Price falls back", "187.19 → 109.15 €/MWh; the deferred trucks resume."),
        (datetime.fromisoformat("2026-11-14T06:00:00+02:00"), "info",
         "Scene closes", "Every truck is full. Only the electricity bill differs."),
    ],
    build=_build,
    left_title="Charge now, ignore the price",
    right_title="Deadline first, defer the flexible",
    jumps={
        "Start": "14:20",
        "Spike": "17:15",
        "Peak": "18:00",
        "Recovery": "18:45",
        "Close": "06:00",
    },
    show_price=True,
    show_cost=True,
    footnote=(
        "<b>How honest is this?</b> Both panels run the same 8 trucks from <code>fleet_schedule.csv</code>, "
        "the same 800 kW site limit and the same 15-minute <code>prices.csv</code> curve; only the dispatch "
        "strategy differs. The baseline leaves T02 short because it splits power evenly instead of protecting "
        "the 17:45 departure; Sentinel charges T02 first and defers T05–T08 through the spike. "
        "Costs are energy-only (spot + depot tariff) for the energy actually drawn."
    ),
)

render_scene(SPEC, kind="fleet", cap_kw=800.0, prices=PRICES)
