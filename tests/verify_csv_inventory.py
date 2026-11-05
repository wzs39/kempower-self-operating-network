import os
import glob
import pandas as pd

DATA_DIR = r"C:\Users\qwe\Desktop\hackson\kempower-challenge\kempower-challenge-data"

# Claims in Section 6.1 of Kempower_Self_Operating_Network_Comprehensive_Survey.md
claimed_stats = {
    "prices.csv": (1344, 4),
    "zone_prices.csv": (1344, 14),
    "tariffs.csv": (2, 6),
    "reserve_market_prices.csv": (2016, 4),
    "co2_intensity.csv": (4368, 3),
    "pv_production.csv": (1344, 3),
    "grid_capacity.csv": (95, 8),
    "grid_events.csv": (2, 8),
    "vehicles.csv": (50, 8),
    "fleet_schedule.csv": (656, 7),
    "departures_baseline.csv": (606, 6),
    "corridors.csv": (12, 8),
    "traffic_points.csv": (2, 3),
    "weather.csv": (8736, 4),
    "sites.csv": (5, 10),
    "power_cabinets.csv": (12, 4),
    "chargers.csv": (46, 6),
    "telemetry.csv": (56448, 8),
    "telemetry_1min.csv": (9000, 6),
    "faults.csv": (19, 10),
    "network_faults_daily.csv": (173, 5),
    "service_tickets.csv": (14, 11),
    "technicians.csv": (3, 5),
    "travel_times.csv": (15, 3),
    "spare_parts.csv": (6, 6),
    "firmware.csv": (100, 3),
    "commissioning_steps.csv": (9, 12),
    "commissioning_history.csv": (108, 8),
    "site_config.csv": (199, 4),
    "candidate_locations.csv": (20, 13),
    "equipment_costs.csv": (10, 3),
    "traffic_counts.csv": (2688, 5),
    "public_arrivals.csv": (3939, 9),
    "price_changes.csv": (8, 4),
    "network_site_power.csv": (134400, 13),
    "contracts.csv": (29, 8),
    "growth_forecast.csv": (60, 4),
    "baseline_kpis.csv": (10, 11),
    "network_kpis.csv": (95, 13),
    "connectivity_outages.csv": (13, 3),
    "operations_log.csv": (1601, 5)
}

print(f"Total files listed in table: {len(claimed_stats)}")

actual_stats = {}
files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
for f in files:
    fname = os.path.basename(f)
    df = pd.read_csv(f)
    actual_stats[fname] = (df.shape[0], df.shape[1])

print(f"Total files in directory: {len(actual_stats)}")

# Check missing from table
missing_from_table = set(actual_stats.keys()) - set(claimed_stats.keys())
print(f"Files in dir but NOT in table: {missing_from_table}")

# Check mismatches
mismatches = []
for fname, (c_rows, c_cols) in claimed_stats.items():
    if fname not in actual_stats:
        mismatches.append((fname, f"Claimed {c_rows}x{c_cols}", "NOT FOUND IN DIR"))
    else:
        a_rows, a_cols = actual_stats[fname]
        if a_rows != c_rows or a_cols != c_cols:
            mismatches.append((fname, f"Claimed {c_rows}x{c_cols}", f"Actual {a_rows}x{a_cols}"))

print(f"\nMismatches count: {len(mismatches)}")
for m in mismatches:
    print(f"  {m[0]}: {m[1]} vs {m[2]}")

if not mismatches:
    print("ALL 41 LISTED FILES IN SECTION 6.1 MATCH EXACT SHAPES (ROWS & COLS)!")

# Wait, why did the table list 41 files when there are 45 files?
# Let's inspect the remaining 4 files!
print("\nMissing from table details:")
for f in missing_from_table:
    print(f"  {f}: {actual_stats[f]}")
