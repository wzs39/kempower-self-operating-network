"""
Overnight charging station power allocation and yard move accounting.

A reproducible discrete-time simulation: given vehicle time windows, energy demands,
connection points, and rectification capacity, calculates on-time completion,
required physical replugs, and failure impact under hardware faults.

Three critical physical behaviors modeled:
  1. Constant Voltage (CV) taper — vehicle charge acceptance drops significantly above 80% SoC,
     causing charging speed to decrease in the late stage.
  2. Cabinet failure causes dropped dispensers rather than uniform throttling — C1-3 shutdown
     directly cuts power to its 4 connected points, interrupting active charging.
  3. Physical replug latency — each manual move_and_replug requires 8 minutes, during which
     the dispenser remains idle.

Two dispatch strategies:
  fcfs    — Baseline status quo. First-come first-served; queueing when full; manual moves when empty.
  urgency — Zero-human autonomy. All vehicles plugged in on arrival; dynamic power distribution
             proportional to urgency (remaining energy needed / remaining dwell time),
             equivalent to a continuous-power Earliest Deadline First (EDF) scheduler.

All inputs originate from data/*.csv without hardcoded results.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
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
class Point:
    """A connection point (charging gun / dispenser)."""

    idx: int
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


def taper_limit(job: Job, soc: float) -> float:
    """CV taper power derating: above 80% SoC, maximum acceptable power drops non-linearly."""
    if soc <= SOC_TAPER_START:
        return job.max_kw
    x = min((soc - SOC_TAPER_START) / (1.0 - SOC_TAPER_START), 1.0)
    return job.max_kw * max(1.0 - TAPER_DEPTH, 1.0 - TAPER_DEPTH * x ** TAPER_EXP)


def cap_profile(events: list[tuple[datetime, float]]):
    """Converts a step-wise capacity event timeline into a continuous t -> cap_kw function."""
    ordered = sorted(events)

    def f(t: datetime) -> float:
        cur = ordered[0][1]
        for ts, cap in ordered:
            if t >= ts:
                cur = cap
        return cur

    return f


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


def simulate(
    jobs: list[Job],
    n_points: int,
    cap_kw: float,
    strategy: str = "fcfs",
    step_min: float = 1.0,
    cap_fn=None,
    fault: tuple[datetime, int] | None = None,
    move_delay_min: float = 0.0,
) -> Result:
    """Simulates an overnight charging schedule.

    strategy      : "fcfs" (first-come first-served + queue replugs) or "urgency" (all connected, urgency-weighted)
    cap_fn        : t -> available capacity in kW
    fault         : (timestamp, dropped_guns), models power cabinet outage causing dispenser deactivation
    move_delay_min: delay before newly replugged vehicle can draw power (8 minutes per operations_log)
    """
    if not jobs:
        return Result()

    if cap_fn is None:
        cap_fn = lambda t: cap_kw  # noqa: E731

    points = [Point(idx=i) for i in range(n_points)]
    delivered = {j.vehicle_id: 0.0 for j in jobs}
    soc = {j.vehicle_id: j.soc_in for j in jobs}
    waiting: list[Job] = []
    seen: set[str] = set()
    moves = 0
    peak = 0.0
    fault_fired = False
    finish_at: dict[str, datetime] = {}

    t = min(j.arrive for j in jobs)
    end = max(j.depart for j in jobs)
    dt = timedelta(minutes=step_min)

    def finished(j: Job) -> bool:
        return soc[j.vehicle_id] >= j.soc_req - 1e-9

    while t <= end:
        # ---- 1) Fault Injection: Dropped guns cut off active charging vehicles ----
        if fault and not fault_fired and t >= fault[0]:
            fault_fired = True
            for p in points[-fault[1]:]:
                p.alive = False
                if p.job is not None:
                    if not finished(p.job):
                        waiting.append(p.job)
                    p.job = None
            waiting.sort(key=lambda x: x.arrive)

        live = [p for p in points if p.alive]
        cap_now = cap_fn(t)

        # ---- 2) Arrival: Connect to available live points ----
        for j in jobs:
            if j.vehicle_id in seen or j.arrive > t:
                continue
            seen.add(j.vehicle_id)
            free = next((p for p in live if p.job is None), None)
            if free is not None:
                free.job = j
                free.ready_at = t
            else:
                waiting.append(j)

        # ---- 3) Release fully charged or departed vehicles ----
        for p in live:
            if p.job is not None and (finished(p.job) or t >= p.job.depart):
                p.job = None

        # ---- 4) Fill vacant points from waiting queue ----
        for p in live:
            if p.job is None and waiting:
                waiting.sort(key=lambda x: x.arrive)
                nxt = waiting.pop(0)
                if nxt.depart > t:
                    p.job = nxt
                    if strategy == "fcfs":
                        p.ready_at = t + timedelta(minutes=move_delay_min)
                        moves += 1          # Manual vehicle repositioning + plug-in
                    else:
                        p.ready_at = t      # Autonomous matrix routing, zero manual delay

        # ---- 5) Power Allocation & Charging ----
        active = [
            p.job for p in live
            if p.job is not None and not finished(p.job)
            and (p.ready_at is None or t >= p.ready_at)
        ]

        if strategy == "fcfs":
            per_point = cap_now / max(len(live), 1)
            peak = max(peak, per_point * len(active))
            for j in active:
                limit = min(per_point, taper_limit(j, soc[j.vehicle_id]))
                room = j.need_kwh - delivered[j.vehicle_id]
                add = max(0.0, min(limit * step_min / 60.0, room))
                delivered[j.vehicle_id] += add
                soc[j.vehicle_id] = min(
                    j.soc_req, j.soc_in + delivered[j.vehicle_id] / j.battery_kwh
                )
                if finished(j) and j.vehicle_id not in finish_at:
                    finish_at[j.vehicle_id] = t
        elif active:
            weight = {}
            for j in active:
                remain_h = max((j.depart - t).total_seconds() / 3600.0, 0.05)
                weight[j.vehicle_id] = (j.need_kwh - delivered[j.vehicle_id]) / remain_h

            # Water-filling distribution: vehicles constrained by taper or vehicle max take their share,
            # remaining capacity is proportionally allocated to unconstrained vehicles until fully allocated.
            alloc_kw = {j.vehicle_id: 0.0 for j in active}
            pool = cap_now
            pending = list(active)
            while pending and pool > 1e-9:
                total_w = sum(weight[j.vehicle_id] for j in pending)
                if total_w <= 1e-9:
                    break
                scale = pool / total_w
                capped = []
                for j in pending:
                    want = weight[j.vehicle_id] * scale
                    limit = min(taper_limit(j, soc[j.vehicle_id]), j.max_kw)
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

            peak = max(peak, sum(alloc_kw.values()))
            for j in active:
                room = j.need_kwh - delivered[j.vehicle_id]
                add = max(0.0, min(alloc_kw[j.vehicle_id] * step_min / 60.0, room))
                delivered[j.vehicle_id] += add
                soc[j.vehicle_id] = min(
                    j.soc_req, j.soc_in + delivered[j.vehicle_id] / j.battery_kwh
                )
                if finished(j) and j.vehicle_id not in finish_at:
                    finish_at[j.vehicle_id] = t

        t += dt

    under = [
        (j.vehicle_id, round(j.need_kwh - delivered[j.vehicle_id], 1))
        for j in jobs
        if delivered[j.vehicle_id] < j.need_kwh - 1.0
    ]
    never = [j.vehicle_id for j in jobs if delivered[j.vehicle_id] < 1.0]
    return Result(
        delivered=delivered,
        moves=moves,
        undercharged=under,
        peak_kw=round(peak, 1),
        total_kwh=round(sum(delivered.values()), 1),
        stranded=never,
        last_finish=max(finish_at.values()) if finish_at else None,
    )
