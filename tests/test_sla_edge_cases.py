import unittest

def compute_fleet_penalty(delayed_trips, undercharged_trips, p_base=250.0, c_min=5.0, c_energy=1.5):
    """
    SLA Formula 4.1:
    Penalty_fleet = sum_{i in delayed_trips} [ P_base + max(0, t_delay_min,i - 15) * C_min ]
                  + sum_{j in undercharged} [ (SoC_req,j - SoC_dep,j) * Cap_batt,j * C_energy ]
    """
    total_penalty = 0.0
    for trip in delayed_trips:
        t_delay = trip['delay_min']
        # If implementation strictly follows math formula:
        delay_cost = p_base + max(0.0, t_delay - 15.0) * c_min
        total_penalty += delay_cost
        
    for trip in undercharged_trips:
        soc_req = trip['soc_req']
        soc_dep = trip['soc_dep']
        cap_kwh = trip['cap_kwh']
        # delta energy
        delta_soc = (soc_req - soc_dep) / 100.0 if soc_req > 1.0 else (soc_req - soc_dep)
        energy_penalty = delta_soc * cap_kwh * c_energy
        total_penalty += energy_penalty
        
    return total_penalty

def compute_availability_deduction(monthly_base_fee, availability_actual):
    """
    SLA Formula 4.2:
    Fee_deduction = Monthly Base Fee * min(100%, max(0, (99.50% - Availability_actual) / 0.10%) * 2.0%)
    """
    shortfall = 99.50 - availability_actual
    if shortfall <= 0:
        return 0.0
    steps = shortfall / 0.10
    deduction_pct = min(100.0, steps * 2.0)
    return monthly_base_fee * (deduction_pct / 100.0)

class TestSLAFormulas(unittest.TestCase):
    
    def test_zero_delay_in_delayed_set(self):
        # Edge case 1: Trip in delayed_trips with delay_min = 0 (arrived exactly at deadline)
        trips = [{'delay_min': 0.0}]
        penalty = compute_fleet_penalty(trips, [])
        # If delayed_trips includes 0-delay, operator is fined 250 EUR!
        print(f"Edge Case 1 (0 min delay in delayed_trips): Penalty = {penalty} EUR")
        self.assertEqual(penalty, 250.0)
        
    def test_negative_delay(self):
        # Edge case 2: Trip departed 5 minutes EARLY (delay_min = -5.0)
        trips = [{'delay_min': -5.0}]
        penalty = compute_fleet_penalty(trips, [])
        print(f"Edge Case 2 (-5 min delay in delayed_trips): Penalty = {penalty} EUR")
        self.assertEqual(penalty, 250.0) # Flat 250 penalty triggered if membership check is flawed!
        
    def test_overcharged_vehicle(self):
        # Edge case 3: Vehicle departed with higher SoC than required (e.g. 80% vs 70%)
        trips = [{'soc_req': 70.0, 'soc_dep': 80.0, 'cap_kwh': 540.0}]
        penalty = compute_fleet_penalty([], trips)
        print(f"Edge Case 3 (Overcharged vehicle in set): Penalty = {penalty} EUR")
        # Gives NEGATIVE penalty: -81.0 EUR!
        self.assertLess(penalty, 0.0)
        
    def test_availability_boundary(self):
        # Test availability formula at 99.50%, 95.00%, 94.00%, 0.0%
        base_fee = 10000.0 # 10,000 EUR
        d_995 = compute_availability_deduction(base_fee, 99.50)
        d_994 = compute_availability_deduction(base_fee, 99.40)
        d_950 = compute_availability_deduction(base_fee, 95.00)
        d_945 = compute_availability_deduction(base_fee, 94.50)
        d_0 = compute_availability_deduction(base_fee, 0.0)
        
        print(f"Availability 99.50%: Deduction = {d_995} EUR (0%)")
        print(f"Availability 99.40%: Deduction = {d_994} EUR (2%)")
        print(f"Availability 95.00%: Deduction = {d_950} EUR (90%)")
        print(f"Availability 94.50%: Deduction = {d_945} EUR (100%)")
        print(f"Availability 0.00%: Deduction = {d_0} EUR (100%)")
        
        self.assertEqual(d_995, 0.0)
        self.assertEqual(d_994, 200.0)
        self.assertEqual(d_950, 9000.0) # Notice at 95.00%, deduction is 90%, NOT 100%!
        self.assertEqual(d_945, 10000.0) # 100% deduction reached at 94.50%, not 95.00%!

if __name__ == '__main__':
    unittest.main()
