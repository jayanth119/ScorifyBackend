from django.core.management.base import BaseCommand
from regularmaintaince.models import Maintenance, Repair
from core.models import Property
from django.contrib.auth import get_user_model
from faker import Faker
import random

customUser = get_user_model()

class Command(BaseCommand):
    help = "Insert data into Maintenance and Repair models"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Fetch existing properties and users
        properties = list(Property.objects.all())
        users = list(customUser.objects.all())

        if not properties or not users:
            self.stdout.write(self.style.WARNING("Ensure you have properties and users in the database."))
            return

        # Create Maintenance records
        for _ in range(5):
            Maintenance.objects.create(
                user=random.choice(users),
                score=random.uniform(0, 10),
                details=fake.sentence(),
                completion_date=fake.date_this_year(),
                status=fake.word(),
                report=fake.text(),
                performed_by=fake.name(),
                history=fake.text(),
                due_date=fake.date_this_year(),
                title=fake.sentence(),
                description=fake.text()
            )

        # Create Repair records
        for _ in range(5):
            Repair.objects.create(
                user=random.choice(users),
                property=random.choice(properties),
                repair_score=random.uniform(0, 10),
                repair_history=fake.text(),
                completion_date=fake.date_this_year(),
                status=fake.word(),
                description=fake.text(),
                completion_report=fake.text(),
                cost=random.uniform(50, 5000),
                reported_by=fake.name()
            )

        self.stdout.write(self.style.SUCCESS("Successfully inserted data into Maintenance and Repair models."))
