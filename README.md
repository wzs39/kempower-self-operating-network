# ⚡ Project Sentinel · The Self-Operating Charging Network
*Kempower Challenge · LahtiES Energy Tech Hackathon 2026 (Thu 5.11. – Sat 7.11.2026 @ LUT Lahti / CrazyTown)*

> **Core Mission**: *"If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"*  
> —— 设计并验证一套在零持续人工干预下稳定运行的自治充电网络系统，直击传统运营中 **20.76 FTE (≈ 21 FTE) 全职人力消耗（1,821,534 €/年 @ 45 €/h）** 与 **5,596 次夜间挪车重插（占频次 63.22% / 占工时 47.93% = 9.95 FTE = 872,976 €/年）** 的物理与算法痛点。

---

## 🚀 项目核心亮点 (Key Highlights)

1. **双轮驱动战略定位 (Dual-Track Positioning)**：
   - **B2B 车队场站 (S1/S2/S5)**：保障 100% 按时满电出勤（场景日 13 辆欠电违约 $\to$ 0 辆），消除夜间无序挪车重插；
   - **C 端公共枢纽 (S3/S4)**：实现高吞吐离线自适应运营，断网期间打破 `50 kW` 静态兜底，将场景日弃流率从 **29.69%**（14 天基准 **14.36%**）压降至 **< 0.5%**。
2. **S1 车场双轨解决方案 (Dual-Strategy S1 Replug Resolution — `A1, B2, B6, D5`)**：
   - **物理边界透明化**：严格区分 Kempower 单连接器输出上限（`max_simultaneous_sessions = 12`）与同时为 24 辆公交充电的物理连接需求；
   - **方案 A（0 € CAPEX 即时软件协同单批次换枪）**：利用现有 12 根单枪桩将夜间无序插拔整合为 `01:30` 单次计划换枪，单日多充 `1,012.00 kWh`，**0 € 硬件成本**消灭 S1 全部 4 辆公交欠电发车；
   - **方案 B（2029 远景硬件扩容 24 枪）**：新增 12 根终端（`18,000 €` 设备 + `9,000 €` 土建 = `27,000 €/枪`，总计 `324,000 €` CAPEX），实现 24 车入场一次插枪与无弧时分复用（对比 S1 单站挪车年人工 `24,336 €/年`，静态回收期 `13.31 年`）。
3. **双层混合时间尺度控制与机柜内 1:N 拓扑 (Two-Tier Hybrid Engine & Intra-Cabinet DPR — `A2–A8, C1–C6`)**：
   - **宏观层 (15 min MILP)**：基于 SciPy HiGHS 求解器，引入 $10^{-3}$ 电价量纲折算、连续 SoC 赤字松弛变量（$z_v \in [0, 1]$，权重 $10,000\text{ €}$）与完整月度峰值需量电费（`6.50 / 7.50 €/kW/月`），在 `799.30 €/MWh` 尖峰电价下绝不恶意弃充任何可履约车辆；
   - **微观层 (毫秒~秒级 FSM)**：严格遵循 `power_cabinets.csv` 与 `chargers.csv` 的 1:N 机柜内铜排拓扑（严禁跨故障机柜倒送电），提前 **199 分钟**（`2026-11-12T22:31:00+02:00`, `59.3°C / 702 rpm`）捕捉 S1 `C1-3` 风机退化，自动派单技师处理 `F016`（`246 min`），并在 `C1-1/C1-2` 维持 `720 kW` N-1 满载输出（`0 kW` 自残切负荷）。
4. **S2 前瞻预充与 S5 三方数字孪生自动对账 (`B3, B8, C6`)**：
   - **S2 DSO 400 kW 限电防御**：在 `14:00` 接收 `G1` 限电预警后于 `14:20–16:00` 预充 `1,102.10 kWh`，消除 4 辆重卡（`T01–T04`）共 `283.50 kWh` 电量赤字；
   - **S5 三方配置对账自愈**：自动核对 `sites.csv` (`900 kW`)、`power_cabinets.csv` (`2×450 = 900 kW`) 与 `site_config.csv` (`grid_limit_kw = 600 kW`)，解锁 `300 kW × 2.5h = 750 kWh > 508.95 kWh` 缺口，同时修复 `D5-7` (`50 -> 150 kW`) 与 `D5-8` (`eSIM` 激活)。
5. **2029 结果导向型商业模式与单页 SLA (`One_Page_SLA_Specification.md`)**：
   - 保底 99.50% 可用率与发车履约率，内置最短合理驻留时间（MRDT）五层防欺诈门禁与 150% 月度赔付上限。

---

## 📂 项目全景文件导航 (Repository Structure)

```
hackson/
├── src/                                      # 生产级核心引擎、仿真器与商业模型源码
│   ├── utils/paths.py                        # 零硬编码跨平台路径解析器 (D4)
│   ├── core/
│   │   ├── dpr_matrix.py                     # 25kW 模块化 DPR 矩阵与 1:N 机柜拓扑约束
│   │   ├── virtual_replug.py                 # S1 方案 A (0€ CAPEX) & 方案 B (324k€) 调度器
│   │   ├── mpc_optimizer.py                  # HiGHS 滚动时域 MILP 优化器 (含连续赤字松弛)
│   │   └── self_healing.py                   # 边缘自愈 FSM、199min 热预警与 S5 三方对账
│   ├── sim/
│   │   ├── data_loader.py                    # 45 个官方 CSV 确定性加载器
│   │   └── scenario_engine.py                # 2026-11-13 场景日 S1~S5 闭环回放引擎
│   └── commercial/
│       ├── sla_calculator.py                 # One-Page SLA 与 MRDT 防欺诈引擎
│       └── roi_analyzer.py                   # 20.76 FTE 人工核算与硬件 CAPEX/ROI 分析器
├── tests/                                    # 179 项确定性实证与端到端测试套件 (0 假绿测试)
│   ├── test_github_issue2_29items.py         # GitHub Issue #2 (A1~D5 共 29 项) 专项实证测试
│   ├── test_gate2_empirical_verification.py  # Gate 2 生产模块与官方 CSV 交叉核验测试
│   ├── test_e2e_suite.py                     # 107 项四层端到端全特性测试套件
│   ├── test_m1_adversarial_probe.py          # M1 数学、电气与边界对抗探针测试
│   ├── test_mpc_math_fixes.py                # MILP 量纲、逆变损耗与松弛测试
│   ├── test_remediated_sla.py                # SLA 分段赔付、MRDT 与免责边界测试
│   └── test_scenario_verification.py         # S1~S5 场景日危机消解验证测试
├── docs/hackathon/                           # 黑客松 Rails 7 份事实文件体系
│   ├── BRIEF.md / RULES.md / JUDGING.md      # 赛题基线、规则红线与五维评分对齐
│   ├── BUILD_PLAN.md / DEMO_SCRIPT.md        # 研发交付追踪与 120 秒路演脚本
│   └── SUBMISSION.md / DECISIONS.md          # Devpost 提交正文与 ADR 001~008 决策账本
├── kempower-challenge/                       # 官方赛题任务书与 45 个 CSV 数据集 (240,635 行)
├── app.py                                    # Streamlit 四象限交互式数字孪生驾驶舱
├── verify_all.py                             # <0.5 秒一键确定性全量验证入口脚本
├── One_Page_SLA_Specification.md             # 2029 单页服务级别协议 (One-Page SLA)
├── PROJECT.md                                # 项目工程总纲与系统架构规范
└── README.md                                 # 本项目主说明文档
```

---

## ⚡ 快速验证与运行指南 (Quick Start)

### 1. 环境准备
```bash
# 推荐 Python 3.10+
pip install numpy pandas scipy pytest streamlit
```

### 2. 运行一键确定性验证 (`< 0.5 秒`) 与 179 项 Pytest 测试套件
```bash
# 运行 <0.5s 全景确定性核验器 (S1~S5 + 商业模型 + 全网零越限)
python verify_all.py

# 执行全部 179 项单元测试、实证测试与 GitHub Issue #2 29 项审计测试
pytest tests/ -v
```

### 3. 启动 Streamlit 四象限交互式演示大屏
```bash
streamlit run app.py
```

---

## 👥 参赛团队与致谢
- **主办方**：LahtiES (Lahti Entrepreneurship Society) · LUT University Lahti / CrazyTown
- **命题与赞助方**：Kempower Oyj (Lahti, Finland)
- **官方导师**：Mats Mattsson, Panu Vartiainen, Iiro Kinnunen, Thet Zin, Chuong Pham, Paul Carlson
