"""
DE Zoomcamp 2026 - Module 2 Homework: Workflow Orchestration
Solves Q1, Q3, Q4, Q5 using DuckDB.
Downloads CSV.gz files locally first to avoid DuckDB httpfs streaming bugs.
"""
import duckdb
import time
import urllib.request
import os

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".data")
os.makedirs(CACHE_DIR, exist_ok=True)

con = duckdb.connect()


def download_and_count(taxi_type, year, month, idx, total):
    """Download a CSV.gz file locally, then count rows with DuckDB."""
    filename = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
    url = f"{BASE_URL}/{taxi_type}/{filename}"
    local_path = os.path.join(CACHE_DIR, filename)

    start = time.time()

    # Skip download if file already exists
    if os.path.exists(local_path):
        mb = os.path.getsize(local_path) / (1024 * 1024)
        print(f"  [{idx}/{total}] {filename} (cached, {mb:.1f}MB)", end="", flush=True)
    else:
        print(f"  [{idx}/{total}] {filename} downloading...", end="", flush=True)

        def reporthook(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                pct = min(100, downloaded * 100 // total_size)
                mb = downloaded / (1024 * 1024)
                print(f"\r  [{idx}/{total}] {filename} downloading... {pct}% ({mb:.1f}MB)", end="", flush=True)

        urllib.request.urlretrieve(url, local_path, reporthook)

    dl_time = time.time() - start

    # Count rows
    count = con.execute(f"SELECT count(*) FROM read_csv_auto('{local_path}')").fetchone()[0]
    total_time = time.time() - start

    print(f"\r  [{idx}/{total}] {filename} -> {count:>12,} rows  ({total_time:.0f}s)")
    return count


try:
    # Q1
    print("=" * 70)
    print("Q1: Uncompressed file size of yellow_tripdata_2020-12.csv")
    print("=" * 70)
    print("  Answer: 128.3 MiB (from Kestra extract task output)")
    print()

    # Q3: Yellow taxi 2020 (12 months)
    print("=" * 70)
    print("Q3: Yellow Taxi 2020 - Total rows (all 12 months)")
    print("=" * 70)
    yellow_2020_total = 0
    for month in range(1, 13):
        yellow_2020_total += download_and_count("yellow", 2020, month, month, 12)
    print(f"  {'TOTAL':>46}: {yellow_2020_total:>12,}")
    print()

    # Q4: Green taxi 2020 (12 months)
    print("=" * 70)
    print("Q4: Green Taxi 2020 - Total rows (all 12 months)")
    print("=" * 70)
    green_2020_total = 0
    for month in range(1, 13):
        green_2020_total += download_and_count("green", 2020, month, month, 12)
    print(f"  {'TOTAL':>46}: {green_2020_total:>12,}")
    print()

    # Q5: Yellow taxi March 2021 (1 file)
    print("=" * 70)
    print("Q5: Yellow Taxi March 2021 - Row count")
    print("=" * 70)
    q5_count = download_and_count("yellow", 2021, 3, 1, 1)
    print()

    # Summary
    print("=" * 70)
    print("ANSWERS SUMMARY")
    print("=" * 70)
    print(f"  Q1: 128.3 MiB")
    print(f"  Q2: green_tripdata_2020-04.csv")
    print(f"  Q3: {yellow_2020_total:,}")
    print(f"  Q4: {green_2020_total:,}")
    print(f"  Q5: {q5_count:,}")
    print(f"  Q6: America/New_York")

finally:
    con.close()
    print(f"\n  Cache dir: {CACHE_DIR} (delete manually when done)")
