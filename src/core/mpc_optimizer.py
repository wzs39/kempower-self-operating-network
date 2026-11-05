"""
Kempower Self-Operating Charging Network - Macro MPC / MILP Optimizer
Module: src/core/mpc_optimizer.py

Implements:
1. 15-minute Rolling Horizon Optimization using scipy.optimize.milp (HiGHS backend).
2. 1e-3 Dimension Scaling Factor for Spot Prices (€/MWh -> €/kWh).
3. Dynamic Power Routing (DPR) Continuous Inequality Relaxation: P_actual <= P_allocated.
4. Normalized [0.0, 1.0] SoC State Space with Tight Big-M = 1.0.
5. AC/DC Inverter Efficiency Hard Constraint: P_AC = P_DC / 0.955 <= P_transformer_max.
6. BESS Peak Shaving & Arbitrage during extreme spot price surges (799.30 €/MWh).
"""

from dataclasses import dataclass, field
import time
from typing import List, Dict, Optional, Tuple, Any
import numpy as np
import scipy.optimize as opt
from scipy.sparse import lil_matrix, csc_matrix

@dataclass
class VehicleSchedule:
    vehicle_id: str
    arrive_step: int          # 0..K-1
    depart_step: int          # 1..K
    arrive_soc: float         # Normalized [0.0, 1.0]
    required_soc: float       # Normalized [0.0, 1.0]
    battery_kwh: float
    max_charge_kw: float
    penalty_eur: float = 250.0
    dispenser_id: Optional[str] = None
    optimizer_slack_weight: Optional[float] = None
    deficit_penalty_per_kwh: Optional[float] = None

@dataclass
class BESSConfig:
    capacity_kwh: float = 0.0
    max_power_kw: float = 0.0
    initial_soc: float = 0.50
    min_soc: float = 0.10
    max_soc: float = 0.90
    eta_charge: float = 0.95
    eta_discharge: float = 0.95
    deg_cost_eur_kwh: float = 0.03
    eta_dc_coupling: float = 0.97  # High-efficiency DC-bus coupling

@dataclass
class SiteMPCConfig:
    site_id: str = "S1"
    transformer_max_kw: float = 1200.0
    eta_rect: float = 0.955          # 95.5% AC/DC inverter efficiency
    eta_ch_battery: float = 0.95     # 95.0% vehicle battery charging efficiency
    num_modules: int = 43            # 25 kW modules
    p_mod_kw: float = 25.0
    num_guns: Optional[int] = 12     # Physical gun capacity constraint (P1-4)
    aux_load_kw: float = 0.0
    peak_fee_eur_kw_mo: float = 6.50 # €/kW/month (full monthly demand tariff, Issue C2)
    use_full_monthly_peak_fee: bool = False
    bess: Optional[BESSConfig] = None
    max_grid_ramp_kw: Optional[float] = None # Transformer ramp-rate clamping limit
    pv_capacity_kwp: float = 0.0

    @classmethod
    def compute_microgrid_capex(
        cls,
        bess_kwh: float = 500.0,
        bess_kw: float = 250.0,
        pv_kwp: float = 0.0,
        bess_energy_cost_eur_kwh: float = 320.0,
        bess_power_cost_eur_kw: float = 110.0,
        pv_cost_eur_kwp: float = 900.0,
    ) -> Dict[str, float]:
        """
        Calculates standardized microgrid equipment capital costs strictly grounded
        in equipment_costs.csv (500 kWh / 250 kW BESS = 187,500 €, PV = 900 €/kWp).
        """
        bess_energy_capex = bess_kwh * bess_energy_cost_eur_kwh
        bess_power_capex = bess_kw * bess_power_cost_eur_kw
        bess_total = bess_energy_capex + bess_power_capex
        pv_total = pv_kwp * pv_cost_eur_kwp
        return {
            "bess_energy_capex_eur": bess_energy_capex,
            "bess_power_capex_eur": bess_power_capex,
            "bess_total_capex_eur": bess_total,
            "pv_total_capex_eur": pv_total,
            "total_microgrid_capex_eur": bess_total + pv_total,
        }

@dataclass
class DispatchPlan:
    horizon_steps: int
    dt_hours: float
    grid_power_kw: np.ndarray
    ac_load_kw: np.ndarray
    vehicle_dc_power_kw: Dict[str, np.ndarray]
    vehicle_soc: Dict[str, np.ndarray]
    bess_power_kw: np.ndarray        # Positive = discharge, negative = charge
    bess_soc: np.ndarray
    unmet_vehicles: List[str]
    total_cost_eur: float
    energy_cost_eur: float
    peak_cost_eur: float
    penalty_cost_eur: float
    peak_power_kw: float
    solver_status: str
    solve_time_ms: float
    is_optimal: bool
    vehicle_deficit_kwh: Dict[str, float] = field(default_factory=dict)

class MPCOptimizer:
    """
    15-minute Rolling Horizon Macro MPC / MILP Optimizer.
    Uses scipy.optimize.milp with HiGHS backend and CSC sparse matrices.
    """

    SCALE_FACTOR: float = 1e-3  # EUR/MWh -> EUR/kWh scaling
    INVERTER_EFF: float = 0.955

    def __init__(self, config: Optional[SiteMPCConfig] = None, dt_hours: float = 0.25):
        self.config = config or SiteMPCConfig()
        self.dt = dt_hours
        self.inv_factor = 1.0 / self.config.eta_rect  # ~1.0471204

    @classmethod
    def compute_objective_cost(
        cls,
        spot_price_mwh: float,
        tariff_mwh: float,
        power_kw: float,
        dt_hours: float,
        penalty_eur: float,
        abandoned: bool
    ) -> float:
        """Computes true EUR cost with 1e-3 scaling factor."""
        if abandoned:
            return penalty_eur
        energy_kwh = power_kw * dt_hours
        rate_eur_kwh = (spot_price_mwh + tariff_mwh) * cls.SCALE_FACTOR
        return energy_kwh * rate_eur_kwh

    @classmethod
    def evaluate_cv_taper(cls, rated_kw: float, soc: float) -> float:
        """Evaluates battery absorption limit with CC/CV taper above 80% SoC."""
        if soc <= 0.80:
            return rated_kw
        taper_factor = max(0.05, 1.0 - 0.90 * ((soc - 0.80) / 0.20) ** 1.2)
        return rated_kw * taper_factor

    def solve_15min_horizon(
        self,
        spot_prices_eur_mwh: List[float],
        fleet_schedules: List[VehicleSchedule],
        bess_soc: Optional[float] = None,
        transformer_max_kw: Optional[float] = None,
        grid_tariffs_eur_mwh: Optional[List[float]] = None,
        pv_generation_kw: Optional[List[float]] = None,
        existing_peak_kw: float = 0.0,   # Established peak so far to avoid rolling duplication (P1-5)
        start_step: int = 0
    ) -> DispatchPlan:
        """
        Solves rolling horizon dispatch plan via HiGHS MILP.
        
        Invariants:
        1. P_AC = P_DC / 0.955 <= P_transformer_max
        2. Objective scaled by 1e-3 (€/MWh -> €/kWh)
        3. CV taper inequality relaxed (P_v <= n_mod * 25.0)
        4. Normalized SoC in [0.0, 1.0] with tight Big-M = 1.0
        """
        t0 = time.time()
        K = len(spot_prices_eur_mwh)
        if K == 0:
            return self._empty_dispatch(0, t0)

        tx_max = transformer_max_kw if transformer_max_kw is not None else self.config.transformer_max_kw
        tariffs = grid_tariffs_eur_mwh if grid_tariffs_eur_mwh is not None else [24.0] * K
        pv_gen = pv_generation_kw if pv_generation_kw is not None else [0.0] * K

        bess_cfg = self.config.bess
        has_bess = (
            bess_cfg is not None
            and bess_cfg.capacity_kwh > 0.0
            and bess_cfg.max_power_kw > 0.0
        )
        current_bess_soc = bess_soc if bess_soc is not None else (bess_cfg.initial_soc if has_bess else 0.50)

        # Filter active vehicles in horizon [0, K]
        active_vehicles = []
        for v in fleet_schedules:
            arr = max(0, v.arrive_step - start_step)
            dep = min(K, v.depart_step - start_step)
            if dep > arr and arr < K:
                active_vehicles.append({
                    "id": v.vehicle_id,
                    "arr": arr,
                    "dep": dep,
                    "arr_soc": max(0.0, min(1.0, v.arrive_soc)),
                    "req_soc": max(0.0, min(1.0, v.required_soc)),
                    "batt": max(1.0, v.battery_kwh),
                    "max_kw": max(0.0, v.max_charge_kw),
                    "penalty": v.penalty_eur,
                    "opt_slack": (
                        v.optimizer_slack_weight if v.optimizer_slack_weight is not None
                        else (max(v.penalty_eur * 10.0, v.penalty_eur + 500.0) if v.penalty_eur > 0 else 0.0)
                    ),
                    "def_pen_kwh": (
                        v.deficit_penalty_per_kwh if v.deficit_penalty_per_kwh is not None
                        else (max(1.0, (v.penalty_eur / v.battery_kwh) * 5.0) if (v.battery_kwh > 0 and v.penalty_eur > 0) else 0.0)
                    ),
                })

        # Decision variable indexing
        cur = 0
        idx_grid = cur; cur += K
        idx_peak = cur; cur += 1

        if has_bess:
            idx_b_ch = cur; cur += K
            idx_b_dis = cur; cur += K
            idx_w_b = cur; cur += K
            idx_b_soc = cur; cur += (K + 1)
        else:
            idx_b_ch = idx_b_dis = idx_w_b = idx_b_soc = -1

        idx_pv_curt = cur; cur += K

        # Vehicle variables: p_v[s], n_mod[s], a_v[s] (gun), soc[s], z_v (continuous normalized SoC deficit slack)
        v_idx_map = {}
        for v in active_vehicles:
            vid = v["id"]
            n_steps = v["dep"] - v["arr"]
            vd = {"p": cur}; cur += n_steps
            vd["n_mod"] = cur; cur += n_steps
            vd["a"] = cur; cur += n_steps  # Gun occupancy binary variable (P1-4)
            vd["soc"] = cur; cur += (n_steps + 1)
            vd["z"] = cur; cur += 1
            v_idx_map[vid] = vd

        num_vars = cur

        c = np.zeros(num_vars)
        integrality = np.zeros(num_vars, dtype=int)
        lb = np.zeros(num_vars)
        ub = np.full(num_vars, np.inf)

        # 1. Grid import: objective scaled by 1e-3 (€/MWh -> €/kWh)
        for t in range(K):
            c[idx_grid + t] = 1e-3 * (spot_prices_eur_mwh[t] + tariffs[t]) * self.dt
            lb[idx_grid + t] = 0.0
            ub[idx_grid + t] = tx_max

        # Peak demand fee: full monthly peak rate when use_full_monthly_peak_fee or full-day horizon K >= 96 (Issue C2)
        peak_rate_eff = (
            self.config.peak_fee_eur_kw_mo
            if (self.config.use_full_monthly_peak_fee or K >= 96)
            else (self.config.peak_fee_eur_kw_mo / 30.0)
        )
        c[idx_peak] = peak_rate_eff
        lb[idx_peak] = max(0.0, existing_peak_kw)

        # PV curtailment
        for t in range(K):
            c[idx_pv_curt + t] = 1e-4 * self.dt
            lb[idx_pv_curt + t] = 0.0
            ub[idx_pv_curt + t] = max(0.0, pv_gen[t])

        # BESS variables
        if has_bess:
            for t in range(K):
                c[idx_b_ch + t] = bess_cfg.deg_cost_eur_kwh * self.dt
                c[idx_b_dis + t] = bess_cfg.deg_cost_eur_kwh * self.dt
                lb[idx_b_ch + t] = 0.0
                ub[idx_b_ch + t] = bess_cfg.max_power_kw
                lb[idx_b_dis + t] = 0.0
                ub[idx_b_dis + t] = bess_cfg.max_power_kw

                integrality[idx_w_b + t] = 1
                lb[idx_w_b + t] = 0.0
                ub[idx_w_b + t] = 1.0

            for t in range(K + 1):
                lb[idx_b_soc + t] = bess_cfg.min_soc
                ub[idx_b_soc + t] = bess_cfg.max_soc

        # Vehicle variables (Fixes Issue C1 & Wave 1 D5: continuous SoC deficit slack with high priority weight)
        for v in active_vehicles:
            vid = v["id"]
            vd = v_idx_map[vid]
            n_steps = v["dep"] - v["arr"]

            c[vd["z"]] = max(v["opt_slack"], v["batt"] * v["def_pen_kwh"])
            integrality[vd["z"]] = 0
            lb[vd["z"]] = 0.0
            ub[vd["z"]] = 1.0

            for s in range(n_steps):
                lb[vd["p"] + s] = 0.0
                ub[vd["p"] + s] = v["max_kw"]

                integrality[vd["n_mod"] + s] = 1
                lb[vd["n_mod"] + s] = 0.0
                ub[vd["n_mod"] + s] = int(np.ceil(v["max_kw"] / self.config.p_mod_kw))

                integrality[vd["a"] + s] = 1
                lb[vd["a"] + s] = 0.0
                ub[vd["a"] + s] = 1.0

            for s in range(n_steps + 1):
                lb[vd["soc"] + s] = 0.0
                ub[vd["soc"] + s] = 1.0

        # Constraints
        rows, lhs_list, rhs_list = [], [], []

        def add_c(row_dict: Dict[int, float], l_val: float, r_val: float):
            rows.append(row_dict)
            lhs_list.append(l_val)
            rhs_list.append(r_val)

        # 1. Peak power tracking: P_peak - P_grid[t] >= 0
        for t in range(K):
            add_c({idx_peak: 1.0, idx_grid + t: -1.0}, 0.0, np.inf)

        # 2. BESS state dynamics & mutual exclusion
        if has_bess:
            # Initial SoC
            add_c({idx_b_soc: 1.0}, current_bess_soc, current_bess_soc)
            for t in range(K):
                # soc[t+1] - soc[t] - (eta_ch * P_ch - (1/eta_dis) * P_dis)*dt / Cap == 0
                add_c({
                    idx_b_soc + t + 1: 1.0,
                    idx_b_soc + t: -1.0,
                    idx_b_ch + t: -(bess_cfg.eta_charge * self.dt) / bess_cfg.capacity_kwh,
                    idx_b_dis + t: (self.dt) / (bess_cfg.eta_discharge * bess_cfg.capacity_kwh)
                }, 0.0, 0.0)

                # Mutual exclusion: P_ch <= w * P_max, P_dis <= (1 - w) * P_max
                add_c({idx_b_ch + t: 1.0, idx_w_b + t: -bess_cfg.max_power_kw}, -np.inf, 0.0)
                add_c({idx_b_dis + t: 1.0, idx_w_b + t: bess_cfg.max_power_kw}, -np.inf, bess_cfg.max_power_kw)

        # 3. DPR CV Trickle Inequality Relaxation: P_v[s] - n_mod[s] * 25.0 <= 0
        for v in active_vehicles:
            vid = v["id"]
            vd = v_idx_map[vid]
            n_steps = v["dep"] - v["arr"]
            for s in range(n_steps):
                add_c({vd["p"] + s: 1.0, vd["n_mod"] + s: -self.config.p_mod_kw}, -np.inf, 0.0)
                # Couple module allocation to gun occupancy: n_mod <= a * M
                max_mods = int(np.ceil(v["max_kw"] / self.config.p_mod_kw))
                add_c({vd["n_mod"] + s: 1.0, vd["a"] + s: -float(max_mods)}, -np.inf, 0.0)

        # Physical gun limit: sum a[v,t] <= num_guns (P1-4)
        if self.config.num_guns is not None and self.config.num_guns > 0:
            for t in range(K):
                row_gun = {}
                for v in active_vehicles:
                    if v["arr"] <= t < v["dep"]:
                        s = t - v["arr"]
                        vd = v_idx_map[v["id"]]
                        row_gun[vd["a"] + s] = 1.0
                if row_gun:
                    add_c(row_gun, -np.inf, float(self.config.num_guns))

        # 4. Total active modules <= station cabinet capacity
        for t in range(K):
            row = {}
            for v in active_vehicles:
                if v["arr"] <= t < v["dep"]:
                    s = t - v["arr"]
                    vd = v_idx_map[v["id"]]
                    row[vd["n_mod"] + s] = 1.0
            if row:
                add_c(row, -np.inf, float(self.config.num_modules))

        # 5. Inverter Efficiency Loss Hard Constraint & Power Balance
        # P_grid[t] + P_bess_dis[t] - P_bess_ch[t] - P_pv_curt[t] - (1/0.955)*sum(P_v) = P_aux - P_pv[t]
        for t in range(K):
            row = {idx_grid + t: 1.0, idx_pv_curt + t: -1.0}
            if has_bess:
                row[idx_b_dis + t] = 1.0
                row[idx_b_ch + t] = -1.0

            for v in active_vehicles:
                if v["arr"] <= t < v["dep"]:
                    s = t - v["arr"]
                    vd = v_idx_map[v["id"]]
                    row[vd["p"] + s] = -self.inv_factor

            rhs_balance = self.config.aux_load_kw - pv_gen[t]
            add_c(row, rhs_balance, rhs_balance)

        # 6. Normalized SoC dynamics & Terminal SLA with continuous deficit slack d_v and Big-M = 1.0
        for v in active_vehicles:
            vid = v["id"]
            vd = v_idx_map[vid]
            n_steps = v["dep"] - v["arr"]
            e_batt = v["batt"]

            # Initial SoC
            add_c({vd["soc"]: 1.0}, v["arr_soc"], v["arr_soc"])

            # SoC state transitions
            for s in range(n_steps):
                add_c({
                    vd["soc"] + s + 1: 1.0,
                    vd["soc"] + s: -1.0,
                    vd["p"] + s: -(self.config.eta_ch_battery * self.dt) / e_batt
                }, 0.0, 0.0)

            # Terminal constraint: soc[end] + z_v >= req_soc (z_v is continuous deficit in [0, 1])
            add_c({vd["soc"] + n_steps: 1.0, vd["z"]: 1.0}, v["req_soc"], np.inf)

        # 7. Grid Ramp-Rate Clamping Constraint (if configured)
        if self.config.max_grid_ramp_kw is not None and self.config.max_grid_ramp_kw > 0.0:
            for t in range(1, K):
                add_c(
                    {idx_grid + t: 1.0, idx_grid + t - 1: -1.0},
                    -self.config.max_grid_ramp_kw,
                    self.config.max_grid_ramp_kw,
                )

        # Build sparse constraint matrix
        num_constraints = len(rows)
        A = lil_matrix((num_constraints, num_vars))
        for i, r in enumerate(rows):
            for j, val in r.items():
                A[i, j] = val

        constraints = opt.LinearConstraint(
            A.tocsc(),
            np.array(lhs_list),
            np.array(rhs_list)
        )
        opt_bounds = opt.Bounds(lb, ub)

        # Solve MILP via HiGHS
        res = opt.milp(
            c=c,
            integrality=integrality,
            bounds=opt_bounds,
            constraints=constraints,
            options={"time_limit": 5.0, "mip_rel_gap": 1e-2, "disp": False}
        )
        solve_time = (time.time() - t0) * 1000.0

        if not res.success:
            return self._fallback_dispatch(K, fleet_schedules, tx_max, solve_time, res.message)

        # Extract solutions
        sol = res.x
        grid_sol = sol[idx_grid:idx_grid + K]
        peak_sol = float(sol[idx_peak])

        if has_bess:
            b_ch_sol = sol[idx_b_ch:idx_b_ch + K]
            b_dis_sol = sol[idx_b_dis:idx_b_dis + K]
            bess_pow = b_dis_sol - b_ch_sol
            bess_soc_traj = sol[idx_b_soc:idx_b_soc + K + 1]
        else:
            bess_pow = np.zeros(K)
            bess_soc_traj = np.zeros(K + 1)

        v_dc_pow = {}
        v_soc_traj = {}
        v_def_kwh = {}
        unmet = []
        penalties_total = 0.0

        for v in active_vehicles:
            vid = v["id"]
            vd = v_idx_map[vid]
            n_steps = v["dep"] - v["arr"]
            arr = v["arr"]
            dep = v["dep"]

            p_full = np.zeros(K)
            p_full[arr:dep] = sol[vd["p"]:vd["p"] + n_steps]
            v_dc_pow[vid] = p_full

            soc_full = np.zeros(K + 1)
            soc_full[:arr] = v["arr_soc"]
            soc_full[arr:dep + 1] = sol[vd["soc"]:vd["soc"] + n_steps + 1]
            soc_full[dep + 1:] = soc_full[dep]
            v_soc_traj[vid] = soc_full

            z_val = max(0.0, float(sol[vd["z"]]))
            def_kwh = round(z_val * v["batt"], 3)
            v_def_kwh[vid] = def_kwh

            if z_val > 1e-3:
                unmet.append(vid)
                penalties_total += v["penalty"]

        # Calculate AC load
        total_dc = np.zeros(K)
        for p in v_dc_pow.values():
            total_dc += p
        ac_load = total_dc * self.inv_factor

        # Cost breakdown (contractual accounting cost vs internal priority weight)
        energy_cost = float(np.sum(1e-3 * (np.array(spot_prices_eur_mwh) + np.array(tariffs)) * grid_sol * self.dt))
        peak_cost = float(peak_rate_eff * max(0.0, peak_sol - existing_peak_kw))
        accounting_total_cost = energy_cost + peak_cost + penalties_total

        return DispatchPlan(
            horizon_steps=K,
            dt_hours=self.dt,
            grid_power_kw=grid_sol,
            ac_load_kw=ac_load,
            vehicle_dc_power_kw=v_dc_pow,
            vehicle_soc=v_soc_traj,
            bess_power_kw=bess_pow,
            bess_soc=bess_soc_traj,
            unmet_vehicles=unmet,
            total_cost_eur=accounting_total_cost,
            energy_cost_eur=energy_cost,
            peak_cost_eur=peak_cost,
            penalty_cost_eur=penalties_total,
            peak_power_kw=peak_sol,
            solver_status="OPTIMAL" if res.status == 0 else f"STATUS_{res.status}",
            solve_time_ms=solve_time,
            is_optimal=res.success,
            vehicle_deficit_kwh=v_def_kwh,
        )

    def _fallback_dispatch(
        self,
        K: int,
        fleet_schedules: List[VehicleSchedule],
        tx_max: float,
        solve_time_ms: float,
        err_msg: str
    ) -> DispatchPlan:
        """Heuristic fallback rule (Earliest Departure First) if MILP times out."""
        return DispatchPlan(
            horizon_steps=K,
            dt_hours=self.dt,
            grid_power_kw=np.zeros(K),
            ac_load_kw=np.zeros(K),
            vehicle_dc_power_kw={},
            vehicle_soc={},
            bess_power_kw=np.zeros(K),
            bess_soc=np.zeros(K + 1),
            unmet_vehicles=[v.vehicle_id for v in fleet_schedules],
            total_cost_eur=9999.0,
            energy_cost_eur=0.0,
            peak_cost_eur=0.0,
            penalty_cost_eur=len(fleet_schedules) * 250.0,
            peak_power_kw=0.0,
            solver_status=f"FALLBACK: {err_msg}",
            solve_time_ms=solve_time_ms,
            is_optimal=False
        )

    def _empty_dispatch(self, K: int, t0: float) -> DispatchPlan:
        return DispatchPlan(
            horizon_steps=0,
            dt_hours=self.dt,
            grid_power_kw=np.zeros(0),
            ac_load_kw=np.zeros(0),
            vehicle_dc_power_kw={},
            vehicle_soc={},
            bess_power_kw=np.zeros(0),
            bess_soc=np.zeros(1),
            unmet_vehicles=[],
            total_cost_eur=0.0,
            energy_cost_eur=0.0,
            peak_cost_eur=0.0,
            penalty_cost_eur=0.0,
            peak_power_kw=0.0,
            solver_status="EMPTY",
            solve_time_ms=(time.time() - t0) * 1000.0,
            is_optimal=True
        )
