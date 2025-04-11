#!/bin/bash
set -e

# Run Alembic migrations
echo "Running migrations..."
alembic upgrade head

# Start the FastAPI application
echo "Starting FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 80