# 自运行充电网络工业级单页服务协议规范
## One-Page Service Level Agreement (SLA) & Operating Specification: Autonomous Energy Certainty
*Contract Form No: KEMP-AUTO-2029-SLA-V1 · Applicable to Commercial Fleets & High-Power CPO Infrastructure*  
*Jurisdiction: Republic of Finland / European Union Energy Law · Effective Date: January 1, 2029*

---

### 0. 协议导言与当事方法定身份 (Preamble & Legal Binding)
本《自运行充电网络单页服务级别协议》（以下简称“本 SLA”）由以下双方在芬兰拉赫蒂依法订立并共同遵守：
1. **网络自治运营方（Autonomous Operator）**：Kempower Autonomous Energy Services Oy（负责提供基于 Kempower DPR 动态功率矩阵、边缘微网网关及自主控制算法的 100% 零人工充电网络托管运营服务）；
2. **签约客户（Contracted Client）**：商用电动公交车队、干线重卡物流运营商或商业充电场站业主（统称“客户”）。

**核心标的**：客户将其场站资产委托由网络自治控制中枢接管。双方明确约定：日常运营与调度全面剥离持续人工介入，实行**以“确定性能量交付服务（Outcome-based Charging-as-a-Service, CaaS）”为核心的自主闭环运行机制**。

---

### 1. 核心服务等级承诺指标 (Guaranteed Service Level Objectives - SLOs)
网络运营方承诺在整个计费周期内严格满足以下五项核心可量化 SLO 指标：

| 指标代码 | 指标名称 (Metric Name) | 承诺服务底线 (SLO Target) | 统计时间窗口与度量口径 | 违约判定门槛 |
|---|---|---|---|---|
| **SLO-1** | **车队按时满电出车履约率** | **100.0%** (零容忍欠电延误) | 按发车班次逐次统计；要求实际离站 $\text{SoC} \ge \text{required\_soc}$ 且延误时差 $\le 0\text{ min}$ | 任何单一班次因充电不足产生延误即视为违约 |
| **SLO-2** | **充电终端综合服务可用率** | **$\ge 99.50\%$** | 全月 720 小时每枪分钟级累计：$\frac{\sum T_{\text{available}}}{\sum T_{\text{total}}} \times 100\%$ | 月度综合可用率跌破 99.50% |
| **SLO-3** | **无网孤岛持续运行韧性** | **$\ge 72\text{ 小时}$** | 广域蜂窝/光纤中断起算，站端保持 100% 额定变压器容量动态负荷分配 | 断网期间发生电网越限或单枪非计划停机 |
| **SLO-4** | **电网进线容量防越限服从率** | **100.0%** (绝对合规) | 秒级进线电流采样：$P_{\text{grid}}(t) \le P_{\text{limit}}(t)$ | 任何瞬时穿透电网限额导致断路器跳闸或罚款 |
| **SLO-5** | **安全与自愈控制环路时延** | **$\le 200\text{ ms}$** | 边缘控制器下达功率截断与矩阵重构指令端到端时延 | 控制响应时延超过 500 ms |

---

### 2. 六大核心维度决策权限边界矩阵 (Explicit Decision Boundaries Matrix)
为确保自治系统在法律与技术维度的确定性，双方明确划分“算法独立决策域”与“强制人工介入域”：

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 自主决策权限 (AI Direct Authority) vs 人工干预边界                             │
├───────────────────────────────┬────────────────────────────────────────────────┬────────────────────────────────┤
│ 业务运营场景                  │ 算法自主决策权限 (AI Direct Authority)        │ 必须升级人工干预 (Human Action)│
├───────────────────────────────┼────────────────────────────────────────────────┼────────────────────────────────┤
│ 1. 动态功率路由与虚拟插拔     │ 完全自主：按出车倒计时无感平移 25kW 矩阵模块   │ 严禁人工介入（防止人工打乱潮流）│
│ 2. 电价尖峰与电网削峰限电     │ 完全自主：调度 BESS 满载放电，下达削峰与避峰   │ 仅在电网公司下发全网紧急停电令 │
│ 3. 模块热异常与次级硬件故障   │ 完全自主：微秒级硬件切离 + N-1 拓扑在线重构     │ 免现场出勤；仅列入月度例行巡检 │
│ 4. 严重电气绝缘与接地击穿     │ 自主闭环：毫秒级切断接触器并锁定故障枪头       │ 连续3次绝缘复测失败强制技师派单│
│ 5. 广域通信完全失联 (WAN Loss)│ 完全自主：接管场站 1500kW 满载离线动态负荷分配 │ 通信中断 >72 小时报电信基站抢修│
│ 6. 物理碰撞、火灾与人身急停   │ 自主闭环：10ms 内物理脱扣切断整站高压进线      │ 必须由持证电气工程师现场复位合闸│
└───────────────────────────────┴────────────────────────────────────────────────┴────────────────────────────────┘
```

---

### 3. 物理与电气安全硬熔断阈值 (Hard Physical Safety Trip Thresholds)
算法必须绝对受制于底层物理安全硬熔断机制。以下安全阈值由机柜与终端 MCU 固件锁死，上层任何优化软件或 AI 指令均无权覆盖或旁路：

$$\begin{cases}
T_{\text{cabinet\_internal}} \ge 65.0^{\circ}\text{C} & \implies \text{机柜自主线性降额（降载 50\%，触发告警与风机反向除尘脉冲）} \\
T_{\text{cabinet\_internal}} \ge 75.0^{\circ}\text{C} & \implies \text{硬件硬切断（Hardware Trip：100 ms 内强制断开交流进线主接触器）} \\
T_{\text{connector\_pin}} \ge 90.0^{\circ}\text{C} & \implies \text{直流回路瞬时切断（DC Disconnect：50 ms 内切断单枪主回路并锁死）} \\
R_{\text{insulation}} < 100\,\Omega/\text{V} & \implies \text{绝缘故障闭锁（IMD Fault：立即终止会话，严禁高压合闸）} \\
I_{\text{residual\_DC}} \ge 30\,\text{mA} & \implies \text{漏电安全跳闸（RCD Trip：40 ms 内切断，严格符合 IEC 61851-23 标准）} \\
P_{\text{site\_grid}} > 1.00 \times P_{\text{transformer\_limit}} & \implies \text{进线硬件限流拦截回路（Overload Clamp：20 ms 内钳位剥离非核心模块）}
\end{cases}$$

---

### 4. 违约法定赔偿公式、责任追究与赔偿限额 (Liquidated Damages, Penalties & Liability Caps)
若因自治网络算法缺陷、自愈重组失败或可避免的现场硬件故障导致履约失败，运营方按以下公式与流程向客户执行赔付：

#### 4.1 最短合理驻留时间（MRDT）前置校验与车队履约赔偿公式
**前置物理可行性门槛（Minimum Required Dwell Time, MRDT）**：  
为防范不合理调度与恶意索赔，车队车辆进站必须满足最低物理补能时间窗口。针对每次发车班次 $j$，系统依据电池物理特性与设备能力计算 $\text{MRDT}_j$：
$$\text{MRDT}_j = \left( \frac{\frac{\text{SoC}_{\text{req}, j} - \text{SoC}_{\text{arrive}, j}}{100.0} \times \text{Cap}_{\text{batt}, j}}{\min(P_{\text{charger\_max}}, P_{\text{vehicle\_max}, j}) \cdot \eta_{\text{system}}} \right) \times 60 + T_{\text{buffer}} \quad [\text{分钟}]$$
- 其中系统综合转换效率 $\eta_{\text{system}} = 0.95$；安全握手、绝缘自检与动态矩阵重组缓冲时间 $T_{\text{buffer}} = 15.0\text{ 分钟}$。
- **履约责任生效条件**：仅当车辆实际进站驻留时间 $\Delta t_{\text{dwell}, j} = (t_{\text{depart\_sched}, j} - t_{\text{arrive\_actual}, j}) \ge \text{MRDT}_j$ 时，下述延误与欠电赔偿责任方始生效。若客户晚于此门槛进站（$\Delta t_{\text{dwell}, j} < \text{MRDT}_j$），运营方完全免除违约责任，仅提供尽力充填服务（Best-Effort Service）。

**延误与欠电违约赔偿金计算方程**：
在满足 MRDT 前置条件的前提下，违约金按下列公式刚性计提：
$$\text{Penalty}_{\text{fleet}} = \sum_{i \in \text{delayed\_trips}} \left[ P_{\text{base}} + \max(0, t_{\text{delay\_min}, i} - 15) \times C_{\text{min}} \right] + \sum_{j \in \text{undercharged}} \left[ \frac{\max(0, SoC_{\text{req}, j} - SoC_{\text{dep}, j})}{100.0} \times \text{Cap}_{\text{batt}, j} \times C_{\text{energy}} \right]$$
- **基础违约金 ($P_{\text{base}}$)**：**250.00 欧元 / 班次**（只要产生延误 $t_{\text{delay}} > 0$，即刻触发）；
- **延误累进补偿 ($C_{\text{min}}$)**：延误超过 15 分钟宽限期后，按 **5.00 欧元 / 分钟** 累进支付额外调度运营损失补偿；
- **缺失能量差额补偿 ($C_{\text{energy}}$)**：对未充入的欠电差额按 **1.50 欧元 / kWh** 予以直接现金补偿，并全额报销车队调用外部应急补能或备用运力的实际合规开销。

#### 4.2 终端可用率不达标月度阶梯扣减公式 (闭环分段函数)
为彻底杜绝数学公式与合同文本的口径分歧，月度服务管理费扣减比例统一采用分段闭环函数执行：
$$\text{Fee}_{\text{deduction}} = \begin{cases}
0, & \text{若 } \text{Availability}_{\text{actual}} \ge 99.50\% \\
\text{Monthly Base Fee} \times \min\left(90.0\%, \, \left\lceil \frac{99.50\% - \text{Availability}_{\text{actual}}}{0.10\%} \right\rceil \times 2.0\% \right), & \text{若 } 95.00\% \le \text{Availability}_{\text{actual}} < 99.50\% \\
\text{Monthly Base Fee} \times 100.0\%, & \text{若 } \text{Availability}_{\text{actual}} < 95.00\% \quad (\text{服务硬失效熔断})
\end{cases}$$
- **阶梯扣除区间 ($95.00\% \le \text{Availability} < 99.50\%$)**：月度综合可用率每低于承诺阈值（99.50%）**0.10%**，扣减当月服务管理费 **2.0%**（扣减比例最高至 90.0%）；
- **服务失效熔断底线 ($\text{Availability} < 95.00\%$)**：若可用率跌破 **95.00%**，直接判定为月度服务硬失效，当月免收全部服务管理费（**100.0% 扣除**）。

#### 4.3 月度赔付与责任总额上限 (Aggregate Monthly Liability Cap)
为保障网络自运行托管模式的商业可持续性，双方就月度累计赔偿设定法定责任上限：
1. **可用率管理费扣减上限**：$\text{Fee}_{\text{deduction}} \le 100.0\% \times \text{Monthly Base Fee}$（仅免除当月管理费，不产生逆向倒贴款项）；
2. **车队违约赔偿金月度上限**：针对单一客户场站，单一计费月内累计的班次延误与欠电违约金总和（$\sum \text{Penalty}_{\text{fleet}}$）上限为该场站**当月服务管理费的 100.0%**；
3. **综合月度累计赔付总上限**：在任何情形下（包括管理费免除与班次赔偿总和），运营方在单一自然月内对客户承担的所有直接经济赔付总额，绝对不得超过当月服务管理费的 **150.0%**：
   $$\text{Total Monthly Payout} = \text{Fee}_{\text{deduction}} + \sum \text{Penalty}_{\text{fleet}} \le 1.50 \times \text{Monthly Base Fee}$$
4. **排除间接与衍生损失 (Consequential Damages Carve-Out)**：运营方的经济责任严格限于上述直接罚则。运营方不承担任何间接损失（Indirect Damages）、下游营业中断损失（Loss of Business）、预期利润损失（Loss of Profit）或惩罚性赔偿。

---

### 5. 免责除外条款与不可抗力边界 (Force Majeure & Liability Carve-Outs)
在且仅在以下经黑匣子客观证据证明的情形下，运营方免除违约金赔付与可用率考核责任：
1. **公用电网非预警断电与限电 (Grid Outage & Force Majeure Curtailment)**：
   - 对于配置 BESS 储能的场站（如全网 20 座储能站），外部电网断电时间超出场站 BESS 物理支撑放电极限（以电芯达到最低保护 SoC 为准，设计冗余为 2 小时）；
   - 对于**未配置 BESS 储能的场站（包括 S1、S2、S3、S5 特写站）**，外部中压电网断电持续超过 **15 分钟** 即刻触发全面不可抗力免责；电网断电期间暂停计入 SLO-1 出车考核与 SLO-2 可用率统计；
2. **车端非法通信、BMS 拒充与内部故障**：经 ISO 15118 通信报文解析证明，充电中断或功率受限系由车辆 BMS 主动报错终止、继电器粘连、电池包内部绝缘失效或电芯过温引发；
3. **客户未满足 MRDT 进站晚到**：车辆进站驻留时间小于系统计算的 $\text{MRDT}_j$ 物理补能窗口；
4. **第三方机械外力破坏**：包括车辆机械碰撞卫星立柱、人为物理剪割电缆、以及未经授权的暴力拔枪造成的物理损毁。

---

### 6. 黑匣子高频遥测存证与免人工自动仲裁 (Automated Black-Box Dispute Settlement)
1. **1 秒级高频物理存证**：场站边缘控制器对每根枪的电压、电流、插针温度、风机转速及 CAN/BMS 报文进行 **1 秒级（1-second resolution）** 不间断环形记录；
2. **SHA-256 密码学签名**：遥测数据流每 15 分钟生成不可篡改的 SHA-256 默克尔树根哈希（Merkle Root Hash），同步沉淀至分布式安全账本；
3. **15 分钟自动化归因与账单自扣**：任何违约事件发生后，系统数字孪生在 **15 分钟内** 自动完成事件重放与责任归因（RCA）。违约金在次月结算账单中由智能合约自动冲抵，彻底杜绝耗时漫长的人工对账与商务诉讼。

---

### 7. 签约生效与密码学印鉴 (Execution & Cryptographic Seal)

```
甲方（网络自治运营方）：                                  乙方（签约车队/场站客户）：
Kempower Autonomous Energy Services Oy                 Lahti Public Transit & Logistics Alliance

授权执行官签名: [Kempower System Chief Architect]       授权代表签名: [Depot Fleet Operations Director]
签约日期: 2029-01-01                                     签约日期: 2029-01-01
智能合约哈希: 0x8F9C4A12E8B907D3E2F4A5C6718293A4B5C6D7E8F90123456789ABCDEF012345
```
