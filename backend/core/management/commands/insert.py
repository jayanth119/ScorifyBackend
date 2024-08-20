from django.core.management.base import BaseCommand
from django.db import transaction
from core.models import Property, Tenant, Landlord, Agent
from authentication.models import CustomUser
from epc.models import EPCReport
from gasandheat.models import GasSafety, HeatingSafety
from mould.models import MouldHumidity
from regularmaintaince.models import Maintenance
from faker import Faker
import random

fake = Faker()

class Command(BaseCommand):
    help = 'Insert random data into the database including properties and related reports'

    def handle(self, *args, **kwargs):
        with transaction.atomic():
            try:
                for _ in range(10):
                    # Create unique users for landlords, tenants, and agents
                    landlord_user = CustomUser.objects.create_user(
                        email=fake.unique.email(),
                        password=fake.password(length=12),
                        user_type='landlord'
                    )
                    self.stdout.write(self.style.SUCCESS('1'))

                    landlord = Landlord.objects.create(
                        user=landlord_user,
                        name=fake.name(),
                        phone=fake.phone_number(),
                        email=landlord_user.email,
                    )
                    self.stdout.write(self.style.SUCCESS('2'))

                    tenant_user = CustomUser.objects.create_user(
                        email=fake.unique.email(),
                        password=fake.password(length=12),
                        user_type='tenant'
                    )
                    self.stdout.write(self.style.SUCCESS('3'))
                   
                    tenant = Tenant.objects.create(
                        user=tenant_user,
                        name=fake.name(),
                        phone=fake.phone_number(),
                        email=tenant_user.email,
                        occupation=fake.job(),
                        is_verified=fake.boolean(),
                    )
                    self.stdout.write(self.style.SUCCESS('4'))

                    agent_user = CustomUser.objects.create_user(
                        email=fake.unique.email(),
                        password=fake.password(length=12),
                        user_type='agent'
                    )
                    self.stdout.write(self.style.SUCCESS('5'))

                    agent = Agent.objects.create(
                        user=agent_user,
                        name=fake.name(),
                        phone=fake.phone_number(),
                        email=agent_user.email,
                        location=fake.city(),
                        website=fake.url(),
                    )
                    self.stdout.write(self.style.SUCCESS('6'))

                    # Create properties and associate them with landlords and tenants
                    for i in range(1):
                        prop = Property.objects.create(
                            address=fake.address(),
                            house_name=fake.word(),
                            zip_code=fake.zipcode(),
                            bathroom_count=random.randint(1, 5),
                            living_room_count=random.randint(1, 3),
                            property_type=random.choice(['Apartment', 'House', 'Condo']),
                            house_age=random.randint(1, 100),
                            floor_map_photos=fake.text(),
                            epc_status=random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
                            risk_assessment_percentage=random.uniform(0, 100),
                            mould_ventilation_percentage=random.uniform(0, 100),
                            gas_safety=fake.boolean(),
                            heat_safety=fake.boolean(),
                            start_date=fake.date_this_decade(),
                            end_date=fake.date_this_decade(),
                            deposit=random.uniform(500, 5000),
                            details=fake.text(),
                            next_inspection_date=fake.date_this_year(),
                            open_repair_count=random.randint(0, 5),
                            inspection_count=random.randint(0, 10),
                            regular_maintenance=fake.boolean(),
                            inventory_count=random.randint(0, 10),
                        )
                        prop.landlords.add(landlord)
                        prop.tenants.add(tenant)
                        self.stdout.write(self.style.SUCCESS('7'))

                        EPCReport.objects.create(
                            property=prop,
                            score=random.uniform(50, 100),
                            report_date=fake.past_date(),
                            report=fake.text(),
                            current_score=random.uniform(50, 100),
                            potential_score=random.uniform(50, 100)
                        )
                        self.stdout.write(self.style.SUCCESS('8'))
                   
                        GasSafety.objects.create(
                            property=prop,
                            repair_score=random.uniform(50, 100),
                            report_date=fake.past_date(),
                            due_date=fake.future_date(),
                            expiry_months=random.randint(12, 60),
                            current_eer=random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G']),
                            potential_eer=random.choice(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
                        )
                        HeatingSafety.objects.create(
                            property=prop,
                            repair_score=random.uniform(50, 100),
                            boiler_condition=fake.word(),
                            controller=fake.word(),
                            radiators_condition=fake.word(),
                            flue_ventilation_condition=fake.word()
                        )
                        MouldHumidity.objects.create(
                            property=prop,
                            avg_humidity_30_days=random.uniform(20, 80),
                            ventilation_score=random.uniform(1, 10),
                            condition=fake.word(),
                            temperature=random.uniform(10, 30),
                            humidity=random.uniform(30, 70),
                            mould_presence_90_days=fake.json(),
                            previous_ventilation_date=fake.past_date(),
                            next_ventilation_date=fake.future_date()
                        )
                        
                        Maintenance.objects.create(
                            user=landlord_user,
                            score=random.uniform(1, 10),
                            details=fake.text(),
                            completion_date=fake.future_date(),
                            status=fake.word(),
                            report=fake.text(),
                            performed_by=fake.name(),
                            history=fake.text(),
                            due_date=fake.future_date(),
                            title=fake.word(),
                            description=fake.text(),
                            upcoming_photo=None
                        )

                self.stdout.write(self.style.SUCCESS('Successfully inserted records for properties and all associated data, including landlords, tenants, and agents.'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error inserting data: {e}'))
