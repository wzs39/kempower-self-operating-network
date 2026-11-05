"""
Kempower Self-Operating Charging Network - Dataset Loader & Empirical Fact Extractor
Module: src/sim/data_loader.py

Provides zero-hardcoded-path access to all 45 official CSV files in
kempower-challenge/kempower-challenge-data and deterministic ground-truth queries.
"""

import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
import pandas as pd

from src.utils.paths import get_data_dir, resolve_csv_path


class KempowerDataLoader:
    """Loads and caches official CSV files from kempower-challenge-data."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir: Path = data_dir or get_data_dir()
        self._df_cache: Dict[str, pd.DataFrame] = {}

    def list_csv_files(self) -> List[Path]:
        """Returns sorted list of all CSV files in the dataset directory (45 files)."""
        return sorted(self.data_dir.glob("*.csv"))

    def load_df(self, filename: str) -> pd.DataFrame:
        """Loads and caches a CSV file as a pandas DataFrame."""
        if filename not in self._df_cache:
            path = self.data_dir / filename if (self.data_dir / filename).exists() else resolve_csv_path(filename)
            self._df_cache[filename] = pd.read_csv(path)
        return self._df_cache[filename]

    def get_vehicle_capacities(self) -> Dict[str, float]:
        """Returns mapping vehicle_id -> battery_kwh from vehicles.csv."""
        df_v = self.load_df("vehicles.csv")
        return {str(r["vehicle_id"]): float(r["battery_kwh"]) for _, r in df_v.iterrows()}

    def get_missed_departures_summary(self) -> Dict[str, Any]:
        """
        Computes exact missed departure statistics from departures_baseline.csv + vehicles.csv:
        - 14-day total missed departures: 24
        - 2026-11-13 Scenario Day missed departures: 13
          * S1: 4 buses (B18: 328 kWh, B20: 328 kWh, B04: 328 kWh, B09: 28 kWh -> 1,012.00 kWh)
          * S2: 4 trucks (T01: 44.82 kWh, T02: 111.24 kWh, T03: 49.14 kWh, T04: 78.30 kWh -> 283.50 kWh)
          * S5: 5 buses (B28: 92.25 kWh, B35: 129.60 kWh, B33: 133.20 kWh, B34: 95.85 kWh, B27: 58.05 kWh -> 508.95 kWh)
        """
        df_dep = self.load_df("departures_baseline.csv")
        cap_map = self.get_vehicle_capacities()

        if "below_required" in df_dep.columns:
            missed_all = df_dep[df_dep["below_required"] == 1].copy()
        else:
            missed_all = df_dep[df_dep["on_time"].astype(str).str.lower() == "false"].copy()

        ts_col = "depart_ts" if "depart_ts" in missed_all.columns else "planned_depart"
        missed_1113 = missed_all[missed_all[ts_col].astype(str).str.startswith("2026-11-13")].copy()

        site_records: Dict[str, List[Dict[str, Any]]] = {"S1": [], "S2": [], "S5": []}
        site_deficit_kwh: Dict[str, float] = {"S1": 0.0, "S2": 0.0, "S5": 0.0}

        for _, row in missed_1113.iterrows():
            sid = str(row["site_id"])
            vid = str(row["vehicle_id"])
            batt = cap_map.get(vid, 400.0)
            req_soc = float(row["required_soc_pct"])
            dep_soc = float(row["depart_soc_pct"])
            def_kwh = round((req_soc - dep_soc) / 100.0 * batt, 2)
            rec = {
                "site_id": sid,
                "vehicle_id": vid,
                "depart_ts": str(row[ts_col]),
                "required_soc_pct": req_soc,
                "depart_soc_pct": dep_soc,
                "battery_kwh": batt,
                "deficit_kwh": def_kwh,
            }
            site_records.setdefault(sid, []).append(rec)
            site_deficit_kwh[sid] = round(site_deficit_kwh.get(sid, 0.0) + def_kwh, 2)

        return {
            "total_missed_14d": int(len(missed_all)),
            "scenario_day_missed_1113": int(len(missed_1113)),
            "s1_missed_count": len(site_records["S1"]),
            "s2_missed_count": len(site_records["S2"]),
            "s5_missed_count": len(site_records["S5"]),
            "s1_deficit_kwh": site_deficit_kwh["S1"],
            "s2_deficit_kwh": site_deficit_kwh["S2"],
            "s5_deficit_kwh": site_deficit_kwh["S5"],
            "total_deficit_1113_kwh": round(sum(site_deficit_kwh.values()), 2),
            "site_records_1113": site_records,
        }

    def verify_network_zero_over_limit(self) -> Dict[str, Any]:
        """Verifies zero grid limit violations across all 134,400 rows of network_site_power.csv (Issues A4, C3)."""
        df_nsp = self.load_df("network_site_power.csv")
        if "over_limit" in df_nsp.columns:
            over_col = df_nsp["over_limit"].astype(str).str.lower()
            over_count = int((over_col == "true").sum() + (over_col == "1").sum())
        else:
            over_count = int((df_nsp["grid_kw"] > df_nsp["grid_limit_kw"] + 1e-4).sum())
        return {
            "total_rows": int(len(df_nsp)),
            "over_limit_count": over_count,
            "zero_over_limit_verified": (over_count == 0),
        }
