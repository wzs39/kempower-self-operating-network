# ⚡ Project Sentinel · The Self-Operating Charging Network
*Kempower Challenge · LahtiES Energy Tech Hackathon 2026 (Thu 5.11. – Sat 7.11.2026 @ LUT Lahti / CrazyTown)*

> **Core Mission**: *"If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"*  
> —— 设计并验证一套在零持续人工干预下稳定运行的自治充电网络系统，直击传统运营中 **21 FTE 全职人力消耗** 与 **5,596 次夜间挪车重插** 的物理与算法痛点。

---

## 🚀 项目核心亮点 (Key Highlights)

1. **双轮驱动战略定位 (Dual-Track Positioning)**：
   - **B2B 车队场站 (S1/S2/S5)**：保障 100% 按时满电出勤，彻底消灭夜间人工挪车重插；
   - **C 端公共枢纽 (S3/S4)**：实现高吞吐自适应运营，断网期间绝不降速，将弃流率从 29.7% 压降至 <0.5%。
2. **双枪卫星桩拓扑与功率时分复用 (Dual-Gun Satellite Architecture)**：
   - 彻底破解 S1 场站“24 辆公交车仅有 12 根充电桩”的物理死穴！
   - 12 桩升级为双枪（共 24 枪），24 辆车夜间 100% 物理连接；
   - 结合 Kempower 专利整流柜 25 kW 步长动态路由，前半夜快充 A 组、后半夜无弧切换 B 组，**1.5 个月收回改造成本**。
3. **双层混合时间尺度控制引擎 (Two-Tier Hybrid Engine)**：
   - **宏观层 (15 min)**：滚动时域优化（MPC / MILP），统筹 799.30 €/MWh 极端现货电价削峰、电网限额与发车计划；
   - **微观层 (毫秒~秒级)**：边缘有限状态机（FSM），硬核接管突发故障自愈、无弧重路由与 N-1 降级主动切负荷。
4. **五大隐蔽失效模式硬核防御 (Latent Failure Defense)**：
   - 计入 95.5% 逆变交流损耗（防进线跳闸）；
   - 动态释放高 SoC 涓流充电虚占功率；
   - 基于 1 分钟高频遥测风扇转速与温升梯度实现过温提前 5 分钟早筛自愈；
   - 断网离线自主调度（打破 50 kW 傻瓜降速）；
   - 新建站上电名牌与数字孪生自动纠错（自愈 S5 参数错配）。
5. **2029 颠覆性商业模式与单页 SLA (One-Page SLA)**：
   - 从卖桩维保转向“保底发车电量交付服务（AEaaS）”；
   - 包含最小驻留时长（MRDT）防刷单机制与 150% 月度赔付上限。

---

## 📂 项目全景文件导航 (Repository Structure)

```
hackson/
├── docs/hackathon/                           # 黑客松 Rails 7 份事实文件体系
│   ├── BRIEF.md                              # 核心痛点、定位与非目标 (Non-goals)
│   ├── RULES.md                              # 官方规则原版条文 vs 假设
│   ├── JUDGING.md                            # 官方五维评分标准与展示点对应
│   ├── BUILD_PLAN.md                         # 敏捷开发冲刺与可见改进计划
│   ├── DEMO_SCRIPT.md                        # 120 秒冠军答辩与 Live Demo 脚本
│   ├── SUBMISSION.md                         # Devpost 提交文案与核对清单
│   ├── DECISIONS.md                          # 架构决策与需求取舍账本
│   └── HACKATHON.md                          # 黑客松主控面板
├── tests/                                    # 自动化实证与测试套件
│   ├── test_scenario_verification.py         # 场景日自愈逻辑验证脚本
│   └── ...
├── kempower-challenge/                       # 官方赛题数据主库
│   ├── Kempower-challenge-brief.pdf          # 赛题官方任务书原件 (3页)
│   └── kempower-challenge-data/              # 官方 45 个 CSV 数据集 (240,635 行)
│       ├── README.md                         # 数据集宏观拓扑说明
│       ├── DATA_DICTIONARY.md                # 全量字段数据字典
│       └── PUBLIC_SOURCES.md                 # 欧洲真实电网/交通/市场数据源
├── PROJECT.md                                # 项目工程总纲与系统架构规范
├── Kempower_Self_Operating_Network_Comprehensive_Survey.md  # 全维度调研白皮书 (99 KB)
├── One_Page_SLA_Specification.md             # 2029 单页服务级别协议 (One-Page SLA)
├── Kempower_Hackathon_Dataset_Comprehensive_Report.md       # 全量 57 个文件逐一解析报告
├── Kempower_LahtiES_hackathon_kickoff_2026-11-05.pptx       # 官方开营演讲 Keynote (42 MB)
├── Energy_Hackathon_2026_mentoring.xlsx      # 导师辅导与预约排班表
├── app.py                                    # Streamlit 竞赛级四模块交互大屏 (构建中)
└── README.md                                 # 本项目主说明文档
```

---

## ⚡ 快速验证与运行指南 (Quick Start)

### 1. 环境准备
```bash
# 推荐 Python 3.10+
pip install pandas numpy streamlit openpyxl pymupdf
```

### 2. 运行自动化测试与混沌断言
```bash
# 执行自动化回归验证
python -m unittest discover tests/
```

### 3. 启动交互式态势演示大屏
```bash
streamlit run app.py
```

---

## 👥 参赛团队与致谢
- **主办方**：LahtiES (Lahti Entrepreneurship Society) · LUT University Lahti / CrazyTown
- **命题与赞助方**：Kempower Oyj (Lahti, Finland)
- **官方导师**：Mats Mattsson, Panu Vartiainen, Iiro Kinnunen, Thet Zin, Chuong Pham, Paul Carlson
