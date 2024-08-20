import uuid
from django.core.management.base import BaseCommand
from faker import Faker
from datetime import timedelta
from core.models import Landlord, Tenant, Agent, Property

class Command(BaseCommand):
    help = 'Insert random data into the database'

    def handle(self, *args, **kwargs):
        fake = Faker()

        landlords = []
        tenants = []
        properties = []
        agents = []

        # Create 20 Properties
        for _ in range(20):
            start_date = fake.date_between(start_date='-2y', end_date='today')
            end_date = start_date + timedelta(days=fake.random_int(min=1, max=365))

            property = Property.objects.create(
                id=uuid.uuid4(),
                address=fake.address(),
                house_name=fake.word(),
                zip_code=fake.zipcode(),
                bathroom_count=fake.random_int(min=1, max=5),
                living_room_count=fake.random_int(min=1, max=3),
                property_type=fake.random_element(elements=("House", "Apartment", "Condo")),
                house_age=fake.random_int(min=1, max=100),
                floor_map_photos=fake.text(),
                epc_status=fake.random_element(elements=("Valid", "Expired")),
                risk_assessment_percentage=fake.random_number(digits=2),
                mould_ventilation_percentage=fake.random_number(digits=2),
                gas_safety=fake.boolean(),
                heat_safety=fake.boolean(),
                start_date=start_date,
                end_date=end_date,
                deposit=fake.random_number(digits=4),
                details=fake.text(),
                next_inspection_date=fake.date_between(start_date=end_date, end_date='+1y'),
                open_repair_count=fake.random_int(min=0, max=10),
                inspection_count=fake.random_int(min=0, max=5),
                regular_maintenance=fake.boolean(),
                inventory_count=fake.random_int(min=0, max=5)
            )
            properties.append(property)
            self.stdout.write(self.style.SUCCESS(f"Created Property: {property.address}"))

        # Create 20 Landlords
        for _ in range(20):
            landlord = Landlord.objects.create(
                id=uuid.uuid4(),
                name=fake.name(),
                phone=fake.phone_number(),
                email=fake.email()
            )
            landlords.append(landlord)

            # Add properties to the landlord
            random_properties = fake.random_elements(elements=properties, length=fake.random_int(min=1, max=3))
            landlord.properties.add(*random_properties)

            self.stdout.write(self.style.SUCCESS(f"Created Landlord: {landlord.name}"))

        # More code here for tenants and agents...
