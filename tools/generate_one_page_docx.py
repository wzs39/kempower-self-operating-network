import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=50, bottom=50, left=80, right=80):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def generate_one_page_docx(output_path):
    doc = docx.Document()
    
    # Page setup: A4, tight margins (0.35 in / 9mm)
    section = doc.sections[0]
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(0.35)
    section.bottom_margin = Inches(0.35)
    section.left_margin = Inches(0.35)
    section.right_margin = Inches(0.35)
    
    # Document Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(2)
    p_title.paragraph_format.line_spacing = 1.05
    run1 = p_title.add_run("Self-Operating Charging Network — ")
    run1.font.name = "Segoe UI"
    run1.font.size = Pt(13)
    run1.font.bold = True
    run1.font.color.rgb = RGBColor(22, 32, 43)
    
    run2 = p_title.add_run("One-Page Service Agreement")
    run2.font.name = "Segoe UI"
    run2.font.size = Pt(13)
    run2.font.bold = True
    run2.font.color.rgb = RGBColor(0, 163, 224) # Kempower Blue
    
    # Subtitle / Metadata
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(4)
    p_sub.paragraph_format.line_spacing = 1.05
    run_sub = p_sub.add_run(
        "Project Sentinel · Kempower Challenge, LahtiES Energy Tech Hackathon 2026 · "
        "Service Provider: Kempower Oyj / Sentinel CaaS Provider (contracts.csv, 18/29 service-scope contracts) · "
        "Client: Transit Fleet & CPO Operators · Scenario Day: 2026-11-13 · Basis: Deterministic synthetic dataset."
    )
    run_sub.font.name = "Segoe UI"
    run_sub.font.size = Pt(6.8)
    run_sub.font.color.rgb = RGBColor(86, 97, 111)

    # 3-Column Master Layout Table
    table = doc.add_table(rows=1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    col_widths = [Inches(2.48), Inches(2.48), Inches(2.48)]
    
    row = table.rows[0]
    
    # Column 1: WHAT WE PROMISE
    cell_p = row.cells[0]
    cell_p.width = col_widths[0]
    set_cell_background(cell_p, "F6FBF8")
    set_cell_margins(cell_p, top=60, bottom=60, left=80, right=80)
    
    p1 = cell_p.paragraphs[0]
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(3)
    r1 = p1.add_run("1 · WHAT WE PROMISE")
    r1.font.name = "Segoe UI"
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = RGBColor(11, 110, 79) # Green
    
    slo_text = (
        "• SLO-1 On-Time Departures: ≥ 99.5% (Titanium ≥ 99.9%, Silver ≥ 99.0%). "
        "Evaluated monthly across all scheduled trips: SoC_dep ≥ required_SoC with 0 min delay (provided MRDT is met).\n"
        "• SLO-2 Gun Availability: ≥ 99.5% per-gun uptime (available minutes ÷ 720h/mo per dispenser).\n"
        "• SLO-3 Off-Grid Islanding: ≥ 72h full-power local operation during WAN cellular outage. "
        "Maintains 1,425 kW DC (1,492 kW AC ≤ 1,500 kW grid cap at η=0.955) instead of 500 kW fallback.\n"
        "• SLO-4 Grid Limit Compliance: 100% guarantee (0 over-limit intervals in 134,400 data rows). P_AC(t) ≤ P_limit(t).\n"
        "• SLO-5 Dynamic Response: < 10ms software decision, 85ms module isolation, 260ms BBM contactor switchover (macro inter-cabinet reroute: 2.63s).\n\n"
        "Carve-Outs: Unannounced medium-voltage utility blackout or DSO hard cut on sites with no BESS (bess_kwh=0) suspends clock; "
        "dwell times < MRDT are best-effort. Announced curtailments (e.g. G1 at S2) remain within SLA commitment."
    )
    p_slo = cell_p.add_paragraph()
    p_slo.paragraph_format.space_before = Pt(0)
    p_slo.paragraph_format.space_after = Pt(2)
    p_slo.paragraph_format.line_spacing = 1.05
    r_slo = p_slo.add_run(slo_text)
    r_slo.font.name = "Segoe UI"
    r_slo.font.size = Pt(6.5)
    r_slo.font.color.rgb = RGBColor(22, 32, 43)

    # Column 2: WHAT THE SYSTEM DECIDES ALONE
    cell_d = row.cells[1]
    cell_d.width = col_widths[1]
    set_cell_background(cell_d, "F6F9FD")
    set_cell_margins(cell_d, top=60, bottom=60, left=80, right=80)
    
    p2 = cell_d.paragraphs[0]
    p2.paragraph_format.space_before = Pt(0)
    p2.paragraph_format.space_after = Pt(3)
    r2 = p2.add_run("2 · WHAT THE SYSTEM DECIDES ALONE")
    r2.font.name = "Segoe UI"
    r2.font.size = Pt(8.5)
    r2.font.bold = True
    r2.font.color.rgb = RGBColor(29, 78, 216) # Blue
    
    dec_text = (
        "• Power Allocation Per Gun: Dynamic Power Routing (DPR) matrix continuously routes 25 kW power modules across dispensers based on demand.\n"
        "• Dispatch & Charging Speed: 15-minute rolling horizon SciPy HiGHS MILP optimizer on spot prices and fleet schedules; "
        "departure urgency strictly prioritized over energy arbitrage.\n"
        "• Curtailment Load Preemption: Autonomously throttles low-urgency buffer vehicles (e.g. S2 G1 curtailment: shifts 283.50 kWh from T05–T08 to T01–T04, achieving 4 → 0 missed).\n"
        "• Fault Isolation & Thermal Rerouting: Autonomous predictive thermal derating at 59.3°C (199 min lead time); executes 260ms BBM reroute to N-1 720 kW capacity.\n"
        "• Site Rating Reconciliation: Autonomously reconciles misconfigured limits across physical cabinets (e.g. S5 600 kW → 900 kW auto-calibration).\n"
        "• Claim Verifiability: Minimum Required Duration of Telemetry (MRDT) gate verified per session before issuance of credit:\n"
        "  MRDT = ΔSoC·E_batt ÷ (min(P_chg, P_veh)·η) × 60 + 15 min (e.g. 57.11 min)."
    )
    p_dec = cell_d.add_paragraph()
    p_dec.paragraph_format.space_before = Pt(0)
    p_dec.paragraph_format.space_after = Pt(2)
    p_dec.paragraph_format.line_spacing = 1.05
    r_dec = p_dec.add_run(dec_text)
    r_dec.font.name = "Segoe UI"
    r_dec.font.size = Pt(6.5)
    r_dec.font.color.rgb = RGBColor(22, 32, 43)

    # Column 3: ACCOUNTABILITY WHEN WRONG
    cell_a = row.cells[2]
    cell_a.width = col_widths[2]
    set_cell_background(cell_a, "FDF7F7")
    set_cell_margins(cell_a, top=60, bottom=60, left=80, right=80)
    
    p3 = cell_a.paragraphs[0]
    p3.paragraph_format.space_before = Pt(0)
    p3.paragraph_format.space_after = Pt(3)
    r3 = p3.add_run("3 · ACCOUNTABILITY WHEN WRONG")
    r3.font.name = "Segoe UI"
    r3.font.size = Pt(8.5)
    r3.font.bold = True
    r3.font.color.rgb = RGBColor(155, 28, 28) # Red
    
    acc_text = (
        "Tiered Penalties Paid by Service Provider:\n"
        "• Delayed / Below-SoC Departure:\n"
        "  - Titanium: €350 per missed trip + emergency replacement cost\n"
        "  - Gold: €250 per missed trip\n"
        "  - Silver: €150 per missed trip (matches municipal penalty)\n"
        "• Delay Duration Fee: €7.50 / €5.00 / €3.00 per minute beyond grace period (10 / 15 / 20 min).\n"
        "• Energy Deficit Reimbursement: €2.00 / €1.50 / €1.00 per unsupplied kWh.\n"
        "• Availability Penalty: -2% monthly service fee per 0.1 pp deficit below 99.5% (capped at 90% fee; 0% fee if availability < 95.0%).\n"
        "• Grid Over-Limit Invariant: 100% reimbursement of all utility demand charges or grid breach penalties incurred by Client.\n"
        "• Anti-Moral-Hazard Rule: Claims rejected if vehicle arrived with dwell < MRDT or if client disconnected cable prematurely."
    )
    p_acc = cell_a.add_paragraph()
    p_acc.paragraph_format.space_before = Pt(0)
    p_acc.paragraph_format.space_after = Pt(2)
    p_acc.paragraph_format.line_spacing = 1.05
    r_acc = p_acc.add_run(acc_text)
    r_acc.font.name = "Segoe UI"
    r_acc.font.size = Pt(6.5)
    r_acc.font.color.rgb = RGBColor(22, 32, 43)

    # Bottom Signatures
    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(6)
    p_sign.paragraph_format.space_after = Pt(0)
    p_sign.paragraph_format.line_spacing = 1.05
    
    t_sign = doc.add_table(rows=1, cols=2)
    t_sign.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_sign.autofit = False
    
    c_s1 = t_sign.rows[0].cells[0]
    c_s1.width = Inches(3.78)
    p_s1 = c_s1.paragraphs[0]
    p_s1.paragraph_format.space_before = Pt(0)
    p_s1.paragraph_format.space_after = Pt(0)
    r_s1 = p_s1.add_run("SERVICE PROVIDER: Kempower Oyj / Project Sentinel CaaS\nSignature: ______________________ Date: 2026-11-07\nName: Mats Mattsson / Authorized Representative")
    r_s1.font.name = "Segoe UI"
    r_s1.font.size = Pt(6.6)
    r_s1.font.color.rgb = RGBColor(86, 97, 111)

    c_s2 = t_sign.rows[0].cells[1]
    c_s2.width = Inches(3.78)
    p_s2 = c_s2.paragraphs[0]
    p_s2.paragraph_format.space_before = Pt(0)
    p_s2.paragraph_format.space_after = Pt(0)
    r_s2 = p_s2.add_run("CLIENT / OPERATOR: Municipal Transit & Fleet Authority\nSignature: ______________________ Date: 2026-11-07\nName: Authorized Fleet Operations Director")
    r_s2.font.name = "Segoe UI"
    r_s2.font.size = Pt(6.6)
    r_s2.font.color.rgb = RGBColor(86, 97, 111)

    doc.save(output_path)
    print(f"Generated 1-Page DOCX agreement: {output_path}")

if __name__ == "__main__":
    out = "Team3-One_Page-Autonomous_Charging_Services_Agreement.docx"
    generate_one_page_docx(out)
