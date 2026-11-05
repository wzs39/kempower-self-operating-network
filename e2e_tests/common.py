"""
Common production adapters and fixtures for e2e_tests suite.
Adheres strictly to the opaque-box test principle by exercising public interface contracts.
"""

import os
import sys
from pathlib import Path
import pandas as pd

# Ensure repo root is in sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from src.utils.paths import get_repo_root, get_data_dir
from src.core.dpr_matrix import DPRMatrix
from src.core.mpc_optimizer import MPCOptimizer
from src.core.self_healing import EdgeFSM
from src.core.virtual_replug import VirtualReplugManager
from src.commercial.sla_calculator import SLACalculator
from src.commercial.roi_analyzer import ROIAnalyzer
from src.sim.scenario_engine import ScenarioEngine

WORKSPACE = str(get_repo_root())
DATA_DIR = str(get_data_dir())
PROJECT_PATH = os.path.join(WORKSPACE, "PROJECT.md")
SLA_PATH = os.path.join(WORKSPACE, "One_Page_SLA_Specification.md")


class ContractDPRMatrix:
    """Production adapter for F01: 25 kW Dynamic Power Routing (src.core.dpr_matrix.DPRMatrix)."""
    MODULE_KW = DPRMatrix.MODULE_KW
    INVERTER_EFF = DPRMatrix.INVERTER_EFF

    @classmethod
    def allocate_power(cls, requests: dict[str, float], grid_limit_ac: float, cabinet_capacity_kw: float) -> dict[str, float]:
        dpr = DPRMatrix(station_id="S1", total_modules=int(max(43, cabinet_capacity_kw // cls.MODULE_KW)))
        res = dpr.allocate_power(
            requests=requests,
            grid_limit_ac=grid_limit_ac,
            cabinet_capacity_kw=cabinet_capacity_kw,
            discrete=True,
        )
        return res.allocated_capacity_kw

    @classmethod
    def re_route_contactor(cls, from_gun: str, to_gun: str, modules: int, initial_current_amps: float) -> dict:
        dpr = DPRMatrix(station_id="S1")
        seq = dpr.re_route_contactor(from_gun, to_gun, modules=modules, initial_current_amps=initial_current_amps)
        return {
            "success": seq["success"],
            "arc_prevented": seq["arc_prevented"],
            "switching_delay_ms": seq["switching_delay_ms"],
            "transferred_modules": seq["transferred_modules"],
        }


class ContractMPCSolver:
    """Production adapter for F02: 15-min Macro MPC/MILP (src.core.mpc_optimizer.MPCOptimizer)."""
    INVERTER_EFF = MPCOptimizer.INVERTER_EFF
    SCALE_FACTOR = MPCOptimizer.SCALE_FACTOR

    @classmethod
    def compute_objective_cost(cls, spot_price_mwh: float, tariff_mwh: float, power_kw: float, dt_hours: float, penalty_eur: float, abandoned: bool) -> float:
        return MPCOptimizer.compute_objective_cost(spot_price_mwh, tariff_mwh, power_kw, dt_hours, penalty_eur, abandoned)

    @classmethod
    def evaluate_cv_taper(cls, rated_kw: float, soc: float) -> float:
        return MPCOptimizer.evaluate_cv_taper(rated_kw, soc)


class ContractEdgeFSM:
    """Production adapter for F03: Edge Micro FSM (src.core.self_healing.EdgeFSM)."""
    NORMAL = "NORMAL"
    THERMAL_WARNING = "THERMAL_WARNING"
    LOAD_MIGRATION = "LOAD_MIGRATION"
    HARDWARE_TRIP = "HARDWARE_TRIP"
    OFFLINE_ISLANDING = "OFFLINE_ISLANDING"
    AUTO_CALIBRATED = "AUTO_CALIBRATED"

    @classmethod
    def tick(cls, telemetry: dict) -> dict:
        fsm = EdgeFSM(site_id=str(telemetry.get("site_id", "S1")))
        res = fsm.tick(telemetry)
        return {
            "state": res["state"],
            "action": res["action"],
            "safe": res["safe"],
            "rpm_drop_pct": res["rpm_drop_pct"],
            "fallback_kw": res["fallback_kw"],
        }


class ContractVirtualReplug:
    """Production adapter for F04: Dual-Gun Satellite Multiplexing (src.core.virtual_replug.VirtualReplugManager)."""
    @classmethod
    def schedule_depot_night(cls, buses_a: list[str], buses_b: list[str], current_time_hour: float) -> dict:
        return VirtualReplugManager.schedule_depot_night(buses_a, buses_b, current_time_hour)


class ContractSLAEngine:
    """Production adapter for F11: One-Page SLA & MRDT (src.commercial.sla_calculator.SLACalculator)."""
    @classmethod
    def compute_mrdt(cls, soc_req: float, soc_arrive: float, batt_kwh: float, p_charger_max: float, p_veh_max: float, eta: float = 0.95, t_buffer: float = 15.0) -> float:
        return SLACalculator.compute_mrdt(soc_req, soc_arrive, batt_kwh, p_charger_max, p_veh_max, eta=eta, t_buffer=t_buffer)

    @classmethod
    def compute_fleet_penalty(cls, delayed_records: list[dict], undercharged_records: list[dict], p_base: float = 250.0, c_min: float = 5.0, c_energy: float = 1.50) -> float:
        return SLACalculator.compute_fleet_penalty(delayed_records, undercharged_records, p_base=p_base, c_min=c_min, c_energy=c_energy)

    @classmethod
    def compute_availability_deduction(cls, monthly_base_fee: float, avail_pct: float) -> float:
        return SLACalculator.compute_availability_deduction(monthly_base_fee, avail_pct)
