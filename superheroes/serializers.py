from rest_framework import serializers
from .models import Superhero


class SuperheroListSerializer(serializers.ModelSerializer):
    """Serializer for superhero list view with essential fields."""
    
    display_name = serializers.ReadOnlyField()
    power_description = serializers.ReadOnlyField()
    
    class Meta:
        model = Superhero
        fields = [
            'id',
            'name',
            'display_name',
            'universe',
            'power_level',
            'power_description',
            'is_active',
            'is_villain',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at']


class SuperheroDetailSerializer(serializers.ModelSerializer):
    """Serializer for superhero detail view with all fields."""
    
    display_name = serializers.ReadOnlyField()
    power_description = serializers.ReadOnlyField()
    
    class Meta:
        model = Superhero
        fields = [
            'id',
            'name',
            'real_name',
            'alias',
            'display_name',
            'age',
            'height',
            'weight',
            'powers',
            'power_level',
            'power_description',
            'origin_story',
            'universe',
            'is_active',
            'is_villain',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate_power_level(self, value):
        """Validate power level is within acceptable range."""
        if value < 1 or value > 10:
            raise serializers.ValidationError(
                "Power level must be between 1 and 10."
            )
        return value
    
    def validate_age(self, value):
        """Validate age is reasonable."""
        if value is not None and (value < 1 or value > 10000):
            raise serializers.ValidationError(
                "Age must be between 1 and 10000 years."
            )
        return value


class SuperheroCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new superheroes."""
    
    class Meta:
        model = Superhero
        fields = [
            'name',
            'real_name',
            'alias',
            'age',
            'height',
            'weight',
            'powers',
            'power_level',
            'origin_story',
            'universe',
            'is_active',
            'is_villain',
        ]
    
    def validate_name(self, value):
        """Validate superhero name is unique."""
        if Superhero.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(
                "A superhero with this name already exists."
            )
        return value


class SuperheroUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating existing superheroes."""
    
    class Meta:
        model = Superhero
        fields = [
            'name',
            'real_name',
            'alias',
            'age',
            'height',
            'weight',
            'powers',
            'power_level',
            'origin_story',
            'universe',
            'is_active',
            'is_villain',
        ]
    
    def validate_name(self, value):
        """Validate superhero name is unique (excluding current instance)."""
        instance = getattr(self, 'instance', None)
        if instance and Superhero.objects.filter(name__iexact=value).exclude(pk=instance.pk).exists():
            raise serializers.ValidationError(
                "A superhero with this name already exists."
            )
        elif not instance and Superhero.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError(
                "A superhero with this name already exists."
            )
        return value


class SuperheroStatsSerializer(serializers.Serializer):
    """Serializer for superhero statistics."""
    
    total_superheroes = serializers.IntegerField()
    active_superheroes = serializers.IntegerField()
    inactive_superheroes = serializers.IntegerField()
    villains = serializers.IntegerField()
    superheroes = serializers.IntegerField()
    average_power_level = serializers.FloatField()
    universe_distribution = serializers.DictField()
    power_level_distribution = serializers.DictField()
