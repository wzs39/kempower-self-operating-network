"""
Kempower Self-Operating Charging Network - Shared Replay Scene Renderer
Module: src/ui/replay_scene.py

One renderer, four independent fault scenes. Each scene gets its own time window,
its own event list and its own baseline-vs-sentinel comparison; nothing is merged
into a single timeline.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from textwrap import dedent
from typing import Callable, Dict, List, Optional, Sequence

import streamlit as st

from src.sim.fault_replays import FleetReplay, PublicReplay

# ---------------------------------------------------------------------------
# Recording mode: when True the scene is compressed so the whole thing fits on
# one screen for screen-recording. Titles shrink, paddings shrink, the long
# honesty footnote is hidden, and the incident feed is capped to 3 entries.
# ---------------------------------------------------------------------------
_RECORD = True

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


@dataclass
class SceneSpec:
    key: str
    title: str
    subtitle: str
    events: List[tuple[datetime, str, str, str]]
    build: Callable[[], Dict[str, object]]
    left_title: str
    right_title: str
    left_tag: str = "what happens today"
    right_tag: str = "this system"
    jumps: Optional[Dict[str, str]] = None
    footnote: str = ""
    show_price: bool = False
    show_cost: bool = False
    show_response_ms: bool = False


def _fleet_chips(frame, vehicles) -> str:
    out = []
    for v in vehicles:
        state = frame.states.get(v.vehicle_id, "idle")
        bg, fg, border = CHIP_STYLE[state]
        kw = frame.kw.get(v.vehicle_id, 0.0)
        soc = frame.soc.get(v.vehicle_id, 0.0)
        pct = max(0.0, min(1.0, soc / v.soc_required if v.soc_required else 0.0))
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
            f'<span style="font-weight:650;font-size:12.5px;color:{fg}">{v.vehicle_id}</span>'
            f'<span style="font-size:10.5px;color:{fg};opacity:.85;white-space:nowrap;'
            f'overflow:hidden;text-overflow:ellipsis">{right}</span></div>'
            f'<div style="height:3px;background:{border};border-radius:2px;margin-top:5px">'
            f'<div style="height:3px;width:{pct * 100:.0f}%;background:{fg};opacity:.75;border-radius:2px"></div>'
            f'</div></div>'
        )
    n = 6 if len(vehicles) <= 12 else 8
    return (
        f'<div style="display:grid;grid-template-columns:repeat({n},minmax(0,1fr));gap:5px">'
        + "".join(out) + "</div>"
    )


def _fleet_panel(rep: FleetReplay, idx: int, title: str, tag: str,
                 show_cost: bool, cap_kw: float) -> str:
    f = rep.frames[idx]
    live = sum(1 for s in f.states.values() if s == "charging")
    missed_now = f.missed_so_far
    load_pct = f.total_kw / cap_kw if cap_kw else 0.0
    metrics = (
        '<div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">Delivered</div>'
        f'<div style="font-size:17px;font-weight:600;color:#15212E;font-variant-numeric:tabular-nums">{f.delivered_kwh:,.0f}<span style="font-size:11px;color:#8A94A6"> kWh</span></div></div>'
        '<div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">Charging</div>'
        f'<div style="font-size:17px;font-weight:600;color:#0B5A86;font-variant-numeric:tabular-nums">{live}<span style="font-size:11px;color:#8A94A6"> / {len(rep.vehicles)}</span></div></div>'
    )
    if show_cost:
        metrics += (
            '<div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">Energy cost</div>'
            f'<div style="font-size:17px;font-weight:600;color:#15212E;font-variant-numeric:tabular-nums">€{f.cost_eur:,.2f}</div></div>'
        )
    metrics += (
        '<div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">Left short</div>'
        f'<div style="font-size:17px;font-weight:600;color:{"#9B1C1C" if missed_now else "#17A673"};font-variant-numeric:tabular-nums">{missed_now}</div></div>'
    )
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
  <div style="display:grid;grid-template-columns:repeat({4 if show_cost else 3},1fr);gap:8px;margin:{m_top} 0 {m_top}">{metrics}</div>
  {_fleet_chips(f, rep.vehicles)}
  <div style="margin-top:{m_top};display:flex;align-items:center;gap:9px">
    <div style="font-size:10.5px;color:#8A94A6;white-space:nowrap">Station load</div>
    <div style="flex:1;height:7px;background:#EFF2F6;border-radius:4px;overflow:hidden">
      <div style="height:7px;width:{min(load_pct, 1) * 100:.1f}%;background:linear-gradient(90deg,#7CC3E8,#0B5A86);border-radius:4px"></div>
    </div>
    <div style="font-size:11.5px;color:#4A5568;font-variant-numeric:tabular-nums;white-space:nowrap">
      {f.total_kw:,.0f} / {cap_kw:,.0f} kW
    </div>
  </div>
</div>
"""


def _public_guns(frame, arrivals) -> str:
    cells = []
    for i, aid in enumerate(frame.guns):
        if frame.faulted_gun_active and i == 1:
            cells.append(
                '<div style="background:#FDECEC;border:1px solid #E88A8A;border-radius:9px;'
                'padding:8px 6px;text-align:center;min-width:0">'
                '<div style="font-size:11.5px;font-weight:650;color:#9B1C1C">D4-2</div>'
                '<div style="font-size:10px;color:#9B1C1C;margin-top:2px">FAULT · locked</div></div>'
            )
            continue
        if aid is None:
            cells.append(
                '<div style="background:#FBFBFC;border:1px dashed #D9DEE5;border-radius:9px;'
                'padding:8px 6px;text-align:center;min-width:0">'
                '<div style="font-size:11px;color:#B9BFC7">free</div>'
                '<div style="font-size:10px;color:#D1D5DB;margin-top:2px">150 kW</div></div>'
            )
            continue
        a = arrivals[aid]
        kw = frame.kw.get(aid, 0.0)
        weak = kw < 0.55 * min(150.0, a.max_kw)
        bg = "#FFF1E8" if weak else "#E7F3FC"
        fg = "#9A4B12" if weak else "#0B5A86"
        border = "#F0B48A" if weak else "#7CC3E8"
        cells.append(
            f'<div style="background:{bg};border:1px solid {border};border-radius:9px;'
            f'padding:8px 6px;min-width:0;overflow:hidden">'
            f'<div style="display:flex;justify-content:space-between;gap:4px;align-items:baseline">'
            f'<span style="font-size:11.5px;font-weight:650;color:{fg}">D4-{i + 1}</span>'
            f'<span style="font-size:10px;color:{fg};opacity:.8">{a.vehicle_class}</span></div>'
            f'<div style="font-size:15px;font-weight:600;color:{fg};margin-top:3px;'
            f'font-variant-numeric:tabular-nums">{kw:.0f}<span style="font-size:10px"> kW</span></div>'
            f'<div style="font-size:10px;color:{fg};opacity:.75">{a.need_kwh:.0f} kWh wanted</div></div>'
        )
    return (
        '<div style="display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:5px">'
        + "".join(cells) + "</div>"
    )


def _public_panel(rep: PublicReplay, idx: int, title: str, tag: str,
                   fault_ts: datetime) -> str:
    f = rep.frames[idx]
    load_pct = f.total_kw / 600.0
    resp_txt = "<0.1" if rep.response_ms < 100 else f"{rep.response_ms / 1000.0:.1f}"
    pad = "9px 11px 11px" if _RECORD else "14px 15px 15px"
    ts_size = "24px" if _RECORD else "30px"
    title_size = "14px" if _RECORD else "15.5px"
    m_top = "8px" if _RECORD else "12px"
    response = (
        f'<div style="margin-top:6px;font-size:11px;color:#9B1C1C">'
        f'FAULTED · D4-2 locked out in {resp_txt} s</div>'
        if f.ts >= fault_ts else
        '<div style="margin-top:6px;font-size:11px;color:#8A94A6">online · all 8 dispensers available</div>'
    )
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
         <div style="font-size:17px;font-weight:600;color:#0B5A86;font-variant-numeric:tabular-nums">{f.charging_now}<span style="font-size:11px;color:#8A94A6"> / 8</span></div></div>
    <div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">In queue</div>
         <div style="font-size:17px;font-weight:600;color:{'#9A4B12' if f.queue_now else '#17A673'};font-variant-numeric:tabular-nums">{f.queue_now}</div></div>
    <div><div style="font-size:10.5px;color:#8A94A6;text-transform:uppercase;letter-spacing:.05em">Response</div>
         <div style="font-size:17px;font-weight:600;color:#15212E;font-variant-numeric:tabular-nums">{resp_txt} s</div></div>
  </div>
  {_public_guns(f, {a.arrival_id: a for a in rep.arrivals})}
  <div style="margin-top:{m_top};display:flex;align-items:center;gap:9px">
    <div style="font-size:10.5px;color:#8A94A6;white-space:nowrap">Station load</div>
    <div style="flex:1;height:7px;background:#EFF2F6;border-radius:4px;overflow:hidden">
      <div style="height:7px;width:{min(load_pct, 1) * 100:.1f}%;background:linear-gradient(90deg,#7CC3E8,#0B5A86);border-radius:4px"></div>
    </div>
    <div style="font-size:11.5px;color:#4A5568;font-variant-numeric:tabular-nums;white-space:nowrap">
      {f.total_kw:,.0f} / 600 kW
    </div>
  </div>
  {response}
</div>
"""


def _price_chart(prices: List[tuple[datetime, float]], idx: int,
                 clocks: List[str], frame_ts: datetime) -> str:
    if not prices:
        return ""
    lo, hi = 0.0, 850.0
    n = len(prices)
    pts = []
    for i, (ts, p) in enumerate(prices):
        x = 20 + (900 - 20) * i / max(n - 1, 1)
        y = 150 - 130 * (p - lo) / (hi - lo)
        pts.append(f"{x:.1f},{y:.1f}")
    # cursor: nearest price point to the current frame timestamp
    cur_i = min(range(n), key=lambda i: abs((prices[i][0] - frame_ts).total_seconds()))
    cur_x = 20 + (900 - 20) * cur_i / max(n - 1, 1)
    cur_y = 150 - 130 * (prices[cur_i][1] - lo) / (hi - lo)
    return f"""
<div style="border:1px solid #E3E8EF;border-radius:14px;padding:12px 14px;background:#fff;margin-top:14px">
  <div style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#8A94A6;font-weight:650">Spot price (€/MWh)</div>
  <svg viewBox="0 0 920 170" style="width:100%;height:170px;margin-top:8px">
    <line x1="20" y1="150" x2="900" y2="150" stroke="#EDF0F4" stroke-width="1"/>
    <line x1="20" y1="20" x2="900" y2="20" stroke="#EDF0F4" stroke-width="1" stroke-dasharray="4 4"/>
    <text x="8" y="154" font-size="10" fill="#B9BFC7">0</text>
    <text x="8" y="24" font-size="10" fill="#B9BFC7">850</text>
    <polyline points="{' '.join(pts)}" fill="none" stroke="#0B5A86" stroke-width="2.2" stroke-linejoin="round"/>
    <circle cx="{cur_x:.1f}" cy="{cur_y:.1f}" r="5" fill="#7CC3E8" stroke="#0B5A86" stroke-width="1.5"/>
    <line x1="{cur_x:.1f}" y1="20" x2="{cur_x:.1f}" y2="150" stroke="#7CC3E8" stroke-width="1" stroke-dasharray="3 3"/>
    <text x="{min(max(cur_x + 8, 24), 780):.0f}" y="{max(cur_y - 10, 16):.0f}" font-size="11" fill="#0B5A86" font-weight="650">
      {prices[cur_i][1]:.1f} €/MWh
    </text>
  </svg>
</div>
"""


def _incident_feed(events, t: datetime) -> str:
    shown = [e for e in events if e[0] <= t][-3:] if _RECORD else [e for e in events if e[0] <= t][-4:]
    if not shown:
        return '<div style="font-size:12px;color:#8A94A6;padding:6px 0">No incident yet.</div>'
    rows = []
    for ts, level, title, detail in shown:
        bg, fg, border = LEVEL_STYLE[level]
        rows.append(
            f'<div style="background:{bg};border-left:3px solid {border};border-radius:6px;'
            f'padding:6px 9px;margin-bottom:5px">'
            f'<div style="font-size:11.5px;color:{fg};font-weight:650">{ts.strftime("%H:%M")} · {title}</div>'
            f'<div style="font-size:11px;color:{fg};opacity:.82">{detail}</div></div>'
        )
    return "".join(rows)


def _verdict(base, sent, idx: int, n_frames: int, kind: str,
             show_cost: bool, show_response_ms: bool) -> str:
    done = idx >= n_frames - 1
    head = "Scene closed — final tally" if done else f"Live tally · frame {idx + 1}/{n_frames}"
    tone = "#0B6E4F" if done else "#8A94A6"
    if kind == "fleet":
        fb, fs = base.frames[idx], sent.frames[idx]
        cells = (
            f'<div><div style="font-size:10.5px;color:#8A94A6">Left short</div>'
            f'<div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">{fb.missed_so_far} <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">{fs.missed_so_far}</span></div></div>'
            f'<div><div style="font-size:10.5px;color:#8A94A6">Energy delivered</div>'
            f'<div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">{fb.delivered_kwh:,.0f} <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">{fs.delivered_kwh:,.0f}</span> <span style="font-size:11px;color:#8A94A6">kWh</span></div></div>'
        )
        if show_cost:
            cells += (
                f'<div><div style="font-size:10.5px;color:#8A94A6">Energy cost</div>'
                f'<div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">€{fb.cost_eur:,.2f} <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">€{fs.cost_eur:,.2f}</span></div></div>'
            )
    else:
        fb, fs = base.frames[idx], sent.frames[idx]
        resp_base = "<0.1" if base.response_ms < 100 else f"{base.response_ms / 1000.0:.1f}"
        resp_sent = "<0.1" if sent.response_ms < 100 else f"{sent.response_ms / 1000.0:.1f}"
        cells = (
            f'<div><div style="font-size:10.5px;color:#8A94A6">Delivered</div>'
            f'<div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">{fb.delivered_kwh:,.0f} <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">{fs.delivered_kwh:,.0f}</span> <span style="font-size:11px;color:#8A94A6">kWh</span></div></div>'
            f'<div><div style="font-size:10.5px;color:#8A94A6">Response time</div>'
            f'<div style="font-size:19px;font-weight:650;color:#15212E;font-variant-numeric:tabular-nums">{resp_base} s <span style="color:#B9BFC7">→</span> <span style="color:#0B6E4F">{resp_sent} s</span></div></div>'
        )
    return f"""
<div style="border:1px solid #E3E8EF;border-radius:14px;padding:12px 14px;background:#FCFDFE">
  <div style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:{tone};font-weight:650">{head}</div>
  <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:9px">{dedent(cells)}</div>
</div>
"""


def _header(title: str, subtitle: str) -> None:
    if _RECORD:
        st.markdown(
            f"""
<div style="padding:0 0 4px">
  <div style="font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:#8A94A6">{subtitle}</div>
  <div style="font-size:22px;font-weight:650;color:#15212E;margin-top:2px">{title}</div>
</div>
""",
            unsafe_allow_html=True,
        )
        return
    st.markdown(
        f"""
<div style="padding:2px 0 10px">
  <div style="font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:#8A94A6">{subtitle}</div>
  <div style="font-size:30px;font-weight:650;color:#15212E;margin-top:4px">{title}</div>
</div>
""",
        unsafe_allow_html=True,
    )


def _controls(key: str, clocks: List[str], jumps: Optional[Dict[str, str]]) -> None:
    idx_key, play_key, adv_key, jump_key = f"{key}_idx", f"{key}_playing", f"{key}_advance", f"{key}_jump"
    if idx_key not in st.session_state:
        st.session_state[idx_key] = 0
    if play_key not in st.session_state:
        st.session_state[play_key] = False
    if adv_key not in st.session_state:
        st.session_state[adv_key] = 4

    def _on_jump() -> None:
        target = (jumps or {}).get(st.session_state.get(jump_key, "—"))
        if target and target in clocks:
            st.session_state[idx_key] = clocks.index(target)
            st.session_state[play_key] = False

    c1, c2, c3, c4 = st.columns([1.0, 1.0, 1.5, 3.2])
    with c1:
        if st.button("▶  Play" if not st.session_state[play_key] else "⏸  Pause",
                     use_container_width=True, key=f"{key}_play"):
            st.session_state[play_key] = not st.session_state[play_key]
            st.rerun()
    with c2:
        if st.button("⟲  Restart", use_container_width=True, key=f"{key}_restart"):
            st.session_state[idx_key] = 0
            st.session_state[play_key] = False
            st.rerun()
    with c3:
        st.select_slider("Playback speed", options=[1, 2, 4, 8, 16],
                         format_func=lambda v: f"{v} min / frame", key=adv_key)
    with c4:
        if jumps:
            st.radio("Jump to", ["—"] + list(jumps), horizontal=True,
                     label_visibility="collapsed", key=jump_key, on_change=_on_jump)


def render_scene(spec: SceneSpec, kind: str = "fleet",
                 cap_kw: float = 800.0, fault_ts: Optional[datetime] = None,
                 prices: Optional[List[tuple[datetime, float]]] = None) -> None:
    """Render one independent fault scene, side by side, with its own clock."""
    _header(spec.title, spec.subtitle)
    replays = spec.build()
    base, sent = replays["baseline"], replays["sentinel"]
    n_frames = min(len(base.frames), len(sent.frames))
    clocks = base.clock_labels
    _controls(spec.key, clocks, spec.jumps)

    def _block() -> None:
        idx = st.session_state[f"{spec.key}_idx"]
        left, right = st.columns(2)
        with left:
            if kind == "fleet":
                st.markdown(_fleet_panel(base, idx, spec.left_title, spec.left_tag,
                                         spec.show_cost, cap_kw), unsafe_allow_html=True)
            else:
                st.markdown(_public_panel(base, idx, spec.left_title, spec.left_tag, fault_ts),
                            unsafe_allow_html=True)
        with right:
            if kind == "fleet":
                st.markdown(_fleet_panel(sent, idx, spec.right_title, spec.right_tag,
                                         spec.show_cost, cap_kw), unsafe_allow_html=True)
            else:
                st.markdown(_public_panel(sent, idx, spec.right_title, spec.right_tag, fault_ts),
                            unsafe_allow_html=True)

        if spec.show_price and prices:
            st.markdown(_price_chart(prices, idx, clocks, base.frames[idx].ts),
                        unsafe_allow_html=True)

        a, b = st.columns([1.5, 1])
        with a:
            st.markdown(_verdict(base, sent, idx, n_frames, kind,
                                 spec.show_cost, spec.show_response_ms),
                        unsafe_allow_html=True)
        with b:
            st.markdown(
                '<div style="border:1px solid #E3E8EF;border-radius:14px;padding:10px 12px;background:#fff">'
                '<div style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#8A94A6;'
                'font-weight:650;margin-bottom:6px">Incident feed</div>'
                + _incident_feed(spec.events, base.frames[idx].ts) + "</div>",
                unsafe_allow_html=True,
            )

        if spec.footnote and not _RECORD:
            st.markdown(
                f'<div style="margin-top:16px;font-size:11.5px;line-height:1.65;color:#8A94A6">{spec.footnote}</div>',
                unsafe_allow_html=True,
            )

    @st.fragment(run_every=0.28 if st.session_state.get(f"{spec.key}_playing") else None)
    def _player() -> None:
        if st.session_state.get(f"{spec.key}_playing"):
            nxt = st.session_state[f"{spec.key}_idx"] + st.session_state[f"{spec.key}_advance"]
            if nxt >= n_frames - 1:
                st.session_state[f"{spec.key}_idx"] = n_frames - 1
                st.session_state[f"{spec.key}_playing"] = False
                _block()
                st.rerun(scope="app")
                return
            st.session_state[f"{spec.key}_idx"] = nxt
        _block()

    _player()
