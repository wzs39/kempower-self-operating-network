import os
import shutil
import re

ROOT = os.path.abspath(".")
SUBMISSION_DIR = os.path.join(ROOT, "submission")

CJK_PATTERN = re.compile(r'[\u4e00-\u9fff]')

def copy_tree_clean(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst, exist_ok=True)
    for root, dirs, files in os.walk(src):
        # ignore __pycache__ and cache dirs
        dirs[:] = [d for d in dirs if d not in ['__pycache__', '.pytest_cache', '.git']]
        rel_dir = os.path.relpath(root, src)
        target_dir = os.path.join(dst, rel_dir) if rel_dir != '.' else dst
        os.makedirs(target_dir, exist_ok=True)
        for f in files:
            if f.endswith(('.pyc', '.pyo')):
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

    print("Staging submission directory...")

    # 1. code/
    code_dir = os.path.join(SUBMISSION_DIR, "code")
    copy_tree_clean(os.path.join(ROOT, "src"), os.path.join(code_dir, "src"))
    copy_tree_clean(os.path.join(ROOT, "e2e_tests"), os.path.join(code_dir, "e2e_tests"))
    copy_tree_clean(os.path.join(ROOT, "tests"), os.path.join(code_dir, "tests"))
    copy_tree_clean(os.path.join(ROOT, "tools"), os.path.join(code_dir, "tools"))
    
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
            
    # demo_day/ manual
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
    pres_files = [
        ("Project_Sentinel_12pages_final.pptx", "Project_Sentinel_12pages_final.pptx"),
        ("PITCH_DECK_OUTLINE_v2.md", "PITCH_DECK_OUTLINE_v2.md"),
        ("PITCH_DECK_OUTLINE.md", "PITCH_DECK_OUTLINE.md"),
        ("demo_scenarios/SPEECH_SIX_SCENES.md", "SPEECH_SIX_SCENES.md"),
        ("demo_scenarios/SPEECH_OVERHEAT_SCENE.md", "SPEECH_OVERHEAT_SCENE.md"),
        ("demo/presentation_demo.mp4", "presentation_demo.mp4"),
        ("demo_scenarios/presentation 1.mp4", "presentation 1.mp4"),
        ("demo_scenarios/presentation 2.mp4", "presentation 2.mp4"),
    ]
    for src_rel, dst_rel in pres_files:
        src_path = os.path.join(ROOT, src_rel)
        if os.path.exists(src_path):
            copy_file_safe(src_path, os.path.join(pres_dir, dst_rel))

    # 4. videos/
    videos_dir = os.path.join(SUBMISSION_DIR, "videos")
    os.makedirs(videos_dir, exist_ok=True)
    video_files = [
        "1.Night replay.mp4",
        "2.Outage replay.mp4",
        "3.Price spike replay.mp4",
        "4.Curtailment replay.mp4",
        "5.Cable fault replay.mp4",
        "6.Commissioning replay.mp4",
    ]
    for vf in video_files:
        src_path = os.path.join(ROOT, "demo_scenarios", vf)
        if os.path.exists(src_path):
            copy_file_safe(src_path, os.path.join(videos_dir, vf))

    # 5. Top-level README.md
    copy_file_safe(os.path.join(ROOT, "README.md"), os.path.join(SUBMISSION_DIR, "README.md"))

    print("Submission directory staged successfully!")

if __name__ == "__main__":
    main()
