from django.contrib.auth.models import Group, User
from rest_framework import serializers
from banners.models import Banner

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = ['id']


