#!/bin/bash

# Dagger CI Pipeline Runner for Superheroes API

set -e

echo "============================================================"
echo "🚀 SUPERHEROES API - DAGGER CI PIPELINE"
echo "============================================================"

# Change to project directory
cd "$(dirname "$0")/.."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is required but not installed."
    exit 1
fi

# Activate virtual environment if it exists
if [ -f "env/bin/activate" ]; then
    echo "📦 Activating virtual environment..."
    source env/bin/activate
fi

# Check if Dagger is installed
echo "🔍 Checking Dagger installation..."
if ! python3 -c "import dagger" 2>/dev/null; then
    echo "📥 Installing Dagger dependencies..."
    pip3 install -r requirements_dagger.txt
else
    echo "✅ Dagger is already installed"
fi

echo ""
echo "🚀 Running Dagger CI Pipeline with detailed output..."
echo "============================================================"

# Run the Dagger pipeline with verbose output to show packages, tests, etc.
PYTHONUNBUFFERED=1 python3 dagger_pipeline.py 2>&1

PIPELINE_EXIT_CODE=$?

echo ""
echo "============================================================"
echo "📋 PIPELINE SUMMARY"
echo "============================================================"

if [ $PIPELINE_EXIT_CODE -eq 0 ]; then
    echo "✅ Dagger CI Pipeline completed successfully!"
    echo "🎉 All linting and tests passed!"
    echo ""
    echo ""
    echo "💡 View detailed analytics at: https://dagger.cloud"
    exit 0
else
    echo "❌ Dagger CI Pipeline failed!"
    echo "🔧 Please check the error messages above and fix issues."
    exit 1
fi
