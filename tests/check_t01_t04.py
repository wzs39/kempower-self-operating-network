import os
import pandas as pd

data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kempower-challenge", "kempower-challenge-data")
sched = pd.read_csv(os.path.join(data_dir, "fleet_schedule.csv"))
s2_sched = sched[(sched['site_id'] == 'S2') & (sched['vehicle_id'].isin(['T01', 'T02', 'T03', 'T04']))]
print(s2_sched.sort_values(['vehicle_id', 'arrive_ts']).to_string())
