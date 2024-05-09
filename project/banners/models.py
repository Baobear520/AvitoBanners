from django.db import models
from django.contrib.auth.models import User as BaseUser
from django.forms import ValidationError
class Tag(models.Model):
    """Model class for tags"""
    pass


class Feature(models.Model):
    """Model class for features"""
    pass


class Banner(models.Model):
    """Model class for banners"""

    tags = models.ManyToManyField(Tag,through='BannerTagFeature')
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE,related_name='banners')
    content = models.JSONField(default=dict)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BannerTagFeature(models.Model):
    """Intermediate model to enforce the unique constraint for a tag and a feature"""
    
    tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    banner = models.ForeignKey(Banner, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tag','banner','feature'], 
                name='unique_banner',
                violation_error_message="A banner must have a unique tag and feature"
                )
        ]

class UserBanner(BaseUser):
    """Model class for users"""
    
    use_last_revision = models.BooleanField(default=False)
    user_tag = models.ForeignKey(Tag,on_delete=models.CASCADE,verbose_name='tag_id')
    