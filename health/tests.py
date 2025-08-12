from rest_framework import status
from rest_framework.test import APITestCase


class HealthCheckTest(APITestCase):
    def test_health_check(self):
        # Send a GET request to the health check endpoint
        response = self.client.get("/health", follow=True)

        # Assert that the response has a status code of 200 (OK)
        print(response.status_code)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Assert the content of the response
        expected_response = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Backend lunched successfully",
            "version": "0.1.0",
        }
        self.assertEqual(response.data, expected_response)
