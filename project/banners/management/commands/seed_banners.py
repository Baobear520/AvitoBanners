import random
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone
from ...models import Feature,Banner,Tag


class Command(BaseCommand):
    help = 'Populate banners table'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--number",type=int,help="How many banners do you want to create?"
        )
    
    
    def handle(self, *args, **kwargs):
        # Create dummy features
        number = kwargs.get('number')
        fake = Faker()
        tags = Tag.objects.all()
        features = Feature.objects.all()
        

        for _ in range(number):
            data = {
                'feature':random.choice(features),
                'content':{
                    'title': fake.sentence(),
                    'text': fake.text(),
                    'url': fake.url()
                    },
                'is_active':random.choices([True, False],weights=[5,1])[0],
                'created_at':timezone.now(),
                'updated_at':timezone.now()
                }
            banner = Banner.objects.create(**data)
            # Add random tags to the banner
            number_of_tags = random.randint(1, tags.count())  # Choose a random number of tags
            selected_tags = random.sample(list(tags), number_of_tags)  # Select random tags
            #Adding tags to the tag field
            for tag in selected_tags:
                banner.tag.add(tag)
            self.stdout.write(self.style.SUCCESS(f"Banner {data['content']['title']} has been created"))

        self.stdout.write(self.style.SUCCESS(f'{number} feature objects created successfully'))