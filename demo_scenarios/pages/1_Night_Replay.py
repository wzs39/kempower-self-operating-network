"""
Night Replay — the 2026-11-12 -> 13 S1 night as an animation, not a table.

Main entry point stays `app.py`. Streamlit picks this file up automatically as
page "Night Replay" in the sidebar (multi-page apps: anything under pages/).

What it shows, side by side, on the exact same 24 buses:
    BASELINE  12 dispensers + one operator shift at 00:30   -> 4 buses leave short
    TIER 3b   24 connection points + cabinet busbar, 0 humans -> 0 buses leave short
              (a HARDWARE scenario; the SHIPPED 0-CAPEX software result is S1 4 -> 3,
               0 human moves, -87.8% of the deficit — see verify_all.py)

Both get the same physical shock at 02:25 (C1-3 overtemperature stop, F016).
The point of the animation: the *only* difference is how many places a cable can
live, and whether a human has to move it.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[2]  # repo root: the demo shares the single authoritative src/ engine
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.sim.night_replay import (  # noqa: E402
    FAULT_TS,
    PRECURSOR_TS,
    build_all,
)

st.set_page_config(page_title="Night Replay — Kempower", layout="wide")

# Recording mode: compress the scene so it fits on one screen for screen-capture.
_RECORD = True
# Show the Play/Pause/Restart + speed controls for a live demo.
_SHOW_CONTROLS = True

# --------------------------------------------------------------------------- data
@st.cache_data(show_spinner="Simulating the night: 24 buses x 693 minutes x 3 scenarios…")
def _night_replays():
    return build_all()


@st.cache_data(show_spinner=False)
def _night_events() -> list[tuple[datetime, str, str, str]]:
    """(timestamp, level, title, detail) — every entry comes from the official CSVs."""
    return [
        (datetime.fromisoformat("2026-11-12T18:58:00+02:00"), "info",
         "Wave 1 arrives", "First buses plug in on their own. No staff involved."),
        (datetime.fromisoformat("2026-11-12T20:00:00+02:00"), "info",
         "Night grid tariff starts", "Spot price drops; the depot enters its cheap window."),
        (datetime.fromisoformat(PRECURSOR_TS), "warn",
         "PdM precursor — D1-9", "Cabinet C1-3 at 59.3 °C, fan 702 rpm. 199 min before F015."),
        (datetime.fromisoformat("2026-11-13T00:30:00+02:00"), "info",
         "Operator bulk swap", "Baseline only: one human walks the row and re-plugs 9 buses."),
        (datetime.fromisoformat("2026-11-13T01:50:00+02:00"), "warn",
         "F015 raised", "Cooling anomaly escalates on cabinet C1-3."),
        (datetime.fromisoformat(FAULT_TS), "critical",
         "F016 — C1-3 overtemperature stop", "One cabinet goes offline. Capacity 1,080 → 720 kW."),
        (datetime.fromisoformat("2026-11-13T06:30:00+02:00"), "info",
         "Last departure", "Shift ends. Count what each network delivered."),
    ]


REPLAYS = _night_replays()
BASE = REPLAYS["baseline"]
SENT = REPLAYS["sentinel"]
NOBAR = REPLAYS["no_busbar"]
N_FRAMES = min(len(BASE.frames), len(SENT.frames))
CLOCKS = [f.ts.strftime("%H:%M") for f in BASE.frames]
EVENTS = _night_events()

LEVEL_STYLE = {
    "info": ("#EEF2F7", "#4A5568", "#C7D2DE"),
    "warn": ("#FFF6E5", "#8A5A00", "#F2C94C"),
    "critical": ("#FDECEC", "#9B1C1C", "#E05252"),
}
CHIP_STYLE = {
    "charging": ("#E7F3FC", "#0B5A86", "#7CC3E8"),
    "waiting": ("#F3F4F6", "#6B7280", "#D1D5DB"),
    "done": ("#E6F6EE", "#0B6E4F", "#7BD3A8"),
    "missed": ("#FDECEC", "#9B1C1C", "#E88A8A"),
    "idle": ("#FBFBFC", "#B9BFC7", "#EDEFF2"),
}

# --------------------------------------------------------------------------- state
if "idx" not in st.session_state:
    st.session_state.idx = 0
if "playing" not in st.session_state:
    st.session_state.playing = False
if "advance" not in st.session_state:
    st.session_state.advance = 4

# --------------------------------------------------------------------------- header
if _RECORD:
    st.markdown(
        """
<div style="padding:0 0 4px">
  <div style="font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#8A94A6">
    Kempower self-operating network · S1 bus depot · 2026-11-12 18:58 → 11-13 06:30
  </div>
  <div style="font-size:22px;font-weight:650;color:#15212E;margin-top:2px">
    One night, one fault, two answers
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
<div style="padding:2px 0 10px">
  <div style="font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#8A94A6">
    Kempower self-operating network · S1 bus depot · 2026-11-12 18:58 → 11-13 06:30
  </div>
  <div style="font-size:30px;font-weight:650;color:#15212E;margin-top:4px">
    One night, one fault, two answers
  </div>
</div>
""",
        unsafe_allow_html=True,
    )


# --------------------------------------------------------------------------- render helpers
def _chips(frame, buses) -> str:
    """24 vehicle chips, 8 per row, each with a SoC hairline underneath."""
    out = []
    for b in buses:
        state = frame.states.get(b.vehicle_id, "idle")
        bg, fg, border = CHIP_STYLE[state]
        kw = frame.kw.get(b.vehicle_id, 0.0)
        soc = frame.soc.get(b.vehicle_id, 0.0)
        pct = max(0.0, min(1.0, soc / b.soc_required if b.soc_required else 0.0))
        if state == "charging":
            right = f"{kw:.0f} kW"
        elif state == "missed":
            right = "SHORT"
        elif state == "done":
            right = "full"
        elif state == "waiting":
            right = "queue"
        else:
            right = "—"
        out.append(
            f'<div style="background:{bg};border:1px solid {border};border-radius:9px;'
            f'padding:6px 7px 5px;min-width:0;overflow:hidden">'
            f'<div style="display:flex;justify-content:space-between;align-items:baseline;gap:4px">'
            f'<span style="font-weight:650;font-size:12.5px;color:{fg}">{b.vehicle_id}</span>'
            f'<span style="font-size:10.5px;color:{fg};opacity:.85;white-space:nowrap;'
            f'overflow:hidden;text-overflow:ellipsis">{right}</span>'
            f"</div>"
            f'<div style="height:3px;background:{border};border-radius:2px;margin-top:5px">'
            f'<div style="height:3px;width:{pct * 100:.0f}%;background:{fg};opacity:.75;border-radius:2px"></div>'
            f"</div></div>"
        )
    return (
        '<div style="display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:5px">'
        + "".join(out)
        + "</div>"
    )


def _panel(rep, idx: int, title: str, tag: str, tag_bg: str, tag_fg: str) -> str:
    f = rep.frames[idx]
    missed_now = f.missed_so_far
    live = sum(1 for s in f.states.values() if s == "charging")
    queue = sum(1 for s in f.states.values() if s == "waiting")
    load_pct = f.total_kw / 1080.0 if 1080.0 else 0.0
    pad = "9px 11px 11px" if _RECORD else "14px 15px 15px"
    ts_size = "24px" if _RECORD else "30px"
    title_size = "14px" if _RECORD else "15.5px"
    m_top = "8px" if _RECORD else "12px"
    return f"""
<div style="border:1px solid #E3E8EF;border-radius:12px;padding:{pad};background:#fff">
  <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px">
    <div>
      <div style="font-size:10.5px;color:#8A94A6;letter-spacing:.06em;text-transform:uppercase">{tag}</div>
      <div style="font-size:{title_size};font-weight:650;color:#15212E;margin-top:2px">{title}</div>
    </div>
    <div style="font-size:{ts_size};font-weight:300;color:#15212E;font-variant-numeric:tabular-nums;line-height:1.05">{f.ts.strftime("%H:%M")}</div>
  </div>

  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin:{m_top} 0 {m_top}">
    <div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">Delivered</div>
         <div style="font-size:17px;font-weight:600;color:#15212E;font-variant-numeric:tabular-nums">{f.delivered_kwh:,.0f}<span style="font-size:11px;color:#8A94A6"> kWh</span></div></div>
    <div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">Charging</div>
         <div style="font-size:17px;font-weight:600;color:#0B5A86;font-variant-numeric:tabular-nums">{live}<span style="font-size:11px;color:#8A94A6"> / {len(rep.buses)}</span></div></div>
    <div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">Human actions</div>
         <div style="font-size:17px;font-weight:600;color:{'#9B1C1C' if f.moves else '#17A673'};font-variant-numeric:tabular-nums">{f.moves}</div></div>
    <div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">Left short</div>
         <div style="font-size:17px;font-weight:600;color:{'#9B1C1C' if missed_now else '#17A673'};font-variant-numeric:tabular-nums">{missed_now}</div></div>
  </div>

  {_chips(f, rep.buses)}

  <div style="margin-top:{m_top};display:flex;align-items:center;gap:9px">
    <div style="font-size:10.5px;color:#8A94A6;white-space:nowrap">Station load</div>
    <div style="flex:1;height:7px;background:#EFF2F6;border-radius:4px;overflow:hidden">
      <div style="height:7px;width:{min(load_pct, 1) * 100:.1f}%;background:linear-gradient(90deg,#7CC3E8,#0B5A86);border-radius:4px"></div>
    </div>
    <div style="font-size:11.5px;color:#4A5568;font-variant-numeric:tabular-nums;white-space:nowrap">
      {f.total_kw:,.0f} / {f.capacity_kw:,.0f} kW
    </div>
  </div>
  <div style="margin-top:6px;font-size:11px;color:{'#9B1C1C' if queue else '#8A94A6'}">
    {f"{queue} bus(es) waiting for a free connection point" if queue else "no vehicle is waiting for a cable"}
  </div>
</div>
"""


def _incident_feed(idx: int) -> str:
    t = BASE.frames[idx].ts
    shown = [e for e in EVENTS if e[0] <= t][-3:] if _RECORD else [e for e in EVENTS if e[0] <= t][-4:]
    if not shown:
        return '<div style="font-size:12px;color:#8A94A6;padding:6px 0">No incident yet — the depot is quiet.</div>'
    rows = []
    for ts, level, title, detail in shown:
        bg, fg, border = LEVEL_STYLE[level]
        rows.append(
            f'<div style="background:{bg};border-left:3px solid {border};border-radius:6px;'
            f'padding:6px 9px;margin-bottom:5px">'
            f'<div style="font-size:11.5px;color:{fg};font-weight:650">'
            f'{ts.strftime("%H:%M")} · {title}</div>'
            f'<div style="font-size:11px;color:{fg};opacity:.82">{detail}</div></div>'
        )
    return "".join(rows)


def _verdict(idx: int) -> str:
    """Live comparison — every number tracks the current frame, so nothing is spoiled."""
    fb, fs = BASE.frames[idx], SENT.frames[idx]
    done = idx >= N_FRAMES - 1
    head = "Night closed — final tally" if done else f"Live tally · frame {idx + 1}/{N_FRAMES}"
    tone = "#0B6E4F" if done else "#8A94A6"
    return f"""
<div style="border:1px solid #E3E8EF;border-radius:14px;padding:12px 14px;background:#FCFDFE">
  <div style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:{tone};font-weight:650">{head}</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:9px">
    <div><div style="font-size:10.5px;color:#8A94A6">Buses left short</div>
      <div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">{fb.missed_so_far} <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">{fs.missed_so_far}</span></div></div>
    <div><div style="font-size:10.5px;color:#8A94A6">Human re-plugs</div>
      <div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">{fb.moves} <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">{fs.moves}</span></div></div>
    <div><div style="font-size:10.5px;color:#8A94A6">Energy delivered</div>
      <div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">{fb.delivered_kwh:,.0f} <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">{fs.delivered_kwh:,.0f}</span> <span style="font-size:11px;color:#8A94A6">kWh</span></div></div>
  </div>
</div>
"""


# --------------------------------------------------------------------------- controls
JUMP_TO = {"Arrivals": "18:58", "Precursor": "22:31", "Fault": "02:25", "Morning": CLOCKS[-1]}


def _on_jump() -> None:
    target = JUMP_TO.get(st.session_state.get("jump_pick", "—"))
    if target and target in CLOCKS:
        st.session_state.idx = CLOCKS.index(target)
        st.session_state.playing = False


c1, c2, c3, c4 = st.columns([1.0, 1.0, 1.5, 3.2])
if _SHOW_CONTROLS:
    with c1:
        if st.button("▶  Play" if not st.session_state.playing else "⏸  Pause", use_container_width=True):
            st.session_state.playing = not st.session_state.playing
            st.rerun()
    with c2:
        if st.button("⟲  Restart", use_container_width=True):
            st.session_state.idx = 0
            st.session_state.playing = False
            st.rerun()
    with c3:
        st.select_slider(
            "Playback speed",
            options=[1, 2, 4, 8, 16],
            format_func=lambda v: f"{v} min / frame",
            key="advance",
        )
with c4:
    st.radio(
        "Jump to",
        ["—", "Arrivals", "Precursor", "Fault", "Morning"],
        horizontal=True,
        label_visibility="collapsed",
        key="jump_pick",
        on_change=_on_jump,
    )


# --------------------------------------------------------------------------- player
def _block() -> None:
    idx = st.session_state.idx
    left, right = st.columns(2)
    with left:
        st.markdown(
            _panel(BASE, idx, "12 dispensers · 1 operator shift", "what happened",
                   "#FDECEC", "#9B1C1C"),
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            _panel(SENT, idx, "24 points + busbar · zero humans", "Tier 3b hardware",
                   "#EEF2FF", "#3730A3"),
            unsafe_allow_html=True,
        )

    st.write("")
    a, b = st.columns([1.5, 1])
    with a:
        st.markdown(_verdict(idx), unsafe_allow_html=True)
    with b:
        st.markdown(
            '<div style="border:1px solid #E3E8EF;border-radius:14px;padding:10px 12px;background:#fff">'
            '<div style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#8A94A6;'
            'font-weight:650;margin-bottom:6px">Incident feed</div>'
            + _incident_feed(idx)
            + "</div>",
            unsafe_allow_html=True,
        )

    # evidence that the busbar is not optional (hidden in recording mode)
    if not _RECORD and BASE.frames[idx].ts >= datetime.fromisoformat(FAULT_TS):
        st.markdown(
            f'<div style="margin-top:10px;background:#FFF9EC;border:1px solid #F2D9A0;'
            f'border-radius:10px;padding:9px 12px;font-size:12.5px;color:#7A5200">'
            f"<b>Why the cabinet busbar is not optional:</b> with the same 24 points but no busbar, "
            f"<b>{len(NOBAR.missed)} buses</b> lose their cable to the dead cabinet and finish short "
            f"({NOBAR.missed_kwh:,.0f} kWh missing). The busbar is what turns a cabinet failure into a "
            f"capacity dip instead of a stranded vehicle.</div>",
            unsafe_allow_html=True,
        )


@st.fragment(run_every=0.28 if st.session_state.playing else None)
def _player() -> None:
    if st.session_state.playing:
        nxt = st.session_state.idx + st.session_state.advance
        if nxt >= N_FRAMES - 1:
            st.session_state.idx = N_FRAMES - 1
            st.session_state.playing = False
            _block()
            st.rerun(scope="app")
            return
        st.session_state.idx = nxt
    _block()


_player()

# --------------------------------------------------------------------------- footnote
if not _RECORD:
    st.markdown(
        f"""
<div style="margin-top:22px;border-top:1px solid #EDF0F4;padding-top:12px;font-size:11.5px;
line-height:1.65;color:#8A94A6">
<b>How honest is this?</b> Both panels run the same 24 buses from <code>fleet_schedule.csv</code>
and the same 1,080 kW capacity from <code>chargers.csv</code>; only the number of connection points,
the cabinet busbar and the human shift differ. The 4 short departures in the left panel match the
real <code>departures_baseline.csv</code> in count, but not bus-by-bus — the model collapses the
operator's shifting habits into a single 00:30 round, so the identities differ
(model: {", ".join(BASE.missed)} / official: B04, B18, B20, B09).
Fault times come from <code>faults.csv</code> (F015 01:50, F016 02:25 → 06:31).
</div>
""",
        unsafe_allow_html=True,
    )
