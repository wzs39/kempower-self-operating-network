"""
Adversarial Stress Test Suite for Streamlit Dashboard (app.py) & Playback Engine.
Target: Kempower Autonomous Command Center (Sentinel v3.0).

Focus Areas:
1. Dual CLI / Streamlit Execution Guard verification.
2. Playback boundary conditions (minute = 0, 1425, 1439, -1, 1500, malformed types).
3. Incident & fault injection UI rendering (S1 Thermal Trip @ 02:25, S3 WAN Drop @ 11:00 per connectivity_outages.csv, S4 Price Spike @ 18:00).
4. Rapid view switches and widget interaction across all 4 cockpit views.
5. Commercial SLA interactive clearing resilience under extreme parameter ranges.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path
from typing import Dict, Any

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

import app
from src.commercial.settlement_clearing import ContractTier, SettlementClearingEngine


class TestDashboardCLIDualModeStress(unittest.TestCase):
    """Stress tests verifying strict dual CLI / Streamlit execution separation."""

    def test_import_app_non_blocking_in_subprocess(self):
        """Verify python -c 'import app' executes without starting a blocking server."""
        cmd = [sys.executable, "-c", "import app; print('CLEAN_IMPORT_OK')"]
        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(result.returncode, 0, f"Import failed with stderr: {result.stderr}")
        self.assertIn("CLEAN_IMPORT_OK", result.stdout)

    def test_cli_execution_runs_and_exits_zero(self):
        """Verify python app.py executes headless CLI test mode and exits cleanly with returncode 0."""
        cmd = [sys.executable, str(REPO_ROOT / "app.py")]
        result = subprocess.run(
            cmd,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, f"app.py failed: {result.stderr}")
        self.assertIn("Dashboard payload verified: 13 -> 3 (0 EUR software) | S1 4->3 same-engine, S2 4->0 same-engine under G1 400 kW, S5 5->0 config fix | zero-miss needs an unpriced cross-cabinet busbar; +12 plugs = 8 missed, worse.", result.stdout)

    def test_cli_execution_under_hostile_environment_variables(self):
        """Verify python app.py survives hostile and unusual environment configurations."""
        hostile_envs = [
            {"STREAMLIT_SERVER_HEADLESS": "true", "STREAMLIT_SERVER_PORT": "12345"},
            {"PYTHONUNBUFFERED": "1", "LANG": "C.UTF-8"},
            {"STREAMLIT_BROWSER_GATHER_USAGE_STATS": "false", "STREAMLIT_THEME_BASE": "light"},
        ]
        for env_delta in hostile_envs:
            env = os.environ.copy()
            env.update(env_delta)
            cmd = [sys.executable, str(REPO_ROOT / "app.py")]
            result = subprocess.run(
                cmd,
                cwd=str(REPO_ROOT),
                capture_output=True,
                text=True,
                timeout=30,
                env=env,
            )
            self.assertEqual(result.returncode, 0, f"Failed under env {env_delta}: {result.stderr}")
            self.assertIn("Dashboard payload verified: 13 -> 3 (0 EUR software) | S1 4->3 same-engine, S2 4->0 same-engine under G1 400 kW, S5 5->0 config fix | zero-miss needs an unpriced cross-cabinet busbar; +12 plugs = 8 missed, worse.", result.stdout)


class TestDashboardPlaybackBoundaryStress(unittest.TestCase):
    """Stress tests verifying slider scrubbing boundaries and malformed time inputs."""

    @classmethod
    def setUpClass(cls):
        # Inject 'streamlit' into sys.argv if not present so AppTest activates Streamlit path
        if not any("streamlit" in arg.lower() for arg in sys.argv):
            sys.argv.append("streamlit")
        from streamlit.testing.v1 import AppTest
        cls.AppTest = AppTest

    def test_apptest_nominal_load_all_views(self):
        """Verify that all 4 views and tabs render cleanly under nominal Streamlit execution."""
        at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
        self.assertEqual(len(at.exception), 0, f"Unexpected exceptions during initial load: {at.exception}")
        self.assertGreaterEqual(len(at.tabs), 4, "Cockpit must have at least 4 top-level views/tabs.")
        self.assertEqual(len(at.button), 6, "Must provide 6 critical incident quick jump buttons.")

    def test_scrub_boundary_minutes(self):
        """Test minute slider scrubbing boundaries: 00:00 (min 0), 23:45 (min 1425), 23:59 (min 1439), -00:01 (min -1), 25:00 (min 1500)."""
        at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
        boundary_inputs = [
            ("00:00", True),     # minute 0 (exact match)
            ("23:45", True),     # minute 1425 (exact match, last 15-min bucket)
            ("23:59", False),    # minute 1439 (boundary off-step, should fallback safely)
            ("-00:01", False),   # minute -1 (underflow)
            ("25:00", False),    # minute 1500 (overflow)
            ("", False),         # empty string
            (None, False),       # None object
            (99999, False),      # Integer type injection
        ]
        for val, is_valid in boundary_inputs:
            at.session_state["scrub_time"] = val
            at.run()
            self.assertEqual(
                len(at.exception),
                0,
                f"Unhandled exception encountered when setting scrub_time={val!r}: {at.exception}",
            )

    def test_quick_jump_incident_buttons_cycling(self):
        """Verify clicking all 6 incident buttons updates scrub_time correctly with 0 unhandled exceptions."""
        expected_times = [
            ("01:30 Wave 1 Swap", "01:30"),
            ("02:25 S1 Thermal Trip", "02:30"),
            ("11:00 S3 WAN Outage", "11:00"),
            ("04:00 S5 3-Way Calib", "04:00"),
            ("14:30 S2 Truck Surge", "14:30"),
            ("18:00 S4 Price Spike", "18:00"),
        ]
        for label, exp_time in expected_times:
            at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
            btn = next(b for b in at.button if b.label == label)
            at = btn.click().run()
            self.assertEqual(len(at.exception), 0, f"Exception on button {label}: {at.exception}")
            self.assertEqual(
                at.session_state.get("scrub_time"),
                exp_time,
                f"Button {label} failed to update scrub_time to {exp_time}",
            )


class TestDashboardFaultInjectionStress(unittest.TestCase):
    """Stress tests verifying dynamic fault injection UI banners and DPR contactor isolation states."""

    @classmethod
    def setUpClass(cls):
        if not any("streamlit" in arg.lower() for arg in sys.argv):
            sys.argv.append("streamlit")
        from streamlit.testing.v1 import AppTest
        cls.AppTest = AppTest

    def test_s1_thermal_trip_fault_injection_ui_state(self):
        """Inject S1 Thermal Trip at 02:25-02:30 and verify active fault banner and DPR matrix isolation."""
        at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
        at.session_state["scrub_time"] = "02:30"
        at.run()
        self.assertEqual(len(at.exception), 0)

        # Verify incident banner
        has_thermal_banner = any(
            "S1 Incident Active: Cabinet C1-3 Overtemperature Stop" in str(e.value)
            for e in at.error
        )
        self.assertTrue(has_thermal_banner, "S1 Thermal trip banner must be rendered in at.error.")

    def test_s3_outage_window_matches_official_file(self):
        """The UI incident times must equal the official connectivity_outages.csv window."""
        import pandas as pd
        from src.sim.data_loader import KempowerDataLoader
        df = KempowerDataLoader().load_df("connectivity_outages.csv")
        day = df[(df["site_id"] == "S3") & (df["start_ts"].astype(str).str.startswith("2026-11-13"))]
        self.assertEqual(len(day), 1, "exactly one S3 outage is expected on the scenario day")
        row = day.iloc[0]
        self.assertEqual(str(row["start_ts"])[11:16], "11:00")
        self.assertEqual(str(row["end_ts"])[11:16], "13:00")
        self.assertNotIn("03:15", str(row["start_ts"]), "03:15 belongs to the S1 F016 window, not the S3 outage")


    def test_s3_wan_drop_fault_injection_ui_state(self):
        """Inject the S3 Cellular WAN outage at its official 11:00 start and check the islanding banner."""
        at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
        at.session_state["scrub_time"] = "11:00"
        at.run()
        self.assertEqual(len(at.exception), 0)

        has_wan_banner = any(
            "S3 Incident Active: Cellular WAN Outage" in str(w.value)
            for w in at.warning
        )
        self.assertTrue(has_wan_banner, "S3 WAN outage islanding banner must be rendered in at.warning.")

    def test_s4_price_spike_fault_injection_ui_state(self):
        """Inject S4 Nord Pool spot price spike at 18:00 and verify peak price reaction banner."""
        at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
        at.session_state["scrub_time"] = "18:00"
        at.run()
        self.assertEqual(len(at.exception), 0)

        has_spike_banner = any(
            "S4 Extreme Spot Price Spike" in str(e.value)
            for e in at.error
        )
        self.assertTrue(has_spike_banner, "S4 Price spike reaction banner must be rendered in at.error.")

    def test_nominal_network_state_ui_rendering(self):
        """Verify nominal operating time (e.g. 10:00) displays green success status banner."""
        at = self.AppTest.from_file(str(REPO_ROOT / "app.py"), default_timeout=30).run()
        at.session_state["scrub_time"] = "10:00"
        at.run()
        self.assertEqual(len(at.exception), 0)

        has_nominal_banner = any(
            "Network Nominal Autonomous Operation" in str(s.value)
            for s in at.success
        )
        self.assertTrue(has_nominal_banner, "Nominal time must render green success banner.")


class TestCommercialSLAInteractiveStress(unittest.TestCase):
    """Stress tests on View 4 interactive settlement clearing and MRDT moral hazard boundary conditions."""

    def test_mrdt_boundary_zero_and_excessive_dwell(self):
        """Verify MRDT moral hazard filter correctly classifies extreme dwell boundaries."""
        from src.commercial.sla_calculator import SLACalculator
        from src.commercial.settlement_clearing import TIER_CONFIGS, ExemptionReason

        # 0 dwell time should always trigger moral hazard filter
        mrdt = SLACalculator.compute_mrdt(
            soc_req=85.0,
            soc_arrive=20.0,
            batt_kwh=400.0,
            p_charger_max=150.0,
            p_veh_max=150.0,
        )
        # MRDT = ((85-20)/100 * 400) / (150 * 0.95) * 60 + 15 = (260 / 142.5) * 60 + 15 = 109.47 + 15 = 124.47 min
        self.assertAlmostEqual(mrdt, 124.47, places=1)

        cfg = TIER_CONFIGS[ContractTier.TITANIUM]

        # Dwell = 10 min < 124.5 min -> Moral Hazard
        short_trip = {
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 20.0,
            "dwell_actual_min": 10.0,
            "delay_min": 30.0,
            "end_reason": "completed",
        }
        eval_short = SettlementClearingEngine.evaluate_mrdt_and_trip(short_trip, cfg)
        self.assertFalse(eval_short.mrdt_satisfied)
        self.assertEqual(eval_short.exemption_reason, ExemptionReason.CUSTOMER_DWELL_SHORTFALL)
        self.assertEqual(eval_short.total_penalty_eur, 0.0)

        # Dwell = 180 min >= 124.5 min -> Feasible, damages apply on delay
        valid_trip = {
            "battery_kwh": 400.0,
            "p_charger_max_kw": 150.0,
            "p_veh_max_kw": 150.0,
            "soc_arrive_pct": 20.0,
            "soc_req_pct": 85.0,
            "soc_dep_pct": 70.0,
            "dwell_actual_min": 180.0,
            "delay_min": 25.0,
            "end_reason": "completed",
        }
        eval_valid = SettlementClearingEngine.evaluate_mrdt_and_trip(valid_trip, cfg)
        self.assertTrue(eval_valid.mrdt_satisfied)
        self.assertEqual(eval_valid.exemption_reason, ExemptionReason.NONE)
        self.assertGreater(eval_valid.total_penalty_eur, 0.0)

    def test_extreme_settlement_parameters_strictly_preserve_liability_cap_and_non_negative_invariants(self):
        """Stress generate_monthly_settlement with catastrophic delays to verify 150% cap & non-negative invariant."""
        # 100 delayed trips with massive deficit
        catastrophic_trips = [
            {
                "trip_id": f"CATASTROPHIC_{i:03d}",
                "vehicle_id": f"BUS_{i:03d}",
                "site_id": "S1",
                "battery_kwh": 600.0,
                "p_charger_max_kw": 400.0,
                "p_veh_max_kw": 400.0,
                "soc_arrive_pct": 10.0,
                "soc_req_pct": 100.0,
                "soc_dep_pct": 10.0,
                "dwell_actual_min": 600.0,
                "delay_min": 180.0,
                "end_reason": "completed",
            }
            for i in range(100)
        ]

        for tier in (ContractTier.TITANIUM, ContractTier.GOLD, ContractTier.SILVER):
            stmt = SettlementClearingEngine.generate_monthly_settlement(
                site_id="S1",
                month="2026-11",
                tier=tier,
                actual_availability_pct=80.0,  # Massive availability breach
                trips=catastrophic_trips,
            )
            # Invariant 1: Final deduction strictly capped at 150% base fee
            max_cap = stmt.monthly_base_fee_eur * 1.50
            self.assertLessEqual(stmt.final_payout_deduction_eur, max_cap + 1e-4)

            # Invariant 2: Net invoice payable is non-negative
            self.assertGreaterEqual(stmt.net_invoice_payable_eur, 0.0)

            # Invariant 3: Audit hash length is valid SHA-256
            self.assertEqual(len(stmt.audit_hash), 64)


if __name__ == "__main__":
    unittest.main()
