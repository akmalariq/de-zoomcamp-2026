# Workshop 1: dlt Homework - Answers

## Q1: Dataset Date Range

**Answer: 2009-06-01 to 2009-07-01**

```sql
SELECT MIN(trip_pickup_date_time), MAX(trip_pickup_date_time) FROM taxi_data.taxi_rides;
-- 2009-06-01 ... 2009-07-01
```

## Q2: Proportion of Trips Paid with Credit Card

**Answer: 26.66%**

Payment type is stored as `'Credit'` (not `'Credit Card'`).

```sql
SELECT ROUND(100.0 * COUNT(*) FILTER (WHERE payment_type = 'Credit') / COUNT(*), 2)
FROM taxi_data.taxi_rides;
-- 26.66%
```

## Q3: Total Tips Generated

**Answer: $6,063.41**

```sql
SELECT ROUND(SUM(tip_amt), 2) FROM taxi_data.taxi_rides;
-- 6063.41
```

## Pipeline Setup

Used `dlt` with the NYC taxi REST API (paginated JSON, 1000 records/page):
- API: `https://us-central1-dlthub-analytics.cloudfunctions.net/data_engineering_zoomcamp_api`
- Destination: DuckDB
- Total records loaded: 10,000
