from django.core.management.base import BaseCommand
from mould.models import MouldHumidity, VentilationItem, VentilationImages
from core.models import Property
from django.contrib.auth import get_user_model
from faker import Faker
import random
import os

customUser = get_user_model()

class Command(BaseCommand):
    help = "Insert data into MouldHumidity, VentilationItem, and VentilationImages models"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Fetch existing properties and users
        properties = list(Property.objects.all())
        users = list(customUser.objects.all())

        if not properties or not users:
            self.stdout.write(self.style.WARNING("Ensure you have properties and users in the database."))
            return

        # Create MouldHumidity records
        for _ in range(5):
            MouldHumidity.objects.create(
                property=random.choice(properties),
                user=random.choice(users),
                avg_humidity_30_days=random.uniform(0, 100),
                ventilation_score=random.uniform(0, 10),
                condition=fake.sentence(),
                temperature=random.uniform(-30, 50),
                humidity=random.uniform(0, 100),
                mould_presence_90_days=fake.words(nb=5, ext_word_list=None),  # Simulate a JSON field
                previous_ventilation_date=fake.date_this_year(),
                next_ventilation_date=fake.date_this_year()
            )

        # Create VentilationItem records
        for _ in range(5):
            item = VentilationItem.objects.create(
                status=fake.word()
            )

            # Create VentilationImages records for each VentilationItem
            for _ in range(random.randint(1, 3)):
                VentilationImages.objects.create(
                    item=item,
                    image=fake.file_name(extension='jpg')  # Simulate an image file name
                )

        self.stdout.write(self.style.SUCCESS("Successfully inserted data into MouldHumidity, VentilationItem, and VentilationImages models."))
