import random
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone
from ...models import Tag

#python manage.py your_module_name --flag arg
class Command(BaseCommand):
    help = 'Populate tags table'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--number",type=int,help="How many tags do you want to create?"
        )
    
    
    def handle(self, *args, **kwargs):
        # Create dummy tags
        number = kwargs.get('number')
        for _ in range(number):
            Tag.objects.create()

        self.stdout.write(self.style.SUCCESS(f'{number} tag objects created successfully'))