# Demo Storyboard — shipped cut: `demo/presentation_demo.mp4` (75 s, 1920x1080@30fps, silent)

**片名**：`Five sites, one day · without people in the loop`
**时长**：98 秒｜1920×1080｜30 fps｜无旁白｜英文字幕
**一句话定位**：不是介绍系统，是把 **Fri 13.11.2026** 这一天在没有人值守的情况下放一遍，让评委看见系统做了什么、以及它做不到什么。

> 本文件是**选定版 C（慢镜）**：与 92 秒版相比，镜头 1 压到 10 s、镜头 3 放到 24 s 并拆三拍、镜头 6/7 各加 2 s。三版对照与选型理由见 [`DEMO_STORYBOARD_VARIANTS.md`](DEMO_STORYBOARD_VARIANTS.md)。

> 本片与官方 kickoff 播放的 `Kempower_video1.mp4`（65 s，`Five sites, one night · today, with people in the loop`）构成**正反打**：同一份数据、同一个版面、同一夜，唯一差别是人不再在环里。

---

## 0. 硬约束（来自官方原文，不可违背）

| 约束 | 出处 | 本片如何满足 |
|---|---|---|
| 跑 **scenario day Fri 13.11** | `kempower-challenge-data/README.md:62` | 全片时间轴 = 2026-11-13 00:00–23:59 |
| **无人工介入** | 同上 | 全片标注 `0 manual moves`；`moves` 字段 = 0 |
| 至少**一个故障** | 同上 | F015 → F016（S1 过温掉柜）、F017（S4 电缆损伤） |
| 至少**一个电价事件** | 同上 | 18:00 = 799.30 €/MWh 尖峰 |
| 用 close-up 站或全网 | 同上 | 五个 close-up 站（S1–S5） |
| 说明**智能在哪一层** | brief p.1 | 镜头 5 显式打出 `EDGE` / `CLOUD` 层标签 |
| 说明**人还留在哪、为什么** | 评分表 Autonomy 25% | 镜头 3（技师 4 h 06 min）+ 镜头 7（F017 未解） |

**三条禁止**：不加配音；不扫参数（不用滑杆/扫描）；不用生成式画面。每一帧的数字必须能从引擎或 CSV 复现。

---

## 1. 技术规格

| 项 | 值 |
|---|---|
| 分辨率 / 帧率 | 1920×1080 / 30 fps |
| 总帧数 | 2,940（98 s × 30 fps） |
| 编码 | H.264, yuv420p, CRF 20, 无音轨 |
| 字体 | `DejaVu Sans`（matplotlib 内置）/ 数字用 `DejaVu Sans Mono` |
| 渲染 | `tools/render_scenario.py` → PNG 序列 → `ffmpeg -framerate 30` |
| 输出 | **已交付**：`demo/presentation_demo.mp4`（75 s）+ `demo/presentation_demo_poster.png`（封面帧）。本文件原设计的 `scenario_day.mp4` / `scenario_day_poster.png` 为同一素材的旧命名，未单独产出，提交清单以 `presentation_demo.*` 为准。 |

### 配色

| 语义 | 色值 | 用途 |
|---|---|---|
| 背景 | `#0B1016` | 全片底色 |
| 面板 | `#131B24` | 单站卡片 |
| 网格 | `#1E2A36` | 分隔线、刻度 |
| 功率正常 | `#00C2A8` | 功率条、达标车辆 |
| 降额 | `#F5A623` | F015、DSO 限电 |
| 故障 | `#FF4D4F` | F016 停柜、F017、欠电车辆 |
| 断网 | `#8B5CF6` | S3 云链路 |
| 主文字 | `#E6EDF3` | 标题、数字 |
| 次文字 | `#8B98A5` | 单位、注释 |
| 焦点强调 | 非焦点面板 `alpha=0.15` | 推镜时使用 |

---

## 2. 版面网格

```
┌──────────────────────────────────────────────────────────────┐
│  Fri 13.11.2026          18:42      ▌ 0 people on shift      │  ← 顶栏 96 px
├──────────────────┬──────────────────┬────────────────────────┤
│  S1 Bus depot N  │  S2 Logistics E  │  S3 Highway hub        │
│  12 guns·3×360   │  8 guns·2×400    │  10 guns·3 cab         │
│  [ 柜 柜 柜 ]     │  [ 柜 柜 ]        │  [ 柜 柜 柜 ]           │  ← 上排 384 px
│  ▓▓▓▓▓ 1,080/1,200│  ▓▓▓▓ 800/800    │  ▓▓▓ 1,425/1,500       │
├──────────────────┼──────────────────┼────────────────────────┤
│  S4 City hub     │  S5 Bus depot S  │  What the system sees  │
│  8 guns·2×450    │  8 guns·2×450    │  (日志滚动)             │  ← 下排 384 px
│  [ 柜 柜 ]        │  [ 柜 柜 ]        │                        │
│  ▓▓▓ 450/600     │  ▓▓▓ 900/900     │                        │
├──────────────────┴──────────────────┴────────────────────────┤
│  字幕行  ▸ 副字幕                                             │  ← 底栏 120 px
└──────────────────────────────────────────────────────────────┘
```

- 单元尺寸 600×384，间距 12 px，外边距 24 px
- 单站卡片内部：标题行 44 px → 柜体图 220 px → 功率条 56 px → 状态行 48 px
- **柜体图**：一个柜 = 一个竖矩形，内分 4 格（每格 = 1 把枪）；枪占用时格内填车辆方块 + 车牌号；故障时整柜描边变红并打叉
- **功率条**：底槽 = 站点额定，实心 = 当前功率，刻度写 `实时 / 额定 kW`

---

## 3. 数据接口（渲染器需要引擎提供什么）

当前 `run_discrete_event_simulation` 只返回聚合结果与 `vehicle_records`，**没有逐分钟轨迹**。渲染前需给引擎加一个可选参数：

```python
run_discrete_event_simulation(..., trace: Optional[list] = None)
# trace 每分钟 append 一条：
# {"t": "2026-11-13T02:25:00+02:00",
#  "site_kw": 720.0,
#  "cabinet_kw": [360.0, 360.0, 0.0],
#  "guns": [{"gun":"D1-1","cabinet":"C1-1","vehicle":"B15","kw":150.0,"soc":0.62}, ...],
#  "events": [{"type":"fault","id":"F016","text":"Cabinet stopped: overtemperature"}]}
```

默认 `None`（零行为变化），全部已有测试不受影响。**这是本片唯一的代码改动。**

分镜中每个数字的取数位置：

| 数字 | 来源 |
|---|---|
| 车辆到发时刻、需求 kWh | `fleet_schedule.csv` + `load_fleet_jobs()` |
| 各柜实时功率、枪位占用 | `trace`（引擎逐分钟） |
| 故障时刻与状态 | `faults.csv`（F015/F016/F017） |
| 限电通知与窗口 | `grid_events.csv`（G1：`notified_ts` 14:00，16:00–19:00） |
| 断网窗口 | `connectivity_outages.csv`（S3：11:00–13:00） |
| 电价曲线 | `prices.csv`（18:00 = 799.30，16:00 = 29.12，22:00–23:45 均值 52.20） |
| 漏发/缺口/峰值 | 引擎 `to_dict()` |
| 公共站到站与放弃 | `public_arrivals.csv`（S3 256 / 76 放弃；S4 101 / 1） |

> **⚠️ 关于分镜里的功率数字**：本文写的 `1,080 → 900 → 720 kW` 是**按柜额定推算的节点值**（3×360 满发减去降额/停机）。引擎实际逐分钟功率受车辆当前需求约束，通常低于额定。渲染时**一律以 `trace` 输出为准**，本文的数值只作版面与叙事校验用；若 `trace` 与本文差异超过 5 %，以 `trace` 为准并回改本文。

---

## 4. 逐镜头分镜

### 镜头 0 ｜静默开机 — `00:00 – 00:08`（8 s / 240 帧）

| 项 | 内容 |
|---|---|
| 画面 | 纯黑底。三行白字依次淡入（每行间隔 2 s，淡入 0.4 s） |
| 文字 | ① `Friday 13.11.2026`（48 px，居中）<br>② `5 close-up sites · 100 sites total · 0 people on shift`（24 px，次色）<br>③ `Same data. Same faults. Same prices.`（24 px，次色） |
| 动效 | 无位移，只有透明度 0→1 |
| 声音 | 无 |
| 意图 | 复刻官方片开头的静默感。第 3 行是全片的论点：**变量只有“人”** |

### 镜头 1 ｜矩阵就位 — `00:08 – 00:18`（10 s）

| 项 | 内容 |
|---|---|
| 画面 | 六格网格**一次**整体淡入（0.6 s，不逐格铺开）。顶栏出现 `Fri 13.11.2026` + 时钟 `18:00` |
| 主事件 | S1 的 **24 辆**公交从 18:58 起依次进场（`B15` 18:58 最早，`B20` 23:28 最晚；合计需求 `7,872 kWh`）。每进一辆，占用一把枪，车辆方块滑入柜格 |
| 时钟 | 18:00 → 00:00，10 s 走 6 h ⇒ **36 min/s** |
| 功率 | S1 功率条从 0 爬到 **1,080 kW**（3 柜 × 360，未触 1,200 限值）；S5 的 12 辆从 19:44 起进场（`B26` 19:44 最早，`B28` 23:04 最晚，`4,376.7 kWh`） |
| 关键视觉 | **20:38 `B21` 进场时，12 把枪全满** → 从这一辆起格内显示 `WAIT` 黄标。**这是全片第一次出现“资源不够”** |
| 字幕 | `18:00 → 00:00 · 24 buses arrive at S1 · 12 guns` |
| 副字幕 | `S1 is the only station where the queue never clears` |
| 数据 | `fleet_schedule.csv`；S1 夜间 24 辆（18:58–23:28 到，05:10–06:30 走）+ 白天 8 辆；S5 12 辆 |

### 镜头 2 ｜过温 — `00:18 – 00:30`（12 s）

| 项 | 内容 |
|---|---|
| 画面 | **推镜**：六格保留，S1 面板 `alpha=1.0`，其余降至 `0.15`；S1 面板向外扩 8 px 白描边，持续到镜头结束 |
| 时钟 | 00:00 → 02:40（12 s 走 2 h 40 min ⇒ 13.3 min/s） |
| 事件 A | **01:50** C1-3 柜描边转橙，柜内 4 格功率数字 `90 → 45 kW`，标签 `F015 derated 50 %`。S1 总功率 1,080 → 900 |
| 事件 B | **02:25** C1-3 柜描边转红，整柜填充变暗，柜内 4 格打 `✕`，功率归 0。S1 总功率 **900 → 720** |
| 日志栏 | `What the system sees` 逐条推送：`01:50 S1-C1-3 derated 50 % (overtemperature)` → `02:25 S1-C1-3 stopped (overtemperature, critical)` |
| 字幕 | `01:50 derated 50 % · 02:25 cabinet stopped — overtemperature` |
| 副字幕 | `One cabinet = one third of the site's power and one third of its guns` |
| 意图 | 让评委看清 **故障的物理含义**：不是“少了点功率”，是 12 把枪变 8 把 |

### 镜头 3 ｜那四小时 — `00:30 – 00:54`（24 s，三拍）

| 项 | 内容 |
|---|---|
| 画面 | S1 面板内部一分为二：**左侧 = 柜体图与车辆出发**，**右侧 = 竖向"人到底在哪"进度轨** |
| 结构 | 本镜拆三拍，节奏完全不同——**先不动、再涌出、最后停住** |

**③-1 静默 — `00:30 – 00:36`（6 s，02:25 → 05:10，27 min/s）**

| 项 | 内容 |
|---|---|
| 画面 | 几乎静止。C1-3 仍是红叉，12 枪只剩 8 枪，队列停在 4 辆不前进 |
| 进度轨 | 只亮一个灰点 `02:25 fault logged` |
| 字幕 | `02:25 fault logged` |
| 意图 | 先让观众**感觉到"没有人在动"**——这是全片唯一一段真正的静止 |

**③-2 涌出 — `00:36 – 00:47`（11 s，05:10 → 06:30，7.3 min/s）**

| 项 | 内容 |
|---|---|
| 左侧事件 | 05:10 起每 5 分钟走一辆，共 24 辆（`B10` 05:10 → `B13` 06:30），约 0.46 s 一辆。四辆欠电车按实际时刻标红：<br>05:35 `B18` ✕、`B20` ✕<br>06:00 `B09` ✕<br>06:15 `B04` ✕ ← **停 1.2 s**<br>其余 20 辆绿色 ✔ 依次驶出，06:30 `B13` 为末班 |
| 进度轨 | 第二点仍为灰 `02:31 ticket opened` |
| 字幕（两段替换） | ① `05:10 first departure — the cabinet is still dead`<br>② `06:15 the fourth bus leaves short` |

**③-3 空白 — `00:47 – 00:54`（7 s，06:30 → 06:31，1 min = 7 s）**

| 项 | 内容 |
|---|---|
| 画面 | **几乎完全静止**：左侧 24 格全空，右侧进度轨只剩一个灰点；唯一在动的是顶栏时钟，从 `06:30` 走到 `06:31`，走满整整一分钟 |
| 关键时刻 | `06:31` 技师节点亮红加粗的同一帧，左侧没有任何车辆了——**两栏之间这一分钟的空白就是论点** |
| 字幕（定格 3 s） | `06:31 technician on site · 4 h 06 min later`<br>副字幕：`By 06:31, every bus had already left.` |
| 数据 | `faults.csv` F016 `cleared_ts=06:31`，`cleared_by=technician`；发车时刻来自 `fleet_schedule.csv` |
| 意图 | **全片最重要的一镜。** 人不是没解决，是晚到 4 小时 06 分——比末班车晚 1 分钟。这一镜直接回答 Autonomy 25% 那句 `where humans still stay in the loop, and why`<br>7 秒的停留不是拖时间：92 秒版只给了这 1 分钟 1 秒，观众读不完字幕；这里让它自己说完 |

### 镜头 4 ｜对照三行 — `00:54 – 01:06`（12 s）

| 项 | 内容 |
|---|---|
| 画面 | **全屏切换**（淡出 0.3 s）。黑底，三行数据自左向右侧对齐，每行间隔 2.6 s |
| 第 1 行 | `no fault` → `0 missed` / `0.0 kWh`，右侧条形长度 0 |
| 第 2 行 | `with F016` → `4 missed` / `398.5 kWh`，条形满格（红），右侧小字 `= official record, vehicle-for-vehicle` |
| 第 3 行 | `our scheduler` → `3 missed` / `48.8 kWh`，条形 12%（青绿），右侧 `−87.8 %`, 并标 `B20 rescued` |
| 底部 | `same engine · same 12 guns · same 02:25 fault` |
| 字幕 | 无（数据即字幕） |
| 数据 | 三组均由同一函数 `run_discrete_event_simulation` 在 `fault=None / fault=(02:25,[2]) × fcfs / urgency` 下算出 |
| 意图 | **不可被质疑的一镜。** 它排除“你们只是调度不行”的质疑：无故障时是 0，所以那 4 辆 100% 由 F016 造成 |

> 这三行必须与 `verify_all.py` 的断言同源。渲染脚本直接调用引擎，不读硬编码常量。

### 镜头 5 ｜云不见了 — `01:06 – 01:16`（10 s）

| 项 | 内容 |
|---|---|
| 画面 | 切回六格（淡入 0.3 s），焦点 S3（其余 `0.35`） |
| 时钟 | 10:50 → 13:10（10 s 走 2 h 20 min ⇒ 14 min/s） |
| 11:00 | 顶栏出现红色横幅 `CLOUD UNREACHABLE`（横贯全宽，高 40 px） |
| 11:00 | S3 面板右上角图层标签由 `CLOUD` 翻转为 **`EDGE`**（紫），并在面板内打出 `L2 · site controller autonomous` |
| 11:00–13:00 | S3 枪位保持占用、功率条维持 `1,425 / 1,500 kW`，**无枪位跌落**；日志栏推送 `11:00 edge takeover · 0 sessions dropped` |
| 13:00 | 红条消失，标签翻回 `CLOUD`，副字幕 `13:00 link restored · nothing to reconcile` |
| 字幕 | `11:00–13:00 · cloud unreachable · the site kept running` |
| 副字幕 | `Intelligence is not in one place: L1 firmware · L2 site · L3 cloud` |
| 数据 | `connectivity_outages.csv`（S3，11:00–13:00）；枪柜 4+4+2 |
| 意图 | 逐字回答 brief 那句 `Where does the intelligence live … and what happens when the connection is lost?` |

### 镜头 6 ｜钱和电同时到 — `01:16 – 01:28`（12 s）

| 项 | 内容 |
|---|---|
| 画面 | 六格全亮；底栏下方插入**电价曲线条**（高 64 px），随时钟滚动 |
| 时钟 | 13:50 → 19:10（12 s 走 5 h 20 min ⇒ 26.7 min/s） |
| 节奏 | 曲线冲到 18:00 时**停 2 s 不动**（字幕同步出现），再回落——这是全片第二次"停住" |
| 14:00 | S2 面板出现橙色角标 `DSO notice · 400 kW from 16:00`（对应 `notified_ts`，提前 2 小时） |
| 16:00 | S2 功率条刻度由 `800` 变为 `400`，实心压至 `400 / 400 kW`（橙）；标签 `limit_cap honoured` |
| 17:30–18:30 | 电价曲线冲顶，18:00 处标注 `799.30 €/MWh`。**S2** 面板打出 `600 kWh → 22:00`（后段 T05–T08 顺延），**S4** 面板打出 `120 kWh avoided at 18:00` |
| 16:00 与 22:00 | 曲线在 16:00 标 `29.12`（当日谷值），在 22:00–23:45 段标 `52.20 avg`，形成对照 |
| 字幕 | `16:00–19:00 · 400 kW honoured · 0 departures missed at S2` |
| 副字幕 | `18:00 · 799.30 €/MWh · 600 kWh moved to 22:00 (52.20 avg)` |
| 数据 | `grid_events.csv` G1；`prices.csv`；S2 结果 4 → 0（同引擎、含限电、逐车误差 ≤1.6 %） |
| 意图 | 一镜同时命中 Energy & Grid 20% 与 Commercial 20% |

### 镜头 7 ｜我们没做到的那一件 — `01:28 – 01:38`（10 s）

| 项 | 内容 |
|---|---|
| 画面 | 全屏汇总，黑底 |
| 上半 | 五行小表，逐行点亮：<br>`S1  4 → 3`（12 guns, F016）<br>`S2  4 → 0`（400 kW curtailment）<br>`S5  5 → 0`（600 → 900 kW config）<br>`S3  islanded 2 h`<br>`S4  peak −76 kW` |
| 中部 | 大字 `13 → 3 remain`（56 px），下注 `0 manual moves`；**停 1 s 再切**（让这行数字单独站住），随后才出 F017 |
| 21:30 | 六格缩略图回闪一帧：S4 的 `D4-2` 变红，标签 `F017 cable damage · cleared_by = open` |
| 字幕 | `One thing we did not solve. A human still goes there.` |
| 收尾（最后 3 s） | 全屏渐暗，只留一行 `python verify_all.py · 0.26 s` |
| 数据 | `faults.csv` F017（`cleared_by=open`，周末仍开）；`baseline_kpis.csv`；引擎结果 |
| 意图 | 主动交代 F017。**这是全片可信度的来源**：一份承认边界的片子，比一份处处完美的片子更难被问倒 |

---

## 5. 字幕全文（可直接作为字幕轨）

```
00:02  Friday 13.11.2026
00:05  Fri 13.11.2026 · 5 close-up sites · 0 people on shift
00:07  Same data. Same faults. Same prices.
00:09  18:00 → 00:00 · 24 buses arrive at S1 · 12 guns
00:13  S1 is the only station where the queue never clears
00:19  01:50 derated 50 % · 02:25 cabinet stopped — overtemperature
00:24  One cabinet = one third of the site's power and one third of its guns
00:31  02:25 fault logged
00:37  05:10 first departure — the cabinet is still dead
00:43  06:15 the fourth bus leaves short
00:48  06:31 technician on site · 4 h 06 min later
00:51  By 06:31, every bus had already left.
00:56  no fault → 0 missed · with F016 → 4 missed · our scheduler → 3 missed
01:01  same engine · same 12 guns · same 02:25 fault
01:08  11:00–13:00 · cloud unreachable · the site kept running
01:12  L1 firmware · L2 site controller · L3 cloud
01:17  16:00–19:00 · 400 kW honoured · 0 departures missed at S2
01:22  18:00 · 799.30 €/MWh · 600 kWh moved to 22:00 (52.20 avg)
01:30  S1 4→3 · S2 4→0 · S5 5→0 · S3 islanded · S4 −76 kW
01:33  One thing we did not solve. A human still goes there.
01:36  python verify_all.py · 0.26 s
```

---

## 6. 验收断言（写进 `verify_all.py`）

片子渲染完成后，追加一个 `check_demo()`，确保视频与引擎永不脱钩：

```python
# 1. 文件存在且时长在 94–102 s
# 2. 帧数 == 2940（30 fps × 98 s）
# 3. 镜头 4 的三个数来自引擎：0 / 4 / 3 辆，398.5 / 48.8 kWh
# 4. 镜头 3 的时间点：F016 cleared_ts == 06:31，晚于 B13 depart 06:30
# 5. 镜头 5 的窗口：11:00–13:00 与 connectivity_outages.csv 一致
# 6. 镜头 6 的尖峰：18:00 的 799.30 与 prices.csv 一致
```

> 断言失败时打印“视频已过期，请重跑 `tools/render_scenario.py`”。这是防止“改了一行仿真、视频变成假证据”的唯一手段。

---

## 7. 复现

```bash
pip install matplotlib                      # 唯一新增依赖
python tools/render_scenario.py --out demo/  # 渲染 2,940 帧 + 合成
python verify_all.py                        # 含 check_demo()
```

渲染时间预估：2,940 帧 × ~35 ms ≈ 105 s（单核），ffmpeg 合成约 8 s。

---

## 8. 已知取舍

| 取舍 | 理由 |
|---|---|
| 用 2D 柜体示意，不做官方片的 3D 俯视 | 2D 能把“哪一柜死、哪把枪空”画得比 3D 更准；且每格颜色都能直接映射到 `cabinet_kw` 数组 |
| 不出现真人画面、不配音 | 官方 65 s 片同样零人声；有旁白会被读成“讲述”而非“展示” |
| S5 只用一行汇总，不展开 | S5 引擎只复现 5 辆中的 1 辆（`B35`），展开会被追问；一行 `5 → 0 (config)` 已足够 |
| 不出现 `324,000 €` 扩容方案 | 该方案需跨柜母联且无报价；片子里只留"做不到"这一格 |
| 不出现 `3×450 kW` 柜扩容（`75,600 €`） | 限值内（`1,146 kW` = `1,200 AC / 0.955`）实测 `0 missed / 0 kWh`，但结果**对枪功率非单调**（`3×500` → 退回 `4` 辆、枪 `140 kW` → `4` 辆），所以不做卖点、不进片子，只留作答辩备查（见 [`DEMO_STORYBOARD_VARIANTS.md`](DEMO_STORYBOARD_VARIANTS.md) §6） |
