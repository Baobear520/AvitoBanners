import random

from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand, CommandParser
from ...models import Tag, UserBanner


class Command(BaseCommand):

    help = 'Populate users table'
    

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--number",type=int,help="How many users do you want to create?"
        )
    
    
    def handle(self, *args, **kwargs):
        # Create dummy features
        number = kwargs.get('number')
        fake = Faker()
        tags = Tag.objects.all()

        if not isinstance(number,int) or number <= 0:
            self.stdout.write(self.style.WARNING('Please provide a valid number of users to create'))
            return
        
        if not tags:
            self.stdout.write(self.style.ERROR("You must create tags before trying to create users"))
            self.stdout.write(self.style.WARNING("First run |seed_tags --number number_of_tags|"))

        try:
            for _ in range(number):
                data = {
                'username':fake.name(),
                'use_last_revision': random.choices([True,False],weights=[1,10])[0],
                'user_tag' :random.choice(tags)
            }
                UserBanner.objects.create(**data)
                self.stdout.write(self.style.SUCCESS(f"User {data['username']} has been created."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"There was an error while creating users - {e}"))
            return
        self.stdout.write(self.style.SUCCESS(f'{number} user objects created successfully'))

        
        