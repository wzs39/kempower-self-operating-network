# -*- coding: utf-8 -*-
"""
Project Sentinel: Comprehensive Bilingual Demo Day Jury Defense Playbook & Hardcore Question Bank
Compiles a publication-grade HTML and converts it into a vector A4 PDF via headless browser.
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.defense_data_bilingual import PERSONAS, ROLES, AXIOMS, CRISES
from tools.qa_items_bilingual import QA_ITEMS

HTML_OUT_PATH = REPO_ROOT / "docs" / "demo_day" / "PROJECT_SENTINEL_JURY_DEFENSE_BILINGUAL_MANUAL.html"
PDF_OUT_DOCS = REPO_ROOT / "docs" / "demo_day" / "PROJECT_SENTINEL_JURY_DEFENSE_BILINGUAL_MANUAL.pdf"
PDF_OUT_ROOT = REPO_ROOT / "PROJECT_SENTINEL_JURY_DEFENSE_BILINGUAL_MANUAL.pdf"

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

def find_browser():
    for p in EDGE_CANDIDATES:
        if os.path.exists(p):
            return p
    return None

def build_full_html() -> str:
    html = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>Project Sentinel · Demo Day Jury Defense Playbook (Bilingual / 中英双语)</title>
<style>
  @page {
    size: A4 portrait;
    margin: 12mm 14mm 14mm 14mm;
  }
  * {
    box-sizing: border-box;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }
  body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Microsoft YaHei", "PingFang SC", "Source Han Sans CN", sans-serif;
    color: #0f172a;
    background-color: #ffffff;
    line-height: 1.45;
    font-size: 9pt;
    margin: 0;
    padding: 0;
  }
  .page-break {
    page-break-before: always;
  }
  .no-break {
    page-break-inside: avoid;
  }
  .cover {
    page-break-after: always;
    text-align: center;
    padding: 35px 25px 25px 25px;
    border: 3px double #0284c7;
    border-radius: 8px;
    background: linear-gradient(135deg, #f8fafc 0%, #e0f2fe 100%);
    margin-bottom: 20px;
  }
  .cover-badge {
    display: inline-block;
    padding: 4px 14px;
    background: #0284c7;
    color: #ffffff;
    font-weight: 700;
    font-size: 9.5pt;
    border-radius: 20px;
    letter-spacing: 1px;
    margin-bottom: 12px;
  }
  .cover-title {
    font-size: 22pt;
    font-weight: 800;
    color: #0b192c;
    margin: 8px 0 4px 0;
    line-height: 1.2;
  }
  .cover-subtitle {
    font-size: 14pt;
    font-weight: 700;
    color: #0369a1;
    margin: 0 0 12px 0;
  }
  .cover-desc {
    font-size: 9.5pt;
    color: #334155;
    max-width: 650px;
    margin: 0 auto 16px auto;
  }
  .cover-meta {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
    max-width: 600px;
    margin: 0 auto 16px auto;
    text-align: left;
    font-size: 8.5pt;
    background: #ffffff;
    padding: 10px 14px;
    border-radius: 6px;
    border: 1px solid #cbd5e1;
  }
  .cover-meta div strong {
    color: #0369a1;
  }
  .section-header {
    border-bottom: 2.5px solid #0284c7;
    padding-bottom: 4px;
    margin-top: 18px;
    margin-bottom: 12px;
  }
  .section-title-en {
    font-size: 13pt;
    font-weight: 800;
    color: #0f172a;
    margin: 0;
  }
  .section-title-cn {
    font-size: 11.5pt;
    font-weight: 700;
    color: #0284c7;
    margin: 2px 0 0 0;
  }
  .card {
    background: #ffffff;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    padding: 10px 12px;
    margin-bottom: 12px;
    page-break-inside: avoid;
    box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  }
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 6px;
    margin-bottom: 8px;
  }
  .q-badge {
    background: #0f172a;
    color: #38bdf8;
    font-weight: 800;
    font-size: 9pt;
    padding: 2px 8px;
    border-radius: 4px;
    display: inline-block;
  }
  .role-tag {
    background: #f1f5f9;
    color: #334155;
    font-size: 8pt;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
    border: 1px solid #cbd5e1;
  }
  .q-title-en {
    font-size: 11pt;
    font-weight: 700;
    color: #0f172a;
    margin: 4px 0 2px 0;
  }
  .q-title-cn {
    font-size: 10pt;
    font-weight: 600;
    color: #0369a1;
    margin: 0 0 4px 0;
  }
  .qa-box {
    margin-bottom: 8px;
    border-left: 3px solid #0284c7;
    background: #f8fafc;
    padding: 6px 10px;
    border-radius: 0 4px 4px 0;
  }
  .qa-box-title {
    font-weight: 700;
    font-size: 8.5pt;
    color: #0369a1;
    margin-bottom: 3px;
    display: flex;
    align-items: center;
    gap: 5px;
  }
  .qa-text-en {
    color: #1e293b;
    margin-bottom: 3px;
    font-size: 8.5pt;
  }
  .qa-text-cn {
    color: #334155;
    font-size: 8.5pt;
    border-top: 1px dashed #cbd5e1;
    padding-top: 3px;
  }
  .proof-box {
    border-left-color: #10b981;
    background: #f0fdf4;
  }
  .proof-box .qa-box-title {
    color: #047857;
  }
  .trap-box {
    border-left-color: #f59e0b;
    background: #fffbeb;
  }
  .trap-box .qa-box-title {
    color: #b45309;
  }
  .close-box {
    border-left-color: #8b5cf6;
    background: #f5f3ff;
  }
  .close-box .qa-box-title {
    color: #6d28d9;
  }
  ul.proof-list {
    margin: 0;
    padding-left: 15px;
    font-size: 8.5pt;
  }
  ul.proof-list li {
    margin-bottom: 2px;
  }
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 8px 0;
    font-size: 8pt;
  }
  th, td {
    border: 1px solid #cbd5e1;
    padding: 5px 6px;
    text-align: left;
    vertical-align: top;
  }
  th {
    background: #f1f5f9;
    color: #0f172a;
    font-weight: 700;
  }
  tr:nth-child(even) {
    background: #f8fafc;
  }
  .code-tag {
    font-family: "JetBrains Mono", Consolas, monospace;
    background: #e2e8f0;
    padding: 1px 3px;
    border-radius: 2px;
    font-size: 7.5pt;
    color: #0f172a;
  }
</style>
</head>
<body>

<!-- COVER PAGE -->
<div class="cover">
  <div class="cover-badge">KEMPOWER CHALLENGE · LAHTIES ENERGY TECH HACKATHON 2026</div>
  <div class="cover-title">PROJECT SENTINEL: JURY DEFENSE PLAYBOOK</div>
  <div class="cover-subtitle">哨兵计划 · 演示日评委答辩攻防手册与中英双语硬核题库</div>
  <div class="cover-desc">
    <b>Definitive Bilingual Tactical Defense & Cross-Examination Playbook</b><br>
    3 Juror Archetypes · 14 Hardcore Q&As · 4-Person Tactical Division · 6 Stage Crisis Protocols<br>
    三大评审角色画像 · 14大核心硬核攻防题库 · 四人答辩协同矩阵 · 六大黑天鹅应急预案
  </div>
  <div class="cover-meta">
    <div><strong>Competition Track / 赛题:</strong> Kempower Flagship Track</div>
    <div><strong>Official Date / 日期:</strong> Saturday 07.11.2026</div>
    <div><strong>Venue / 答辩地点:</strong> LUT University Lahti Campus / CrazyTown</div>
    <div><strong>Design Perspective / 视角:</strong> Equipment Manufacturer / Turnkey Service Provider</div>
    <div><strong>Verification Standard / 检验基准:</strong> 45 Official CSVs (240,635 rows)</div>
    <div><strong>Test Status / 测试状态:</strong> 568/568 Tests Passing (100% Pass)</div>
  </div>
  <div style="font-size:8pt; color:#475569; margin-top:8px;">
    <b>Core Defense Axiom / 核心法则:</b> <i>"Every statement backed by immutable CSV rows, verified electrical physics, and non-negotiable contract SLAs."</i><br>
    <i>所有论述均以真实不可变数据集、电气物理学定律与刚性服务合同为唯一准绳。</i>
  </div>
</div>

<!-- SECTION 1: TRIPARTITE JUDGE PERSONAS -->
<div class="section-header">
  <div class="section-title-en">Part 1: Tripartite Judge Personas & Evaluation Psychology</div>
  <div class="section-title-cn">第一部分：三大评审角色画像与评分心理透视</div>
</div>
"""

    for p in PERSONAS:
        p_html = f"""
<div class="card no-break">
  <div class="card-header">
    <div>
      <span class="q-badge">{p['id']} · JUROR ARCHETYPE</span>
      <span style="font-weight:700; font-size:10.5pt; margin-left:8px; color:#0f172a;">{p['title_en']}</span>
      <span style="font-weight:600; font-size:9.5pt; color:#0284c7; margin-left:6px;">({p['title_cn']})</span>
    </div>
    <span class="role-tag">{p['representatives']}</span>
  </div>
  
  <div class="qa-box" style="border-left-color:#3b82f6;">
    <div class="qa-box-title">🧠 Psychological Mindset / 评审心理特征</div>
    <div class="qa-text-en"><strong>[EN]:</strong> {p['mindset_en']}</div>
    <div class="qa-text-cn"><strong>[CN]:</strong> {p['mindset_cn']}</div>
  </div>

  <div class="qa-box proof-box">
    <div class="qa-box-title">🎯 Core Priorities & Evaluation Weights / 核心关注点与评分权重</div>
    <div class="qa-text-en">
      <ul class="proof-list">
        {''.join([f"<li>{item}</li>" for item in p['priorities_en']])}
      </ul>
    </div>
    <div class="qa-text-cn">
      <ul class="proof-list">
        {''.join([f"<li>{item}</li>" for item in p['priorities_cn']])}
      </ul>
    </div>
  </div>

  <div class="qa-box trap-box">
    <div class="qa-box-title">⚠️ Red-Flag Triggers & Pet Peeves / 扣分雷区与禁忌</div>
    <div class="qa-text-en"><strong>[EN]:</strong> {p['red_flags_en']}</div>
    <div class="qa-text-cn"><strong>[CN]:</strong> {p['red_flags_cn']}</div>
  </div>

  <div class="qa-box close-box">
    <div class="qa-box-title">💬 Signature Cross-Examination Style / 典型质询提问风格</div>
    <div class="qa-text-en"><em>{p['style_en']}</em></div>
    <div class="qa-text-cn"><em>{p['style_cn']}</em></div>
  </div>
</div>
"""
        html += p_html

    # SECTION 2: 14 HARDCORE Q&A PLAYBOOK
    html += """
<div class="section-header page-break">
  <div class="section-title-en">Part 2: 14 Core Hardcore Questions & Structured Defense Playbook</div>
  <div class="section-title-cn">第二部分：14 大核心硬核攻防题库与结构化应答白皮书</div>
</div>
"""

    for q in QA_ITEMS:
        proof_en_items = "".join([f"<li>{item}</li>" for item in q['proof_en']])
        proof_cn_items = "".join([f"<li>{item}</li>" for item in q['proof_cn']])
        
        q_html = f"""
<div class="card no-break">
  <div class="card-header">
    <div>
      <span class="q-badge">{q['id']}</span>
      <span style="font-weight:700; font-size:10.5pt; margin-left:6px; color:#0f172a;">{q['title_en']}</span>
      <span style="font-weight:600; font-size:9.5pt; color:#0284c7; margin-left:6px;">({q['title_cn']})</span>
    </div>
    <span class="role-tag">Primary: {q['responder_en']}</span>
  </div>

  <!-- Juror Statement -->
  <div class="qa-box" style="border-left-color:#0284c7;">
    <div class="qa-box-title">🎙️ Juror Question Statement / 评委原话提问</div>
    <div class="qa-text-en"><strong>[EN]:</strong> <em>"{q['statement_en']}"</em></div>
    <div class="qa-text-cn"><strong>[CN]:</strong> <em>“{q['statement_cn']}”</em></div>
  </div>

  <!-- Underlying Trap -->
  <div class="qa-box trap-box">
    <div class="qa-box-title">⚠️ Juror Psychological Trap & Intent / 提问动机与底层陷阱分析</div>
    <div class="qa-text-en"><strong>[EN]:</strong> {q['trap_en']}</div>
    <div class="qa-text-cn"><strong>[CN]:</strong> {q['trap_cn']}</div>
  </div>

  <!-- Opening Stance -->
  <div class="qa-box" style="border-left-color:#0f172a; background:#f1f5f9;">
    <div class="qa-box-title">🎯 Opening Stance / 开门见山立论</div>
    <div class="qa-text-en"><strong>[EN]:</strong> <strong>"{q['opening_en']}"</strong></div>
    <div class="qa-text-cn"><strong>[CN]:</strong> <strong>“{q['opening_cn']}”</strong></div>
  </div>

  <!-- Quantitative Proof -->
  <div class="qa-box proof-box">
    <div class="qa-box-title">📊 Quantitative Proof & Citations / 量化证据链与数据出处</div>
    <div class="qa-text-en">
      <ul class="proof-list">{proof_en_items}</ul>
    </div>
    <div class="qa-text-cn">
      <ul class="proof-list">{proof_cn_items}</ul>
    </div>
  </div>

  <!-- Architectural Mechanism -->
  <div class="qa-box" style="border-left-color:#6366f1; background:#eef2ff;">
    <div class="qa-box-title">⚙️ Architectural & Physical Mechanism / 底层物理机理与控制逻辑</div>
    <div class="qa-text-en"><strong>[EN]:</strong> {q['arch_en']}</div>
    <div class="qa-text-cn"><strong>[CN]:</strong> {q['arch_cn']}</div>
  </div>

  <!-- Preemptive Close -->
  <div class="qa-box close-box">
    <div class="qa-box-title">🛡️ Preemptive Close & Counter-Strike / 连环追问反杀与闭环金句</div>
    <div class="qa-text-en"><strong>[EN]:</strong> <em>"{q['close_en']}"</em></div>
    <div class="qa-text-cn"><strong>[CN]:</strong> <em>“{q['close_cn']}”</em></div>
  </div>
</div>
"""
        html += q_html

    # SECTION 3: TEAM SYNERGY & INVARIANT AXIOMS
    html += """
<div class="section-header page-break">
  <div class="section-title-en">Part 3: Team Synergy, 4-Member Role Matrix & Invariant Axioms</div>
  <div class="section-title-cn">第三部分：四人答辩协同分工与五大不可违背公理</div>
</div>

<div class="card no-break">
  <div class="card-header">
    <span class="q-badge">TEAM FORMATION</span>
    <span style="font-weight:700; font-size:10.5pt; color:#0f172a;">4-Member Defense Responsibilities & Hand-off Protocol</span>
  </div>
  <table>
    <thead>
      <tr>
        <th style="width:18%;">Role / 角色与站位</th>
        <th style="width:34%;">Scope of Authority / 答辩主控范围</th>
        <th style="width:24%;">Verbatim Bridge / 交接暗号口令</th>
        <th style="width:24%;">Tactical Rescue / 兜底救援预案</th>
      </tr>
    </thead>
    <tbody>
"""
    for r in ROLES:
        html += f"""
      <tr>
        <td><strong>{r['role']}</strong><br><span style="color:#0284c7;">{r['title_cn']}</span><br><small style="color:#64748b;">{r['stage_pos']}</small></td>
        <td><strong>[EN]:</strong> {r['scope_en']}<br><strong>[CN]:</strong> {r['scope_cn']}</td>
        <td><strong>[EN]:</strong> <em>{r['bridge_en']}</em><br><strong>[CN]:</strong> <em>{r['bridge_cn']}</em></td>
        <td><strong>[EN]:</strong> {r['rescue_en']}<br><strong>[CN]:</strong> {r['rescue_cn']}</td>
      </tr>
"""
    html += """
    </tbody>
  </table>
</div>

<div class="card no-break">
  <div class="card-header">
    <span class="q-badge" style="background:#047857; color:#ffffff;">GOLDEN AXIOMS</span>
    <span style="font-weight:700; font-size:10.5pt; color:#0f172a;">Five Non-Negotiable Quantitative Axioms / 五大黄金数据公理</span>
  </div>
  <table>
    <thead>
      <tr>
        <th style="width:30%;">Axiom Title / 公理名称</th>
        <th style="width:70%;">Quantitative Engineering Truth / 量化工程事实与论据</th>
      </tr>
    </thead>
    <tbody>
"""
    for a in AXIOMS:
        html += f"""
      <tr>
        <td><strong>{a['axiom_en']}</strong><br><span style="color:#0284c7;">{a['axiom_cn']}</span></td>
        <td><strong>[EN]:</strong> {a['details_en']}<br><strong>[CN]:</strong> {a['details_cn']}</td>
      </tr>
"""
    html += """
    </tbody>
  </table>
</div>

<!-- SECTION 4: STAGE CRISIS RESPONSE MANUAL -->
<div class="section-header page-break">
  <div class="section-title-en">Part 4: Stage Crisis Emergency Response Protocols</div>
  <div class="section-title-cn">第四部分：现场六大黑天鹅极端突发危机处置预案</div>
</div>
"""

    for c in CRISES:
        c_html = f"""
<div class="card no-break">
  <div class="card-header">
    <div>
      <span class="q-badge" style="background:#dc2626; color:#ffffff;">{c['id']}</span>
      <span style="font-weight:700; font-size:10.5pt; margin-left:6px; color:#0f172a;">{c['title_en']}</span>
      <span style="font-weight:600; font-size:9.5pt; color:#dc2626; margin-left:6px;">({c['title_cn']})</span>
    </div>
  </div>

  <div class="qa-box trap-box">
    <div class="qa-box-title">⚡ Trigger Event / 触发险情</div>
    <div class="qa-text-en"><strong>Trigger:</strong> {c['trigger']}</div>
  </div>

  <div class="qa-box proof-box">
    <div class="qa-box-title">🛡️ Standard Operating Procedure (SOP) / 处置流程与行动准则</div>
    <div class="qa-text-en"><strong>[EN]:</strong> {c['action_en']}</div>
    <div class="qa-text-cn"><strong>[CN]:</strong> {c['action_cn']}</div>
  </div>
</div>
"""
        html += c_html

    html += """
<div class="card no-break" style="background:#f8fafc; border-top:2px solid #0284c7; text-align:center; padding:15px; margin-top:20px;">
  <div style="font-weight:800; font-size:11pt; color:#0f172a;">PROJECT SENTINEL · CERTAINTY AS A SERVICE</div>
  <div style="font-size:9pt; color:#0284c7; font-weight:600; margin:3px 0;">哨兵计划 · 迈向确定性的无人化自愈充电新纪元</div>
  <div style="font-size:8pt; color:#64748b;">
    Kempower Flagship Challenge · LahtiES Energy Tech Hackathon 2026 · LUT University Lahti / CrazyTown<br>
    568 Automated Tests Passing (100%) · 45 Official CSVs Unmodified · Zero CJK Presentation Rule Verified
  </div>
</div>

</body>
</html>
"""
    return html

def main():
    browser = find_browser()
    if not browser:
        print("[ERROR] No Edge/Chrome executable found.")
        sys.exit(1)

    print(f"[1/4] Found headless browser: {browser}")
    print("[2/4] Assembling full publication HTML...")
    html_content = build_full_html()

    os.makedirs(HTML_OUT_PATH.parent, exist_ok=True)
    with open(HTML_OUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"[OK] HTML written: {HTML_OUT_PATH} ({len(html_content):,} chars)")

    print("[3/4] Compiling vector PDF via headless browser...")
    cmd = [
        browser,
        "--headless",
        "--disable-gpu",
        "--no-pdf-header-footer",
        f"--print-to-pdf={str(PDF_OUT_DOCS)}",
        str(HTML_OUT_PATH),
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"[ERROR] Headless browser returned code {res.returncode}")
        print(res.stderr)
        sys.exit(res.returncode)

    if not PDF_OUT_DOCS.exists() or PDF_OUT_DOCS.stat().st_size == 0:
        print("[ERROR] PDF generation failed or output is empty.")
        sys.exit(1)

    # Mirror to root directory
    shutil.copy2(PDF_OUT_DOCS, PDF_OUT_ROOT)
    print(f"[OK] PDF generated at docs: {PDF_OUT_DOCS} ({PDF_OUT_DOCS.stat().st_size:,} bytes)")
    print(f"[OK] PDF mirrored to root : {PDF_OUT_ROOT} ({PDF_OUT_ROOT.stat().st_size:,} bytes)")

    # Verify with PyMuPDF
    try:
        import fitz
        doc = fitz.open(PDF_OUT_DOCS)
        page_count = len(doc)
        print(f"[4/4] PDF Verified via PyMuPDF: {page_count} pages, {PDF_OUT_DOCS.stat().st_size / 1024:.1f} KB")
        doc.close()
    except Exception as e:
        print(f"[WARN] PyMuPDF inspection skipped: {e}")

    print("\n[SUCCESS] Bilingual Jury Defense PDF manual generated successfully!")

if __name__ == "__main__":
    main()
