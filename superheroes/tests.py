from decimal import Decimal

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Superhero
from .serializers import SuperheroDetailSerializer


class SuperheroModelTest(TestCase):
    """Test cases for Superhero model."""

    def setUp(self):
        """Set up test data."""
        self.superhero_data = {
            "name": "Spider-Man",
            "real_name": "Peter Parker",
            "alias": "Spidey",
            "age": 25,
            "height": Decimal("175.50"),
            "weight": Decimal("70.00"),
            "powers": "Web-slinging, wall-crawling, spider-sense",
            "power_level": 7,
            "origin_story": "Bitten by a radioactive spider",
            "universe": "Marvel",
            "is_active": True,
            "is_villain": False,
        }

    def test_superhero_creation(self):
        """Test creating a superhero."""
        superhero = Superhero.objects.create(**self.superhero_data)
        self.assertEqual(superhero.name, "Spider-Man")
        self.assertEqual(superhero.real_name, "Peter Parker")
        self.assertEqual(superhero.power_level, 7)
        self.assertTrue(superhero.is_active)
        self.assertFalse(superhero.is_villain)

    def test_superhero_str_method(self):
        """Test superhero string representation."""
        superhero = Superhero.objects.create(**self.superhero_data)
        self.assertEqual(str(superhero), "Spider-Man")

    def test_display_name_property(self):
        """Test display_name property."""
        superhero = Superhero.objects.create(**self.superhero_data)
        self.assertEqual(superhero.display_name, "Spider-Man (Spidey)")

        # Test without alias
        superhero.alias = None
        superhero.save()
        self.assertEqual(superhero.display_name, "Spider-Man")

    def test_power_description_property(self):
        """Test power_description property."""
        superhero = Superhero.objects.create(**self.superhero_data)
        self.assertEqual(superhero.power_description, "Elite")

        # Test different power levels
        superhero.power_level = 1
        self.assertEqual(superhero.power_description, "Beginner")

        superhero.power_level = 10
        self.assertEqual(superhero.power_description, "Godlike")

    def test_superhero_ordering(self):
        """Test superhero ordering by name."""
        Superhero.objects.create(name="Wolverine", power_level=8)
        Superhero.objects.create(name="Batman", power_level=6)
        Superhero.objects.create(name="Superman", power_level=10)

        superheroes = list(Superhero.objects.all())
        self.assertEqual(superheroes[0].name, "Batman")
        self.assertEqual(superheroes[1].name, "Superman")
        self.assertEqual(superheroes[2].name, "Wolverine")


class SuperheroAPITest(APITestCase):
    """Test cases for Superhero API endpoints."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()

        # Create test superheroes
        self.superhero1 = Superhero.objects.create(
            name="Spider-Man",
            real_name="Peter Parker",
            power_level=7,
            universe="Marvel",
            is_active=True,
            is_villain=False,
        )

        self.superhero2 = Superhero.objects.create(
            name="Batman",
            real_name="Bruce Wayne",
            power_level=6,
            universe="DC",
            is_active=True,
            is_villain=False,
        )

        self.villain = Superhero.objects.create(
            name="Joker",
            real_name="Unknown",
            power_level=5,
            universe="DC",
            is_active=True,
            is_villain=True,
        )

    def test_get_superheroes_list(self):
        """Test getting list of superheroes."""
        url = reverse("superhero-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 3)

    def test_get_superhero_detail(self):
        """Test getting superhero details."""
        url = reverse("superhero-detail", kwargs={"pk": self.superhero1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Spider-Man")
        self.assertEqual(response.data["real_name"], "Peter Parker")

    def test_create_superhero(self):
        """Test creating a new superhero."""
        url = reverse("superhero-list")
        data = {
            "name": "Wonder Woman",
            "real_name": "Diana Prince",
            "power_level": 9,
            "universe": "DC",
            "is_active": True,
            "is_villain": False,
        }

        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Superhero.objects.count(), 4)
        self.assertEqual(
            Superhero.objects.get(name="Wonder Woman").real_name, "Diana Prince"
        )

    def test_update_superhero(self):
        """Test updating a superhero."""
        url = reverse("superhero-detail", kwargs={"pk": self.superhero1.pk})
        data = {
            "name": "Spider-Man",
            "real_name": "Peter Benjamin Parker",
            "power_level": 8,
            "universe": "Marvel",
        }

        response = self.client.patch(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.superhero1.refresh_from_db()
        self.assertEqual(self.superhero1.real_name, "Peter Benjamin Parker")
        self.assertEqual(self.superhero1.power_level, 8)

    def test_delete_superhero(self):
        """Test deleting a superhero."""
        url = reverse("superhero-detail", kwargs={"pk": self.superhero1.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Superhero.objects.count(), 2)

    def test_filter_by_universe(self):
        """Test filtering superheroes by universe."""
        url = reverse("superhero-list")
        response = self.client.get(url, {"universe": "Marvel"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Spider-Man")

    def test_filter_by_villain_status(self):
        """Test filtering by villain status."""
        url = reverse("superhero-list")
        response = self.client.get(url, {"is_villain": "true"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Joker")

    def test_search_superheroes(self):
        """Test searching superheroes."""
        url = reverse("superhero-list")
        response = self.client.get(url, {"search": "Spider"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Spider-Man")

    def test_order_superheroes(self):
        """Test ordering superheroes."""
        url = reverse("superhero-list")
        response = self.client.get(url, {"ordering": "-power_level"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data["results"]
        self.assertEqual(results[0]["name"], "Spider-Man")  # power_level 7
        self.assertEqual(results[1]["name"], "Batman")  # power_level 6
        self.assertEqual(results[2]["name"], "Joker")  # power_level 5

    def test_get_superheroes_by_universe_action(self):
        """Test custom action to get superheroes by universe."""
        url = reverse("superhero-by-universe")
        response = self.client.get(url, {"universe": "DC"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Batman and Joker

    def test_get_top_superheroes_action(self):
        """Test custom action to get top superheroes."""
        url = reverse("superhero-top-superheroes")
        response = self.client.get(url, {"limit": 2})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # Should exclude villains
        names = [superhero["name"] for superhero in response.data]
        self.assertIn("Spider-Man", names)
        self.assertIn("Batman", names)
        self.assertNotIn("Joker", names)

    def test_get_villains_action(self):
        """Test custom action to get villains."""
        url = reverse("superhero-villains")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Joker")

    def test_toggle_villain_action(self):
        """Test toggling villain status."""
        url = reverse("superhero-toggle-villain", kwargs={"pk": self.superhero1.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.superhero1.refresh_from_db()
        self.assertTrue(self.superhero1.is_villain)
        self.assertIn("villain", response.data["message"])

    def test_toggle_active_action(self):
        """Test toggling active status."""
        url = reverse("superhero-toggle-active", kwargs={"pk": self.superhero1.pk})
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.superhero1.refresh_from_db()
        self.assertFalse(self.superhero1.is_active)
        self.assertIn("inactive", response.data["message"])

    def test_superhero_stats(self):
        """Test superhero statistics endpoint."""
        url = reverse("superhero-stats")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.data
        self.assertEqual(data["total_superheroes"], 3)
        self.assertEqual(data["active_superheroes"], 3)
        self.assertEqual(data["inactive_superheroes"], 0)
        self.assertEqual(data["villains"], 1)
        self.assertEqual(data["superheroes"], 2)
        self.assertIn("average_power_level", data)
        self.assertIn("universe_distribution", data)
        self.assertIn("power_level_distribution", data)

    def test_create_superhero_validation(self):
        """Test superhero creation validation."""
        url = reverse("superhero-list")

        # Test duplicate name
        data = {"name": "Spider-Man", "power_level": 5}  # Already exists
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test invalid power level
        data = {"name": "New Superhero", "power_level": 15}  # Invalid (max is 10)
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SuperheroSerializerTest(TestCase):
    """Test cases for SuperheroDetailSerializer validations."""

    def setUp(self):
        self.valid_data = {
            "name": "Thor",
            "real_name": "Thor Odinson",
            "alias": "God of Thunder",
            "age": 1500,
            "height": 195,
            "weight": 110,
            "powers": "Lightning, flight",
            "power_level": 7,
            "origin_story": "Prince of Asgard",
            "universe": "Marvel",
            "is_active": True,
            "is_villain": False,
        }

    def test_valid_power_level(self):
        """Ensure serializer passes for valid power_level between 1 and 10."""
        serializer = SuperheroDetailSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_power_level_below_minimum(self):
        """Ensure serializer raises error when power_level < 1."""
        data = self.valid_data.copy()
        data["power_level"] = 0
        serializer = SuperheroDetailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("power_level", serializer.errors)
        self.assertEqual(
            serializer.errors["power_level"][0],
            "Power level must be between 1 and 10.",
        )

    def test_power_level_above_maximum(self):
        """Ensure serializer raises error when power_level > 10."""
        data = self.valid_data.copy()
        data["power_level"] = 15
        serializer = SuperheroDetailSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("power_level", serializer.errors)
        self.assertEqual(
            serializer.errors["power_level"][0],
            "Power level must be between 1 and 10.",
        )
