"""
Verification Script for Project Sentinel Pitch Deck
Validates OpenXML structure, dimensions, 16:9 widescreen ratio, Slide 8 video showcase,
native OpenXML transitions/animations, 100% English purity (zero CJK), and speaker notes.
"""

import os
import sys
import re
import pptx
from pptx.util import Inches
from pptx.enum.shapes import MSO_SHAPE_TYPE

def verify_presentation(pptx_path: str):
    print("=" * 80)
    print("PROJECT SENTINEL PITCH DECK VERIFICATION AUDIT")
    print(f"Target File: {pptx_path}")
    print("=" * 80)

    # 1. Existence and size
    assert os.path.exists(pptx_path), f"File not found: {pptx_path}"
    file_size = os.path.getsize(pptx_path)
    file_size_kb = file_size / 1024
    print(f"[CHECK 1] File Existence: PASS (Size: {file_size_kb:.1f} KB / {file_size} bytes)")
    assert file_size > 50_000, f"File size unexpectedly small ({file_size} bytes)"

    # 2. OpenXML Parse
    prs = pptx.Presentation(pptx_path)
    print("[CHECK 2] OpenXML Parse: PASS (Successfully parsed by python-pptx)")

    # 3. Slide Dimensions (16:9 Widescreen)
    w_in = prs.slide_width.inches
    h_in = prs.slide_height.inches
    aspect_ratio = w_in / h_in
    print(f"[CHECK 3] Dimensions: {w_in:.3f}\" x {h_in:.3f}\" (Aspect Ratio: {aspect_ratio:.4f})")
    assert abs(w_in - 13.333) < 0.01 and abs(h_in - 7.500) < 0.01, f"Dimensions not exact 16:9 widescreen: {w_in} x {h_in}"
    assert abs(aspect_ratio - (16.0 / 9.0)) < 0.01, f"Aspect ratio not 16:9: {aspect_ratio}"
    print("          Dimensions Verification: PASS (Exact 16:9 Widescreen)")

    # 4. Slide Count (Strict Hackathon Constraint: 8 to 12 slides)
    slide_count = len(prs.slides)
    print(f"[CHECK 4] Slide Count: {slide_count} slides")
    assert slide_count == 12, f"Expected exactly 12 slides, got {slide_count}"
    assert 8 <= slide_count <= 12, f"Slide count outside 8-12 rule: {slide_count}"
    print("          Slide Count Verification: PASS (Exactly 12 slides)")

    # 5. Slide-by-Slide Detailed Inspection
    print("\n" + "-" * 80)
    print("DETAILED SLIDE-BY-SLIDE INSPECTION")
    print("-" * 80)

    all_slide_texts = []
    all_notes_texts = []
    transitions_count = 0
    timings_count = 0
    slide_8_picture_details = None

    for idx, slide in enumerate(prs.slides, 1):
        shapes = list(slide.shapes)
        has_picture = any(s.shape_type == MSO_SHAPE_TYPE.PICTURE for s in shapes)
        has_timing = '<p:timing' in slide._element.xml
        has_trans = '<p:transition' in slide._element.xml
        
        if has_trans:
            transitions_count += 1
        if has_timing:
            timings_count += 1

        # Extract slide shape texts
        slide_text_snippets = []
        for s in shapes:
            if s.has_text_frame:
                for p in s.text_frame.paragraphs:
                    t = p.text.strip()
                    if t:
                        slide_text_snippets.append(t)
            elif s.has_table:
                for row in s.table.rows:
                    for cell in row.cells:
                        t = cell.text.strip()
                        if t:
                            slide_text_snippets.append(t)

        slide_full_text = " ".join(slide_text_snippets)
        all_slide_texts.append(slide_full_text)

        # Check Notes Slide
        assert slide.has_notes_slide, f"Slide {idx} missing notes slide!"
        notes_text = slide.notes_slide.notes_text_frame.text.strip()
        assert len(notes_text) > 100, f"Slide {idx} notes text too short ({len(notes_text)} chars)!"
        all_notes_texts.append(notes_text)

        # Title snippet
        title = slide_text_snippets[1] if len(slide_text_snippets) > 1 else (slide_text_snippets[0] if slide_text_snippets else "UNTITLED")
        title_disp = title.replace("\n", " ")[:45]

        # Check Slide 8 picture details
        if idx == 8:
            pic_shapes = [s for s in shapes if s.shape_type == MSO_SHAPE_TYPE.PICTURE]
            assert pic_shapes, "Slide 8 missing embedded picture shape!"
            pic = pic_shapes[0]
            slide_8_picture_details = (pic.left.inches, pic.top.inches, pic.width.inches, pic.height.inches)

        print(f"Slide {idx:02d}: {len(shapes):02d} shapes | Anim: {has_timing} | Trans: {has_trans} | Notes: {len(notes_text):04d} chars | Title: {title_disp}...")

    # 6. Requirement R3: Slide 8 Video Showcase Verification
    print("\n" + "-" * 80)
    print("REQUIREMENT R3: SLIDE 8 DEDICATED VIDEO DEMO SHOWCASE")
    print("-" * 80)
    assert slide_8_picture_details is not None, "CRITICAL ERROR: Slide 8 has no video poster image!"
    px, py, pw, ph = slide_8_picture_details
    video_aspect = pw / ph
    print(f"[CHECK 5] Video Poster Shape Embedded: PASS")
    print(f"          Position: Left={px:.2f}\", Top={py:.2f}\", Width={pw:.2f}\", Height={ph:.2f}\"")
    print(f"          Aspect Ratio: {video_aspect:.4f} (Target 16:9 = {16/9:.4f})")
    assert abs(video_aspect - (16.0 / 9.0)) < 0.05, f"Canvas not 16:9 ratio: {video_aspect}"

    # Verify 4 Core Highlight Cards on Slide 8
    s8_blob = all_slide_texts[7]
    s8_highlights = [
        "01 · DYNAMIC BUSBAR RECONFIGURATION" in s8_blob,
        "02 · 10x SPOT PRICE SPIKE ARBITRAGE" in s8_blob,
        "03 · HIGHWAY 72h SQLITE WAL ISLANDING BRAIN" in s8_blob,
        "04 · HARDWARE GROUND-FAULT & DIGITAL TWIN AUTO-HEAL" in s8_blob,
    ]
    print(f"[CHECK 6] Slide 8 4 Core Highlight Cards: PASS ({all(s8_highlights)})")
    assert all(s8_highlights), f"One or more highlight cards missing on Slide 8: {s8_highlights}"

    # 7. 100% English Purity Verification (Zero CJK)
    print("\n" + "-" * 80)
    print("LANGUAGE AUDIT: 100% ENGLISH PURITY (ZERO CJK CHARACTERS)")
    print("-" * 80)
    total_deck_text = "\n".join(all_slide_texts + all_notes_texts)
    cjk_matches = re.findall(r'[\u4e00-\u9fff]', total_deck_text)
    print(f"[CHECK 7] CJK Characters Count in Presentation & Notes: {len(cjk_matches)}")
    assert len(cjk_matches) == 0, f"Found unexpected CJK characters: {cjk_matches[:20]}"
    print("          English Purity Verification: PASS (Strictly 100% English)")

    # 8. Native OpenXML Dynamics: Transitions & Sequential Build Timing
    print("\n" + "-" * 80)
    print("DYNAMICS AUDIT: NATIVE OPENXML TRANSITIONS & TIMINGS")
    print("-" * 80)
    print(f"[CHECK 8] OpenXML Slide Transitions: {transitions_count} / {slide_count} slides with <p:transition><p:fade/></p:transition>")
    assert transitions_count == slide_count, f"Not all slides have transitions: {transitions_count}/{slide_count}"
    print(f"[CHECK 9] OpenXML Build Animations: {timings_count} / {slide_count} slides with native <p:timing>")
    assert timings_count == slide_count, f"Not all slides have build animations: {timings_count}/{slide_count}"

    # 9. Dynamic Process Flow Badges Audit on Key Process Slides (Slides 4, 5, 6, 7, 9)
    print("\n" + "-" * 80)
    print("PROCESS FLOW BADGES AUDIT: 'STEP 1: DETECT' ➔ 'STEP 2: ISOLATE' ➔ 'STEP 3: REROUTE' ➔ 'STEP 4: ZERO DEFICIT'")
    print("-" * 80)
    process_slides = [4, 5, 6, 7, 9]
    for p_idx in process_slides:
        slide_text = all_slide_texts[p_idx - 1]
        has_step_1 = "STEP 1:" in slide_text
        has_step_2 = "STEP 2:" in slide_text
        has_step_3 = "STEP 3:" in slide_text
        has_step_4 = "STEP 4:" in slide_text
        print(f"Slide {p_idx:02d} Process Flow Badges: Step1={has_step_1}, Step2={has_step_2}, Step3={has_step_3}, Step4={has_step_4}")
        assert has_step_1 and has_step_2 and has_step_3 and has_step_4, f"Slide {p_idx} missing full 4-step process flow!"
    print("[CHECK 10] Dynamic Process Flow Badges: PASS (All process slides verified)")

    # 10. Speaker Notes & Signature Quote Audit
    print("\n" + "-" * 80)
    print("SPEAKER NOTES AUDIT & SIGNATURE QUOTE VERIFICATION")
    print("-" * 80)
    signature_quote = "What we built is not six patches, but one unified self-operating system; the goal is not to make equipment never fail, but to make failures never require human intervention."
    s12_card_has_quote = signature_quote in all_slide_texts[11]
    s12_notes_has_quote = signature_quote in all_notes_texts[11]
    print(f"Slide 12 Card Signature Quote: {s12_card_has_quote}")
    print(f"Slide 12 Notes Signature Quote: {s12_notes_has_quote}")
    assert s12_card_has_quote, "Slide 12 card text missing signature quote!"
    assert s12_notes_has_quote, "Slide 12 speaker notes missing signature quote!"
    print("[CHECK 11] Signature Quote Verification: PASS (Exact English quote present in card and notes)")

    # 11. Final Summary Statistics
    print("\n" + "=" * 80)
    print("VERIFICATION AUDIT COMPLETE: 100% PASS")
    print("=" * 80)
    print(f"Total Slides: {slide_count}")
    print(f"File Size: {file_size_kb:.1f} KB")
    print(f"Transitions Verified: {transitions_count} / {slide_count}")
    print(f"Animations Verified: {timings_count} / {slide_count}")
    print(f"Speaker Notes Verified: {len(all_notes_texts)} / {slide_count}")
    print(f"CJK Character Count: 0 (100% Pure English)")
    print("All Acceptance Criteria Satisfied: YES")
    print("=" * 80)

if __name__ == "__main__":
    default_target = "Project_Sentinel_12pages_final.pptx" if os.path.exists("Project_Sentinel_12pages_final.pptx") else "Project_Sentinel_Pitch_Deck.pptx"
    pptx_path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), default_target)
    verify_presentation(pptx_path)
