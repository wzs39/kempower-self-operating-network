"""
Project Sentinel: 12-Slide Championship Pitch Deck Generator
Target: Microsoft PowerPoint ECMA-376 (.pptx) via python-pptx
Standard: 16:9 Widescreen (13.333 in x 7.500 in)
Language: Strictly 100% English across all slides and speaker notes
Design System: Nordic Executive Deep Slate (Apple Keynote / Stripe Tech Aesthetic)
Animations: Native OpenXML <p:transition> (Morph/Fade) & <p:timing> Sequential Build Animations
"""

import os
import sys
from typing import Optional, List, Tuple, Any
import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
from pptx.oxml.ns import nsdecls


class Theme:
    """Nordic Executive Deep Slate Palette & Design Tokens."""
    # 60% Canvas & Containers
    BG_DARK = RGBColor(9, 13, 22)               # #090D16 Deep Matte Basalt Slate
    CARD_BG = RGBColor(17, 24, 42)              # #11182A Solid Surface Slate
    CARD_BG_MUTED = RGBColor(14, 20, 34)        # #0E1422 Problem / Challenge Container
    CARD_BG_ACCENT = RGBColor(20, 30, 52)       # #141E34 Solution Container
    CARD_BG_CHIP = RGBColor(13, 18, 30)         # #0D121E Inner Chip Container
    
    # 0.5pt Hairline Borders (Disciplined, no glowing neon)
    CARD_BORDER = RGBColor(30, 41, 59)          # #1E293B Subtle Hairline Border
    CARD_BORDER_FOCUS = RGBColor(0, 145, 255)   # #0091FF Electric Blue Border Focus
    
    # 10% Accents
    BLUE_ACCENT = RGBColor(0, 145, 255)         # #0091FF Kempower Electric Blue Primary
    CYAN_HERO = RGBColor(0, 229, 255)           # #00E5FF Highlight Cyan
    CORAL_RED = RGBColor(248, 113, 113)         # #F87171 Soft Coral Red (Pain Points / Legacy)
    EMERALD_SUCCESS = RGBColor(16, 185, 129)    # #10B981 Emerald Green (Autonomous Success)
    AMBER_ALERT = RGBColor(245, 158, 11)        # #F59E0B Warning / Notice
    
    # 30% Executive Typography
    TEXT_PRIMARY = RGBColor(255, 255, 255)      # #FFFFFF Pure Crisp White
    TEXT_SECONDARY = RGBColor(203, 213, 225)    # #CBD5E1 Light Slate Body
    TEXT_MUTED = RGBColor(148, 163, 184)        # #94A3B8 Secondary Slate 400
    TEXT_DARK = RGBColor(100, 116, 139)         # #64748B Metadata & Footers


class Layout:
    """16:9 Widescreen Geometry Coordinates."""
    SLIDE_WIDTH = Inches(13.333)
    SLIDE_HEIGHT = Inches(7.500)
    LEFT_MARGIN = Inches(0.80)
    CONTENT_WIDTH = Inches(11.733)
    CONTENT_TOP = Inches(1.80)
    CONTENT_HEIGHT = Inches(4.90)


# ============================================================================
# OpenXML Native Animation & Transition Utilities
# ============================================================================

def add_slide_transition(slide, transition_type: str = "fade"):
    """Appends smooth slide transition (morph or fade) to the slide element."""
    if transition_type == "morph":
        trans_xml = f'<p:transition {nsdecls("p")} advClick="1"><p:morph/></p:transition>'
    else:
        trans_xml = f'<p:transition {nsdecls("p")} advClick="1"><p:fade/></p:transition>'
    slide._element.append(parse_xml(trans_xml))


def add_sequential_build_animation(slide, shape_ids: List[str]):
    """Adds on-click sequential fade-in animations to the specified shapes in order."""
    if not shape_ids:
        return
    
    par_elements = []
    c_tn_counter = 3
    for sp_id in shape_ids:
        p_id = c_tn_counter
        p2_id = c_tn_counter + 1
        p3_id = c_tn_counter + 2
        p4_id = c_tn_counter + 3
        c_tn_counter += 4
        par_elements.append(f"""
        <p:par>
          <p:cTn id="{p_id}" fill="hold">
            <p:stCondLst><p:cond delay="0"/></p:stCondLst>
            <p:childTnLst>
              <p:par>
                <p:cTn id="{p2_id}" fill="hold">
                  <p:stCondLst><p:cond delay="0"/></p:stCondLst>
                  <p:childTnLst>
                    <p:set>
                      <p:cBhvr>
                        <p:cTn id="{p3_id}" dur="1" fill="hold"/>
                        <p:tgtEl><p:spTgt spid="{sp_id}"/></p:tgtEl>
                        <p:attrNameLst><p:attrName>style.visibility</p:attrName></p:attrNameLst>
                      </p:cBhvr>
                      <p:to><p:strVal val="visible"/></p:to>
                    </p:set>
                    <p:animEffect transition="in" filter="fade">
                      <p:cBhvr>
                        <p:cTn id="{p4_id}" dur="400"/>
                        <p:tgtEl><p:spTgt spid="{sp_id}"/></p:tgtEl>
                      </p:cBhvr>
                    </p:animEffect>
                  </p:childTnLst>
                </p:cTn>
              </p:par>
            </p:childTnLst>
          </p:cTn>
        </p:par>""")

    timing_xml = f"""<p:timing {nsdecls("p")}>
  <p:tnLst>
    <p:par>
      <p:cTn id="1" dur="indefinite" restart="always" nodeType="tmRoot">
        <p:childTnLst>
          <p:seq concurrent="1" nextAc="seek">
            <p:cTn id="2" dur="indefinite" nodeType="mainSeq">
              <p:childTnLst>
                {''.join(par_elements)}
              </p:childTnLst>
            </p:cTn>
          </p:seq>
        </p:childTnLst>
      </p:cTn>
    </p:par>
  </p:tnLst>
</p:timing>"""
    slide._element.append(parse_xml(timing_xml))


# ============================================================================
# Visual Component Builders
# ============================================================================

def apply_background(slide):
    """Draws full-slide background rectangle ensuring clean dark mode."""
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Layout.SLIDE_WIDTH, Layout.SLIDE_HEIGHT)
    bg.fill.solid()
    bg.fill.fore_color.rgb = Theme.BG_DARK
    bg.line.fill.background()
    return bg


def add_header(slide, category: str, title: str, subtitle: str, pill_color: RGBColor = Theme.BLUE_ACCENT):
    """Adds conclusion-first header band: category pill, master title, and subtitle."""
    pill_w = max(Inches(2.2), Inches(len(category) * 0.085 + 0.50))
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Layout.LEFT_MARGIN, Inches(0.48), pill_w, Inches(0.26))
    pill.fill.solid()
    pill.fill.fore_color.rgb = Theme.CARD_BG_CHIP
    pill.line.color.rgb = pill_color
    pill.line.width = Pt(0.75)
    tf_p = pill.text_frame
    tf_p.word_wrap = False
    tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
    p = tf_p.paragraphs[0]
    p.text = category.upper()
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Segoe UI"
    p.font.size = Pt(8.5)
    p.font.bold = True
    p.font.color.rgb = pill_color

    tb_title = slide.shapes.add_textbox(Layout.LEFT_MARGIN, Inches(0.80), Layout.CONTENT_WIDTH, Inches(0.50))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = tf_t.margin_right = tf_t.margin_top = tf_t.margin_bottom = 0
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(21)
    p_t.font.bold = True
    p_t.font.color.rgb = Theme.TEXT_PRIMARY

    tb_sub = slide.shapes.add_textbox(Layout.LEFT_MARGIN, Inches(1.33), Layout.CONTENT_WIDTH, Inches(0.35))
    tf_s = tb_sub.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = tf_s.margin_right = tf_s.margin_top = tf_s.margin_bottom = 0
    p_s = tf_s.paragraphs[0]
    p_s.text = subtitle
    p_s.font.name = "Segoe UI"
    p_s.font.size = Pt(11.0)
    p_s.font.color.rgb = Theme.TEXT_MUTED


def add_footer(slide, current_slide: int, total_slides: int = 12):
    """Adds standardized bottom metadata bar and slide pagination."""
    tb_footer = slide.shapes.add_textbox(Layout.LEFT_MARGIN, Inches(7.08), Inches(9.0), Inches(0.25))
    tf = tb_footer.text_frame
    tf.word_wrap = False
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]
    p.text = "Project Sentinel · Autonomous Charging Network Core  |  LahtiES Hackathon 2026 @ Kempower"
    p.font.name = "Segoe UI"
    p.font.size = Pt(8.5)
    p.font.color.rgb = Theme.TEXT_DARK

    tb_num = slide.shapes.add_textbox(Inches(10.5), Inches(7.08), Inches(2.033), Inches(0.25))
    tf_num = tb_num.text_frame
    tf_num.word_wrap = False
    tf_num.margin_left = tf_num.margin_right = tf_num.margin_top = tf_num.margin_bottom = 0
    p_num = tf_num.paragraphs[0]
    p_num.alignment = PP_ALIGN.RIGHT
    p_num.text = f"{current_slide:02d} / {total_slides:02d}"
    p_num.font.name = "Segoe UI"
    p_num.font.size = Pt(8.5)
    p_num.font.color.rgb = Theme.TEXT_DARK


def create_card(slide, left, top, width, height, 
                bg_color: RGBColor = Theme.CARD_BG, 
                border_color: RGBColor = Theme.CARD_BORDER, 
                line_width_pt: float = 0.5):
    """Creates a container card with fine hairline border."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(line_width_pt)
    else:
        card.line.fill.background()
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.16)
    tf.margin_bottom = Inches(0.14)
    return card


def add_process_flow_badges(slide, steps: List[Tuple[str, str]], top_y = Inches(1.80), height = Inches(0.48)) -> List[Any]:
    """
    Renders high-hierarchy dynamic process flow badges:
    'STEP 1: DETECT' -> 'STEP 2: ISOLATE' -> 'STEP 3: REROUTE' -> 'STEP 4: ZERO DEFICIT'
    Returns list of step box shapes for OpenXML timing sequential animation.
    """
    num_steps = len(steps)
    total_w = Layout.CONTENT_WIDTH
    arrow_w = Inches(0.35)
    total_arrow_w = arrow_w * (num_steps - 1)
    badge_w = (total_w - total_arrow_w) / num_steps
    
    badge_shapes = []
    for i, (step_title, step_desc) in enumerate(steps):
        bx = Layout.LEFT_MARGIN + i * (badge_w + arrow_w)
        is_final = (i == num_steps - 1)
        border_col = Theme.EMERALD_SUCCESS if is_final else (Theme.BLUE_ACCENT if i == 0 else Theme.CARD_BORDER_FOCUS)
        
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, top_y, badge_w, height)
        box.fill.solid()
        box.fill.fore_color.rgb = Theme.CARD_BG_CHIP
        box.line.color.rgb = border_col
        box.line.width = Pt(1.0 if is_final else 0.75)
        box.adjustments[0] = 0.08
        
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.06)
        tf.margin_right = Inches(0.06)
        tf.margin_top = Inches(0.04)
        tf.margin_bottom = Inches(0.04)
        
        p0 = tf.paragraphs[0]
        p0.text = step_title
        p0.font.name = "Segoe UI"
        p0.font.size = Pt(8.5)
        p0.font.bold = True
        p0.font.color.rgb = Theme.EMERALD_SUCCESS if is_final else Theme.BLUE_ACCENT
        p0.alignment = PP_ALIGN.CENTER
        
        p1 = tf.add_paragraph()
        p1.text = step_desc
        p1.font.name = "Segoe UI"
        p1.font.size = Pt(8.0)
        p1.font.color.rgb = Theme.TEXT_PRIMARY if is_final else Theme.TEXT_SECONDARY
        p1.alignment = PP_ALIGN.CENTER
        
        badge_shapes.append(box)
        
        if i < num_steps - 1:
            ax = bx + badge_w
            tb_arr = slide.shapes.add_textbox(ax, top_y, arrow_w, height)
            tf_a = tb_arr.text_frame
            tf_a.margin_left = tf_a.margin_right = tf_a.margin_top = tf_a.margin_bottom = 0
            p_a = tf_a.paragraphs[0]
            p_a.text = "➔"
            p_a.font.name = "Segoe UI"
            p_a.font.size = Pt(12.0)
            p_a.font.bold = True
            p_a.font.color.rgb = Theme.TEXT_MUTED
            p_a.alignment = PP_ALIGN.CENTER
            
    return badge_shapes


def get_shape_id(shape) -> str:
    """Extracts OpenXML shape ID for animation timeline sequencing."""
    return str(shape._element.spPr.getparent().nvSpPr.cNvPr.get("id"))


def add_speaker_notes(slide, notes_text: str):
    """Sets English speaker notes on the slide."""
    notes_slide = slide.notes_slide
    text_frame = notes_slide.notes_text_frame
    text_frame.text = notes_text.strip()


# ============================================================================
# Slide Builders (12 Dynamic, Layered, All-English Slides)
# ============================================================================

def build_slide_1(prs):
    """Slide 1: Cover & North Star Vision."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)

    # Category Pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Layout.LEFT_MARGIN, Inches(1.30), Inches(4.2), Inches(0.35))
    pill.fill.solid()
    pill.fill.fore_color.rgb = Theme.CARD_BG_CHIP
    pill.line.color.rgb = Theme.BLUE_ACCENT
    pill.line.width = Pt(0.75)
    tf_p = pill.text_frame
    p = tf_p.paragraphs[0]
    p.text = "KEMPOWER CHALLENGE 2026 · CHAMPIONSHIP ROADSHOW"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = Theme.BLUE_ACCENT

    # Main Hero Title
    tb_title = slide.shapes.add_textbox(Layout.LEFT_MARGIN, Inches(1.80), Inches(11.5), Inches(1.6))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "PROJECT SENTINEL"
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(46)
    p_t.font.bold = True
    p_t.font.color.rgb = Theme.TEXT_PRIMARY

    p_sub = tf_t.add_paragraph()
    p_sub.text = "The Autonomous Charging Network Core"
    p_sub.font.name = "Segoe UI"
    p_sub.font.size = Pt(24)
    p_sub.font.bold = True
    p_sub.font.color.rgb = Theme.BLUE_ACCENT
    p_sub.space_before = Pt(8)

    # Radical Question
    tb_quote = slide.shapes.add_textbox(Layout.LEFT_MARGIN, Inches(3.60), Inches(11.5), Inches(0.70))
    tf_q = tb_quote.text_frame
    p_q = tf_q.paragraphs[0]
    p_q.text = '"If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?"'
    p_q.font.name = "Segoe UI"
    p_q.font.size = Pt(15)
    p_q.font.italic = True
    p_q.font.color.rgb = Theme.TEXT_SECONDARY

    # 3 North Star Cards
    card_w = Inches(3.65)
    card_h = Inches(1.80)
    top_pos = Inches(4.55)

    c1 = create_card(slide, Layout.LEFT_MARGIN, top_pos, card_w, card_h, Theme.CARD_BG)
    tf1 = c1.text_frame
    p1 = tf1.paragraphs[0]
    p1.text = "THE NORTH STAR OBJECTIVE"
    p1.font.size = Pt(9)
    p1.font.bold = True
    p1.font.color.rgb = Theme.CORAL_RED
    p1_v = tf1.add_paragraph()
    p1_v.text = "Eliminate 20.76 FTE"
    p1_v.font.size = Pt(20)
    p1_v.font.bold = True
    p1_v.font.color.rgb = Theme.TEXT_PRIMARY
    p1_v.space_before = Pt(4)
    p1_d = tf1.add_paragraph()
    p1_d.text = "Remove continuous manual labor across 100 commercial depot and highway sites."
    p1_d.font.size = Pt(10.5)
    p1_d.font.color.rgb = Theme.TEXT_MUTED
    p1_d.space_before = Pt(4)

    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(4.04), top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.BLUE_ACCENT, 1.0)
    tf2 = c2.text_frame
    p2 = tf2.paragraphs[0]
    p2.text = "THE AUTONOMOUS FOUNDATION"
    p2.font.size = Pt(9)
    p2.font.bold = True
    p2.font.color.rgb = Theme.BLUE_ACCENT
    p2_v = tf2.add_paragraph()
    p2_v.text = "25kW Busbar & Edge FSM"
    p2_v.font.size = Pt(20)
    p2_v.font.bold = True
    p2_v.font.color.rgb = Theme.TEXT_PRIMARY
    p2_v.space_before = Pt(4)
    p2_d = tf2.add_paragraph()
    p2_d.text = "260ms hardware Break-Before-Make contactors over shared DC busbars."
    p2_d.font.size = Pt(10.5)
    p2_d.font.color.rgb = Theme.TEXT_MUTED
    p2_d.space_before = Pt(4)

    c3 = create_card(slide, Layout.LEFT_MARGIN + Inches(8.08), top_pos, card_w, card_h, Theme.CARD_BG)
    tf3 = c3.text_frame
    p3 = tf3.paragraphs[0]
    p3.text = "COMMERCIAL SLA BOTTOM LINE"
    p3.font.size = Pt(9)
    p3.font.bold = True
    p3.font.color.rgb = Theme.EMERALD_SUCCESS
    p3_v = tf3.add_paragraph()
    p3_v.text = "€ 1,821,534 / Yr"
    p3_v.font.size = Pt(20)
    p3_v.font.bold = True
    p3_v.font.color.rgb = Theme.TEXT_PRIMARY
    p3_v.space_before = Pt(4)
    p3_d = tf3.add_paragraph()
    p3_d.text = "OPEX savings delivering an 8.4-month payback on hardware retrofits."
    p3_d.font.size = Pt(10.5)
    p3_d.font.color.rgb = Theme.TEXT_MUTED
    p3_d.space_before = Pt(4)

    add_footer(slide, 1)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(c1), get_shape_id(c2), get_shape_id(c3)])

    add_speaker_notes(slide, """
[00:00 - 00:30] Slide 1: Welcome & North Star Hook
"Good afternoon, members of the jury.
The challenge Kempower put to us was radical: 'If humans were no longer allowed to continuously operate and maintain a charging network, how would you redesign it?'
Today, charging networks rely on an invisible army of 20.76 FTE technicians manually swapping cables, rebooting frozen controllers, and nursing faulted cabinets.
We built Project Sentinel. Sentinel is an autonomous operating core that eliminates continuous human intervention. It ensures every vehicle leaves on time, protects grid transformers, and delivers 1.82 million euros in annual savings.
Let us examine the empirical reality."
""")


def build_slide_2(prs):
    """Slide 2: The 20.76 FTE Crisis."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)
    add_header(slide, "Empirical Ground Truth", 
               "The 20.76 FTE Crisis: 47.9% of Labor Spent Swapping Cables in Freezing Depots", 
               "Forensic audit of 240,635 rows across all 45 official Kempower Challenge dataset CSVs.")

    card_w = Inches(3.65)
    card_h = Inches(4.75)
    top_pos = Layout.CONTENT_TOP

    # Card 1: Total Labor
    c1 = create_card(slide, Layout.LEFT_MARGIN, top_pos, card_w, card_h, Theme.CARD_BG_MUTED)
    tf1 = c1.text_frame
    tf1.paragraphs[0].text = "TOTAL HUMAN INTERVENTIONS"
    tf1.paragraphs[0].font.size = Pt(9.5)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.CORAL_RED
    
    p1 = tf1.add_paragraph()
    p1.text = "8,852 Ops"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = Theme.TEXT_PRIMARY
    p1.space_before = Pt(4)

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "20.76 FTE Required"
    p1_sub.font.size = Pt(13)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = Theme.CORAL_RED
    p1_sub.space_before = Pt(2)

    p1_desc = tf1.add_paragraph()
    p1_desc.text = "Across 100 commercial and highway stations, 14 days of operations consumed 93,412 technician minutes.\n\nAnnualized under Finnish statutory work hours (37.5 h/wk), this demands 20.76 full-time staff running in place."
    p1_desc.font.size = Pt(11)
    p1_desc.font.color.rgb = Theme.TEXT_MUTED
    p1_desc.space_before = Pt(12)

    p1_box = tf1.add_paragraph()
    p1_box.text = "ANNUAL LABOR OPEX BURN\n€ 1,821,534 / Year"
    p1_box.font.size = Pt(12)
    p1_box.font.bold = True
    p1_box.font.color.rgb = Theme.TEXT_PRIMARY
    p1_box.space_before = Pt(16)

    # Card 2: Replug Bottleneck
    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(4.04), top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.AMBER_ALERT, 1.0)
    tf2 = c2.text_frame
    tf2.paragraphs[0].text = "THE REPLUG BOTTLENECK"
    tf2.paragraphs[0].font.size = Pt(9.5)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.AMBER_ALERT
    
    p2 = tf2.add_paragraph()
    p2.text = "5,596 Events"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = Theme.TEXT_PRIMARY
    p2.space_before = Pt(4)

    p2_sub = tf2.add_paragraph()
    p2_sub.text = "47.93% of Total Labor Time"
    p2_sub.font.size = Pt(13)
    p2_sub.font.bold = True
    p2_sub.font.color.rgb = Theme.AMBER_ALERT
    p2_sub.space_before = Pt(2)

    p2_desc = tf2.add_paragraph()
    p2_desc.text = "In commercial depots (e.g. S1), 24 buses share only 12 dispensers (1:2 ratio).\n\nNight staff must wake up at 00:30 and walk 9 rounds in freezing weather just to unplug full buses and plug in empty ones."
    p2_desc.font.size = Pt(11)
    p2_desc.font.color.rgb = Theme.TEXT_MUTED
    p2_desc.space_before = Pt(12)

    p2_box = tf2.add_paragraph()
    p2_box.text = "SINGLE-TASK WASTED LABOR\n9.95 FTE (€ 872,976 / yr)"
    p2_box.font.size = Pt(12)
    p2_box.font.bold = True
    p2_box.font.color.rgb = Theme.TEXT_PRIMARY
    p2_box.space_before = Pt(16)

    # Card 3: Scenario Day Crisis
    c3 = create_card(slide, Layout.LEFT_MARGIN + Inches(8.08), top_pos, card_w, card_h, Theme.CARD_BG_MUTED)
    tf3 = c3.text_frame
    tf3.paragraphs[0].text = "SCENARIO DAY COLLAPSE"
    tf3.paragraphs[0].font.size = Pt(9.5)
    tf3.paragraphs[0].font.bold = True
    tf3.paragraphs[0].font.color.rgb = Theme.CORAL_RED
    
    p3 = tf3.add_paragraph()
    p3.text = "13 Missed"
    p3.font.size = Pt(36)
    p3.font.bold = True
    p3.font.color.rgb = Theme.TEXT_PRIMARY
    p3.space_before = Pt(4)

    p3_sub = tf3.add_paragraph()
    p3_sub.text = "1,804.5 kWh Deficit"
    p3_sub.font.size = Pt(13)
    p3_sub.font.bold = True
    p3_sub.font.color.rgb = Theme.CORAL_RED
    p3_sub.space_before = Pt(2)

    p3_desc = tf3.add_paragraph()
    p3_desc.text = "On Friday 2026-11-13, compounding hardware trips and network blackouts overwhelmed manual responders.\n\n13 commercial fleet vehicles failed departure deadlines, and public hub S3 suffered 29.69% driver abandonment."
    p3_desc.font.size = Pt(11)
    p3_desc.font.color.rgb = Theme.TEXT_MUTED
    p3_desc.space_before = Pt(12)

    p3_box = tf3.add_paragraph()
    p3_box.text = "LATE DEPARTURE PENALTIES\n€ 150 – 250 / Vehicle Delay"
    p3_box.font.size = Pt(12)
    p3_box.font.bold = True
    p3_box.font.color.rgb = Theme.TEXT_PRIMARY
    p3_box.space_before = Pt(16)

    add_footer(slide, 2)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(c1), get_shape_id(c2), get_shape_id(c3)])

    add_speaker_notes(slide, """
[00:30 - 01:30] Slide 2: The Empirical Baseline
"We audited all 240,635 rows across the 45 official CSVs.
Here is the baseline: across 100 sites, 8,852 manual operations burned 93,412 minutes in just two weeks. Under statutory Finnish labor laws, that is 20.76 full-time staff costing 1.82 million euros annually.
Notice the central card: 47.93% of all human labor is spent on a single repetitive task: unplugging a bus at 2 AM to plug in the next one.
When crisis hit on Friday, November 13th, the human system broke down entirely: 13 commercial fleet vehicles were stranded, over 1,800 kWh of energy was lost, and public drivers abandoned chargers in frustration.
We engineered Sentinel to eliminate all 20.76 FTEs."
""")


def build_slide_3(prs):
    """Slide 3: Two-Tier Architecture."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)
    add_header(slide, "System Architecture", 
               "Two-Tier Decoupled Core: Offline Edge FSM (L2) + Cloud Rolling MILP (L3)", 
               "Physics-grounded deterministic safety over Kempower 25kW hardware with zero cloud single-point-of-failure.")

    card_w = Inches(5.65)
    card_h = Inches(4.75)
    top_pos = Layout.CONTENT_TOP

    # L2 Edge Card
    c1 = create_card(slide, Layout.LEFT_MARGIN, top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.BLUE_ACCENT, 1.0)
    tf1 = c1.text_frame
    tf1.paragraphs[0].text = "L2: SITE-LEVEL AUTONOMOUS EDGE FSM"
    tf1.paragraphs[0].font.size = Pt(10)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.BLUE_ACCENT

    p1 = tf1.add_paragraph()
    p1.text = "Sub-Second Physical Protection"
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = Theme.TEXT_PRIMARY
    p1.space_before = Pt(4)

    p1_body = tf1.add_paragraph()
    p1_body.text = "• 260ms Hardware Break-Before-Make (BBM): Contactor switching executes with zero electrical arcing and zero short-circuit risks.\n\n• Complete Network Outage Immunity: If cloud WAN severs, the edge controller takes full autonomous command—maintaining 1,425kW with zero transformer overlimits.\n\n• Microsecond Fault Isolation: Ground fault and cable insulation failures tripped in <40ms, immediately dispatching automated service orders."
    p1_body.font.size = Pt(11.5)
    p1_body.font.color.rgb = Theme.TEXT_SECONDARY
    p1_body.space_before = Pt(14)

    p1_stat = tf1.add_paragraph()
    p1_stat.text = "REACTION TIME: < 40 ms  |  TRANSFORMER VIOLATIONS: 0"
    p1_stat.font.size = Pt(11)
    p1_stat.font.bold = True
    p1_stat.font.color.rgb = Theme.EMERALD_SUCCESS
    p1_stat.space_before = Pt(20)

    # L3 Cloud Card
    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(6.08), top_pos, card_w, card_h, Theme.CARD_BG)
    tf2 = c2.text_frame
    tf2.paragraphs[0].text = "L3: FLEET-WIDE CLOUD ORCHESTRATION"
    tf2.paragraphs[0].font.size = Pt(10)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.EMERALD_SUCCESS

    p2 = tf2.add_paragraph()
    p2.text = "15-Minute Rolling Economic MILP"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = Theme.TEXT_PRIMARY
    p2.space_before = Pt(4)

    p2_body = tf2.add_paragraph()
    p2_body.text = "• Nord Pool Dynamic Spot Arbitrage: 15-minute rolling Mixed-Integer Linear Program continuously solves multi-vehicle charging schedules.\n\n• Hard Departure Deadline Primacy: Commercial fleet timetables strictly override tariff saving routines—zero vehicles ever leave depleted.\n\n• Dynamic Power Wear-Leveling: Cyclic duty-cycle rotation across 25kW modules equalizes thermal stress, extending hardware life by 35%."
    p2_body.font.size = Pt(11.5)
    p2_body.font.color.rgb = Theme.TEXT_SECONDARY
    p2_body.space_before = Pt(14)

    p2_stat = tf2.add_paragraph()
    p2_stat.text = "TARIFF SAVINGS: -47.7%  |  ON-TIME DISPATCH: 100%"
    p2_stat.font.size = Pt(11)
    p2_stat.font.bold = True
    p2_stat.font.color.rgb = Theme.BLUE_ACCENT
    p2_stat.space_before = Pt(20)

    add_footer(slide, 3)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(c1), get_shape_id(c2)])

    add_speaker_notes(slide, """
[01:30 - 02:30] Slide 3: Two-Tier Architecture
"To eliminate human operators safely, we decoupled physical protection from economic optimization into two distinct layers.
On the left: Layer 2 is the Site-Level Edge FSM. Operating locally on the station controller, it enforces hardware constraints with sub-second determinism. Its 260ms Break-Before-Make contactor sequence prevents arcing during dynamic routing, and it survives complete cloud network outages without shedding load.
On the right: Layer 3 is our Cloud Orchestrator. Every 15 minutes, a rolling MILP solver analyzes day-ahead Nord Pool tariffs and depot timetables. It shifts charging away from expensive price spikes while strictly honoring commercial departure deadlines.
Now let us demonstrate how this architecture handles real-world failure events."
""")


def build_slide_4(prs):
    """Slide 4: Hero Solution 1 - Cabinet Thermal Overheating (Closed-Loop Self-Healing)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)
    add_header(slide, "Hero Operational Solution 1 · Hardware Self-Healing", 
               "Cabinet Overheating: Dynamic Busbar Reconfiguration Delivers 0 Deficit & Eliminates 9 Night Trips", 
               "S1 Bus Depot (02:25 Overheat Trip): Shared DC busbar reroutes power in 260ms without human intervention.",
               Theme.BLUE_ACCENT)

    # Dynamic Process Flow Badges
    steps = [
        ("STEP 1: DETECT", "59.3°C Thermal Warning (199m Lead)"),
        ("STEP 2: ISOLATE", "Cabinet #1 Safe Trip (02:25 AM)"),
        ("STEP 3: REROUTE", "260ms BBM Busbar Transfer (<10ms SW)"),
        ("STEP 4: ZERO DEFICIT", "100% Fleet Rollout (0 vs 4 Deficit)")
    ]
    badges = add_process_flow_badges(slide, steps, top_y=Inches(1.80), height=Inches(0.48))

    card_w = Inches(5.65)
    card_h = Inches(4.45)
    top_pos = Inches(2.42)

    # Left: Status Quo
    c1 = create_card(slide, Layout.LEFT_MARGIN, top_pos, card_w, card_h, Theme.CARD_BG_MUTED)
    tf1 = c1.text_frame
    tf1.paragraphs[0].text = "STATUS QUO: CONVENTIONAL ISOLATED TOPOLOGY"
    tf1.paragraphs[0].font.size = Pt(9.5)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.CORAL_RED

    p1 = tf1.add_paragraph()
    p1.text = "4 Buses Stranded Uncharged"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = Theme.TEXT_PRIMARY
    p1.space_before = Pt(4)

    p1_body = tf1.add_paragraph()
    p1_body.text = "• At 02:25, Cabinet #1 overheated and shut down.\n\n• In legacy architectures, all 4 dispensers hardwired to Cabinet #1 die instantly. The cables stay connected to dead equipment.\n\n• With no automated routing, 4 morning commuter buses receive zero charge, causing widespread morning transit cancellations.\n\n• Night shift staff forced to walk 9 rounds (8 min/trip) in sub-zero snow manually swapping cables."
    p1_body.font.size = Pt(11.0)
    p1_body.font.color.rgb = Theme.TEXT_SECONDARY
    p1_body.space_before = Pt(12)

    p1_metric = tf1.add_paragraph()
    p1_metric.text = "MORNING TALLY: 4 DEFICITS  |  9 MANUAL TRIPS"
    p1_metric.font.size = Pt(11.5)
    p1_metric.font.bold = True
    p1_metric.font.color.rgb = Theme.CORAL_RED
    p1_metric.space_before = Pt(16)

    # Right: Sentinel Solution
    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(6.08), top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.EMERALD_SUCCESS, 1.0)
    tf2 = c2.text_frame
    tf2.paragraphs[0].text = "SENTINEL: 24-POINT SHARED DC BUSBAR"
    tf2.paragraphs[0].font.size = Pt(9.5)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.EMERALD_SUCCESS

    p2 = tf2.add_paragraph()
    p2.text = "0 Deficits · 0 Human Actions"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = Theme.TEXT_PRIMARY
    p2.space_before = Pt(4)

    p2_body = tf2.add_paragraph()
    p2_body.text = "• All 24 charging points connect to a common DC busbar.\n\n• Upon Cabinet #1 thermal trip, the Edge FSM trips isolation contactors in 260ms (Break-Before-Make).\n\n• Power automatically re-routes from surviving Cabinets #2 and #3. Total station power gently adjusts from 1,080kW to 720kW.\n\n• All dispensers remain energized—eliminating the midnight cable-swapping chore at the source."
    p2_body.font.size = Pt(11.0)
    p2_body.font.color.rgb = Theme.TEXT_SECONDARY
    p2_body.space_before = Pt(12)

    p2_metric = tf2.add_paragraph()
    p2_metric.text = "MORNING TALLY: 0 DEFICITS  |  0 HUMAN INTERVENTIONS"
    p2_metric.font.size = Pt(11.5)
    p2_metric.font.bold = True
    p2_metric.font.color.rgb = Theme.EMERALD_SUCCESS
    p2_metric.space_before = Pt(16)

    add_footer(slide, 4)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(s) for s in badges] + [get_shape_id(c1), get_shape_id(c2)])

    add_speaker_notes(slide, """
[02:30 - 03:30] Slide 4: Solution 1 - Cabinet Overheating Trip
"Here is the first real crisis: S1 Bus Depot at 02:25 AM. Cabinet 1 overheated and tripped.
In the old system on the left, all four dispensers under Cabinet 1 died. The cables were still plugged into buses, but with nobody there to swap them, four morning transit buses sat on dead iron until morning. 4 missed departures, 9 manual replug trips.
Now look at Sentinel on the right: all 24 points connect to a shared DC busbar.
The moment Cabinet 1 trips, our Edge FSM actuates contactors in 260ms. Power dynamically routes around the failure through Cabinets 2 and 3. The guns stay alive—station power adjusts from 1,080 to 720 kW.
Morning result: 0 buses short, 0 manual trips. Labor is eliminated because the reason to unplug cables at night no longer exists."
""")


def build_slide_5(prs):
    """Slide 5: Hero Solution 2 - 10x Tariff Spike Arbitrage (Economic Optimization)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)
    add_header(slide, "Hero Operational Solution 2 · Economic Optimization", 
               "10x Dynamic Tariff Spike: Departure-Time Priority Slashes Electricity by 47.7%", 
               "Evening Peak (17:15–18:45): Price surges from €69.80 to €799.30/MWh — 100% full battery dispatch guaranteed.",
               Theme.EMERALD_SUCCESS)

    # Dynamic Process Flow Badges
    steps = [
        ("STEP 1: MONITOR", "Nord Pool €799.30/MWh Peak (10x Surge)"),
        ("STEP 2: EVALUATE", "15-Min Rolling MILP + SoC Elasticity"),
        ("STEP 3: DEFER", "Shift Bulk Charging to Valley Window"),
        ("STEP 4: SAVE 47.7%", "€179 vs €342 per Charge (100% Full Battery)")
    ]
    badges = add_process_flow_badges(slide, steps, top_y=Inches(1.80), height=Inches(0.48))

    card_w = Inches(5.65)
    card_h = Inches(4.45)
    top_pos = Inches(2.42)

    # Left: Status Quo
    c1 = create_card(slide, Layout.LEFT_MARGIN, top_pos, card_w, card_h, Theme.CARD_BG_MUTED)
    tf1 = c1.text_frame
    tf1.paragraphs[0].text = "STATUS QUO: UNCONSTRAINED FIFO CHARGING"
    tf1.paragraphs[0].font.size = Pt(9.5)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.CORAL_RED

    p1 = tf1.add_paragraph()
    p1.text = "€ 342 Cost · T02 Depleted"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = Theme.TEXT_PRIMARY
    p1.space_before = Pt(4)

    p1_body = tf1.add_paragraph()
    p1_body.text = "• Electricity tariffs skyrocket 10x from €69 to €799/MWh during the 90-minute evening peak.\n\n• Legacy systems treat all vehicles equally—blindly dividing 800kW across all 8 connected trucks.\n\n• Truck T02 (scheduled to depart at 17:45) is starved of power and leaves uncharged.\n\n• Meanwhile, trucks staying until tomorrow morning consume expensive €799/MWh power unnecessarily."
    p1_body.font.size = Pt(11.0)
    p1_body.font.color.rgb = Theme.TEXT_SECONDARY
    p1_body.space_before = Pt(12)

    p1_metric = tf1.add_paragraph()
    p1_metric.text = "EVENING ENERGY BILL: € 342  |  DEPARTURE DEFICITS: 1"
    p1_metric.font.size = Pt(11.5)
    p1_metric.font.bold = True
    p1_metric.font.color.rgb = Theme.CORAL_RED
    p1_metric.space_before = Pt(16)

    # Right: Sentinel Solution
    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(6.08), top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.EMERALD_SUCCESS, 1.0)
    tf2 = c2.text_frame
    tf2.paragraphs[0].text = "SENTINEL: TIME-FIRST ROLLING MILP"
    tf2.paragraphs[0].font.size = Pt(9.5)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.EMERALD_SUCCESS

    p2 = tf2.add_paragraph()
    p2.text = "€ 179 Cost · 100% On-Time Full"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = Theme.TEXT_PRIMARY
    p2.space_before = Pt(4)

    p2_body = tf2.add_paragraph()
    p2_body.text = "• Hierarchy of constraints: Safety #1, Grid bounds #2, Departure time #3, Price #4.\n\n• Urgent departures (T01–T04) receive immediate full charging regardless of tariff.\n\n• Overnight trucks (T05–T08) throttle to idle during the 90-minute €799 spike, resuming at 19:00 at €69/MWh.\n\n• Result: All 8 trucks leave 100% full, slashing energy spend by 47.7%."
    p2_body.font.size = Pt(11.0)
    p2_body.font.color.rgb = Theme.TEXT_SECONDARY
    p2_body.space_before = Pt(12)

    p2_metric = tf2.add_paragraph()
    p2_metric.text = "EVENING ENERGY BILL: € 179 (-47.7%)  |  DEFICITS: 0"
    p2_metric.font.size = Pt(11.5)
    p2_metric.font.bold = True
    p2_metric.font.color.rgb = Theme.EMERALD_SUCCESS
    p2_metric.space_before = Pt(16)

    add_footer(slide, 5)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(s) for s in badges] + [get_shape_id(c1), get_shape_id(c2)])

    add_speaker_notes(slide, """
[03:30 - 04:30] Slide 5: Solution 2 - 10x Tariff Spike Arbitrage
"Scene 3 involves no broken machine: only electricity price.
From 17:15 to 18:45, the tariff jumped from 69 to 799 euros per megawatt-hour—more than tenfold.
The old habit is 'whoever is plugged in keeps charging'. Eight trucks share 800 kW evenly. Truck T02 had to leave at 17:45, but its power was spread thin—so it left short. The evening energy bill hit 342 euros.
We changed one fundamental rule: look at departure time first, then price.
T01 through T04 must leave, so we fill them first. T05 through T08 leave tomorrow morning, so they wait out the expensive 90 minutes and recharge when prices fall back to 69 euros.
Result: all eight trucks leave 100% full, at 179 euros—saving 47.7%."
""")


def build_slide_6(prs):
    """Slide 6: Solution 3 - Highway 2-Hour Cellular Outage (Edge Autonomous Islanding)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)
    add_header(slide, "Operational Solution 3 · Edge Autonomous Islanding", 
               "2-Hour Network Outage: Edge Brain Retains Full 1,425 kW Capacity Offline", 
               "S3 Highway Hub (11:00–13:00): Retaining local decision authority prevents the catastrophic 50kW fallback.",
               Theme.BLUE_ACCENT)

    # Dynamic Process Flow Badges
    steps = [
        ("STEP 1: DETECT", "Cellular Loss at 11:00 (Heartbeat Fail)"),
        ("STEP 2: ISLAND", "Edge SQLite WAL Autonomous Brain"),
        ("STEP 3: MAINTAIN", "1,425 kW Matrix Dispensing (45m Turnaround)"),
        ("STEP 4: RECONCILE", "0 Out-of-Order Records Synced to Cloud")
    ]
    badges = add_process_flow_badges(slide, steps, top_y=Inches(1.80), height=Inches(0.48))

    card_w = Inches(5.65)
    card_h = Inches(4.45)
    top_pos = Inches(2.42)

    # Left: Status Quo
    c1 = create_card(slide, Layout.LEFT_MARGIN, top_pos, card_w, card_h, Theme.CARD_BG_MUTED)
    tf1 = c1.text_frame
    tf1.paragraphs[0].text = "STATUS QUO: CLOUD DEPENDENCY & PANIC THROTTLE"
    tf1.paragraphs[0].font.size = Pt(9.5)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.CORAL_RED

    p1 = tf1.add_paragraph()
    p1.text = "Session Blows Out to 269 Min"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = Theme.TEXT_PRIMARY
    p1.space_before = Pt(4)

    p1_body = tf1.add_paragraph()
    p1_body.text = "• WAN disconnects between 11:00 and 13:00.\n\n• Because power limits are decided in the cloud, the disconnected station panics—fearing transformer overload—and defaults to 50kW safe-mode.\n\n• Station throughput collapses from 1,425 kW down to 500 kW across 10 dispensers.\n\n• A 224 kWh truck charge blows out from 45 minutes to 269 minutes. Commercial drivers give up, yielding a 29.69% abandonment rate."
    p1_body.font.size = Pt(11.0)
    p1_body.font.color.rgb = Theme.TEXT_SECONDARY
    p1_body.space_before = Pt(12)

    p1_metric = tf1.add_paragraph()
    p1_metric.text = "STATION CAPACITY: 500 kW  |  ABANDONMENT: 29.7%"
    p1_metric.font.size = Pt(11.5)
    p1_metric.font.bold = True
    p1_metric.font.color.rgb = Theme.CORAL_RED
    p1_metric.space_before = Pt(16)

    # Right: Sentinel Solution
    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(6.08), top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.BLUE_ACCENT, 1.0)
    tf2 = c2.text_frame
    tf2.paragraphs[0].text = "SENTINEL: AUTONOMOUS LOCAL EDGE BRAIN"
    tf2.paragraphs[0].font.size = Pt(9.5)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.BLUE_ACCENT

    p2 = tf2.add_paragraph()
    p2.text = "Full 1,425 kW Kept · 45-Min Session"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = Theme.TEXT_PRIMARY
    p2.space_before = Pt(4)

    p2_body = tf2.add_paragraph()
    p2_body.text = "• An outage severs decision-making authority, not electrical energy.\n\n• Sentinel's local Edge Brain assumes immediate command, allocating dynamic power up to the 1,500 kW transformer limit.\n\n• All 10 dispensers continue high-speed DC fast charging at 1,425 kW with zero degradation in driver experience.\n\n• When the network reconnects at 13:00, billing records and CDRs synchronize automatically."
    p2_body.font.size = Pt(11.0)
    p2_body.font.color.rgb = Theme.TEXT_SECONDARY
    p2_body.space_before = Pt(12)

    p2_metric = tf2.add_paragraph()
    p2_metric.text = "STATION CAPACITY: 1,425 kW  |  DRIVER IMPACT: 0%"
    p2_metric.font.size = Pt(11.5)
    p2_metric.font.bold = True
    p2_metric.font.color.rgb = Theme.EMERALD_SUCCESS
    p2_metric.space_before = Pt(16)

    add_footer(slide, 6)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(s) for s in badges] + [get_shape_id(c1), get_shape_id(c2)])

    add_speaker_notes(slide, """
[04:30 - 05:30] Slide 6: Solution 3 - 2-Hour Network Outage
"In Scene 2, the S3 highway hub lost its network connection for two hours.
Notice: it lost the connection, not electrical power. What it lost was the cloud telling it how much power to give each vehicle.
In the old design, the station panics and drops to a 50kW safety setting. Total power drops from 1,425 to 500 kW. A truck charge stretches from 45 to 269 minutes. In the data, drivers wait at most 46 minutes—so people see the queue and leave.
Sentinel embeds an autonomous Edge Brain on-site. When the cloud disappears, the Edge Brain calculates optimal allocations locally, never exceeding the 1,500 kW transformer limit.
Same outage, same trucks: our 10 guns keep delivering 1,425 kW. Drivers never even notice."
""")


def build_slide_7(prs):
    """Slide 7: Solution 4 - 400kW Grid Curtailment (Emergency Triage)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)
    add_header(slide, "Operational Solution 4 · Grid Emergency Triage", 
               "400kW Grid Curtailment: Chronological Queue Guarantees 0 Deficits Across All 8 Trucks", 
               "Logistics Hub (16:00–19:00): Grid cuts capacity from 800kW to 400kW — 'A cut is not less energy, but for whom'.",
               Theme.BLUE_ACCENT)

    # Dynamic Process Flow Badges
    steps = [
        ("STEP 1: SIGNAL", "50% DSO Cap Order (800kW ➔ 400kW)"),
        ("STEP 2: SORT", "Earliest Commercial Departure Deadlines"),
        ("STEP 3: INJECT", "100% Available Power to Departing Vans"),
        ("STEP 4: ZERO DEFICIT", "All 8 Vans Depart Full; 0 Penalties")
    ]
    badges = add_process_flow_badges(slide, steps, top_y=Inches(1.80), height=Inches(0.48))

    card_w = Inches(5.65)
    card_h = Inches(4.45)
    top_pos = Inches(2.42)

    # Left: Status Quo
    c1 = create_card(slide, Layout.LEFT_MARGIN, top_pos, card_w, card_h, Theme.CARD_BG_MUTED)
    tf1 = c1.text_frame
    tf1.paragraphs[0].text = "STATUS QUO: FIRST-COME FIRST-SERVED (FIFO)"
    tf1.paragraphs[0].font.size = Pt(9.5)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.CORAL_RED

    p1 = tf1.add_paragraph()
    p1.text = "4 Fleet Trucks Depart Depleted"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = Theme.TEXT_PRIMARY
    p1.space_before = Pt(4)

    p1_body = tf1.add_paragraph()
    p1_body.text = "• The grid curtails station capacity from 800 kW down to 400 kW between 16:00 and 19:00.\n\n• Legacy FIFO prioritizes trucks that plugged in early in the afternoon—even though they don't depart until morning.\n\n• The 400 kW allocation is locked by overnight vehicles.\n\n• Four trucks departing at 17:30, 17:45, 18:00, and 18:15 receive almost zero energy and leave stranded."
    p1_body.font.size = Pt(11.0)
    p1_body.font.color.rgb = Theme.TEXT_SECONDARY
    p1_body.space_before = Pt(12)

    p1_metric = tf1.add_paragraph()
    p1_metric.text = "MISSED DEPARTURES: 4 TRUCKS STRANDED"
    p1_metric.font.size = Pt(11.5)
    p1_metric.font.bold = True
    p1_metric.font.color.rgb = Theme.CORAL_RED
    p1_metric.space_before = Pt(16)

    # Right: Sentinel Solution
    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(6.08), top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.EMERALD_SUCCESS, 1.0)
    tf2 = c2.text_frame
    tf2.paragraphs[0].text = "SENTINEL: EARLIEST-DEADLINE-FIRST (EDF)"
    tf2.paragraphs[0].font.size = Pt(9.5)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.EMERALD_SUCCESS

    p2 = tf2.add_paragraph()
    p2.text = "All 8 Trucks 100% Full On Time"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = Theme.TEXT_PRIMARY
    p2.space_before = Pt(4)

    p2_body = tf2.add_paragraph()
    p2_body.text = "• Sentinel reorders allocation: whoever leaves first charges first.\n\n• The entire 400 kW cap is funneled to the 4 departing trucks, clearing their required energy quotas.\n\n• Overnight trucks yield during the 3-hour curtailment window.\n\n• At 19:00 when the grid cap lifts, overnight trucks catch up at full 800 kW power. Zero missed departures."
    p2_body.font.size = Pt(11.0)
    p2_body.font.color.rgb = Theme.TEXT_SECONDARY
    p2_body.space_before = Pt(12)

    p2_metric = tf2.add_paragraph()
    p2_metric.text = "MISSED DEPARTURES: 0  |  CAP COMPLIANCE: 100%"
    p2_metric.font.size = Pt(11.5)
    p2_metric.font.bold = True
    p2_metric.font.color.rgb = Theme.EMERALD_SUCCESS
    p2_metric.space_before = Pt(16)

    add_footer(slide, 7)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(s) for s in badges] + [get_shape_id(c1), get_shape_id(c2)])

    add_speaker_notes(slide, """
[05:30 - 06:30] Slide 7: Solution 4 - 400kW Grid Curtailment
"In Scene 4, the utility issued a curtailment order: from 16:00 to 19:00, station power is cut from 800 to 400 kW.
Legacy habits look after early-arriving overnight trucks because they plugged in first. So overnight trucks hold the 400 kW, and the four vehicles departing at 17:30, 17:45, 18:00 and 18:15 leave stranded.
We use the same 400 kW and change only the sorting rule: Earliest Deadline First.
During the cut, departing vehicles take 100% of available power; overnight trucks wait. At 19:00 the cap lifts and overnight trucks catch up at 800 kW.
Result: all eight trucks depart fully charged.
The takeaway: a grid cut is not 'less energy'—it is 'less energy for whom'. Sort the same 400 kW properly, and nobody misses out."
""")


def build_slide_8(prs, poster_path: str):
    """Slide 8: Dedicated Video Demo Showcase — Master Video Player Frame & 4 Core Highlights (Requirement R3)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)
    add_header(
        slide,
        category="System Demonstration · 75-Second High-Fidelity Live Showcase",
        title="System in Action: 75-Second Autonomous Closed-Loop Demo",
        subtitle="Verifiable execution across the full 24-hour crisis timeline of Friday, November 13, 2026",
        pill_color=Theme.BLUE_ACCENT
    )

    card_top = Layout.CONTENT_TOP
    left_w = Inches(7.50)
    left_h = Inches(4.50)

    # Left: Video Player Box
    video_card = create_card(slide, Layout.LEFT_MARGIN, card_top, left_w, left_h, Theme.CARD_BG_CHIP, Theme.BLUE_ACCENT, 1.0)
    
    # Embed Poster Image if present (exact 16:9 widescreen ratio: 7.20" x 4.05")
    if os.path.exists(poster_path):
        img_w = Inches(7.20)
        img_h = Inches(4.05)
        img_left = Layout.LEFT_MARGIN + (left_w - img_w) / 2
        img_top = card_top + (left_h - img_h) / 2
        slide.shapes.add_picture(poster_path, img_left, img_top, img_w, img_h)

    # Live Badge on Player Top-Left
    live_badge = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Layout.LEFT_MARGIN + Inches(0.25), card_top + Inches(0.25), Inches(1.50), Inches(0.30))
    live_badge.fill.solid()
    live_badge.fill.fore_color.rgb = Theme.CARD_BG_CHIP
    live_badge.line.color.rgb = Theme.EMERALD_SUCCESS
    live_badge.line.width = Pt(0.75)
    tf_lb = live_badge.text_frame
    tf_lb.margin_left = tf_lb.margin_right = tf_lb.margin_top = tf_lb.margin_bottom = 0
    p_lb = tf_lb.paragraphs[0]
    p_lb.text = "● LIVE REPLAY"
    p_lb.font.name = "Segoe UI"
    p_lb.font.size = Pt(9.0)
    p_lb.font.bold = True
    p_lb.font.color.rgb = Theme.EMERALD_SUCCESS
    p_lb.alignment = PP_ALIGN.CENTER

    # Player Metadata Bar
    player_bar = slide.shapes.add_textbox(Layout.LEFT_MARGIN + Inches(0.25), card_top + left_h - Inches(0.40), left_w - Inches(0.50), Inches(0.30))
    tf_pb = player_bar.text_frame
    tf_pb.margin_left = tf_pb.margin_right = tf_pb.margin_top = tf_pb.margin_bottom = 0
    p_pb = tf_pb.paragraphs[0]
    p_pb.text = "00:42 / 01:15  ·  1080P HD  ·  STREAMLIT INTERACTIVE APP"
    p_pb.font.name = "Segoe UI"
    p_pb.font.size = Pt(8.5)
    p_pb.font.bold = True
    p_pb.font.color.rgb = Theme.TEXT_MUTED

    # Right: 4 Verifiable Highlight Cards
    right_left = Layout.LEFT_MARGIN + Inches(7.75)
    right_w = Inches(3.98)
    callout_h = Inches(1.02)
    spacing = Inches(0.14)

    f1 = create_card(slide, right_left, card_top, right_w, callout_h, Theme.CARD_BG_CHIP, Theme.BLUE_ACCENT, 0.75)
    tf1 = f1.text_frame
    tf1.paragraphs[0].text = "01 · DYNAMIC BUSBAR RECONFIGURATION (260ms BBM)"
    tf1.paragraphs[0].font.size = Pt(8.5)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.BLUE_ACCENT
    p1 = tf1.add_paragraph()
    p1.text = "Break-Before-Make contactors reroute 25kW DPR modules with zero arcing; 0 missed departures vs 4 stranded."
    p1.font.size = Pt(8.0)
    p1.font.color.rgb = Theme.TEXT_SECONDARY
    p1.space_before = Pt(3)

    f2 = create_card(slide, right_left, card_top + callout_h + spacing, right_w, callout_h, Theme.CARD_BG_CHIP, Theme.EMERALD_SUCCESS, 0.75)
    tf2 = f2.text_frame
    tf2.paragraphs[0].text = "02 · 10x SPOT PRICE SPIKE ARBITRAGE (-47.7% COST)"
    tf2.paragraphs[0].font.size = Pt(8.5)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.EMERALD_SUCCESS
    p2 = tf2.add_paragraph()
    p2.text = "15-min rolling MILP navigates €799.30/MWh surge; cuts bill from €342 to €179 with 100% full battery."
    p2.font.size = Pt(8.0)
    p2.font.color.rgb = Theme.TEXT_SECONDARY
    p2.space_before = Pt(3)

    f3 = create_card(slide, right_left, card_top + 2 * (callout_h + spacing), right_w, callout_h, Theme.CARD_BG_CHIP, Theme.CARD_BORDER_FOCUS, 0.75)
    tf3 = f3.text_frame
    tf3.paragraphs[0].text = "03 · HIGHWAY 72h SQLITE WAL ISLANDING BRAIN"
    tf3.paragraphs[0].font.size = Pt(8.5)
    tf3.paragraphs[0].font.bold = True
    tf3.paragraphs[0].font.color.rgb = Theme.BLUE_ACCENT
    p3 = tf3.add_paragraph()
    p3.text = "Edge controller maintains full 1,425kW fast charging during 2-hour cellular blackout; 45m vs 269m."
    p3.font.size = Pt(8.0)
    p3.font.color.rgb = Theme.TEXT_SECONDARY
    p3.space_before = Pt(3)

    f4 = create_card(slide, right_left, card_top + 3 * (callout_h + spacing), right_w, callout_h, Theme.CARD_BG_CHIP, Theme.CARD_BORDER, 0.75)
    tf4 = f4.text_frame
    tf4.paragraphs[0].text = "04 · HARDWARE GROUND-FAULT & DIGITAL TWIN AUTO-HEAL"
    tf4.paragraphs[0].font.size = Pt(8.5)
    tf4.paragraphs[0].font.bold = True
    tf4.paragraphs[0].font.color.rgb = Theme.TEXT_PRIMARY
    p4 = tf4.add_paragraph()
    p4.text = "40ms analog safety loop trips damaged cables; digital twin cross-audits commissioning tables in 3s."
    p4.font.size = Pt(8.0)
    p4.font.color.rgb = Theme.TEXT_SECONDARY
    p4.space_before = Pt(3)

    add_footer(slide, 8)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(f1), get_shape_id(f2), get_shape_id(f3), get_shape_id(f4)])

    add_speaker_notes(slide, """
[07:30 - 08:30] Slide 8: Live Demo Showcase
"Let us watch our 75-second live simulation recording.
Notice the exact contactor timing: 260 milliseconds for Break-Before-Make switching. In that quarter of a second, high-voltage current safely reroutes across the shared DC busbar without creating an arc.
Observe how the power levels smoothly: as Cabinet 1 drops, Cabinets 2 and 3 instantly rebalance the remaining vehicles. No driver experiences a disconnected session.
And simultaneously, the 15-minute rolling MILP solver navigates the Nord Pool tariff spike, deferring overnight trucks while keeping departing trucks charging at full power.
Every frame in this video is reproducible from our open-source simulation engine."
""")


def build_slide_9(prs):
    """Slide 9: Operational Solutions 5 & 6 (Hardware Safety & Digital Twin Auto-Heal)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)
    add_header(slide, "Operational Solutions 5 & 6 · Physical & Configuration Defenses", 
               "40ms Hardware Cable Trip & Digital Twin Self-Correction Eliminate Hidden Failure Points", 
               "Autonomous protection spanning physical layer insulation tripping and software commissioning reconciliation.",
               Theme.BLUE_ACCENT)

    # Dynamic Process Flow Badges
    steps = [
        ("STEP 1: TRACE", "40ms Ground Sensor Trip (D4-2 Cable)"),
        ("STEP 2: ISOLATE", "Dispensers 1-2 Trip; 3-4 Remain Hot"),
        ("STEP 3: RESYNC", "Digital Twin Audits 3 Commissioning Tables (3s)"),
        ("STEP 4: AUTO-HEAL", "600kW Limit Reconciled to 900kW (0 Deficit)")
    ]
    badges = add_process_flow_badges(slide, steps, top_y=Inches(1.80), height=Inches(0.48))

    card_w = Inches(5.65)
    card_h = Inches(4.45)
    top_pos = Inches(2.42)

    # Left: Cable Trip (Scene 5)
    c1 = create_card(slide, Layout.LEFT_MARGIN, top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.BLUE_ACCENT, 1.0)
    tf1 = c1.text_frame
    tf1.paragraphs[0].text = "SCENE 5: 40ms HARDWARE CABLE ISOLATION"
    tf1.paragraphs[0].font.size = Pt(9.5)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.BLUE_ACCENT

    p1 = tf1.add_paragraph()
    p1.text = "30s Manual Delay ➔ 40ms Trip"
    p1.font.size = Pt(22)
    p1.font.bold = True
    p1.font.color.rgb = Theme.TEXT_PRIMARY
    p1.space_before = Pt(4)

    p1_body = tf1.add_paragraph()
    p1_body.text = "• At 21:30 in an urban hub, charging cable D4-2 suffers insulation failure.\n\n• Legacy: Cloud polling + human dispatcher ticket = 30-second delay with severe arcing and electrical hazard.\n\n• Sentinel: Local analog safety circuit detects ground leakage in 40ms and trips shunt contactors.\n\n• Automatically opens an automated spare-part work order; the other 7 dispensers continue charging with zero interruption."
    p1_body.font.size = Pt(11.0)
    p1_body.font.color.rgb = Theme.TEXT_SECONDARY
    p1_body.space_before = Pt(12)

    p1_metric = tf1.add_paragraph()
    p1_metric.text = "RESPONSE TIME: 40 ms  |  MANUAL TICKETING: ZERO"
    p1_metric.font.size = Pt(11.5)
    p1_metric.font.bold = True
    p1_metric.font.color.rgb = Theme.EMERALD_SUCCESS
    p1_metric.space_before = Pt(16)

    # Right: Digital Twin Commissioning (Scene 6)
    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(6.08), top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.EMERALD_SUCCESS, 1.0)
    tf2 = c2.text_frame
    tf2.paragraphs[0].text = "SCENE 6: DIGITAL TWIN PARAMETER RECONCILIATION"
    tf2.paragraphs[0].font.size = Pt(9.5)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.EMERALD_SUCCESS

    p2 = tf2.add_paragraph()
    p2.text = "5 Deficits ➔ 0 Deficits Self-Healed"
    p2.font.size = Pt(22)
    p2.font.bold = True
    p2.font.color.rgb = Theme.TEXT_PRIMARY
    p2.space_before = Pt(4)

    p2_body = tf2.add_paragraph()
    p2_body.text = "• New bus depot commissioning error: two engineering tables specify 900kW, but a third table sets a 600kW cap; one gun is throttled and a SIM is unactivated.\n\n• Legacy: 5 of 12 buses depart uncharged due to bureaucratic mismatch.\n\n• Sentinel: Digital Twin cross-audits commissioning tables in 3 seconds, reconciles the limit back to 900kW, and activates the SIM card.\n\n• Same buses, same hardware: 0 missed departures."
    p2_body.font.size = Pt(11.0)
    p2_body.font.color.rgb = Theme.TEXT_SECONDARY
    p2_body.space_before = Pt(12)

    p2_metric = tf2.add_paragraph()
    p2_metric.text = "SELF-RECONCILIATION: 3 SEC  |  DEPOT DEFICITS: 0"
    p2_metric.font.size = Pt(11.5)
    p2_metric.font.bold = True
    p2_metric.font.color.rgb = Theme.EMERALD_SUCCESS
    p2_metric.space_before = Pt(16)

    add_footer(slide, 9)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(s) for s in badges] + [get_shape_id(c1), get_shape_id(c2)])

    add_speaker_notes(slide, """
[06:30 - 07:30] Slide 9: Solutions 5 & 6 - Cable Trip & Digital Twin
"Scenes 5 and 6 prove that self-operating networks must protect both the physical layer and the configuration layer.
In Scene 5, a charging cable is damaged at 21:30. In the old flow, waiting for cloud alarms and a human ticket took 30 seconds. Sentinel's local hardware safety loop trips in 40 milliseconds, opens a service ticket automatically, and keeps the other seven dispensers working.
In Scene 6, the machines are fine, but configuration tables contradict: two tables say 900 kW, the third says 600 kW. Under legacy operations, five buses left short. Our Digital Twin compares the tables, fixes the limit to 900 kW, and eliminates all five deficits.
Self-operating means saving yourself when physical faults strike, but also self-correcting human configuration errors."
""")


def build_slide_10(prs):
    """Slide 10: Multi-Site Scalability & Grid Protection."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)
    add_header(slide, "Technical Credibility", 
               "Multi-Site Scalability: Zero Transformer Overlimits Across 100 Sites & 72 Capped Depots", 
               "539 Automated Tests (433 Unit + 106 E2E, 100% Passing) validating physical constraints and standards.")

    card_w = Inches(3.65)
    card_h = Inches(4.75)
    top_pos = Layout.CONTENT_TOP

    # Card 1: 0 Transformer Overlimits
    c1 = create_card(slide, Layout.LEFT_MARGIN, top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.EMERALD_SUCCESS, 1.0)
    tf1 = c1.text_frame
    tf1.paragraphs[0].text = "GRID & TRANSFORMER INTEGRITY"
    tf1.paragraphs[0].font.size = Pt(9.5)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.EMERALD_SUCCESS
    
    p1 = tf1.add_paragraph()
    p1.text = "0 Violations"
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = Theme.TEXT_PRIMARY
    p1.space_before = Pt(4)

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Across 72 Grid-Capped Sites"
    p1_sub.font.size = Pt(13)
    p1_sub.font.bold = True
    p1_sub.font.color.rgb = Theme.EMERALD_SUCCESS
    p1_sub.space_before = Pt(2)

    p1_desc = tf1.add_paragraph()
    p1_desc.text = "Sentinel enforces strict mathematical transformer capacity limits on every feeder and substation.\n\nEven during extreme simultaneous vehicle arrivals and cabinet failures, the Edge FSM never permits grid overdraw."
    p1_desc.font.size = Pt(11)
    p1_desc.font.color.rgb = Theme.TEXT_MUTED
    p1_desc.space_before = Pt(12)

    p1_box = tf1.add_paragraph()
    p1_box.text = "GRID SANCTION EXPOSURE\n€ 0.00 Overlimit Penalties"
    p1_box.font.size = Pt(12)
    p1_box.font.bold = True
    p1_box.font.color.rgb = Theme.TEXT_PRIMARY
    p1_box.space_before = Pt(16)

    # Card 2: 25kW Wear Leveling
    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(4.04), top_pos, card_w, card_h, Theme.CARD_BG)
    tf2 = c2.text_frame
    tf2.paragraphs[0].text = "HARDWARE LIFE EXTENSION"
    tf2.paragraphs[0].font.size = Pt(9.5)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.BLUE_ACCENT
    
    p2 = tf2.add_paragraph()
    p2.text = "+35% Life"
    p2.font.size = Pt(36)
    p2.font.bold = True
    p2.font.color.rgb = Theme.TEXT_PRIMARY
    p2.space_before = Pt(4)

    p2_sub = tf2.add_paragraph()
    p2_sub.text = "25kW Dynamic Wear-Leveling"
    p2_sub.font.size = Pt(13)
    p2_sub.font.bold = True
    p2_sub.font.color.rgb = Theme.BLUE_ACCENT
    p2_sub.space_before = Pt(2)

    p2_desc = tf2.add_paragraph()
    p2_desc.text = "Rather than keeping primary power modules continuously stressed at 100% while spares sit idle, Sentinel rotates active modules every 60 minutes.\n\nThermal wear is distributed evenly, delaying module degradation."
    p2_desc.font.size = Pt(11)
    p2_desc.font.color.rgb = Theme.TEXT_MUTED
    p2_desc.space_before = Pt(12)

    p2_box = tf2.add_paragraph()
    p2_box.text = "MODULE REPLACEMENT SAVINGS\n€ 142,000 / Fleet Depot"
    p2_box.font.size = Pt(12)
    p2_box.font.bold = True
    p2_box.font.color.rgb = Theme.TEXT_PRIMARY
    p2_box.space_before = Pt(16)

    # Card 3: Standards & Testing
    c3 = create_card(slide, Layout.LEFT_MARGIN + Inches(8.08), top_pos, card_w, card_h, Theme.CARD_BG)
    tf3 = c3.text_frame
    tf3.paragraphs[0].text = "STANDARDS & VERIFICATION"
    tf3.paragraphs[0].font.size = Pt(9.5)
    tf3.paragraphs[0].font.bold = True
    tf3.paragraphs[0].font.color.rgb = Theme.TEXT_PRIMARY
    
    p3 = tf3.add_paragraph()
    p3.text = "539 Tests"
    p3.font.size = Pt(36)
    p3.font.bold = True
    p3.font.color.rgb = Theme.TEXT_PRIMARY
    p3.space_before = Pt(4)

    p3_sub = tf3.add_paragraph()
    p3_sub.text = "100% Automated Pass Rate"
    p3_sub.font.size = Pt(13)
    p3_sub.font.bold = True
    p3_sub.font.color.rgb = Theme.TEXT_PRIMARY
    p3_sub.space_before = Pt(2)

    p3_desc = tf3.add_paragraph()
    p3_desc.text = "• OCPP 2.0.1 Smart Charging TxProfile certified.\n• ISO 15118-20 Plug & Charge TLS 1.3 cryptographic security.\n• 433 unit tests + 106 E2E scenario day tests executed on every commit."
    p3_desc.font.size = Pt(11)
    p3_desc.font.color.rgb = Theme.TEXT_MUTED
    p3_desc.space_before = Pt(12)

    p3_box = tf3.add_paragraph()
    p3_box.text = "PROTOCOL COMPLIANCE\nOCPP 2.0.1 · ISO 15118"
    p3_box.font.size = Pt(12)
    p3_box.font.bold = True
    p3_box.font.color.rgb = Theme.TEXT_PRIMARY
    p3_box.space_before = Pt(16)

    add_footer(slide, 10)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(c1), get_shape_id(c2), get_shape_id(c3)])

    add_speaker_notes(slide, """
[08:30 - 09:15] Slide 10: Multi-Site Scalability & Technical Credibility
"We tested Sentinel across the full 100-site challenge dataset.
Across 72 grid-constrained sites, Sentinel maintained zero transformer violations under all simulated failure conditions.
Furthermore, by dynamically rotating the 25kW power modules, we distribute thermal stress and increase hardware lifespan by 35%.
Our entire codebase is backed by 539 automated tests, with full compliance for OCPP 2.0.1 Smart Charging profiles and ISO 15118-20 Plug & Charge."
""")


def build_slide_11(prs):
    """Slide 11: Commercial Viability & One-Page SLA."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)
    add_header(slide, "Commercial Viability", 
               "Outcome-Based Commercial SLA: €1.82M Annual Savings & 8.4-Month Payback", 
               "Transforming reactive charger sales into bankable Charging-as-a-Service (CaaS) with guaranteed availability.")

    card_w = Inches(5.65)
    card_h = Inches(4.75)
    top_pos = Layout.CONTENT_TOP

    # Left: Financial Payback
    c1 = create_card(slide, Layout.LEFT_MARGIN, top_pos, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.EMERALD_SUCCESS, 1.0)
    tf1 = c1.text_frame
    tf1.paragraphs[0].text = "FINANCIAL PAYBACK & OPEX REDUCTION"
    tf1.paragraphs[0].font.size = Pt(9.5)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.EMERALD_SUCCESS

    p1 = tf1.add_paragraph()
    p1.text = "8.4-Month Full Payback"
    p1.font.size = Pt(24)
    p1.font.bold = True
    p1.font.color.rgb = Theme.TEXT_PRIMARY
    p1.space_before = Pt(4)

    p1_body = tf1.add_paragraph()
    p1_body.text = "• Annual Labor Savings: Eliminating 20.76 FTE continuous maintenance recovers €1,821,534 / year.\n\n• Busbar Hardware Retrofit: Upgrading existing cabinets to shared DC busbars with contactors costs €324,000 across a 100-depot network.\n\n• Payback Horizon: Capital expenditure is amortized in exactly 8.4 months.\n\n• Long-Term Value: Delivers over €1.49M in net cash savings every subsequent year."
    p1_body.font.size = Pt(11.5)
    p1_body.font.color.rgb = Theme.TEXT_SECONDARY
    p1_body.space_before = Pt(14)

    p1_metric = tf1.add_paragraph()
    p1_metric.text = "ANNUAL NET SAVINGS: € 1,497,534 / YEAR"
    p1_metric.font.size = Pt(12)
    p1_metric.font.bold = True
    p1_metric.font.color.rgb = Theme.EMERALD_SUCCESS
    p1_metric.space_before = Pt(20)

    # Right: The One-Page SLA
    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(6.08), top_pos, card_w, card_h, Theme.CARD_BG, Theme.BLUE_ACCENT, 1.0)
    tf2 = c2.text_frame
    tf2.paragraphs[0].text = "THE ONE-PAGE SLA CONTRACT"
    tf2.paragraphs[0].font.size = Pt(9.5)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.BLUE_ACCENT

    p2 = tf2.add_paragraph()
    p2.text = "From Hardware Vending to CaaS"
    p2.font.size = Pt(24)
    p2.font.bold = True
    p2.font.color.rgb = Theme.TEXT_PRIMARY
    p2.space_before = Pt(4)

    p2_body = tf2.add_paragraph()
    p2_body.text = "• Minimum Required Delivery Throughput (MRDT): Guarantees 99.8% energy availability on commercial departure windows.\n\n• Transparent Dispute Clearing: Local cryptographic event ledgers eliminate finger-pointing between fleet operator, site host, and equipment vendor.\n\n• Automatic Settlement: Contractual late-departure penalties (€150–250/event) eliminated entirely through autonomous certainty."
    p2_body.font.size = Pt(11.5)
    p2_body.font.color.rgb = Theme.TEXT_SECONDARY
    p2_body.space_before = Pt(14)

    p2_metric = tf2.add_paragraph()
    p2_metric.text = "ENERGY AVAILABILITY SLA: 99.8% GUARANTEED"
    p2_metric.font.size = Pt(12)
    p2_metric.font.bold = True
    p2_metric.font.color.rgb = Theme.BLUE_ACCENT
    p2_metric.space_before = Pt(20)

    add_footer(slide, 11)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(c1), get_shape_id(c2)])

    add_speaker_notes(slide, """
[09:15 - 09:45] Slide 11: Commercial Viability & One-Page SLA
"From a commercial perspective, Sentinel turns reactive hardware sales into a high-margin Charging-as-a-Service model.
On the left: retrofitting a shared DC busbar across a 100-site network costs approximately 324,000 euros. Against 1.82 million euros in eliminated labor, the retrofit pays for itself in just 8.4 months.
On the right: our One-Page SLA contract guarantees 99.8% energy availability. By moving from equipment warranties to guaranteed energy throughput, Kempower can capture fleet contracts that competitors cannot touch."
""")


def build_slide_12(prs):
    """Slide 12: Executive Vision & Conclusion."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    apply_background(slide)

    # Category Pill
    pill = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Layout.LEFT_MARGIN, Inches(0.80), Inches(3.2), Inches(0.28))
    pill.fill.solid()
    pill.fill.fore_color.rgb = Theme.CARD_BG_CHIP
    pill.line.color.rgb = Theme.BLUE_ACCENT
    pill.line.width = Pt(0.75)
    tf_p = pill.text_frame
    p = tf_p.paragraphs[0]
    p.text = "EXECUTIVE CONCLUSION"
    p.font.name = "Segoe UI"
    p.font.size = Pt(9.0)
    p.font.bold = True
    p.font.color.rgb = Theme.BLUE_ACCENT

    # Title
    tb_title = slide.shapes.add_textbox(Layout.LEFT_MARGIN, Inches(1.15), Layout.CONTENT_WIDTH, Inches(0.55))
    tf_t = tb_title.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.text = "The Self-Operating Network: Failures That No Longer Need A Human"
    p_t.font.name = "Segoe UI"
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = Theme.TEXT_PRIMARY

    # Subtitle
    tb_sub = slide.shapes.add_textbox(Layout.LEFT_MARGIN, Inches(1.72), Layout.CONTENT_WIDTH, Inches(0.35))
    tf_s = tb_sub.text_frame
    p_s = tf_s.paragraphs[0]
    p_s.text = "Project Sentinel · Built for Kempower · LahtiES Energy Tech Hackathon 2026"
    p_s.font.name = "Segoe UI"
    p_s.font.size = Pt(11.5)
    p_s.font.color.rgb = Theme.TEXT_MUTED

    card_top = Inches(2.25)
    card_w = Inches(5.65)
    card_h = Inches(4.55)

    # Left: The 4 Truths
    c1 = create_card(slide, Layout.LEFT_MARGIN, card_top, card_w, card_h, Theme.CARD_BG_ACCENT, Theme.BLUE_ACCENT, 1.0)
    tf1 = c1.text_frame
    tf1.paragraphs[0].text = "THE FOUR AUTONOMOUS PILLARS"
    tf1.paragraphs[0].font.size = Pt(10)
    tf1.paragraphs[0].font.bold = True
    tf1.paragraphs[0].font.color.rgb = Theme.BLUE_ACCENT

    p1 = tf1.add_paragraph()
    p1.text = "1. Departure Priority First\nWhen vehicles arrive, schedule by timetable deadline—never blind FIFO.\n\n2. 260ms Hardware Busbar Routing\nWhen equipment fails, reroute current through surviving cabinets in 260ms.\n\n3. Local Edge Autonomy\nWhen network severs, maintain full power under local transformer control.\n\n4. Digital Twin Reconciliation\nWhen configuration tables conflict, resolve discrepancies automatically."
    p1.font.size = Pt(11.5)
    p1.font.color.rgb = Theme.TEXT_SECONDARY
    p1.space_before = Pt(12)

    # Right: Closing Statement
    c2 = create_card(slide, Layout.LEFT_MARGIN + Inches(6.08), card_top, card_w, card_h, Theme.CARD_BG)
    tf2 = c2.text_frame
    tf2.paragraphs[0].text = "THE SENTINEL COMMITMENT"
    tf2.paragraphs[0].font.size = Pt(10)
    tf2.paragraphs[0].font.bold = True
    tf2.paragraphs[0].font.color.rgb = Theme.EMERALD_SUCCESS

    p2_quote = tf2.add_paragraph()
    p2_quote.text = '"What we built is not six patches, but one unified self-operating system; the goal is not to make equipment never fail, but to make failures never require human intervention."'
    p2_quote.font.size = Pt(17.5)
    p2_quote.font.bold = True
    p2_quote.font.color.rgb = Theme.TEXT_PRIMARY
    p2_quote.space_before = Pt(20)

    p2_ty = tf2.add_paragraph()
    p2_ty.text = "Project Sentinel is ready for commercial field deployment.\nThank you!"
    p2_ty.font.size = Pt(13)
    p2_ty.font.bold = True
    p2_ty.font.color.rgb = Theme.BLUE_ACCENT
    p2_ty.space_before = Pt(36)

    add_footer(slide, 12)
    add_slide_transition(slide, "fade")
    add_sequential_build_animation(slide, [get_shape_id(c1), get_shape_id(c2)])

    add_speaker_notes(slide, """
[09:45 - 10:00] Slide 12: Executive Vision & Conclusion
"Looking back at these operational challenges, we did not build six isolated patches. We engineered a single autonomous operating core:
When a vehicle arrives, ask when it must depart.
When equipment trips, reroute power in 260 milliseconds.
When energy prices spike 10x, defer non-critical load.
When communications drop, keep charging locally.
When settings conflict, let the digital twin self-correct.
What we built is not six patches, but one unified self-operating system; the goal is not to make equipment never fail, but to make failures never require human intervention.
That is what we mean by the self-operating charging network.
Thank you, and we look forward to your questions."
""")


def main():
    prs = Presentation()
    prs.slide_width = Layout.SLIDE_WIDTH
    prs.slide_height = Layout.SLIDE_HEIGHT

    poster_path = os.path.join(os.path.dirname(__file__), "demo", "presentation_demo_poster.png")

    print("Compiling 12-slide All-English Animated Pitch Deck...")
    build_slide_1(prs)
    build_slide_2(prs)
    build_slide_3(prs)
    build_slide_4(prs)
    build_slide_5(prs)
    build_slide_6(prs)
    build_slide_7(prs)
    build_slide_8(prs, poster_path)
    build_slide_9(prs)
    build_slide_10(prs)
    build_slide_11(prs)
    build_slide_12(prs)

    output_path = os.path.join(os.path.dirname(__file__), "Project_Sentinel_Pitch_Deck.pptx")
    prs.save(output_path)
    print(f"Successfully generated: {output_path} ({len(prs.slides)} slides)")


if __name__ == "__main__":
    main()
