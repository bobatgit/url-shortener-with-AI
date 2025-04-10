#!/bin/bash
set -e

# Configuration
HOST=${1:-"localhost"}
PORT=${2:-"8000"}
ENDPOINT="http://$HOST:$PORT/monitoring/health"
MAX_RETRIES=5
RETRY_INTERVAL=5

check_health() {
    local status_code=$(curl -s -o /dev/null -w "%{http_code}" $ENDPOINT)
    if [ $status_code -eq 200 ]; then
        return 0
    else
        return 1
    fi
}

echo "Checking health at $ENDPOINT"

for i in $(seq 1 $MAX_RETRIES); do
    if check_health; then
        echo "Service is healthy!"
        exit 0
    else
        echo "Attempt $i of $MAX_RETRIES failed. Retrying in ${RETRY_INTERVAL}s..."
        sleep $RETRY_INTERVAL
    fi
done

echo "Service health check failed after $MAX_RETRIES attempts"
exit 1