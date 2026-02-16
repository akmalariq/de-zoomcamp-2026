-- DE Zoomcamp 2026 - Module 3: Data Warehouse
-- BigQuery SQL queries for homework
-- Replace 'your_project.your_dataset' with your actual project/dataset

-- Setup: Create external table from GCS parquet files
CREATE OR REPLACE EXTERNAL TABLE `your_project.your_dataset.yellow_tripdata_ext`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://your-bucket/yellow_tripdata_2024-*.parquet']
);

-- Setup: Create materialized table (no partition/cluster)
CREATE OR REPLACE TABLE `your_project.your_dataset.yellow_tripdata`
AS SELECT * FROM `your_project.your_dataset.yellow_tripdata_ext`;

-- Q1: Total record count
SELECT count(*) FROM `your_project.your_dataset.yellow_tripdata`;

-- Q2: Distinct PULocationIDs - check estimated bytes for each
-- Run on external table:
SELECT count(DISTINCT PULocationID) FROM `your_project.your_dataset.yellow_tripdata_ext`;
-- Run on materialized table:
SELECT count(DISTINCT PULocationID) FROM `your_project.your_dataset.yellow_tripdata`;

-- Q4: Records with fare_amount = 0
SELECT count(*) FROM `your_project.your_dataset.yellow_tripdata` WHERE fare_amount = 0;

-- Q5: Create optimized table (partition + cluster)
CREATE OR REPLACE TABLE `your_project.your_dataset.yellow_tripdata_partitioned`
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS SELECT * FROM `your_project.your_dataset.yellow_tripdata`;

-- Q6: Compare estimated bytes for date range query
-- Run on non-partitioned (materialized) table:
SELECT DISTINCT VendorID
FROM `your_project.your_dataset.yellow_tripdata`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- Run on partitioned table:
SELECT DISTINCT VendorID
FROM `your_project.your_dataset.yellow_tripdata_partitioned`
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';

-- Bonus Q9: SELECT count(*) on materialized table
SELECT count(*) FROM `your_project.your_dataset.yellow_tripdata`;
-- Estimated: 0 bytes (BigQuery stores row count in metadata)
