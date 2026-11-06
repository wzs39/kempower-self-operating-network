"""
Kempower Self-Operating Charging Network - Connectivity Outage Replay (S3)
Module: src/sim/outage_replay.py

Second replay scenario, complementing night_replay.py (S1 thermal trip).

    S3 highway public hub, 2026-11-13, 256 arrivals, 10 dispensers
    (D3-1..D3-8 = 300 kW, D3-9/D3-10 = 150 kW), 1,500 kW AC grid limit.

    11:00 -> 13:00  cellular outage (connectivity_outages.csv, the only S3
                    outage on the scenario day).

Two answers to the exact same arrivals:

    BASELINE  : the vendor's conservative offline fallback, 50 kW per dispenser
                (site_config.csv: offline_fallback_kw_per_dispenser = 50)
                -> station collapses 1,425 kW -> 500 kW for two hours.
    SENTINEL  : edge islanding. The cloud is unreachable, but nothing on site
                needs the cloud to divide power. Local DLM keeps 1,425 kW DC
                (1,492.15 kW AC <= 1,500 kW grid limit).

Nothing here is hardcoded except the two capacity levels, both of which come
from site_config.csv / chargers.csv. Arrivals, energy demand and driver
patience (max_wait_min) are read row by row from public_arrivals.csv.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Sequence

from src.utils.paths import resolve_csv_path

DAY = "2026-11-13"
OUTAGE_START = "2026-11-13T11:00:00+02:00"
OUTAGE_END = "2026-11-13T13:00:00+02:00"

GRID_LIMIT_AC_KW = 1500.0
CAP_NORMAL_DC_KW = 1425.0            # InverterEfficiencyGuard.max_safe_dc_kw(1500)
CAP_OUTAGE_FALLBACK_KW = 500.0       # 10 dispensers x 50 kW naive fallback
GUN_LIMITS_KW = [300.0] * 8 + [150.0] * 2
CLASS_LIMIT_KW = {"car": 150.0, "van": 150.0, "truck": 300.0}
STEP_MINUTES = 1.0

CHARGING, WAITING, DONE, LEFT, IDLE = "charging", "waiting", "done", "left", "idle"


@dataclass(frozen=True)
class Arrival:
    arrival_id: str
    arrive: datetime
    vehicle_class: str
    need_kwh: float
    max_wait_min: float

    @property
    def max_kw(self) -> float:
        return CLASS_LIMIT_KW.get(self.vehicle_class, 150.0)


@dataclass
class Frame:
    ts: datetime
    states: Dict[str, str]
    kw: Dict[str, float]
    guns: List[Optional[str]]         # arrival_id occupying each dispenser
    total_kw: float
    capacity_kw: float
    online: bool
    delivered_kwh: float
    abandoned_so_far: int
    charging_now: int
    queue_now: int


@dataclass
class OutageReplay:
    label: str
    frames: List[Frame]
    arrivals: List[Arrival]
    abandoned: List[str]
    delivered_kwh: float
    charged: int

    @property
    def abandonment_pct(self) -> float:
        return round(100.0 * len(self.abandoned) / max(1, len(self.arrivals)), 2)

    @property
    def clock_labels(self) -> List[str]:
        return [f.ts.strftime("%H:%M") for f in self.frames]


def load_arrivals(day: str = DAY) -> List[Arrival]:
    out: List[Arrival] = []
    with open(resolve_csv_path("public_arrivals.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["site_id"] != "S3" or not row["ts"].startswith(day):
                continue
            out.append(
                Arrival(
                    arrival_id=row["arrival_id"],
                    arrive=datetime.fromisoformat(row["ts"]),
                    vehicle_class=row["vehicle_class"],
                    need_kwh=float(row["energy_wanted_kwh"]),
                    max_wait_min=float(row["max_wait_min"]),
                )
            )
    return sorted(out, key=lambda a: (a.arrive, a.arrival_id))


def replay(
    arrivals: Sequence[Arrival],
    *,
    label: str,
    outage_start: datetime,
    outage_end: datetime,
    cap_normal_kw: float = CAP_NORMAL_DC_KW,
    cap_outage_kw: float = CAP_OUTAGE_FALLBACK_KW,
) -> OutageReplay:
    """Minute-by-minute public-hub simulation with an impatience queue."""
    n = len(GUN_LIMITS_KW)
    guns: List[Optional[Arrival]] = [None] * n
    got: Dict[str, float] = {a.arrival_id: 0.0 for a in arrivals}
    seen: set[str] = set()
    waiting: List[Arrival] = []
    wait_since: Dict[str, datetime] = {}
    abandoned: List[str] = []
    frames: List[Frame] = []

    t = min(a.arrive for a in arrivals).replace(hour=0, minute=0)
    end = max(a.arrive for a in arrivals) + timedelta(hours=8)
    dt = timedelta(minutes=STEP_MINUTES)

    while t <= end:
        online = not (outage_start <= t < outage_end)
        capacity = cap_normal_kw if online else cap_outage_kw

        # 1. arrivals: take a free dispenser, else join the queue
        for a in arrivals:
            if a.arrival_id in seen or a.arrive > t:
                continue
            seen.add(a.arrival_id)
            slot = next((i for i in range(n) if guns[i] is None), None)
            if slot is None:
                waiting.append(a)
                wait_since[a.arrival_id] = t
            else:
                guns[slot] = a

        # 2. drivers who ran out of patience leave without charging
        still: List[Arrival] = []
        for a in waiting:
            if (t - wait_since[a.arrival_id]).total_seconds() / 60.0 >= a.max_wait_min:
                abandoned.append(a.arrival_id)
            else:
                still.append(a)
        waiting = still

        # 3. finished vehicles free their dispenser, queue moves up
        for i in range(n):
            a = guns[i]
            if a is not None and got[a.arrival_id] >= a.need_kwh - 1e-9:
                guns[i] = None
        for i in range(n):
            if guns[i] is None and waiting:
                nxt = waiting.pop(0)
                wait_since.pop(nxt.arrival_id, None)
                guns[i] = nxt

        # 4. split the station budget evenly, capped per dispenser and per vehicle
        active = [(i, a) for i, a in enumerate(guns) if a is not None]
        alloc: Dict[str, float] = {}
        total_kw = 0.0
        if active:
            pool = capacity
            pending = list(active)
            while pending and pool > 1e-9:
                share = pool / len(pending)
                capped = [
                    (i, a) for i, a in pending
                    if share >= min(GUN_LIMITS_KW[i], a.max_kw) - 1e-9
                ]
                if not capped:
                    for i, a in pending:
                        alloc[a.arrival_id] = share
                    pool = 0.0
                    break
                for i, a in capped:
                    limit = min(GUN_LIMITS_KW[i], a.max_kw)
                    alloc[a.arrival_id] = limit
                    pool -= limit
                    pending = [(j, b) for j, b in pending if j != i]
            for _, a in active:
                kw = alloc.get(a.arrival_id, 0.0)
                got[a.arrival_id] = min(
                    a.need_kwh, got[a.arrival_id] + kw * STEP_MINUTES / 60.0
                )
            total_kw = sum(alloc.values())

        # 5. snapshot
        states: Dict[str, str] = {}
        kw_now: Dict[str, float] = {}
        charging_ids = {a.arrival_id for _, a in active}
        waiting_ids = {a.arrival_id for a in waiting}
        for a in arrivals:
            if a.arrive > t:
                states[a.arrival_id] = IDLE
            elif a.arrival_id in abandoned:
                states[a.arrival_id] = LEFT
            elif a.arrival_id in charging_ids:
                states[a.arrival_id] = CHARGING
                kw_now[a.arrival_id] = alloc.get(a.arrival_id, 0.0)
            elif got[a.arrival_id] >= a.need_kwh - 1e-9:
                states[a.arrival_id] = DONE
            elif a.arrival_id in waiting_ids:
                states[a.arrival_id] = WAITING
            else:
                states[a.arrival_id] = IDLE
        frames.append(
            Frame(
                ts=t,
                states=states,
                kw=kw_now,
                guns=[a.arrival_id if a else None for a in guns],
                total_kw=total_kw,
                capacity_kw=capacity,
                online=online,
                delivered_kwh=sum(got.values()),
                abandoned_so_far=len(abandoned),
                charging_now=len(active),
                queue_now=len(waiting),
            )
        )
        t += dt

    return OutageReplay(
        label=label,
        frames=frames,
        arrivals=list(arrivals),
        abandoned=abandoned,
        delivered_kwh=round(sum(got.values()), 1),
        charged=sum(1 for a in arrivals if got[a.arrival_id] >= a.need_kwh - 1e-9),
    )


def build_all() -> Dict[str, OutageReplay]:
    arrivals = load_arrivals()
    start = datetime.fromisoformat(OUTAGE_START)
    end = datetime.fromisoformat(OUTAGE_END)
    return {
        "baseline": replay(
            arrivals,
            label="Baseline — 50 kW offline fallback",
            outage_start=start,
            outage_end=end,
            cap_outage_kw=CAP_OUTAGE_FALLBACK_KW,
        ),
        "sentinel": replay(
            arrivals,
            label="Sentinel — edge islanding, full local power",
            outage_start=start,
            outage_end=end,
            cap_outage_kw=CAP_NORMAL_DC_KW,
        ),
    }
