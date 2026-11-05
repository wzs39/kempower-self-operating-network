import os
import glob
import pandas as pd
import numpy as np

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "kempower-challenge", "kempower-challenge-data")

def test_total_csv_rows():
    print("=" * 60)
    print("1. TOTAL ROWS AND COLUMNS ACROSS 45 CSVs")
    print("=" * 60)
    files = sorted(glob.glob(os.path.join(DATA_DIR, "*.csv")))
    print(f"Total CSV files found: {len(files)}")
    
    total_data_rows = 0
    total_file_lines = 0
    file_stats = []
    
    for f in files:
        fname = os.path.basename(f)
        # count lines with open
        with open(f, "r", encoding="utf-8", errors="ignore") as fp:
            lines = sum(1 for _ in fp)
        total_file_lines += lines
        
        # count with pandas
        try:
            df = pd.read_csv(f)
            nrows, ncols = df.shape
            total_data_rows += nrows
            file_stats.append((fname, nrows, ncols, lines))
        except Exception as e:
            file_stats.append((fname, -1, -1, lines, str(e)))
            
    print(f"Total data rows (excluding header): {total_data_rows}")
    print(f"Total raw lines (including header): {total_file_lines}")
    print(f"Claim in report: 240,635 rows")
    diff = total_data_rows - 240635
    print(f"Difference (data rows - 240635): {diff}")
    diff_lines = total_file_lines - 240635
    print(f"Difference (raw lines - 240635): {diff_lines}")
    
    return file_stats, total_data_rows, total_file_lines

def test_price_surge():
    print("\n" + "=" * 60)
    print("2. PRICE SURGE VERIFICATION (Claim: 799.30 €/MWh at 2026-11-13 18:00)")
    print("=" * 60)
    prices_path = os.path.join(DATA_DIR, "prices.csv")
    df = pd.read_csv(prices_path)
    print(f"prices.csv columns: {list(df.columns)}")
    max_spot = df["spot_eur_mwh"].max()
    max_row = df.loc[df["spot_eur_mwh"] == max_spot]
    print(f"Max spot price: {max_spot} EUR/MWh")
    print(f"Occurs at:\n{max_row[['ts', 'spot_eur_mwh']]}")
    
    # Check around 2026-11-13 18:00
    sub = df[df["ts"].str.contains("2026-11-13T17|2026-11-13T18|2026-11-13T19")]
    print("\nPrices around evening peak on 2026-11-13:")
    print(sub[["ts", "spot_eur_mwh", "grid_tariff_depot_eur_mwh", "grid_tariff_public_eur_mwh"]])

def test_operations_log():
    print("\n" + "=" * 60)
    print("3. OPERATIONS LOG VERIFICATION")
    print("Claim: 10,380 operations, 93,412 staff minutes, 5,596 move_and_replug_vehicle actions (47.93%)")
    print("=" * 60)
    ops_path = os.path.join(DATA_DIR, "operations_log.csv")
    df = pd.read_csv(ops_path)
    print(f"operations_log.csv shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
    
    # Check if operations is a count column or each row is an operation
    if "count" in df.columns or "actions" in df.columns:
        print("Columns with counts detected.")
    
    # Let's inspect column names and summary
    for col in df.columns:
        print(f"Column '{col}' sample: {df[col].iloc[:3].tolist()}")
        
    # Group by action
    if "action" in df.columns:
        grouped = df.groupby("action")
        # Check what columns exist: count? minutes?
        print("\nAggregations by action:")
        summary = df.groupby("action").agg({col: ["sum", "count"] for col in df.select_dtypes(include=[np.number]).columns})
        print(summary)
        
        # Check total staff minutes
        total_minutes = None
        for col in ["staff_minutes", "minutes", "duration_minutes", "total_minutes"]:
            if col in df.columns:
                total_minutes = df[col].sum()
                print(f"Total {col}: {total_minutes}")
                move_minutes = df[df["action"] == "move_and_replug_vehicle"][col].sum()
                print(f"move_and_replug_vehicle {col}: {move_minutes} ({move_minutes/total_minutes*100:.4f}%)")
                
        # Check total operations/actions
        for col in ["count", "num_operations", "operations", "frequency"]:
            if col in df.columns:
                total_ops = df[col].sum()
                print(f"Total {col}: {total_ops}")
                move_ops = df[df["action"] == "move_and_replug_vehicle"][col].sum()
                print(f"move_and_replug_vehicle {col}: {move_ops} ({move_ops/total_ops*100:.4f}%)")
        if "count" not in df.columns:
            print(f"Total rows in df: {len(df)}")
            move_count = (df["action"] == "move_and_replug_vehicle").sum()
            print(f"move_and_replug_vehicle row count: {move_count}")

def test_service_tickets():
    print("\n" + "=" * 60)
    print("4. SERVICE TICKETS VERIFICATION")
    print("Claim: 14 service tickets costing 12,185.80 €")
    print("=" * 60)
    tickets_path = os.path.join(DATA_DIR, "service_tickets.csv")
    df = pd.read_csv(tickets_path)
    print(f"service_tickets.csv shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
    
    num_tickets = len(df)
    print(f"Number of service tickets: {num_tickets}")
    
    # Check cost columns
    for col in df.columns:
        if "cost" in col or "eur" in col or "price" in col:
            print(f"Sum of {col}: {df[col].sum():.2f}")
    if "total_cost_eur" in df.columns:
        print(f"Total cost eur: {df['total_cost_eur'].sum():.2f}")
    elif "cost_eur" in df.columns:
        print(f"Cost eur: {df['cost_eur'].sum():.2f}")

def test_failed_departures():
    print("\n" + "=" * 60)
    print("5. FAILED DEPARTURES ON SCENARIO DAY (2026-11-13)")
    print("Claim: 13 failed departures on scenario day across S1, S2, S5")
    print("=" * 60)
    dep_path = os.path.join(DATA_DIR, "departures_baseline.csv")
    df = pd.read_csv(dep_path)
    print(f"departures_baseline.csv shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(df.head())
    
    # Filter for 2026-11-13
    df_13 = df[df["depart_ts"].str.startswith("2026-11-13")]
    print(f"Departures on 2026-11-13: {len(df_13)}")
    
    # Check failure/below_required column
    for col in ["below_required", "below_req", "failed", "delayed", "compliant"]:
        if col in df.columns:
            print(f"Column '{col}' value counts on 2026-11-13:")
            print(df_13[col].value_counts())
            print(f"By site on 2026-11-13 for {col}:")
            if "site_id" in df.columns:
                print(df_13.groupby(["site_id", col]).size().unstack(fill_value=0))
            elif "vehicle_id" in df.columns:
                # check which site
                print(df_13[df_13[col] == 1])

def test_s3_abandonment():
    print("\n" + "=" * 60)
    print("6. S3 PUBLIC CHARGING ABANDONMENT ON SCENARIO DAY (2026-11-13)")
    print("Claim: S3 76 abandoned drivers (29.69%) during 2h outage")
    print("=" * 60)
    # Check baseline_kpis.csv
    kpi_path = os.path.join(DATA_DIR, "baseline_kpis.csv")
    df_kpi = pd.read_csv(kpi_path)
    print("baseline_kpis.csv:")
    print(df_kpi)
    
    # Check public_arrivals.csv
    arr_path = os.path.join(DATA_DIR, "public_arrivals.csv")
    df_arr = pd.read_csv(arr_path)
    print(f"\npublic_arrivals.csv columns: {list(df_arr.columns)}")
    df_arr_s3_13 = df_arr[(df_arr["site_id"] == "S3") & (df_arr["ts"].str.startswith("2026-11-13"))]
    print(f"S3 arrivals on 2026-11-13: {len(df_arr_s3_13)}")
    if "outcome" in df_arr.columns:
        print(df_arr_s3_13["outcome"].value_counts())
        outcomes = df_arr_s3_13["outcome"].value_counts()
        total_s3 = len(df_arr_s3_13)
        abandoned = outcomes.get("left_queue", 0)
        print(f"Abandoned count: {abandoned}, pct: {abandoned / total_s3 * 100:.2f}%")
            
    # Check connectivity_outages.csv
    outage_path = os.path.join(DATA_DIR, "connectivity_outages.csv")
    df_out = pd.read_csv(outage_path)
    print(f"\nconnectivity_outages.csv:\n{df_out}")

if __name__ == "__main__":
    test_total_csv_rows()
    test_price_surge()
    test_operations_log()
    test_service_tickets()
    test_failed_departures()
    test_s3_abandonment()
