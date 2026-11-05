import pandas as pd
import numpy as np

# Simulation parameters
# T01-T04 parameters
trucks = {
    'T01': {'arrive': 14*60 + 25, 'depart': 17*60 + 30, 'soc_arr': 0.185, 'soc_req': 0.70, 'batt_kwh': 540, 'max_kw': 300}, # charger max is 300 kW
    'T02': {'arrive': 14*60 + 45, 'depart': 17*60 + 45, 'soc_arr': 0.100, 'soc_req': 0.70, 'batt_kwh': 540, 'max_kw': 300},
    'T03': {'arrive': 14*60 + 20, 'depart': 18*60 + 0,  'soc_arr': 0.100, 'soc_req': 0.70, 'batt_kwh': 540, 'max_kw': 300},
    'T04': {'arrive': 14*60 + 45, 'depart': 18*60 + 15, 'soc_arr': 0.100, 'soc_req': 0.70, 'batt_kwh': 540, 'max_kw': 300},
}

def run_edf_sim(start_charge_min, allow_precharge=True, max_kw_per_truck=300):
    # Time steps: 1 minute from 14:00 (840) to 19:00 (1140)
    # Curtailment: 16:00 (960) to 19:00 (1140) limit = 400 kW. Before 960 limit = 800 kW.
    soc = {t: trucks[t]['soc_arr'] for t in trucks}
    energy_delivered = {t: 0.0 for t in trucks}
    
    log = []
    
    for m in range(840, 1140):
        # Grid limit at minute m
        grid_limit = 400.0 if m >= 960 else 800.0
        
        # Determine active trucks present and needing charge
        active = []
        for t, d in trucks.items():
            if allow_precharge:
                present = (m >= d['arrive']) and (m < d['depart'])
            else:
                present = (m >= max(d['arrive'], 960)) and (m < d['depart'])
            
            if present and soc[t] < d['soc_req']:
                active.append(t)
        
        # Sort by EDF (earliest deadline first: depart time)
        active.sort(key=lambda t: trucks[t]['depart'])
        
        # Allocate power greedily by EDF
        rem_grid = grid_limit
        power_alloc = {}
        for t in active:
            # Need power to reach soc_req
            needed_kwh = (trucks[t]['soc_req'] - soc[t]) * trucks[t]['batt_kwh']
            p_max = min(rem_grid, max_kw_per_truck)
            # max energy in 1 minute = p_max / 60
            if needed_kwh > 0:
                p_actual = min(p_max, needed_kwh * 60)
                power_alloc[t] = p_actual
                rem_grid -= p_actual
            else:
                power_alloc[t] = 0.0
        
        # Deliver energy
        for t, p in power_alloc.items():
            kwh = p / 60.0
            energy_delivered[t] += kwh
            soc[t] += kwh / trucks[t]['batt_kwh']
            
    return soc, energy_delivered

print("=== SCENARIO A: STRICT CURTAILMENT ONLY (16:00-19:00, NO PRE-CHARGE) ===")
print("Dispensers capped at 300 kW:")
soc_a, kwh_a = run_edf_sim(960, allow_precharge=False, max_kw_per_truck=300)
for t in trucks:
    req = trucks[t]['soc_req']
    print(f"{t}: Final SoC: {soc_a[t]*100:.2f}% (Req: {req*100:.0f}%), Delivered: {kwh_a[t]:.1f} kWh, Success: {soc_a[t] >= req}")

print("\nDispensers uncapped at 350 kW:")
soc_a350, kwh_a350 = run_edf_sim(960, allow_precharge=False, max_kw_per_truck=350)
for t in trucks:
    req = trucks[t]['soc_req']
    print(f"{t}: Final SoC: {soc_a350[t]*100:.2f}% (Req: {req*100:.0f}%), Delivered: {kwh_a350[t]:.1f} kWh, Success: {soc_a350[t] >= req}")

print("\n=== SCENARIO B: WITH PRE-CHARGING UPON ARRIVAL (14:20-16:00 at 800 kW) ===")
soc_b, kwh_b = run_edf_sim(840, allow_precharge=True, max_kw_per_truck=300)
for t in trucks:
    req = trucks[t]['soc_req']
    print(f"{t}: Final SoC: {soc_b[t]*100:.2f}% (Req: {req*100:.0f}%), Delivered: {kwh_b[t]:.1f} kWh, Success: {soc_b[t] >= req}")
