import os
import pandas as pd

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kempower-challenge", "kempower-challenge-data")
power = pd.read_csv(os.path.join(data_dir, "site_power_baseline.csv"))
print("Columns of site_power_baseline:", power.columns)

# Filter for S1 on 2026-11-13
s1_p = power[(power['site_id'] == 'S1') & (power['ts'].str.startswith('2026-11-13'))]
print("S1 power on 2026-11-13 around 01:00 to 03:00:")
print(s1_p[(s1_p['ts'] >= '2026-11-13T01:00:00') & (s1_p['ts'] <= '2026-11-13T03:00:00')].to_string())

print("\nSummary of S1 power on 2026-11-13:")
print("Max power:", s1_p['power_kw'].max())
print("Mean power:", s1_p['power_kw'].mean())
