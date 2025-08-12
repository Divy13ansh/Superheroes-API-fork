#!/usr/bin/env python
"""
Demo script to show the Superheroes API endpoints.
"""

try:
    import requests
    import json
    from urllib.parse import urljoin
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def print_section(title):
    """Print a section header."""
    print(f"\n{'='*60}")
    print(f"🦸 {title}")
    print('='*60)


def show_available_endpoints():
    """Show all available API endpoints."""
    print_section("AVAILABLE ENDPOINTS")
    
    endpoints = [
        ("GET", "/api/superheroes/", "List all superheroes"),
        ("POST", "/api/superheroes/", "Create a new superhero"),
        ("GET", "/api/superheroes/{id}/", "Get superhero details"),
        ("PUT", "/api/superheroes/{id}/", "Update superhero (full)"),
        ("PATCH", "/api/superheroes/{id}/", "Update superhero (partial)"),
        ("DELETE", "/api/superheroes/{id}/", "Delete superhero"),
        ("GET", "/api/superheroes/stats/", "Get superhero statistics"),
        ("GET", "/api/superheroes/by_universe/", "Get superheroes by universe"),
        ("GET", "/api/superheroes/top_superheroes/", "Get top superheroes"),
        ("GET", "/api/superheroes/villains/", "Get all villains"),
        ("POST", "/api/superheroes/{id}/toggle_villain/", "Toggle villain status"),
        ("POST", "/api/superheroes/{id}/toggle_active/", "Toggle active status"),
    ]
    
    for method, endpoint, description in endpoints:
        print(f"{method:6} {endpoint:40} - {description}")
    
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
        ("List all superheroes", "GET /api/superheroes/"),
        ("Get Marvel superheroes", "GET /api/superheroes/?universe=Marvel"),
        ("Search for Spider-Man", "GET /api/superheroes/?search=Spider"),
        ("Get superheroes with power level 8+", "GET /api/superheroes/?power_level_min=8"),
        ("Get top 5 superheroes", "GET /api/superheroes/top_superheroes/?limit=5"),
        ("Get all villains", "GET /api/superheroes/villains/"),
        ("Get superhero statistics", "GET /api/superheroes/stats/"),
    ]
    
    for title, request in examples:
        print(f"• {title:35} - {request}")
    
    print_section("EXAMPLE CURL COMMANDS")
    
    curl_examples = [
        "# List all superheroes",
        "curl -X GET http://localhost:8000/api/superheroes/",
        "",
        "# Create a new superhero",
        'curl -X POST http://localhost:8000/api/superheroes/ \\',
        '  -H "Content-Type: application/json" \\',
        '  -d \'{"name": "New Superhero", "power_level": 5, "universe": "Custom"}\'',
        "",
        "# Get superhero by ID",
        "curl -X GET http://localhost:8000/api/superheroes/1/",
        "",
        "# Update superhero",
        'curl -X PATCH http://localhost:8000/api/superheroes/1/ \\',
        '  -H "Content-Type: application/json" \\',
        '  -d \'{"power_level": 8}\'',
        "",
        "# Get statistics",
        "curl -X GET http://localhost:8000/api/superheroes/stats/",
    ]
    
    for example in curl_examples:
        print(example)


if __name__ == "__main__":
    print("🚀 SUPERHEROES API - SUPERHEROES ENDPOINT DEMO")
    
    show_available_endpoints()
    show_api_documentation()
    show_example_requests()
    
    print("\n" + "="*60)
    print("🔧 GETTING STARTED:")
    print("1. Start the development server:")
    print("   python manage.py runserver")
    print("\n2. Visit the API documentation:")
    print("   http://localhost:8000/api/docs/")
    print("\n3. Test the health endpoint:")
    print("   curl http://localhost:8000/health/")
    print("\n4. List all superheroes:")
    print("   curl http://localhost:8000/api/superheroes/")
    print("\n🧪 TESTING:")
    print("• Run all tests: python manage.py test")
    print("• Run superheroes tests: python manage.py test superheroes")
    print("• Run with coverage: coverage run --source='.' manage.py test")
    print("\n📊 SAMPLE DATA:")
    print("• Populate superheroes: python manage.py populate_superheroes")
    print("• Clear and repopulate: python manage.py populate_superheroes --clear")
    print("="*60)
    
    if not REQUESTS_AVAILABLE:
        print("\n💡 TIP: Install 'requests' library to enable live API testing:")
        print("pip install requests")
