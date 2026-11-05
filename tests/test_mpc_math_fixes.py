"""
Verification Script for Explorer Fix 1: MPC Mathematical Fixes
Using scipy.optimize.milp (HiGHS) to verify exact mathematical behaviors:
1. Dimensional scaling factor (1e-3): Demonstrates why missing 1e-3 forces solver to abandon vehicle charging, and why 1e-3 restores optimal charging.
2. DPR relaxation (P_d <= sum(u) * P_mod): Demonstrates why strict equality fails under CC/CV taper (<25kW), and why inequality enables continuous tapering.
3. SoC scaling consistency: Demonstrates state update and terminal check in [0.0, 1.0].
"""
import numpy as np
import scipy.optimize as opt

def test_dimensional_scaling():
    print("=== TEST 1: Dimensional Scaling Factor (1e-3) ===")
    spot_price = 799.30  # EUR/MWh
    tariff = 24.00       # EUR/MWh
    p_req = 100.0        # kW
    dt = 0.25            # h
    penalty_eur = 250.0  # EUR
    
    # Decision vector: x = [P_grid, z]
    # P_grid >= 0, z in {0, 1}
    # Constraint: P_grid >= p_req * (1 - z)  =>  -P_grid - p_req * z <= -p_req
    integrality = [0, 1]  # P_grid continuous, z binary
    bounds = opt.Bounds([0.0, 0.0], [p_req, 1.0])
    A = np.array([[-1.0, -p_req]])
    b_u = np.array([-p_req])
    constraints = opt.LinearConstraint(A, -np.inf, b_u)
    
    # CASE A: Flawed unscaled objective (Price * P * dt)
    # c_grid = (799.30 + 24.00) * 0.25 = 205.825
    c_unscaled = np.array([(spot_price + tariff) * dt, penalty_eur])
    res_a = opt.milp(c=c_unscaled, integrality=integrality, bounds=bounds, constraints=constraints)
    
    cost_charge_unscaled = (spot_price + tariff) * p_req * dt
    print(f"Case A (Unscaled): Evaluated charging as {cost_charge_unscaled:.2f} EUR vs Penalty {penalty_eur:.2f} EUR")
    print(f"  Solver Decision: P_grid = {res_a.x[0]:.2f} kW, z = {res_a.x[1]:.0f} (1 = Abandon charging / pay penalty)")
    assert res_a.x[1] == 1.0, "Expected solver to abandon charging due to 1000x inflated cost!"
    
    # CASE B: Corrected scaled objective (1e-3 * Price * P * dt)
    # c_grid = 1e-3 * (799.30 + 24.00) * 0.25 = 0.205825
    c_scaled = np.array([((spot_price + tariff) / 1000.0) * dt, penalty_eur])
    res_b = opt.milp(c=c_scaled, integrality=integrality, bounds=bounds, constraints=constraints)
    
    real_cost_charge = ((spot_price + tariff) / 1000.0) * p_req * dt
    print(f"Case B (Corrected 1e-3): Real charging cost = {real_cost_charge:.2f} EUR vs Penalty {penalty_eur:.2f} EUR")
    print(f"  Solver Decision: P_grid = {res_b.x[0]:.2f} kW, z = {res_b.x[1]:.0f} (0 = Charge vehicle, meet SLA)")
    assert res_b.x[1] == 0.0, "Expected solver to successfully charge vehicle!"
    print("  -> TEST 1 PASSED: 1e-3 factor is mathematically mandatory!\n")

def test_dpr_cv_tapering():
    print("=== TEST 2: Dynamic Power Routing CC/CV Relaxation ===")
    p_mod = 25.0         # 25 kW per module
    p_veh_taper = 16.8   # vehicle in CV phase can only absorb 16.8 kW (< 25 kW)
    
    # Maximize delivered power: min -P_d
    # Decision vector: x = [P_d, u]
    # bounds: 0 <= P_d <= p_veh_taper, u in {0, 1}
    c = np.array([-1.0, 0.0])
    integrality = [0, 1]
    bounds = opt.Bounds([0.0, 0.0], [p_veh_taper, 1.0])
    
    # CASE A: Flawed strict equality (P_d == u * 25  =>  P_d - 25*u == 0)
    A_eq = np.array([[1.0, -p_mod]])
    constraints_eq = opt.LinearConstraint(A_eq, [0.0], [0.0])
    res_a = opt.milp(c=c, integrality=integrality, bounds=bounds, constraints=constraints_eq)
    
    print(f"Case A (Strict Equality): P_d == u * 25 kW, P_veh_max = {p_veh_taper} kW")
    print(f"  Solver Result: P_d = {res_a.x[0]:.2f} kW, u = {res_a.x[1]:.0f}")
    assert res_a.x[0] == 0.0, "Strict equality must force P_d to 0 kW when taper < 25 kW!"
    
    # CASE B: Relaxed capacity envelope (P_d <= u * 25  =>  P_d - 25*u <= 0)
    constraints_ineq = opt.LinearConstraint(A_eq, [-np.inf], [0.0])
    res_b = opt.milp(c=c, integrality=integrality, bounds=bounds, constraints=constraints_ineq)
    
    print(f"Case B (Relaxed Envelope): P_d <= u * 25 kW, P_veh_max = {p_veh_taper} kW")
    print(f"  Solver Result: P_d = {res_b.x[0]:.2f} kW, u = {res_b.x[1]:.0f}")
    assert abs(res_b.x[0] - 16.8) < 1e-4, "Relaxed envelope must deliver exact 16.8 kW!"
    assert res_b.x[1] == 1.0, "Must allocate 1 module!"
    print("  -> TEST 2 PASSED: DPR relaxation P_d <= sum(u)*P_mod is mathematically mandatory!\n")

def test_soc_normalization():
    print("=== TEST 3: SoC Scaling Consistency in [0.0, 1.0] ===")
    arrive_soc_pct = 64.4
    required_soc_pct = 90.0
    battery_kwh = 400.0
    eta_ch = 0.95
    dt = 0.25 # h
    charge_kw = 150.0
    
    # Normalized model
    soc_0 = arrive_soc_pct / 100.0  # 0.644
    req_soc = required_soc_pct / 100.0  # 0.900
    
    # 4 time steps (1 hour) of 150 kW charging:
    # Energy into battery = 150 kW * 0.95 * 1.0 h = 142.5 kWh
    # Delta SoC = 142.5 / 400.0 = 0.35625 (35.625%)
    soc_t = soc_0
    for step in range(4):
        delta = (eta_ch * charge_kw * dt) / battery_kwh
        soc_t += delta
        
    print(f"Initial Normalized SoC: {soc_0:.4f} ({soc_0*100:.1f}%)")
    print(f"After 1 hour of 150kW charge: Final SoC: {soc_t:.4f} ({soc_t*100:.2f}%)")
    print(f"Required SoC: {req_soc:.4f} ({req_soc*100:.1f}%)")
    
    assert soc_t >= req_soc, "Expected vehicle to exceed required SoC of 90%!"
    shortfall = max(0.0, req_soc - soc_t)
    z_violation = 1 if shortfall > 0 else 0
    print(f"Violation flag z = {z_violation} (0 = compliant)")
    assert z_violation == 0, "Expected compliant departure!"
    print("  -> TEST 3 PASSED: Normalized SoC model operates seamlessly without scale distortion!\n")

if __name__ == "__main__":
    test_dimensional_scaling()
    test_dpr_cv_tapering()
    test_soc_normalization()
    print("ALL MATHEMATICAL FIX TESTS PASSED PERFECTLY!")
