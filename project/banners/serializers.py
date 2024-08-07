from rest_framework import serializers
from banners.models import Banner,UserBanner,BannerTagFeature
from core.serializers import AdminAvitoUserSerializer, UserAvitoUserSerializer


class AdminProfileSerializer(serializers.ModelSerializer):
    user = AdminAvitoUserSerializer()
    class Meta:
        model = UserBanner
        fields = ['user','id','use_last_revision','user_tag']
    
    def update(self, instance, validated_data):
        # Update fields on the instance
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = AdminAvitoUserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Update other fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserAvitoUserSerializer()
    class Meta:
        model = UserBanner
        fields = ['user','user_tag']

    def update(self, instance, validated_data):
        # Update fields on the instance
        user_data = validated_data.pop('user', None)
        if user_data:
            user_serializer = UserAvitoUserSerializer(instance.user, data=user_data, partial=True)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Update other fields on the instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

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