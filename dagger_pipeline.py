#!/usr/bin/env python3
import sys
import asyncio
import dagger


async def test():
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # Get reference to the local project (excluding heavy directories)
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
            ],
        )

        # Create optimized PostgreSQL service (Alpine for speed)
        postgres = (
            client.container()
            .from_("postgres:15-alpine")
            .with_env_variable("POSTGRES_USER", "postgres")
            .with_env_variable("POSTGRES_PASSWORD", "postgres")
            .with_env_variable("POSTGRES_DB", "test_superheroes")
            .with_env_variable("POSTGRES_HOST_AUTH_METHOD", "trust")
            .with_env_variable("POSTGRES_INITDB_ARGS", "--auth-host=trust")
            # Optimize PostgreSQL for speed
            .with_env_variable("POSTGRES_SHARED_PRELOAD_LIBRARIES", "")
            .with_env_variable("POSTGRES_MAX_CONNECTIONS", "20")
            .with_env_variable("POSTGRES_SHARED_BUFFERS", "32MB")
            .with_exposed_port(5432)
            .as_service()
        )

        # Create base Python container with minimal dependencies
        base_python = (
            client.container()
            .from_("python:3.10-slim")
            # Install only essential system dependencies
            .with_exec(["apt-get", "update"])
            .with_exec(
                [
                    "apt-get",
                    "install",
                    "-y",
                    "libpq-dev",
                    "gcc",
                    "--no-install-recommends",
                ]
            )
            .with_exec(["apt-get", "clean"])
            .with_exec(["rm", "-rf", "/var/lib/apt/lists/*"])
            # Install minimal Python dependencies
            .with_file(
                "/tmp/requirements_dagger.txt", src.file("requirements_dagger.txt")
            )
            .with_exec(["pip", "install", "--no-cache-dir", "--upgrade", "pip"])
            .with_exec(
                [
                    "pip",
                    "install",
                    "--no-cache-dir",
                    "-r",
                    "/tmp/requirements_dagger.txt",
                ]
            )
        )

        # Fast linting container (runs in parallel)
        async def run_fast_linting():
            linting_container = (
                base_python.with_directory("/app", src)
                .with_workdir("/app")
                .with_exec(["python", "-m", "py_compile", "manage.py"])
                .with_exec(["black", "--check", "."])
                .with_exec(["isort", "--check-only", "."])
                .with_exec(["flake8", "."])
            )

            print("Starting fast linting...")
            await linting_container.sync()
            print("Fast linting completed!")

        # Fast testing container with PostgreSQL (runs in parallel)
        async def run_fast_tests():
            test_container = (
                base_python.with_directory("/app", src)
                .with_workdir("/app")
                .with_service_binding("postgres", postgres)
                .with_env_variable(
                    "DATABASE_URL",
                    "postgresql://postgres:postgres@postgres:5432/test_superheroes",
                )
                .with_env_variable("SECRET_KEY", "test-secret-key-for-ci")
                .with_env_variable("DEBUG", "False")
                .with_env_variable("TEST_DATABASE_PREFIX", "test_")
                .with_exec(
                    [
                        "sh",
                        "-c",
                        """
                    echo "Running fast tests with PostgreSQL..."

                    # Quick PostgreSQL readiness check (optimized)
                    echo "Waiting for PostgreSQL..."
                    for i in $(seq 1 10); do
                        if python -c "
import psycopg2
import sys
try:
    conn = psycopg2.connect(
        host='postgres',
        database='test_superheroes',
        user='postgres',
        password='postgres',
        connect_timeout=3
    )
    conn.close()
    print('PostgreSQL is ready!')
    sys.exit(0)
except Exception as e:
    print(f'Waiting for PostgreSQL ({i}/10)...')
    sys.exit(1)
" 2>/dev/null; then
                            break
                        fi
                        sleep 1
                    done

                    echo "Running migrations (fast mode)..."
                    python manage.py migrate --verbosity=0 --run-syncdb
                    echo "Running unit tests (no coverage)..."
                    python manage.py test --verbosity=2

                    echo "All tests passed!"
                    """,
                    ]
                )
            )

            print("Starting fast tests with PostgreSQL...")
            await test_container.sync()
            print("Fast tests completed!")

        # Run linting and testing in parallel
        print("Starting  parallel execution with PostgreSQL...")

        start_time = asyncio.get_event_loop().time()

        await asyncio.gather(run_fast_linting(), run_fast_tests())

        end_time = asyncio.get_event_loop().time()
        duration = end_time - start_time

        print(f"PostgreSQL pipeline completed in {duration:.2f} seconds!")


if __name__ == "__main__":
    asyncio.run(test())
