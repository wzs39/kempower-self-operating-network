"""
充电场站夜间功率分配与挪车次数核算。

一个可复现的离散时间仿真：给定车辆时间窗、补能需求、连接点数量与整流容量，
算出能否按时充满、需要多少次物理换位、故障发生时谁会被牺牲。

三个必须建模对的物理事实，缺了数字就不真实：
  1. 恒压段衰减（CV taper）—— SoC 超过 80% 后车端受电功率骤降，
     这是充电后段"越充越慢"的根本原因。
  2. 机柜故障是"掉枪"而不是"全体降速"—— C1-3 停机等于挂在它上面的
     4 个连接点直接失电，上面的车当场断充。
  3. 换位要时间 —— 一次 move_and_replug 是 8 分钟，这期间枪位空转。

两种调度策略：
  fcfs    —— 现状。先到先充，枪满了排队，枪一空就要人挪车。
  urgency —— 零人化。所有车到场即插，按「剩余电量 / 剩余时间」分功率，
             等价于 EDF（最早截止期优先）的连续功率版本。

所有输入来自 data/*.csv，不硬编码任何结果。
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

SOC_TAPER_START = 0.80
TAPER_EXP = 1.2
TAPER_DEPTH = 0.9


@dataclass
class Job:
    """一辆车的夜间充电任务。"""

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
    """一个连接点（枪）。"""

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
    """恒压段功率衰减：SoC 超过 80% 后，车端能接受的功率按曲线下降。"""
    if soc <= SOC_TAPER_START:
        return job.max_kw
    x = min((soc - SOC_TAPER_START) / (1.0 - SOC_TAPER_START), 1.0)
    return job.max_kw * max(1.0 - TAPER_DEPTH, 1.0 - TAPER_DEPTH * x ** TAPER_EXP)


def cap_profile(events: list[tuple[datetime, float]]):
    """把「某时刻容量变成多少」的事件表，变成一个 t -> cap_kw 的函数。"""
    ordered = sorted(events)

    def f(t: datetime) -> float:
        cur = ordered[0][1]
        for ts, cap in ordered:
            if t >= ts:
                cur = cap
        return cur

    return f


def load_jobs(site_id: str = "S1", day: str = "2026-11-12", night_only: bool = True) -> list[Job]:
    """从赛题数据读出场站的充电任务。"""
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
    """跑一遍夜间充电。

    strategy      : "fcfs" 先到先充 + 排队挪车；"urgency" 全部插上按紧迫度分功率
    cap_fn        : t -> 可用容量 kW
    fault         : (时刻, 掉枪数)，模拟机柜停机导致若干连接点失电
    move_delay_min: 一次换位要多久才能重新送电（取自 operations_log 的 8 分钟）
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
        # ---- 1) 故障注入：掉枪，挂在上面的车当场断充 ----
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

        # ---- 2) 到场：有活着的空点就插上 ----
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

        # ---- 3) 释放充饱或到点的车 ----
        for p in live:
            if p.job is not None and (finished(p.job) or t >= p.job.depart):
                p.job = None

        # ---- 4) 空位补给排队最久的车 ----
        for p in live:
            if p.job is None and waiting:
                waiting.sort(key=lambda x: x.arrive)
                nxt = waiting.pop(0)
                if nxt.depart > t:
                    p.job = nxt
                    if strategy == "fcfs":
                        p.ready_at = t + timedelta(minutes=move_delay_min)
                        moves += 1          # 人工开车过去 + 插枪
                    else:
                        p.ready_at = t      # 矩阵直接改道，无需人

        # ---- 5) 充电 ----
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

            # 注水式分配：被恒压段或车端上限卡住的车拿走它能吃的部分，
            # 剩余功率再按权重分给没被卡住的车，直到分完或全部封顶。
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
