# Data Engineering Zoomcamp 2026 - Homework 1 Answers
## Module 1: Docker & SQL

---

## Question 1: Understanding Docker images
**What's the version of pip in the `python:3.13` image?**

```bash
docker run --rm python:3.13 pip --version
# Output: pip 24.3.1 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

### ✅ Answer: **24.3.1**

---

## Question 2: Understanding Docker networking and docker-compose
**What is the hostname and port that pgadmin should use to connect to the postgres database?**

Given the docker-compose.yaml:
- The postgres service is named `db` (not the container_name `postgres`)
- Within a docker-compose network, services communicate using **service names** as hostnames
- The **internal port** is `5432` (the external mapping `5433:5432` is only for host access)

### ✅ Answer: **db:5432**

> **Note:** When containers communicate within the same docker-compose network, they use the **service name** (not container_name) and the **internal port** (right side of the port mapping).

---

## Question 3: Counting short trips
**Trips in November 2025 with trip_distance <= 1 mile**

```sql
SELECT COUNT(*) as short_trips
FROM green_taxi
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1
```

### ✅ Answer: **8,007**

---

## Question 4: Longest trip for each day
**Which pickup day had the longest trip distance? (excluding trips >= 100 miles)**

```sql
SELECT 
    DATE(lpep_pickup_datetime) as pickup_day,
    MAX(trip_distance) as max_distance
FROM green_taxi
WHERE trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_distance DESC
LIMIT 5
```

Results:
| Pickup Day | Max Distance |
|------------|-------------|
| 2025-11-14 | 88.03 miles |
| 2025-11-20 | 73.84 miles |
| 2025-11-23 | 45.26 miles |
| 2025-11-22 | 40.16 miles |
| 2025-11-15 | 39.81 miles |

### ✅ Answer: **2025-11-14**

---

## Question 5: Biggest pickup zone by total_amount
**Pickup zone with largest total_amount sum on November 18, 2025**

```sql
SELECT 
    z.Zone,
    SUM(g.total_amount) as total
FROM green_taxi g
JOIN zones z ON g.PULocationID = z.LocationID
WHERE DATE(g.lpep_pickup_datetime) = '2025-11-18'
GROUP BY z.Zone
ORDER BY total DESC
```

Results:
| Zone | Total Amount |
|------|-------------|
| East Harlem North | $9,281.92 |
| East Harlem South | $6,696.13 |
| Central Park | $2,378.79 |
| Washington Heights South | $2,139.05 |
| Morningside Heights | $2,100.59 |

### ✅ Answer: **East Harlem North**

---

## Question 6: Largest tip
**Drop-off zone with largest tip for pickups in "East Harlem North" in November 2025**

```sql
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
```

Results:
| Drop-off Zone | Max Tip |
|---------------|---------|
| Yorkville West | $81.89 |
| LaGuardia Airport | $50.00 |
| East Harlem North | $45.00 |

### ✅ Answer: **Yorkville West**

---

## Question 7: Terraform Workflow
**Which sequence describes the workflow for:**
1. Downloading provider plugins and setting up backend
2. Generating proposed changes and auto-executing the plan
3. Removing all resources managed by terraform

| Step | Correct Command |
|------|----------------|
| 1. Init | `terraform init` |
| 2. Apply | `terraform apply -auto-approve` |
| 3. Destroy | `terraform destroy` |

### ✅ Answer: **terraform init, terraform apply -auto-approve, terraform destroy**

---

## Summary of All Answers

| Question | Answer |
|----------|--------|
| Q1 | **24.3.1** |
| Q2 | **db:5432** |
| Q3 | **8,007** |
| Q4 | **2025-11-14** |
| Q5 | **East Harlem North** |
| Q6 | **Yorkville West** |
| Q7 | **terraform init, terraform apply -auto-approve, terraform destroy** |
