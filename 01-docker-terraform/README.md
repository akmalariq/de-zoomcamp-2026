# Module 1 Homework: Docker & SQL

## 📋 Overview

This module covers Docker fundamentals, SQL queries, and Terraform for infrastructure provisioning. The homework involves working with NYC taxi trip data using Docker containers and PostgreSQL.

## 🎯 Homework Questions

### Question 1: Understanding Docker Images

**Task**: Run docker with the `python:3.13` image using `bash` as the entrypoint and find the pip version.

**Command**:
```bash
docker run -it --entrypoint bash python:3.13
pip --version
```

**Answer**: 
```
# TODO: Add answer after running the command
```

---

### Question 2: Understanding Docker Networking and docker-compose

**Task**: Given the docker-compose.yaml configuration, determine the hostname and port that pgadmin should use to connect to postgres.

**Docker Compose Configuration**:
```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

**Options**:
- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- db:5432

**Answer**: 
```
# TODO: Add answer
```

**Explanation**:
```
# TODO: Explain why this is the correct answer
```

---

## 📊 Data Preparation

### Download Required Datasets

**Green Taxi Trips Data (November 2025)**:
```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
```

**Taxi Zone Lookup Data**:
```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

### Data Ingestion

```bash
# TODO: Add commands/scripts used to ingest data into PostgreSQL
```

---

## 🔍 SQL Questions

### Question 3: Counting Short Trips

**Task**: For trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive), count trips with trip_distance ≤ 1 mile.

**SQL Query**:
```sql
-- TODO: Add SQL query
SELECT COUNT(*)
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01'
  AND lpep_pickup_datetime < '2025-12-01'
  AND trip_distance <= 1;
```

**Options**:
- 7,853
- 8,007
- 8,254
- 8,421

**Answer**: 
```
# TODO: Add answer
```

---

### Question 4: Longest Trip for Each Day

**Task**: Find the pickup day with the longest trip distance (excluding trips ≥ 100 miles to avoid data errors).

**SQL Query**:
```sql
-- TODO: Add SQL query
SELECT DATE(lpep_pickup_datetime) as pickup_date,
       MAX(trip_distance) as max_distance
FROM green_taxi_trips
WHERE trip_distance < 100
GROUP BY DATE(lpep_pickup_datetime)
ORDER BY max_distance DESC
LIMIT 1;
```

**Options**:
- 2025-11-14
- 2025-11-20
- 2025-11-23
- 2025-11-25

**Answer**: 
```
# TODO: Add answer
```

---

### Question 5: Biggest Pickup Zone

**Task**: Find the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025.

**SQL Query**:
```sql
-- TODO: Add SQL query with JOIN to taxi_zone_lookup
SELECT tz.Zone,
       SUM(gt.total_amount) as total_revenue
FROM green_taxi_trips gt
JOIN taxi_zone_lookup tz ON gt.PULocationID = tz.LocationID
WHERE DATE(gt.lpep_pickup_datetime) = '2025-11-18'
GROUP BY tz.Zone
ORDER BY total_revenue DESC
LIMIT 1;
```

**Options**:
- East Harlem North
- East Harlem South
- Morningside Heights
- Forest Hills

**Answer**: 
```
# TODO: Add answer
```

---

### Question 6: Largest Tip

**Task**: For passengers picked up in "East Harlem North" in November 2025, find the drop-off zone with the largest tip.

**SQL Query**:
```sql
-- TODO: Add SQL query with JOINs
SELECT dz.Zone as dropoff_zone,
       MAX(gt.tip_amount) as max_tip
FROM green_taxi_trips gt
JOIN taxi_zone_lookup pz ON gt.PULocationID = pz.LocationID
JOIN taxi_zone_lookup dz ON gt.DOLocationID = dz.LocationID
WHERE pz.Zone = 'East Harlem North'
  AND gt.lpep_pickup_datetime >= '2025-11-01'
  AND gt.lpep_pickup_datetime < '2025-12-01'
GROUP BY dz.Zone
ORDER BY max_tip DESC
LIMIT 1;
```

**Options**:
- JFK Airport
- Yorkville West
- East Harlem North
- LaGuardia Airport

**Answer**: 
```
# TODO: Add answer
```

---

## ☁️ Terraform

### Question 7: Terraform Workflow

**Task**: Identify the correct sequence for:
1. Downloading provider plugins and setting up backend
2. Generating proposed changes and auto-executing the plan
3. Removing all resources managed by Terraform

**Options**:
- terraform import, terraform apply -y, terraform destroy
- terraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy
- terraform import, terraform apply -y, terraform rm

**Answer**: 
```
# TODO: Add answer
```

**Explanation**:
```
# TODO: Explain each command in the workflow
```

### Terraform Configuration

```bash
# TODO: Add terraform commands used to provision GCP resources
terraform init
terraform plan
terraform apply
```

**Resources Created**:
- [ ] GCP Bucket
- [ ] BigQuery Dataset

---

## 📝 Notes

### Key Learnings

1. **Docker Networking**:
   - Containers in the same docker-compose network can communicate using service names
   - Port mapping format: `host_port:container_port`

2. **SQL Best Practices**:
   - Use proper date filtering with exclusive upper bounds
   - JOIN tables efficiently for zone lookups
   - Filter out data errors (e.g., trip_distance >= 100)

3. **Terraform Workflow**:
   - `init`: Initialize and download providers
   - `plan`: Preview changes
   - `apply`: Execute changes
   - `destroy`: Remove resources

### Challenges Faced

```
# TODO: Document any challenges and how you solved them
```

---

## 🔗 Resources

- [Course Repository](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- [Module 1 Materials](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/cohorts/2026/01-docker-terraform)
- [Homework Submission Form](https://courses.datatalks.club/de-zoomcamp-2026/homework/hw1)

---

## ✅ Submission Checklist

- [ ] All questions answered
- [ ] SQL queries tested and verified
- [ ] Terraform resources created successfully
- [ ] Code pushed to GitHub repository
- [ ] README updated with solutions
- [ ] Homework submitted via form
- [ ] Shared progress on LinkedIn/Twitter (optional)

---

**Completed**: [Date]

**Time Spent**: [Hours]
