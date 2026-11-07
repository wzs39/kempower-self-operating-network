# TEST_INFRA: Demo Day Simulation Independent E2E Test Infrastructure

## 1. Overview & Test Architecture

This test infrastructure document formalizes the validation architecture, test methodology, and quality verification gates for the **Project Sentinel Demo Day Simulation Deliverables** at the *LahtiES Energy Tech Hackathon 2026 (Kempower Challenge)*.

```
                           ┌────────────────────────────────────────┐
                           │          ORIGINAL_REQUEST.md           │
                           │  & orchestrator_r1/PROJECT.md Specs    │
                           └──────────────────┬─────────────────────┘
                                              │
                         ┌────────────────────▼───────────────────┐
                         │      TEST_INFRA.md Specification       │
                         │ (Methodology, Invariants, Assertions)  │
                         └────────────────────┬───────────────────┘
                                              │
                        ┌─────────────────────▼─────────────────────┐
                        │   tests/test_demo_day_simulation.py       │
                        │    Independent Pytest Verification        │
                        └─────────────────────┬─────────────────────┘
                                              │
            ┌─────────────────────────────────┼─────────────────────────────────┐
            ▼                                 ▼                                 ▼
┌───────────────────────┐         ┌───────────────────────┐         ┌───────────────────────┐
│ R1: Stage Master      │         │ R2: 4-Person Roles &  │         │ R3: Judge Personas &  │
│ Schedule & Failsafe   │         │ Relay Synergy SOP     │         │ Hardcore Questions    │
│ (01_stage_schedule)   │         │ (02_team_roles)       │         │ (03_judge_personas)   │
└───────────────────────┘         └───────────────────────┘         └───────────────────────┘
            │                                 │                                 │
            └─────────────────────────────────┼─────────────────────────────────┘
                                              │
            ┌─────────────────────────────────┴─────────────────────────────────┐
            ▼                                                                   ▼
┌───────────────────────┐                                           ┌───────────────────────┐
│ R4: Structured        │                                           │ Master Integration &  │
│ Defense & Crisis      │                                           │ Mirrored Docs Tree    │
│ (04_structured_defense│                                           │ (README, 00_pocket,   │
│  & crisis manual)     │                                           │  docs/demo_day/*)     │
└───────────────────────┘                                           └───────────────────────┘
```

The test suite (`tests/test_demo_day_simulation.py`) operates as a completely independent, requirement-driven audit barrier. It verifies structural completeness, semantic validity, quantitative fidelity, and cross-document coherence without circular assumptions or facade shortcuts.

---

## 2. Test Methodology & Authoritative Invariant Derivation

### 2.1 Authoritative Specification Sources
Every test assertion is directly derived from primary hackathon contracts:
1. `Kempower-challenge-brief.pdf`: Strict 10-minute presentation mandate, 2029 customer story, one-page agreement, 5-dimensional evaluation rubric.
2. `Kempower_LahtiES_hackathon_kickoff_2026-11-05.pptx` (Mats Mattsson keynote): 21 FTE baseline (€1,365,000/yr @ €65,000/yr), 10-minute pitch stage cutoff.
3. `ORIGINAL_REQUEST.md`: R1 stage timeline, R2 4-person roles (Speaker A, Speaker B, Member C, Member D), R3 >= 3 judge personas & >= 12 hardcore questions, R4 structured 3-part answers and crisis response procedures.
4. `PROJECT.md` (orchestrator_r1): 11 Features (F1–F11), 5 Milestones (M1–M5), Interface contracts (Slide timestamps, role routing, physical constraints).
5. Repository Ground Truth: `One_Page_SLA_Specification.md` (MRDT §5.1 gate), `docs/assumptions_and_additions.md` (Inverter loss $\eta=0.955$, 1,425 kW DC = 1,492.15 kW AC $\le$ 1,500 kW transformer), `src/core/self_healing.py` (260ms BBM 6-step timing).

### 2.2 Anti-Facade & Adversarial Rules
1. **Physical Existence & Non-Trivial Volume**: Every required deliverable file must exist, be readable, and contain substantive content (minimum byte size and structured markdown headings).
2. **Exact Numerical Invariants**: Tests programmatically enforce exact regex matching on critical numbers (e.g. `21 FTE`, `1.365M €` / `1,365,000`, `13->3` / `13 → 3`, `799.30`, `260ms` / `260 ms`, `1,425 kW` / `1425 kW`, `MRDT`).
3. **Failsafe Triad Validation**: Tests confirm all three offline backup tiers are documented with operational cutover rules:
   - Tier 1: Streamlit interactive cockpit (`app.py`)
   - Tier 2: Deterministic CLI verification runner (`verify_all.py`)
   - Tier 3: Pre-rendered backup video (`presentation_demo.mp4`)
4. **Mirror Parity Check**: Tests confirm exact byte-level or line-level parity between `demo_day_simulation/` and `docs/demo_day/`.

---

## 3. Feature Inventory & Test Coverage Matrix

| Feature ID | Feature Name | Target Deliverable | Test Class / Functions in Pytest |
|---|---|---|---|
| **F1** | Stage Master Schedule & Timeline | `01_stage_schedule_and_setup.md` | `TestR1StageScheduleAndSetup::test_pitch_total_duration_600s`<br>`TestR1StageScheduleAndSetup::test_qa_duration_3_to_5_min`<br>`TestR1StageScheduleAndSetup::test_live_demo_slot_120s` |
| **F2** | Stage Setup & Failsafe Triad Protocol | `01_stage_schedule_and_setup.md` | `TestR1StageScheduleAndSetup::test_stage_setup_and_diagram`<br>`TestR1StageScheduleAndSetup::test_failsafe_triad_components` |
| **F3** | 4-Person Role Division & Positioning | `02_team_roles_and_coordination.md` | `TestR2TeamRolesAndCoordination::test_four_member_role_definitions`<br>`TestR2TeamRolesAndCoordination::test_physical_positioning_and_presence` |
| **F4** | Dual-Speaker Relay Script & Transitions | `02_team_roles_and_coordination.md` | `TestR2TeamRolesAndCoordination::test_verbatim_speaker_transitions` |
| **F5** | Member C & D Console SOP & Triggers | `02_team_roles_and_coordination.md` | `TestR2TeamRolesAndCoordination::test_member_c_console_sop_and_hotkeys`<br>`TestR2TeamRolesAndCoordination::test_emergency_cutover_triggers` |
| **F6** | Tripartite Judge Persona Profiles | `03_judge_personas_and_question_bank.md` | `TestR3JudgePersonasAndQuestions::test_judge_personas_presence`<br>`TestR3JudgePersonasAndQuestions::test_judge_perspectives_and_scoring_focus` |
| **F7** | Hardcore Question Bank (>= 12 Questions) | `03_judge_personas_and_question_bank.md` | `TestR3JudgePersonasAndQuestions::test_question_bank_count_and_structure`<br>`TestR3JudgePersonasAndQuestions::test_question_persona_and_category_mapping` |
| **F8** | Structured Defense Answers & Proofs | `04_structured_defense_and_crisis_manual.md` | `TestR4StructuredDefenseAndCrisis::test_three_part_structured_answers`<br>`TestR4StructuredDefenseAndCrisis::test_quantitative_facts_citations` |
| **F9** | Team Synergy & Defense Handoff Rules | `04_structured_defense_and_crisis_manual.md` | `TestR4StructuredDefenseAndCrisis::test_team_defense_handoff_rules` |
| **F10** | Live Crisis Emergency Response Manual | `04_structured_defense_and_crisis_manual.md` | `TestR4StructuredDefenseAndCrisis::test_crisis_response_protocols` |
| **F11** | Master Integration, Pocket Cards & Mirror | `README.md`, `00_pocket_cheat_sheet.md`, `docs/demo_day/*` | `TestMasterIntegrationAndMirroring::test_master_readme_exists_and_indexes`<br>`TestMasterIntegrationAndMirroring::test_pocket_cheat_sheet_exists`<br>`TestMasterIntegrationAndMirroring::test_docs_mirror_complete_and_identical` |

---

## 4. Requirement Verification Rules

### 4.1 Requirement 1 (R1): Stage Schedule & Setup
- **Rule R1.1**: Total spoken pitch duration must explicitly equal 10 minutes (600 seconds), respecting the hard cutoff of LahtiES / Kempower challenge brief.
- **Rule R1.2**: Q&A schedule must explicitly define a 3–5 minute defense window (180–300 seconds), bringing total stage presence to 13–15 minutes.
- **Rule R1.3**: The Live Demo segment must be allotted a dedicated 120-second (2:00) slot positioned within the 5:00 to 7:00 window (Slides P7–P8).
- **Rule R1.4**: Stage setup must include an ASCII stage diagram positioning 4 members (Speakers A & B at front lectern/stage center; Member C at the tech console laptop; Member D on standing standby).
- **Rule R1.5**: The Failsafe Triad must be explicitly documented with:
  1. Primary: Streamlit interactive dashboard (`app.py`)
  2. Fallback 1: Deterministic CLI runner (`verify_all.py`)
  3. Fallback 2: 1080p pre-rendered video (`presentation_demo.mp4` / `Kempower_video*.mp4`)
  4. Hard trigger: Cutover decision rule if latency exceeds 2.5s or app freezes.

### 4.2 Requirement 2 (R2): 4-Person Roles & Synergy
- **Rule R2.1**: Exactly 4 distinct roles must be defined with unambiguous boundaries:
  - **Speaker A**: Business pain points, commercial viability, AEaaS model, 2029 customer story (Pekka Virtanen), closing call to action.
  - **Speaker B**: Technical architecture, 3-tier decoupling (L1/L2/L3), Kempower DPR fidelity, 25 kW modular matrix, physical grid invariants.
  - **Member C**: Live Console pilot, Streamlit scenario steering, failure injection execution, A/V failsafe switching.
  - **Member D**: Deep technical defense, mathematical formulations, continuous slack variables, edge islanding proof, One-Page SLA legal/contract terms.
- **Rule R2.2**: Verbatim dual-speaker handoff scripts must be provided:
  - Speaker A $\to$ Speaker B handoff (Business to Technical Architecture).
  - Speaker B $\to$ Member C handoff (Technical Architecture to Live Console Demo).
  - Speaker B $\to$ Speaker A handoff (Live Demo back to Commercial AEaaS & 2029 Story).
- **Rule R2.3**: Member C Console SOP must provide step-by-step hotkeys, scenario injection sequence (S1 $\to$ S2 $\to$ S3 $\to$ S4 $\to$ S5), and emergency video cutover protocol.

### 4.3 Requirement 3 (R3): Judge Personas & Question Bank
- **Rule R3.1**: At least 3 distinct judge personas must be profiled:
  1. *Technical Architect / Power Electronics Expert* (Mats Mattsson / Panu Vartiainen persona: focused on DPR, 25kW modules, BBM 260ms, inverter losses, offline edge resilience).
  2. *Commercial / Venture Capital Investor* (LahtiES / VC persona: focused on 21 FTE savings, €1.365M/yr, 2-month payback, CaaS pricing, defensibility).
  3. *Kempower Flagship Challenge Judge* (Lead Evaluator persona: focused on rule compliance, 0 edited CSVs, equipment_costs.csv fidelity, honest technician retention).
- **Rule R3.2**: The question bank must contain at least 12 distinct hardcore questions (target 14), each with:
  - Distinct Question Identifier (`Q01`, `Q02`, etc.)
  - Target Persona / Question Category
  - Underlying Judge Concern & Evaluation Dimension

### 4.4 Requirement 4 (R4): Structured Defense & Crisis Response
- **Rule R4.1**: Every question in the bank must have a structured 3-part defense answer:
  1. *Direct Bottom-Line Assertion* (15-second executive answer).
  2. *Empirical & Mathematical Proof* (exact citation of data, equations, benchmarks).
  3. *Commercial or Operational Takeaway* (SLA term, contract guarantee, edge resilience).
- **Rule R4.2**: Quantitative facts must be accurately cited across the defense answers:
  - `21 FTE` manual labor keynote baseline (€1,365,000 / €1.365M / yr @ €65k/yr) vs 20.76 FTE statutory baseline (€1.82M/yr @ €45/h).
  - `1.365M €` (or `€1,365,000`) annual operational labor expenditure.
  - `13->3 vs 13->0` (Sentinel 0 € CAPEX software triage cuts missed departures from 13 to 3; reaching 0 requires either €324,000 dual-gun expansion which alone leaves 8 missed without busbar tie, or Tier 5 hardware expansion).
  - `799.30 €/MWh` (S4 synthetic spot tariff price spike handled by continuous SoC slack variable $z \in [0, 1]$ in HiGHS MILP).
  - `260ms BBM` (Break-Before-Make contactor relay 6-step switching protocol < 500 ms).
  - `1,425 kW DC` (S3 highway hub edge islanding load; $P_{AC} = 1425 / 0.955 = 1492.15\text{ kW} \le 1500\text{ kW}$ transformer limit).
  - `MRDT anti-fraud` (Minimum Required Dwell Time gate in One_Page_SLA_Specification.md §5.1 waives liquidated damages if dwell time is shorter than physical energy requirement).
- **Rule R4.3**: Crisis response procedures must cover at least 5 black-swan stage emergencies:
  1. Live Demo laptop crash / freeze
  2. Projector disconnection / resolution distortion
  3. Hostile / interrupting judge
  4. Timer signal alert (1 minute left or 30 seconds left)
  5. Question completely outside hackathon dataset scope

### 4.5 Master Integration & Mirroring
- **Rule M.1**: `demo_day_simulation/README.md` must exist and provide a master directory index, reading roadmap, and stage checklist.
- **Rule M.2**: `demo_day_simulation/00_pocket_cheat_sheet.md` must exist as a concise quick-reference card for on-stage recall.
- **Rule M.3**: Every file in `demo_day_simulation/` must have an identical mirror copy in `docs/demo_day/`.

---

## 5. Test Execution Protocol

```powershell
# Run the complete Demo Day Simulation E2E test suite
pytest tests/test_demo_day_simulation.py -v --tb=short

# Run with specific requirement focus
pytest tests/test_demo_day_simulation.py -k "TestR1" -v
pytest tests/test_demo_day_simulation.py -k "TestR2" -v
pytest tests/test_demo_day_simulation.py -k "TestR3" -v
pytest tests/test_demo_day_simulation.py -k "TestR4" -v
pytest tests/test_demo_day_simulation.py -k "TestMaster" -v
```
