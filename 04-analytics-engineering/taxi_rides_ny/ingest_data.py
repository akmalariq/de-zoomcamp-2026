"""
Download and ingest Yellow/Green taxi data (2019-2020) into DuckDB for dbt.
Run from the taxi_rides_ny/ directory:
    uv run --with duckdb --with requests python ingest_data.py
"""
import duckdb
import time
import urllib.request
import os
from pathlib import Path

BASE_URL = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download"
DATA_DIR = Path("data")


def download_file(taxi_type, year, month, idx, total):
    """Download CSV.gz, convert to parquet, cache result."""
    data_dir = DATA_DIR / taxi_type
    data_dir.mkdir(exist_ok=True, parents=True)

    parquet_file = data_dir / f"{taxi_type}_tripdata_{year}-{month:02d}.parquet"

    if parquet_file.exists():
        mb = parquet_file.stat().st_size / (1024 * 1024)
        print(f"  [{idx}/{total}] {parquet_file.name} (cached, {mb:.1f}MB)")
        return parquet_file

    csv_gz_name = f"{taxi_type}_tripdata_{year}-{month:02d}.csv.gz"
    csv_gz_path = data_dir / csv_gz_name
    url = f"{BASE_URL}/{taxi_type}/{csv_gz_name}"

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

    # Convert to parquet
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
    total_files = 48  # 2 types x 2 years x 12 months
    idx = 0

    for taxi_type in ["yellow", "green"]:
        print(f"\n{'=' * 70}")
        print(f"Downloading {taxi_type.upper()} taxi data (2019-2020)")
        print(f"{'=' * 70}")
        for year in [2019, 2020]:
            for month in range(1, 13):
                idx += 1
                download_file(taxi_type, year, month, idx, total_files)

    # Load into DuckDB
    print(f"\n{'=' * 70}")
    print("Loading data into DuckDB (prod schema)")
    print(f"{'=' * 70}")

    db_path = "taxi_rides_ny.duckdb"
    con = duckdb.connect(db_path)
    con.execute("CREATE SCHEMA IF NOT EXISTS prod")

    for taxi_type in ["yellow", "green"]:
        print(f"  Loading {taxi_type} data...", end="", flush=True)
        start = time.time()
        con.execute(f"""
            CREATE OR REPLACE TABLE prod.{taxi_type}_tripdata AS
            SELECT * FROM read_parquet('data/{taxi_type}/*.parquet', union_by_name=true)
        """)
        count = con.execute(f"SELECT count(*) FROM prod.{taxi_type}_tripdata").fetchone()[0]
        elapsed = time.time() - start
        print(f" {count:,} rows ({elapsed:.0f}s)")

    con.close()
    print(f"\nDone! Database: {db_path}")


if __name__ == "__main__":
    main()
