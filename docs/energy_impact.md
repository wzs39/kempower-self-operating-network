# Energy & Grid Impact Verification Report (`docs/energy_impact.md`)

> **Evaluation Dimension**: **Energy and Grid Impact (20% Weight)**  
> **Official Rubric Prompt**: *"What your design does to **energy cost**, **peak power**, **grid limits** and **the use of available energy**, **shown with numbers from the data**. The baseline numbers in `baseline_kpis.csv` and `network_kpis.csv` show how the network performs with people in the loop today. Use them as a reference point when you show your results."*  
> **Reproducibility**: All numbers below are deterministically computed from the 45 unmodified official CSV files (`baseline_kpis.csv`, `site_power_baseline.csv`, `prices.csv`, `tariffs.csv`, `network_site_power.csv`, `network_kpis.csv`) and `verify_all.py`.

---

## 1. Master Station-by-Station Energy & Grid Impact Table (Scenario Day `2026-11-13`)

Reference baseline values are taken directly from `baseline_kpis.csv` (`period=scenario_day`) and cross-verified by integrating `site_power_baseline.csv` × (`prices.csv` + `tariffs.csv`) at 15-minute resolution (`0.25 h`).

### Table 1A: Calendar-Day Energy Cost, Peak Power & Grid Limit Compliance (`2026-11-13`)

| 站点 | 基线 €/日 (`baseline_kpis.csv` / 积分精确值) | 优化 €/日 (同电量口径 / 含补齐欠电总支出) | 节省 €/日 (同电量口径) | 节省% (单位 MWh 成本降幅) | 基线峰值 kW (`baseline_kpis.csv`) | 优化峰值 kW (实测) | 峰值降幅 kW | 越限行数 (`grid_kw > grid_limit_kw`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S1 (Bus Depot, 12 guns)** | **668.00 €** (`668.33 €`, `9.23 MWh`) | **664.05 €** *(含补齐 `+349.5 kWh` 实付 `682.43 €`, `9.58 MWh`)* | **+4.28 €** *(多充 `349.5 kWh` 净增 `14.10 €`)* | **+0.6%** *(单位电价 `72.37 -> 71.20 €/MWh`, **-1.6%**)* | **1,080.0 kW** | **1,080.0 kW** | **0.0 kW (峰值未下降)**¹ | `0 / 96` |
| **S2 (Truck Depot, 8 guns)** | **689.00 €** (`689.07 €`, `5.96 MWh`) | **386.09 €** (`5.96 MWh`, 移峰 `600 kWh` 避开 `799.30 €/MWh` 尖峰) | **+302.98 €** | **+44.0%** (`115.69 -> 64.82 €/MWh`) | **800.0 kW** | **800.0 kW** *(16:00–20:00 DSO 限电期压至 **400.0 kW**)* | **0.0 kW (全天) / 400.0 kW (DSO 窗口)**² | `0 / 96` |
| **S3 (Highway Hub, 10 guns)** | **2,300.00 €** (`2,300.48 €`, `17.03 MWh`) | **2,051.59 €** (`17.03 MWh`, 尖峰期 `623.8 kWh` 涓流移峰) | **+248.89 €** | **+10.8%** (`135.06 -> 120.45 €/MWh`) | **1,500.0 kW** | **1,425.0 kW DC** (`1,492.15 kW AC`) | **75.0 kW DC / 7.85 kW AC**³ | `0 / 96` |
| **S4 (City Hub, 8 guns)** | **401.00 €** (`401.05 €`, `3.90 MWh`) | **344.09 €** (`3.90 MWh`, 避开 `18:00` `799.30 €/MWh` 尖峰 `120 kWh`) | **+56.96 €** | **+14.2%** (`102.93 -> 88.31 €/MWh`) | **526.0 kW** (`525.9 kW`) | **450.0 kW** | **76.0 kW (-14.4%)** | `0 / 96` |
| **S5 (New Bus Depot, 8 guns)** | **299.00 €** (`298.92 €`, `4.19 MWh`) | **276.45 €** *(含补齐 `+508.95 kWh` 实付 `301.80 €`, `4.70 MWh`)* | **+22.47 €** *(多充 `508.95 kWh` 净增 `2.88 €`)* | **+7.5%** *(单位电价 `71.42 -> 64.28 €/MWh`, **-10.0%**)* | **600.0 kW** *(错配锁死)* | **900.0 kW** *(修复错配释放 `+300 kW`)* | **-300.0 kW (主动解锁瓶颈)**⁴ | `0 / 96` |
| **五站合计 (`S1–S5`)** | **4,357.00 €** (`4,357.85 €`, `40.31 MWh`) | **3,722.27 €** *(含补齐 `+858.45 kWh` 实付 `3,766.00 €`, `41.17 MWh`)* | **+635.58 €** *(含扩容电量净省 **591.85 €/日**)* | **+14.6%** *(含扩容电量净省 **+13.6%**, 单位成本 **-15.4%**)* | **4,506.0 kW** (算术和) | **4,655.0 kW** (含 S5 解锁 `+300 kW`) | **S3+S4 降峰 151.0 kW；S1/S2 物理封顶** | **`0 / 480`** (场景日) / **`0 / 134,400`** (全集) |

> **Honest Engineering Notes on Peak Power (为何 S1/S2 峰值未下降、S5 峰值反而上升)**:
> 1. **S1 峰值未下降 (`1,080.0 kW -> 1,080.0 kW`)**：S1 夜间需为 **32 个次日出发班次**（总需求 `7,872.0 kWh`，其中 24 辆在夜间集中到达）充电，却只有 12 把物理 CCS2 枪（3 台 360 kW 机柜 = `1,080 kW` 物理上限，贴近 `1,200 kW` 电网限额），且 `02:25` C1-3 过温跳闸后可用容量跌至 `720 kW`。在零硬件投入下，12 把枪在故障前必须满功率运行才能抢在跳闸前多充入 `+349.5 kWh`（把仿真缺口从 `398.5 kWh` 压到 `48.8 kWh`）。**在 S1 降低峰值功率必须配置 BESS 储能或扩容充电枪位，纯软件若强行压降 S1 峰值只会加剧公交欠电漏发**。
> 2. **S2 全天峰值未下降 (`800.0 kW`)，但限电窗口严格压降至 `400.0 kW`**：S2 在 `14:20–16:00` 电网正常窗口需跑满 `800.0 kW` 为下午出车的 `T01–T04` 抢充电量；在 `16:00–20:00` DSO 限电窗口严格压死在 `400.0 kW`，并将过夜卡车 `T05–T08` 的 `600.0 kWh` 充电负荷从 `17:15–18:45` 电价尖峰（最高 `799.30 €/MWh`）平移至 `22:00` 后低谷（`54.40 €/MWh`），单日省电费 **302.98 € (-44.0%)**。
> 3. **S3 峰值受 $\eta=0.955$ 逆变损耗安全护栏约束**：在 `1,500 kW` 变压器交流上限下，站端本地 DLM 将直流母线上限控制在 `1,425.0 kW DC`（对应交流输入 `1,492.15 kW AC <= 1,500 kW`），留出 `7.85 kW AC` 裕度防止逆变损耗导致主变过载。
> 4. **S5 峰值从 `600.0 kW` 升至 `900.0 kW` 是修复工程事故**：S5 物理安装了 `2×450 kW = 900 kW` 机柜且变压器容量为 `900 kW`，但 `site_config.csv` 第 164 行误设为 `600 kW`，导致 5 辆早班公交欠电 `508.95 kWh`。三方配置核对器自动将 `grid_limit_kw` 恢复为 `900 kW`，在 `01:00–04:30` 低谷电价期（均价 `49.80 €/MWh`）补齐全部 `508.95 kWh` 缺口。

---

### Table 1B: Same-Engine Shift-Window Simulation Output (`src/sim/discrete_sim.py` × `prices.csv`)

To guarantee 100% same-engine A/B comparability (`fcfs` vs `urgency` on the exact same timetable window in `discrete_sim.py`), the table below reports the direct simulator outputs (`total_kwh` × minute-by-minute price from `prices.csv`):

| 站点与班次窗口 | 仿真情景 | 漏发车辆 (`missed_departures`) | 仿真能量缺口 (`deficit_kwh`) | 仿真交付电量 (`total_kwh`) | 班次仿真电费 (`€`) | 仿真峰值 (`peak_kw`) |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **S1 (`2026-11-13` 全部 32 班次)** | 同引擎基线 (`12 枪, cross_tie=False, fcfs`) | **4** (`B04, B09, B18, B20`) | **398.5 kWh** *(官方无会话绝对缺口 `1,012.00 kWh`)* | **7,473.5 kWh** | **326.92 €** | **1,080.0 kW** |
| **S1 (`2026-11-13` 全部 32 班次)** | 零 CAPEX 软件 (`12 枪, cross_tie=False, urgency`) | **3** (`B04, B09, B18` — **B20 救回**) | **48.8 kWh (-87.8%)** | **7,823.0 kWh** (`+349.5 kWh`) | **344.12 €** *(因多充 `349.5 kWh`)* | **1,080.0 kW** |
| **S1 (`2026-11-13` 全部 32 班次)** | 硬件扩容 (`24 点位, cross_tie=True, urgency`) | **0** | **0.0 kWh (-100.0%)** | **7,872.0 kWh** (`+398.5 kWh`) | **346.07 €** *(充入 100% 需求)* | **1,080.0 kW** |
| **S5 (`2026-11-13` 夜间 12 班次)** | 修复 `900 kW` 后 (`8 枪, cross_tie=False, urgency`) | **0** *(官方错配基线为 **5**)* | **0.0 kWh** *(官方错配缺口 `508.95 kWh`)* | **4,376.7 kWh** | **181.17 €** | **900.0 kW** |

> ⚠️ **口径隔离声明**：官方 `departures_baseline.csv` 导出的 **1,012.00 kWh** 是 `B04/B18/B20`（当日 0 会话，各缺 `328 kWh`）与 `B09`（缺 `28 kWh`）的记录绝对缺口；而同引擎仿真输出的 **398.5 kWh -> 48.8 kWh** 是 12 枪连续调度下的出发时刻残余缺口。两者统计口径不同，严禁混算或直接相减。

---

## 2. Rubric Object #3: Grid Limits — The 95-Station `network_kpis.csv` Proof & `network_site_power.csv` Basis Audit

### 2.1 The 95-Station Golden Proof (`network_kpis.csv`)
While `sites.csv` + `baseline_kpis.csv` cover the **5 detailed inspection sites (`S1–S5`)**, `network_kpis.csv` provides the **95 broader network sites** (`95 + 5 = 100` total sites; the two tables have disjoint station sets and are never summed together):

| `network_kpis.csv` 实测聚合指标（95 个网络站点，14 天） | 官方 CSV 精确数值 | 物理与运营含义 |
| :--- | :--- | :--- |
| **总交付能量 (`SUM(energy_mwh)`)** | **13,368.6 MWh** | 95 站 14 天总充电量 |
| **需求超电网限额累计时长 (`SUM(hours_demand_above_grid_limit)`)** | **2,096.1 小时** | 车辆原始充电需求超出变压器限额的总时长 |
| **发生需求超限的站点数 (`hours_demand_above_grid_limit > 0`)** | **72 / 95 站 (75.8%)** | 超过四分之三的场站面临变压器容量瓶颈 |
| **峰值功率分毫不差等于电网限额的站点数 (`peak_grid_kw == grid_limit_kw`)** | **72 / 95 站 (75.8%)** | 如 `SE-24` (`2,050 == 2,050 kW`)、`FI-13` (`1,250 == 1,250 kW`) |
| **欠电发车总数 (`SUM(departures_below_required)`)** | **352 班次** | 人工压负荷导致的次生欠电违约 |
| **公共充电排队放弃 (`SUM(abandoned) / SUM(arrivals)`)** | **26,482 / 169,006 (15.67%)** | 功率受限与排队导致的公共端流失 |
| **平均充电桩可用率 (`AVG(dispenser_availability_pct)`)** | **99.56%** | 硬件本身正常，瓶颈在于功率调度与配网限额 |

**Why this matters**: Natural electrical load never stops at the exact integer of `grid_limit_kw` across 72 stations. Having `peak_grid_kw == grid_limit_kw` across 72 stations during **2,096.1 hours** of excess demand is the **operational fingerprint of manual/reactive power capping** (`14,600 min = 3.25 FTE` of manual load shedding in `operations_log.csv`). Our edge DLM and 15-minute MILP automate all **2,096.1 hours** of grid-limit enforcement while prioritizing urgent departures (`urgency waterfilling`) to prevent the 352 undercharged departures.

### 2.2 `network_site_power.csv` (134,400 Rows) Two-Basis Audit
1. **Official `grid_kw` Column Basis**: Across all `134,400` rows of `network_site_power.csv`, `grid_kw > grid_limit_kw` occurs in **`0` rows** (a built-in recording invariant of the baseline dataset).
2. **True AC Input Basis (`delivered_kw / 0.955`)**: In `network_site_power.csv`, `grid_kw` was recorded equal to `delivered_kw` (DC) without dividing by the $\eta = 0.955$ AC/DC rectifier efficiency. If recomputed as `delivered_kw / 0.955 > grid_limit_kw`, **`9,644` rows (`7.18%`)** exceed `grid_limit_kw`. This is a **baseline recording basis difference** (not claimed as an optimization delta of our algorithm), whereas our `InverterEfficiencyGuard` explicitly enforces $P_{\text{DC}} \le 0.955 \times P_{\text{grid\_limit}}$ (`1,425.0 kW DC = 1,492.15 kW AC <= 1,500 kW` at S3).

---

## 3. Rubric Object #4: Use of Available Energy (可用能量与枪时利用率)

Rather than leaving cables plugged into already-full vehicles or starving late arrivals on a single cabinet, urgency waterfilling maximizes the **use of available hardware & grid energy** during constrained windows:

| 指标 (Station S1 夜间窗口 `18:58–06:30`，含 `02:25` C1-3 跳闸) | 同引擎 FCFS 基线 (`12 枪`) | 零 CAPEX Urgency 优化 (`12 枪`) | 24 点位扩容 (`24 点位`) | 变化率 (零 CAPEX vs 基线) |
| :--- | :--- | :--- | :--- | :--- |
| **可用机柜容量上限 (`Available Cabinet Energy`)** | `16,662.0 kWh` (全周期) / `10,986.0 kWh` (夜间) | `16,662.0 kWh` / `10,986.0 kWh` | `16,662.0 kWh` / `10,986.0 kWh` | 物理上限相同 |
| **可用枪时容量 (`gun_kw × 可用枪时`)** | `27,770.0 kWh` (全周期) / `16,470.0 kWh` (夜间) | `27,770.0 kWh` / `16,470.0 kWh` | `69,900.0 kWh` | 12 枪物理上限相同 |
| **实际充入有效电量 (`Delivered Energy`)** | **7,473.5 kWh** | **7,823.0 kWh** | **7,872.0 kWh** | **+349.5 kWh (+4.68%)** |
| **夜间机柜可用能量利用率 (`Delivered / 10,986 kWh`)** | **68.03%** | **71.21%** | **71.65%** | **+3.18 个百分点** |
| **夜间可用枪时利用率 (`Delivered / 16,470 kWh`)** | **45.38%** | **47.50%** | 23.90% (24 枪分母翻倍) | **+2.12 个百分点** |
| **车队目标电量满足率 (`Delivered / 7,872.0 kWh`)** | **94.94%** (缺 `398.5 kWh`, 4 辆欠电) | **99.38%** (缺 `48.8 kWh`, 3 辆微欠, **B20 救回**) | **100.00%** (0 缺口) | **消除 87.8% 能量缺口** |

---

## 4. 全网 134,400 行实证深化：电网削峰与人工压功率的因果咬合（连接 20% 能源维度与 25% 自治度）

> 参见 [`docs/attribution_matrix.md`](./attribution_matrix.md) 获取 S1 16 格因果归因矩阵（证明去掉 `F016` 单柜故障后朴素 `fcfs` 在 12 枪 `cross_tie=False` 下即为 `0` 漏发，且 `urgency` 算法将人工搬枪从 `12` 次降至 `0` 次）。

### 4.1 100 站 × 14 天 × 15 分钟 (`network_site_power.csv`) 能量削减与人工操作强相关证明

| 实测指标（100 站 × 1,344 步 = 134,400 行） | 精确数值 | 数据来源与计算公式 |
|---|---:|---|
| 需求超过电网限值的 15 分钟时段数 | **9,293 / 134,400 (`6.91%`)** | `network_site_power.csv`: `demand_kw > grid_limit_kw` |
| `delivered_kw == min(demand_kw, grid_limit_kw)` 行占比 | **130,235 / 134,400 (`96.90%`)** | 证明基线网络靠“硬削顶”运行 |
| **因电网限值被削掉（未交付）的能量** | **1,229.3 MWh / 14d $\to$ 32,050 MWh / 年** | `((demand_kw - grid_limit_kw).clip(lower=0) * 0.25).sum()` |
| 被削减能量占实际交付能量 (`13,834.4 MWh`) 比例 | **8.89%** | `1,229.3 / 13,834.4`（总需求 `14,858.0 MWh`） |
| 超限小时数 / 超限站数（95 个网络站口径） | **2,096.1 h / 72 站** *(逐行复算 `2,102.2 h`)* | `network_kpis.csv`: `hours_demand_above_grid_limit` |
| 超限小时数 / 超限站数（含 S1–S5 的 100 站口径） | **2,323.2 h / 77 站** | `network_site_power.csv` 全量 100 站汇总 |
| 被削顶时段 vs 未被削顶时段的客户放弃率 | **23.82% vs 14.43%** | `abandoned / arrivals` |
| 被削顶时段 vs 未被削顶时段的平均排队长度 | **2.74 辆 vs 0.08 辆 (`34×`)** | `queue_len` |
| 人工下发功率调整 (`manual_load_adjustment`) | **684 次 / 10,260 分钟（两周）** | `operations_log.csv` (`7.73%` 事件，`10.98%` 工时) |
| **684 次人工压功率落在哪些站点** | **100.0% 落在有超限的站点（非超限站 0 次）** | `operations_log.csv` $\bowtie$ `network_site_power.csv` |
| 站点超限小时数 × 人工压功率分钟数相关性 | **Spearman $\rho = 0.802$ / Pearson $r = 0.913$** | 100 站截面显著正相关 |

- **主动交代的官方基线数据记录特征**：
  1. `network_site_power.csv` 中存在 **2,621 行 `delivered_kw > grid_limit_kw`**（系基线历史数据记录口径特征，不计作本方案优化成果）；
  2. 全网有 **12 个站点的 `grid_limit_kw` 随时间动态变化**（包含 S2、S4 及 DK-02、NO-12、FI-15、FI-20、NO-01、SE-06 等），因此所有合规校验均严格按**逐行时变 `grid_limit_kw(t)`** 计算。

### 4.2 全网 100 站硬件可用能量窗口利用率 (`Use of Available Energy`) 与 2029 增长压力

| 窗口口径（100 站 × 336 小时） | 14 天能量容量 / 交付量 | 利用率 / 结论 |
|---|---:|---|
| **100 站充电硬件额定能量窗口** (`Σ dispensers × dispenser_kw × 336h`) | **79,816.8 MWh / 14d** | **硬件能量窗口利用率仅 `17.33%`**（**`82.67%` 硬件窗口闲置**） |
| **100 站电网准入能量窗口** (`Σ grid_limit_kw × 336h`) | **47,896.8 MWh / 14d** | **电网能量窗口利用率 `28.88%`** |
| **100 站 14 天实际交付总能量** (`Σ delivered_kw × 0.25h`) | **13,834.4 MWh / 14d** | S1 全天 `19.6%`（夜间 `33.8%`），S2 `7.7%`，S3 `20.0%`，S4 `14.0%`，S5 `6.8%` |
| **2029 增长压力 (`growth_forecast.csv`)** | FI 重卡指数 **420 (`4.2×`)**，DE 重卡 **520 (`5.2×`)** | 同一套硬件利用率将从 `17.3%` 推高至 **`~73%`** |
| **柔性电网免扩容窗口 (`grid_capacity.csv`)** | **23 个超限站**可由合同既有 `flexible_extra_kw` **免费覆盖** | 对比全网硬扩容需 **14.5 M€ CAPEX** 与 **13–41 个月施工期** |

### 4.3 官方 14 天电费账单零误差复现与同能量窗口重排节费 (`tariffs.csv` + `prices.csv`)

1. **官方 14 天电费零误差复现（建立成本模型公信力）**：
   - 严格按 `network_site_power.delivered_kw × 0.25 × (prices.spot + tariffs day/night)` 复算 S1–S5 的 14 天电费：
     - **S1 (`T_DEPOT`)**：复算 **`6,298 €`** vs 官方 `baseline_kpis.csv` **`6,298 €`**（**误差 `0 €`**）
     - **S2 (`T_DEPOT`)**：复算 **`3,965 €`** vs 官方 **`3,965 €`**（**误差 `0 €`**）
     - **S3 (`T_PUBLIC`)**：复算 **`14,747 €`** vs 官方 **`14,747 €`**（**误差 `0 €`**）
     - **S4 (`T_PUBLIC`)**：复算 **`3,590 €`** vs 官方 **`3,590 €`**（**误差 `0 €`**）
     - **S5 (`T_DEPOT`)**：复算 **`1,378 €`** vs 官方 **`1,378 €`**（**误差 `0 €`**）
2. **场景日（`2026-11-13`）同能量、仅在车辆各自驻留窗口内重排的可演示节费**：
   - 在保持每辆车交付能量完全不变、仅将充电时段平移至驻留窗口内低价时隙的前提下：
     - **S1（32 辆）**：立刻充（ASAP）`415.0 €` $\to$ 窗口优化 **`325.2 €`**（**省 `89.8 €/日`，`-21.6%`**）
     - **S2（18 辆）**：立刻充（ASAP）`324.4 €` $\to$ 窗口优化 **`240.6 €`**（**省 `83.8 €/日`，`-25.8%`**）
     - **S5（12 辆）**：立刻充（ASAP）`182.9 €` $\to$ 窗口优化 **`155.7 €`**（**省 `27.2 €/日`，`-14.9%`**）
     - **三站合计直接节费**：**`200.8 €/日`（`≈ 22%`）** *(注：14 天同能量理论上限 bound 为 S1 `-51.7%`、S2 `-52.7%`、S5 `-55.3%`，仅作为理论裕度参考，不作为直接成果宣称)*。
3. **月度峰值需量电费账单基准 (`tariffs.csv`: 车队站 `6.50 €/kW·月`，公共站 `7.50 €/kW·月`)**：
   - S1 (`1,080 kW` $\to$ `7,020 €/月`)、S2 (`800 kW` $\to$ `5,200 €/月`)、S3 (`1,500 kW` $\to$ `11,250 €/月`)、S4 (`600 kW` $\to$ `4,500 €/月`)、S5 (`600 kW` $\to$ `3,900 €/月`)，五站合计 **`31,870 €/月`**（每削减 `5%` 峰值对应 **`19,122 €/年`** 需量电费节省，*billing-basis estimate on recorded peaks*）。
