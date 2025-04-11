#!/bin/bash
set -e

# Wait for the database to be ready (using pg_isready or a custom loop)
until pg_isready -h db -p 5432; do
    echo "Waiting for the PostgreSQL database at db:5432..."
    sleep 1
done

# Run Alembic migrations
echo "Running migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 80
