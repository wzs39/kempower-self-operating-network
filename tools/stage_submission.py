import os
import sys
import shutil
import re
from pathlib import Path

ROOT = os.path.abspath(".")
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tools.md_to_pdf import convert_md_to_pdf, convert_html_to_pdf
SUBMISSION_DIR = os.path.join(ROOT, "submission")

CJK_PATTERN = re.compile(r'[\u4e00-\u9fff]')

def copy_tree_clean(src, dst, exclude_exts=None, exclude_names=None):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)
    exclude_exts = exclude_exts or []
    exclude_names = exclude_names or []
    
    for root, dirs, files in os.walk(src):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.pytest_cache', '.git', '.idea', '.vscode']]
        rel_dir = os.path.relpath(root, src)
        target_dir = os.path.join(dst, rel_dir) if rel_dir != '.' else dst
        os.makedirs(target_dir, exist_ok=True)
        for f in files:
            if f.endswith(('.pyc', '.pyo')):
                continue
            if any(f.endswith(ext) for ext in exclude_exts):
                continue
            if f in exclude_names:
                continue
            src_file = os.path.join(root, f)
            dst_file = os.path.join(target_dir, f)
            shutil.copy2(src_file, dst_file)

def copy_file_safe(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)

def main():
    if os.path.exists(SUBMISSION_DIR):
        shutil.rmtree(SUBMISSION_DIR)
    os.makedirs(SUBMISSION_DIR, exist_ok=True)

    print("=" * 70)
    print("STAGING SUBMISSION DIRECTORY (Pillars 1-4 + Zero-CJK + Markdown-to-PDF)")
    print("=" * 70)

    # -------------------------------------------------------------
    # Pillar 1: A 10-Minute Pitch Built Around 2029 Customer Story
    # -------------------------------------------------------------
    p1_dir = os.path.join(SUBMISSION_DIR, "1_Pitch_and_2029_Customer_Story")
    os.makedirs(p1_dir, exist_ok=True)
    p1_files = [
        ("Project_Sentinel_12pages_v3.pptx", "Project_Sentinel_12pages_v3.pptx"),
        ("docs/CUSTOMER_STORY_2029.md", "CUSTOMER_STORY_2029.md"),
        ("Project_Sentinel_Pitch_Script_12pages.md", "Project_Sentinel_Pitch_Script_12pages.md"),
        ("docs/SPEECH_10MIN_ENGLISH_OFFICIAL.md", "SPEECH_10MIN_ENGLISH_OFFICIAL.md"),
        ("docs/PPT_SPEECH_PLAN.md", "PPT_SPEECH_PLAN.md"),
        ("PITCH_DECK_OUTLINE_v2.md", "PITCH_DECK_OUTLINE_v2.md"),
    ]
    for s, d in p1_files:
        src_p = os.path.join(ROOT, s)
        if os.path.exists(src_p):
            copy_file_safe(src_p, os.path.join(p1_dir, d))

    # -------------------------------------------------------------
    # Pillar 2: The Demonstration (Part 2)
    # -------------------------------------------------------------
    p2_dir = os.path.join(SUBMISSION_DIR, "2_The_Demonstration_Part2")
    os.makedirs(p2_dir, exist_ok=True)
    copy_file_safe(os.path.join(ROOT, "docs/DEMONSTRATION_WALKTHROUGH.md"), os.path.join(p2_dir, "DEMONSTRATION_WALKTHROUGH.md"))
    copy_file_safe(os.path.join(ROOT, "demo_scenarios/SPEECH_SIX_SCENES.md"), os.path.join(p2_dir, "SPEECH_SIX_SCENES.md"))
    copy_file_safe(os.path.join(ROOT, "demo_scenarios/SPEECH_OVERHEAT_SCENE.md"), os.path.join(p2_dir, "SPEECH_OVERHEAT_SCENE.md"))
    
    for f in ["verify_all.py", "run_s1.py", "app.py", "requirements.txt", "pytest.ini"]:
        p = os.path.join(ROOT, f)
        if os.path.exists(p):
            copy_file_safe(p, os.path.join(p2_dir, f))

    copy_tree_clean(os.path.join(ROOT, "src"), os.path.join(p2_dir, "src"))
    copy_tree_clean(os.path.join(ROOT, "tests"), os.path.join(p2_dir, "tests"))
    copy_tree_clean(os.path.join(ROOT, "e2e_tests"), os.path.join(p2_dir, "e2e_tests"))
    copy_tree_clean(os.path.join(ROOT, "tools"), os.path.join(p2_dir, "tools"))
    
    # demo_scenarios code (strictly excluding all mp4 video files)
    demo_scenarios_src = os.path.join(ROOT, "demo_scenarios")
    demo_scenarios_dst = os.path.join(p2_dir, "demo_scenarios")
    copy_tree_clean(demo_scenarios_src, demo_scenarios_dst, exclude_exts=['.mp4', '.avi', '.mov', '.webm'])

    # -------------------------------------------------------------
    # Pillar 3: Commercial Model & One-Page Service Agreement (Part 3)
    # -------------------------------------------------------------
    p3_dir = os.path.join(SUBMISSION_DIR, "3_Commercial_Model_and_One_Page_SLA_Part3")
    os.makedirs(p3_dir, exist_ok=True)
    p3_files = [
        ("Team3-One_Page-Autonomous_Charging_Services_Agreement.docx", "Team3-One_Page-Autonomous_Charging_Services_Agreement.docx"),
        ("docs/COMMERCIAL_BUSINESS_MODEL.md", "COMMERCIAL_BUSINESS_MODEL.md"),
        ("One_Page_SLA_Specification.md", "One_Page_SLA_Specification.md"),
        ("docs/one_page_agreement.html", "one_page_agreement.html"),
        ("docs/one_page_agreement.md", "one_page_agreement.md"),
    ]
    for s, d in p3_files:
        src_p = os.path.join(ROOT, s)
        if os.path.exists(src_p):
            copy_file_safe(src_p, os.path.join(p3_dir, d))

    # -------------------------------------------------------------
    # Pillar 4: Energy and Control Core Architecture (Part 1)
    # -------------------------------------------------------------
    p4_dir = os.path.join(SUBMISSION_DIR, "4_Energy_and_Control_Core_Part1")
    os.makedirs(p4_dir, exist_ok=True)
    p4_files = [
        ("ZERO_HUMAN_DESIGN.md", "ZERO_HUMAN_DESIGN.md"),
        ("docs/PROJECT_AUDIT_REPORT.md", "PROJECT_AUDIT_REPORT.md"),
        ("docs/energy_impact.md", "energy_impact.md"),
        ("docs/attribution_matrix.md", "attribution_matrix.md"),
        ("docs/assumptions_and_additions.md", "assumptions_and_additions.md"),
        ("README_EN.md", "README_EN.md"),
        ("PROJECT.md", "PROJECT.md"),
        ("HACKATHON.md", "HACKATHON.md"),
    ]
    for s, d in p4_files:
        src_p = os.path.join(ROOT, s)
        if os.path.exists(src_p):
            copy_file_safe(src_p, os.path.join(p4_dir, d))

    # demo_day/ handbook
    demo_day_src = os.path.join(ROOT, "docs", "demo_day")
    demo_day_dst = os.path.join(p4_dir, "demo_day")
    os.makedirs(demo_day_dst, exist_ok=True)
    for f in [
        "README.md",
        "00_pocket_cheat_sheet.md",
        "01_stage_schedule_and_setup.md",
        "02_team_roles_and_coordination.md",
        "03_judge_personas_and_question_bank.md",
        "04_structured_defense_and_crisis_manual.md",
        "05_live_demo_operational_sop.md",
        "06_code_proof_and_authenticity_guide.md",
        "PROJECT_SENTINEL_MASTER_PORTRAIT_AND_FILE_INDEX_EN.md",
    ]:
        p = os.path.join(demo_day_src, f)
        if os.path.exists(p):
            copy_file_safe(p, os.path.join(demo_day_dst, f))

    # hackathon/ package
    hackathon_src = os.path.join(ROOT, "docs", "hackathon")
    hackathon_dst = os.path.join(p4_dir, "hackathon")
    copy_tree_clean(hackathon_src, hackathon_dst)

    # -------------------------------------------------------------
    # Root Files
    # -------------------------------------------------------------
    copy_file_safe(os.path.join(ROOT, "README.md"), os.path.join(SUBMISSION_DIR, "README.md"))

    print("\nStaging files completed. Starting batch PDF generation for all markdown files...")

    # Generate PDF for every .md and agreement .html file
    pdf_count = 0
    for root, dirs, files in os.walk(SUBMISSION_DIR):
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.pytest_cache', '.git']]
        for f in files:
            if f.endswith('.md'):
                md_path = os.path.join(root, f)
                pdf_path = os.path.splitext(md_path)[0] + ".pdf"
                convert_md_to_pdf(md_path, pdf_path)
                pdf_count += 1
            elif f == "one_page_agreement.html":
                html_path = os.path.join(root, f)
                pdf_path = os.path.join(root, "one_page_agreement.pdf")
                convert_html_to_pdf(html_path, pdf_path)
                pdf_count += 1

    print(f"\nAll {pdf_count} PDF companion files successfully generated!")
    print("Staging fully completed.")

if __name__ == "__main__":
    main()
