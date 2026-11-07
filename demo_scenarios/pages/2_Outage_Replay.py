"""
Outage Replay — S3 highway hub, 2026-11-13, 256 arrivals, 11:00-13:00 cellular outage.

Second animation page (Streamlit picks up anything under pages/).

    BASELINE  vendor offline fallback: 50 kW per dispenser -> 500 kW for 2 h
    SENTINEL  edge islanding: local DLM keeps 1,425 kW DC, drivers never notice

Honesty note (also rendered on the page): the official public_arrivals.csv shows
76 abandonments that day, but only 13 of them fall inside the outage window.
38 of them happen 15:00-18:00 with the network healthy. The outage is an
amplifier of a capacity problem, not the root cause of the 29.69% figure.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

import streamlit as st

REPO_ROOT = Path(__file__).resolve().parents[2]  # repo root: the demo shares the single authoritative src/ engine
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.sim.outage_replay import (  # noqa: E402
    OUTAGE_END,
    OUTAGE_START,
    build_all,
)

st.set_page_config(page_title="Outage Replay — Kempower", layout="wide")

# Compact layout keeps the scene on one screen for recording; set False for a
# roomier layout. Playback controls are controlled separately by _SHOW_CONTROLS.
_RECORD = True
# Show the Play/Pause/Restart + speed controls for a live demo.
_SHOW_CONTROLS = True


@st.cache_data(show_spinner="Simulating S3: 256 arrivals x 1,909 minutes x 2 scenarios…")
def _outage_replays():
    return build_all()


@st.cache_data(show_spinner=False)
def _outage_events() -> list[tuple[datetime, str, str, str]]:
    return [
        (datetime.fromisoformat("2026-11-13T08:00:00+02:00"), "info",
         "Morning traffic builds", "10 dispensers, 300 kW each on D3-1..D3-8."),
        (datetime.fromisoformat(OUTAGE_START), "critical",
         "11:00 — cellular link lost", "Cloud unreachable. Baseline drops to 50 kW per gun = 500 kW."),
        (datetime.fromisoformat("2026-11-13T12:00:00+02:00"), "warn",
         "One hour offline", "Trucks that needed 60 min now need 360 min. Drivers start walking away."),
        (datetime.fromisoformat(OUTAGE_END), "info",
         "13:00 — link restored", "Baseline has a two-hour backlog to work through."),
        (datetime.fromisoformat("2026-11-13T15:00:00+02:00"), "warn",
         "Afternoon peak", "Network is fine now. This is a capacity problem, not a connectivity problem."),
    ]


REPLAYS = _outage_replays()
BASE = REPLAYS["baseline"]
SENT = REPLAYS["sentinel"]
ARR = {a.arrival_id: a for a in BASE.arrivals}
N_FRAMES = min(len(BASE.frames), len(SENT.frames))
CLOCKS = [f.ts.strftime("%H:%M") for f in BASE.frames]
EVENTS = _outage_events()

LEVEL_STYLE = {
    "info": ("#EEF2F7", "#4A5568", "#C7D2DE"),
    "warn": ("#FFF6E5", "#8A5A00", "#F2C94C"),
    "critical": ("#FDECEC", "#9B1C1C", "#E05252"),
}
CLASS_SHORT = {"car": "car", "van": "van", "truck": "truck"}

st.markdown(
    """
<div style="padding:0 0 4px">
  <div style="font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#8A94A6">
    Kempower self-operating network · S3 highway hub · 2026-11-13 · 256 arrivals
  </div>
  <div style="font-size:22px;font-weight:650;color:#15212E;margin-top:2px">
    Losing the cloud is not losing the power
  </div>
</div>
""",
    unsafe_allow_html=True,
)


def _guns(frame) -> str:
    cells = []
    for i, aid in enumerate(frame.guns):
        limit = 300 if i < 8 else 150
        if aid is None:
            cells.append(
                '<div style="background:#FBFBFC;border:1px dashed #D9DEE5;border-radius:9px;'
                'padding:8px 6px;text-align:center;min-width:0">'
                '<div style="font-size:11px;color:#B9BFC7">free</div>'
                f'<div style="font-size:10px;color:#D1D5DB;margin-top:2px">{limit} kW</div></div>'
            )
            continue
        a = ARR[aid]
        kw = frame.kw.get(aid, 0.0)
        weak = kw < 0.55 * min(limit, a.max_kw)
        bg = "#FFF1E8" if weak else "#E7F3FC"
        fg = "#9A4B12" if weak else "#0B5A86"
        border = "#F0B48A" if weak else "#7CC3E8"
        cells.append(
            f'<div style="background:{bg};border:1px solid {border};border-radius:9px;'
            f'padding:8px 6px;min-width:0;overflow:hidden">'
            f'<div style="display:flex;justify-content:space-between;gap:4px;align-items:baseline">'
            f'<span style="font-size:11.5px;font-weight:650;color:{fg}">D3-{i + 1}</span>'
            f'<span style="font-size:10px;color:{fg};opacity:.8">{CLASS_SHORT[a.vehicle_class]}</span></div>'
            f'<div style="font-size:15px;font-weight:600;color:{fg};margin-top:3px;'
            f'font-variant-numeric:tabular-nums">{kw:.0f}<span style="font-size:10px"> kW</span></div>'
            f'<div style="font-size:10px;color:{fg};opacity:.75">{a.need_kwh:.0f} kWh wanted</div></div>'
        )
    return (
        '<div style="display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:5px">'
        + "".join(cells)
        + "</div>"
    )


def _panel(rep, idx: int, title: str, tag: str, tag_bg: str, tag_fg: str) -> str:
    f = rep.frames[idx]
    load_pct = f.total_kw / 1425.0
    cap_color = "#9B1C1C" if not f.online else "#8A94A6"
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
         <div style="font-size:17px;font-weight:600;color:#0B5A86;font-variant-numeric:tabular-nums">{f.charging_now}<span style="font-size:11px;color:#8A94A6"> / 10</span></div></div>
    <div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">In queue</div>
         <div style="font-size:17px;font-weight:600;color:{'#9A4B12' if f.queue_now else '#17A673'};font-variant-numeric:tabular-nums">{f.queue_now}</div></div>
    <div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">Walked away</div>
         <div style="font-size:17px;font-weight:600;color:{'#9B1C1C' if f.abandoned_so_far else '#17A673'};font-variant-numeric:tabular-nums">{f.abandoned_so_far}</div></div>
  </div>

  {_guns(f)}

  <div style="margin-top:{m_top};display:flex;align-items:center;gap:9px">
    <div style="font-size:10.5px;color:#8A94A6;white-space:nowrap">Station load</div>
    <div style="flex:1;height:7px;background:#EFF2F6;border-radius:4px;overflow:hidden">
      <div style="height:7px;width:{min(load_pct, 1) * 100:.1f}%;background:linear-gradient(90deg,#7CC3E8,#0B5A86);border-radius:4px"></div>
    </div>
    <div style="font-size:11.5px;color:#4A5568;font-variant-numeric:tabular-nums;white-space:nowrap">
      {f.total_kw:,.0f} / {f.capacity_kw:,.0f} kW
    </div>
  </div>
  <div style="margin-top:6px;font-size:11px;color:{cap_color}">
    {"OFFLINE — cloud unreachable" if not f.online else "online · cloud connected"}
  </div>
</div>
"""


def _incident_feed(idx: int) -> str:
    t = BASE.frames[idx].ts
    shown = [e for e in EVENTS if e[0] <= t][-3:] if _RECORD else [e for e in EVENTS if e[0] <= t][-4:]
    if not shown:
        return '<div style="font-size:12px;color:#8A94A6;padding:6px 0">No incident yet.</div>'
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
    fb, fs = BASE.frames[idx], SENT.frames[idx]
    done = idx >= N_FRAMES - 1
    head = "Day closed — final tally" if done else f"Live tally · frame {idx + 1}/{N_FRAMES}"
    tone = "#0B6E4F" if done else "#8A94A6"
    return f"""
<div style="border:1px solid #E3E8EF;border-radius:14px;padding:12px 14px;background:#FCFDFE">
  <div style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:{tone};font-weight:650">{head}</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:9px">
    <div><div style="font-size:10.5px;color:#8A94A6">Drivers who walked away</div>
      <div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">{fb.abandoned_so_far} <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">{fs.abandoned_so_far}</span></div></div>
    <div><div style="font-size:10.5px;color:#8A94A6">Power during the outage</div>
      <div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">500 <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">1,425</span> <span style="font-size:11px;color:#8A94A6">kW</span></div></div>
    <div><div style="font-size:10.5px;color:#8A94A6">Energy delivered</div>
      <div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">{fb.delivered_kwh:,.0f} <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">{fs.delivered_kwh:,.0f}</span> <span style="font-size:11px;color:#8A94A6">kWh</span></div></div>
  </div>
</div>
"""


JUMP_TO = {"Outage 11:00": "11:00", "Mid-outage 12:00": "12:00",
           "Restored 13:00": "13:00", "Evening peak 16:00": "16:00", "Close": CLOCKS[-1]}


def _on_jump() -> None:
    target = JUMP_TO.get(st.session_state.get("outage_jump", "—"))
    if target and target in CLOCKS:
        st.session_state.outage_idx = CLOCKS.index(target)
        st.session_state.outage_playing = False


if "outage_idx" not in st.session_state:
    st.session_state.outage_idx = CLOCKS.index("10:30") if "10:30" in CLOCKS else 0
if "outage_playing" not in st.session_state:
    st.session_state.outage_playing = False
if "outage_advance" not in st.session_state:
    st.session_state.outage_advance = 4

c1, c2, c3, c4 = st.columns([1.0, 1.0, 1.5, 3.6])
if _SHOW_CONTROLS:
    with c1:
        if st.button("▶  Play" if not st.session_state.outage_playing else "⏸  Pause",
                     use_container_width=True, key="outage_play"):
            st.session_state.outage_playing = not st.session_state.outage_playing
            st.rerun()
    with c2:
        if st.button("⟲  Restart", use_container_width=True, key="outage_restart"):
            st.session_state.outage_idx = 0
            st.session_state.outage_playing = False
            st.rerun()
    with c3:
        st.select_slider("Playback speed", options=[1, 2, 4, 8, 16],
                         format_func=lambda v: f"{v} min / frame", key="outage_advance")
with c4:
    st.radio("Jump to", ["—"] + list(JUMP_TO), horizontal=True,
             label_visibility="collapsed", key="outage_jump", on_change=_on_jump)


def _block() -> None:
    idx = st.session_state.outage_idx
    left, right = st.columns(2)
    with left:
        st.markdown(_panel(BASE, idx, "50 kW offline fallback", "what happens today",
                           "#FDECEC", "#9B1C1C"), unsafe_allow_html=True)
    with right:
        st.markdown(_panel(SENT, idx, "edge islanding · full local power", "this system",
                           "#E6F6EE", "#0B6E4F"), unsafe_allow_html=True)

    st.write("")
    a, b = st.columns([1.5, 1])
    with a:
        st.markdown(_verdict(idx), unsafe_allow_html=True)
    with b:
        st.markdown(
            '<div style="border:1px solid #E3E8EF;border-radius:14px;padding:10px 12px;background:#fff">'
            '<div style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#8A94A6;'
            'font-weight:650;margin-bottom:6px">Incident feed</div>'
            + _incident_feed(idx) + "</div>", unsafe_allow_html=True)

    if not _RECORD and BASE.frames[idx].ts >= datetime.fromisoformat(OUTAGE_START):
        st.markdown(
            '<div style="margin-top:10px;background:#FFF9EC;border:1px solid #F2D9A0;'
            'border-radius:10px;padding:9px 12px;font-size:12.5px;color:#7A5200">'
            '<b>Why 50 kW is the real failure:</b> a truck wanting 224 kWh finishes in 45 min at '
            '300 kW. At 50 kW it needs 269 min — longer than any driver will wait. The outage does '
            'not break the hardware; it breaks the <i>throughput</i>. Local islanding removes that '
            'penalty entirely, because dividing power never required the cloud.</div>',
            unsafe_allow_html=True)


@st.fragment(run_every=0.28 if st.session_state.outage_playing else None)
def _player() -> None:
    if st.session_state.outage_playing:
        nxt = st.session_state.outage_idx + st.session_state.outage_advance
        if nxt >= N_FRAMES - 1:
            st.session_state.outage_idx = N_FRAMES - 1
            st.session_state.outage_playing = False
            _block()
            st.rerun(scope="app")
            return
        st.session_state.outage_idx = nxt
    _block()


_player()

if not _RECORD:
    st.markdown(
        f"""
<div style="margin-top:22px;border-top:1px solid #EDF0F4;padding-top:12px;font-size:11.5px;
line-height:1.65;color:#8A94A6">
<b>How honest is this?</b> Both panels replay the same 256 arrivals from
<code>public_arrivals.csv</code> with the same dispenser limits from <code>chargers.csv</code>;
only the station budget during 11:00–13:00 differs (500 vs 1,425 kW).
The official file records <b>76 abandonments</b> that day (29.69%), but only <b>13</b> of them fall
inside the outage window and <b>38</b> happen 15:00–18:00 with the network healthy — so the outage
is an amplifier of a capacity shortage, not the root cause of the 29.69% figure.
This model reproduces that mechanism ({len(BASE.abandoned)} vs {len(SENT.abandoned)} walked away),
not the official vehicle-by-vehicle count; driver patience is taken from each row's
<code>max_wait_min</code>, and vehicles are assumed to stay until their requested energy is delivered.
</div>
""",
        unsafe_allow_html=True,
    )
