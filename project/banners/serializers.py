
from django.forms import ValidationError
from rest_framework import serializers
from banners.models import Banner,UserBanner,BannerTagFeature



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBanner
        fields = ['id','use_last_revision','user_tag']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id','tags','feature','content','is_active','created_at','updated_at']
       
class BannerTagFeatureSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='banner.content.title')
    text = serializers.CharField(source='banner.content.text')
    url = serializers.URLField(source='banner.content.url')
    class Meta:
        model = BannerTagFeature
        fields = ['title','text','url']