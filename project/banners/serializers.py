from rest_framework import serializers
from banners.models import Banner,UserBanner,BannerTagFeature
from core.serializers import AdminAvitoUserSerializer, UserAvitoUserSerializer


class AdminProfileSerializer(serializers.ModelSerializer):
    user = AdminAvitoUserSerializer()
    class Meta:
        model = UserBanner
        fields = ['user','id','use_last_revision','user_tag']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserAvitoUserSerializer()
    class Meta:
        model = UserBanner
        fields = ['user','user_tag']

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id','tags','feature','content','is_active','created_at','updated_at']
       
class BannerTagFeatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = BannerTagFeature
        fields = ['tag','feature','banner']

class UpdateBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Banner
        fields = ['tags','feature','content','is_active']