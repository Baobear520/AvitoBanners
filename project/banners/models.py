from django.db import models

class Tag(models.Model):
    """Model class for tags"""
    pass


class Feature(models.Model):
    """Model class for features"""
    pass

class Banner(models.Model):
    """Model class for banners"""

    tag_id = models.ManyToManyField(
        Tag,
        max_length=5,
        unique=True,
        verbose_name="list_of_tags"
    )
    feature_id = models.ForeignKey(
        Feature,
        on_delete=models.CASCADE,
        max_length=5,
        unique=True
    )
    content = models.JSONField(

    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()




class User(models.Model):
    """Model class for users"""
    use_last_revision = models.BooleanField(default=False)
    tag_id = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        unique=True
    )
    