from django.db import models

class Tag(models.Model):
    """Model class for tags"""
    pass


class Feature(models.Model):
    """Model class for features"""
    pass

class Banner(models.Model):
    """Model class for banners"""

    def content_data():
        return {'title':"",'text':"",'url':""}
    
    tag = models.ManyToManyField(Tag,verbose_name="list_of_tags")
    feature = models.ForeignKey(Feature,on_delete=models.CASCADE)
    content = models.JSONField(default = content_data())
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
class User(models.Model):
    """Model class for users"""
    username = models.CharField(max_length=64,unique=True)
    use_last_revision = models.BooleanField(default=False)
    user_tag = models.ForeignKey(Tag,on_delete=models.CASCADE)
    