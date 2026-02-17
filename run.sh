#!/bin/bash
export PYTHONPATH=$PYTHONPATH:$(pwd)/backend
echo "Using python: $(which python3)"
echo "Installing dependencies..."
python3 -m pip install -r backend/requirements.txt
echo "Seeding data..."
python3 backend/seed_data.py
echo "Starting Server..."
python3 -m uvicorn backend.app.main:app --reload --port 8000
