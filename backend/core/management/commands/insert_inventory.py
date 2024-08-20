from django.core.management.base import BaseCommand
from inventory_insception.models import Inventory, Room, Condition, Defect, AgentLandlord
from core.models import Property, Landlord, Agent
from faker import Faker
import random
import os
class Command(BaseCommand):
    help = "Insert data into the Inventory, Room, Condition, Defect, and AgentLandlord models"

    def handle(self, *args, **kwargs):
        fake = Faker()

        # Fetch existing properties, landlords, and agents
        properties = list(Property.objects.all())
        landlords = list(Landlord.objects.all())
        agents = list(Agent.objects.all())

        if not properties or not landlords or not agents:
            self.stdout.write(self.style.WARNING("Ensure you have properties, landlords, and agents in the database."))
            return

        # Create Inventory records
        for _ in range(5):
            inventory = Inventory.objects.create(
                property=random.choice(properties),
                document=fake.text(),
                score=random.uniform(0, 10),
                date=fake.date_this_year(),
                type=fake.word(),
                title=fake.sentence(),
                created_by=fake.name(),
                expiry_date=fake.date_this_year(),
                past_inventory=fake.boolean()
            )

            # Create Room records for each Inventory
            for _ in range(random.randint(1, 3)):
                room = Room.objects.create(
                    inventory=inventory,
                    name=fake.word(),
                    completion_percentage=random.uniform(0, 100)
                )

                # Create Condition records for each Room
                for _ in range(random.randint(1, 5)):
                    Condition.objects.create(
                        room=room,
                        item=fake.word(),
                        condition=random.choice(['good', 'fair', 'repair']),
                        cleanliness=random.choice(['good', 'fair', 'poor']),
                        photo=fake.file_name(extension='jpg')  # Simulate a photo file name
                    )

                # Create Defect records for each Room
                for _ in range(random.randint(0, 2)):  # Some rooms might not have defects
                    Defect.objects.create(
                        room=room,
                        description=fake.text()
                    )

        # Create AgentLandlord records
        for _ in range(5):
            AgentLandlord.objects.create(
                agent=random.choice(agents),
                landlord=random.choice(landlords)
            )

        self.stdout.write(self.style.SUCCESS("Successfully inserted data into Inventory, Room, Condition, Defect, and AgentLandlord models."))
