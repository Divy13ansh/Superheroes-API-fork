#!/usr/bin/env python3
import asyncio
import sys

import dagger


async def test():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # Get reference to the local project
        src = client.host().directory(
            ".",
            exclude=[
                "env/",
                "test_env/",
                ".git/",
                "__pycache__/",
                "*.pyc",
                ".pytest_cache/",
                ".coverage",
                "*.log",
                "node_modules/",
            ],
        )

        # PostgreSQL service with memory optimizations
        postgres = (
            client.container()
            .from_("postgres:15-alpine")
            .with_env_variable("POSTGRES_USER", "postgres")
            .with_env_variable("POSTGRES_PASSWORD", "postgres")
            .with_env_variable("POSTGRES_DB", "test_superheroes")
            .with_env_variable("POSTGRES_HOST_AUTH_METHOD", "trust")
            .with_env_variable("POSTGRES_INITDB_ARGS", "--auth-host=trust")
            .with_env_variable("POSTGRES_MAX_CONNECTIONS", "10")
            .with_env_variable("POSTGRES_SHARED_BUFFERS", "16MB")
            .with_env_variable("POSTGRES_WORK_MEM", "1MB")
            .with_env_variable("POSTGRES_MAINTENANCE_WORK_MEM", "8MB")
            .with_env_variable("POSTGRES_CHECKPOINT_COMPLETION_TARGET", "0.9")
            .with_env_variable("POSTGRES_WAL_BUFFERS", "1MB")
            .with_env_variable("POSTGRES_DEFAULT_STATISTICS_TARGET", "10")
            .with_exposed_port(5432)
            .as_service()
        )

        # Base Python container with aggressive caching
        base_python = (
            client.container()
            .from_("python:3.10-slim")
            .with_exec(["apt-get", "update"])
            .with_exec(
                [
                    "apt-get",
                    "install",
                    "-y",
                    "libpq-dev",
                    "gcc",
                    "git",
                    "--no-install-recommends",
                ]
            )
            .with_exec(["apt-get", "clean"])
            .with_exec(["rm", "-rf", "/var/lib/apt/lists/*"])
            .with_exec(["pip", "install", "--upgrade", "pip", "wheel"])
        )

        # Cache Python dependencies
        python_deps = (
            base_python.with_file("/tmp/requirements.txt", src.file("requirements.txt"))
            .with_exec(
                [
                    "pip",
                    "install",
                    "--no-deps",
                    "--cache-dir",
                    "/pip-cache",
                    "-r",
                    "/tmp/requirements.txt",
                ]
            )
            .with_exec(
                [
                    "pip",
                    "install",
                    "--cache-dir",
                    "/pip-cache",
                    "black",
                    "isort",
                    "flake8",
                    "coverage",
                ]
            )
        )

        # Linting job
        async def run_linting():
            linting = (
                python_deps.with_directory("/app", src)
                .with_workdir("/app")
                .with_exec(["python", "-m", "py_compile", "manage.py"])
                .with_exec(["black", "--check", "."])
                .with_exec(["isort", "--check-only", "."])
                .with_exec(["flake8", "."])
            )

            print("Running linting checks...")
            await linting.sync()
            print("Linting completed!")

        # Testing job
        async def run_tests():
            testing = (
                python_deps.with_directory("/app", src)
                .with_workdir("/app")
                .with_service_binding("postgres", postgres)
                .with_env_variable(
                    "DATABASE_URL",
                    "postgresql://postgres:postgres@postgres:5432/test_superheroes",
                )
                .with_env_variable("SECRET_KEY", "test-secret-key")
                .with_env_variable("DEBUG", "False")
                .with_exec(
                    [
                        "sh",
                        "-c",
                        """
                    echo "Waiting for PostgreSQL..."
                    for i in $(seq 1 15); do
                        if python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='postgres',
        database='test_superheroes',
        user='postgres',
        password='postgres',
        connect_timeout=2
    )
    conn.close()
    exit(0)
except:
    exit(1)
" 2>/dev/null; then
                            break
                        fi
                        sleep 0.5
                    done

                    echo "Running migrations..."
                    python manage.py migrate --verbosity=0

                    echo "Running tests..."
                    python manage.py test --verbosity=2 --parallel auto --keepdb
                    """,
                    ]
                )
            )

            print("Running tests...")
            await testing.sync()
            print("Tests completed!")

        # Security scan job
        # async def run_security():
        #     security = (
        #         python_deps.with_directory("/app", src)
        #         .with_workdir("/app")
        #         .with_exec(["pip", "install", "safety", "bandit"])
        #         .with_exec(["safety", "check", "--json"])
        #         .with_exec(
        #             ["bandit", "-r", ".", "-f", "json", "-x", "*/env/*,*/test_env/*"]
        #         )
        #     )

        #     print("Running security checks...")
        #     await security.sync()
        #     print("Security checks completed!")

        # Coverage job
        async def run_coverage():
            coverage = (
                python_deps.with_directory("/app", src)
                .with_workdir("/app")
                .with_service_binding("postgres", postgres)
                .with_env_variable(
                    "DATABASE_URL",
                    "postgresql://postgres:postgres@postgres:5432/test_superheroes",
                )
                .with_env_variable("SECRET_KEY", "test-secret-key")
                .with_env_variable("DEBUG", "False")
                .with_exec(
                    [
                        "sh",
                        "-c",
                        """
                    echo "Waiting for PostgreSQL..."
                    for i in $(seq 1 15); do
                        if python -c "
import psycopg2
try:
    conn = psycopg2.connect(
        host='postgres',
        database='test_superheroes',
        user='postgres',
        password='postgres',
        connect_timeout=2
    )
    conn.close()
    exit(0)
except:
    exit(1)
" 2>/dev/null; then
                            break
                        fi
                        sleep 0.5
                    done

                    echo "Running migrations..."
                    python manage.py migrate --verbosity=0

                    echo "Running coverage..."
                    coverage run --source='.' manage.py test --keepdb
                    coverage report --show-missing
                    coverage html
                    """,
                    ]
                )
            )

            print("Running coverage analysis...")
            await coverage.sync()
            print("Coverage analysis completed!")

        # Run all jobs in parallel
        print("Starting CI pipeline...")
        start_time = asyncio.get_event_loop().time()

        # await asyncio.gather(run_linting(), run_tests(), run_security(), run_coverage())
        await asyncio.gather(
            run_linting(),
        )
        await asyncio.gather(run_tests())

        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time

        print(f"CI pipeline completed in {duration:.2f} seconds!")

        if duration > 120:
            print("WARNING: Pipeline took longer than 2 minutes")
        else:
            print("SUCCESS: Pipeline completed under 2 minutes!")


if __name__ == "__main__":
    asyncio.run(test())
