import os
import pandas as pd

data_dir = r"C:\Users\qwe\Desktop\hackson\kempower-challenge\kempower-challenge-data"
df = pd.read_csv(os.path.join(data_dir, "telemetry_1min.csv"))
s1_later = df[(df['charger_id'].str.startswith('D1-')) & (df['ts'] >= '2026-11-13T02:20:00') & (df['ts'] <= '2026-11-13T04:00:00')]
print(s1_later[s1_later['power_kw'] > 0][['ts', 'charger_id', 'power_kw', 'cabinet_temp_c', 'error_events']].head(30).to_string())

# Check when power drops to 0
for ch in ['D1-9', 'D1-10', 'D1-11', 'D1-12']:
    sub = df[(df['charger_id'] == ch) & (df['ts'] >= '2026-11-13T02:00:00') & (df['ts'] <= '2026-11-13T06:30:00')]
    nonzero = sub[sub['power_kw'] > 0]
    print(f"{ch}: max power {sub['power_kw'].max():.1f}, nonzero points: {len(nonzero)}, last nonzero: {nonzero['ts'].max() if len(nonzero) else 'None'}")
