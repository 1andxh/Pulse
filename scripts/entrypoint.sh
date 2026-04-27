#!/bin/bash
set -e

echo "checking database migrations..."
uv run alembic upgrade head

echo "starting Pulse..."
exec uvicorn src:app --host 0.0.0.0 --port 8000 --workers 1


echo "_______________________________________"
