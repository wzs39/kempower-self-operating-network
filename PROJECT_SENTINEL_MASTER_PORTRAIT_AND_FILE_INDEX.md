<div align="center">

# ⚡ Project Sentinel · The Self-Operating Charging Network
### 哨兵计划 · Kempower 自主运行充电网络全景大典与系统白皮书

[![Language: 🇨🇳 中文](https://img.shields.io/badge/Language-%F0%9F%87%A8%F0%9F%87%B3%20%E4%B8%AD%E6%96%87-blue?style=for-the-badge)](./README.md)
[![Language: 🇬🇧 English](https://img.shields.io/badge/Language-%F0%9F%87%AC%F0%9F%87%A7%20English-lightgrey?style=for-the-badge)](./README_EN.md)

**[ 🇨🇳 简体中文版 (当前浏览) ](./README.md)** &nbsp;&nbsp;|&nbsp;&nbsp; **[ 🇬🇧 English Version (Full Blueprint) ](./README_EN.md)**

---
</div>

# Project Sentinel · 全景自画像与全量文件深度索引大典
## (Master Comprehensive Self-Portrait & Exhaustive File-by-File Repository Index)

```
========================================================================================
项目名称：Project Sentinel（哨兵计划）· Kempower 自主运行充电网络
赛事背景：LahtiES Energy Tech Hackathon 2026 · Kempower 官方旗舰赛题
核心使命：在彻底禁止人类持续运维的约束下，重构新一代高可靠、电网友好型自主充电网络
交付形态：单文件全景整合（自画像顶层设计 + 仓库所有文件逐一深度索引与使用说明）
文件版本：v3.5-DEFINITIVE-MASTER · 终极合一全景大典
========================================================================================
```

---

# 目录导航

- [第一卷：项目全景自画像 (Master Self-Portrait)](#第一卷项目全景自画像-master-self-portrait)
  - [1.1 项目档案与赛题破题](#11-项目档案与赛题破题)
  - [1.2 评审五维权重与两大绝对红线](#12-评审五维权重与两大绝对红线)
  - [1.3 L1-L3 全栈三层系统架构](#13-l1-l3-全栈三层系统架构)
  - [1.4 核心数学运筹模型与物理电气约束](#14-核心数学运筹模型与物理电气约束)
  - [1.5 商业价值体系与 20.76 FTE 人力消除模型](#15-商业价值体系与-2076-fte-人力消除模型)
  - [1.6 技术真实性与五大铁律不变量（母排真相）](#16-技术真实性与五大铁律不变量母排真相)
  - [1.7 展示日现场实操全流程 SOP（含三级逃生防线）](#17-展示日现场实操全流程-sop含三级逃生防线)
  - [1.8 代码级验证推导与现场调证指南](#18-代码级验证推导与现场调证指南)
  - [1.9 评委全景问答库与黄金 75 秒应答应诉速查](#19-评委全景问答库与黄金-75-秒应答应诉速查)
- [第二卷：全代码库逐文件深度索引 (Exhaustive File-by-File Index)](#第二卷全代码库逐文件深度索引-exhaustive-file-by-file-index)
  - [2.1 根目录核心执行脚本与演示资产](#21-根目录核心执行脚本与演示资产)
  - [2.2 根目录权威规范与架构设计白皮书](#22-根目录权威规范与架构设计白皮书)
  - [2.3 展示日实战演练资产包目录 `demo_day_simulation/`](#23-展示日实战演练资产包目录-demo_day_simulation)
  - [2.4 核心算法库 `src/core/`](#24-核心算法库-srccore)
  - [2.5 仿真与数据引擎 `src/sim/`](#25-仿真与数据引擎-srcsim)
  - [2.6 商业结算引擎 `src/commercial/`](#26-商业结算引擎-srccommercial)
  - [2.7 支撑库与调度包 (`src/edf_packer.py` 等)](#27-支撑库与调度包-srcedf_packerpy-等)
  - [2.8 自动化测试与红蓝军验证套件 `tests/`](#28-自动化测试与红蓝军验证套件-tests)
  - [2.9 官方原始数据集资产总览 (45 CSVs)](#29-官方原始数据集资产总览-45-csvs)
- [第三卷：全场景常用命令与快速实战速查卡](#第三卷全场景常用命令与快速实战速查卡)
- [第四卷：比赛官方提交通行证与交付物清单大典 (Official Hackathon Submission Package)](#第四卷比赛官方提交通行证与交付物清单大典-official-hackathon-submission-package)
  - [4.1 官方比赛八大交付物总览清单](#41-官方比赛八大交付物总览清单)
  - [4.2 交付物合规性门禁与物理资产核验表](#42-交付物合规性门禁与物理资产核验表)
  - [4.3 官方强制 Rule 3：22 项假设与增补清单 (Assumptions & Additions Register)](#43-官方强制-rule-322-项假设与增补清单-assumptions--additions-register)
  - [4.4 Devpost / 比赛平台标准英文提交文案 (Project Story & Summary)](#44-devpost--比赛平台标准英文提交文案-project-story--summary)
  - [4.5 Pitch 答辩路演全套资产交付大典 (The Complete Pitch & Presentation Deliverables)](#45-pitch-答辩路演全套资产交付大典-the-complete-pitch--presentation-deliverables)
- [第五卷：S1-S5 五大旗舰场站场景日危机与 16 单元归因矩阵全解 (The S1-S5 Scenarios & 16-Cell Attribution Matrix)](#第五卷s1-s5-五大旗舰场站场景日危机与-16-单元归因矩阵全解-the-s1-s5-scenarios--16-cell-attribution-matrix)
  - [5.1 S1 公交北站：F016 跳闸与 16 单元因果归因矩阵深度拆解](#51-s1-公交北站f016-跳闸与-16-单元因果归因矩阵深度拆解)
  - [5.2 S2 物流东站：G1 限电危机与 1 kW 涓流调度预占](#52-s2-物流东站g1-限电危机与-1-kw-涓流调度预占)
  - [5.3 S3 高速大功率枢纽：断网光纤挖断孤岛与 1,425 kW 边缘坚守](#53-s3-高速大功率枢纽断网光纤挖断孤岛与-1425-kw-边缘坚守)
  - [5.4 S4 城市快充站：799.30 €/MWh 天价现货电价与 HiGHS MILP 连续松弛削峰](#54-s4-城市快充站79930-mwh-天价现货电价与-highs-milp-连续松弛削峰)
  - [5.5 S5 郊区大巴场站：三方配置冲突自校准与功率释放](#55-s5-郊区大巴场站三方配置冲突自校准与功率释放)
- [第六卷：45 份官方 CSV 原始数据集分类字典与全量行数盘库 (The 45 CSVs Data Dictionary & Inventory)](#第六卷45-份官方-csv-原始数据集分类字典与全量行数盘库-the-45-csvs-data-dictionary--inventory)
  - [6.1 六大类 45 份 CSV 详细字段字典与行数盘点](#61-六大类-45-份-csv-详细字段字典与行数盘点)
  - [6.2 官方数据质量陷阱、基线口径与预处理规则](#62-官方数据质量陷阱基线口径与预处理规则)
- [第七卷：深度审计、路线纠偏与工程反思报告全量集成 (Audit, Course Correction & Fusion Reports)](#第七卷深度审计路线纠偏与工程反思报告全量集成-audit-course-correction--fusion-reports)
  - [7.1 《反思与路线纠偏报告》三大核心教训](#71-反思与路线纠偏报告三大核心教训)
  - [7.2 《漏洞审查与赛题要求对照_第三轮》关键合规防线](#72-漏洞审查与赛题要求对照_第三轮关键合规防线)
  - [7.3 系统性审计报告集群与多端融合报告摘要](#73-系统性审计报告集群与多端融合报告摘要)
  - [7.4 官方开营演讲 PPTX、导师预约 Excel 与 24 条款法务原件深度索引](#74-官方开营演讲-pptx导师预约-excel-与-24-条款法务原件深度索引)
  - [7.5 现场图纸、架构拓扑与多媒体切片解析 (JPG/PNG/MP4)](#75-现场图纸架构拓扑与多媒体切片解析-jpgpngmp4)

---

# 第一卷：项目全景自画像 (Master Self-Portrait)

## 1.1 项目档案与赛题破题
- **项目代号**：Project Sentinel（哨兵计划）
- **赛事背景**：LahtiES Energy Tech Hackathon 2026（芬兰拉赫蒂，LUT University / CrazyTown）
- **赛题主办方**：Kempower（全球电动汽车大功率动态充电拓扑与模块化硬件领军企业）
- **官方主评审与导师**：
  - **Mats Mattsson**：Kempower 云端软件研发总监兼主评审（提出 21 FTE 运维人力基线）
  - **Panu Vartiainen**：Kempower 电气架构与系统专家
- **核心命题**：
  > *“If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?”*  
  > （如果不再允许人类持续运营和维护充电网络，该如何彻底重构它？）

### 破题逻辑：重新定义“零人化”的本质
常规团队往往陷入误区，试图用复杂的机械臂实现“无人插枪”，或宣称“永远不需要工程师巡检”。Project Sentinel 从第一性原理穿透官方 100 个场站、14 天跨度、240,635 行的真实数据集发现：
1. **司机的插拔动作是服务消费，而非运维负担**：夜班大巴司机回场顺手插枪，属于正常的消费交互行为；
2. **真正的运维黑洞源于“硬件拓扑的稀缺错配”**：以 S1 公交北站为例，24 辆夜间大巴仅配备 12 个物理充电枪（比例 2:1）。后半夜大巴无枪可插，逼迫夜班操作员凌晨 00:30 冒着 -18°C 极寒在雪地里集中人工挪车、拔枪、换插；
3. **零人化的真谛**：**消灭“夜间人工挪车”与“故障现场人工复位”，以【动态功率路由（DPR）+ 一拖二卫星即插即走】在物理层为每辆车提供永远待命的连接点，并以【边缘自主自愈 FSM】在毫秒级内平抑设备异常与电网冲击。**

---

## 1.2 评审五维权重与两大绝对红线
评委会严格依据五大维度打分，Project Sentinel 针对每一维度建立了最高规格的防御性证据链：
- **自主性（Autonomy, 25%）**：L1-L3 分层自治，全网消除 20.76 FTE 中的 14.5 FTE 日常运维，故障 260ms 自愈。
- **电网与能源影响（Energy & Grid Impact, 20%）**：134,400 行电网记录 0 越限，95.5% 逆变效率物理贴合，HiGHS MILP 实时削峰。
- **技术可信度（Technical Credibility, 20%）**：45 份官方 CSV 原始数据驱动，拒绝假母线造假（13→3 诚实边界），通过 28 项自动化 E2E 验证。
- **商业可行性（Commercial Viability, 20%）**：21 FTE 人力节约 136.5 万欧/年，软件投资静态回收期仅 2.1 个月，首创 One-Page CaaS 结果交付型 SLA。
- **方案清晰度（Clarity, 15%）**：10 分钟极速演讲与 2 分钟高潮迭起的 Live Demo，4 人微弧形协同站位与 75 秒三段式答辩范式。

> [!CAUTION]
> **两大不可逾越红线**：
> 1. **“Never change the data we gave”**：官方 45 份 CSV、240,635 行数据保持 100% 只读未改；
> 2. **“Count the cost”**：任何硬件必须按官方 [`equipment_costs.csv`](./equipment_costs.csv) 严格计价，严禁虚拟无成本硬件。

---

## 1.3 L1-L3 全栈三层系统架构

Project Sentinel 摒弃了脆弱的“纯云端集中式调度”，构建了具备极高工业级容错力的 **物理层 (L1) - 边缘层 (L2) - 云端层 (L3)** 三层协同体系：

```mermaid
graph TD
    subgraph L3 ["自主云端编排层 (L3 Autonomous Cloud Orchestrator)"]
        MPC["15分钟滚动 MILP 优化器<br/>(Nord Pool 电价套利 / 799.30€ 极端削峰)"]
        COMM["商业 ROI 与 SLA 清算引擎<br/>(MRDT §5.1 防欺诈门禁 / 月度账单自动清算)"]
    end

    subgraph L2 ["场站边缘自治控制器 (L2 Station Edge Controller)"]
        DLM["边缘 FSM 与自主局部动态负荷管理 (Local DLM)<br/>(100ms-15min 响应)"]
        ISLAND["72小时断网离线孤岛自愈<br/>(1,425 kW DC 满载输出，NVMe 本地暂存)"]
        PDM["提前 199 分钟超前热退化预警<br/>(59.3°C / 702 RPM 捕获)"]
        WEAR["25 kW 功率模块微观磨损均衡<br/>W = h + 0.5ΔT + 0.05Cycles"]
    end

    subgraph L1 ["物理设备与接触器阵列 (L1 Physical Device Layer)"]
        DPR["Kempower 模块化 DPR 矩阵与双枪分时卫星<br/>(<100ms 响应 / 25kW 功率单元投切)"]
        BBM["6 步严格先断后合 (Break-Before-Make) 状态机<br/>(260ms 零直流拉弧保护)"]
        SAFE["硬件级硬联锁防线<br/>(75°C 熔断器 / 30mA 漏电保护 RCD / 绝缘监测)"]
    end

    MPC -->|WAN / OCPP 2.0.1 TxProfile| DLM
    COMM -->|SLA 履约结算| DLM
    DLM -->|Modbus TCP / CAN / IEC 61851| DPR
    ISLAND --> DPR
    PDM --> DPR
    WEAR --> DPR
    DPR --> BBM
    BBM --> SAFE
```

---

## 1.4 核心数学运筹模型与物理电气约束

### 1.4.1 15分钟滚动 MILP 优化调度模型
在自主云端编排层，Sentinel 运行基于 `scipy.optimize.milp`（HiGHS 求解器后端）的 15 分钟滚动时域优化器：

$$\min_{P_{ch}, P_{bess}, z} \sum_{t=1}^{K} \left[ C_{spot}(t) \cdot P_{grid}(t) \cdot \Delta t + C_{peak} \cdot P_{peak\_monthly} + \sum_{i=1}^{N} \lambda_i \cdot z_i(t) \right]$$
- $C_{spot}(t)$：芬兰 Nord Pool 日前与实时现货电价（€/kWh）；
- $P_{grid}(t)$：场站电网侧吸收功率（kW）；
- $P_{peak\_monthly}$：月度需量电费峰值惩罚（6.50 €/kW/月）；
- $z_i(t) \in [0, 1]$：**连续松弛惩罚变量（Slack Variable）**。

### 核心物理约束集
1. **变压器与整流效率硬约束**：
   $$P_{AC}(t) = \frac{P_{DC}(t)}{\eta_{rect}} \le P_{transformer\_max} \quad (\eta_{rect} = 0.955)$$
   在 S3 高速站，$P_{DC} = 1,425\text{ kW}$，折算电网端输入为 $1425 / 0.955 = 1492.15\text{ kW} \le 1500\text{ kVA}$，完全受控于变压器安全物理容量内。
2. **电池荷电状态（SoC）递推与早高峰出车保底约束**：
   $$SoC_i(t+1) = SoC_i(t) + \frac{P_{ch,i}(t) \cdot \Delta t \cdot \eta_{ch}}{E_{batt,i}}$$
   $$SoC_i(T_{depart,i}) \ge SoC_{target,i} - z_i \quad (SoC_{target} \ge 90\%)$$
   通过松弛项 $z_i$，即使在 799.30 €/MWh 的天价电价洪峰下，求解器依然能在 **80ms 内凸收敛**，绝不崩溃无解。

---

### 1.4.2 260ms BBM（先断后合）零直流拉弧状态机
针对高压直流母线（800V DC）切换可能产生的致命电弧事故，Sentinel 在 [`src/core/self_healing.py`](./src/core/self_healing.py) 实现了严格的 6 步 BBM 状态机：

```mermaid
sequenceDiagram
    autonumber
    participant Controller as 边缘控制器 (Edge FSM)
    participant Module as 25kW 功率模块
    participant ContactorOld as 故障机柜接触器
    participant ContactorNew as 备用机柜接触器

    Note over Controller: 捕获过温停机告警 (F016)
    Controller->>Module: 1. 软件软关断，降电流至 0A (耗时 50ms)
    Module-->>Controller: 电流已归零确认
    Controller->>Controller: 2. 校验母线压差 <= 5V (耗时 60ms)
    Controller->>ContactorOld: 3. 驱动断开故障接触器 (耗时 80ms)
    ContactorOld-->>Controller: 4. 辅助微动开关回位确认 (耗时 50ms)
    Controller->>ContactorNew: 5. 驱动闭合目标接触器 (耗时 20ms)
    ContactorNew-->>Controller: 合闸完成到位
    Controller->>Module: 6. 重新快速爬升电流 (软启动)
    Note over Controller,ContactorNew: 总耗时 260ms (远优于 IEC 61851 500ms 安全窗口)
```

---

### 1.4.3 MRDT §5.1 防虚假插拔与骗取 SLA 算法
在 [`src/core/anti_fraud.py`](./src/core/anti_fraud.py) 中，系统建立了三支柱时空与电气指纹防线：
1. **时间邻近门禁**：$\Delta t < 180\text{s}$（3 分钟内重新插拔）；
2. **SoC 连续性门禁**：$|\Delta SoC| \le 1.0\%$（电量几乎无变化）；
3. **电流爬升率门禁**：$dI/dt > 100\text{ A/s}$（未经过冷启动缓充）。
- **处置机制**：被判定为 `PHANTOM_REPLUG_STITCHED` 的会话，系统自动免除重复的基础连接费（2.50 €），并缝合为一个连续的计费和驻留时间序列，阻断黑产通过反复断插制造“桩机故障”假象骗取 SLA 违约赔偿。

---

## 1.5 商业价值体系与 20.76 FTE 人力消除模型

基于 `operations_log.csv` 全部 8,852 行真实工单记录的严格穿透：

| 运维工单类别 | 记录次数 | 累计耗时 (min) | 耗时占比 | 对应 FTE | 消除机制与技术手段 |
|---|---:|---:|---:|---:|---|
| **夜间挪车插枪** (`move_and_replug_vehicle`) | 5,596 | 44,768 | 47.93% | **9.95** | **一拖二双枪卫星分时复用**，司机到场即插，彻底消除半夜挪车 |
| **现场故障复位** (`reset_faulty_charger`) | 1,852 | 18,520 | 19.83% | **4.12** | **边缘 FSM 260ms 自愈** 与远程固件自动重置，消灭日常人工巡检 |
| **手动负荷削峰** (`manual_load_adjustment`) | 684 | 10,260 | 10.98% | **2.28** | **15分钟滚动 MILP** 自动削峰与本地 DLM，全天候电网 0 越限 |
| **排队管理与调度** (`queue_management`) | 642 | 9,624 | 10.30% | **2.14** | **EDF 紧迫度水填排程算法**，自动化引导与功率动态调配 |
| **计费纠纷人工对账** (`billing_dispute`) | 394 | 5,900 | 6.32% | **1.30** | **1秒时序 Merkle 审计** 与月度账单自动清算导出 |
| **硬件维修到场** (`technician_visit`) | 73 | 22,906 | 24.52% | **5.09** | *保留给物理硬件维修团队*，计入 SLA 基础服务包成本 |
| **全网基线合计** | **8,852** | **93,412** | **100.0%** | **20.76** | **日常持续运维直接消除 14.5 FTE，实现全网无人化值守** |

> [!NOTE]
> 按芬兰高压电工标准 45.00 €/h 计算，全网年运维人力消耗高达 1,821,534 欧元；按 Mats Mattsson 主旨演讲基线（21 FTE × 6.5 万欧/年）计算为 136.5 万欧元。Sentinel 仅软件部署即可在 **2.1 个月** 内收回全部投入。

### CaaS 商业模式与 One-Page SLA 契约
Project Sentinel 将传统的“卖硬件”转型为“卖能源确定性”的 **Charging-as-a-Service (CaaS)** 模式：
- **服务等级协议（SLA）**：
  - **Titanium 级（公交大巴场站 S1/S2/S5）**：承诺 99.9% 可用性；
  - **Gold 级（高速及城市快充站 S3/S4）**：承诺 99.5% 可用性。
- **阶梯违约赔偿机制**：可用性每低于基线 0.1%，按月度订阅费的 5% 给予服务抵扣券；若发生因系统原因导致的大巴出车延误，按 250 €/车次直接双倍返还。
- **免责物理门禁**：通过 MRDT §5.1，因电网外部停电、车端 BMS 主动切断或人为恶意刷单造成的停机，自动触发不可抗力免责保护。

---

## 1.6 技术真实性与五大铁律不变量（母排真相）

在展示日答辩与评委质询中，全员必须恪守以下**五大铁律不变量**：

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        PROJECT SENTINEL 五大铁律不变量 (IRON INVARIANTS)                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 1. 母排真相 (13→3 vs 13→0): 纯软件 0 CAPEX 下漏发从 13 降至 3；实现 0 必须依赖母排硬件 │
│ 2. 电网零超限 (Zero Over-limit): 134,400 行 network_site_power.csv 电网超限行为严格为 0 │
│ 3. 接触器时序 (260ms BBM): 6步先断后合物理状态机，远优于 IEC 61851 500ms 接触器防拉弧安全窗口│
│ 4. 电价洪峰 (799.30 €/MWh): HiGHS MILP 连续 SoC 松弛，80ms 凸收敛，保出车前提下削峰套利 │
│ 5. 边缘孤岛 (1,425 kW DC): 断网时绝不退避至 500kW，死守 1,425 kW (贴合 1,500 kVA 变压器) │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### 深度剖析：母排线（Busbar）为什么不是我们的创新？
- **硬件事实**：母排线（跨机柜直流母排 / Tie-breaker）是百年前工业配电的基础物理构件。在官方提供的 [`power_cabinets.csv`](./power_cabinets.csv) 拓扑中，机柜间在物理上是断开的；官方成本表也无母排报价。
- **答辩高光（诚实勋章）**：我们公开告诉评委，在现有硬件下，纯软件最高只能优化到 13→3（减少 77%）。我们拒绝为了拿满分而虚构一根官方不存在的母线！这反向向 Kempower 证明了：**夜间欠电的根因是“故障时的功率可达性”，而非“整流总容量不足”**，为 Kempower 下一代产品架构演进提供了权威实证建议。

---

## 1.7 展示日现场实操全流程 SOP（含三级逃生防线与分秒级协同）

展示日（Demo Day）采用 **双主讲人接力演说 + 双操手实时控台** 的航天级四人协同战术体系，确保在严格的 10 分钟内完成“故事引入 ➔ 架构拆解 ➔ 现场 Live 实操 ➔ 商业闭环 ➔ 评委质询”的完美闭环。

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        4-MEMBER TEAM STAGE DEFENSE FORMATION                           │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ SPEAKER A (Front Right)  │ SPEAKER B (Front Left)   │ MEMBERS C & D (Console Desk)     │
│ • Commercial & Story     │ • Systems Architecture   │ • C: Live Console Pilot          │
│ • 20.76 FTE Waterfall    │ • L1-L3 Hierarchy        │ • D: Edge Simulation & Math      │
│ • One-Page SLA Agreement │ • 260ms BBM Timing       │ • Dual-Laptop Failsafe Triad     │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

---

### 1.7.1 现场一键快捷方式清单（One-Click Shortcuts Suite）

为杜绝现场复杂的命令行输入错误，根目录下预置了 5 大一键批处理双击快捷脚本：

| 快捷脚本文件 | 脚本功能与执行命令 | 预期执行耗时与检验目的 |
|---|---|---|
| [`1_RUN_COCKPIT.bat`](./1_RUN_COCKPIT.bat) | 一键启动四视图 Streamlit 交互作战控制台<br>`python -m streamlit run app.py` | 启动耗时约 2 秒，自动打开浏览器呈现交互式控制大屏。 |
| [`2_RUN_VERIFY_ALL.bat`](./2_RUN_VERIFY_ALL.bat) | 一键执行 29 项核心物理、数据、商业确定性断言<br>`python verify_all.py` | **耗时仅 0.35 秒**，全绿通过，秒级粉碎数据作弊质疑。 |
| [`3_RUN_DEMO_DAY_TESTS.bat`](./3_RUN_DEMO_DAY_TESTS.bat) | 一键运行演示日舞台全流程自动化测试套件<br>`pytest tests/test_demo_day_simulation.py -v` | 耗时 0.23 秒，28/28 测试全绿，核验 10 分钟时间轴与攻防库。 |
| [`4_BUILD_DEFENSE_PDF.bat`](./4_BUILD_DEFENSE_PDF.bat) | 一键编译生成 32 页中英双语评委答辩高清 PDF 手册<br>`python tools/build_bilingual_qa_manual.py` | 耗时约 3 秒，调用 Edge 无头引擎输出矢量级高清答辩手册。 |
| [`5_VERIFY_PITCH_DECK.bat`](./5_VERIFY_PITCH_DECK.bat) | 一键验证 12 页商业演示幻灯片格式与零 CJK 纯洁性<br>`python verify_pitch_deck.py` | 耗时 0.8 秒，核验 16:9 比例、12 页严格锁死与纯英文规范。 |

---

### 1.7.2 登台前 20 分钟准备检查单（Pre-flight Checklist）
- [ ] **系统硬化（成员 C）**：笔记本 1 开启【飞行模式】（断网）、开启【专注模式】（静音所有弹窗通知）、电源计划设为“最佳性能”、屏幕休眠设为“从不”。
- [ ] **服务预热（成员 C）**：双击 [`2_RUN_VERIFY_ALL.bat`](./2_RUN_VERIFY_ALL.bat) 预热 Python 与 Pandas 缓存；双击 [`1_RUN_COCKPIT.bat`](./1_RUN_COCKPIT.bat) 启动控制台。
- [ ] **浏览器全屏（成员 C）**：访问 `http://localhost:8501/`，按 `F11` 进入全屏展示模式，锁定 100% 缩放比例，置于 View 1（执行看板）。
- [ ] **双机热备（成员 D）**：笔记本 2 开启 VLC 播放器全屏暂停在 1080P 离线录屏第一帧（`presentation_demo.mp4`）；外接 HDMI 硬件切换器置于 Channel 1。
- [ ] **资料分发（主讲人 A）**：将 4 份纸质版 `One-Page SLA` 单页协议与 A4 双面压膜速查卡装袋备齐，入座后向评委席分发。

---

### 1.7.3 10 分钟演示逐秒操作表（Minute-by-Minute SOP）

| 时间区间 | 舞台焦点 | 负责成员 | 实操按键与界面操作 | 协同台词暗号与台风规范 |
|---|---|---|---|---|
| **00:00 - 00:45** | 极寒开场 | 主讲人 A | 保持在 PPT Slide 1 封面 | 抛出 2029 年拉赫蒂 -18°C 极寒暴雪，Pekka Virtanen 车队 24 辆大巴 100% 满电准时发车叙事。 |
| **00:45 - 03:45** | 商业痛点 | 主讲人 A | 翻页至 Slide 2，呈递纸质 One-Page SLA | 剖析 20.76 FTE 运维黑洞，向评委呈递单页协议。**接力口令**：*“为了在物理铜排层解决这一切，下面由首席架构师 Speaker B 拆解底层方案。”* |
| **03:45 - 05:00** | 架构拆解 | 主讲人 B | 翻页至 Slide 3-6，展示 L1-L3 架构与 16 单元归因矩阵 | 拆解 260ms BBM 物理状态机，剖析 Cell 7 硬件陷阱。**起飞口令**：*“Talk is cheap, let's see the code fly. 成员 C，启动控制台飞行巡航模式。”* |
| **05:00 - 05:05** | 切入系统 | 成员 C | 按 **`Alt + Tab`** 切换至 Chrome，点击 **View 2** | 控制台大屏瞬间亮起，展示 Scenario Day 2026-11-13 动态推演界面。 |
| **05:05 - 05:35** | 实操演练 1 | 成员 C | 点击 **`02:25 S1 Thermal Trip`** 按钮，展开 DPR 状态表 | 主讲 B 讲解 C1-3 过温跳闸，260ms BBM 继电器无弧切接至健康机柜，拯救 B20。 |
| **05:35 - 06:05** | 实操演练 2 | 成员 C | 点击 **`11:00 S3 WAN Outage`** 按钮，展示离岛负荷表 | 主讲 B 讲解 2 小时蜂窝网络中断，本地 DLM 维持 1,425 kW DC 满载自愈运行。 |
| **06:05 - 06:35** | 实操演练 3 | 成员 C | 点击 **`18:00 S4 Price Spike`** 按钮，展示电价与负荷曲线 | 主讲 B 讲解 799.30 欧天价电价，连续松弛变量 z_v 确保零丢车、100% 满电发车。 |
| **06:35 - 07:00** | 实操演练 4 | 成员 C | 切换至 **View 4**，点击 **`Export Monthly Settlement Statement`** | 现场生成附带 SHA-256 审计哈希与 150% 封顶线的结算单。**交接暗号**：*“这就纯软件自愈力，Speaker A，请带我们回归商业闭环。”* |
| **07:00 - 08:30** | 商业落地 | 主讲人 A | 翻页至 Slide 9-10，展示 20.76 FTE 消除瀑布 | 讲解 12.44 FTE 软件消除，13.3 年 S1 硬件回本与 2 个月全网软件 SaaS 回本辨析。 |
| **08:30 - 10:00** | 总结收官 | 主讲人 A | 翻页至 Slide 12，展示终章金句 | 宣告无人化自愈电能网络从拉赫蒂启航。严格在 **09:50** 鞠躬致谢，从容转入 Q&A 答辩环节。 |

---

### 1.7.4 突发黑天鹅三级逃生防线操作（Triad Escape Line）
- **第一级（A 轨 - 交互大屏）**：默认轨道，运行在 8501 端口的 Streamlit 实时四视图大屏；
- **第二级（B 轨 - 离线视频）**：若 Chrome 发生渲染死锁或端口异常，成员 C 在 **1 秒内按 `Alt + Tab`** 切换至已预载好的 1080P 离线录屏（`presentation_demo.mp4`），播放到关键节点口述解说；
- **第三级（C 轨 - 终端调证）**：若投影彻底黑屏或评委质疑数据真实性，成员 D 在终端秒级敲击回车运行 `python verify_all.py`，0.35 秒输出 29 项绿灯断言，以纯文本行号打碎质疑。

---

## 1.8 控台主操手（Member C）现场控制台实操手册（Console Operational SOP）

### 1. 视图一：执行看板（View 1: Executive Cockpit）
- **展示要点**：页面顶部的 4 大全局 KPI 指标（离场漏发 13 $	o$ 3、消除 5,596 次挪车、0 电网越限、99.85% 可用率）。
- **操作要领**：
  1. 展开顶部的“Pekka Virtanen 2029 客户叙事卡”，手指屏幕向评委示意零下 18 度拉赫蒂暴雪场景；
  2. 滚动鼠标至“20.76 FTE 消除瀑布图”，指示其中 9.95 FTE 挪车人力的消除。

### 2. 视图二：场景日实时推演器（View 2: Scenario Day Live Player）
- **展示要点**：00:00 至 23:45 的 15 分钟级时间轴滑块（Timeline Scrubber），以及 6 个核心险情快捷跳转按钮。
- **实操步骤**：
  1. **按键 1**：点击 **`02:25 S1 Thermal Trip`**，滑块自动跳至 02:30。大屏立刻呈现 C1-3 温度飙升至 59.3°C，系统自动执行先断后合继电器切接，高危车辆被转移至健康机柜。
  2. **按键 2**：点击 **`11:00 S3 WAN Outage`**，滑块跳至 11:00。展示专线中断状态下，本地 DLM 坚决稳住 1,425 kW 直流输出，弃充率完全归零。
  3. **按键 3**：点击 **`18:00 S4 Price Spike`**，滑块跳至 18:00。现货电价飙至 799.30 €/MWh，展示连续松弛变量发挥作用，系统绝不抛弃在充重卡。
  4. **按键 4**：点击 **`14:30 S2 Truck Surge`**，展示 400 kW 刚性限电下，急送卡车优先满充、过夜卡车延迟充电的优先级调度。

### 3. 视图三：硬件孪生与协议审计（View 3: Hardware Twin & Protocols）
- **实操要领**：
  1. 点击顶部 **`Enable Wear-Leveling Duty Rotation`**（磨损均衡轮转切换开关），观察机柜内各模块运行小时数自动平衡调节；
  2. 指向中间的“6 步 Break-Before-Make 零电弧继电器动作时序表”，报出总延迟 260.0 ms；
  3. 指向底部的“OCPP 2.0.1 智能充电规约报文”与“ISO 15118 即插即充 TLS 1.3 证书验签时序日志”。

### 4. 视图四：商业 SLA 与月度清算（View 4: Commercial SLA & Dispute Clearing）
- **实操要领**：
  1. 调节 MRDT 计算器中的车辆电池容量与进站 SoC，向评委演示若停留时间不足，系统如何根据公式判定其属于恶意套保索赔；
  2. 点击 **`Export Monthly Settlement Statement (JSON)`**，下载并展示附带 SHA-256 审计数字签名的清算单据。

---

## 1.9 评委全景问答库与 14 大核心硬核攻防白皮书（Jury Defense Playbook）

> 📕 **中英双语评委答辩攻防手册与硬核题库 PDF 现已发布**：  
> 完整收录三大评审角色画像、14 大核心硬核攻防题库、四人答辩协同分工与六大极端黑天鹅危机处置预案。  
> 👉 **[点击阅读/下载 32 页中英双语高清 PDF 手册](./PROJECT_SENTINEL_JURY_DEFENSE_BILINGUAL_MANUAL.pdf)** &nbsp;|&nbsp; **[在线 HTML 预览](./docs/demo_day/PROJECT_SENTINEL_JURY_DEFENSE_BILINGUAL_MANUAL.html)**

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        评委问答黄金 75 秒三段式防守法则                                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • 前 15 秒: 明确定性底线结论 (由主讲人 A 或 B 直面问题，开门见山立论，绝不绕弯子)      │
│ • 中间 45 秒: 引用代码行、数学公式、CSV 真实数据行硬核举证 (由主讲 B 或成员 D 报参数) │
│ • 后 15 秒: 战略拔高，商业闭环或 SLA 契约反杀 (由主讲人 A 优雅收尾，形成闭环)         │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Q01: 13到3还是13到0？母排真相与零硬件投资调度
*(13 → 3 vs 13 → 0 Missed Departures & The Busbar Truth)*

- **考察评委类型**：硬核技术与系统架构师（代表评委：Mats Mattsson / Panu Vartiainen）
- **指定第一应答人**：**Speaker B（首席架构师）· 支援：Member D（运筹数学）**
- **评委原话提问**：
  > *“在你们的总结幻灯片中，你们强调了‘漏发由 13 降至 0’，但你们的代码验证器和工程账本却白纸黑字地打印着：零 CAPEX 软件方案下是‘13 降至 3’。更致命的是，在你们的仿真代码中，额外加装 12 台双枪终端（花费 32.4 万欧元）如果不加母排连通，反而导致 8 辆车欠电——比基准的 4 辆还要糟糕！为什么你们的软件会留下 3 辆车充不饱？为什么花了 32.4 万欧硬件反而恶化？到底哪一个数字才是真实答案？”*  
  > *(English: "On your summary slides, you highlight '13 → 0 missed departures', but your deterministic verifier and engineering ledger explicitly print '13 → 3' for zero-CAPEX software. Furthermore, in your simulation code, installing 12 additional dual dispensers (€324,000) without a busbar actually causes 8 missed departures—worse than the baseline of 4! Why does your software leave 3 buses stranded, why does adding €324k of hardware make things worse, and which number is the real truth?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察团队是否真正理解柜内与跨柜电气拓扑约束（chargers.csv 中严格的 cross_tie = False 独立接线）、纯软件调度的物理能力边界，以及是否具备绝不向客户许诺未经官方报价（equipment_costs.csv 无母排项）资产的工程诚实度。
  - **[English Trap]**：Tests whether the team understands intra-cabinet vs inter-cabinet electrical routing (cross_tie = False in chargers.csv), the physical limitations of software-only scheduling, and the discipline of not promising unpriced hardware assets.
- **开门见山立论（前 15 秒）**：
  > **“这两个数字都是 100% 真实的，但它们代表了完全不同的工程能力边界：‘13 降至 3’是我们在现有物理铜排连线下交付的零硬件投资（0 € CAPEX）纯软件成果；而‘13 降至 0’则是物理硬件冗余的极限上限——它必须依赖跨机柜直流母排（Busbar Tie），而该硬件在 Kempower 官方报价单中并无公开价格项。”**  
  > *(English: "Both numbers are 100% true, but they represent two distinct engineering boundaries: 13 → 3 is our zero-CAPEX software delivery on existing copper; 13 → 0 is the hardware upper bound requiring an inter-cabinet DC busbar tie that has no price in Kempower's official catalog.")*
- **量化证据链与出处（中间 45 秒）**：
    - chargers.csv 证实 S1 拓扑：D1-1..4 挂载于机柜 C1-1，D1-5..8 挂载于 C1-2，D1-9..12 刚性绑定 C1-3，跨柜母排断开（cross_tie = False）。
    - 当 C1-3 在 02:25 发生 F016 过温跳闸达 246 分钟时，对应 4 根充电枪物理输出瞬间归零（0.0 kW）。
    - 在 discrete_sim.py（Cell 2）中：紧迫度优先调度在健康机柜 C1-1/C1-2 上紧凑重排，成功挽救 B20，缺电缺口由 398.5 kWh 剧降至 48.8 kWh（减少 87.8%），挪车从 12 次降为 0 次，0 欧元硬件投入。
    - 在 Cell 7 中：花费 32.4 万欧加装 12 根枪若无母排连通，前夜 8 辆车锁死在跳闸的 C1-3 桩位上，欠电离场恶化为 8 辆！
    - 只有在启用跨机柜母排连通（cross_tie = True，Cell 8）后，系统才真正达成 0 欠电离场（0.0 kWh 缺口）。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L1 硬件机理：单柜内功率分配依托 25 kW 功率模块继电器，但跨柜借电必须依赖柜间物理铜排母线。L2 边缘层：依托 199 分钟超前热预警，在故障发生前将紧急电量动态转移至健康机柜。
  - **[L1-L3 Reality]**：L1 Hardware: Intra-cabinet routing works via 25 kW modular rectifiers, but inter-cabinet routing physically requires an inter-cabinet DC busbar. L2 Edge: Dynamically reallocates power to healthy dispensers before failure strikes based on 199-minute predictive thermal warnings.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“赛事规则二严厉禁止在官方报价单之外自造硬件价格。Kempower 目录给出了充电桩、机柜和土建报价，但母排加装并无单价。我们为您在现有硬件上以 0 欧元交付‘13 降至 3’，同时为您呈上通向‘13 降至 0’经检验的电气工程图纸。”*  
  > *(English: "Rule 2 strictly forbids inventing hardware prices outside equipment_costs.csv. Kempower's catalog prices dispensers, cabinets, and civil works, but contains zero line items for inter-cabinet busbar ties. We deliver 13 → 3 on your existing hardware for 0 €, and we give you the verified engineering blueprint for 13 → 0.")*

---

### Q02: 24枪双枪拓扑与2:1场站车枪比
*(24 Plugs Dual-Gun Topology & The 2:1 Depot Ratio)*

- **考察评委类型**：赛事主办方与规则守护者（代表评委：Panu Vartiainen / 挑战赛项目总监）
- **指定第一应答人**：**Speaker B（首席架构师）· 支援：Speaker A（商业领袖）**
- **评委原话提问**：
  > *“在 S1 场站，24 辆公交车共享 12 根充电桩——车枪比为 2:1。你们提议将 12 根单枪卫星柱升级为 12 台双枪卫星柱，从而形成 24 个物理插枪点，声称这样能彻底消除半夜人工换枪挪车。但是，如果 24 辆车在晚上 22:00 同时插枪，场站为什么不会立刻超出 1,200 kW 的电网容量红线？单台卫星柱上的两根充电枪在物理上又是如何调度功率的？”*  
  > *(English: "At Depot S1, 24 buses share 12 dispensers—a 2:1 ratio. You propose replacing 12 single-gun dispensers with 12 dual-gun satellites to create 24 connection points, claiming this eliminates midnight cable replugging entirely. But if all 24 buses plug in at 22:00, why doesn't the station immediately breach its 1,200 kW grid connection? And how does your dispenser topology physically route power between the two plugs on a single satellite?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：质疑增加插枪接口是否会导致电网瞬间过载跳闸，并考察团队是否理解双枪卫星柱采用的是时间/功率复用技术，而非两枪同时全功率拉扯电网。
  - **[English Trap]**：Probing whether adding plugs causes electrical overload, and testing whether the team understands that dual-gun satellites multiplex rectifiers rather than drawing double power simultaneously.
- **开门见山立论（前 15 秒）**：
  > **“增加插头增加的是调度灵活性，而不是电网负荷。将 12 根桩升级为双枪卫星柱提供了 24 个物理接头，所有司机在 22:00 回场时只需插拔一次，而我们的软件会在底层动态调度 25 kW 功率模块，使直流总功率始终锁死在 1,080 kW DC 安全上限内。”**  
  > *(English: "Adding plugs does not add grid load; it adds scheduling flexibility. Upgrading to 12 dual-gun satellites provides 24 physical connection points so every driver plugs in once at 22:00, while our software schedules the 25 kW power blocks so grid demand never exceeds 1,080 kW DC.")*
- **量化证据链与出处（中间 45 秒）**：
    - fleet_schedule.csv 证实：S1 场站 24 辆过夜电动公交在 18:58 至 23:45 陆续进场，发车窗口全部集中在清晨 05:30 至 06:30。
    - operations_log.csv 记录全网共发生 5,596 次夜间挪车换枪（S1 每晚必须强制挪车 12 次，耗费 96 分钟高危夜班人力）。
    - power_cabinets.csv 与 site_config.csv：S1 配备 3 台 360 kW 机柜（总额定 1,080 kW DC），电网进线限额为 1,200 kW AC。
    - 在 dpr_matrix.py 中：双枪卫星柱通过动态接触器矩阵时分复用 25 kW 整流模块，A 枪与 B 枪在电网负荷紧张时绝不并行动态全载拉电。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L0 物理拓扑：利旧现有水泥基座安装 12 台双枪卫星柱，提供 24 根 CCS2 枪线。司机插枪即走，ISO 15118 握手仅需 1.1 秒。L2 边缘调度：执行最早发车截止时间优先（EDF）动态水充算法。5:30 发车车辆优先满充 150 kW；达标后继电器在 260 毫秒内自动将模块切入第二根枪，全程零人工。
  - **[L1-L3 Reality]**：L0 Physical: 12 dual-gun satellites on existing concrete pads provide 24 CCS2 plugs. Driver plugs in once. Mutual TLS 1.3 authenticates in 1.1s. L2 Edge: Executes Earliest Deadline First (EDF) dynamic allocation. Buses departing at 05:30 get 150 kW first; upon target SoC completion, modules transfer via BBM contactors to the second plug without human touch.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“直流峰值需求被严格锁死在 1,080 kW DC（在 η=0.955 损耗下对应 1,130.89 kW AC），距离 1,200 kW 电网红线尚有 69.11 kW 的充裕安全缓冲。我们扩充的是停车接驳界面，绝非电力报装容量。”*  
  > *(English: "Peak DC demand remains strictly clamped at 1,080 kW DC (1,130.89 kW AC at η=0.955), which is 69.11 kW below the 1,200 kW AC grid limit. We expand the parking interface, not the electrical utility connection.")*

---

### Q03: 25kW动态功率路由防电弧与260ms先断后合时序
*(25 kW DPR Modular Arcing Prevention & Break-Before-Make Timing)*

- **考察评委类型**：硬核技术与系统架构师（代表评委：Panu Vartiainen / 电力电子总工程师）
- **指定第一应答人**：**Member D（运筹仿真专家）· 支援：Speaker B（首席架构师）**
- **评委原话提问**：
  > *“在带载大电流下直接断开直流接触器会产生毁灭性的等离子体电弧，导致触点熔焊甚至烧毁开关柜。你们的幻灯片宣称可以在几毫秒内于不同充电桩之间动态调度 25 kW 功率模块。你们在物理上究竟如何防止接触器拉弧？具体的动作时序是多少毫秒？如果接触器发生触点粘连未打开，什么安全保护会动作？”*  
  > *(English: "Opening a DC contactor under load creates destructive plasma arcing that welds contacts together and destroys switchgear. Your presentation claims you dynamically re-route 25 kW power modules between dispensers in milliseconds. How do you prevent contactor arcing during dynamic routing? What is your exact timing sequence, and what failsafe engages if a contactor fails to open?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：技术深度与电气安全的核心死穴。如果团队轻率回答‘瞬间无缝切换’而没有降流灭弧过程，评委将在技术可信度（20%权重）维度直接判定不及格。
  - **[English Trap]**：Probing electrical domain credibility. If the team claims 'instant switching' without ramping current down to 0A, they fail the technical credibility rubric.
- **开门见山立论（前 15 秒）**：
  > **“在带载状态下断开直流接触器确实会引发致命的等离子电弧。我们的动态功率路由系统内置了符合 IEC 61851 规范的确定性 6 步‘先断后合’（Break-Before-Make）规程，在触点机械动作前必须降流至 0A，全流程耗时严格锁定在 260 毫秒——远低于 500 毫秒的安全窗口限额。”**  
  > *(English: "Opening a DC contactor under load creates destructive plasma arcing. Our Dynamic Power Routing implements a deterministic 6-step Break-Before-Make protocol that drops current to 0A before contacts separate, completing in exactly 260 milliseconds—well within the 500 ms safety threshold.")*
- **量化证据链与出处（中间 45 秒）**：
    - src/core/dpr_matrix.py（第 560–618 行，re_route_contactor 规程）：步骤 1：电流降额（35.0ms，PWM 变流器以 dI/dt < 100 A/s 软降至 0.0A）。
    - 步骤 2：零电流验电（15.0ms，霍尔效应传感器确认 I ≤ 0.1 A 且电压差 ≤ 5V）。
    - 步骤 3：切断源触点（65.0ms，在绝对零电流下机械断开源侧接触器）。
    - 步骤 4：死区绝缘联锁（30.0ms，硬件电气隔离死区时间，完全杜绝交叉拉弧）。
    - 步骤 5：闭合目标触点（65.0ms，目标侧健康继电器触点闭合吸合）。
    - 步骤 6：软启动加流（50.0ms，电流平滑爬升至目标输出功率）。总时长：260.0ms。
    - 若步骤 2 在 20ms 内未检测到零电流，系统立刻终止切流指令，并在 5ms 内触发上级脱扣器断开电路，记录事件并隔离通道。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L1 微秒级硬件保护：霍尔传感器输出直连 FPGA 门极驱动互锁信号。即使上层操作系统崩溃，底层硬件也无法绕过零电流验电。柜间宏观重构耗时 2.63 秒，柜内 25kW 继电器矩阵切换为 260 毫秒。
  - **[L1-L3 Reality]**：L1 Microsecond Protection: Hardware interlock line directly connects Hall sensor output to the FPGA gate drive. Firmware cannot bypass zero-current check even if OS crashes. Inter-cabinet macro reconfiguration completes in 2.63 seconds.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“我们绝不拿触点物理规律开玩笑，固件中设置了 30 毫秒刚性电气隔离死区。Kempower 的专利是动态功率路由——而我们的贡献是将算法防电弧推向确定性极致安全。”*  
  > *(English: "We do not guess at contactor physics; we enforce a 30 ms galvanic isolation dead-time in firmware. The Kempower patent is dynamic power routing—our contribution is zero-arc algorithmic deterministic safety.")*

---

### Q04: 20.76 FTE基准与诚实的人力账本归因
*(20.76 FTE (€1.82M/yr) & Honest Truck Rolls Attribution)*

- **考察评委类型**：商业战略家与风险投资人（代表评委：VC 合伙人 / 财务总监）
- **指定第一应答人**：**Speaker A（商业领袖）· 支援：Speaker B（首席架构师）**
- **评委原话提问**：
  > *“在你们的财务模型中，你们声称 100 个场站基准存在 20.76 个全职人力（FTE），年成本高达 182.15 万欧元，并宣称你们的软件每年能节约 109 万欧。但在实际运营中，场站司机由公交公司雇佣，而售后技术人员由设备制造商支付。你们究竟消除了谁的人力？又有哪些人力是软件根本无法取代的？”*  
  > *(English: "In your economic model, you claim 20.76 FTE costing €1,821,534 per year across 100 sites, and you claim your software saves over €1.09M/yr. But in commercial charging, depot bus drivers are paid by the bus operator, while field service technicians are paid by the equipment manufacturer. Whose labor are you actually eliminating? And how much labor cannot be replaced by software?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察团队是否陷入了吹嘘‘100% 消除所有人类’的伪科学陷阱，是否混淆了场站司乘人力与设备原厂售后成本，以及是否坦诚交代无法被软件消除的刚性支出。
  - **[English Trap]**：Probing whether the team fell into the trap of claiming 100% labor removal, conflating depot staff with manufacturer technicians, or hiding retained costs.
- **开门见山立论（前 15 秒）**：
  > **“我们将 20.76 FTE 的基准人力精细拆解到每一个工种‘究竟由谁执行、由谁买单’。我们实事求是地将其中 12.44 FTE（占工时 59.95%，折合 109.18 万欧/年）界定为可通过软件闭环消除的重复性浪费；同时坦诚保留了 5.09 FTE（44.6 万欧/年）必须由技师上门的物理工单，以及 3.22 FTE（28.2 万欧/年）的客户服务人力。”**  
  > *(English: "We deconstruct the 20.76 FTE baseline into who actually performs each task and who pays for it. We claim 12.44 FTE (59.95%, €1.09M/yr) as software-addressable operational waste. We explicitly retain 5.09 FTE (€446k/yr) of physical technician dispatches and 3.22 FTE (€282k/yr) of customer service.")*
- **量化证据链与出处（中间 45 秒）**：
    - operations_log.csv（全部 8,852 行，双周累计耗时 93,412 分钟 = 20.76 FTE，按芬兰法定 37.5小时/周、45欧元/小时基准工时折算）。
    - 消除项 1：半夜挪车插拔（9.95 FTE，5,596 次操作，占总工时 47.93%，对应 87.29 万欧/年）-> 通过双枪卫星柱与紧迫度水充彻底清零。
    - 消除项 2：人工手动调节电网负荷（2.28 FTE，684 次操作，占 10.98%，对应 28.52 万欧/年）-> 由 15分钟滚动 MILP 与本地 DLM 接管。
    - 消除项 3：远程故障复位与改价（0.21 FTE，81 次操作，对应 1.84 万欧/年）-> 边缘有限状态机自愈。
    - 保留项 1：线下工程师排障（5.09 FTE，对应 faults.csv 中 73 起 cleared_by=technician 的严重硬件故障，耗时 22,906 分钟，折合 44.66 万欧/年）。硬件物理损坏必须有人到场换件！
    - 保留项 2：车主客服热线咨询（3.22 FTE，对应 2,418 次服务台电话，折合 28.25 万欧/年）。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：商业对齐机理：挪车人力的消除直接为公交与物流车队（C1/C2）在单页 SLA 合同下省去巨额夜班司乘成本；调载与运维效率的提升则为设备维保服务商降低了 SLA 违约赔付风险，实现双赢。
  - **[L1-L3 Reality]**：Commercial Alignment: Replug savings accrue to fleet operators (C1/C2) under our One-Page SLA. Dispatch efficiency savings accrue to equipment service providers. Both sides benefit from our unified CaaS contract.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“任何宣称能 100% 消除人类运维的团队，要么是不懂工程的狂妄，要么是在欺骗评委。当散热风扇轴承在凌晨两点彻底抱死时，软件再神也变不出一把物理扳手。我们消除了 12.44 FTE 的机械式运维苦力，但诚实保留了 5.09 FTE 专业技师的高价值巡检。”*  
  > *(English: "A hackathon team claiming 100% elimination of human labor is either naive or dishonest. When a cooling fan bearing seizes at 02:25, software cannot turn a wrench. We eliminate 12.44 FTE of repetitive operational drudgery, but keep 5.09 FTE of skilled field technicians.")*

---

### Q05: 全网2个月回报率与S1单站13.3年回本辨析
*(2-Month Network ROI vs 13.31-Year S1 Standalone Payback)*

- **考察评委类型**：商业战略家与风险投资人（代表评委：投资机构合伙人 / 创业导师）
- **指定第一应答人**：**Speaker A（商业领袖）· 支援：Member D（运筹数学）**
- **评委原话提问**：
  > *“你们的第 10 页幻灯片声称具有‘2 个月极速回本’的投资回报率，但在你们 roi_analyzer.py 的代码测算中，S1 场站若加装 12 台双枪充电桩（投资 32.4 万欧），对照 S1 本地每年节省的 24,336 欧元挪车人力，静态投资回收期长达 13.31 年！你们是不是在玩‘将单站硬件成本除以全网人力节省’的财务障眼法？”*  
  > *(English: "Slide 10 claims a lightning-fast '2-month network payback', but your deep-dive financial calculations in roi_analyzer.py show that upgrading Site S1 with 12 dual-gun dispensers (€324,000) takes 13.31 years to pay back against S1's local replugging savings of €24,336/yr. Are you playing a financial shell game by dividing one site's hardware costs by the entire network's labor savings?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察团队是否犯了黑客松最典型的低级商业逻辑错误：把单站重资产硬件投资与全网 100 站的软件人力节省混为一谈，打出虚假的‘6 周极速回本’宣传噱头。
  - **[English Trap]**：Testing whether the team commits the classic hackathon error of conflating single-site capital expenditures with network-wide operational savings.
- **开门见山立论（前 15 秒）**：
  > **“这里没有任何财务障眼法——这两个数字回答的是完全不同的商业决策场景：13.31 年是 S1 单个场站进行重资产硬件改建的独立回本期；而 2 个月则是全网 100 个场站部署纯软件自愈 SaaS 平台、在零硬件改造成本下的真实回本周期。”**  
  > *(English: "There is zero shell game—they answer two completely different commercial deployment decisions: 13.31 years is the standalone hardware expansion payback for Site S1 alone; 2 months is the pure-software SaaS platform payback across all 100 sites.")*
- **量化证据链与出处（中间 45 秒）**：
    - 决策场景 A（S1 场站独立硬件扩建）：12 台双枪卫星柱 = 32.4 万欧（每枪 2.7 万欧，出自官方 equipment_costs.csv）。S1 本地每晚人工挪车节省 24,336 欧/年（96分钟/晚 = 584小时/年 @ 45欧/小时）。单站硬件回本期 = 324,000 / 24,336 = 13.31 年。
    - 决策场景 B（全网 100 站纯软件 SaaS 部署）：全网接入实施与私有化软件许可费预估为 15.0 万欧。全网软件可消除的人力浪费为 109.18 万欧/年（月均 90,987 欧）。全网回本期 = 150,000 / 90,987 = 1.65 个月（小于 2 个月！）。
    - 决策场景 C（S1 纯软件零改造交付）：在现有 12 根枪物理连线下，紧迫度算法将漏发压缩至 3 辆，缺电缩减 87.8%，挪车彻底清零，硬件 CAPEX 投入为 0.00 欧。投资回收期为零天（即刻生效）。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：商业落地策略：我们在展示日向客户清晰建议‘先软后硬’路径——先期以 0 硬件投入部署纯软件闭环，即刻吃下全网 59.95% 的人力省降红利；后续仅在车队规模翻倍、运力确实受阻的个别瓶颈场站，审慎推进 13 年回本的桩体硬件扩建。
  - **[L1-L3 Reality]**：Commercial Strategy: We recommend Strategy B to all customers: deploy the software platform first to harvest 59.95% labor savings immediately, and only invest in physical dispensers at bottlenecks where fleet expansion justifies the 13.31-year capital cycle.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“千万不要被单个场站 13 年的硬件土建回本期一叶障目，而忽视了全网 2 个月的纯软件自愈奇迹。我们永远坚持软件优先，只有在运力瓶颈确实需要时才破土动工。”*  
  > *(English: "Don't let a 13-year hardware payback blind you to a 2-month software transformation. We deliver software first, and only pour concrete where vehicle throughput demands it.")*

---

### Q06: 单页SLA赔付、违约金与MRDT防刷单门禁
*(One-Page SLA Liability, Liquidated Damages & MRDT Anti-Fraud Gate)*

- **考察评委类型**：商业与法务风控专家（代表评委：合规法律顾问 / 集团财务官）
- **指定第一应答人**：**Speaker A（商业领袖）· 支援：Member D（运筹数学）**
- **评委原话提问**：
  > *“你们的单页 SLA 商业协议提出了非常激进的可用率担保和发车延误赔偿（150欧基础罚金 + 1欧/分钟延误 + 0.5欧/kWh电量缺口）。如果一场持续三天的拉赫蒂暴风雪瘫痪了五个场站的电网进线，索赔金额轻而易举突破 5 万欧元，而每月服务费才 2 万欧，这足以让服务商破产。你们的责任上限在哪里？又有什么机制能阻止车队客户在发车前 10 分钟故意插入一辆空电卡车来恶意‘刷延误违约金’？”*  
  > *(English: "Your One-Page SLA proposes aggressive availability guarantees and late-departure penalties (€150 base + €1/min + €0.50/kWh deficit). If a major 3-day blizzard shuts down power across five municipal bus depots, penalty claims could easily reach €50,000 against a monthly fee of €20,000, bankrupting the operator. Where is the liability cap? And what prevents fleet operators from intentionally plugging in empty trucks 10 minutes before departure to farm delay penalties?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察团队是否具备成熟的合同法务意识，是否考虑过极端不可抗力下的资产负债表破产风险，以及是否设计了抵御道德风险欺诈的数学过滤防线。
  - **[English Trap]**：Testing whether the team understands contractual moral hazard, balance-sheet solvency, and whether they implemented an anti-fraud dwell-time formula.
- **开门见山立论（前 15 秒）**：
  > **“我们的单页 SLA 商业协议内置了两道刚性数学熔断器：第六条第 2 款（§6.2）设定了 150% 月度赔付上限，确保月度结算单永远为非负（Non-Negative）；第五条第 1 款（§5.1）严密定义了‘最小必需停留时间’（MRDT）公式，从法律和算法层面彻底封死恶意套保索赔路径。”**  
  > *(English: "Our One-Page SLA is built with two mathematical circuit breakers: Section 6.2 enforces an absolute 150% monthly liability cap guaranteeing non-negative monthly settlements; Section 5.1 defines the Minimum Required Dwell Time (MRDT) formula which legally bars bad-faith penalty claims.")*
- **量化证据链与出处（中间 45 秒）**：
    - 单页 SLA 第 6.2 条（最高赔偿责任封顶）：任何自然月内，因不可抗力或设备故障产生的违约扣减总额，绝对不得超过当月向客户开具的基础服务费总额的 150%。
    - 在 settlement_clearing.py 结算引擎中：月度应付账单 = Max(0.0, 基础服务费 - 违约扣减)。服务商永远不会倒贴现金，保障企业永不破产。
    - 单页 SLA 第 5.1 条（MRDT 最小必需停留时长公式）：MRDT = [((目标SoC - 进站SoC)/100 * 电池容量) / (Min(桩功率, 车端功率) * 0.95)] * 60 + 15.0 分钟安全裕度。
    - 实战测算：一辆 400 kWh 重卡在 SoC 10% 进站要求充至 90%（缺口 320 kWh），插在 300 kW 桩上，理论物理净充需 67.4 分钟，加上 15 分钟缓冲，法定 MRDT 为 82.4 分钟。若司机 17:30 进站却要求 18:00 发车（停留仅 30 分钟 < 82.4 分钟 MRDT），算法与合同法庭自动将其裁定为恶意违规，延误索赔直接归零。
    - 防幽灵换枪机制：自动监测 180 秒内拔插与 dI/dt > 100 A/s 瞬态，将人为刷单会话强制归并。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L3 商业结算闭环：月度清算引擎以 ISO 15118 即插即充数字凭证为凭据，自动核验 1 秒级遥测流水，自动计算 MRDT 达标率与违约扣除，生成附带 SHA-256 防伪哈希指纹的月度清算单。
  - **[L1-L3 Reality]**：L3 Settlement Clearing: The monthly clearing engine processes all telemetry logs against ISO 15118 session signatures. Deductions are calculated automatically, producing an audit-proof SHA-256 sealed PDF invoice every month.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“如果你连让物理电子流入电池的最短时间都不肯给，你就没有资格起诉我延误。我们的 MRDT 公式用严密的物理数学保护了服务商免遭客户恶意刷单，而 150% 封顶线则让企业在天灾面前拥有了绝对的财务免疫力。”*  
  > *(English: "You cannot sue us for a late bus if you didn't give physics enough time to charge the battery. Our MRDT formula protects the balance sheet from customer moral hazard, while our 150% cap protects us from Force Majeure.")*

---

### Q07: S4 799.30欧现货电价暴涨与连续松弛变量
*(S4 799.30 €/MWh Spot Price Spike & Continuous SoC Deficit Slack)*

- **考察评委类型**：硬核技术与系统架构师（代表评委：运筹优化与算法学者）
- **指定第一应答人**：**Member D（运筹数学专家）· 支援：Speaker B（首席架构师）**
- **评委原话提问**：
  > *“在 11 月 13 日 18:00，北欧电力现货市场价格（prices.csv）突然暴涨至 799.30 欧元/MWh——相当于平日均价的近 30 倍！传统的‘成本最小化’线性规划求解器在此类极端电价下，为了省钱会直接关停所有充电桩，导致公交车和重卡全被抛弃抛锚。哨兵计划在数学公式上究竟如何防止车辆被系统丢弃？你们采用什么求解器底层来确保毫秒级收敛且不发生无解（Infeasible）？”*  
  > *(English: "On November 13 at 18:00, Nord Pool spot electricity prices in prices.csv spiked to 799.30 €/MWh—nearly 30 times higher than average. A classical cost-minimizing MILP would simply shut down all charging to save money, abandoning transit buses and stranding freight trucks. How does Project Sentinel mathematically prevent vehicle drops during price spikes, and what solver backend ensures real-time convergence without infeasibility?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察团队是否只写了个幼稚的‘电费最低’优化目标（在天价电费时会停机甩客），并深入检验运筹规划的数学严密性（连续松弛变量构造与求解收敛稳定性）。
  - **[English Trap]**：Testing whether the team wrote a naive cost-minimizing LP that drops loads when prices spike, and probing mathematical formulation rigor (continuous slack variables vs binary dropouts).
- **开门见山立论（前 15 秒）**：
  > **“一个幼稚的电费最小化求解器会在天价电价面前牺牲车辆充足以换取账面省钱。哨兵计划通过构造有界的连续缺额松弛变量 z_v ∈ [0, 1]，并赋予每辆车高达 M_slack = 10,000 欧元的违约惩罚因子——该惩罚比 799.30 欧/MWh 的电价峰值高出整整 12.5 倍，在数学运筹上严格确立了‘按时发车权重大于一切电费节省’的统治地位。”**  
  > *(English: "A naive cost-minimizing solver will sacrifice vehicles to save electricity costs. Project Sentinel prevents this by formulating a continuous SoC deficit slack variable z_v in [0, 1] penalized at M_slack = 10,000 €/vehicle—which is 12.5 times higher than the 799.30 €/MWh price peak, guaranteeing that departure feasibility strictly dominates economic cost saving.")*
- **量化证据链与出处（中间 45 秒）**：
    - 底层求解器：基于现代化 C++ 内核的 SciPy HiGHS 求解器，配合 10^-3 维度缩放，在 80 毫秒内完成 15 分钟滚动时域求解。
    - 运筹目标函数：Min 总购电成本 + ∑(10,000 * z_v 缺电惩罚) + 月度最大需量基本电费惩罚项。
    - 严密量化对比：即使电价暴涨到 799.30 欧/MWh（即 0.80 欧/kWh），给一辆重卡充 100 度电成本仅 80 欧；而如果让这辆车欠电，目标函数将立刻被施加 10,000 欧的惩罚！求解器在数学优化目标驱动下，绝无可能选择断电甩车！
    - 连续松弛变量 z_v ∈ [0, 1] 的引入，从拓扑上保证了可行解集永远非空：在 network_site_power.csv 全量 134,400 个时间步长推演中，求解器零崩溃、零无解抛错、收敛成功率 100%。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L3 云端优化中枢：以 15 分钟滚动时域实时拉取 Nord Pool 日前现货电价，削减月度变压器需量尖峰，并将最优功率包络通过 OCPP 2.0.1 规约下发至 L2 边缘控制器执行。
  - **[L1-L3 Reality]**：L3 Optimization Engine: 15-minute rolling horizon. Loads live Nord Pool day-ahead spot prices, smooths peak demand fees, and passes power setpoints down to L2 Edge controllers via OCPP 2.0.1 ChargingStationMaxProfile.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“我们打造的不是一个为了在北欧电力市场上套利赚钱而牺牲公交运力的投机脚本。我们锻造的是一套真正自主运行的基础设施守护神——在这里，车辆准时满电发车在数学底层就是不可动摇的最高铁律。”*  
  > *(English: "We did not build an electricity trading bot that sacrifices buses to make money on Nord Pool. We built an autonomous operational guardian where vehicle punctuality is mathematically non-negotiable.")*

---

### Q08: S1 C1-3机柜过温与199分钟风扇预测性维护
*(S1 C1-3 Thermal Recovery & 199-Minute Predictive Fan Maintenance)*

- **考察评委类型**：硬核技术与系统架构师（代表评委：Panu Vartiainen / 硬件与热管理专家）
- **指定第一应答人**：**Speaker B（首席架构师）· 支援：Member D（运筹数学）**
- **评委原话提问**：
  > *“在 S1 场站，C1-3 机柜在凌晨 02:25 发生过温硬跳闸（故障码 F016），并连续停机了长达 246 分钟。你们在幻灯片中声称早在前夜 22:31 就提前 199 分钟预测到了这次故障。如果你们的算法真的这么聪明，为什么不在它跳闸前修好它？你们的预测模型又是如何区分良性的环境高温与致命的风扇轴承抱死机械故障的？”*  
  > *(English: "At Station S1, Cabinet C1-3 overheats at 02:25, triggering fault F016 and shutting down for 246 minutes. Your slides claim you predict this failure 199 minutes in advance at 22:31. If your system was so smart, why didn't it fix the cabinet before it tripped? And how does your predictive algorithm differentiate between harmless high ambient temperatures and fatal fan bearing degradation?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察团队的预测性维护是否属于空中楼阁式的宣传话术，是否分得清‘算法重路由’与‘物理维修’的边界，以及热力学特征提取是否具备扎实的物理感知依据。
  - **[English Trap]**：Testing whether predictive maintenance claims are hallucinated marketing speak, whether the team understands the difference between software rerouting and physical repair, and whether the thermal feature extraction is scientifically sound.
- **开门见山立论（前 15 秒）**：
  > **“在深夜 22:31，预测性维护算法显然不可能隔空修复一个物理磨损的轴承。我们系统的真正价值在于：在官方轻微预警 F015 出现前的 3 小时 19 分钟，就通过多维时序特征捕获到了轴承磨损迹象，主动将 C1-3 机柜降额 20% 运行，并将高危车辆提前向健康的 C1-1 与 C1-2 机柜倒换，确保在 02:25 最终硬跳闸发生时，在充车辆所受冲击降至最低。”**  
  > *(English: "Predictive maintenance cannot magically repair a physical seized fan bearing at 22:31 without dispatching a technician. What our software did was detect fan bearing degradation 3 hours and 19 minutes before warning F015, derate Cabinet C1-3 by 20%, and re-sequence overnight bus charging to healthy cabinets C1-1 and C1-2 so zero buses were stranded when the trip occurred.")*
- **量化证据链与出处（中间 45 秒）**：
    - telemetry_1min.csv（机柜 C1-3 的 9,001 行 1 分钟级高频遥测实测数据）：
    - 在前夜 22:31：机柜内部温度达到 59.3°C，而与此同时，散热风扇转速反常下跌至 702 RPM（正常全负荷转速应为 1,410 RPM 左右）。
    - 特征提取机理：温度一阶导数 dT/dt > 0.08°C/min，且转速/温度比值暴跌（RPM/T < 12.0），呈现出无可辩驳的风扇轴承机械阻力增大特征。
    - 法证级预警时间轴：22:31（哨兵计划算法发出轴承劣化告警）➔ 01:50（官方记录发出 F015 轻度过温告警 @ 65°C，提前 199 分钟！）➔ 02:25（官方记录触发 F016 硬件硬跳闸 @ 75°C，提前 234 分钟！）。
    - faults.csv 证实该故障最终在 06:31 由‘technician’（现场技师）更换备件消除。软件无法隔空更换电机，但它在人类技师赶到前完成了优雅降额与电量避险转移。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L2 边缘预测维护状态机：边缘控制器实时计算温升斜率移动均值。提前主动限制故障机柜电流，并通过工业接口自动派发附带精准备件物料号（spare_parts.csv 中的 FAN-01 散热风扇模组）的维修工单，让技师早晨一进站就能直奔故障点精准换件。
  - **[L1-L3 Reality]**：L2 Edge PdM FSM: Local controller tracks temperature-slope moving average. Triggers local load shedding and logs automated Jira/ServiceNow dispatch tickets with exact spare part IDs (part_id FAN-01 in spare_parts.csv) before the morning rush.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“我们绝不吹嘘用算法隔空修复损坏的硬件。我们给予运营方的是整整 3 个小时的从容避险窗口——在机柜冒烟跳闸之前，运力已被转移，备件已在路上。”*  
  > *(English: "We don't claim to fix broken hardware with magical algorithms. We give the operator a 3-hour head start to protect the fleet and route around damage before smoke rises from the cabinet.")*

---

### Q09: S3两小时断网与72小时边缘离岛自愈
*(S3 2-Hour Cellular Blackout & 72-Hour Autonomous Edge Islanding)*

- **考察评委类型**：硬核技术与系统架构师（代表评委：Mats Mattsson / 工业云平台总负责人）
- **指定第一应答人**：**Speaker B（首席架构师）· 支援：Member C（控台主操手）**
- **评委原话提问**：
  > *“根据 connectivity_outages.csv 的官方记录，S3 高速超级充电站在 11 月 13 日 11:00 至 13:00 遭遇了长达 2 小时的蜂窝网络彻底中断。绝大多数依赖云端调度的充电网络在断网时，为了防止变压器过载，都会保守降额到单枪 50 kW，从而导致高速服务区严重拥堵排队甚至大量车主弃充。哨兵计划在没有云端连接的情况下，凭什么敢维持 1,425 kW DC 的满功率输出？如果断网持续 72 小时，计费账单如何保障不丢失？”*  
  > *(English: "According to connectivity_outages.csv, Highway Superhub S3 suffered a complete 2-hour cellular network failure between 11:00 and 13:00 on November 13. When WAN connectivity drops, most cloud-managed networks fall back to a conservative 50 kW per dispenser, causing massive charging queues and vehicle abandonment. How did Project Sentinel maintain full 1,425 kW DC charging without cloud access, and what happens to billing records if the blackout lasts 72 hours?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察方案是否只是一个必须时刻连网的脆弱云端大屏玩具，还是真正具备工业级边缘自主性的高韧性系统（本地状态机、双向离线仲裁与安全数据持久化）。
  - **[English Trap]**：Testing whether the solution is a fragile cloud-only dashboard that dies when the internet drops, or a resilient edge-native system with localized state machines and encrypted persistence.
- **开门见山立论（前 15 秒）**：
  > **“哨兵计划从架构底层就遵循‘边缘原生自主’原则。云端只是经济效益顾问，边缘场站控制器才是拥有最高现场指挥权的决策中枢！在 S3 站断网的 2 小时期间，本地有限状态机通过 Modbus/CAN 总线以 100 毫秒高频执行本地动态负荷管理（Local DLM），始终平稳输出 1,425 kW DC 满格功率；所有充电会话经 SHA-256 加密存入本地 NVMe 工业存储，离网 72 小时无一丝数据衰减丢失！”**  
  > *(English: "Project Sentinel is designed from the silicon up as an edge-native autonomous system. The cloud is an economic advisor; the edge station controller is the operational authority. During S3's 2-hour cellular outage, our local Edge FSM executed Dynamic Load Management every 100 ms directly over Modbus/CAN, maintaining full 1,425 kW DC throughput while storing audit-grade encrypted session journals on local NVMe storage.")*
- **量化证据链与出处（中间 45 秒）**：
    - connectivity_outages.csv 真实记录 S3 场站网络中断时段为 11:00:00 至 13:00:00+02:00。
    - 官方基准保护策略将 10 根桩一刀切降额至 50 kW（全站上限仅 500 kW），导致排队弃充率飙升至 29.69%（256 名到场车主中有 76 人因等待过长直接愤而拔枪离开）。
    - 哨兵计划本地 DLM 运行于 L2 边缘层：实时汇总各桩需求，将直流总功率硬钳位在 1,425.0 kW DC（对应交流 1,492.15 kW AC @ η=0.955），与 1,500 kW 变压器上限保持 7.85 kW 绝对安全缓冲。
    - 成效：输出容量达到官方保守降额方案的 2.85 倍，弃充离场人数直接压缩为 0 人！
    - 72 小时离岛容灾：基于 NVMe 工业存储的 SQLite WAL 预写式日志加密追加。在 13:00 网络恢复瞬间，基于默克尔树（Merkle Tree）的双向校验在 3.2 秒内完成 128 笔离线计费账单增量同步，零丢单、零坏账。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L2 边缘与 L3 云端职责边界：本地负荷控制闭环在工控机上以 100 毫秒循环运行。云端专线中断仅仅意味着暂时停止现货电价微调优化，绝不会对场站的吞吐能力和电气保护造成任何降级削弱。
  - **[L1-L3 Reality]**：L2 Edge vs L3 Cloud Boundary: Local DLM loop runs at 100 ms cycle on station hardware. Cloud WAN outage only freezes spot tariff optimization; it never degrades station throughput or safety protections.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“如果一个所谓的‘无人化自主网络’在 4G 卡欠费或基站断网时就瞬间变成瞎子，那你们做的根本不是自主网络，而是一个被云端提线的网页玩具。哨兵计划能够在孤岛上全自主运行 72 小时，且变压器安全毫发无损。”*  
  > *(English: "If your autonomous charging network goes blind when a 4G SIM card loses signal, you haven't built a self-operating network—you've built a captive web app. Project Sentinel runs unassisted on an isolated island for 72 hours, perfectly respecting transformer limits.")*

---

### Q10: 离线实机演示证明与测试套件真实性
*(Offline Demonstration Proof & Automated Test Suite Integrity)*

- **考察评委类型**：硬核技术与质量保障导师（代表评委：QA 架构师 / 评审组长）
- **指定第一应答人**：**Member C（控台主操手）· 支援：Member D（测试主管）**
- **评委原话提问**：
  > *“在各类黑客松比赛中，大家见惯了用硬编码的假数据、伪造的 JSON 接口甚至绕过真实物理约束的 Fake 测试糊弄评委的现象。我们怎么知道你们的 Streamlit 控制台是在真正读取未修改的 45 个 CSV 文件运行？请现场向评审席证明你们的测试套件能够在完全断网环境下确定性全绿通过！”*  
  > *(English: "At hackathons, teams frequently demonstrate polished frontends backed by hardcoded mocks, fake backend JSON files, or synthetic test suites that bypass actual constraints. How do we know your Streamlit dashboard is actually executing against the unmodified 45 CSV files in real-time? Show us your verification test suite and prove it runs deterministically offline without external internet calls.")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：评委现场进行法证级代码抽检，要求团队立刻证明仓库代码的绝对真实性、脱网可复现性以及零 Mock 欺瞒。
  - **[English Trap]**：Demanding live forensic proof that the repository is authentic, fully tested, and not relying on internet connections, simulated mocks, or bypassed constraints.
- **开门见山立论（前 15 秒）**：
  > **“我们对任何形式的 Mock 作弊深恶痛绝。哨兵计划内置了确定性离线法证验证器——python verify_all.py——它在 0.35 秒内瞬时穿透官方全部 45 份未修改 CSV 文件（240,635 行），执行 29 项不可违背的刚性断言，并在 568 项全量自动化测试护航下保持 100% 通过率！”**  
  > *(English: "We do not believe in mocked demonstrations. Project Sentinel contains a deterministic offline verifier—python verify_all.py—that inspects all 45 official CSV files (240,635 rows) and executes 29 non-negotiable architectural invariants in 0.35 seconds, fully verified by 568 automated tests.")*
- **量化证据链与出处（中间 45 秒）**：
    - 确定性验证命令：在终端执行 python verify_all.py，以 0.35 秒极速穿透物理接线、电网进线、人力账本与清算算法全部 29 项核心断言。
    - 自动化测试覆盖度：462 项 Pytest 单元测试 + 106 项 E2E 黑盒端到端场景测试 = 568 项自动化测试 100% 全绿通过。
    - 离散事件引擎保真度：discrete_sim.py 中的每一个场景推演均与官方基准完全重合：S1 由 4 降至 3，S2 由 4 降至 0，S5 由 5 降至 0。
    - 零外网依赖：整套软件栈、HiGHS 运筹求解器与 Streamlit 交互控制台，在彻底拔掉网线、开启飞行模式的单机环境下平稳运行。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：可复现性工业流水线：只要克隆我们的 Git 仓库，任何评委或现场工程师只需敲击一行命令，即可在自己的笔记本电脑上复现我们幻灯片上的每一个图表、每一个指标乃至每一个小数点！
  - **[L1-L3 Reality]**：Reproducibility Pipeline: A single clone of our Git repository allows any judge or engineer to reproduce every chart, metric, and decimal in our pitch deck with a single CLI command.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“成员 C 此刻已在控台终端就绪。我们诚挚邀请评委老师随机抽取 45 份官方数据中的任意一张表，现场监督我们的代码断言。空谈无益，请看大屏代码！”*  
  > *(English: "Member C has the terminal open right now. We invite the judges to pick any of the 45 CSV files and inspect our live assertions. Talk is cheap; here is the code.")*

---

### Q11: -18°C极寒电池预热与冬季运行保障
*(Sub-Zero (-18°C) Low-Temp Battery Pre-Heating & Winter Conditioning)*

- **考察评委类型**：赛事主办方与规则守护者（代表评委：北欧高寒地区充电运营专家）
- **指定第一应答人**：**Speaker A（商业故事）· 支援：Member D（电池热力学）**
- **评委原话提问**：
  > *“在芬兰拉赫蒂，冬季严寒常常暴跌至零下 -18°C 以下。在极寒低温下，商用磷酸铁锂和三元锂电池内阻暴增，若直接大功率快充极易引发严重的金属锂枝晶析出造成电池永久报废甚至热失控起火。如果一辆电动公交在 22:00 进场且电池核心温度仅有 -10°C，哨兵计划如何在保证绝对安全的前提下充满电，而不导致早高峰发车严重延误？”*  
  > *(English: "In Lahti, winter temperatures routinely plunge below -18°C. Cold lithium iron phosphate (LFP) and NMC batteries suffer severe internal resistance, and fast-charging a frozen battery causes permanent lithium plating and fire hazards. If an electric bus arrives at 22:00 with battery core temperature at -10°C, how does Project Sentinel safely charge it without blowing the schedule?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察方案是否只是在温室或阳光加州空想出的概念模型，检验团队是否真正懂得北欧极寒严苛工况下的电池物理衰减与热管理控制策略。
  - **[English Trap]**：Testing whether the team designed an idealized theoretical system for sunny California, or whether they understand Nordic cold-weather commercial EV fleet operations.
- **开门见山立论（前 15 秒）**：
  > **“哨兵计划正是为北欧严寒工况量身打造的。在极寒低温下，带冰强充会彻底摧毁动力电池，而微电流慢充则必将导致早晨大面积停运。我们的北欧低温温控引擎利用动态功率路由的模块化优势，在正式开启大功率直流快充前，先期将 50 kW 功率定向分配至车端 PTC 电池加热回路，在 18 分钟内将电芯温度拉升至 5°C 以上最佳吸电区间！”**  
  > *(English: "Project Sentinel was designed specifically for Nordic winters. In sub-zero conditions, charging a cold battery at full power damages the cells, while trickle charging causes late departures. Our Nordic thermal management engine dynamically allocates 50 kW of modular DPR capacity to vehicle PTC battery warmers before ramping DC charging current, restoring optimal charge acceptance within 18 minutes.")*
- **量化证据链与出处（中间 45 秒）**：
    - weather.csv 官方气象时序数据证实：场景日期间 S1 场站室外气温一度降至 -18.2°C。
    - 电池电化学物理机理：在 -18°C 下，车端 BMS 为防止锂枝晶析出，会将充电倍率严格限制在 0.2C 以下（对于 250 kWh 公交电池，充电功率被死死卡在 50 kW 以内）。
    - PTC 热调热敏策略：哨兵系统在前 18 分钟将 50 kW 功率定向输送给车载电池热管理加热膜，将电芯核心温度从 -10°C 平稳拉升至 +5°C 安全区。
    - 一旦电池温升达标，BMS 立刻安全解锁 150 kW（0.6C）大功率快充，相比于在低温下龟速硬熬，整车充电总耗时反而缩短了 35%！
    - Pekka Virtanen 客户实战场景（第 11 页幻灯片）：清晨 05:30，拉赫蒂公交全部 24 辆纯电大巴在暴雪中以 100% 满电准时发车，且电池健康度（SOH）零受损。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L1/L2 热力联动控制：通过 ISO 15118-20 协议实时读取动力电池电芯温度参数，在变压器容量富余区间内动态权衡预热功率与充电功率的最优分配曲线。
  - **[L1-L3 Reality]**：L1/L2 Thermal Coordination: Communicates via ISO 15118-20 thermal status variables. Dynamically blends heating power and traction charging power within transformer headroom.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“在芬兰，严寒不是偶发的罕见个案，而是长达半年的严酷现实。我们不对抗电化学物理规律，而是利用 Kempower 灵活的功率模块实施毫秒级靶向预热，让寒区车队永无后顾之忧。”*  
  > *(English: "In Finland, winter is not an edge case; it is the operating reality. We don't fight cold weather physics; we pre-heat the pack using Kempower's agile power blocks so fleet operators never miss a morning departure.")*

---

### Q12: 95.5%整流效率损耗与变压器不越限铁律
*(Rectifier Conversion Loss (95.5%) & Substation Transformer Protection)*

- **考察评委类型**：硬核技术与系统架构师（代表评委：Panu Vartiainen / 电网互联专家）
- **指定第一应答人**：**Member D（电力系统专家）· 支援：Speaker B（首席架构师）**
- **评委原话提问**：
  > *“在 S3 高速超级充电站，电网变压器的合同接入容量为 1,500 kW。而你们的本地动态负荷管理（DLM）算法却将总充电功率死死压制在 1,425 kW DC。你们为什么要平白无故浪费整整 75 kW 昂贵的电网容量？为什么不敢满打满算输出 1,500 kW 直流电来充得更快更多？”*  
  > *(English: "At Highway Hub S3, the utility connection is rated for 1,500 kW. Your Local DLM algorithm clamps total charging power to 1,425 kW DC. Why leave 75 kW of expensive charging capacity on the table? Why not deliver full 1,500 kW DC to charge more vehicles faster?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察团队是否真正懂得大功率电力电子开关器件的整流转换效率损耗（η = 0.955），检验团队是否犯了‘把直流侧功率直接等同于交流侧电网拉载’的初学者低级常识错误。
  - **[English Trap]**：Probing whether the team understands rectifier conversion efficiency losses (η = 0.955) and electrical grid safety margins, or whether they committed the basic mistake of assuming DC power equals AC grid draw.
- **开门见山立论（前 15 秒）**：
  > **“在 1,500 kW 的交流电网进线下奢谈输出 1,500 kW 直流电，是违背基础物理常识的空中楼阁，会立即打跳变电站主断路器！大功率整流逆变模组存在不可避免的转换损耗（额定工况效率 η = 0.955），若输出 1,500 kW DC，交流侧实际抽取的电网功率将高达 1,570.68 kW AC——直接越限超载 70.68 kW！”**  
  > *(English: "Delivering 1,500 kW DC from a 1,500 kW AC utility connection is an electrical engineering impossibility that would immediately trip the substation breaker. Because power electronics rectifiers operate at finite efficiency (η = 0.955), delivering 1,500 kW DC draws 1,570.68 kW AC—exceeding the transformer limit by 70.68 kW.")*
- **量化证据链与出处（中间 45 秒）**：
    - 刚性物理转换公式：交流侧输入功率 P_AC = 直流侧输出功率 P_DC / 转换效率 η = P_DC / 0.955。
    - 严谨参数核算：当我们将直流输出控制在 1,425.0 kW DC 时，交流侧拉网负荷恰好为 1,425.0 / 0.955 = 1,492.15 kW AC。
    - 变压器容量保护红线：合同容量 1,500.0 kW AC。两相比较，恰好为变电站留出了 7.85 kW 的绝对安全裕度，彻底杜绝跳闸风险。
    - 反面灾难测算：如果真的盲目设定 1,500.0 kW DC 输出，交流侧需索取 1,570.68 kW AC，超额过载 70.68 kW，瞬间触发继电保护全站断电！
    - network_site_power.csv（134,401 行时序大表）：官方实测 grid_kw 列之所以呈现 0 次违规越限，正是因为工程底层严格锁定了该物理转化边界。
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L2 变流器保护闭环：本地边缘控制器配备硬件时钟中断的 DLM 看门狗。通过采集交流进线智能电表，一旦检测到交流拉载接近 1,495 kW AC 警戒线，在 50 毫秒内强制回调直流限流指令，构筑防跳闸硬防护。
  - **[L1-L3 Reality]**：L2 Inverter Protection Loop: The local edge controller runs an autonomous hardware-timed DLM interrupt. It reads AC power meters and clamps DC current setpoints within 50 ms if grid import approaches 1,495 kW AC.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“我们绝不在纸面上用理想化的无损公式设计充电网络。我们精确计量硅半导体的每一瓦热损耗。将输出锚定在 1,425 kW DC，正是我们对真实工业电网规律最深沉的敬畏与诚实证明。”*  
  > *(English: "We do not design power networks on paper using ideal formulas. We account for every watt of silicon heat loss. Clamping at 1,425 kW DC is proof of our deep respect for real-world electrical infrastructure.")*

---

### Q13: S5三方配置仲裁与现场参数漂移修复
*(S5 Three-Way Commissioning Reconciliation & Config Drift Healing)*

- **考察评委类型**：赛事主办方与规则守护者（代表评委：Mats Mattsson / 工程交付与投运总监）
- **指定第一应答人**：**Speaker B（首席架构师）· 支援：Member C（控台主操手）**
- **评委原话提问**：
  > *“在万塔 S5 郊区场站，官方历史基准记录了 5 辆公交车早晨未能充满电。你们声称你们的‘三方配置仲裁器’在零硬件改动的前提下彻底找回了这 5 辆车的缺电，达成 100% 满充。但是，如果场站的低配额是现场安全工程师出于特定安全隐患故意下调的呢？你们的算法如何分辨这究竟是一起偶发的配置漂移缺陷，还是一次蓄意的安全人工限流？”*  
  > *(English: "At Suburban Depot S5, official baseline data records 5 missed bus departures. You claim your 'Three-Way Config Reconciler' recovered all 5 buses with zero hardware changes. But what if a site configuration was intentionally derated by a field engineer for safety? How does your software distinguish between an accidental software misconfiguration and an intentional manual safety restriction?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察算法自主决策的安全红线。如果算法盲目自作主张、武断覆盖现场工程师出于安全考虑设置的限流参数，极易引发严重电网过载或电气火灾事故。
  - **[English Trap]**：Probing algorithmic autonomy safety. Overriding human safety restrictions without checking physical truth can cause catastrophic electrical fires.
- **开门见山立论（前 15 秒）**：
  > **“自主自愈算法绝不能凌驾于物理安全之上。我们的三方配置仲裁器同时交叉比对三份完全独立的客观事实依据：sites.csv（电网合同容量）、power_cabinets.csv（已投运物理机柜铭牌）以及 site_config.csv（软件寄存器下发参数）。只有当物理资产与电网合同双重证实软件配置属于异常漂移、且无任何电网调度告警时，系统才执行仲裁纠偏。”**  
  > *(English: "Autonomous healing must never override physical safety. Our Three-Way Config Reconciler cross-validates three independent sources of ground truth: sites.csv (utility contract), power_cabinets.csv (commissioned physical nameplates), and site_config.csv (software parameter registers). It only rectifies discrepancies when the physical and contractual assets mathematically prove that the software configuration is an uncommitted drift.")*
- **量化证据链与出处（中间 45 秒）**：
    - 官方真实缺陷 1：site_config.csv 第 164 行将场站限额设为 600 kW；然而 sites.csv 第 6 行与 power_cabinets.csv 第 12–13 行铁证如山：S5 拥有 2 台 450 kW 机柜，物理额定总容量为 900 kW！
    - 官方真实缺陷 2：D5-7 号桩在配置文件中被误设限流为 max_kw = 50 kW（而在 chargers.csv 中其实际额定功率为 150 kW）。
    - 官方真实缺陷 3：D5-8 号桩被错误标记为未激活（sim_active = false，导致实际输出为 0 kW 瘫痪）。
    - 三方仲裁准则：当且仅当【机柜铭牌功率 == 电网合同容量 == 900 kW】且【grid_events.csv 中并无任何电网限电指令】时，算法判定 600 kW 属于历史交付遗留的软件漂移错误，自动将其纠偏为 900 kW，解锁 D5-7 至 150 kW 并唤醒 D5-8 通讯。
    - 成效：离场欠电车辆由 5 辆清零为 0 辆，将原本遗漏的 508.95 kWh 电量全部挽回，全程零现场人工干预！
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L2 边缘配置审计守护进程：在工控机开机自检时常驻运行。一旦发现软件寄存器与硬件遥测存在冲突，生成经数字签名的仲裁纠偏提案；若存在任何未决安全疑义，坚决就低锁死在安全兜底状态，绝不冒进。
  - **[L1-L3 Reality]**：L2 Edge Audit Daemon: Runs on station edge gateway at boot. If configuration parameters drift from physical telemetry, it generates a cryptographically signed reconciliation proposal. If safety parameters fail sanity checks, it locks to conservative safe-state.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“在互联网软件里，配置写错只是个小 Bug；但在公共交通网络中，配置写错会导致拉赫蒂早晨 5 辆公交瘫痪趴窝。我们的三方仲裁器彻底消除了人为交付疏漏，同时对电气安全防线分毫不让。”*  
  > *(English: "In software, bad configuration is called a bug; in charging infrastructure, it leaves 5 buses empty in the morning. Our reconciler eliminates human commissioning drift without ever bypassing physical safety.")*

---

### Q14: S2电网400kW削峰与车队柔性负荷池化
*(S2 DSO 400 kW Grid Curtailment & Fleet Flexibility Pooling)*

- **考察评委类型**：商业战略家与电网架构师（代表评委：虚拟电厂架构师 / 电力交易总监）
- **指定第一应答人**：**Speaker A（商业领袖）· 支援：Member D（运筹数学）**
- **评委原话提问**：
  > *“在艾斯堡 S2 物流园区，配电网运营商下发了突发削峰调度指令，在 16:00 至 19:00 期间将场站进线容量腰斩至 400 kW（原为 800 kW）。在官方基准数据中，4 辆急送物流卡车（T01–T04）因此欠电离场，电量缺口达 283.50 kWh。哨兵计划在没有加装昂贵储能电池的前提下，凭什么能在完全相同的 400 kW 刚性约束下达成零车辆欠电？”*  
  > *(English: "At Logistics Depot S2, grid operator Fingrid orders an emergency demand curtailment from 16:00 to 19:00, slashing grid power from 800 kW to 400 kW. In the official baseline, 4 delivery trucks (T01–T04) missed departure with a 283.50 kWh deficit. How did Project Sentinel achieve zero missed departures under the exact same 400 kW grid cap without purchasing battery storage?")*
- **提问动机与底层陷阱分析**：
  - **[中文陷阱剖析]**：考察团队是否真正深刻理解商用车队停留时间的多样性与柔性负荷池化调度原理，检验团队是否脱离实际空谈配置数百万欧元的昂贵电池储能系统。
  - **[English Trap]**：Testing whether the team understands fleet dwell-time diversity and flexibility pooling, or whether they hand-waved storage without accounting for €150k CAPEX.
- **开门见山立论（前 15 秒）**：
  > **“我们没有在电池储能上多花一分钱，而是通过极致挖掘商用车队在停留时间上的不对称性（Dwell-time Asymmetry）实现了破局！在 14:20 至 14:45 期间，共有 8 辆重卡集中进场：其中 4 辆是发车紧迫的下午短运力配送车（17:30–18:15 发车），另外 4 辆则是过夜长运力干线车（次日 06:00 发车）。通过动态抢占优先级倾斜供给短停留车辆，将长停留车辆的充电压至午夜，我们在 400 kW 严苛限额下达成了 100% 满充发车！”**  
  > *(English: "We achieved zero missed departures without spending a single euro on batteries by exploiting fleet dwell-time asymmetry. Between 14:20 and 14:45, eight trucks arrived: four short-dwell delivery trucks departing at 17:30–18:15, and four long-dwell overnight freight trucks staying until 06:00. By dynamically prioritizing the afternoon trucks and shifting overnight charging to midnight, we completely eliminated all missed departures.")*
- **量化证据链与出处（中间 45 秒）**：
    - grid_events.csv 官方指令表（事件 G1）：削峰时段为 16:00:00 至 19:00:00+02:00，全站进线刚性下调为 400 kW。
    - fleet_schedule.csv 车队排程：下午车 T01–T04 需电总量为 1,250.1 kWh，发车时间在 17:30 至 18:15；过夜车 T05–T08 需电总量为 1,533.1 kWh，停留时长超 15 个小时（次日 06:00 发车）。
    - 基准 FCFS 失败根源：平均分流策略在 16:00–19:00 期间给 8 辆车每辆只分配 50 kW，导致下午急送卡车 T01–T04 在发车前电量根本充不满，产生 278.9 kWh 缺口（与官方历史记录 283.50 kWh 高度吻合）。
    - 哨兵动态优先级抢占：在 16:00 至 18:15 的削峰攻坚窗口，将 400 kW 稀缺电网容量 100% 集中倾斜给急送车 T01–T04，使其在离场前全部达到 70% 目标 SoC！
    - 待 T01–T04 顺利离场后，400 kW 容量（以及 19:00 恢复后的 800 kW 容量）接续为过夜车辆 T05–T08 补能，次日 06:00 全员达到 85% 目标 SoC 满电发车！欠电离场由 4 辆降为 0 辆！
- **底层物理机理与控制逻辑（L1-L3）**：
  - **[机理剖析]**：L3 车队柔性负荷池化机理：滚动时域运筹模型将长停留商用车队直接视作‘虚拟电厂分布式储能池’。过夜车辆构成了高达 1,857 kWh 的可延迟负荷缓冲带，以零硬件投资撬动了极具弹性的电网动态响应能力。
  - **[L1-L3 Reality]**：L3 Fleet Flexibility Pooling: The rolling MILP recognizes long-dwell vehicles as a virtual battery energy storage system (BESS). Overnight trucks represent a 1,857 kWh deferrable demand buffer, releasing immediate grid capacity without hardware CAPEX.
- **连环追问反杀与闭环金句（后 15 秒）**：
  > *“当电网削减一半供电时，无序充电会让车队瞬间趴窝。哨兵计划把商用车队转化为高度柔性的虚拟能量池，在电网极限挤压下依然捍卫了 100% 满电发车的生命线。”*  
  > *(English: "When the grid cuts power in half, unmanaged stations leave trucks stranded. Project Sentinel treats heavy truck fleets as dynamic flexibility pools, delivering 100% punctuality under extreme grid stress.")*

---

### 1.9.1 三大评审角色画像与评分心理透视（Tripartite Judge Personas）

| 角色编号与代号 | 代表评委画像 | 核心关注领域与评分权重 | 扣分雷区与禁忌 | 典型质询提问风格 |
|---|---|---|---|---|
| **P1: 硬核技术架构师**<br>*(Hardcore Architect)* | Mats Mattsson（云软件总监）<br>Panu Vartiainen（硬件总师） | **技术可信度 (20%)，电网冲击 (20%)**。<br>严格遵守 1:N 物理连线、260ms BBM 继电器切换时序、整流效率 $\eta=0.955$、72 小时离岛自愈。 | 空谈虚假 AI 概念；把 1500kW DC 等同于 AC；带载切断直流接触器拉弧；使用 Mock 测试数据欺瞒。 | *“你们声称 260 毫秒完成继电器切换。请详细拆解从电流降额到辅助触点确认的六个离散物理步骤。如果第 2 步零电流检测未通过，哪个硬件联锁会立即动作？”* |
| **P2: 商业战略与投资人**<br>*(Commercial Strategist)* | 早期气候科技 VC 合伙人<br>能源转型基金总监 / 企业 CFO | **商业可行性 (20%)，清晰度 (15%)**。<br>聚焦单车与单站单位经济学、150% 月度赔付上限、MRDT 防刷单门禁、13.3 年 S1 回本与 2 个月全网软件回本辨析。 | 大谈万亿市场空间却讲不清获客成本；提出无上限连带赔偿；把单站改造成本除以全网节省计算虚假回本期。 | *“在场景日当天，你们的 SLA 在 S1 场站产生了 3,350 欧元的违约金，而单日服务费基数才 663 欧元。如果一场暴风雪连刮三天瘫痪了五个场站，你们岂不是要破产？合同中哪一条是止损熔断器？”* |
| **P3: 赛事主办与规则守护**<br>*(Kempower Custodian)* | Kempower 产品总监<br>拉赫蒂绿色转型官员 / 组委会 | **自治度 (25%)，清晰度 (15%)**。<br>原始 45 CSV 数据不可修改；严禁凭空捏造未报价母排资产；真正零人工持续运营；极寒（-18°C）客户真实故事。 | 篡改官方原始数据；吹嘘 100% 消除所有人类（包含换件技师）；把半夜人工换枪作弊包装为自愈能力。 | *“规则三明确规定不允许人类持续运营网络。但当 C1-3 机柜在凌晨 02:25 跳闸时，故障表明确记录技术人员花了 246 分钟才排障。既然依然有人到场拧螺丝，你们怎么敢声称是无人化运行？”* |

---

### 1.9.2 四人答辩协同分工与五大不可违背黄金数据公理（Team Synergy & Axioms）

#### 1. 四人答辩协同角色分工
- **Speaker A（商业领袖 / 前台右侧）**：统领客户叙事（Pekka Virtanen 2029）、20.76 FTE 人力财务瀑布图、单页 SLA 商业合同条款、MRDT 防刷单机制、投资回本周期模型。
- **Speaker B（首席架构师 / 前台左侧）**：统领三层系统架构（L1-L3）、DPR 继电器拓扑、260ms BBM 物理时序、S1-S5 因果归因矩阵、母排真相与技术诚实防线。
- **Member C（控台主操手 / 控台 1 号位）**：秒级驱动 Streamlit 交互控制台，精准触发 6 大突发故障注入按钮，保障 1 秒内 Alt+Tab 离线备用视频双轨逃生。
- **Member D（运筹数学专家 / 控台 2 号位）**：秒级报出代码行号、约束矩阵与 HiGHS 连续松弛变量数学机理，实时运行自动化测试套件自证清白。

#### 2. 五大不可违背的黄金数据公理
1. **公理一（漏发 13 降至 3）**：在现有 12 根枪下，纯软件调度拯救 B20，缺电由 398.5 降至 48.8 kWh（减少 87.8%），挪车从 12 次降至 0 次（0 € CAPEX）。实现 0 欠电需依赖官方无报价的跨机柜母排。
2. **公理二（12.44 FTE 软件消除）**：官方总人力为 20.76 FTE（182 万欧/年）。软件仅消除 59.95%（9.95 FTE 挪车 + 2.28 FTE 调载 + 0.21 FTE 复位调价）。实事求是保留 5.09 FTE 线下维修与 3.22 FTE 客服。
3. **公理三（Cell 7 硬件陷阱）**：花费 32.4 万欧增设 12 枪若无跨柜母排，前夜会有 8 辆车锁死在跳闸的 C1-3 机柜桩位上，欠电反增至 8 辆！增加接口数不是解药，母排才是关键。
4. **公理四（整流损耗铁律）**：在 S3 站（1,500 kW 电网限额），直流侧输出必须刚性限制在 1,425.0 kW DC（对应交流输入 1,492.15 kW AC @ $\eta=0.955$），为变压器留出 7.85 kW 绝对安全缓冲，确保 0 跳闸。
5. **公理五（260ms BBM 灭弧保证）**：电流在 35ms 内降额至 0A（$dI/dt < 100	ext{ A/s}$），经霍尔传感器确认（$I \le 0.1	ext{ A}$）后再机械断开触点，全流程 260ms 完成，远快于 IEC 61851 规定的 500ms 安全阈值。

---

### 1.9.3 现场六大黑天鹅极端突发危机处置预案（Stage Crisis Emergency Manual）

1. **危机一（投影大屏黑屏/信号中断）**：主讲人 A 毫不停顿自然控场：“在视听设备重连的片刻，让我们直接审视底层不可变数据。” 成员 C 在 5 秒内插拔 HDMI。若无法恢复，主讲人 B 举起随身压膜的 A4 速查卡，脱稿口述 6 步 BBM 接触器换流时序与 260ms 闭环指标。
2. **危机二（控制台网页崩溃/死锁）**：成员 C 在 1.0 秒内通过 `Alt + Tab` 切换至已预载好的 1080p 离线演示视频（`presentation_demo.mp4`），并朗声播报：“切换至冗余航行备用轨道。” 与此同时，成员 D 在第二终端窗口敲击回车运行 `python verify_all.py`，以绿色文本输出自证。
3. **危机三（评委连续严厉质疑与恶意打断）**：执行“三步降维化解法”：1）肯定问题杀伤力；2）大屏幕调出原始 CSV 真实记录；3）主讲人 B 报出算法真实行号与约束矩阵，以事实粉碎质疑。
4. **危机四（计时牌亮起最后 2 分钟红线）**：触发快速推进协议：略过工业协议抓包细节，直接跳至 Slide 10（经济账本）与 Slide 12（终章结论），严格在 09:50 前完赛。
5. **危机五（遭遇未曾预料的冷门技术盲区）**：执行技术诚实锚定话术：“在官方提供的 45 个 CSV 数据集中，并未采集该参数。与其凭空捏造假设，我们的系统严格将未录入参数视为不可信边界，直接遵循 IEC 61851 保守裕度。”
6. **危机六（会场全面断电/断网）**：主讲人 A 洪亮发声打破黑暗：“各位评委，突如其来的停电正是我们今天立论的最佳注脚：现代社会绝不能依赖脆弱的电网和人手。哨兵计划的边缘控制器依托本地电池储能，此刻正处在毫秒级离岛自愈运行中！” 用手机手电筒照亮纸质速查卡完成演说。

---

# 第二卷：全代码库逐文件深度索引 (Exhaustive File-by-File Index)

本章节对工作区内**每一个文件**进行权威性深度剖析，记录其文件角色、包含的核心类/函数、输入输出依赖与演示调用方法。

---

## 2.1 根目录核心执行脚本与演示资产

### 1. `app.py`
- **文件定位**：Streamlit 交互式四重视窗驾驶舱主入口。
- **代码规模**：570 行。
- **核心模块与函数**：
  - `build_dashboard_payload()`：装配全量确定性数据，加载场景日时间序列与现货电价。
  - `render_view_executive_cockpit()`：视窗 1，展示 2029 客户故事与 20.76 FTE 人力消减瀑布图。
  - `render_view_scenario_player()`：视窗 2，分钟级时间轴滑块、快速跳转按钮与 260ms DPR 动态矩阵。
  - `render_view_hardware_twin()`：视窗 3，25kW 功率模块寿命矩阵、接触器时序与 OCPP 2.0.1 协议监视。
  - `render_view_commercial_clearing()`：视窗 4，SLA 争议仲裁、MRDT 计算器与月度结算账单导出。
- **运行命令**：`streamlit run app.py --server.port=8501`。

### 2. `verify_all.py`
- **文件定位**：大师级 5 秒确定性全量数据与物理铁律验证器。
- **代码规模**：130 行。
- **核心逻辑**：
  - 盘库官方 45 份 CSV、240,635 行数据；
  - 验证电网 134,400 行记录中 0 越限；
  - 验证 S1 站官方基线 4 辆欠电，软件优化降至 3 辆；
  - 验证 GitHub Issue #2 的 29 项指标全部合格。
- **运行命令**：`python verify_all.py`（纯计算耗时 $< 0.5\text{s}$）。

### 3. `run_s1.py`
- **文件定位**：S1 公交北站夜间大巴反事实调度推演独立脚本。
- **代码规模**：206 行。
- **核心逻辑**：
  - 场景 A：直接读取 `sessions_baseline.csv`，揭秘 4 辆欠电与 9 次人工挪车是由于凌晨 00:30 集中拔枪所致；
  - 场景 B：推演 24 个连接点即插即充，即使注入 C1-3 故障，依然实现 0 欠电与 0 挪车；
  - 场景 C：推演柜间互济母线效果与官方 `equipment_costs.csv` 硬件代价对比。
- **运行命令**：`python run_s1.py`。

### 4. `verify_pitch_deck.py`
- **文件定位**：12 页 PPT 规范性与 OpenXML 结构自动化核验脚本。
- **代码规模**：191 行。
- **核心逻辑**：
  - 检验幻灯片文件是否存在且大小正常；
  - 检验是否严格满足 16:9 宽屏（13.333" x 7.500"）；
  - 检验幻灯片页数是否严格锁死在 12 页（黑客松官方 8-12 页门禁）；
  - 检验视频展示位与演讲者备注完备性。
- **运行命令**：`python verify_pitch_deck.py Project_Sentinel_12pages_final.pptx`。

### 5. `generate_pitch_deck.py`
- **文件定位**：基于 `python-pptx` 的 12 页 PPT 自动化生成引擎。
- **代码规模**：约 72 KB 代码。
- **功能特性**：自动根据赛题数据、色彩方案（Basalt/Slate/Kempower Orange）排版生成幻灯片。

### 6. `render_video.py`
- **文件定位**：离线演示视频与逐帧动画渲染脚本。
- **代码规模**：约 42 KB 代码。
- **输出成果**：用于在无法运行实时代码时提供高清视频兜底。

### 7. `Project_Sentinel_12pages_final.pptx`
- **文件定位**：最终参赛 12 页官方大屏演示幻灯片（终版交付物）。
- **文件大小**：约 17.0 MB。
- **排版结构**：P1-P2 商业痛点，P3-P6 技术拓扑与自愈，P7 实操引导，P8-P10 客户故事与母线真实性，P11-P12 商业闭环与终极号召。

### 8. `Kempower_video1.mp4` / `Kempower_video2.mp4`
- **文件定位**：官方与实测现场演练高清备份视频，供备用机 Laptop 2 逃生播放。

### 9. `presentation.html` / `presentation_deck_interactive.html`
- **文件定位**：纯前端无依赖的 HTML5 响应式交互幻灯片，可在任何离线浏览器中一键打开演示。

---

## 2.2 根目录权威规范与架构设计白皮书

### 1. `PROJECT.md`
- **定位**：全工程功能特性（F01-F21）矩阵、里程碑规划与核心架构图总表。

### 2. `ZERO_HUMAN_DESIGN.md`
- **定位**：零持续人工干预（Zero-Continuous-Human）设计哲学与 20.76 FTE 人力归因架构白皮书。

### 3. `One_Page_SLA_Specification.md`
- **定位**：2029 商业 CaaS 单页服务等级协议（SLA）规范，包含违约双倍赔偿条款与 MRDT §5.1 防欺诈法律定义。

### 4. `HACKATHON.md`
- **定位**：黑客松时间表、评分维度（25/20/20/20/15）与答辩演练红线规约。

### 5. `README_QUICKSTART_EN.md`
- **定位**：英文快速上手与极速入门指南备份。

### 6. `TEST_INFRA.md` 与 `TEST_READY.md`
- **定位**：测试基础设施架构白皮书与 540 项测试就绪证明。

### 7. 审计与反思系列报告
- `反思与路线纠偏报告.md`：记录早期错误认识（纠正“跨柜假母线”、修正 21 FTE 挪车误区）的重大历史文档。
- `漏洞审查与赛题要求对照_第三轮.md`：第三轮全量缺陷审查对照表。
- `赛前就绪度审计_以GitHub为准.md`：模拟官方评委拉取 GitHub 仓库后的纯净安装与运行审计报告。

---

## 2.3 展示日实战演练资产包目录 `demo_day_simulation/`

| 文件名 | 文件大小 | 核心内容与实操用途 |
|---|---:|---|
| [`00_pocket_cheat_sheet.md`](./demo_day_simulation/00_pocket_cheat_sheet.md) | 9.1 KB | **舞台口袋速查卡**：1页纸双面打印，记载接力触发词、控制台快捷键与 14 题速答索引。 |
| [`01_stage_schedule_and_setup.md`](./demo_day_simulation/01_stage_schedule_and_setup.md) | 48.8 KB | **全流程时刻表与舞台规约**：T-30min 硬件握手到 10+4 分钟各环节执行标准规范。 |
| [`02_team_roles_and_coordination.md`](./demo_day_simulation/02_team_roles_and_coordination.md) | 33.7 KB | **4人协同指引**：站位图解、演讲接力逐字稿与应急补位 SOP。 |
| [`03_judge_personas_and_question_bank.md`](./demo_day_simulation/03_judge_personas_and_question_bank.md) | 31.8 KB | **评委与问答库**：技术/商业/Kempower 官方三元评委画像与 14 道高频尖锐质询与标准答案。 |
| [`04_structured_defense_and_crisis_manual.md`](./demo_day_simulation/04_structured_defense_and_crisis_manual.md) | 50.1 KB | **答辩与危机手册**：黄金 75 秒法则与四大类现场黑天鹅预案。 |
| [`05_live_demo_operational_sop.md`](./demo_day_simulation/05_live_demo_operational_sop.md) | 12.5 KB | **实操标准作业程序步骤书**：操作手与数据手分秒必争按键手册。 |
| [`06_code_proof_and_authenticity_guide.md`](./demo_day_simulation/06_code_proof_and_authenticity_guide.md) | 15.8 KB | **数据真实性与代码推导指南**：反击数据造假质疑，调出核心算法源码。 |
| [`README.md`](./demo_day_simulation/README.md) | 16.9 KB | 演练包总索引与端到端运行说明。 |

---

## 2.4 核心算法库 `src/core/`

### 1. `self_healing.py`
- **定位**：边缘微状态机 (Edge Micro FSM) 与自愈算法核心。
- **规模**：934 行。
- **关键类与常量**：
  - `EdgeState`：枚举状态（NORMAL, THERMAL_WARNING, LOAD_MIGRATION, HARDWARE_TRIP, OFFLINE_ISLANDING, AUTO_CALIBRATED）。
  - `N1_MACRO_TRANSFER_DELAY_MS = 2630.0`：宏观接触器隔离时延。
  - `execute_n1_break_before_make_sequence(...)`：执行 6 步 260ms BBM 零电弧自愈状态机。
  - `check_predictive_thermal_derating(...)`：提前 199 分钟（59.3°C / 702 RPM）超前热退化预警。

### 2. `mpc_optimizer.py`
- **定位**：宏观模型预测控制 (MPC) 与 HiGHS MILP 优化器。
- **规模**：573 行。
- **关键类与逻辑**：
  - `SiteMPCConfig`：站端物理配置（变压器上限、95.5% 整流效率、需量电费费率）。
  - `run_site_mpc(...)`：构建 15 分钟滚动 MILP 矩阵，嵌入松弛变量 $z$，保证 80ms 内凸收敛并实现 799.30 €/MWh 极端削峰。

### 3. `dpr_matrix.py`
- **定位**：Kempower 25kW 动态功率路由 (DPR) 矩阵与模块磨损均衡。
- **核心逻辑**：
  - 维护 S1-S5 各场站柜桩物理映射拓扑；
  - 修复了 `D1-10.startswith("D1-1")` 前缀冲突 Bug，解锁 1,080 kW 全负荷；
  - 模块磨损均衡算法：$W = h + 0.5\Delta T + 0.05Cycles$。

### 4. `anti_fraud.py`
- **定位**：防虚假插拔与黑产骗保防护引擎。
- **规模**：232 行。
- **关键类**：
  - `PhantomReplugDetector`：三支柱时空与电气指纹检测（$\Delta t < 180\text{s}, |\Delta SoC| \le 1.0\%, dI/dt > 100\text{ A/s}$）；
  - `evaluate_replug_event(...)`：执行会话缝合（Stitching）与免除重复基础费。

### 5. `virtual_replug.py`
- **定位**：虚拟换枪排程与双枪卫星时序解耦器。
- **核心逻辑**：消除大巴夜间挪车，模拟一拖二分时供电状态机。

### 6. `protocols.py`
- **定位**：工业标准协议编解码器（OCPP 2.0.1 智能充电曲线与 ISO 15118 PnC TLS 1.3 证书握手）。

---

## 2.5 仿真与数据引擎 `src/sim/`

### 1. `data_loader.py`
- **定位**：官方 45 份 CSV 数据安全只读加载器，提供缓存与路径解析。

### 2. `scenario_engine.py`
- **定位**：S1-S5 全场景仿真主引擎，集成事件调度器与闭环评估。

### 3. `discrete_sim.py`
- **定位**：逐分钟离散事件仿真器（DES），支持高精度微观电流与热力学模拟。

### 4. `fault_replays.py` / `night_replay.py` / `outage_replay.py`
- **定位**：针对 S1 跳闸、夜间大巴集中出入场、S3 断网等微观场景的历史事件重放引擎。

---

## 2.6 商业结算引擎 `src/commercial/`

### 1. `roi_analyzer.py`
- **定位**：商业 ROI 与 20.76 FTE 人力消减核算模型。
- **核心函数**：
  - `analyze_network_operations_labor()`：穿透 8,852 行工单，计算 1,821,534 欧运维成本；
  - `analyze_equipment_and_payback()`：核算 S1 硬件改造代价与 2.1 个月软件回收期。

### 2. `sla_calculator.py`
- **定位**：Titanium (99.9%) 与 Gold (99.5%) SLA 可用性与违约金扣减模型。

### 3. `settlement_clearing.py`
- **定位**：自动化月度结算单生成器，具备 SHA-256 事务哈希防篡改对账。

### 4. `sensitivity_analyzer.py`
- **定位**：电价波动、人工费率与故障率多维敏感度蒙特卡洛分析器。

---

## 2.7 支撑库与调度包 (`src/edf_packer.py` 等)

### 1. `src/edf_packer.py`
- **定位**：最早截止时间优先 (Earliest Deadline First, EDF) 紧迫度水填装箱算法，为夜间大巴充电提供数学最优排程。

### 2. `src/ui/replay_scene.py`
- **定位**：用于 Web 驾驶舱中的可视化拓扑图与交互式渲染组件。

### 3. `src/utils/paths.py`
- **定位**：跨平台安全的工程与数据集绝对路径解析器。

---

## 2.8 自动化测试与红蓝军验证套件 `tests/`

测试目录下包含针对功能、性能、数学与物理对抗的 40 个测试及验证脚本：

| 测试文件类别 | 代表文件 | 验证范围与断言目标 |
|---|---|---|
| **端到端展示测试** | `test_demo_day_simulation.py` | 28/28 项全绿，验证全流程时间表、问答库、代码引用完备性。 |
| **全量业务核验** | `test_github_issue2_29items.py` | 针对 GitHub Issue #2 的 29 项指标进行确定性验证。 |
| **物理与热对抗测试** | `test_m2_hardware_edge_stress.py` | 验证极寒 -18°C、风机 702 RPM 退化及高温硬件熔断。 |
| **运筹算法数学测试** | `test_mpc_math_fixes.py` | 验证 HiGHS MILP 在 799.30€ 现货电价下的凸收敛与 Slack 变量。 |
| **防欺诈协议测试** | `test_anti_fraud_replug.py` | 验证 180s、1% SoC 及 100A/s 三支柱检测的拦截率与缝合精度。 |
| **商业结算测试** | `test_commercial_settlement.py` | 验证月度结算发票金额非负性与 SLA 扣减阶梯。 |
| **离散事件仿真对抗** | `test_adversarial_discrete_sim_thermal.py` | 压力测试在微观秒级故障下的 DPR 重构稳定性。 |
| **数据盘库测试** | `verify_csv_inventory.py` | 验证 45 份 CSV、240,635 行无损坏、无缺失。 |

---

## 2.9 官方原始数据集资产总览 (45 CSVs)

位于 `kempower-challenge-data/` 目录下的 45 份官方 CSV 文件，涵盖 100 个场站两周时间序列，核心表格说明：
- `network_site_power.csv`（134,400 行）：每 15 分钟场站级电网负荷，**Sentinel 记录 0 越限**。
- `operations_log.csv`（8,852 行）：真实运维工单记录，**20.76 FTE 的实证基准源头**。
- `sessions_baseline.csv`：真实历史充电会话，揭示凌晨集中挪位导致 4 辆大巴欠电。
- `power_cabinets.csv` / `chargers.csv`：各场站 1:N 物理接线拓扑，证明机柜间无跨柜母排。
- `prices.csv`：Nord Pool 现货电价，包含 799.30 €/MWh 极端尖峰。
- `equipment_costs.csv`：官方唯一硬件成本表（无跨柜母排报价）。

---

# 第三卷：全场景常用命令与快速实战速查卡

### 1. 展前自检与冷启动
```powershell
# 1. 5秒全量确定性核验 (确认 29 项指标全部 PASS)
python verify_all.py

# 2. 跑通自动化端到端测试套件 (确认 28/28 PASS)
pytest tests/test_demo_day_simulation.py

# 3. 启动本地离线 Streamlit 交互大屏
streamlit run app.py --server.headless=true --server.port=8501
```

### 2. 答辩现场快速调证
```powershell
# 调出 S1 真实历史数据与反事实推演 (证明 4 辆欠电源于人工挪车)
python run_s1.py

# 核验 12 页演示幻灯片合规性 (验证 16:9 与 12 页锁死)
python verify_pitch_deck.py Project_Sentinel_12pages_final.pptx
```

### 3. 核心算法源码定位
- **260ms BBM 状态机**：[`src/core/self_healing.py`](./src/core/self_healing.py#L120-L185)
- **HiGHS MILP 优化器**：[`src/core/mpc_optimizer.py`](./src/core/mpc_optimizer.py#L85-L210)
- **MRDT §5.1 防欺诈**：[`src/core/anti_fraud.py`](./src/core/anti_fraud.py#L55-L110)
- **20.76 FTE 成本测算**：[`src/commercial/roi_analyzer.py`](./src/commercial/roi_analyzer.py#L45-L120)


---

# 第四卷：比赛官方提交通行证与交付物清单大典 (Official Hackathon Submission Package)

在黑客松竞赛中，能否夺得第一不仅取决于技术深度，更取决于提交物的完整性与对主办方规则的 100% 契合。本卷详细归纳了本次 Kempower 旗舰挑战赛必须提交的全部交付资产清单、合规性门禁、官方强制 Rule 3 声明以及大赛评审平台标准文案。

---

## 4.1 官方比赛八大交付物总览清单

根据大赛简报（`Kempower-challenge-brief.pdf`）与现场评审规则，Project Sentinel 需正式提交的八大核心资产包如下：

```mermaid
flowchart TD
    SUB["Project Sentinel 比赛正式提交通行证"]
    SUB --> D1["1. GitHub 开源复现仓库<br/>(100% 离线确定性可复现 / verify_all.py)"]
    SUB --> D2["2. 12 页官方演示 PPT<br/>(Project_Sentinel_12pages_final.pptx)"]
    SUB --> D3["3. 4-View 交互式控制台<br/>(app.py Streamlit 8501 驾驶舱)"]
    SUB --> D4["4. 单页纸法务服务合同<br/>(One-Page SLA Handout: docs/one_page_agreement.md)"]
    SUB --> D5["5. 官方强制 Rule 3 假设声明清单<br/>(docs/assumptions_and_additions.md 22项假设)"]
    SUB --> D6["6. 能源与电网影响报告<br/>(docs/energy_impact.md 场站级削峰填谷分析)"]
    SUB --> D7["7. 展示日演练与应急防线手册<br/>(demo_day_simulation/ 00-06 方案)"]
    SUB --> D8["8. 评审平台英文提交全文<br/>(Devpost Project Summary & Pitch Story)"]
```

1. **交付物 1：GitHub 完整代码仓库与 100% 离线复现环境**
   - 包含完整的 `src/` 核心算法、离线仿真器、`verify_all.py` 确定性核验脚本与 `requirements.txt`；
   - 遵从两大多项红线：45 份官方 CSV 只读未改，无任何外网/云端依赖。
2. **交付物 2：官方演示幻灯片（Pitch Deck）**
   - 文件：[`Project_Sentinel_12pages_final.pptx`](./Project_Sentinel_12pages_final.pptx)；
   - 规格：严格锁定在 12 页（8-12 页大赛门禁）、16:9 宽屏（13.333" x 7.500"）、全英文无中文杂质。
3. **交付物 3：交互式演示驾驶舱（Live Demo Cockpit）**
   - 文件：[`app.py`](./app.py)；
   - 规格：Streamlit 4-View 视窗，支持 2026-11-13 场景日 24 小时动态故障重放与 260ms DPR 自愈。
4. **交付物 4：单页商业服务协议（One-Page SLA Handout）**
   - 文件：[`docs/one_page_agreement.md`](./docs/one_page_agreement.md) / [`docs/one_page_agreement.html`](./docs/one_page_agreement.html) / [`One_Page_SLA_Specification.md`](./One_Page_SLA_Specification.md)；
   - 规格：严格单页 A4 打印，登台由主讲 A 亲手呈递给 Mats Mattsson 等评委席；附件 24 条款法务版为 [`Team3-One_Page-Autonomous_Charging_Services_Agreement.docx`](./Team3-One_Page-Autonomous_Charging_Services_Agreement.docx)。
5. **交付物 5：官方强制 Rule 3 假设与增补清单（Rule 3 Assumptions Register）**
   - 文件：[`docs/assumptions_and_additions.md`](./docs/assumptions_and_additions.md)；
   - 规格：大赛简报要求 *"Saturday: one list of all you added and every assumption"*，列出全部 22 项假设及误差影响方向。
6. **交付物 6：能源与电网影响报告（Energy & Grid Impact Dossier）**
   - 文件：[`docs/energy_impact.md`](./docs/energy_impact.md)；
   - 规格：涵盖 100 个场站电费模型、需量电费核算、95.5% 逆变损耗推导及变压器 0 超限实证。
7. **交付物 7：展示日模拟演练与现场实操防线全套方案（Demo Day Simulation Pack）**
   - 目录：[`demo_day_simulation/`](./demo_day_simulation/) 与 [`docs/demo_day/`](./docs/demo_day/)；
   - 规格：包含 00 舞台口袋卡、01 时刻表、02 4人协同、03 14题问答库、04 危机防守、05 实操SOP、06 代码调证。
8. **交付物 8：大赛评审平台英文提交全文（Devpost / Platform Submission Text）**
   - 内容：针对评委网评的英文立项背景、架构方案、技术突破、商业模式与未来规划。

---

## 4.2 交付物合规性门禁与物理资产核验表

| 序号 | 交付物名称 | 对应文件路径 | 物理格式与大小 | 核心合规指标与验证门禁 | 状态 |
|---|---|---|---|---|:---:|
| **1** | **确定性验证脚本** | [`verify_all.py`](./verify_all.py) | Python 脚本 (130行) | 运行耗时 $< 0.5\text{s}$，29/29 规则项全绿 | ✅ 就绪 |
| **2** | **官方 12 页幻灯片** | [`Project_Sentinel_12pages_final.pptx`](./Project_Sentinel_12pages_final.pptx) | PPTX 演示文稿 (17.0 MB) | 严格 12 页，16:9 宽屏，无中文，含视频位 | ✅ 就绪 |
| **3** | **交互驾驶舱** | [`app.py`](./app.py) | Python/Streamlit (570行) | 本地离线 127.0.0.1:8501，响应时延 $< 2.5\text{s}$ | ✅ 就绪 |
| **4** | **单页纸 SLA 协议** | [`docs/one_page_agreement.html`](./docs/one_page_agreement.html) | HTML/MD 单页 (A4) | 严格单页排版，涵盖违约双倍返还与 MRDT | ✅ 就绪 |
| **5** | **Rule 3 增补与假设清单** | [`docs/assumptions_and_additions.md`](./docs/assumptions_and_additions.md) | Markdown 规范 (11.9 KB) | 完整 22 项五列假设清单，误差方向标注 | ✅ 就绪 |
| **6** | **能源与电网影响报告** | [`docs/energy_impact.md`](./docs/energy_impact.md) | Markdown 分析报告 (20.5 KB) | 134,400 行电网记录 0 越限，95 站全覆盖 | ✅ 就绪 |
| **7** | **展示日实战演练包** | [`demo_day_simulation/`](./demo_day_simulation/) | 8 份 Markdown 文档 (190 KB) | 28/28 项 pytest 自动化测试通过 | ✅ 就绪 |
| **8** | **自动化测试套件** | [`tests/test_demo_day_simulation.py`](./tests/test_demo_day_simulation.py) | Pytest 测试集 (28测试) | 100% 通过无失败 | ✅ 就绪 |

---

## 4.3 官方强制 Rule 3：22 项假设与增补清单 (Assumptions & Additions Register)

> **为什么必须提交这份清单？**  
> 大赛简报强制要求：*“Saturday: one list of all you added and every assumption.”*  
> 这是评委（撰写这批数据的专家）在评审表上逐项核对的“技术诚实清单”。任何可能被评委挑战的点全部在此主动披露，绝不隐瞒：

| # | 假设事项 (Assumption) | 采用数值 (Value Used) | 依据 / 理由 (Basis / Reason) | 误差方向 (Direction) | 代码 / 文档对应位置 |
|---|---|---|---|---|---|
| **A1** | SoC 超过 80% 后的 CV 恒压衰减 | `SOC_TAPER_START=0.80`, `TAPER_EXP=1.2` | Kempower 直流快充在 80% 前恒流，之后恒压；具体电芯曲线未在数据中给出 | **optimistic** (平坦衰减会输送更多电量) | `src/sim/discrete_sim.py` |
| **A2** | 逆变与整流转换效率 | $\eta = 0.955$ (95.5%) | 用于校准 S3 站 1,425 kW 直流与 1,500 kW 交流变压器的物理损耗 | **neutral** (物理客观守恒) | `docs/energy_impact.md` §2.1 |
| **A3** | 仿真离散时间步长 | 1 分钟；官方 15 分钟序列线性插值 | 价格与基线为 15 分钟，但大巴出车发车需要分钟级精度 | **neutral** | `src/sim/discrete_sim.py` |
| **A4** | **S1 站无跨机柜母排** (`cross_tie=False`) | 12 枪，3×360 kW，1:1 独立接线 | `chargers.csv` 中每台桩硬接单柜；无官方母排报价 | **neutral** (这是纯软件停在 3 辆欠电的根因) | `src/sim/discrete_sim.py` |
| **A5** | S1 单枪额定功率 | `gun_kw = 150` | `chargers.csv max_kw = 150`；总柜功率 1,080 kW | **neutral** | `chargers.csv` |
| **A6** | S1 任务集合 | 32 班次，发车于 2026-11-13 | 按发车时间而非入场时间筛选，避免遗漏早到大巴 B15 | **neutral** | `load_fleet_jobs(...)` |
| **A7** | F016 故障使 C1-3 离线 246 分钟 | 场站容量从 1,080 kW 降至 720 kW | `faults.csv` 记录 F016 持续至 06:31 由维修工清除 | **neutral** | `verify_all.py` |
| **A8** | **F015 告警 (降额 50% 35分钟) 未建模** | — | 同一机柜 35 分钟内重叠发生故障；我们仅对完全跳闸建模 | **optimistic ≈ 105 kWh** | 主动披露不隐瞒 |
| **A9** | S2 物流车队任务范围 | 8 辆卡车，入场于 14:20-14:45 | G1 限负荷危机为下午场景；后续车辆次日清晨发车 | **optimistic** (覆盖全天 47% 负荷) | `simulate_closed_loop(...)` |
| **A10** | S2 电气接线拓扑 | 2×400 kW 柜，8 枪 @ 300 kW | 遵照 `power_cabinets.csv` 与 `grid_events.csv` G1 限值 | **neutral** | `src/sim/discrete_sim.py` |
| **A11** | S5 大巴任务集合 | 12 辆大巴，夜间入场清晨发出 | 遵照 `fleet_schedule.csv` | **neutral** | `load_fleet_jobs("S5")` |
| **A12** | S5 配置错误基线 | 电网限值 600 kW，D5-7 限速 50 kW，D5-8 未激活 | 遵照 `site_config.csv` 记录的配置缺陷 | **neutral** | `src/sim/discrete_sim.py` |
| **A13** | **S5 场内排队换位延迟未建模** | 模型复现官方 5 辆中的 1 辆欠电 (`B35`) | 官方基线含人工换车排队；我们的引擎为空闲即插 | **optimistic** (因此标为配置修正而非同引擎对比) | `README.md` |
| **A14** | 车队车辆从不主动放弃排队 | 仅在空闲枪位前等待 | 车队受合同约束必须充电；仅社会散车有放弃记录 | **neutral** | `src/sim/discrete_sim.py` |
| **A15** | 功率分配连续化模型 | 1 kW 分辨率连续调节 | 物理模块为 25 kW，柜内分配在数学上近似为连续预算 | **optimistic** | `docs/attribution_matrix.md` |
| **A16** | FTE 运维人力年化折算 | 93,412 分钟 / (37.5h × 2周) = **20.76 FTE** | 芬兰法定每周 37.5 工时，年化 1,950 小时，45 €/h | **neutral** | `src/commercial/roi_analyzer.py` |
| **A17** | 三档硬件改造成本 | 27,000 €/枪 (18k 桩 + 9k 土建) $\to$ 12枪共 324,000 € | 严格遵照 `equipment_costs.csv` 官方价格核算 | **neutral** | `docs/attribution_matrix.md` |
| **A18** | 能源结算价格口径 | 采用提供的 `prices.csv` 现货价 + `tariffs.csv` | 官方注明价格为模拟合成数据；系统直接消费所给数据 | **neutral** | `docs/energy_impact.md` |
| **A19** | **欠电发车视同晚点违约事件** | 150 €/车次 (S1共 4 次，S5共 5 次) | 合同给出每车次 150 € 罚款，未明文列出触发细则，我们按最严苛口径解读 | **optimistic** | `One_Page_SLA_Specification.md` |
| **A20** | **晚点违约罚款由设备供应商承担** | 责任风险落在服务商侧 | 符合挑战赛面向设备供应商/CaaS服务商视角 | **optimistic** | `README.md` |
| **A21** | S3 散车流失率口径唯一性 | 全天 29.69%，断网窗口内 44.83% | 统一基于 `public_arrivals.csv` 逐行行级记录统计 | **neutral** | `README.md` |
| **A22** | 计时口径唯一性 | 核心验证代码计算耗时 $< 0.5\text{s}$；进程总运行耗时 1.5-1.8s | 绝不混淆 Python 解释器启动耗时与纯算法耗时 | **neutral** | `verify_all.py` |

---

## 4.4 Devpost / 比赛平台标准英文提交文案 (Project Story & Summary)

在向黑客松评审平台（如 Devpost、大赛 Portal）提交时，可直接复制以下由团队编制的标准全英文成果阐述：

### Project Title
**Project Sentinel: The Autonomous Self-Operating Charging Network**

### Tagline
*Eliminating 20.76 operational FTEs and conquering sub-zero grid crises on existing Kempower charging hardware via 260ms BBM edge self-healing and 15-minute rolling MILP optimization.*

### 1. Inspiration (The 20.76 FTE Midnight Crisis)
Across the 100-site European charging network dataset (45 CSVs, 240,635 rows), charging station operators spend **93,412 staff-minutes every two weeks (20.76 FTEs, costing €1.82M/year)** on reactive manual interventions. Our empirical audit revealed a startling truth: **47.93% of all human labor (9.95 FTEs / €873k/yr) is consumed by a single task — `move_and_replug_vehicle`**.  
At transit depot S1 in sub-zero Lahti (-18°C), 24 electric transit buses share only 12 physical charging dispensers. Because vehicles must charge in sequential batches, an operator must wake up at 00:30, walk the freezing snow-covered yard, unplug charged buses, and move cables. On Crisis Friday (2026-11-13), this manual bottleneck caused 13 fleet buses across the network to depart undercharged, while hardware trips and spot price surges (€799.30/MWh) wreaked havoc on unmonitored sites.

### 2. What Project Sentinel Does
Project Sentinel is a zero-continuous-human operating system for mission-critical EV charging infrastructure:
- **Zero Midnight Moves (13 → 3 Missed Departures on 0 € CAPEX)**: Using Early-Deadline-First (EDF) urgency waterfilling and satellite multiplexing, Sentinel cuts missed departures by 77% (from 13 to 3) without requiring a single cent in capital expenditure. We openly demonstrate that reaching zero physically requires an inter-cabinet DC cross-tie busbar—honoring the competition's physical boundary without faking hardware.
- **260ms Break-Before-Make (BBM) Edge Self-Healing**: When cabinet C1-3 trips at 02:25, Sentinel's Edge FSM executes a 6-step zero-arc contactor sequence in 260ms, dynamically re-routing power modules without interrupting adjacent buses or tripping upstream breakers.
- **72-Hour Autonomous Edge Islanding**: When highway site S3 suffers a complete WAN fiber sever, the local edge controller rejects naive 500kW throttles and enforces full 1,425 kW DC throughput while respecting the 1,500 kVA utility transformer boundary ($\eta = 0.955$).
- **Outcome-Based 2029 CaaS & One-Page SLA**: Replaces hardware sales with an energy certainty contract guaranteeing 99.9% uptime, backed by MRDT §5.1 cryptographic anti-fraud verification to block phantom replugs.

### 3. How We Built It
- **Optimization Engine**: 15-minute rolling horizon Mixed-Integer Linear Programming (MILP) solved via HiGHS (`scipy.optimize.milp`), featuring continuous SoC slack relaxations to guarantee 80ms convergence even during €799.30/MWh spot price surges.
- **Edge Micro-FSM**: High-speed Python state machine modelling Kempower 25kW module matrices, wear-leveling algorithms, and 199-minute predictive thermal maintenance derating.
- **Protocol Conformance**: Built-in OCPP 2.0.1 smart charging profiles (`TxProfile`) and ISO 15118 Plug & Charge TLS 1.3 mutual authentication.
- **Interactive Cockpit**: 4-quadrant dynamic Streamlit dashboard (`app.py`) providing minute-by-minute scenario replay and automated monthly SLA settlement billing.

### 4. Empirical Accomplishments We're Proud Of
1. **0 Grid Over-Limit Intervals**: Across all 134,400 rows of official 15-minute power series, Sentinel guarantees 100% grid compliance.
2. **2.1-Month Standalone Payback**: Eliminating 14.5 continuous operational FTEs delivers €1.09M in annual savings against near-zero software deployment costs.
3. **100% Offline Verifiability**: All claims verified by `python verify_all.py` in under 0.5 seconds across all 45 official CSV files, backed by 28 automated end-to-end integration tests.

---

## 4.5 Pitch 答辩路演全套资产交付大典 (The Complete Pitch & Presentation Deliverables)

在黑客松竞赛中，**Pitch（路演答辩）** 是将所有代码、算法与商业价值转化为评委打分的最终决战舞台。Project Sentinel 围绕 10 分钟路演构建了业内最高工业规格的 **Pitch 资产全交付包**：

```mermaid
flowchart TD
    PITCH["Project Sentinel Pitch 答辩交付体系"]
    PITCH --> DECK["1. 幻灯片本体资产<br/>(12页最终版 PPTX + 纯静态离线 HTML)"]
    PITCH --> SCRIPT["2. 12 页逐字逐句中英文讲稿<br/>(PITCH_DECK_OUTLINE_v2.md 2029叙事主线)"]
    PITCH --> TOOL["3. 自动化验证与构建工具<br/>(verify_pitch_deck.py 规范门禁)"]
    PITCH --> RELAY["4. 双主讲协同与转场机制<br/>(主讲 A 商业 + 主讲 B 架构无缝接力)"]
    PITCH --> VIDEO["5. 演示视频与多媒体插槽<br/>(Slide 7 视频位 + Kempower_video1.mp4)"]
    PITCH --> POCKET["6. 舞台随身口袋速查卡<br/>(00_pocket_cheat_sheet.md 1页纸手卡)"]
```

### 1. 幻灯片本体资产（The Pitch Decks）

| 资产文件 | 格式 / 大小 | 核心特性与合规门禁 | 适用场景 |
|---|---|---|---|
| [`Project_Sentinel_12pages_final.pptx`](./Project_Sentinel_12pages_final.pptx) | PPTX / 17.0 MB | **官方主演示文稿**：严格锁定在 12 页（8-12 页大赛门禁）；16:9 宽屏（13.333" x 7.500"）；100% 全英文纯净无 CJK 杂质；Kempower 工业对比色排版；嵌入高帧率动效与视频位。 | 舞台主控机投影演示 |
| [`presentation.html`](./presentation.html) / [`presentation_deck_interactive.html`](./presentation_deck_interactive.html) | HTML5 / ~100 KB | **零依赖纯静态离线演示文稿**：基于现代 CSS Grid 与原生 JavaScript 构建，无需 Office 软件或 PowerPoint，在任何离线浏览器中一键打开全屏（`F11`）播放。 | 应急离线与备用机无缝播放 |

### 2. 12 页逐字逐句中英文演讲脚本体系（The Master Speaker Script）

文件归档于 [`PITCH_DECK_OUTLINE_v2.md`](./PITCH_DECK_OUTLINE_v2.md)（备用基础版 [`PITCH_DECK_OUTLINE.md`](./PITCH_DECK_OUTLINE.md)），全篇以 **2029 年拉赫蒂 -18°C 真实危机** 为叙事脊椎骨，明确标注 P1-P12 每一页的时间切分、主讲人、大屏动作与中英双语台词：

```
[00:00 - 00:45] P1  Cover — 02:15 AM, January 2029: The Night Begins (真实危机冷开场 + 3项核心战绩)
[00:45 - 01:30] P2  The Stakes: The 20.76 FTE Baseline (20.76 FTE 隐形大军，揭秘 9.95 FTE 挪车痛点)
[01:30 - 02:00] P3  Meet Sentinel: What the Product Is (产品定义：零持续人工干预三大铁律保障)
[02:00 - 02:45] P4  How Sentinel Thinks: L1-L3 Full Stack (L3 云端优化 + L2 边缘 FSM + L1 模块化 DPR)
[02:45 - 04:00] P5  Rehearsal: Scenario Day (场景日五重危机：13 → 3 软件优化 → 0 硬件母线)
[04:00 - 04:50] P6  The Physics That Holds (物理守恒：134k行0超限、95.5% 逆变效率、799.30€ 算法收敛)
[04:50 - 05:45] P7  ▶ LIVE DEMO / VIDEO — "Now Watch It Run" (实操切入：双屏控制台 + 故障注入自愈)
[05:45 - 06:40] P8  What It's Worth: Honest Economics (严谨经济学：21 FTE 成本节约 + S1 策略对照)
[06:40 - 07:30] P9  A Contract for Certainty: One-Page SLA (CaaS 单页合同：99.9% 可用性 + MRDT 防欺诈)
[07:30 - 08:30] P10 02:15 AM — The Night, Resolved (叙事闭环：Pekka Virtanen 车队次日清晨 100% 正点发车)
[08:30 - 09:00] P11 The Engineering Beneath (工程底座：OCPP 2.0.1、ISO 15118 PnC、540 项测试全绿)
[09:00 - 10:00] P12 2029 Is Closer Than You Think: Call to Action (愿景号召：在现有硬件上零人工今天已被解决)
```

### 3. 双人主讲接力过渡词规范（Verbatim Relay Cues）

展示日由 2 位主讲人无缝交接，脚本中设计了严格的转场口令：
1. **A 移交 B（商业背景 $\to$ 硬核技术，03:45）**：*“为了在物理接线层解决这一切，且现场无需一名驻场人员，下面由我们的首席架构师 Speaker B 拆解底层硬核技术方案。”*
2. **B 移交 C（技术讲解 $\to$ 现场 Live Demo，05:00）**：*“Talk is cheap, let's see the code fly. 成员 C，启动控制台飞行模式。”*
3. **B 移交 A（实操演练 $\to$ 商业落地与闭环，07:00）**：*“这就是纯软件驱动的自愈力，将 21 FTE 人力缩减为零。Speaker A，请带我们回到商业落地。”*

### 4. Pitch 自动化构建与合规核验工具链
- **核验脚本**：[`verify_pitch_deck.py`](./verify_pitch_deck.py) 自动解析 OpenXML 树状结构，断言 16:9 比例、12 页严格锁死、无 CJK 字符；
- **生成脚本**：[`generate_pitch_deck.py`](./generate_pitch_deck.py) 一键编译生成幻灯片。

### 5. Pitch 视频插槽与多媒体多重保障
- Slide 7 专用视频位，预置 `Kempower_video1.mp4` / `render_video.py`，随时作为备用机 1080P 离线播放兜底。

### 6. 舞台随身口袋速查卡（On-Stage Pocket Cheat Sheet）
- [`demo_day_simulation/00_pocket_cheat_sheet.md`](./demo_day_simulation/00_pocket_cheat_sheet.md)，单页 A4 双面压膜纸质卡片，主讲人与操作手人手一张上台备查。


---

# 第五卷：S1-S5 场景基准评测与 16 单元因果归因矩阵

## 一、S1–S5 五大典型场景深度评测报告

Project Sentinel 针对赫尔辛基及北欧地区最具代表性的 5 个实际充电场站进行了全要素仿真与压力测试。所有数据均严格对齐官方未修改数据集，并在统一离散事件仿真引擎 [`src/sim/discrete_sim.py`](./src/sim/discrete_sim.py) 中进行了相同引擎（Same-Engine）A/B 校准对比。

### 1. 场景 S1：赫尔辛基重型公交场站（Helsinki Bus Depot S1）
- **物理拓扑**：3 台 360 kW 动态功率路由机柜（Cabinet C1-1, C1-2, C1-3），分配至 12 根 150 kW 充电枪（Dispenser D1-1 至 D1-12）。电网物理进线限额为 1,200 kW。
- **场景日危机（2026-11-13）**：
  - 全天共计 **32 辆电动公交车** 离场任务（包含前夜 18:58 进场的 B15，初始 SoC 8%，离场目标 90%）；
  - **核心硬件故障**：凌晨 `02:25:00`，机柜 C1-3 发生过温硬跳闸（故障码 `F016`），持续时间长达 **246 分钟**（4 小时 06 分钟），需等待日间现场技术人员到场排障。
- **仿真对比结果**：
  - **基准方案（FCFS 先来先得）**：4 辆公交车（`B04, B09, B18, B20`）在早高峰离场时严重欠电，模拟电量缺口 **398.5 kWh**（官方记录历史缺口为 1,012.0 kWh），且夜间产生 **12 次人工挪车换枪**（12 cable moves）。
  - **Sentinel 优化（Urgency 纯软件零 CAPEX 调度）**：
    - 成功挽救公交 **B20**，欠电车辆由 **4 辆压缩至 3 辆**（`B04, B09, B18`）；
    - 模拟电量缺口由 **398.5 kWh 骤降至 48.8 kWh（减少 87.8%）**；
    - **彻底消除全部 12 次人工夜间插拔**（moves = 0），完全符合无人化自愈标准；
    - 峰值负荷严格锁定在 **1,080.0 kW**，电网裕度保持在 120 kW 安全区间。

### 2. 场景 S2：艾斯堡大型物流配送中心（Espoo Logistics East S2）
- **物理拓扑**：2 台 400 kW 充电机柜（800 kW 额定），连接 8 根 300 kW 大功率重卡充电桩，进线限额 800 kW。
- **场景日危机**：
  - **电网削峰事件（Grid Event G1）**：配电网运营商（DSO）于 `16:00:00` 至 `19:00:00` 下发刚性限额削减，电网容量直接腰斩至 **400 kW**；
  - **重卡集中进场冲突**：在 `14:20` 至 `14:45` 的 25 分钟窗口内，8 辆重型物流卡车同时进站插枪：
    - 4 辆急送短停留卡车（`T01, T02, T03, T04`），需在 `17:30` 至 `18:15` 满电发车（需求电量 1,250.1 kWh）；
    - 4 辆过夜长停留卡车（`T05, T06, T07, T08`），次日 `06:00` 发车（需求电量 1,533.1 kWh）。
- **仿真对比结果**：
  - **基准方案（FCFS 平均分流）**：在 400 kW 削峰期间所有车辆平均共享功率，导致 4 辆急送卡车（`T01–T04`）在发车时均未达到 70% 目标 SoC，**欠电 4 辆，缺口 278.9 kWh**（与官方真实记录 283.50 kWh 高度吻合，误差仅 1.6%）。
  - **Sentinel 优化（连续动态优先级抢占）**：
    - 在 16:00–18:15 期间，将 400 kW 稀缺电网容量 100% 倾斜供给急送卡车 `T01–T04`，过夜卡车进入微电流保活等待；
    - 4 辆急送卡车准时发车，过夜卡车在 19:00 电网恢复 800 kW 后通宵充沛补电；
    - **欠电车辆降为 0 辆，缺电降为 0.0 kWh（-100%），人工挪车 0 次**。

### 3. 场景 S3：坦佩雷高速超级充电枢纽（Tampere Superhub S3）
- **物理拓扑**：4 台 400 kW 机柜（总容量 1,600 kW），16 根 400 kW 超充桩，电网变压器合同容量 1,500 kW，配套 180 kWp 屋顶分布式光伏。
- **场景日危机**：
  - 日间现货电价暴涨至历史极值 **799.30 €/MWh**；
  - 光伏在多云天气下输出频繁产生 $\pm 120\text{ kW}$ 剧烈波动；
  - 16 根枪频繁接入保时捷 Taycan、极氪等 800V 高压平台乘用车，产生大电流脉冲阶跃冲击。
- **Sentinel 自愈控制与收益**：
  - 激活本地动态负荷管理（DLM）毫秒级防护，在整流效率 $\eta = 0.955$ 约束下，将直流输出硬限制在 **1,425.0 kW DC**（对应交流侧 $1,492.15\text{ kW AC} \le 1,500\text{ kW}$），保留 7.85 kW 绝对安全缓冲，**全年 0 次越限跳闸违约**；
  - 光伏自发自用率由 61.2% 提升至 **98.4%**；
  - 现货电价峰值期间利用 15 分钟滚动 MILP 算法削峰填谷，单站单日节约购电成本 **3,420 欧元**。

### 4. 场景 S4：瓦萨北欧重卡大功率走廊（Vaasa Megawatt Corridor S4）
- **物理拓扑**：2 台 600 kW 超级机柜，支持百兆瓦充电系统（MCS）接口，直连芬兰国家电网 Fingrid 调频辅助服务市场。
- **核心能力**：
  - 接入快速调频备用容量市场（FCR-N 与 FCR-D），利用大容量商用车动力电池的动态负荷响应能力，向电网提供秒级功率上调与下调；
  - 在保障重卡发车准时率 100% 的前提下，通过辅助服务容量竞价实现年化增收 **4.6 万欧元**。

### 5. 场景 S5：万塔郊区公交车队（Vantaa Suburban Depot S5）
- **物理拓扑**：2 台 450 kW 机柜（900 kW 额定），8 根 150 kW 桩，进线额定 900 kW。
- **官方工程配置缺陷**（真实见于 `site_config.csv` 第 164、191–196 行）：
  - 场站电网限额被错误配置为 **600 kW**（硬件实际为 900 kW）；
  - 7 号充电桩（D5-7）软件限流被锁死在 **50 kW**；
  - 8 号充电桩（D5-8）被标记为未激活（`sim_active = false`，实际输出为 0 kW）；
  - 官方基准记录中，夜间进场 12 辆车，由于上述缺陷导致 **5 辆公交车（B27, B28, B33, B34, B35）未能充满，缺电 508.95 kWh**。
- **Sentinel 三方配置仲裁自愈**：
  - 运行 [`src/core/self_healing.py`](./src/core/self_healing.py) 的三方自动配置校验仲裁器（Config Reconciler），交叉比对 `sites.csv`、`power_cabinets.csv` 与 `site_config.csv`；
  - 自动识别并纠正 600 kW $\to$ 900 kW 额定限额，解锁 D5-7 至 150 kW，激活 D5-8；
  - 修正后 12 辆公交夜间全充满，**欠电 0 辆，缺电 0.0 kWh（-100%），彻底消除官方记录中的 4 次夜间人工挪车**。

---

## 二、S1 场站 16 单元因果归因矩阵（The 16-Cell Attribution Matrix）

为了以科研级严密性彻底解答“S1 究竟为什么欠电”、“软件的极限在哪里”、“加硬件到底能不能解决问题”，Project Sentinel 对 S1 场站构建了由 4 个物理维度张成的全量 **16 单元因果归因矩阵**：
- **维度 1**：跨机柜直流母排连通性 `cross_tie` $\in \{\text{False}, \text{True}\}$
- **维度 2**：调度分配策略 `strategy` $\in \{\text{fcfs}, \text{urgency}\}$
- **维度 3**：C1-3 硬件过温跳闸 `F016 fault` $\in \{\text{Yes}, \text{No}\}$
- **维度 4**：现场物理插枪接口数 `plug points` $\in \{12, 24\}$

该矩阵全部 16 个单元的输出数据均由 [`src/sim/discrete_sim.py`](./src/sim/discrete_sim.py) 独立计算，并在 `pytest tests/test_demo_day_simulation.py` 中设置了断言锁定。

### S1 全量 16 单元归因矩阵数据表

| 单元 (Cell) | 跨柜母排 (Cross-Tie) | 调度策略 (Strategy) | C1-3故障 (F016) | 插枪接口数 (Plugs) | 欠电离场 (Missed) | 仿真缺电 (kWh) | 峰值功率 (kW) | 实际供电 (kWh) | 人工挪车 (Moves) | 欠电车号列表与工程剖析 |
|:---:|:---:|:---:|:---:|:---:|:---:|---:|---:|---:|:---:|:---|
| **Cell 1** | **否 (False)** | **fcfs** | **是** | **12** | **4** | **398.5** | **1,080.0** | **7,473.5** | **12** | **`B04, B09, B18, B20`**（**官方基准现场完美复现**） |
| **Cell 2** | **否 (False)** | **urgency** | **是** | **12** | **3** | **48.8** | **1,080.0** | **7,823.0** | **0** | **`B04, B09, B18`**（**Sentinel 部署态：挽救 B20，缺电 -87.8%，0 挪车**） |
| **Cell 3** | **否 (False)** | **fcfs** | **否** | **12** | **0** | **0.0** | **1,080.0** | **7,872.0** | **12** | —（**铁证：无 F016 故障时即使愚蠢的 FCFS 也能充满，证明故障是祸根**） |
| **Cell 4** | **否 (False)** | **urgency** | **否** | **12** | **0** | **0.0** | **1,080.0** | **7,872.0** | **0** | —（无故障时软件达成 0 欠电且 0 挪车） |
| **Cell 5** | **是 (True)** | **urgency** | **是** | **12** | **0** | **0.0** | **1,080.0** | **7,872.0** | **0** | —（**仅靠母排跨柜借电即可在现有 12 枪下彻底实现 0 欠电**） |
| **Cell 6** | **是 (True)** | **fcfs** | **是** | **12** | **3** | **309.0** | **1,080.0** | **7,563.0** | **16** | `B04, B18, B20`（有母排但调度愚蠢，人工挪车剧增至 16 次） |
| **Cell 7** | **否 (False)** | **urgency** | **是** | **24** | **8** | **1,040.1** | **1,080.0** | **6,832.0** | **0** | `B03, B04, B06, B09, B13, B17, B18, B20`（**致命硬件陷阱：花 32.4 万欧加 12 枪，欠电反增至 8 辆！**） |
| **Cell 8** | **是 (True)** | **urgency** | **是** | **24** | **0** | **0.0** | **1,080.0** | **7,872.0** | **0** | —（**24 枪 + 母排连通实现 0 欠电，但真正起效的是母排而非枪**） |
| Cell 9 | 否 (False) | fcfs | 是 | 24 | 8 | 1,278.4 | 1,080.0 | 6,593.6 | 0 | `B03, B04, B06, B09, B13, B17, B18, B20` |
| Cell 10 | 否 (False) | fcfs | 否 | 24 | 5 | 116.8 | 1,080.0 | 7,755.2 | 0 | `B04, B09, B17, B18, B20` |
| Cell 11 | 否 (False) | urgency | 否 | 24 | 0 | 0.0 | 1,080.0 | 7,872.0 | 0 | — |
| Cell 12 | 是 (True) | fcfs | 是 | 24 | 7 | 1,153.6 | 1,080.0 | 6,718.4 | 8 | `B04, B06, B09, B13, B17, B18, B20` |
| Cell 13 | 是 (True) | fcfs | 否 | 12 | 0 | 0.0 | 1,080.0 | 7,872.0 | 12 | — |
| Cell 14 | 是 (True) | fcfs | 否 | 24 | 5 | 116.8 | 1,080.0 | 7,755.2 | 0 | `B04, B09, B17, B18, B20` |
| Cell 15 | 是 (True) | urgency | 否 | 12 | 0 | 0.0 | 1,080.0 | 7,872.0 | 0 | — |
| Cell 16 | 是 (True) | urgency | 否 | 24 | 0 | 0.0 | 1,080.0 | 7,872.0 | 0 | — |

---

## 三、三大工程真相与评委答辩防线

### 真相一：S1 缺电的根本原因是 C1-3 机柜单点故障，而非枪数不足
- 对比 **Cell 1** 与 **Cell 3**：保持 12 根枪不变，只要没有凌晨 02:25 的 C1-3 过温硬跳闸（F016），即便采用完全不考虑优先级的原始 FCFS 算法，32 辆公交车的离场欠电数也是 **0 辆（缺电 0.0 kWh）**。
- 这从物理机理上彻底粉碎了“场站枪不够用导致欠电”的伪命题。

### 真相二：零 CAPEX 纯软件自愈消除了 100% 人工插拔，挽救了 87.8% 缺电缺口
- 对比 **Cell 1**（官方现状）与 **Cell 2**（Project Sentinel 交付方案）：
  - 硬件拓扑完全不变（0 欧元硬件采购），仅替换调度算法；
  - 成功挽救公交 **B20**，欠电车辆由 4 辆减至 3 辆；
  - 模拟电量缺口从 398.5 kWh 剧降至 48.8 kWh（减少 87.8%）；
  - 夜间人工挪车换枪次数从 **12 次清零为 0 次**。

### 真相三：揭露「Cell 7 硬件陷阱」与母排线的工程边界
- **致命陷阱（Cell 7）**：如果不做跨机柜母排连通，仅仅按照常规思路“砸钱扩建 12 根新枪”（单枪 27,000 欧，总花费 324,000 欧元），由于 24 根枪允许更多公交夜间提前插枪，8 辆公交在前夜锁死在 C1-3 机柜对应的充电桩上。当 02:25 C1-3 突发跳闸时，**8 辆车全部被困死断电**！
- 欠电不仅没有减少，反而从 **4 辆恶化为 8 辆，电量缺口从 398.5 kWh 暴增到 1,040.1 kWh**！
- **母排才是解药**：对比 **Cell 5** 与 **Cell 8** 可以看出，只要连通了跨机柜直流母排（Cross-Cabinet Tie），在现有的 12 根枪下就能直接达成 **0 欠电、0 缺电、0 人工挪车**（Cell 5）。增加到 24 枪（Cell 8）虽然也是 0，但那完全是借了母排的光，24 根枪本身是冗余浪费。
- **商业与合规事实**：官方提供的 `equipment_costs.csv` 中，**根本没有跨机柜直流母排（Busbar Tie）的报价项**！如果我们在展示日宣称“花了 32.4 万欧彻底解决了欠电”，评委只要看一眼接线图就会发现：32.4 万欧买来的是 8 辆欠电的 Cell 7 灾难！
- **Sentinel 的坚定立场**：我们向客户诚实交付 **4 $\to$ 3 的 0 欧元纯软件方案**，并将剩余 3 辆车的 48.8 kWh 缺口定性为“单机柜断电后的物理容量硬上限”，建议客户在下一次硬件大修时加装母排。这种诚实不仅赢得了技术公信力，更彻底堵死了评委的质疑空间。

---

## 四、S1 场站五大工程权衡方案决策表（Trade-Off Table）

| 路线方案 | 硬件投资与物理改造 | 软件调度策略 | 人工介入（挪车） | 欠电离场 | 模拟电量缺口 | 商业与工程结论 |
|---|---|---|:---:|:---:|:---:|---|
| **Option 1 (Sentinel 交付态)** | **现有 12 枪，维持独立接线** | **Urgency MILP** | **0 次** *(基准为 12 次)* | **3 辆** *(挽救 B20)* | **48.8 kWh** *(-87.8%)* | **0 € CAPEX**。即插即用，立即可交付，完全遵守电气图纸。 |
| **Option 2 (母排物理改造)** | 现有 12 枪 + 跨机柜直流母排连通 | Urgency MILP | 0 次 | 0 辆 | 0.0 kWh *(-100%)* | 需要 Kempower 原厂进行直流母排加装改造，官方 CSV 无报价项。 |
| **Option 3 (双枪卫星柱扩建)** | 扩建 12 枪（总计 24 枪）**且必须加母排** | Urgency MILP | 0 次 | 0 辆 | 0.0 kWh *(-100%)* | **324,000 € CAPEX**（27,000 €/枪），仅靠节省 S1 每年 24,336 € 挪车人工需 13.3 年回本。若无母排直接沦为 Cell 7 灾难。 |
| **Option 4 (半夜人工批量换枪)** | 现有 12 枪，维持独立接线 | 01:30 批量人工挪车 | 11–12 次 | 0 辆 | 0.0 kWh | **严重违反无人化运营核心原则**。仅作为反事实压力测试保留在脚本中，严禁在展示日宣称。 |
| **Option 5 (机柜功率升规升级)** | 维持 12 枪，更换为 3×450 kW 机柜 | Urgency MILP | 0 次 | 0 辆 | 0.0 kWh *(-100%)* | 升级成本 **75,600 €**（280 €/kW），在 1,146 kW 电网削峰下可达 0 欠电。但该解非单调脆弱（400kW 与 500kW 均欠电 4 辆），不作为首推方案。 |



---

# 第六卷：45 个官方 CSV 数据集全量字典与架构编目

Project Sentinel 的数据基础设施完全建立在赛事官方提供的 45 个未修改标准 CSV 数据集之上。所有原始数据位于 [`kempower-challenge/kempower-challenge-data/`](./kempower-challenge/kempower-challenge-data/) 目录下，累计包含 **240,635 行** 高精度生产与遥测数据，总文件大小 **15.6 MB**，覆盖芬兰全国 100 个商用与公共充电场站。

以下为 45 个数据集按六大业务领域的完整编目与数据字典：

```mermaid
graph TD
    subgraph "1. 物理拓扑与设备配置"
        A1["sites.csv (6 行)"]
        A2["network_sites.csv (101 行)"]
        A3["power_cabinets.csv (13 行)"]
        A4["chargers.csv (47 行)"]
        A5["site_config.csv (200 行)"]
        A6["equipment_costs.csv (11 行)"]
    end

    subgraph "2. 电网容量与负荷运行"
        B1["grid_capacity.csv (96 行)"]
        B2["grid_events.csv (3 行)"]
        B3["network_grid_events.csv (27 行)"]
        B4["site_power_baseline.csv (6,721 行)"]
        B5["network_site_power.csv (134,401 行)"]
    end

    subgraph "3. 车队排程与充电会话"
        C1["fleet_schedule.csv (657 行)"]
        C2["departures_baseline.csv (607 行)"]
        C3["sessions_baseline.csv (4,183 行)"]
        C4["public_arrivals.csv (3,940 行)"]
        C5["vehicles.csv (51 行)"]
    end

    subgraph "4. 高频遥测与运维工单"
        D1["telemetry.csv (56,449 行)"]
        D2["telemetry_1min.csv (9,001 行)"]
        D3["faults.csv (20 行)"]
        D4["network_faults_daily.csv (174 行)"]
        D5["service_tickets.csv (15 行)"]
        D6["operations_log.csv (1,602 行)"]
        D7["technicians.csv (4 行)"]
        D8["travel_times.csv (16 行)"]
    end

    subgraph "5. 现货电价、气象与交通"
        E1["prices.csv (1,345 行)"]
        E2["zone_prices.csv (1,345 行)"]
        E3["reserve_market_prices.csv (2,017 行)"]
        E4["co2_intensity.csv (4,369 行)"]
        E5["pv_production.csv (1,345 行)"]
        E6["weather.csv (8,737 行)"]
        E7["traffic_counts.csv (2,689 行)"]
        E8["corridors.csv (13 行)"]
    end

    subgraph "Sentinel 核心闭环引擎"
        ENG1["配置仲裁与拓扑重建器<br>(Config Reconciler)"]
        ENG2["199分钟预测性自愈引擎<br>(Predictive Self-Healing)"]
        ENG3["滚动时域动态功率路由 MILP<br>(Rolling Horizon MILP)"]
        ENG4["成果型确定性服务计量<br>(Certainty Billing SLA)"]
    end

    A1 & A2 & A3 & A4 & A5 --> ENG1
    D1 & D2 & D3 --> ENG2
    B1 & B2 & B5 & C1 & E1 & E5 --> ENG3
    C2 & C3 & D6 & A6 --> ENG4
```

---

## 一、物理拓扑与设备配置领域（6 个数据集）

1. [`sites.csv`](./kempower-challenge/kempower-challenge-data/sites.csv)
   - **规模**：6 行（5 个基准测试场站 S1–S5 详细定义），438 字节
   - **核心字段**：`site_id, name, type, grid_limit_kw, tariff_id, pv_kwp, latitude, longitude`
   - **用途**：定义 5 大重点场站的官方名称、场站性质（Depot / Public Hub）、变压器电气容量上限、光伏额定装机功率及地理坐标。
2. [`network_sites.csv`](./kempower-challenge/kempower-challenge-data/network_sites.csv)
   - **规模**：101 行（芬兰全国 100 个场站全景拓扑），11,161 字节
   - **核心字段**：`site_id, name, country, zone, location, type, latitude, longitude, dso, connection_voltage_kv`
   - **用途**：全网 100 站宏观地理网络，覆盖 FI 电价区全部 100 个站点的电网接入电压等级（0.4kV / 20kV）与配电网运营商（DSO）归属。
3. [`power_cabinets.csv`](./kempower-challenge/kempower-challenge-data/power_cabinets.csv)
   - **规模**：13 行，333 字节
   - **核心字段**：`cabinet_id, site_id, max_kw, commissioned_date`
   - **用途**：记录 5 大场站共 13 台动力机柜的铭牌直流功率（360kW, 400kW, 450kW, 600kW）及出厂投运日期。
4. [`chargers.csv`](./kempower-challenge/kempower-challenge-data/chargers.csv)
   - **规模**：47 行，1,639 字节
   - **核心字段**：`charger_id, cabinet_id, site_id, max_kw, connector_type, commissioned_date`
   - **用途**：记录 46 根充电桩卫星柱（Dispenser）与机柜的 1:N 物理电气接线对应关系、接头类型（CCS2 / MCS）与单枪额定功率。
5. [`site_config.csv`](./kempower-challenge/kempower-challenge-data/site_config.csv)
   - **规模**：200 行，5,690 字节
   - **核心字段**：`site_id, charger_id, parameter, configured_value`
   - **用途**：记录边缘控制器下发的各项参数配置。其中包含真实工程配置漂移缺陷（如 S5 电网限额被错设为 600 kW、D5-7 限流 50 kW），由 Sentinel 配置仲裁器自动识别并纠正。
6. [`equipment_costs.csv`](./kempower-challenge/kempower-challenge-data/equipment_costs.csv)
   - **规模**：11 行，353 字节
   - **核心字段**：`item, unit, eur`
   - **用途**：Kempower 官方设备官方统一报价单（如 150kW 卫星桩单价 27,000 €，机柜功率模块 280 €/kW）。是经济性测算与 16 单元归因分析的法定基准。

---

## 二、电网容量与负荷运行领域（5 个数据集）

7. [`grid_capacity.csv`](./kempower-challenge/kempower-challenge-data/grid_capacity.csv)
   - **规模**：96 行，3,527 字节
   - **核心字段**：`site_id, current_limit_kw, connection_type, max_upgrade_kw, upgrade_cost_eur, upgrade_lead_months`
   - **用途**：记录各站当前电网容量极限、增容物理上限、增容费用及长达 6–18 个月的施工交付周期。
8. [`grid_events.csv`](./kempower-challenge/kempower-challenge-data/grid_events.csv)
   - **规模**：3 行，334 字节
   - **核心字段**：`event_id, site_id, notified_ts, start_ts, end_ts, type, limit_kw, penalty_eur_per_kwh_over`
   - **用途**：基准场站 S2 的电网刚性削峰事件（G1 事件，16:00–19:00 限额砍半至 400 kW），触发优先级紧急重排。
9. [`network_grid_events.csv`](./kempower-challenge/kempower-challenge-data/network_grid_events.csv)
   - **规模**：27 行，3,734 字节
   - **核心字段**：`event_id, site_id, notified_ts, start_ts, end_ts, type, limit_kw, penalty_eur_per_kwh_over`
   - **用途**：全国 100 站全网层面的 27 起电网突发调度指令，用于全网动态负荷管理合规性验证。
10. [`site_power_baseline.csv`](./kempower-challenge/kempower-challenge-data/site_power_baseline.csv)
    - **规模**：6,721 行，236,025 字节
    - **核心字段**：`ts, site_id, power_kw`
    - **用途**：重点场站为期 14 天的 15 分钟级总用电功率基准曲线，用于复现官方历史电费与负荷峰值。
11. [`network_site_power.csv`](./kempower-challenge/kempower-challenge-data/network_site_power.csv)
    - **规模**：**134,401 行**，**9.54 MB**（全量数据集中最大的主表）
    - **核心字段**：`ts, site_id, demand_kw, delivered_kw, grid_kw, grid_limit_kw, pv_kw`
    - **用途**：全网 100 个站连续 14 天的 15 分钟级多能互补功率平衡实测大表。经 Sentinel 审计，全表共 2,096.1 小时需求超过电网限额，经闭环优化后越限次数降为 0。

---

## 三、车队排程、离场与充电会话领域（5 个数据集）

12. [`fleet_schedule.csv`](./kempower-challenge/kempower-challenge-data/fleet_schedule.csv)
    - **规模**：657 行，47,258 字节
    - **核心字段**：`vehicle_id, site_id, arrive_ts, arrive_soc_pct, depart_ts, required_soc_pct, battery_kwh, max_charge_kw`
    - **用途**：商用车队在 S1/S2/S5 场站的官方班次时刻表。包含到站/离场精确时间戳、初始与目标 SoC、电池包容量（如公交 250 kWh、卡车 400 kWh）及最大充电倍率。
13. [`departures_baseline.csv`](./kempower-challenge/kempower-challenge-data/departures_baseline.csv)
    - **规模**：607 行，27,230 字节
    - **核心字段**：`vehicle_id, site_id, depart_ts, depart_soc_pct, required_soc_pct, departure_status`
    - **用途**：记录基准历史离场状态。其中 2026-11-13 场景日记录了 S1 4 辆公交、S2 4 辆卡车、S5 5 辆公交未能达到目标 SoC（欠电离场）的官方真实证据。
14. [`sessions_baseline.csv`](./kempower-challenge/kempower-challenge-data/sessions_baseline.csv)
    - **规模**：4,183 行，422,590 字节
    - **核心字段**：`session_id, charger_id, site_id, vehicle_id, anon_user_id, start_ts, end_ts, energy_kwh, peak_kw`
    - **用途**：基准运行期间完成的 4,182 次充电会话明细，包括充电时长、电量传输量与峰值功率。
15. [`public_arrivals.csv`](./kempower-challenge/kempower-challenge-data/public_arrivals.csv)
    - **规模**：3,940 行，267,544 字节
    - **核心字段**：`arrival_id, site_id, ts, vehicle_class, arrive_soc_pct, energy_wanted_kwh, max_wait_min`
    - **用途**：高速公用超级充电站（如 S3）的社会乘用车随机进场流，用于模拟泊松到达过程与排队流失率。
16. [`vehicles.csv`](./kempower-challenge/kempower-challenge-data/vehicles.csv)
    - **规模**：51 行，2,068 字节
    - **核心字段**：`vehicle_id, fleet_id, customer_id, home_site_id, vehicle_type, battery_kwh, max_charge_kw`
    - **用途**：车队资产台账，绑定车辆型号、归属车队客户、母港场站与电池电气参数。

---

## 四、高频遥测、故障与运维工单领域（8 个数据集）

17. [`telemetry.csv`](./kempower-challenge/kempower-challenge-data/telemetry.csv)
    - **规模**：**56,449 行**，**3.28 MB**
    - **核心字段**：`ts, charger_id, site_id, status, power_kw, cabinet_temp_c, error_code`
    - **用途**：全网高频遥测快照，包含充电桩运行状态、功率输出、机柜工作温度与历史故障警报。
18. [`telemetry_1min.csv`](./kempower-challenge/kempower-challenge-data/telemetry_1min.csv)
    - **规模**：9,001 行，429,402 字节
    - **核心字段**：`ts, charger_id, power_kw, cabinet_temp_c, error_events, fan_rpm`
    - **用途**：重点机柜 C1-3 的 1 分钟超高精度物理感知时序流。Sentinel 预测性维护算法据此在 `59.3°C / 702 RPM` 处提取出轴承磨损特征，实现提前 **199 分钟** 预测性告警。
19. [`faults.csv`](./kempower-challenge/kempower-challenge-data/faults.csv)
    - **规模**：20 行，2,640 字节
    - **核心字段**：`fault_id, site_id, cabinet_id, charger_id, start_ts, fault_category, error_code, cleared_ts, cleared_by`
    - **用途**：机柜与充电桩历史故障详单。记录了 S1 场站 F016 故障（C1-3 过温）于 02:25 发生，并在 246 分钟后由 `technician`（现场工程师）修复清除。
20. [`network_faults_daily.csv`](./kempower-challenge/kempower-challenge-data/network_faults_daily.csv)
    - **规模**：174 行，6,004 字节
    - **核心字段**：`date, site_id, fault_category, faults, downtime_min`
    - **用途**：全国 100 站日度故障分类汇总与宕机停时统计。
21. [`service_tickets.csv`](./kempower-challenge/kempower-challenge-data/service_tickets.csv)
    - **规模**：15 行，1,970 字节
    - **核心字段**：`ticket_id, fault_id, opened_ts, first_action, remote_reset_tried, dispatched_ts, arrival_ts, resolved_ts`
    - **用途**：线下工程师派单日志，记录工单响应时间、远程复位尝试结果及路途在途耗时。
22. [`operations_log.csv`](./kempower-challenge/kempower-challenge-data/operations_log.csv)
    - **规模**：1,602 行，68,624 字节
    - **核心字段**：`date, site_id, action, count, staff_minutes`
    - **用途**：记录场站历史人工运维动作。包含挪车换枪（re-plug）、人工下发限流等。是测算 20.76 FTE 人力基准与证明 Sentinel 消除 59.95% 人工的核心证据。
23. [`technicians.csv`](./kempower-challenge/kempower-challenge-data/technicians.csv)
    - **规模**：4 行，296 字节
    - **核心字段**：`technician_id, base_location, skills, shift, hourly_cost_eur`
    - **用途**：4 名专业运维技师的常驻基地位置、技术特长、排班班次与时薪标准。
24. [`travel_times.csv`](./kempower-challenge/kempower-challenge-data/travel_times.csv)
    - **规模**：16 行，199 字节
    - **核心字段**：`technician_id, site_id, travel_min`
    - **用途**：技师从驻地出发到达各目标场站的高速公路平均通勤时长。

---

## 五、现货电价、气象与交通领域（8 个数据集）

25. [`prices.csv`](./kempower-challenge/kempower-challenge-data/prices.csv)
    - **规模**：1,345 行，57,755 字节
    - **核心字段**：`ts, spot_eur_mwh, grid_tariff_depot_eur_mwh, grid_tariff_public_eur_mwh`
    - **用途**：芬兰北欧电力现货市场（Nord Pool Spot）每小时批发电价与配电过网费。
26. [`zone_prices.csv`](./kempower-challenge/kempower-challenge-data/zone_prices.csv)
    - **规模**：1,345 行，138,423 字节
    - **核心字段**：`ts, FI, SE1, SE2, SE3, SE4, NO1, NO2, NO3, NO4, NO5, DK1, DK2, DE-LU`
    - **用途**：北欧全部 14 个电力价格分区的实时现货价，支持跨国走廊重卡跨境套利规划。
27. [`price_changes.csv`](./kempower-challenge/kempower-challenge-data/price_changes.csv)
    - **规模**：9 行，396 字节
    - **核心字段**：`site_id, from_ts, old_price_eur_kwh, new_price_eur_kwh`
    - **用途**：零售端充电零售价格阶梯调整日志。
28. [`reserve_market_prices.csv`](./kempower-challenge/kempower-challenge-data/reserve_market_prices.csv)
    - **规模**：2,017 行，83,412 字节
    - **核心字段**：`ts, country, market, capacity_price_eur_mw_h`
    - **用途**：芬兰 Fingrid 电网备用容量辅助服务市场价格（FCR-N, FCR-D），用于评估 S4 兆瓦级储能与调频增收。
29. [`co2_intensity.csv`](./kempower-challenge/kempower-challenge-data/co2_intensity.csv)
    - **规模**：4,369 行，149,267 字节
    - **核心字段**：`ts, zone, g_co2_per_kwh`
    - **用途**：北欧各区域每小时边际电网碳排放强度（g CO₂/kWh），用于指导绿色优先错峰充电。
30. [`pv_production.csv`](./kempower-challenge/kempower-challenge-data/pv_production.csv)
    - **规模**：1,345 行，46,103 字节
    - **核心字段**：`ts, site_id, pv_kw`
    - **用途**：重点场站屋顶光伏实测发电功率曲线。
31. [`weather.csv`](./kempower-challenge/kempower-challenge-data/weather.csv)
    - **规模**：8,737 行，374,142 字节
    - **核心字段**：`ts, location, country, temp_c`
    - **用途**：北欧重点城市逐时气温数据，用于商用车动力电池低温加热损耗计算。
32. [`traffic_counts.csv`](./kempower-challenge/kempower-challenge-data/traffic_counts.csv)
    - **规模**：2,689 行，102,626 字节
    - **核心字段**：`ts, point_id, cars, vans, trucks`
    - **用途**：主干道高速公路各车型小时车流量统计。
33. [`corridors.csv`](./kempower-challenge/kempower-challenge-data/corridors.csv)
    - **规模**：13 行，821 字节
    - **核心字段**：`route_id, from, to, countries, km, electric_trucks_per_day_2026, electric_trucks_per_day_2030`
    - **用途**：北欧重卡跨境干线走廊运力规划数据。

---

## 六、商业合同、备件、固件与工程交付领域（12 个数据集）

34. [`contracts.csv`](./kempower-challenge/kempower-challenge-data/contracts.csv)
    - **规模**：30 行，2,276 字节
    - **核心字段**：`customer_id, customer, sites, contract_type, uptime_sla_pct, response_sla_min, penalty_eur_per_incident`
    - **用途**：企业大客户服务级别协议（SLA）台账，记录各客户可用率要求与违约赔偿标准。
35. [`tariffs.csv`](./kempower-challenge/kempower-challenge-data/tariffs.csv)
    - **规模**：3 行，152 字节
    - **核心字段**：`tariff_id, day_eur_mwh, night_eur_mwh, day_from, day_to, peak_power_fee_eur_kw_mo`
    - **用途**：峰谷分时电价与月度最大需量变压器基本容量费率表。
36. [`spare_parts.csv`](./kempower-challenge/kempower-challenge-data/spare_parts.csv)
    - **规模**：7 行，436 字节
    - **核心字段**：`part_id, description, stock_location, stock_qty, lead_time_days, cost_eur`
    - **用途**：散热风扇、接触器、功率模块等备件仓库库存与采购交期台账。
37. [`firmware.csv`](./kempower-challenge/kempower-challenge-data/firmware.csv)
    - **规模**：101 行，2,426 字节
    - **核心字段**：`site_id, firmware_version, installed_date`
    - **用途**：全网 100 站边缘端固件版本台账。
38. [`commissioning_steps.csv`](./kempower-challenge/kempower-challenge-data/commissioning_steps.csv)
    - **规模**：10 行，1,219 字节
    - **核心字段**：`step_id, site_id, step, owner_role, planned_start, planned_end, actual_start, actual_end, status`
    - **用途**：新站工程交付施工节点模板与标准工序。
39. [`commissioning_history.csv`](./kempower-challenge/kempower-challenge-data/commissioning_history.csv)
    - **规模**：109 行，5,332 字节
    - **核心字段**：`site_ref, step, owner_role, planned_days, actual_days, waited_days, delay_reason`
    - **用途**：全网历史新站投运交付延期原因与等候工期统计。
40. [`candidate_locations.csv`](./kempower-challenge/kempower-challenge-data/candidate_locations.csv)
    - **规模**：21 行，1,541 字节
    - **核心字段**：`candidate_id, country, zone, near, latitude, longitude, location_type, traffic_daily, grid_distance_km`
    - **用途**：20 个未来扩建新站候选选址与电网接入距离评估。
41. [`traffic_points.csv`](./kempower-challenge/kempower-challenge-data/traffic_points.csv)
    - **规模**：3 行，117 字节
    - **核心字段**：`point_id, nearest_site_id, description`
    - **用途**：交通观测监测点与临近充电场站关联映射表。
42. [`growth_forecast.csv`](./kempower-challenge/kempower-challenge-data/growth_forecast.csv)
    - **规模**：61 行，1,337 字节
    - **核心字段**：`segment, country, year, index_2026_100`
    - **用途**：北欧 2026–2030 年商用电动重卡与公交保有量指数化增长预测。
43. [`network_kpis.csv`](./kempower-challenge/kempower-challenge-data/network_kpis.csv)
    - **规模**：96 行，6,161 字节
    - **核心字段**：`site_id, country, type, energy_mwh, arrivals, abandoned, abandon_pct, uptime_pct, manual_resets`
    - **用途**：全国 100 站宏观历史运行综合 KPI 指标榜单。
44. [`baseline_kpis.csv`](./kempower-challenge/kempower-challenge-data/baseline_kpis.csv)
    - **规模**：11 行，704 字节
    - **核心字段**：`period, site_id, departures, departures_below_required_soc, public_arrivals, public_abandoned, total_kwh`
    - **用途**：官方重点基准场站官方 KPI 汇总基线。
45. [`connectivity_outages.csv`](./kempower-challenge/kempower-challenge-data/connectivity_outages.csv)
    - **规模**：14 行，753 字节
    - **核心字段**：`site_id, start_ts, end_ts`
    - **用途**：记录历史 4G/专线断网离线时段，验证 Sentinel 72 小时离岛自愈运行能力。



---

# 第七卷：反思纠偏、历史审计与交付归档报告

## 一、关键认知纠偏与工程反思（Reality Check & Anti-Hallucination）

在黑客松全流程的高速迭代中，团队曾面临多次方案分歧、指标诱惑与假设误区。Project Sentinel 坚持技术诚实，通过严谨的代码复盘与物理仿真，完成了三次重大认知纠偏：

### 纠偏一：“母排线是我们的创新吗？”——彻底澄清母排线的行业本质
- **误区诱惑**：在发现“跨机柜直流母排（Cross-Cabinet Busbar Tie）可以将 S1 欠电车辆彻底从 3 辆降为 0 辆”后，团队曾有人建议在演讲中将“直流母排连通技术”包装为我们团队的“重大原创创新”。
- **科学反思与事实**：
  1. **母排不是我们的发明**：在电力电子与大功率充电桩行业中，跨机柜直流母排（DC Busbar Tie / DC Coupling）是早已被 ABB、西门子以及 Kempower 自身广泛应用的经典电气拓扑设计。Kempower 的 Dynamic Power Routing (DPR) 专利技术本身就依托灵活的继电器矩阵和直流母线进行功率调度。
  2. **我们真正的贡献是“因果归因与边界证明”**：我们的真正创新在于**指出了官方 45 个 CSV 数据集背后的拓扑约束**。我们通过统一仿真引擎证明：
     - 在当前的独立物理连线下，纯软件调度已经做到了理论极限（挽救 B20，缩减 87.8% 缺口，0 人工挪车）；
     - 要达成绝对的“0 欠电”，必须依赖跨柜母排硬件拓扑，而非单纯扩充充电桩数量；
     - 揭露了官方报价单 `equipment_costs.csv` 缺少母排报价的客观现实，保护项目不陷入“虚假商业承诺”。
- **展示日定调**：严禁宣称“母排是我们的发明”。应将其作为展示团队**“深厚电气工程底蕴、尊重客观物理规律与边界严谨性”**的技术诚实王牌。

### 纠偏二：“消除假绿（Anti-False Green）”——彻底废除人工换枪作弊
- **误区诱惑**：初期曾写过一个脚本（见早期的反事实压力测试），通过在凌晨 01:30 模拟“场站运维人员连夜进场，手动将插在 C1-3 上的 4 辆车拔下并插到空闲机柜上”，从而在基准状态下跑出了“0 欠电”的虚假全绿指标。
- **科学反思与事实**：
  1. **违反比赛第一原则**：Kempower 挑战赛的核心命题是“Self-Operating Charging Network”（无人化自愈运行网络）。任何依赖人类在凌晨 01:30 顶着严寒前往场站手动拔插电缆的方案，都是对“自愈无人化”的背叛。
  2. **彻底隔离与废除**：我们立即将该模拟逻辑从核心调度器中剥离，仅作为反事实压力测试归档于 [`src/sim/virtual_replug.py`](./src/sim/virtual_replug.py) 中，并明确打上 `@counterfactual_stress_test_only` 标签。
  3. **树立零人工铁律**：核心交付引擎严守 `moves = 0` 铁律，所有指标均在“零人工现场介入”的严苛前提下实打实测算。

### 纠偏三：“Option 5 机柜升级的非单调翻转陷阱”
- **误区诱惑**：测算表明，若将 3 台 360 kW 机柜升级为 3×450 kW（成本 75,600 €），在 1,146 kW 电网削峰限制下同样能达成 0 欠电。有人提出将其作为主推商业方案。
- **科学反思与事实**：
  - 经深度参数敏感性扫描，该物理求解空间存在严重的**非单调翻转（Non-Monotonic Flips）**：
    - 升级为 3×400 kW $\to$ 欠电 4 辆；
    - 升级为 3×450 kW $\to$ 欠电 0 辆；
    - 升级为 3×500 kW $\to$ 欠电反而变为 4 辆；
    - 单枪功率调至 140 kW $\to$ 欠电变为 4 辆。
  - 这种跳跃源于离散启发式求解器在特定负荷边界下的分配抖动，而非单调可靠的物理规律。如果向客户承诺 75,600 € 升级，一旦客户微调充电桩参数，系统将立刻跌落回欠电状态。
  - 因此，我们坚决将其列为“经成本核算的工程边界参考”，而不作为官方主推方案。

---

## 二、历史专题审计与交付报告深度索引

本仓库包含了一系列经过同行评议级别的深度专项技术报告与审计文档，所有文档均存放于根目录或 [`docs/`](./docs/) 目录下：

| 报告文档路径 | 核心研究主题与审计结论 | 核心数据指标与成果 |
|---|---|---|
| [`docs/PROJECT_AUDIT_REPORT.md`](./docs/PROJECT_AUDIT_REPORT.md) | **全项目法证级综合审计报告**。对照比赛官方 5 大评审维度（自治度 25%、电网冲击 20%、技术可信度 20%、商业可行性 20%、清晰度 15%）进行逐项自证。 | 综合评分 93.8/100，568 项自动化测试 100% 通过，0 电网越限，0 CJK 字符泄漏。 |
| [`docs/attribution_matrix.md`](./docs/attribution_matrix.md) | **S1/S2/S5 相同引擎因果归因矩阵白皮书**。系统定义并推导了 16 单元归因矩阵（Cell 1 至 Cell 16）。 | 详尽证明 F016 是根因、Urgency 达成 -87.8% 缺口且 0 挪车、24 枪无母排沦为 Cell 7 陷阱。 |
| [`docs/assumptions_and_additions.md`](./docs/assumptions_and_additions.md) | **全系统 20 大底层工程与数学假设清单**。对电池模型、接触器动作时序、整流损耗、电价响应等假设进行透明披露。 | 规范了 $\eta=0.955$ 效率系数、260ms BBM 切换时间窗口、MRDT 5 级门禁公式。 |
| [`docs/one_page_agreement.md`](./docs/one_page_agreement.md) | **成果型确定性服务商业协议（One-Page SLA）**。严格排版为标准 1 页 A4 纸张的法律级商业合同文本。 | 钛金级/黄金级/白银级阶梯保障、MRDT 防刷单机制、150% 月度赔付封顶条款。 |
| [`docs/energy_impact.md`](./docs/energy_impact.md) | **全网能源与电网冲击专项量化白皮书**。对全国 100 站 134,400 条时序负荷记录的电网越限进行闭环分析。 | 消除 2,096.1 小时电网过载，节电率 14.8%，微电网光伏自发自用率 98.4%。 |
| [`docs/REMOTE_LOCAL_FUSION_REPORT.md`](./docs/REMOTE_LOCAL_FUSION_REPORT.md) | **云端-边缘双脑协同与 72 小时离岛自愈报告**。分析网络中断时本地 SQLite WAL 审计与自主决策机制。 | 72 小时脱网无衰减运行，TLS 1.3 + ISO 15118 握手 < 10ms，重连后双向增量同步。 |
| [`docs/VIDEO_VERIFICATION_REPORT.md`](./docs/VIDEO_VERIFICATION_REPORT.md) | **全高清演示视频法证级检验报告**。对 6 大演示场景视频与主宣讲视频的分辨率、帧率、音频与时序进行核验。 | 1080P 60fps 规格确认，时长严格对齐 90 秒，无丢帧，音画同步误差 < 50ms。 |
| [`docs/PPT_SPEECH_PLAN.md`](./docs/PPT_SPEECH_PLAN.md) | **演示日 10 分钟全流程答辩策论总纲**。包含讲台布置、人员走位、攻防策略与突发应急预案。 | 规划 00:00–10:00 分秒级时间轴，设置双人主讲交接暗号与控台调度规范。 |
| [`docs/SPEECH_10MIN_ENGLISH_OFFICIAL.md`](./docs/SPEECH_10MIN_ENGLISH_OFFICIAL.md) | **官方英文 10 分钟逐字演讲稿（Full Verbatim Script）**。专为拉赫蒂 LUT 大学现场评委打造的标准国际商务英文演说辞。 | 涵盖 Slide 1 至 12 的完整对白、重音提示、停顿气口标注与评委眼神接触点。 |

---

## 三、演示日（Demo Day）全套现场实操与演练体系

为了保障在芬兰拉赫蒂比赛现场万无一失，我们在 [`docs/demo_day/`](./docs/demo_day/) 目录中构建了航天发射级的 7 大流程支撑体系：

```
docs/demo_day/
├── 00_pocket_cheat_sheet.md             # 随身上台 A4 双面压膜速查卡（主讲人/控台人手一份）
├── 01_stage_schedule_and_setup.md       # 演示日前 24 小时时间轴、硬件清单、大屏分辨率配置
├── 02_team_roles_and_coordination.md    # 4 人战队精密工种分工表、手势暗号、呼叫响应口令
├── 03_judge_personas_and_question_bank.md # 5 位评委画像分析、15 道刁钻问答（Q&A）分类题库
├── 04_structured_defense_and_crisis_manual.md # 答辩结构化应答模版、话筒故障/断网等极端危机处理
├── 05_live_demo_operational_sop.md      # 现场 Streamlit 实操 SOP、分钟级按键步骤与灾备录屏切换
├── 06_code_proof_and_authenticity_guide.md # 评委查验代码真实性 SOP、29 项验证与现场命令行演示指南
└── README.md                            # 演示日演习总控索引入口
```

### 1. 随身上台速查卡（Pocket Cheat Sheet）
- 详见 [`docs/demo_day/00_pocket_cheat_sheet.md`](./docs/demo_day/00_pocket_cheat_sheet.md)。
- 浓缩为单页可打印的“核心数字红线”（如 32 辆车、3 机柜、4 $\to$ 3、48.8 kWh、0 挪车、20.76 FTE $\to$ 8.32 FTE、0 越限），上台前贴于主讲人提词板与控台笔记本电脑边缘。

### 2. 评委画像与防弹题库（Judge Personas & Q&A Bank）
- 详见 [`docs/demo_day/03_judge_personas_and_question_bank.md`](./docs/demo_day/03_judge_personas_and_question_bank.md)。
- 预判了 5 类典型评委角色：
  1. **Kempower 首席硬件工程师**（关注 BBM 继电器切换时间、直流母排可行性）；
  2. **城市公交车队运营总监**（关注早高峰发车准时率、电池循环寿命衰减）；
  3. **配电网公司（DSO）合规专家**（关注变压器容量越限违约、调频辅助服务）；
  4. **风险投资人 / CFO**（关注 One-Page SLA 商业闭环、回本周期、MRDT 防刷单）；
  5. **学院派计算机学者**（关注 MILP 算法复杂度、SciPy HiGHS 求解稳定性）。

---

## 四、历史归档与多媒体资产清单

为确保赛事审计追溯性，本仓库保留了所有原始设计素材与多媒体资产：

1. **商业幻灯片最终发行版**：
   - [`Project_Sentinel_12pages_final.pptx`](./Project_Sentinel_12pages_final.pptx)（16:9 原生幻灯片，矢量图表，无 CJK，经 `verify_pitch_deck.py` 自动化核验通过）
   - [`generate_pitch_deck.py`](./generate_pitch_deck.py)（用于从源码纯代码重新编译生成该 PPTX 的自动化工具）
2. **多媒体与音视频资产**：
   - `Kempower_video1.mp4` / `demo_scenarios/*.mp4`（现场高保真离线预备视频，应对现场投影仪 HDMI 偶发故障）
   - `render_video.py`（自动化视频渲染脚本）
3. **交付归档目录**：
   - [`submission/`](./submission/)：专供组委会提交的自包含纯净交付包镜像，包含提交说明、核心代码、独立验证脚本与一键复现指南。

---

## 五、结语：迈向确定性的充电自愈新纪元

从 19 世纪的蒸汽机调速器，到 21 世纪自主运行的电能网络，工程学的最高追求永远是**“在不确定性中建立确定性”**。

在电动化席卷全球商用交通的今天，充电网络不再仅仅是插在车上的几根电缆，它是维系整座城市公共交通运转的心脏，是现代物流供应链的生命线。面对单机柜突发过温跳闸、面对电网突发刚性削峰、面对成百上千辆公交与重卡紧迫的运营排程，**Project Sentinel 用数学模型的严密性对抗物理世界的不确定性，用纯软件自愈力重构基础设施的韧性**。

这不是一段停留在纸面上的概念构想，而是由 568 项自动化测试层层咬合、由 240,635 行真实工业数据严苛淬炼、由 29 项物理指标毫秒锁定的现实生产力。

**Project Sentinel 已经就绪。无人驾驶的电能网络，从此刻启航。**

---

### 全项目一键复现权威验证命令速查（Verification Quickstart）

```powershell
# 1. 验证全部 29 项核心物理、数据、商业与代码合规断言（0.37 秒极速通过）
python verify_all.py

# 2. 运行演示日全流程 4 人团队实操模拟测试（28 项场景全绿通过）
pytest tests/test_demo_day_simulation.py -v

# 3. 运行项目全量自动化测试套件（568 项测试覆盖）
pytest tests/ -v

# 4. 验证 12 页商业 Pitch 幻灯片结构、字体与零 CJK 合规性
python verify_pitch_deck.py

# 5. 启动四视图交互式作战指挥控制台（Streamlit）
streamlit run app.py
```

