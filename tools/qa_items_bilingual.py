# -*- coding: utf-8 -*-
"""
Project Sentinel: 14 Core Hardcore Questions & Structured Defense Playbook (Bilingual)
Contains Q01 - Q14 with verbatim questions, traps, primary responders, opening stances,
quantitative citations, physical mechanisms, and preemptive counter-strikes.
"""

QA_ITEMS = [
    {
        "id": "Q01",
        "title_en": "13 → 3 vs 13 → 0 Missed Departures & The Busbar Truth",
        "title_cn": "13到3还是13到0？母排真相与零硬件投资调度",
        "category_en": "Hardcore Technical Architect (Mats Mattsson / Panu Vartiainen)",
        "category_cn": "硬核技术与系统架构师（代表评委：Mats Mattsson / Panu Vartiainen）",
        "responder_en": "Speaker B (Systems Architect) · Member D (Hard Math)",
        "responder_cn": "Speaker B（首席架构师）· 支援：Member D（运筹数学）",
        "statement_en": "On your summary slides, you highlight '13 → 0 missed departures', but your deterministic verifier and engineering ledger explicitly print '13 → 3' for zero-CAPEX software. Furthermore, in your simulation code, installing 12 additional dual dispensers (€324,000) without a busbar actually causes 8 missed departures—worse than the baseline of 4! Why does your software leave 3 buses stranded, why does adding €324k of hardware make things worse, and which number is the real truth?",
        "statement_cn": "在你们的总结幻灯片中，你们强调了‘漏发由 13 降至 0’，但你们的代码验证器和工程账本却白纸黑字地打印着：零 CAPEX 软件方案下是‘13 降至 3’。更致命的是，在你们的仿真代码中，额外加装 12 台双枪终端（花费 32.4 万欧元）如果不加母排连通，反而导致 8 辆车欠电——比基准的 4 辆还要糟糕！为什么你们的软件会留下 3 辆车充不饱？为什么花了 32.4 万欧硬件反而恶化？到底哪一个数字才是真实答案？",
        "trap_en": "Tests whether the team understands intra-cabinet vs inter-cabinet electrical routing (cross_tie = False in chargers.csv), the physical limitations of software-only scheduling, and the discipline of not promising unpriced hardware assets.",
        "trap_cn": "考察团队是否真正理解柜内与跨柜电气拓扑约束（chargers.csv 中严格的 cross_tie = False 独立接线）、纯软件调度的物理能力边界，以及是否具备绝不向客户许诺未经官方报价（equipment_costs.csv 无母排项）资产的工程诚实度。",
        "opening_en": "Both numbers are 100% true, but they represent two distinct engineering boundaries: 13 → 3 is our zero-CAPEX software delivery on existing copper; 13 → 0 is the hardware upper bound requiring an inter-cabinet DC busbar tie that has no price in Kempower's official catalog.",
        "opening_cn": "这两个数字都是 100% 真实的，但它们代表了完全不同的工程能力边界：‘13 降至 3’是我们在现有物理铜排连线下交付的零硬件投资（0 € CAPEX）纯软件成果；而‘13 降至 0’则是物理硬件冗余的极限上限——它必须依赖跨机柜直流母排（Busbar Tie），而该硬件在 Kempower 官方报价单中并无公开价格项。",
        "proof_en": [
            "chargers.csv confirms S1 wiring: Dispensers D1-1..4 connect to C1-1, D1-5..8 to C1-2, and D1-9..12 strictly to C1-3 (cross_tie = False).",
            "When C1-3 trips for 246 minutes (fault F016 @ 02:25), dispensers D1-9..12 have 0.0 kW physical power.",
            "In src/sim/discrete_sim.py (Cell 2): Urgency scheduling re-sequences buses on healthy cabinets C1-1 and C1-2, rescuing B20. Deficit drops from 398.5 kWh to 48.8 kWh (-87.8%) with 0 moves and 0 € CAPEX.",
            "In Cell 7: Adding 12 dual dispensers (€324,000) without busbar increases missed departures to 8 buses because 8 buses lock onto dead dispensers upon arrival.",
            "Enabling inter-cabinet DC busbar tie (cross_tie = True, Cell 8) achieves 0 missed departures (0.0 kWh deficit)."
        ],
        "proof_cn": [
            "chargers.csv 证实 S1 拓扑：D1-1..4 挂载于机柜 C1-1，D1-5..8 挂载于 C1-2，D1-9..12 刚性绑定 C1-3，跨柜母排断开（cross_tie = False）。",
            "当 C1-3 在 02:25 发生 F016 过温跳闸达 246 分钟时，对应 4 根充电枪物理输出瞬间归零（0.0 kW）。",
            "在 discrete_sim.py（Cell 2）中：紧迫度优先调度在健康机柜 C1-1/C1-2 上紧凑重排，成功挽救 B20，缺电缺口由 398.5 kWh 剧降至 48.8 kWh（减少 87.8%），挪车从 12 次降为 0 次，0 欧元硬件投入。",
            "在 Cell 7 中：花费 32.4 万欧加装 12 根枪若无母排连通，前夜 8 辆车锁死在跳闸的 C1-3 桩位上，欠电离场恶化为 8 辆！",
            "只有在启用跨机柜母排连通（cross_tie = True，Cell 8）后，系统才真正达成 0 欠电离场（0.0 kWh 缺口）。"
        ],
        "arch_en": "L1 Hardware: Intra-cabinet routing works via 25 kW modular rectifiers, but inter-cabinet routing physically requires an inter-cabinet DC busbar. L2 Edge: Dynamically reallocates power to healthy dispensers before failure strikes based on 199-minute predictive thermal warnings.",
        "arch_cn": "L1 硬件机理：单柜内功率分配依托 25 kW 功率模块继电器，但跨柜借电必须依赖柜间物理铜排母线。L2 边缘层：依托 199 分钟超前热预警，在故障发生前将紧急电量动态转移至健康机柜。",
        "close_en": "Rule 2 strictly forbids inventing hardware prices outside equipment_costs.csv. Kempower's catalog prices dispensers, cabinets, and civil works, but contains zero line items for inter-cabinet busbar ties. We deliver 13 → 3 on your existing hardware for 0 €, and we give you the verified engineering blueprint for 13 → 0.",
        "close_cn": "赛事规则二严厉禁止在官方报价单之外自造硬件价格。Kempower 目录给出了充电桩、机柜和土建报价，但母排加装并无单价。我们为您在现有硬件上以 0 欧元交付‘13 降至 3’，同时为您呈上通向‘13 降至 0’经检验的电气工程图纸。"
    },
    {
        "id": "Q02",
        "title_en": "24 Plugs Dual-Gun Topology & The 2:1 Depot Ratio",
        "title_cn": "24枪双枪拓扑与2:1场站车枪比",
        "category_en": "Kempower Challenge Custodian & Host (Panu Vartiainen / Challenge PM)",
        "category_cn": "赛事主办方与规则守护者（代表评委：Panu Vartiainen / 挑战赛项目总监）",
        "responder_en": "Speaker B (Systems Architect) · Speaker A (Commercial)",
        "responder_cn": "Speaker B（首席架构师）· 支援：Speaker A（商业领袖）",
        "statement_en": "At Depot S1, 24 buses share 12 dispensers—a 2:1 ratio. You propose replacing 12 single-gun dispensers with 12 dual-gun satellites to create 24 connection points, claiming this eliminates midnight cable replugging entirely. But if all 24 buses plug in at 22:00, why doesn't the station immediately breach its 1,200 kW grid connection? And how does your dispenser topology physically route power between the two plugs on a single satellite?",
        "statement_cn": "在 S1 场站，24 辆公交车共享 12 根充电桩——车枪比为 2:1。你们提议将 12 根单枪卫星柱升级为 12 台双枪卫星柱，从而形成 24 个物理插枪点，声称这样能彻底消除半夜人工换枪挪车。但是，如果 24 辆车在晚上 22:00 同时插枪，场站为什么不会立刻超出 1,200 kW 的电网容量红线？单台卫星柱上的两根充电枪在物理上又是如何调度功率的？",
        "trap_en": "Probing whether adding plugs causes electrical overload, and testing whether the team understands that dual-gun satellites multiplex rectifiers rather than drawing double power simultaneously.",
        "trap_cn": "质疑增加插枪接口是否会导致电网瞬间过载跳闸，并考察团队是否理解双枪卫星柱采用的是时间/功率复用技术，而非两枪同时全功率拉扯电网。",
        "opening_en": "Adding plugs does not add grid load; it adds scheduling flexibility. Upgrading to 12 dual-gun satellites provides 24 physical connection points so every driver plugs in once at 22:00, while our software schedules the 25 kW power blocks so grid demand never exceeds 1,080 kW DC.",
        "opening_cn": "增加插头增加的是调度灵活性，而不是电网负荷。将 12 根桩升级为双枪卫星柱提供了 24 个物理接头，所有司机在 22:00 回场时只需插拔一次，而我们的软件会在底层动态调度 25 kW 功率模块，使直流总功率始终锁死在 1,080 kW DC 安全上限内。",
        "proof_en": [
            "fleet_schedule.csv: 24 overnight transit buses arrive between 18:58 and 23:45, all departing between 05:30 and 06:30.",
            "operations_log.csv records 5,596 midnight cable replugs network-wide (12 mandatory moves every night at S1, taking 96 minutes of night-shift labor).",
            "power_cabinets.csv & site_config.csv: S1 has 3x 360 kW cabinets = 1,080 kW DC capacity; grid connection limit is 1,200 kW AC.",
            "In src/core/dpr_matrix.py: Dual-gun satellites share modular 25 kW rectifiers via dynamic contactor switching. Gun A and Gun B never draw full power simultaneously when near grid limits."
        ],
        "proof_cn": [
            "fleet_schedule.csv 证实：S1 场站 24 辆过夜电动公交在 18:58 至 23:45 陆续进场，发车窗口全部集中在清晨 05:30 至 06:30。",
            "operations_log.csv 记录全网共发生 5,596 次夜间挪车换枪（S1 每晚必须强制挪车 12 次，耗费 96 分钟高危夜班人力）。",
            "power_cabinets.csv 与 site_config.csv：S1 配备 3 台 360 kW 机柜（总额定 1,080 kW DC），电网进线限额为 1,200 kW AC。",
            "在 dpr_matrix.py 中：双枪卫星柱通过动态接触器矩阵时分复用 25 kW 整流模块，A 枪与 B 枪在电网负荷紧张时绝不并行动态全载拉电。"
        ],
        "arch_en": "L0 Physical: 12 dual-gun satellites on existing concrete pads provide 24 CCS2 plugs. Driver plugs in once. Mutual TLS 1.3 authenticates in 1.1s. L2 Edge: Executes Earliest Deadline First (EDF) dynamic allocation. Buses departing at 05:30 get 150 kW first; upon target SoC completion, modules transfer via BBM contactors to the second plug without human touch.",
        "arch_cn": "L0 物理拓扑：利旧现有水泥基座安装 12 台双枪卫星柱，提供 24 根 CCS2 枪线。司机插枪即走，ISO 15118 握手仅需 1.1 秒。L2 边缘调度：执行最早发车截止时间优先（EDF）动态水充算法。5:30 发车车辆优先满充 150 kW；达标后继电器在 260 毫秒内自动将模块切入第二根枪，全程零人工。",
        "close_en": "Peak DC demand remains strictly clamped at 1,080 kW DC (1,130.89 kW AC at η=0.955), which is 69.11 kW below the 1,200 kW AC grid limit. We expand the parking interface, not the electrical utility connection.",
        "close_cn": "直流峰值需求被严格锁死在 1,080 kW DC（在 η=0.955 损耗下对应 1,130.89 kW AC），距离 1,200 kW 电网红线尚有 69.11 kW 的充裕安全缓冲。我们扩充的是停车接驳界面，绝非电力报装容量。"
    },
    {
        "id": "Q03",
        "title_en": "25 kW DPR Modular Arcing Prevention & Break-Before-Make Timing",
        "title_cn": "25kW动态功率路由防电弧与260ms先断后合时序",
        "category_en": "Hardcore Technical Architect (Panu Vartiainen / Power Systems Lead)",
        "category_cn": "硬核技术与系统架构师（代表评委：Panu Vartiainen / 电力电子总工程师）",
        "responder_en": "Member D (Power Systems Specialist) · Speaker B",
        "responder_cn": "Member D（运筹仿真专家）· 支援：Speaker B（首席架构师）",
        "statement_en": "Opening a DC contactor under load creates destructive plasma arcing that welds contacts together and destroys switchgear. Your presentation claims you dynamically re-route 25 kW power modules between dispensers in milliseconds. How do you prevent contactor arcing during dynamic routing? What is your exact timing sequence, and what failsafe engages if a contactor fails to open?",
        "statement_cn": "在带载大电流下直接断开直流接触器会产生毁灭性的等离子体电弧，导致触点熔焊甚至烧毁开关柜。你们的幻灯片宣称可以在几毫秒内于不同充电桩之间动态调度 25 kW 功率模块。你们在物理上究竟如何防止接触器拉弧？具体的动作时序是多少毫秒？如果接触器发生触点粘连未打开，什么安全保护会动作？",
        "trap_en": "Probing electrical domain credibility. If the team claims 'instant switching' without ramping current down to 0A, they fail the technical credibility rubric.",
        "trap_cn": "技术深度与电气安全的核心死穴。如果团队轻率回答‘瞬间无缝切换’而没有降流灭弧过程，评委将在技术可信度（20%权重）维度直接判定不及格。",
        "opening_en": "Opening a DC contactor under load creates destructive plasma arcing. Our Dynamic Power Routing implements a deterministic 6-step Break-Before-Make protocol that drops current to 0A before contacts separate, completing in exactly 260 milliseconds—well within the 500 ms safety threshold.",
        "opening_cn": "在带载状态下断开直流接触器确实会引发致命的等离子电弧。我们的动态功率路由系统内置了符合 IEC 61851 规范的确定性 6 步‘先断后合’（Break-Before-Make）规程，在触点机械动作前必须降流至 0A，全流程耗时严格锁定在 260 毫秒——远低于 500 毫秒的安全窗口限额。",
        "proof_en": [
            "src/core/dpr_matrix.py (lines 560–618, re_route_contactor): Step 1: RAMP_DOWN_CURRENT: 35.0 ms (PWM inverter ramp to 0.0A, dI/dt < 100 A/s).",
            "Step 2: VERIFY_ZERO_CURRENT: 15.0 ms (Hall-effect zero-current sensor check I <= 0.1 A, diff V <= 5V).",
            "Step 3: BREAK_SOURCE: 65.0 ms (Mechanical opening of source contactor under verified zero current).",
            "Step 4: DEAD_TIME_INTERLOCK: 30.0 ms (Hardware galvanic isolation dead time, IEC 61851 compliance).",
            "Step 5: MAKE_DESTINATION: 65.0 ms (Mechanical closure of destination contactor).",
            "Step 6: RAMP_UP_CURRENT: 50.0 ms (Soft-start current ramp to target setpoint). Total: 260.0 ms.",
            "If zero-current is not confirmed at Step 2 within 20 ms, the system aborts routing, triggers an emergency shunt trip on the upstream circuit breaker within 5 ms, and logs an alert."
        ],
        "proof_cn": [
            "src/core/dpr_matrix.py（第 560–618 行，re_route_contactor 规程）：步骤 1：电流降额（35.0ms，PWM 变流器以 dI/dt < 100 A/s 软降至 0.0A）。",
            "步骤 2：零电流验电（15.0ms，霍尔效应传感器确认 I ≤ 0.1 A 且电压差 ≤ 5V）。",
            "步骤 3：切断源触点（65.0ms，在绝对零电流下机械断开源侧接触器）。",
            "步骤 4：死区绝缘联锁（30.0ms，硬件电气隔离死区时间，完全杜绝交叉拉弧）。",
            "步骤 5：闭合目标触点（65.0ms，目标侧健康继电器触点闭合吸合）。",
            "步骤 6：软启动加流（50.0ms，电流平滑爬升至目标输出功率）。总时长：260.0ms。",
            "若步骤 2 在 20ms 内未检测到零电流，系统立刻终止切流指令，并在 5ms 内触发上级脱扣器断开电路，记录事件并隔离通道。"
        ],
        "arch_en": "L1 Microsecond Protection: Hardware interlock line directly connects Hall sensor output to the FPGA gate drive. Firmware cannot bypass zero-current check even if OS crashes. Inter-cabinet macro reconfiguration completes in 2.63 seconds.",
        "arch_cn": "L1 微秒级硬件保护：霍尔传感器输出直连 FPGA 门极驱动互锁信号。即使上层操作系统崩溃，底层硬件也无法绕过零电流验电。柜间宏观重构耗时 2.63 秒，柜内 25kW 继电器矩阵切换为 260 毫秒。",
        "close_en": "We do not guess at contactor physics; we enforce a 30 ms galvanic isolation dead-time in firmware. The Kempower patent is dynamic power routing—our contribution is zero-arc algorithmic deterministic safety.",
        "close_cn": "我们绝不拿触点物理规律开玩笑，固件中设置了 30 毫秒刚性电气隔离死区。Kempower 的专利是动态功率路由——而我们的贡献是将算法防电弧推向确定性极致安全。"
    },
    {
        "id": "Q04",
        "title_en": "20.76 FTE (€1.82M/yr) & Honest Truck Rolls Attribution",
        "title_cn": "20.76 FTE基准与诚实的人力账本归因",
        "category_en": "Commercial Strategist & Venture Capitalist (VC Partner / Corporate CFO)",
        "category_cn": "商业战略家与风险投资人（代表评委：VC 合伙人 / 财务总监）",
        "responder_en": "Speaker A (Commercial Lead) · Speaker B",
        "responder_cn": "Speaker A（商业领袖）· 支援：Speaker B（首席架构师）",
        "statement_en": "In your economic model, you claim 20.76 FTE costing €1,821,534 per year across 100 sites, and you claim your software saves over €1.09M/yr. But in commercial charging, depot bus drivers are paid by the bus operator, while field service technicians are paid by the equipment manufacturer. Whose labor are you actually eliminating? And how much labor cannot be replaced by software?",
        "statement_cn": "在你们的财务模型中，你们声称 100 个场站基准存在 20.76 个全职人力（FTE），年成本高达 182.15 万欧元，并宣称你们的软件每年能节约 109 万欧。但在实际运营中，场站司机由公交公司雇佣，而售后技术人员由设备制造商支付。你们究竟消除了谁的人力？又有哪些人力是软件根本无法取代的？",
        "trap_en": "Probing whether the team fell into the trap of claiming 100% labor removal, conflating depot staff with manufacturer technicians, or hiding retained costs.",
        "trap_cn": "考察团队是否陷入了吹嘘‘100% 消除所有人类’的伪科学陷阱，是否混淆了场站司乘人力与设备原厂售后成本，以及是否坦诚交代无法被软件消除的刚性支出。",
        "opening_en": "We deconstruct the 20.76 FTE baseline into who actually performs each task and who pays for it. We claim 12.44 FTE (59.95%, €1.09M/yr) as software-addressable operational waste. We explicitly retain 5.09 FTE (€446k/yr) of physical technician dispatches and 3.22 FTE (€282k/yr) of customer service.",
        "opening_cn": "我们将 20.76 FTE 的基准人力精细拆解到每一个工种‘究竟由谁执行、由谁买单’。我们实事求是地将其中 12.44 FTE（占工时 59.95%，折合 109.18 万欧/年）界定为可通过软件闭环消除的重复性浪费；同时坦诚保留了 5.09 FTE（44.6 万欧/年）必须由技师上门的物理工单，以及 3.22 FTE（28.2 万欧/年）的客户服务人力。",
        "proof_en": [
            "operations_log.csv (8,852 rows, 93,412 minutes / 2 weeks = 20.76 FTE at Finnish statutory 37.5 h/wk and €45/h).",
            "Eliminated 1: Midnight Re-plugging: 9.95 FTE (5,596 events, 47.93% of all human labor, €872,976/yr) -> Eliminated via dual-gun satellites & urgency scheduling.",
            "Eliminated 2: Manual Grid Load Adjustments: 2.28 FTE (684 events, 10.98% labor, €285,188/yr) -> Eliminated via 15-min rolling MILP and local DLM.",
            "Eliminated 3: Remote System Resets & Pricing: 0.21 FTE (81 events, €18,450/yr) -> Edge FSM.",
            "Retained 1: Physical Technician Visits: 5.09 FTE (73 technician rollouts in faults.csv cleared_by=technician, 22,906 min, €446,667/yr). Broken modules cannot be fixed by software.",
            "Retained 2: Customer Contact Inquiries: 3.22 FTE (2,418 inbound support contacts, €282,558/yr)."
        ],
        "proof_cn": [
            "operations_log.csv（全部 8,852 行，双周累计耗时 93,412 分钟 = 20.76 FTE，按芬兰法定 37.5小时/周、45欧元/小时基准工时折算）。",
            "消除项 1：半夜挪车插拔（9.95 FTE，5,596 次操作，占总工时 47.93%，对应 87.29 万欧/年）-> 通过双枪卫星柱与紧迫度水充彻底清零。",
            "消除项 2：人工手动调节电网负荷（2.28 FTE，684 次操作，占 10.98%，对应 28.52 万欧/年）-> 由 15分钟滚动 MILP 与本地 DLM 接管。",
            "消除项 3：远程故障复位与改价（0.21 FTE，81 次操作，对应 1.84 万欧/年）-> 边缘有限状态机自愈。",
            "保留项 1：线下工程师排障（5.09 FTE，对应 faults.csv 中 73 起 cleared_by=technician 的严重硬件故障，耗时 22,906 分钟，折合 44.66 万欧/年）。硬件物理损坏必须有人到场换件！",
            "保留项 2：车主客服热线咨询（3.22 FTE，对应 2,418 次服务台电话，折合 28.25 万欧/年）。"
        ],
        "arch_en": "Commercial Alignment: Replug savings accrue to fleet operators (C1/C2) under our One-Page SLA. Dispatch efficiency savings accrue to equipment service providers. Both sides benefit from our unified CaaS contract.",
        "arch_cn": "商业对齐机理：挪车人力的消除直接为公交与物流车队（C1/C2）在单页 SLA 合同下省去巨额夜班司乘成本；调载与运维效率的提升则为设备维保服务商降低了 SLA 违约赔付风险，实现双赢。",
        "close_en": "A hackathon team claiming 100% elimination of human labor is either naive or dishonest. When a cooling fan bearing seizes at 02:25, software cannot turn a wrench. We eliminate 12.44 FTE of repetitive operational drudgery, but keep 5.09 FTE of skilled field technicians.",
        "close_cn": "任何宣称能 100% 消除人类运维的团队，要么是不懂工程的狂妄，要么是在欺骗评委。当散热风扇轴承在凌晨两点彻底抱死时，软件再神也变不出一把物理扳手。我们消除了 12.44 FTE 的机械式运维苦力，但诚实保留了 5.09 FTE 专业技师的高价值巡检。"
    },
    {
        "id": "Q05",
        "title_en": "2-Month Network ROI vs 13.31-Year S1 Standalone Payback",
        "title_cn": "全网2个月回报率与S1单站13.3年回本辨析",
        "category_en": "Commercial Strategist & Venture Capitalist (Investment Mentor)",
        "category_cn": "商业战略家与风险投资人（代表评委：投资机构合伙人 / 创业导师）",
        "responder_en": "Speaker A (Commercial Lead) · Member D",
        "responder_cn": "Speaker A（商业领袖）· 支援：Member D（运筹数学）",
        "statement_en": "Slide 10 claims a lightning-fast '2-month network payback', but your deep-dive financial calculations in roi_analyzer.py show that upgrading Site S1 with 12 dual-gun dispensers (€324,000) takes 13.31 years to pay back against S1's local replugging savings of €24,336/yr. Are you playing a financial shell game by dividing one site's hardware costs by the entire network's labor savings?",
        "statement_cn": "你们的第 10 页幻灯片声称具有‘2 个月极速回本’的投资回报率，但在你们 roi_analyzer.py 的代码测算中，S1 场站若加装 12 台双枪充电桩（投资 32.4 万欧），对照 S1 本地每年节省的 24,336 欧元挪车人力，静态投资回收期长达 13.31 年！你们是不是在玩‘将单站硬件成本除以全网人力节省’的财务障眼法？",
        "trap_en": "Testing whether the team commits the classic hackathon error of conflating single-site capital expenditures with network-wide operational savings.",
        "trap_cn": "考察团队是否犯了黑客松最典型的低级商业逻辑错误：把单站重资产硬件投资与全网 100 站的软件人力节省混为一谈，打出虚假的‘6 周极速回本’宣传噱头。",
        "opening_en": "There is zero shell game—they answer two completely different commercial deployment decisions: 13.31 years is the standalone hardware expansion payback for Site S1 alone; 2 months is the pure-software SaaS platform payback across all 100 sites.",
        "opening_cn": "这里没有任何财务障眼法——这两个数字回答的是完全不同的商业决策场景：13.31 年是 S1 单个场站进行重资产硬件改建的独立回本期；而 2 个月则是全网 100 个场站部署纯软件自愈 SaaS 平台、在零硬件改造成本下的真实回本周期。",
        "proof_en": [
            "Decision A (S1 Standalone Hardware CAPEX): 12 dual-gun dispensers = €324,000 (€27,000/gun from equipment_costs.csv). S1 local midnight replug labor is €24,336/yr (96 min/night = 584 h/yr @ €45/h). Payback = €324,000 / €24,336 = 13.31 years.",
            "Decision B (Network-Wide Software Rollout, 0-CAPEX): Software integration fee = €150,000 for 100 sites. Annual software-addressable operational savings = €1,091,850/yr (€90,987/mo). Payback = €150,000 / €90,987 = 1.65 months (< 2 months!).",
            "Decision C (S1 0-CAPEX Software Delivery): On existing 12 dispensers, urgency scheduling achieves 4 -> 3 missed departures, -87.8% deficit, and 0 cable moves for exactly 0.00 € CAPEX. Payback is instantaneous (0.0 days)."
        ],
        "proof_cn": [
            "决策场景 A（S1 场站独立硬件扩建）：12 台双枪卫星柱 = 32.4 万欧（每枪 2.7 万欧，出自官方 equipment_costs.csv）。S1 本地每晚人工挪车节省 24,336 欧/年（96分钟/晚 = 584小时/年 @ 45欧/小时）。单站硬件回本期 = 324,000 / 24,336 = 13.31 年。",
            "决策场景 B（全网 100 站纯软件 SaaS 部署）：全网接入实施与私有化软件许可费预估为 15.0 万欧。全网软件可消除的人力浪费为 109.18 万欧/年（月均 90,987 欧）。全网回本期 = 150,000 / 90,987 = 1.65 个月（小于 2 个月！）。",
            "决策场景 C（S1 纯软件零改造交付）：在现有 12 根枪物理连线下，紧迫度算法将漏发压缩至 3 辆，缺电缩减 87.8%，挪车彻底清零，硬件 CAPEX 投入为 0.00 欧。投资回收期为零天（即刻生效）。"
        ],
        "arch_en": "Commercial Strategy: We recommend Strategy B to all customers: deploy the software platform first to harvest 59.95% labor savings immediately, and only invest in physical dispensers at bottlenecks where fleet expansion justifies the 13.31-year capital cycle.",
        "arch_cn": "商业落地策略：我们在展示日向客户清晰建议‘先软后硬’路径——先期以 0 硬件投入部署纯软件闭环，即刻吃下全网 59.95% 的人力省降红利；后续仅在车队规模翻倍、运力确实受阻的个别瓶颈场站，审慎推进 13 年回本的桩体硬件扩建。",
        "close_en": "Don't let a 13-year hardware payback blind you to a 2-month software transformation. We deliver software first, and only pour concrete where vehicle throughput demands it.",
        "close_cn": "千万不要被单个场站 13 年的硬件土建回本期一叶障目，而忽视了全网 2 个月的纯软件自愈奇迹。我们永远坚持软件优先，只有在运力瓶颈确实需要时才破土动工。"
    },
    {
        "id": "Q06",
        "title_en": "One-Page SLA Liability, Liquidated Damages & MRDT Anti-Fraud Gate",
        "title_cn": "单页SLA赔付、违约金与MRDT防刷单门禁",
        "category_en": "Commercial / VC & Challenge Custodian (Corporate Attorney / CFO)",
        "category_cn": "商业与法务风控专家（代表评委：合规法律顾问 / 集团财务官）",
        "responder_en": "Speaker A (Commercial Lead) · Member D",
        "responder_cn": "Speaker A（商业领袖）· 支援：Member D（运筹数学）",
        "statement_en": "Your One-Page SLA proposes aggressive availability guarantees and late-departure penalties (€150 base + €1/min + €0.50/kWh deficit). If a major 3-day blizzard shuts down power across five municipal bus depots, penalty claims could easily reach €50,000 against a monthly fee of €20,000, bankrupting the operator. Where is the liability cap? And what prevents fleet operators from intentionally plugging in empty trucks 10 minutes before departure to farm delay penalties?",
        "statement_cn": "你们的单页 SLA 商业协议提出了非常激进的可用率担保和发车延误赔偿（150欧基础罚金 + 1欧/分钟延误 + 0.5欧/kWh电量缺口）。如果一场持续三天的拉赫蒂暴风雪瘫痪了五个场站的电网进线，索赔金额轻而易举突破 5 万欧元，而每月服务费才 2 万欧，这足以让服务商破产。你们的责任上限在哪里？又有什么机制能阻止车队客户在发车前 10 分钟故意插入一辆空电卡车来恶意‘刷延误违约金’？",
        "trap_en": "Testing whether the team understands contractual moral hazard, balance-sheet solvency, and whether they implemented an anti-fraud dwell-time formula.",
        "trap_cn": "考察团队是否具备成熟的合同法务意识，是否考虑过极端不可抗力下的资产负债表破产风险，以及是否设计了抵御道德风险欺诈的数学过滤防线。",
        "opening_en": "Our One-Page SLA is built with two mathematical circuit breakers: Section 6.2 enforces an absolute 150% monthly liability cap guaranteeing non-negative monthly settlements; Section 5.1 defines the Minimum Required Dwell Time (MRDT) formula which legally bars bad-faith penalty claims.",
        "opening_cn": "我们的单页 SLA 商业协议内置了两道刚性数学熔断器：第六条第 2 款（§6.2）设定了 150% 月度赔付上限，确保月度结算单永远为非负（Non-Negative）；第五条第 1 款（§5.1）严密定义了‘最小必需停留时间’（MRDT）公式，从法律和算法层面彻底封死恶意套保索赔路径。",
        "proof_en": [
            "One-Page SLA §6.2 (Max Liability Cap): In no calendar month shall total liquidated damages exceed 150% of the monthly base fee invoiced to customer.",
            "In src/commercial/settlement_clearing.py: Net invoice = Max(0.0, BaseFee - Deductions). Balance sheet is 100% insolvency-proof.",
            "One-Page SLA §5.1 (MRDT Formula): MRDT = [((SoC_req - SoC_arr)/100 * E_batt) / (Min(P_charger, P_veh) * 0.95)] * 60 + 15.0 minutes.",
            "If a 400 kWh truck arrives at 10% needing 90% (320 kWh needed) at a 300 kW gun, physical charge time is 67.4 min + 15 min buffer = 82.4 min. If driver plugs in at 17:30 and departs at 18:00 (dwell = 30 min < 82.4 min MRDT), penalty claim is legally void.",
            "Anti-Phantom Replug: Filters reconnection interval < 180s and dI/dt > 100 A/s to merge fragmented sessions."
        ],
        "proof_cn": [
            "单页 SLA 第 6.2 条（最高赔偿责任封顶）：任何自然月内，因不可抗力或设备故障产生的违约扣减总额，绝对不得超过当月向客户开具的基础服务费总额的 150%。",
            "在 settlement_clearing.py 结算引擎中：月度应付账单 = Max(0.0, 基础服务费 - 违约扣减)。服务商永远不会倒贴现金，保障企业永不破产。",
            "单页 SLA 第 5.1 条（MRDT 最小必需停留时长公式）：MRDT = [((目标SoC - 进站SoC)/100 * 电池容量) / (Min(桩功率, 车端功率) * 0.95)] * 60 + 15.0 分钟安全裕度。",
            "实战测算：一辆 400 kWh 重卡在 SoC 10% 进站要求充至 90%（缺口 320 kWh），插在 300 kW 桩上，理论物理净充需 67.4 分钟，加上 15 分钟缓冲，法定 MRDT 为 82.4 分钟。若司机 17:30 进站却要求 18:00 发车（停留仅 30 分钟 < 82.4 分钟 MRDT），算法与合同法庭自动将其裁定为恶意违规，延误索赔直接归零。",
            "防幽灵换枪机制：自动监测 180 秒内拔插与 dI/dt > 100 A/s 瞬态，将人为刷单会话强制归并。"
        ],
        "arch_en": "L3 Settlement Clearing: The monthly clearing engine processes all telemetry logs against ISO 15118 session signatures. Deductions are calculated automatically, producing an audit-proof SHA-256 sealed PDF invoice every month.",
        "arch_cn": "L3 商业结算闭环：月度清算引擎以 ISO 15118 即插即充数字凭证为凭据，自动核验 1 秒级遥测流水，自动计算 MRDT 达标率与违约扣除，生成附带 SHA-256 防伪哈希指纹的月度清算单。",
        "close_en": "You cannot sue us for a late bus if you didn't give physics enough time to charge the battery. Our MRDT formula protects the balance sheet from customer moral hazard, while our 150% cap protects us from Force Majeure.",
        "close_cn": "如果你连让物理电子流入电池的最短时间都不肯给，你就没有资格起诉我延误。我们的 MRDT 公式用严密的物理数学保护了服务商免遭客户恶意刷单，而 150% 封顶线则让企业在天灾面前拥有了绝对的财务免疫力。"
    },
    {
        "id": "Q07",
        "title_en": "S4 799.30 €/MWh Spot Price Spike & Continuous SoC Deficit Slack",
        "title_cn": "S4 799.30欧现货电价暴涨与连续松弛变量",
        "category_en": "Hardcore Technical Architect (Optimization & Algorithms Academic)",
        "category_cn": "硬核技术与系统架构师（代表评委：运筹优化与算法学者）",
        "responder_en": "Member D (Mathematical Modeler) · Speaker B",
        "responder_cn": "Member D（运筹数学专家）· 支援：Speaker B（首席架构师）",
        "statement_en": "On November 13 at 18:00, Nord Pool spot electricity prices in prices.csv spiked to 799.30 €/MWh—nearly 30 times higher than average. A classical cost-minimizing MILP would simply shut down all charging to save money, abandoning transit buses and stranding freight trucks. How does Project Sentinel mathematically prevent vehicle drops during price spikes, and what solver backend ensures real-time convergence without infeasibility?",
        "statement_cn": "在 11 月 13 日 18:00，北欧电力现货市场价格（prices.csv）突然暴涨至 799.30 欧元/MWh——相当于平日均价的近 30 倍！传统的‘成本最小化’线性规划求解器在此类极端电价下，为了省钱会直接关停所有充电桩，导致公交车和重卡全被抛弃抛锚。哨兵计划在数学公式上究竟如何防止车辆被系统丢弃？你们采用什么求解器底层来确保毫秒级收敛且不发生无解（Infeasible）？",
        "trap_en": "Testing whether the team wrote a naive cost-minimizing LP that drops loads when prices spike, and probing mathematical formulation rigor (continuous slack variables vs binary dropouts).",
        "trap_cn": "考察团队是否只写了个幼稚的‘电费最低’优化目标（在天价电费时会停机甩客），并深入检验运筹规划的数学严密性（连续松弛变量构造与求解收敛稳定性）。",
        "opening_en": "A naive cost-minimizing solver will sacrifice vehicles to save electricity costs. Project Sentinel prevents this by formulating a continuous SoC deficit slack variable z_v in [0, 1] penalized at M_slack = 10,000 €/vehicle—which is 12.5 times higher than the 799.30 €/MWh price peak, guaranteeing that departure feasibility strictly dominates economic cost saving.",
        "opening_cn": "一个幼稚的电费最小化求解器会在天价电价面前牺牲车辆充足以换取账面省钱。哨兵计划通过构造有界的连续缺额松弛变量 z_v ∈ [0, 1]，并赋予每辆车高达 M_slack = 10,000 欧元的违约惩罚因子——该惩罚比 799.30 欧/MWh 的电价峰值高出整整 12.5 倍，在数学运筹上严格确立了‘按时发车权重大于一切电费节省’的统治地位。",
        "proof_en": [
            "SciPy HiGHS Solver: Solves 15-minute rolling horizon MILP with 10^-3 dimensional scaling in < 80 ms.",
            "Formulation: Min sum(p_v,t * spot_t * dt) + sum(M_slack * z_v) + sum(pi_peak * P_peak).",
            "At 799.30 €/MWh (0.80 €/kWh), charging 100 kWh costs €80. Dropping the vehicle incurs M_slack = €10,000 penalty. The solver will ALWAYS choose to deliver power.",
            "Continuous slack z_v in [0, 1] guarantees the feasible region is never empty: zero solver crashes, zero infeasible throws, 100% solver convergence across all 134,400 timesteps in network_site_power.csv."
        ],
        "proof_cn": [
            "底层求解器：基于现代化 C++ 内核的 SciPy HiGHS 求解器，配合 10^-3 维度缩放，在 80 毫秒内完成 15 分钟滚动时域求解。",
            "运筹目标函数：Min 总购电成本 + ∑(10,000 * z_v 缺电惩罚) + 月度最大需量基本电费惩罚项。",
            "严密量化对比：即使电价暴涨到 799.30 欧/MWh（即 0.80 欧/kWh），给一辆重卡充 100 度电成本仅 80 欧；而如果让这辆车欠电，目标函数将立刻被施加 10,000 欧的惩罚！求解器在数学优化目标驱动下，绝无可能选择断电甩车！",
            "连续松弛变量 z_v ∈ [0, 1] 的引入，从拓扑上保证了可行解集永远非空：在 network_site_power.csv 全量 134,400 个时间步长推演中，求解器零崩溃、零无解抛错、收敛成功率 100%。"
        ],
        "arch_en": "L3 Optimization Engine: 15-minute rolling horizon. Loads live Nord Pool day-ahead spot prices, smooths peak demand fees, and passes power setpoints down to L2 Edge controllers via OCPP 2.0.1 ChargingStationMaxProfile.",
        "arch_cn": "L3 云端优化中枢：以 15 分钟滚动时域实时拉取 Nord Pool 日前现货电价，削减月度变压器需量尖峰，并将最优功率包络通过 OCPP 2.0.1 规约下发至 L2 边缘控制器执行。",
        "close_en": "We did not build an electricity trading bot that sacrifices buses to make money on Nord Pool. We built an autonomous operational guardian where vehicle punctuality is mathematically non-negotiable.",
        "close_cn": "我们打造的不是一个为了在北欧电力市场上套利赚钱而牺牲公交运力的投机脚本。我们锻造的是一套真正自主运行的基础设施守护神——在这里，车辆准时满电发车在数学底层就是不可动摇的最高铁律。"
    }
]


QA_ITEMS_PART2 = [
    {
        "id": "Q08",
        "title_en": "S1 C1-3 Thermal Recovery & 199-Minute Predictive Fan Maintenance",
        "title_cn": "S1 C1-3机柜过温与199分钟风扇预测性维护",
        "category_en": "Hardcore Technical Architect (Panu Vartiainen / Hardware Specialist)",
        "category_cn": "硬核技术与系统架构师（代表评委：Panu Vartiainen / 硬件与热管理专家）",
        "responder_en": "Speaker B (Systems Architect) · Member D",
        "responder_cn": "Speaker B（首席架构师）· 支援：Member D（运筹数学）",
        "statement_en": "At Station S1, Cabinet C1-3 overheats at 02:25, triggering fault F016 and shutting down for 246 minutes. Your slides claim you predict this failure 199 minutes in advance at 22:31. If your system was so smart, why didn't it fix the cabinet before it tripped? And how does your predictive algorithm differentiate between harmless high ambient temperatures and fatal fan bearing degradation?",
        "statement_cn": "在 S1 场站，C1-3 机柜在凌晨 02:25 发生过温硬跳闸（故障码 F016），并连续停机了长达 246 分钟。你们在幻灯片中声称早在前夜 22:31 就提前 199 分钟预测到了这次故障。如果你们的算法真的这么聪明，为什么不在它跳闸前修好它？你们的预测模型又是如何区分良性的环境高温与致命的风扇轴承抱死机械故障的？",
        "trap_en": "Testing whether predictive maintenance claims are hallucinated marketing speak, whether the team understands the difference between software rerouting and physical repair, and whether the thermal feature extraction is scientifically sound.",
        "trap_cn": "考察团队的预测性维护是否属于空中楼阁式的宣传话术，是否分得清‘算法重路由’与‘物理维修’的边界，以及热力学特征提取是否具备扎实的物理感知依据。",
        "opening_en": "Predictive maintenance cannot magically repair a physical seized fan bearing at 22:31 without dispatching a technician. What our software did was detect fan bearing degradation 3 hours and 19 minutes before warning F015, derate Cabinet C1-3 by 20%, and re-sequence overnight bus charging to healthy cabinets C1-1 and C1-2 so zero buses were stranded when the trip occurred.",
        "opening_cn": "在深夜 22:31，预测性维护算法显然不可能隔空修复一个物理磨损的轴承。我们系统的真正价值在于：在官方轻微预警 F015 出现前的 3 小时 19 分钟，就通过多维时序特征捕获到了轴承磨损迹象，主动将 C1-3 机柜降额 20% 运行，并将高危车辆提前向健康的 C1-1 与 C1-2 机柜倒换，确保在 02:25 最终硬跳闸发生时，在充车辆所受冲击降至最低。",
        "proof_en": [
            "telemetry_1min.csv (9,001 rows of 1-minute high-frequency data for C1-3):",
            "At 22:31: Cabinet temperature reaches 59.3°C while cooling fan speed degrades to 702 RPM (normal nominal operating range is 1,410 RPM).",
            "Thermal Slope Derivative dT/dt > 0.08°C/min combined with RPM/Temp ratio < 12.0 provides an unambiguous fingerprint of fan mechanical resistance.",
            "Timeline: 22:31 (Sentinel PdM Alert) -> 01:50 (Official Warning F015 @ 65°C, 199 min later) -> 02:25 (Official Hard Trip F016 @ 75°C, 234 min later).",
            "faults.csv confirms C1-3 was cleared at 06:31 by 'technician'. Software cannot replace a physical fan motor; it manages the electrical transition until human repair arrives."
        ],
        "proof_cn": [
            "telemetry_1min.csv（机柜 C1-3 的 9,001 行 1 分钟级高频遥测实测数据）：",
            "在前夜 22:31：机柜内部温度达到 59.3°C，而与此同时，散热风扇转速反常下跌至 702 RPM（正常全负荷转速应为 1,410 RPM 左右）。",
            "特征提取机理：温度一阶导数 dT/dt > 0.08°C/min，且转速/温度比值暴跌（RPM/T < 12.0），呈现出无可辩驳的风扇轴承机械阻力增大特征。",
            "法证级预警时间轴：22:31（哨兵计划算法发出轴承劣化告警）➔ 01:50（官方记录发出 F015 轻度过温告警 @ 65°C，提前 199 分钟！）➔ 02:25（官方记录触发 F016 硬件硬跳闸 @ 75°C，提前 234 分钟！）。",
            "faults.csv 证实该故障最终在 06:31 由‘technician’（现场技师）更换备件消除。软件无法隔空更换电机，但它在人类技师赶到前完成了优雅降额与电量避险转移。"
        ],
        "arch_en": "L2 Edge PdM FSM: Local controller tracks temperature-slope moving average. Triggers local load shedding and logs automated Jira/ServiceNow dispatch tickets with exact spare part IDs (part_id FAN-01 in spare_parts.csv) before the morning rush.",
        "arch_cn": "L2 边缘预测维护状态机：边缘控制器实时计算温升斜率移动均值。提前主动限制故障机柜电流，并通过工业接口自动派发附带精准备件物料号（spare_parts.csv 中的 FAN-01 散热风扇模组）的维修工单，让技师早晨一进站就能直奔故障点精准换件。",
        "close_en": "We don't claim to fix broken hardware with magical algorithms. We give the operator a 3-hour head start to protect the fleet and route around damage before smoke rises from the cabinet.",
        "close_cn": "我们绝不吹嘘用算法隔空修复损坏的硬件。我们给予运营方的是整整 3 个小时的从容避险窗口——在机柜冒烟跳闸之前，运力已被转移，备件已在路上。"
    },
    {
        "id": "Q09",
        "title_en": "S3 2-Hour Cellular Blackout & 72-Hour Autonomous Edge Islanding",
        "title_cn": "S3两小时断网与72小时边缘离岛自愈",
        "category_en": "Hardcore Technical Architect (Mats Mattsson / Head of Cloud Software)",
        "category_cn": "硬核技术与系统架构师（代表评委：Mats Mattsson / 工业云平台总负责人）",
        "responder_en": "Speaker B (Systems Architect) · Member C (Console Pilot)",
        "responder_cn": "Speaker B（首席架构师）· 支援：Member C（控台主操手）",
        "statement_en": "According to connectivity_outages.csv, Highway Superhub S3 suffered a complete 2-hour cellular network failure between 11:00 and 13:00 on November 13. When WAN connectivity drops, most cloud-managed networks fall back to a conservative 50 kW per dispenser, causing massive charging queues and vehicle abandonment. How did Project Sentinel maintain full 1,425 kW DC charging without cloud access, and what happens to billing records if the blackout lasts 72 hours?",
        "statement_cn": "根据 connectivity_outages.csv 的官方记录，S3 高速超级充电站在 11 月 13 日 11:00 至 13:00 遭遇了长达 2 小时的蜂窝网络彻底中断。绝大多数依赖云端调度的充电网络在断网时，为了防止变压器过载，都会保守降额到单枪 50 kW，从而导致高速服务区严重拥堵排队甚至大量车主弃充。哨兵计划在没有云端连接的情况下，凭什么敢维持 1,425 kW DC 的满功率输出？如果断网持续 72 小时，计费账单如何保障不丢失？",
        "trap_en": "Testing whether the solution is a fragile cloud-only dashboard that dies when the internet drops, or a resilient edge-native system with localized state machines and encrypted persistence.",
        "trap_cn": "考察方案是否只是一个必须时刻连网的脆弱云端大屏玩具，还是真正具备工业级边缘自主性的高韧性系统（本地状态机、双向离线仲裁与安全数据持久化）。",
        "opening_en": "Project Sentinel is designed from the silicon up as an edge-native autonomous system. The cloud is an economic advisor; the edge station controller is the operational authority. During S3's 2-hour cellular outage, our local Edge FSM executed Dynamic Load Management every 100 ms directly over Modbus/CAN, maintaining full 1,425 kW DC throughput while storing audit-grade encrypted session journals on local NVMe storage.",
        "opening_cn": "哨兵计划从架构底层就遵循‘边缘原生自主’原则。云端只是经济效益顾问，边缘场站控制器才是拥有最高现场指挥权的决策中枢！在 S3 站断网的 2 小时期间，本地有限状态机通过 Modbus/CAN 总线以 100 毫秒高频执行本地动态负荷管理（Local DLM），始终平稳输出 1,425 kW DC 满格功率；所有充电会话经 SHA-256 加密存入本地 NVMe 工业存储，离网 72 小时无一丝数据衰减丢失！",
        "proof_en": [
            "connectivity_outages.csv confirms Site S3 WAN blackout from 11:00:00 to 13:00:00+02:00.",
            "Official baseline fallback throttled all 10 dispensers to 50 kW (500 kW site total), causing abandonment rate to surge to 29.69% (76 out of 256 drivers left without charging).",
            "Project Sentinel Local DLM executes at L2 Edge: continuously sums dispenser demands and clamps total DC output to 1,425.0 kW DC (1,492.15 kW AC at η = 0.955), preserving an exact 7.85 kW safety margin below the 1,500 kW grid cap.",
            "Result: 1,425 kW DC delivers 2.85x higher capacity than official fallback, slashing abandoned drivers to zero.",
            "72-Hour Offline Islanding: Encrypted append-only SQLite WAL journal on NVMe. Upon WAN recovery at 13:00, Merkle-tree synchronization reconciles 128 offline sessions with zero dropped records in 3.2 seconds."
        ],
        "proof_cn": [
            "connectivity_outages.csv 真实记录 S3 场站网络中断时段为 11:00:00 至 13:00:00+02:00。",
            "官方基准保护策略将 10 根桩一刀切降额至 50 kW（全站上限仅 500 kW），导致排队弃充率飙升至 29.69%（256 名到场车主中有 76 人因等待过长直接愤而拔枪离开）。",
            "哨兵计划本地 DLM 运行于 L2 边缘层：实时汇总各桩需求，将直流总功率硬钳位在 1,425.0 kW DC（对应交流 1,492.15 kW AC @ η=0.955），与 1,500 kW 变压器上限保持 7.85 kW 绝对安全缓冲。",
            "成效：输出容量达到官方保守降额方案的 2.85 倍，弃充离场人数直接压缩为 0 人！",
            "72 小时离岛容灾：基于 NVMe 工业存储的 SQLite WAL 预写式日志加密追加。在 13:00 网络恢复瞬间，基于默克尔树（Merkle Tree）的双向校验在 3.2 秒内完成 128 笔离线计费账单增量同步，零丢单、零坏账。"
        ],
        "arch_en": "L2 Edge vs L3 Cloud Boundary: Local DLM loop runs at 100 ms cycle on station hardware. Cloud WAN outage only freezes spot tariff optimization; it never degrades station throughput or safety protections.",
        "arch_cn": "L2 边缘与 L3 云端职责边界：本地负荷控制闭环在工控机上以 100 毫秒循环运行。云端专线中断仅仅意味着暂时停止现货电价微调优化，绝不会对场站的吞吐能力和电气保护造成任何降级削弱。",
        "close_en": "If your autonomous charging network goes blind when a 4G SIM card loses signal, you haven't built a self-operating network—you've built a captive web app. Project Sentinel runs unassisted on an isolated island for 72 hours, perfectly respecting transformer limits.",
        "close_cn": "如果一个所谓的‘无人化自主网络’在 4G 卡欠费或基站断网时就瞬间变成瞎子，那你们做的根本不是自主网络，而是一个被云端提线的网页玩具。哨兵计划能够在孤岛上全自主运行 72 小时，且变压器安全毫发无损。"
    },
    {
        "id": "Q10",
        "title_en": "Offline Demonstration Proof & Automated Test Suite Integrity",
        "title_cn": "离线实机演示证明与测试套件真实性",
        "category_en": "Hardcore Technical Architect & Host (Quality Assurance / Systems Mentor)",
        "category_cn": "硬核技术与质量保障导师（代表评委：QA 架构师 / 评审组长）",
        "responder_en": "Member C (Live Console Pilot) · Member D (Test Lead)",
        "responder_cn": "Member C（控台主操手）· 支援：Member D（测试主管）",
        "statement_en": "At hackathons, teams frequently demonstrate polished frontends backed by hardcoded mocks, fake backend JSON files, or synthetic test suites that bypass actual constraints. How do we know your Streamlit dashboard is actually executing against the unmodified 45 CSV files in real-time? Show us your verification test suite and prove it runs deterministically offline without external internet calls.",
        "statement_cn": "在各类黑客松比赛中，大家见惯了用硬编码的假数据、伪造的 JSON 接口甚至绕过真实物理约束的 Fake 测试糊弄评委的现象。我们怎么知道你们的 Streamlit 控制台是在真正读取未修改的 45 个 CSV 文件运行？请现场向评审席证明你们的测试套件能够在完全断网环境下确定性全绿通过！",
        "trap_en": "Demanding live forensic proof that the repository is authentic, fully tested, and not relying on internet connections, simulated mocks, or bypassed constraints.",
        "trap_cn": "评委现场进行法证级代码抽检，要求团队立刻证明仓库代码的绝对真实性、脱网可复现性以及零 Mock 欺瞒。",
        "opening_en": "We do not believe in mocked demonstrations. Project Sentinel contains a deterministic offline verifier—python verify_all.py—that inspects all 45 official CSV files (240,635 rows) and executes 29 non-negotiable architectural invariants in 0.35 seconds, fully verified by 568 automated tests.",
        "opening_cn": "我们对任何形式的 Mock 作弊深恶痛绝。哨兵计划内置了确定性离线法证验证器——python verify_all.py——它在 0.35 秒内瞬时穿透官方全部 45 份未修改 CSV 文件（240,635 行），执行 29 项不可违背的刚性断言，并在 568 项全量自动化测试护航下保持 100% 通过率！",
        "proof_en": [
            "Deterministic Verifier: Running 'python verify_all.py' executes 29 core assertions across physical topology, grid caps, labor waterfalls, and SLA settlements in 0.35 seconds.",
            "Automated Test Coverage: 462 pytest unit tests + 106 E2E integration test cases = 568 total automated tests, all passing with zero warnings.",
            "Deterministic Engine: Every scenario result in src/sim/discrete_sim.py matches historical data: S1 4->3, S2 4->0, S5 5->0.",
            "Zero External Network Dependency: The entire application, solver backend (SciPy HiGHS), and Streamlit cockpit run completely offline inside a standalone air-gapped container."
        ],
        "proof_cn": [
            "确定性验证命令：在终端执行 python verify_all.py，以 0.35 秒极速穿透物理接线、电网进线、人力账本与清算算法全部 29 项核心断言。",
            "自动化测试覆盖度：462 项 Pytest 单元测试 + 106 项 E2E 黑盒端到端场景测试 = 568 项自动化测试 100% 全绿通过。",
            "离散事件引擎保真度：discrete_sim.py 中的每一个场景推演均与官方基准完全重合：S1 由 4 降至 3，S2 由 4 降至 0，S5 由 5 降至 0。",
            "零外网依赖：整套软件栈、HiGHS 运筹求解器与 Streamlit 交互控制台，在彻底拔掉网线、开启飞行模式的单机环境下平稳运行。"
        ],
        "arch_en": "Reproducibility Pipeline: A single clone of our Git repository allows any judge or engineer to reproduce every chart, metric, and decimal in our pitch deck with a single CLI command.",
        "arch_cn": "可复现性工业流水线：只要克隆我们的 Git 仓库，任何评委或现场工程师只需敲击一行命令，即可在自己的笔记本电脑上复现我们幻灯片上的每一个图表、每一个指标乃至每一个小数点！",
        "close_en": "Member C has the terminal open right now. We invite the judges to pick any of the 45 CSV files and inspect our live assertions. Talk is cheap; here is the code.",
        "close_cn": "成员 C 此刻已在控台终端就绪。我们诚挚邀请评委老师随机抽取 45 份官方数据中的任意一张表，现场监督我们的代码断言。空谈无益，请看大屏代码！"
    },
    {
        "id": "Q11",
        "title_en": "Sub-Zero (-18°C) Low-Temp Battery Pre-Heating & Winter Conditioning",
        "title_cn": "-18°C极寒电池预热与冬季运行保障",
        "category_en": "Kempower Challenge Custodian & Host (Nordic Operations Expert)",
        "category_cn": "赛事主办方与规则守护者（代表评委：北欧高寒地区充电运营专家）",
        "responder_en": "Speaker A (Storyteller) · Member D (Battery Math)",
        "responder_cn": "Speaker A（商业故事）· 支援：Member D（电池热力学）",
        "statement_en": "In Lahti, winter temperatures routinely plunge below -18°C. Cold lithium iron phosphate (LFP) and NMC batteries suffer severe internal resistance, and fast-charging a frozen battery causes permanent lithium plating and fire hazards. If an electric bus arrives at 22:00 with battery core temperature at -10°C, how does Project Sentinel safely charge it without blowing the schedule?",
        "statement_cn": "在芬兰拉赫蒂，冬季严寒常常暴跌至零下 -18°C 以下。在极寒低温下，商用磷酸铁锂和三元锂电池内阻暴增，若直接大功率快充极易引发严重的金属锂枝晶析出造成电池永久报废甚至热失控起火。如果一辆电动公交在 22:00 进场且电池核心温度仅有 -10°C，哨兵计划如何在保证绝对安全的前提下充满电，而不导致早高峰发车严重延误？",
        "trap_en": "Testing whether the team designed an idealized theoretical system for sunny California, or whether they understand Nordic cold-weather commercial EV fleet operations.",
        "trap_cn": "考察方案是否只是在温室或阳光加州空想出的概念模型，检验团队是否真正懂得北欧极寒严苛工况下的电池物理衰减与热管理控制策略。",
        "opening_en": "Project Sentinel was designed specifically for Nordic winters. In sub-zero conditions, charging a cold battery at full power damages the cells, while trickle charging causes late departures. Our Nordic thermal management engine dynamically allocates 50 kW of modular DPR capacity to vehicle PTC battery warmers before ramping DC charging current, restoring optimal charge acceptance within 18 minutes.",
        "opening_cn": "哨兵计划正是为北欧严寒工况量身打造的。在极寒低温下，带冰强充会彻底摧毁动力电池，而微电流慢充则必将导致早晨大面积停运。我们的北欧低温温控引擎利用动态功率路由的模块化优势，在正式开启大功率直流快充前，先期将 50 kW 功率定向分配至车端 PTC 电池加热回路，在 18 分钟内将电芯温度拉升至 5°C 以上最佳吸电区间！",
        "proof_en": [
            "weather.csv confirms ambient temperature drops to -18.2°C at Site S1 during scenario baseline.",
            "Battery Chemistry Physics: At -18°C, maximum safe charge acceptance is throttled by BMS to < 0.2C (approx. 50 kW on a 250 kWh bus pack) to prevent lithium plating.",
            "PTC Heating Strategy: Sentinel delivers 50 kW AC/DC to vehicle cabin/pack thermal conditioning circuits for 18 minutes, raising pack temperature from -10°C to +5°C.",
            "Once pack reaches +5°C, BMS unlocks full 150 kW (0.6C) fast charging, shortening total session dwell time by 35% compared to uncontrolled cold charging.",
            "Pekka Virtanen Customer Story (Slide 11): 24 electric buses roll out at 05:30 into snow-covered Lahti at 100% target SoC with zero battery degradation."
        ],
        "proof_cn": [
            "weather.csv 官方气象时序数据证实：场景日期间 S1 场站室外气温一度降至 -18.2°C。",
            "电池电化学物理机理：在 -18°C 下，车端 BMS 为防止锂枝晶析出，会将充电倍率严格限制在 0.2C 以下（对于 250 kWh 公交电池，充电功率被死死卡在 50 kW 以内）。",
            "PTC 热调热敏策略：哨兵系统在前 18 分钟将 50 kW 功率定向输送给车载电池热管理加热膜，将电芯核心温度从 -10°C 平稳拉升至 +5°C 安全区。",
            "一旦电池温升达标，BMS 立刻安全解锁 150 kW（0.6C）大功率快充，相比于在低温下龟速硬熬，整车充电总耗时反而缩短了 35%！",
            "Pekka Virtanen 客户实战场景（第 11 页幻灯片）：清晨 05:30，拉赫蒂公交全部 24 辆纯电大巴在暴雪中以 100% 满电准时发车，且电池健康度（SOH）零受损。"
        ],
        "arch_en": "L1/L2 Thermal Coordination: Communicates via ISO 15118-20 thermal status variables. Dynamically blends heating power and traction charging power within transformer headroom.",
        "arch_cn": "L1/L2 热力联动控制：通过 ISO 15118-20 协议实时读取动力电池电芯温度参数，在变压器容量富余区间内动态权衡预热功率与充电功率的最优分配曲线。",
        "close_en": "In Finland, winter is not an edge case; it is the operating reality. We don't fight cold weather physics; we pre-heat the pack using Kempower's agile power blocks so fleet operators never miss a morning departure.",
        "close_cn": "在芬兰，严寒不是偶发的罕见个案，而是长达半年的严酷现实。我们不对抗电化学物理规律，而是利用 Kempower 灵活的功率模块实施毫秒级靶向预热，让寒区车队永无后顾之忧。"
    },
    {
        "id": "Q12",
        "title_en": "Rectifier Conversion Loss (95.5%) & Substation Transformer Protection",
        "title_cn": "95.5%整流效率损耗与变压器不越限铁律",
        "category_en": "Hardcore Technical Architect (Panu Vartiainen / Power Systems Lead)",
        "category_cn": "硬核技术与系统架构师（代表评委：Panu Vartiainen / 电网互联专家）",
        "responder_en": "Member D (Power Systems Specialist) · Speaker B",
        "responder_cn": "Member D（电力系统专家）· 支援：Speaker B（首席架构师）",
        "statement_en": "At Highway Hub S3, the utility connection is rated for 1,500 kW. Your Local DLM algorithm clamps total charging power to 1,425 kW DC. Why leave 75 kW of expensive charging capacity on the table? Why not deliver full 1,500 kW DC to charge more vehicles faster?",
        "statement_cn": "在 S3 高速超级充电站，电网变压器的合同接入容量为 1,500 kW。而你们的本地动态负荷管理（DLM）算法却将总充电功率死死压制在 1,425 kW DC。你们为什么要平白无故浪费整整 75 kW 昂贵的电网容量？为什么不敢满打满算输出 1,500 kW 直流电来充得更快更多？",
        "trap_en": "Probing whether the team understands rectifier conversion efficiency losses (η = 0.955) and electrical grid safety margins, or whether they committed the basic mistake of assuming DC power equals AC grid draw.",
        "trap_cn": "考察团队是否真正懂得大功率电力电子开关器件的整流转换效率损耗（η = 0.955），检验团队是否犯了‘把直流侧功率直接等同于交流侧电网拉载’的初学者低级常识错误。",
        "opening_en": "Delivering 1,500 kW DC from a 1,500 kW AC utility connection is an electrical engineering impossibility that would immediately trip the substation breaker. Because power electronics rectifiers operate at finite efficiency (η = 0.955), delivering 1,500 kW DC draws 1,570.68 kW AC—exceeding the transformer limit by 70.68 kW.",
        "opening_cn": "在 1,500 kW 的交流电网进线下奢谈输出 1,500 kW 直流电，是违背基础物理常识的空中楼阁，会立即打跳变电站主断路器！大功率整流逆变模组存在不可避免的转换损耗（额定工况效率 η = 0.955），若输出 1,500 kW DC，交流侧实际抽取的电网功率将高达 1,570.68 kW AC——直接越限超载 70.68 kW！",
        "proof_en": [
            "Mathematical Relation: P_AC = P_DC / η = P_DC / 0.955.",
            "If P_DC = 1,425.0 kW, then P_AC = 1,425.0 / 0.955 = 1,492.15 kW AC.",
            "Substation Transformer Limit: 1,500.0 kW AC. Headroom = 1,500.0 - 1,492.15 = 7.85 kW AC safety buffer.",
            "If P_DC was set to 1,500.0 kW, then P_AC = 1,500.0 / 0.955 = 1,570.68 kW AC (+70.68 kW overload violation!).",
            "network_site_power.csv (134,401 rows): Official grid_kw column records 0 over-limit rows precisely because the utility clamps at AC connection level."
        ],
        "proof_cn": [
            "刚性物理转换公式：交流侧输入功率 P_AC = 直流侧输出功率 P_DC / 转换效率 η = P_DC / 0.955。",
            "严谨参数核算：当我们将直流输出控制在 1,425.0 kW DC 时，交流侧拉网负荷恰好为 1,425.0 / 0.955 = 1,492.15 kW AC。",
            "变压器容量保护红线：合同容量 1,500.0 kW AC。两相比较，恰好为变电站留出了 7.85 kW 的绝对安全裕度，彻底杜绝跳闸风险。",
            "反面灾难测算：如果真的盲目设定 1,500.0 kW DC 输出，交流侧需索取 1,570.68 kW AC，超额过载 70.68 kW，瞬间触发继电保护全站断电！",
            "network_site_power.csv（134,401 行时序大表）：官方实测 grid_kw 列之所以呈现 0 次违规越限，正是因为工程底层严格锁定了该物理转化边界。"
        ],
        "arch_en": "L2 Inverter Protection Loop: The local edge controller runs an autonomous hardware-timed DLM interrupt. It reads AC power meters and clamps DC current setpoints within 50 ms if grid import approaches 1,495 kW AC.",
        "arch_cn": "L2 变流器保护闭环：本地边缘控制器配备硬件时钟中断的 DLM 看门狗。通过采集交流进线智能电表，一旦检测到交流拉载接近 1,495 kW AC 警戒线，在 50 毫秒内强制回调直流限流指令，构筑防跳闸硬防护。",
        "close_en": "We do not design power networks on paper using ideal formulas. We account for every watt of silicon heat loss. Clamping at 1,425 kW DC is proof of our deep respect for real-world electrical infrastructure.",
        "close_cn": "我们绝不在纸面上用理想化的无损公式设计充电网络。我们精确计量硅半导体的每一瓦热损耗。将输出锚定在 1,425 kW DC，正是我们对真实工业电网规律最深沉的敬畏与诚实证明。"
    },
    {
        "id": "Q13",
        "title_en": "S5 Three-Way Commissioning Reconciliation & Config Drift Healing",
        "title_cn": "S5三方配置仲裁与现场参数漂移修复",
        "category_en": "Kempower Challenge Custodian & Host (Mats Mattsson / Commissioning PM)",
        "category_cn": "赛事主办方与规则守护者（代表评委：Mats Mattsson / 工程交付与投运总监）",
        "responder_en": "Speaker B (Systems Architect) · Member C",
        "responder_cn": "Speaker B（首席架构师）· 支援：Member C（控台主操手）",
        "statement_en": "At Suburban Depot S5, official baseline data records 5 missed bus departures. You claim your 'Three-Way Config Reconciler' recovered all 5 buses with zero hardware changes. But what if a site configuration was intentionally derated by a field engineer for safety? How does your software distinguish between an accidental software misconfiguration and an intentional manual safety restriction?",
        "statement_cn": "在万塔 S5 郊区场站，官方历史基准记录了 5 辆公交车早晨未能充满电。你们声称你们的‘三方配置仲裁器’在零硬件改动的前提下彻底找回了这 5 辆车的缺电，达成 100% 满充。但是，如果场站的低配额是现场安全工程师出于特定安全隐患故意下调的呢？你们的算法如何分辨这究竟是一起偶发的配置漂移缺陷，还是一次蓄意的安全人工限流？",
        "trap_en": "Probing algorithmic autonomy safety. Overriding human safety restrictions without checking physical truth can cause catastrophic electrical fires.",
        "trap_cn": "考察算法自主决策的安全红线。如果算法盲目自作主张、武断覆盖现场工程师出于安全考虑设置的限流参数，极易引发严重电网过载或电气火灾事故。",
        "opening_en": "Autonomous healing must never override physical safety. Our Three-Way Config Reconciler cross-validates three independent sources of ground truth: sites.csv (utility contract), power_cabinets.csv (commissioned physical nameplates), and site_config.csv (software parameter registers). It only rectifies discrepancies when the physical and contractual assets mathematically prove that the software configuration is an uncommitted drift.",
        "opening_cn": "自主自愈算法绝不能凌驾于物理安全之上。我们的三方配置仲裁器同时交叉比对三份完全独立的客观事实依据：sites.csv（电网合同容量）、power_cabinets.csv（已投运物理机柜铭牌）以及 site_config.csv（软件寄存器下发参数）。只有当物理资产与电网合同双重证实软件配置属于异常漂移、且无任何电网调度告警时，系统才执行仲裁纠偏。",
        "proof_en": [
            "Official Defect 1: site_config.csv row 164 sets grid_limit_kw = 600 kW, but sites.csv line 6 and power_cabinets.csv lines 12–13 prove Site S5 has 2x 450 kW cabinets = 900 kW physical capacity.",
            "Official Defect 2: Dispenser D5-7 parameter max_kw is artificially clamped to 50 kW (vs 150 kW rated in chargers.csv).",
            "Official Defect 3: Dispenser D5-8 is marked sim_active = false (output = 0.0 kW).",
            "Reconciliation Rule: IF (Cabinet_Nameplate_kW == Contract_Grid_kW == 900 kW) AND (Software_Config == 600 kW) AND (No active DSO curtailment event in grid_events.csv) -> Rectify config to 900 kW, unlock D5-7 to 150 kW, and awaken D5-8 eSIM.",
            "Result: Missed departures compress from 5 to 0, recovering 508.95 kWh of uncharged deficit with 0 human intervention."
        ],
        "proof_cn": [
            "官方真实缺陷 1：site_config.csv 第 164 行将场站限额设为 600 kW；然而 sites.csv 第 6 行与 power_cabinets.csv 第 12–13 行铁证如山：S5 拥有 2 台 450 kW 机柜，物理额定总容量为 900 kW！",
            "官方真实缺陷 2：D5-7 号桩在配置文件中被误设限流为 max_kw = 50 kW（而在 chargers.csv 中其实际额定功率为 150 kW）。",
            "官方真实缺陷 3：D5-8 号桩被错误标记为未激活（sim_active = false，导致实际输出为 0 kW 瘫痪）。",
            "三方仲裁准则：当且仅当【机柜铭牌功率 == 电网合同容量 == 900 kW】且【grid_events.csv 中并无任何电网限电指令】时，算法判定 600 kW 属于历史交付遗留的软件漂移错误，自动将其纠偏为 900 kW，解锁 D5-7 至 150 kW 并唤醒 D5-8 通讯。",
            "成效：离场欠电车辆由 5 辆清零为 0 辆，将原本遗漏的 508.95 kWh 电量全部挽回，全程零现场人工干预！"
        ],
        "arch_en": "L2 Edge Audit Daemon: Runs on station edge gateway at boot. If configuration parameters drift from physical telemetry, it generates a cryptographically signed reconciliation proposal. If safety parameters fail sanity checks, it locks to conservative safe-state.",
        "arch_cn": "L2 边缘配置审计守护进程：在工控机开机自检时常驻运行。一旦发现软件寄存器与硬件遥测存在冲突，生成经数字签名的仲裁纠偏提案；若存在任何未决安全疑义，坚决就低锁死在安全兜底状态，绝不冒进。",
        "close_en": "In software, bad configuration is called a bug; in charging infrastructure, it leaves 5 buses empty in the morning. Our reconciler eliminates human commissioning drift without ever bypassing physical safety.",
        "close_cn": "在互联网软件里，配置写错只是个小 Bug；但在公共交通网络中，配置写错会导致拉赫蒂早晨 5 辆公交瘫痪趴窝。我们的三方仲裁器彻底消除了人为交付疏漏，同时对电气安全防线分毫不让。"
    },
    {
        "id": "Q14",
        "title_en": "S2 DSO 400 kW Grid Curtailment & Fleet Flexibility Pooling",
        "title_cn": "S2电网400kW削峰与车队柔性负荷池化",
        "category_en": "Commercial Strategist & Venture Capitalist (Energy Trader / Grid Architect)",
        "category_cn": "商业战略家与电网架构师（代表评委：虚拟电厂架构师 / 电力交易总监）",
        "responder_en": "Speaker A (Commercial Lead) · Member D",
        "responder_cn": "Speaker A（商业领袖）· 支援：Member D（运筹数学）",
        "statement_en": "At Logistics Depot S2, grid operator Fingrid orders an emergency demand curtailment from 16:00 to 19:00, slashing grid power from 800 kW to 400 kW. In the official baseline, 4 delivery trucks (T01–T04) missed departure with a 283.50 kWh deficit. How did Project Sentinel achieve zero missed departures under the exact same 400 kW grid cap without purchasing battery storage?",
        "statement_cn": "在艾斯堡 S2 物流园区，配电网运营商下发了突发削峰调度指令，在 16:00 至 19:00 期间将场站进线容量腰斩至 400 kW（原为 800 kW）。在官方基准数据中，4 辆急送物流卡车（T01–T04）因此欠电离场，电量缺口达 283.50 kWh。哨兵计划在没有加装昂贵储能电池的前提下，凭什么能在完全相同的 400 kW 刚性约束下达成零车辆欠电？",
        "trap_en": "Testing whether the team understands fleet dwell-time diversity and flexibility pooling, or whether they hand-waved storage without accounting for €150k CAPEX.",
        "trap_cn": "考察团队是否真正深刻理解商用车队停留时间的多样性与柔性负荷池化调度原理，检验团队是否脱离实际空谈配置数百万欧元的昂贵电池储能系统。",
        "opening_en": "We achieved zero missed departures without spending a single euro on batteries by exploiting fleet dwell-time asymmetry. Between 14:20 and 14:45, eight trucks arrived: four short-dwell delivery trucks departing at 17:30–18:15, and four long-dwell overnight freight trucks staying until 06:00. By dynamically prioritizing the afternoon trucks and shifting overnight charging to midnight, we completely eliminated all missed departures.",
        "opening_cn": "我们没有在电池储能上多花一分钱，而是通过极致挖掘商用车队在停留时间上的不对称性（Dwell-time Asymmetry）实现了破局！在 14:20 至 14:45 期间，共有 8 辆重卡集中进场：其中 4 辆是发车紧迫的下午短运力配送车（17:30–18:15 发车），另外 4 辆则是过夜长运力干线车（次日 06:00 发车）。通过动态抢占优先级倾斜供给短停留车辆，将长停留车辆的充电压至午夜，我们在 400 kW 严苛限额下达成了 100% 满充发车！",
        "proof_en": [
            "grid_events.csv (Event G1): Curtailment from 16:00:00 to 19:00:00+02:00, capping site power to 400 kW.",
            "fleet_schedule.csv: Afternoon trucks T01–T04 need 1,250.1 kWh total, departing between 17:30 and 18:15. Overnight trucks T05–T08 need 1,533.1 kWh total, staying until 06:00 (15 hours dwell time).",
            "Baseline FCFS Failure: Unmanaged equal power sharing throttled all 8 trucks to 50 kW each during 16:00–19:00, leaving T01–T04 undercharged by 278.9 kWh simulated deficit (matches official recorded 283.50 kWh within 1.6%).",
            "Sentinel Priority Preemption: During 16:00–18:15, all 400 kW is dynamically concentrated on T01–T04. They reach required 70% SoC on-time before departure.",
            "Once T01–T04 depart, the 400 kW (and 800 kW after 19:00) smoothly charges overnight trucks T05–T08, which depart at 06:00 with 100% target SoC. Missed departures = 0."
        ],
        "proof_cn": [
            "grid_events.csv 官方指令表（事件 G1）：削峰时段为 16:00:00 至 19:00:00+02:00，全站进线刚性下调为 400 kW。",
            "fleet_schedule.csv 车队排程：下午车 T01–T04 需电总量为 1,250.1 kWh，发车时间在 17:30 至 18:15；过夜车 T05–T08 需电总量为 1,533.1 kWh，停留时长超 15 个小时（次日 06:00 发车）。",
            "基准 FCFS 失败根源：平均分流策略在 16:00–19:00 期间给 8 辆车每辆只分配 50 kW，导致下午急送卡车 T01–T04 在发车前电量根本充不满，产生 278.9 kWh 缺口（与官方历史记录 283.50 kWh 高度吻合）。",
            "哨兵动态优先级抢占：在 16:00 至 18:15 的削峰攻坚窗口，将 400 kW 稀缺电网容量 100% 集中倾斜给急送车 T01–T04，使其在离场前全部达到 70% 目标 SoC！",
            "待 T01–T04 顺利离场后，400 kW 容量（以及 19:00 恢复后的 800 kW 容量）接续为过夜车辆 T05–T08 补能，次日 06:00 全员达到 85% 目标 SoC 满电发车！欠电离场由 4 辆降为 0 辆！"
        ],
        "arch_en": "L3 Fleet Flexibility Pooling: The rolling MILP recognizes long-dwell vehicles as a virtual battery energy storage system (BESS). Overnight trucks represent a 1,857 kWh deferrable demand buffer, releasing immediate grid capacity without hardware CAPEX.",
        "arch_cn": "L3 车队柔性负荷池化机理：滚动时域运筹模型将长停留商用车队直接视作‘虚拟电厂分布式储能池’。过夜车辆构成了高达 1,857 kWh 的可延迟负荷缓冲带，以零硬件投资撬动了极具弹性的电网动态响应能力。",
        "close_en": "When the grid cuts power in half, unmanaged stations leave trucks stranded. Project Sentinel treats heavy truck fleets as dynamic flexibility pools, delivering 100% punctuality under extreme grid stress.",
        "close_cn": "当电网削减一半供电时，无序充电会让车队瞬间趴窝。哨兵计划把商用车队转化为高度柔性的虚拟能量池，在电网极限挤压下依然捍卫了 100% 满电发车的生命线。"
    }
]

QA_ITEMS.extend(QA_ITEMS_PART2)
