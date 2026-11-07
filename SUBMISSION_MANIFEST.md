# Project Sentinel · Official Submission Manifest
### Cryptographic Package Verification & Component Functional Index
*Kempower Challenge · LahtiES Energy Tech Hackathon 2026 (LUT University Lahti / CrazyTown)*

---
- **Package Archive**: `submission.zip`
- **Total Deliverable Files**: 122
- **Total Uncompressed Volume**: 1183.83 MB (1,241,337,742 bytes)
- **Zero-CJK Rule Compliance**: 100% Pure Professional English Verified (`[\u4e00-\u9fff]` match count = 0)
- **Deterministic Verification**: `python code/verify_all.py` (29 checks passing in < 0.5s)
- **Automated Test Coverage**: 462 Pytest + 106 E2E = 568 total automated tests (100% pass rate)
---

## Deliverable Summary by Category

- **`root/`**: 1 files (23.78 KB)
- **`code/`**: 82 files (979.06 KB)
- **`docs/`**: 25 files (375.55 KB)
- **`presentation/`**: 8 files (136.72 MB)
- **`videos/`**: 6 files (1045.77 MB)

---

## Complete Cryptographic Inventory

| # | Category | Relative File Path | Size | SHA-256 Checksum | Functional Description |
|:---:|:---:|:---|:---:|:---|:---|
| 1 | `code` | `code/app.py` | 32.14 KB | `a1d9010f7d722b6c45cd1a50c102f5e211ed483a7338c69540ab49adbe136bd8` | Interactive 4-View Streamlit Command Center and Executive Cockpit |
| 2 | `code` | `code/e2e_tests/__init__.py` | 90 B | `de00142fb1e50bcd4418d8b2c7263ae5e82720dd1ab086172c34814e49aa5979` | End-to-End opaque-box testing test suite component |
| 3 | `code` | `code/e2e_tests/common.py` | 4.82 KB | `828699c80d91ea344d6ba0ad9b8c53b2a0a18a20d24cac28e8e8e1404dc09730` | End-to-End opaque-box testing test suite component |
| 4 | `code` | `code/e2e_tests/test_runner.py` | 5.79 KB | `1dcf1cb66c6df0fb0eaa57333b1dae9181175aae632b822893991dc98303edee` | End-to-End opaque-box testing test suite component |
| 5 | `code` | `code/e2e_tests/tier1_feature_coverage.py` | 20.12 KB | `8223a3139b255427e58ffd605b7125fcd90c61f7e3b44b8eb693fbc1977a423d` | End-to-End opaque-box testing test suite component |
| 6 | `code` | `code/e2e_tests/tier2_boundary_corner.py` | 13.35 KB | `19f07c20f80a3eafeaaabace23545f3bf87cfb070e5cb37780ea0dbe695ae82d` | End-to-End opaque-box testing test suite component |
| 7 | `code` | `code/e2e_tests/tier3_cross_feature.py` | 6.44 KB | `4542d7bc49d5805f984319d350943576be5b9324e8400d20fbc7fc8e8088d4d5` | End-to-End opaque-box testing test suite component |
| 8 | `code` | `code/e2e_tests/tier4_real_world_scenario.py` | 8.69 KB | `37576eb3980aa71881606eab7b3668d5198a511a068d38f2b2dcb820cc2748b4` | End-to-End opaque-box testing test suite component |
| 9 | `code` | `code/pytest.ini` | 42 B | `b160d82f7811555051f8966d8e02750a985227c1d022208c784e606946f2eada` | Pytest configuration specifying test paths and options |
| 10 | `code` | `code/requirements.txt` | 488 B | `31e6ed5500590b635780438f395a0d0c677a5792be567f90048d2d853273ce9f` | Python dependencies and exact package versions |
| 11 | `code` | `code/run_s1.py` | 10.13 KB | `e0fef5a26ad049e0890b3d6331705eb13aa1a75d55c1a2f85eb50015599fb430` | S1 Bus Depot overnight simulation comparing baseline vs zero-human autonomy |
| 12 | `code` | `code/src/__init__.py` | 64 B | `1abc659bc8548aaa23a37b1b161f89580478d84e044079e58d9b346ae0fc8dac` | Core package initializer |
| 13 | `code` | `code/src/commercial/__init__.py` | 253 B | `92bf037063f5bc20ddfdb80cfd5865e762ef11c4638f9bc1e1cb2325dcb4c62c` | Commercial subpackage initializer |
| 14 | `code` | `code/src/commercial/roi_analyzer.py` | 10.30 KB | `a3d8f7a36b1d8de4156579e8b34406bf33d8a838867e68f88496d008ffb55f70` | 20.76 FTE labor accounting, CAPEX/OPEX payback, and financial models |
| 15 | `code` | `code/src/commercial/sensitivity_analyzer.py` | 10.88 KB | `ed1f8f98fbaffe9d90c5f8d7e24ea04b33ba9689397870e63fed22c44319aae9` | Multi-axis sensitivity analysis and pure Python NPV/IRR financial model |
| 16 | `code` | `code/src/commercial/settlement_clearing.py` | 18.15 KB | `515f22d2f0ebf93ea465a86190444aa14a0575d6f43e58f45bc8ceb5bfd2fee6` | B2B monthly settlement engine and automated invoice clearing |
| 17 | `code` | `code/src/commercial/sla_calculator.py` | 4.41 KB | `176b755b5e9395ba85653ba7bf7546c483c8c9dc2dfa4cddcd2544ffdbffdda1` | Outcome-based SLA tiered deductions and MRDT anti-moral-hazard calculator |
| 18 | `code` | `code/src/core/__init__.py` | 1.99 KB | `3ec1b6a99e8e63783cfaae64afcc4ce63bd66900ca0f93331869b49a490adcc4` | Core architecture subpackage initializer |
| 19 | `code` | `code/src/core/anti_fraud.py` | 9.54 KB | `17f392630087311f25aae723ab44f45231cbe81d861c91a2f870637ecac78174` | Anti-phantom replug detector and MRDT electrical fingerprint gate |
| 20 | `code` | `code/src/core/dpr_matrix.py` | 29.74 KB | `139fffd4616829f39f49a4128ead4cb14168b20e9e0cef1359b1dc3899802648` | Kempower 25kW Dynamic Power Routing (DPR) matrix and BBM contactor FSM |
| 21 | `code` | `code/src/core/mpc_optimizer.py` | 21.21 KB | `b0a4daee6238ab1d0aea01a9abc70070b328ba7f79129c1ec6901536f284c570` | 15-minute rolling horizon SciPy HiGHS MILP optimizer with continuous SoC slack |
| 22 | `code` | `code/src/core/protocols.py` | 40.56 KB | `476f7ef80ba7ea7546a50fbe7a481cb06841301b616f1a44e375544c0d5a5a70` | OCPP 2.0.1 Smart Charging profiles and ISO 15118-2/20 Plug & Charge TLS 1.3 stack |
| 23 | `code` | `code/src/core/self_healing.py` | 40.85 KB | `1cfd3757821f355631abbd793ff61b1c40a47aa2eae1b37c1cce166e3699d0aa` | 199-minute predictive thermal PdM, 260ms BBM sequencer, and offline edge islanding |
| 24 | `code` | `code/src/core/virtual_replug.py` | 25.39 KB | `a7fb6e1f558e6325d89d1b05c71b68f9ada2966941c196015af15f1c3471f25a` | S1 Strategy A (0 EUR software) and Strategy B (324k EUR hardware) evaluation |
| 25 | `code` | `code/src/edf_packer.py` | 10.87 KB | `2c77ed8343639b39f75386842d1191d6972255d7ea24c2b7b008a6abe8af71c2` | Continuous Earliest Deadline First (EDF) discrete charging simulator |
| 26 | `code` | `code/src/sim/__init__.py` | 265 B | `879039c8c27764d2aa6b76ed9c796c608e6d45ab4eadd224b6a2d59349d20e87` | Simulation subpackage initializer |
| 27 | `code` | `code/src/sim/data_loader.py` | 4.82 KB | `89cacb4f2df1397b1cb9b3088ad55d59c9d314fe5b5912de5a6c10d9052fc0bf` | Official 45 CSV dataset loader and SHA-256 hash verifier |
| 28 | `code` | `code/src/sim/discrete_sim.py` | 24.13 KB | `ead22a7ccb56c684923ebca0b7c69f7da72902136bc22a8c0dba8161831b4388` | High-fidelity minute-by-minute discrete event charging simulator |
| 29 | `code` | `code/src/sim/fault_replays.py` | 24.68 KB | `e38becc1669acbbc35f499822b9ef2f2790f92dce1dbd442a94261ff874b8022` | Multi-station fault injection and hardware degradation harnesses |
| 30 | `code` | `code/src/sim/night_replay.py` | 15.50 KB | `473d1b8de78046cec9b1b8911e7284f6f2e068e2e2bc830fe762164e2b912aaa` | S1 overnight fleet charging simulation harness |
| 31 | `code` | `code/src/sim/outage_replay.py` | 9.24 KB | `57e60806400e5e2d1c0033994a29b6e87f8026830db197a840c10d9268cfe6ad` | S3 cellular WAN outage and autonomous edge islanding harness |
| 32 | `code` | `code/src/sim/scenario_engine.py` | 16.22 KB | `1c12c39430a5c7f74444f7425bae10066d34c3efc42cdd50f9cf69ec121632d8` | Master closed-loop scenario simulation and benchmark orchestrator |
| 33 | `code` | `code/src/ui/__init__.py` | 84 B | `81d9ba7d47beb44af1384215a904f7fdbbcfb151717582a93e637f75241d585b` | UI rendering subpackage initializer |
| 34 | `code` | `code/src/ui/replay_scene.py` | 22.61 KB | `bd6a0fde23441b7f4af13c623e98fcf723d230999833a8a6d11dcfbe8c35c1f8` | Streamlit rendering helpers and interactive UI components |
| 35 | `code` | `code/src/utils/__init__.py` | 211 B | `f96583f042dbc2fc7cab4bf9558fb43c4bc10e2208f569547847d79bc385b0fa` | Utilities subpackage initializer |
| 36 | `code` | `code/src/utils/paths.py` | 1.57 KB | `7d219ac723250015622e02d913447993ba3df3de36763fd6b8ff82463e924abb` | Cross-platform deterministic path resolver for challenge datasets |
| 37 | `code` | `code/tests/analyze_scenario_day.py` | 3.19 KB | `9b8d5c9b34b6655cd2adb199ec55b30d57e8ab9af4e36257036968db10641d8e` | Pytest automated unit/integration test module |
| 38 | `code` | `code/tests/check_bess.py` | 554 B | `6c6f5f1532f1b68f4f75b03f32ef62638636112ca56f9153d9654ee289acf208` | Pytest automated unit/integration test module |
| 39 | `code` | `code/tests/check_d1_9.py` | 374 B | `415358dd9fef8a0d4e93348461592a2583bbc68d8d7f887a49115dd0f09c412d` | Pytest automated unit/integration test module |
| 40 | `code` | `code/tests/check_d1_later.py` | 878 B | `bda9828a9aee79bb65f99ca0598f971c7fc6ca4e148a79ea897a7f7b4382eb24` | Pytest automated unit/integration test module |
| 41 | `code` | `code/tests/check_s1_power.py` | 704 B | `cb16ddba8d133dedf79ae9942d3770f4f0e1b06e1943332ab61b72f35b8615fe` | Pytest automated unit/integration test module |
| 42 | `code` | `code/tests/check_s3_outage.py` | 875 B | `91f87cf90aa8b92cced44c86f0f348c90ad324fb2e98a8b14244bde5d2994ecf` | Pytest automated unit/integration test module |
| 43 | `code` | `code/tests/check_t01_t04.py` | 404 B | `e3ed4d5f76d62a9bb5dc632d71d9b6baf2ff3b6f77b814be4a803f9e0f8cc6c4` | Pytest automated unit/integration test module |
| 44 | `code` | `code/tests/conftest.py` | 157 B | `f1efac1390e32ed1e95fc156828ccb5ae89afd49a4e3efa72ae77ad3a74eaa3c` | Pytest automated unit/integration test module |
| 45 | `code` | `code/tests/edf_simulation.py` | 3.39 KB | `6b1952c1a6548386e8446a7bb7e35bf73f94def94605439956486d86e0af697f` | Pytest automated unit/integration test module |
| 46 | `code` | `code/tests/inspect_cols.py` | 454 B | `8be91976946d4e3a19421fe3f516d220de816d8b8ea2980ab011533a9c3a7d93` | Pytest automated unit/integration test module |
| 47 | `code` | `code/tests/inspect_dataset.py` | 955 B | `4d3442437c17b4eb003a322ca67f54248de6fd9cbee7722fe70381d76da17f39` | Pytest automated unit/integration test module |
| 48 | `code` | `code/tests/inspect_s1_telemetry.py` | 1.10 KB | `f06cdaabdd4f8db9305f2b164e69502d3c6681f29ea5e34e83658bb639cf4c36` | Pytest automated unit/integration test module |
| 49 | `code` | `code/tests/query_scenario_data.py` | 1.53 KB | `a5c848437b5e132665655201603f6ef306e6cd9e20b83f56881fa81090eff404` | Pytest automated unit/integration test module |
| 50 | `code` | `code/tests/simulate_s2_curtailment.py` | 2.75 KB | `b88a98fb37592964b92d3802faa6eea4bfa384ee47ae433200bb5eeb6b0db0e7` | Pytest automated unit/integration test module |
| 51 | `code` | `code/tests/test_adversarial_discrete_sim_thermal.py` | 24.76 KB | `123976b1868da5328a43f6cbfbe09d882ee28916eb93f0d7790726c96abbde80` | Pytest automated unit/integration test module |
| 52 | `code` | `code/tests/test_adversarial_m1.py` | 19.24 KB | `3d22b03e00023d1c208f3dd876876b84fc6118681d9d5d1d48269a4f9a44417b` | Pytest automated unit/integration test module |
| 53 | `code` | `code/tests/test_anti_fraud_replug.py` | 5.19 KB | `93b485cc6dfc88184f95686be1c720bbc648b906cde86a58327d30b11a9172b8` | Pytest automated unit/integration test module |
| 54 | `code` | `code/tests/test_commercial_settlement.py` | 15.60 KB | `4c73d7bdd9fec16867f1151098a993c9d88f0dae526244f9e5d35854a92702a1` | Pytest automated unit/integration test module |
| 55 | `code` | `code/tests/test_dashboard_runtime_stress.py` | 14.51 KB | `ce3f40c9a5c25b6d60c1baff3dd868d248f0af496e4f2df43b2617ba51fab859` | Pytest automated unit/integration test module |
| 56 | `code` | `code/tests/test_demo_day_simulation.py` | 19.28 KB | `bbb4afbd86d92b222b1ef4cd8ed58a2361a728418ccaf6f74254b85e83798827` | Pytest automated unit/integration test module |
| 57 | `code` | `code/tests/test_discrete_sim_engine.py` | 8.00 KB | `c6012da71b0f8dc933557e9447236a87c15985978adf3990edd4c117b93c9d0f` | Pytest automated unit/integration test module |
| 58 | `code` | `code/tests/test_dpr_stress_adversarial.py` | 19.89 KB | `666effd97188e1f1534e94ff1fd7e1fae43c908e63876cf6be4af6bb3eefc9dc` | Pytest automated unit/integration test module |
| 59 | `code` | `code/tests/test_e2e_suite.py` | 45.75 KB | `10b7ad1b2b5c69f94687a08ac158bf5f05d83a840fca2b9329f78e407057bfe6` | Pytest automated unit/integration test module |
| 60 | `code` | `code/tests/test_gate2_empirical_verification.py` | 6.97 KB | `c4a1e8f11cc9101874febb8a21b534a47426d44f0a1784ca344f7ad67f43f9f0` | Pytest automated unit/integration test module |
| 61 | `code` | `code/tests/test_github_issue2_29items.py` | 14.33 KB | `243ef14cb284c97473a0a12f0ce3a5933ea2a6688720558f0c5c12ce39662338` | Pytest automated unit/integration test module |
| 62 | `code` | `code/tests/test_m1_adversarial_probe.py` | 21.96 KB | `879b0152b52209f98b372a0ea5860baa4fde47c4081f2d140e85ac502cb7dc7f` | Pytest automated unit/integration test module |
| 63 | `code` | `code/tests/test_m1_remediation.py` | 13.75 KB | `c408e705ba07c7f3f8aa9998e9bb730a03ac7e614b1dda4560047de55c26cef3` | Pytest automated unit/integration test module |
| 64 | `code` | `code/tests/test_m2_challenger_empirical.py` | 21.39 KB | `3daf44cf881c14f7532e2966fdd5e0e1592eaf106bc24925d6ee0317370ba66c` | Pytest automated unit/integration test module |
| 65 | `code` | `code/tests/test_m2_hardware_edge_stress.py` | 17.97 KB | `f7118be5fb53d1be6ab324d9b968d7529447de3c3ee1584ab6059add98734be5` | Pytest automated unit/integration test module |
| 66 | `code` | `code/tests/test_m2_hardware_self_healing.py` | 16.38 KB | `ab2808b81adaad14d89ae56bd5c73eb20ad6ac86660fc9ad8835fe72a7e7b9c4` | Pytest automated unit/integration test module |
| 67 | `code` | `code/tests/test_m2_protocols_anti_fraud_adversarial.py` | 19.76 KB | `0370eeef177b3a24cd67b85513649d114f1d5efbe655ea979ab1dcd073b94ce1` | Pytest automated unit/integration test module |
| 68 | `code` | `code/tests/test_m3_adversarial_stress.py` | 16.52 KB | `218df08d523ca666d4437d6e0351bd58226ca2b803c93be0fa53eaf487ce2637` | Pytest automated unit/integration test module |
| 69 | `code` | `code/tests/test_mpc_math_fixes.py` | 5.64 KB | `a721eaf0bb90da158a2e37d91ae2c3a0fe0cf1ae8f14542ade3749bafd0e948d` | Pytest automated unit/integration test module |
| 70 | `code` | `code/tests/test_protocols_ocpp_iso.py` | 14.93 KB | `dbdddd0672d752b41e1f95372a68280487e17c68cf06662dbc17df20bfa276d2` | Pytest automated unit/integration test module |
| 71 | `code` | `code/tests/test_remediated_sla.py` | 5.71 KB | `b304876d5bd0d4742c288319e519639df3a5b233d8c479d40eea2e854c26ac73` | Pytest automated unit/integration test module |
| 72 | `code` | `code/tests/test_sla_edge_cases.py` | 3.77 KB | `92732951bf0c93e53350d4c8b28e4b16c2b77b5ca3c960e9cc729a5c20047e22` | Pytest automated unit/integration test module |
| 73 | `code` | `code/tests/test_tier5_commercial_adversarial.py` | 42.05 KB | `c3f3871bf19d77315e2a5ab9d9dc3393edd488f313f152a457fd84dd2125a237` | Pytest automated unit/integration test module |
| 74 | `code` | `code/tests/test_tier5_core_adversarial.py` | 43.93 KB | `a0838458f9ae65f9184428aea32a842b0b649f54bd92a1e47ebcfabe8e050135` | Pytest automated unit/integration test module |
| 75 | `code` | `code/tests/verify_csv_inventory.py` | 2.94 KB | `4c97df1cf3dd36ae7cb8aac3c9ea9b3aa70d2df28b612dc0570f471b94b6feb3` | Pytest automated unit/integration test module |
| 76 | `code` | `code/tests/verify_empirical_claims.py` | 7.84 KB | `c22ca88a0dd01ca42b8601e615e75a3f3e9b838177b31cb7083d7868e3d05c26` | Pytest automated unit/integration test module |
| 77 | `code` | `code/tools/check_demo_artifacts.py` | 3.12 KB | `7f35cdc91661faece79eaf71b2536df05328321d7a9bf1bb9d012d9fbd9b82d5` | Engineering verification and artifact analysis utility |
| 78 | `code` | `code/tools/cjk_audit.py` | 1.41 KB | `3ba5b8cd1979b16a15df80afa705f19e34a5ea8184e380708b3b822b9de0b286` | Engineering verification and artifact analysis utility |
| 79 | `code` | `code/tools/export_deck_ledger.py` | 39.59 KB | `a20260946a57c8857add3b5e3d5b70ef580cc7271223e5b67577c4329cc99378` | Engineering verification and artifact analysis utility |
| 80 | `code` | `code/tools/s1_multicabinet_sim.py` | 12.12 KB | `ea9c9c403c849dd14cecfb3ea9435c29120477dff24cd7ff12c50c9a67584b01` | Engineering verification and artifact analysis utility |
| 81 | `code` | `code/tools/stage_submission.py` | 5.21 KB | `43d403b013af388893cfb884e74e3b72363d4f62c9dac016a00603bb6dd6560b` | Engineering verification and artifact analysis utility |
| 82 | `code` | `code/verify_all.py` | 6.76 KB | `f8d05f4dd439d48773ad4aafdd434650a45d4435bf6136fc9f549285a01368c4` | Deterministic CLI verifier executing 29 validation checks across 45 CSVs in < 0.5s |
| 83 | `docs` | `docs/HACKATHON.md` | 3.72 KB | `be16e96cf571ffabb8f728d489dc26d55ef9e668bc9dca41c8b2b0b971b74fdb` | Challenge alignment, competition boundaries, and judging rules reference |
| 84 | `docs` | `docs/One_Page_SLA_Specification.md` | 22.20 KB | `65fe05c7e3269eea74359e9f966929b515a6be84c3952960b9148d5ac5f3f693` | Comprehensive outcome-based CaaS SLA specification and 2029 customer story |
| 85 | `docs` | `docs/PROJECT.md` | 17.15 KB | `1804e340c355504f911c24279dc490bceca22cc65617baaee3d39d988c81de14` | Single source of engineering truth and system technical blueprint |
| 86 | `docs` | `docs/PROJECT_AUDIT_REPORT.md` | 7.17 KB | `9ee879203249404d8ac5b1c49ea2bee0ad0fb9a2bb428c7c92e4219de829fddf` | Forensic audit report verifying all 5 competition evaluation dimensions |
| 87 | `docs` | `docs/ZERO_HUMAN_DESIGN.md` | 18.70 KB | `4a1df3da519f8b69c763474128e7fccb0bae965ed1d5244bca0efcc9e7ecfc03` | Comprehensive zero-human autonomous architecture design specification |
| 88 | `docs` | `docs/assumptions_and_additions.md` | 11.67 KB | `b51226c0eabfe14f722e204828169e3558e1a40b4ba13d6e06afa4d46c79f2bf` | Transparent dictionary of 20 engineering assumptions and introduced artifacts |
| 89 | `docs` | `docs/attribution_matrix.md` | 13.94 KB | `c589f83d68fa7cfcada147a9c1c7e4f8373d318bd45d1b1ac20c926308096e76` | 16-cell causal attribution matrix for S1, S2, and S5 scenarios |
| 90 | `docs` | `docs/demo_day/00_pocket_cheat_sheet.md` | 8.88 KB | `8c1e41f37a71acf3d5591d7c2eaed0d7317803b670bfe04af8069a3ae2fe5842` | On-stage quick-reference card, timeline checkpoints, and golden quotes |
| 91 | `docs` | `docs/demo_day/01_stage_schedule_and_setup.md` | 47.69 KB | `94bd789edce7e64106fb7bb345c0c8998badab46596fe86a71d41b68fe388921` | Minute-by-minute presentation timeline and dual-laptop hardware setup |
| 92 | `docs` | `docs/demo_day/02_team_roles_and_coordination.md` | 32.92 KB | `35a0133c5902c568cfdc30d30848179cceda5941d2893ddbc35d69408e105a22` | 4-person role matrix, verbatim speaker handoff cues, and console SOP |
| 93 | `docs` | `docs/demo_day/03_judge_personas_and_question_bank.md` | 31.10 KB | `fbe274474571ad072923fd77e3f4a09f7aaf00346c6cc2676b9ed83988f2747e` | 3 juror profiles and 14 representative hardcore questions |
| 94 | `docs` | `docs/demo_day/04_structured_defense_and_crisis_manual.md` | 48.96 KB | `bfde4d27f643c05125d413f31e3906192b155520a32f5ed68c65403856f8f02a` | 3-part structured defense responses and emergency crisis procedures |
| 95 | `docs` | `docs/demo_day/05_live_demo_operational_sop.md` | 12.56 KB | `d80535b094e780b7ba1b0c5dfe0cf04129f645454910d2c57b8e0079a1712809` | Live console operator step-by-step Standard Operating Procedure |
| 96 | `docs` | `docs/demo_day/06_code_proof_and_authenticity_guide.md` | 12.18 KB | `1aafcb5d859dae4de823a21f10d3a0cfdb3a0b0850c8cb3518553b4406169aed` | Code-level proof walkthrough and data authenticity verification guide |
| 97 | `docs` | `docs/demo_day/README.md` | 16.53 KB | `14e87f49a9ca2ea5871ea0a355b6758117120c670b1fe56b1c8cc3f36b2d26ae` | Demo Day operational handbook master index |
| 98 | `docs` | `docs/energy_impact.md` | 20.66 KB | `deffb9be6a910a30dc7f277e1bca728dcd253bb1a15aa43f18e2ce45407842c5` | Station-by-station energy ledger and 95-site network-wide grid impact proof |
| 99 | `docs` | `docs/hackathon/BRIEF.md` | 6.18 KB | `571c27eb8738cb0b1a6d1ce3775c6ad1b413acb34473c4e1d7603bfadbf47f27` | Official Kempower challenge brief transcription |
| 100 | `docs` | `docs/hackathon/BUILD_PLAN.md` | 2.31 KB | `11af160f1836588db876ec8d590c705f032476be909dd7dd0afbc4298006ad02` | Engineering build and delivery milestone schedule |
| 101 | `docs` | `docs/hackathon/DECISIONS.md` | 3.41 KB | `db08a4e7f78a9724bc30a86188fabc432d4bc919ac443858227a198c29d6f967` | Architectural decisions and rationale log |
| 102 | `docs` | `docs/hackathon/DEMO_SCRIPT.md` | 5.61 KB | `4b3979ec02a20e050d04812cc9ab0f6ece8b85fac0e1348e88ebbfcf12658022` | 120-second live demonstration script |
| 103 | `docs` | `docs/hackathon/JUDGING.md` | 5.51 KB | `c6b827e9d0665a249fc563c9e00e0c2a3153374fea6244b8d4d8c2ecc75c2d98` | Official evaluation criteria, weights, and scoring rubrics |
| 104 | `docs` | `docs/hackathon/RULES.md` | 3.51 KB | `76170f3d29259f6c0232486e31fbc944ee97f95a3f556b4e21c4dbe4847ee9d0` | Competition rules, design perspective, and integrity boundaries |
| 105 | `docs` | `docs/hackathon/SUBMISSION.md` | 5.32 KB | `13f6abe5fee18c06ecbc981db851a47a3a766dfc479895ea66e0ef1ec58ad456` | Deliverable manifest checklist and submission requirements |
| 106 | `docs` | `docs/one_page_agreement.html` | 11.08 KB | `a92cb6b5c7427ea02d216cd5d97ea4cfd157cc43f0c8af9cfd05ada0a999b60d` | Rendered one-page SLA agreement strictly formatted to 1 A4 page |
| 107 | `docs` | `docs/one_page_agreement.md` | 6.58 KB | `254e3961995d99d9d151b2db2f824a852659df918809bb6ab7506a4a5ee23af7` | Markdown source of the one-page SLA agreement |
| 108 | `presentation` | `presentation/PITCH_DECK_OUTLINE.md` | 44.41 KB | `5f7987a8719de3c1533052b9db6394c440358ea0118f08d3a4e9881e0329b3c9` | Original pitch deck structure reference outline |
| 109 | `presentation` | `presentation/PITCH_DECK_OUTLINE_v2.md` | 44.95 KB | `204e2a9c5640f609e12c9908903296354b73091010728986aa57d005de614917` | Detailed pitch deck structure and jury defense talking points |
| 110 | `presentation` | `presentation/Project_Sentinel_12pages_final.pptx` | 16.31 MB | `3cbc088ad7887f89238e0fae7a5e1e80fceac5174e7ac3ecd6f0017eabaf83a9` | 12-slide modern presentation pitch deck for championship defense |
| 111 | `presentation` | `presentation/SPEECH_OVERHEAT_SCENE.md` | 9.17 KB | `d42e7d94fc6c27176052d87b432aa895e7d1f7c528387695c6d1068bbd8b46a8` | Deep-dive verbal script for S1 sub-zero thermal trip scenario |
| 112 | `presentation` | `presentation/SPEECH_SIX_SCENES.md` | 12.60 KB | `6beabed6486dd43476d4c3bcad97c0003eac9c1d887c07c5ddc7adc7776055fc` | Verbal presentation speech script covering all 6 failure scenarios |
| 113 | `presentation` | `presentation/presentation 1.mp4` | 61.05 MB | `2dd2206be17fe2dbca005a490a1bf424cc74c59b2f0b84d28cf5e0fdd8ea143d` | Stage presentation rehearsal demonstration video part 1 |
| 114 | `presentation` | `presentation/presentation 2.mp4` | 53.47 MB | `f7e1a5e90888dc1e37ae53b4baa6641d1d03c8f4735d75385e83e66e0a979ef3` | Stage presentation rehearsal demonstration video part 2 |
| 115 | `presentation` | `presentation/presentation_demo.mp4` | 5.78 MB | `e3881b1d21b1c15e26b8809a5a9e4a1c642ae516103dc5694c4aec5375d8763e` | Master 1080p presentation demo video (75s runtime) |
| 116 | `root` | `README.md` | 23.78 KB | `3f3e17acc7fbd1c04a0dc880551b8ee8422dfbe4b90894ce8aee28707c16fb1e` | Master project documentation, system architecture, 6-scenario benchmark, and quickstart guide |
| 117 | `videos` | `videos/1.Night replay.mp4` | 149.79 MB | `fed7cac36fe3051b22b700dafaf573f1bf20b47179d428d5fdfa471a0162aaf9` | Scenario 1: S1 overnight bus depot sub-zero charging & thermal trip replay (1080p) |
| 118 | `videos` | `videos/2.Outage replay.mp4` | 374.07 MB | `3f9a6c1d0dc221cf0b8a07fd546dead842fbe21c4318a7feec75ca61d3dffd6d` | Scenario 2: S3 highway public hub 2-hour cellular outage & edge islanding replay (1080p) |
| 119 | `videos` | `videos/3.Price spike replay.mp4` | 205.84 MB | `a6e57eaf9207cff17a502640951dd36982bc838a2e66fdd1a19b61260c1edafd` | Scenario 3: S4 urban hub 799.30 EUR/MWh price spike peak shaving replay (1080p) |
| 120 | `videos` | `videos/4.Curtailment replay.mp4` | 104.31 MB | `ad4c607f9e7f946efa7508f18f05e3d6bfb8a0a0a0f5b5fd8253404f378cb93e` | Scenario 4: S2 logistics depot 400 kW DSO curtailment preemption replay (1080p) |
| 121 | `videos` | `videos/5.Cable fault replay.mp4` | 77.86 MB | `a8ec106a3b47e4d07b7c94f1e78649e2de7604cb3227c887e331825b54052f9d` | Scenario 5: S1 dispenser cable fault & BBM rerouting replay (1080p) |
| 122 | `videos` | `videos/6.Commissioning replay.mp4` | 133.89 MB | `bf81e08b2998daeadcd5831bcea249769a196e9deb14dca57120e9e0e7625e89` | Scenario 6: S5 commissioning configuration reconciliation replay (1080p) |

---

## Independent Verification Instructions

To independently verify the integrity of all files in this submission, run:
```bash
# 1. Unzip the archive
unzip submission.zip -d submission_verify/
cd submission_verify/

# 2. Run the automated verifier
python code/verify_all.py

# 3. Run the complete E2E and Pytest test suites
python -m code.e2e_tests.test_runner
pytest code/tests/ -q
```
