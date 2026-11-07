import os
import shutil
import re

ROOT = os.path.abspath(".")
SUBMISSION_DIR = os.path.join(ROOT, "submission")

CJK_PATTERN = re.compile(r'[\u4e00-\u9fff]')

def copy_tree_clean(src, dst, exclude_exts=None, exclude_names=None):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)
    exclude_exts = exclude_exts or []
    exclude_names = exclude_names or []
    
    for root, dirs, files in os.walk(src):
        # Ignore cache and hidden dirs
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

    print("Staging submission directory strictly per official guidelines (No videos, No rejected web demos)...")

    # 1. code/
    code_dir = os.path.join(SUBMISSION_DIR, "code")
    copy_tree_clean(os.path.join(ROOT, "src"), os.path.join(code_dir, "src"))
    copy_tree_clean(os.path.join(ROOT, "e2e_tests"), os.path.join(code_dir, "e2e_tests"))
    copy_tree_clean(os.path.join(ROOT, "tests"), os.path.join(code_dir, "tests"))
    copy_tree_clean(os.path.join(ROOT, "tools"), os.path.join(code_dir, "tools"))
    
    # demo_scenarios code (strictly excluding all mp4 video files)
    demo_scenarios_src = os.path.join(ROOT, "demo_scenarios")
    demo_scenarios_dst = os.path.join(code_dir, "demo_scenarios")
    copy_tree_clean(demo_scenarios_src, demo_scenarios_dst, exclude_exts=['.mp4', '.avi', '.mov', '.webm'])

    for f in ["verify_all.py", "run_s1.py", "app.py", "requirements.txt", "pytest.ini"]:
        src_path = os.path.join(ROOT, f)
        if os.path.exists(src_path):
            copy_file_safe(src_path, os.path.join(code_dir, f))

    # 2. docs/
    docs_dir = os.path.join(SUBMISSION_DIR, "docs")
    os.makedirs(docs_dir, exist_ok=True)
    
    # Core specification & audit reports
    doc_files = [
        ("One_Page_SLA_Specification.md", "One_Page_SLA_Specification.md"),
        ("Team3-One_Page-Autonomous_Charging_Services_Agreement.docx", "Team3-One_Page-Autonomous_Charging_Services_Agreement.docx"),
        ("docs/one_page_agreement.html", "one_page_agreement.html"),
        ("docs/one_page_agreement.md", "one_page_agreement.md"),
        ("docs/PROJECT_AUDIT_REPORT.md", "PROJECT_AUDIT_REPORT.md"),
        ("docs/energy_impact.md", "energy_impact.md"),
        ("docs/attribution_matrix.md", "attribution_matrix.md"),
        ("docs/assumptions_and_additions.md", "assumptions_and_additions.md"),
        ("ZERO_HUMAN_DESIGN.md", "ZERO_HUMAN_DESIGN.md"),
        ("PROJECT.md", "PROJECT.md"),
        ("HACKATHON.md", "HACKATHON.md"),
    ]
    for src_rel, dst_rel in doc_files:
        src_path = os.path.join(ROOT, src_rel)
        if os.path.exists(src_path):
            copy_file_safe(src_path, os.path.join(docs_dir, dst_rel))
            
    # demo_day/ manual (English only, exclude Chinese master portrait)
    demo_day_src = os.path.join(ROOT, "docs", "demo_day")
    demo_day_dst = os.path.join(docs_dir, "demo_day")
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

    # hackathon/ pack
    hackathon_src = os.path.join(ROOT, "docs", "hackathon")
    hackathon_dst = os.path.join(docs_dir, "hackathon")
    copy_tree_clean(hackathon_src, hackathon_dst)

    # 3. presentation/
    pres_dir = os.path.join(SUBMISSION_DIR, "presentation")
    os.makedirs(pres_dir, exist_ok=True)
    
    # Strictly user-provided PPT (Project_Sentinel_12pages_v3.pptx) and pitch scripts
    # NO video files, NO web presentations, NO other PPT versions
    pres_files = [
        ("Project_Sentinel_12pages_v3.pptx", "Project_Sentinel_12pages_v3.pptx"),
        ("Project_Sentinel_Pitch_Script_12pages.md", "Project_Sentinel_Pitch_Script_12pages.md"),
        ("docs/SPEECH_10MIN_ENGLISH_OFFICIAL.md", "SPEECH_10MIN_ENGLISH_OFFICIAL.md"),
        ("docs/PPT_SPEECH_PLAN.md", "PPT_SPEECH_PLAN.md"),
        ("PITCH_DECK_OUTLINE_v2.md", "PITCH_DECK_OUTLINE_v2.md"),
        ("PITCH_DECK_OUTLINE.md", "PITCH_DECK_OUTLINE.md"),
        ("demo_scenarios/SPEECH_SIX_SCENES.md", "SPEECH_SIX_SCENES.md"),
        ("demo_scenarios/SPEECH_OVERHEAT_SCENE.md", "SPEECH_OVERHEAT_SCENE.md"),
    ]
    for src_rel, dst_rel in pres_files:
        src_path = os.path.join(ROOT, src_rel)
        if os.path.exists(src_path):
            copy_file_safe(src_path, os.path.join(pres_dir, dst_rel))

    # 4. Top-level README.md and master English portrait
    copy_file_safe(os.path.join(ROOT, "README.md"), os.path.join(SUBMISSION_DIR, "README.md"))
    copy_file_safe(os.path.join(ROOT, "README_EN.md"), os.path.join(SUBMISSION_DIR, "README_EN.md"))

    print("Submission directory staged successfully!")

if __name__ == "__main__":
    main()
