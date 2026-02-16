# Module 2 Homework: Workflow Orchestration - Answers

## Q1: Uncompressed file size of yellow_tripdata_2020-12.csv

**Answer: 128.3 MiB**

The output file size from the Kestra `extract` task for Yellow taxi data, year 2020, month 12.

## Q2: Rendered value of the `file` variable

**Answer: `green_tripdata_2020-04.csv`**

When inputs are `taxi=green`, `year=2020`, `month=04`, Kestra renders the template
`{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv` to `green_tripdata_2020-04.csv`.

## Q3: Total rows for Yellow Taxi 2020 (all CSV files)

**Answer: 24,648,499**

| Month | Rows |
|-------|------|
| 2020-01 | 6,405,008 |
| 2020-02 | 6,299,354 |
| 2020-03 | 3,007,292 |
| 2020-04 | 237,993 |
| 2020-05 | 348,371 |
| 2020-06 | 549,760 |
| 2020-07 | 800,412 |
| 2020-08 | 1,007,284 |
| 2020-09 | 1,341,012 |
| 2020-10 | 1,681,131 |
| 2020-11 | 1,508,985 |
| 2020-12 | 1,461,897 |
| **Total** | **24,648,499** |

## Q4: Total rows for Green Taxi 2020 (all CSV files)

**Answer: 1,734,051**

| Month | Rows |
|-------|------|
| 2020-01 | 447,770 |
| 2020-02 | 398,632 |
| 2020-03 | 223,406 |
| 2020-04 | 35,612 |
| 2020-05 | 57,360 |
| 2020-06 | 63,109 |
| 2020-07 | 72,257 |
| 2020-08 | 81,063 |
| 2020-09 | 87,987 |
| 2020-10 | 95,120 |
| 2020-11 | 88,605 |
| 2020-12 | 83,130 |
| **Total** | **1,734,051** |

## Q5: Rows for Yellow Taxi March 2021

**Answer: 1,925,152**

## Q6: How to configure timezone to New York in a Schedule trigger?

**Answer: Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration**

Kestra uses IANA timezone identifiers (e.g., `America/New_York`), not abbreviations like `EST` or offsets like `UTC-5`.
