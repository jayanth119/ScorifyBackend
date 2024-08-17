
import os
import random
import uuid
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
from django.conf import settings
from core.models import Property
from gasandheat.models  import GasSafety

class Command(BaseCommand):
    help = 'Add 3 Gas Safety reports for each property for testing purposes'

    def handle(self, *args, **kwargs):
        fake = Faker()
        properties = Property.objects.all()

        if not properties.exists():
            self.stdout.write(self.style.WARNING('No properties found in the database.'))
            return

        for property in properties:
            for i in range(3):  # Add 3 reports per property
                report_date = timezone.now().date() - timedelta(days=random.randint(30, 365 * 2))
                due_date = report_date + timedelta(days=random.randint(30, 365))
                expiry_months = (due_date.year - timezone.now().date().year) * 12 + due_date.month - timezone.now().date().month

                document = self.create_sample_document(property.id, f'report_{i + 1}.txt')

                GasSafety.objects.create(
                    id=uuid.uuid4(),
                    property=property,
                    repair_score=random.uniform(50, 100),  # Random repair score between 50 and 100
                    report_date=report_date,
                    due_date=due_date,
                    expiry_months=expiry_months,
                    current_eer=random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
                    potential_eer=random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
                    document=document
                )

            self.stdout.write(self.style.SUCCESS(f'Added 3 Gas Safety reports for property ID: {property.id}'))

    def create_sample_document(self, property_id, filename):
        # Create a sample text file as the document
        file_path = os.path.join(settings.MEDIA_ROOT, 'gassafety', str(property_id), filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write("This is a sample Gas Safety report.")

        # Return a relative path to be stored in the database
        return os.path.join('gassafety', str(property_id), filename)

