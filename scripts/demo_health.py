#!/usr/bin/env python
"""
Demo script to test the health endpoint and show Swagger documentation URLs.
"""

import json
from urllib.parse import urljoin

import requests


def test_health_endpoint(base_url="http://localhost:8000"):
    """Test the health endpoint."""
    health_url = urljoin(base_url, "/health/")

    try:
        print(f"Testing health endpoint: {health_url}")
        response = requests.get(health_url, timeout=5)

        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Body: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200:
            print("✅ Health check passed!")
        else:
            print("❌ Health check failed!")

    except requests.exceptions.RequestException as e:
        print(f"❌ Error connecting to health endpoint: {e}")
        print("Make sure the Django development server is running:")
        print("python manage.py runserver")


def show_swagger_urls(base_url="http://localhost:8000"):
    """Show Swagger documentation URLs."""
    print("\n📚 API Documentation URLs:")
    print(f"• Swagger UI: {urljoin(base_url, '/api/docs/')}")
    print(f"• ReDoc: {urljoin(base_url, '/api/redoc/')}")
    print(f"• OpenAPI Schema: {urljoin(base_url, '/api/schema/')}")


if __name__ == "__main__":
    print("🚀 Superheroes API Health Check Demo")
    print("=" * 40)

    test_health_endpoint()
    show_swagger_urls()

    print("\n📝 To start the development server:")
    print("python manage.py runserver")

    print("\n🧪 To run tests:")
    print("python manage.py test health")
