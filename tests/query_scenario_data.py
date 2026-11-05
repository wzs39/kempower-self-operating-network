import os
import pandas as pd
import numpy as np

data_dir = r"C:\Users\qwe\Desktop\hackson\kempower-challenge\kempower-challenge-data"

print("--- 1. S1 Cabinets and Chargers ---")
chargers = pd.read_csv(os.path.join(data_dir, "chargers.csv"))
cabinets = pd.read_csv(os.path.join(data_dir, "power_cabinets.csv"))
sites = pd.read_csv(os.path.join(data_dir, "sites.csv"))
print("Sites:")
print(sites[sites['site_id'].isin(['S1', 'S2', 'S3'])][['site_id', 'name', 'grid_limit_kw', 'tariff_id', 'pv_kwp']])

print("\nCabinets S1:")
print(cabinets[cabinets['site_id'] == 'S1'])

print("\nChargers S1:")
print(chargers[chargers['site_id'] == 'S1'])

print("\n--- 2. Faults S1 (F015, F016) ---")
faults = pd.read_csv(os.path.join(data_dir, "faults.csv"))
print(faults[faults['site_id'] == 'S1'])

print("\n--- 3. Grid Events S2 ---")
grid_events = pd.read_csv(os.path.join(data_dir, "grid_events.csv"))
print(grid_events)

print("\n--- 4. Vehicles & Fleet Schedule S2 ---")
vehicles = pd.read_csv(os.path.join(data_dir, "vehicles.csv"))
schedule = pd.read_csv(os.path.join(data_dir, "fleet_schedule.csv"))
print("S2 Vehicles in fleet_schedule:")
s2_sched = schedule[schedule['site_id'] == 'S2']
print(f"Total S2 schedule entries: {len(s2_sched)}")
print(s2_sched.head(10))

print("\nCheck departures_baseline for S2 on 2026-11-13:")
dep_base = pd.read_csv(os.path.join(data_dir, "departures_baseline.csv"))
s2_dep = dep_base[(dep_base['site_id'] == 'S2') & (dep_base['depart_ts'].str.startswith('2026-11-13'))]
print(s2_dep)
