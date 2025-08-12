from rest_framework import serializers


class HealthCheckResponseSerializer(serializers.Serializer):
    """Serializer for health check response."""

    status = serializers.CharField(help_text="Status of the health check")
    code = serializers.IntegerField(help_text="HTTP status code")
    message = serializers.CharField(help_text="Health check message")
    version = serializers.CharField(help_text="API version")
