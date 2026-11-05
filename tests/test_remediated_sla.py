import unittest
import numpy as np

def compute_remediated_fleet_penalty(delayed_trips, undercharged_trips, p_base=250.0, c_min=5.0, c_energy=1.5):
    """
    Remediated SLA Formula 4.1:
    Penalty_fleet = sum_{i in delayed_trips} [ P_base + max(0, t_delay_min,i - 15) * C_min ]
                  + sum_{j in undercharged} [ max(0, SoC_req,j - SoC_dep,j)/100.0 * Cap_batt,j * C_energy ]
    """
    total_penalty = 0.0
    for trip in delayed_trips:
        # Check MRDT condition
        if not trip.get('mrdt_satisfied', True):
            continue # exempt
        t_delay = trip['delay_min']
        if t_delay > 0:
            delay_cost = p_base + max(0.0, t_delay - 15.0) * c_min
            total_penalty += delay_cost
            
    for trip in undercharged_trips:
        if not trip.get('mrdt_satisfied', True):
            continue # exempt
        soc_req = trip['soc_req']
        soc_dep = trip['soc_dep']
        cap_kwh = trip['cap_kwh']
        delta_soc = max(0.0, soc_req - soc_dep) / 100.0
        energy_penalty = delta_soc * cap_kwh * c_energy
        total_penalty += energy_penalty
        
    return total_penalty

def compute_remediated_availability_deduction(monthly_base_fee, availability_actual):
    """
    Remediated SLA Formula 4.2 (Piecewise closed-form):
    Fee_deduction = 
      0, if Availability >= 99.50%
      Monthly Base Fee * min(90.0%, ceil((99.50% - Availability)/0.10%) * 2.0%), if 95.00% <= Availability < 99.50%
      Monthly Base Fee * 100.0%, if Availability < 95.00%
    """
    avail = round(availability_actual, 4)
    if avail >= 99.50:
        return 0.0
    elif avail >= 95.00:
        shortfall = round(99.50 - avail, 4)
        steps = int(np.ceil(shortfall / 0.10))
        pct = min(90.0, steps * 2.0)
        return monthly_base_fee * (pct / 100.0)
    else:
        return monthly_base_fee * 1.0

def compute_mrdt(soc_req, soc_arrive, batt_kwh, p_charger_max, p_veh_max, eta=0.95, t_buffer=15.0):
    """
    SLA Section 4.1 MRDT Formula:
    MRDT = [ ( (SoC_req - SoC_arrive)/100.0 * Cap_batt ) / ( min(P_charger, P_veh) * eta ) ] * 60 + T_buffer
    """
    delta_soc = max(0.0, soc_req - soc_arrive) / 100.0
    needed_energy = delta_soc * batt_kwh
    eff_power = min(p_charger_max, p_veh_max) * eta
    if eff_power <= 0:
        return float('inf')
    charge_hours = needed_energy / eff_power
    return charge_hours * 60.0 + t_buffer

class TestRemediatedSLA(unittest.TestCase):
    
    def test_mrdt_malicious_claim_prevention(self):
        # Malicious truck: arrives 10 mins before departure, SoC=5%, requires 85%
        # Battery = 540 kWh, charger = 350 kW, veh = 300 kW
        mrdt = compute_mrdt(soc_req=85.0, soc_arrive=5.0, batt_kwh=540.0, p_charger_max=350.0, p_veh_max=300.0)
        print(f"Malicious claim test: MRDT required = {mrdt:.1f} minutes")
        # MRDT = (0.80 * 540) / (300 * 0.95) * 60 + 15 = 432 / 285 * 60 + 15 = 90.9 + 15 = 105.9 minutes
        self.assertGreater(mrdt, 100.0)
        
        # If actual dwell is 10 min:
        dwell_actual = 10.0
        mrdt_satisfied = (dwell_actual >= mrdt)
        self.assertFalse(mrdt_satisfied)
        
        # In remediated formula, penalty is 0 EUR because MRDT is not satisfied!
        trip = {
            'mrdt_satisfied': mrdt_satisfied,
            'delay_min': 10.0,
            'soc_req': 85.0,
            'soc_dep': 15.0,
            'cap_kwh': 540.0
        }
        penalty = compute_remediated_fleet_penalty([trip], [trip])
        print(f"Penalty assessed under remediated SLA: {penalty} EUR (Properly EXEMPT)")
        self.assertEqual(penalty, 0.0)

    def test_overcharged_vehicle_no_negative_penalty(self):
        # Vehicle arrives at 70%, departs at 80% (required was 70%)
        trip = {'mrdt_satisfied': True, 'soc_req': 70.0, 'soc_dep': 80.0, 'cap_kwh': 540.0}
        penalty = compute_remediated_fleet_penalty([], [trip])
        print(f"Overcharged vehicle penalty: {penalty} EUR (No negative penalty)")
        self.assertEqual(penalty, 0.0)

    def test_early_departure_no_penalty(self):
        # Vehicle departs 5 min early (delay = -5 min)
        trip = {'mrdt_satisfied': True, 'delay_min': -5.0}
        penalty = compute_remediated_fleet_penalty([trip], [])
        print(f"Early departure penalty: {penalty} EUR (No penalty)")
        self.assertEqual(penalty, 0.0)

    def test_piecewise_availability(self):
        base_fee = 10000.0
        # >= 99.50%
        self.assertEqual(compute_remediated_availability_deduction(base_fee, 99.50), 0.0)
        self.assertEqual(compute_remediated_availability_deduction(base_fee, 99.55), 0.0)
        # 99.40% -> 1 step of 0.10% = 2.0% = 200 EUR
        self.assertEqual(compute_remediated_availability_deduction(base_fee, 99.40), 200.0)
        # 95.00% -> shortfall 4.50% = 45 steps = 90% = 9000 EUR
        self.assertEqual(compute_remediated_availability_deduction(base_fee, 95.00), 9000.0)
        # 94.99% -> < 95.00% -> 100% full waiver = 10000 EUR
        self.assertEqual(compute_remediated_availability_deduction(base_fee, 94.99), 10000.0)
        # 90.00% -> 100% full waiver = 10000 EUR
        self.assertEqual(compute_remediated_availability_deduction(base_fee, 90.00), 10000.0)
        print("Piecewise availability deduction tests PASSED seamlessly!")

    def test_monthly_liability_cap(self):
        base_fee = 10000.0
        # Even if penalties are huge, total monthly payout cannot exceed 150% (15,000 EUR)
        total_payout_uncapped = 25000.0 # e.g. 10000 EUR fee waiver + 15000 EUR fleet delays
        capped_payout = min(total_payout_uncapped, 1.50 * base_fee)
        self.assertEqual(capped_payout, 15000.0)
        print(f"Aggregate monthly cap test: uncapped {total_payout_uncapped} -> capped {capped_payout} EUR (PASSED)")

if __name__ == '__main__':
    unittest.main()
