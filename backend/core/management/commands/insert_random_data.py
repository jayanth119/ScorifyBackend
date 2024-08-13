import uuid
from django.core.management.base import BaseCommand
from faker import Faker
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
                start_date=fake.date(),
                end_date=fake.date(),
                deposit=fake.random_number(digits=4),
                details=fake.text(),
                next_inspection_date=fake.date(),
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

        # Create 20 Tenants
        for landlord in landlords:
            for _ in range(fake.random_int(min=1, max=3)):
                tenant = Tenant.objects.create(
                    id=uuid.uuid4(),
                    name=fake.name(),
                    phone=fake.phone_number(),
                    email=fake.email(),
                    current_tenancy_score=fake.random_number(digits=2),
                    landlord=landlord
                )
                tenant.properties.add(*fake.random_elements(elements=landlord.properties.all(), length=1))
                tenants.append(tenant)
                self.stdout.write(self.style.SUCCESS(f"Created Tenant: {tenant.name}"))

        # Create 20 Agents and associate them with landlords and tenants
        for _ in range(20):
            agent = Agent.objects.create(
                id=uuid.uuid4(),
                name=fake.name(),
                phone=fake.phone_number(),
                email=fake.email(),
                location=fake.address(),
                website=fake.url()
            )
            agents.append(agent)

            # Add landlords to the agent
            random_landlords = fake.random_elements(elements=landlords, length=fake.random_int(min=1, max=5))
            agent.landlords.add(*random_landlords)

            # Add tenants to the agent
            random_tenants = fake.random_elements(elements=tenants, length=fake.random_int(min=1, max=5))
            agent.tenants.add(*random_tenants)

            self.stdout.write(self.style.SUCCESS(f"Created Agent: {agent.name}"))
