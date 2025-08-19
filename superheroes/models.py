from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Superhero(models.Model):
    """Superhero model representing a superhero."""

    # Basic Information
    name = models.CharField(
        max_length=100, unique=True, help_text="The superhero's name"
    )
    real_name = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="The superhero's real/civilian name",
    )
    alias = models.CharField(
        max_length=100, blank=True, null=True, help_text="Alternative name or alias"
    )

    # Physical Attributes
    age = models.PositiveIntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        help_text="Age in years",
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Height in centimeters",
    )
    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="Weight in kilograms",
    )

    # Powers and Abilities
    powers = models.TextField(
        blank=True, null=True, help_text="List of superpowers and abilities"
    )
    power_level = models.IntegerField(
        default=1,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        help_text="Power level from 1 (weakest) to 10 (strongest)",
    )

    # Background
    origin_story = models.TextField(
        blank=True, null=True, help_text="Superhero's origin story"
    )
    universe = models.CharField(
        max_length=50,
        default="Marvel",
        choices=[
            ("Marvel", "Marvel Universe"),
            ("DC", "DC Universe"),
            ("Custom", "Custom Universe"),
            ("Other", "Other Universe"),
        ],
        help_text="Which universe the superhero belongs to",
    )

    # Status
    is_active = models.BooleanField(
        default=True, help_text="Whether the superhero is currently active"
    )
    is_villain = models.BooleanField(
        default=False, help_text="Whether this character is a villain"
    )

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Superhero"
        verbose_name_plural = "Superheroes"

    def __str__(self):
        return self.name

    @property
    def display_name(self):
        """Return the best display name for the superhero."""
        if self.alias:
            return f"{self.name} ({self.alias})"
        return self.name

    @property
    def power_description(self):
        """Return a description of the superhero's power level."""
        power_descriptions = {
            1: "Beginner",
            2: "Novice",
            3: "Competent",
            4: "Skilled",
            5: "Expert",
            6: "Advanced",
            7: "Elite",
            8: "Master",
            9: "Legendary",
            10: "Godlike",
        }
        return power_descriptions.get(self.power_level, "Unknown")
