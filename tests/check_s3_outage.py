import os
import pandas as pd

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kempower-challenge", "kempower-challenge-data")

arrivals = pd.read_csv(os.path.join(data_dir, "public_arrivals.csv"))
s3_arr = arrivals[(arrivals['site_id'] == 'S3') & (arrivals['ts'].str.startswith('2026-11-13'))]
print(f"Total public arrivals at S3 on 2026-11-13: {len(s3_arr)}")
s3_arr_outage = s3_arr[(s3_arr['ts'] >= '2026-11-13T11:00:00') & (s3_arr['ts'] <= '2026-11-13T13:00:00')]
print(f"Arrivals during outage (11:00-13:00): {len(s3_arr_outage)}")
print("Outcomes during outage:")
print(s3_arr_outage['outcome'].value_counts())
print("\nSample arrivals during outage:")
print(s3_arr_outage.head(10).to_string())

cfg = pd.read_csv(os.path.join(data_dir, "site_config.csv"))
print("\nS3 site_config:")
print(cfg[cfg['site_id'] == 'S3'].to_string())
