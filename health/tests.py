from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class HealthCheckTest(APITestCase):
    """Test cases for health check endpoint."""

    def setUp(self):
        """Set up test client."""
        self.client = APIClient()
        self.health_url = reverse("health_check")

    def test_health_check_get_success(self):
        """Test successful GET request to health check endpoint."""
        response = self.client.get(self.health_url)

        # Assert that the response has a status code of 200 (OK)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the content of the response
        expected_response = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Superheroes API launched successfully",
            "version": "0.1.0",
        }
        self.assertEqual(response.data, expected_response)

    def test_health_check_response_structure(self):
        """Test that health check response has correct structure."""
        response = self.client.get(self.health_url)

        # Check that all required fields are present
        required_fields = ["status", "code", "message", "version"]
        for field in required_fields:
            self.assertIn(field, response.data)

    def test_health_check_response_types(self):
        """Test that health check response fields have correct types."""
        response = self.client.get(self.health_url)

        # Check field types
        self.assertIsInstance(response.data["status"], str)
        self.assertIsInstance(response.data["code"], int)
        self.assertIsInstance(response.data["message"], str)
        self.assertIsInstance(response.data["version"], str)

    def test_health_check_status_values(self):
        """Test that health check returns expected status values."""
        response = self.client.get(self.health_url)

        # Check specific values
        self.assertEqual(response.data["status"], "success")
        self.assertEqual(response.data["code"], 200)
        self.assertEqual(response.data["version"], "0.1.0")

    def test_health_check_content_type(self):
        """Test that health check returns JSON content type."""
        response = self.client.get(self.health_url)

        self.assertEqual(response["Content-Type"], "application/json")

    def test_health_check_method_not_allowed(self):
        """Test that non-GET methods return 405 Method Not Allowed."""
        # Test POST method
        response = self.client.post(self.health_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test PUT method
        response = self.client.put(self.health_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        # Test DELETE method
        response = self.client.delete(self.health_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_health_check_url_resolution(self):
        """Test that health check URL resolves correctly."""
        from django.urls import resolve

        resolver = resolve("/health/")
        self.assertEqual(resolver.view_name, "health_check")


class HealthCheckIntegrationTest(TestCase):
    """Integration tests for health check endpoint."""

    def test_health_check_endpoint_accessibility(self):
        """Test that health check endpoint is accessible via direct URL."""
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_health_check_with_trailing_slash(self):
        """Test health check endpoint with and without trailing slash."""
        # With trailing slash
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Without trailing slash (should redirect or work)
        response = self.client.get("/health")
        self.assertIn(
            response.status_code,
            [status.HTTP_200_OK, status.HTTP_301_MOVED_PERMANENTLY],
        )
