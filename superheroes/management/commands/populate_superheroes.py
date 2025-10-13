from decimal import Decimal

from django.core.management.base import BaseCommand

from superheroes.models import Superhero


class Command(BaseCommand):
    help = "Populate the database with sample superheroes data"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing superheroes before adding new ones",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            Superhero.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared all existing superheroes."))

        sample_superheroes = [
            {
                "name": "Spider-Man",
                "real_name": "Peter Parker",
                "alias": "Spidey",
                "age": 25,
                "height": Decimal("175.50"),
                "weight": Decimal("70.00"),
                "powers": (
                    "Web-slinging, wall-crawling, spider-sense, "
                    "superhuman strength and agility"
                ),
                "power_level": 7,
                "origin_story": (
                    "Bitten by a radioactive spider while on a school field trip"
                ),
                "universe": "Marvel",
                "is_active": True,
                "is_villain": False,
            },
            {
                "name": "Batman",
                "real_name": "Bruce Wayne",
                "alias": "The Dark Knight",
                "age": 35,
                "height": Decimal("188.00"),
                "weight": Decimal("95.00"),
                "powers": (
                    "Martial arts mastery, detective skills, advanced technology, "
                    "peak human conditioning"
                ),
                "power_level": 6,
                "origin_story": (
                    "Witnessed his parents murder as a child, "
                    "dedicated his life to fighting crime"
                ),
                "universe": "DC",
                "is_active": True,
                "is_villain": False,
            },
            {
                "name": "Superman",
                "real_name": "Clark Kent",
                "alias": "Man of Steel",
                "age": 30,
                "height": Decimal("191.00"),
                "weight": Decimal("107.00"),
                "powers": (
                    "Flight, super strength, invulnerability, heat vision, "
                    "x-ray vision, super speed"
                ),
                "power_level": 10,
                "origin_story": (
                    "Last son of Krypton, sent to Earth as a baby "
                    "before his planet was destroyed"
                ),
                "universe": "DC",
                "is_active": True,
                "is_villain": False,
            },
            {
                "name": "Wonder Woman",
                "real_name": "Diana Prince",
                "alias": "Amazon Princess",
                "age": 3000,
                "height": Decimal("183.00"),
                "weight": Decimal("74.00"),
                "powers": (
                    "Super strength, flight, lasso of truth, "
                    "bulletproof bracelets, combat skills"
                ),
                "power_level": 9,
                "origin_story": "Amazonian princess from Themyscira, daughter of Zeus",
                "universe": "DC",
                "is_active": True,
                "is_villain": False,
            },
            {
                "name": "Iron Man",
                "real_name": "Tony Stark",
                "alias": "Armored Avenger",
                "age": 45,
                "height": Decimal("185.00"),
                "weight": Decimal("102.00"),
                "powers": (
                    "Genius intellect, powered armor suit, repulsors, "
                    "flight, advanced AI"
                ),
                "power_level": 8,
                "origin_story": (
                    "Billionaire inventor who built a suit of armor to escape captivity"
                ),
                "universe": "Marvel",
                "is_active": True,
                "is_villain": False,
            },
            {
                "name": "The Joker",
                "real_name": "Unknown",
                "alias": "Clown Prince of Crime",
                "age": 40,
                "height": Decimal("185.00"),
                "weight": Decimal("86.00"),
                "powers": (
                    "Genius-level intellect, unpredictability, toxins, "
                    "psychological warfare"
                ),
                "power_level": 5,
                "origin_story": (
                    "Fell into a vat of chemicals, driving him insane "
                    "and bleaching his skin"
                ),
                "universe": "DC",
                "is_active": True,
                "is_villain": True,
            },
            {
                "name": "Green Goblin",
                "real_name": "Norman Osborn",
                "alias": "Goblin",
                "age": 50,
                "height": Decimal("180.00"),
                "weight": Decimal("84.00"),
                "powers": (
                    "Enhanced strength, glider flight, pumpkin bombs, genius intellect"
                ),
                "power_level": 6,
                "origin_story": (
                    "Chemical formula gave him enhanced abilities but drove him insane"
                ),
                "universe": "Marvel",
                "is_active": True,
                "is_villain": True,
            },
            {
                "name": "Captain America",
                "real_name": "Steve Rogers",
                "alias": "First Avenger",
                "age": 100,
                "height": Decimal("188.00"),
                "weight": Decimal("109.00"),
                "powers": (
                    "Enhanced strength, speed, agility, endurance, "
                    "vibranium shield, tactical genius"
                ),
                "power_level": 7,
                "origin_story": "Weak soldier enhanced by super-soldier serum during WWII",
                "universe": "Marvel",
                "is_active": True,
                "is_villain": False,
            },
            {
                "name": "The Flash",
                "real_name": "Barry Allen",
                "alias": "Fastest Man Alive",
                "age": 28,
                "height": Decimal("183.00"),
                "weight": Decimal("81.00"),
                "powers": "Super speed, time travel, phasing, speed force manipulation",
                "power_level": 9,
                "origin_story": (
                    "Struck by lightning while working in his lab, "
                    "gained connection to Speed Force"
                ),
                "universe": "DC",
                "is_active": True,
                "is_villain": False,
            },
            {
                "name": "Wolverine",
                "real_name": "James Howlett",
                "alias": "Logan",
                "age": 200,
                "height": Decimal("160.00"),
                "weight": Decimal("136.00"),
                "powers": "Healing factor, adamantium claws, enhanced senses, longevity",
                "power_level": 8,
                "origin_story": (
                    "Born with mutant abilities, subjected to Weapon X program"
                ),
                "universe": "Marvel",
                "is_active": True,
                "is_villain": False,
            },
            {
                "name": "Black Widow",
                "real_name": "Natasha Romanoff",
                "alias": "Natasha",
                "age": 35,
                "height": Decimal("170.00"),
                "weight": Decimal("59.00"),
                "powers": "Expert martial artist, master spy, skilled marksman, peak human agility and reflexes",
                "power_level": 7,
                "origin_story": (
                    "Trained in the Red Room program as a Russian spy and assassin, later defected to S.H.I.E.L.D. and became an Avenger"
                ),
                "universe": "Marvel",
                "is_active": True,
                "is_villain": False,
            },
            {
                "name": "Aquaman",
                "real_name": "Arthur Curry",
                "alias": "King of Atlantis",
                "age": 36,
                "height": Decimal("185.00"),
                "weight": Decimal("101.00"),
                "powers": "Superhuman strength, underwater breathing, telepathic communication with marine life, enhanced swimming speed, expert combat skills",
                "power_level": 8,
                "origin_story": (
                    "Born to a human father and Atlantean mother, Arthur discovered his heritage and destiny to unite the surface world and Atlantis as its rightful king."
                ),
                "universe": "DC",
                "is_active": True,
                "is_villain": False,
            },
            
                "name": "Hulk",
                "real_name": "Bruce Banner",
                "alias": "The Incredible Hulk",
                "age": 40,
                "height": Decimal("244.00"),
                "weight": Decimal("635.00"),
                "powers": "Superhuman strength, regeneration, endurance, resistance to injury, transformation triggered by anger",
                "power_level": 10,
                "origin_story": (
                    "After exposure to gamma radiation during an experiment gone wrong, scientist Bruce Banner transforms into the Hulk whenever he experiences extreme emotional stress"
                ),
                "universe": "Marvel",
                "is_active": True,
                "is_villain": False,
            }

        ]

        created_count = 0
        for superhero_data in sample_superheroes:
            superhero, created = Superhero.objects.get_or_create(
                name=superhero_data["name"], defaults=superhero_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"Created superhero: {superhero.name}")
            else:
                self.stdout.write(f"Superhero already exists: {superhero.name}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully populated {created_count} new superheroes. "
                f"Total superheroes in database: {Superhero.objects.count()}"
            )
        )
