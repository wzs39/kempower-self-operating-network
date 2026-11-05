import os
import pandas as pd

data_dir = r"C:\Users\qwe\Desktop\hackson\kempower-challenge\kempower-challenge-data"

for name in ["sites", "chargers", "power_cabinets", "grid_events", "faults", "fleet_schedule", "vehicles", "departures_baseline"]:
    df = pd.read_csv(os.path.join(data_dir, f"{name}.csv"))
    print(f"\n=== {name}.csv ===")
    print("Columns:", list(df.columns))
    print(df.head(2))
