from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os

spark = SparkSession.builder \
    .master("local[*]") \
    .appName("de-zoomcamp-hw6") \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
PARQUET_PATH = os.path.join(DATA_DIR, "yellow_tripdata_2025-11.parquet")
ZONE_PATH = os.path.join(DATA_DIR, "taxi_zone_lookup.csv")
OUTPUT_DIR = os.path.join(DATA_DIR, "yellow_2025_11_partitioned")

# Q1: Spark version
print(f"\nQ1 - Spark version: {spark.version}")

# Q2: Repartition to 4, save as parquet, check avg file size
df = spark.read.parquet(PARQUET_PATH)
df.repartition(4).write.mode("overwrite").parquet(OUTPUT_DIR)

part_files = [
    os.path.getsize(os.path.join(OUTPUT_DIR, f))
    for f in os.listdir(OUTPUT_DIR)
    if f.endswith(".parquet")
]
avg_mb = sum(part_files) / len(part_files) / (1024 * 1024)
print(f"Q2 - Avg parquet file size: {avg_mb:.1f} MB (from {len(part_files)} files)")

# Q3: Trips starting on Nov 15
df_partitioned = spark.read.parquet(OUTPUT_DIR)
nov15_count = df_partitioned.filter(
    F.to_date("tpep_pickup_datetime") == "2025-11-15"
).count()
print(f"Q3 - Trips on Nov 15: {nov15_count:,}")

# Q4: Longest trip in hours
longest = df_partitioned.withColumn(
    "duration_hours",
    (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 3600
).agg(F.max("duration_hours")).collect()[0][0]
print(f"Q4 - Longest trip: {longest:.1f} hours")

# Q5: Spark UI port (factual)
print("Q5 - Spark UI port: 4040")

# Q6: Least frequent pickup zone
zones = spark.read.option("header", "true").csv(ZONE_PATH)
df_with_zones = df_partitioned.join(
    zones.select(F.col("LocationID").cast("integer"), F.col("Zone")),
    df_partitioned["PULocationID"] == F.col("LocationID"),
    "left"
)
least_frequent = df_with_zones.groupBy("Zone") \
    .count() \
    .orderBy("count") \
    .first()
print(f"Q6 - Least frequent zone: {least_frequent['Zone']} ({least_frequent['count']:,} trips)")

spark.stop()
