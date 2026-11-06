# 视频演示（Streamlit 六场故障演示）

Kempower 自营充电网络黑客松项目的现场演示套件，用六个独立 Streamlit 页面分别展示六种故障场景下「原系统 vs 本系统」的左右对比动画。

## 六场故障场景

| 页面文件 | 场景 | 数据锚点 |
| --- | --- | --- |
| `pages/1_Night_Replay.py` | 机柜过热（C1-3 F016）；右栏为 **Tier 3b 硬件场景**（24 点位+母联），非零 CAPEX 软件成绩 | 2026-11-13 02:25 |
| `pages/2_Outage_Replay.py` | 断网（蜂窝链路中断） | 11:00–13:00 |
| `pages/3_Price_Spike_Replay.py` | 电价尖峰 | 爬坡自 17:15；`prices.csv` 中 >600 €/MWh 仅 17:45 / 18:00 / 18:15，峰值 799.30 @18:00 |
| `pages/4_Curtailment_Replay.py` | 电网限电 | 16:00–19:00 |
| `pages/5_Cable_Fault_Replay.py` | 电缆异常 | 21:30 |
| `pages/6_Commissioning_Replay.py` | 配置错误 | 全天 |

每个页面左上角都有 ▶ Play / ⏸ Pause / ⟲ Restart 和播放速度滑块，画面已压缩为一屏，适合现场讲解或屏幕录制。

## 运行方式

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动（在仓库根目录下）
python -m streamlit run 视频演示/app.py
```

浏览器访问 `http://localhost:8501`，从左侧边栏进入六个页面。

## 数据依赖

六页面的模拟引擎从官方 Kempower 数据集读取 CSV，路径由 `src/utils/paths.py` 自动解析：

- 优先读环境变量 `KEMPOWER_DATA_DIR`；
- 否则回退到仓库根目录下的 `kempower-challenge/kempower-challenge-data`（数据已随主仓库提供，无需额外下载）。

## 演讲稿

- `演讲稿_六场中英对照.md` —— 六段共 10 分钟的中英对照演示稿（含每段操作提示与口播稿）。
- `演讲稿_机柜过热单场.md` —— 机柜过热单场的中文详细讲解稿。
