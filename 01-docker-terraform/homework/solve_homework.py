#!/usr/bin/env python3
"""Script to answer DE Zoomcamp Homework 1 Questions 3-6 using DuckDB."""

import duckdb

# Connect to DuckDB (in-memory)
con = duckdb.connect()

# Load the data
print("Loading data...")
con.execute("""
    CREATE TABLE green_taxi AS 
    SELECT * FROM read_parquet('green_tripdata_2025-11.parquet')
""")
con.execute("""
    CREATE TABLE zones AS 
    SELECT * FROM read_csv_auto('taxi_zone_lookup.csv')
""")

print("\n" + "="*60)
print("QUESTION 3: Counting short trips")
print("="*60)
print("Trips in November 2025 with trip_distance <= 1 mile")
result = con.execute("""
    SELECT COUNT(*) as short_trips
    FROM green_taxi
    WHERE lpep_pickup_datetime >= '2025-11-01'
      AND lpep_pickup_datetime < '2025-12-01'
      AND trip_distance <= 1
""").fetchone()
print(f"Answer: {result[0]:,}")

print("\n" + "="*60)
print("QUESTION 4: Longest trip for each day")
print("="*60)
print("Pickup day with longest trip (excluding trips >= 100 miles)")
result = con.execute("""
    SELECT 
        DATE(lpep_pickup_datetime) as pickup_day,
        MAX(trip_distance) as max_distance
    FROM green_taxi
    WHERE trip_distance < 100
    GROUP BY DATE(lpep_pickup_datetime)
    ORDER BY max_distance DESC
    LIMIT 5
""").fetchall()
print("Top 5 days by longest trip:")
for row in result:
    print(f"  {row[0]}: {row[1]:.2f} miles")
print(f"\nAnswer: {result[0][0]}")

print("\n" + "="*60)
print("QUESTION 5: Biggest pickup zone by total_amount")
print("="*60)
print("Pickup zone with largest total_amount sum on November 18, 2025")
result = con.execute("""
    SELECT 
        z.Zone,
        SUM(g.total_amount) as total
    FROM green_taxi g
    JOIN zones z ON g.PULocationID = z.LocationID
    WHERE DATE(g.lpep_pickup_datetime) = '2025-11-18'
    GROUP BY z.Zone
    ORDER BY total DESC
    LIMIT 5
""").fetchall()
print("Top 5 zones by total_amount:")
for row in result:
    print(f"  {row[0]}: ${row[1]:,.2f}")
print(f"\nAnswer: {result[0][0]}")

print("\n" + "="*60)
print("QUESTION 6: Largest tip")
print("="*60)
print("Drop-off zone with largest tip for pickups in 'East Harlem North'")
result = con.execute("""
    SELECT 
        dz.Zone as dropoff_zone,
        MAX(g.tip_amount) as max_tip
    FROM green_taxi g
    JOIN zones pz ON g.PULocationID = pz.LocationID
    JOIN zones dz ON g.DOLocationID = dz.LocationID
    WHERE pz.Zone = 'East Harlem North'
      AND g.lpep_pickup_datetime >= '2025-11-01'
      AND g.lpep_pickup_datetime < '2025-12-01'
    GROUP BY dz.Zone
    ORDER BY max_tip DESC
    LIMIT 5
""").fetchall()
print("Top 5 drop-off zones by max tip:")
for row in result:
    print(f"  {row[0]}: ${row[1]:.2f}")
print(f"\nAnswer: {result[0][0]}")

print("\n" + "="*60)
print("SUMMARY OF ANSWERS")
print("="*60)
