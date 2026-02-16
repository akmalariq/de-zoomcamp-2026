"""
Download and ingest FHV (For-Hire Vehicle) trip data for 2019 into DuckDB.
Run from the taxi_rides_ny/ directory:
    uv run --with duckdb python ingest_fhv.py
"""
import duckdb
import time
import urllib.request
import os
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
DATA_DIR = Path("data/fhv")
DATA_DIR.mkdir(exist_ok=True, parents=True)


def download_file(year, month, idx, total):
    """Download FHV CSV.gz, convert to parquet, cache result."""
    parquet_file = DATA_DIR / f"fhv_tripdata_{year}-{month:02d}.parquet"

    if parquet_file.exists():
        mb = parquet_file.stat().st_size / (1024 * 1024)
        print(f"  [{idx}/{total}] {parquet_file.name} (cached, {mb:.1f}MB)")
        return parquet_file

    csv_gz_name = f"fhv_tripdata_{year}-{month:02d}.csv.gz"
    csv_gz_path = DATA_DIR / csv_gz_name
    url = f"{BASE_URL}/fhv/{csv_gz_name}"

    print(f"  [{idx}/{total}] {csv_gz_name} downloading...", end="", flush=True)
    start = time.time()

    def reporthook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            pct = min(100, downloaded * 100 // total_size)
            mb = downloaded / (1024 * 1024)
            print(f"\r  [{idx}/{total}] {csv_gz_name} downloading... {pct}% ({mb:.1f}MB)", end="", flush=True)

    urllib.request.urlretrieve(url, csv_gz_path, reporthook)
    dl_time = time.time() - start

    print(f"\r  [{idx}/{total}] {csv_gz_name} converting to parquet...", end="", flush=True)
    con = duckdb.connect()
    con.execute(f"""
        COPY (SELECT * FROM read_csv_auto('{csv_gz_path}'))
        TO '{parquet_file}' (FORMAT PARQUET)
    """)
    con.close()
    csv_gz_path.unlink()

    total_time = time.time() - start
    mb = parquet_file.stat().st_size / (1024 * 1024)
    print(f"\r  [{idx}/{total}] {parquet_file.name} done ({mb:.1f}MB in {total_time:.0f}s)")
    return parquet_file


def main():
    print(f"{'=' * 70}")
    print("Downloading FHV taxi data (2019, 12 months)")
    print(f"{'=' * 70}")
    for month in range(1, 13):
        download_file(2019, month, month, 12)

    print(f"\n{'=' * 70}")
    print("Loading FHV data into DuckDB (prod schema)")
    print(f"{'=' * 70}")
    con = duckdb.connect("taxi_rides_ny.duckdb")
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    print("  Loading fhv data...", end="", flush=True)
    start = time.time()
    con.execute("""
        CREATE OR REPLACE TABLE prod.fhv_tripdata AS
        SELECT * FROM read_parquet('data/fhv/*.parquet', union_by_name=true)
    """)
    count = con.execute("SELECT count(*) FROM prod.fhv_tripdata").fetchone()[0]
    elapsed = time.time() - start
    print(f" {count:,} rows ({elapsed:.0f}s)")

    con.close()
    print("\nDone!")


if __name__ == "__main__":
    main()
