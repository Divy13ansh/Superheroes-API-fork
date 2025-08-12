from django.contrib import admin
from .models import Superhero


@admin.register(Superhero)
class SuperheroAdmin(admin.ModelAdmin):
    """Admin interface for Superhero model."""
    
    list_display = [
        'name',
        'real_name',
        'universe',
        'power_level',
        'power_description',
        'is_active',
        'is_villain',
        'created_at',
    ]
    
    list_filter = [
        'universe',
        'is_active',
        'is_villain',
        'power_level',
        'created_at',
    ]
    
    search_fields = [
        'name',
        'real_name',
        'alias',
        'powers',
        'origin_story',
    ]
    
    readonly_fields = [
        'display_name',
        'power_description',
        'created_at',
        'updated_at',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'real_name', 'alias', 'display_name')
        }),
        ('Physical Attributes', {
            'fields': ('age', 'height', 'weight'),
            'classes': ('collapse',)
        }),
        ('Powers & Abilities', {
            'fields': ('powers', 'power_level', 'power_description')
        }),
        ('Background', {
            'fields': ('origin_story', 'universe'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_villain')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['name']
    
    actions = ['make_active', 'make_inactive', 'make_superhero', 'make_villain']
    
    def make_active(self, request, queryset):
        """Mark selected superheroes as active."""
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} superheroes marked as active.')
    make_active.short_description = "Mark selected superheroes as active"
    
    def make_inactive(self, request, queryset):
        """Mark selected superheroes as inactive."""
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} superheroes marked as inactive.')
    make_inactive.short_description = "Mark selected superheroes as inactive"
    
    def make_superhero(self, request, queryset):
        """Mark selected characters as superheroes."""
        updated = queryset.update(is_villain=False)
        self.message_user(request, f'{updated} characters marked as superheroes.')
    make_superhero.short_description = "Mark selected characters as superheroes"
    
    def make_villain(self, request, queryset):
        """Mark selected characters as villains."""
        updated = queryset.update(is_villain=True)
        self.message_user(request, f'{updated} characters marked as villains.')
    make_villain.short_description = "Mark selected characters as villains"
