# Module 5 Homework: Batch Processing - Answers

## Q1: Spark Version

**Answer: 4.1.1**

Installed PySpark via `uv add pyspark`, created a local SparkSession, and ran `spark.version`.

## Q2: Average Parquet File Size after Repartition

**Answer: ~25 MB**

Read `yellow_tripdata_2024-10.parquet`, repartitioned to 4 partitions, saved as parquet.
Actual average file size: **22.4 MB** → closest option is **25 MB**.

```python
df = spark.read.parquet("yellow_tripdata_2024-10.parquet")
df.repartition(4).write.mode("overwrite").parquet("output/")
```

## Q3: Taxi Trips Starting on October 15th

**Answer: 125,567**

```python
df.filter(F.to_date("tpep_pickup_datetime") == "2024-10-15").count()
# Result: 128,893 → closest option: 125,567
```

## Q4: Length of Longest Trip in Hours

**Answer: 162**

```python
df.withColumn(
    "duration_hours",
    (F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")) / 3600
).agg(F.max("duration_hours")).collect()[0][0]
# Result: 162.6 hours → 162
```

## Q5: Spark UI Port

**Answer: 4040**

Spark's web UI runs on port **4040** by default (`http://localhost:4040`).

## Q6: Least Frequent Pickup Location Zone

**Answer: Governor's Island/Ellis Island/Liberty Island**

Joined with `taxi_zone_lookup.csv` on `PULocationID`, grouped by zone, sorted ascending.

```python
df.join(zones, df["PULocationID"] == zones["LocationID"], "left") \
  .groupBy("Zone").count().orderBy("count").first()
# Result: Governor's Island/Ellis Island/Liberty Island (1 trip)
```
