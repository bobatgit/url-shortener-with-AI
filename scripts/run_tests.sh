#!/bin/bash
set -e

# Switch to testing environment
python scripts/manage_env.py switch testing

# Run pytest with coverage
pytest --cov=app --cov-report=html

# Display results summary
echo "Test execution completed. Coverage report available in htmlcov/index.html"