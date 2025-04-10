#!/bin/bash
set -e

# Switch to production environment
python scripts/manage_env.py switch production

# Run database migrations
python scripts/manage_db.py migrate

# Build and start the production containers
docker-compose -f docker-compose.prod.yml up --build -d

# Display container status
docker-compose -f docker-compose.prod.yml ps

echo "Deployment completed successfully!"