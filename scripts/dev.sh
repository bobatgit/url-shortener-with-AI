#!/bin/bash
set -e

# Switch to development environment
python scripts/manage_env.py switch development

# Run database migrations
python scripts/manage_db.py migrate

# Start the application in development mode
docker-compose up --build