#!/usr/bin/env python
"""
Demo script to show the Heroes API endpoints.
"""

REQUESTS_AVAILABLE = False


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"🦸 {title}")
    print("=" * 60)


def show_available_endpoints():
    """Show all available API endpoints."""
    print_section("AVAILABLE ENDPOINTS")

    endpoints = [
        ("GET", "/api/heroes/", "List all heroes"),
        ("POST", "/api/heroes/", "Create a new hero"),
        ("GET", "/api/heroes/{id}/", "Get hero details"),
        ("PUT", "/api/heroes/{id}/", "Update hero (full)"),
        ("PATCH", "/api/heroes/{id}/", "Update hero (partial)"),
        ("DELETE", "/api/heroes/{id}/", "Delete hero"),
        ("GET", "/api/heroes/stats/", "Get hero statistics"),
        ("GET", "/api/heroes/by_universe/", "Get heroes by universe"),
        ("GET", "/api/heroes/top_heroes/", "Get top heroes"),
        ("GET", "/api/heroes/villains/", "Get all villains"),
        ("POST", "/api/heroes/{id}/toggle_villain/", "Toggle villain status"),
        ("POST", "/api/heroes/{id}/toggle_active/", "Toggle active status"),
    ]

    for method, endpoint, description in endpoints:
        print(f"{method:6} {endpoint:35} - {description}")

    print_section("QUERY PARAMETERS")
    filters = [
        ("search", "Search in name, real_name, alias, powers"),
        ("universe", "Filter by universe (Marvel, DC, Custom, Other)"),
        ("is_active", "Filter by active status (true/false)"),
        ("is_villain", "Filter by villain status (true/false)"),
        ("power_level", "Filter by exact power level"),
        ("power_level_min", "Filter by minimum power level"),
        ("power_level_max", "Filter by maximum power level"),
        ("age_min", "Filter by minimum age"),
        ("age_max", "Filter by maximum age"),
        ("ordering", "Order by field (name, power_level, age, created_at)"),
        ("page", "Page number for pagination"),
        ("page_size", "Number of items per page"),
    ]

    for param, description in filters:
        print(f"{param:20} - {description}")


def show_api_documentation(base_url="http://localhost:8000"):
    """Show API documentation URLs."""
    print_section("API DOCUMENTATION")
    print(f"📚 Swagger UI: {base_url}/api/docs/")
    print(f"📚 ReDoc: {base_url}/api/redoc/")
    print(f"📚 OpenAPI Schema: {base_url}/api/schema/")
    print(f"🏥 Health Check: {base_url}/health/")


def show_example_requests():
    """Show example API requests."""
    print_section("EXAMPLE REQUESTS")

    examples = [
        ("List all heroes", "GET /api/heroes/"),
        ("Get Marvel heroes", "GET /api/heroes/?universe=Marvel"),
        ("Search for Spider-Man", "GET /api/heroes/?search=Spider"),
        ("Get heroes with power level 8+", "GET /api/heroes/?power_level_min=8"),
        ("Get top 5 heroes", "GET /api/heroes/top_heroes/?limit=5"),
        ("Get all villains", "GET /api/heroes/villains/"),
        ("Get hero statistics", "GET /api/heroes/stats/"),
    ]

    for title, request in examples:
        print(f"• {title:30} - {request}")

    print_section("EXAMPLE CURL COMMANDS")

    curl_examples = [
        "# List all heroes",
        "curl -X GET http://localhost:8000/api/heroes/",
        "",
        "# Create a new hero",
        "curl -X POST http://localhost:8000/api/heroes/ \\",
        '  -H "Content-Type: application/json" \\',
        '  -d \'{"name": "New Hero", "power_level": 5, "universe": "Custom"}\'',
        "",
        "# Get hero by ID",
        "curl -X GET http://localhost:8000/api/heroes/1/",
        "",
        "# Update hero",
        "curl -X PATCH http://localhost:8000/api/heroes/1/ \\",
        '  -H "Content-Type: application/json" \\',
        "  -d '{\"power_level\": 8}'",
        "",
        "# Get statistics",
        "curl -X GET http://localhost:8000/api/heroes/stats/",
    ]

    for example in curl_examples:
        print(example)


if __name__ == "__main__":
    print("🚀 SUPERHEROES API - HEROES ENDPOINT DEMO")

    show_available_endpoints()
    show_api_documentation()
    show_example_requests()

    print("\n" + "=" * 60)
    print("🔧 GETTING STARTED:")
    print("1. Start the development server:")
    print("   python manage.py runserver")
    print("\n2. Visit the API documentation:")
    print("   http://localhost:8000/api/docs/")
    print("\n3. Test the health endpoint:")
    print("   curl http://localhost:8000/health/")
    print("\n4. List all heroes:")
    print("   curl http://localhost:8000/api/heroes/")
    print("\n🧪 TESTING:")
    print("• Run all tests: python manage.py test")
    print("• Run heroes tests: python manage.py test heroes")
    print("• Run with coverage: coverage run --source='.' manage.py test")
    print("\n📊 SAMPLE DATA:")
    print("• Populate heroes: python manage.py populate_heroes")
    print("• Clear and repopulate: python manage.py populate_heroes --clear")
    print("=" * 60)

    if not REQUESTS_AVAILABLE:
        print("\n💡 TIP: Install 'requests' library to enable live API testing:")
        print("pip install requests")
