#!/usr/bin/env python3
"""
Kempower Self-Operating Charging Network - Master Demo Video Generator
Script: render_video.py

Generates a 75.0-second (2,250 frames @ 30fps) Full HD 1080p presentation video
for Project Sentinel (LahtiES Energy Tech Hackathon 2026).
Designed with Apple/Tesla Keynote minimalism:
- Zero subtitles, zero subtitle boxes, zero bilingual text clutter
- Zero SHA256 hashes, zero millisecond counters, zero tiny progress bars
- Single dominant visual focus per scene, giant 54pt-72pt hero numbers, 40%+ whitespace
- High-contrast luminous Nordic palette (#0B111E, #00E5FF, #0091FF, #FF6B00, #10B981)
- Center on 2 core hero processes:
    * Process 1: Cabinet overheat topology self-healing via DC busbar tie (4 -> 0 missed)
    * Process 2: 10x price spike dynamic scheduling (-47.7% electricity cost, €179 vs €342)
- Recursive directory creation for output_path and poster_path
- Strictly 0 audio streams (silent presentation video)
"""

import argparse
import math
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from PIL import Image, ImageDraw, ImageFont

# -----------------------------------------------------------------------------
# Configuration & Constants
# -----------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent
DEMO_DIR = REPO_ROOT / "demo"
DEFAULT_OUTPUT = DEMO_DIR / "presentation_demo.mp4"
DEFAULT_POSTER = DEMO_DIR / "presentation_demo_poster.png"

WIDTH = 1920
HEIGHT = 1080
FPS = 30
TOTAL_SECONDS = 75.0
TOTAL_FRAMES = int(TOTAL_SECONDS * FPS)  # 2,250 frames

# High-Contrast Luminous Nordic Keynote Palette
C_BG = (11, 17, 30)             # #0B111E (Deep Matte Slate)
C_HEADER_BG = (15, 23, 42)      # #0F172A (Nordic Navy Slate)
C_HEADER_BORDER = (30, 41, 59)  # #1E293B
C_CARD_BG = (21, 31, 50)        # #151F32 (Executive Card Slate)
C_CARD_BORDER = (37, 53, 77)    # #25354D (Subtle Hairline Border)
C_CYAN = (0, 229, 255)          # #00E5FF (Luminous Electric Cyan)
C_BLUE = (0, 145, 255)          # #0091FF (Kempower Blue)
C_ORANGE = (255, 107, 0)        # #FF6B00 (Vibrant Kempower Orange)
C_AMBER = (245, 158, 11)        # #F59E0B (Warning Amber)
C_GREEN = (16, 185, 129)        # #10B981 (Emerald Green)
C_RED = (248, 113, 113)         # #F87171 (Muted Danger Red)
C_VIOLET = (139, 92, 246)       # #8B5CF6 (Cloud MILP Violet)
C_TEXT_WHITE = (255, 255, 255)  # Pure Crisp White
C_TEXT_LIGHT = (203, 213, 225)  # #CBD5E1 (Slate Light)
C_TEXT_MUTED = (148, 163, 184)  # #94A3B8 (Slate Muted)
C_TEXT_DIM = (100, 116, 139)    # #64748B (Slate Dim)


# -----------------------------------------------------------------------------
# Font Manager (Windows System Fonts)
# -----------------------------------------------------------------------------
class FontManager:
    """Manages high-DPI TrueType fonts with automatic fallbacks."""
    def __init__(self):
        font_dir = Path(r"C:\Windows\Fonts")
        self.segoe = str(font_dir / "segoeui.ttf") if (font_dir / "segoeui.ttf").exists() else "arial.ttf"
        self.segoe_b = str(font_dir / "segoeuib.ttf") if (font_dir / "segoeuib.ttf").exists() else self.segoe
        self.consola = str(font_dir / "consola.ttf") if (font_dir / "consola.ttf").exists() else self.segoe
        self.consola_b = str(font_dir / "consolab.ttf") if (font_dir / "consolab.ttf").exists() else self.consola
        self._cache: Dict[Tuple[str, int], ImageFont.FreeTypeFont] = {}

    def get(self, font_type: str, size: int) -> ImageFont.FreeTypeFont:
        key = (font_type, size)
        if key not in self._cache:
            path_map = {
                "title": self.segoe_b,
                "text": self.segoe,
                "mono": self.consola,
                "mono_b": self.consola_b,
            }
            font_path = path_map.get(font_type, self.segoe)
            try:
                self._cache[key] = ImageFont.truetype(font_path, size)
            except Exception:
                self._cache[key] = ImageFont.load_default()
        return self._cache[key]


# -----------------------------------------------------------------------------
# Drawing Helpers
# -----------------------------------------------------------------------------
def draw_card(draw: ImageDraw.ImageDraw, box: Tuple[int, int, int, int],
              fill=C_CARD_BG, outline=C_CARD_BORDER, radius: int = 14, width: int = 1):
    """Draws a clean, modern Keynote container rectangle with rounded corners."""
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=fill, outline=outline, width=width)


def draw_bolt_icon(draw: ImageDraw.ImageDraw, center: Tuple[int, int], size: int = 28, color=C_CYAN):
    """Draws a stylized, crisp Kempower lightning bolt."""
    cx, cy = center
    s = size / 24.0
    pts = [
        (cx + 2 * s, cy - 12 * s),
        (cx - 8 * s, cy + 1 * s),
        (cx - 1 * s, cy + 1 * s),
        (cx - 3 * s, cy + 12 * s),
        (cx + 8 * s, cy - 1 * s),
        (cx + 1 * s, cy - 1 * s),
    ]
    draw.polygon(pts, fill=color)


def draw_header(draw: ImageDraw.ImageDraw, fonts: FontManager, current_time: float, scene_title: str):
    """Draws the ultra-clean, minimalist Keynote top navigation bar."""
    draw.rectangle([0, 0, WIDTH, 70], fill=C_HEADER_BG)
    draw.line([(0, 70), (WIDTH, 70)], fill=C_HEADER_BORDER, width=1)

    # Left: Brand lockup
    draw_bolt_icon(draw, (36, 35), size=26, color=C_CYAN)
    draw.text((58, 22), "PROJECT SENTINEL", fill=C_CYAN, font=fonts.get("title", 20))
    draw.text((254, 23), "|", fill=C_HEADER_BORDER, font=fonts.get("text", 18))
    draw.text((272, 24), "Autonomous Operating Core", fill=C_TEXT_MUTED, font=fonts.get("text", 16))

    # Center: Chapter breadcrumb
    bbox = draw.textbbox((0, 0), scene_title, font=fonts.get("title", 18))
    tw = bbox[2] - bbox[0]
    draw.text(((WIDTH - tw) // 2, 23), scene_title, fill=C_TEXT_LIGHT, font=fonts.get("title", 18))

    # Right: Live autonomous indicator
    pulse = (math.sin(current_time * 4.0) + 1.0) / 2.0
    dot_color = (int(C_CYAN[0] * pulse), int(C_CYAN[1]), int(C_CYAN[2]))
    draw.ellipse([1600, 29, 1612, 41], fill=dot_color)
    draw.text((1624, 25), "AUTONOMOUS CORE ACTIVE", fill=C_CYAN, font=fonts.get("mono_b", 14))


def draw_minimal_footer(draw: ImageDraw.ImageDraw, fonts: FontManager):
    """Draws a subtle, non-intrusive metadata strip with zero clutter."""
    y = 1044
    draw.line([(80, y - 8), (WIDTH - 80, y - 8)], fill=C_HEADER_BORDER, width=1)
    draw.text((80, y), "LahtiES Energy Tech Hackathon 2026 · Kempower Challenge", fill=C_TEXT_DIM, font=fonts.get("text", 14))
    right_text = "Hardware-Software Autonomous Closed Loop · 1920x1080@30fps"
    bbox = draw.textbbox((0, 0), right_text, font=fonts.get("text", 14))
    rw = bbox[2] - bbox[0]
    draw.text((WIDTH - 80 - rw, y), right_text, fill=C_TEXT_DIM, font=fonts.get("text", 14))


# -----------------------------------------------------------------------------
# Scene 1: The Radical Vision (00:00 - 00:10, 10s)
# -----------------------------------------------------------------------------
def render_scene_1(draw: ImageDraw.ImageDraw, fonts: FontManager, t: float, rel_t: float):
    """
    Scene 1: The Radical Vision & Title Lockup
    - 0-4s: Dramatic hook question with generous whitespace
    - 4-10s: Master title reveal and clean side-by-side contrast
    """
    if rel_t < 4.0:
        # Dramatic hook question
        alpha_factor = min(1.0, rel_t / 1.5)
        q_color = (int(255 * alpha_factor), int(255 * alpha_factor), int(255 * alpha_factor))

        draw_bolt_icon(draw, (WIDTH // 2, 360), size=90, color=C_CYAN)

        q1 = "If humans were no longer allowed to operate a charging network..."
        bbox1 = draw.textbbox((0, 0), q1, font=fonts.get("title", 38))
        draw.text(((WIDTH - (bbox1[2] - bbox1[0])) // 2, 480), q1, fill=q_color, font=fonts.get("title", 38))

        q2 = "...how would you redesign it from the ground up?"
        bbox2 = draw.textbbox((0, 0), q2, font=fonts.get("title", 36))
        draw.text(((WIDTH - (bbox2[2] - bbox2[0])) // 2, 550), q2, fill=C_CYAN, font=fonts.get("title", 36))

        tag = "Kempower Challenge 2026 · LahtiES Energy Tech Hackathon · LUT University"
        bboxt = draw.textbbox((0, 0), tag, font=fonts.get("text", 20))
        draw.text(((WIDTH - (bboxt[2] - bboxt[0])) // 2, 650), tag, fill=C_TEXT_MUTED, font=fonts.get("text", 20))

    else:
        # Master Title & Architectural Thesis
        draw_bolt_icon(draw, (WIDTH // 2, 210), size=76, color=C_CYAN)

        title = "PROJECT SENTINEL"
        bbt = draw.textbbox((0, 0), title, font=fonts.get("title", 72))
        draw.text(((WIDTH - (bbt[2] - bbt[0])) // 2, 270), title, fill=C_CYAN, font=fonts.get("title", 72))

        sub = "The Autonomous Operating Core for Kempower Hardware"
        bbs = draw.textbbox((0, 0), sub, font=fonts.get("title", 28))
        draw.text(((WIDTH - (bbs[2] - bbs[0])) // 2, 365), sub, fill=C_TEXT_WHITE, font=fonts.get("title", 28))

        thesis = "Closed-loop industrial intelligence: Zero continuous labor, deterministic energy certainty"
        bbth = draw.textbbox((0, 0), thesis, font=fonts.get("text", 18))
        draw.text(((WIDTH - (bbth[2] - bbth[0])) // 2, 415), thesis, fill=C_TEXT_MUTED, font=fonts.get("text", 18))

        # Two Large Comparison Cards
        # Left: Traditional
        draw_card(draw, (140, 480, 920, 840), fill=(26, 20, 28), outline=(80, 35, 45), radius=16, width=2)
        draw.text((180, 515), "TRADITIONAL CHARGING NETWORK", fill=C_RED, font=fonts.get("title", 22))
        draw.text((180, 560), "20.76 FTE · €1.82M/yr", fill=C_TEXT_WHITE, font=fonts.get("mono_b", 42))
        draw.text((180, 620), "Human-Dependent · Reactive · High Burn", fill=C_RED, font=fonts.get("title", 18))

        draw.text((180, 675), "•  5,596 midnight vehicle replugs in frozen yards", fill=C_TEXT_LIGHT, font=fonts.get("text", 18))
        draw.text((180, 715), "•  13 fleet vehicles missed departure on Scenario Day", fill=C_TEXT_LIGHT, font=fonts.get("text", 18))
        draw.text((180, 755), "•  29.7% driver abandonment under cellular outages", fill=C_TEXT_LIGHT, font=fonts.get("text", 18))

        # Right: Project Sentinel
        draw_card(draw, (1000, 480, 1780, 840), fill=(18, 32, 46), outline=C_CYAN, radius=16, width=2)
        draw.text((1040, 515), "PROJECT SENTINEL AUTONOMOUS CORE", fill=C_CYAN, font=fonts.get("title", 22))
        draw.text((1040, 560), "0 Human Moves · €0 CAPEX", fill=C_TEXT_WHITE, font=fonts.get("mono_b", 42))
        draw.text((1040, 620), "Autonomous · Self-Healing · Guaranteed SLA", fill=C_CYAN, font=fonts.get("title", 18))

        draw.text((1040, 675), "•  260ms Break-Before-Make zero-arc topology self-healing", fill=C_TEXT_LIGHT, font=fonts.get("text", 18))
        draw.text((1040, 715), "•  100ms edge FSM with 72-hour offline islanding", fill=C_TEXT_LIGHT, font=fonts.get("text", 18))
        draw.text((1040, 755), "•  Dynamic spot price arbitrage (-47.7% electricity cost)", fill=C_TEXT_LIGHT, font=fonts.get("text", 18))


# -----------------------------------------------------------------------------
# Scene 2: The 20.76 FTE Human Crisis (00:10 - 00:22, 12s)
# -----------------------------------------------------------------------------
def render_scene_2(draw: ImageDraw.ImageDraw, fonts: FontManager, t: float, rel_t: float):
    """
    Scene 2: The 20.76 FTE Human Crisis
    - Left: Nordic Telemetry Map with 100 Sites
    - Right: Giant twin hero counters counting up and the midnight replugging crisis
    """
    # Left: Nordic Network Telemetry Map
    draw_card(draw, (80, 105, 920, 970), fill=C_CARD_BG, outline=C_CARD_BORDER, radius=16, width=1)
    draw.text((120, 135), "NORDIC CHARGING TELEMETRY AUDIT", fill=C_TEXT_WHITE, font=fonts.get("title", 22))
    draw.text((120, 168), "100 Commercial Sites across Finland, Sweden, Norway & Denmark", fill=C_TEXT_MUTED, font=fonts.get("text", 16))

    # Scandinavian landmasses
    nordic_polys = [
        [(620, 360), (730, 320), (780, 420), (750, 540), (680, 630), (610, 620), (590, 500)],  # Finland
        [(500, 320), (580, 350), (570, 540), (530, 660), (460, 680), (450, 550), (470, 410)],  # Sweden
        [(430, 260), (500, 310), (440, 410), (420, 550), (360, 580), (380, 470), (400, 350)],  # Norway
        [(430, 710), (480, 710), (470, 750), (420, 750)],                                        # Denmark
    ]
    for poly in nordic_polys:
        draw.polygon(poly, fill=(24, 34, 48), outline=(42, 58, 78))

    # Scatter 95 stations
    import random
    rng = random.Random(42)
    for _ in range(95):
        sx = rng.randint(460, 750)
        sy = rng.randint(340, 690)
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=C_BLUE)

    # 5 Key Focal Stations with radar pulses
    focal_sites = [(670, 600), (710, 560), (630, 530), (680, 630), (650, 640)]
    pulse_phase = (t * 2.5) % 2.0
    pulse_r = int(pulse_phase * 22)
    for fx, fy in focal_sites:
        draw.ellipse([fx - pulse_r, fy - pulse_r, fx + pulse_r, fy + pulse_r], outline=C_CYAN, width=1)
        draw.ellipse([fx - 5, fy - 5, fx + 5, fy + 5], fill=C_CYAN)

    # Map Inset Badge
    draw_card(draw, (120, 830, 880, 930), fill=(16, 25, 38), outline=C_CARD_BORDER, radius=10, width=1)
    draw.text((140, 850), "240,635 Ground Truth Telemetry Rows Audited", fill=C_CYAN, font=fonts.get("title", 18))
    draw.text((140, 885), "0 Official Grid Overlimit intervals / 134,400 verified bit-for-bit", fill=C_TEXT_MUTED, font=fonts.get("text", 15))

    # Right: Giant Twin Hero Counters & The Replugging Crisis
    prog = min(1.0, rel_t / 3.5)
    cur_fte = 20.76 * prog
    cur_cost = 1821534 * prog

    # Twin Hero KPI Cards
    draw_card(draw, (960, 105, 1370, 280), fill=C_CARD_BG, outline=C_CARD_BORDER, radius=14, width=1)
    draw.text((990, 130), f"{cur_fte:.2f} FTE", fill=C_TEXT_WHITE, font=fonts.get("title", 54))
    draw.text((990, 215), "Continuous Manual Labor Burden", fill=C_TEXT_MUTED, font=fonts.get("text", 18))

    draw_card(draw, (1410, 105, 1840, 280), fill=C_CARD_BG, outline=(80, 45, 35), radius=14, width=1)
    draw.text((1440, 130), f"€{cur_cost:,.0f}", fill=C_ORANGE, font=fonts.get("title", 50))
    draw.text((1440, 215), "Annual Operational OPEX Burn", fill=C_TEXT_MUTED, font=fonts.get("text", 18))

    # Dominant Crisis Highlight Card
    draw_card(draw, (960, 310, 1840, 680), fill=(26, 28, 40), outline=(80, 50, 35), radius=16, width=2)
    draw.text((1000, 340), "THE INVISIBLE FLEET YARD CRISIS", fill=C_TEXT_MUTED, font=fonts.get("title", 20))
    draw.text((1000, 385), "5,596 Midnight Replugging Events", fill=C_ORANGE, font=fonts.get("title", 44))
    draw.text((1000, 460), "47.9% of ALL network labor (44,768 minutes) spent dragging cables", fill=C_TEXT_WHITE, font=fonts.get("title", 22))
    draw.text((1000, 510), "Consumes 9.95 full-time staff every night in freezing depot yards", fill=C_TEXT_LIGHT, font=fonts.get("text", 18))
    draw.text((1000, 555), "€872,976 wasted every year on preventable manual cable shifting", fill=C_ORANGE, font=fonts.get("title", 20))

    # Clean percentage bar
    draw.rounded_rectangle([1000, 615, 1800, 640], radius=6, fill=(35, 42, 54))
    draw.rounded_rectangle([1000, 615, 1000 + int(800 * 0.4793 * prog), 640], radius=6, fill=C_ORANGE)

    # Bottom Crisis Breakdown
    draw_card(draw, (960, 710, 1840, 970), fill=(36, 18, 24), outline=(120, 40, 50), radius=16, width=2)
    draw.text((1000, 745), "SCENARIO DAY HUMAN SYSTEM BREAKDOWN", fill=C_RED, font=fonts.get("title", 20))
    draw.text((1000, 790), "13 Fleet Vehicles Missed Morning Departure", fill=C_TEXT_WHITE, font=fonts.get("title", 36))
    draw.text((1000, 860), "1,804.45 kWh energy deficit · Human dispatch breaks down under compounding stress", fill=C_TEXT_LIGHT, font=fonts.get("text", 18))
    draw.text((1000, 905), "Proves adding more human staff cannot solve physical synchronization limits", fill=C_RED, font=fonts.get("text", 16))


# -----------------------------------------------------------------------------
# Scene 3: 3-Layer Closed-Loop OS (00:22 - 00:36, 14s)
# -----------------------------------------------------------------------------
def render_scene_3(draw: ImageDraw.ImageDraw, fonts: FontManager, t: float, rel_t: float):
    """
    Scene 3: 3-Layer Closed-Loop OS
    - 3 large, clean architectural pillars (Cloud MILP -> Edge FSM -> DPR Matrix)
    - Bottom highlight: 260ms BBM zero-arc contactor + ISO 15118 PnC in 1.1s
    """
    # Header
    draw.text((100, 105), "THREE-LAYER CLOSED-LOOP ARCHITECTURE", fill=C_TEXT_WHITE, font=fonts.get("title", 26))
    draw.text((100, 142), "Separation of concerns: Global Economics vs Millisecond Hardware Safety", fill=C_TEXT_MUTED, font=fonts.get("text", 17))

    # 3 Architectural Pillars
    pillars = [
        (
            100, 640, "LAYER 3 · CLOUD MILP", C_VIOLET,
            "15-Min", "Rolling SciPy HiGHS Optimizer",
            [
                "•  Nord Pool day-ahead spot price arbitrage",
                "•  Absorbs €799.30/MWh extreme price peaks",
                "•  Predictive fleet dwell time buffer scheduling",
                "•  Eliminates €7.50/kW monthly peak demand tariff",
            ]
        ),
        (
            680, 1220, "LAYER 2 · STATION EDGE FSM", C_CYAN,
            "100ms", "Autonomous Edge DLM Controller",
            [
                "•  72-hour autonomous offline islanding mode",
                "•  Zero cloud WAN dependency for local safety",
                "•  Deterministic clamping: 1,425.0 kW DC limit",
                "•  Anti-phantom replug fraud filtering (Δt < 180s)",
            ]
        ),
        (
            1260, 1800, "LAYER 1 · PHYSICAL MATRIX", C_BLUE,
            "25kW", "Modular Power Rectifier Matrix",
            [
                "•  260ms Break-Before-Make zero-arc relays",
                "•  Contactor mechanical separation at strictly 0.0A",
                "•  Dynamic thermal wear-leveling across modules",
                "•  Shared DC busbar cross-cabinet power routing",
            ]
        ),
    ]

    for x0, x1, p_title, p_color, hero_num, hero_sub, points in pillars:
        draw_card(draw, (x0, 185, x1, 790), fill=C_CARD_BG, outline=p_color, radius=16, width=2)
        draw.text((x0 + 35, 220), p_title, fill=p_color, font=fonts.get("title", 18))
        draw.text((x0 + 35, 260), hero_num, fill=p_color, font=fonts.get("title", 64))
        draw.text((x0 + 35, 345), hero_sub, fill=C_TEXT_WHITE, font=fonts.get("title", 20))

        y_pt = 415
        for pt in points:
            draw.text((x0 + 35, y_pt), pt, fill=C_TEXT_LIGHT, font=fonts.get("text", 17))
            y_pt += 45

    # Bottom Highlight Ribbon
    draw_card(draw, (100, 825, 1800, 960), fill=(16, 28, 42), outline=C_CYAN, radius=14, width=2)
    ribbon_text = "260ms Break-Before-Make Zero-Arc Relay  ·  ISO 15118 Plug & Charge in 1.1s  ·  OCPP 2.0.1 Native"
    bbr = draw.textbbox((0, 0), ribbon_text, font=fonts.get("title", 22))
    draw.text(((WIDTH - (bbr[2] - bbr[0])) // 2, 855), ribbon_text, fill=C_CYAN, font=fonts.get("title", 22))

    sub_ribbon = "Hardware-software co-design delivering sub-second safety guarantees and zero human intervention"
    bbsr = draw.textbbox((0, 0), sub_ribbon, font=fonts.get("text", 16))
    draw.text(((WIDTH - (bbsr[2] - bbsr[0])) // 2, 905), sub_ribbon, fill=C_TEXT_LIGHT, font=fonts.get("text", 16))


# -----------------------------------------------------------------------------
# Scene 4: HERO PROCESS 1 — Cabinet Overheat Topology Self-Healing (00:36 - 00:54, 18s)
# -----------------------------------------------------------------------------
def render_scene_4(draw: ImageDraw.ImageDraw, fonts: FontManager, t: float, rel_t: float):
    """
    Scene 4: HERO PROCESS 1 — Cabinet Overheat Topology Self-Healing via DC Busbar Tie
    - Stage 1 (0-5s): 02:25 Cabinet C1-3 fan fails (59.3°C, 199-min PdM lead time)
    - Stage 2 (5-11s): 260ms BBM contactor switches (zero-arc isolation)
    - Stage 3 (11-18s): Shared DC busbar tie dynamically reallocates power from C2/C3 -> 24 buses charged!
    - Giant comparison: 4 Missed -> 0 MISSED DEPARTURES (72pt Emerald Green)
    """
    # 3-Stage Process Stepper at Top
    stage = 1 if rel_t < 5.0 else (2 if rel_t < 11.0 else 3)

    steps = [
        ("STAGE 1 · 02:25 Overheat Alert", "199-min PdM lead time at 59.3°C", 1),
        ("STAGE 2 · 260ms BBM Contactor", "Zero-arc mechanical separation at 0.0A", 2),
        ("STAGE 3 · DC Busbar Re-Route", "Dynamic cross-cabinet power sharing", 3),
    ]

    sx0 = 100
    for s_name, s_sub, s_idx in steps:
        is_active = (s_idx == stage)
        card_fill = (24, 38, 54) if is_active else C_CARD_BG
        card_border = C_CYAN if is_active else C_CARD_BORDER
        text_color = C_CYAN if is_active else C_TEXT_MUTED
        draw_card(draw, (sx0, 95, sx0 + 530, 175), fill=card_fill, outline=card_border, radius=12, width=2 if is_active else 1)
        draw.text((sx0 + 25, 110), s_name, fill=text_color, font=fonts.get("title", 18))
        draw.text((sx0 + 25, 140), s_sub, fill=C_TEXT_LIGHT if is_active else C_TEXT_DIM, font=fonts.get("text", 15))
        sx0 += 565

    # Center Visual Topology Diagram
    draw_card(draw, (100, 195, 1800, 690), fill=C_CARD_BG, outline=C_CARD_BORDER, radius=16, width=1)
    draw.text((130, 215), "STATION S1 · 1,080 kW DC POWER TOPOLOGY (3x360 kW CABINETS)", fill=C_TEXT_WHITE, font=fonts.get("title", 20))

    # 3 Cabinets
    cab_w = 480
    cab_h = 180
    cabs = [
        (140, "CABINET 1 (360 kW DC)", 1),
        (660, "CABINET 2 (360 kW DC)", 2),
        (1180, "CABINET 3 (360 kW DC)", 3),
    ]

    for cx, ctitle, cnum in cabs:
        if cnum == 1:
            if stage == 1:
                c_fill = (45, 25, 20)
                c_border = C_ORANGE
                status_txt = "OVERHEAT DETECTED: 59.3°C (Fan Degrading)"
                status_color = C_ORANGE
            else:
                c_fill = (30, 20, 24)
                c_border = (90, 45, 50)
                status_txt = "SAFELY ISOLATED (260ms BBM Trip · 0.0 Amps)"
                status_color = C_RED
        else:
            c_fill = (18, 36, 48) if stage == 3 else (21, 31, 50)
            c_border = C_CYAN if stage == 3 else C_CARD_BORDER
            status_txt = "ACTIVE POWER SUPPLY: 360 kW NOMINAL" if stage < 3 else "SHARED DC BUSBAR POWER BOOST: ACTIVE"
            status_color = C_CYAN

        draw_card(draw, (cx, 260, cx + cab_w, 260 + cab_h), fill=c_fill, outline=c_border, radius=12, width=2)
        draw.text((cx + 25, 280), ctitle, fill=C_TEXT_WHITE, font=fonts.get("title", 18))
        draw.text((cx + 25, 320), status_txt, fill=status_color, font=fonts.get("title", 15))

        # Module status line
        m_label = "Modules M01–M12: DEGRADED" if (cnum == 1 and stage == 1) else (
            "Modules M01–M12: ZERO-ARC OFF" if cnum == 1 else (
                f"Modules M{13 if cnum==2 else 25}–M{24 if cnum==2 else 36}: 100% HEALTHY"
            )
        )
        draw.text((cx + 25, 360), m_label, fill=C_TEXT_LIGHT, font=fonts.get("mono", 14))

    # Shared DC Busbar Tie Conduit (Horizontal Glowing Bar)
    by0 = 475
    by1 = 535
    busbar_active = (stage == 3)
    bar_outline = C_CYAN if busbar_active else C_CARD_BORDER
    bar_fill = (15, 45, 60) if busbar_active else (25, 33, 44)
    draw_card(draw, (140, by0, 1660, by1), fill=bar_fill, outline=bar_outline, radius=10, width=2)

    tie_label = "SHARED DC BUSBAR TIE (DYNAMIC POWER RE-ROUTING ENABLED)" if busbar_active else "SHARED DC BUSBAR TIE (STANDBY CONTACTOR CIRCUIT)"
    draw.text((180, by0 + 16), tie_label, fill=C_CYAN if busbar_active else C_TEXT_MUTED, font=fonts.get("title", 17))

    # Animated glowing current pulses on busbar if active
    if busbar_active:
        pulse_pos = int((t * 240) % 1400)
        draw.ellipse([200 + pulse_pos - 8, by0 + 18, 200 + pulse_pos + 8, by0 + 34], fill=C_CYAN)
        draw.text((1200, by0 + 16), "⚡ REALLOCATING LOAD TO C2 & C3", fill=C_GREEN, font=fonts.get("mono_b", 15))

    # 24 Bus Fleet Charging Dispensers Row
    draw.text((140, 565), "DEPOT S1 FLEET: 24 ARTICULATED ELECTRIC BUSES", fill=C_TEXT_WHITE, font=fonts.get("title", 17))
    bus_y = 605
    for b_idx in range(24):
        bx = 140 + b_idx * 63
        if stage < 3 and b_idx in [3, 8, 17, 19]:  # B04, B09, B18, B20
            b_col = C_RED
            b_num = f"B{b_idx+1:02d}"
        else:
            b_col = C_GREEN
            b_num = f"B{b_idx+1:02d}"
        draw.rectangle([bx, bus_y, bx + 52, bus_y + 40], fill=(22, 30, 42), outline=b_col, width=2)
        draw.text((bx + 8, bus_y + 10), b_num, fill=b_col, font=fonts.get("mono_b", 13))

    # Bottom Giant Hero Comparison
    draw_card(draw, (100, 715, 1800, 970), fill=C_CARD_BG, outline=C_GREEN if stage == 3 else C_CARD_BORDER, radius=16, width=2)

    # Left: Baseline
    draw.text((140, 745), "BASELINE HUMAN SYSTEM", fill=C_RED, font=fonts.get("title", 20))
    draw.text((140, 790), "4 Missed Departures", fill=C_RED, font=fonts.get("title", 40))
    draw.text((140, 855), "B04, B09, B18, B20 stalled · 398.5 kWh deficit", fill=C_TEXT_LIGHT, font=fonts.get("text", 18))
    draw.text((140, 895), "12 midnight manual cable replugs failed to rescue buses", fill=C_TEXT_MUTED, font=fonts.get("text", 16))

    # Middle Divider
    draw.line([(880, 740), (880, 945)], fill=C_CARD_BORDER, width=2)

    # Right: Project Sentinel Autonomous Core
    draw.text((930, 745), "PROJECT SENTINEL AUTONOMOUS HEALING", fill=C_GREEN, font=fonts.get("title", 20))
    draw.text((930, 785), "0 MISSED DEPARTURES", fill=C_GREEN, font=fonts.get("title", 68))
    draw.text((930, 875), "All 24 City Buses Depart 100% On-Time · €0 Unbudgeted CAPEX", fill=C_TEXT_WHITE, font=fonts.get("title", 22))
    draw.text((930, 915), "Dynamic busbar cross-tie eliminates all depot yard replugging", fill=C_CYAN, font=fonts.get("text", 17))


# -----------------------------------------------------------------------------
# Scene 5: HERO PROCESS 2 — 10x Price Spike Dynamic Scheduling (00:54 - 01:08, 14s)
# -----------------------------------------------------------------------------
def render_scene_5(draw: ImageDraw.ImageDraw, fonts: FontManager, t: float, rel_t: float):
    """
    Scene 5: HERO PROCESS 2 — 10x Price Spike Dynamic Scheduling
    - Stage 1 (0-4s): Nord Pool spot price surges from €69 to €799.30/MWh
    - Stage 2 (4-9s): Dynamic algorithm preemption (T01-T04 charge, T05-T08 sleep)
    - Stage 3 (9-14s): Giant hero outcome (-47.7% electricity cost, €179 vs €342)
    """
    stage = 1 if rel_t < 4.0 else (2 if rel_t < 9.0 else 3)

    steps = [
        ("STAGE 1 · Spot Price Spike", "€69 -> €799.30/MWh Nord Pool surge", 1),
        ("STAGE 2 · MILP Preemption", "Evening rush prioritized, overnight buffer sleeps", 2),
        ("STAGE 3 · Commercial Triumph", "-47.7% electricity cost (€179 vs €342)", 3),
    ]

    sx0 = 100
    for s_name, s_sub, s_idx in steps:
        is_active = (s_idx == stage)
        card_fill = (24, 38, 54) if is_active else C_CARD_BG
        card_border = C_CYAN if is_active else C_CARD_BORDER
        text_color = C_CYAN if is_active else C_TEXT_MUTED
        draw_card(draw, (sx0, 95, sx0 + 530, 175), fill=card_fill, outline=card_border, radius=12, width=2 if is_active else 1)
        draw.text((sx0 + 25, 110), s_name, fill=text_color, font=fonts.get("title", 18))
        draw.text((sx0 + 25, 140), s_sub, fill=C_TEXT_LIGHT if is_active else C_TEXT_DIM, font=fonts.get("text", 15))
        sx0 += 565

    # Center: Interactive Split (Spot Price Curve vs Dynamic Preemption Engine)
    # Left: Spot Price Curve
    draw_card(draw, (100, 195, 920, 690), fill=C_CARD_BG, outline=C_CARD_BORDER, radius=16, width=1)
    draw.text((130, 220), "NORD POOL HOURLY SPOT PRICE PROFILE", fill=C_TEXT_WHITE, font=fonts.get("title", 20))
    draw.text((130, 252), "Logistics Station S2 · 24-Hour Horizon with 10x Evening Spike", fill=C_TEXT_MUTED, font=fonts.get("text", 15))

    # Graph plotting area (X: 140 to 880, Y: 290 to 570)
    gx0, gy0, gx1, gy1 = 140, 300, 880, 560
    draw.rectangle([gx0, gy0, gx1, gy1], fill=(16, 23, 34), outline=C_HEADER_BORDER)

    # Grid lines
    draw.line([(gx0, gy1 - 50), (gx1, gy1 - 50)], fill=(28, 38, 50), width=1)
    draw.line([(gx0, gy1 - 130), (gx1, gy1 - 130)], fill=(28, 38, 50), width=1)
    draw.line([(gx0, gy0 + 30), (gx1, gy0 + 30)], fill=(28, 38, 50), width=1)

    draw.text((gx0 + 10, gy1 - 45), "€69 / MWh (Normal)", fill=C_TEXT_MUTED, font=fonts.get("mono", 13))
    draw.text((gx0 + 10, gy0 + 15), "€799.30 / MWh (10x Peak Surge)", fill=C_ORANGE, font=fonts.get("mono_b", 14))

    # Spot Price Curve Points
    pts = [
        (gx0, gy1 - 40),
        (gx0 + 150, gy1 - 42),
        (gx0 + 300, gy1 - 55),
        (gx0 + 420, gy1 - 65),
        (gx0 + 500, gy0 + 25),  # 17:15 Spike
        (gx0 + 570, gy0 + 25),  # 18:45 Spike Peak
        (gx0 + 640, gy1 - 70),
        (gx0 + 740, gy1 - 35),
    ]
    # Draw curve
    for i in range(len(pts) - 1):
        line_color = C_ORANGE if i in [3, 4, 5] else C_CYAN
        draw.line([pts[i], pts[i + 1]], fill=line_color, width=3)

    # Shaded Spike Zone
    draw.rectangle([gx0 + 460, gy0 + 10, gx0 + 610, gy1], fill=(50, 25, 20, 80), outline=C_ORANGE, width=1)
    draw.text((gx0 + 475, gy1 + 15), "17:15–18:45 PEAK", fill=C_ORANGE, font=fonts.get("mono_b", 14))

    draw.text((130, 615), "• Pre-charges 283.50 kWh buffer in morning valley hours", fill=C_CYAN, font=fonts.get("text", 16))
    draw.text((130, 650), "• Automatically sheds 300 kW peak load during €799 spike", fill=C_TEXT_LIGHT, font=fonts.get("text", 16))

    # Right: Fleet Preemption Scheduling Engine
    draw_card(draw, (960, 195, 1800, 690), fill=C_CARD_BG, outline=C_CARD_BORDER, radius=16, width=1)
    draw.text((990, 220), "AUTONOMOUS FLEET PREEMPTION ENGINE", fill=C_TEXT_WHITE, font=fonts.get("title", 20))
    draw.text((990, 252), "Dynamic MILP priority scheduling based on departure deadlines", fill=C_TEXT_MUTED, font=fonts.get("text", 15))

    # Group 1: Rush Departures
    draw_card(draw, (990, 295, 1770, 470), fill=(18, 38, 48), outline=C_GREEN, radius=12, width=2)
    draw.text((1020, 315), "RUSH LOGISTICS: TRUCKS T01 – T04", fill=C_GREEN, font=fonts.get("title", 18))
    draw.text((1020, 350), "100% On-Time Rush Departure at 18:30", fill=C_TEXT_WHITE, font=fonts.get("title", 24))
    draw.text((1020, 395), "Preempted 283.50 kWh before the peak to guarantee full delivery dispatch", fill=C_TEXT_LIGHT, font=fonts.get("text", 16))
    draw.text((1020, 430), "STATUS: FULL CHARGE PREEMPTED · ZERO DELAY", fill=C_GREEN, font=fonts.get("mono_b", 15))

    # Group 2: Overnight Buffer Fleet
    draw_card(draw, (990, 495, 1770, 665), fill=(28, 28, 42), outline=C_CYAN, radius=12, width=2)
    draw.text((1020, 515), "OVERNIGHT FLEET: TRUCKS T05 – T08", fill=C_CYAN, font=fonts.get("title", 18))
    draw.text((1020, 550), "Morning Departure at 07:00 (1,857 kWh Pool)", fill=C_TEXT_WHITE, font=fonts.get("title", 24))
    draw.text((1020, 595), "Charging paused during €799 peak; automatically resumes at €42 night valley", fill=C_TEXT_LIGHT, font=fonts.get("text", 16))
    draw.text((1020, 630), "STATUS: INTELLIGENT SLACK SLEEP · PEAK SHAVED", fill=C_CYAN, font=fonts.get("mono_b", 15))

    # Bottom Giant Outcome Card
    draw_card(draw, (100, 715, 1800, 970), fill=C_CARD_BG, outline=C_CYAN, radius=16, width=2)

    # Left: Baseline Cost
    draw.text((140, 745), "BASELINE UNMANAGED (FCFS)", fill=C_RED, font=fonts.get("title", 20))
    draw.text((140, 790), "€342.18", fill=C_RED, font=fonts.get("title", 48))
    draw.text((140, 875), "Charges naively into €799.30 peak", fill=C_TEXT_LIGHT, font=fonts.get("text", 18))
    draw.text((140, 915), "4 commercial trucks delayed and uncharged", fill=C_TEXT_MUTED, font=fonts.get("text", 16))

    # Middle Divider
    draw.line([(880, 740), (880, 945)], fill=C_CARD_BORDER, width=2)

    # Right: Sentinel Hero Outcome
    draw.text((930, 745), "PROJECT SENTINEL DYNAMIC MILP: €179.05", fill=C_GREEN, font=fonts.get("title", 20))
    draw.text((930, 785), "-47.7% ELECTRICITY COST", fill=C_CYAN, font=fonts.get("title", 66))
    draw.text((930, 875), "100% On-Time Departures · 0 Delivery Delays · 0 Fleet Penalties", fill=C_TEXT_WHITE, font=fonts.get("title", 22))
    draw.text((930, 915), "Mathematical certainty protecting commercial fleet margins", fill=C_GREEN, font=fonts.get("text", 17))


# -----------------------------------------------------------------------------
# Scene 6: Deterministic Proof & Closing (01:08 - 01:15, 7s)
# -----------------------------------------------------------------------------
def render_scene_6(draw: ImageDraw.ImageDraw, fonts: FontManager, t: float, rel_t: float):
    """
    Scene 6: Deterministic Proof & Master Closing Lockup
    - 3 Giant Hero Metric Badges (0 Overlimits, 539 Tests, 0.35s verify_all)
    - Hero closing quote: "Kempower Hardware. Project Sentinel Brain."
    """
    draw.text((100, 100), "DETERMINISTIC VERIFICATION & SYSTEM CLOSING", fill=C_TEXT_WHITE, font=fonts.get("title", 24))
    draw.text((100, 135), "100% Genuine Reproduction under Single Terminal Command", fill=C_TEXT_MUTED, font=fonts.get("text", 16))

    # 3 Giant Hero Metric Badges
    badges = [
        (100, 630, "0", C_GREEN, "Grid Overlimits", "134,400 intervals verified bit-for-bit"),
        (680, 1220, "539", C_CYAN, "Tests Green (100%)", "433 Pytest + 106 Independent E2E"),
        (1270, 1800, "0.35s", C_BLUE, "verify_all.py Runtime", "Zero hardcoded facades · Instant audit"),
    ]

    for x0, x1, b_num, b_col, b_title, b_sub in badges:
        draw_card(draw, (x0, 175, x1, 460), fill=C_CARD_BG, outline=b_col, radius=16, width=2)
        draw.text((x0 + 40, 205), b_num, fill=b_col, font=fonts.get("title", 72))
        draw.text((x0 + 40, 310), b_title, fill=C_TEXT_WHITE, font=fonts.get("title", 24))
        draw.text((x0 + 40, 365), b_sub, fill=C_TEXT_LIGHT, font=fonts.get("text", 17))

    # Master Hero Closing Lockup Card
    draw_card(draw, (100, 500, 1800, 960), fill=(16, 24, 38), outline=C_CYAN, radius=18, width=2)
    draw_bolt_icon(draw, (WIDTH // 2, 580), size=68, color=C_CYAN)

    q1 = '"Kempower builds the world\'s most flexible DC charging hardware."'
    bb1 = draw.textbbox((0, 0), q1, font=fonts.get("title", 32))
    draw.text(((WIDTH - (bb1[2] - bb1[0])) // 2, 640), q1, fill=C_TEXT_WHITE, font=fonts.get("title", 32))

    q2 = '"Project Sentinel provides the autonomous operating brain it deserves."'
    bb2 = draw.textbbox((0, 0), q2, font=fonts.get("title", 32))
    draw.text(((WIDTH - (bb2[2] - bb2[0])) // 2, 695), q2, fill=C_CYAN, font=fonts.get("title", 32))

    sub_close = "Autonomous Energy Certainty-as-a-Service · LahtiES Energy Tech Hackathon 2026 · LUT University"
    bbs = draw.textbbox((0, 0), sub_close, font=fonts.get("text", 20))
    draw.text(((WIDTH - (bbs[2] - bbs[0])) // 2, 780), sub_close, font=fonts.get("text", 20))

    # Bottom Triad Pills
    pills = "[ 100 Sites Ground Truth ]   ·   [ 0 Continuous Operations ]   ·   [ Bankable Outcome SLA ]"
    bbp = draw.textbbox((0, 0), pills, font=fonts.get("mono_b", 18))
    draw.text(((WIDTH - (bbp[2] - bbp[0])) // 2, 860), pills, fill=C_TEXT_LIGHT, font=fonts.get("mono_b", 18))


# -----------------------------------------------------------------------------
# Main Video Rendering Pipeline
# -----------------------------------------------------------------------------
def probe_encoder() -> Tuple[str, List[str]]:
    """Probes whether NVIDIA NVENC is operational; falls back to libx264."""
    nvenc_cmd = [
        "ffmpeg", "-y", "-f", "rawvideo", "-vcodec", "rawvideo",
        "-s", "64x64", "-pix_fmt", "rgb24", "-r", "30",
        "-i", "-",
        "-c:v", "h264_nvenc", "-preset", "p4", "-pix_fmt", "yuv420p", "-an",
        "-f", "null", "-"
    ]
    try:
        p = subprocess.Popen(nvenc_cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        dummy_frame = b"\x00" * (64 * 64 * 3)
        p.stdin.write(dummy_frame)
        p.stdin.close()
        ret = p.wait(timeout=3)
        if ret == 0:
            return "h264_nvenc", ["-c:v", "h264_nvenc", "-preset", "p4", "-b:v", "5M"]
    except Exception:
        pass

    # Fallback to libx264
    return "libx264", ["-c:v", "libx264", "-preset", "ultrafast", "-crf", "20"]


def render_all_frames(output_path: Path, poster_path: Path, fast_mode: bool = False) -> int:
    """Executes frame-by-frame rendering and FFmpeg streaming with keynote minimalism."""
    # Enforce recursive directory creation
    output_path.parent.mkdir(parents=True, exist_ok=True)
    poster_path.parent.mkdir(parents=True, exist_ok=True)
    DEMO_DIR.mkdir(parents=True, exist_ok=True)

    fonts = FontManager()

    frame_step = 5 if fast_mode else 1
    target_frames = TOTAL_FRAMES // frame_step

    encoder_name, encoder_flags = probe_encoder()
    print(f"[*] Encoder selected: {encoder_name} (Fast Mode: {fast_mode})")
    print(f"[*] Output destination: {output_path}")
    print(f"[*] Target frames: {target_frames} @ {FPS} fps ({TOTAL_SECONDS:.1f}s)")

    ffmpeg_bin = shutil.which("ffmpeg")
    if not ffmpeg_bin:
        print("[!] Error: ffmpeg binary not found in system PATH!", file=sys.stderr)
        return 1

    cmd = [
        ffmpeg_bin, "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-pix_fmt", "rgb24",
        "-r", str(FPS),
        "-i", "-",
        *encoder_flags,
        "-pix_fmt", "yuv420p",
        "-an",  # Strictly silent video per Requirement R3
        str(output_path)
    ]

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    t_start = time.time()
    last_print = t_start
    poster_saved = False

    try:
        for f_idx in range(0, TOTAL_FRAMES, frame_step):
            current_time = f_idx / float(FPS)

            # Clean deep slate canvas
            img = Image.new("RGB", (WIDTH, HEIGHT), C_BG)
            draw = ImageDraw.Draw(img)

            # Determine active scene & chapter breadcrumb
            if current_time < 10.0:
                scene_title = "ACT 1 · THE RADICAL VISION"
                render_scene_1(draw, fonts, current_time, current_time)
            elif current_time < 22.0:
                scene_title = "ACT 2 · THE 20.76 FTE HUMAN CRISIS"
                render_scene_2(draw, fonts, current_time, current_time - 10.0)
            elif current_time < 36.0:
                scene_title = "ACT 3 · THREE-LAYER CLOSED-LOOP OS"
                render_scene_3(draw, fonts, current_time, current_time - 22.0)
            elif current_time < 54.0:
                scene_title = "ACT 4 · HERO PROCESS 1: TOPOLOGY SELF-HEALING"
                render_scene_4(draw, fonts, current_time, current_time - 36.0)
            elif current_time < 68.0:
                scene_title = "ACT 5 · HERO PROCESS 2: 10x PRICE SPIKE PREEMPTION"
                render_scene_5(draw, fonts, current_time, current_time - 54.0)
            else:
                scene_title = "ACT 6 · DETERMINISTIC PROOF & CLOSING"
                render_scene_6(draw, fonts, current_time, current_time - 68.0)

            # Clean top header (NO subtitle boxes, NO SHA256 hashes, NO millisecond counters)
            draw_header(draw, fonts, current_time, scene_title)
            draw_minimal_footer(draw, fonts)

            # Save poster frame at t=45.0s (Hero Process 1: Topology Self-Healing)
            if not poster_saved and current_time >= 45.0:
                img.save(str(poster_path))
                poster_saved = True

            # Write raw RGB bytes to FFmpeg stdin pipe
            proc.stdin.write(img.tobytes())

            now = time.time()
            if now - last_print >= 2.0 or f_idx >= TOTAL_FRAMES - frame_step:
                pct = (f_idx + 1) / float(TOTAL_FRAMES) * 100.0
                fps_render = (f_idx + 1) / max(0.001, (now - t_start))
                print(f"[>] Rendering: {pct:5.1f}% | Frame {f_idx:04d}/{TOTAL_FRAMES} | Speed: {fps_render:.1f} fps")
                last_print = now

        proc.stdin.close()
        ret = proc.wait()

    except Exception as e:
        print(f"[!] Rendering exception: {e}", file=sys.stderr)
        try:
            proc.kill()
        except Exception:
            pass
        return 1

    elapsed = time.time() - t_start
    if ret != 0:
        print(f"[!] FFmpeg exited with non-zero returncode: {ret}", file=sys.stderr)
        return ret

    # Fallback to save poster if not yet saved
    if not poster_saved:
        img.save(str(poster_path))

    file_size_mb = output_path.stat().st_size / (1024 * 1024) if output_path.exists() else 0.0
    print("=" * 78)
    print(f"[SUCCESS] Video rendered in {elapsed:.2f}s ({TOTAL_FRAMES / elapsed:.1f} fps)")
    print(f"[SUCCESS] Output Video : {output_path} ({file_size_mb:.2f} MB)")
    print(f"[SUCCESS] Poster Image : {poster_path}")
    print("=" * 78)
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Render Project Sentinel 75-second Demo Video")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT),
                        help="Path to output MP4 video file")
    parser.add_argument("--poster", type=str, default=str(DEFAULT_POSTER),
                        help="Path to output PNG poster image")
    parser.add_argument("--fast", action="store_true",
                        help="Fast preview mode (renders every 5th frame)")
    args = parser.parse_args()

    out_path = Path(args.output).resolve()
    post_path = Path(args.poster).resolve()
    return render_all_frames(out_path, post_path, fast_mode=args.fast)


if __name__ == "__main__":
    sys.exit(main())
