# Module 5 Homework: Data Platforms (Bruin) - Answers

## Q1: Required Files in a Bruin Project

**Answer: `pipeline.yml` and `assets/` only**

The minimal required structure is:

```text
my-pipeline/
├─ pipeline.yml
└─ assets/
   ├─ asset1.sql
   └─ asset2.py
```

`.bruin.yml` is **auto-generated** at the repo root the first time you run `bruin validate` or `bruin run` — you don't create it manually.

## Q2: Materialization Strategy for Time-Based Interval Processing

**Answer: `time_interval` — incremental based on a time column**

`time_interval` deletes and re-inserts data for a specific time window, making it ideal for monthly NYC taxi data where you process one month at a time without rebuilding the entire table.

## Q3: Overriding a Variable When Running the Pipeline

**Answer: `bruin run --var 'taxi_types=["yellow"]'`**

The `--var` flag accepts key=value pairs. Since `taxi_types` expects an array, the correct format uses JSON array syntax with single quotes to wrap the expression.

## Q4: Running an Asset with All Downstream Dependencies

**Answer: `bruin run ingestion/trips.py --downstream`**

The `--downstream` flag tells Bruin to run the specified asset and all assets that depend on it.

## Q5: Quality Check for No NULL Values

**Answer: `name: not_null`**

```yaml
checks:
  - name: not_null
```

The `not_null` check ensures the column never contains NULL values and fails the pipeline if any are found.

## Q6: Visualizing the Dependency Graph Between Assets

**Answer: `bruin lineage`**

```bash
bruin lineage path/to/asset.sql
```

Shows upstream and downstream dependencies for an asset. Use `--full` to include indirect dependencies.

## Q7: Flag to Create Tables from Scratch on a New Database

**Answer: `--full-refresh`**

`--full-refresh` truncates the table before running and sets `full_refresh = True` in Jinja templates, ensuring a clean slate on a new DuckDB database.
