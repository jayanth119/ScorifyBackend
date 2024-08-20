from django.core.management.base import BaseCommand
from gasandheat.models import GasSafety, HeatingSafety
from core.models import Property
from faker import Faker
import random
import os

class Command(BaseCommand):
    help = "Insert data into the GasSafety and HeatingSafety models"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Fetch existing properties
        properties = list(Property.objects.all())
        if not properties:
            self.stdout.write(self.style.WARNING("No properties found. Please create properties before running this script."))
            return

        # Create GasSafety records
        for _ in range(5):
            GasSafety.objects.create(
                property=random.choice(properties),
                repair_score=random.uniform(0, 10),
                report_date=fake.date_this_year(),
                due_date=fake.date_this_year(),
                expiry_months=random.randint(1, 12),
                current_eer=random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
                potential_eer=random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
                document=fake.file_name(extension='pdf')  # Simulate a file name for the document
            )

        # Create HeatingSafety records
        for _ in range(5):
            HeatingSafety.objects.create(
                property=random.choice(properties),
                repair_score=random.uniform(0, 10),
                boiler_condition=fake.word(),
                controller=fake.word(),
                radiators_condition=fake.word(),
                flue_ventilation_condition=fake.word()
            )

        self.stdout.write(self.style.SUCCESS("Successfully inserted data into the GasSafety and HeatingSafety models."))
