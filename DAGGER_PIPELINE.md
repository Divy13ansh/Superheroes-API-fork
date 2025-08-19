# Dagger CI Pipeline for Superheroes API

This document describes the Dagger CI pipeline implementation for the Superheroes API project.

## Overview

The Dagger pipeline provides a containerized CI/CD solution that runs:
- Code quality checks (Black, isort, Flake8)
- Unit tests with coverage reporting
- Docker image building and testing
- Integration tests

## Prerequisites

- Python 3.10+
- Docker (for Dagger to create containers)
- PostgreSQL (handled automatically by Dagger)

## Installation

1. Install Dagger dependencies:
   ```bash
   pip install -r requirements-dagger.txt
   ```

2. Ensure Docker is running on your system

## Usage

### Quick Start

Run the complete CI pipeline:
```bash
./scripts/run-dagger-ci.sh
```

### Manual Execution

Run the Dagger pipeline directly:
```bash
python3 dagger_pipeline.py
```

## Pipeline Stages

### 1. Code Quality Checks
- **Black**: Code formatting verification
- **isort**: Import sorting verification  
- **Flake8**: Linting and style checks

### 2. Unit Tests
- Sets up PostgreSQL test database
- Runs Django migrations
- Executes all unit tests with coverage
- Generates coverage reports

### 3. Docker Image Build
- Creates production-ready Docker image
- Tests image startup and basic functionality
- Validates Django configuration

### 4. Integration Tests (Optional)
- Health endpoint verification
- API endpoint testing
- End-to-end functionality validation

## Configuration

### Environment Variables

The pipeline uses these environment variables:

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: Django secret key for testing
- `DEBUG`: Set to False for production-like testing
- `TEST_DATABASE_PREFIX`: Prefix for test databases

### Customization

You can modify `dagger_pipeline.py` to:
- Add additional test stages
- Modify container configurations
- Add deployment steps
- Integrate with external services

## Pipeline Architecture

```
┌─────────────────┐
│   Source Code   │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Code Quality    │
│ - Black         │
│ - isort         │
│ - Flake8        │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Unit Tests      │
│ - PostgreSQL    │
│ - Django Tests  │
│ - Coverage      │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Docker Build    │
│ - Image Build   │
│ - Startup Test  │
└─────────┬───────┘
          │
          ▼
┌─────────────────┐
│ Integration     │
│ - Health Check  │
│ - API Tests     │
└─────────────────┘
```

## Benefits of Dagger

1. **Reproducible**: Same environment across all machines
2. **Fast**: Efficient caching and parallelization
3. **Portable**: Works on any system with Docker
4. **Programmable**: Pipeline as code in Python
5. **Debuggable**: Easy to test and modify locally

## Troubleshooting

### Common Issues

1. **Docker not running**:
   ```
   Error: Cannot connect to the Docker daemon
   ```
   Solution: Start Docker Desktop or Docker daemon

2. **Permission errors**:
   ```
   Permission denied: './scripts/run-dagger-ci.sh'
   ```
   Solution: `chmod +x scripts/run-dagger-ci.sh`

3. **Python import errors**:
   ```
   ModuleNotFoundError: No module named 'dagger'
   ```
   Solution: `pip install -r requirements-dagger.txt`

### Debug Mode

To run with verbose output:
```bash
DAGGER_LOG_LEVEL=debug python3 dagger_pipeline.py
```

## Integration with GitHub Actions

You can integrate this Dagger pipeline with GitHub Actions:

```yaml
name: Dagger CI
on: [push, pull_request]

jobs:
  ci:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Run Dagger Pipeline
      run: |
        pip install -r requirements-dagger.txt
        python3 dagger_pipeline.py
```

## Performance

Typical pipeline execution times:
- Code Quality: ~30 seconds
- Unit Tests: ~2-3 minutes
- Docker Build: ~1-2 minutes
- Integration Tests: ~1 minute

Total: ~5-7 minutes

## Security

The pipeline follows security best practices:
- No secrets in code
- Isolated container environments
- Minimal container privileges
- Secure database connections

## Contributing

To modify the pipeline:

1. Edit `dagger_pipeline.py`
2. Test locally: `python3 dagger_pipeline.py`
3. Update documentation if needed
4. Submit pull request

## Support

For issues with the Dagger pipeline:
1. Check the troubleshooting section
2. Review Dagger logs
3. Open an issue with pipeline output
