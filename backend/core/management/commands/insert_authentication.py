from django.core.management.base import BaseCommand
from authentication.models import CustomUser
from faker import Faker
import random

class Command(BaseCommand):
    help = "Insert random data into CustomUser model using Faker"

    def handle(self, *args, **kwargs):
        fake = Faker()
        user_types = ['landlord', 'agent', 'tenant']

        for _ in range(10):  # Create 10 random users
            email = fake.email()
            user_type = random.choice(user_types)
            phone = fake.phone_number()
            occupation = fake.job()
            profile_photo = None  # Set this to None or a valid image path if needed

            # Create the user
            user = CustomUser.objects.create_user(
                email=email,
                password='password123',
                user_type=user_type,
                phone=phone,
                occupation=occupation,
                profile_photo=profile_photo,
            )

            self.stdout.write(self.style.SUCCESS(f'Successfully created user {user.email}'))

