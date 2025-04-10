#!/bin/bash
set -e

echo "Creating data directory if it doesn't exist..."
mkdir -p data

echo "Initializing database..."
python scripts/manage_db.py init

echo "Running migrations..."
python scripts/manage_db.py migrate

echo "Database setup completed successfully!"