#!/bin/bash
# run.sh - Start the picture frame

cd "$(dirname "$0")"

echo "Starting E-Ink Picture Frame..."

# Activate virtual environment
source venv/bin/activate

# Run the application
python src/main.py