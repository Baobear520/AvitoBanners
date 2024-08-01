import random
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand, CommandParser
from django.db import transaction
from core.models import AvitoUser
from ...models import Tag, UserBanner
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):

    help = 'Populate Banners service users table'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--number", type=int, help="How many users do you want to create?"
        )

    def handle(self, *args, **kwargs):
        # Create dummy features
        number = kwargs.get('number')
        fake = Faker()
        tags = Tag.objects.all()

        if not isinstance(number, int) or number <= 0:
            self.stdout.write(self.style.WARNING('Please provide a valid number of users to create'))
            return

        if not tags:
            self.stdout.write(self.style.ERROR("You must create tags before trying to create users"))
            self.stdout.write(self.style.WARNING("First run |seed_tags --number number_of_tags|"))
            return

        try:
            with transaction.atomic():
                for _ in range(number):
                    avito_user_data = {
                        'password': make_password(fake.password()),  
                        'username': fake.user_name().strip(" "),
                        'is_superuser': False,
                        'is_staff': random.choices([True, False], weights=[1, 10])[0],
                        'email': fake.email(),
                        'is_active': True
                    }
                    user_banner_data = {
                        'use_last_revision': avito_user_data['is_staff'],
                        'user_tag': random.choice(tags)
                    }
                    avito_user = AvitoUser.objects.create(**avito_user_data)
                    self.stdout.write(self.style.SUCCESS(f"User {avito_user_data['username']} has been created."))

                    UserBanner.objects.create(user=avito_user, **user_banner_data)
                    self.stdout.write(self.style.SUCCESS(f"Banner user profile for {avito_user_data['username']} has been created."))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"There was an error while creating users - {e}"))
            return
        self.stdout.write(self.style.SUCCESS(f'{number} user objects created successfully'))
