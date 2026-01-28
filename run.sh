#!/bin/bash
cd "$(dirname "$0")"

echo "Starting E-Ink Picture Frame..."

source venv/bin/activate
python src/main.py