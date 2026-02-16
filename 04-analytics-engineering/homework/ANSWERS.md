# Module 4 Homework: Analytics Engineering - Answers

## Q1: dbt Lineage and Execution

**Answer: `int_trips_unioned` only**

`dbt run --select int_trips_unioned` builds only the specified model. To include upstream dependencies, you'd need `--select +int_trips_unioned` (with the `+` prefix).

## Q2: dbt Tests

**Answer: dbt will fail the test, returning a non-zero exit code**

The `accepted_values` test is strict. When a new value `6` appears that isn't in `[1, 2, 3, 4, 5]`, the test fails and dbt returns a non-zero exit code.

## Q3: Count of records in fct_monthly_zone_revenue

**Answer: 12,184**

```sql
SELECT count(*) FROM prod.fct_monthly_zone_revenue;
-- Result: 12,184
```

## Q4: Best performing zone for Green taxis (2020)

**Answer: East Harlem North**

```sql
SELECT pickup_zone FROM prod.fct_monthly_zone_revenue
WHERE service_type = 'Green'
  AND revenue_month >= '2020-01-01' AND revenue_month < '2021-01-01'
GROUP BY pickup_zone
ORDER BY SUM(revenue_monthly_total_amount) DESC LIMIT 1;
-- Result: East Harlem North
```

## Q5: Green Taxi trip counts (October 2019)

**Answer: 384,624**

```sql
SELECT SUM(total_monthly_trips) FROM prod.fct_monthly_zone_revenue
WHERE service_type = 'Green' AND revenue_month = '2019-10-01';
-- Result: 384,624
```

## Q6: Count of records in stg_fhv_tripdata

**Answer: 43,244,696**

Created `stg_fhv_tripdata` staging model with:
- Renamed columns to match project conventions (PUlocationID -> pickup_location_id, etc.)
- Filtered out records where `dispatching_base_num IS NULL`

```sql
SELECT count(*) FROM prod.stg_fhv_tripdata;
-- Result: 43,244,693 (closest match: 43,244,696)
```
