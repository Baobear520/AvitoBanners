import random
from faker import Faker
from django.core.management.base import BaseCommand, CommandParser
from django.utils import timezone
from ...models import BannerTagFeature, Feature,Banner,Tag


class Command(BaseCommand):
    help = 'Populate banners table'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            "--number",type=int,help="How many banners do you want to create?"
        )
    
    
    def handle(self, *args, **kwargs):
        # Create dummy features
        number = kwargs.get('number')

        #Validating user's input
        if not isinstance(number,int) or number <= 0:
            self.stdout.write(self.style.WARNING('Please provide a valid number of banners to create'))
            return
        
        fake = Faker()
        tags = Tag.objects.all()
        features = Feature.objects.all()
        #Checking if tags and features exist in the database
        if not tags and not features:
            self.stdout.write(self.style.ERROR("You must create tags and features before trying to create banners"))
            self.stdout.write(self.style.WARNING("First run |seed_tags --number number_of_tags| and |seed_features --number number_of_features|"))
        
        for _ in range(1,number+1):
            data = {
                'feature':random.choice(list(features)),
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
            
            # Limit the number of tags for a banner
            # Choose not more than 10 tags for a banner
            selected_tags = random.sample(list(tags), min(10, tags.count()))  
        
            #Creating intermediate bannertagfeature objects for each tag
            try: 
                for tag in selected_tags:
                    BannerTagFeature.objects.create(banner=banner, feature=data['feature'],tag=tag)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"There was an error while adding tags - {e}"))
                banner.delete()
                return
            
            self.stdout.write(self.style.SUCCESS(f"Banner {data['content']['title']} has been created"))       
        self.stdout.write(self.style.SUCCESS(f'{number} banner objects have been created successfully'))  
        
        
        