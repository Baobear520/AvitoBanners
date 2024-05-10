import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.utils import timezone
from ...models import BannerTagFeature, Feature, Banner, Tag

class Command(BaseCommand):
    help = 'Populate banners table'

    def add_arguments(self, parser):
        parser.add_argument("--number", type=int, help="How many banners do you want to create?")

    def handle(self, *args, **kwargs):
        number = kwargs.get('number')

        #Validating the input
        if not isinstance(number, int) or number <= 0:
            self.stdout.write(self.style.WARNING('Please provide a valid number of banners to create'))
            return
        
        fake = Faker()

        features = Feature.objects.all()
        tags = Tag.objects.all()

        #Checking if any tags and features exist in the database
        if not tags or not features:
            self.stdout.write(self.style.ERROR("You must create tags and features before trying to create banners"))
            self.stdout.write(self.style.WARNING("First run |seed_tags --number number_of_tags| and |seed_features --number number_of_features|"))
            return
        
        #Proceed
        created_banner_counter = 0
        for _ in range(1, number + 1):
            feature = random.choice(features)
            #Defining available tags (not in the DB) for the current feature
            tags_used = BannerTagFeature.objects.filter(feature=feature).values_list('tag', flat=True)
            list_of_tags_available = tags.exclude(id__in=tags_used)
            #Limiting the number of tags for the banner
            tags_limit = min(10, list_of_tags_available.count())

            #Checking if there are available tags to create a unique banner
            if tags_limit == 0:
                self.stdout.write(self.style.WARNING(f"For the current feature '{feature}', there are no available tags. Skipping banner creation."))
                continue
            
            #Selecting a random number of tags to the banner from the list of available tags
            selected_tags = random.sample(list(list_of_tags_available), random.randint(1, tags_limit))
            #Defining data
            content = {
                'title': fake.sentence(),
                'text': fake.text(),
                'url': fake.url()
            }
            is_active = random.choices([True, False], weights=[5, 1])[0]

            #Creating objects in the DB
            try:
                banner = Banner.objects.create(feature=feature, content=content, is_active=is_active, created_at=timezone.now(), updated_at=timezone.now())
                BannerTagFeature.objects.bulk_create([BannerTagFeature(banner=banner, feature=feature, tag=tag) for tag in selected_tags])
                created_banner_counter += 1
                self.stdout.write(self.style.SUCCESS(f"Banner '{content['title']}' has been created"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"There was an error while creating banner: {e}"))

        self.stdout.write(self.style.SUCCESS(f"{created_banner_counter} banner objects have been created successfully"))
