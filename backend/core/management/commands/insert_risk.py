from django.core.management.base import BaseCommand
from risk.models import SafetyAssessment, RiskAssessment  # Update import path if necessary
from core.models import Property
from faker import Faker
import random

class Command(BaseCommand):
    help = "Insert data into SafetyAssessment and RiskAssessment models"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Fetch existing properties
        properties = list(Property.objects.all())

        if not properties:
            self.stdout.write(self.style.WARNING("Ensure you have properties in the database."))
            return

        # Create SafetyAssessment records
        for _ in range(5):
            SafetyAssessment.objects.create(
                property=random.choice(properties),
                score=random.uniform(0, 10),
                electricity_condition=fake.sentence(),
                gas_condition=fake.sentence(),
                structural_integrity=fake.sentence(),
                mould_damp_condition=fake.sentence(),
                asbestos_condition=fake.sentence(),
                security_risk=fake.sentence(),
                report=fake.text()
            )

        # Create RiskAssessment records
        for _ in range(5):
            RiskAssessment.objects.create(
                property=random.choice(properties),
                document=fake.text(),
                date=fake.date_this_year(),
                document_type=fake.word(),
                title=fake.sentence(),
                expiry_date=fake.date_this_year()
            )

        self.stdout.write(self.style.SUCCESS("Successfully inserted data into SafetyAssessment and RiskAssessment models."))
