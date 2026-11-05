import os
import glob
import pandas as pd

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kempower-challenge", "kempower-challenge-data")
files = glob.glob(os.path.join(data_dir, "*.csv"))
print(f"Total CSVs found: {len(files)}")

# Check key files
for name in ["sites", "chargers", "power_cabinets", "site_config", "faults", "fleet_schedule", "vehicles", "departures_baseline", "grid_curtailments", "curtailments", "connectivity_outages", "tariffs"]:
    target = os.path.join(data_dir, f"{name}.csv")
    if os.path.exists(target):
        df = pd.read_csv(target)
        print(f"=== {name}.csv (shape: {df.shape}) ===")
        print(df.head(2))
    else:
        # search for similar
        matches = [f for f in files if name in os.path.basename(f)]
        if matches:
            print(f"Matches for {name}: {[os.path.basename(m) for m in matches]}")
        else:
            print(f"No match for {name}")
