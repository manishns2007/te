#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing backend dependencies..."
pip install -r requirements.txt

echo "Generating mock data and training XGBoost model..."
python scripts/seed_database.py

echo "Build complete."
