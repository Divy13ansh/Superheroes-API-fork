#!/bin/bash

# Superheroes API - Unit Test Runner
# Simple shell script to run all unit tests

echo "============================================================"
echo "🧪 SUPERHEROES API - UNIT TEST RUNNER"
echo "============================================================"

# Change to project directory
cd "$(dirname "$0")/.."

# Activate virtual environment if it exists
if [ -f "env/bin/activate" ]; then
    echo "📦 Activating virtual environment..."
    source env/bin/activate
fi

echo ""
echo "📋 Running all unit tests..."
echo "----------------------------------------"

# Run all tests with verbose output
python manage.py test --verbosity=2

TEST_EXIT_CODE=$?

echo ""
echo "📋 Running health app tests specifically..."
echo "----------------------------------------"

# Run health tests specifically
python manage.py test health --verbosity=2

HEALTH_EXIT_CODE=$?

echo ""
echo "📋 Generating test coverage report..."
echo "----------------------------------------"

# Run coverage if available
if command -v coverage &> /dev/null; then
    coverage run --source='.' manage.py test
    echo ""
    echo "📊 Overall Coverage:"
    coverage report
    echo ""
    echo "📊 Health App Coverage:"
    coverage report --include="health/*"
else
    echo "⚠️  Coverage not installed. Install with: pip install coverage"
fi

echo ""
echo "============================================================"
echo "📋 TEST SUMMARY"
echo "============================================================"

if [ $TEST_EXIT_CODE -eq 0 ] && [ $HEALTH_EXIT_CODE -eq 0 ]; then
    echo "✅ All tests passed successfully!"
    echo "🎉 Your code is ready for deployment!"
    exit 0
else
    echo "❌ Some tests failed!"
    echo "🔧 Please fix the failing tests before proceeding."
    exit 1
fi
