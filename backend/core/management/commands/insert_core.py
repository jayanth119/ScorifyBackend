from django.core.management.base import BaseCommand
from core.models import Property, Management, LettingManagement, SalesManagement, PropertyTimeline, HousePhoto,Agent,Landlord,Tenant
from faker import Faker
import random
import uuid

class Command(BaseCommand):
    help = "Insert data into the core models excluding Agent, Landlord, and Tenant"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Create Properties
        properties = []
        for _ in range(10):
            property = Property.objects.create(
                address=fake.address(),
                house_name=fake.word(),
                zip_code=fake.zipcode(),
                bathroom_count=random.randint(1, 4),
                living_room_count=random.randint(1, 2),
                property_type=random.choice(['Apartment', 'House', 'Villa']),
                house_age=random.randint(1, 30),
                floor_map_photos=fake.text(),
                epc_status=random.choice(['Pass', 'Fail']),
                risk_assessment_percentage=random.uniform(0, 100),
                mould_ventilation_percentage=random.uniform(0, 100),
                gas_safety=random.choice([True, False]),
                heat_safety=random.choice([True, False]),
                start_date=fake.date_this_decade(),
                end_date=fake.date_this_decade(),
                deposit=random.uniform(500, 2000),
                details=fake.text(),
                next_inspection_date=fake.date_this_year(),
                open_repair_count=random.randint(0, 10),
                inspection_count=random.randint(0, 5),
                regular_maintenance=random.choice([True, False]),
                inventory_count=random.randint(0, 5),
            )
            properties.append(property)

        # Fetch existing agents
        agents = list(Agent.objects.all())
        if not agents:
            self.stdout.write(self.style.WARNING("No agents found. Please create agents before running this script."))
            return

        # Create Management records
        for _ in range(5):
            Management.objects.create(
                agent=random.choice(agents),
                property=random.choice(properties),
                details=fake.text(),
            )

        # Create LettingManagement records
        for _ in range(5):
            LettingManagement.objects.create(
                agent=random.choice(agents),
                tenant_property=random.choice(properties),
                landlord_property=random.choice(properties),
                details=fake.text(),
            )

        # Create SalesManagement records
        for _ in range(5):
            SalesManagement.objects.create(
                agent=random.choice(agents),
                landlord_property=random.choice(properties),
                details=fake.text(),
            )

        # Create PropertyTimeline records
        for _ in range(5):
            PropertyTimeline.objects.create(
                property=random.choice(properties),
                date=fake.date_this_year(),
                maintenance_repair_type=fake.word(),
                performed_by=fake.name(),
                details=fake.text(),
            )

        # Create HousePhoto records
        for _ in range(5):
            HousePhoto.objects.create(
                property=random.choice(properties),
                name=fake.word(),
                photo=fake.image_url(),
                photo_type=random.choice(['Floor Plan', 'Interior', 'Exterior']),
                uploaded_date=fake.date_this_year(),
            )

        self.stdout.write(self.style.SUCCESS("Successfully inserted data into Property, Management, LettingManagement, SalesManagement, PropertyTimeline, and HousePhoto models."))
