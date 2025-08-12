from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SuperheroViewSet, SuperheroStatsView

# Create router and register viewsets
router = DefaultRouter()
router.register(r'superheroes', SuperheroViewSet, basename='superhero')

urlpatterns = [
    # Statistics endpoint (must come before router URLs)
    path('api/superheroes/stats/', SuperheroStatsView.as_view(), name='superhero-stats'),
    
    # API routes
    path('api/', include(router.urls)),
]
