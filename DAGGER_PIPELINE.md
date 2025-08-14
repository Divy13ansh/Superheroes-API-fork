# Dagger Pipeline for Superheroes API

This document describes the Dagger-based CI/CD pipeline that replaces the GitHub Actions workflow defined in `.github/workflows/ci.yml`.

## Overview

The Dagger pipeline provides the same DevSecOps capabilities as the original GitHub Actions workflow but with the following advantages:

- **Local Development**: Run the entire CI/CD pipeline locally
- **Consistency**: Same pipeline runs locally and in CI/CD
- **Language Native**: Written in Python, matching your Django application
- **Portable**: Works across different CI/CD platforms
- **Faster Feedback**: No need to push to see pipeline results

## Pipeline Stages

### 1. Setup and Test (`setup_and_test`)
- Sets up Python 3.9 environment
- Starts PostgreSQL service for testing
- Installs dependencies from `requirements.txt`
- Runs Django unit tests
- Performs code quality checks:
  - **Black**: Code formatting
  - **isort**: Import sorting
  - **Flake8**: Linting

### 2. Security Scans (`security_scans`)
- **PyRaider**: Static Composition Analysis for vulnerabilities
- **Trufflehog**: Secret scanning in codebase

### 3. License Compliance (`license_compliance`)
- Generates license report using `pip-licenses`
- Runs license compliance script if available

### 4. Docker Security Scan (`docker_security_scan`)
- Builds Docker image (creates basic Dockerfile if missing)
- Runs **Dockle** security scan on the built image

## Usage

### Prerequisites

1. **Install Dagger CLI**:
   ```bash
   curl -L https://dl.dagger.io/dagger/install.sh | sh
   ```

2. **Set Environment Variables**:
   ```bash
   export SECRET_KEY="your-django-secret-key"
   export DOCKER_USERNAME="your-docker-username"  # Optional
   export DOCKER_PASSWORD="your-docker-password"  # Optional
   ```

### Running the Pipeline

#### Option 1: Using the Shell Script (Recommended)

```bash
# Quick test (development)
./run-dagger.sh quick

# Full pipeline
./run-dagger.sh full

# Security scans only
./run-dagger.sh security

# Docker security scan only
./run-dagger.sh docker

# Setup and tests only
./run-dagger.sh setup
```

#### Option 2: Using Dagger CLI Directly

```bash
# Install Python dependencies
pip install -r requirements-dagger.txt

# Run specific functions
dagger call quick-test --source=. --secret-key=env:SECRET_KEY
dagger call pipeline --source=. --secret-key=env:SECRET_KEY
dagger call security-scans --source=.
dagger call docker-security-scan --source=.
```

#### Option 3: Using Python Directly

```bash
python dagger.py
```

## Pipeline Functions

### `pipeline(source, secret_key, docker_username?, docker_password?)`
Runs the complete DevSecOps pipeline equivalent to the GitHub Actions workflow.

### `quick_test(source, secret_key)`
Runs a subset of checks for rapid development feedback:
- Django system check
- Code formatting check
- Linting

### `setup_and_test(source, secret_key)`
Sets up the environment and runs comprehensive tests and linting.

### `security_scans(source)`
Runs security vulnerability and secret scanning.

### `license_compliance(source)`
Checks package license compliance.

### `docker_security_scan(source)`
Builds Docker image and runs security scan.

## Comparison with GitHub Actions

| Feature | GitHub Actions | Dagger |
|---------|----------------|--------|
| **Environment** | Ubuntu Latest | Python 3.9 Slim |
| **PostgreSQL** | Service Container | Dagger Service |
| **Python Setup** | actions/setup-python@v2 | Python Container |
| **Dependencies** | pip install | pip install |
| **Tests** | python manage.py test | python manage.py test |
| **Linting** | black, isort, flake8 | black, isort, flake8 |
| **Security** | pyraider, trufflehog3 | pyraider, trufflehog3 |
| **License Check** | pip-licenses + script | pip-licenses + script |
| **Docker Build** | docker build | Dagger build |
| **Docker Scan** | dockle-action | dockle container |
| **Secrets** | GitHub Secrets | Dagger Secrets |

## Advantages of Dagger Approach

1. **Local Testing**: Test your entire CI/CD pipeline locally before pushing
2. **Faster Iteration**: No waiting for CI/CD runners
3. **Consistent Environment**: Same containers locally and in CI/CD
4. **Language Integration**: Native Python code, easier to maintain
5. **Portable**: Works with any CI/CD system (GitHub Actions, GitLab CI, Jenkins, etc.)
6. **Caching**: Intelligent caching reduces build times
7. **Debugging**: Easier to debug pipeline issues locally

## Integration with Existing CI/CD

You can integrate this Dagger pipeline with your existing CI/CD systems:

### GitHub Actions Integration
```yaml
name: Dagger Pipeline
on: [push, pull_request]
jobs:
  dagger:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: dagger/dagger-for-github@v3
      with:
        verb: call
        args: pipeline --source=. --secret-key=env:SECRET_KEY
      env:
        SECRET_KEY: ${{ secrets.SECRET_KEY }}
```

### GitLab CI Integration
```yaml
dagger:
  image: dagger/dagger:latest
  script:
    - dagger call pipeline --source=. --secret-key=env:SECRET_KEY
  variables:
    SECRET_KEY: $SECRET_KEY
```

## Customization

The pipeline is modular and can be easily customized:

1. **Add New Stages**: Create new functions in the `SuperheroesCI` class
2. **Modify Containers**: Change base images or add new tools
3. **Environment Variables**: Add new secrets or configuration
4. **Conditional Logic**: Add conditions based on branch, environment, etc.

## Troubleshooting

### Common Issues

1. **Docker Permission Issues**:
   ```bash
   sudo usermod -aG docker $USER
   # Log out and back in
   ```

2. **Secret Key Missing**:
   ```bash
   export SECRET_KEY="your-secret-key"
   ```

3. **Dagger CLI Not Found**:
   ```bash
   curl -L https://dl.dagger.io/dagger/install.sh | sh
   export PATH="$HOME/.local/bin:$PATH"
   ```

4. **Python Dependencies**:
   ```bash
   pip install -r requirements-dagger.txt
   ```

## Performance Tips

1. **Use Caching**: Dagger automatically caches layers
2. **Parallel Execution**: Independent stages run in parallel
3. **Minimal Base Images**: Use slim images for faster pulls
4. **Layer Optimization**: Order operations from least to most frequently changing

## Next Steps

1. **Customize** the pipeline for your specific needs
2. **Integrate** with your preferred CI/CD platform
3. **Add** additional security tools or checks
4. **Optimize** for your team's workflow
5. **Monitor** pipeline performance and adjust as needed

The Dagger pipeline provides a modern, efficient, and developer-friendly approach to CI/CD that maintains all the security and quality checks of your original GitHub Actions workflow while offering improved local development experience.
