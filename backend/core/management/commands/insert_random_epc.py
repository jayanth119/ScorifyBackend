import uuid
import os
from django.core.management.base import BaseCommand
from core.models import Property
from epc.models import EPCReport
from faker import Faker
from django.conf import settings

class Command(BaseCommand):
    help = 'Insert sample EPC data'

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Retrieve existing properties
        properties = Property.objects.all()

        if not properties.exists():
            self.stdout.write(self.style.WARNING('No properties found in the database. Please create some properties first.'))
            return

        # Create EPC reports for each property
        for property in properties:
            for _ in range(3):  # Create 3 reports per property
                report = EPCReport.objects.create(
                    id=uuid.uuid4(),
                    property=property,
                    score=fake.random_element(elements=list("ABCDEFG")),
                    report_date=fake.date_between(start_date='-2y', end_date='today'),
                    report=fake.text(),
                    current_score=fake.random_element(elements=list("ABCDEFG")),
                    potential_score=fake.random_element(elements=list("ABCDEFG")),
                    document=self.create_sample_document(property.id)
                )
                self.stdout.write(self.style.SUCCESS(f'Created EPC Report for Property: {property.address} on {report.report_date}'))

    def create_sample_document(self, property_id):
        # Create a sample text file as the document
        file_name = f"sample_epc_report_{property_id}.txt"
        file_path = os.path.join(settings.MEDIA_ROOT, 'database', 'epc', str(property_id), file_name)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as f:
            f.write("This is a sample EPC report.")

        # Return a relative path to be stored in the database
        return os.path.join('database', 'epc', str(property_id), file_name)
