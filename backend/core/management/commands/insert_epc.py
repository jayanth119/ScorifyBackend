from django.core.management.base import BaseCommand
from epc.models import EPCReport
from core.models import Property
from faker import Faker
import random

class Command(BaseCommand):
    help = "Insert data into the EPCReport model"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Fetch existing properties
        properties = list(Property.objects.all())
        if not properties:
            self.stdout.write(self.style.WARNING("No properties found. Please create properties before running this script."))
            return

        # Create EPCReports
        for _ in range(5):
            EPCReport.objects.create(
                property=random.choice(properties),
                score=random.uniform(0, 100),
                report_date=fake.date_this_year(),
                report=fake.text(),
                current_score=random.uniform(0, 100),
                potential_score=random.uniform(0, 100),
                document=fake.file_name(extension='pdf')  # Simulate a file name for the document
            )

        self.stdout.write(self.style.SUCCESS("Successfully inserted data into the EPCReport model."))
