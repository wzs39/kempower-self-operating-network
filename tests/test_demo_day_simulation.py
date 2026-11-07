"""
Independent E2E Test Suite for Project Sentinel Demo Day Simulation Deliverables.
Author: test_writer_e2e_1
Specifications: TEST_INFRA.md, ORIGINAL_REQUEST.md, and orchestrator_r1/PROJECT.md.

Validates:
- R1: Stage Master Schedule (10 min pitch, 3-5 min Q&A, 120s demo, Failsafe Triad)
- R2: 4-Person Roles, Positioning, Verbatim Transitions, Member C Console SOP & Triggers
- R3: >= 3 Judge Personas, >= 12 Hardcore Questions with ID, category, and target persona
- R4: Structured 3-part answers, exact quantitative facts (21 FTE, 1.365M, 13->3 vs 13->0, 799.30, 260ms, 1,425 kW, MRDT), and Crisis SOPs
- Master Integration: README.md, 00_pocket_cheat_sheet.md, and complete docs/demo_day/ mirroring
"""

import os
import re
from pathlib import Path
import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SIM_DIR = REPO_ROOT / "demo_day_simulation"
DOCS_DIR = REPO_ROOT / "docs" / "demo_day"

ALL_EXPECTED_SIM_FILES = [
    "README.md",
    "00_pocket_cheat_sheet.md",
    "01_stage_schedule_and_setup.md",
    "02_team_roles_and_coordination.md",
    "03_judge_personas_and_question_bank.md",
    "04_structured_defense_and_crisis_manual.md",
]


def read_sim_file(filename: str) -> str:
    filepath = SIM_DIR / filename
    assert filepath.exists(), f"Expected deliverable file does not exist: {filepath}"
    content = filepath.read_text(encoding="utf-8")
    assert len(content.strip()) > 0, f"File {filename} is empty"
    return content


# ==============================================================================
# R1 Tests: Stage Schedule & Setup
# ==============================================================================
class TestR1StageScheduleAndSetup:
    """Verifies R1 requirements from 01_stage_schedule_and_setup.md."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.filename = "01_stage_schedule_and_setup.md"
        self.filepath = SIM_DIR / self.filename

    def test_r1_file_exists_and_substantial(self):
        assert self.filepath.exists(), f"R1 deliverable {self.filepath} not found"
        content = self.filepath.read_text(encoding="utf-8")
        assert len(content) >= 1500, f"R1 deliverable content is too short ({len(content)} chars)"

    def test_r1_pitch_total_duration_600s(self):
        content = read_sim_file(self.filename)
        # Check for 10-minute / 600s pitch limit specification
        has_10_min = bool(
            re.search(r"10\s*(?:min|minute)", content, re.IGNORECASE)
            or re.search(r"600\s*(?:s|sec|second)", content, re.IGNORECASE)
        )
        assert has_10_min, "R1 must explicitly define the 10-minute (600s) pitch total duration"

    def test_r1_qa_schedule_3_to_5_min(self):
        content = read_sim_file(self.filename)
        # Check for 3-5 minute Q&A / jury defense schedule
        has_qa = bool(
            re.search(r"[3-5]\s*[-–—~]\s*[3-5]\s*(?:min|minute)", content, re.IGNORECASE)
            or re.search(r"(?:180|240|300)\s*(?:s|sec|second)", content, re.IGNORECASE)
            or re.search(r"(?:Q&A|Defense).*?(?:3|5)\s*(?:min|minute)", content, re.IGNORECASE)
            or "10:00" in content and ("13:00" in content or "15:00" in content)
        )
        assert has_qa, "R1 must define the 3-5 minute Q&A defense schedule"

    def test_r1_live_demo_slot_120s(self):
        content = read_sim_file(self.filename)
        # Check for 120s live demo window within 5:00 to 7:00
        has_demo_slot = bool(
            re.search(r"120\s*(?:s|sec|second)", content, re.IGNORECASE)
            or re.search(r"2\s*(?:min|minute)", content, re.IGNORECASE)
        )
        assert has_demo_slot, "R1 must specify a 120-second (2-minute) live demo allocation"

        has_timing_window = bool(
            re.search(r"0?5:00\s*[-–—~]\s*0?7:00", content)
            or re.search(r"0?4:50\s*[-–—~]\s*0?7:00", content)
            or re.search(r"0?5:00\s*[-–—~]\s*0?6:[3-5][0-9]", content)
            or ("5:00" in content and "7:00" in content)
        )
        assert has_timing_window, "R1 must schedule live demo between 5:00 and 7:00"

    def test_r1_stage_layout_and_positioning(self):
        content = read_sim_file(self.filename)
        # Should contain stage setup / layout diagram or description
        has_layout = bool(
            re.search(r"(?:stage\s+layout|physical\s+setup|console|lectern|podium)", content, re.IGNORECASE)
        )
        assert has_layout, "R1 must provide stage layout and physical member positioning"

    def test_r1_failsafe_triad_components(self):
        content = read_sim_file(self.filename)
        # Failsafe Triad must reference:
        # 1. Streamlit app (app.py)
        # 2. CLI deterministic verifier (verify_all.py)
        # 3. Backup video (presentation_demo.mp4 or mp4 recording)
        assert "app.py" in content or "streamlit" in content.lower(), "Failsafe Triad missing Streamlit app reference"
        assert "verify_all.py" in content, "Failsafe Triad missing verify_all.py reference"
        assert re.search(r"(?:\.mp4|video|recording|backup\s*video)", content, re.IGNORECASE), "Failsafe Triad missing backup video reference"

        # Check cutover rule or latency threshold
        has_cutover_rule = bool(
            re.search(r"(?:fallback|cutover|failsafe|trigger|timeout)", content, re.IGNORECASE)
        )
        assert has_cutover_rule, "R1 must define failsafe cutover / fallback trigger rules"


# ==============================================================================
# R2 Tests: 4-Person Roles & Synergy
# ==============================================================================
class TestR2TeamRolesAndCoordination:
    """Verifies R2 requirements from 02_team_roles_and_coordination.md."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.filename = "02_team_roles_and_coordination.md"
        self.filepath = SIM_DIR / self.filename

    def test_r2_file_exists_and_substantial(self):
        assert self.filepath.exists(), f"R2 deliverable {self.filepath} not found"
        content = self.filepath.read_text(encoding="utf-8")
        assert len(content) >= 1500, f"R2 deliverable content is too short ({len(content)} chars)"

    def test_r2_four_member_role_definitions(self):
        content = read_sim_file(self.filename)
        # Distinct roles for Speaker A, Speaker B, Member C, Member D
        for role_pat in [r"Speaker\s+A",
                         r"Speaker\s+B",
                         r"Member\s+C",
                         r"Member\s+D"]:
            assert re.search(role_pat, content, re.IGNORECASE), f"R2 missing role definition for pattern: {role_pat}"

    def test_r2_role_responsibilities_separation(self):
        content = read_sim_file(self.filename)
        # Speaker A: Commercial, pain points, business model, 2029 customer story
        has_speaker_a_scope = bool(
            re.search(r"(?:commercial|business|pain|aeaas|caas|customer\s*story)", content, re.IGNORECASE)
        )
        assert has_speaker_a_scope, "Speaker A must cover business pain points and commercial model"

        # Speaker B: Technical architecture, L1/L2/L3, DPR, modular 25kW, physical grid
        has_speaker_b_scope = bool(
            re.search(r"(?:architecture|dpr|l1|l2|l3|25\s*kw|power\s*matrix)", content, re.IGNORECASE)
        )
        assert has_speaker_b_scope, "Speaker B must cover system architecture and technical solution"

        # Member C: Live Demo console, UI injection, screen switching
        has_member_c_scope = bool(
            re.search(r"(?:console|live\s*demo|injection|screen\s*switch)", content, re.IGNORECASE)
        )
        assert has_member_c_scope, "Member C must cover live demo console operations"

        # Member D: Deep Q&A defense, math formulas, SLA legal terms, extreme cases
        has_member_d_scope = bool(
            re.search(r"(?:defense|q&a|math|sla|mrdt|extreme)", content, re.IGNORECASE)
        )
        assert has_member_d_scope, "Member D must cover deep technical defense and math proofs"

    def test_r2_verbatim_speaker_transitions(self):
        content = read_sim_file(self.filename)
        # Must contain verbatim transition scripts / handoffs between speakers
        has_transitions = bool(
            re.search(r"(?:transition|handoff|relay)", content, re.IGNORECASE)
            and ("Speaker A" in content and "Speaker B" in content)
        )
        assert has_transitions, "R2 must provide verbatim dual-speaker relay transition scripts"

    def test_r2_member_c_console_sop_and_triggers(self):
        content = read_sim_file(self.filename)
        # Must define console SOP, hotkeys or execution commands, and cutover trigger
        has_sop = bool(
            re.search(r"(?:sop|checklist|hotkey|procedure|step)", content, re.IGNORECASE)
        )
        assert has_sop, "R2 must provide Member C Console Operator SOP"

        has_cutover_triggers = bool(
            re.search(r"(?:emergency|cutover|freeze|crash|black[- ]swan)", content, re.IGNORECASE)
        )
        assert has_cutover_triggers, "R2 must define emergency cutover triggers for Member C"


# ==============================================================================
# R3 Tests: Judge Personas & Questions
# ==============================================================================
class TestR3JudgePersonasAndQuestions:
    """Verifies R3 requirements from 03_judge_personas_and_question_bank.md."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.filename = "03_judge_personas_and_question_bank.md"
        self.filepath = SIM_DIR / self.filename

    def test_r3_file_exists_and_substantial(self):
        assert self.filepath.exists(), f"R3 deliverable {self.filepath} not found"
        content = self.filepath.read_text(encoding="utf-8")
        assert len(content) >= 2000, f"R3 deliverable content is too short ({len(content)} chars)"

    def test_r3_judge_personas_count_and_types(self):
        content = read_sim_file(self.filename)
        # Must have at least 3 distinct personas: Technical/Architect, Commercial/VC, Kempower Challenge
        has_tech_judge = bool(
            re.search(r"(?:technical|architect|engineer|panu|iiro)", content, re.IGNORECASE)
        )
        has_vc_judge = bool(
            re.search(r"(?:commercial|vc|investor|lahties)", content, re.IGNORECASE)
        )
        has_kempower_judge = bool(
            re.search(r"(?:kempower|mats|mattsson|challenge\s*lead)", content, re.IGNORECASE)
        )

        assert has_tech_judge, "R3 missing Technical/Architect judge persona"
        assert has_vc_judge, "R3 missing Commercial/VC judge persona"
        assert has_kempower_judge, "R3 missing Kempower Challenge Provider judge persona"

    def test_r3_hardcore_questions_count_at_least_12(self):
        content = read_sim_file(self.filename)
        # Match question identifiers like Q01..Q14, Q1..Q14, or Question 1..14
        matches = re.findall(r"(?:Q\s*0?[1-9]|Q\s*1[0-9]|Question\s*0?[1-9]|Question\s*1[0-9]|###\s*Q[0-9]+)", content, re.IGNORECASE)
        unique_matches = set(re.sub(r"\s+", "", m.upper()) for m in matches)
        assert len(unique_matches) >= 12, (
            f"R3 must provide at least 12 distinct hardcore questions. Found {len(unique_matches)}: {unique_matches}"
        )

    def test_r3_question_structure_metadata(self):
        content = read_sim_file(self.filename)
        # Questions should have ID, Category, Target Persona
        has_id = bool(re.search(r"Q0?[1-9]|Q1[0-9]", content))
        has_target_persona = bool(
            re.search(r"(?:Target\s*Persona|Target\s*Judge|Primary\s*Juror|Juror\s*Category)", content, re.IGNORECASE)
        )
        has_category = bool(
            re.search(r"(?:Category|Focus|Target\s*Domain)", content, re.IGNORECASE)
        )

        assert has_id, "Questions must feature distinct identifiers (e.g. Q01..Q14)"
        assert has_target_persona, "Questions must explicitly target specific judge personas"
        assert has_category, "Questions must state their evaluation category/focus"


# ==============================================================================
# R4 Tests: Structured Defense & Crisis Response
# ==============================================================================
class TestR4StructuredDefenseAndCrisis:
    """Verifies R4 requirements from 04_structured_defense_and_crisis_manual.md."""

    @pytest.fixture(autouse=True)
    def setup_class(self):
        self.filename = "04_structured_defense_and_crisis_manual.md"
        self.filepath = SIM_DIR / self.filename

    def test_r4_file_exists_and_substantial(self):
        assert self.filepath.exists(), f"R4 deliverable {self.filepath} not found"
        content = self.filepath.read_text(encoding="utf-8")
        assert len(content) >= 2500, f"R4 deliverable content is too short ({len(content)} chars)"

    def test_r4_three_part_structured_answers(self):
        content = read_sim_file(self.filename)
        # Structured defense framework: 3 parts (Direct assertion / Data & math proof / Strategic takeaway)
        has_three_part = bool(
            re.search(r"(?:3-part|bottom-line|direct\s*answer|assertion|quantitative)", content, re.IGNORECASE)
            or (re.search(r"(?:Part\s*1|1\.|Direct)", content) and re.search(r"(?:Part\s*2|2\.|Proof|Data)", content))
        )
        assert has_three_part, "R4 must provide structured 3-part answers for defense questions"

    def test_r4_quantitative_facts_21_fte(self):
        content = read_sim_file(self.filename)
        # 21 FTE or 20.76 FTE
        has_21_fte = bool(re.search(r"(?:21|20\.76)\s*FTE", content, re.IGNORECASE))
        assert has_21_fte, "R4 must cite the 21 FTE (or 20.76 FTE) labor benchmark"

    def test_r4_quantitative_facts_1_365m_eur(self):
        content = read_sim_file(self.filename)
        # 1.365M € or 1,365,000 or 1.82M
        has_1_365m = bool(
            re.search(r"1\.365\s*(?:M|M€|million)", content, re.IGNORECASE)
            or "1,365,000" in content
            or "1365000" in content
            or "1.82M" in content
        )
        assert has_1_365m, "R4 must cite 1.365M € labor expenditure benchmark"

    def test_r4_quantitative_facts_missed_departures_13_to_3_vs_0(self):
        content = read_sim_file(self.filename)
        # 13->3 vs 13->0 (or 13 → 3)
        has_13_to_3 = bool(
            re.search(r"13\s*(?:->|→|to)\s*3", content)
            or re.search(r"13\s*missed.*?3", content, re.IGNORECASE)
        )
        assert has_13_to_3, "R4 must explain 13->3 missed departures (software 0 €) vs 13->0 requirements"

    def test_r4_quantitative_facts_spot_spike_799_30(self):
        content = read_sim_file(self.filename)
        # 799.30 €/MWh
        has_799_30 = bool(re.search(r"799\.30", content))
        assert has_799_30, "R4 must cite the 799.30 €/MWh spot price spike"

    def test_r4_quantitative_facts_bbm_260ms(self):
        content = read_sim_file(self.filename)
        # 260ms BBM (Break-Before-Make)
        has_260ms = bool(re.search(r"260\s*ms", content, re.IGNORECASE))
        has_bbm = bool(re.search(r"BBM|Break-Before-Make", content, re.IGNORECASE))
        assert has_260ms and has_bbm, "R4 must cite the 260ms 6-step Break-Before-Make (BBM) contactor protocol"

    def test_r4_quantitative_facts_edge_islanding_1425kw(self):
        content = read_sim_file(self.filename)
        # 1,425 kW DC / 1425 kW DC
        has_1425 = bool(re.search(r"1[,.]?425\s*kW", content, re.IGNORECASE))
        assert has_1425, "R4 must cite the 1,425 kW DC edge islanding capacity"

    def test_r4_quantitative_facts_mrdt_anti_fraud(self):
        content = read_sim_file(self.filename)
        # MRDT anti-fraud / minimum required dwell time
        has_mrdt = bool(
            re.search(r"MRDT|Minimum\s+Required\s+Dwell\s+Time", content, re.IGNORECASE)
        )
        assert has_mrdt, "R4 must cite the MRDT anti-fraud dwell time gate"

    def test_r4_crisis_response_procedures(self):
        content = read_sim_file(self.filename)
        # Must cover crisis / emergency / black swan scenarios
        has_crisis_manual = bool(
            re.search(r"(?:crisis|emergency|contingency|black[- ]swan)", content, re.IGNORECASE)
        )
        assert has_crisis_manual, "R4 must contain crisis response procedures"

        # Check for coverage of typical demo day crises
        has_tech_failure = bool(
            re.search(r"(?:crash|freeze|disconnect|failure|black\s*screen)", content, re.IGNORECASE)
        )
        has_judge_challenge = bool(
            re.search(r"(?:aggressive|hostile|dispute|interrupt|out[- ]of[- ]scope)", content, re.IGNORECASE)
        )
        assert has_tech_failure, "Crisis manual must cover hardware/laptop/projector failure"
        assert has_judge_challenge, "Crisis manual must cover aggressive judge or out-of-scope question"


# ==============================================================================
# Master Integration & Mirroring Tests
# ==============================================================================
class TestMasterIntegrationAndMirroring:
    """Verifies Master README, 00_pocket_cheat_sheet.md, and docs/demo_day/ mirroring."""

    def test_master_readme_exists_and_indexes(self):
        readme_path = SIM_DIR / "README.md"
        assert readme_path.exists(), f"Master README not found at {readme_path}"
        content = readme_path.read_text(encoding="utf-8")
        assert len(content) >= 500, "Master README is too short"
        # Check index to the other files
        assert "00_pocket_cheat_sheet.md" in content, "README missing link to 00_pocket_cheat_sheet.md"
        assert "01_stage_schedule_and_setup.md" in content, "README missing link to 01_stage_schedule_and_setup.md"
        assert "02_team_roles_and_coordination.md" in content, "README missing link to 02_team_roles_and_coordination.md"
        assert "03_judge_personas_and_question_bank.md" in content, "README missing link to 03_judge_personas_and_question_bank.md"
        assert "04_structured_defense_and_crisis_manual.md" in content, "README missing link to 04_structured_defense_and_crisis_manual.md"

    def test_pocket_cheat_sheet_exists_and_concise(self):
        cheat_sheet_path = SIM_DIR / "00_pocket_cheat_sheet.md"
        assert cheat_sheet_path.exists(), f"Pocket cheat sheet not found at {cheat_sheet_path}"
        content = cheat_sheet_path.read_text(encoding="utf-8")
        assert len(content) >= 500, "Pocket cheat sheet is too short"
        # Must contain quick reference points
        has_quick_points = bool(
            re.search(r"(?:timeline|schedule|cheat\s*sheet|quick\s*reference)", content, re.IGNORECASE)
        )
        assert has_quick_points, "Pocket cheat sheet must provide on-stage quick reference reminders"

    def test_docs_mirror_complete_and_identical(self):
        assert DOCS_DIR.exists(), f"Docs mirror directory {DOCS_DIR} does not exist"
        for filename in ALL_EXPECTED_SIM_FILES:
            sim_file = SIM_DIR / filename
            doc_file = DOCS_DIR / filename
            assert sim_file.exists(), f"Source simulation file {sim_file} missing"
            assert doc_file.exists(), f"Mirrored file {doc_file} missing in docs/demo_day/"

            # Compare contents (allow normal newline normalization)
            sim_text = sim_file.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            doc_text = doc_file.read_text(encoding="utf-8").replace("\r\n", "\n").strip()
            assert sim_text == doc_text, f"Mirrored content mismatch between {sim_file} and {doc_file}"
