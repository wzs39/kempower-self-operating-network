import os
import pandas as pd

data_dir = r"C:\Users\qwe\Desktop\hackson\kempower-challenge\kempower-challenge-data"
site_cfg = pd.read_csv(os.path.join(data_dir, "site_config.csv"))
print("BESS or battery in site_config:")
print(site_cfg[site_cfg['parameter'].str.contains('bess|battery|storage', case=False, na=False)])

print("\nAll site_config parameters:")
print(site_cfg['parameter'].unique())

print("\nSites info:")
sites = pd.read_csv(os.path.join(data_dir, "sites.csv"))
print(sites.to_string())
