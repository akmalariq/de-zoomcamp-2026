# Module 3 Homework: Data Warehouse - Answers

## Q1: Record count for 2024 Yellow Taxi Data

**Answer: 20,332,093**

Verified locally with DuckDB across all 6 parquet files (Jan-Jun 2024).

## Q2: Estimated data for SELECT DISTINCT PULocationID

**Answer: 0 MB for the External Table and 155.12 MB for the Materialized Table**

BigQuery cannot estimate scan size for external tables (shows 0 MB) since the data lives in GCS.
For materialized (native) tables, BigQuery knows the exact column size and shows the estimate.

## Q3: Why are estimated bytes different for 1 column vs 2 columns?

**Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.**

## Q4: Records with fare_amount = 0

**Answer: 8,333**

Verified locally with DuckDB: `SELECT count(*) FROM taxi WHERE fare_amount = 0`

## Q5: Best strategy for filtering by tpep_dropoff_datetime and ordering by VendorID

**Answer: Partition by tpep_dropoff_datetime and Cluster on VendorID**

- **Partition** on the datetime filter column for efficient date-range pruning
- **Cluster** on VendorID for sorting within partitions

## Q6: Estimated bytes for date range query (non-partitioned vs partitioned)

**Answer: 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table**

The partitioned table only scans the relevant date partitions (Mar 1-15, 2024),
while the non-partitioned table must scan the entire datetime column.

## Q7: Where is External Table data stored?

**Answer: GCP Bucket**

External tables reference data stored in Google Cloud Storage (GCS), not in BigQuery's native storage.

## Q8: Is it best practice to always cluster your data?

**Answer: False**

Clustering is not always beneficial. Small tables, tables with low cardinality columns,
or tables that are rarely queried with filters don't benefit from clustering.
The overhead of maintaining clusters can outweigh the performance gains.

## Bonus Q9: SELECT count(*) estimated bytes on materialized table

**Answer: 0 bytes**

BigQuery stores table metadata including row count, so `SELECT count(*)` doesn't need to scan any data.
