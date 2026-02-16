"""
DE Zoomcamp 2026 - Module 3 Homework: Data Warehouse
Downloads Yellow Taxi 2024 (Jan-Jun) parquet files and answers Q1, Q4 locally.
Q2, Q3, Q5-Q8 are BigQuery-specific or conceptual.
"""
import duckdb
import time
import urllib.request
import os

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
CACHE_DIR = os.path.join(os.path.dirname(__file__), ".data")
os.makedirs(CACHE_DIR, exist_ok=True)

con = duckdb.connect()


def download_parquet(year, month, idx, total):
    """Download a parquet file with progress, skip if cached."""
    filename = f"yellow_tripdata_{year}-{month:02d}.parquet"
    url = f"{BASE_URL}/{filename}"
    local_path = os.path.join(CACHE_DIR, filename)

    if os.path.exists(local_path):
        mb = os.path.getsize(local_path) / (1024 * 1024)
        print(f"  [{idx}/{total}] {filename} (cached, {mb:.1f}MB)")
        return local_path

    print(f"  [{idx}/{total}] {filename} downloading...", end="", flush=True)
    start = time.time()

    def reporthook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            pct = min(100, downloaded * 100 // total_size)
            mb = downloaded / (1024 * 1024)
            print(f"\r  [{idx}/{total}] {filename} downloading... {pct}% ({mb:.1f}MB)", end="", flush=True)

    urllib.request.urlretrieve(url, local_path, reporthook)
    elapsed = time.time() - start
    mb = os.path.getsize(local_path) / (1024 * 1024)
    print(f"\r  [{idx}/{total}] {filename} done ({mb:.1f}MB in {elapsed:.0f}s)")
    return local_path


try:
    # Download all 6 parquet files
    print("=" * 70)
    print("Downloading Yellow Taxi 2024 Parquet files (Jan-Jun)")
    print("=" * 70)
    files = []
    for i, month in enumerate(range(1, 7), 1):
        files.append(download_parquet(2024, month, i, 6))
    print()

    # Create a view over all files
    file_pattern = os.path.join(CACHE_DIR, "yellow_tripdata_2024-*.parquet")
    con.execute(f"CREATE VIEW taxi AS SELECT * FROM read_parquet('{file_pattern}')")

    # Q1: Total record count
    print("=" * 70)
    print("Q1: Total record count for 2024 Yellow Taxi Data")
    print("=" * 70)
    q1 = con.execute("SELECT count(*) FROM taxi").fetchone()[0]
    print(f"  Count: {q1:,}")
    print()

    # Q4: Records with fare_amount = 0
    print("=" * 70)
    print("Q4: Records with fare_amount = 0")
    print("=" * 70)
    q4 = con.execute("SELECT count(*) FROM taxi WHERE fare_amount = 0").fetchone()[0]
    print(f"  Count: {q4:,}")
    print()

    # Bonus: Quick column stats
    print("=" * 70)
    print("Extra: Distinct PULocationIDs (relevant for Q2)")
    print("=" * 70)
    distinct_pu = con.execute("SELECT count(DISTINCT PULocationID) FROM taxi").fetchone()[0]
    print(f"  Distinct PULocationIDs: {distinct_pu}")
    print()

    # Summary
    print("=" * 70)
    print("ANSWERS SUMMARY")
    print("=" * 70)
    print(f"  Q1: {q1:,}")
    print(f"  Q2: 0 MB for External Table and 155.12 MB for Materialized Table")
    print(f"      (External tables can't estimate scan size; materialized knows column size)")
    print(f"  Q3: BigQuery is columnar - only scans requested columns")
    print(f"  Q4: {q4:,}")
    print(f"  Q5: Partition by tpep_dropoff_datetime and Cluster on VendorID")
    print(f"  Q6: 310.24 MB for non-partitioned and 26.84 MB for partitioned")
    print(f"  Q7: GCP Bucket")
    print(f"  Q8: False")

finally:
    con.close()
    print(f"\n  Cache dir: {CACHE_DIR}")
