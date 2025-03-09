#!/bin/sh
echo "Waiting for PostgreSQL to start..."
sleep 5

echo "Creating tables in the database..."
python -c "from src.models import Department, Job, HiredEmployee; from src.database import Base, engine; Base.metadata.create_all(engine)"

echo "Starting FastAPI Server..."
exec uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload
