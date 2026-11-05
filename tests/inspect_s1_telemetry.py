import os
import pandas as pd

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kempower-challenge", "kempower-challenge-data")

telemetry_path = os.path.join(data_dir, "telemetry_1min.csv")
df = pd.read_csv(telemetry_path)
print(f"Total rows in telemetry_1min: {len(df)}")
print("Chargers in telemetry_1min:", df['charger_id'].unique())
print("Time range:", df['ts'].min(), "to", df['ts'].max())

# Filter for S1 (D1-*)
s1_tel = df[df['charger_id'].str.startswith('D1-')].copy()
print(f"Total S1 rows: {len(s1_tel)}")

# Look around 01:40 to 02:40 on 2026-11-13
sub_time = s1_tel[(s1_tel['ts'] >= '2026-11-13T01:40:00') & (s1_tel['ts'] <= '2026-11-13T02:40:00')].sort_values(['ts', 'charger_id'])
print("\nTelemetry around 01:40 to 02:40 on 2026-11-13:")
print(sub_time.head(40).to_string())

# Summarize cabinet temp and fan rpm by charger
print("\nSummary around failure time (01:45 to 02:30):")
fail_window = s1_tel[(s1_tel['ts'] >= '2026-11-13T01:45:00') & (s1_tel['ts'] <= '2026-11-13T02:30:00')]
print(fail_window.groupby('charger_id')[['power_kw', 'cabinet_temp_c', 'fan_rpm']].mean())
