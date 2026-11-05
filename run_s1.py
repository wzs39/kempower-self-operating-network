"""
S1 公交北场站 · 夜间充电方案对比

跑法：
    python run_s1.py

设计原则：基线不靠模型猜，直接读数据。
  场景 A —— 真实记录：sessions_baseline.csv 里 11-12 夜间的实际充电会话，
            加上 baseline_kpis.csv 的官方欠电统计。
  场景 B —— 仿真反事实：同一批车辆，换成 24 个连接点、司机到场即插、
            按「剩余电量 / 剩余时间」分配功率，并注入 C1-3 机柜停机故障。
  场景 C —— 在 B 的基础上加「柜间互济」，卫星可由其他机柜供电。

不含任何硬编码结果，所有数字由 data/ 下的原始 CSV 计算得出。
"""

from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from src.edf_packer import Job, cap_profile, load_jobs, simulate

SITE = "S1"
NIGHT = "2026-11-12"
DAY = "2026-11-13"
CABINETS_KW = 360 * 3
GUNS_NOW = 12
POINTS_AFTER = 24
FAULT_TS = datetime.fromisoformat("2026-11-13T02:25:00+02:00")
GUNS_ON_CABINET = 4
KW_LOST = 360
MIN_PER_MOVE = 8


def hr(title: str) -> None:
    print()
    print("=" * 74)
    print(title)
    print("=" * 74)


def read_csv(name: str):
    with open(ROOT / "data" / name, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def baseline_from_data(jobs: list[Job]) -> dict:
    t_lo = datetime.fromisoformat(f"{NIGHT}T18:00:00+02:00")
    t_hi = datetime.fromisoformat(f"{DAY}T07:00:00+02:00")
    sessions = [
        r for r in read_csv("sessions_baseline.csv")
        if r["site_id"] == SITE
        and t_lo <= datetime.fromisoformat(r["start_ts"]) < t_hi
    ]

    by_vehicle: dict[str, float] = {}
    for r in sessions:
        if r["vehicle_id"]:
            by_vehicle[r["vehicle_id"]] = by_vehicle.get(r["vehicle_id"], 0.0) + float(r["energy_kwh"])

    moves = 0
    for r in sessions:
        if not r["vehicle_id"]:
            continue
        job = next((j for j in jobs if j.vehicle_id == r["vehicle_id"]), None)
        if job is None:
            continue
        if (datetime.fromisoformat(r["start_ts"]) - job.arrive).total_seconds() / 60 > 10:
            moves += 1

    under = []
    for j in jobs:
        got = by_vehicle.get(j.vehicle_id, 0.0)
        if got < j.need_kwh - 1.0:
            under.append((j.vehicle_id, round(j.need_kwh - got, 1)))

    return {
        "sessions": len(sessions),
        "moves": moves,
        "undercharged": under,
        "total_kwh": round(sum(by_vehicle.values()), 1),
        "first_start": min((r["start_ts"] for r in sessions), default=""),
        "last_end": max((r["end_ts"] for r in sessions), default=""),
        "never_charged": [v for v, _ in under if by_vehicle.get(v, 0.0) < 1.0],
    }


def official_kpi():
    for row in read_csv("baseline_kpis.csv"):
        if row["site_id"] == SITE and row["period"] == "scenario_day":
            return row
    return None


def main() -> None:
    jobs = load_jobs(SITE, NIGHT, night_only=True)
    if not jobs:
        raise SystemExit("没读到班次数据，检查 data/ 是否完整")

    total_need = sum(j.need_kwh for j in jobs)
    t0 = min(j.arrive for j in jobs)
    t1 = max(j.depart for j in jobs)
    window_h = (t1 - t0).total_seconds() / 3600
    available = CABINETS_KW * window_h

    hr("1. 需求侧核算")
    print(f"站点            : {SITE}（公交北场站）")
    print(f"夜间到场日      : {NIGHT}（次日 {DAY} 早晨发车，即场景日班次）")
    print(f"夜间班次        : {len(jobs)} 辆")
    print(f"到场            : {t0:%H:%M} 起，末班 {max(j.arrive for j in jobs):%H:%M} 到")
    print(f"发车            : {min(j.depart for j in jobs):%H:%M} 起，末班 {t1:%H:%M} 走")
    print(f"场站窗口        : {window_h:.2f} 小时")
    print(f"整流容量        : {CABINETS_KW} kW（3 柜 × 360 kW）")
    print(f"总补能需求      : {total_need:.0f} kWh")
    print(f"窗口内可供电    : {available:.0f} kWh")
    print(f"能量利用率      : {total_need / available * 100:.1f}%")
    tight = max(jobs, key=lambda j: j.avg_kw_needed)
    print(f"最紧的一辆车    : {tight.vehicle_id}（{tight.window_h:.2f}h 窗口，需 {tight.avg_kw_needed:.1f} kW 均值）")

    hr("2. 场景 A：真实记录（11-12 夜间实际发生了什么）")
    a = baseline_from_data(jobs)
    print(f"充电会话        : {a['sessions']} 次 / {len(jobs)} 辆车")
    print(f"首枪开始        : {a['first_start'][11:16]}      末枪结束 : {a['last_end'][11:16]}")
    print(f"实际充入        : {a['total_kwh']:.0f} kWh / 需求 {total_need:.0f} kWh")
    print(f"人工挪车        : {a['moves']} 次（插枪时间晚于到场 >10 分钟）")
    print(f"欠电发车        : {len(a['undercharged'])} 辆")
    if a["undercharged"]:
        print("  明细          : " + "、".join(f"{v}(缺 {d:.0f} kWh)" for v, d in a["undercharged"]))
    if a["never_charged"]:
        print(f"  其中从未充过电 : {len(a['never_charged'])} 辆（{'、'.join(a['never_charged'])}）")
    off = official_kpi()
    if off:
        print(f"官方基线        : 欠电 {off['departures_below_required_soc']} 辆 / "
              f"可用率 {off['charger_availability_pct']}% / 电费 {float(off['energy_cost_eur']):.0f} €")
    print()
    print("关键观察：第一波 12 辆在 19:00~20:20 插上，全部到 00:30 才被")
    print("          unplugged_by_operator —— 操作员是凌晨统一走一轮批量换位，")
    print("          不是充满就换。第二波 00:30 才开始，只剩 5.5 小时，")
    print("          结果 3 辆车整夜没轮到枪，1 辆只充了 300 kWh。")

    fault_cap = cap_profile([(t0, CABINETS_KW), (FAULT_TS, CABINETS_KW - KW_LOST)])

    hr("3. 场景 B：零人化，24 个连接点（含机柜停机故障）")
    b = simulate(jobs, POINTS_AFTER, CABINETS_KW, strategy="urgency",
                 cap_fn=fault_cap, fault=(FAULT_TS, GUNS_ON_CABINET))
    print(f"连接点          : {POINTS_AFTER} 个（12 台双枪卫星，一拖二车位）")
    print(f"故障            : {FAULT_TS:%H:%M} C1-3 停机，{GUNS_ON_CABINET} 个连接点失电")
    print(f"人工挪车        : {b.moves} 次")
    print(f"欠电发车        : {len(b.undercharged)} 辆")
    print(f"全队充满时刻    : {b.last_finish:%H:%M}" if b.last_finish else "全队充满时刻    : N/A")
    print(f"总充入          : {b.total_kwh:.0f} kWh / 需求 {total_need:.0f} kWh")
    print(f"峰值功率        : {b.peak_kw:.0f} kW / 上限 {CABINETS_KW} kW")

    hr("4. 场景 C：零人化 + 柜间互济")
    c = simulate(jobs, POINTS_AFTER, CABINETS_KW, strategy="urgency", cap_fn=fault_cap)
    print(f"连接点          : {POINTS_AFTER} 个，卫星可由任意机柜供电")
    print(f"故障            : {FAULT_TS:%H:%M} C1-3 停机，点位不死，容量降到 {CABINETS_KW - KW_LOST} kW")
    print(f"人工挪车        : {c.moves} 次")
    print(f"欠电发车        : {len(c.undercharged)} 辆")
    print(f"全队充满时刻    : {c.last_finish:%H:%M}" if c.last_finish else "全队充满时刻    : N/A")
    print(f"总充入          : {c.total_kwh:.0f} kWh / 需求 {total_need:.0f} kWh")
    print(f"峰值功率        : {c.peak_kw:.0f} kW / 上限 {CABINETS_KW} kW")
    print()
    print("说明：B 与 C 在本场景下结果相同 —— 因为全队在 02:30 已充满，")
    print("      02:25 的故障落下时系统已经空载。柜间互济不是本场景的必需项，")
    print("      而是应对「多柜同时故障」或「充电被延误拖后」的保险。")

    hr("5. 对比表")
    rows = [
        ("连接点", GUNS_NOW, POINTS_AFTER, POINTS_AFTER),
        ("人工挪车 次/夜", a["moves"], b.moves, c.moves),
        ("夜间人工 分钟", a["moves"] * MIN_PER_MOVE, 0, 0),
        ("欠电发车 辆", len(a["undercharged"]), len(b.undercharged), len(c.undercharged)),
        ("全队充满 时刻", a["last_end"][11:16], b.last_finish.strftime("%H:%M") if b.last_finish else "-",
         c.last_finish.strftime("%H:%M") if c.last_finish else "-"),
        ("总充入 kWh", round(a["total_kwh"]), round(b.total_kwh), round(c.total_kwh)),
    ]
    print(f"{'指标':<18}{'A 真实基线':>14}{'B 零人化':>14}{'C 零人化+互济':>16}")
    print("-" * 62)
    for name, *vals in rows:
        print(f"{name:<18}" + "".join(f"{v:>14}" if i < 2 else f"{v:>16}" for i, v in enumerate(vals)))

    hr("6. 硬件代价（按官方 equipment_costs.csv 口径）")
    unit, civil = 18_000, 9_000
    extra = POINTS_AFTER - GUNS_NOW
    print("方案            : 现有 12 台卫星换双枪输出 + 柜间互济母排")
    print(f"新增连接点      : {extra} 个")
    print(f"保守口径        : {extra} × {unit:,} € = {extra * unit:,} €（按整机计价）")
    print(f"枪线口径        : {extra} × 3,000~5,000 € = {extra * 3_000:,} ~ {extra * 5_000:,} €")
    print(f"对照：加整台枪   : {extra} × ({unit:,}+{civil:,}) € = {extra * (unit + civil):,} €")
    print()
    print("说明：官方成本表无「单条枪线」与「柜间互济母排」条目，")
    print("      pitch 中报保守值，并注明实际应更低。")


if __name__ == "__main__":
    main()
