# Quick Start Guide

## 🚀 Getting Started

### 1. Initialize Git Repository

```bash
cd /home/neo/projects/de-zoomcamp-2026
git init
git add .
git commit -m "Initial commit: DE Zoomcamp 2026 repository setup"
```

### 2. Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository named `de-zoomcamp-2026`
3. **Do NOT** initialize with README, .gitignore, or license (we already have these)

### 3. Push to GitHub

```bash
git remote add origin git@github.com:YOUR_USERNAME/de-zoomcamp-2026.git
git branch -M main
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

---

## 📚 Working on Module 1

### Setup Docker Environment

1. **Create docker-compose.yml** in `module-01-docker-terraform/`:

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

2. **Start the services**:

```bash
cd module-01-docker-terraform
docker-compose up -d
```

3. **Access pgAdmin**:
   - Open browser: http://localhost:8080
   - Login: pgadmin@pgadmin.com / pgadmin

### Download Data

```bash
cd module-01-docker-terraform/homework

# Download green taxi data
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet

# Download zone lookup data
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

### Ingest Data into PostgreSQL

You'll need to create a Python script to:
1. Read the parquet file
2. Convert to pandas DataFrame
3. Insert into PostgreSQL

Example script location: `module-01-docker-terraform/scripts/ingest_data.py`

---

## 📝 Workflow

1. **Work on homework questions** in `module-01-docker-terraform/`
2. **Update README.md** with your answers and SQL queries
3. **Take notes** in `module-01-docker-terraform/notes/`
4. **Commit your progress**:
   ```bash
   git add .
   git commit -m "Completed Question X"
   git push
   ```

---

## ✅ Before Submission

- [ ] All questions answered in README
- [ ] SQL queries tested and working
- [ ] Code pushed to GitHub
- [ ] Repository is public
- [ ] Submit via [homework form](https://courses.datatalks.club/de-zoomcamp-2026/homework/hw1)

---

## 🌟 Share Your Progress

Post on LinkedIn or Twitter using the templates in the main README!

---

## 🔗 Useful Commands

### Docker
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Access postgres CLI
docker exec -it postgres psql -U postgres -d ny_taxi
```

### Git
```bash
# Check status
git status

# Add all changes
git add .

# Commit with message
git commit -m "Your message"

# Push to GitHub
git push

# View commit history
git log --oneline
```

---

Good luck with your Data Engineering journey! 🚀
