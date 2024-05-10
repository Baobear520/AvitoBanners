
from django.forms import ValidationError
from rest_framework import serializers
from banners.models import Banner,UserBanner,BannerTagFeature



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserBanner
        fields = ['id','use_last_revision','user_tag']

class BannerTagFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = BannerTagFeature
        fields = ['banner','feature','tag']
class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ['id','tags','feature','content','is_active','created_at','updated_at']
       
class BannerContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['content']