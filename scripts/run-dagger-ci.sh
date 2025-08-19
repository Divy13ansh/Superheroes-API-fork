#!/bin/bash

# Dagger CI Pipeline Runner for Superheroes API

set -e

echo "Superheroes API - Dagger CI Pipeline"
echo "===================================="

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if Dagger is installed
echo "Checking Dagger installation..."
if ! python3 -c "import dagger" 2>/dev/null; then
    echo "Installing Dagger..."
    pip3 install -r requirements-dagger.txt
else
    echo "Dagger is already installed"
fi

# Run the Dagger pipeline
echo ""
echo "Running Dagger CI Pipeline..."
echo "============================="

python3 dagger_pipeline.py

echo ""
echo "Dagger CI Pipeline completed successfully!"
echo "========================================"
