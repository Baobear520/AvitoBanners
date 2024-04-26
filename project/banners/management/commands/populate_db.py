import random
from typing import Any
from faker import Faker
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone
from ...models import Tag, Feature, Banner


class Command(BaseCommand):
    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        # Create dummy tags
        for _ in range(999):
            Tag.objects.create()

        # Create dummy features
        for _ in range(999):
            Feature.objects.create()

        # Create dummy banners

        
        tag = Tag.objects.order_by('?').first()
        feature = Feature.objects.order_by('?').first()
        content = {
            'title': fake,
            'text': fake,
            'url': fake'
        }
        is_active = random.choice([True, False])
        created_at = timezone.now()
        updated_at = timezone.now()
        Banner.objects.bulk_create(
            objs=Banner,
            batch_size=2000,
            tag = tag, 
            feature = feature, 
            content=content, 
            is_active=is_active, 
            created_at=created_at, 
            updated_at=updated_at)

        self.stdout.write(self.style.SUCCESS('Database populated successfully'))