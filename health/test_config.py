"""
Test configuration and utilities for health app tests.
"""

# Test data constants
HEALTH_CHECK_EXPECTED_RESPONSE = {
    "status": "success",
    "code": 200,
    "message": "Superheroes API launched successfully",
    "version": "0.1.0",
}

# Test URLs
HEALTH_CHECK_URL = "/health/"

# HTTP methods for testing
ALLOWED_METHODS = ["GET"]
DISALLOWED_METHODS = ["POST", "PUT", "DELETE", "PATCH"]
