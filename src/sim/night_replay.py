"""
Kempower Self-Operating Charging Network - Night Replay Engine
Module: src/sim/night_replay.py

Turns the 2026-11-12 -> 2026-11-13 night at S1 (24 bidirectional buses, 18:58 -> 07:00)
into a frame-by-frame sequence so the Streamlit dashboard can *animate* what happens
instead of showing four static tables.

Two scenarios are simulated on the exact same fleet:

    BASELINE  : 12 physical connection points + one operator shift at 00:30
                (the operator habits observed in operations_log.csv)
    TIER 3b   : 24 connection points + cabinet busbar, zero human action
                (hardware scenario, NOT the shipped 0-CAPEX software result)

Both scenarios get the same physical shock at the same minute:
    02:25  cabinet C1-3 overtemperature stop (F016, cleared 06:31 by a technician)

Why the two scenarios differ in the fault model (this is the whole point):
    - BASELINE kills 4 points (C1-3 carries 4 of the 12 single-gun dispensers).
      A cable plugged into a dead cabinet cannot be unplugged by nobody -> the bus
      goes back to the queue and loses the rest of the night.
    - SENTINEL keeps all 24 points alive because the cabinet busbar re-routes them,
      and only the station capacity drops 1,080 -> 720 kW. Buses keep charging.

All numbers are derived from the 45 official CSVs; nothing is hardcoded except the
fault timestamps, which come from faults.csv (F015 01:50, F016 02:25 -> 06:31).
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Sequence

from src.utils.paths import resolve_csv_path

# --------------------------------------------------------------------------- constants
NIGHT_DAY = "2026-11-12"          # arrive_ts of the cross-midnight shift
CAP_DC_KW = 1080.0                # 3 power cabinets x 360 kW (chargers.csv)
CAP_TWO_CABINETS_KW = 720.0       # C1-3 offline -> 2 cabinets left
GUNS_BASELINE = 12                # dispensers currently installed at S1
POINTS_SENTINEL = 24              # one dual-gun satellite per dispenser
GRID_LIMIT_KW = 1200.0            # network_sites.csv S1

FAULT_TS = "2026-11-13T02:25:00+02:00"       # F016 overtemperature stop
FAULT_CLEARED_TS = "2026-11-13T06:31:00+02:00"
PRECURSOR_TS = "2026-11-12T22:31:00+02:00"   # D1-9 59.3 C / 702 rpm (telemetry_1min.csv)
BATCH_TS = "2026-11-13T00:30:00+02:00"       # operator's one bulk swap of the night

SOC_TAPER_START = 0.80            # constant-voltage taper begins here
TAPER_DEPTH = 0.90
TAPER_EXP = 1.20
STEP_MINUTES = 1.0

# Frame states used by the UI
CHARGING, WAITING, DONE, MISSED, IDLE = "charging", "waiting", "done", "missed", "idle"


@dataclass(frozen=True)
class Bus:
    """One bidirectional bus that must reach soc_req before it departs."""

    vehicle_id: str
    arrive: datetime
    depart: datetime
    battery_kwh: float
    soc_arrive: float
    soc_required: float
    max_kw: float

    @property
    def need_kwh(self) -> float:
        return self.battery_kwh * (self.soc_required - self.soc_arrive)


@dataclass
class Frame:
    """One 1-minute snapshot, ready to be rendered as a single animation frame."""

    ts: datetime
    states: Dict[str, str]        # vehicle_id -> charging|waiting|done|missed|idle
    kw: Dict[str, float]          # vehicle_id -> instantaneous DC power
    soc: Dict[str, float]         # vehicle_id -> state of charge (0-1)
    total_kw: float               # station DC load this minute
    capacity_kw: float            # available station capacity this minute
    moves: int                    # cumulative human re-plug actions
    delivered_kwh: float          # cumulative kWh delivered so far
    missed_so_far: int            # buses already known to have left short


@dataclass
class Replay:
    """A full night, plus the summary numbers the UI shows next to the animation."""

    label: str
    frame_minutes: List[int]      # minute offset from 00:00 of the first frame
    frames: List[Frame]
    buses: List[Bus]
    missed: List[str]
    missed_kwh: float
    delivered_kwh: float
    moves: int
    last_full: Optional[datetime]
    never_plugged: List[str]

    @property
    def clock_labels(self) -> List[str]:
        return [f.ts.strftime("%H:%M") for f in self.frames]


# --------------------------------------------------------------------------- loading
def load_buses(day: str = NIGHT_DAY) -> List[Bus]:
    """Cross-midnight S1 shifts. A bus qualifies when depart.date() > arrive.date()."""
    vehicles = {
        r["vehicle_id"]: r
        for r in csv.DictReader(open(resolve_csv_path("vehicles.csv"), encoding="utf-8"))
    }
    buses: List[Bus] = []
    with open(resolve_csv_path("fleet_schedule.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["site_id"] != "S1" or not row["arrive_ts"].startswith(day):
                continue
            arrive = datetime.fromisoformat(row["arrive_ts"])
            depart = datetime.fromisoformat(row["depart_ts"])
            if depart.date() == arrive.date():
                continue                      # same-day shift, not part of the night
            v = vehicles[row["vehicle_id"]]
            buses.append(
                Bus(
                    vehicle_id=row["vehicle_id"],
                    arrive=arrive,
                    depart=depart,
                    battery_kwh=float(v["battery_kwh"]),
                    soc_arrive=float(row["arrive_soc_pct"]) / 100.0,
                    soc_required=float(row["required_soc_pct"]) / 100.0,
                    max_kw=float(v["max_charge_kw"]),
                )
            )
    return sorted(buses, key=lambda b: (b.arrive, b.vehicle_id))


def taper_limit(bus: Bus, soc: float) -> float:
    """Constant-voltage taper: above 80% SoC the vehicle stops accepting full power."""
    if soc <= SOC_TAPER_START:
        return bus.max_kw
    x = min((soc - SOC_TAPER_START) / (1.0 - SOC_TAPER_START), 1.0)
    return bus.max_kw * max(1.0 - TAPER_DEPTH, 1.0 - TAPER_DEPTH * x**TAPER_EXP)


# --------------------------------------------------------------------------- simulation
def replay(
    buses: Sequence[Bus],
    n_points: int,
    *,
    label: str,
    replug: str = "none",
    batch_ts: Optional[datetime] = None,
    fault_ts: Optional[datetime] = None,
    dead_points: int = 0,
    capacity_before_kw: float = CAP_DC_KW,
    capacity_after_kw: float = CAP_TWO_CABINETS_KW,
) -> Replay:
    """
    Minute-by-minute dispatch.

    replug: "none"  -> zero-human: a bus plugs in exactly once, on arrival
            "batch" -> one operator shift at batch_ts (everyone re-plugged once)
    dead_points: how many of the last n_points physically die at fault_ts.
                 0 means the cabinet busbar keeps every point alive (capacity-only loss).
    """
    n = n_points
    points: List[Optional[Bus]] = [None] * n
    alive = [True] * n
    soc: Dict[str, float] = {b.vehicle_id: b.soc_arrive for b in buses}
    got: Dict[str, float] = {b.vehicle_id: 0.0 for b in buses}
    seen: set[str] = set()
    waiting: List[Bus] = []
    finished: Dict[str, datetime] = {}
    moves = 0
    frames: List[Frame] = []

    t = min(b.arrive for b in buses)
    end = max(b.depart for b in buses)
    dt = timedelta(minutes=STEP_MINUTES)
    fault_done = batch_done = False

    def is_full(b: Bus) -> bool:
        return soc[b.vehicle_id] >= b.soc_required - 1e-9

    while t <= end:
        # ---- 1. physical shock: cabinet dies -------------------------------
        if fault_ts is not None and dead_points and not fault_done and t >= fault_ts:
            fault_done = True
            for i in range(n - dead_points, n):
                alive[i] = False
                if points[i] is not None:
                    lost = points[i]
                    if not is_full(lost):
                        waiting.append(lost)      # cable stuck: nobody there to unplug it
                    points[i] = None

        # ---- 2. arrivals: plug in once, or queue ---------------------------
        for b in buses:
            if b.vehicle_id in seen or b.arrive > t:
                continue
            seen.add(b.vehicle_id)
            slot = next((i for i in range(n) if alive[i] and points[i] is None), None)
            if slot is None:
                waiting.append(b)
            else:
                points[slot] = b

        # ---- 3. releases ---------------------------------------------------
        for i in range(n):
            if points[i] is not None and (is_full(points[i]) or t >= points[i].depart):
                points[i] = None

        # ---- 4. optional human shift ---------------------------------------
        if replug == "batch" and batch_ts is not None and not batch_done and t >= batch_ts:
            batch_done = True
            waiting.sort(key=lambda b: b.arrive)
            for i in range(n):
                if alive[i] and points[i] is None and waiting:
                    nxt = waiting.pop(0)
                    if nxt.depart > t and not is_full(nxt):
                        points[i] = nxt
                        moves += 1

        # ---- 5. urgency-weighted water filling ------------------------------
        active = [p for p in points if p is not None and not is_full(p)]
        total_kw = 0.0
        if active:
            capacity = capacity_before_kw if (fault_ts is None or t < fault_ts) else capacity_after_kw
            weight = {
                b.vehicle_id: max(b.need_kwh - got[b.vehicle_id], 0.0)
                / max((b.depart - t).total_seconds() / 3600.0, 0.05)
                for b in active
            }
            alloc = {b.vehicle_id: 0.0 for b in active}
            pool = capacity
            pending = list(active)
            while pending and pool > 1e-9:
                total_w = sum(weight[b.vehicle_id] for b in pending)
                if total_w <= 1e-9:
                    break
                scale = pool / total_w
                capped = [
                    (b, min(taper_limit(b, soc[b.vehicle_id]), b.max_kw))
                    for b in pending
                    if weight[b.vehicle_id] * scale
                    >= min(taper_limit(b, soc[b.vehicle_id]), b.max_kw) - 1e-9
                ]
                if not capped:
                    for b in pending:
                        alloc[b.vehicle_id] = weight[b.vehicle_id] * scale
                    pool = 0.0
                    break
                for b, limit in capped:
                    alloc[b.vehicle_id] = limit
                    pool -= limit
                    pending.remove(b)
            for b in active:
                share = max(
                    0.0, min(alloc[b.vehicle_id] * STEP_MINUTES / 60.0, b.need_kwh - got[b.vehicle_id])
                )
                got[b.vehicle_id] += share
                soc[b.vehicle_id] = min(
                    b.soc_required, b.soc_arrive + got[b.vehicle_id] / b.battery_kwh
                )
                if is_full(b) and b.vehicle_id not in finished:
                    finished[b.vehicle_id] = t
            total_kw = sum(alloc.values())

        # ---- 6. snapshot ---------------------------------------------------
        states: Dict[str, str] = {}
        kw_now: Dict[str, float] = {}
        occupied = {id(p): p for p in points if p is not None}
        charging_ids = {p.vehicle_id for p in active}
        for b in buses:
            if b.arrive > t:
                states[b.vehicle_id] = IDLE
            elif b.vehicle_id in charging_ids:
                states[b.vehicle_id] = CHARGING
                kw_now[b.vehicle_id] = alloc.get(b.vehicle_id, 0.0)
            elif is_full(b):
                states[b.vehicle_id] = DONE
            elif b.depart <= t:
                states[b.vehicle_id] = MISSED
            else:
                states[b.vehicle_id] = WAITING
        # a bus that already left short cannot be re-labelled by a later plug-in
        for b in buses:
            if b.depart <= t and got[b.vehicle_id] < b.need_kwh - 1.0:
                states[b.vehicle_id] = MISSED
                kw_now[b.vehicle_id] = 0.0

        frames.append(
            Frame(
                ts=t,
                states=states,
                kw=kw_now,
                soc=dict(soc),
                total_kw=total_kw,
                capacity_kw=(capacity_before_kw if (fault_ts is None or t < fault_ts) else capacity_after_kw),
                moves=moves,
                delivered_kwh=sum(got.values()),
                missed_so_far=sum(1 for b in buses if b.depart <= t and got[b.vehicle_id] < b.need_kwh - 1.0),
            )
        )
        t += dt

    missed = [b.vehicle_id for b in buses if got[b.vehicle_id] < b.need_kwh - 1.0]
    return Replay(
        label=label,
        frame_minutes=[int((f.ts - frames[0].ts).total_seconds() // 60) for f in frames],
        frames=frames,
        buses=list(buses),
        missed=missed,
        missed_kwh=round(sum(b.need_kwh - got[b.vehicle_id] for b in buses if b.vehicle_id in missed), 1),
        delivered_kwh=round(sum(got.values()), 1),
        moves=moves,
        last_full=max(finished.values()) if finished else None,
        never_plugged=[b.vehicle_id for b in buses if got[b.vehicle_id] < 1.0],
    )


# --------------------------------------------------------------------------- scenarios
def build_baseline() -> Replay:
    """What actually happened: 12 dispensers, one operator shift at 00:30, C1-3 dies."""
    return replay(
        load_buses(),
        GUNS_BASELINE,
        label="Baseline — 12 dispensers, 1 operator shift",
        replug="batch",
        batch_ts=datetime.fromisoformat(BATCH_TS),
        fault_ts=datetime.fromisoformat(FAULT_TS),
        dead_points=4,                    # C1-3 carries 4 of the 12 single-gun dispensers
    )


def build_sentinel() -> Replay:
    """Tier 3b hardware scenario: 24 points + cabinet busbar, zero human action.

    This is not the shipped product. The zero-CAPEX software result (S1 4 -> 3 missed,
    0 human moves, 398.5 -> 48.8 kWh) is computed by discrete_sim.py and printed by
    verify_all.py; this lane only shows what a busbar tie + dual guns would buy.
    """
    return replay(
        load_buses(),
        POINTS_SENTINEL,
        label="Tier 3b — 24 points + busbar, zero human action",
        replug="none",
        fault_ts=datetime.fromisoformat(FAULT_TS),
        dead_points=0,                    # busbar re-routes; only capacity is lost
    )


def build_no_busbar() -> Replay:
    """Counter-evidence: 24 points *without* the busbar lose 8 cables to the dead cabinet."""
    return replay(
        load_buses(),
        POINTS_SENTINEL,
        label="24 points, no cabinet busbar",
        replug="none",
        fault_ts=datetime.fromisoformat(FAULT_TS),
        dead_points=8,                    # C1-3 carries 8 of the 24 points
    )


def build_all() -> Dict[str, Replay]:
    buses = load_buses()
    detach = datetime.fromisoformat(FAULT_TS)
    return {
        "baseline": replay(
            buses,
            GUNS_BASELINE,
            label="Baseline — 12 dispensers, 1 operator shift",
            replug="batch",
            batch_ts=datetime.fromisoformat(BATCH_TS),
            fault_ts=detach,
            dead_points=4,
        ),
        "sentinel": replay(
            buses,
            POINTS_SENTINEL,
            label="Tier 3b — 24 points + busbar, zero human action",
            replug="none",
            fault_ts=detach,
            dead_points=0,
        ),
        "no_busbar": replay(
            buses,
            POINTS_SENTINEL,
            label="24 points, no cabinet busbar",
            replug="none",
            fault_ts=detach,
            dead_points=8,
        ),
    }
