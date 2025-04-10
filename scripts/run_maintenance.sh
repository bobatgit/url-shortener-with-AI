#!/bin/bash
set -e

echo "Running URL cleanup..."
python scripts/maintenance.py cleanup

echo "Displaying database statistics..."
python scripts/maintenance.py stats