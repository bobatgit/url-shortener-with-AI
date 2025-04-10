#!/bin/bash
set -e

echo "Setting up URL Shortener development environment..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install development dependencies
echo "Installing development dependencies..."
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "Setting up pre-commit hooks..."
pre-commit install

# Initialize development database
echo "Initializing development database..."
python scripts/manage_env.py switch development
python scripts/manage_db.py init
python scripts/manage_db.py migrate

# Create necessary directories
mkdir -p data
mkdir -p logs

echo "Development environment setup complete!"
echo "Run 'source venv/bin/activate' to activate the virtual environment"
echo "Run 'make run-dev' to start the development server"