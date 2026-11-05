import os
import pandas as pd

data_dir = r"C:\Users\qwe\Desktop\hackson\kempower-challenge\kempower-challenge-data"

print("==================================================")
print("PART 1: S1 C1-3 THERMAL FAILURE (F015 / F016)")
print("==================================================")
faults = pd.read_csv(os.path.join(data_dir, "faults.csv"))
s1_faults = faults[faults['site_id'] == 'S1']
print("S1 Faults:")
print(s1_faults.to_string())

chargers = pd.read_csv(os.path.join(data_dir, "chargers.csv"))
s1_chargers = chargers[chargers['site_id'] == 'S1']
print("\nS1 Chargers:")
print(s1_chargers.to_string())

cabinets = pd.read_csv(os.path.join(data_dir, "power_cabinets.csv"))
s1_cabinets = cabinets[cabinets['site_id'] == 'S1']
print("\nS1 Cabinets:")
print(s1_cabinets.to_string())

sites = pd.read_csv(os.path.join(data_dir, "sites.csv"))
s1_site = sites[sites['site_id'] == 'S1']
print("\nS1 Site Config:")
print(s1_site.to_string())

print("==================================================")
print("PART 2: S2 DSO CURTAILMENT (G1) & TRUCKS T01-T04")
print("==================================================")
grid_events = pd.read_csv(os.path.join(data_dir, "grid_events.csv"))
print("Grid events for S2:")
print(grid_events[grid_events['site_id'] == 'S2'].to_string())

schedule = pd.read_csv(os.path.join(data_dir, "fleet_schedule.csv"))
vehicles = pd.read_csv(os.path.join(data_dir, "vehicles.csv"))

s2_sched_13 = schedule[(schedule['site_id'] == 'S2') & (schedule['depart_ts'].str.startswith('2026-11-13'))]
s2_sched_13 = s2_sched_13.merge(vehicles, on='vehicle_id', how='left')
print("\nS2 Fleet Schedule on 2026-11-13:")
print(s2_sched_13[['vehicle_id', 'arrive_ts', 'arrive_soc_pct', 'depart_ts', 'required_soc_pct', 'battery_kwh', 'max_charge_kw']].sort_values('depart_ts').to_string())

print("\nAll S2 Fleet Schedule on 2026-11-13 (including arrivals on 13th):")
s2_sched_all = schedule[(schedule['site_id'] == 'S2') & ((schedule['arrive_ts'].str.startswith('2026-11-13')) | (schedule['depart_ts'].str.startswith('2026-11-13')))]
s2_sched_all = s2_sched_all.merge(vehicles, on='vehicle_id', how='left')
print(s2_sched_all[['vehicle_id', 'arrive_ts', 'arrive_soc_pct', 'depart_ts', 'required_soc_pct', 'battery_kwh', 'max_charge_kw']].sort_values('arrive_ts').to_string())

print("\nDepartures baseline for S2 on 2026-11-13:")
dep_base = pd.read_csv(os.path.join(data_dir, "departures_baseline.csv"))
s2_dep_13 = dep_base[(dep_base['site_id'] == 'S2') & (dep_base['depart_ts'].str.startswith('2026-11-13'))]
print(s2_dep_13.to_string())

print("==================================================")
print("PART 3: S3 OFFLINE & TRANSFORMER LIMIT")
print("==================================================")
s3_site = sites[sites['site_id'] == 'S3']
print("S3 Site config:")
print(s3_site.to_string())

s3_cabinets = cabinets[cabinets['site_id'] == 'S3']
print("\nS3 Cabinets:")
print(s3_cabinets.to_string())

s3_chargers = chargers[chargers['site_id'] == 'S3']
print("\nS3 Chargers:")
print(s3_chargers.to_string())

outages = pd.read_csv(os.path.join(data_dir, "connectivity_outages.csv"))
s3_outages = outages[outages['site_id'] == 'S3']
print("\nS3 Outages:")
print(s3_outages.to_string())
