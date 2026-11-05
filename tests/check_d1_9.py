import os
import pandas as pd

data_dir = r"C:\Users\qwe\Desktop\hackson\kempower-challenge\kempower-challenge-data"
df = pd.read_csv(os.path.join(data_dir, "telemetry_1min.csv"))
s1_d1_9 = df[(df['charger_id'] == 'D1-9') & (df['ts'] >= '2026-11-13T01:48:00') & (df['ts'] <= '2026-11-13T02:30:00')]
print(s1_d1_9.to_string())
