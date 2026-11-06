"""
Kempower Self-Operating Charging Network - Minute-by-Minute Discrete Simulation Engine
Module: src/sim/discrete_sim.py

Implements closed-loop discrete event simulation for Kempower charging stations:
1. Nonlinear Constant-Voltage (CV) Taper Curve (>80% SoC)
2. Kempower DPR Dynamic Intra/Inter-Cabinet Routing (Cross-Tie Busbar)
3. Urgency Waterfilling Algorithm (Earliest Deadline First with Continuous Power Allocation)
4. Hardware Contactor BBM Switching & Cable Multiplexing (0-CAPEX Virtual Replug vs Hardware Dual-Gun)
5. Minute-by-Minute Vehicle SoC Trajectories & Dynamic Missed Departure Verification
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

from src.utils.paths import resolve_csv_path

# Physics constants
SOC_TAPER_START: float = 0.80
TAPER_EXP: float = 1.2
TAPER_DEPTH: float = 0.90


@dataclass
class Job:
    """A vehicle charging demand job within a station timetable."""
    vehicle_id: str
    arrive: datetime
    depart: datetime
    battery_kwh: float
    soc_in: float
    soc_req: float
    max_kw: float = 150.0

    @property
    def need_kwh(self) -> float:
        return max(0.0, self.battery_kwh * (self.soc_req - self.soc_in))

    @property
    def window_h(self) -> float:
        return max(0.05, (self.depart - self.arrive).total_seconds() / 3600.0)

    @property
    def avg_kw_needed(self) -> float:
        return self.need_kwh / self.window_h if self.window_h > 0 else float("inf")


@dataclass
class Cabinet:
    """A modular Kempower DPR power cabinet."""
    idx: int
    kw: float
    alive: bool = True


@dataclass
class Point:
    """A physical satellite dispenser or charging connector."""
    idx: int
    cabinet: int
    job: Optional[Job] = None
    alive: bool = True
    ready_at: Optional[datetime] = None


@dataclass
class SimulationResult:
    """Structured results from a minute-by-minute discrete simulation run."""
    site_id: str
    date: str
    strategy: str
    delivered: Dict[str, float] = field(default_factory=dict)
    final_soc: Dict[str, float] = field(default_factory=dict)
    moves: int = 0
    undercharged: List[Tuple[str, float]] = field(default_factory=list)
    missed_departures: int = 0
    deficit_kwh: float = 0.0
    peak_kw: float = 0.0
    total_kwh: float = 0.0
    never_charged: List[str] = field(default_factory=list)
    last_finish: Optional[datetime] = None
    points_lost: int = 0
    vehicle_records: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "site_id": self.site_id,
            "date": self.date,
            "strategy": self.strategy,
            "missed_departures": self.missed_departures,
            "deficit_kwh": round(self.deficit_kwh, 2),
            "moves": self.moves,
            "peak_kw": round(self.peak_kw, 2),
            "total_kwh": round(self.total_kwh, 2),
            "delivered_per_vehicle": {k: round(v, 2) for k, v in self.delivered.items()},
            "final_soc_per_vehicle": {k: round(v, 4) for k, v in self.final_soc.items()},
            "undercharged_vehicles": self.undercharged,
            "never_charged": self.never_charged,
            "last_finish_ts": self.last_finish.isoformat() if self.last_finish else None,
            "points_lost": self.points_lost,
            "vehicle_records": self.vehicle_records,
        }


def taper_limit(job: Job, soc: float) -> float:
    """
    Computes the maximum acceptance power under battery CV tapering.
    Beyond 80% SoC, internal resistance ramps and acceptance power drops nonlinearly.
    """
    if soc <= SOC_TAPER_START:
        return job.max_kw
    x = min((soc - SOC_TAPER_START) / (1.0 - SOC_TAPER_START), 1.0)
    return job.max_kw * max(1.0 - TAPER_DEPTH, 1.0 - TAPER_DEPTH * (x ** TAPER_EXP))


def waterfill_allocate(
    items: List[Job],
    cap_kw: float,
    weight_fn,
    limit_fn,
) -> Dict[str, float]:
    """
    Waterfilling algorithm for continuous power allocation.
    Vehicles hitting their physical limit (taper limit or gun limit) are clamped,
    and leftover headroom is reallocated to unclamped vehicles proportional to weight.
    """
    alloc: Dict[str, float] = {j.vehicle_id: 0.0 for j in items}
    pool = cap_kw
    pending = list(items)

    while pending and pool > 1e-9:
        total_w = sum(weight_fn(j) for j in pending)
        if total_w <= 1e-9:
            break
        scale = pool / total_w
        capped = []
        for j in pending:
            limit = limit_fn(j)
            if weight_fn(j) * scale >= limit - 1e-9:
                capped.append((j, limit))
        if not capped:
            for j in pending:
                alloc[j.vehicle_id] = weight_fn(j) * scale
            return alloc
        for j, lim in capped:
            alloc[j.vehicle_id] = lim
            pool -= lim
            pending.remove(j)

    return alloc


def load_fleet_jobs(
    site_id: str,
    date: str,
    night_only: bool = False,
    depart_date: Optional[str] = None,
) -> List[Job]:
    """
    Loads vehicle charging jobs from official fleet_schedule.csv and vehicles.csv.
    Handles variable timetable windows and missing departure timestamps gracefully.
    """
    vehicles_path = resolve_csv_path("vehicles.csv")
    vehicles_spec: Dict[str, Dict[str, str]] = {}
    with open(vehicles_path, mode="r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            vehicles_spec[row["vehicle_id"].strip()] = row

    schedule_path = resolve_csv_path("fleet_schedule.csv")
    jobs: List[Job] = []

    with open(schedule_path, mode="r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["site_id"].strip() != site_id:
                continue
            arr_str = row["arrive_ts"].strip()
            dep_str = row.get("depart_ts", "").strip()

            if night_only and depart_date:
                if not dep_str.startswith(depart_date):
                    continue
                arr = datetime.fromisoformat(arr_str)
            else:
                if not arr_str.startswith(date):
                    continue
                arr = datetime.fromisoformat(arr_str)
                if night_only and arr.hour < 19:
                    continue

            if dep_str:
                dep = datetime.fromisoformat(dep_str)
            else:
                # Default dwell: next day 06:00
                dep = arr.replace(hour=6, minute=0, second=0) + timedelta(days=1)

            vid = row["vehicle_id"].strip()
            spec = vehicles_spec.get(vid, {})
            battery_kwh = float(spec.get("battery_kwh", 400.0))
            max_kw = float(spec.get("max_charge_kw", 150.0))
            soc_in = float(row.get("arrive_soc_pct", 20.0)) / 100.0
            soc_req = float(row.get("required_soc_pct", 85.0)) / 100.0

            jobs.append(Job(
                vehicle_id=vid,
                arrive=arr,
                depart=dep,
                battery_kwh=battery_kwh,
                soc_in=soc_in,
                soc_req=soc_req,
                max_kw=max_kw,
            ))

    jobs.sort(key=lambda j: j.arrive)
    return jobs


def run_discrete_event_simulation(
    jobs: List[Job],
    site_id: str,
    date: str,
    cabinet_kw: List[float],
    points_per_cabinet: Any = 4,
    strategy: str = "urgency",
    step_min: float = 1.0,
    fault: Optional[Tuple[datetime, List[int]]] = None,
    cross_tie: bool = True,
    move_delay_min: float = 0.0,
    gun_kw: float = 150.0,
    grid_limit_kw: Optional[float] = None,
    grid_curtailment: Optional[List[Tuple[datetime, datetime, float]]] = None,
    point_gun_kw: Optional[List[float]] = None,
) -> SimulationResult:
    """
    Executes a minute-by-minute discrete event charging simulation.

    Parameters:
        grid_limit_kw: Site-level grid import limit (kW). If None, no site-level cap.
        grid_curtailment: List of (start, end, limit_kw) DSO curtailment windows that
            temporarily override grid_limit_kw during those periods.
        point_gun_kw: Per-point gun kW overrides. Length must match total points.
            If None, all points use `gun_kw`.
    """
    if not jobs:
        return SimulationResult(site_id=site_id, date=date, strategy=strategy)

    cabinets = [Cabinet(i, kw) for i, kw in enumerate(cabinet_kw)]
    # Support variable points per cabinet: int -> uniform, list -> per-cabinet
    if isinstance(points_per_cabinet, int):
        ppc = [points_per_cabinet] * len(cabinets)
    else:
        ppc = list(points_per_cabinet)
    points: List[Point] = []
    for ci, c in enumerate(cabinets):
        for _ in range(ppc[ci]):
            points.append(Point(idx=len(points), cabinet=c.idx))

    # Build per-point gun limit lookup
    _point_gun_kw: List[float] = list(point_gun_kw) if point_gun_kw else [gun_kw] * len(points)

    delivered = {j.vehicle_id: 0.0 for j in jobs}
    soc = {j.vehicle_id: j.soc_in for j in jobs}
    waiting: List[Job] = []
    seen: set = set()
    stranded: set = set()
    moves = 0
    peak = 0.0
    fault_fired = False
    points_lost = 0
    finish_at: Dict[str, datetime] = {}

    t = min(j.arrive for j in jobs)
    end = max(j.depart for j in jobs)
    dt = timedelta(minutes=step_min)

    def finished(j: Job) -> bool:
        return soc[j.vehicle_id] >= j.soc_req - 1e-9

    def alive_cap() -> float:
        return sum(c.kw for c in cabinets if c.alive)

    def effective_grid_limit(now: datetime) -> float:
        """Returns the effective site-level grid import limit at time `now`."""
        base = grid_limit_kw if grid_limit_kw is not None else float("inf")
        if grid_curtailment:
            for curt_start, curt_end, curt_kw in grid_curtailment:
                if curt_start <= now < curt_end:
                    base = min(base, curt_kw)
        return base

    while t <= end:
        # Step 1: Cabinet Fault Injection
        if fault and not fault_fired and t >= fault[0]:
            fault_fired = True
            dead = set(fault[1])
            for c in cabinets:
                if c.idx in dead:
                    c.alive = False
            for p in points:
                if p.cabinet in dead:
                    if not cross_tie:
                        p.alive = False
                        points_lost += 1
                    if p.job is not None:
                        if not finished(p.job):
                            if cross_tie:
                                waiting.append(p.job)
                            else:
                                stranded.add(p.job.vehicle_id)
                        p.job = None
            waiting.sort(key=lambda x: x.arrive)

        live = [p for p in points if p.alive]
        cap_now = alive_cap()

        # Step 2: Arrival & Plug-In
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

        # Step 3: Departure / Release Finished Vehicles
        for p in live:
            if p.job is not None and (finished(p.job) or t >= p.job.depart):
                p.job = None

        # Step 4: Queue Servicing
        for p in live:
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

        # Step 5: Power Allocation & Energy Integration
        active = [
            (p, p.job) for p in live
            if p.job is not None and not finished(p.job)
            and (p.ready_at is None or t >= p.ready_at)
        ]

        if strategy == "fcfs":
            draw = 0.0
            plan = []
            eff_limit = effective_grid_limit(t)
            for p, j in active:
                cab = cabinets[p.cabinet]
                if not cab.alive:
                    continue
                per_point = cab.kw / ppc[p.cabinet]
                limit = min(per_point, taper_limit(j, soc[j.vehicle_id]), _point_gun_kw[p.idx])
                plan.append((j, limit))
            # If total exceeds grid limit, scale down proportionally
            total_request = sum(lim for _, lim in plan)
            if total_request > eff_limit and total_request > 1e-9:
                scale = eff_limit / total_request
                plan = [(j, lim * scale) for j, lim in plan]
            draw = sum(lim for _, lim in plan)
            peak = max(peak, draw)

            for j, limit in plan:
                room = j.need_kwh - delivered[j.vehicle_id]
                add = max(0.0, min(limit * step_min / 60.0, room))
                delivered[j.vehicle_id] += add
                soc[j.vehicle_id] = min(
                    j.soc_req, j.soc_in + delivered[j.vehicle_id] / j.battery_kwh
                )
                if finished(j) and j.vehicle_id not in finish_at:
                    finish_at[j.vehicle_id] = t
        elif active:
            def w_fn(j: Job) -> float:
                remain_h = max((j.depart - t).total_seconds() / 3600.0, 0.05)
                return (j.need_kwh - delivered[j.vehicle_id]) / remain_h

            def l_fn(j: Job) -> float:
                # Find the point this job is on to get per-point gun limit
                pgun = gun_kw
                for pp, jj in active:
                    if jj.vehicle_id == j.vehicle_id:
                        pgun = _point_gun_kw[pp.idx]
                        break
                return min(taper_limit(j, soc[j.vehicle_id]), j.max_kw, pgun)

            eff_limit = effective_grid_limit(t)

            if cross_tie:
                groups = {None: [j for _, j in active]}
            else:
                groups = {}
                for p, j in active:
                    groups.setdefault(p.cabinet, []).append(j)

            total_alloc = 0.0
            all_allocs: Dict[str, float] = {}
            for cab_idx, group in groups.items():
                cap = cap_now if cab_idx is None else cabinets[cab_idx].kw
                alloc = waterfill_allocate(group, cap, w_fn, l_fn)
                total_alloc += sum(alloc.values())
                all_allocs.update(alloc)

            # Enforce site-level grid limit
            if total_alloc > eff_limit and total_alloc > 1e-9:
                scale = eff_limit / total_alloc
                all_allocs = {vid: kw * scale for vid, kw in all_allocs.items()}
                total_alloc = eff_limit

            for _, j in active:
                room = j.need_kwh - delivered[j.vehicle_id]
                add = max(0.0, min(all_allocs.get(j.vehicle_id, 0.0) * step_min / 60.0, room))
                delivered[j.vehicle_id] += add
                soc[j.vehicle_id] = min(
                    j.soc_req, j.soc_in + delivered[j.vehicle_id] / j.battery_kwh
                )
                if finished(j) and j.vehicle_id not in finish_at:
                    finish_at[j.vehicle_id] = t
            peak = max(peak, total_alloc)

        t += dt

    under = [
        (j.vehicle_id, round(j.need_kwh - delivered[j.vehicle_id], 1))
        for j in jobs
        if delivered[j.vehicle_id] < j.need_kwh - 1.0
    ]
    never = [j.vehicle_id for j in jobs if delivered[j.vehicle_id] < 1.0]
    total_deficit = round(sum(d for _, d in under), 1)

    vehicle_records = [
        {
            "vehicle_id": j.vehicle_id,
            "arrive_ts": j.arrive.isoformat(),
            "depart_ts": j.depart.isoformat(),
            "soc_initial": round(j.soc_in, 4),
            "soc_required": round(j.soc_req, 4),
            "soc_final": round(soc[j.vehicle_id], 4),
            "need_kwh": round(j.need_kwh, 2),
            "delivered_kwh": round(delivered[j.vehicle_id], 2),
            "satisfied": (soc[j.vehicle_id] >= j.soc_req - 1e-4),
        }
        for j in jobs
    ]

    return SimulationResult(
        site_id=site_id,
        date=date,
        strategy=strategy,
        delivered=delivered,
        final_soc=soc,
        moves=moves,
        undercharged=under,
        missed_departures=len(under),
        deficit_kwh=total_deficit,
        peak_kw=round(peak, 1),
        total_kwh=round(sum(delivered.values()), 1),
        never_charged=never,
        last_finish=max(finish_at.values()) if finish_at else None,
        points_lost=points_lost,
        vehicle_records=vehicle_records,
    )


def simulate_closed_loop_minute_by_minute(
    site_id: str,
    date: str = "2026-11-13",
    strategy: str = "urgency",
    cross_tie: bool = False,
) -> Dict[str, Any]:
    """
    Standard interface contract: executes dynamic closed-loop minute-by-minute
    simulation for any station on Scenario Day, replacing hardcoded literals.
    """
    if site_id == "S1":
        # S1 Bus Depot: 3x360 kW cabinets, 12 connection points
        # chargers.csv: D1-1..D1-12, one CCS2 each, 150 kW, 1:1 bound to one cabinet.
        # Strict 1:N intra-cabinet wiring => no cross-cabinet tie (no busbar between cabinets).
        jobs = load_fleet_jobs("S1", "2026-11-13", night_only=True, depart_date="2026-11-13")
        fault_ts = datetime.fromisoformat("2026-11-13T02:25:00+02:00")
        res = run_discrete_event_simulation(
            jobs=jobs,
            site_id="S1",
            date=date,
            cabinet_kw=[360.0, 360.0, 360.0],
            points_per_cabinet=4,  # 3 * 4 = 12 points == 12 CCS2 guns
            strategy=strategy,
            fault=(fault_ts, [2]),  # C1-3 trips at 02:25
            cross_tie=False,
            gun_kw=150.0,
        )
        return res.to_dict()

    elif site_id == "S2":
        # S2 Logistics Depot: 2x400 kW cabinets = 800 kW, 8 points
        # Afternoon peak trucks arriving 14:20-14:45
        # DSO curtailment G1: 16:00-19:00 limit_cap = 400 kW (grid_events.csv)
        schedule_path = resolve_csv_path("fleet_schedule.csv")
        vehicles_path = resolve_csv_path("vehicles.csv")
        vehicles_spec: Dict[str, Dict[str, str]] = {}
        with open(vehicles_path, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                vehicles_spec[row["vehicle_id"].strip()] = row

        jobs = []
        with open(schedule_path, mode="r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row["site_id"].strip() == "S2" and row["arrive_ts"].strip().startswith("2026-11-13T14:"):
                    arr = datetime.fromisoformat(row["arrive_ts"].strip())
                    dep = datetime.fromisoformat(row["depart_ts"].strip())
                    vid = row["vehicle_id"].strip()
                    sp = vehicles_spec.get(vid, {})
                    jobs.append(Job(
                        vehicle_id=vid,
                        arrive=arr,
                        depart=dep,
                        battery_kwh=float(sp.get("battery_kwh", 540.0)),
                        soc_in=float(row.get("arrive_soc_pct", 10.0)) / 100.0,
                        soc_req=float(row.get("required_soc_pct", 70.0)) / 100.0,
                        max_kw=float(sp.get("max_charge_kw", 350.0)),
                    ))

        curtailment = [
            (
                datetime.fromisoformat("2026-11-13T16:00:00+02:00"),
                datetime.fromisoformat("2026-11-13T19:00:00+02:00"),
                400.0,
            )
        ]
        res = run_discrete_event_simulation(
            jobs=jobs,
            site_id="S2",
            date=date,
            cabinet_kw=[400.0, 400.0],
            points_per_cabinet=4,
            strategy=strategy,
            cross_tie=cross_tie,
            gun_kw=300.0,
            grid_limit_kw=800.0,
            grid_curtailment=curtailment,
        )
        return res.to_dict()

    elif site_id == "S5":
        # S5 Bus Depot: 2x450 kW cabinets = 900 kW, 8 points
        # 12 overnight buses arriving Nov 12 and departing Nov 13 morning
        jobs = load_fleet_jobs("S5", "2026-11-13", night_only=True, depart_date="2026-11-13")
        if not jobs:
            jobs = load_fleet_jobs("S5", date, night_only=True)

        if strategy == "fcfs":
            # Baseline unreconciled configuration (site_config.csv row 164 & 191-196):
            # grid_limit_kw = 600 kW, D5-7 throttled to 50 kW, D5-8 inactive (0 kW)
            point_guns = [150.0, 150.0, 150.0, 150.0, 150.0, 150.0, 50.0, 0.0]
            grid_limit = 600.0
        else:
            # Reconciled 3-way commissioning configuration:
            # grid_limit_kw = 900 kW, all 8 dispensers fully commissioned at 150 kW
            point_guns = [150.0] * 8
            grid_limit = 900.0

        res = run_discrete_event_simulation(
            jobs=jobs,
            site_id="S5",
            date=date,
            cabinet_kw=[450.0, 450.0],
            points_per_cabinet=4,
            strategy=strategy,
            cross_tie=cross_tie,
            gun_kw=150.0,
            grid_limit_kw=grid_limit,
            point_gun_kw=point_guns,
        )
        return res.to_dict()

    else:
        # Generic fallback
        jobs = load_fleet_jobs(site_id, date)
        res = run_discrete_event_simulation(
            jobs=jobs,
            site_id=site_id,
            date=date,
            cabinet_kw=[360.0, 360.0],
            points_per_cabinet=4,
            strategy=strategy,
            cross_tie=cross_tie,
        )
        return res.to_dict()
