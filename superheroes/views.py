from django.db.models import Avg, Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import SuperheroFilter
from .models import Superhero
from .serializers import (
    SuperheroCreateSerializer,
    SuperheroDetailSerializer,
    SuperheroListSerializer,
    SuperheroStatsSerializer,
    SuperheroUpdateSerializer,
)


@extend_schema_view(
    list=extend_schema(
        summary="List all superheroes",
        description="Get a paginated list of all superheroes with basic information",
        tags=["Superheroes"],
    ),
    create=extend_schema(
        summary="Create a new superhero",
        description="Create a new superhero with the provided information",
        tags=["Superheroes"],
    ),
    retrieve=extend_schema(
        summary="Get superhero details",
        description="Get detailed information about a specific superhero",
        tags=["Superheroes"],
    ),
    update=extend_schema(
        summary="Update superhero",
        description="Update all fields of a specific superhero",
        tags=["Superheroes"],
    ),
    partial_update=extend_schema(
        summary="Partially update superhero",
        description="Update specific fields of a superhero",
        tags=["Superheroes"],
    ),
    destroy=extend_schema(
        summary="Delete superhero",
        description="Delete a specific superhero",
        tags=["Superheroes"],
    ),
)
class SuperheroViewSet(ModelViewSet):
    """
    ViewSet for managing superheroes.

    Provides CRUD operations for superheroes with filtering, searching, and ordering.
    """

    queryset = Superhero.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = SuperheroFilter
    search_fields = ["name", "real_name", "alias", "powers"]
    ordering_fields = ["name", "power_level", "age", "created_at", "updated_at"]
    ordering = ["name"]

    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == "list":
            return SuperheroListSerializer
        elif self.action == "create":
            return SuperheroCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return SuperheroUpdateSerializer
        return SuperheroDetailSerializer

    @extend_schema(
        summary="Get superheroes by universe",
        description="Get all superheroes from a specific universe",
        tags=["Superheroes"],
    )
    @action(detail=False, methods=["get"])
    def by_universe(self, request):
        """Get superheroes filtered by universe."""
        universe = request.query_params.get("universe")
        if not universe:
            return Response(
                {"error": "Universe parameter is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        superheroes = self.queryset.filter(universe__iexact=universe)
        serializer = SuperheroListSerializer(superheroes, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get top superheroes by power level",
        description="Get superheroes with the highest power levels",
        tags=["Superheroes"],
    )
    @action(detail=False, methods=["get"])
    def top_superheroes(self, request):
        """Get top superheroes by power level."""
        try:
            limit = int(request.query_params.get("limit", 10))
            if limit < 0:
                raise ValueError("Invalid value for 'limit'. Must be a positive integer")
        except ValueError:
            return Response(
                {"error": "Invalid value for 'limit'. Must be an integer."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        superheroes = self.queryset.filter(is_villain=False).order_by(
            "-power_level", "name"
        )[:limit]
        serializer = SuperheroListSerializer(superheroes, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Get villains",
        description="Get all villains (characters marked as villains)",
        tags=["Superheroes"],
    )
    @action(detail=False, methods=["get"])
    def villains(self, request):
        """Get all villains."""
        villains = self.queryset.filter(is_villain=True)
        serializer = SuperheroListSerializer(villains, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Toggle superhero/villain status",
        description="Toggle whether a character is a superhero or villain",
        tags=["Superheroes"],
    )
    @action(detail=True, methods=["post"])
    def toggle_villain(self, request, pk=None):
        """Toggle villain status of a superhero."""
        superhero = self.get_object()
        superhero.is_villain = not superhero.is_villain
        superhero.save()

        serializer = SuperheroDetailSerializer(superhero)
        villain_status = "villain" if superhero.is_villain else "superhero"
        return Response(
            {
                "message": f"{superhero.name} is now a {villain_status}",
                "superhero": serializer.data,
            }
        )

    @extend_schema(
        summary="Toggle active status",
        description="Toggle whether a superhero is active or inactive",
        tags=["Superheroes"],
    )
    @action(detail=True, methods=["post"])
    def toggle_active(self, request, pk=None):
        """Toggle active status of a superhero."""
        superhero = self.get_object()
        superhero.is_active = not superhero.is_active
        superhero.save()

        serializer = SuperheroDetailSerializer(superhero)
        active_status = "active" if superhero.is_active else "inactive"
        return Response(
            {
                "message": f"{superhero.name} is now {active_status}",
                "superhero": serializer.data,
            }
        )


class SuperheroStatsView(APIView):
    """
    View for getting superhero statistics.
    """

    @extend_schema(
        summary="Get superhero statistics",
        description="Get comprehensive statistics about all superheroes",
        responses={200: SuperheroStatsSerializer},
        tags=["Superheroes"],
    )
    def get(self, request):
        """Get superhero statistics."""
        total_superheroes = Superhero.objects.count()
        active_superheroes = Superhero.objects.filter(is_active=True).count()
        inactive_superheroes = Superhero.objects.filter(is_active=False).count()
        villains = Superhero.objects.filter(is_villain=True).count()
        superheroes = Superhero.objects.filter(is_villain=False).count()

        # Average power level
        avg_power = (
            Superhero.objects.aggregate(avg_power=Avg("power_level"))["avg_power"] or 0
        )

        # Universe distribution
        universe_stats = (
            Superhero.objects.values("universe")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        universe_distribution = {
            stat["universe"]: stat["count"] for stat in universe_stats
        }

        # Power level distribution
        power_stats = (
            Superhero.objects.values("power_level")
            .annotate(count=Count("id"))
            .order_by("power_level")
        )
        power_level_distribution = {
            str(stat["power_level"]): stat["count"] for stat in power_stats
        }

        stats_data = {
            "total_superheroes": total_superheroes,
            "active_superheroes": active_superheroes,
            "inactive_superheroes": inactive_superheroes,
            "villains": villains,
            "superheroes": superheroes,
            "average_power_level": round(avg_power, 2),
            "universe_distribution": universe_distribution,
            "power_level_distribution": power_level_distribution,
        }

        serializer = SuperheroStatsSerializer(stats_data)
        return Response(serializer.data)
