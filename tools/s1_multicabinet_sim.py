"""
Charging station overnight power allocation and yard move accounting.

A discrete-time simulation: given vehicle arrival windows, energy demands, and cabinet configurations,
calculates on-time completion, required physical yard replugs, and failure impact under hardware faults.

Physical behaviors modeled:
1. CV taper (Constant Voltage):
   Vehicle charge acceptance drops significantly above 80% SoC, decreasing charging speed in the late stage.
2. Cabinet failure causes dropped cabinets rather than uniform throttling:
   S1 has 3 power cabinets (360 kW each, 4 satellites per cabinet). C1-3 shutdown directly de-energizes
   its 4 connected points.
3. Cross-cabinet busbar redundancy (cross_tie):
   By default, each cabinet only powers its assigned dispensers. Adding a cross-cabinet busbar tie
   allows any surviving cabinet to power any dispenser.
4. Physical replug latency:
   Each manual move_and_replug takes 8 minutes (staff_minutes in operations_log.csv).

Two dispatch strategies:
  fcfs    — Status quo baseline. First-come first-served; queueing when full; manual moves when empty.
  urgency — Zero-human autonomy. All vehicles connected; dynamic power allocation proportional to urgency.

All inputs originate from data/*.csv without hardcoded results.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.utils.paths import get_data_dir

DATA_DIR = get_data_dir()

SOC_TAPER_START = 0.80
TAPER_EXP = 1.2
TAPER_DEPTH = 0.9

@dataclass
class Job:
    """Overnight vehicle charging job."""

    vehicle_id: str
    arrive: datetime
    depart: datetime
    battery_kwh: float
    soc_in: float
    soc_req: float
    max_kw: float = 150.0

    @property
    def need_kwh(self) -> float:
        return self.battery_kwh * (self.soc_req - self.soc_in)

    @property
    def window_h(self) -> float:
        return (self.depart - self.arrive).total_seconds() / 3600.0

    @property
    def avg_kw_needed(self) -> float:
        return self.need_kwh / self.window_h if self.window_h > 0 else float("inf")

@dataclass
class Cabinet:
    """A power rectifier cabinet."""

    idx: int
    cap_kw: float
    alive: bool = True

@dataclass
class Point:
    """A connection point (gun) assigned physically to a cabinet."""

    idx: int
    cabinet_idx: int
    job: Job | None = None
    alive: bool = True
    ready_at: datetime | None = None

@dataclass
class Result:
    delivered: dict[str, float] = field(default_factory=dict)
    moves: int = 0
    undercharged: list[tuple[str, float]] = field(default_factory=list)
    peak_kw: float = 0.0
    total_kwh: float = 0.0
    stranded: list[str] = field(default_factory=list)
    last_finish: datetime | None = None

    def summary(self) -> str:
        return (
            f"Moves: {self.moves} | Undercharged: {len(self.undercharged)} | "
            f"Peak: {self.peak_kw:.0f} kW | Delivered: {self.total_kwh:.0f} kWh"
        )

def taper_limit(job: Job, soc: float) -> float:
    """CV taper derating: above 80% SoC, maximum acceptable power drops non-linearly."""
    if soc <= SOC_TAPER_START:
        return job.max_kw
    x = min((soc - SOC_TAPER_START) / (1.0 - SOC_TAPER_START), 1.0)
    return job.max_kw * max(1.0 - TAPER_DEPTH, 1.0 - TAPER_DEPTH * x ** TAPER_EXP)

def load_jobs(site_id: str = "S1", day: str = "2026-11-12", night_only: bool = True) -> list[Job]:
    """Loads station charging jobs directly from dataset CSV files."""
    vehicles = {}
    with open(DATA_DIR / "vehicles.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            vehicles[row["vehicle_id"]] = row

    jobs: list[Job] = []
    with open(DATA_DIR / "fleet_schedule.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["site_id"] != site_id or not row["arrive_ts"].startswith(day):
                continue
            arrive = datetime.fromisoformat(row["arrive_ts"])
            if night_only and arrive.hour < 19:
                continue
            spec = vehicles[row["vehicle_id"]]
            jobs.append(
                Job(
                    vehicle_id=row["vehicle_id"],
                    arrive=arrive,
                    depart=datetime.fromisoformat(row["depart_ts"]),
                    battery_kwh=float(spec["battery_kwh"]),
                    soc_in=float(row["arrive_soc_pct"]) / 100.0,
                    soc_req=float(row["required_soc_pct"]) / 100.0,
                    max_kw=float(spec["max_charge_kw"]),
                )
            )
    jobs.sort(key=lambda j: j.arrive)
    return jobs

def _waterfill(jobs: list[Job], cap: float, soc: dict[str, float], delivered: dict[str, float],
               t: datetime, gun_kw: float) -> dict[str, float]:
    """Water-filling power allocation respecting CV taper and maximum charging power."""
    if not jobs or cap <= 1e-9:
        return {j.vehicle_id: 0.0 for j in jobs}

    weight = {}
    for j in jobs:
        remain_h = max((j.depart - t).total_seconds() / 3600.0, 0.05)
        weight[j.vehicle_id] = (j.need_kwh - delivered[j.vehicle_id]) / remain_h

    alloc_kw = {j.vehicle_id: 0.0 for j in jobs}
    pool = cap
    pending = list(jobs)
    while pending and pool > 1e-9:
        total_w = sum(weight[j.vehicle_id] for j in pending)
        if total_w <= 1e-9:
            break
        scale = pool / total_w
        capped = []
        for j in pending:
            want = weight[j.vehicle_id] * scale
            limit = min(taper_limit(j, soc[j.vehicle_id]), j.max_kw, gun_kw)
            if want >= limit - 1e-9:
                capped.append((j, limit))
        if not capped:
            for j in pending:
                alloc_kw[j.vehicle_id] = weight[j.vehicle_id] * scale
            pool = 0.0
            break
        for j, lim in capped:
            alloc_kw[j.vehicle_id] = lim
            pool -= lim
            pending.remove(j)

    return alloc_kw

def simulate(
    jobs: list[Job],
    cabinet_kw: list[float],
    points_per_cabinet: int,
    strategy: str = "fcfs",
    step_min: float = 1.0,
    fault: tuple[datetime, list[int]] | None = None,
    cross_tie: bool = False,
    move_delay_min: float = 0.0,
    gun_kw: float = 150.0,
) -> Result:
    """Simulates multi-cabinet overnight charging.

    cabinet_kw        : capacity of each rectifier cabinet (e.g. [360, 360, 360])
    points_per_cabinet: number of dispensers connected per cabinet (4 for 1-gun, 8 for dual-gun)
    strategy          : "fcfs" or "urgency"
    fault             : (timestamp, [cabinet_indices])
    cross_tie         : if True, surviving cabinets share power across all connection points
    move_delay_min    : yard move delay (8 minutes per operations_log)
    gun_kw            : physical hardware power limit per dispenser (150 kW)
    """
    if not jobs:
        return Result()

    n_cabs = len(cabinet_kw)
    cabinets = [Cabinet(idx=i, cap_kw=kw) for i, kw in enumerate(cabinet_kw)]
    points: list[Point] = []
    pidx = 0
    for c in cabinets:
        for _ in range(points_per_cabinet):
            points.append(Point(idx=pidx, cabinet_idx=c.idx))
            pidx += 1

    delivered = {j.vehicle_id: 0.0 for j in jobs}
    soc = {j.vehicle_id: j.soc_in for j in jobs}
    waiting: list[Job] = []
    seen: set[str] = set()
    moves = 0
    peak = 0.0
    fault_fired = False
    stranded: set[str] = set()
    finish_at: dict[str, datetime] = {}

    t = min(j.arrive for j in jobs)
    end = max(j.depart for j in jobs)
    dt = timedelta(minutes=step_min)

    def finished(j: Job) -> bool:
        return soc[j.vehicle_id] >= j.soc_req - 1e-9

    while t <= end:
        # ---- 1) Fault Injection ----
        if fault and not fault_fired and t >= fault[0]:
            fault_fired = True
            down_cabs = set(fault[1])
            for c in cabinets:
                if c.idx in down_cabs:
                    c.alive = False
            for p in points:
                if p.cabinet_idx in down_cabs:
                    if not cross_tie:
                        p.alive = False
                    if p.job is not None:
                        if not finished(p.job):
                            if cross_tie:
                                waiting.append(p.job)
                            else:
                                stranded.add(p.job.vehicle_id)
                        p.job = None
            waiting.sort(key=lambda x: x.arrive)

        live_pts = [p for p in points if p.alive]

        # ---- 2) Arrival ----
        for j in jobs:
            if j.vehicle_id in seen or j.arrive > t:
                continue
            seen.add(j.vehicle_id)
            free = next((p for p in live_pts if p.job is None), None)
            if free is not None:
                free.job = j
                free.ready_at = t
            else:
                waiting.append(j)

        # ---- 3) Release completed vehicles ----
        for p in live_pts:
            if p.job is not None and (finished(p.job) or t >= p.job.depart):
                p.job = None

        # ---- 4) Queue replenishment ----
        for p in live_pts:
            if p.job is None and waiting:
                waiting.sort(key=lambda x: x.arrive)
                nxt = waiting.pop(0)
                if nxt.depart > t:
                    p.job = nxt
                    if strategy == "fcfs":
                        p.ready_at = t + timedelta(minutes=move_delay_min)
                        moves += 1
                    else:
                        p.ready_at = t

        # ---- 5) Power Allocation ----
        active_pts = [
            p for p in live_pts
            if p.job is not None and not finished(p.job)
            and (p.ready_at is None or t >= p.ready_at)
        ]

        alloc_kw: dict[str, float] = {}
        if strategy == "fcfs":
            if cross_tie:
                total_cap = sum(c.cap_kw for c in cabinets if c.alive)
                per_pt = total_cap / max(len(live_pts), 1)
                for p in active_pts:
                    alloc_kw[p.job.vehicle_id] = min(
                        per_pt, taper_limit(p.job, soc[p.job.vehicle_id]), p.job.max_kw, gun_kw
                    )
            else:
                for c in cabinets:
                    c_live = [p for p in live_pts if p.cabinet_idx == c.idx]
                    c_act = [p for p in active_pts if p.cabinet_idx == c.idx]
                    if not c.alive or not c_act:
                        continue
                    per_pt = c.cap_kw / max(len(c_live), 1)
                    for p in c_act:
                        alloc_kw[p.job.vehicle_id] = min(
                            per_pt, taper_limit(p.job, soc[p.job.vehicle_id]), p.job.max_kw, gun_kw
                        )
        else:
            if cross_tie:
                total_cap = sum(c.cap_kw for c in cabinets if c.alive)
                alloc_kw = _waterfill([p.job for p in active_pts], total_cap, soc, delivered, t, gun_kw)
            else:
                for c in cabinets:
                    if not c.alive:
                        continue
                    c_act_jobs = [p.job for p in active_pts if p.cabinet_idx == c.idx]
                    alloc_kw.update(_waterfill(c_act_jobs, c.cap_kw, soc, delivered, t, gun_kw))

        peak = max(peak, sum(alloc_kw.values()))
        for j_id, kw in alloc_kw.items():
            job = next(j for j in jobs if j.vehicle_id == j_id)
            room = job.need_kwh - delivered[j_id]
            add = max(0.0, min(kw * step_min / 60.0, room))
            delivered[j_id] += add
            soc[j_id] = min(job.soc_req, job.soc_in + delivered[j_id] / job.battery_kwh)
            if finished(job) and j_id not in finish_at:
                finish_at[j_id] = t

        t += dt

    under = [
        (j.vehicle_id, round(j.need_kwh - delivered[j.vehicle_id], 1))
        for j in jobs
        if delivered[j.vehicle_id] < j.need_kwh - 1.0
    ]
    return Result(
        delivered=delivered,
        moves=moves,
        undercharged=under,
        peak_kw=round(peak, 1),
        total_kwh=round(sum(delivered.values()), 1),
        stranded=sorted(stranded),
        last_finish=max(finish_at.values()) if finish_at else None,
    )
