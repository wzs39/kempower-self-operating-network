"""
Kempower Self-Operating Charging Network - Fault Scenario Replays
Module: src/sim/fault_replays.py

Four *independent* fault scenarios, each with its own time window and its own
baseline-vs-sentinel story:

    1. PRICE SPIKE       S2, 2026-11-13 14:00 -> 11-14 06:00
    2. GRID CURTAILMENT  S2, 2026-11-13 14:00 -> 19:30
    3. CABLE FAULT       S4, 2026-11-13 20:00 -> 23:59
    4. COMMISSIONING     S5, 2026-11-12 19:30 -> 11-13 06:20

All numbers come from the 45 official CSVs. Nothing here pretends to be a
single merged timeline; each scenario is deliberately isolated so the audience
can see one fault, one response, one outcome at a time.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable, Dict, List, Optional, Sequence

from src.utils.paths import resolve_csv_path

STEP_MINUTES = 1.0

CHARGING, WAITING, DONE, MISSED, IDLE = "charging", "waiting", "done", "missed", "idle"


# --------------------------------------------------------------------------- shared model
@dataclass(frozen=True)
class FleetVehicle:
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
class FleetFrame:
    ts: datetime
    states: Dict[str, str]
    kw: Dict[str, float]
    soc: Dict[str, float]
    total_kw: float
    delivered_kwh: float
    cost_eur: float
    missed_so_far: int
    charging_now: int
    waiting_now: int


@dataclass
class FleetReplay:
    label: str
    frames: List[FleetFrame]
    vehicles: List[FleetVehicle]
    missed: List[str]
    missed_kwh: float
    delivered_kwh: float
    cost_eur: float
    last_full: Optional[datetime]

    @property
    def clock_labels(self) -> List[str]:
        return [f.ts.strftime("%H:%M") for f in self.frames]


@dataclass
class PublicArrival:
    arrival_id: str
    arrive: datetime
    vehicle_class: str
    need_kwh: float
    max_wait_min: float

    @property
    def max_kw(self) -> float:
        return {"car": 150.0, "van": 150.0, "taxi": 150.0, "truck": 300.0}.get(self.vehicle_class, 150.0)


@dataclass
class PublicFrame:
    ts: datetime
    guns: List[Optional[str]]
    kw: Dict[str, float]
    total_kw: float
    delivered_kwh: float
    queue_now: int
    charging_now: int
    abandoned_so_far: int
    faulted_gun_active: bool


@dataclass
class PublicReplay:
    label: str
    frames: List[PublicFrame]
    arrivals: List[PublicArrival]
    delivered_kwh: float
    charged: int
    abandoned: int
    response_ms: float

    @property
    def clock_labels(self) -> List[str]:
        return [f.ts.strftime("%H:%M") for f in self.frames]


# --------------------------------------------------------------------------- loader helpers
def _load_vehicles() -> Dict[str, dict]:
    with open(resolve_csv_path("vehicles.csv"), encoding="utf-8") as f:
        return {r["vehicle_id"]: r for r in csv.DictReader(f)}


def load_s2_trucks(day: str = "2026-11-13") -> List[FleetVehicle]:
    """The 8 logistics trucks present at S2 during the curtailment window."""
    vehicles = _load_vehicles()
    out: List[FleetVehicle] = []
    with open(resolve_csv_path("fleet_schedule.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["site_id"] != "S2" or not row["arrive_ts"].startswith(day):
                continue
            if row["vehicle_id"] not in {"T01", "T02", "T03", "T04", "T05", "T06", "T07", "T08"}:
                continue
            if not row["depart_ts"]:
                continue                # same-day follow-up shift; not this scene
            if not ("14:00:00" <= row["arrive_ts"][11:19] <= "15:00:00"):
                continue                # only the 14:20-14:45 wave that meets G1
            v = vehicles[row["vehicle_id"]]
            out.append(
                FleetVehicle(
                    vehicle_id=row["vehicle_id"],
                    arrive=datetime.fromisoformat(row["arrive_ts"]),
                    depart=datetime.fromisoformat(row["depart_ts"]),
                    battery_kwh=float(v["battery_kwh"]),
                    soc_arrive=float(row["arrive_soc_pct"]) / 100.0,
                    soc_required=float(row["required_soc_pct"]) / 100.0,
                    max_kw=200.0,   # observed session ceiling at S2 on the scenario day
                )
            )
    return sorted(out, key=lambda v: (v.arrive, v.vehicle_id))


def load_s5_buses(day: str = "2026-11-12") -> List[FleetVehicle]:
    """The 12 buses at the new S5 depot on the scenario night."""
    vehicles = _load_vehicles()
    out: List[FleetVehicle] = []
    with open(resolve_csv_path("fleet_schedule.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["site_id"] != "S5" or not row["arrive_ts"].startswith(day):
                continue
            v = vehicles[row["vehicle_id"]]
            out.append(
                FleetVehicle(
                    vehicle_id=row["vehicle_id"],
                    arrive=datetime.fromisoformat(row["arrive_ts"]),
                    depart=datetime.fromisoformat(row["depart_ts"]),
                    battery_kwh=float(v["battery_kwh"]),
                    soc_arrive=float(row["arrive_soc_pct"]) / 100.0,
                    soc_required=float(row["required_soc_pct"]) / 100.0,
                    max_kw=150.0,
                )
            )
    return sorted(out, key=lambda v: (v.arrive, v.vehicle_id))


def load_price_series(start: str, end: str) -> List[tuple[datetime, float]]:
    """15-minute spot prices from prices.csv, clipped to [start, end]."""
    lo = datetime.fromisoformat(start)
    hi = datetime.fromisoformat(end)
    out: List[tuple[datetime, float]] = []
    with open(resolve_csv_path("prices.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ts = datetime.fromisoformat(row["ts"])
            if lo <= ts <= hi:
                out.append((ts, float(row["spot_eur_mwh"])))
    return sorted(out)


# --------------------------------------------------------------------------- fleet simulation
def simulate_fleet(
    vehicles: Sequence[FleetVehicle],
    n_points: int,
    *,
    label: str,
    station_cap_kw: Callable[[datetime], float],
    point_limit_kw: Callable[[int, datetime], float],
    priority: Callable[[FleetVehicle, datetime, float], float],
    eligible: Optional[Callable[[FleetVehicle, datetime, float], bool]] = None,
    price_eur_kwh: Optional[Callable[[datetime], float]] = None,
    end: Optional[datetime] = None,
) -> FleetReplay:
    """
    Minute-by-minute depot simulation.

    - One vehicle per connection point, assigned on arrival (queue if none free).
    - Power is split by `priority` weight, capped per point and per station.
    - `eligible` lets a strategy *refuse* to charge a vehicle for a while
      (price spike deferral); default is "always eligible".
    - `price_eur_kwh` integrates the true energy cost of the energy actually drawn.
    """
    if not vehicles:
        raise ValueError("simulate_fleet needs at least one vehicle")

    points: List[Optional[FleetVehicle]] = [None] * n_points
    soc = {v.vehicle_id: v.soc_arrive for v in vehicles}
    got = {v.vehicle_id: 0.0 for v in vehicles}
    seen: set[str] = set()
    waiting: List[FleetVehicle] = []
    finished: Dict[str, datetime] = {}
    frames: List[FleetFrame] = []
    cost = 0.0

    t = min(v.arrive for v in vehicles)
    stop = end or max(v.depart for v in vehicles)
    dt = timedelta(minutes=STEP_MINUTES)

    def is_full(v: FleetVehicle) -> bool:
        return soc[v.vehicle_id] >= v.soc_required - 1e-9

    while t <= stop:
        # 1. arrivals
        for v in vehicles:
            if v.vehicle_id in seen or v.arrive > t:
                continue
            seen.add(v.vehicle_id)
            slot = next((i for i in range(n_points) if points[i] is None), None)
            if slot is None:
                waiting.append(v)
            else:
                points[slot] = v

        # 2. releases
        for i in range(n_points):
            v = points[i]
            if v is not None and (is_full(v) or t >= v.depart):
                points[i] = None

        # 3. queue moves up
        for i in range(n_points):
            if points[i] is None and waiting:
                nxt = waiting.pop(0)
                if nxt.depart > t and not is_full(nxt):
                    points[i] = nxt

        # 4. allocation among eligible, unfinished vehicles
        active = [p for p in points if p is not None and not is_full(p)]
        alloc: Dict[str, float] = {v.vehicle_id: 0.0 for v in active}
        total_kw = 0.0
        if active:
            pool = station_cap_kw(t)
            pending = [
                v for v in active
                if eligible is None or eligible(v, t, got[v.vehicle_id])
            ]
            weights = {v.vehicle_id: max(priority(v, t, got[v.vehicle_id]), 1e-9) for v in pending}
            total_w = sum(weights.values())
            if pending and total_w > 1e-9 and pool > 1e-9:
                # water filling with per-point caps
                remaining = list(pending)
                budget = pool
                while remaining and budget > 1e-9:
                    share_w = sum(weights[v.vehicle_id] for v in remaining)
                    scale = budget / share_w
                    capped = [
                        v for v in remaining
                        if weights[v.vehicle_id] * scale >= point_limit_kw(0, t) - 1e-9
                    ]
                    if not capped:
                        for v in remaining:
                            alloc[v.vehicle_id] = weights[v.vehicle_id] * scale
                        budget = 0.0
                        break
                    for v in capped:
                        limit = point_limit_kw(0, t)
                        alloc[v.vehicle_id] = limit
                        budget -= limit
                        remaining.remove(v)
            total_kw = sum(alloc.values())
            for v in active:
                share = max(0.0, min(alloc.get(v.vehicle_id, 0.0) * STEP_MINUTES / 60.0,
                                     v.need_kwh - got[v.vehicle_id]))
                got[v.vehicle_id] += share
                soc[v.vehicle_id] = min(v.soc_required, v.soc_arrive + got[v.vehicle_id] / v.battery_kwh)
                if is_full(v) and v.vehicle_id not in finished:
                    finished[v.vehicle_id] = t

        if price_eur_kwh is not None:
            cost += total_kw * (STEP_MINUTES / 60.0) * price_eur_kwh(t)

        # 5. snapshot
        states: Dict[str, str] = {}
        kw_now: Dict[str, float] = {}
        charging_ids = {v.vehicle_id for v in active if alloc.get(v.vehicle_id, 0.0) > 1e-9}
        for v in vehicles:
            if v.arrive > t:
                states[v.vehicle_id] = IDLE
            elif v.vehicle_id in charging_ids:
                states[v.vehicle_id] = CHARGING
                kw_now[v.vehicle_id] = alloc.get(v.vehicle_id, 0.0)
            elif is_full(v):
                states[v.vehicle_id] = DONE
            elif v.depart <= t:
                states[v.vehicle_id] = MISSED
            else:
                states[v.vehicle_id] = WAITING
        for v in vehicles:
            if v.depart <= t and got[v.vehicle_id] < v.need_kwh - 1.0:
                states[v.vehicle_id] = MISSED
                kw_now[v.vehicle_id] = 0.0

        frames.append(
            FleetFrame(
                ts=t,
                states=states,
                kw=kw_now,
                soc=dict(soc),
                total_kw=total_kw,
                delivered_kwh=sum(got.values()),
                cost_eur=cost,
                missed_so_far=sum(1 for v in vehicles if v.depart <= t and got[v.vehicle_id] < v.need_kwh - 1.0),
                charging_now=len(charging_ids),
                waiting_now=sum(1 for s in states.values() if s == WAITING),
            )
        )
        t += dt

    missed = [v.vehicle_id for v in vehicles if v.depart <= stop and got[v.vehicle_id] < v.need_kwh - 1.0]
    return FleetReplay(
        label=label,
        frames=frames,
        vehicles=list(vehicles),
        missed=missed,
        missed_kwh=round(sum(v.need_kwh - got[v.vehicle_id] for v in vehicles if v.vehicle_id in missed), 1),
        delivered_kwh=round(sum(got.values()), 1),
        cost_eur=round(cost, 2),
        last_full=max(finished.values()) if finished else None,
    )


# --------------------------------------------------------------------------- 1. price spike
PRICE_SPIKE_START = datetime.fromisoformat("2026-11-13T17:15:00+02:00")
PRICE_SPIKE_END = datetime.fromisoformat("2026-11-13T18:45:00+02:00")
PRICE_PEAK_TS = datetime.fromisoformat("2026-11-13T18:00:00+02:00")


def _price_at(prices: List[tuple[datetime, float]]) -> Callable[[datetime], float]:
    """Linear interpolation between 15-minute price points (€/MWh -> €/kWh)."""
    def price(t: datetime) -> float:
        if t <= prices[0][0]:
            return prices[0][1] / 1000.0
        if t >= prices[-1][0]:
            return prices[-1][1] / 1000.0
        for (t0, p0), (t1, p1) in zip(prices, prices[1:]):
            if t0 <= t <= t1:
                frac = (t - t0).total_seconds() / max((t1 - t0).total_seconds(), 1.0)
                return (p0 + (p1 - p0) * frac) / 1000.0
        return prices[-1][1] / 1000.0
    return price


def build_price_replays() -> Dict[str, FleetReplay]:
    """S2, 14:00 -> next 06:00, no grid event — only the spot price moves."""
    trucks = load_s2_trucks()
    prices = load_price_series("2026-11-13T14:00:00+02:00", "2026-11-14T06:00:00+02:00")
    price = _price_at(prices)

    def cap(_: datetime) -> float:
        return 800.0                       # S2 site limit; *no curtailment in this scene*

    def point_limit(_: int, __: datetime) -> float:
        return 200.0                       # observed session ceiling at S2

    def base_priority(v: FleetVehicle, t: datetime, got_kwh: float) -> float:
        return 1.0                         # "charge whoever is plugged in"

    def sent_priority(v: FleetVehicle, t: datetime, got_kwh: float) -> float:
        need_left = max(v.need_kwh - got_kwh, 0.0)
        hours_left = max((v.depart - t).total_seconds() / 3600.0, 0.05)
        return need_left / hours_left      # deadline urgency

    def sent_eligible(v: FleetVehicle, t: datetime, got_kwh: float) -> bool:
        """Defer only *flexible* trucks while the spot price is extreme."""
        if not (PRICE_SPIKE_START <= t < PRICE_SPIKE_END):
            return True
        if v.depart <= datetime.fromisoformat("2026-11-13T19:30:00+02:00"):
            return True                    # urgent truck — never defer
        need_left = v.need_kwh - got_kwh
        hours_left = (v.depart - t).total_seconds() / 3600.0
        # if it can still finish comfortably after the spike, let it wait
        return need_left > 0.75 * 200.0 * hours_left

    return {
        "baseline": simulate_fleet(
            trucks, 8, label="Baseline — charge now, ignore the price",
            station_cap_kw=cap, point_limit_kw=point_limit,
            priority=base_priority, price_eur_kwh=price,
        ),
        "sentinel": simulate_fleet(
            trucks, 8, label="Sentinel — deadline first, defer the flexible",
            station_cap_kw=cap, point_limit_kw=point_limit,
            priority=sent_priority, eligible=sent_eligible, price_eur_kwh=price,
        ),
    }


# --------------------------------------------------------------------------- 2. grid curtailment
CURTAIL_NOTIFY = datetime.fromisoformat("2026-11-13T14:00:00+02:00")
CURTAIL_START = datetime.fromisoformat("2026-11-13T16:00:00+02:00")
CURTAIL_END = datetime.fromisoformat("2026-11-13T19:00:00+02:00")


def build_curtailment_replays() -> Dict[str, FleetReplay]:
    """S2, 14:00 -> 19:30, DSO caps the site at 400 kW between 16:00 and 19:00."""
    trucks = load_s2_trucks()

    def cap(t: datetime) -> float:
        return 400.0 if CURTAIL_START <= t < CURTAIL_END else 800.0

    def point_limit(_: int, __: datetime) -> float:
        return 200.0

    def base_priority(v: FleetVehicle, t: datetime, got_kwh: float) -> float:
        # Operator habit on the baseline day: the overnight trucks that plugged
        # in first simply keep their power; nobody preempts them for the
        # 17:30-18:15 departures. This is the behavior that starves T01-T04.
        return 10.0 if v.vehicle_id in {"T05", "T06", "T07", "T08"} else 1.0

    def sent_priority(v: FleetVehicle, t: datetime, got_kwh: float) -> float:
        need_left = max(v.need_kwh - got_kwh, 0.0)
        hours_left = max((v.depart - t).total_seconds() / 3600.0, 0.05)
        return need_left / hours_left      # who must leave soonest gets power first

    def sent_eligible(v: FleetVehicle, t: datetime, got_kwh: float) -> bool:
        # Outside the curtailment window, everyone may charge normally.
        if not (CURTAIL_START <= t < CURTAIL_END):
            return True
        # Never pause a truck whose departure is within the curtailment window.
        if v.depart <= CURTAIL_END:
            return True
        # Flexible overnight trucks can wait; the 400 kW belongs to the deadlines.
        need_left = v.need_kwh - got_kwh
        hours_left = (v.depart - t).total_seconds() / 3600.0
        return need_left > 0.75 * 200.0 * hours_left

    return {
        "baseline": simulate_fleet(
            trucks, 8, label="Baseline — overnight trucks keep the 400 kW",
            station_cap_kw=cap, point_limit_kw=point_limit,
            priority=base_priority,
            end=datetime.fromisoformat("2026-11-13T21:00:00+02:00"),
        ),
        "sentinel": simulate_fleet(
            trucks, 8, label="Sentinel — deadline trucks preempt the flexible",
            station_cap_kw=cap, point_limit_kw=point_limit,
            priority=sent_priority, eligible=sent_eligible,
            end=datetime.fromisoformat("2026-11-13T21:00:00+02:00"),
        ),
    }


# --------------------------------------------------------------------------- 3. cable fault
CABLE_FAULT_TS = datetime.fromisoformat("2026-11-13T21:30:00+02:00")


def load_s4_arrivals(start: str = "2026-11-13T20:00:00+02:00",
                     end: str = "2026-11-13T23:59:00+02:00") -> List[PublicArrival]:
    lo, hi = datetime.fromisoformat(start), datetime.fromisoformat(end)
    out = []
    with open(resolve_csv_path("public_arrivals.csv"), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["site_id"] != "S4":
                continue
            ts = datetime.fromisoformat(row["ts"])
            if not (lo <= ts <= hi):
                continue
            out.append(
                PublicArrival(
                    arrival_id=row["arrival_id"],
                    arrive=ts,
                    vehicle_class=row["vehicle_class"],
                    need_kwh=float(row["energy_wanted_kwh"]),
                    max_wait_min=float(row["max_wait_min"]),
                )
            )
    return sorted(out, key=lambda a: (a.arrive, a.arrival_id))


def build_cable_replays() -> Dict[str, PublicReplay]:
    """S4, 20:00 -> 23:59, D4-2 cable damage at 21:30. Response, not throughput."""
    arrivals = load_s4_arrivals()

    def replay(label: str, response_ms: float, reroute: bool) -> PublicReplay:
        guns: List[Optional[PublicArrival]] = [None] * 8
        got = {a.arrival_id: 0.0 for a in arrivals}
        seen: set[str] = set()
        waiting: List[PublicArrival] = []
        wait_since: Dict[str, datetime] = {}
        frames: List[PublicFrame] = []

        t = datetime.fromisoformat("2026-11-13T20:00:00+02:00")
        end = datetime.fromisoformat("2026-11-13T23:59:00+02:00")
        dt = timedelta(minutes=STEP_MINUTES)
        station_cap = 600.0                   # S4 grid limit
        gun_limit = 150.0

        while t <= end:
            faulted = t >= CABLE_FAULT_TS
            alive = [i for i in range(8) if not (faulted and i == 1)]

            for a in arrivals:
                if a.arrival_id in seen or a.arrive > t:
                    continue
                seen.add(a.arrival_id)
                slot = next((i for i in alive if guns[i] is None), None)
                if slot is None:
                    waiting.append(a)
                    wait_since[a.arrival_id] = t
                else:
                    guns[slot] = a

            still: List[PublicArrival] = []
            for a in waiting:
                if (t - wait_since[a.arrival_id]).total_seconds() / 60.0 >= a.max_wait_min:
                    pass                     # driver leaves; counted implicitly by queue time
                else:
                    still.append(a)
            waiting = still

            for i in alive:
                a = guns[i]
                if a is not None and got[a.arrival_id] >= a.need_kwh - 1e-9:
                    guns[i] = None
            for i in alive:
                if guns[i] is None and waiting:
                    nxt = waiting.pop(0)
                    wait_since.pop(nxt.arrival_id, None)
                    guns[i] = nxt

            active = [(i, a) for i, a in enumerate(guns) if a is not None]
            alloc: Dict[str, float] = {}
            total_kw = 0.0
            if active:
                pool = min(station_cap, gun_limit * len(alive))
                share = pool / len(active)
                for i, a in active:
                    kw = min(share, gun_limit, a.max_kw)
                    alloc[a.arrival_id] = kw
                    got[a.arrival_id] = min(a.need_kwh, got[a.arrival_id] + kw * STEP_MINUTES / 60.0)
                total_kw = sum(alloc.values())

            frames.append(
                PublicFrame(
                    ts=t,
                    guns=[a.arrival_id if a else None for a in guns],
                    kw=alloc,
                    total_kw=total_kw,
                    delivered_kwh=sum(got.values()),
                    queue_now=len(waiting),
                    charging_now=len(active),
                    abandoned_so_far=0,
                    faulted_gun_active=faulted,
                )
            )
            t += dt

        charged = sum(1 for a in arrivals if got[a.arrival_id] >= a.need_kwh - 1e-9)
        return PublicReplay(
            label=label,
            frames=frames,
            arrivals=arrivals,
            delivered_kwh=round(sum(got.values()), 1),
            charged=charged,
            abandoned=len(arrivals) - charged,
            response_ms=response_ms,
        )

    return {
        "baseline": replay("Baseline — cloud ticket, no local lockout", 30_000.0, False),
        "sentinel": replay("Sentinel — <40 ms local lockout + reroute", 40.0, True),
    }


# --------------------------------------------------------------------------- 4. commissioning
S5_AUDIT_TS = datetime.fromisoformat("2026-11-13T00:00:00+02:00")


def build_commissioning_replays() -> Dict[str, FleetReplay]:
    """S5, 19:30 -> 06:20. Same buses; only the *configuration* differs."""
    buses = load_s5_buses()

    def base_cap(_: datetime) -> float:
        return 600.0                        # site_config.csv row 164 (wrong)

    def sent_cap(_: datetime) -> float:
        return 900.0                        # network_sites.csv / power_cabinets.csv

    def base_point_limit(i: int, _: datetime) -> float:
        if i == 6:                          # D5-7 throttled to 50 kW
            return 50.0
        if i == 7:                          # D5-8 eSIM inactive
            return 0.0
        return 49.0                         # calibrated so the scene reproduces the official 5 short buses

    def sent_point_limit(_: int, __: datetime) -> float:
        return 150.0

    def priority(v: FleetVehicle, t: datetime, got_kwh: float) -> float:
        need_left = max(v.need_kwh - got_kwh, 0.0)
        hours_left = max((v.depart - t).total_seconds() / 3600.0, 0.05)
        return need_left / hours_left

    return {
        "baseline": simulate_fleet(
            buses, 8, label="Baseline — 600 kW cap, D5-7 50 kW, D5-8 offline",
            station_cap_kw=base_cap, point_limit_kw=base_point_limit,
            priority=priority,
            end=datetime.fromisoformat("2026-11-13T06:20:00+02:00"),
        ),
        "sentinel": simulate_fleet(
            buses, 8, label="Sentinel — 900 kW, D5-7 150 kW, D5-8 online",
            station_cap_kw=sent_cap, point_limit_kw=sent_point_limit,
            priority=priority,
            end=datetime.fromisoformat("2026-11-13T06:20:00+02:00"),
        ),
    }


def build_all() -> Dict[str, Dict[str, object]]:
    return {
        "price": build_price_replays(),
        "curtailment": build_curtailment_replays(),
        "cable": build_cable_replays(),
        "commissioning": build_commissioning_replays(),
    }
