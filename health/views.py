from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import HealthCheckResponseSerializer


class HealthCheck(APIView):
    """Health Check View for monitoring API status."""

    @extend_schema(
        operation_id="health_check",
        summary="Health Check",
        description="Check the health status of the API service",
        responses={
            200: HealthCheckResponseSerializer,
        },
        tags=["Health"],
    )
    def get(self, request, *args, **kwargs):
        """
        Get health status of the API.

        Returns basic information about the API status including:
        - Service status
        - HTTP status code
        - Success message
        - API version
        """
        response = {
            "status": "success",
            "code": status.HTTP_200_OK,
            "message": "Superheroes API launched successfully",
            "version": "0.1.0",
        }
        return Response(response, status.HTTP_200_OK)
