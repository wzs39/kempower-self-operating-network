# 修复清单（执行版）

> 交接对象：执行修改的 AI / 工程师
> 项目：Kempower Self-Operating Charging Network（黑客松参赛仓库）
> 目标：在不新增功能、不重写架构的前提下，消除物理口径错误与数字口径混乱
> 本文档中所有数值均已由人工实测确认，**执行方不得自行推算或替换**

---

## 0. 铁律（违反任一条即视为任务失败）

1. **禁止修改 `kempower-challenge/kempower-challenge-data/` 下任何文件**（45 个 CSV、240,635 行，是官方数据，改了就失去可信度）。
2. **禁止删除或跳过 `tests/` 下任何测试**来让测试变绿。测试失败必须查根因。
3. **所有对外声明的数字必须来自脚本实际输出**，禁止手写、禁止四舍五入到更漂亮的数。
4. **每完成一项 P0，必须重跑** `python verify_all.py` 与 `python -m pytest tests/ -q`，全绿才能进入下一项。
5. **禁止新增第三方依赖**。已有依赖：pandas、scipy、pytest、cryptography、pypdf（仅文档用）。
6. 改动必须**同步**：代码、`verify_all.py` 断言、文档、`app.py` 的 payload 四处口径一致。只改其一不可交付。

---

## 1. 问题背景（30 秒读完）

项目原结论是「场景日 13 辆公交欠电 → 0 辆」。审计后发现两个口径错误：

- **S1 用了 24 个充电点位，但数据里只有 12 把枪。** `chargers.csv` 中 S1 = 12 把（D1-1..D1-12），全部 CCS2、每枪 150 kW、每枪只接一个功率柜。仿真却按每柜 8 点（3×8=24）并允许跨柜共享。
- **夜间任务集漏了 1 辆车。** `night_only` 用「到达小时 < 19 就丢弃」，把 B15（18:58 到达、次日 05:40 出发、进场 SoC 8%、要求 90%）排除了，分母变成 23 而非 32。

**关键发现**：改正这两处后，仿真在真实 12 枪拓扑 + 先到先充下跑出 **4 辆欠电，且欠电车辆恰好是 B04 / B09 / B18 / B20**——与官方 `departures_baseline.csv` 逐辆完全一致，峰值 1080 kW 也与官方 `baseline_kpis.csv` 的 1080 一致。

**结论不是「我们失败了」，而是「我们的仿真器被官方基线校准了」。** 修复后的叙事立刻比原来更强。

---

## 2. 已实测的验收基准（照抄，勿改）

口径说明：任务集 = `fleet_schedule.csv` 中 `site_id=S1` 且 `depart_ts` 以 `2026-11-13` 开头的全部班次（**32 辆**）。柜功率 `[360, 360, 360]`，`gun_kw=150`，故障注入 `C1-3 @ 2026-11-13T02:25`。

| 情景 | 点位/接线 | 策略 | 漏发 | 能量缺口 | 峰值 | 交付 |
|---|---|---|---|---|---|---|
| 基线（对应官方 4 辆） | 12 枪 / 不跨柜 | `fcfs` | **4** | **398.5 kWh** | **1080 kW** | 7474 kWh |
| 零 CAPEX 优化 | 12 枪 / 不跨柜 | `urgency` | **3** | **48.8 kWh** | 1080 kW | 7823 kWh |
| 扩容后 | 24 点位 / 跨柜 | `urgency` | **0** | **0.0 kWh** | 1080 kW | 7872 kWh |

欠电车辆：
- 基线 = `B04, B09, B18, B20`（每辆缺口 94.0 / 89.5 / 104.5 / 110.5 kWh）
- 优化 = `B04, B09, B18`（每辆缺口 20.1 / 16.8 / 11.9 kWh）—— **B20 被救回**
- 扩容 = 空

官方参照（`baseline_kpis.csv`，`period=scenario_day, site_id=S1`）：`departures=32`、`departures_below_required_soc=4`、`energy_mwh=9.23`、`energy_cost_eur=668`、`peak_kw=1080.0`、`charger_availability_pct=94.10`。

### ⚠️ 能量口径陷阱（最容易出错的地方）

官方 `departures_baseline.csv` 推出的 **1,012.00 kWh** 是「这几辆车当日完全无充电会话的绝对缺口（328×3 + 28）」；而仿真输出的 **398.5 kWh** 是「在调度下到出发时刻仍缺的能量」。**两个数不可相加、不可互相替代、不可并列成对比**。文档中必须分别标注口径，或只保留其中一个。

---

## 3. P0 必改项（不改则答辩必被问穿）

### P0-1 修正 S1 物理拓扑

**文件**：`src/sim/discrete_sim.py` 第 473–489 行

原文：
```python
    if site_id == "S1":
        # S1 Bus Depot: 3x360 kW cabinets, 24 connection points (dual-gun)
        # Night arrivals on 2026-11-12 departing 2026-11-13 morning
        jobs = load_fleet_jobs("S1", "2026-11-12", night_only=True)
        ...
            points_per_cabinet=8,  # 3 * 8 = 24 points
            ...
            cross_tie=cross_tie,
```

改为：
```python
    if site_id == "S1":
        # S1 Bus Depot: 3x360 kW cabinets, 12 connection points
        # chargers.csv: D1-1..D1-12, one CCS2 each, 150 kW, 1:1 bound to one cabinet.
        # Strict 1:N intra-cabinet wiring => no cross-cabinet tie (no busbar between cabinets).
        jobs = load_fleet_jobs("S1", "2026-11-13", night_only=True)
        ...
            points_per_cabinet=4,  # 3 * 4 = 12 points == 12 CCS2 guns
            ...
            cross_tie=False,
```

**同时必须处理**：`scenario_engine.py` 第 62 行显式传了 `cross_tie=True`，改为 `cross_tie=False`。

**验收**：该函数单独调用时输出 `missed_departures=4`、`deficit_kwh=398.5`、`peak_kw=1080`（策略 `fcfs`）。

---

### P0-2 修正任务集边界（分母）

**文件**：`src/sim/discrete_sim.py` 第 158–213 行 `load_fleet_jobs`

原文（第 185 行）：
```python
            if night_only and arr.hour < 19:
                continue
```

问题：按「到达小时」过滤会丢掉 B15（18:58 到、次日 05:40 走）。这辆车是全场最恶劣工况，恰恰最该被检验。

改为按「出发日期」筛选：新增参数 `depart_date: Optional[str] = None`，逻辑改为：
```python
            if night_only and depart_date and not dep_str.startswith(depart_date):
                continue
```
保留 `night_only` 向后兼容（无 `depart_date` 时行为不变，避免一次性炸掉其他站点与测试）。

**S1 调用处**必须传 `depart_date="2026-11-13"`。

**验收**：`load_fleet_jobs("S1","2026-11-13",night_only=True,depart_date="2026-11-13")` 返回 **32** 个 job，且 vehicle_id 列表包含 `B15`。

---

### P0-3 基线改为同引擎产出，不得再抄 CSV 常量

**文件**：`src/sim/scenario_engine.py` 第 55–80 行（S1 段）

现状：`"baseline_missed_departures": 4` 与 `"baseline_deficit_kwh": 1012.00` 是硬编码，与优化结果不同源，属「拿 CSV 当基线、拿理想模型当优化」的 A/B 不可比问题。

改为：在同一任务集上额外跑一次基线仿真：
```python
sim_s1_baseline = simulate_closed_loop_minute_by_minute(
    site_id="S1", date="2026-11-13", strategy="fcfs", cross_tie=False
)
```
返回字典中：
- `baseline_missed_departures` ← `sim_s1_baseline["missed_departures"]`
- `baseline_deficit_kwh` ← `sim_s1_baseline["deficit_kwh"]`
- 新增 `baseline_official_deficit_kwh: 1012.00`，并加注释 `# official recorded absolute gap (0 sessions), different basis from simulated deficit`
- 新增 `baseline_undercharged_vehicles` / `optimized_undercharged_vehicles`

**验收**：`baseline_missed_departures == 4`、`baseline_deficit_kwh == 398.5`、`baseline_undercharged_vehicles == ["B04","B09","B18","B20"]`、`optimized_missed_departures == 3`。

---

### P0-4 改写 verify_all.py 断言（拆成两条，不许删）

**文件**：`verify_all.py` 第 46–53 行

原文：
```python
    s1 = results["S1"]
    assert s1["baseline_deficit_kwh"] == 1012.00 and s1["optimized_missed_departures"] == 0
```

改为（保留强度，拆开表达）：
```python
    s1 = results["S1"]
    assert s1["baseline_missed_departures"] == 4
    assert s1["baseline_deficit_kwh"] == 398.5
    assert s1["baseline_undercharged_vehicles"] == ["B04", "B09", "B18", "B20"]
    assert s1["optimized_missed_departures"] == 3
    assert s1["optimized_deficit_kwh"] == 48.8
    assert s1["capacity_expansion_missed_departures"] == 0
    # ⚠️ 口径警告：该字段来自 scenario_engine.py:82-85，同时设了
    #    points_per_cabinet=8 (24 点位) 且 cross_tie=True (跨柜)，
    #    因此它是「扩容 + 跨柜互备」的复合情景，0 漏发成立。
    #    绝不可对外表述为「扩容到 24 枪 = 0 漏发」——单独扩容实测为 8 辆（更差）。
    assert s1["expansion_only_no_cross_tie_missed_departures"] == 8   # 仅扩容、不跨柜
```

**同时必须改字段命名或加注释**：`scenario_engine.py` 第 82–85 行的 `capacity_expansion_*` 系列容易被下游误读。建议在 `run_all_scenarios` 的返回 dict 里加一个 `capacity_expansion_note` 字段，值为 `"24 points + cross-cabinet busbar, composite scenario; expansion alone = 8 missed"`，并让 `app.py` 的 payload 一并带出。**这是 PPT 第 9 页写错数字的直接源头。**

第 50–53 行的打印文案改为：
```
[PASS] Station S1 (Bus Depot) : 12 CCS2 guns (physical) | Official 4 below-SoC = B04/B09/B18/B20
       Same-engine baseline 4 missed (398.5 kWh) -> Urgency 3 missed (48.8 kWh, -87.8%)
       Zero-miss paths: +12 plugs=8 missed (worse) | cabinets 3x450kW=0 but 1350kW > 1200kW grid limit
       Only in-limit zero path = cross-cabinet busbar (not in chargers.csv, no price) | D1-9 59.3C @ 22:31 | N-1 720 kW
```

第 101–104 行的总结句 `13 -> 0 Scenario Day Missed Departures` 改为：
```
13 official below-SoC -> S1 4 to 3 after zero-CAPEX software | S2/S5 = MEASURE, do not guess | zero-miss needs busbar redundancy (unpriced)
```

**注意**：`capacity_expansion_missed_departures` 需要 `scenario_engine` 额外跑一次 24 点位情景（`points_per_cabinet=8, cross_tie=True`），作为「扩容情景」字段返回，不能删掉这个能力——它是定价依据。

---

## 4. P1 交付层修复

### P1-1 全局数字统一（13→0 必须改成三档）

涉及文件：`README.md`、`PROJECT.md`、`HACKATHON.md`、`PITCH_DECK_OUTLINE.md`、`docs/hackathon/SUBMISSION.md`、`docs/hackathon/BRIEF.md`、`反思与路线纠偏报告.md`、`One_Page_SLA_Specification.md`

规则：凡出现「13 → 0」「0 missed」「zero missed departures」**未加条件**的表述，一律替换为下表陈述：

| 档位 | 投入 | 结果 | 是否成立 |
|---|---|---|---|
| 官方基线（12 枪、先到先充） | — | 13 辆（S1=4, S2=4, S5=5） | 参照 |
| 零 CAPEX 软件（12 枪、urgency） | 0 € | S1 4→**3**（缺口 398.5→48.8 kWh）；S2、S5 以实测为准 | ✅ 可交付 |
| 加 12 把枪 @ S1（24 点位、无跨柜） | 324,000 € | S1 **8 辆**（**恶化**，每枪 90→45 kW） | ❌ 不成立 |
| 柜扩容至 3×450 kW @ S1 | 75,600 € | S1 0 辆，但峰值 **1,350 kW > 1,200 kW 电网限值** | ❌ 物理不可行 |
| 跨柜母线互备 @ S1 | 官方无报价 | S1 0 辆，峰值仍 1,080 kW | ⚠️ 唯一在限值内清零，但无价格 |

> **⚠️ 重要更正（2026-11-06 实测）**：本清单原稿写的「324,000 € = 0 辆、13.31 年回收」是**错的**，与本文件同源的归因矩阵（24 点位 + 无跨柜 + 有故障 = 8 辆漏发）自相矛盾。原因：324,000 € 只买 dispenser（`18,000 + 9,000 civil_works = 27,000 €/把 × 12`），**不增加柜功率**（仍 3×360 = 1,080 kW），也不改变「每把枪只接一个柜」的接线事实。**执行时不要再写「324,000 € 换 0 漏发」，也不要再写 13.31 年回收。**

**必须注意**：S2、S5 的优化后数字**不要凭本清单推断**，执行方需用同样方法各跑 fcfs 与 urgency 两遍，取实测值填入。若 S2/S5 在真实点位下仍为 0，则如实写 0——但必须来自实测。

替换后建议保留这段统一说明（英文版供 PPT 用）：
> "Zero missed departures is achievable in our model — but not by buying more plugs. Doubling S1's dispensers to 24 (324,000 EUR) actually makes it **worse** (8 missed departures), because cabinet power stays at 1,080 kW and each gun drops from 90 kW to 45 kW. Raising cabinet power to 3×450 kW reaches zero, but the resulting 1,350 kW peak **exceeds the 1,200 kW grid limit**. The only zero-miss path that stays inside your grid limit is cross-cabinet busbar redundancy — which is not in `chargers.csv` and has no price in `equipment_costs.csv`. So we do not invent that number. Our zero-CAPEX software closes 87.8% of the energy gap with **zero manual replugs**."

### P1-2 测试数口径统一

现状（同一口径出现四种数）：`README.md` 322 / 428；`PROJECT.md` 179 / 431；`HACKATHON.md` 179；`PITCH_DECK_OUTLINE.md` 454。

执行步骤：
1. 运行 `python -m pytest tests/ -q` 取真实通过数（记为 N）。
2. 运行 `python -m e2e_tests.test_runner` 取真实通过数（记为 M，现为 106）。
3. **全局统一为** `N pytest + M E2E`，并在括号中写总数。禁止再出现其他版本。
4. `.agents/` 目录下历史记录文件**不要改**（属于过程记录，不是交付物）。

### P1-3 补能量维度对照表（官方 20% 权重的硬要求）

官方原文要求「用数据里的数字展示对电费、峰值功率、电网限额的影响」。目前项目只有机制、没有结果表，这是最亏的失分。

新建 `docs/energy_impact.md`，表格必须含以下列：

| 站点 | 基线 €/日 | 优化 €/日 | 节省 €/日 | 节省% | 基线峰值 kW | 优化峰值 kW | 峰值降幅 kW | 越限行数 |
|---|---|---|---|---|---|---|---|---|

数据来源：
- 基线列：`baseline_kpis.csv`（`period=scenario_day`）的 `energy_cost_eur` 与 `peak_kw`（注意这是「日」值表，勿当年度值）
- 优化列：仿真输出 `total_kwh` × 分时电价（电价取自官方 CSV，勿硬编码）
- S1 峰值已验证：基线与优化均为 1080 kW（与官方 1080 完全一致），**如实写「峰值未下降」，并解释原因是 12 枪物理上限已接近电网限值，降峰需 BESS 或扩容**——这句诚实说明比编一个降幅值更得分。

### P1-4 同步 app.py payload

`app.py` 展示的 S1 指标需与新口径一致（4 → 3、398.5 → 48.8、扩容 0）。改完跑一次 `python app.py` 确认不报错。

---

## 5. P2 表述与逻辑修复

| 项 | 位置 | 现状 | 改为 |
|---|---|---|---|
| P2-1 | 全局文档 | "digital twin / 数字孪生" | "offline discrete-event simulator（离线离散事件仿真器）" |
| P2-2 | 全局文档 | "microsecond switching / 微秒级" | "millisecond-scale break-before-make relay sequencing；software decision <10 ms" |
| P2-3 | 全局文档 | "predictive AI / 预测性 AI" | "threshold + slope extrapolation（阈值+斜率外推，199 min lead）" |
| P2-4 | 涉及 BESS 的段落 | 表述为已实现 | 标注 "interface defined, not field-validated（接口已定义，未实测）" |
| P2-5 | `src/core/virtual_replug.py` 第 8–15 行 Track A2 | 用「11 次人工换枪」实现 0 漏发 | 明确标注为「反事实压力测试：证明 0 漏发需付出 11 次人工移动，因此不推荐；不计入主成果」 |
| P2-6 | `verify_all.py` 第 42–44 行「0 越限」 | 用官方 `grid_kw` 列自证 0 越限，属数据自带恒等式 | 改为两句：①官方 `grid_kw` 列 0 行越限（数据事实）；②若按 `delivered_kw/0.955` 口径复算存在 N 行越限，属基线记录口径差异，**不作为本方案成果**。N 需实测填写 |

---

## 6. 明确禁止做的事

- 不要新增功能模块（BESS 调度、V2G、新协议都不要碰）
- 不要重写架构或目录结构
- 不要为了让 `verify_all.py` 通过而放宽断言（如把 `==` 改成 `<=`）
- 不要删除 24 点位仿真能力（它是扩容定价的依据，只是不再作为主口径）
- 不要把 398.5 kWh 与 1,012 kWh 写在同一句对比里
- 不要在文档中保留「零人工移动」类表述（若某情景含人工换枪，必须显式标注次数）

---

## 7. 最终验收清单

```
[ ] python verify_all.py                 -> 全绿，打印三档口径（4 / 3 / 0）
[ ] python -m pytest tests/ -q           -> 全绿，数量与文档一致
[ ] python -m e2e_tests.test_runner      -> 106/106
[ ] python app.py                        -> 正常启动无异常
[ ] grep -rn "13 -> 0\|13→0" *.md docs/  -> 无未加条件的残留
[ ] grep -rn "数字孪生\|microsecond\|微秒" *.md docs/ src/ -> 无残留
[ ] S1 点位 = 12（grep points_per_cabinet 确认 S1 为 4）
[ ] 所有对外数字可在 5 秒内被 verify_all.py 复现
```

完成标准：任何人拿到仓库，执行 `python verify_all.py`，能在 5 秒内看到「官方基线 4 辆 → 零 CAPEX 3 辆 → 扩容 0 辆」这一行，且 4 辆的车辆编号与官方 CSV 一致。
