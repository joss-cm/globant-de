# FastAPI & PostgreSQL Data Loader

## Project Overview
This project provides a REST API built with FastAPI and PostgreSQL to handle CSV data ingestion. It includes:
- A structured database model (star schema).
- Batch data insertion (up to 1000 rows per request).
- API endpoints to upload CSV files.

## Prerequisites

### 1. Install Dependencies (MacOS)
1. **Install Docker** (Version `4.37` recommended to avoid malware warnings):
   ```bash
   brew install --cask docker
   ```
2. **Install Git**:
   ```bash
   brew install git
   ```
3. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo-name.git
   cd your-repo-name
   ```

## 2. Setting up Docker & PostgreSQL

### - Pull and Run PostgreSQL
1. **Pull the PostgreSQL image**:
   ```bash
   docker pull postgres:15
   ```
2. **Start containers with Docker Compose**:
   ```bash
   docker-compose up --build
   ```
   _(If you encounter errors, restart using: `docker compose down -v` and repeat step 2)_

3. **Verify PostgreSQL is running**:
   ```bash
   docker exec -it postgres_local psql -U admin -d testdb
   ```
   Inside PostgreSQL, check existing tables:
   ```sql
   \dt
   ```

## Loading CSV Data

To load CSV files into the database:

```bash
docker exec -it api_service python -m scripts.load_csv
```

Expected Output:
```bash
Departments loaded successfully!
Jobs loaded successfully!
Hired employees loaded successfully!
```

## Debugging & Useful Commands

- **Check running containers**:
  ```bash
  docker ps -a
  ```
- **Restart API container**:
  ```bash
  docker restart api_service
  ```
- **Check logs**:
  ```bash
  docker logs api_service --tail 50
  ```
- **Shut down everything**:
  ```bash
  docker compose down -v
  ```

## API Testing

Once the API is running, test the connection:
```bash
curl http://localhost:8000/ping
```
Expected Response:
```json
{"message":"API is running!"}
```

## Contribution
1. Fork the repository.
2. Create a feature branch: `git checkout -b feature-branch`
3. Commit changes: `git commit -m "Description"`
4. Push changes: `git push origin feature-branch`
5. Submit a pull request.

---

💡 **Tip:** If you encounter issues, restart Docker and verify `.env` variables are correctly set!
