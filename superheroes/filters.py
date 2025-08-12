import django_filters
from .models import Superhero


class SuperheroFilter(django_filters.FilterSet):
    """Filter set for Superhero model."""
    
    # Text filters
    name = django_filters.CharFilter(lookup_expr='icontains')
    real_name = django_filters.CharFilter(lookup_expr='icontains')
    alias = django_filters.CharFilter(lookup_expr='icontains')
    powers = django_filters.CharFilter(lookup_expr='icontains')
    origin_story = django_filters.CharFilter(lookup_expr='icontains')
    
    # Range filters
    age_min = django_filters.NumberFilter(field_name='age', lookup_expr='gte')
    age_max = django_filters.NumberFilter(field_name='age', lookup_expr='lte')
    height_min = django_filters.NumberFilter(field_name='height', lookup_expr='gte')
    height_max = django_filters.NumberFilter(field_name='height', lookup_expr='lte')
    weight_min = django_filters.NumberFilter(field_name='weight', lookup_expr='gte')
    weight_max = django_filters.NumberFilter(field_name='weight', lookup_expr='lte')
    power_level_min = django_filters.NumberFilter(field_name='power_level', lookup_expr='gte')
    power_level_max = django_filters.NumberFilter(field_name='power_level', lookup_expr='lte')
    
    # Date filters
    created_after = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    updated_after = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='gte')
    updated_before = django_filters.DateTimeFilter(field_name='updated_at', lookup_expr='lte')
    
    class Meta:
        model = Superhero
        fields = {
            'universe': ['exact', 'in'],
            'is_active': ['exact'],
            'is_villain': ['exact'],
            'power_level': ['exact', 'lt', 'gt', 'lte', 'gte'],
        }
