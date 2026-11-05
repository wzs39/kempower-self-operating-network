import os
import pandas as pd
import numpy as np

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kempower-challenge", "kempower-challenge-data")

# Load fleet schedule and vehicles
sched = pd.read_csv(os.path.join(data_dir, "fleet_schedule.csv"))
vehicles = pd.read_csv(os.path.join(data_dir, "vehicles.csv"))
chargers = pd.read_csv(os.path.join(data_dir, "chargers.csv"))
cabinets = pd.read_csv(os.path.join(data_dir, "power_cabinets.csv"))
sites = pd.read_csv(os.path.join(data_dir, "sites.csv"))

s2_site = sites[sites['site_id'] == 'S2']
s2_chargers = chargers[chargers['site_id'] == 'S2']
s2_cabinets = cabinets[cabinets['site_id'] == 'S2']

print("S2 site:", s2_site[['site_id', 'grid_limit_kw']])
print("S2 cabinets:\n", s2_cabinets)
print("S2 chargers:\n", s2_chargers)

# Check all vehicles present at S2 on 2026-11-13 between 12:00 and 20:00
sched['arrive_dt'] = pd.to_datetime(sched['arrive_ts'])
sched['depart_dt'] = pd.to_datetime(sched['depart_ts'])

s2_all = sched[sched['site_id'] == 'S2'].copy()
# Filter for vehicles active during 2026-11-13
s2_active_13 = s2_all[
    (s2_all['arrive_dt'] <= pd.to_datetime('2026-11-13 19:00:00+02:00')) &
    (s2_all['depart_dt'] >= pd.to_datetime('2026-11-13 14:00:00+02:00'))
].sort_values('depart_dt')

s2_active_13 = s2_active_13.merge(vehicles, on='vehicle_id', how='left')
print("\nActive vehicles at S2 between 14:00 and 19:00 on 2026-11-13:")
print(s2_active_13[['vehicle_id', 'arrive_ts', 'arrive_soc_pct', 'depart_ts', 'required_soc_pct', 'battery_kwh', 'max_charge_kw']].to_string())

# Energy required for T01-T04:
print("\n--- Energy calculations for T01-T04 ---")
for v in ['T01', 'T02', 'T03', 'T04']:
    row = s2_active_13[s2_active_13['vehicle_id'] == v].iloc[0]
    batt = row['battery_kwh']
    arr_soc = row['arrive_soc_pct']
    req_soc = row['required_soc_pct']
    delta_soc = req_soc - arr_soc
    needed_kwh = delta_soc / 100.0 * batt
    print(f"{v}: Arrive {row['arrive_ts'][11:16]} ({arr_soc}%), Depart {row['depart_ts'][11:16]} ({req_soc}%), Delta SoC: {delta_soc:.1f}%, Needed kWh: {needed_kwh:.2f} kWh")

# Total energy needed for T01-T04
total_needed = sum([(row['required_soc_pct'] - row['arrive_soc_pct'])/100.0 * row['battery_kwh'] 
                    for _, row in s2_active_13[s2_active_13['vehicle_id'].isin(['T01', 'T02', 'T03', 'T04'])].iterrows()])
print(f"\nTotal energy needed for T01-T04: {total_needed:.2f} kWh")

# Check time available in curtailment (16:00 to 19:00):
# From 16:00 to 17:30 (T01): 1.5 h -> at 400 kW total energy = 600 kWh
# From 16:00 to 17:45 (T02): 1.75 h -> 700 kWh
# From 16:00 to 18:00 (T03): 2.0 h -> 800 kWh
# From 16:00 to 18:15 (T04): 2.25 h -> 900 kWh
print(f"Total grid energy available under 400 kW from 16:00 to 18:15 (2.25 h): {400 * 2.25} kWh")
