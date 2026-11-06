# 自运行充电网络工业级单页服务协议规范与 2029 客户故事
## One-Page Service Level Agreement (SLA) & Operating Specification: Autonomous Energy Certainty
*Contract Form No: KEMP-AUTO-2029-SLA-V2 · Applicable to Commercial Fleets & High-Power CPO Infrastructure*  
*Jurisdiction: Republic of Finland / European Union Energy Law · Effective Date: January 1, 2029*

---

## 📖 2029 客户典型故事：拉赫蒂冬季风雪夜的“零接触”发车奇迹
### A Sub-Zero Winter Night in Lahti with Pekka Virtanen (Lahti City Transit / LSL)

> **背景与人物**：  
> 佩卡·维尔塔宁（Pekka Virtanen）是芬兰拉赫蒂城市公共交通（Lahden Seudun Liikenne, LSL）的运营总监。2026年，佩卡最头疼的是冬季人员招聘与调度管理：芬兰冬天零下十几度，每天深夜在积雪深厚的场站里，至少需要 3~4 名值班人员拖动沉重的 400A 充电电缆在 24 辆双铰接纯电公交之间来回拔插（Move & Replug）。一旦有人感冒误工或插头虚接，次日清晨早高峰 06:00 就会有 4~5 条核心公交线路因欠电抛锚脱班，换来的是市政数万欧元的履约罚单与市民雪地里的漫长等待。

> **2029 年 1 月 19 日，星期五，拉赫蒂北区车场（Depot S1）· 气温 -18°C · 暴风雪**：
>
> 1. **22:00 — 零接触极速入场与静默授信**：  
>    24 辆 18 米铰接电动公交陆续归场。司机只需将电缆插入车身插座，依托 **ISO 15118-20 Plug & Charge (PnC)** 协议，站端边缘控制器与车载 SECC 在 **1.1 秒** 内完成基于 ECDSA P-256 证书链的双向 TLS 1.3 身份认证与充电合约绑定。司机锁车下班，车场空无一人。
>
> 2. **02:15 — 极寒低温自愈与动态功率分流**：  
>    户外气温骤降至 -18°C，磷酸铁锂电池组电芯温度跌破冰点，常规充电倍率受阻。**Sentinel 边缘自愈控制器**敏锐感知电池极寒冷浸，立即驱动 Kempower 25 kW 模块化 DPR 矩阵，先期将 50 kW 功率动态注入车辆车载 PTC 电池温控加热回路。**18 分钟内**，电芯温度跃升至最佳吸热区间（15°C），全站充电效率逆势提速 35%，彻底避开低温慢充导致的延误陷阱。
>
> 3. **03:40 — 机柜毫秒级 BBM 自愈与 N-1 功率调度**：  
>    监测系统检测到 3 号机柜（C1-3）风机转速异常（阈值+斜率外推热告警模型在 199 分钟前已提前锁死退化趋势，自动派发次日技师更换风机工单 `cleared_by = technician`）。站端毫秒级先断后通（Break-Before-Make, BBM）继电器时序（软件决策 <10 ms，物理切换 85 ms）安全隔离受影响回路，并由健康机柜 C1-1 与 C1-2 的 720 kW N-1 功率池协同全站 24 个双枪终端（324,000 € 钛金级硬件配置）持续补能，无声保障清晨出车。
>
> 4. **05:30 — 100% 满电准时发车与清晨的第一杯咖啡**：  
>    清晨 05:30，拉赫蒂北区车场全部 24 辆电动公交的 SoC 指示灯整齐亮起绿色（100.0% 准时满电）。早班司机准时登车上电，首班车驶出车场破雪前行。
>    佩卡在拉赫蒂市中心的公寓醒来，喝着晨光中的热咖啡，手机弹出一条静默推送：  
>    *“拉赫蒂北区车场（S1）24/24 班次已 100% 准时满电出车。夜间零人工干预，自愈处理 1 起低温预热及 1 起机柜 N-1 降额；当月履约率 99.98%，SLA 绿标达成。”*
>
> **这就是 2029：充电不再是耗费人力的运维负担，而是确定性的能量交付服务（Outcome-Based CaaS）。**

---

## 🏛️ 0. 协议导言与当事方法定身份 (Preamble & Legal Binding)
本《自运行充电网络单页服务级别协议》（以下简称“本 SLA”）由以下双方在芬兰拉赫蒂依法订立并共同遵守：
1. **网络自治运营方（Autonomous Operator）**：Kempower Autonomous Energy Services Oy（负责提供基于 Kempower DPR 动态功率矩阵、边缘微网网关及自主控制算法的 100% 零人工充电网络托管运营服务）；
2. **签约客户（Contracted Client）**：商用电动公交车队（如拉赫蒂公交 LSL）、干线重卡物流运营商或商业充电场站业主（统称“客户”）。

**核心标的**：客户将其场站资产委托由网络自治控制中枢接管。双方明确约定：日常运营与调度全面剥离持续人工介入，实行**以“确定性能量交付服务（Outcome-based Charging-as-a-Service, CaaS）”为核心的自主闭环运行机制**。

---

## 🎖️ 1. 三级商业服务保障体系 (Three-Tier Commercial Service Levels)
针对不同车队与场站的业务容忍度，系统提供清晰的三级阶梯服务：

| 服务维度 | 钛金级 (Titanium Tier) · 核心公交/重卡 | 黄金级 (Gold Tier) · 标准商业车队/公共站 | 白银级 (Silver Tier) · 辅助车队/目的地站 |
|---|---|---|---|
| **适用场景** | 城市骨干公交 (S1/S5)、零容忍干线重卡 (S2) | 高吞吐公共快充站 (S3/S4)、区域物流配送 | 园区内通勤车、非高峰城市慢充站 |
| **按时满电发车履约率 (SLO-1)**| **$\ge 99.90\%$** (年延误 $\le 3$ 班次) | **$\ge 99.50\%$** (标准工业级承保线) | **$\ge 99.00\%$** (商用宽容保障线) |
| **终端综合服务可用率 (SLO-2)**| **$\ge 99.90\%$** (月离线 $\le 43$ 分钟) | **$\ge 99.50\%$** (月离线 $\le 216$ 分钟) | **$\ge 99.00\%$** (月离线 $\le 432$ 分钟) |
| **自愈响应与控制时延 (SLO-5)**| **$\le 50\text{ ms}$** (软件决策 <10 ms + 毫秒级 BBM 矩阵重构) | **$\le 100\text{ ms}$** (标准硬件级 BBM 切换) | **$\le 200\text{ ms}$** (常规接触器重组) |
| **无网孤岛持续运行能力 (SLO-3)**| **$\ge 72\text{ 小时}$** (满载 1,425 kW 本地 DLM) | **$\ge 48\text{ 小时}$** (额定变压器负荷管控) | **$\ge 24\text{ 小时}$** (基础功率均分模式) |
| **夜间挪车重插保障 (Replug)**| **0 人工接触** (24 枪双枪扩展 `324,000 €` **+ 跨柜母联** / 0 欠电；**仅加枪为 8 辆漏发，更差**；母联无官方报价) | **0 人工接触** (0 € 纯软件紧急度调度，S1 缺口缩减 87.8%) | 尽力服务 (提供自动化挪车通知) |
| **违约延误基础赔偿 ($P_{\text{base}}$)**| **350.00 欧元 / 班次** | **250.00 欧元 / 班次** | **150.00 欧元 / 班次** |
| **延误累进补偿 ($C_{\text{min}}$)**| **7.50 欧元 / 分钟** (> 10 分钟起算) | **5.00 欧元 / 分钟** (> 15 分钟起算) | **3.00 欧元 / 分钟** (> 20 分钟起算) |
| **欠电能量补偿 ($C_{\text{energy}}$)**| **2.00 欧元 / kWh** + 报销应急租车 | **1.50 欧元 / kWh** | **1.00 欧元 / kWh** |
| **基准管理费系数 (Base Fee Multiplier)**| **$1.25\times$** 基准费率 | **$1.00\times$** 基准费率 (标准基线) | **$0.80\times$** 基准费率 |

---

## ⚡ 2. 核心服务等级承诺指标 (Guaranteed Service Level Objectives - SLOs)
网络运营方在计费周期内承诺满足以下核心可量化 SLO 指标（以黄金级标准为法定基准，钛金级依系数升级）：

| 指标代码 | 指标名称 (Metric Name) | 黄金级承诺服务底线 (SLO Target) | 统计时间窗口与度量口径 | 违约判定门槛 |
|---|---|---|---|---|
| **SLO-1** | **车队按时满电出车履约率** | **$\ge 99.50\%$** | 按发车班次逐次统计；要求在满足 MRDT 前提下，实际离站 $\text{SoC} \ge \text{required\_soc}$ 且延误时差 $\le 0\text{ min}$ | 月度班次履约率低于 99.50% 触发阶梯违约赔付 |
| **SLO-2** | **充电终端综合服务可用率** | **$\ge 99.50\%$** | 全月 720 小时每枪分钟级累计：$\frac{\sum T_{\text{available}}}{\sum T_{\text{total}}} \times 100\%$ | 月度综合可用率跌破 99.50% |
| **SLO-3** | **无网孤岛持续运行韧性** | **$\ge 72\text{ 小时}$** (广域断网) | 广域蜂窝/光纤中断起算，站端保持 100% 额定变压器容量动态负荷分配 | 断网期间发生电网越限或单枪非计划停机 |
| **SLO-4** | **电网进线容量防越限服从率** | **100.0%** (绝对合规) | 秒级进线电流采样：$P_{\text{grid}}(t) \le P_{\text{limit}}(t)$ (含 95.5% 逆变损耗防护) | 任何瞬时穿透电网限额导致断路器跳闸或罚款 |
| **SLO-5** | **安全与自愈控制环路时延** | **$\le 100\text{ ms}$** | 边缘控制器下达功率截断与矩阵重构指令端到端时延 | 控制响应时延超过 200 ms |

---

## 🎛️ 3. 六大核心维度决策权限边界矩阵 (Explicit Decision Boundaries Matrix)
为确保自治系统在法律与技术维度的确定性，双方明确划分“算法独立决策域”与“强制人工介入域”：

```
┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                                 自主决策权限 (AI Direct Authority) vs 人工干预边界                             │
├───────────────────────────────┬────────────────────────────────────────────────┬────────────────────────────────┤
│ 业务运营场景                  │ 算法自主决策权限 (AI Direct Authority)        │ 必须升级人工干预 (Human Action)│
├───────────────────────────────┼────────────────────────────────────────────────┼────────────────────────────────┤
│ 1. 动态功率路由与虚拟插拔     │ 完全自主：按出车倒计时无感平移 25kW 矩阵模块   │ 严禁人工介入（防止人工打乱潮流）│
│ 2. 电价尖峰与电网削峰限电     │ 完全自主：负荷侧预充避峰（BESS 接口已定义，未实测）│ 仅在电网公司下发全网紧急停电令 │
│ 3. 模块热异常与次级硬件故障   │ 完全自主：毫秒级 BBM 切离 + N-1 柜内功率池化   │ 硬件跳闸(如F016)自动派单技师更换│
│ 4. 严重电气绝缘与接地击穿     │ 自主闭环：毫秒级切断接触器并锁定故障枪头       │ 连续3次绝缘复测失败强制技师派单│
│ 5. 广域通信完全失联 (WAN Loss)│ 完全自主：接管场站 1500kW 满载离线动态负荷分配 │ 通信中断 >72 小时报电信基站抢修│
│ 6. 物理碰撞、火灾与人身急停   │ 自主闭环：10ms 内物理脱扣切断整站高压进线      │ 必须由持证电气工程师现场复位合闸│
└───────────────────────────────┴────────────────────────────────────────────────┴────────────────────────────────┘
```

---

## 🔒 4. 物理与电气安全硬熔断阈值 (Hard Physical Safety Trip Thresholds)
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

## 💰 5. 违约法定赔偿公式、道德风险门禁与责任限额 (Liquidated Damages & MRDT Gate)

### 5.1 最短合理驻留时间（MRDT）前置校验与车队履约赔偿公式
**前置物理可行性门槛（Minimum Required Dwell Time, MRDT）**：  
为防范不合理调度与恶意索赔（防范道德风险与敲诈），车队车辆进站必须满足最低物理补能时间窗口。针对每次发车班次 $j$，系统依据电池物理特性与设备能力计算 $\text{MRDT}_j$：
$$\text{MRDT}_j = \left( \frac{\frac{\text{SoC}_{\text{req}, j} - \text{SoC}_{\text{arrive}, j}}{100.0} \times \text{Cap}_{\text{batt}, j}}{\min(P_{\text{charger\_max}}, P_{\text{vehicle\_max}, j}) \cdot \eta_{\text{system}}} \right) \times 60 + T_{\text{buffer}} \quad [\text{分钟}]$$
- 其中系统综合转换效率 $\eta_{\text{system}} = 0.95$；安全握手、绝缘自检与动态矩阵重组缓冲时间 $T_{\text{buffer}} = 15.0\text{ 分钟}$。
- **履约责任生效条件**：仅当车辆实际进站驻留时间 $\Delta t_{\text{dwell}, j} = (t_{\text{depart\_sched}, j} - t_{\text{arrive\_actual}, j}) \ge \text{MRDT}_j$ 时，下述延误与欠电赔偿责任方始生效。若客户晚于此门槛进站（$\Delta t_{\text{dwell}, j} < \text{MRDT}_j$），运营方完全免除违约责任，仅提供尽力充填服务（Best-Effort Service）。

**延误与欠电违约赔偿金计算方程（黄金级基准）**：
在满足 MRDT 前置条件的前提下，违约金按下列公式刚性计提：
$$\text{Penalty}_{\text{fleet}} = \sum_{i \in \text{delayed\_trips}} \left[ P_{\text{base}} + \max(0, t_{\text{delay\_min}, i} - 15) \times C_{\text{min}} \right] + \sum_{j \in \text{undercharged}} \left[ \frac{\max(0, SoC_{\text{req}, j} - SoC_{\text{dep}, j})}{100.0} \times \text{Cap}_{\text{batt}, j} \times C_{\text{energy}} \right]$$
- **基础违约金 ($P_{\text{base}}$)**：**250.00 欧元 / 班次**（只要产生延误 $t_{\text{delay}} > 0$，即刻触发）；
- **延误累进补偿 ($C_{\text{min}}$)**：延误超过 15 分钟宽限期后，按 **5.00 欧元 / 分钟** 累进支付额外调度运营损失补偿；
- **缺失能量差额补偿 ($C_{\text{energy}}$)**：对未充入的欠电差额按 **1.50 欧元 / kWh** 予以直接现金补偿。

### 5.2 终端可用率不达标月度阶梯扣减公式 (闭环分段函数)
月度服务管理费扣减比例统一采用分段闭环函数执行：
$$\text{Fee}_{\text{deduction}} = \begin{cases}
0, & \text{若 } \text{Availability}_{\text{actual}} \ge 99.50\% \\
\text{Monthly Base Fee} \times \min\left(90.0\%, \, \left\lceil \frac{99.50\% - \text{Availability}_{\text{actual}}}{0.10\%} \right\rceil \times 2.0\% \right), & \text{若 } 95.00\% \le \text{Availability}_{\text{actual}} < 99.50\% \\
\text{Monthly Base Fee} \times 100.0\%, & \text{若 } \text{Availability}_{\text{actual}} < 95.00\% \quad (\text{服务硬失效熔断})
\end{cases}$$
- **阶梯扣除区间 ($95.00\% \le \text{Availability} < 99.50\%$)**：月度综合可用率每低于承诺阈值（99.50%）**0.10%**，扣减当月服务管理费 **2.0%**（扣减比例最高至 90.0%）；
- **服务失效熔断底线 ($\text{Availability} < 95.00\%$)**：若可用率跌破 **95.00%**，直接判定为月度服务硬失效，当月免收全部服务管理费（**100.0% 扣除**）。

### 5.3 月度赔付与责任总额上限 (Aggregate Monthly Liability Cap)
1. **可用率管理费扣减上限**：$\text{Fee}_{\text{deduction}} \le 100.0\% \times \text{Monthly Base Fee}$（仅免除当月管理费，不产生逆向倒贴款项）；
2. **车队违约赔偿金月度上限**：针对单一客户场站，单一计费月内累计的班次延误与欠电违约金总和（$\sum \text{Penalty}_{\text{fleet}}$）上限为该场站**当月服务管理费的 100.0%**；
3. **综合月度累计赔付总上限与非负对账账单保证**：在任何情形下（包括管理费免除与班次赔偿总和），运营方在单一自然月内对客户承担的所有直接经济赔付总额，绝对不得超过当月服务管理费的 **150.0%**：
   $$\text{Total Monthly Payout} = \text{Fee}_{\text{deduction}} + \sum \text{Penalty}_{\text{fleet}} \le 1.50 \times \text{Monthly Base Fee}$$
   生成的对账账单应付金额严格满足 $\text{Net Payable} = \max(0.0, \text{Monthly Base Fee} - \text{Credits})$，多余赔偿转化为次月服务抵用券，确保商业财务模型的闭环可持续性。
4. **排除间接与衍生损失 (Consequential Damages Carve-Out)**：运营方的经济责任严格限于上述直接罚则。运营方不承担任何间接损失（Indirect Damages）、下游营业中断损失（Loss of Business）或惩罚性赔偿。

---

## 🛡️ 6. 免责除外条款与不可抗力边界 (Force Majeure & Liability Carve-Outs)
在且仅在以下经黑匣子客观证据证明的情形下，运营方免除违约金赔付与可用率考核责任：
1. **公用电网非预警断电与限电 (Grid Outage & Force Majeure Curtailment)**：
   - 对于配置 BESS 储能的场站（如全网 20 座储能站），外部电网断电时间超出场站 BESS 物理支撑放电极限（以电芯达到最低保护 SoC 为准，设计冗余为 2 小时）；
   - 对于**未配置 BESS 储能的场站（包括 S1、S2、S3、S5 特写站）**，由于站端无储能缓冲，外部中压电网断电或电网公司（DSO）下达的非预告硬限电**自发生之瞬间起即刻全面免责**；电网异常期间暂停计入 SLO-1 出车考核与 SLO-2 可用率统计；
2. **车端非法通信、BMS 拒充与内部故障**：经 ISO 15118 通信报文解析证明，充电中断或功率受限系由车辆 BMS 主动报错终止、继电器粘连、电池包内部绝缘失效或电芯过温引发；
3. **客户未满足 MRDT 进站晚到**：车辆进站驻留时间小于系统计算的 $\text{MRDT}_j$ 物理补能窗口；
4. **第三方机械外力破坏**：包括车辆机械碰撞卫星立柱、人为物理剪割电缆、以及未经授权的暴力拔枪造成的物理损毁。

---

## 🔍 7. 黑匣子高频遥测存证与免人工自动仲裁 (Automated Black-Box Dispute Settlement)
1. **1 秒级高频物理存证**：场站边缘控制器对每根枪的电压、电流、插针温度、风机转速及 CAN/BMS 报文进行 **1 秒级（1-second resolution）** 不间断环形记录，本地 NVMe 环形缓冲区提供 72 小时离线掉电保护（WAL 存证）；
2. **SHA-256 密码学签名**：遥测数据流周期性生成不可篡改的 SHA-256 默克尔树根哈希（Merkle Root Hash），在联网状态下实时沉淀、在断网状态下待网络恢复后 15 分钟内批量补齐同步；
3. **事件自动化归因与账单自扣**：任何违约事件发生后，离线离散事件仿真与对账引擎在网络可达状态下 **15 分钟内**（断网则于恢复后 15 分钟内）自动完成事件重放与责任归因（RCA）。违约金在次月结算账单中由智能合约自动冲抵，彻底杜绝耗时漫长的人工对账与商务诉讼。

---

## ✍️ 8. 签约生效与密码学印鉴 (Execution & Cryptographic Seal)

```
甲方（网络自治运营方）：                                  乙方（签约车队/场站客户）：
Kempower Autonomous Energy Services Oy                 Lahden Seudun Liikenne (Lahti City Transit)
                                                       & European Logistics Depot Alliance

授权执行官签名: [Kempower System Chief Architect]       授权代表签名: [Pekka Virtanen, Fleet Operations Director]
签约日期: 2029-01-01                                     签约日期: 2029-01-01
智能合约哈希: 0x8F9C4A12E8B907D3E2F4A5C6718293A4B5C6D7E8F90123456789ABCDEF012345
验证通道: https://sentinel.kempower.com/verify/contract/2029-LSL-DEPOT-01
```
