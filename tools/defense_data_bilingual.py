# -*- coding: utf-8 -*-
"""
Project Sentinel: Comprehensive Bilingual Defense Intelligence Data
Contains verified data for all 3 Juror Personas, 14 Hardcore Q&As, 4-Member Roles, 5 Axioms, and 6 Crisis Protocols.
"""

PERSONAS = [
    {
        "id": "P1",
        "title_en": "The Hardcore Technical & Systems Architect",
        "title_cn": "硬核技术与系统架构师",
        "representatives": "Mats Mattsson (Head of Cloud Software, Kempower) & Panu Vartiainen (Hardware / Electrical Lead)",
        "mindset_en": "Deeply skeptical of high-level AI marketing slides. Evaluates solutions strictly against the laws of physics, real-world power electronics topologies, contactor timing, and edge failure resilience.",
        "mindset_cn": "对空洞的高大上 AI 宣传保持高度怀疑。严格依据电气物理学定律、真实电力电子拓扑、接触器先断后合动作时序以及边缘端离线容灾韧性来拷问方案可行性。",
        "priorities_en": [
            "Hardware Realism: Respects strict 1:N physical cabinet wiring in chargers.csv (cross_tie = False).",
            "Autonomous Edge Islanding: 72-hour full local autonomous operation via SQLite WAL when WAN drops.",
            "Electrical Invariants: Strict enforcement of rectifier efficiency (η = 0.955) preventing substation overloads.",
            "Optimization Solvability: Real-time HiGHS MILP solving in < 80ms without vehicle drops during price spikes.",
            "Protocol Fidelity: OCPP 2.0.1 smart charging profiles & ISO 15118-20 Plug & Charge ECDSA P-256 verification."
        ],
        "priorities_cn": [
            "硬件真实性：严格遵守 chargers.csv 中的 1:N 独立物理接线（cross_tie = False），不凭空捏造母排。",
            "边缘离岛自愈：网络中断时通过本地 SQLite WAL 日志保障 72 小时全离线自主负荷控制。",
            "电气损耗铁律：严格执行整流器效率约束（η = 0.955），绝不允许直流输出超出变压器交流容量。",
            "运筹实时求解：HiGHS 混合整数规划在 80ms 内极速求解，现货电价暴涨至 799.30 欧时不漏发甩车。",
            "工业协议合规：OCPP 2.0.1 Smart Charging 报文格式合规，ISO 15118-20 即插即充国密级验签。"
        ],
        "red_flags_en": "Hand-waving buzzwords ('AI dynamically optimizes'); pretending 1,500 kW DC equals 1,500 kW AC; contactor switching under load; mocked test suites.",
        "red_flags_cn": "使用虚假 AI 概念搪塞技术细节；忽视整流器损耗将 1500 kW 直流等同于交流；带载切断直流接触器产生拉弧；用 Mock 数据欺骗测试。",
        "style_en": "'You claim 260 ms contactor switching. Walk me through the six discrete physical steps from current ramp-down to relay verification. If the zero-current sensor fails, what hardware safety interlock engages?'",
        "style_cn": "“你们声称 260 毫秒完成继电器切换。请详细拆解从电流降额到辅助触点确认的六个离散物理步骤。如果第 2 步零电流检测未通过，哪个硬件联锁会立即动作？”"
    },
    {
        "id": "P2",
        "title_en": "The Commercial Strategist & Venture Capitalist",
        "title_cn": "商业战略家与风险投资人",
        "representatives": "Early-Stage Climate Tech VC General Partner, Corporate CFO, LahtiES Commercial Mentor",
        "mindset_en": "Laser-focused on unit economics, gross margins, customer willingness to pay, risk allocation, and downside protection. Does not care how elegant code is if the business model goes bankrupt after one bad month.",
        "mindset_cn": "聚焦单车与单桩单位经济学、毛利率、客户付费意愿、商业风险分担机制与下行底线兜底。如果遇到极端事件企业一个月就会破产，再优美的代码也没有任何商业价值。",
        "priorities_en": [
            "AEaaS Monetization: Clear outcome-based commercial model selling Energy Certainty rather than hardware markups.",
            "Economic Honesty: Distinguishing between depot fleet labor and manufacturer field service costs.",
            "Payback Integrity: Defending the 13.31-year S1 standalone hardware payback vs the 2-month network SaaS deployment.",
            "Liquidated Damages & Caps: Enforceable One-Page SLA with non-negative guarantee and 150% monthly liability cap.",
            "Anti-Moral-Hazard Gates: Minimum Required Dwell Time (MRDT §5.1) preventing fraudulent penalty claims."
        ],
        "priorities_cn": [
            "确定性服务变现：通过按成果付费的确定性服务（CaaS）销售能源确定性，而非单纯加价卖桩。",
            "经济账本诚实度：严格区分车队场站常驻司乘人力与设备原厂售后技师成本，杜绝偷换概念。",
            "回本周期严谨性：合理解释 S1 硬件单独投资需 13.31 年回本，与全网纯软件部署 2 个月回本的差异。",
            "合同风控闭环：单页 SLA 合同必须具备月度赔偿非负保证与 150% 刚性封顶上限，防止极端索赔爆仓。",
            "防刷单道德风险门禁：最小必需停留时间（MRDT §5.1）门禁，彻底封死虚假延误索赔漏洞。"
        ],
        "red_flags_en": "Quoting TAM without CAC/LTV; uncapped operational liabilities; double-counting savings; conflating single-site CAPEX with network-wide OPEX.",
        "red_flags_cn": "大谈万亿市场空间却讲不清单站获客成本；提出无上限连带赔偿；把电网套利与人力省钱重复计算；将单站硬件成本除以全网人力计算虚假回报期。",
        "style_en": "'On Scenario Day, your SLA incurred €3,350 in penalties against a base fee of €663. If a 3-day blizzard knocks out grid power across five depots, does your operating company face insolvency? Where is the liability circuit breaker?'",
        "style_cn": "“在场景日当天，你们的 SLA 在 S1 场站产生了 3,350 欧元的违约金，而单日服务费基数才 663 欧元。如果一场暴风雪连刮三天瘫痪了五个场站，你们岂不是要破产？合同中哪一条是止损熔断器？”"
    },
    {
        "id": "P3",
        "title_en": "The Kempower Challenge & Host Custodian",
        "title_cn": "赛事主办方与规则守护者",
        "representatives": "Kempower Product Managers, Challenge Leads (Mats & Panu), LahtiES Organizing Committee",
        "mindset_en": "Guardians of the Kempower brand, challenge rules, and European Green Capital ideals. Vigilant about data immutability, intellectual honesty, zero continuous human operation, and compelling customer narratives.",
        "mindset_cn": "Kempower 品牌声誉、赛事规则与欧洲绿色之都（拉赫蒂）愿景的守护者。严格核查原始数据不可篡改性、技术诚实度、真正零人工持续运营以及接地气的客户故事。",
        "priorities_en": [
            "Rule 1 (Data Immutability): Zero modifications, filtering, or synthetics injected into official 45 CSV files.",
            "Rule 2 (No Unpriced Hardware): Never inventing unpriced assets (e.g. inter-cabinet busbar ties) outside equipment_costs.csv.",
            "Rule 3 (Zero Continuous Human Touch): Eliminating recurring midnight yard re-plugging (moves = 0).",
            "Honest Retention: Explicitly retaining 5.09 FTE physical technician visits (cleared_by=technician) and 3.22 FTE customer service.",
            "Customer Narrative: Grounding the 2029 vision in Pekka Virtanen's sub-zero (-18°C) blizzard morning rollout in Lahti."
        ],
        "priorities_cn": [
            "规则一（数据纯洁性）：官方 45 个 CSV 文件绝不允许被修改、人为过滤或注入虚假数据。",
            "规则二（报价单红线）：严禁在 equipment_costs.csv 之外凭空编造未经官方定价的硬件资产（如跨柜母排）。",
            "规则三（零人工持续运维）：彻底消除夜间反复插拔挪车，将例行运营操作压缩为零（moves = 0）。",
            "诚实保留必要人力：坦诚保留 5.09 FTE 必须由技师上门的物理维修工单，以及 3.22 FTE 客户联络中心人力。",
            "真实客户故事：将 2029 愿景锚定在拉赫蒂极寒（-18°C）暴风雪中 Pekka Virtanen 的公交发车实战中。"
        ],
        "red_flags_en": "Altering dataset files; claiming 100% elimination of all hardware technician rollouts; presenting manual replugging scripts as autonomous self-healing; ignoring sub-zero battery physics.",
        "red_flags_cn": "篡改官方原始数据；吹嘘 100% 消除所有线下维修技师（违背物理常识）；将半夜人工换枪作弊代码包装为自愈能力；无视极寒天气动力电池物理特性。",
        "style_en": "'Rule 3 states that humans cannot continuously operate the network. But when Cabinet C1-3 overheats at 02:25, faults.csv says it took a technician 246 minutes to clear it. How can you claim zero-human operation if a human technician had to turn a wrench?'",
        "style_cn": "“规则三明确规定不允许人类持续运营网络。但当 C1-3 机柜在凌晨 02:25 跳闸时，故障表明确记录技术人员花了 246 分钟才排障。既然依然有人到场拧螺丝，你们怎么敢声称是无人化运行？”"
    }
]

ROLES = [
    {
        "role": "Speaker A",
        "title_en": "Commercial Lead & Head of Storytelling",
        "title_cn": "商业领袖与首席宣讲人",
        "stage_pos": "Front Stage Right · 前台右侧（靠近评审席）",
        "scope_en": "Customer narrative (Pekka Virtanen 2029), 20.76 FTE economic waterfall, One-Page SLA commercial agreements, MRDT anti-fraud gate, ROI payback modeling.",
        "scope_cn": "客户故事阐述（Pekka Virtanen 2029）、20.76 FTE 人力财务瀑布图、单页 SLA 商业合同条款、MRDT 防刷单机制、投资回本周期模型。",
        "bridge_en": "'To see how our physical power routing solves this at the copper layer, our Chief Systems Architect Speaker B will deconstruct the core engine.'",
        "bridge_cn": "“为了深入拆解底层物理功率路由如何在铜排层解决这些痛点，下面请我们的首席系统架构师 Speaker B 剖析核心硬核引擎。”",
        "rescue_en": "Intervenes if Member D gets bogged down in mathematical formulas by pulling the discussion back to commercial unit economics and contract certainty.",
        "rescue_cn": "若 Member D 陷入过于晦涩的运筹数学公式推导，立即插话将其升维拉回至商业确定性与客户合同履约维度。"
    },
    {
        "role": "Speaker B",
        "title_en": "Chief Systems Architect & Technical Lead",
        "title_cn": "首席系统架构师与技术领袖",
        "stage_pos": "Front Stage Left · 前台左侧（靠近控制大屏）",
        "scope_en": "L1-L3 three-layer architecture, 25kW modular DPR matrix, 260ms Break-Before-Make timing, S1-S5 causal attribution, 13->3 vs 13->0 busbar truth.",
        "scope_cn": "L1-L3 三层架构全景体系、25kW 模块化动态功率路由矩阵、260ms 先断后合防电弧时序、S1-S5 因果归因、13到3与13到0母排真相。",
        "bridge_en": "'Talk is cheap, let's see the code fly. Member C, engage the autonomous console flight mode.'",
        "bridge_cn": "“空谈无益，代码见真章。成员 C，启动控制台飞行巡航演示模式。”",
        "rescue_en": "Intervenes if Speaker A faces deep electrical questions (transformer protection, contactor arcing) to provide authoritative physical evidence.",
        "rescue_cn": "若 Speaker A 遭遇深度电气物理质疑（变压器交流损耗、接触器拉弧破坏），立即接管并给出经法证级验证的底层证据。"
    },
    {
        "role": "Member C",
        "title_en": "Live Console Pilot & Verification Guardian",
        "title_cn": "控制台主操手与真实性卫士",
        "stage_pos": "Console Workstation 1 · 控台 1 号位（大屏直连输出）",
        "scope_en": "Streamlit 4-view live cockpit scrubber, live fault injection (02:25 S1 trip, 11:00 S3 outage, 18:00 S4 price spike), deterministic CLI verifier (python verify_all.py).",
        "scope_cn": "Streamlit 四视图交互控制台精准推演、现场故障动态注入（02:25 S1跳闸、11:00 S3断网、18:00 S4电价尖峰）、一键运行命令行验证器（verify_all.py）。",
        "bridge_en": "'Console initialized at timestamp 02:25:00. F016 thermal fault injected. Autonomic edge FSM re-routes modules in 260 milliseconds.'",
        "bridge_cn": "“控制台已锁定时间戳 02:25:00。F016 过温硬故障已注入。边缘有限状态机在 260 毫秒内完成模块自愈重路由。”",
        "rescue_en": "Keeps backup 1080p video tab (presentation_demo.mp4) buffered at 00:00, ready to switch via Alt+Tab in < 1 second if network fails.",
        "rescue_cn": "浏览器后台始终预载 1080p 备用录屏，若现场 HDMI 或控制台发生任何卡顿，1 秒内通过 Alt+Tab 切换为平滑离线视频。"
    },
    {
        "role": "Member D",
        "title_en": "Edge Simulation & Mathematical Modeler",
        "title_cn": "边缘仿真与运筹数学专家",
        "stage_pos": "Console Workstation 2 · 控台 2 号位（测试代码终端）",
        "scope_en": "SciPy HiGHS rolling MILP slack formulations, 16-cell discrete attribution matrix (src/sim/discrete_sim.py), 568 automated test suite execution.",
        "scope_cn": "SciPy HiGHS 滚动混合整数规划连续松弛变量构建、16 单元因果归因离散事件仿真、全套 568 项自动化测试脚本与断言矩阵。",
        "bridge_en": "'Under 799.30 €/MWh spot pricing, our continuous slack penalty M_slack=10,000 € strictly dominates price arbitrage, guaranteeing zero vehicle drops.'",
        "bridge_cn": "“在 799.30 欧现货电价极值下，我们的连续松弛惩罚项 M_slack=10,000 欧在数学上严格压制电价套利，保证甩车数为零。”",
        "rescue_en": "Immediately cites exact code line numbers (e.g., dpr_matrix.py line 582, discrete_sim.py Cell 7) when jurors probe algorithmic authenticity.",
        "rescue_cn": "当评委质询算法真实性时，秒级报出确切代码文件与行号（如 dpr_matrix.py 第 582 行，discrete_sim.py Cell 7），用代码说话。"
    }
]

AXIOMS = [
    {
        "axiom_en": "Axiom 1: 13 → 3 Missed Departures (Zero-CAPEX Delivery)",
        "axiom_cn": "公理一：漏发 13 降至 3（零硬件投资纯软件交付）",
        "details_en": "On existing 12 guns, software rescues B20, cuts energy deficit from 398.5 to 48.8 kWh (-87.8%), and eliminates all 12 cable moves (0 € CAPEX). Reaching 0 requires an unpriced inter-cabinet busbar.",
        "details_cn": "在现有 12 根枪下，纯软件调度拯救 B20，缺电由 398.5 降至 48.8 kWh（减少 87.8%），挪车从 12 次降至 0 次（0 € CAPEX）。实现 0 欠电需依赖官方无报价的跨机柜母排。"
    },
    {
        "axiom_en": "Axiom 2: 12.44 FTE Software-Addressable (€1.09M/yr)",
        "axiom_cn": "公理二：12.44 FTE 软件消除人力（109 万欧/年）",
        "details_en": "Total recorded labor is 20.76 FTE (€1.82M/yr). We address 59.95% (9.95 FTE replug + 2.28 FTE load adjustment + 0.21 FTE resets/pricing). We explicitly retain 5.09 FTE technician visits & 3.22 FTE customer service.",
        "details_cn": "官方总人力为 20.76 FTE（182 万欧/年）。软件仅消除 59.95%（9.95 FTE 挪车 + 2.28 FTE 调载 + 0.21 FTE 复位调价）。实事求是保留 5.09 FTE 线下维修与 3.22 FTE 客服。"
    },
    {
        "axiom_en": "Axiom 3: Cell 7 Hardware Trap (24 Guns without Busbar = 8 Missed)",
        "axiom_cn": "公理三：Cell 7 硬件陷阱（花 32.4 万欧加 12 枪欠电恶化为 8 辆）",
        "details_en": "Spending €324,000 to add 12 dispensers without a busbar tie causes 8 buses to lock onto dead Cabinet C1-3 upon arrival, worsening missed departures from 4 to 8! Busbars, not plugs, reach zero.",
        "details_cn": "花费 32.4 万欧增设 12 枪若无跨柜母排，前夜会有 8 辆车锁死在跳闸的 C1-3 机柜桩位上，欠电反增至 8 辆！增加接口数不是解药，母排才是关键。"
    },
    {
        "axiom_en": "Axiom 4: Inverter Efficiency Invariant (η = 0.955 Protection)",
        "axiom_cn": "公理四：整流器效率损耗铁律（η = 0.955 电网进线保护）",
        "details_en": "At Station S3 (1,500 kW grid connection), maximum DC output is strictly clamped to 1,425.0 kW DC (1,492.15 kW AC at η = 0.955), preserving an exact 7.85 kW AC safety buffer under the transformer limit.",
        "details_cn": "在 S3 站（1,500 kW 电网限额），直流侧输出必须刚性限制在 1,425.0 kW DC（对应交流输入 1,492.15 kW AC），为变压器留出 7.85 kW 绝对安全缓冲，确保 0 跳闸。"
    },
    {
        "axiom_en": "Axiom 5: 260 ms Break-Before-Make Zero-Arc Guarantee",
        "axiom_cn": "公理五：260 毫秒先断后合防电弧安全切换",
        "details_en": "Current ramps down to 0A at dI/dt < 100 A/s, verified by Hall sensors (I ≤ 0.1A) before contactor separates, fully executing in 260 ms (well inside IEC 61851 500 ms safety threshold).",
        "details_cn": "电流在 35ms 内降额至 0A（dI/dt < 100 A/s），经霍尔传感器确认（I ≤ 0.1A）后再机械断开触点，全流程 260ms 完成，远快于 IEC 61851 规定的 500ms 安全阈值。"
    }
]

CRISES = [
    {
        "id": "C1",
        "title_en": "Crisis 1: Projector Display Blackout / Signal Loss",
        "title_cn": "危机一：投影大屏黑屏或信号中断",
        "trigger": "HDMI disconnects, projector enters sleep mode, or venue AV console crashes.",
        "action_en": "Speaker A immediately pivots without breaking speech cadence: 'While the AV refreshes, let's examine the immutable facts.' Member C unplugs/replugs HDMI within 5 seconds. If unrecovered, Speaker B holds up the physical A4 Pocket Cheat Sheet and delivers the 6-step BBM contactor sequence verbally.",
        "action_cn": "Speaker A 毫不停顿自然控场：“在视听设备重连的片刻，让我们直接审视底层不可变数据。” 成员 C 在 5 秒内迅速插拔 HDMI。若无法恢复，Speaker B 举起随身压膜的 A4 速查卡，脱稿口述 6 步 BBM 接触器换流时序与 260ms 闭环指标。"
    },
    {
        "id": "C2",
        "title_en": "Crisis 2: Streamlit Interactive Console Crash or Port Conflict",
        "title_cn": "危机二：Streamlit 控制台意外崩溃或端口冲突",
        "trigger": "Browser tab crashes, Python memory spike, or WebGL renderer stall.",
        "action_en": "Member C triggers Alt+Tab to the pre-loaded 1080p offline video tab (presentation_demo.mp4) within 1.0s. Member C states: 'Switching to our redundant pre-rendered flight track.' Concurrently, Member D opens secondary terminal and executes 'python verify_all.py' to show green text.",
        "action_cn": "成员 C 在 1.0 秒内通过 Alt+Tab 切换至已预载好的 1080p 离线演示视频（presentation_demo.mp4），并朗声播报：“切换至冗余航行备用轨道。” 与此同时，成员 D 在第二终端窗口敲击回车运行 python verify_all.py，以绿色文本输出自证。"
    },
    {
        "id": "C3",
        "title_en": "Crisis 3: Aggressive / Hostile Juror Consecutive Interruptions",
        "title_cn": "危机三：评委连续严厉质疑与恶意打断",
        "trigger": "Juror aggressively challenges: 'Your numbers look completely fabricated!'",
        "action_en": "Speaker A remains calm, smiles, and deploys the 3-Step De-escalation Protocol: 1) Validate: 'That is the single most critical skepticism in fleet electrification.' 2) Evidence: 'May we draw your attention to row 164 of site_config.csv...' 3) Pass: Speaker B cites exact module line numbers.",
        "action_cn": "Speaker A 保持微笑，执行“三步降维化解法”：1）肯定：“这正是商用电动化中最具杀伤力、最核心的质疑。” 2）出证：“请看大屏幕 site_config.csv 第 164 行真实记录……” 3）交接：Speaker B 报出算法真实行号与约束矩阵，以事实粉碎质疑。"
    },
    {
        "id": "C4",
        "title_en": "Crisis 4: Time Remaining 2-Minute Warning from Timer Bell",
        "title_cn": "危机四：计时牌亮起最后 2 分钟红线警报",
        "trigger": "Pitch is at Slide 7 when timer bell rings for 2 minutes remaining.",
        "action_en": "Speaker B triggers fast-forward protocol: skips deep protocol packet inspection, fast-forwards directly to Slide 10 (Economics) and Slide 12 (Conclusion): 'In our remaining 120 seconds, let's close on the commercial certainty that makes this bankable for Lahti.'",
        "action_cn": "Speaker B 触发快速推进协议：略过工业协议抓包细节，直接跳至 Slide 10（经济账本）与 Slide 12（终章结论）：“在最后的 120 秒内，让我们聚焦于让拉赫蒂市不可拒绝的商业确定性闭环。” 严格在 09:50 前完赛。"
    },
    {
        "id": "C5",
        "title_en": "Crisis 5: Unanswerable / Unknown Technical Edge Question",
        "title_cn": "危机五：遭遇未曾预料的冷门技术盲区",
        "trigger": "Juror asks about an unmodeled parameter (e.g. harmonic distortion THD in 4th-order harmonics).",
        "action_en": "Speaker B delivers the Intellectual Honesty Pivot: 'In the official 45 CSV dataset, electrical harmonics are not logged at the 4th order. Rather than speculate, our system treats non-logged parameters as an unmodeled boundary, clamping to IEC 61851 envelope limits. Here is how our architecture bounds that uncertainty.'",
        "action_cn": "Speaker B 执行“技术诚实锚定话术”：“在官方提供的 45 个 CSV 数据集中，并未采集 4 次谐波畸变率。与其凭空捏造假设，我们的系统严格将未录入参数视为不可信边界，直接遵循 IEC 61851 保守裕度。以下是我们在底层如何封闭该风险……”"
    },
    {
        "id": "C6",
        "title_en": "Crisis 6: Total Venue Power Outage or Grid Blackout",
        "title_cn": "危机六：会场突发大面积停电或完全断网",
        "trigger": "Auditorium lights go dark, PA system cuts off.",
        "action_en": "Speaker A projects voice loudly in the dark: 'Ladies and gentlemen, this blackout proves our central thesis: modern society cannot depend on fragile human operators. Project Sentinel's edge controller is battery-backed and continues islanded operation right now.' Holds up phone flashlight against printed cheat sheet.",
        "action_cn": "Speaker A 洪亮发声打破黑暗：“各位评委，突如其来的停电正是我们今天立论的最佳注脚：现代社会绝不能依赖脆弱的电网和人手。哨兵计划的边缘控制器依托本地电池储能，此刻正处在毫秒级离岛自愈运行中！” 用手机手电筒照亮纸质速查卡完成演说。"
    }
]
