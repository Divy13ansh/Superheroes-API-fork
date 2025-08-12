# Scripts Directory

This directory contains utility scripts for the Superheroes API project.

## 🧪 Test Runner Scripts

### `run-unittest` (Python Script)
Comprehensive Python-based test runner with detailed reporting.

**Usage:**
```bash
python scripts/run-unittest
```

**Features:**
- Runs all unit tests with verbose output
- Generates test coverage reports
- Provides detailed summary and recommendations
- Cross-platform compatibility
- Error handling and graceful exits

### `run-unittest.sh` (Shell Script)
Simple bash script for quick test execution.

**Usage:**
```bash
./scripts/run-unittest.sh
# or
bash scripts/run-unittest.sh
```

**Features:**
- Fast execution
- Automatic virtual environment activation
- Coverage reporting (if available)
- Exit codes for CI/CD integration

## 🎯 Other Scripts

### `test_health.py`
Dedicated test runner for health app only.

**Usage:**
```bash
python scripts/test_health.py
```

### `demo_health.py`
Demo script to test the health endpoint and show documentation URLs.

**Usage:**
```bash
python scripts/demo_health.py
```

## 🚀 Quick Commands

```bash
# Run all tests (recommended)
python scripts/run-unittest

# Run health tests only
python scripts/test_health.py

# Run with shell script
./scripts/run-unittest.sh

# Demo the health endpoint
python scripts/demo_health.py
```

## 📋 Manual Test Commands

If you prefer to run tests manually:

```bash
# Basic test run
python manage.py test

# Verbose output
python manage.py test -v 2

# Health tests only
python manage.py test health

# With coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔧 Requirements

- Python 3.8+
- Django 4.2+
- Virtual environment (recommended)
- Coverage.py (optional, for coverage reports)

## 📊 Expected Output

When all tests pass, you should see:
- ✅ All tests passed successfully!
- 🎉 Your code is ready for deployment!
- 100% coverage for health app

## 🐛 Troubleshooting

If tests fail:
1. Check that all dependencies are installed
2. Ensure virtual environment is activated
3. Verify database migrations are up to date
4. Check for any syntax errors in test files

## 🎯 CI/CD Integration

These scripts return appropriate exit codes:
- `0` - All tests passed
- `1` - Tests failed or errors occurred

Perfect for integration with CI/CD pipelines!
