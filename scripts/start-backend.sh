#!/bin/bash

set -e

# Apply database migrations
echo "Applying database migrations..."
alembic upgrade head

# Start FastAPI server
echo "Starting server..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
