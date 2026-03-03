import dlt
import requests
import duckdb

API_URL = "https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api"

@dlt.resource(name="taxi_rides", write_disposition="replace")
def taxi_rides():
    page = 1
    while True:
        response = requests.get(API_URL, params={"page": page})
        response.raise_for_status()
        data = response.json()
        if not data:
            break
        yield data
        page += 1

pipeline = dlt.pipeline(
    pipeline_name="taxi_pipeline",
    destination="duckdb",
    dataset_name="taxi_data",
)

print("Loading data...")
load_info = pipeline.run(taxi_rides())
print(load_info)

# Answer the questions directly with DuckDB
conn = duckdb.connect(f"{pipeline.pipeline_name}.duckdb")

print("\n--- Q1: Date range ---")
q1 = conn.execute("SELECT MIN(pickup_datetime), MAX(pickup_datetime) FROM taxi_data.taxi_rides").fetchone()
print(f"Start: {q1[0]}, End: {q1[1]}")

print("\n--- Q2: Credit card payment proportion ---")
q2 = conn.execute("""
    SELECT
        ROUND(100.0 * COUNT(*) FILTER (WHERE payment_type = 'Credit Card') / COUNT(*), 2) AS pct
    FROM taxi_data.taxi_rides
""").fetchone()
print(f"Credit card: {q2[0]}%")

print("\n--- Q3: Total tips ---")
q3 = conn.execute("SELECT ROUND(SUM(tip_amount), 2) FROM taxi_data.taxi_rides").fetchone()
print(f"Total tips: ${q3[0]:,.2f}")

conn.close()
