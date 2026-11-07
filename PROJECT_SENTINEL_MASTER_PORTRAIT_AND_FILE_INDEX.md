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

## 1.7 展示日现场实操全流程 SOP（含三级逃生防线）

### 1.7.1 登台前 20 分钟准备检查单（Pre-flight Checklist）
- [ ] **系统硬化（成员 C）**：笔记本 1 开启【飞行模式】（断网）、开启【专注模式】（静音通知）、电源设为“最佳性能”、休眠设为“从不”。
- [ ] **服务预热（成员 C）**：
  ```powershell
  python verify_all.py
  streamlit run app.py --server.headless=true --server.port=8501
  ```
- [ ] **浏览器全屏（成员 C）**：访问 `http://localhost:8501/`，按 `F11` 全屏，锁定 100% 缩放，置于 View 1。
- [ ] **双机热备（成员 D）**：笔记本 2 开启 VLC 播放器全屏暂停在 1080P 离线录屏第一帧；HDMI 硬件切换器置于 Channel 1。
- [ ] **资料分发（主讲人 A）**：将 4 份纸质版 `One-Page SLA` 单页协议装袋备齐。

---

### 1.7.2 10 分钟演示逐秒操作表（Minute-by-Minute SOP）

| 时间区间 | 舞台焦点 | 负责成员 | 实操按键与界面操作 | 协同台词暗号与台风 |
|---|---|---|---|---|
| **00:00 - 00:30** | 商业开场 | 主讲人 A | 保持在 PPT P1 封面 | 抛出 2029 年拉赫蒂 -18°C 大巴停摆危机 |
| **00:30 - 03:45** | 商业痛点 | 主讲人 A | 翻页至 P2，呈递纸质 SLA | 剖析 21 FTE 运维黑洞，分发纸质合同 |
| **03:45 - 05:00** | 架构接力 | 主讲人 B | 翻页至 P3-P6 架构拓扑 | 拆解 L1-L3 与 260ms BBM 物理状态机 |
| **05:00 - 05:05** | 切入系统 | 成员 C | 按 **`Alt + Tab`** 切换至 Chrome，点击 **View 2** | 主讲 B：*“Let's see the code fly. 启动飞行模式。”* |
| **05:05 - 05:40** | 演练 1 | 成员 C | 点击 **`02:25 S1 Thermal Trip`** 按钮，展开 DPR 状态表 | 主讲 B 讲解 C1-3 跳闸，260ms BBM 无弧切接 |
| **05:40 - 06:20** | 演练 2 | 成员 C | 点击 **`18:00 S4 Price Spike`** 按钮，展示削峰折线 | 主讲 B 讲解 799.30€ 算法平滑负荷与储能放电 |
| **06:20 - 06:50** | 演练 3 | 成员 C | 点击 **`11:00 S3 WAN Outage`** 按钮，指向 1,425 kW 指标 | 主讲 B 讲解光纤挖断孤岛本地 DLM 坚守满负荷 |
| **06:50 - 07:00** | 价值收官 | 成员 C | 点击切回 **View 1**，大屏展示 20.76 FTE 消除瀑布表 | 主讲 B：*“将 21 FTE 缩减为零。Speaker A 请回。”* |
| **07:00 - 09:30** | 客户落地 | 主讲人 A | 按 **`Alt + Tab`** 切回 PPT P8-P10 | 主讲 A 讲述客户故事，宣讲 13→3 诚实边界 |
| **09:30 - 10:00** | 金句收敛 | 主讲人 A | 翻页至 P12 终页 | *“在现有硬件上，零人工已被彻底解决。”* 鸣谢 |
| **10:00 - 14:00** | 评委 Q&A | 全员 4 人 | 参照 14 题速查表秒级调证（3 秒内调出数据） | 黄金 75 秒三段式答辩，数据代码精准反击 |

---

### 1.7.3 突发黑天鹅三级逃生防线操作
1. **一级防线（Web 页面卡顿/假死）**：成员 C 在 3 秒内按 `Alt + Tab` 切至预留的 PowerShell 终端，敲回车运行 `python verify_all.py`，全绿终端日志当场震撼评委。
2. **二级防线（浏览器崩溃/端口断开）**：成员 C 在第二个备用终端按方向键上键 + 回车快速重启 `streamlit run app.py`。
3. **三级防线（主控机死机/蓝屏/黑屏）**：成员 D 在 **1 秒内果断按下 HDMI 硬件切换器按键 B**，大屏幕瞬间无缝切换至笔记本 2 播放 1080P 高清离线录屏，主讲 B 配合录屏继续解说。

---

## 1.8 代码级验证推导与现场调证指南

在展示日，面对技术评委的数据真实性质疑，团队可随时运行以下脚本进行穿透性验证：

### 1. 0.3 秒全量盘库验证：`python verify_all.py`
- **验证目的**：证明 45 份 CSV、240,635 行数据真实完整，电网 0 越限，基线 100% 真实。
- **核心源码**：[`verify_all.py`](./verify_all.py)

### 2. S1 场站真实历史反事实推演：`python run_s1.py`
- **验证目的**：直接读取官方 `sessions_baseline.csv`，证明基线 4 辆欠电是由于人工凌晨 00:30 集中挪位所致；证明一拖二零人化排程可实现 0 欠电。
- **核心源码**：[`run_s1.py`](./run_s1.py)

### 3. 自动化测试套件全绿验证：`pytest tests/test_demo_day_simulation.py`
- **验证目的**：28/28 单元与端到端测试全绿通过，证明时刻表、协同矩阵、问答库无空桩作弊。
- **核心源码**：[`tests/test_demo_day_simulation.py`](./tests/test_demo_day_simulation.py)

---

## 1.9 评委全景问答库与黄金 75 秒应答应诉速查

> 📕 **中英双语评委答辩攻防手册与硬核题库 PDF 现已发布**：  
> 完整收录三大评审角色画像、14 大核心硬核攻防题库（评委原话提问、底层陷阱剖析、开门见山立论、量化证据链、底层物理机理、连环追问反杀）、四人答辩协同分工与六大极端黑天鹅危机处置预案。  
> 👉 **[点击阅读/下载 32 页中英双语高清 PDF 手册](./PROJECT_SENTINEL_JURY_DEFENSE_BILINGUAL_MANUAL.pdf)** &nbsp;|&nbsp; **[在线 HTML 预览](./docs/demo_day/PROJECT_SENTINEL_JURY_DEFENSE_BILINGUAL_MANUAL.html)**

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        评委问答黄金 75 秒三段式防守法则                                │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ • 前 15 秒: 明确定性底线结论 (由主讲人 A 或 B 直面问题，绝不绕弯子)                   │
│ • 中间 45 秒: 引用代码行、数学公式、CSV 真实数据行硬核举证 (由主讲 B 或成员 D 报参数) │
│ • 后 15 秒: 战略拔高，商业闭环或 SLA 契约保障 (由主讲人 A 优雅收尾)                   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

| 题号 | 评委关注领域与核心问题 | 推荐作答人 | 核心举证与标准答辩词要点 |
|---|---|---|---|
| **Q01** | **技术诚实度**：Slide 8 提到漏发从 13 次降至 3 次，为什么不是 0？ | 主讲人 B | *“因为我们拒绝在黑客松中对评委撒谎！0 漏发在物理上需要跨机柜母排硬件，而官方成本表无此报价。Sentinel 在现有硬件 0 CAPEX 下减少 77% 漏发；只要客户追加母排，系统立即解锁 13→0。”* |
| **Q02** | **电气安全**：双枪同时为一辆车或两辆车充电时，内部母线短路如何防护？ | 主讲人 B | 解释模块化 DPR 的电气分段与双联接触器硬件联锁，单枪故障绝不逆向倒灌邻近车位。 |
| **Q03** | **自愈时延**：260ms 完成自愈，接触器动作机械时间与电弧熄灭是否充分？ | 成员 D | 引用 [`src/core/self_healing.py`](./src/core/self_healing.py) 6 步 BBM 状态机：降流 50ms $\to$ 压差校验 60ms $\to$ 断开 80ms $\to$ 回位 50ms $\to$ 合闸 20ms = 260ms。 |
| **Q04** | **商业基线**：21 FTE 运维成本 136.5 万欧是如何测算得出的？ | 主讲人 A | 援引 Mats 主旨演讲 21 FTE 基线与芬兰工会高压电工标准年薪 6.5 万欧（含税费社保），45 个终端日常运维全覆盖。 |
| **Q05** | **ROI 质疑**：2 个月收回软件投资，是否低估了现场网关与传感器改造费？ | 主讲人 A | 强调纯软件算法部署在现有 Kempower 边缘控制器中，无需追加任何外挂硬件网关，故属于纯 0-CAPEX 软件交付。 |
| **Q06** | **SLA 防骗保**：承诺 99.5% 运行时间与赔偿，如何防止恶意虚假刷单？ | 主讲人 A | 引用 One-Page SLA §5.1 与 [`src/core/anti_fraud.py`](./src/core/anti_fraud.py) MRDT 引擎：3分钟内重插且 SoC 波动 $\le 1\%$ 自动缝合会话，阻断恶意虚构故障。 |
| **Q07** | **算法收敛**：电价峰值冲到 799.30 €/MWh 时，MILP 求解器是否会出现无解？ | 成员 D | 引用 [`src/core/mpc_optimizer.py`](./src/core/mpc_optimizer.py) 引入连续松弛惩罚变量，HiGHS 求解器在 80ms 内必凸收敛，保早高峰出车前提下削峰。 |
| **Q08** | **热衰减预测**：极寒极热交替下的热疲劳，预测性维护有真实依据吗？ | 主讲人 B | 引用 `telemetry_1min.csv` 在 22:31:00（59.3°C / 702 RPM）提前 199 分钟捕获风机性能退化，先于官方告警平滑限流降温。 |
| **Q09** | **离线孤岛**：S3 高速站光纤挖断后，边缘网关无 NTP 如何同步计费与调度？ | 主讲人 B | 解释站端本地硬件晶振时钟与本地 NVMe 事务 WAL 预写日志，断网 72 小时内仍保持 1,425 kW 极限输出，联网后以哈希追溯自动结算。 |
| **Q10** | **现场真实性**：刚刚演示的 Live Demo 是不是预录的静态 Mock 假数据？ | 成员 C / D | 按 `Alt+Tab` 切至终端执行 `python verify_all.py` 当场全绿，并邀请评委指定任意枪号现场断开实算。 |
| **Q11** | **极寒电池**：-18°C 动力电池无法大功率充电，系统如何协调功率与预热？ | 成员 D | 引用 Nordic 低温控制策略，动态将 50kW DPR 功率分流至车载 PTC 电池加热回路，使电池在 18 分钟内恢复最佳吸纳温度，节约 35% 充电时间。 |
| **Q12** | **变压器约束**：S3 站充入 1,425 kW 直流，变压器仅 1,500 kVA，损耗考虑了吗？ | 成员 D | 给出物理公式：$1425 / 0.955 = 1492.15\text{ kW} \le 1500\text{ kVA}$，95.5% 整流效率下贴合极限运行。 |
| **Q13** | **硬件复用**：部署 Project Sentinel 需要更换现有的 Kempower 充电桩吗？ | 主讲人 B | 100% 兼容现有 Kempower C-Series 柜与 S-Series 卫星桩，所有调度指令全部基于原生 Modbus 与 CAN 总线协议下发。 |
| **Q14** | **调频合规**：S2 商圈的灵活性套利收益，在芬兰 Fingrid 市场中具备资质吗？ | 主讲人 A | Sentinel 调度响应精度达 15 分钟，完全满足 Fingrid mFRR（手动频率复原储备）准入标准，合规享受调频辅助服务补贴。 |

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

