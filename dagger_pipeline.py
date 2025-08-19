#!/usr/bin/env python3
"""
Dagger CI Pipeline for Superheroes API

This pipeline runs the complete CI process including:
- Code formatting checks (Black)
- Import sorting checks (isort)
- Linting (Flake8)
- Unit tests with coverage
- Docker image building
"""

import sys
from pathlib import Path

import dagger


async def main():
    """Main pipeline function."""
    config = dagger.Config(log_output=sys.stderr)
    
    async with dagger.Connection(config) as client:
        # Get the source directory
        source = client.host().directory(".", exclude=[
            ".git",
            ".github",
            "__pycache__",
            "*.pyc",
            ".pytest_cache",
            ".coverage",
            "htmlcov",
            "node_modules",
            ".env",
            "*.log"
        ])
        
        print("🚀 Starting Superheroes API CI Pipeline")
        
        # Run all CI steps
        await run_linting_checks(client, source)
        await run_tests(client, source)
        await build_docker_image(client, source)
        
        print("✅ All CI steps completed successfully!")


async def run_linting_checks(client: dagger.Client, source: dagger.Directory):
    """Run code quality checks (Black, isort, Flake8)."""
    print("\n📋 Running code quality checks...")
    
    # Create Python container with dependencies
    python_container = (
        client.container()
        .from_("python:3.10-slim")
        .with_workdir("/app")
        .with_directory("/app", source)
        .with_exec(["pip", "install", "--upgrade", "pip"])
        .with_exec(["pip", "install", "-r", "requirements.txt"])
    )
    
    # Run Black check
    print("  🖤 Checking code formatting with Black...")
    black_result = await (
        python_container
        .with_exec(["black", "--check", "."])
        .stdout()
    )
    print("  ✅ Black formatting check passed")
    
    # Run isort check
    print("  📦 Checking import sorting with isort...")
    isort_result = await (
        python_container
        .with_exec(["isort", "--check-only", "."])
        .stdout()
    )
    print("  ✅ isort import sorting check passed")
    
    # Run Flake8 linting
    print("  🔍 Running Flake8 linting...")
    flake8_result = await (
        python_container
        .with_exec(["flake8", "."])
        .stdout()
    )
    print("  ✅ Flake8 linting passed")
    
    print("✅ All code quality checks passed!")


async def run_tests(client: dagger.Client, source: dagger.Directory):
    """Run unit tests with coverage."""
    print("\n🧪 Running unit tests with coverage...")
    
    # Create test environment with PostgreSQL
    postgres = (
        client.container()
        .from_("postgres:15")
        .with_env_variable("POSTGRES_USER", "postgres")
        .with_env_variable("POSTGRES_PASSWORD", "postgres")
        .with_env_variable("POSTGRES_DB", "test_superheroes")
        .with_exposed_port(5432)
        .as_service()
    )
    
    # Create Python test container
    test_container = (
        client.container()
        .from_("python:3.10-slim")
        .with_workdir("/app")
        .with_directory("/app", source)
        .with_service_binding("postgres", postgres)
        .with_env_variable("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/test_superheroes")
        .with_env_variable("SECRET_KEY", "test-secret-key-for-ci")
        .with_env_variable("DEBUG", "False")
        .with_env_variable("TEST_DATABASE_PREFIX", "test_")
        .with_exec(["apt-get", "update"])
        .with_exec(["apt-get", "install", "-y", "libpq-dev", "gcc"])
        .with_exec(["pip", "install", "--upgrade", "pip"])
        .with_exec(["pip", "install", "-r", "requirements.txt"])
    )
    
    # Wait for PostgreSQL to be ready
    print("  🐘 Waiting for PostgreSQL to be ready...")
    await (
        test_container
        .with_exec(["python", "-c", """
import time
import psycopg2
import sys

for i in range(30):
    try:
        conn = psycopg2.connect(
            host='postgres',
            database='test_superheroes',
            user='postgres',
            password='postgres'
        )
        conn.close()
        print('PostgreSQL is ready!')
        sys.exit(0)
    except psycopg2.OperationalError:
        print(f'Waiting for PostgreSQL... ({i+1}/30)')
        time.sleep(2)

print('PostgreSQL failed to start')
sys.exit(1)
        """])
        .stdout()
    )
    
    # Run database migrations
    print("  🗄️  Running database migrations...")
    await (
        test_container
        .with_exec(["python", "manage.py", "migrate"])
        .stdout()
    )
    
    # Run tests with coverage
    print("  🧪 Running unit tests...")
    test_output = await (
        test_container
        .with_exec(["coverage", "run", "--source=.", "manage.py", "test"])
        .stdout()
    )
    print(f"  📊 Test output:\n{test_output}")
    
    # Generate coverage report
    print("  📊 Generating coverage report...")
    coverage_output = await (
        test_container
        .with_exec(["coverage", "report", "--show-missing"])
        .stdout()
    )
    print(f"  📈 Coverage report:\n{coverage_output}")
    
    print("✅ All tests passed!")


async def build_docker_image(client: dagger.Client, source: dagger.Directory):
    """Build Docker image."""
    print("\n🐳 Building Docker image...")
    
    # Create Dockerfile if it doesn't exist
    dockerfile_content = """
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    libpq-dev \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "superheroes_project.wsgi:application"]
"""
    
    # Build the Docker image
    image = (
        client.container()
        .from_("python:3.10-slim")
        .with_workdir("/app")
        .with_directory("/app", source)
        .with_new_file("/app/Dockerfile", dockerfile_content)
        .with_exec(["apt-get", "update"])
        .with_exec(["apt-get", "install", "-y", "libpq-dev", "gcc"])
        .with_exec(["pip", "install", "--upgrade", "pip"])
        .with_exec(["pip", "install", "-r", "requirements.txt"])
        .with_exec(["python", "manage.py", "collectstatic", "--noinput"])
        .with_exposed_port(8000)
        .with_entrypoint(["gunicorn", "--bind", "0.0.0.0:8000", "superheroes_project.wsgi:application"])
    )
    
    # Test that the image can start
    print("  🔍 Testing Docker image startup...")
    startup_test = (
        image
        .with_env_variable("SECRET_KEY", "test-secret-key")
        .with_env_variable("DEBUG", "False")
        .with_exec(["python", "manage.py", "check"])
    )
    
    await startup_test.stdout()
    print("  ✅ Docker image built and tested successfully!")
    
    print("✅ Docker image build completed!")


async def run_integration_tests(client: dagger.Client, source: dagger.Directory):
    """Run integration tests against the built application."""
    print("\n🔗 Running integration tests...")
    
    # This could include API endpoint tests, health checks, etc.
    # For now, we'll do a basic health check
    
    postgres = (
        client.container()
        .from_("postgres:15")
        .with_env_variable("POSTGRES_USER", "postgres")
        .with_env_variable("POSTGRES_PASSWORD", "postgres")
        .with_env_variable("POSTGRES_DB", "superheroes")
        .with_exposed_port(5432)
        .as_service()
    )
    
    app_container = (
        client.container()
        .from_("python:3.10-slim")
        .with_workdir("/app")
        .with_directory("/app", source)
        .with_service_binding("postgres", postgres)
        .with_env_variable("DATABASE_URL", "postgresql://postgres:postgres@postgres:5432/superheroes")
        .with_env_variable("SECRET_KEY", "test-secret-key-for-integration")
        .with_env_variable("DEBUG", "False")
        .with_exec(["apt-get", "update"])
        .with_exec(["apt-get", "install", "-y", "libpq-dev", "gcc", "curl"])
        .with_exec(["pip", "install", "--upgrade", "pip"])
        .with_exec(["pip", "install", "-r", "requirements.txt"])
        .with_exec(["python", "manage.py", "migrate"])
        .with_exec(["python", "manage.py", "populate_superheroes"])
        .with_exposed_port(8000)
    )
    
    # Start the application in the background
    app_service = (
        app_container
        .with_exec(["gunicorn", "--bind", "0.0.0.0:8000", "superheroes_project.wsgi:application"])
        .as_service()
    )
    
    # Test the health endpoint
    test_container = (
        client.container()
        .from_("curlimages/curl:latest")
        .with_service_binding("app", app_service)
        .with_exec(["curl", "-f", "http://app:8000/health/"])
    )
    
    health_response = await test_container.stdout()
    print(f"  🏥 Health check response: {health_response}")
    
    print("✅ Integration tests passed!")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
